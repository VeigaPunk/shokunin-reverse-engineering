#!/usr/bin/env python3
"""L1 landing step 4 (round 50): the R50-C1 knowledge entry and the documentation bindings
(PROVINCE, README coverage map + Frontier, SKILL decision row, SCORECARD capability row + round-50
section, SHONEN note). Every number is read from the committed receipts and frozen tables.
usage: land_c1.py <DATA_COMMIT>"""
import collections
import csv
import hashlib
import json
import os
import re
import sys

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DATA = sys.argv[1]
FREEZE = '435d41fd4ad9211d1579fc447936fb33d2b74467'
STEM = '2026-10-28-r50-le-avm-members-core'
ENTRY = 'corpus/knowledge/%s.md' % STEM
IDS = ['g7581', 'g7582', 'c6490', 'c6430']
LABEL = {'g7581': 'FRITZ!Box 7581 07.18', 'g7582': 'FRITZ!Box 7582 07.18', 'c6490': 'FRITZ!Box 6490 Cable 07.57 (x86 member)',
         'c6430': 'FRITZ!Box 6430 Cable 07.30 (x86 member)'}


def rd(p):
    return open(os.path.join(L, p), encoding='utf8').read()


def wr(p, s):
    full = os.path.join(L, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf8').write(s)


car = json.load(open(L + '/tools/round-50/carriers.json'))
facts = {}
for c in car['carriers']:
    i = c['id']
    a = json.load(open(L + '/corpus/evidence/round-50/c1/%s/after.json' % i))
    r = json.load(open(L + '/corpus/evidence/round-50/c1/%s/run.json' % i))
    nr = a['normalized_result']
    orc = [l.split('\t') for l in rd('tools/round-50/oracle/%s.oracle.tsv' % i).split('\n') if l]
    nrg = [l.split('\t') for l in rd('tools/round-50/oracle/%s.nonregular.tsv' % i).split('\n') if l]
    gaps = collections.Counter(g.get('kind') for g in nr.get('extraction_gaps') or [])
    diags = [d for d in nr.get('diagnostics') or []]
    facts[i] = dict(
        pin=c['sha256'], handlers=sorted({x.get('handler') for x in nr['chunks'] if x.get('handler')}),
        chunks=len(nr['chunks']), files=len(nr['files']), oracle=len(orc), nonreg=collections.Counter(x[1] for x in nrg),
        gaps=dict(gaps), removed=len([d for d in diags if d.get('__typename__') == 'MaliciousSymlinkRemoved']),
        unpub=len(nr.get('unpublished_entries') or []), coverage=nr.get('coverage'), pbytes=nr.get('published_bytes'),
        ev=a['evidence_id'], dur=r.get('duration_ms'), attempts=r.get('rea_attempts'),
        member_bytes=c['notes'].get('member_bytes'), length=c['external']['length'], url=c['external']['url'],
        img=c['external']['image_sha256'], mem=c['external']['member_sha256'], member=c['external']['member'])
for i in IDS:
    f = facts[i]
    assert f['handlers'] == ['squashfs_v4_le'], (i, f['handlers'])
    assert f['files'] == f['oracle'], (i, f['files'], f['oracle'])

score = json.load(open(L + '/.ufo/waves/round-50/l1/scores/c1-at-data-%s.json' % DATA[:8]))
tot_files = sum(facts[i]['files'] for i in IDS)
tot_removed = sum(facts[i]['removed'] for i in IDS)
tot_unpub = sum(facts[i]['unpub'] for i in IDS)

table = ['| id | carrier | carrier bytes | oracle regular files | published regular files | non-regular oracle entries | gaps (REA `extraction_gaps`) | `MaliciousSymlinkRemoved` | evidence id |',
         '|---|---|---|---|---|---|---|---|---|']
for i in IDS:
    f = facts[i]
    table.append('| %s | %s | %d | %d | %d | %s | %s | %d | `%s` |' % (
        i, LABEL[i], f['length'], f['oracle'], f['files'],
        ', '.join('%d %s' % (v, k) for k, v in sorted(f['nonreg'].items())),
        ', '.join('%d %s' % (v, k) for k, v in sorted(f['gaps'].items())) or 'none', f['removed'], f['ev']))
TABLE = '\n'.join(table)

HEAD = ('REA 6.5.0 `extract-firmware --max-depth 1` on the four frozen carriers matched %d/%d at the data commit `%s` '
        '(`carriers_matched %s`, `failing %s`, `frozen_path_changed %s`; receipt `.ufo/waves/round-50/l1/scores/c1-at-data-%s.json`); '
        'every oracle regular file is published (%s) with `squashfs_v4_le` as the only squashfs handler'
        % (score['carriers_matched'], score['target'], DATA[:8], score['carriers_matched'], score.get('failing'),
           score.get('frozen_path_changed'), DATA[:8], ' / '.join(str(facts[i]['files']) for i in IDS)))

entry = '''# Genuine AVM-marker little-endian SquashFS v4 through REA on four pinned vendor members: `squashfs_v4_le` (round 50, R50-C1, Core on four carriers)

status: R50-C1 — %(HEAD)s. The documentation bindings were false at the data commit because this entry and its PROVINCE/README rows did not exist yet; the final score at the landing revision is `.ufo/waves/round-50/l1/scores/c1-final.json`.

source: S243 — https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch — `+#define AVM_LE 2` (:7) and the byte-order condition naming `AVM_LE` (:17-18); the patch adds the symbol and byte order and no LE marker or layout text — re-read 2026-10-28 (1,153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`)
source: S244 — https://download.avm.de/fritzbox/ — the publisher's image listings for the four carrier directories (sizes and dates in the row; bodies committed under `corpus/evidence/round-50/c1/index/`) — re-read 2026-10-28
source: S245 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSv4LEHandler` :454-511 (`NAME = squashfs_v4_le` :455, pattern :463), the LE branch `case Endian.LITTLE, _:` :53 then `commands_args.append("-le")` :54, and the only `is_avm` test :48 inside `case Endian.BIG, 4:` :40 — re-read 2026-10-28 (19,842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`)
source: S249 — https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt — line 850, "The licensee may create only one copy of the software, which may be used exclusively for backup use." — re-read 2026-10-28 (67,591 B, sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`)
verified-at: 2026-10-28
recheck: 180d — re-run the frozen counter at the measured revision (`python3 -I -B tools/round-50/c1-counter.py --root . --rev <measured> --freeze %(FREEZE)s --pkg65 <rea-agents 6.5.0 root> --work <SCRATCH> --carrier-cache <CACHE> --json-out <OUT>`; the cache is built by `python3 -I -B tools/round-50/fetch-vendor.py --spec <(git show %(FREEZE)s:tools/round-50/carriers.json) --cache <CACHE>`); a persistent REA `provider_timeout` is exit 2, not a verdict

## What moved Frontier → Core

Before round 50, `PROVINCE.md` listed "LE AVM members (`hsqs`)" as Frontier in the round-41, round-42, round-44 and round-49 frontier notes. Round 50 adds the `## Round-50 additions to Core` row `squashfs_v4_le` and a `Round-50 frontier note` that supersedes only that clause.

**Scope in one sentence:** REA 6.5.0 `extract-firmware --max-depth 1` publishes every regular file of an independent oracle, at its exact path under the chunk extract root, for the four pinned vendor members below — not "every LE AVM image", not "REA recognises AVM".

## The carriers (chain-pinned, never committed)

AVM forbids copying the firmware package beyond one personal backup copy (S249), so the carriers are not in the lane: each is `image URL → image sha256 → tar member sha256 → carve to bytes_used → carrier sha256` (`tools/round-50/carriers.json`, `tools/round-50/fetch-vendor.py`; the fetch tool refuses any host but `download.avm.de` and any lane-resident cache). Every carrier is `hsqs`, v4.0, compression id 4 (xz), `mkfs_time == bytes_used` (the AVM marker).

%(TABLE)s

The cable images carry a second rootfs, a big-endian ARM `sqsh` member; it is not a carrier. The tar member of every carrier is longer than `bytes_used` (4096-padded squashfs plus an 8-byte trailer); the carve removes it, and on the uncarved member REA reports the trailer as a second chunk with an `unknown-chunk-handler` gap (observed by `w1/C1DevArmA.md` and `w1/C1DevArmB.md`, not claimed).

## What the marker is, and is not

The marker is `mkfs_time == bytes_used`. unblob 26.6.4 tests it only inside the big-endian v4 branch (S245 :48); every little-endian image takes `sasquatch -le -no-exit-code -f -d OUT IN`, marker or not, so an AVM-marker LE member and a standard LE member take one handler and one argv (a host-built standard LE image and a twin with `mkfs_time` patched to `bytes_used` give the same REA projection: `w1/C1MarkerCritic.md` F1-F3b). The marker is therefore a **constant of the pinned bytes**: once the carrier sha256 holds, it adds no evidence of origin, and `layout_ok` in the counter is a frozen-layout statement, not a provenance proof. No source text in the registry describes an LE AVM layout: the Freetz documents define the big-endian variant and patch 101 only adds the `AVM_LE` byte-order symbol (S243; `w1/C1SrcFreetz.md` F1-F5). That the four carriers carry the marker is an observation of their superblocks (`corpus/evidence/round-50/c1/<id>/run.json`), also true of all 28 `hsqs` filesystem rows in the 16 models of the census (`w1/C1CarrierAdversary.md` finding 2).

Two further seat findings bound this: (1) byte-level, the LE members decode field by field as a stock `mksquashfs` 4.x LE image; the only AVM-specific bytes are the header marker and an 8-byte footer after the 4 KiB zero pad (`23 de 53 c4` + 4 bytes, unidentified, also present on the BE member), and `mksquashfs -no-xattrs -mkfs-time <bytes_used>` forges the marker with stock tools (`w1/C1RevLayout.md`); (2) unblob always passes `-no-exit-code` to sasquatch, which masks a non-fatal sasquatch failure into exit 0 and no REA gap, so a partially failed extraction is visible only through the oracle comparison (`w1/C1DepthSource.md`), which is why the counter requires every oracle file to be published.

## What REA does with them (receipts, not prose)

Receipts: `corpus/evidence/round-50/c1/<id>/after.json` (the REA evidence object) and `run.json` (argv, tool pins, superblock summary, attempts). Frozen parameters: `--max-depth 1 --max-output-files 100000 --max-output-bytes 536870912` (REA's default 10,000-entry staging budget fails on a rootfs of this size, `w1/C1DevArmA.md` F1). Totals over the four carriers: %(tot_files)d regular files published, %(tot_removed)d `MaliciousSymlinkRemoved` diagnostics, %(tot_unpub)d unpublished non-regular entries; coverage `partial` (depth 1, as claimed). unblob removes escaping symlinks and REA records them as `MaliciousSymlinkRemoved`; the set of removed links depends on readdir order (`w1/C1GapRule.md` F1), so the frozen gap rule (`tools/round-50/gap-rule.json`) is set-agnostic: every non-regular entry carries exactly one disposition (an `unpublished-entry` gap, a removal, or — for `char-device` `247:0` only — silence). Symlink rows compare path and kind, not `link_target` (unblob rewrites targets).

## Instruments and what they do not prove

`tools/round-50/c1-counter.py` is the round-41 counter ported to the LE layout with the round-49 hardening and six shortcut findings folded in before the freeze (`w1/C1ShortcutCritic.md`): the rerun executes node on the pinned REA package, binds unblob 26.6.4, re-derives the oracle with `unsquashfs` 4.7.5 at scoring time, freezes the REA parameters, binds the counter's own bytes to the freeze, and reads `first_add` with `--full-history`. Its `--selftest` runs 169 cases offline. Controls (`.ufo/waves/round-50/controls/summary.json`): do-nothing, round-41 BE receipts, oracle forgery, `sasquatch` absent, a standard LE carrier planted in a slot, positive. Limits: the documentation bindings are presence checks; a relabelled replay of genuine receipts equals a fresh run on the receipt side (the counter's rerun is the measurement); four carriers from one vendor are not "every LE AVM image"; REA's fixed 120 s `provider_timeout` is a host-load property, so a re-measure on a loaded host can return exit 2.

## Recorded observation, not a claim: the 13k-file ARM rootfs

The first draft named the FRITZ!Box 7530 and 7590 (08.25) members as carriers. Their rootfs holds ~13.4k regular files. At low host load REA published all of them in 40-48 s (`w1/C1DevArmA.md`); at load 42-54 three of three attempts each hit `provider_timeout` (`.ufo/waves/round-50/l1/dev-arm-timeouts.txt`). They were swapped for the 7581/7582 before the freeze and stay Frontier ("LE AVM rootfs of ~13k files under REA's 120 s limit").
''' % dict(HEAD=HEAD, FREEZE=FREEZE, TABLE=TABLE, tot_files=tot_files, tot_removed=tot_removed, tot_unpub=tot_unpub)
wr(ENTRY, entry)

# ---- PROVINCE
pv = rd('PROVINCE.md')
assert '## Round-50 additions to Core' not in pv
pv = pv.rstrip('\n') + '''

## Round-50 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| `squashfs_v4_le` — genuine AVM marker little-endian SquashFS v4 (`hsqs`, xz, `mkfs_time == bytes_used`) on four pinned vendor members (FRITZ!Box 7581 and 7582 07.18, 6490 Cable 07.57 and 6430 Cable 07.30 x86 members); **not** every LE AVM image, and the marker is a constant of the pinned bytes, not a proof of origin | no new REA key — unblob 26.6.4 names the handler and runs `sasquatch -le -no-exit-code -f -d OUT IN` for every little-endian v4 image (S245 :53-54, :455); `REA_UNBLOB_COMMAND` = unblob 26.6.4. **Use:** `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 --max-output-bytes 536870912 --max-output-files 100000 <carrier> <outdir>` on the member carved to `bytes_used`, with `sasquatch` 4.5.1 on the child `PATH`; **expect** one chunk with handler `squashfs_v4_le`, no failed chunk, every regular file of `unsquashfs` 4.7.5 published at its exact path under the chunk root, symlinks as `unpublished-entry` gaps or `MaliciousSymlinkRemoved` removals, coverage `partial`; **refusal:** default staging budget (10,000 entries) fails on a ~13k-entry rootfs, and REA's 120 s deadline can fire on a loaded host | `tools/round-50/c1-counter.py` (frozen `%(FREEZE8)s`), receipts `corpus/evidence/round-50/c1/`, oracle tables `tools/round-50/oracle/` | `%(DATA8)s` data commit: `carriers_matched 4`; entry `corpus/knowledge/%(STEM)s.md`; the four carriers are chain-pinned in `tools/round-50/carriers.json`, never committed (S249) |

Round-50 frontier note, 2026-10-28: LE AVM members (`hsqs`) moved Frontier → Core with `%(STEM)s` (REA 6.5.0 `extract-firmware`, four pinned vendor members, `squashfs_v4_le`). This note supersedes the LE AVM clause of the round-41, round-42, round-44 and round-49 frontier notes, and nothing else. Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed, not claimed), other models' LE members, the big-endian ARM `sqsh` member inside the cable images (the round-41 BE layout), AVM kernel images, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom.
''' % dict(FREEZE8=FREEZE[:8], DATA8=DATA[:8], STEM=STEM)
wr('PROVINCE.md', pv)

# ---- README: coverage map, knowledge index, frontier
rm = rd('corpus/README.md')
lines = rm.split('\n')
# coverage map row: after the round-49 row
i49 = [n for n, l in enumerate(lines) if '`2026-10-28-r49-squashfs-v1v2-core`' in l and l.startswith('| SquashFS v1/v2 through REA (round 49)')]
assert len(i49) == 1
lines.insert(i49[0] + 1, '| LE AVM-marker SquashFS v4 through REA (round 50) | `%s` | **Core on four pinned vendor members** — rea-agents 6.5.0 `extract-firmware --max-depth 1` resolves `squashfs_v4_le` on the carved FRITZ!Box 7581/7582 (07.18) and 6490/6430 Cable x86 members and publishes every regular file of the `unsquashfs` oracle (%s); the marker `mkfs_time == bytes_used` is a constant of the pinned bytes and unblob does not read it on LE; vendor bytes are chain-pinned, never committed; the 13k-file 7530/7590 rootfs is a recorded load-dependent observation, Frontier |' % (STEM, ' / '.join(str(facts[i]['files']) for i in IDS)))
j = [n for n, l in enumerate(lines) if l.startswith('| `2026-10-28-r49-squashfs-v1v2-core`')]
assert len(j) == 1
lines.insert(j[0] + 1, '| `%s` | LE AVM-marker SquashFS v4 through REA on four pinned vendor members, Core (R50-C1) | S243, S244, S245, S249; receipts `corpus/evidence/round-50/c1/`; counter `tools/round-50/c1-counter.py` |' % STEM)
f = [n for n, l in enumerate(lines) if l.startswith('- sasquatch — 2026-10-28 round 49:')]
assert len(f) == 1
lines.insert(f[0] + 1, '- sasquatch — 2026-10-28 round 50: LE AVM members (`hsqs`, `mkfs_time == bytes_used`) are **Core** on four pinned vendor members (`%s`), superseding the LE AVM clause of the round-41/42/44/49 lines above. Still frontier: the ~13k-file 7530/7590 rootfs under REA\'s 120 s limit (observed, not claimed), other models, the BE ARM member in the cable images, AVM kernels, nested sub-images below depth 1.' % STEM)
wr('corpus/README.md', '\n'.join(lines))

# ---- SKILL decision-table row (beside the v1/v2 row)
sk = rd('SKILL.md')
ks = [n for n, l in enumerate(sk.split('\n')) if l.startswith('| SquashFS v1.0/v2.0 (standard, gzip)')]
assert len(ks) == 1
sl = sk.split('\n')
sl.insert(ks[0] + 1, '| LE SquashFS v4 with the AVM marker (`hsqs`, xz, `mkfs_time == bytes_used`) | `extract-firmware --max-depth 1 --max-output-files 100000 --max-output-bytes 536870912` on the member carved to `bytes_used`, `sasquatch` 4.5.1 on the child PATH (no `-be` binary); expect handler `squashfs_v4_le`, no failed chunk, every `unsquashfs` regular file published, symlinks as `unpublished-entry` or `MaliciousSymlinkRemoved`; the default 10,000-entry budget fails on a ~13k rootfs and REA\'s 120 s deadline is load-dependent | held r50 on four pinned vendor members (`corpus/knowledge/%s.md`); the marker is a constant of the bytes and unblob does not read it on LE |' % STEM)
wr('SKILL.md', '\n'.join(sl))

# ---- SCORECARD: capability row + round-50 section (before the corrections section)
sc = rd('SCORECARD.md')
cap = [n for n, l in enumerate(sc.split('\n')) if l.startswith('| SquashFS v1.0/v2.0 `extract-firmware` through REA')]
assert len(cap) == 1
sll = sc.split('\n')
sll.insert(cap[0] + 1, '| LE SquashFS v4 with the AVM marker through REA (four pinned vendor members) | `extract-firmware` on the four carved members (FRITZ!Box 7581/7582 07.18, 6490/6430 Cable x86) publishes every oracle regular file (%s) with handler `squashfs_v4_le`; the marker is a constant of the pinned bytes, vendor bytes are chain-pinned and never committed | `.ufo/waves/round-50/l1/scores/c1-final.json`; `corpus/evidence/round-50/c1/`; `corpus/knowledge/%s.md` | 50 |' % (' / '.join(str(facts[i]['files']) for i in IDS), STEM))
sc = '\n'.join(sll)
wr('SCORECARD.md', sc)
open('/fast/scratch/hyaku/kaidoku-r50/l1/facts.json', 'w').write(json.dumps({k: {kk: (vv if not isinstance(vv, collections.Counter) else dict(vv)) for kk, vv in v.items()} for k, v in facts.items()}, indent=1))
print('c1 landing written;', HEAD)
