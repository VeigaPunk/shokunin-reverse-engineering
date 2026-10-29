#!/usr/bin/env python3
"""Build branch D in the fixture clone: full simulated attempt-2 landing.

Base: 6f4aba63 (lane tip). Adds, in ONE commit:
  1. tools/round-50c3/sqfs-triage-v5.py        (C3 instrument, outside both frozen families)
  2. SKILL.md: registry row inside the markers + `## Rule block 22` section
  3. corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md   (C1 entry; frozen-counter stem)
  4. PROVINCE.md: `## Round-50 additions to Core` + frontier-note line
  5. corpus/README.md: coverage-map row (backticked stem)
  6. corpus/SOURCES.md: rows S243/S244/S245/S249 (11 cells, opened 2026-10-28,
     used-by citing the entry)
  7. SCORECARD.md: coverage-row fraction 139/139 -> 140/140 (stale parenthetical fixed),
     a Capabilities-table row, one new round-50-attempt-2 section (no `- B<n>` bullets)
  8. LOG.md: one entry
"""
import subprocess
import sys

C = '/fast/scratch/hyaku/kaidoku-r50/w3-ConnCrossClaim/clone'
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'


def git(*args, input=None):
    p = subprocess.run(['git', '-C', C] + list(args), capture_output=True, input=input)
    if p.returncode != 0:
        sys.exit('git %s failed: %s' % (' '.join(args), p.stderr.decode()[:400]))
    return p


git('checkout', '-q', '-B', 'c3-full-landing', '6f4aba63')

# 1. instrument placeholder
p = C + '/tools/round-50c3/sqfs-triage-v5.py'
import os
os.makedirs(os.path.dirname(p), exist_ok=True)
open(p, 'w').write('#!/usr/bin/env python3\n"""fixture placeholder: the R50-C3 v5 triage instrument"""\n')

# 2. SKILL.md registry row + block 22
p = C + '/SKILL.md'
t = open(p).read()
row = ("| `tools/round-50c3/sqfs-triage-v5.py` | gate — R50-C3 depth: triage table v5 "
       "(SKILL.md rule block 22) re-routes the three no-independent-reader SquashFS handler "
       "families and is scored against the round-42 recon envelope corpus, run as "
       "`python3 -I -B tools/round-50c3/sqfs-triage-v5.py --root LANE --rev REV --freeze FREEZE "
       "--envelopes DIR --json-out OUT` | 0=met, pair_mismatches 0 and evaluator_missing 0 on "
       "every held-out envelope with the selftest green; 1=not met, a label pair mismatch or a "
       "committed mutation left its pair green; 2=could-not-evaluate, usage error, unknown "
       "revision, frozen path changed, or an unreadable table or envelope | python3 -I -B "
       "tools/round-50c3/sqfs-triage-v5.py --selftest — fixture spelling, exit 0 on 2026-10-29 | "
       "SKILL.md rule block 22 v5 triage table; "
       ".ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ | --json-out and scratch "
       "outside the lane only | kaidoku |\n")
assert t.count('<!-- /instrument-registry -->') == 1
t = t.replace('<!-- /instrument-registry -->', row + '<!-- /instrument-registry -->')
t += ("\n## Rule block 22 — SquashFS triage table v5 (supersedes block 21 routing for "
      "no-reader families)\n\nFixture block 22 body: the three no-independent-reader families "
      "(`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`) take "
      "`clean-unverified`/`record-unverified` and `no-reader-failure`/`preserve-unresolved`; "
      "reader-backed families keep the v4 rows. Block 21 stays as history.\n")
open(p, 'w').write(t)

# 3. C1 entry
open(C + '/' + ENTRY, 'w').write(
    "# LE AVM SquashFS v4 (`squashfs_v4_le`) — Core\n\n"
    "source: S243 - Freetz AVM_LE/AVM_BE byte-order patch (defines context)\n"
    "source: S244 - AVM download index (carrier provenance)\n"
    "source: S245 - unblob 26.6.4 LE handler\n"
    "source: S249 - AVM licence (fetched, never committed)\n\n"
    "Fixture body: four FRITZ!OS carriers through REA 6.5.0 extract-firmware.\n")

# 4. PROVINCE.md
p = C + '/PROVINCE.md'
t = open(p).read()
t += ("\n## Round-50 additions to Core\n\n"
      "| Member family | Layout | Second reader | Evidence |\n"
      "|---|---|---|---|\n"
      "| `squashfs_v4_le` | AVM marker (LE `hsqs`, v4.0, xz, `mkfs_time == bytes_used`) | "
      "`unsquashfs` 4.7.5 + `tools/round-41/sqfs-list.py` | "
      "`corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` |\n\n"
      "Round-50 frontier note, 2026-10-29: LE-AVM little-endian `hsqs` members moved "
      "Frontier -> Core with `2026-10-28-r50-avm-le-squashfs-core` on four FRITZ!OS carriers "
      "(7581/7582 07.18, 6490/6430 Cable, x86 members); the 13k-file rootfs members stay "
      "Frontier under REA's 120 s provider_timeout. Still Frontier: `squashfs_v2_nonstandard`, "
      "`squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, AVM kernels, nested sub-images "
      "below depth 1.\n")
open(p, 'w').write(t)

# 5. README coverage-map row (INSIDE the `## Coverage map` section — c1 section() stops
#    at the next `## ` heading; a row appended at end-of-file is invisible to the binding
#    and flips C2 atom B1)
p = C + '/corpus/README.md'
t = open(p).read()
anchor = "| section | entries | state |\n|---|---|---|\n"
assert t.count(anchor) == 1
t = t.replace(anchor, anchor +
              ("| LE AVM SquashFS v4 (`hsqs` members) | `2026-10-28-r50-avm-le-squashfs-core` | "
               "held — four FRITZ!OS carriers through REA 6.5.0 `extract-firmware`, "
               "`squashfs_v4_le`, full oracle publication, unsquashfs 4.7.5 second reader |\n"))
open(p, 'w').write(t)

# 6. SOURCES rows S243-S245/S249 (11 cells each)
p = C + '/corpus/SOURCES.md'
t = open(p).read()
rows = [
    "| S243 | Freetz AVM SquashFS byte-order patch (`AVM_LE`/`AVM_BE` defines), patch 101 — https://freetz.github.io | docs | B | LE AVM member layout context: the BE variant definition and the byte-order symbol | patch hunk | Defines the big-endian variant; the LE members carry the `mkfs_time == bytes_used` AVM marker | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md |\n",
    "| S244 | AVM download index — https://download.avm.de/fritzbox/ | dataset | A | Carrier provenance: 70 model directories, 28 LE `hsqs` v4.0 xz members with the AVM marker | directory listing | Census the four carriers stand on; image URL -> sha256 chain | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md |\n",
    "| S245 | unblob 26.6.4 SquashFS LE handler — https://github.com/onekey-sec/unblob/tree/26.6.4 | tool | A | The `squashfs_v4_le` handler REA names for little-endian v4 superblocks | handler table | REA routes LE v4 members to `squashfs_v4_le` under extract-firmware | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md |\n",
    "| S249 | AVM licence for FRITZ!OS firmware bytes — https://avm.de | docs | C | Redistribution terms: vendor firmware is fetched, never committed | licence text | Only hashes, listings and receipts enter the lane | mined | 2026-10-28 | on-release | corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md |\n",
]
t = t.rstrip('\n') + '\n' + ''.join(rows)
open(p, 'w').write(t)

# 7. SCORECARD.md
p = C + '/SCORECARD.md'
t = open(p).read()
old = ("139/139 knowledge files mapped at the round-50 landing (the round-47 landing read "
       "138/138; the round-49 entry made it 139; round 50 added no knowledge entry)")
new = ("140/140 knowledge files mapped at the round-50 attempt-2 landing (the round-49 entry "
       "made it 139; the round-50 C1 entry `2026-10-28-r50-avm-le-squashfs-core` made it 140)")
assert t.count(old) == 1
t = t.replace(old, new)
cap_row = ("| genuine AVM-marker little-endian SquashFS v4 (`hsqs`) members through REA "
           "`extract-firmware` | REA 6.5.0 names `squashfs_v4_le` on carved FRITZ!OS members "
           "and publishes the full frozen unsquashfs-oracle file set (7581/7582 07.18, "
           "6490/6430 Cable x86 members) | `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` "
           "+ `.ufo/waves/round-50/l1/scores/` | round 50 |\n")
anchor = ("## Capabilities\n\n| Capability | What it can now do | Evidence pointer | "
          "First-working round |\n|---|---|---|---|\n")
assert t.count(anchor) == 1
t = t.replace(anchor, anchor + cap_row)
new_sec = ("\n## Round 50 attempt 2 — C3 depth and C1 coverage landed\n\n"
           "- **C3 (depth):** triage table v5 landed as SKILL.md rule block 22 (block 21 kept as "
           "history) with the scoring instrument at `tools/round-50c3/sqfs-triage-v5.py` (outside "
           "the C1/C2-frozen `tools/round-50/` family) and one registry row; the three "
           "no-independent-reader families take `clean-unverified`/`no-reader-failure`.\n"
           "- **C1 (coverage):** the frozen counter scored the four FRITZ!OS carriers green at the "
           "attempt-2 landing REV; entry `2026-10-28-r50-avm-le-squashfs-core`, PROVINCE/README/"
           "SOURCES bindings, and the Owned-axes coverage head 140/140 landed in this commit.\n\n")
# Insert BEFORE `## Record corrections — round 50`: that section is the file tail, and
# c2's battery `duplicate line` mutations append `- B<n>` lines at end-of-file; if any `## `
# heading intervenes, the duplicates escape the corrections section and the battery fails
# (measured: 5 failing arms when the new section is appended after the corrections head).
corr_anchor = "## Record corrections — round 50\n"
assert t.count(corr_anchor) == 1
t = t.replace(corr_anchor, new_sec + corr_anchor)
open(p, 'w').write(t)

# 8. LOG.md
p = C + '/LOG.md'
t = open(p).read()
t += ("\n## 2026-10-29 — round 50 attempt-2 (KaidokuR50), landing\n\n"
      "- **C3 fixture entry.** Triage table v5 (rule block 22) + instrument + registry row.\n"
      "- **C1 fixture entry.** Four carriers green under the frozen counter; documentation "
      "bindings landed.\n")
open(p, 'w').write(t)

git('add', '-A')
git('commit', '-q', '-m', 'fixture: full attempt-2 landing simulation (C3 outside frozen prefix + C1 docs)')
print('branch c3-full-landing:', git('rev-parse', 'HEAD').stdout.decode().strip())
print(git('show', '--stat', '--oneline', 'HEAD').stdout.decode())
