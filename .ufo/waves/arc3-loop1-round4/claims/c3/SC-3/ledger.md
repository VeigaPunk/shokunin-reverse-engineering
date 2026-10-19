# SC-3 injection ledger — chain c3, wave `arc3-loop1-round4`

Seat SC-3 (scribe) · chain c3 · task: "injection ledger + records drafts for the
parent (PIN-FREE)". Artifacts: this file, `claims/c3/SC-3/harness/injections.sh`,
`claims/c3/SC-3/evidence/before/`, and the two drafts under
`claims/c3/records-drafts/`. Scratch: `/var/tmp/sc3-r4` (never `/tmp`).
Custody paths were never opened for writing: every fixture below is a scratch
path under `/var/tmp`; `custody-pair.py` itself was read only (copied, never
modified — the real target is EX-21's, and it is untouched by this seat).

## Identity (rule #14) and method

| role | object | revision | re-derived |
|---|---|---|---|
| BEFORE | `.ufo/gates/custody-pair/custody-pair.py` (round-3 landed, EX-21) | sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, 1155 L | re-derived at copy to `/var/tmp/sc3-r4/base/custody-pair.py` (14:04:54Z) and again at draft close |
| BEFORE | `.ufo/gates/custody-pair/README.md` (round-3 landed) | sha256 `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`, 185 L | same two reads, identical |
| AFTER | `.ufo/gates/custody-pair/custody-pair.py` (round-4, EX-21's landing) | sha256 `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`, 1343 L | landed 14:09:30Z (watcher caught the transition); copied to `/var/tmp/sc3-r4/after-base/custody-pair.py` and re-derived at 14:09:46Z and at 14:11Z — identical all three times; the whole after-column below is first-hand on this revision |
| AFTER | `.ufo/gates/custody-pair/README.md` (round-4) | sha256 `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186`, 267 L | observed at 14:10:00Z; the README moved twice inside the landing window (`f30df42e…` → `91fd386b…` → `125e7e02…`) while the tool stayed `29bb45ae…` — the parent re-derives the settled pair at the commit point (rule #14) |

Measured 2026-10-19 14:04–14:07Z (−03 11:04–11:07), Python 3.14.7, uid 1000,
host plazir27. Method: `harness/injections.sh <tool-copy> <workdir> <tag>` —
one scratch copy of the tool, fixtures under `/var/tmp/sc3-r4/work/fixtures`,
every leg's stdout+stderr and exit code kept per leg (`evidence/before/before-<id>.out`,
`before-<id>.rc`). A second driver (`/var/tmp/sc3-r4/controls.sh`) holds the
r3-guard controls and the compound cases; its transcript is
`evidence/before/controls-summary.txt`. Selftest control (basename-preserving
copy, so the TZ case re-invokes the right file): `CLEAN cases=22 passed=22
failed=0 exit=0`.

Baselines at the records-side HEAD `015e1ba` (independent of the tool): command A
`{"knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [],
"citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0,
"depth_score": 10.0}`; census `.ufo/gates/c1-census-v10.py --root .`
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0.
Both are the parent's re-measurement targets at the work commit, not this seat's
claim.

## The ledger — four holes × before × after × declared class

"R" = a receipt written by the tool itself. All four holes were re-measured
first-hand by this seat on the base copy; the cross-corroboration column names
seats that measured the same shape independently (their artifacts, their runs).

| # | hole (r3 debt id) | injection (command shape) | BEFORE — `7cd19c3c…` (this seat, 14:04–14:07Z) | cross-corroboration | AFTER — declared class | state at draft close |
|---|---|---|---|---|---|---|
| a | **sidecar path not scope-checked** (r3 c2 verdict item 3; CR-4 §1; RV-8 gap 2) | `capture --paths X.sha256 --out X` (spelling A: the sidecar lands **on** the measured file); `capture --paths X --out X.sha256` (spelling B: the sidecar lands on the measured file's **neighbour**, and a second sidecar `X.sha256.sha256` is created) | A: `RECEIPT: vic  sha256=299ca3c0…`, `SIDECAR: vic.sha256`, `OK paths=1/1 exit=0` — the measured file `vic.sha256` is **replaced** by the 2-line sidecar text `299ca3c0…  vic` (pre-image `alpha\n`, sha `b6a98d9c…` → `03b5430f…`). B: exit 0, both `vic.sha256` and `vic.sha256.sha256` written (`evidence/before/before-a1.out`) | EX-23 `before-probe.out` (A, B, B2 — identical exits, TOUCHED-FILES lists match); CU-1 `A6a.out` (spelling B: `exit=0`, neighbour clobbered); RV-7 `BASE-7cd19c3c-probe.json` (leg A `exit 0`, `measured_file_intact=false`); RV-8 (leg a: rc 0, measured file replaced by the 68 B sidecar); EX-24 `before/matrix.txt` L13 `sidecar-clobbered=yes`; CR-4 T7/T18 (r3, base `112d01dc…`) | `2 USAGE` — a refused write, per the r3 write-guard's own class for a guarded aim | **CLOSED at `29bb45ae…` (first-hand, 14:10Z)**: spelling A → `USAGE: refusing to write a receipt or its derived sidecar over a path it measures, a custody path, or the sidecar-shaped neighbour of one (resolved path or inode)` exit 2, and `vic.sha256` re-derives its pre-image sha `b6a98d9c…` (byte-intact); spelling B → same refusal exit 2, both `vic` and `vic.sha256` byte-intact and **no** `vic.sha256.sha256` created. RV-7's variant matrix (reference `6e920b22…`, MUT-A restores the before-behavior) shows the fix is load-bearing; the landed guard derives the sidecar name inside a guarded region, so the RV-7 attack-1 `--out ''` trap is avoided (`--out ''` reads the declared `USAGE` with a message, exit 2, `after-b2.out`) |
| b | **`out.parent.mkdir` outside the guarded `try`** (CR-3 §3 / CR-4 T16) | `capture --paths X --out <existing-regular-file>/sub/r.txt` | raw `NotADirectoryError` traceback from `out.parent.mkdir(parents=True, exist_ok=True)` at `custody-pair.py:653` (outside the `try` that catches `OSError` at `:654-661`), **exit 1**, no receipt, outside the declared map (`evidence/before/before-b1.out`) | EX-24 `before/matrix.txt` L1 `exit=1 traceback=1` (same shape; also L3 parent-unwritable `exit=1 traceback=1`); CU-1 `A6b.out` (same traceback tail, exit 1); RV-7 `BASE` leg B `exit=1 traceback=true`; RV-8 (leg b: rc 1 raw `NotADirectoryError` / `PermissionError`) | `2 USAGE` — "a refused/failed write" (the existing `except OSError` arm already prints `USAGE: write failed (…)`) | **CLOSED at `29bb45ae…` (first-hand, 14:10Z)**: `USAGE: cannot create the receipt directory ([Errno 20] Not a directory: …): <out>` exit 2, no traceback (`after-b1.out`); the fresh-parent control still works (`--out new/deep/r.txt` → `OK paths=1/1 exit=0`, receipt + sidecar created, `/var/tmp/sc3-r4/freshp/`). RV-7's MUT-B restores the traceback exactly; EX-24's independently-built candidate `ac2cd74e…` showed the same shape (L1 `exit=2 traceback=0`, L3 `exit=2`, L4 `exit=0`, selftest 24/24) |
| c | **coverage gate counts stanzas, not distinct paths** (r3 verdict item 5; EX-24 patch) | `verify <reference with 5 duplicate stanzas for ONE path> --live --require-paths 5`; v2 shape (`capture --paths P P P P P`) and v1 sums shape (5 identical `sha256  path` rows) and v1 pipe shape (5 identical `path|ino|…|sha` rows) | all three shapes **pass the gate**: `stanzas=5` printed, `VERDICT: MATCH paths=1 … exit=0` (v2/sums; `before-c3.out`, `before-c5.out`) and `MATCH-V1-PARTIAL paths=1/1 drift=0 exit=0` (pipe, `i9.out`), with **zero** `REFERENCE-COVERAGE` lines — the gate's own line is only printed on the failure path, so a padded reference passes **silently**; the other four custody paths remain unexamined | EX-24 (r3 patch author, `579304d4…`) and its r4 re-run `before/matrix.txt`; CU-1 `A1-padded.out` (`MATCH paths=1/1 exit=0`, no coverage line) and `A2-noncanonical.out` (5 unrelated paths also pass) — CU-1's verdict: "real and open at the landed revision"; RV-7 `BASE` leg C `exit=0, distinct=none`; RV-8 (leg c: rc 0, zero coverage lines); EX-24's `after2` still counts stanzas (its L13 is the sidecar leg) | `2 USAGE` — "fewer reference paths than `--require-paths N` demands", counting **distinct resolved paths** (the EX-24 one-line change: `have = {…}` then `len(have) >= required`, and the same basis in the USAGE message) | **CLOSED at `29bb45ae…` (first-hand, 14:10Z)**: all three padded shapes refused — v2 duplicate (`after-c3.out`), v1 sums duplicate (`after-c5.out`), v1 pipe duplicate (`after-pipe.out`) each read `USAGE: reference covers 1 of the required 5 distinct paths` + `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: <5 canonical>`, exit 2. Controls stay green: 5 distinct paths `MATCH 5/5 exit=0` (`after-c7.out`), mixed set `MATCH 5/5` (`i6`), 1-of-5 refusal unchanged (`after-c1.out`). RV-7's MUT-C restores the silent pass exactly. **Named coupling kept**: the count and the `unaccounted:` list share one basis, so no self-contradictory line prints |
| d | **both-sides-absent MATCH semantics** (r3 verdict item 4-wording / R1) | ghost path, two shapes: **(d1) capture-while-absent** `capture --paths <absent>` → `PARTIAL paths=0/1 exit=13`; then `verify R --live` and `verify R R`. **(d2) capture-then-delete** (CU-1's shape) receipt captured while present, path then removed: `verify R R` and `verify R --live` | d1: both modes read `MATCH paths=1 MATCH=1 exit=0`, `compared=0/11`, `SHA256-CONTRACT: 0/0` — an absent path agrees with an absent path (`before-d2.out`, `before-d3.out`). d2: receipt-vs-receipt `MATCH 1/1 compared=11/11 exit=0` (the receipts agree on stored fields), while the same receipt vs **live** reads `ABSENT exit=13` — the same path, two verdicts, by which side is the candidate | r3 SC-3 ledger R1 (d1 shape at `112d01dc…`/`7cd19c3c…`); r3 c2 verdict §"both-sides-absent MATCH adjudicated as declared design"; CU-1 `A3b-ghost-ghost.out` (d2 receipt-vs-receipt `MATCH … compared=11/11`), `A3a-ghost-live.out` (`ABSENT exit=13`), `A3c-ghost-vs-custody.out` (ghost reference vs a canonical-5 receipt → `ABSENT exit=13`, five `EXTRA-PATH` rows); RV-7 `BASE` leg D (`MATCH compared=0/11 exit 0`; error-carrying stanza → `UNEVALUABLE exit 14` — the discriminator is the error line); RV-8 (leg d: rc 0 `MATCH`, `compared=0/11`, declared design) | **adjudication, not a class change** (per the frozen claim: "adjudicate and document … only error-carrying stanzas are UNEVALUABLE"); the ruling text must land in the gate README | **CLOSED at `29bb45ae…` + README `125e7e02…` (first-hand, 14:10Z)**: the ruling landed as README §"The both-absent `MATCH` (ruling, arc3-loop1-round4)" — "only error-carrying stanzas are `UNEVALUABLE`; a cleanly absent stanza on both sides is `MATCH`", with the weak-witness caveat ("pair an all-absent reference with a present-path reference when the witness is meant to carry content") and the flag alternative recorded as considered-and-rejected. The tool also now **annotates each both-absent row**: `note: both sides record the path absent — the MATCH is an agreement on absence, not a verified presence (declared ruling: …)` (`i2`/`i3` on the after revision) — so the compound case's `MATCH 5/5` is no longer silent. Selftest case `both-sides-absent-is-agreement-match` PASS; error-carrying stanzas still `UNEVALUABLE 14` |

### (d) cross-corroboration detail — the same path, two verdicts

CU-1's d2 shape makes the adjudication's scope concrete: a receipt captured while the
path existed, then the path removed, verifies `MATCH 1/1 compared=11/11 exit=0`
against *itself* (CU-1 `A3b-ghost-ghost.out`) and `ABSENT exit=13` against the live
tree (`A3a-ghost-live.out`). Both readings are consistent with the declared design —
the receipt is a record of a moment, and the comparison's meaning is "do these two
sides agree", not "does this path exist" — but a claim that quotes only the first
number ("verified MATCH") is vacuous for custody. The ruling text should say which
comparison mode a custody claim must quote (`--live`), and that a receipt-vs-receipt
`MATCH` on an absent path is agreement-about-absence, not evidence of custody.

### The compound case (c)+(d) — measured, not inferred

`capture --paths <five absent scratch paths> --out R` → `PARTIAL paths=0/5
exit=13`; then `verify R --live --require-paths 5` → `VERDICT: MATCH paths=5
MATCH=5 exit=0`, every row `MATCH compared=0/11`, `SHA256-CONTRACT: 0/0`;
receipt-vs-receipt identical (`controls i2/i3`, `evidence/before/i2.out`,
`i3.out`). So a reference that (i) passes the coverage gate on stanza count and
(ii) examines **nothing** reads a clean `MATCH 5/5`. This is the strongest
argument for the distinct-path counting fix (c): counting `len(have)` makes the
five-absent reference count **5** — which is why the fix alone does *not* close
this case, and why (d)'s ruling must say what a reference whose paths are all
absent actually asserts. Two admissible rulings, for the parent to pick (both
are documentable; neither is a behavior change):
1. **declared-absence reading**: a path absent on both sides is agreement
   *about absence*; the receipt's `paths: 0 present` header and the capture-side
   `PARTIAL exit=13` are the declared signals, and a `--require-paths` consumer
   must also read the receipt's presence count (an opt-in
   `--require-present N` would make it mechanical);
2. **non-vacuity reading**: a verify whose `SHA256-CONTRACT` denominator is 0
   (or whose compared-field sum is 0 across all rows) is not evidence of
   custody — the ruling states the verdict is `MATCH` only in the class sense
   and names the minimum non-vacuous contract line a claim may quote.
This seat takes no side; the ledger's job is to make the choice explicit and
non-silent, and to record that today the tool's own output distinguishes the
case (`paths=0 present` in the header, `0/0` contract) for any reader who looks.

**After (`29bb45ae…` + README `125e7e02…`) — how the landing resolved it:** the
tool kept the declared-absence reading (option 1) and made it non-silent: every
both-absent row now prints `note: both sides record the path absent — the MATCH
is an agreement on absence, not a verified presence (declared ruling: only
error-carrying stanzas are UNEVALUABLE)` (`i2.out`/`i3.out` on the after
revision), the README carries the ruling as a named section with the
weak-witness caveat and the rejected flag alternative, and a selftest case
(`both-sides-absent-is-agreement-match`) pins it. The compound shape still
reads `MATCH 5/5 exit 0` — that is the declared ruling, not a defect — but the
per-row note means the output no longer lets a reader mistake it for evidence
of presence. The coverage half of the compound case is closed by (c): the
five-absent reference is now counted as **5 distinct** paths (the reference
genuinely carries five distinct paths), so `--require-paths 5` passes on the
count basis *by design*, and the note is what carries the meaning.

### Controls (green at the base, re-run on the landing — all must stay green)

| control | base `7cd19c3c…` | landed `29bb45ae…` |
|---|---|---|
| r3 write guard: `--paths X --out X` | `USAGE exit=2` | `USAGE exit=2` (guard message now names sidecar/neighbour), victim sha `b6a98d9c…` unchanged |
| r3 write guard: hardlink alias as `--out` | `USAGE exit=2` | `USAGE exit=2`, victim unchanged |
| legitimate write beside a measured `.sha256` file | `OK` + sidecar + `MATCH 1/1` (EX-23 control C) | `after-c0` `RECEIPT`+`SIDECAR` `OK paths=1/1 exit=0` |
| distinct-path reference, `--require-paths 5` | `MATCH 5/5 exit=0` | `MATCH 5/5 exit=0` (`after-c7.out`), mixed set `MATCH 5/5` (`i6`) |
| 1-of-5 reference, `--require-paths 5` | `USAGE exit=2` + coverage line | `USAGE exit=2` + `REFERENCE-COVERAGE: 1/5 … unaccounted: <5 canonical>` (`after-c1.out`) |
| `--out ''` | declared `USAGE exit=2` | declared `USAGE exit=2`, new message `--out carries no usable name, so no sidecar path can be derived` (`after-b2.out`) — no traceback |
| fresh parent created | `OK paths=1/1 exit=0` (EX-24 L4) | `OK paths=1/1 exit=0`, receipt + sidecar in the new directory (`/var/tmp/sc3-r4/freshp/`) |
| selftest | `CLEAN cases=22 passed=22 failed=0` | `CLEAN cases=28 passed=28 failed=0` (`after-k1.out`) |
| `selftest --scratch <missing>` | declared `USAGE exit=2` | declared `USAGE exit=2` (selftest internal case, unchanged) |
| receipt self-pin | `# tool: … 7cd19c3c…` | `# tool: custody-pair.py  sha256 29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` (header of `work-after/fixtures/r1.txt`) |
| end-to-end live pair (this seat, scratch) | — | capture `OK paths=5/5 exit=0` then `verify … --live --require-paths 5` → `MATCH 5/5 drift=0 exit=0`; receipt sha `f7a89abd…`, sidecar `78c0db4c…` |

The landing's own new selftest cases (from `after-k1.out`): the four frozen
claim-relevant names —
`coverage-gate-rejects-duplicate-stanzas`, `coverage-gate-passes-distinct-five`,
`refuses-sidecar-over-measured-file`, `refuses-receipt-over-sidecar-neighbour`,
`out-parent-not-a-directory-usage-exit`, `both-sides-absent-is-agreement-match`
— all PASS (six names visible in the tail; the full 28-case list is in the
transcript).

## Cross-seat landing corroboration (EX-21, the implementer)

EX-21's landing package (`claims/c3/EX-21/`) landed after the tool itself; three
independent cross-checks against my artifacts, all first-hand:

- **My harness, run by EX-21 on the landed revision** (`matrix/after-sc3-injections.out`,
  TAG=final, tool `29bb45ae…`, 1343 L): every leg reads the same exit code and
  the same message family as my `evidence/after/summary.txt` (a1 `rc=2` with the
  sidecar/neighbour refusal and `vic.sha256` re-deriving `b6a98d9c…`; b1/b2
  `rc=2`; c3/c5 `rc=2` on the distinct-path basis; c4/c7 `rc=0`; d1 `rc=13`,
  d2/d3 `rc=0`; k1 28 cases). Two seats, two machines' worth of fixtures, same
  matrix. (Their before-run of my harness shows the known path-resolution
  artifact of running it with a relative tool path from inside the fixture dir —
  `python3: can't open file …`; recorded so it is not miscounted as a before
  result. The before-column authority remains my own run.)
- **Their live pair, verified by me, read-only** (`receipts/live-pre.txt`,
  `live-post.txt`, captured-utc 2026-10-19T14:10:24Z, both self-pinning
  `29bb45ae…`): my independent `verify pre post` → `MATCH 5/5 exit=0`; my
  independent `verify post --live --require-paths 5` → `MATCH 5/5 exit=0`; both
  sidecars `sha256sum -c` OK (`7f5a6fd5…`, `2225f866…`).
- **Their selftest** (`selftest/selftest-final-28cases.out`): `CLEAN cases=28
  passed=28 failed=0`, the same count and case names as my run.

The **registry row is patch text, not landed**: `SKILL.md` still carries the
round-3 row (22 cases, no sidecar-guard clause) at line 390, while
`EX-21/patch/proposed-skill-registry-row.patch.md` holds the replacement
(line-neutral, base `5eec51c0…`/390 L → patched `8e56f3d9…`/390 L). The parent
must apply it in the same commit as the tool + README (the frozen claim's
same-commit coupling).

## Named residuals (not hidden, not claimed as closed)

- **R1 — RESOLVED at the landing; the trap is recorded.** The half-fix shape
  (spelling A closed, B open — EX-23's measured variant) did not land: both
  spellings refuse at `29bb45ae…`, with victim bytes re-derived intact and no
  `X.sha256.sha256` created. RV-7's attack-1 trap (a naive eager sidecar-name
  computation breaking the `--out ''` control) is also avoided: `--out ''` keeps
  its declared USAGE class with a named message.
- **R2 — RESOLVED at the landing.** `--out` under a fresh parent still captures
  (`OK paths=1/1 exit=0`); the directory-creation failure reads the declared
  USAGE class, not a traceback. The EX-24 `flag-only` variant's L4 regression
  (refusing a fresh parent) did not land.
- **R3 — OPEN, by design, as a scope statement.** Distinct-path counting makes
  padding visible; it does not make the *coverage claim* true: a reference of
  five **distinct non-canonical** paths still passes the gate (measured on both
  revisions — `i6.out` before, `i6` after). The r3 verdict already named this
  ("the other four custody paths unexamined"); the optional identity gate
  (`--require-custody-set`) in EX-24's patch text remains the stronger form and
  is **not** in the landed claim's scope. A future round that wants
  `--require-paths 5` to mean "the canonical five" must add it.
- **R4 — RESOLVED: the after-column is now landing-measured.** The landing
  arrived at 14:09:30Z (caught by the 15 s watcher); every AFTER cell above was
  re-measured by this seat against `/var/tmp/sc3-r4/after-base/custody-pair.py`
  (copy sha `29bb45ae…`, re-derived three times). The README moved twice inside
  the landing window (`f30df42e…` → `91fd386b…` → `125e7e02…`) while the tool
  digest stayed fixed; the parent re-derives the settled pair at the commit
  point (rule #14).
- **R5 — the same-commit coupling is the parent's.** The registry row in
  `SKILL.md` is still the round-3 row at draft close (the replacement is patch
  text: `claims/c3/EX-21/patch/proposed-skill-registry-row.patch.md`, line-
  neutral); the round's own live pre/post pair (EX-21, both receipts self-pinning
  `29bb45ae…`, captured 14:10:24Z) verifies `MATCH 5/5` plain and gated under my
  independent run, with both sidecars `sha256sum -c` OK. Applying the row and
  landing the pair in the same commit as the tool + README is the parent's step.

## Evidence index (each pointer is a file in `claims/c3/SC-3/`)

- Harness: `harness/injections.sh` (a1/b1/b2/c0–c7/d1–d3/k1–k2).
- BEFORE: `evidence/before/summary.txt` (one line per leg: id, rc, head);
  per-leg `before-<id>.out`/`.rc`; `evidence/before/controls-summary.txt`
  (g1/g2, i1–i9); receipts kept: `dupe5.txt` (5× duplicate v2 stanzas),
  `ghost-receipt.txt` (both-sides-absent), `vic.sha256` (post-clobber state);
  `evidence/before/SHA256SUMS`.
- AFTER (landing `29bb45ae…`): `evidence/after/summary.txt` + per-leg
  `after-<id>.out`/`.rc`; `evidence/after/controls-summary.txt`; the compound
  case's annotated rows (`i2`/`i3`) and the padded v1 pipe refusal
  (`after-pipe.out`); the fresh-parent control under `/var/tmp/sc3-r4/freshp/`;
  the end-to-end live pair `live-pre.txt` + `.sha256` (receipt sha `f7a89abd…`).
- Simulation (§3): `evidence/sim/census-{base,records,control}.out` +
  `SHA256SUMS`.
- Raw scratch tree: `/var/tmp/sc3-r4/{base,after-base,work,work-after,ctl,ctl-after,watch,sim}`
  (copies here are byte-equal; `sha256sum -c` in the evidence dirs).
- Identity record: `/var/tmp/sc3-r4/identity.txt` (base pair, python, tz).

## Notes for the parent

- The ledger's "declared class" column cites the *declared* exit map (landed
  README §Exit codes); three of the four cells are classes the map already
  defined, and (d) is an adjudication landed as README text plus a per-row
  annotation — not a new code class.
- The frozen claim's phrase "the three injections reproduce as their declared
  classes (before: measured residuals)" is satisfied by this file's before
  column; the after column is now landing-measured (R4 resolved) — the parent
  re-derives the identities at the commit point, because the README moved twice
  inside the landing window while the tool digest stayed fixed.
- The Controls table is the regression net this ledger offers: every leg was
  green at the base and re-measured green on the landing.
- The one residual this ledger deliberately leaves open is **R3** (the gate
  still does not assert the canonical set) — it is a scope statement, not a
  defect, and it should survive into the records rather than be smoothed away.
