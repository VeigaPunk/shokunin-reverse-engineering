#!/usr/bin/env python3
"""round-51 seat ScribeSources — locate every quote in the served bytes.

Each ANCHOR is (file, line, expected_text). The script asserts the expected
text is a contiguous run of the bytes on that exact 1-based line, and that the
same run is unique enough to find. It also verifies the composite (assembled
from adjacent C string literals) quotes by reconstructing them from the
literal fragments and reporting the exact source lines they come from.

Exit 0 = every contiguous quote located; 1 = at least one missing.
"""
import sys

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (os.path.join(_HERE, 'body'),
              '/fast/scratch/hyaku/kaidoku-r51/w1-ScribeSources/body'):
    if os.path.isdir(_cand):
        BODY = _cand + '/'
        break
else:
    raise SystemExit('no body directory found (looked in the seat dir and the scratch)')

# (file, line, contiguous literal expected on that line)
CONTIGUOUS = [
    # --- S250: upstream squashfs-tools 4.7.5 unsquashfs.c -------------------
    ('unsquashfs-4.7.5.c', 1296, 'res = mknod(pathname, chrdev ? S_IFCHR :'),
    ('unsquashfs-4.7.5.c', 1299, 'EXIT_UNSQUASH_STRICT("create_inode: "'),
    ('unsquashfs-4.7.5.c', 1313, 'EXIT_UNSQUASH_STRICT("create_inode: could not"'),
    ('unsquashfs-4.7.5.c', 1315, '" not superuser!\\n", chrdev ?'),
    ('unsquashfs-4.7.5.c', 1328, 'res = mknod(pathname, S_IFIFO, 0);'),
    ('unsquashfs-4.7.5.c', 1330, 'ERROR("create_inode: failed to create fifo %s, "'),
    ('unsquashfs-4.7.5.c', 1349, 'res = mknod(pathname, S_IFSOCK, 0);'),
    ('unsquashfs-4.7.5.c', 4459, 'root_process = geteuid() == 0;'),
    ('unsquashfs_error.h-4.7.5', 44, '#define EXIT_UNSQUASH_STRICT(s, args...) \\'),
    ('unsquashfs_error.h-4.7.5', 46, 'if(!strict_errors) \\'),
    ('unsquashfs_error.h-4.7.5', 47, 'ERROR(s, ##args); \\'),
    ('unsquashfs_error.h-4.7.5', 49, 'BAD_ERROR(s, ##args); \\'),
    ('error.h-4.7.5', 42, '#define ERROR(s, args...) \\'),
    ('error.h-4.7.5', 44, 'progressbar_error(s, ## args); \\'),
    ('error.h-4.7.5', 56, '#define BAD_ERROR(s, args...) \\'),
    ('error.h-4.7.5', 58, 'progressbar_error("FATAL ERROR: " s, ##args); \\'),
    ('error.h-4.7.5', 60, 'exit(1); \\'),
    ('unsquashfs-4.7.5.c', 86, 'int strict_errors = FALSE;'),
    ('unsquashfs-4.7.5.c', 92, 'int set_exit_code = TRUE;'),
    ('unsquashfs-4.7.5.c', 3463,
     'return (failed == TRUE || res == TRUE) && set_exit_code ? 2 : 0;'),
    ('unsquashfs-4.7.5.c', 3936, 'set_exit_code = FALSE;'),
    # master ref, same lines shifted
    ('unsquashfs-master.c', 1373, 'res = mknod(pathname, chrdev ? S_IFCHR :'),
    ('unsquashfs-master.c', 1376, 'EXIT_UNSQUASH_STRICT("create_inode: "'),
    ('unsquashfs-master.c', 1390, 'EXIT_UNSQUASH_STRICT("create_inode: could not"'),
    ('unsquashfs-master.c', 1392, '" not superuser!\\n", chrdev ?'),
    ('unsquashfs-master.c', 1405, 'res = mknod(pathname, S_IFIFO, 0);'),
    ('unsquashfs-master.c', 1426, 'res = mknod(pathname, S_IFSOCK, 0);'),
    ('unsquashfs-master.c', 5381, 'root_process = geteuid() == 0;'),
    # --- S251: upstream squashfs-tools 4.7.5 mksquashfs.c -------------------
    ('mksquashfs-4.7.5.c', 197, '/* Will Mksquashfs pad the filesystem to a multiple of 4 Kbytes? */'),
    ('mksquashfs-4.7.5.c', 596, 'if(!nopad && (i = get_dpos() & (4096 - 1))) {'),
    ('mksquashfs-4.7.5.c', 5964, 'block = nopad ? get_dpos() : (get_dpos() + 4095) & ~4095;'),
    ('mksquashfs-4.7.5.c', 7113, '} else if(strcmp(argv[i], "-nopad") == 0)'),
    ('mksquashfs-4.7.5.c', 7114, 'nopad = TRUE;'),
    ('mksquashfs-4.7.5.c', 7491, 'if(!nopad && (i = get_dpos() & (4096 - 1))) {'),
    ('mksquashfs-4.7.5.c', 8946, 'if(!nopad && (i = get_dpos() & (4096 - 1))) {'),
    ('mksquashfs_help.c-4.7.5', 467, '"-nopad\\t\\t\\tdo not pad filesystem to a multiple of 4K\\n",'),
    # master ref, same lines shifted
    ('mksquashfs-master.c', 573, ' *    pad to 4Kbyte multiple */'),
    ('mksquashfs-master.c', 588, 'if(!nopad && tail) {'),
    ('mksquashfs-master.c', 6262, 'block = nopad ? get_dpos() : (get_dpos() + 4095) & ~4095;'),
    ('mksquashfs-master.c', 7362, '} else if(strcmp(argv[i], "-nopad") == 0)'),
    ('mksquashfs-master.c', 7363, 'nopad = TRUE;'),
    ('mksquashfs_help.c-db038ef265ed00bb17aaf695a72f9b0c3489eb20', 488,
     '"-nopad\\t\\t\\tdo not pad filesystem to a multiple of 4K\\n",'),
]

# (file, [lines], assembled message, label)  -- quoted as `composite`
COMPOSITE = [
    ('unsquashfs-4.7.5.c', [1313, 1314, 1315],
     'create_inode: could not create %s device %s, because you\'re not superuser!'),
    ('unsquashfs-4.7.5.c', [1299, 1300, 1301],
     'create_inode: failed to create %s device %s, because %s'),
    ('unsquashfs-master.c', [1390, 1391, 1392],
     'create_inode: could not create %s device %s, because you\'re not superuser!'),
]

# negative control: a quote that is NOT in the served bytes must be reported MISSING
NEGATIVE = [('unsquashfs-4.7.5.c', 1296, 'res = mknod(pathname, S_IFCHR, 0);')]


def lines_of(fname):
    with open(BODY + fname, encoding='utf-8', errors='replace') as fh:
        return fh.read().split('\n')


def words(text):
    return len(text.split())


def main():
    located = missing = 0
    for fname, lineno, expect in CONTIGUOUS:
        body = lines_of(fname)
        if lineno > len(body):
            print('MISSING %s:%d (line beyond EOF, %d lines)' % (fname, lineno, len(body)))
            missing += 1
            continue
        actual = body[lineno - 1]
        if expect in actual:
            located += 1
            print('LOCATED %s:%d  %r  (%d words)'
                  % (fname, lineno, expect, words(expect)))
        else:
            missing += 1
            print('MISSING %s:%d  expected %r  actual %r'
                  % (fname, lineno, expect, actual.strip()))

    # composite: reconstruct from the C string literal fragments on the lines
    for fname, linenos, msg in COMPOSITE:
        body = lines_of(fname)
        frags = []
        ok = True
        for n in linenos:
            line = body[n - 1]
            parts = []
            inlit = False
            cur = ''
            for ch in line:
                if ch == '"':
                    if inlit:
                        parts.append(cur)
                        cur = ''
                    inlit = not inlit
                    continue
                if inlit:
                    cur += ch
            frags.append(parts)
        joined = ''.join(p for parts in frags for p in parts)
        # the assembled message drops the trailing format specifier formatting
        norm = joined.replace('\\n', '')
        if msg.replace("'", '’') in norm or msg in norm:
            located += 1
            print('LOCATED %s:%s  composite %r  (%d words)'
                  % (fname, '+'.join(map(str, linenos)), msg, words(msg)))
        else:
            missing += 1
            print('MISSING %s:%s  composite %r  fragments=%r'
                  % (fname, '+'.join(map(str, linenos)), msg, norm))

    # negative control: this MUST be reported missing
    for fname, lineno, expect in NEGATIVE:
        body = lines_of(fname)
        actual = body[lineno - 1]
        if expect in actual:
            missing += 1
            print('CONTROL-FAILED %s:%d  the negative control was FOUND' % (fname, lineno))
        else:
            located += 1
            print('CONTROL-OK %s:%d  the negative control is absent as required'
                  % (fname, lineno))

    print('QUOTE_CHECK located=%d missing=%d' % (located, missing))
    return 0 if missing == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
