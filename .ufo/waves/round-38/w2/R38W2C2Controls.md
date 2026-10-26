# R38W2C2Controls — controls replay + new C2 shortcut (round 38, attempt 2, wave 2)

**DEFECTS FOUND.** The seven frozen controls replay red from the first-freeze generator, and the
C2 landing itself reproduces byte-for-byte — but three strictly weaker "do-nothing" states also
score **green** under the frozen C2 counter (one of them leaves the false statement visibly in
`PROVINCE.md`). Plus: the on-disk C1 control receipts are not first-freeze artifacts; they were
silently overwritten by the post-freeze re-scores.

Axes attacked: **calibration** (C2 counter discrimination), **coverage** (adversaries absent from
control suite and selftest), **provenance** (receipt identity vs the counter that produced it).

## 0. Revision chain (corrected against the brief)

`git log --format='%h %p %s' -12 HEAD` shows the real order — **`efd5c47a` is the child of
`e059ca93`, i.e. it predates freeze v2/v3**, not a later "corrected generator" sitting after them:

```
e059ca93 (freeze) -> efd5c47a (control receipts) -> 9c9d496b -> cb4326b2
  -> 79f69347 (freeze v2) -> 3b0da5dd (c1 controls re-scored v2)
  -> f1010f67 (freeze v3) -> 077e212b (c1-0 re-scored v3)
  -> 3b960fe5 (C1 data + C2 pointer repair) -> 0fc61133 (SCORECARD/LOG/lesson) -> e265533e
```

Counter identity per revision (`git show REV:tools/round-38/<f> | sha256sum`, first 12 hex):

| rev | c1-counter | c2-counter | gen-controls |
|---|---|---|---|
| e059ca93 | `a7a62b098709` | `7f137b664984` | `fb30efa3b45a` |
| efd5c47a | `a7a62b098709` | `7f137b664984` | `db54f1a643cd` |
| 79f69347 (v2) | `46c466014ac8` | `7f137b664984` | `db54f1a643cd` |
| f1010f67 (v3) | `d9aa8b622086` | `7f137b664984` | `db54f1a643cd` |
| 3b960fe5 / 0fc61133 / HEAD | `d9aa8b622086` | `7f137b664984` | `db54f1a643cd` |

Consequence for the claims' rule: **the C2 counter never moved** (`7f137b66`, identical at all
seven revisions), so the C2 controls and the C2 verdict are scored by the same instrument. The C1
counter moved twice after the freeze (`a7a62b09 → 46c46601 → d9aa8b62`) and the C1 verdict at
`3b960fe5` was taken with **v3**, not the first-freeze counter — already disclosed by L1
(`.ufo/waves/round-38/l1/freeze-drift-077e212b.json` reports `drift` on `c1-counter.py` for both
amendments; `l1/scores/c1-v3-at-3b960fe5-NOT-THE-RULE.json` names it). My seat confirms that
independently and adds the receipt-consequence in §2. [INFERENCE] the "corrected generator" framing
in the wave-2 brief ("efd … corrected") is a mislabel: efd is the *unamended* generator.

## 1. Seven frozen controls, replayed at efd (task item 1) — all red, receipts reproduce

Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2C2Controls`, `export TMPDIR=$S
HYAKU_SCRATCH=/fast/scratch/hyaku`, tools extracted read-only:

```
git archive efd5c47a72a50b3a434783f82268fb4a96e636a1 tools | tar -x -C "$S"
sha256sum "$S/tools/round-38/gen-controls.py"   # db54f1a643cdb1e2231eeadce0ec668d1c563cb2aaf294f0aeffc081c98b4613
```

Each control was re-run from `$S` (cwd, so `tools/round-38/gen-controls.py` resolves) with its
recorded argv verbatim except `--out` redirected into
`.ufo/waves/round-38/w2/artifacts/R38W2C2Controls/`:

| control | counter exit | met_target | detail | receipt |
|---|---|---|---|---|
| c1-0 do-nothing | 1 | false | carriers_matched 0, all bindings false but `frontier_note` | `replay-c1-0.json` |
| c1-1 three carriers | 1 | false | **carriers_matched 3** (K2 dropped) | `replay-c1-1.json` |
| c1-2 wrong handler | 1 | false | carriers_matched 0 | `replay-c1-2.json` |
| c2-0 do-nothing @ base | 1 | false | mismatches 1 (`prov_core:REA MCP server` → `evidence/doctor/`), guards_ok false | `replay-c2-0.json` |
| c2-1 junk count | 1 | false | mismatches 1 (O1 stated 999/999, observed 3/3) | `replay-c2-1.json` |
| c2-2 delete bad pointer | 1 | false | mismatches 0, guards_ok false (pointers_not_fewer / unrepaired) | `replay-c2-2.json` |
| c2-3 substitute other doc | 1 | false | mismatches 0, guards_ok false | `replay-c2-3.json` |

`gen-controls.py` itself exited **0** for all seven (its contract: 0 = control did *not* meet the
target; 1 = kill). No kill.

Reproducibility check against the **efd-tree** receipts (`git show efd5c47a:.ufo/.../ctl-*.json`):
every field of every `output` block is identical to my replay except `output.revision`, which is a
fresh `mktemp` fixture commit hash by construction. 7/7 exact.

Two extra argv variants for completeness:

* c1-0 with the *first-freeze-era* argv (`--rev e059ca93 --freeze e059ca93`): counter exit 1,
  met_target false (`replay-c1-0-efdargv.json`). The current receipt's argv (`--rev f1010f67`) is
  the v3 re-score and is also red.
* c1-1 / c1-2 re-scored with the **v2** and **v3** counters (`$S/v2`, `$S/v3` extractions):
  exit 1, carriers_matched 0 in all four runs (`replay-v[23]-c1-*.json`). So the two re-scored
  C1 controls hold under the counter that actually judged C1.

Frozen selftests, run at efd: `c2-counter.py --selftest` → `{"cases":14,"green_ok":1,"red_ok":13,
"failures":[]}`, exit 0; `c1-counter.py --selftest --pkg65 …` → `{"cases":15,"green_ok":1,
"red_ok":14,"failures":[]}`, exit 0.

**C2 landing reproduces too.** Frozen counter at the landed revision:

```
python3 -I -B tools/round-38/c2-counter.py --root /home/vgpnk/.../kaidoku-shokunin \
  --rev 0fc6113376a156fddc3ec385386d71c3a4a9f690 --base 77091b492cc53f8743bd0701b1e7d5e66123dd84
# {"mismatches":0,"guards_ok":true,"met_target":true,...}  exit 0   -> c2-landed-reproduce.json
```

Identical to `.ufo/waves/round-38/l1/scores/c2-at-0fc61133.json` on every field
(`revision, mismatches, unresolved, assertion_mismatches, guards_ok, met_target, pointers,
observed, guards`). The repair target is substantive, not cosmetic: at `0fc61133`
`.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt` and `doctor-6.7.0.txt` are committed
content, and the same tree already exists at the base `77091b49`.

## 2. Defect: the on-disk C1 control receipts are post-amendment overwrites (provenance)

File mtimes in `.ufo/waves/round-38/controls/` (`ls -la --time-style=full-iso`):

```
ctl-c1-1-three-carriers.json    2026-10-26 03:31:09.698   <- 3b0da5dd (v2 re-score, 03:31:12)
ctl-c1-2-wrong-handler.json     2026-10-26 03:31:09.898   <- 3b0da5dd
ctl-c1-0-do-nothing.json        2026-10-26 03:33:18.318   <- 077e212b (v3 re-score, 03:33:18)
ctl-c2-*.json                   2026-10-26 03:06:38-03:09:11   <- efd5c47a
```

The receipt content changed with the overwrite, and the argv did not:

| file | at efd (tree) | at HEAD | which counter produced the HEAD copy |
|---|---|---|---|
| `ctl-c1-1-three-carriers.json` | `carriers_matched: 3`, rev `801e2019…` | `carriers_matched: 0`, rev `a3646b58…` | v2 (`46c46601`) |
| `ctl-c1-2-wrong-handler.json` | 0 | 0 | v2 |
| `ctl-c1-0-do-nothing.json` | `--rev e059ca93` | `--rev f1010f67` | v3 (`d9aa8b62`) |

The recorded `argv` does not name a counter revision, so the file now claims "gen-controls.py c1-1"
while holding numbers only v2/v3 can produce (my v2/v3 replays give exactly `carriers_matched: 0`;
the efd counter gives exactly `3`). Nothing in the receipt distinguishes the two. The first-freeze
values survive only in git objects (`git show efd5c47a:.ufo/waves/round-38/controls/…`), not in the
working tree that wave-2 seats are handed.

Damage assessment: **no kill** — every variant of every C1 control is red under every counter
version (a7a62b09 / 46c46601 / d9aa8b62), so the kill rule still holds on substance. The defect is
that a receipt's provenance no longer identifies its instrument, which is exactly R36-CL6-class
(receipt identity), and it is a regression *relative to the first freeze*, which the claims promise
never changes counters after.

## 3. Kill signal: three C2 shortcuts score green under the frozen counter

`resolves()` (c2-counter.py:120-135) tests **path existence only**; `units()` (c2-counter.py:57-100)
builds a **dict keyed by first cell**, so a later row with the same first cell silently shadows an
earlier one; `unrepaired` accepts any resolving pointer whose path equals the base-bad path *or
ends with `/` + that path*. Each of those is exploited below. All runs use the frozen counter
(`7f137b66`, identical at efd and HEAD), `--base 77091b492cc53f8743bd0701b1e7d5e66123dd84`, on
`--no-hardlinks` clones in scratch (clone toplevel verified == scratch path before the first commit;
fixture identity only inside the clone).

### S2 — cheapest: base tree + one fabricated file, **zero self-assessment edits** → GREEN

```
git clone -q --no-checkout --no-hardlinks "$LANE" "$S/s2"
git -C "$S/s2" checkout -q 77091b492cc53f8743bd0701b1e7d5e66123dd84           # the BASE, untouched
mkdir -p "$S/s2/evidence/doctor" && printf 'stub: nothing measured\n' > "$S/s2/evidence/doctor/doctor-6.5.0.txt"
git -C "$S/s2" add -A && git -C "$S/s2" commit -qm 'S2 shortcut: materialize evidence/doctor/ at base'
git -C "$S/s2" diff --stat 77091b49 HEAD
#  evidence/doctor/doctor-6.5.0.txt | 1 +
#  1 file changed, 1 insertion(+)
python3 -I -B tools/round-38/c2-counter.py --root "$S/s2" --rev HEAD --base 77091b49…
# {"assertion_mismatches":[],"guards_ok":true,"met_target":true,"mismatches":0,"unresolved":[]}  exit 0
```

Frozen receipt: `shortcut-s2.json`. `PROVINCE.md` still reads `doctor outputs in `evidence/doctor/``
— the text CTL-C2-0 marks as the one mismatch — and the file the pointer names is a one-line stub
written by the claimant. The C2 "before/after" delta (1 mismatch → 0) is therefore obtainable
**without any repair at all**: manufacture the missing path. Cost: one commit, one file, no reading
of the intended document.

### S1 — landed tree, pointer reverted, path fabricated → GREEN

```
checkout 0fc61133; replace `doctor outputs in `.ufo/waves/round-19/evidence/doctor/` (doctor-6.5.0.txt, doctor-6.7.0.txt)`
               with `doctor outputs in `evidence/doctor/``        # i.e. revert the C2 repair exactly
add evidence/doctor/doctor-6.5.0.txt (stub) ; commit
python3 -I -B tools/round-38/c2-counter.py --root "$S/s1" --rev HEAD --base 77091b49…
# {"mismatches":0,"guards_ok":true,"met_target":true}  exit 0    -> shortcut-s1.json
```

`unrepaired` is satisfied because `evidence/doctor` now *exists at the measured revision*, so the
base-bad path "repairs itself". The claim's stated binding — "every pointer unresolved at the base
repaired by a resolving pointer **to the same document** (the committed
`.ufo/waves/round-19/evidence/doctor/` tree)" — is not what the counter tests.

### S3c — sharpest: the false pointer stays visible in `PROVINCE.md` → GREEN

```
checkout 0fc61133
PROVINCE.md: restore `doctor outputs in `evidence/doctor/`` in the REA MCP server row  (false at this rev)
             append a duplicate row LATER in ## Core:
             | REA MCP server | duplicate row | doctor outputs in `.ufo/waves/round-19/evidence/doctor/` |
SHONEN.md:   `PROVINCE.md:97-125` -> `PROVINCE.md:98-126`   (compensate the one-line shift)
python3 -I -B tools/round-38/c2-counter.py --root "$S/s3c" --rev HEAD --base 77091b49…
# {"assertion_mismatches":[],"guards_ok":true,"met_target":true,"mismatches":0}  exit 0  -> shortcut-s3c.json
git -C "$S/s3c" show HEAD:PROVINCE.md | grep -c 'doctor outputs in `evidence/doctor/`'   # 1  (still there)
git -C "$S/s3c" cat-file -e HEAD:evidence/doctor || echo ABSENT                          # ABSENT
```

The predicate sentence is *literally false* at the measured revision (a backticked lane-repo
pointer in a self-assessment surface does not resolve) and the counter returns `met_target: true`,
because `units()` keeps only the last row per first cell. `pointers_not_fewer` still holds (the
duplicate row is an extra token, 51 ≥ 48) and `unrepaired` is satisfied by the shadow row.

Intermediate run for calibration: appending the duplicate row **without** shifting the SHONEN range
fails only on `R3 SHONEN box4 Adjacent range` (`observed [98,126]`, `stated [97,125]`) — i.e. the
line-range assertion is the incidental catcher, not any duplicate-row or provenance check
(`shortcut-s3b.json`, exit 1). An agent that adjusts the stated range (as above) walks through.

### What is NOT defeated (calibration of the kill)

The landed state is honest: single row, real round-19 doctor documents, no fabricated path
(`git cat-file -e 0fc61133:evidence/doctor` → absent; `grep -c "^| REA MCP server"` → 1). The
shortcuts are counter-instrument defects, not evidence that `0fc61133` misstates the repo. So the
C2 verdict "met at 0fc61133" survives; what does not survive is the claim that a green C2 receipt
means "the self-assessment surfaces carry zero mismatches" — it means "no mismatch is visible to a
last-row-wins, existence-only scan".

## 4. Coverage gap in the control suite and selftest

The 14-case C2 selftest and the 4 frozen C2 controls contain: do-nothing, junk count, deleted
count, deleted pointer, substitution by another *existing* document, unresolved pointer kept, box
removed, three range errors, new unresolved pointer, wrong counts. They do **not** contain:

* materialize-the-missing-path (S1/S2) — the pointer is left unresolved-by-intent and the path is
  created, which is the natural lazy fix an agent reaches for;
* duplicate-row shadowing (S3c) — no case has two rows with the same first cell.

Equivalently, no adversary in the suite adds a *new* path to the repo. That is the single cheapest
shortcut against this predicate and it is unrepresented. [INFERENCE] c2-3 "substitute other
document" was intended to cover substitution, but it substitutes into an already-existing path in a
fixture and never exercises base-bad-pointer repair by *creation*, which is why the hole survived.

## 5. Impacted axes

* **calibration** (C2, the axis C2 claims to work): counter accepts three non-repairs; the green
  receipt does not certify the sentence it is printed for.
* **coverage**: adversary space missing the cheapest fake-fix; control suite gives false assurance
  for the class "pointer repaired by fabricating the target".
* **provenance**: C1 receipts rewritten in place by later commits while retaining the earlier argv;
  the receipt no longer names its instrument (R36-CL6 class).

## 6. Smallest safe correction (round 39; nothing here changes round-38 verdicts)

1. `resolves()` for a **base-unresolved** repair must require the target to exist **at the base**
   (`exists(root, base, p2)`), not merely at the measured revision. The real repair
   (`.ufo/waves/round-19/evidence/doctor/`) does exist at `77091b49`; S1/S2's fabricated
   `evidence/doctor/` does not. One added condition, no predicate text change.
2. `units()` must **accumulate rows per first cell** (list, not dict overwrite) and fail on a
   duplicate first cell in `## Core` / `## Frontier` / `## Owned axes` / `## Capabilities`. Kills S3c
   in one line, and closes the same shadowing hole for every other bound surface.
3. Control receipts must record the counter digest (`sha256` of the counter file at the commit that
   wrote the receipt) and be written to a new path instead of being overwritten. Re-score receipts
   append; they never replace.
4. Add the two adversaries (materialize-path, duplicate-row) to the C2 selftest and the frozen
   control set before round 39's freeze.

## 7. Bounds / tooling

Read-only on the lane: only `git show/log/ls-tree/cat-file/archive/diff`, `grep`, `python3`, `ls`.
No `npx`, no REA invocation, no VCS mutation in the lane; all clones/fixtures under
`/fast/scratch/hyaku/kaidoku-r38/R38W2C2Controls` (`git -C "$S/<v>" rev-parse --show-toplevel`
verified == that path) and removed on exit. Artifacts written only under
`.ufo/waves/round-38/w2/artifacts/R38W2C2Controls/` (18 receipts, listed in §1/§3). No tool
installed or upgraded (node v24.21.0, python 3.14 from the system; nothing needed).

[INFERENCE]-tagged items: the generation-order mislabel in §0 and the intent attribution in §4.

Report: `.ufo/waves/round-38/w2/R38W2C2Controls.md`
