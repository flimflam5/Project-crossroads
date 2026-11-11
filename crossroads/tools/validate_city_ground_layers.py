#!/usr/bin/env python3
"""Independent visible-ground/garbage-layer check for the complete city scope.

NORMAL metatiles put their top art above Joe and inject BG3 tile0x3014.
Matching a renderer that reproduces magenta garbage is not a quality test.
This check rejects that actual composed color and empty public ground below
foreground artwork. Intentional roof/canopy overlays retain their ground layer.
"""
import argparse,functools,json,re,struct
from pathlib import Path
from PIL import Image
from validate_city_graphics_limits import R,load,headers,meta_source,graphic_source,resource
graphic_source += '\n'+(R/'src/graphics.c').read_text()

@functools.lru_cache(None)
def side(symbol):
    body=re.search(r'const struct Tileset\s+'+re.escape(symbol)+r'\s*=\s*\{(.*?)\};',headers,re.S)[1]
    attr=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)[1]
    tile=re.search(r'\.tiles\s*=\s*(\w+)',body)[1]
    pal=re.search(r'\.palettes\s*=\s*(\w+)',body)[1]
    ap=re.search(re.escape(attr)+r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"',meta_source)[1]
    tp=re.search(re.escape(tile)+r'\[\]\s*=\s*INCGFX_U32\("([^"]+)"',graphic_source)[1]
    match=re.search(re.escape(pal)+r'\s*\[\s*\]\s*\[\s*16\s*\]\s*=\s*\{(.*?)\};',graphic_source,re.S)
    assert match,(symbol,'Actual palette definition unresolved',pal)
    pbody=match[1]
    pp=re.findall(r'INCGFX_U16\("([^"]+\.pal)"',pbody);assert len(pp)==16,(symbol,'Actual palette alias unresolved')
    b=(R/ap).read_bytes();attrs=struct.unpack('<'+str(len(b)//2)+'H',b)
    pals=[tuple(tuple(int(c)//8 for c in row.split())for row in (R/p).read_text().splitlines()[3:])for p in pp]
    return resource(symbol),attrs,Image.open(R/tp),pals

def validate(frames=(),report_path=None):
    names={r['map']for r in load('crossroads/hgss/ecruteak-qa09-building-checklist.json')['maps']}
    names|={p.parent.name for p in (R/'data/maps').glob('OlivineCity*/map.json')};assert len(names)==51
    layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};failures=[];checked=0
    for name in sorted(names):
        m=load(f'data/maps/{name}/map.json');l=layouts[m['layout']];p,s=[side(l[k])for k in ['primary_tileset','secondary_tileset']]
        @functools.lru_cache(None)
        def glyph(word):
            n=word&1023;im=[p,s][n>=512][2];i=n%512
            tile=im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
            if word&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if word&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            bank=word>>12;pal=[p,s][bank>=6][3][bank]
            return tuple(pal[c]if c else None for c in tile.tobytes())
        @functools.lru_cache(None)
        def metatile(n):
            pool=[p,s][n>=512];refs=pool[0][n%512*8:n%512*8+8];layer=pool[1][n%512]>>12
            bottom=sum((glyph(v)for v in refs[:4]),());top=sum((glyph(v)for v in refs[4:]),())
            backdrop=p[3][0][0];fallback=glyph(0x3014)*4 if layer==0 else (backdrop,)*256
            visible=tuple(t if t is not None else b if b is not None else f if f is not None else backdrop for b,t,f in zip(bottom,top,fallback))
            return layer,sum(c is not None for c in bottom),sum(c is not None for c in top),visible.count((31,0,31))
        for kind,path in [('map',l['blockdata_filepath']),('border',l['border_filepath'])]:
            b=(R/path).read_bytes();width=l['width']if kind=='map'else 2
            for i,word in enumerate(struct.unpack('<'+str(len(b)//2)+'H',b)):
                n=word&1023;layer,bottom,top,magenta=metatile(n);checked+=1
                issues=[]
                if layer not in(0,1,2):issues.append('unsupported engine metatile layer type')
                if magenta:issues.append('visible debug magenta')
                if kind=='map'and not word&0xc00 and word>>12 in(1,3)and layer in(0,2)and bottom==0 and top:issues.append('public ground missing below foreground art')
                if issues:failures.append(dict(map=name,kind=kind,x=i%width,y=i//width,word=hex(word),layer=layer,bottom_opaque_pixels=bottom,top_opaque_pixels=top,magenta_pixels=magenta,issues=issues))
    frame_reports=[]
    for path in frames:
        im=Image.open(path).convert('RGB');assert im.size==(240,160),(path,'Native framebuffer required')
        count=sum(c==(255,0,255)for c in im.getdata());frame_reports.append(dict(path=str(path),magenta_pixels=count));assert count==0,(path,'Actual framebuffer contains debug magenta',count)
    report=dict(maps=len(names),checked_cells=checked,failures=failures,native_frames=frame_reports)
    if report_path:Path(report_path).write_text(json.dumps(report,indent=2)+'\n')
    if failures:print(json.dumps(failures[:60],indent=2))
    assert not failures,('City ground/layer quality failures',len(failures))
    print('Actual NORMAL/SPLIT ground and all51-map composed debug-magenta rejection: PASS',checked,'cells;',len(frames),'native frames')
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--frames',nargs='*',default=[]);p.add_argument('--report');a=p.parse_args();validate(a.frames,a.report)
