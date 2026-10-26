# R42MistakeHunt — wave 1 report

Verdict: **DONE** — mined one new round-42 lesson mistake (round-41 closure **D2**: dead lesson pointer `w2/R41W2C2Table.md`) with a stdlib gate shown **RED at the mistaken state (exit 1) and GREEN on a repaired fixture (exit 0)**.

## 1. Candidate selection

Candidates from `corpus/lessons/round-41-verifier-spotcheck.md` §5 (D1–D5), mined for the round-42 lesson `## Mistakes` under the criterion "not already mined in round-39/40/41 `## Mistakes`":

| candidate | already mined? | captured by base QUALITY? | why not mined |
|---|---|---|---|
| D1 report filed before wave-2 WAVE-DONE | M39-3 is adjacent (wave reports uncommitted until last commits) but distinct | **QUALITY 47** (round-29: "filed only after its last seat has settled", prefile-check.sh exits 0 at filing) | Q47 already targets this exact failure; nothing new to add |
| D2 lesson pointer to an uncommitted wave report | **not mined** (sweep below) | **none** (see §3) | chosen |
| D4 receipts without `counter_sha256` | not mined | **QUALITY 73** (receipt must state reader digest/argv/commit/instant or `caller_asserted`); the round-42 draft claim already encodes the fix ("records the scorer's exit code **and the sha256 of the counter file**") | already captured + already being fixed by the claim |
| D5 non-segment-bounded path prefix | not mined | partially **QUALITY 83** (compare relative to one recorded root, never by suffix); routed into the R42-C1 predicate ("segment-bounded per round-41 closure D5") | already routed into the claim draft |

Sweep proving D2 (and D4/D5) are unmined — candidate fingerprints in the Mistakes tables at the base `c4a38ea2`:

```
$ for f in round-39 round-40 round-41; do git show c4a38ea2:corpus/lessons/$f.md \
    | sed -n '/^## Mistakes/,/^## Gate/p' | grep -nE 'WAVE-DONE|uncommitted|R41W2C2Table|counter_sha256|segment-bounded|PathRule|non-segment|diagnostic'; done
-- round-39 Mistakes table:
7:| M39-3 | wave reports uncommitted until the round's last commits, ... (M39-3, not D2)
-- round-40 Mistakes table:   (no candidate fingerprint)
-- round-41 Mistakes table:   (no candidate fingerprint)
```

D2's distinguishing features vs M39-3: M39-3 is about *whether* wave reports are committed at all (fix: commit wave 1 at the freeze). D2 is about a *committed* record citing a file that is not in the commit tree at that record's own revision — a dead internal pointer. M41-2 (S126 provenance URL unresolvable from a lane checkout) is the external-provenance sibling; it is fixed by `local-source-gate.py`, which does not cover lesson↔wave pointers.

## 2. The mistake (proposed row M42-1)

- **class**: a committed round record (lesson) cites a wave-report path that resolves neither in the commit tree at that revision nor (at closure) on disk — a dead internal citation; it is the citation-level residue of the D1 sequencing failure (Q47's prefile gate would have caught the *unclean tree*, but a *clean* tree can still cite a file that was never committed).
- **evidence pointer**: `corpus/lessons/round-41.md:76` at `74064474` — the R40-CL5 row: "…reviewed `w2/R41W2C2Table.md`". `round-41-verifier-spotcheck.md` §5 D2. The cited file is absent from the tree at `74064474` and at the round-42 base `c4a38ea2`; it appears only at `ae5dc3f3` ("round-41: wave-2 settled — remaining reports…"). All other 20 wave-relative pointers in the lesson at `74064474` resolve.
- **captured-by**: `none`. Base `QUALITY.md` (c4a38ea2) has no criterion that mechanically requires a committed record's internal pointers to resolve at its own revision: Q1 (resolvable source) is an *admission* criterion for corpus entries; Q52 governs reports citing gate results; Q81 governs pointer-repair *claims*; Q47 governs filing cleanliness, not citation integrity. A clean tree passes Q47 while still containing the dead pointer (the lesson was committed before the cited report landed).
- **fix**: land the cited report in the same commit as the lesson, or correct the pointer by an appended erratum (both make the pointer resolve), and adopt a dead-pointer gate for every committed record (lesson/report/score): every `w1|w2|l1|l2/…` token in the record must resolve via `git cat-file -e <rev>:<path>` at the revision that contains the record. Shown able to fail below.

## 3. The stdlib check (RED → GREEN)

`citation-gate.py` (stdlib only: argparse/re/subprocess; `git -C` read-only). Scans the record's bytes at `--rev` (via `git show <rev>:<file>`), extracts `w[12]|l1|l2/…` pointers (explicit `.ufo/waves/<round>/…` forms too, brace groups `{1..6}`/`{A,B,C,D}` expanded), and checks each against the tree at the same `--rev` with `git cat-file -e`. Exit 0 iff every pointer resolves; exit 1 with the DEAD list otherwise. sha256 `e6fc195a081e7c2491600e461ce9881fea5ad7313867db2dc8d270c86251077c`. It honours `TMPDIR` (no /tmp use) and never writes to the repo.

**RED — mistaken state reconstructed** (sandbox clone `--shared` of the lane; `rev-parse --show-toplevel` verified before any change; no lane/fleet VCS mutation):

```
git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin red/lane
git -C red/lane checkout -q 740644747865c1c331bfacaf4daf46ea218762c3
# + uncommitted closure state exactly per spotcheck line 25:
#   M w2/R41W2ReproV4.md; D w2/artifacts/R41W2Reservation/tx-exec-calls.json
#   untracked late wave-2 reports R41W2C1Rescore.md / R41W2C2CounterMut.md /
#   R41W2Reservation.md + their artifact dirs; w2.ready.dispatched;
#   stray green.err/red.err in lane root and corpus/evidence/round-41/c1/V4/
$ python3 -I -B citation-gate.py --repo red/lane \
    --rev 740644747865c1c331bfacaf4daf46ea218762c3 \
    --wave-root .ufo/waves/round-41 --file corpus/lessons/round-41.md
citations checked: 21
DEAD corpus/lessons/round-41.md:76 w2/R41W2C2Table.md (not in tree at 74064474…)
      line: | R40-CL5 | fixed in prose | … reviewed `w2/R41W2C2Table.md` |
EXIT=1
```

`red.txt` (artifact) holds the full run.

**GREEN — repaired fixture**: same base, then land the cited report (bytes from `ae5dc3f3`, i.e. the real report) and commit as the repair:

```
git -C green/lane checkout -q ae5dc3f3 -- .ufo/waves/round-41/w2/R41W2C2Table.md
git -C green/lane -c user.name=fx -c user.email=fx@fx commit -q -m "fix: land wave-2 C2 table report cited by round-41 lesson"
$ python3 -I -B citation-gate.py --repo green/lane \
    --rev 46d60ae461f2ac20250ba0bb811bbded1427183a \
    --wave-root .ufo/waves/round-41 --file corpus/lessons/round-41.md
citations checked: 21
EXIT=0
```

`green.txt` (artifact) holds the full run.

## 4. Calibration (gate does not over-fire)

| scanned at | files | result |
|---|---|---|
| `74064474` (closure) | round-41.md | exit 1, exactly one DEAD: `w2/R41W2C2Table.md` |
| `c4a38ea2` (round-42 base) | round-41.md + round-41-verifier-spotcheck.md | exit 1, DEAD on round-41.md:76; also flags the spotcheck's **descriptive quote** of D2 at :93 (that line literally describes the absence; see limit below) |
| `c4a38ea2` | round-39.md, round-40.md | exit 0 (brace-expanded `{1..6}`/`{A,B,C,D}` pointers in round-39 resolve; no false positives) |
| `HEAD` (`fdabdfa4`) | round-41.md + spotcheck | exit 0 (the real repair at `ae5dc3f3` landed the reports) |

Limits ([INFERENCE] where inferred):
- The gate is token-level; a quoted path inside a *description of an absence* (spotcheck :93) is flagged too — acceptable, but a follow-up can allow an explicit "not committed/absent" annotation or an adverbs list. The canonical D2 instance (round-41.md:76) is a true mis-citation, not a descriptive quote.
- The gate checks resolvability, not that the cited file is the *intended* one (that is the Q81 concern); it does not run on the real lane (read-only `git show`/`cat-file` only, all `-C`-named).
- Nothing was installed (no tooling authorization events); system `python3` used; no pacman transaction; scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42MistakeHunt` created per spec and removed after artifact copy (`TMPDIR=$S`). Artifacts copied into the lane artifacts dir; no third-party bytes; no VCS mutation anywhere outside fixtures.

## 5. Handoff to L1

- Land the check as `tools/round-42/citation-gate.py` (or integrate into the prefile gate) and run it over `corpus/lessons/*.md` at the round-42 freeze.
- The dead pointer itself is already resolved in history (`ae5dc3f3`); the round-42 lesson row can record M42-1 with this evidence and the red/green receipts.
