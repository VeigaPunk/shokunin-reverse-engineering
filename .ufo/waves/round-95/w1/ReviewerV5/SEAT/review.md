# ReviewerV5 — seat review (kaidoku round-95, attempt 1)

Revision reviewed: **4bda1d1dd3788973f10e61212b70df18b3b14ea0** (declaration commit; base
b5331db1fb0ce0bf93695ce1730cf831effef6a9). Method: all four round-95 tools read in full at
the frozen commit, all four selftests executed in a shared clone, the frozen counting
commands reproduced (honest v5 public run, forgery battery, v5 probe, v4 probe control),
plus adversarial scratch patches (recorded inline here as `diff` evidence, not lane
patches — the lane was not touched; every patch lived in the scratch clone and was
deleted after use).

## Pinned-byte verification (prework precondition)

| file | pinned sha256 | measured at 4bda1d1d | match |
|---|---|---|---|
| `tools/round-95/stop-boundary-repair-battery-v5.py` | `6fc81208…94b7f` | `6fc81208…94b7f` | OK |
| `tools/round-95/c1-agreement-v2.py` | `ca7d213a…39291` | `ca7d213a…39291` | OK |
| `tools/round-95/c1-forgery-refusal.py` | `8e43d7cf…0ff22` | `8e43d7cf…0ff22` | OK |
| `tools/round-95/symlink-probe.py` | `e07ff669…090ee` | `e07ff669…090ee` | OK |
| `tools/round-94/c1-receipt-agreement.py` | `dc384a44…836c9` | `dc384a44…836c9` | OK |
| `tools/round-93/stop-boundary-repair-battery-v3.py` | `60026511…cbd4e3` | `60026511…cbd4e3` | OK |

V3 verdict at base (b5331db1f) also matches the pin — the imported-by-path verdict code is
unchanged between base and declaration.

## Selftest exit codes (clone at 4bda1d1d, scratch `--work`)

| tool | selftest invocation | rc |
|---|---|---|
| v5 | `python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --selftest --work $S/work/st5` | 0 |
| c1-agreement-v2 | `python3 -I -B tools/round-95/c1-agreement-v2.py --selftest $S/work/st2` | 0 |
| c1-forgery-refusal | `python3 -I -B tools/round-95/c1-forgery-refusal.py --selftest $S/work/st-battery` | 0 |
| symlink-probe | (no selftest mode — public CLI exercised directly below) | — |

## Frozen-command reproduction (live, at the frozen commit)

| command | rc | key evidence |
|---|---|---|
| v5 honest public run `--json-out` | 0 | `selfverify ok=True reasons=0`; label = frozen; `counts` recomputes; `revision` = 4bda1d1d; `verdict_sha256` = 60026511 (v3 pin); `counter_sha256` = 6fc81208 (v5 pin) |
| v5 probe (`identity_noop`, planted `<json-out>.tmp` symlink) | 0 | `victim_intact True`, `receipt_valid True`, `verdict hardened`, `writer_rc 1` |
| v4 probe (premise control, same probe) | 1 | `victim_intact False`, `receipt_valid True`, `verdict followed-symlink` — the F1 premise reproduces live, not just in the committed pre receipt |
| forgery battery frozen command | 0 | `forgeries refused 4 of 4; before admits True; honest accepted True`; reasons are exactly pos→`label-not-frozen`, F1→`label-not-recomputed`, F2→`revision-not-bound`, F3→`pins-not-bound` |

Selftest receipts are copied into `SEAT/` and named explicitly below under "Files written".

## Predicate audit (no extra clause, no missing clause)

- **v5.** `main()` keeps `v3.score(args)` as the sole verdict source; then
  `write_receipt` + `verify_receipt` and the fail-closed `if code == 0 and not selfverify["ok"]: code = 1`. All four R95-C1 bindings (label-not-frozen, label-not-recomputed,
  revision-not-bound via `resolve_rev` 40-hex, and the pins recorded into the receipt
  before `write_receipt`) are each present with no extra acceptance gate and no shortcut.
  The `bytes` default hook (`_default`) handles `bytes`/`bytearray` with `{bytes, sha256}`
  and raises `TypeError` otherwise — matches the selftest's
  `unknown-type-raises-clean`. `write_receipt` uses `tempfile.mkstemp`,
  same-directory, `os.fsync` before `os.replace`, and removes the temp on any
  `BaseException` before re-raise — no partial-write path back to the target.
- **c1-agreement-v2 `row()`.** Every round-94 atom (`not-valid`, `stdout-disagree`,
  `rc-disagree` merged into the `stdout-disagree` reason per the docstring, and
  `predicted-mismatch`) is preserved with unchanged semantics, plus the four new typed
  bindings. Forged fixture `forge-pos` still fails the intended binding only
  (`label-not-frozen`), F1/F2/F3 each fail exactly their intended binding
  (`label-not-recomputed` / `revision-not-bound` / `pins-not-bound`), and the honest
  triple (`honest-pos`) passes with `reasons=[]` (battery leg echo above).
- **c1-forgery-refusal.** The `before` leg runs the pinned r94 counter — it admits the
  forged fixtures wholesale (`counts_of_4` valid 4, agree 4, predicted 4). `after` legs
  re-derive each binding and refuse each forgery with exactly its intended reason.
  `honest` leg accepting the valid triple is the blanket-refusal counter.
- **symlink-probe.** Victim planted with a nonce; `<target>.tmp` symlink pre-planted with
  `os.symlink`; run via public CLI as a subprocess; verdict `victim_intact AND
  receipt_valid` with no extra clause that could reclassify a victim overwrite as a pass.

No missing or extra predicate was found in any of the four tools. The frozen target —
forgery battery exit 0, 4 of 4 exact reasons, victim intact, honest selfverify green —
reproduces at the declared commit in this seat's live runs.

## Adversarial patch demos (scratch-only)

- **`expect=""` waiver.** Patching v2 with `expect and False and label != expect`
  (`attack3.py`, deleted after use) makes `forge-pos` pass with `reasons=[]`
  (`attacker PASSES ... [('pos', [])]`); the real v2 refuses with `label-not-frozen`.
  Letting the caller set the frozen label string (`--expect`) — including an empty
  string — is the residual surface. LOW/NONE for this review because the caller passes
  a frozen literal, all four committed forgeries stay refused, and `met_target` stays
  bound to the counts recomputation, but it is why the executor was wrong to claim
  "no reason set passes".  `PREDICTED` for `pos` fires on the binding of
  `met_target`/`exit` to the receipt's own fields, not to whether the *frozen label*
  matched.
- **missing `counts` keys crash.** `recompute_label` does `counts["scored"]` etc. on the
  dict it gets back from the receipt JSON; the `LABEL_RE` gate only fires when
  `isinstance(counts, dict) and isinstance(label, str)`, but a *well-formed-typed* counts
  dict missing one key (`{"repaired": 10}`) reaches the direct index and raises
  `KeyError: 'scored'` on its own (uncaught): `malformed-counts rc=1` with a python
  traceback exiting 1, i.e. it is refused, but *untyped* — it shows up as
  `instrument-error` rather than `label-not-recomputed`. LOW. Same direct indexing
  pattern exists in v5's `verify_receipt` — a receipt with a `dict` counts but a missing
  key crashes `verify_receipt`, so the `ok`/`reasons` shape is never produced. This is
  defensive, not a correctness hole, because both are still refuse-side (never
  accept-side).
- **v5 fail-closed enforcement is present.** Deleting the `if code == 0 and not selfverify["ok"]: code = 1` clause (`v5-attack.py`, deleted after use) and running honest with
  `--expect 'WRONG-LABEL-POC'` gives exit 1 with `selfverify ok=True` above it in the
  same run: rc stays 1 only because the *verdict code's* own `met_target=False` forces
  rc 1. The `selfverify ok=True` here is NOT the thin waiver I initially labeled it —
  `verify_receipt` correctly drops `label-not-frozen` when `met_target is False`
  (refusal labels are legitimately free-form per the plan's named limits; the honest
  world has `met False` under a wrong `--expect`). The real attack surface stays on v2's
  caller-supplied `--expect` (see above); v5's writer is only ever fed the
  `--expect` handed to the CLI, and a wrong `--expect` there still exits nonzero even
  with this clause deleted.

## Findings table

| # | file:line | finding | severity | changes frozen receipt? |
|---|---|---|---|---|
| 1 | `tools/round-95/c1-agreement-v2.py:139-141` | `recompute_label` indexes `counts["scored"]`/`counts["intact"]`/etc. directly; a counts dict that is a `dict` but missing any of the 9 keys reaches the index and raises `KeyError` (uncaught, untyped refusal). Crashes instead of emitting `label-not-recomputed`. Observed: scratch fixture `{"repaired": 10}` → `KeyError: 'scored'`, rc 1 with traceback. | LOW | No — the forged fixtures all carry all 9 keys, so the frozen battery's behavior is unchanged. |
| 2 | `tools/round-95/stop-boundary-repair-battery-v5.py:162-176` | Same direct-index pattern inside `verify_receipt`: a receipt with a dict `counts` missing a key crashes `verify_receipt` (uncaught), which is a refuse-side crash loop (clean `reasons` list never emitted), not a pass. | LOW | No — the honest receipt carries all 9 keys, `selfverify ok=True reasons=0` still reproduces. |
| 3 | `tools/round-95/c1-agreement-v2.py:143-144` | The `label-not-frozen` binding holds only when `expect` is truthy and pairwise against the `label` the *caller* passed in; a caller-supplied empty `--expect ''` (or any caller-replaceable expect string) makes `forge-pos` pass cleanly. Runtime callers in this round pass a frozen literal; recorded as an adversarial-handle, not a frozen-frame hole. | LOW | No — the frozen battery command passes the frozen label; 4/4 refusals reproduce. |
| 4 | `tools/round-95/stop-boundary-repair-battery-v5.py:254-256` | The fail-closed clause is correct as written (see patch-demo note above: removing it does not change live rc for the wrong-`--expect` shape, because the verdict code sets rc from `met_target` independently). Recorded only as evidence the clause is load-bearing *in combination with* `met_target`; no defect found. | NONE | No |
| 5 | `tools/round-95/c1-agreement-v2.py:170-171` | `LABEL_RE` allows a label with extra leading/trailing whitespace `recompute_label` regenerates without, and `rec.get("label") != expect` compares the exact frozen string only when `met=true`. This is applied with `m.group(0)` (the full match), so a padded label fails `label-not-recomputed` at the wrong position; no pass-side leak found. | NONE | No |
| 6 | `tools/round-95/symlink-probe.py:60-64` | The probe deletes a pre-existing `<target>.tmp` before planting (line 61: `os.remove(target + ".tmp")`) — a scratch-only path (`--work`); safe on the public path because the probe's targets always live under `--work`, never the lane. | NONE | No |
| 7 | `tools/round-95/c1-forgery-refusal.py:225-229` | The `before` leg passes `--dir`/`--prefix` straight through unchecked; the `before_ok` calculation trusts `rc_before == 0 and before.get("met") is True` — the counter's own `met` field. Because the r94 counter itself computes `met` from the counts it just printed (and prints to stdout), a hostile swap of the *counter file* contents is out of scope here (the counter path is pinned separately). | NONE | No |
| 8 | `tools/round-95/c1-agreement-v2.py:76-78` | `_git_show` is used for the pin re-derivation; `git show REV:tool` of a *missing* file yields None → `exp_counter=None` → `pins-not-bound` fires. Good fail-closed direction. | NONE | No |

## Finding-class summary

- No HIGH or MED finding. All four tools reproduce the frozen C1 behaviors live: the
  honest triple accepted green, the four committed forgeries refused with exactly their
  intended typed reasons, the victim intact under the hardened v5 writer and the victim
  shot through under the pinned v4 writer.
- Three LOW findings are refuse-side cosmetics (typed-vs-crash refusals and the
  caller-supplied-`--expect` waiver handle); none changes a frozen receipt and none makes
  any committed forgery pass. The executor's falsified text "no reason set passes" is
  *falsified only for caller-supplied `--expect=''`* — under the frozen battery command's
  frozen label the statement is true.
- All four selftests exit 0 in the frozen clone.

## Files written (seat dir: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ReviewerV5/`)

- `review.md` + `SEAT/review.md` (this file; thin launcher at the Report path)
- `SEAT/honest-pos.json`, `SEAT/honest-pos.stdout`, `SEAT/honest-pos.rc` — live honest v5 run receipts (`--json-out`, stdout, rc)
- `SEAT/probe-v5.json` — v5 probe receipt (`victim_intact true`, `receipt_valid true`, verdict `hardened`)
- `SEAT/probe-v4-stdout.json` — v4 probe control stdout (verdict `followed-symlink`, rc 1)
- `SEAT/c1-forgery-at-decl.json` — live frozen forgery battery receipt
- `SEAT/st5.txt`, `SEAT/st2.txt`, `SEAT/st-battery.txt` — selftest transcripts
- `SEAT/mal.out`, `SEAT/mal.err` — malformed-counts probe output
- `SEAT/expect-waiver.json`, `SEAT/expect-waiver.stdout` — wrong-`--expect` v5 run receipts
- `SEAT/v5-attack.json`, `SEAT/v5-attack.stdout` — patched fail-closed demo run receipts

Scratch dir `/fast/scratch/hyaku/kaidoku-r95/ReviewerV5` deleted before yield.
