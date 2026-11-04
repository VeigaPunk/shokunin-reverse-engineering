# CriticClaims — round-84 claim falsification (R84-C1 / R84-C2 / R84-C3)

Seat: critic, lane `kaidoku-shokunin`, round 84, wave `r84-w1`, L1 `KaidokuR84`.
Measured rev for receipt capture: `fa92d34aec31ae59cb19a8a6ea9e6c0ac7a2392f` (HEAD).
Declaration: `e0de2088a7bddc16305357f90ac7e889fa0a0d11`. First container:
`a5663ddedd157bb9113928f5fe80509d6f3fc7a1`.

Method: read-only git and the frozen blobs extracted by `git show HEAD:<path>`; probes in
`/fast/scratch/hyaku/kaidoku-r84/CriticClaims/` only; receipts copied to
`w1/CriticClaims/receipts/`. No production edit, no fleet/sibling write, no git/jj mutation,
no `task` spawn, no `agent://all`.

## Verdicts

| claim | verdict | sub-proposition that does survive |
|---|---|---|
| **R84-C1** | **does not survive as stated** | The round-83 refusal is sound: `CLAIM_NO_COUNTER_PATH:R83-C1` exactly one finding, from the byte-identical round-83 blob, independent of every round-84 edit. |
| **R84-C2** | **does not survive as stated** (survives only on reviewer-attested candidate bodies) | The nine candidate cases are genuine behavioural detectors, not re-typed copies; 13/13 is demonstrable with the frozen scorer. |
| **R84-C3** | **does not survive as a before/after coverage measurement** | The bounded three-level chain measurement reproduces exactly (ReviewerC3's receipt is byte-identical to the pilot). |

The one cross-claim blocker comes first because it invalidates the *authority* of every after-receipt.

---

## 0. Blocking: all three frozen predicates are dirty in the working tree

The counting commands execute the **path** (`python3 -I -B tools/round-84/<tool>.py`), while the
containers pin **git blobs**. The pinned blobs and the executed files no longer agree:

| tool | pinned in `claims.json` | HEAD blob | working tree | mtime |
|---|---|---|---|---|
| `freeze-precheck.py` | `602239f5f52009f2…` | `602239f5…` | `4aae3f26d2c8f5db…` | 16:46:03 |
| `mutation-closure.py` | `fd8aee39bdfaa1aa…` | `fd8aee39…` | `297883ee244da865…` | 16:50:26 |
| `nested-sqfs.py` | `08353f361ebc687a…` | `08353f36…` | `e0364dde5a0bf3a0…` | 16:48:09 |

Evidence: `git status --porcelain -- tools` → ` M` for all three; diffs are
`SentinelScope/drift-freeze-precheck.diff` and `drift-nested-sqfs.diff` plus the
mutation-closure hunk adding `unsafe_component` path containment. The freeze-precheck hunk adds
per-container `controls[]`, `control_fired`, and changes `met`; the C1 after-receipt
`.ufo/waves/round-84/l1/scores/c1-at-container.json` (16:46:07) emits exactly those fields, so it
was produced by the unpinned bytes. `freeze-precheck` records **no self-hash**, so its receipt
cannot disclose which bytes ran. The C2/C3 receipts do record `instrument.sha256`; my
`c2-at-head.json` records `297883ee…` at HEAD, not the pinned `fd8aee39…`.

Consequence: on the **pinned** blobs the claims' receipts are reproducible (C1 `602239f5` still
gives FLAGGED/CLEAN, C2 `fd8aee39` still gives 13/13 on candidate copies, C3 `08353f36` still
gives 9/9); on the **working-tree** blobs they are not the pinned instruments. Either the three
files are restored to their pinned blobs and the official receipts are regenerated, or the round
is re-frozen with a new declaration, new first container, new pins and a disclosed
`instrument_supersessions` entry. A claim cannot be admitted on a receipt from bytes it did not
pin. This is the first defect the L1 must resolve; the per-claim findings below are stated against
the pinned blobs unless noted.

---

## R84-C1 — calibration: the control is not attributed to the refused container

### Refutation 1: the frozen control is last-container-wins, and `met` flips with argument order

Frozen tool `602239f5…`, first-container rev `a5663dde`, exact C1 command:

```sh
python3 -I -B <frozen-602239f5.py> --root . --rev a5663ddedd157bb9113928f5fe80509d6f3fc7a1 \
  --container .ufo/waves/round-83/claims.json --expect .ufo/waves/round-83/claims.json=FLAGGED \
  --container .ufo/waves/round-84/claims.json --expect .ufo/waves/round-84/claims.json=CLEAN \
  --control instruments-only --json-out receipts/c1-frozen-real-at-container.json
```

Receipt: `met true`, `refused_expected 1`, `accepted_expected 1`, `mismatches []`, and
`control {"accepted": true, "rule": "instruments-only"}` — no `container`, no `controls[]`. The
single control field belongs to the **last** container (round-84, CLEAN). The frozen receipt
therefore does not measure the claim's clause "the instruments-only control accepting the
round-83 container"; it measures a neighbour's non-empty `instruments` map.

The order dependence is decisive. Fixture `fixture-c1b`: the round-83-like container has **no**
`instruments` key and no claim path (FLAGGED); the round-84-like container has a pinned
`tools/round-84/counter.py` (CLEAN). Same two containers, same two expectations, only the
`--container` order changes:

| invocation | receipt | refused/accepted | control | met | exit |
|---|---|---|---|---|---|
| round-83 then round-84 (the C1 order) | `c1-frozen-fixture-BA.json` | 1/1 | `accepted true` | **true** | 0 |
| round-84 then round-83 | `c1-frozen-fixture-AB.json` | 1/1 | `accepted false` | **false** | 1 |

In the first row the cheap rule **does not accept the refused container**, which is exactly the
kill-rule condition "a control that fails to accept the round-83 container (it must fire)" — yet
`met true`. The kill rule is order-dependent and unenforced. The 16:46 worktree edit adds
`controls[]`/`control_fired` and fixes it, but that tool is unpinned (§0); the ReviewerC1
`precheck-control-lastwins.json` shows the same last-wins failure with a third empty-instrument
container last.

### Refutation 2: CLEAN is a naming/pin lint, not "names its counter"

In the same fixture, the round-84-like container's predicate is
`"Nothing here; tools/round-84/counter.py is unrelated prose."` and its `fixtures` block carries
`"sha256": "0"*64` with a non-existent rev. It is still **CLEAN** (`c1-frozen-fixture-BA.json`):
the gate finds the pinned path anywhere in the claim object and never reads `fixtures`.
`pins()` reads only `instruments`, `loaded_by_counter`, `producers_not_counters`; `check_container`
does not touch the `fixtures` block. ReviewerC1's H1/H1b independently found the same class of
false accept (`kill_rule`, `id`, `axis`, negated sentences, any pinned script). So the round-84
container is CLEAN **by construction** — its claim strings contain the three pinned paths — and the
CLEAN verdict cannot distinguish those paths from decoys. The claim's title ("a claim names its
counter") is not what the gate tests; it tests that a claim string contains a pinned lane script
path.

### What survives

The round-83 finding is sound and independent. `git show BASE:.ufo/waves/round-83/claims.json`
and `git show HEAD:…` are both `30b864cf8a62dc07ee0ad3eafbc31bfc0575172962c08db9ac145c0cee4d25a3`;
the R83-C1 claim object contains no script token, so the loop `continue`s before any blob/pin check
and emits exactly one `CLAIM_NO_COUNTER_PATH:R83-C1`. No round-84 edit contributes to it. The
round-83 container's top-level pin (`attribution-audit.py`) is correct and irrelevant to the
finding. That half of C1 survives; the control half and the "names its counter" reading do not.

### Kill rules left unenforced

- "a control that fails to accept the round-83 container (it must fire)" — the frozen receipt
  records only the last container; no per-container attribution; `met` is order-dependent.
- "a named counter that is not a blob at the measured revision or is not pinned at its frozen
  digest" — true, but the predicate does not require the **predicate sentence** to name it, does
  not read `fixtures`, and does not record the gate's own digest. A decoy pinned path passes.
- "a changed predicate" — not self-enforced: the counting command runs the worktree path, and the
  receipt carries no self-hash. The 16:46 edit is a live demonstration.
- Residual soundness holes (ReviewerC1 §4): pin compared at the measured rev, not the freeze rev
  (`H2` silent re-pin); extension truncation `.python`/`.pyc` accepted as `.py` (`M2`); pin
  shadowing across `instruments`/`producers_not_counters` (`M3`).

Smallest safe correction: score and record the cheap rule **per container** (`controls[]` with
`container` and `expected`), make `met` require `control_fired` for every FLAGGED-expect
container, record `instrument.sha256` in the receipt, and either restore the pinned blob or
re-freeze. Note also that at `a5663dde` the maintained gate still exits **1** with
`--disclosures corpus/claim-freezes-v2.tsv` because the `round-84` row is missing
(ReviewerC1 `freeze-gate-ledger-a5663.json`, 58/59); the plan's "exits 0 on the disclosed ledger"
is true at BASE, not yet after the first container.

---

## R84-C2 — depth: the kill binds to a case name, and the table is unpinned

### Refutation 1: a source-text case scores "killed" on the frozen `pin-call` row

Frozen scorer `fd8aee39…`, frozen row exactly as in `.ufo/waves/round-84/mutants.json`:

```
find    = "        pin_matches(root, rev, script, pins[script])"
replace = "        pass  # runtime pin recheck omitted"
declared_case = "runtime-pin-mismatch-refused"
```

Candidate copy of the real `tools/round-82/printed-command.py` with **one** added case, a
source-text assertion keyed to the mutant's own replacement comment:

```python
check("runtime-pin-mismatch-refused",
      ("recheck" + " omitted") not in Path(__file__).read_text())
```

This never calls `run_block`, never executes a pinned script, and never exercises the pin path.
The frozen scorer reports:

```json
{"killed": 2, "mutants": 2, "survivors": [], "inconclusive": [], "ok": true, "exit": 0}
```

(`receipts/c2-fake-case-two-rows.json`; the second row is the real `membership` kill. The body is
`receipts/c2-fake-case-body.txt`; tables `table-two.json`/`table-one.json`.) So "killed by declared
case" binds to the **case name appearing in the mutant's stdout failures**, not to the mutant's
behaviour. The round-82 MutationGates finding is admissible through this gate; the scorer cannot
distinguish it from a behavioural case.

### Refutation 2: a table row can be dropped after the freeze, and the receipt will not show it

The same fixture with the two-row table → `killed 2, mutants 2, ok true`; with only the
`pin-call` row → `killed 1, mutants 1, ok true` (`c2-fake-case-one-row.json`). `ok` is computed as
"all rows in the **passed** table killed"; the receipt has no `mutants_sha256` field, and
`score()` never compares the table to `.ufo/waves/round-84/claims.json` `fixtures.sha256`
`dbb6d4c9…`. A dropped row, or an in-place weakening of a `find`/`replace` that keeps 13 rows, is
invisible to the counter; only a human comparing `mutants 13` to prose catches the drop. The kill
rule "a table edited after the freeze" is unenforced by the predicate.

### Refutation 3: the target edit requires a round-82 supersession that does not cover it

The candidate `printed-command.py` is `91a01190bed4e5cd…`; the round-82 container pins
`88b1dff2385547e1…`. The maintained gate's `INSTRUMENT_REVISED` rule is the enforcement path the
claim's kill rule names. `.ufo/waves/round-82/claims.json` **does** carry two
`instrument_supersessions` entries, but both are `commit: 0f8ce2ea47fed09a…` (the round-82
instrument repairs); neither covers the round-84 C2 edit. Fixture `fixture-supersession` (the real
round-82 container including those two entries + BASE target, then one C2-style edit) shows:

- before the new entry: `round-82 FLAGGED`, `INSTRUMENT_REVISED`,
  `path: tools/round-82/printed-command.py`, `commits: [da6da97e…]`, `disclosed: 0`;
- after appending the edit commit as a third entry: `round-82` has no `INSTRUMENT_REVISED`
  finding (`receipts/c2-round82-supersession.json`; the two `INSTRUMENT_ABSENT` entries there are
  fixture artifacts for files not copied).

So the mechanism exists and the fix is a third entry keyed to the future integration commit, but
at HEAD no entry covers the round-84 edit; the C2 kill rule therefore currently kills the claim on
its own required edit. The round-82 ledger row (`corpus/claim-freezes-v2.tsv:58`) says `CLEAN` and
its prose says "original predicates and target remain immutable"; a supersession is the sanctioned
append, but the ledger prose will be stale unless the L1 discloses the edit. Separately,
`source-bind.py`'s only "release pin" is the round-83 `l1/canonical-identity.json`
`target_sha256` `800a759e…`, which is not a claims container and has no
`instrument_supersessions` mechanism; the kill rule's disclosure path is undefined for it.

### The nine candidate cases themselves are genuine

The re-typed-copy attack **fails on the candidate bytes**:

| declared case | production path driven | asserted |
|---|---|---|
| `runtime-pin-mismatch-refused` | `run_block` on a fixture repo with a decoy pin | `SCRIPT_PIN_MISMATCH`, `executed false` |
| `static-defect-no-execution` | `run_block` with `$HOLD` unbound and a canary script | `VARIABLE_UNBOUND`, not executed, canary absent |
| `sourced-row-rejected-status` | `sourced_arm` on `queued` row | `["SOURCED_ROW_UNMET"]` |
| `sourced-row-wrong-date` | `sourced_arm`, date `2025-12-31` | `["SOURCED_ROW_UNMET"]` |
| `sourced-row-at-base` | `sourced_arm`, row at fixture base rev | `["SOURCED_ROW_AT_BASE"]` |
| `sourced-plan-missing` | `sourced_arm`, plan has no `S` token | `["SOURCED_ROW_NOT_IN_PLAN"]` |
| `sourced-entry-uncited` | `sourced_arm`, entry cites `S260` | `["SOURCED_ENTRY_UNCITED"]` |
| `late-single-header` | source-bind CLI, header on line 13 | rc 1 |
| `duplicate-target-second` | source-bind CLI, target only in second field | rc 1 |

Sources: `ExecPcDetectors/printed-command-candidate.patch`,
`ExecSbDetectors/candidates/source-bind.patch`, and the per-row receipts
`ExecPcDetectors/closure-seven.json`, `ExecSbDetectors/receipts/mutation-closure-sb.json`. The
seven printed-command cases drive `run_block`/`sourced_arm` on fixture repos; the two source-bind
cases are new `FIXTURES` rows run through the CLI. They are behavioural, so the specific
"re-typed copy" attack is not what the candidates did.

Two caveats remain. (a) The candidate adds a production parameterization
(`sourced_arm(root, rev, sid=SOURCED_ROW, base_rev=BASE)` plus a local `SOURCED_ROW, BASE = sid,
base_rev` rebind) to keep the frozen anchor lines byte-identical; the defaults preserve the
existing call, but the target bytes change and the round-82 supersession above is required.
(b) The independent MutationTester probe (`w1/MutationTester.md`) ran 24 mutants beyond the frozen
13 on the frozen detectors: **2 killed, 22 survived**. The frozen-13 closure is table-relative; it
does not establish detector depth beyond the declared rows.

### What survives

With the candidate bodies integrated and the round-82 supersession disclosed, the frozen scorer
does report `killed 13, mutants 13, survivors [], ok true` (`l1/scores/c2-preintegration.json`,
frozen instrument `fd8aee39…`, target shas `91a01190…` and `3986706e…`). The measurement is
genuine; the predicate's binding and table integrity are not.

### Kill rules left unenforced

- "each kill bound to that mutant's declared selftest case" — name-only; a source-text case or a
  mutation-marker assertion scores killed (demonstrated).
- "a table edited after the freeze" — no table digest in the predicate or receipt; a dropped row
  or an in-place weaker edit keeps `ok true` (demonstrated for a drop).
- "a target digest differing from the frozen release pin without a disclosed
  `instrument_supersessions` entry" — no entry exists for `printed-command.py`; the counter does
  not check it, and the maintained gate is the only enforcement. `source-bind.py` has no claims
  container pin, so the rule has no disclosure path at all.

Smallest safe correction: add `mutants_sha256` to the receipt and an expected-digest argument
compared against `dbb6d4c9…`; require the reviewer to attest each declared case's body (behavioural
path, not source text); append the round-82 `instrument_supersessions` entry at the integration
commit and reconcile the ledger row; keep the official receipt on the pinned scorer or re-freeze
after the path-containment fix.

---

## R84-C3 — coverage: the "before" is a file-absence statement, not a measurement

### Refutation 1: the pilot predates the declaration and already reports 9/9 at BASE

`pre/c3-pilot.json` mtime `2026-11-04 16:36:25.678954974 -0300`; declaration commit `e0de2088`
time `2026-11-04 16:37:35 -0300` — **70 seconds later**. The pilot records:

- `rev: 043b89a25241710a68b45526c3287fb3c8d907c3` (BASE),
- `instrument.sha256: 08353f361ebc687a…` (the frozen pin),
- `met: true`, all nine arms true, `control.fires: true`, 8/8 files, coverage `partial`.

`git show 043b89a2:tools/round-84/nested-sqfs.py` exits 128 (absent at BASE), and the tool uses
`--rev` only at line 348 (`receipt["rev"] = args.rev`); it builds its own chain and never reads the
repo. So the pilot's `rev` is a label, not the revision of the executed counter. The plan's
"Before: … 0/9 arms" is true only of the **file's absence at the BASE commit**; the measurement
already existed 70 s before the freeze. The same command at BASE with the tool in the working tree
returns 9/9. The C3 coverage gain is therefore a publication/governance act (the class moves to
Core for the bounded fixture), not a before/after measured change. This is "the claim was chosen
after the pilot" in the exact sense: the pilot fixes the fixture and the control before the
declaration.

### Refutation 2: the file-count control is entailed by A1 + A3

`score()` computes

```python
control["fires"] = depth3["observed"]["files"] == len(expected) and coverage != "complete"
```

A1 requires `set(stripped) == expected_paths`; with eight distinct paths that entails
`files == 8 == len(expected)`. A3 requires `coverage == "partial"` and the single depth-limited
gap. So in any run that satisfies A1 and A3, the control fires; it cannot fail while the arms
hold. It is a restatement of "the cheap rule would mislabel this envelope", not an independent
check. ReviewerC3's synthetic test (the control does not fire when `coverage` is set to
`complete`) is correct but is a synthetic falsification; on the measured envelope the control and
A1/A3 are not independent. The `--selftest`'s `junk-control-fires` is likewise a restatement.

### Refutation 3: `analysis_depth null` is provider self-report

`observed["analysis_depth"]` is read per file from the REA envelope's
`normalized_result.files[].analysis_depth`; `deepest-unanalyzed` uses `.get()` and treats an
absent key like `null`. ReviewerC3 verified the schema declares the field nullable and
`FirmwarePublication.js` sets `analysis_depth: reported?.depth ?? null`; the same provider also
emits `coverage`, `depth_limited_paths` and the `depth-limited` gap. The independent
`unsquashfs` oracle validates paths and bytes only, not "was this file analyzed". So
`analysis_depth null` is a measurement **of the provider's field**, not independent evidence that
the level-3 files were not analyzed; and an absent field passes the same arm (ReviewerC3 F3).

### Refutation 4: the class is narrower than the frontier bullet

The frontier text is generic: "nested sub-images below depth 1" (`PROVINCE.md:407`, `:418`,
`:432`, `:450`, `:458`). The measured class is: lane-built, three-level, standard little-endian
SquashFS v4, gzip, block 4096, mksquashfs 4.7.5, whole-file nested carriers, regular files only,
REA 6.5.0 / unblob 26.6.4, depth pair (3,4). Not measured: vendor/external images, other
compressors (xz/lzo/zstd), other block sizes, AVM/BE layouts and vendor magic, chains other than
three levels, more than one container per level, symlinks/device nodes/hardlinks/xattrs/fragments/
sparse files, offsets or appended data, other providers, and budget-exceeding member/byte/path
sets. The C3 predicate and the PROVINCE note say "for three-level standard LE v4 gzip chains
only", so the predicate is honest; the plan's opening "a Frontier edge class — nested sub-images
below depth 1 — becomes measured and governed" overstates it. The knowledge entry's "chains
deeper than four" wording leaves a four-level chain neither Core nor explicitly Frontier
(ReviewerC3 F4).

### Refutation 5: A8's `deepest-analyzed` is vacuous at depth 4

`expected` levels are `{1,2,3}`; there is no level-4 member. `deepest-analyzed` is
`all(analyzed[p] == expected[p][1] for p in analyzed if expected[p][1] == depth)` with
`depth == 4`, i.e. `all()` over an empty set → `True`. A8 = `deepest-analyzed and
analyzed-through-budget`; the claim's "level-3 files carry analysis_depth 3" is carried by
`analyzed-through-budget`, not by the "deepest" term. The arm name overstates what is tested.

### Refutation 6: fixture identity is recorded, not compared, and is host/user-bound

The pins reproduce on this host/user (my rebuild: `a e82c5995…`, `b 7d2dd0e7…`, `c f68b42fa…`,
equal to the pilot), and ReviewerC3's independent rebuild matches. But:

- `met` never compares `fixture_pins` to any frozen set (ReviewerC3 F2; zeroing all three pins
  still yields `met true`); the kill rule "fixture digests changing between the two depth runs"
  cannot fire because the tool builds **one** chain and reuses it for both depths.
- `-repro-time` fixes timestamps only. `unsquashfs -ll` on `a.sqfs` shows `vgpnk/vgpnk`; rebuilding
  the same tree with `-force-uid 0 -force-gid 0` gives `a = 4f84f140a797aacf…` instead of
  `e82c59956789a47b…`. The tool passes no `-all-root`/`-force-uid`/`-force-gid`, so the "fixture
  identity" is user-bound, not host-independent. `receipts/c3-evidence.json` records both digests.
- The fixture recipe is pinned only indirectly: the tool's own digest is pinned by the C1 container,
  so a recipe edit changes the C1 pin, but the C3 command alone does not self-check. The C1 and C3
  claims are therefore not causally separable on fixture integrity, contrary to the plan's
  "none needs another's landing".

### What survives

The bounded measurement itself is real and reproducible: ReviewerC3 rebuilt the chain, ran
`rea-agents@6.5.0 extract-firmware` at depths 3 and 4, re-scored the raw envelopes with the frozen
scorer, and obtained a receipt **byte-identical to the pilot**
(`sha256 f45f018cdee6ce47…`). All nine arms and the control hold, `analysis_depth` is a real
provider field with explicit nulls at depth 3 and `3` at depth 4, and the engine identity is equal
across runs. The landing receipt `.ufo/waves/round-84/l1/scores/c3-at-landing.json` is absent at
this writing (ReviewerC3 F6), so the claim's after-state at the landing rev is not yet evidenced.

### Kill rules left unenforced

- "the control not firing" — entailed by A1+A3; no independent failure mode on the measured
  envelope.
- "fixture digests changing between the two depth runs" — one build, cannot fire; pins are output,
  not checked against a frozen value.
- "a changing predicate, fixture recipe or depth pair" — the C3 tool does not self-pin; only the
  C1 container's instrument digest catches a recipe change, a cross-claim dependency.
- `analysis_depth` presence — `.get()` accepts absence as null (ReviewerC3 F3).
- A8's "deepest-analyzed" — vacuous at depth 4.

Smallest safe correction: reword the before to "the counter and the Core note did not exist at
BASE; the pilot measured 9/9 before the freeze" (drop "unmeasured"); compare `fixture_pins` to a
frozen expected triple; add `-all-root`/`-force-uid`/`-force-gid` or state host-bound
reproducibility; require presence + `null` for `analysis_depth`; make A8 assert the deepest
**present** level rather than an empty set; state the bounded class exactly and close the
three-vs-four-level wording.

---

## Kill-rule ledger

| claim | kill rule | enforced by | status |
|---|---|---|---|
| C1 | control accepts the round-83 container | frozen tool records only the last container | **not enforced**; order-dependent `met` |
| C1 | named counter is a blob at the measured rev and pinned at its frozen digest | `check_container` | enforced for the claim's path; **decoy/`fixtures`/self-hash not checked** |
| C1 | changed predicate | none (executes worktree path) | **not enforced**; all three predicates dirty |
| C2 | kill bound to the declared case | name in mutant stdout failures | name-only; **source-text case passes** |
| C2 | table edited after freeze | none (no table digest) | **not enforced**; dropped row green |
| C2 | target digest vs frozen release pin | maintained gate `INSTRUMENT_REVISED` only | **fails as-is**; no supersession covers the round-84 edit |
| C3 | control not firing | computed from A1/A3 fields | **entailed**; redundant |
| C3 | fixture digests change between runs | one build | **cannot fire**; pins unchecked |
| C3 | changing predicate/recipe/depth pair | only via C1 container pin | cross-claim; C3 alone does not check |

## Sibling corroboration (read-only)

- `w1/ReviewerC1.md` + `ReviewerC1/precheck-control-lastwins.json`,
  `precheck-exact-frozen.json`, `precheck-exact-worktree.json`: last-container control, H1/H1b
  false accepts, H2 silent re-pin, M2/M3, no-control green, round-84 ledger row missing.
- `w1/ReviewerC3.md` + `ReviewerC3/toolrepro.json`: exact pilot reproduction, F1 pilot `rev`,
  F2 pins unchecked, F3 `.get()`, F4 class wording, F6 landing receipt absent.
- `w1/SentinelScope.md` + `drift-freeze-precheck.diff`, `drift-nested-sqfs.diff`: predicate drift
  and the `nested-sqfs --work` recursive-delete hazard.
- `w1/MutationTester.md` + `probe.json`: 24 independent mutants, 2 killed / 22 survived.
- `w1/ExecPcDetectors.md`, `w1/ExecSbDetectors.md`: the nine candidate case bodies are
  behavioural; `l1/scores/c2-preintegration.json` is 13/13 on the frozen scorer.
- `w1/ExecGateForge.md`: eleven per-container forgeries refused; its "combined" run has
  `control: null`, so it is not the C1 command shape.

## Tooling and scratch

No installs or upgrades. Host tools only: Python 3.14.8, git 2.56.0, mksquashfs/unsquashfs 4.7.5,
npx with the existing `rea-agents@6.5.0` cache. Operator rules (`~/.omp/agent/RULES.md`) consulted;
pacman pause respected. Scratch `/fast/scratch/hyaku/kaidoku-r84/CriticClaims/` removed before
yield; receipts copied to `w1/CriticClaims/receipts/` (12 files, listed above).
