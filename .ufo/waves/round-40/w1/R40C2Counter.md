# R40C2Counter — P40-C2 counter (`tools/round-40/c2-counter.py`)

**DONE** — `c2-counter.py` written, `--selftest` 42/42 at exit 0, wired to the draft predicate P40-C2
(`plans/round-40-claims.md:69-99`) including the two round-40 additions that did not exist in the
round-39 counter: the rule-block-18 (table v1) invariance at a base commit, and the `(label, action)`
pair reported through a scored closed-vocabulary `action` column plus a counted
`distinct_decisions`.

Seat: R40C2Counter (leaf, wave 1 = pre-freeze build). Writes confined to
`.ufo/waves/round-40/w1/R40C2Counter.md` and
`.ufo/waves/round-40/w1/artifacts/R40C2Counter/`. No REA run, no unblob run, no carrier run, no
VCS mutation, no edits under `corpus/`, `tools/`, `plans/`, or any frozen surface.

## Deliverables

| file | sha256 | role |
|---|---|---|
| `.ufo/.../artifacts/R40C2Counter/c2-counter.py` | `b3834bd46bf17cee6674f165b736d6abd298345ed6da7719c4fc9992f85876e9` | the gate; copy **byte-identically** to `tools/round-40/c2-counter.py` at the freeze |
| `.ufo/.../artifacts/R40C2Counter/probe-real.py` | `87031dabe91ed7df047976a373b5161a547c1a404db9a5106cc79b30cf1d925c` | read-only recon helper (not a gate) |
| `.ufo/.../artifacts/R40C2Counter/probe-real.json` | `bff2ef106cdb0f7e8d09e2abc9438fe65eebfd1948167b7c33c2940660e0981e` | real-lane probe output cited below |
| `.ufo/.../artifacts/R40C2Counter/selftest-output.txt` | `52eff824b3349f7b25b193aa6d07a2553e4459869ca49c69b89f1f912eec3213` | `--selftest` stdout |
| `.ufo/.../artifacts/R40C2Counter/smoke-lane-head.receipt.json` | `5707258d71056af1892ee2968ef0e473d54419210187c3beadf6402d93274c12` | receipt of the real-lane run at `fa6a8a3f` |
| `.ufo/.../artifacts/R40C2Counter/smoke-lane-head.stdout.json` | `836f2f8047307d76c30ac57f851ab9e6933f76dd5a3e6a2b30291d4e9bc49c47` | its stdout line |

Installed CLI (exactly as assigned):

```
python3 -I -B c2-counter.py --root LANE --rev REV --freeze FREEZE [--json-out PATH] [--base COMMIT]
python3 -I -B c2-counter.py --selftest
```

`--base` is optional; without it the base is derived from history (below) so the freeze needs no
hard-coded sha. Exit contract: `0` met, `1` not met (a binding false or a pair mismatch, receipt
still written), `2` unevaluable. Every receipt carries its own `exit_code` (R39-CL6), including the
`2` receipt.

## What the counter binds (predicate clause → binding)

| binding | predicate clause | source |
|---|---|---|
| `seed_matches_freeze` | "seed = the freeze commit hash" | manifest at REV |
| `v2_table_present` / `v2_table_identical` / `v2_table_columns` | "the frozen interpreter reading only the v2 table"; "the v2 table bytes equal the freeze bytes" | `SKILL.md` at FREEZE and REV; columns `label`,`operation`,`provider`,`action` present (domain guard + scored action, claims:73-80) |
| `v1_table_present` / `v1_table_identical` | block 18 stays byte-identical (claims:71-72) | v1 block at *base* vs REV |
| `interpreter_present_at_freeze`, `interpreter.freeze_sha256` | "the frozen interpreter `tools/round-40/sqfs-triage-v2.py`" | bytes at FREEZE, never at REV |
| `manifest_generator_path`, `generator_sha_matches_freeze`, `writer_matches_manifest` | "the frozen `tools/round-40/heldout-gen-v2.py`" | manifest `generator` object or path string |
| `classes_unique`, `classes_two_each`, `n_equals_twice_classes`, `ids_unique`, `arms_valid` | "2 per class", N envelopes | manifest |
| `carriers_regenerated`, `regenerated_seed_matches_freeze` | "carriers regenerate byte-identically from that seed" | frozen generator run in a mirrored tree |
| `carriers_committed`, `carrier_paths_unique`, `envelope_paths_unique` | carriers are git objects at the pinned sha | carrier blobs at REV |
| `envelopes_valid` | "every envelope's subject digest equals its carrier's sha256" | envelope `subject.digest.sha256` (accepts both `{ok,data,meta}` and the bare `data` object) |
| `manifest_after_freeze`, `manifest_before_envelopes` | "first added in a commit descending from the freeze and no later than its envelopes" | `git log --diff-filter=A --reverse` |
| `decisions_reported`, `row_decisions_consistent` | "the counter reports the number of distinct row decisions" (claims:81-82) | interpreter-reported row index per envelope; one row per expected pair, distinct pairs on distinct rows |
| `matched` / `met_target` | "(label, action) == expected for every envelope" | `matched == N and all bindings` |

`met_target` is computed once and re-derived before it is returned: `met_target_consistent` must be
true or the run is unevaluable (`met_target_inconsistent`), so a receipt can never carry a target
claim its own numbers contradict.

### `distinct_decisions`

`res['distinct_decisions']` = number of distinct row indices among the *matched* envelopes;
`distinct_row_list`, `per_class[...].row`, `label_action_vocabulary`, and
`replicates_identical_in_class` are reported alongside. Row indices are the interpreter's own, so the
counter infers the numbering base (0 or 1) from the rows the interpreter itself names, and from its
`--table-only` listing, instead of assuming one. That was necessary: the lane's round-39 interpreter
numbers rows from 1 (`probe-real.json: row_index_base_from_reported_rows = 1`,
`row_index_base_from_table_only = 1`).

### Base for the block-18 check

`derive_base` walks `git log FREEZE -- SKILL.md` newest-first and returns the newest commit whose
`SKILL.md` has no `<!-- sqfs-triage-table v2 -->` marker and does carry the v1 block (else simply the
newest without the v2 marker). On the real lane at `fa6a8a3f` it returns
`2b0b6a29578c0b8917f677321557d96a444e994e` (`base_source: derived`) — the round-39 tip state. The
L1 may pass `--base` explicitly to pin it; the selftest covers both paths.

### Freeze integrity (exit 2)

Frozen paths of this claim: `tools/round-40/sqfs-triage-v2.py`, `tools/round-40/heldout-gen-v2.py`,
`tools/round-40/c2-counter.py`, `plans/round-40-claims.md`. Any commit in `FREEZE..REV` touching one
of them → `frozen_path_changed`, exit 2, no `met_target` (claims:15-19). `SKILL.md` is deliberately
**not** a frozen path: a table edit after the freeze is caught by `v2_table_identical` / the pair
mismatches at exit 1, matching how round 39 separated table drift from frozen tooling.

Other exit-2 reasons: `freeze_not_ancestor_of_rev`, `unknown_revision`, `no_manifest_at_rev`,
`manifest_unparsable`, `manifest_not_an_object`, `generator_absent_at_freeze`, `generator_failed`,
`generator_wrote_no_manifest`, `regenerated_manifest_unparsable`, `interpreter_failed` (both the JSON
and the TSV interface failed), `met_target_inconsistent`.

## Contract the freeze must satisfy (for the v2 interpreter/generator authors)

The counter is interface-driven; it never parses the v2 table's semantics itself. Three interfaces
must hold.

1. **Interpreter argv** — `python3 -I -B sqfs-triage-v2.py --skill SKILL.md [--json]
   [--table-only] ENV...`
   - `--json` → one JSON object `{"results": [{"path", "label", "action", "rule"|"row_index"|
     "index", "row": [cells]}]}` (round-39's `--json` already emits `label`, `rule`, `row` cells:
     `probe-real.json`).
   - no `--json` → one line per envelope, TSV: `path<TAB>label<TAB>action[<TAB>row]`.
   - `--table-only` → `INDEX. label` lines (round-39 form) or `{"rules":[{index,label}]}`.
   - exit 0 on success; a non-zero `--json` is tolerated (the counter falls back to TSV), but a
     non-zero TSV run is `interpreter_failed` (exit 2).
   - **`action` must be reported either as a JSON/TSV field or reachable through the reported row**:
     when only a row index is named, the counter reads the pair off the row cells using the frozen
     v2 header. A table without an exact `action` column cannot satisfy `v2_table_columns`.
2. **Generator argv** — `python3 -I -B tools/round-40/heldout-gen-v2.py --seed FREEZE --out DIR`
   must work from a *mirror* of `tools/round-40/` + `tools/round-37/` taken at the freeze, with
   `TMPDIR` set to the counter's scratch and `KAIDOKU_GEN_SQUASHFS` pointing at the mirrored
   `tools/round-37/gen-squashfs.py`. It must write `DIR/manifest.json` with the same carrier `id`
   and `carrier` relative path per id, plus `class`, `arm`, `expected_label`, `expected_action`.
   A generator that hardcodes the lane root outside those two trees cannot be regenerated and the
   run would stop at `generator_failed`.
3. **Manifest** — `corpus/evidence/round-40/c2/heldout/manifest.json`:
   `{seed, generator: "tools/round-40/heldout-gen-v2.py" | {name, version, sha256, writer{path,sha256}},
   classes: [...], carriers: [{id, class, arm, carrier, sha256, envelope, expected_label,
   expected_action}]}`. `envelope` may be omitted (the counter falls back to the carrier's sibling
   `envelope.json`); `label`/`action` are accepted as aliases for `expected_label`/`expected_action`;
   carrier and envelope paths may be lane-relative or manifest-relative.

Table placement: the v2 block must sit inside `## Queue-drain craft` after the
`<!-- sqfs-triage-table v2 -->` marker line; a marker outside that section is invisible to the
counter (the round-39 convention, `SKILL.md:333` for v1).

## Evidence

### E1 — selftest, 42 cases, exit 0

```
$ python3 -I -B c2-counter.py --selftest
{"selftest": "c2-counter r40", "cases": 42, "green": 11, "red": 31, "pass": 42, "fail": 0, "failures": []}
SELFTEST cases=42 pass=42 fail=0
exit=0
```

Every case builds a private git fixture (`mktemp` under `$HYAKU_SCRATCH/kaidoku-r40`, `git init -q`,
`git -C "$D" rev-parse --show-toplevel == $D` checked before the first commit, identity only via
`-c user.name=fx -c user.email=fx@fx`), then runs the counter as a subprocess with
`--root/--rev/--freeze/--json-out`. Per case the harness asserts: process exit code, that the JSON
receipt exists and its `exit_code` equals the process exit (R39-CL6), `met_target_consistent`, the
named false/true bindings, and that the counter left the measured repo clean
(`git status --porcelain` empty — no scratch, no writes inside the lane).

Case inventory — 11 exit-0, 22 exit-1, 9 exit-2 (threshold ≥30 met):

- *green and interface shapes (11)*: green; generator object with matching sha; envelope path
  omitted (sibling inferred); full CLI `{ok,data,meta}` envelope; lane-relative paths; tab
  interface with a row column; rows from `--table-only`; JSON without a row index; rows only, pair
  read off the table; rows numbered from 1, pair read off the table; explicit `--base`.
- *not met (22)*: v2 block removed after freeze; v2 table edited after freeze; v1 table edited after
  freeze; v1 block removed at REV; `seed != freeze`; manifest added before freeze; envelope before
  manifest; carrier not committed as pinned; subject digest mismatch; missing envelope; 3 carriers
  in one class; one wrong expected label; label right / action wrong; envelopes swapped between
  carriers; *best table + `*` default row instead of the domain guard*; catch-all table; truncated
  table (unclassified fall-through); generator object with wrong sha; two carriers on one path; no
  row and no `--table-only`; rows only with a v2 header lacking `action`; v2 header without
  `action`.
- *unevaluable (9)*: no manifest at REV; interpreter / generator / claims / counter edited after
  freeze; interpreter fails outright; manifest unparsable; unknown revision; freeze not an ancestor
  of REV.

### E2 — real lane at `fa6a8a3f`: exit 2, no manifest (expected pre-freeze)

```
$ python3 -I -B c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev HEAD --freeze HEAD --json-out .../smoke-lane-head.receipt.json
{"exit_code": 2, "freeze": "fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f",
 "frozen_paths_changed": [], "revision": "fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f",
 "unevaluable": "no_manifest_at_rev"}
exit=2
```

Receipt (`smoke-lane-head.receipt.json`) also records `base_commit 2b0b6a29…`, `base_source
derived`, `predicate P40-C2` and its own `exit_code: 2`.

### E3 — block 18 (table v1) on real history, read-only

`python3 -I -B probe-real.py` (see `probe-real.json`): `v1_present_at_head/base = true`,
`v1_identical_base_head = true`, `v1_sha256` `21759e9f33e05d5b305a5a2ccc37e69f0f19fc9c8b5a2bb7f89bdb4887781bda`
at both ends, `v1_bytes = 3086`, `v1_header_cells` exactly the round-39 nine columns (`… |
cause -> action | source`), `v2_present_at_head = false`. So at the freeze the invariance check has
teeth and a known-good baseline; note that v1's `cause -> action` cell does **not** satisfy the v2
`action` column, i.e. a verbatim v1 transcription into a v2 block fails `v2_table_columns`.

### E4 — the lane's real interpreter through the counter's parsers

Same probe, `tools/round-39/sqfs-triage.py` materialised from git, run on committed round-39
held-out envelopes only (no REA, no unblob): `--json` exit 0, four results with
`label=clean, row=8, cells[:2]=['clean','squashfs_v4_*']`; plain TSV exit 0 with
`path\tlabel` only; `--table-only` exit 0 with 8 labels. Index base inferred as `1` from both
signals. This is the concrete confirmation of the interface contract in §"Contract" and of the
1-based numbering the counter must not assume.

### E5 — round-39 held-out evidence compatibility

Read-only scan of `corpus/evidence/round-39/c2/heldout/`: 20 carriers, manifest keys
`seed/generator/classes/carriers`, generator given as an object (`heldout-gen.py`), carrier keys
`id/class/label/arm/carrier/sha256` (no `envelope` field — sibling inference path), 20/20 envelope
`subject.digest.sha256` equal to their manifest `sha256`, `operation == 'extract_firmware'`
(underscore spelling), `provider == {"id":"unblob","name":"Unblob","version":"26.6.4"}`. The
counter's aliases and its `provider_name`/`envelope_data` helpers therefore match the real REA
envelope shape the v2 set will reuse.

## Residual risks / items the freeze must decide

1. **Generator sandboxing** (highest). Regeneration runs in a mirrored tree of `tools/round-40` +
   `tools/round-37` at the freeze with `TMPDIR`/`KAIDOKU_GEN_SQUASHFS` redirected. If
   `heldout-gen-v2.py` needs any other lane path (e.g. a round-40 writer, a data file under
   `corpus/`), it must load it relative to `__file__` or via the env var, or the counter stops at
   `generator_failed` (exit 2). Round-39's generator already satisfies this; the v2 generator should
   be written the same way.
2. **`action` column name.** `v2_table_columns` requires exact header cells `label`, `operation`,
   `provider`, `action` (backticks stripped). A prose header such as `cause -> action` will not do.
3. **Row-index reporting.** Without a reported row the run is exit 1 (`decisions_reported` false),
   even if all pairs match — the claim scores the decision, so the interpreter must expose it (JSON
   `rule`/`row_index`/`index`, a 4th TSV field, or `--table-only` for labels the interpreter names).
4. **`distinct_decisions` has no target value** in the draft; the counter reports it (plus per-class
   rows and `replicates_identical_in_class`) and binds only the structural invariant (one row per
   expected pair, distinct pairs on distinct rows). If the freeze wants an exact count, it must add
   it to the predicate, not to the counter.
5. **[INFERENCE]** The v2 held-out classes include `out-of-domain` (a non-`extract-firmware` REA
   operation). The counter does not require `operation == 'extract_firmware'` on every envelope —
   requiring it would make the domain-guard class unschedulable. It records `operation`/`provider`
   per envelope in the receipt so a replay can see the guard inputs.
6. Selftest fixtures live under `$HYAKU_SCRATCH/kaidoku-r40` and are removed per case; the whole
   selftest leaves no directory behind (verified: no `c2-counter.*`/`probe*` entries under
   `/fast/scratch/hyaku/kaidoku-r40` afterwards).
7. Landscape note for the L1, not mine to touch: `detail.log` (9535 B, mtime 2026-10-26 15:29:36)
   is untracked at the lane root and holds another seat's C1 counter `DETAIL` lines (AVM carriers,
   receipts, projection). My counter and probe never write it (`grep detail.log` finds no reference
   in my artifacts) and my selftest writes only inside its per-case fixture repos and its
   `--json-out` path. It should be removed or ignored before the freeze commit so a wide `git add`
   does not freeze a peer's scratch log.

## Bounds, tooling

- No `git add/commit/…` in the lane or fleet; all git calls read-only (`show`, `log`, `ls-tree`,
  `merge-base`, `rev-parse`, `status`).
- No REA invocation, no unblob invocation, no sasquatch/sasquatch-v4be run, no V1/V2/L1/L2 carrier
  touched, no held-out carrier built or run.
- Scratch was `/fast/scratch/hyaku/kaidoku-r40` via `mktemp -d`, removed; nothing cited depends on a
  scratch or `/tmp` path.
- No tools installed or upgraded this wave (no pacman/uv/npx transaction; the pacman pause was not
  needed). `python3 -I -B -m py_compile` was used once for a syntax check and its `__pycache__`
  removed from the artifacts dir.
