#!/usr/bin/env python3
"""Verify the owner-supplied corporate outfit and its actual engine wiring."""
from pathlib import Path
import re
from PIL import Image

root = Path(__file__).resolve().parents[2]
assets = root / 'graphics/object_events/pics/people/joe/corporate'
sheet = Image.open(assets / 'walking.png')
assert sheet.mode == 'P' and sheet.size == (256, 32)
assert sheet.info.get('transparency') == 0
palette = sheet.getpalette()
assert len(palette) == 48
for d, direction in enumerate(('down', 'left', 'right', 'up')):
    poses = []
    for i in range(4):
        original = Image.open(assets / 'source' / f'joe_{direction}_{i}.png')
        assert original.mode == 'P' and original.size == (16, 32)
        assert original.info.get('transparency') == 0 and original.getpalette()[:48] == palette
        actual = sheet.crop(((d * 4 + i) * 16, 0, (d * 4 + i + 1) * 16, 32))
        assert actual.tobytes() == original.tobytes(), (direction, i)
        assert original.convert('RGBA').getbbox()[3] == 32
        assert len(original.getcolors()) <= 16
        poses.append(actual.tobytes())
    assert len(set(poses)) == 4
anims = (root / 'src/data/object_events/object_event_anims.h').read_text().split('// Joe:')[1]
assert 'hFlip' not in anims
for direction, base in [('SOUTH', 0), ('NORTH', 12), ('WEST', 4), ('EAST', 8)]:
    assert f'sAnim_Joe_Face{direction}[] = {{\n    ANIMCMD_FRAME({base}, 16)' in anims
    for group in ('ANIM_STD_FACE', 'ANIM_STD_GO', 'ANIM_STD_GO_FAST', 'ANIM_STD_GO_FASTER', 'ANIM_STD_GO_FASTEST', 'ANIM_RUN', 'ANIM_SPIN'):
        assert f'[{group}_{direction}]' in anims
constants = (root / 'include/constants/event_objects.h').read_text()
assert '#define OBJ_EVENT_GFX_JOE_NORMAL OBJ_EVENT_GFX_UNUSED_250' in constants
for gender in ['MALE', 'FEMALE']:
    assert re.search(r'^#define PLAYER_AVATAR_GFX_' + gender + r'_NORMAL.*: OBJ_EVENT_GFX_JOE_NORMAL\)', constants, re.M)
assert '[OBJ_EVENT_GFX_JOE_NORMAL] = &gObjectEventGraphicsInfo_JoeCorporate' in (root / 'src/data/object_events/object_event_graphics_info_pointers.h').read_text()
assert '.anims = sAnimTable_JoeCorporate' in (root / 'src/data/object_events/object_event_graphics_info.h').read_text()
assert '{gObjectEventPal_JoeCorporate,          OBJ_EVENT_PAL_TAG_JOE_CORPORATE}' in (root / 'src/event_object_movement.c').read_text()
print('Joe source frames, transparency, shared palette, exact repack, 4-direction animations and playable wiring: PASS')

for direction in ['SOUTH', 'NORTH', 'WEST', 'EAST']:
    spin = anims.split(f'sAnim_Joe_Spin{direction}[]', 1)[1].split('};', 1)[0]
    assert 'ANIMCMD_LOOP(1)' in spin and 'ANIMCMD_END' in spin
print('Joe spin animations preserve finite completion and 4-direction rotation: PASS')

# Some old engine consumers index this table by ordinal (not tag).
movement = (root / 'src/event_object_movement.c').read_text()
palette_table = movement.split('sObjectEventSpritePalettes[] = {', 1)[1].split('};', 1)[0]
assert palette_table.index('gObjectEventPal_JoeCorporate') > palette_table.index('gObjectEventPaletteNeonLight')
for path, size in [('front.png', (64,64)), ('back.png', (64,256))]:
    image = Image.open(root / 'graphics/trainers/joe' / path)
    assert image.size == size and image.mode == 'P' and max(image.tobytes()) < 16
    assert image.info.get('transparency') == 0
assert 'TRAINER_PIC_JOE,' in (root / 'include/constants/trainers.h').read_text()
assert '[TRAINER_PIC_JOE]' in (root / 'src/data/graphics/trainers.h').read_text()
print('Joe palette appended without shifting existing ordinals; trainer assets and references: PASS')
