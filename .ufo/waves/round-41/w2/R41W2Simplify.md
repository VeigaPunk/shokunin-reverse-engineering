# R41W2Simplify — YAGNI review of the round-41 counters

**DEFECTS FOUND** — I attacked the two frozen counters for dead code paths, legacy-matcher
scaffolding kept alive only so the selftest can demonstrate it, and probing of multiple manifest key
names. The key-name probing is not a style defect: it is the scored cause of the R41-C2 honest stop,
and it is fixable in one line with no change to the frozen tools or data. Two further defects found
on the way (a frozen-path set that is broader than the claim's own sentence, and a C1 projection
profile whose alias silently weakens the rerun binding) matter more for round 42 than the dead code.

Files reviewed at HEAD `e1c83313` (dispatch tip `7a24ff74`; `e1c83313` touches only `corpus/`):

| file | lines | sha256 | frozen identity |
|---|---|---|---|
| `tools/round-41/c1-counter.py` | 3413 | `bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc` | no per-file sha in the C1 receipt; `frozen_tables_valid: true`, `frozen_path_changed: []` |
| `tools/round-41/c2-counter.py` | 2499 | `c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8` | equal to `frozen_units['tools/round-41/c2-counter.py']` in `l1/scores/c2-at-e9a24d07.json` |

Artifacts: `.ufo/waves/round-41/w2/artifacts/R41W2Simplify/` —
`dead-branch-inventory.json` (machine-readable item list), `patch-onekey.diff`,
`c2-onekey-at-e9a24d07.json`, `c2-unpatched-at-e9a24d07.json`, `feature-compare-52.json`,
`selftest-c1-counter.json`, `selftest-c2-counter.out` (verbatim stdout: one JSON summary line plus
the harness's human summary line).

## 1. What "dead code" turned out to be here

AST reachability from `measure` / `selftest` / `selftest_rea` roots plus a load-name count:

```
c1-counter.py: 56 top-level functions, 0 unreachable, 0 unused module constants
c2-counter.py: 45 top-level functions, 0 unreachable, 1 unused module constant (OPERATION_TOKEN:175)
```

So neither file has dead *symbols*. The weight is in (a) unreachable *branches* — probe lists, alias
maps and output dialects that the frozen inputs can never satisfy — and (b) test scaffolding that
lives inside a frozen scored artifact. Line attribution:

| bucket | c1-counter.py | c2-counter.py |
|---|---|---|
| scored path + `main` | 1574 (46 %) | 1335 (53 %) |
| `selftest` | 1173 (34 %) | 567 (23 %) |
| stub-tool sources (`STUB_GEN`/`STUB_EVAL`/`STUB_INTERP`) | — | 270 (11 %) |
| `selftest_rea` | 172 (5 %) | — |
| module prose/constants | 495 (14 %) | 328 (13 %) |

Both harnesses are *working* at tip and are named by the kill rules, so they are not deletable —
they are relocatable. Measured now:

```
$ cd $S && HYAKU_SCRATCH="$S/hy" TMPDIR="$S" python3 -I -B <lane>/tools/round-41/c2-counter.py --selftest
{"selftest": "c2-counter r41 (v3)", "cases": 70, "green": 20, "red": 50, "pass": 70, "fail": 0, "failures": []}   exit=0

$ cd $S && HYAKU_SCRATCH="$S/hy" TMPDIR="$S" python3 -I -B <lane>/tools/round-41/c1-counter.py --selftest \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"selftest":"c1-counter","cases":97,"green_ok":12,"red_ok":85,"path_probes":6,
 "path_probes_discriminating":3,"root_probes":8,"spec_probes":7,"failures":[]}                                     exit=0
```

## 2. The manifest-key probe is the C2 stop (rank 1)

`c2-counter.py:1486-1505`:

```python
decl_key = None
for key in ('class_features', 'classes_features', 'feature_tuples',
            'features_by_class', 'class_tuples'):
    if isinstance(man.get(key), dict):
        decl_key = key
        break
...
    cex = c.get('class_expected')
    if isinstance(cex, dict) and isinstance(cex.get('features'), dict):
        decl = cex['features']
    elif isinstance(c.get('features'), dict):
        decl = c['features']
    elif isinstance(c.get('declared_features'), dict):
        decl = c['declared_features']
    elif decl_key:
        d = man[decl_key].get(c.get('class'))
        decl = d if isinstance(d, dict) else None
```

Measured against `corpus/evidence/round-41/c2/heldout/manifest.json`:

- none of the five top-level key names exists; `decl_key` is always `None`;
- no carrier carries `features` or `declared_features` (key census over all 52: `class_expected`,
  `declared`, `declared_extras` are the only tuple-bearing keys);
- the manifest's own `declared_schema.location` says **`carriers[].declared` (every carrier)**, and
  `declared_schema.fields` is exactly the counter's `REQUIRED_FEATURES` (6 names) — the counter's
  required-key constant was written for the documented source and then reads two others;
- 40 named carriers resolve through `class_expected.features`, which the claim marks
  **reported, not scored** (`class_map_agreement`), and which additionally carries
  `extraction_failed` — a dimension `declared_schema` explicitly excludes from the binding;
- the 12 `combo` carriers have `class_expected: null`, so every probe misses and the binding fails.

Reproduced and then repaired in a scratch copy (nothing in the lane edited):

```
$ python3 -I -B <lane>/tools/round-41/c2-counter.py --root <lane> --rev e9a24d07… --freeze d764389e…
{"bindings_false": ["observed_features_match_declared"], "matched": 52, "n": 52, "met_target": false, "exit_code": 1}

$ diff -u c2-counter.py c2-counter.onekey.py        # patch-onekey.diff: one hunk, -13/+2 lines
$ python3 -I -B c2-counter.onekey.py --root <lane> --rev e9a24d07… --freeze d764389e…
{"bindings_false": [], "matched": 52, "matched_classes": 40, "matched_combos": 12,
 "met_target": true, "met_target_consistent": true, "declared_features": {"source": "declared"}, "exit_code": 0}
```

Receipt diff, whole file: `argv`, `bindings`, `bindings_false`, `bindings_ok`, `carriers`,
`declared_features`, `exit_code`, `met_target`, `met_target_formula`. Per-carrier, only
`features_checked`/`features_match` change — the 6 documented keys replace 7 (named) and `null`
(combos). Independent of the counter, over all 52 envelopes with the counter's own reader:

```
declared key:        52/52 match, 0 mismatch
class_expected key:  40/40 match, 12 absent
class_expected vs declared on shared keys: 0 diffs
```

**Reading.** The R41-C2 stop is a *reader* defect, not a data defect: at the measured revision the
data satisfies `observed_features_match_declared` under the manifest's documented tuple. The frozen
score at `e9a24d07` remains exit 1 and I am not rescoring it — but the round-42 refreeze should carry
the one-line source change, and the C2 honest-stop report should say the binding failed on a key
name, not on a feature disagreement.

## 3. Ranked drop-list for a round-42 refreeze

Risk = chance the item changes a *score* (not just file size) if left in place.

| # | item | span | risk | drop, or what to do instead |
|---|---|---|---|---|
| 1 | C2 declared-tuple probe: 5 top-level key names + 3 per-carrier fallbacks (`features`, `declared_features`, `class_expected.features`) | c2 1486-1505 | **critical** — it is the scored NOT MET, and it scores two different documents in one run (40 carriers from a *reported* tuple, 12 from nothing) | drop all 8 probes; read `c.get('declared')` and let `REQUIRED_FEATURES` fail loudly on a missing tuple |
| 2 | C2 `FROZEN_PATHS` includes the directory `tools/round-41` (13 files) | c2 115 | **high** (over-blocking) — the claim freezes 4 C2 tools + writer; the other 9 round-41 tools (c1-counter, c1-extra, c1-run.sh, fetch-vendor, sqfs-list, mk-l-carriers, c2-controls, local-source-gate, gen-squashfs) are never read by C2, so any edit to one of them makes a correct C2 score exit 2 `frozen_path_changed`, contradicting `## Separability` ("Neither reads the other's round-41 data") | freeze the 4 C2 units + writer scope + manifest dir; `frozen_units` already pins the shas, so nothing loosens |
| 3 | C1 profile aliases: `core`, `plus-mime`, `plus-content` all map to the same 6-key tuple; `projection()`/`projection_diff()` default `'core'` never taken (single caller at 1655 passes the spec) | c1 1235, 1370-1383 | **high** (scoring-strength hole) — `"projection": "core"` is a *legal* spec value (595 only rejects unknown names) and silently scores the rerun over 6 keys instead of 10, weakening the binding the claim rests on | keep `plus-extractor` only, or give each profile a distinct tuple; drop the dead `'core'` defaults |
| 4 | C2 CLI dialect probes: evaluator tries 5 interfaces, interpreter tries 4 | c2 946-951, 851-855 | **medium-high** — 3 of 5 and 2 of 4 are rejected by the frozen tools' own argparse (`indep-eval-v3.py`: `--envelopes/--out/--full/--selftest`; `sqfs-triage-v3.py`: `--skill/--json/--table-only`+positionals); the scored run used attempt 1 of each (`interpreter_attempts`/`evaluator_attempts` each length 1) | one documented interface per frozen tool; the tools are sha-pinned in `frozen_units`, so a changed CLI is a freeze change, not something the counter should absorb |
| 5 | C2 dialect parsing substrate: `parse_json_results`, `parse_tab_results`, `parse_table_only`, `infer_index_base`, `_pair`, `parse_eval_pairs` (~150 lines) | c2 676-823 | **medium** — these are the ways a wrong tool shape still yields a decision | keep one parser per retained interface; delete the index-base voting and the depth-4 scan |
| 6 | C2 `FEATURE_ALIASES`: 23 spellings; 16 never appear in the frozen manifest; the only live non-identity alias `files`→`published` collides by name with `carriers[].damage.files` | c2 160-172 | **medium** — canonicalization turns key drift into a scored dimension instead of the missing-tuple failure the binding exists to raise | drop the map; compare canonical names, fail on unknown keys |
| 7 | Test harness inside the frozen artifact: c1 selftest + fixtures, c2 stubs + selftest | c1 1803-2060, 2063-3235; c2 1654-1925, 1929-2495 | **medium** — 1415 lines (41 %) and 839 lines (34 %); a harness bug cannot be fixed without a refreeze, and the fixtures re-implement contracts the frozen tools own (`sb_carrier` = a second AVM superblock model, `mk_env`/`rehost` = a second receipt model, three stubs with `@@MODE@@` switchboards) | move to `tests/round-41/…` and freeze only the scored modules; the refreeze must name both files because the kill rules cite the selftest |
| 8 | `selftest_rea` + `DEV_AVM_IMAGE` absolute path into `/home/vgpnk/Projects/shokuknow/...` | c1 300-301, 3238-3409 | **medium** (false red / portability) — not named by any counting command or kill rule; `SystemExit` on a checkout without that path | drop, or gate it behind an explicit image argument and verify the image's sha256 |
| 9 | `legacy_same_rel` (verbatim round-40 suffix matcher) + probe `want_legacy` half + `discriminating >= 3` guard | c1 969-973, 2439-2444, 3118-3127 | **low** (inert) — but the selftest *requires* ≥3 of 6 probes to discriminate against it (measured 3), and the kill rule names it ("both collision directions under the round-40 suffix matcher") | delete with a claims rewording: the five scored-pipeline fixtures at 2486-2529 already pin both collision directions through `measure`; keep `same_rel`'s own `want_new` assertions |
| 10 | `--no-rerun` | c1 1755, 1763-1771 | **low** — a flag whose only behaviour is exit 2 with a fixed message | drop |
| 11 | `OPERATION_TOKEN` (zero loads) | c2 175 | **low** | drop; the operation test is the interpreter's step 1 |
| 12 | duplicate frontier authority: `frontier_note` (mark + stem) is a strict subset of `c1-extra.py`'s `frontier_content` (parsed verdict) | c1 1695 | **low** — two authorities for one sentence | keep `c1-extra`'s; reduce the counter's to the marker or drop it |

Keep, explicitly: C1's exact-path/derivation-root matcher (`same_rel`/`extract_rel`/`subject_root`) and
`disposition_check` — that is the round-40 defect repair the claim exists for; C1's `FROZEN_PATHS`
(10 named files, the model C2 should copy); C2's `observed_features` and the `REQUIRED_FEATURES` gate;
C2's `bindings_undeclared` / `bindings_declared_unset` agreement checks; both `--selftest` harnesses.

## 4. Tradeoffs and limits

- Items 1, 3 and 5–12 are *deletions of dead branch space*: no scored behaviour changes. Item 1 is
  the exception, and its change is small in blast radius — I verified with the frozen tools at the
  same `--rev`/`--freeze` that only the declared-source rows move.
- Item 2 is a *loosening of the freeze set*, which is why I rank it second rather than second-to-last:
  it removes over-blocking, not teeth (`frozen_units`' per-file shas stay).
- Items 7 and 8 need a claims edit as well as a code move; item 9 needs the kill-rule sentence
  reworded from "the round-40 suffix matcher" to "the collision fixtures". I did not edit
  `plans/`, `tools/` or `SKILL.md` (out of scope for this seat).
- Not claimed: that R41-C2 is MET. The frozen counter at `e9a24d07` still exits 1 and the report
  that says so stands; what I show is that the failure is in the reader, and I did not re-run REA or
  unblob, fetch vendor bytes, or touch any carrier.
- Untested by me: the three C2 controls under `controls/c2/` and C1's `--selftest-rea` (needs the
  development image outside the lane). Both selftests that I could run are green at tip (above).

## 5. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r41/R41W2Simplify ; L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
mkdir -p "$S" && cd "$S" && export HYAKU_SCRATCH="$S/hy" TMPDIR="$S"
python3 -I -B "$L/tools/round-41/c2-counter.py" --selftest
python3 -I -B "$L/tools/round-41/c1-counter.py" --selftest \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
python3 -I -B "$L/tools/round-41/c2-counter.py" --root "$L" \
  --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f
cp "$L/tools/round-41/c2-counter.py" c2-counter.onekey.py   # apply patch-onekey.diff
python3 -I -B c2-counter.onekey.py --root "$L" \
  --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f
```

Artifact rebuilding: `feature-compare-52.json` is produced by importing `c2-counter.py` from the lane
(`envelope_data`, `observed_features`, `canon_features`) over
`corpus/evidence/round-41/c2/heldout/{manifest.json,<ID>/envelope.json}`; the two score receipts are
that counter's `--json-out` at `e9a24d07`. All artifacts are < 100 kB; nothing here redistributes
vendor bytes.

## 6. Housekeeping

- Tool installs: none. No pacman, no `uv tool`, no npx/REA run, nothing written to a PATH directory.
  Only `git` (read-only), `python3 -I -B`, `sha256sum`, `diff` and the lane's own frozen tools ran.
- Lane tree untouched: no VCS mutation, no write outside `.ufo/waves/round-41/w2/R41W2Simplify.md` and
  `.ufo/waves/round-41/w2/artifacts/R41W2Simplify/`. Scratch `S` removed before yielding; probe
  sources were copies inside `S`, the lane's counters were opened read-only and imported, never
  written.
