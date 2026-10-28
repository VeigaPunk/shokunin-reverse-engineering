#!/usr/bin/env python3
"""L1 repair of NON-frozen landed text after wave 2 (KaidokuR49). Every replacement asserts its anchor."""
import os
import re

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'


def rd(p):
    return open(os.path.join(L, p), encoding='utf8').read()


def wr(p, s):
    open(os.path.join(L, p), 'w', encoding='utf8').write(s)


def rep(s, old, new, count=1):
    assert old in s, 'anchor missing: ' + old[:80]
    return s.replace(old, new, count)


# ---------------------------------------------------------------- entry
e = rd(ENTRY)
e = rep(e, 'extraction this round does measure', 'extraction round 49 does measure')
e = rep(e, 'Nothing in this round measures a non-gzip v1/v2 body', 'Nothing in round 49 measures a non-gzip v1/v2 body')
e = rep(e, 'the gzip v3 fixtures are round-42 C2 held-out inputs with no C1 receipt', 'the gzip v3 fixtures have no round-49 REA receipt')
e = rep(e, '(receipts `S112-raw`, `S112-snapshot`; the snapshot is `artifacts/squashfs-26.6.4.py`)',
        '(receipts `S112-raw`, `S112-snapshot`; the snapshot is `.ufo/waves/round-49/w1/C1ScribeEntry/artifacts/squashfs-26.6.4.py`)')
e = e.rstrip('\n') + """

## Corrections after the wave-2 attack (2026-10-28)

Round-49 wave 2 (`.ufo/waves/round-49/w2/`, 40 seats) attacked this entry at `29883d4e`. Its numbers reproduce; the statements below are the repairs it forced. They supersede the sentence they name; the entry is not otherwise rewritten.

1. **Landing score.** The score at the landing revision is `.ufo/waves/round-49/l1/scores/c1-final.json` (its `revision` field names the measured commit; the file is committed one commit later, so it cannot name its own commit). The data-commit score `c1-at-data-4aabb0b4.json` has `exit_code 1` and `met_target false`: six documentation bindings were false because this entry and the PROVINCE/README rows did not yet exist; its `carriers_matched 4`, `failing []` are the carrier clauses.
2. **What the provenance clause is.** `provenance_ok` in the frozen counter is `isabs ∧ no '..' ∧ startswith('/fast/scratch/hyaku/kaidoku-r49/')`. It does not compare the output directory with the committed path, does not read `provenance.json`, and authenticates neither the writer nor the round. Where the status paragraph says the counter "implements that sentence", read this one.
3. **Limits the entry omitted (the plan discloses them).** (a) A relabelled replay — the round-44 receipts with `output_directory` rewritten under `/fast/scratch/hyaku/kaidoku-r49/` and the evidence id re-minted — scores `carriers_matched 4`, as does an envelope computed from the oracle (`.ufo/waves/round-49/w1/C1ProvCritic.md`, `C1GoldForgery.md`; reproduced in `w2/W2C1Forge.md`, `w2/W2Honesty.md`); the claim rests on the counter's own REA rerun, not on the committed receipt. (b) The six documentation bindings are presence checks: a PROVINCE/entry that asserts the opposite scores exit 0 (`w2/W2Honesty.md` H4, `w1/C1DocBindings.md`). (c) **The four carriers are the round-44 fixtures, already measured once in round 44: this is a re-run under a restated predicate, not new data.** (d) The scratch output root named in each `after.json` (`/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/rea-out`, the name `probe-` is the runner's) was pruned after the verbatim copy; `provenance.json` records `copied_verbatim`.
4. **Scope.** The Core row covers the four standard **v1.0 and v2.0** fixtures (`s_major:s_minor` 1:0 and 2:0). `squashfs_v2` also matches `s_minor` 1 (the handler pattern does not constrain it) and both readers read the standard v2.1 pair, but REA never ran on a v2.1 image and no fixture of that minor is a carrier (`w2/W2Coverage.md` F1). The v3 DD-WRT no-pad and 4k-pad images named above are Frontier as well (`F2` there).
5. **REA pin.** The tool whose behaviour is measured is `rea-agents` 6.5.0 (`npx -y rea-agents@6.5.0 extract-firmware --format json --full-output`, `--max-depth` default 3, no depth-limited gap), recorded in each `run.json`; unblob 26.6.4 and sasquatch 4.5.1 are recorded in `extract-env.json` and match the live host (`w2/W2C1Rea.md`).
6. **Field names.** `handler_detail`, `per_carrier_failing`, `gap_kinds` and `provenance_ok` are the *counter's* score fields or paraphrases, not envelope keys: in the envelopes the handler is `chunks[0].handler`, emptiness is `normalized_result.extraction_gaps == []` and `unpublished_entries == []`, and the per-carrier provenance flag is `run_provenance_ok` (`w2/W2Rea.md` F2-F4). The four envelopes contain none of the typed gap strings (`missing-extractor-dependency`, `unpublished-entry`, `depth-limited`, `MaliciousSymlinkRemoved`): they witness "no gap emitted", not the type strings.
7. **S112 line citations.** The class `SquashFSv2Handler` (:158-196) also assigns `NAME = "squashfs_v2"` (:159) and a `DOC` block (:180-196); it does not assign `EXTRACTOR`. The v1 struct closes at :136 (`HEADER_STRUCT` is :137). `squashfs_v3_broadcom` is the `NAME` string at :364 (class :363) and `squashfs_v3_nonstandard` at :410 (class :409). The `match endian, self.version` argv decision starts at :39 (executable at :37). The registry row S112 says `lines 24-70`; the extractor ends at :69 and the row is append-only, so it is left (`w2/W2C1Sources.md`).
8. **Tail fields.** `block_size_1`, `block_log`, `flags`, `no_uids`/`no_guids` and `mkfs_time` are decoded from the packed layout that follows the 32-byte head; the S112 v1/v2 struct (:123-136) ends at the head, so these offsets rest on the bytes and `unsquashfs -s`, not on S112 (`w2/W2C1Entry.md` D6). `unsquashfs -s` prints `Duplicates are removed` for all four carriers, including the two v1 images whose `flags` byte reads `0x00`: the printed line is not a reading of that bit. That the tail offsets and the `78 da` offsets are exact was re-derived by an independent parser (`w2/W2C1Superblock.md`, 0 differences).
9. **Receipt paths.** `scripts/sb.py` and `scripts/s138.py` are `.ufo/waves/round-49/w1/C1ScribeEntry/scripts/sb.py` and `.../s138.py`; the receipt `counter-fixed-path` ran `sed -n 266,272p .ufo/waves/round-49/draft/tools/round-49/c1-counter.py` on the draft (the frozen counter's `FIXED_PATH` is at `tools/round-49/c1-counter.py:276`, and hard-codes the fnm node-24.21.0 path).
10. **Round-44 values.** The round-44 entry records the v1 `mkfs_time` in host-local time (-0300: 04:18:58 and 04:18:51); the UTC values are 07:18:58Z and 07:18:51Z, as in the table above. The statement that the gzip v3 fixtures are "round-42 C2 held-out inputs" is withdrawn (the round-42 entry does not say it).
"""
wr(ENTRY, e)

# ---------------------------------------------------------------- PROVINCE (own appended block, rewritten)
pv = rd('PROVINCE.md')
i = pv.index('## Round-49 additions to Core')
head = pv[:i]
block = """## Round-49 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| `squashfs_v1` and `squashfs_v2` — SquashFS v1 and v2 on the four standard v1.0/v2.0 fixtures (gzip bodies, both byte orders; 4 KiB each); **not** every v1/v2 image, and no v2.1 image was measured | no new REA key — unblob 26.6.4 names the `squashfs_v1`/`squashfs_v2` handlers (S112 :101-102, :158-159; the same URL as S108) and runs `sasquatch -le`/`-be` from the child `PATH` per superblock endianness (S112 :24-26, :51-54, :68-69; dependency contract S110); `REA_UNBLOB_COMMAND` = unblob 26.6.4. **Use:** `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <image> <outdir>` with `sasquatch` 4.5.1 on the child `PATH`; **expect** one chunk whose `handler` is `squashfs_v1` or `squashfs_v2`, `extraction_gaps == []`, and every regular file of `unsquashfs -lls` published under `firmware.bin_extract/` with the same sha256; **refusal signature** without sasquatch: a `missing-extractor-dependency` gap naming `sasquatch` and no published member (round-36 receipts) | `tools/round-49/c1-counter.py` at the round-49 freeze (its own REA rerun is the measurement); second reader `/usr/bin/unsquashfs` (squashfs-tools 4.7.5, a second reader from another release, not an independent producer) `-lls` member census + extracted member digests, cross-checked against the unblob 26.6.4 `__output__` expected trees committed under `corpus/evidence/round-44/oracle/` (S138; S139 grounds the squashfs-tools identity) | four committed MIT fixtures (v1le `b45925fa…`, v1be `529e1077…`, v2le `7c62dbe3…`, v2be `79c0f388…`): the carrier clauses matched 4/4 at the data commit `4aabb0b4` (`carriers_matched 4`, `failing []`, `gaps []`, 3/3/4/4 oracle members published; `.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`, exit 1 there only because the documentation bindings did not yet exist); the score at the landing revision is `.ufo/waves/round-49/l1/scores/c1-final.json`; the same bytes were already measured once in round 44 (not new data); entry `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` (S112, S138, S139) |

Round-49 frontier note, 2026-10-28: SquashFS v1/v2 moved Frontier → Core with `2026-10-28-r49-squashfs-v1v2-core` (`squashfs_v1` and `squashfs_v2`, both byte orders, rea-agents 6.5.0 `extract-firmware` on four committed unblob 26.6.4 fixtures, v1.0 and v2.0 only; second reader `/usr/bin/unsquashfs` 4.7.5 plus the unblob `__output__` expected trees). This note supersedes the SquashFS v1/v2 status of the `## Round-44 measured, not promoted (R44-C1 honest stop)` section and of the round-44 frontier note above (`measured, not promoted`), and the v1/v2 clause of the round-42 frontier note, and nothing else: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images (the handler pattern admits `s_minor` 1; nothing measured), LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1 stay Frontier.
"""
wr('PROVINCE.md', head + block)

# ---------------------------------------------------------------- README
r = rd('corpus/README.md')
r = rep(r, 'oracle `/usr/bin/unsquashfs` (squashfs-tools 4.7.5) `-lls` member census + extracted member digests, cross-checked against the unblob `__output__` expected trees (S138); REA 6.5.0',
        'second reader `/usr/bin/unsquashfs` (squashfs-tools 4.7.5; a second reader from another release, not an independent producer) `-lls` member census + extracted member digests, cross-checked against the unblob `__output__` expected trees (S138); same four round-44 fixtures, so not new data; REA 6.5.0')
r = rep(r, '- sasquatch — 2026-10-26 round 42: SquashFS v3', '- [2026-10-28: the `v1/v2` item below is superseded by the round-49 line further down] sasquatch — 2026-10-26 round 42: SquashFS v3')
r = rep(r, 'Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.\n',
        'Scope: the four standard v1.0/v2.0 fixtures only. Supersedes the round-42 and round-44 lines above for v1/v2. Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3, v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.\n') if 'Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.\n' in r else r
wr('corpus/README.md', r)

# ---------------------------------------------------------------- SOURCES: S112 used-by append only
s = rd('corpus/SOURCES.md').split('\n')
out = []
done = False
for l in s:
    if re.match(r'^ {0,3}\|\s*S112\s*\|', l) and ENTRY not in l:
        l = l.rstrip().rstrip('|').rstrip() + ', ' + ENTRY + ' |'
        done = True
    out.append(l)
assert done
wr('corpus/SOURCES.md', '\n'.join(out))

# ---------------------------------------------------------------- SKILL.md decision table row
k = rd('SKILL.md')
row = ('| SquashFS v1.0/v2.0 (standard, gzip) | `extract-firmware` with `sasquatch` 4.5.1 on the child PATH; expect handler `squashfs_v1`/`squashfs_v2`, `extraction_gaps == []`, members equal `unsquashfs -lls`; without sasquatch a `missing-extractor-dependency` gap | held r49 on four fixtures (`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`); `squashfs_v2_nonstandard` (no second reader), v2.1, v3 Broadcom/non-standard stay frontier — the v4 triage table (block 21) does not apply to them |\n')
anchor = '| Firmware blob | `inspect-firmware-regions` (binwalk 3.1.0), `extract-firmware` (unblob 26.6.4) | held r4u;'
assert anchor in k
i = k.index(anchor)
j = k.index('\n', i) + 1
k = k[:j] + row + k[j:]
wr('SKILL.md', k)
print('repairs applied')
