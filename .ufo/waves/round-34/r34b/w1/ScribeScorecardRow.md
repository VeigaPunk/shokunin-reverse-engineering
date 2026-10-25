# ScribeScorecardRow — R34-C2 SCORECARD row and Round-34 C2 paragraph (drafts)

Seat: `L1Kaidoku34-2.ScribeScorecardRow` (leaf, no subagent dispatch, no lane VCS write).
Prompt read first: `.ufo/waves/round-34/r34b/w1/prompts/ScribeScorecardRow.md` (first bytes `/skill:godspeed` + the verbatim directive).
Claim under attack: **R34-C2** (capability acquisition, axis depth), frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Inherited **R34-C1** (GNU version-needs) stayed stopped throughout: its production reader, its twelve carriers and its counter were **not executed, not read as programs and not scored** by this seat. The only `tools/round-34/version-needs-counter.py` touched at all is the one the C2 counter does *not* invoke; I did not invoke it.
Mode: read-only verification on copies. Every write is under `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeScorecardRow/` or this report. Lane VCS was read with `git rev-parse` / `git show` / `git cat-file` / `git ls-files` / `git status` / `git check-ignore` only. `python3` = `/usr/bin/python3` (3.14.8). No tool installed or upgraded, so no tooling record beyond §9.

Run window (UTC): 2026-10-25T07:18:49Z → 2026-10-25T07:23:42Z. Host local zone America/Sao_Paulo (-03); all times below are UTC.

Result in one line: the production receipt and all five controls reproduce **line-for-line and byte-for-byte** on a copy, all 26 pins match at the freeze commit, and two new gate-layer bypasses (a mislabelled shortcut class; a counter that selectively under-reports `met_target`) each yield `REPLAY_GATE_CLEAN` while a shortcut reader is at 8/8. None of the six frozen clauses is affected; both are draft-disclosure material, not claim changes.

---

## 0. Axes named (Godspeed)

| axis | proxy used here | direction | kept move |
|---|---|---|---|
| A1 receipt fidelity | byte equality of my recount vs the cited after-receipt | identical = better | §3 (0 differing keys) |
| A2 clause arithmetic | all six clause booleans re-derived from stored fields | more agreement = better | §4 |
| A3 falsifier reach | does the gate's own stated guarantee survive probes it does not cover? | more surviving holes found *and* classified = better | §5 S1/S2/S3 |
| A4 custody | are cited receipts anchored to a revision? | anchored = better | §5 S6/S7 |
| A5 draft fit | does the row/paragraph assert only what ran, at the right column/axis? | no overclaim = better | §6, §7 |

Cheap parallel iterations that were kept: recount (2.7 s), five control replays (~11 s), four gate probes (~2 s), five green + three red stability runs (~10 s), per-reader scoring (~2.5 s). No move was made at the cost of another axis: nothing below edits an instrument, claim, target, class or receipt.

---

## 1. Environment and inputs

| input | path | sha256 / state |
|---|---|---|
| frozen claim record | `.ufo/waves/round-34/r34b/claims.json` | `de3afbfb61d70fee177392b256719bb665ad07d999303999381442120facd828`; worktree bytes **equal to the blob in `c79bbe7b`** (`git show c79bbe7b:.ufo/waves/round-34/r34b/claims.json \| sha256sum`) |
| production receipt | `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` | `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` |
| before receipt | `.ufo/waves/round-34/r34b/before/c2-at-base.txt` | `b512cfc25d401c31a16dd4a4dd977a19c7252fd6b4a4d26f56af2de73bc19c2b` |
| controls (5 JSON + 5 TXT) | `.ufo/waves/round-34/r34b/controls/` | `do-nothing.json` `bce6aa9f…`; `gate-always-clean.py.json` `22f819c4…`; `gate-junk-clean.py.json` `25485cb9…`; `gate-no-positive-check.py.json` `50516d79…`; `gate-vacuous-no-floor.py.json` `a12f720d…` |
| control gate mutants | `.ufo/waves/round-34/r34b/controls/gates/` | `gate-always-clean.py` `fbb2eca6…`; `gate-junk-clean.py` `777013c2…`; `gate-no-positive-check.py` `d0b03f1b…`; `gate-vacuous-no-floor.py` `0646a3df…` |
| lane instruments | `tools/round-34/{replay-gate.py,c2-shortcut-gate-counter.py,gate-config-mini.json,gate-config-naive.json}` + `mini-fix/**` | 26/26 pins, §2 |

Read-only git facts: `git rev-parse HEAD` → `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; freeze commit committer time **2026-10-25T07:13:11Z** (message: "round-34: freeze R34-C2 pre-freeze shortcut-replay gate (instruments, eight synthetic fixtures, seven shortcut classes, red and green configs) before any production run"); `git status --porcelain tools/round-34` → 0 lines.

---

## 2. Pin verification — 26/26 at the freeze

Method: for each `claims[0].pins` entry, sha256 of the worktree file **and** of `git show c79bbe7b:<path>`, compared to the declared digest. Full ledger: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeScorecardRow/pins.txt`.

`TOTAL=26 OK=26 MISMATCH=0` — every declared digest equals both the worktree bytes and the freeze blob. Load-bearing five:

```
8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558  tools/round-34/replay-gate.py
41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72  tools/round-34/c2-shortcut-gate-counter.py
4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c  tools/round-34/gate-config-mini.json
72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428  tools/round-34/gate-config-naive.json
43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52  tools/round-34/mini-fix/mini-counter.py
```

The eight fixtures are 512-byte static files, mode `0644`; they were never executed. Nine readers exist and are executed only as `python3` children of a counter.

Independently corroborated (not re-derived by me): `w1/RevClaimsVsInstruments.md` §1 reports the same 26/26; `w1/ExecRecountC2.md` §2 reports 26/26 on a fresh clone.

---

## 3. Independent reproduction — production receipt and five controls

Copy (not clone) of `tools/round-34` into scratch, hashes re-checked equal to the pins, then:

| # | UTC | command | exit | outcome |
|---|---|---|---|---|
| P1 | 07:18:49Z | `/usr/bin/python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <SCRATCH>/root --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out <SCRATCH>/c2-recount.json` | **0** | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` |
| P2 | 07:18:49Z | recursive leaf diff of `c2-recount.json` vs the cited after-receipt | 0 | **DIFF_KEYS: []** — 30 leaves equal; `clauses`, `red`, `green` equal; same sha256 `da78f444…` |
| P3 | 07:20:27Z | counter `--gate controls-gates/gate-always-clean.py` | 1 | `GATE_COUNTER_MISS … selftest_failures=2 mutants_killed=3 red=REPLAY_GATE_CLEAN green=REPLAY_GATE_CLEAN clauses_failed=red_refused,selftest_clean` — equal to stored line |
| P4 | 07:20:32Z | `--gate controls-gates/gate-junk-clean.py` | 1 | `… selftest_failures=0 … clauses_failed=red_refused` — equal |
| P5 | 07:20:35Z | `--gate controls-gates/gate-no-positive-check.py` | 1 | `… mutants_killed=2 … clauses_failed=mutants_killed,selftest_clean` — equal |
| P6 | 07:20:38Z | `--gate controls-gates/gate-vacuous-no-floor.py` | 1 | `… selftest_failures=1 … clauses_failed=selftest_clean` — equal |
| P7 | 07:20:38Z | `--gate tools/round-34/absent-gate.py` | **2** | `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=c79bbe7b…` — equal |

Receipts: `<SCRATCH>/{c2-recount.json, ctl-*.json}`. Recursive diff against the stored control receipts: the **only** differing key in all four scored controls is `gate_path` (`controls-gates/<name>` in my copy root vs `.ufo/waves/round-34/r34b/controls/gates/<name>` in the stored receipt); the do-nothing receipt is byte-identical (`diff: []`). All five verdict lines are character-identical, and the production JSON is byte-identical. The `gate_path`-only difference matches `w1/ExecRecountC2.md` §4 independently.

Stability, because the green counter's name-pool permutation uses a fresh `random` RNG per fixture:

| surface | runs | observed | exit |
|---|---|---|---|
| green `gate-config-mini.json` | 5 (07:22Z) | `REPLAY_GATE_CLEAN … shortcuts_below_target=7 shortcuts_over_target=-` ×5 | 0 |
| red `gate-config-naive.json` | 3 | `REPLAY_GATE_REFUSED … shortcuts_below_target=6 shortcuts_over_target=label-memorization` ×3 | 2 |
| `--selftest` | 3 | `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3, "selftest": "replay-gate"}` ×3 | 0 |

Base state, verified against git rather than trusted from the before receipt: `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` → `fatal: path … exists on disk, but not in 'ec3125ad…'` (exit 128); the same for `c2-shortcut-gate-counter.py`. So `gate_absent` at the base is a property of the revision, not merely of the file the counter was pointed at.

---

## 4. Clause arithmetic and what the green surface does

Six clauses (`c2-shortcut-gate-counter.py:112-119`), all true in P1/P2:

| clause | test | measured |
|---|---|---|
| `gate_present` | `replay-gate.py` exists under `--root` | true |
| `selftest_clean` | selftest exit 0 **and** `failures == 0` | exit 0, 0 |
| `mutants_killed` | `mutants_killed == 3` | 3/3 |
| `red_refused` | red exit 2, verdict `REPLAY_GATE_REFUSED`, `label-memorization` in `classes_over_target` | 2, `["label-memorization"]` |
| `green_clean` | green exit 0, verdict `REPLAY_GATE_CLEAN` | 0, CLEAN |
| `green_positive_meets_target` | `structural.matched == 8` | 8 |

Selftest composition (verified by reading `replay-gate.py`): 6 behaviour cases (`clean`, `red-one`, `red-two`, `boundary-below`, `positive-below`, `counter-garbage`) + 2 config refusals (`two-shortcuts-unevaluable`, `duplicate-class-unevaluable`) + 1 `positive-absent` + 3 mutant kills = 12. The three mutants patch exactly the branches the predicate names: `if over:` → `if False:`; `if not positive["met_target"]:` → `if False:`; `len(shortcuts) < MIN_SHORTCUTS` → `len(shortcuts)`.

Per-reader scores, both surfaces, from my own runs (07:23:41Z, `/fast/scratch/…/ScribeScorecardRow/per-reader.txt`):

| reader | green matched | red matched |
|---|---|---|
| `structural` (positive control) | **8** | **8** |
| `all_false` | 0 | 0 |
| `size_keyed` | 1 | 1 |
| `fixed_slice` | 0 | 0 |
| `digest_keyed` | 0 | 0 |
| `string_scan` | 0 | 0 |
| `record_order_replay` | 0 | 0 |
| `label_replay_full` (registered as `label-memorization`) | 0 | **8** |
| `label_keyed` (unregistered in both configs) | 0 | 0 |

Green mechanics (`mini-counter.py` docstring + code): each fixture is copied to an opaque temp path as a **permutation of the name pool** with every `name_off` rewritten; total size (512), record order and value bytes are unchanged. Label, size, whole-file digest, fixed offsets and build-record-order are therefore all identity-defeating, and only record-array traversal can associate a name with its record. That is why the structural reader is 8/8 there and `label_replay_full` is 0/8, while on the untouched red surface `label_replay_full` is 8/8.

---

## 5. Findings

Severity key: **H** = yields a false `REPLAY_GATE_CLEAN`; **M** = record/custody defect, no false verdict; **L** = disclosure.

### S1 (H) — a shortcut registered under the positive control's class name is silently excluded from `over`
`evaluate()` computes `over = [row for row in findings if row["met_target"] and row["class"] != positive_spec["class"]]`; `load_config()` validates duplicate classes **only among the shortcuts**, never against `positive_control.class`. Probe: `gate-config-naive.json` with the `label-memorization` entry re-registered as `{"class": "structural", "path": "…/label_replay_full.py"}` — the memorizer still answers 8/8 (measured), yet:

```
2026-10-25T07:23:32Z  replay-gate.py --root . --config config-class-relabel.json
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=-   EXIT=0
```

So the gate emits CLEAN while a shape-only reader meets the target, when the config author is careless (or hostile) about class naming. The frozen green config registers seven distinct classes, none named `structural`, so the production receipt is unaffected. Related but distinct: `w1/MutGateBranches.md` M5 shows the inverse mutation (`over` *including* the positive row) is killed, and flags the config-level duplicate-class gap without an end-to-end CLEAN demonstration; S1 supplies that demonstration.

### S2 (H) — the gate trusts the counter's `met_target`; a selective under-report passes as CLEAN
`run_counter()` reads `matched`, `target`, `met_target` from the counter's own stdout and never checks `met_target == (matched >= target)`. Probe: a counter stub printing `matched=8, target=8, met_target=(reader basename == "structural.py")`:

```
2026-10-25T07:23:33Z  replay-gate.py --root . --config config-selective.json
REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-   EXIT=0
```

Bounded counter-probe: the blunt version (`met_target=false` for *every* reader) does **not** pass — the positive-control floor turns it into `REPLAY_GATE_UNEVALUABLE finding=positive_control_below_target` (exit 3, 07:23:33Z). So the hole needs an inconsistent-but-positive-reporting counter; the frozen `mini-counter.py` derives `met_target` from `matched == TARGET`, so it is not affected. `w1/MutGateBranches.md` M4 tests the *other* direction (using the child exit code instead of `met_target`) and its lying counter reports `0` for shortcuts, so it does not exercise this case. Same family, verified here: the counter contains no `git` call, so `measured_revision` is only the `--rev` echo (`c2-shortcut-gate-counter.py:73`).

### S3 (positive control, no defect) — the refusal branch is class-agnostic
Six config classes (`all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`, `record-order-replay`) were all pointed at the structural reader (8/8):

```
2026-10-25T07:23:34Z  REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=0
shortcuts_over_target=all-false,digest-keyed,fixed-slice,record-order-replay,size-keyed,string-scan   EXIT=2
```

The refusal does not depend on the class being `label-memorization`; only the `structural` name is reserved (S1).

### S4 (M) — the fixture set cannot exhibit a size-keyed replay at target, so that refusal is only demonstrated by code reading
All eight fixtures are 512 bytes, so `size_keyed` scores 1/8 on **both** surfaces and only `label-memorization` ever reaches 8/8 on the red case. The gate would refuse a size-keyed replay (S3 proves the branch), but the round's red surface does not construct one. The claim's red clause names label-keyed memorization only, so this is a width disclosure, not a target shortfall. Consequence for the draft: the row must not imply the red case exhibits the r34-C1 failure mode (size-keyed fixed-slice replay); it exhibits label memorization on a shape-only counter.

### S5 (L) — eight readers exist, seven are registered
`readers/label_keyed.py` is in the pin map and in neither config. Measured 0/8 on both surfaces, so omitting it from the class inventory gained nothing (the kill rule's "no shortcut class may be dropped" is not evaded by its absence). Its pin is therefore an unused-instrument pin; the row should not say "eight registered classes" without qualification (the green gate prints 8 rows = 1 positive + 7 shortcuts).

### S6 (M) — `claims.json` mtime is not a write-order fact
`.ufo/waves/round-34/r34b/claims.json` mtime is `2026-10-23T10:46:59Z`, while its `declared_at_utc` is `2026-10-25T07:11:52Z` and the instruments it pins were written 2026-10-25T07:09:52Z–07:11:41Z. Content is bound (worktree == freeze blob `de3afbfb…`, committed in `c79bbe7b` at 07:13:11Z), but the mtime cannot be used as evidence that the claim predates the instruments. Receipt mtimes are `07:13:21Z` (before), `07:13:24Z` (after), `07:13:46Z`–`07:13:52Z` (controls): the *after* receipt was written 10 s after the freeze commit and the controls 20–40 s after that — the reverse of round 32's controls-before-production order. That ordering is harmless here (the after-run is the L1's own instrument check against synthetic fixtures, not domain data), but a "controls landed before production" sentence must not be written.

### S7 (M, custody) — cited receipts are not anchored to the freeze
`git ls-files .ufo/waves/round-34/r34b` → **exactly one** file (`claims.json`); `before/`, `after/`, `controls/` are untracked and not ignored (`git check-ignore` silent). The freeze commit therefore binds instruments and claims, not the receipts the claim cites. Same conclusion as `w1/ExecRecountC2.md` F6, independently re-checked here. For the outside closure these receipts must be committed (or re-issued under a commit) or the row's "evidence pointer" points at mutable worktree bytes. Their hashes are pinned in this report so they can be committed as-is without a rescan.

### S8 (L, record) — the predicate sentence is not one sentence
`claims[0].predicate` and both gate configs carry sentence **A** (237 chars, sha256 `7c6c17f0cca6c680…`); `c2-shortcut-gate-counter.py:PREDICATE` and every receipt carry sentence **B** (351 chars, sha256 `8340aea51154fc0e…`). Measured `A == B` → `False`; common prefix 21 chars (the `P34-shortcut-replay: ` label). The claim's `predicate_identity` field asserts they are one sentence — already disclosed as `PREDICATE_IDENTITY_FALSE` in `.ufo/waves/round-34/r34b/predicate-reconciliation.json` and audited twice (`w1/RevPredicateIdentity.md`, `w1/ExecRecountC2.md` F1). **Draft implication: the C2 paragraph quotes A verbatim (the frozen claim's own sentence) and must not repeat the `predicate_identity` claim.**

### S9 (L) — S106 has no landed registry row yet
`claims[0].sources_opened_this_round` is `["S106"]`; `corpus/SOURCES.md` ends at **S105** (line 111) at 07:2xZ and `grep -rn S106 corpus/` returns nothing. S106 (pinned binutils `readelf.c`, the gate's legitimate-reader ground) is being drafted by the `ScribeSourcesRow` seat. The C2 paragraph may say "S106 (opened this round; registry row pending)" but must not cite a landed `corpus/SOURCES.md:NNN` row for it.

---

## 6. DRAFT A — SCORECARD Capabilities row (append after the round-17 row, `SCORECARD.md:626`)

<!-- DRAFT A BEGIN -->
| pre-freeze shortcut-replay gate for structural-decoding counters | Runs any config-named counter argv against one registered structural positive control and seven registered structure-blind shortcut classes (all-false, size-keyed, fixed-slice, digest-keyed, string-scan, record-order-replay, label-memorization) under the counter's own target; returns `REPLAY_GATE_REFUSED` (exit 2) when any shortcut meets it, `REPLAY_GATE_CLEAN` (exit 0) only when the structural control meets it and every shortcut stays below, `REPLAY_GATE_UNEVALUABLE` (exit 3) when it cannot run. At `c79bbe7b` it refused the shape-only counter (label-memorization 8/8) and cleared the identity-defeating counter on the same eight fixtures (structural 8/8, seven shortcuts ≤1/8), and its 12-case selftest kills all three mutants of its refusal, positive-control and shortcut-floor branches | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33`; gate `tools/round-34/replay-gate.py`; receipts `.ufo/waves/round-34/r34b/after/c2-at-instruments.json` + `.../controls/`; independent recount and probes `.ufo/waves/round-34/r34b/w1/ScribeScorecardRow.md`, `w1/ExecRecountC2.md` | round 34 |
<!-- DRAFT A END -->

Note to append with the row (two sentences, capability limits — not a waiver):

<!-- DRAFT A NOTE BEGIN -->
The gate audits the counter's own rule, not a hostile counter: it trusts the config's shortcut class labels and the counter's `met_target` field, so a shortcut entered under the positive control's class name, or a counter whose `met_target` disagrees with its own `matched`/`target`, still yields CLEAN (seat probes `.ufo/waves/round-34/r34b/w1/ScribeScorecardRow.md` §5 S1/S2). The frozen green and red configs and the frozen `mini-counter.py` are not affected; the class inventory and receipt-field consistency are open repair ground, and the fixtures are eight author-built 512-byte synthetic records, never domain evidence.
<!-- DRAFT A NOTE END -->

Fit check against the table's own rule ("rows entered through rounds that demonstrated each capability running"): the intended invocation ran and is receipted; the row adds no axis score and claims no domain result.

---

## 7. DRAFT B — `## Round 34` section, C2 subsection (append after `SCORECARD.md:3345`, i.e. after the R34-C1 subsection)

If the L1 prefers, amend the heading to `## Round 34 — prospective GNU ELF version-needs depth; C2 pre-freeze shortcut-replay gate`; the draft below does not require it.

<!-- DRAFT B BEGIN -->
### R34-C2 — pre-freeze shortcut-replay gate (capability acquisition, depth)

R34-C2 / depth, a capability acquisition: the lane now owns a **pre-freeze, config-driven shortcut-replay gate** for finite structural-decoding counters, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (`.ufo/waves/round-34/r34b/claims.json`, blob `de3afbfb…`, committed in the freeze commit at 07:13:11Z before any wave seat ran). Axis basis as frozen: the three owned numeric proxies are tied at 10 and none retired, so depth is a lowest non-retired axis; the surface this round moves is the lane's structural-counter admission instrument, **not** a numeric proxy score, and no coverage or calibration credit is inferred.

P34-shortcut-replay (the frozen sentence, verbatim): "P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does." The counter's `PREDICATE` constant and its receipts carry a longer elaboration (351 chars) of the same label; the two sentences are not byte-identical (`predicate-reconciliation.json`, `PREDICATE_IDENTITY_FALSE`), so no identity is claimed here.

| claim / surface | before at base `ec3125ad` | after at the instruments `c79bbe7b` | verdict / score delta |
|---|---|---|---|
| R34-C2 / depth — pre-freeze structure-blind shortcut-replay gate | no gate exists: `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad…`, exit 2 (`r34b/before/c2-at-base.txt`); `git cat-file -e ec3125ad:tools/round-34/replay-gate.py` fails, so absence is a property of the revision | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0 (`r34b/after/c2-at-instruments.json`, sha256 `da78f444…`); all six clauses true | **target met as measured at the frozen instruments**; owned scores 10→10, delta 0; capability row entered |

Values inside the receipt: red `exit 2`, `classes_over_target=["label-memorization"]`; green `exit 0`, `shortcuts_below_target=7`, `positive_matched=8` (structural 8/8, the seven shortcut classes 0–1/8); selftest `{"cases": 12, "failed": [], "failures": 0, "mutants": 3, "mutants_killed": 3}`. The red surface is the shape-only `naive-counter` (fixtures keep their names and bytes) where `label_replay_full` memorizes 8/8; the green surface is the identity-defeating `mini-counter`, which runs every fixture through an opaque path as a name-pool permutation with rewritten `name_off` (same 512-byte size, same record order, same value bytes), so label, size, digest, fixed offsets and build order cannot identify an input and only record-array traversal resolves a name.

Counting command: `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>`.

Controls (all pre-registered, all landed, none meets the target): do-nothing `gate_absent` exit 2; `gate-always-clean` 4/6 clauses (`red_refused`, `selftest_clean` fail); `gate-junk-clean` 5/6 (`red_refused`); `gate-no-positive-check` 4/6 (`mutants_killed`, `selftest_clean`); `gate-vacuous-no-floor` 5/6 (`selftest_clean`). Receipts `.ufo/waves/round-34/r34b/controls/`, hashes in `w1/ScribeScorecardRow.md` §1. Independent reproduction this round: a copy-based recount reproduced the verdict line and the after-receipt **byte-for-byte** (`da78f444…`, 30/30 fields), the five control lines character-identically, green/red/selftest verdicts stably across repeated runs, and 26/26 pins at the freeze (`w1/ScribeScorecardRow.md` §§2-3; independent clone recount `w1/ExecRecountC2.md`).

Known limits of the frozen instrument, disclosed and not waived: the gate trusts the config's class labels and the counter's `met_target`, so a shortcut entered under the positive control's class name (CLEAN with a 8/8 memorizer) or a counter that under-reports `met_target` selectively (CLEAN with `matched=8`) passes — both reproduced (`w1/ScribeScorecardRow.md` §5 S1/S2), neither affects the frozen configs or the frozen mini-counter; the counter never checks `measured_revision` against the checkout; `green.shortcuts_below_target` is recorded but not asserted, so dropping one green-registered class is undetected (`w1/ExecRecountC2.md` F3); the eight fixtures are author-built synthetic bytes and the red case exhibits label memorization, not the r34-C1 size-keyed fixed-slice replay (all fixtures are 512 bytes, `size_keyed` = 1/8); the receipts cited above are worktree files not yet committed (`git ls-files .ufo/waves/round-34/r34b` = 1, `claims.json`). No target, counter, predicate, label or registered class was changed after the freeze, and no shortcut class was dropped.

**Verdict: target met at the frozen instruments (six clauses true, exit 0). Outside closure pending — `[OUTSIDE-R34-C2: pending]`; replace this bracket when the outside decision lands.** The claim's own kill rule was not triggered, so nothing is relabelled, rescaled or re-frozen.

**R34-C1 stays stopped.** R34-C1 remains frozen and stopped at `54a87a51a865ab931fd355e767303337b05cccf4` (`.ufo/waves/round-34/claim-stop.json`): not re-opened, not re-scored, not relabelled, not re-run. Its production reader and its twelve carriers were not executed or scored in this attempt, and its subsection above stands unchanged as **falsified measure / rejected-honest-stop**. Owned scores remain **10 → 10** on coverage, depth and calibration, delta 0; the capability row is a capability record, not an axis score, and neither the C1 stop nor the C2 gate is calibration evidence.
<!-- DRAFT B END -->

---

## 8. Out of scope / deliberately not done

- No lane doc was edited: `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/**` untouched; §6/§7 are drafts for the L1. Verified: no write outside this report and `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeScorecardRow/`.
- No VCS mutation: no `git add/commit/stash/checkout/reset/pull/push`, no `jj` command at all, no clone in the lane; scratch work used `cp -a` of `tools/round-34` and `controls/gates/`.
- No ELF carrier, fixture or reader was executed as a program: fixtures were never invoked; readers ran only as `python3` children of the pinned counters. `tools/round-34/version-needs-counter.py`, its twelve carriers and the C1 production reader were not invoked, read as programs or scored.
- No network. No tool installed or upgraded.
- Not verified here (owned by other seats): the S106 capture itself (ScoutReadelfSource), the acceptance of the 512-byte fixture format as an independent oracle (ExecGreenIndependence), and the mutation census beyond the three shipped mutants (MutGateBranches).
- Not done by design: re-scoring, relabelling, widening or repairing the claim; amending a frozen instrument; promoting any probe into a clause.

---

## 9. Tooling record

Nothing installed, nothing upgraded, no package manager invoked (pacman transactions are paused host-wide anyway). Tools used: `/usr/bin/python3` 3.14.8, `/usr/bin/git`, coreutils (`sha256sum`, `stat`, `cp`). Reason: the task needed only the interpreter and hashing; installing anything would have added surface without improving an axis.

---

## 10. Artifact paths

- Drafts: this report §6 (capabilities row + limits note) and §7 (Round-34 C2 subsection).
- Scratch evidence: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeScorecardRow/` — `c2-recount.json` (byte-identical to the after-receipt), `ctl-{do-nothing,gate-always-clean.py,gate-junk-clean.py,gate-no-positive-check.py,gate-vacuous-no-floor}.json`, `pins.txt` (26/26), `per-reader.txt` (both surfaces), `probes.log` (four gate probes with UTC), `root/config-class-relabel.json`, `root/config-selfreport.json`, `root/config-selective.json`, `root/config-six-classes-meeting.json`, `root/counter-{selfreport,selective}.py`.
- Lane evidence cited: `.ufo/waves/round-34/r34b/{claims.json,before/c2-at-base.txt,after/c2-at-instruments.json,controls/**,predicate-reconciliation.json,instruments.json}`; seat reports `w1/{ExecRecountC2,RevClaimsVsInstruments,RevPredicateIdentity,MutGateBranches,RevControls,ExecGreenIndependence}.md`.

---

**Verdict: `SCORECARD_DRAFTS_READY` — R34-C2 reproduces byte-for-byte at `c79bbe7b` (exit 0, receipt `da78f444…`, 26/26 pins, five controls character-identical, verdicts stable); capability row and Round-34 C2 subsection drafted with before/after values, counting command, control arithmetic, a pending outside verdict placeholder and the explicit "R34-C1 stays stopped, scores 10→10"; four disclosure findings (S1/S2 gate-trust bypasses reproduced; S4 fixture-width limit; S6/S7 custody) are stated as limits of the frozen instrument and change no clause, target or label.**
