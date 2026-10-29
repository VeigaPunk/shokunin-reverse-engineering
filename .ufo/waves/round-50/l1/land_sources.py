#!/usr/bin/env python3
"""L1 landing step 1 (round 50): corpus/SOURCES.md rows S243-S249, round-50 search-log entry,
and the committed snapshots the rows pin. Idempotent guard: refuses to run twice."""
import hashlib
import os
import re
import shutil

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W = L + '/.ufo/waves/round-50'
STEM = '2026-10-28-r50-le-avm-members-core'
ENTRY = 'corpus/knowledge/%s.md' % STEM
LESSON = 'corpus/lessons/round-50.md'
SRC = '/fast/scratch/hyaku/kaidoku-r50/l1/srcs/'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


reg = open(L + '/corpus/SOURCES.md', encoding='utf8').read()
assert '| S243 |' not in reg, 'already landed'
rowsold = {}
for l in reg.split('\n'):
    m = re.match(r'^ {0,3}\|\s*(S\d{3,})\s*\|', l)
    if m:
        rowsold[m.group(1)] = [c.strip() for c in l.strip().strip('|').split('|')]

# ---- snapshots
ev = L + '/corpus/evidence/round-50'
os.makedirs(ev + '/c1/index', exist_ok=True)
os.makedirs(ev + '/c2/unblob-listings', exist_ok=True)
for n in ('fritzbox-7581_other', 'fritzbox-7582_other', 'fritzbox-6490-cable_deutschland', 'fritzbox-6430-cable_deutschland'):
    shutil.copy(SRC + n + '.html', ev + '/c1/index/%s-fritz.os.html' % n)
shutil.copy(SRC + 'info6490.txt', ev + '/c1/index/fritzbox-6490-cable-info_en.txt')
lst = {}
for f in sorted(os.listdir(W + '/w1/C2RowS138/listings')):
    shutil.copy(W + '/w1/C2RowS138/listings/' + f, ev + '/c2/unblob-listings/' + f)
    lst[f] = sha(ev + '/c2/unblob-listings/' + f)
p_idx = 'corpus/evidence/round-50/c1/index/'
p_lst = 'corpus/evidence/round-50/c2/unblob-listings/'

S = {}
# S243 Freetz patch 101
S['S243'] = ('| S243 | Freetz `squashfs4-host-be` patch 101, `AVM_BE`/`AVM_LE` symbols — '
             'https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/'
             '101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch | code | B | the Freetz host-tool patch that '
             'defines the AVM target-format symbols and maps `AVM_LE` to little-endian byte order; a build patch '
             'from a third-party repack, not a description of AVM images | `+#define AVM_LE 2` (`:7`); the byte-order '
             'condition naming `SQUASHFS4_LE` or `AVM_LE` selects `__LITTLE_ENDIAN` (`:17`-`:18`); HTTP 200 on '
             '2026-10-28, 1,153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`; snapshot '
             '`.ufo/waves/round-50/w1/C1SrcFreetz/sources/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` | '
             'Under its symbols-only name the patch adds the `AVM_LE` symbol and maps it to little-endian byte order and '
             'nothing else: no LE marker and no LE layout text; the shipped Freetz build compiles only `AVM_BE` '
             '(`squashfs4-host-be.mk:33`), so no source text in the registry describes an LE AVM layout and the marker on '
             'the LE carriers is an observation of their bytes | mined | 2026-10-28 | 180d | `%s` |' % ENTRY)
# S244 AVM index
S['S244'] = ('| S244 | AVM FRITZ!OS download index for the four carrier directories — https://download.avm.de/fritzbox/ '
             '(root, 70 `fritzbox-*` directories) and `fritzbox-7581/other/fritz.os/`, `fritzbox-7582/other/fritz.os/`, '
             '`fritzbox-6490-cable/deutschland/fritz.os/`, `fritzbox-6430-cable/deutschland/fritz.os/` | dataset | A | '
             'which firmware image files AVM publishes in these four directories and their listed sizes and dates; not the image '
             'contents, not any tar member, layout or carrier | listing rows `FRITZ.Box_7581-07.18.image` 19-Aug-2024 12:33 '
             '32010240 B; `FRITZ.Box_7582-07.18.image` 19-Aug-2024 12:36 32256000 B; `FRITZ.Box_6490_Cable-07.57.image` '
             '04-Sep-2023 17:07 39741440 B; `FRITZ.Box_6430_Cable-07.30.image` 05-Sep-2023 09:10 35911680 B; listing bodies '
             'committed under `%s` (sha256 7581 `%s`, 7582 `%s`, 6490 `%s`, 6430 `%s`); HTTP 200 on 2026-10-28 | AVM lists these '
             'four full image files at these sizes (32.0, 32.3, 39.7, 35.9 MB), not the tar-member sizes the carrier table cites; '
             'the 7581/7582 07.18 rows are dated 2024 and sit under `other`, not `deutschland` | mined | 2026-10-28 | 90d | `%s` |'
             % (p_idx, sha(SRC + 'fritzbox-7581_other.html'), sha(SRC + 'fritzbox-7582_other.html'),
                sha(SRC + 'fritzbox-6490-cable_deutschland.html'), sha(SRC + 'fritzbox-6430-cable_deutschland.html'), ENTRY))
# S245 unblob LE handler
S['S245'] = ('| S245 | unblob SquashFS v4 little-endian handler at tag 26.6.4 — '
             'https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | '
             'The `squashfs_v4_le` class (name, `hsqs` v4 pattern, superblock fields) and its little-endian argv only; not the BE AVM '
             'branch (S108, S112), not sasquatch decoding, not any carrier, not other unblob versions | tag 26.6.4 = commit '
             '`1fcc7a0a584a70a96c31f5a276c20944d199a089`; fetched 2026-10-28 HTTP 200, 19,842 B, sha256 '
             '`2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` (equal to S108 and the installed uv-tool copy); '
             'line 25 `EXECUTABLE = sasquatch`; lines 53-54 `case Endian.LITTLE, _:` and `commands_args.append("-le")`; line 455 '
             '`NAME = squashfs_v4_le`; line 463 pattern `68 73 71 73 [24] 04 00`; the only `is_avm` is line 48, inside `case Endian.BIG, 4:` '
             '(line 40) | Name little-endian v4 extraction as `sasquatch -le -no-exit-code -f -d OUT IN` with no AVM-marker test, so an '
             'AVM-marker LE member and a standard LE member take one handler and one argv | mined | 2026-10-28 | 180d | `%s` |' % ENTRY)
# S246 S147 tier correction
o = rowsold['S147']
S['S246'] = ('| S246 | Stanford Encyclopedia of Philosophy, Karl Popper — https://plato.stanford.edu/entries/popper/ | %s | B | '
             'Popper falsifiability criterion | `2. Backdrop to Popper’s Thought`: "falsifiability as his criterion for demarcating science '
             'from non-science: if a theory is incompatible with possible empirical observations it is scientific" (21 words); SEP '
             '`substantive revision Fri Jul 31, 2026`; re-opened 2026-10-28 HTTP 200, 118,135 bytes, sha256 '
             '`2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`, snapshot `corpus/evidence/round-49/c2/popper.html` | '
             'supersedes S147 — tier B (was tier A): CORPUS.md tier text defines B as "strong secondary (expert write-up with reproducible detail, '
             'survey, textbook)" and A as "primary or authoritative"; this entry is a named-author survey with a bibliography, so the '
             'learner cites Popper\'s own works for the criterion\'s wording; the round-49 closure `corpus/lessons/round-49-verifier-spotcheck.md` '
             'disagreed with tier A | mined | 2026-10-28 | 365d | `%s`, `corpus/lessons/round-49.md` |' % (o[2], LESSON))
# S247 S149 correction
o = rowsold['S149']
S['S247'] = ('| S247 | sysexits(3) FreeBSD manual, correction of S149 — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | %s | %s | '
             'The stated reason and locator of S149 only: what the FreeBSD sysexits(3) page says about the EX_USAGE gloss and where the '
             'interface first appeared | `ERRORS`: "EX_USAGE (64) The command was used incorrectly" (7 words), under `ERRORS` and not '
             'under `DESCRIPTION`; `HISTORY`: "The sysexits file first appeared in 4BSD." (7 words); re-opened 2026-10-28 HTTP 200, 59,251 '
             'bytes, byte-identical to the committed snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html`, sha256 '
             '`1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` | supersedes S149 — REJECTED: S149\'s reason was wrong '
             'and inverted provenance: FreeBSD is the origin of sysexits (its `HISTORY` dates the file to 4BSD) and man7 is the Linux '
             'rendering, so this page is not a "second mirror" of S148; it stays rejected because S148\'s header already gives 64 the '
             'meaning "command line usage error" and this page adds no claim a registry row makes; flip: a claim whose verdict rests on '
             'the prose gloss beyond S148\'s header comment, or on the 4BSD origin, which would admit this page with locator `ERRORS` or '
             '`HISTORY` | %s | 2026-10-28 | on-request | `%s` |' % (o[2], o[3], o[7], LESSON))
# S248 S138 grounding
o = rowsold['S138']
f1, f2, f3, f4 = ('squashfs_v1_big_endian__squashfs_v1.0_be.bin_extract.json', 'squashfs_v1_little_endian__squashfs_v1.0_le.bin_extract.json',
                  'squashfs_v2_big_endian__squashfs_v2.0_be.bin_extract.json', 'squashfs_v2_little_endian__squashfs_v2.0_le.bin_extract.json')
S['S248'] = ('| S248 | unblob 26.6.4 SquashFS `__output__` expected trees, member listings — '
             'https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (contents API '
             '`https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs/<tree>/__output__?ref=26.6.4`; '
             'commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`) | %s | %s | unblob 26.6.4 upstream expected member listings, census only | '
             'committed listing snapshots (v1 3 files each, v2.0 and v2.1 4 files each per endian = 22 file entries in 4 endian '
             'trees); located names, each a `name` field of its listing: "cherry.txt" (1 words) in `%s%s` sha256 `%s`; '
             '"cherry.txt" (1 words) in `%s%s` sha256 `%s`; "apple4.txt" (1 words) in `%s%s` sha256 `%s`; "apple4.txt" (1 words) in `%s%s` sha256 `%s` | '
             'supersedes S138 — the census of 22 member files (v1 3 each; v2.0 and v2.1 4 each per endian) rests on these fetched member listings, '
             'not on the directory name S138 quoted; grounds the member census only, not handler code, extractor behaviour, a carrier or an '
             'independent producer | %s | 2026-10-28 | 180d | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, '
             '`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md` |'
             % (o[2], o[3], p_lst, f1, lst[f1], p_lst, f2, lst[f2], p_lst, f3, lst[f3], p_lst, f4, lst[f4], o[7]))
# S249 AVM licence
S['S249'] = ('| S249 | AVM FRITZ!OS firmware licence, publisher info_en.txt of the 6490 cable directory — '
             'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt | docs | A | the licence wording that limits '
             'copying of the firmware package; not a statement about SquashFS layout, extraction or any member | line 850: "The licensee may '
             'create only one copy of the software, which may be used exclusively for backup use." (18 words); line 853 forbids the package being '
             'reverse engineered and then copied or propagated; HTTP 200 on 2026-10-28, 67,591 B, sha256 '
             '`6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`, snapshot `%sfritzbox-6490-cable-info_en.txt` | the publisher '
             'permits one personal backup copy only, so the four carriers are chain-pinned and fetched, never committed | mined | 2026-10-28 | '
             '90d | `%s` |' % (p_idx, ENTRY))
S = {k: S[k] for k in ('S246', 'S247', 'S248')}   # honest stop: C1 rows S243-S245/S249 are not landed (no entry cites them)
for k in list(S):                       # used-by cell: plain paths, no backticks (census E11)
    head, _, last = S[k][:-1].rstrip().rpartition('|')
    S[k] = head + '|' + last.replace('`', '') + ' |'
for k, v in S.items():
    assert v.count('|') == 12 + v.count('\\|'), (k, v.count('|'))
lines = reg.split('\n')
i = max(n for n, l in enumerate(lines) if re.match(r'^ {0,3}\|\s*S149\s*\|', l))
lines[i + 1:i + 1] = [S[k] for k in sorted(S)]
reg = '\n'.join(lines)
# search log entry (before '## Leads')
slog = ('- 2026-10-28 round 50 — Question: do the S147 tier, the S149 reason and locator, and the S138 census grounding survive a re-open (corrections only)? '
        'Where searched: the SEP Popper entry and the FreeBSD sysexits(3) page re-opened against their committed round-49 snapshots, and the GitHub contents API '
        'for the unblob 26.6.4 `__output__` trees (six listings committed under `corpus/evidence/round-50/c2/unblob-listings/`). Identified 3, screened 3, included 3 '
        '(S246-S248), excluded 0; rows 149 -> 152. Stop: the three routed corrections are grounded; the C1 sources opened this round (Freetz patch 101, the AVM index, the '
        'unblob LE handler, the AVM licence text) were NOT registered because no landed entry cites them (the operator wrap-up stopped the round before the data run); '
        'they are recorded in the round-50 lesson `## Gate`.')
reg = reg.replace('\n## Leads (unopened)', '\n' + slog + '\n\n## Leads (unopened)', 1)
open(L + '/corpus/SOURCES.md', 'w', encoding='utf8').write(reg)
print('rows added', sorted(S))
