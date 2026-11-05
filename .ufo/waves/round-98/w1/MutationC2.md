# MutationC2 — mutation test of stop-boundary-repair-battery-v8.py under frozen C2

Seat: MutationC2 (mutation-tester). Lane: kaidoku R98 attempt 1. Rev under test: L = 72346895a35a74af18151b125934fa0c09fe1e3c.

## Setup (commands run)
- `git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone && git -C $S/clone checkout --detach 72346895a35a74af18151b125934fa0c09fe1e3c` (S=/fast/scratch/hyaku/kaidoku-r98/MutationC2). HEAD verified `72346895a35a74af18151b125934fa0c09fe1e3c`; toplevel verified = $S/clone.
- Pristine counter sha256 `7a9837466d2d4eeb0a8096b71b8033c970ac2c43e00ec6f10cc8dd4f6de08a83` (identical in clone and lane).
- Each mutant: edited in place in `$S/clone/tools/round-98/stop-boundary-repair-battery-v8.py` (edit tool), then `score-mutant.sh NAME`: runs the frozen checker
  `python3 -I -B tools/round-98/allowlist-check.py --counter tools/round-98/stop-boundary-repair-battery-v8.py --rev 72346895... --work $S/work/NAME --json-out $S/receipts/NAME.json`
  and a semantic probe `semantic.py` (same real14/stub9/extra inputs, plus verify_receipt on honest and malformed receipts, no subprocess), then restores pristine bytes and asserts the sha256.
- Pristine control: frozen checker exit 0, `legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1 met True`. Semantic probes all 1.
- Tools installed: none. Scratch is removed at exit (trap-delete).

## Results (14 mutants; rc = public subprocess return code, exit = checker exit)
| # | Mutant | Frozen label | rc/exit | Semantic probe signal | Verdict |
|---|---|---|---|---|---|
| M1 | drop `silent` from COUNT_KEYS | legs passed 2 of 4; public 0; real14 0; stub9 1; extra 1 | 1/1 | real14=0 | KILLED (semantic) |
| M2 | add `bogus` to COUNT_KEYS | legs passed 1 of 4; public 0; real14 0; stub9 1; extra 0 | 1/1 | real14=0 extra=0 | KILLED (semantic) |
| M3 | skip missing-key append | legs passed 2 of 4; public 0; real14 1; stub9 0; extra 1 | 1/1 | stub9=0 | KILLED (semantic) |
| M4 | skip extra-key loop | legs passed 2 of 4; public 0; real14 1; stub9 1; extra 0 | 1/1 | extra=0 | KILLED (semantic) |
| M5 | accept bool as int | legs passed 3 of 4; public 0; real14 1; stub9 1; extra 1 | 1/1 | bool_int_refused=0, verify_bool_refused=0 | KILLED only by public confound |
| M6 | invert verify_receipt `ok` | legs passed 4 of 4; public 1; real14 1; stub9 1; extra 1 met True | 0/0 | verify_honest_ok=0 | **SURVIVES frozen predicate** |
| M7 | skip schema extend in verify_receipt | legs passed 3 of 4; public 0 ... | 1/1 | verify_missing_key_refused=0, verify_bool_refused=0 | KILLED only by public confound |
| M8 | fail-closed `code = 1` -> `code = 0` | legs passed 3 of 4; public 0 ... | 0/1 | none (branch unreachable in-process) | KILLED only by public confound |
| M9 | exempt `bogus` only from extra check | legs passed 2 of 4; public 0; real14 1; stub9 1; extra 0 | 1/1 | extra=0 | KILLED (semantic) |
| M10 | skip met-typed check | legs passed 3 of 4; public 0 ... | 1/1 | none (no non-bool met probe) | KILLED only by public confound |
| M11 | non-dict counts -> refused | legs passed 3 of 4; public 0 ... | 1/1 | none (all legs pass dicts) | KILLED only by public confound |
| M12 | drop `fresh_scored` from NINE_LABEL_KEYS | legs passed 3 of 4; public 0 ... | 1/1 | none (selftest-only consumer) | KILLED only by public confound |
| M13 | fail-open: `if code == 0 and selfverify["ok"]` | legs passed 3 of 4; public 0 ... | 0/1 | none (main-only branch) | KILLED only by public confound |
| M14 | drop `not schema` guard in label branch | legs passed 3 of 4; public 0 ... | 1/1 | direct: missing `wrong` -> KeyError (not refusal) | KILLED only by public confound; divergence on direct API |

Receipts: `.ufo/waves/round-98/w1/MutationC2/` (frozen JSON per mutant, `.stdout`, mutated `.counter.py` copies with sha256 prefixes, `semantic.py`, `score-mutant.sh`). Semantic outputs: `$S/receipts/NAME-semantic.json` (copied).

## Findings
1. **[defect, high] The frozen C2 public leg is confounded for every in-place mutant.** The public subprocess verifies its own receipt with byte binding (`counter_sha256` vs the blob at `--rev`). Editing the frozen counter dirties the tree, so every mutant's selfverify reports `byte-pin-not-bound:counter` (see `M1..M14` public_stderr). The public leg therefore fails for any mutant, independent of its semantics. Consequence: 8 of 13 frozen kills (M5, M7, M8, M10–M14) are attributable to the byte pin, not to the mutated behavior. Only M1–M4 and M9 are killed by the three semantic legs the C2 contract describes. A committed mutant at a new revision (the byte binding's intended use) would be needed to score the semantics through the public leg; this seat cannot commit (no mutating git).

2. **[defect, high] M6 (inverted `ok` in verify_receipt) passes the frozen predicate.** Its `ok` is `bool(reasons)`, which returns True exactly when a reason exists. The dirty tree always adds `byte-pin-not-bound:counter`, so the public run prints `selfverify ok=True reasons=1` and the checker reports `legs passed 4 of 4; public 1; ... met True`, exit 0 (receipt `M6-invert-verify-ok.json`, public_stdout and public_stderr confirmed). A verifier that refuses every honest receipt is accepted by C2. The semantic probe catches it (`verify_honest_ok=0`); the frozen checker does not call verify_receipt on an honest receipt outside the public subprocess.

3. **[blind spot] Behavior not exercised by any C2 leg.** The C2 checker calls only `count_problems` (real14/stub9/extra) and the public subprocess. Survivors on the semantic axis (probes all pass for the mutant):
   - M5 (bool accepted as int): `count_problems({..., wrong: False})` returns no reason. Not probed by C2. Not equivalent: a real defect in the schema.
   - M7 (no schema in verify_receipt): semantic probe catches it, C2 does not.
   - M10 (non-bool `met` unchecked), M11 (non-dict counts passed), M12 (NINE_LABEL_KEYS): C2 never feeds these inputs. M12's only consumer is `_selftest`, which C2 never runs.
   - M8 and M13 (the fail-closed gate in `main`): reachable only when selfverify fails in the public run, which in this seat happens only through the byte-pin confound. The gate is unexercised on a clean tree.
   - M14 (no `not schema` guard): **equivalent on every path `main` reaches** (its receipts always carry all keys, so schema is empty). Not equivalent for direct callers: a receipt missing a NINE key (`wrong`) raises `KeyError` from `recompute_label` instead of returning `ok=False` (checked directly on the mutant: `RAISES KeyError: 'wrong'`; baseline returns the schema refusal by the `if not schema:` guard).

4. **[equivalence arguments]**
   - M11 is equivalent on every dict input any leg supplies; differs only for non-dict input (blind spot above).
   - M12 is equivalent for every C2 leg; it changes only the counter's own selftest case (`tools/round-98/stop-boundary-repair-battery-v8.py:399-400`).
   - M10 is equivalent on honest receipts (bool `met` always), differs only on malformed `met` (blind spot).

## Summary counts
- Mutants: 14 (all eight requested categories covered: M1 drop key, M2 add key, M3 skip missing-key loop, M4 skip extra-key loop, M5 accept bool, M6 invert ok, M7 skip schema in verify, M8 return code 1 -> 0 in the fail-closed gate; M9–M14 extra).
- Killed by frozen predicate: 13 (5 semantic: M1–M4, M9; 8 byte-pin confound only).
- Survived frozen predicate: 1 (M6).
- Detected by semantic probes, undetected by frozen predicate: M5, M6, M7, M14.
- Undetected by any probe in scope: M8, M10, M11, M12, M13 (blind spots / main-only / selftest-only / non-dict).

## Verdict line
C2 frozen predicate is not sensitive to its own semantics: 8 of 13 kills come from the byte-pin confound, and an inverted verify_receipt (M6) passes `legs passed 4 of 4; public 1`, exit 0.

## Lane observation (not my change)
Lane HEAD read as `9cb930014a57c9b29d830739e0c4229f6e7e7016` at check time (clone at L is unaffected). `corpus/SOURCES.md` shows a pre-existing modification from another seat; this seat did not touch it. Lane writes: only `.ufo/waves/round-98/w1/MutationC2/` and this report.
