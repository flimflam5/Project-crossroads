#!/usr/bin/env python3
"""Exercise the actual solution check with a native isolated sprite fixture.

This verifies the empty-slot sentinel against cursor contents, missing/extra
pieces, wrong positions and rotations. It does not emulate the puzzle screen.
"""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'src/sliding_puzzle.c').read_text()
signature = 'static void CheckForSolution(void)\n{'
start = source.index(signature)
open_brace = source.index('{', start)
depth = 0
for pos in range(open_brace, len(source)):
    if source[pos] == '{':
        depth += 1
    elif source[pos] == '}':
        depth -= 1
        if not depth:
            function = source[start:pos + 1]
            break
else:
    raise AssertionError('Unterminated puzzle solution function')

prefix = r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
typedef uint8_t u8;
#define TRUE 1
#define FALSE 0
#define __ 0
#define NUM_SLIDING_PUZZLE_ROWS 4
#define NUM_SLIDING_PUZZLE_COLS 6
#define SLIDING_PUZZLE_SOLVED 0
#define ORIENTATION_0 0
#define sTileId data[4]
#define sOrientation data[5]
struct Sprite { uint16_t data[8]; } gSprites[64];
struct Puzzle { u8 tiles[4][6]; u8 solved; } puzzle, *sSlidingPuzzle = &puzzle;
static const u8 sPuzzleLayouts[1][4][6] = {{{0,1,2,3,4,0},{0,5,6,7,8,0},
                                            {0,9,10,11,12,0},{0,13,14,15,16,0}}};
'''
suffix = r'''
static void valid(void) {
    memset(&puzzle, 0, sizeof(puzzle)); memset(gSprites, 0, sizeof(gSprites));
    for (u8 r=0; r<4; r++) for (u8 c=1; c<5; c++) {
        u8 id = sPuzzleLayouts[0][r][c]; puzzle.tiles[r][c] = id;
        gSprites[id].sTileId = id; gSprites[id].sOrientation = ORIENTATION_0;
    }
    // Sprite zero is the cursor, not an empty tile. Its data must be irrelevant.
    gSprites[0].sTileId = 99; gSprites[0].sOrientation = 2;
}
int main(void) {
    valid(); CheckForSolution(); assert(puzzle.solved);
    valid(); puzzle.tiles[0][1] = 0; CheckForSolution(); assert(!puzzle.solved);
    valid(); puzzle.tiles[0][0] = 17; gSprites[17].sTileId = 1;
    CheckForSolution(); assert(!puzzle.solved);
    valid(); gSprites[1].sOrientation = 1; CheckForSolution(); assert(!puzzle.solved);
    valid(); puzzle.tiles[0][1] = 2; CheckForSolution(); assert(!puzzle.solved);
    return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='black-ledger-puzzle-test-') as temp:
    temp = Path(temp)
    (temp / 'test.c').write_text(prefix + '\n' + function + '\n' + suffix)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Werror', str(temp / 'test.c'),
                    '-o', str(temp / 'test')], check=True)
    subprocess.run([str(temp / 'test')], check=True)
print('PASS: actual puzzle solution function handles cursor data, solved board, '
      'missing/extra pieces, wrong rotation and wrong position. No emulator claim.')
