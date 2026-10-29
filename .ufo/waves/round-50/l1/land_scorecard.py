#!/usr/bin/env python3
"""L1 landing step 3 (round 50): SCORECARD.md in-place repairs of the two Owned-axes heads (B1, B2,
the same in-place refresh every earlier round made) and the append-only `## Record corrections — round 50`
section (B3, B4, B5, B10, B11). The round-50 results section is written separately after the data run."""
import re
import sys

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
N = int(sys.argv[1])          # knowledge files at the landing (139 at base + the C1 entry)
sc = open(L + '/SCORECARD.md', encoding='utf8').read()
assert '## Record corrections — round 50' not in sc
old = '138/138 knowledge files mapped at the round-47 landing'
assert sc.count(old) == 1
sc = sc.replace(old, '%d/%d knowledge files mapped at the round-50 landing (the round-47 landing read 138/138; the round-49 entry made it 139 and the round-50 entry %d)' % (N, N, N), 1)
lines = sc.split('\n')
for i, l in enumerate(lines):
    if re.match(r'^\|\s*calibration\s*\|', l) and 'rejected-harmed' not in l:
        assert l.rstrip().endswith('|')
        lines[i] = (l.rstrip()[:-1].rstrip() + ' Round 50: the round-48 closure `corpus/lessons/round-48-verifier-spotcheck.md` graded '
                    'calibration `rejected-harmed`; the round-49 record corrections measured `mismatches 9 \u2192 0` '
                    '(`.ufo/waves/round-49/l1/scores/c2-final.json`); this row is a finite proxy over the atoms its counters name, '
                    'not an expertise score. |')
        break
else:
    raise SystemExit('no calibration row')
sc = '\n'.join(lines)
exp_sha = '0a9ddec8dc917f835a609352218854f41b6038a17418962b3047dfc5b033c36f'
sc = sc.rstrip('\n') + '''

## Record corrections — round 50

Append-only repair of the round-48/49 self-assessment atoms `tools/round-50/c2-record.py` re-derives (B3, B4,
B5, B10, B11; B1 and B2 are the in-place Owned-axes heads above, B6-B8 are the SOURCES correction rows S247,
S246 and S248, B9 the registry rows in `SKILL.md`). The original sentences stay where they were written.

- B3 seats=75 reports=72 blocked=C1Meaning aborted=ScribeReportNumbers missing=C1Battery,C1Meaning,ScribeReportNumbers
- B4 coverage=unchanged depth=improved calibration=harmed expansion=unchanged quality=harmed discernment=improved discernment_scope=decision-level-only source=corpus/lessons/round-48-verifier-spotcheck.md
- B5 receipt=33f65a91 tip=8847042a c1_sha256=6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e c2_sha256=d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914
- B10 selftest=tools/round-50/selftest-r49-c2.py cases=40 expected_sha256=%s
- B11 expansion=improved quality=unchanged discernment=unchanged admission=admitted spot_check=landed source=corpus/lessons/round-49-verifier-spotcheck.md

What each line corrects, in prose: **B3** the round-48 section's "all 75 seats settled" holds for 73 handles; `C1Meaning` ended
`blocked` (`frozen_worktree_dirty`) and `ScribeReportNumbers` `aborted`, and three seats have no report artifact (72 of 75). **B4**
the round-48 trend line "quality improved on the instruments / discernment improved" is the lane's own reading; the non-author
closure graded quality `harmed` (source-record errors) and discernment `improved` at decision level only. **B5** the round-48
final receipts are `c1-final-33f65a91.json` and `c2-final-33f65a91.json` (lane tip `8847042a`), which the round-48 section never
names. **B10** the closure asked for a `--selftest` of `c2-mismatch.py`; the frozen file stays byte-identical and the hermetic
self-test is `tools/round-50/selftest-r49-c2.py` (40 cases against a hand-written expected file whose sha256 is stated above).
**B11** the round-49 trend line says discernment "improved at decision level ... the non-author spot-check is pending"; the
round-49 closure (`corpus/lessons/round-49-verifier-spotcheck.md`) is that spot-check and grades discernment `unchanged`, with
admission `admitted`.
''' % exp_sha
open(L + '/SCORECARD.md', 'w', encoding='utf8').write(sc)
print('ok', N)
