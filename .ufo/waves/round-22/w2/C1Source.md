# C1Source — R22-C1 counter review (bound record vs round-22 S### citation)

Reviewer: KaidokuR22R.C1Source-6 · 2026-10-21 · lane: kaidoku-shokunin (read-only; only this report + same-name `.json` written)
Target: `.ufo/waves/round-22/tools/count-c1.py` (working tree, git hash-object `50b49a22271e9b2bba7e83be603002cb51b861ed`, mtime 10:19:47). No installs, no REA invocation, no ADB contact, no lane code edits; all adversarial cases ran in temp git clones via `/tmp/c1w2-attack.py`.

## 0. Mid-flight rewrites observed (process risk)

The counter changed **twice while this review ran**: `38e5ef5` (HEAD-committed v1, bare-record bind, worktree helpers) → `f243b9f…` (10:12:18, v2: `bind_cli` envelope binding, `CLI_BIND_VERB`, rev-pinned helpers) → `50b49a2…` (10:19:47, v3: `source:` must be the file's first line, tier A/B gate, `data` must be a direct record, raw/normalized refusal walk, `allow_nan` round-trip). My first baseline run printed the v1 limit line and the HEAD run seconds later printed the v2 limit line from the same command block — the file was rewritten between the two subprocess spawns. **Any verify.py run started before 10:19:47 predates v3 and must be re-run.**

## 1. Lane measurements with the current (v3) counter

```
python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev 7787fea4…   → exit 1, t1_exercised_count 0/6   (= before_expected)
python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev HEAD        → exit 1, t1_exercised_count 1/6
    witness: ["ev_3458b996…d866b", ".ufo/waves/round-22/evidence/c1/identify-godot.envelope.json"]
    unsupported_candidates: identify-godot-run.json, identify-godot.evidence.json (bare-record reps correctly unevaluable)
python3 -I -B .ufo/waves/round-22/tools/count-c1.py --selftest                      → exit 0 (11 C1 controls, incl. helper_drift and forged_debug_operation)
```

## 2. Assigned falsifier — "bound matching record but entry lacks round-22 S### citation"

Direct forms are **blocked** by v3 (all observed in temp clones, counter argv `[python3, -I, -B, <lane>/count-c1.py, --root, <tmp>, --rev, <sha>]`, each case exit 1 with per-verb `exercised=false`):

| case | entry first line | bound record cited | exercised |
|---|---|---|---|
| `no_source_direct_target` | `source: none` | yes | false (blocked) |
| `old_row_only` | `source: S007` | yes | false (blocked) |
| `entry_unlisted` | `source: S051`, row's used-by names another file | yes | false (blocked) |
| `codeblock_source_line` | `source: S051` only inside a fenced block | yes | false (blocked by first-line rule) |

However, **two residual paths still count a bound record for an entry whose round-22 linkage is defective**, plus one refusal-envelope hole:

### F1 (HIGH) — duplicate-row forgery makes an unlisted entry eligible
`source_rows[cells[1]] = …` overwrites silently; SOURCES.md is parsed for qualifying rows anywhere in the file. Observed (`duplicate_row_forgery`): honest `| S051 |` row naming `other.md`, plus a second `| S051 |` row naming `entry-b.md` → `entry-b.md` (whose real citation to S051 does not exist) becomes eligible, its bound envelope counts: `t1_exercised_count=1`, per-verb `exercised=true`. This is exactly the assigned falsifier: the counted entry's round-22 "citation" is a forged duplicate, not the honest row. Narrow fix, inside the existing row loop:

```python
if cells[1] in source_rows:
    raise ValueError("duplicate_source_row: " + cells[1])
source_rows[cells[1]] = cells[11].split(",")
```

(main already maps ValueError → exit 2 unevaluable, so a duplicated registry fails loud instead of admitting forged linkage.)

### F2 (MEDIUM) — typed refusal inside `meta` counts
`bind_cli` checks `r21.refused(envelope)` (never descends into `meta`) and the v3 walk only follows `raw_result`/`normalized_result` and `ok != True` nodes. Observed: `{"ok":true,"data":{bound},"meta":{"command":"identify-flutter-build","error":{"code":"execution_failure"}}}` → exercised=true; same with `meta.exit_code=1` → exercised=true. Hits declared falsifier "a typed refusal envelope counts". Fix in `bind_cli`, after the `refused(envelope)` check: `if r21.refused(envelope.get("meta")): return 1`, and add `"meta"` to the pending-walk keys. (No retained envelope carries refusal in `meta` — real meta is `{command, duration}` — so the fix cannot regress honest data.)

### F3 (MEDIUM) — directory citation counts a file the entry never names
`r20.is_cited` accepts cited prefixes ending `/`, so an eligible entry citing only `.ufo/waves/round-22/evidence/c1/` binds a witness from `identify-flutter-build.json` inside it (observed: exercised=true), contradicting the docstring's "cites a retained file … by full lane path". Fix: in `measure()`, `r20.is_cited = lambda path, cited: path in cited` (exact match). The real r22 entry cites three full file paths, so no honest regression.

### Low-severity notes
- **F4** witness gate is `text in eligible` keyed by file *content*: a byte-identical ineligible clone of an eligible entry would pass the gate. No count delta today; track eligible paths, not texts.
- **F5** eligibility uses `any()` over S### tokens on the first line: one qualifying naming row suffices even if the line also cites rows that do not name the entry. Consistent with the declared manual limit; an `all()` variant would close mixed-citation drift at the cost of false negatives.
- **F6** `revision_helpers` loads helpers at the raw `--rev` before `resolve_revision` validates it; fails safely today (git rejects odd tokens) but a `'HEAD'` TOCTOU exists. Resolve first, pass the resolved sha.

## 3. Hardening confirmed working (adversarial, observed false)

`ok:false` envelope; record-level `error.code` inside `data`; bare-record R21 representation (never counts, reported as `unsupported_candidates`); `source:`-inside-code-fence (v3 first-line rule); forged `debug_with_gdb`/`debug_with_rizin` data operations (fixture expects 4/6, passes); worktree helper tampering (`helper_drift` expects 6/6 — helpers are loaded from rev blobs via `revision_helpers`). `CLI_BIND_VERB` is grounded in rea-agents 6.5.0 dist (`reconstructionObligationLedgerSchemas-Bao0xMr-.js:949` maps `"debug-with-gdb": ["gdb_console"]`; tool contracts name `gdb_console`/`rizin_debug_command`). That `meta.command` equals the catalog verb for the two debug verbs is [INFERENCE] from package source; the retained identify envelope confirms the pattern (`meta.command == "identify-flutter-build"`) and CLI execution is forbidden this wave.

## 4. Residual risk / verification gaps

- SOURCES row truthfulness (mined / opened 2026-10-21 / tier / used-by) stays manual, as the limit string declares; a well-formatted dishonest row is undetectable mechanically.
- L1 must re-run `verify.py` after the final counter lands (see §0 race) and re-record `script_sha256`.
- `count-c2.py` and the frozen v1 red controls were out of scope and not reviewed. No tool installs were made.
