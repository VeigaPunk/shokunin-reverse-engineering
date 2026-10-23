# ExecFreezeSelftest — round-34 freeze-integrity selftest + pin verification

- **Seat:** `KaidokuR34.ExecFreezeSelftest` (UFO-FSD executor, leaf)
- **Lane root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only for this seat)
- **Sandbox:** `/fast/scratch/hyaku/kaidoku-r34/w1/ExecFreezeSelftest`, branch `seat-r34-ExecFreezeSelftest`, HEAD `54a87a51a865ab931fd355e767303337b05cccf4`, worktree clean before and after
- **Freeze rev:** `54a87a51a865ab931fd355e767303337b05cccf4` (both `--rev` and `--freeze`)
- **Scope:** `tools/round-34/freeze-integrity.py` only. No production parser (`elf-version-needs.py`) run, no counter run, no REA run, no binary fixtures authored, no production/shared file edited, no installs/updates, no shared production edits.

## 1. Headline result

| Item | Result |
|---|---|
| `--selftest` (run **exactly once**) | **exit 1 — FAIL**, 24/25 cases PASS, `failed=restored_after_change` |
| Root cause of the failure | **not a gate defect.** A *substring-collision bug in the selftest's own assertion* for the `restored_after_change` case. The gate behaved correctly (exit 1, digest matches, history flagged). |
| Read-only `--round 34 --rev 54a87a51…` over actual frozen claims | **exit 0 — `freeze-integrity: CLEAN pins=21 freeze=54a87a51a865 rev=54a87a51a865ab931fd355e767303337b05cccf4`**, at lane root **and** in the sandbox; 21/21 `ok` rows, zero `FAIL` rows |
| Independent digest re-verification of all 21 pins at the freeze rev | **0 mismatches** |
| Predicate | Preserved verbatim. No rule, target, pin, or digest was repaired, rescaled, or amended by this seat. |

## 2. Exact run 1 — `--selftest` (exactly once)

```
argv:   ['python3', '-I', '-B', 'tools/round-34/freeze-integrity.py', '--selftest']
cwd:    /fast/scratch/hyaku/kaidoku-r34/w1/ExecFreezeSelftest
UTC:    2026-10-23T10:52:49.321936Z -> 2026-10-23T10:52:51.608549Z  (elapsed 2.29 s, timeout 180 s, not timed out)
exit:   1
stderr: <empty>
```

stdout (verbatim):

```
case clean: PASS freeze=1ae5a96f06e8 pins=2 exit=0
case tampered_pin: PASS exit=1 changed=1 sha=2412b990a7d3
case restored_after_change: FAIL restore commit must still fail: 'FAIL\tbin/tool.py\tsha=94eb0c109cd7\tcommits_after_freeze=0516618,be39d4e'
case absent_claims: PASS exit=2 claims=.ufo/waves/round-99/claims.json absent
case missing_pinned_file: PASS exit=1 sha=absent changed=1
case compat_absent_frozen_inputs: PASS exit=0 pins=1
case compat_empty_frozen_inputs: PASS exit=0 pins=2
case compat_round32_shape: PASS exit=0 pins=8
case schema_empty_instruments: PASS exit=3 code=instruments_empty
case schema_omitted_instruments: PASS exit=3 code=instruments_missing
case schema_no_pin_keys: PASS exit=3 code=instruments_missing
case schema_empty_list_instruments: PASS exit=3 code=instruments_not_object
case schema_empty_string_instruments: PASS exit=3 code=instruments_not_object
case schema_pair_list_instruments: PASS exit=3 code=instruments_not_object
case schema_empty_list_frozen_inputs: PASS exit=3 code=frozen_inputs_not_object
case schema_null_instruments: PASS exit=3 code=instruments_not_object
case schema_null_frozen_inputs: PASS exit=3 code=frozen_inputs_not_object
case schema_bad_digest: PASS exit=3 code=pin_digest_format
case schema_absolute_pin: PASS exit=3 code=pin_path_not_relative
case schema_parent_pin: PASS exit=3 code=pin_path_not_relative
case schema_empty_pin_key: PASS exit=3 code=pin_key_empty
case schema_duplicate_pin: PASS exit=3 code=pin_path_duplicate
case schema_malformed_json: PASS exit=3 code=claims_not_json
case schema_top_level_array: PASS exit=3 code=claims_not_object
case schema_top_level_null: PASS exit=3 code=claims_not_object
freeze-integrity-selftest: FAIL cases=25 failed=restored_after_change elapsed_s=2.23
```

Retained: `ExecFreezeSelftest-files/selftest-run.json`, `selftest-stdout.txt`, `selftest-stderr.txt`.

Tool under test is byte-identical to the frozen pinned instrument:
`sha256(tools/round-34/freeze-integrity.py) = fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138`
= the `instruments` pin in `.ufo/waves/round-34/claims.json` = the lane copy = the prep copy (`.ufo/waves/round-34/prep/R34FreezeSchema-files/freeze-integrity.py`).

## 3. Exact run 2 — read-only gate over the actual frozen claims

```
argv: ['python3','-I','-B','tools/round-34/freeze-integrity.py','--root','/home/vgpnk/Projects/shokunin/kaidoku-shokunin',
       '--round','34','--rev','54a87a51a865ab931fd355e767303337b05cccf4']
UTC:  2026-10-23T10:54:06.052745Z -> 2026-10-23T10:54:06.282573Z  (elapsed 0.23 s)   exit 0
argv: [... '--root','/fast/scratch/hyaku/kaidoku-r34/w1/ExecFreezeSelftest' ...]
UTC:  2026-10-23T10:54:06.282830Z -> 2026-10-23T10:54:06.475470Z  (elapsed 0.19 s)   exit 0
```

Both roots, identical verdict:

```
freeze-integrity: CLEAN pins=21 freeze=54a87a51a865 rev=54a87a51a865ab931fd355e767303337b05cccf4
```

21 `ok` rows, zero `FAIL` rows: 4 `instruments` (`version-needs-counter.py`, `elf-version-needs.py`, `freeze-integrity.py`, `prep/R34Expected-files/author_expected.py`) + 17 `frozen_inputs` (expected.json, approved-skill-section.txt, 2 source captures, 12 ELF carriers `e01.bin`–`e12.bin`, 1 knowledge doc). Full stdout retained in `ExecFreezeSelftest-files/gate-round34-stdout.txt` and `pin-verification.json`.

Independent cross-check (not via the tool): every pin digest recomputed with `hashlib.sha256` over `git show 54a87a51…:<path>` in the lane repo — **21 pins checked, 0 mismatches** (`pin-verification.json`).

Additional read-only pass at `--rev HEAD` (lane HEAD `d52e2404ea0160de990d28df673011bb671829f8`, one commit after the freeze): `CLEAN pins=21`, `commits_after_freeze=0` for every pin — the one post-freeze commit touches no pinned path (`gate-at-head.json`).

## 4. Root cause — the frozen selftest's own assertion is hash-prefix-collision prone

The failing case asserts on a **substring of the whole rendered line**:

```python
# tools/round-34/freeze-integrity.py:297  (identical at tools/round-33/freeze-integrity.py:180)
_check("commits_after_freeze=0" not in lines[0], "restore commit must still fail: %r" % lines[0])
```

The gate's field is `commits_after_freeze=<comma-separated short hashes>` (or the literal `0`). When the list is non-empty the field begins with a hex hash, so the literal text `commits_after_freeze=0` **is a substring** of `commits_after_freeze=0516618,be39d4e` — the assertion then fires on a *correct* gate and the case is reported FAIL. The check should compare the field value, not search for a substring.

The observed failing line is exactly this shape: the gate printed `FAIL bin/tool.py sha=94eb0c109cd7 commits_after_freeze=0516618,be39d4e` — digest **matches** the pin (restored bytes) and the **history flag is present** (two post-freeze commits listed), i.e. the gate did the right thing; the assertion mis-read it.

**Mechanism confirmed exactly (N=200 independent disposable Git fixtures, frozen assertion vs. rendered line):**

| Quantity | Value |
|---|---|
| Spurious failures of the frozen assertion | **16/200 = 0.0800** |
| Fixtures whose first post-freeze short hash begins with `0` | **16/200 = 0.0800** |
| Correspondence mismatches | **0 — mechanism exact** |

The failure occurs iff the first post-freeze short hash starts with the hex digit `0` (theoretical 1/16 = 0.0625; observed 0.080 over 200 draws). It is **nondeterministic**: the fixture commit hashes vary per run, so the same frozen bytes pass or fail depending on the clock.

Corroborating evidence that this is a latent, not a one-off, defect:
- The L1's own prep receipt `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/receipt.json` records `selftest.exit = 0` at `2026-10-23T10:26:30Z`, with `case restored_after_change: PASS … commits_after_freeze=f9d4a9b,4f68497` — a hash list whose first hash starts with `f`, so the collision did not trigger there. The green prep receipt is therefore **not reproducible**; the same bytes failed at 10:52:49Z in this seat's run.
- The round-33 ancestor carries the identical assertion (`tools/round-33/freeze-integrity.py:180`), and round-33's prep receipt `R33FreezeSelftest.md` likewise records a green run with `commits_after_freeze=3c3aa5f,875ddb6`. The defect is inherited, not introduced by round-34. Rounds 31/32 have no `_case_restored` case at all, so the assertion entered the family in round-33.

Scope of impact: **the defect is in the selftest's verification logic, not in the gate's decision logic.** The gate's own verdict on the real frozen claims is CLEAN under both the pristine and the patched tool (§5). Nothing in this wave's frozen pins, digests, or predicate is affected.

## 5. Bounded repair falsification (scratch copies only — frozen files untouched)

Candidate repair, replacing the substring search with a field-value comparison:

```python
_field = lines[0].split("\t")[-1]
_check(_field != "0" and _field != "", "restore commit must still fail: %r" % lines[0])
```

Retained as `ExecFreezeSelftest-files/freeze-integrity.patched-candidate.py`
(sha256 `4f131413ab9ff6c14dd673db7826aace98763df53313b2d5fdd15a0a23df5df0`).

| Probe | Result |
|---|---|
| Patched candidate, 8 consecutive `--selftest` runs | **8/8 `PASS cases=25`, exit 0** |
| Patched candidate vs 200 synthetic restored-case fixtures | **0 spurious failures** (frozen assertion: 16/200) |
| Patched candidate on the real frozen claims | `CLEAN pins=21 freeze=54a87a51a865 rev=54a87a51…`, exit 0 — verdict unchanged |
| **Mutant kill preserved:** gate mutant with the post-freeze history check dropped (`ok = got == digest`, dropping `and not touched`), run against the **patched** candidate | restored case **FAILS** (`expected exit 1, got 0`) → mutant still killed |
| Same history-dropped mutant against the **pristine** frozen tool | restored case **FAILS** → identical kill power |
| Patched candidate on the pristine gate | restored case **PASS**, `commits_after_freeze=0e8f55f,de72cb3` |

So the candidate repair removes the nondeterminism **without** weakening the case's ability to kill the history-check mutant — the property the case exists to protect. Evidence: `repair-falsification.json`, `repair-mutant-kill.json`.

**No production file was edited by this seat.** `git status --porcelain` over `tools/`, `.ufo/waves/round-34/claims.json`, `.ufo/waves/round-34/expected.json` and `corpus/evidence/round-34/` is empty; the sandbox copy of `tools/round-34/freeze-integrity.py` is byte-identical to the pinned digest after all probes (`fe955c57…`). The patched candidate is a retained scratch artifact only; landing it is the L1's decision, not this seat's.

## 6. Containment and hygiene

- Selftest ran under `subprocess.run(..., timeout=180)`; elapsed 2.29 s. Gate runs under timeout 180 s (0.19–0.23 s each). Patched-candidate runs and the 200-fixture measurement were likewise bounded.
- `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` stripped from every child env, exactly as the tool does.
- All Git writes were confined to disposable `git init` fixtures under my own scratch (`/fast/scratch/hyaku/kaidoku-r34/w1/ExecFreezeSelftest-probe`, `…-probe2`), each removed in a `finally` block. `/usr/bin/find` confirms **0 leftovers** in the tool's own `/fast/scratch/hyaku/kaidoku-r34/R34FreezeSchemaSelftest` base and in my probe dirs (both probe dirs removed).
- No target binary was executed; no production parser/counter was run; no binary fixture authored; the 12 ELF carriers were only read as bytes for digest re-verification (`git show` → sha256), never executed.
- No background job, delegate, broadcast, or operator-config write. No tool install/update was performed, so no install receipt applies.
- Lane `git status` shows only other seats' wave artifacts plus my own `ExecFreezeSelftest-files/`; production content is untouched.

## 7. Findings for the L1

1. **The frozen round-34 freeze-integrity instrument's `--selftest` is nondeterministic and can report a false FAIL** (rate ≈ 1/16 per run, 16/200 measured) because of the substring assertion at `tools/round-34/freeze-integrity.py:297`. The gate logic is unaffected. The L1's green prep receipt (exit 0 at 10:26:30Z) is a lucky sample and is not reproducible.
2. **The pin verification itself is sound**: `CLEAN pins=21` at both the lane root and the sandbox, plus 21/21 independent digest matches at the freeze rev, and CLEAN still holds at the post-freeze lane HEAD. Claim R34-C1's frozen pins are intact as of this measurement.
3. **The same assertion is inherited from round-33** (`tools/round-33/freeze-integrity.py:180`), so this is a family-level latent defect, not a round-34 regression. A repair that lands in round-34 alone leaves the round-33 successor gate (SKILL.md registry row 1092) still flaky.
4. **A minimal, mutation-preserving repair exists** and is falsified in both directions (§5): field-value comparison instead of substring search; kills the history-drop mutant exactly as the frozen assertion does; 8/8 green selftest runs; real-pin verdict unchanged.
5. Recommended L1 action (not executed here): land the field-value repair in the round-34 successor, and record in the registry row for `Schema-validating freeze integrity` (SKILL.md:1188) that the selftest was flaky at ≈1/16 prior to the repair, with this seat's red run as the able-to-fail evidence. Note that the repair changes the instrument's bytes, so it must be handled as a **new instrument revision with a re-freeze and a new pin**, not as an in-place edit of the pinned `fe955c57…` file.

## 8. Files

Changed (lane, my exclusive scope only):
- `.ufo/waves/round-34/w1/ExecFreezeSelftest.md` — this report
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/selftest-run.json`, `selftest-stdout.txt`, `selftest-stderr.txt` — the single `--selftest` run (argv/UTC/exit/stdout/stderr)
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/gate-round34-run.json`, `gate-round34-stdout.txt` — read-only `--round 34 --rev 54a87a51…` runs
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/pin-verification.json` — both-root gate runs + independent 21-pin digest re-verification
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/gate-at-head.json` — additional read-only pass at `--rev HEAD`
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/repair-falsification.json` — 8 patched selftest runs + patched gate on real pins
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/repair-mutant-kill.json` — mutant-kill comparison (patched vs pristine)
- `.ufo/waves/round-34/w1/ExecFreezeSelftest-files/freeze-integrity.patched-candidate.py` — retained candidate repair (scratch artifact; sha256 `4f131413…`)

Modified in the sandbox clone: **none** (worktree clean; no commits, no branch change).

## 9. Blockers / risks

- None blocking. The only judgement call left to the L1 is whether to land the repair and how to re-freeze, since the repair changes the pinned instrument bytes and the lane is read-only for this seat.
- Residual risk: any downstream consumer that treats `--selftest` exit status as a green/red gate inherits a ≈1/16 false-red rate until the repair lands. The gate's own verdict on production content is unaffected.
