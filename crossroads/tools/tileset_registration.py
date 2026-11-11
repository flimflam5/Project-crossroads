"""Safe generated sections, including externs inside the tilesets include guard.

Registration must not use the last ``#endif``: generated blocks contain their own
conditions. Likewise, replacing an outer block must never delete another
generator's complete nested section. Such historical children become siblings
immediately after the replaced block, retaining their own condition and bytes.
"""
import re

TILESETS_GUARD_END = '#endif //GUARD_tilesets_H'
MARKER = re.compile(r'^// (BEGIN|END) (.+)$', re.M)


def _foreign_sections(body):
    stack = []
    sections = []
    for marker in MARKER.finditer(body):
        action, name = marker.groups()
        if action == 'BEGIN':
            stack.append((name, marker.start()))
        else:
            assert stack and stack[-1][0] == name, ('Unbalanced generated section', name)
            _, start = stack.pop()
            if not stack:
                sections.append(body[start:marker.end()])
    assert not stack, ('Unclosed generated section', stack)
    return sections


def upsert(text, begin, end, section, *, externs=False):
    """Replace the owned marked block or insert at the exact include boundary.

    Existing sections retain their location. This function performs no writes;
    callers' existing assertion-only ``--check`` paths remain effective.
    """
    assert section.startswith(begin + '\n') and section.endswith(end)
    assert text.count(begin) <= 1 and text.count(end) <= 1, ('Duplicate generated marker', begin)
    if begin in text:
        assert end in text, ('Missing generated end marker', end)
        start = text.index(begin)
        finish = text.index(end, start) + len(end)
        children = _foreign_sections(text[start + len(begin):finish - len(end)])
        replacement = section + ''.join('\n' + child for child in children)
        updated = text[:start] + replacement + text[finish:]
    else:
        assert end not in text, ('Orphan generated end marker', end)
        if externs:
            boundary = re.search(r'^' + re.escape(TILESETS_GUARD_END) + r'$', text, re.M)
            assert boundary and text.count(TILESETS_GUARD_END) == 1, 'Missing/duplicate exact tilesets guard'
            start = boundary.start()
            updated = text[:start] + section + '\n' + text[start:]
        else:
            updated = text + '\n' + section + '\n'
    if externs:
        assert updated.index(begin) < updated.index(TILESETS_GUARD_END), ('Extern block outside include guard', begin)
    return updated
