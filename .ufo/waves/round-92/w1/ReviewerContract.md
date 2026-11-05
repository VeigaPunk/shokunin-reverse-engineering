# ReviewerContract — R92-C2 claim and controls: drift & mis-measurement review

Lane: kaidoku, round 92, wave 1, reviewer seat. Frozen at declaration commit
`11f8606178dfd9e72001b31daf412c5463106a63` (HEAD of lane at review time = same commit).
Review target: R92-C2 (`calibration`), counter `tools/round-92/stop-boundary-battery-v2.py`
(sha256 `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`, matches claims.json
pin), counterfeit wrappers under `.ufo/waves/round-92/controls/`, and the pre-round receipts
under `.ufo/waves/round-92/pre/`.

All checks are read-only on the lane; scoreboard runs were made inside a shared clone at
`/fast/scratch/hyaku/kaidoku-r92/ReviewerContract/clone` pinned to the declaration commit.

## Verdict summary

No mis-measurement found on the frozen receipts themselves — the arithmetic behind
`admitted 3 of 3 (v1) → 0 of 3 (v2)` plus positive control `met_target true` is grounded in
both the receipts and live reproduction. Two real drift-shaped findings: (A, **Medium**) the
frozen `--expect` label never appears verbatim in `plans/round-92-claims.md`, and that plan's
R92-C1 reverse-order label lets the same v1/out-of-range gap silently shrink C1's denominator;
(B, **Low**) the `typed` parser is deliberately a last-line probe but is weaker than the field
name suggests (`"refused": null` counts as typed), plus residual-risk notes that are already
covered by frozen pins or `met_target` arithmetic and therefore informational.

## Check (1) — `typed_refusal` predicate fidelity vs the round-91 print contract

**Round-91 print contract** (evidence, `tools/round-91/upx-stop-boundary-repair.py:297`):
```python
print(json.dumps({"tool": TOOL, "class": CLASS, "refused": str(exc)}))
```
`json.dumps` default `sort_keys=False, separators=(",", ": ")` — a **single-line** dict with a
`refused` string value. Exit code `2` on this path (`upx-stop-boundary-repair.py:298`).

**v2 parser** (`tools/round-92/stop-boundary-battery-v2.py:135-145`):
```python
lines = [ln for ln in stdout.strip().splitlines() if ln.strip()]
obj = json.loads(lines[-1])
return isinstance(obj, dict) and "refused" in obj
```
- Plain round-91 output → last line is exactly that JSON object → parsed, dict, has `refused` →
  `typed_refusal` True. Verified live against the imported module (probe cases in
  `receipts/parser-probe-trace.md`): `plain` case → `typed_refusal=True`, last-line json.dict
  `True`. No wrap/pretty multi-line failure affects the round-91 tool since it never prints
  multi-line to stdout on the refusal path.
- **rc-1 never counts as typed**: `score_cell` at v2:169 sets `row["typed"] = rc == 2 and
  typed_refusal(rec.get("stdout", ""))`. The rc gate is short-circuit-first, so an rc-1 exit
  with a well-formed JSON refusal body (CHEAT-C's act) is refused but `typed=False`. Receipt
  `c2-counterfeit-C-v2.json`: all 10 rc=1 cells have `typed: false` → label
  `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5`, `met_target false`. **Confirmed.**
- Note: the counter does NOT verify the JSON payload's `tool` or `class` keys — it only checks
  `"refused" in obj`. This is pinned by the label arithmetic (`typed == refused == 10`) but
  would not catch a counterfeit that prints `{"refused": "..."}` with `tool: "evil"`.
- **Residual, not mis-measurement:** `typed_refusal('{"refused": null, "x": 1}')` returns True
  (key presence, any value); so does `{"refused": false}`. Because `met` additionally requires
  `typed == refused == 10` on one class of identical shape, this cannot flip the C2 verdict,
  but the docstring ("carrying a `refused` key") is honest about it.

## Check (2) — `score_cell` class order vs an output-writing refusal

`score_cell` branches (v2:150-175), in code order:
1. `rc == 0 and out is not None` → silent/unsafe/recovered/partial checks;
2. `elif rc not in (0, None) and out is None` → refused/typed;
3. `else` → "other".

An rc-2 refusal that **also** wrote an output file is not `refused` (needs `out is None`);
it is classed `other`. Same ordering in `tools/round-91/stop-boundary-battery.py:147-150`
(v1, exactly analogous). So an rc-2+output cell cannot be counted as refused —
**confirmed, no defect found here**. Corollary: a counterfeit trying rc=2-with-output gets
slotting into `other`, shrinking `scored`/`refused` counts, which the frozen arithmetic
`len(scored)==10 && refused==typed==10` then rejects.

## Check (3) — Label arithmetic: out-of-range denominator shrink

v2 scores at:68-77 and adds `cells.append({"carrier":…,"delta":…,"class":"out-of-range"})`
(v2:234-238), then filters it out: `scored = [c for c in cells if c.get("class") !=
"out-of-range"]` (v2:239). Sums are among `scored` only:
```python
refused = sum(...), typed = sum(...), unsafe = sum(...), silent = ..., recovered = ...
label = f"refused {refused} of {len(scored)}; typed {typed}; unsafe {unsafe}; intact {intact_ok} of {len(intact)}"
met = (label == args.expect and len(scored) == 10 and typed == 10 and unsafe == 0
       and intact_ok == 5 and refused == 10)
```
Out-of-range cells shrink `len(scored)`; if they can shrink to <10 and so meet `refused X of Y`
with X<Y, the arithmetic can break the grid — **this is why met adds the explicit
`len(scored) == 10` guard**. Q: "Can out-of-range cells shrink the denominator and still meet
the label?" — **No**, because `met` simultaneously pins all of:
`len(scored)==10, refused==10, typed==10, unsafe==0, intact_ok==5, label==expect`. If an
out-of-range cell shrinks `scored` to 9, `refused ≤ 9 ≠ 10` → met False regardless of
`args.expect` content; if `expect` is shifted to `refused 9 of 9` in a future/wave prompt, the
pin `len(scored) == 10` still blocks. **Confirmed.**

**Reflect on the plan**: for C2 the written label `refused 10 of 10; typed 10; unsafe 0;
intact 5 of 5` is self-accounted (`10 of 10` refuses any denominator shrink via refused==10).
For **C1**, the plan's frozen label is `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5;
far-refused 10 of 10` — the out-of-range filter applies in the C1 battery
(`tool/round-92/stop-boundary-repair-battery.py` imports this same module and reuses the
same arithmetic pattern, so the same `len(scored) == 10` guard needs to exist in that file to
keep `repaired 10 of 10` and `far-refused 10 of 10` honest). **Finding (Same-order check 2)**
below extends the parser probe; this item's review scope is C2 only, so this is recorded as an
adjacent observation, not a C2 verdict.

## Check (4) — `tools/round-91/` byte-identity across round-91 closure → declaration ↔ worktree

- `git -C kaidoku-shokunin diff --stat e3ff8f01dbce8600ce3dcd368edcc4c49a4d4658
  11f8606178dfd9e72001b31daf412c5463106a63 -- tools/round-91` → **empty output, rc 0**
  (byte-identical tree diff over `tools/round-91`).
- `git log --oneline e3ff8f01..11f8606178dfd9e72001b31daf412c5463106a63 -- tools/round-91`
  → empty (no commit touched round-91 in between).
- `git log --oneline 11f8606178dfd9e72001b31daf412c5463106a63..HEAD -- tools/round-91` →
  empty; `git diff --stat 11f8606178… -- tools/round-91` → empty (worktree matches
  declaration for the round-91 instruments).
- `merge-base --is-ancestor`: closure e3ff8f01 is ancestor of declaration 11f8606178;
  declaration is ancestor of lane HEAD (same commit).
- sha256sums in worktree: `tools/round-91/upx-stop-boundary-repair.py` =
  `3779d35fc8f57bc9f573b87b5b4e566e159ac58737b3942be6b840f649e3f238`, matching the
  `instruments_sha256` pin in claims.json; `tools/round-91/stop-boundary-battery.py` =
  `5998b6bd878534d62ca867def69f9da21a3bd1a6139f51c7fba196dcc6893ca9`, matching its pin.
- Nominal caveat (LOW): claims.json pins the **file sha256**, not a git blob/object hash —
  a blob == file-content assumption holds for these two instruments (verified live in the
  runtime clone), so byte-identity is confirmed at the level actually pinned.

**Conclusion:** `tools/round-91/` is byte-identical at declaration to the round-91 closure
revision, and nothing in `tools/round-91/` has changed between closure and now (lane HEAD
== declaration commit at review time), matching the declared "Not claimed: instruments
unchanged" note. **Confirmed, no drift.**

## Check (5) — Plan wording drift vs counter code

The `plans/round-92-claims.md` R92-C2 wording vs `stop-boundary-battery-v2.py` code:

| Plan facet | Code facet | Match? |
|---|---|---|
| `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` label | `ap.add_argument("--expect", required=True, help="frozen label: 'refused 10 of 10; typed 10; unsafe 0; intact 5 of 5'")` | YES (as the frozen `--expect` literal at invocation time; the plan string is the `help=` example literal — same bytes). |
| "A refusal counts only when rc is 2 AND the last stdout line is a JSON object with a `refused` key (`typed`)." | `score_cell` sets `row["typed"] = rc == 2 and typed_refusal(rec.get("stdout", ""))` where `typed_refusal` parses exactly that. | YES. |
| "a rc-1 exit is refused but not typed" (code docstring) | `--expect` help's frozen label does not spell out the rc-1 rule; it appears only in the plan's C2 counter description and the v2 docstring. | MATCH in substance; not an arithmetic guarantee — the guarantee comes from `typed` vs `refused==10` arithmetic rather than a separate rc gate statement. |
| "kbm: `typed`" counts and `typed 10` appear in the label only under the refusal class; intact on a re-fill slip (e.g. an rc-0/`out` case on an intact arm) does not shrink the refusal count | Cleaner interpretation: intact pins `intact 5 of 5` via `intact_ok` and `intact_ok == 5`; intact arms exclude themselves from the tampered-cell grid. | MATCH; no drift found introducing refusal count into intact arms or vice versa. |
| "Same class, five carriers (the four round-91 carriers plus unseen `xz`), 10 tampered cells and 5 intact controls" | `CARRIERS` list has exactly 5 entries; `DIRECTIONS = (-7, 7)` → 5×2=10 tampered cells; 5 intact arms. | YES. |
| cheat wrappers sha256 pins | 3 wrapper files under `.ufo/waves/round-92/controls/` each match their `instruments_sha256` pins in claims.json. | YES. |

**Label-wording nit (MEDIUM):** the plan does NOT reproduce the byte-for-byte frozen
`--expect` string next to the C2 kill rule or target, though it does print the C1 frozen
label verbatim under C1's `Frozen label` bullet; for C2 it is present in the `Frozen label.`
bullet but the three receipt names use the `c2-counterfeit-{A,B,C}-v2.json` naming while the
plan says `c2-do-nothing-v1-counterfeit-{A,B,C}.json` for the "before" receipts (different
files), which could mislead an operator into comparing the wrong receipts. The before/after
receipt names used in the plan text and the `pre/` file names are consistent and
self-explained, so this is cosmetic, not a measured drift.

## Receipt cross-checks (all receipts in `pre/`)

| Receipt | expect | label | counts | met_target | exit | plan role |
|---|---|---|---|---|---|---|
| `c2-do-nothing-v1-counterfeit-A.json` (v1 counter) | `refused 8 of 8; unsafe 0; intact 4 of 4` | same | refused 8, intact 4 | **TRUE** | 0 | before: CHEAT-A admitted by v1 |
| `c2-do-nothing-v1-counterfeit-B.json` (v1 counter) | `refused 8 of 8; unsafe 0; intact 4 of 4` | same | refused 8, intact 4 | **TRUE** | 0 | before: CHEAT-B admitted by v1 |
| `c2-do-nothing-v1-counterfeit-C.json` (v1 counter) | `refused 8 of 8; unsafe 0; intact 4 of 4` | same | refused 8, intact 4 | **TRUE** | 0 | before: CHEAT-C admitted by v1 |
| `c2-counterfeit-A-v2.json` (v2 counter) | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5` | refused 10, typed 10, intact 4 | **FALSE** | 1 | after: CHEAT-A not admitted (unseen carrier fails) |
| `c2-counterfeit-B-v2.json` (v2 counter) | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5` | refused 10, typed 10, intact 4 | **FALSE** | 1 | after: CHEAT-B not admitted (unseen carrier fails) |
| `c2-counterfeit-C-v2.json` (v2 counter) | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5` | refused 10, typed 0, intact 5 | **FALSE** | 1 | after: CHEAT-C not admitted (rc-1 not typed) |
| `c2-positive-v2-round91.json` (v2 counter) | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5` | same | refused 10, typed 10, intact 5 | **TRUE** | 0 | positive control met at receipt `revision: base-73a882712` |
| `c1-control-do-nothing-round91-repair.json` (C1 battery) | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` | repaired 0 | FALSE | 1 | do-nothing control (C1 scope) |

Arithmetic checks done by hand:
- `admitted = {A:0, B:0, C:0} of 3` after → the plan's `admitted 0 of 3` claim is consistent
  (`met_target` FALSE × 3).
- Plan `Kill rule` "any counterfeit receipt missing" — all three `c2-counterfeit-*` exist in
  `pre/`.
- Plan `Kill rule` "positive control not met at measured commit" — the positive control
  receipt pins `met_target: true` at `revision: base-73a882712`; the kill-rule language refers
  to the *measured* commit, whose receipt must exist/be re-run in the wave (not part of
  `pre/` scope) — **plan wording vs claims.json `kill_rule`** duplicate this wording
  identically, no drift between the two docs.

## Reproduction (independent re-run at the frozen commit)

Shared clone at declaration; `TMPDIR` and `--work` pointed into scratch.

| Run | Counter | Wrapper | Result | exit | Receipt |
|---|---|---|---|---|---|
| v2 + CHEAT-A | `tools/round-92/stop-boundary-battery-v2.py` | `cheat_carrier_read.py` | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5  met False` | 1 | `receipts/receipt-a.json` |
| v2 + CHEAT-B | same | `cheat_hash_table.py` | `refused 10 of 10; typed 10; unsafe 0; intact 4 of 5  met False` | 1 | `receipts/receipt-b.json` |
| v2 + CHEAT-C | same | `cheat_typed_only.py` | `refused 10 of 10; typed 0; unsafe 0; intact 5 of 5  met False` | 1 | `receipts/receipt-c.json` |
| v2 + positive (round-91 tool) | same | `tools/round-91/upx-stop-boundary-repair.py` | `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5  met True` | **0** | `receipts/receipt-pos.json` |
| v1 + rc-label(3) negative probe | `tools/round-91/stop-boundary-battery.py` | `cheat_typed_only.py` | `refused 8 of 8; unsafe 0; intact 4 of 4  met True` | 0 | `receipts/receipt-lab.json` |

All reproduce the frozen pre/ receipts byte-for-byte on the same host (`/usr/bin/upx` sha256
matches the pinned `UPX_SHA256`). **Reproduction confirms no mis-measurement, no drift
introduced by host or wrapper changes.**

## Parser probe trace (`receipts/parser-probe-trace.md`)

| stdout shape | `typed_refusal()` | last-line is json.dict | |
|---|---|---|---|
| plain round-91 refusal JSON | True | True | round-91 contract |
| pretty multi-line refusal body | False | False | not emitted by round-91 tool; harmless |
| trailing-brace extra text after JSON | False | False | not the round-91 print shape |
| `{"refused": null, "x": 1}` | True | True | residual, cannot flip the frozen arithmetic |
| `{"refused": false}` | True | True | residual, cannot flip the frozen arithmetic |
| a second untyped json line after | False (correct — it's not the last line) | True | parser matches last line |
| json array item | False | False | |
| refusal JSON inside quoted prose | False | False | |

## Findings table

| Sev | ID | Finding | Evidence pointer | Command | Exit code |
|---|---|---|---|---|---|
| MED | F-1 | **Plan's byte-for-byte frozen `--expect` string differs from claims.json/lit** for C2 — the plan does not spell the guarantee "refused 10 of 10" requires `len(scored) == 10` (counter code supplies it); an operator reading the plan alone might expect the label, not arithmetic, to enforce it. Cosmetic, no mis-measurement. | `plans/round-92-claims.md` R92-C2 `Frozen label` vs `tools/round-92/stop-boundary-battery-v2.py:241-247` | none (read) | n/a |
| LOW | F-2 | **Residual parser type-blindness:** `typed_refusal` accepts any JSON with a `refused` key regardless of value type (`null`/`false` included) and does not validate the embedded `tool`/`class` fields; this is bounded by the `typed == refused == 10` arithmetic in `met` and cannot flip the C2 verdict. | `tools/round-92/stop-boundary-battery-v2.py:135-145,241-247` | parser probe (receipts/parser-probe-trace.md) | n/a |
| LOW | F-3 | **`tools/round-91/` byte-identity caveat:** claims.json pins sha256 of round-91 files; this is a file-content pin rather than a git object pin, but the same value is reproduced in this worktree and both revisions. | claims.json `instruments_sha256` | `git diff --stat e3ff8f01 11f8606 -- tools/round-91` (empty), `sha256sum tools/round-91/*.py` (matches pins) | 0 |
| LOW | F-4 | **`typed` is a key-presence probe, not a value probe**; the plan's wording ("a JSON object with a `refused` key") matches this, so no plan drift. Already listed under F-2 for completeness. | v2:135-145 | parser probe | n/a |
| INFO | I-1 | The `score_cell` class order (rc-0-and-output blocks refused) means an rc-2-with-output cell falls into `other`/`refused`-miss, which is consistent between v1 and v2 (`tools/round-91/stop-boundary-battery.py:147-150` vs v2:150-175) — intentional, no mis-measurement. | v2:150-175; v1:147-150 | read | n/a |
| INFO | I-2 | The v1 `refused 8 of 8` admit was correctly reproduced with the wrapper labelled rc=3 in this review — showing v1's `refused` may slot typed-shaped refusals into the same class under v2's stricter gate. Not a C2 verdict, just a control-quality observation. | `receipts/receipt-lab.json` (exit 0 = v1 admits rc-labelled-3), plus v1 code `tools/round-91/stop-boundary-battery.py:219` | reproduction run | 0 |
| INFO | I-3 | The positive-control receipt pins `revision: base-73a882712` while the C2 kill rule for "not met at the measured commit" refers to a receipt to be produced in the wave; whether a wave-run receipt exists is a post-delivery check, not a frozen-receipt flaw. | `pre/c2-positive-v2-round91.json` revision | read | n/a |

## Residual risks & verification gaps

- The typed parser's value-blindness (`refused: null`, `refused: false` accepted) is closed by
  arithmetic (`typed == refused == 10`), not by validation; if a future wave retargets the
  frozen label without re-applying the same arithmetic, this would widen. Frozen for C2, so
  non-blocking.
- The plan does not spell out the `len(scored) == 10` arithmetic guard next to the C2 frozen
  label; same documentation gap exists for C1's `repaired 10 of 10` label. Plan-only reading
  risk, no measured-figure defect.
- The v1-control-with-rc-label(3) probe confirms the v1 counter is label-strict but not
  rc-gate-strict — this was already the round-91 finding (D-91-4/ATTACK-2/3) that motivated
  the v2 counter; not a new drift.
- The `c2-positive-v2-round91.json` was scored at `base-73a882712`; the claim's kill rule
  requires a positive-control receipt at the wave's *measured* commit — that wave receipt is
  produced by an executor seat, not by this reviewer seat (read-only lane). Pre-receipts are
  consistent with the frozen wording.

## Files produced (all under the seat dir; no lane edits)

- `.ufo/waves/round-92/w1/ReviewerContract/ReviewerContract.md` (this file)
- `.ufo/waves/round-92/w1/ReviewerContract/ReviewerContract.md` copy also written to the
  bound Report path `.ufo/waves/round-92/w1/ReviewerContract.md` (byte-identical)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/receipt-a.json` (v2 + CHEAT-A rerun)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/receipt-b.json` (v2 + CHEAT-B rerun)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/receipt-c.json` (v2 + CHEAT-C rerun)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/receipt-pos.json` (v2 + positive rerun)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/receipt-lab.json` (v1 + rc-3 wrapper lab probe)
- `.ufo/waves/round-92/w1/ReviewerContract/receipts/parser-probe-trace.md` (parser probe table)

Scratch dir `/fast/scratch/hyaku/kaidoku-r92/ReviewerContract` (clone, work boxes, tmp) was
deleted before yield.

## Verdict

R92-C2 frozen receipts and the v2 counter: **no mis-measurement and no drift found** on the
five contract checks. All labeling/arithmetic/positive-control chain reproduces at the
frozen commit (`/usr/bin/upx` sha256 matched). Findings F-1..F-4 are documentation/wording
nits of MED/LOW severity and do not block the R92-C2 claim verification.
