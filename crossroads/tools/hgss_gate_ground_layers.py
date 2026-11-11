"""Narrow gate layering correction; no game outputs or art redesign.

Call after the existing gate generator packs its historical artwork. `pack`
must append/deduplicate glyphs without rewriting any existing glyph. This helper
changes metatile layer references in place, preserves ALL existing attributes,
and appends four north-plant variants because their four wall crops differ.

The returned raw_changes are the ONLY map-word changes required: the four north
plant cells. Existing floor/lower-plant/void IDs stay stable. A caller applies
those exact cell changes as an independent, immutable rendering-fix contract.
Private palette8 index1 must be opaque RGB(0,0,0); index0 remains transparent.
No existing game generator/validator/resource is imported or mutated on import.
"""
from PIL import Image

BLACK_BANK=8
BLACK_INDEX=1
BLANK=0x6200

def apply_layer_fixes(words,attrs,placements,pack,art):
    """Fix flat floor/void/plant layers, append north variants, return details.

    words: mutable flat list of eight u16 references per secondary metatile.
    attrs: mutable u16 attribute list, indexed by metatileID-512.
    placements: existing generator records including x,y,kind,metatile,after.
    pack: pack(indexed8x8, palette_bank) -> tile reference, append-only.
    art: existing opaque `floor`, opaque160x32 `wall`, transparent16x32 `plant`.

    The function intentionally leaves placement records unchanged, allowing the
    caller to verify the original authoring contract before applying raw_changes.
    """
    assert len(words)==len(attrs)*8
    old_words=words.copy();old_attrs=attrs.copy();old_count=len(attrs)
    by_kind={kind:[p for p in placements if p['kind']==kind]
             for kind in ('floor','void','plant')}
    assert by_kind['floor'] and len(by_kind['plant'])==8
    assert not any(v==0 for v in art['floor'].tobytes())
    assert not any(v==0 for v in art['wall'].tobytes())

    def refs(im,bank=7):
        assert im.size==(16,16)
        return [pack(im.crop((x,y,x+8,y+8)),bank)
                for x,y in ((0,0),(8,0),(0,8),(8,8))]
    floor=refs(art['floor'])
    fix_ids=set()
    # NORMAL0 floor937 used to be fully opaque on the foreground layer and
    # hid Joe at2/10,9. All flat floor variants now have the same ground-only
    # placement, including the six warp aliases and boundary-floor variants.
    for p in by_kind['floor']:
        n=p['metatile'];k=(n-512)*8
        words[k:k+8]=floor+[BLANK]*4;fix_ids.add(n)

    # Replacement pole-top void904 is transparent on BOTH layers while its
    # NORMAL0 attribute exposes the primary debug backdrop (e.g.0x3014).
    # Inherited512 uses COVERED1 and already composes as intended black.
    black=Image.new('P',(8,8),BLACK_INDEX)
    black_word=pack(black,BLACK_BANK)
    for n in {p['metatile']for p in by_kind['void']}:
        k=(n-512)*8;words[k:k+8]=[black_word]*4+[BLANK]*4;fix_ids.add(n)

    # The existing plant top/base IDs are shared by north and south corners.
    # Preserve them as the lower plants, with fully opaque floor behind their
    # original transparent leaves/pot overlay. This retains canopy overlap.
    plant_ids={p['metatile']for p in by_kind['plant']}
    for n in plant_ids:
        k=(n-512)*8
        assert words[k+4:k+8]==old_words[k+4:k+8]
        words[k:k+4]=floor;fix_ids.add(n)

    # Northplants occupy four different window/wall background crops. Their
    # previous shared906/915 IDs cannot encode those backgrounds independently.
    # Four append-only variants are therefore necessary; no IDs are reassigned.
    raw=[];appended=[];north_backgrounds=[]
    for p in sorted((p for p in by_kind['plant']if p['y']in(2,3)),key=lambda p:(p['y'],p['x'])):
        x,y=p['x'],p['y'];assert x in(2,10)
        dx,dy=x-1,y-2
        im=art['wall'].crop((dx*16,dy*16,dx*16+16,dy*16+16))
        under=refs(im);old=p['metatile'];k=(old-512)*8
        new=512+len(attrs);words.extend(under+old_words[k+4:k+8]);attrs.append(old_attrs[old-512])
        before=p['after'];assert before&1023==old
        raw.append(dict(x=x,y=y,before=before,after=(before&0xfc00)|new))
        appended.append(new);north_backgrounds.append(dict(x=x,y=y,source_wall_tile=[dx,dy],metatile=new))
    assert len(raw)==4 and len({(p['x'],p['y'])for p in raw})==4
    assert len(attrs)<=512
    assert attrs[:old_count]==old_attrs,'Existing gate attributes changed'
    for i in range(old_count):
        if i+512 not in fix_ids:
            assert words[i*8:i*8+8]==old_words[i*8:i*8+8],'Unrelated gate art changed'
    return dict(raw_changes=raw,render_fix_metatile_ids=sorted(fix_ids),
                appended_metatile_ids=appended,north_plant_underlays=north_backgrounds,
                black_palette_bank=BLACK_BANK,black_palette_index=BLACK_INDEX,
                black_glyph_word=black_word,
                preserved_existing_attribute_count=old_count,
                source_note='Flat floors and black void on opaque ground; original plant overlays over opaque corresponding floor/wall. Counter/side/wall drawings are already opaque and remain unchanged.')
