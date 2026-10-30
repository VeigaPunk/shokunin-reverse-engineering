# MutGapRule — R51-C1 gap-rule mutation battery (round 51, wave 1)

**Verdict: the battery table is computed and GREEN (17/17 expectations on the amended
mutation set, 32/32 cross-check agreements; 16/16 and 36/36 on the pre-amendment set), and
the amended law behaves exactly as the claims require. But the pre-freeze controls path does
not yet evaluate the clause the amended mutation set depends on: `law_shape_ok` is computed
only inside `measure()`, never inside `controls_mode()`, so the F4-M1 all-thirteen-whitelist
mutant — which the claims require to be **RED** — scores `dispositions_matched 4`, exit 0
(GREEN) in the controls path. The kill rule cannot fire as written.**

> **Timing note.** `tools/round-51/c1-counter.py` changed bytes **three** times while this
> seat was working (sha256 `be376891…` at 02:17, `3648f63c…` at 02:19, `ecc0dc18…` at 02:21).
> An earlier version called `controls_mode(...)` without defining it (a `NameError` crash);
> the L1 has since implemented it. **The findings below are against the final bytes,
> sha256 `ecc0dc187fcd4d1422aa188ce00f00dbf28d172711300d79b63795f30aa2d629`** (recorded in
> `receipts.json` and `controls-mode-evidence.json`). Every claim below was re-verified
> against those final bytes.

> **Misroot (contained, recorded by the L1).** An intermediate version of
> `amended-law-battery.py` was written to the **fleet** repo root instead of the lane
> (`kaidoku-r51/w1/MutGapRule/amended-law-battery.py`, sha256 `0bde7b78…ec602`) because the
> write path was relative to the fleet root rather than the lane. The L1 contained it per
> protocol: the fleet copy was deleted and the bytes preserved at
> `.ufo/waves/round-51/w1/misroot/kaidoku-r51/w1/MutGapRule/amended-law-battery.py`. The
> **authoritative script is the seat copy**,
> `.ufo/waves/round-51/w1/MutGapRule/amended-law-battery.py`
> (sha256 `a8a28df65c5503a4a1afe1977ab7fe5934c76f271e66383ca072dca3cda23dc9`), which is the
> corrected final version (the preserved misroot copy is an intermediate revision without the
> `argparse`/`ast` imports). The battery was **re-run from the lane path** after
> containment and reproduces the same result (exit 0, 17/17 expectations, 32/32
> agreements); `receipts.json` records that run. The fleet repo is clean
> (`git status --porcelain` empty).

Artifacts (this seat's directory, `.ufo/waves/round-51/w1/MutGapRule/`):

| file | what |
|---|---|
| `amended-law-battery.py` | the battery for the **amended** mutation set (F3/F4/F10) + `law_shape_ok` + the counter audits |
| `amended-expected-verdicts.md` | **the expected-verdict table** for the amended set (which carriers pass/fail, which clause fires, which oracle entries are unaccounted) |
| `amended-battery.json` | machine-readable results of the above |
| `controls-mode-evidence.json` | **end-to-end measurement of the real `--controls` mode** against a scratch fixture clone, with the expected-vs-observed table |
| `gap-rule-mutation-battery.py`, `expected-verdicts.md`, `battery.json` | the pre-amendment battery (M0–M6s), kept for the record |
| `law-enforcement-probe.py`, `probe.json` | the law-enforcement and claim-string probes |
| `receipts.json` | exact commands, exit codes, stdout/stderr sha256, UTC times |

No REA run, no network, no lane write. All inputs read at base
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

---

## 0. Note on the round's shape

The L1 amended `plans/round-51-claims.md` **during** this wave (amendment record F1–F11).
F3 changed the rule shape, F4 renumbered the frozen mutation set and added the
`law_shape_ok` binding, F10 changed the claim grammar. My first battery was computed
against the **pre-amendment** set; this report's primary table is the **amended** one, and
the pre-amendment table is kept alongside it. Two of my three earlier findings (the claim
string, the missing `--controls` flags) have been **fixed by the L1** in the meantime — the
remaining `controls_mode` defect is the same finding, one layer deeper.

---

## 1. The amended mutation battery — expected verdicts

Data: the four committed REA 6.5.0 envelopes `corpus/evidence/round-50/c1/<id>/after.json`
and the four frozen census tables `tools/round-50/oracle/<id>.nonregular.tsv`.

**Method.** Two *independent* evaluations per cell: (a) this seat's own three-family
disposition evaluator, a re-implementation of the clause semantics documented at
`tools/round-50/c1-counter.py:1458-1569`; and (b) the lane's amended v2 counter
`tools/round-51/c1-counter.py` (sha256 `ecc0dc187fcd4d1422aa188ce00f00dbf28d172711300d79b63795f30aa2d629`),
imported read-only. **Agreements 32, disagreements 0.**

| Rule (F4 frozen set) | c6430 | c6490 | g7581 | g7582 | disposition verdict | `law_shape_ok` |
|---|---|---|---|---|---|---|
| **F4-M1** all-thirteen whitelist (`required.char-device=true`, silent names all thirteen) | green | green | green | green | 4/4 green | **FALSE** |
| **F4-M1 + 14th device** | **red** | **red** | **red** | **red** | 0/4 green | **FALSE** |
| **F4-M3** regression: `required.char-device=true`, only `247:0` silent | green | green | **red** | **red** | 2/4 green | **FALSE** |
| **F4-M4** regression: strict subset (`247:0` + `136:0-136:7`) | green | green | **red** | **red** | 2/4 green | **FALSE** |
| **F4-LAW** the amended law (F3 shape) | green | green | green | green | 4/4 green | **TRUE** |
| **F4-LAW + 14th device** | green | green | green | green | 4/4 green | **TRUE** |
| **F4-WHITELIST-ONLY** all-thirteen whitelist *without* `required.char-device=true` | green | green | green | green | 4/4 green | **FALSE** |
| **F4-WHITELIST-ONLY + 14th device** | green | green | green | green | 4/4 green | **FALSE** |

Unaccounted oracle entries:

- **F4-M3** → the **twelve** non-`247:0` char-devices on both FRITZ!Box carriers
  (`dev/pts/0-7`, `dev/tiatm`, `dev/ttyp0-2`) — exactly the claims' "twelve other
  char-devices", measured. Nothing on the Cable class.
- **F4-M4** → **four** rows (`dev/tiatm`, `dev/ttyp0-2`) — the M50 partial-widening trap.
- **F4-M1 + 14th** → the one fourteenth device (`dev/ttyS0 4:64`).
- **F4-LAW**, **F4-LAW + 14th** → none.

### What this establishes for the claims

- **F4-M1 must be red, and it is — but only via `law_shape_ok`.** The amended M1 is
  disposition-**green** on all four carriers, because over these four carriers the law and
  the all-thirteen whitelist are extensionally identical (the law says "no disposition", the
  whitelist says "these thirteen dispositions"). That is exactly why F4 added the
  `law_shape_ok` binding, and my measurement confirms the binding is what separates them:
  `law_shape_ok` is **FALSE** for M1 (reasons: `removed.silent['char-device']` names 13
  device details; `required[char-device]` is `True`, not `false`) and **TRUE** for the law.
  **The `law_shape_ok` clause is load-bearing: without it M1 is green and the kill rule
  cannot fire.**
- **The law is green on all four carriers and fires no clause**, and it stays green when a
  fourteenth, unlisted device is added to the census (F4-LAW + 14th: 4/4 green, no
  unaccounted rows). The whitelist is red on the same fixture (F4-M1 + 14th: 0/4, the
  fourteenth device unaccounted). **The amended set's M2 expectation holds** — but note the
  mechanism precisely: the fourteenth-device fixture is red under a whitelist only when the
  whitelist also sets `required.char-device=true` (F4-M1). A whitelist that leaves
  `required.char-device=false` (F4-WHITELIST-ONLY) stays **green** even with the fourteenth
  device, because the disposition clause skips the kind entirely. Such a shape is still
  caught by `law_shape_ok` (FALSE), so the round is covered — but the *fourteenth-device
  fixture alone* does not kill it. **The L1 should make sure the control battery includes
  the `law_shape_ok` verdict for the whitelist-only shape, not only the disposition verdict.**
- **F4-M3 reproduces the round-50 miss exactly** (2/4: Cable green, FRITZ!Box red, twelve
  unaccounted rows) — the battery is anchored to the committed miss receipt
  (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`, `carriers_matched 2`).
- **F4-M4 stays red** (the partial-widening trap).

The full machine-readable table, with the `law_shape_ok` reason lists and all 17
expectations, is in `MutGapRule/amended-expected-verdicts.md` and
`MutGapRule/amended-battery.json`.

---

## 2. CRITICAL finding — the controls path never evaluates `law_shape_ok`, so F4-M1 is GREEN

The L1 has implemented the F2 offline mode (`--controls`, `--gap-rule`, `--receipts` are all
argparse options; `controls_mode` is now defined) and has assigned `b['law_shape_ok']` in
`measure()` (`tools/round-51/c1-counter.py:2666`). My earlier findings (b) and (c) are
**fixed**. But the amended mutation set depends on `law_shape_ok`, and:

```
$ grep -n "law_shape_ok" tools/round-51/c1-counter.py
19:  - F3+F4: `law_shape_ok` — a frozen binding: ...      (docstring)
478:            'gap_rule_ok', 'frozen_tables_valid', 'law_shape_ok')   (BINDINGS)
2666:    b['law_shape_ok'] = not shape_notes             (measure() only)
```

**`controls_mode` contains zero occurrences of `law_shape_ok`** (measured: 0 in its body,
lines 2692–2790). It evaluates only `gaps_ok` and `nonregular_unpublished_ok`, and its exit
rule is `return 0 if matched == len(per) else 1` — a purely disposition-based verdict.

Measured end-to-end against the **real** counter (current bytes) in a scratch fixture clone:

| rule scored via `--controls` | dispositions_matched | exit | the claims require |
|---|---|---|---|
| `old` (the round-50 rule) | 2 | 1 | CTL-OLD 2, exit 1 — **matches** |
| the amended law | 4 | 0 | CTL-NEW 4, exit 0 — **matches** |
| `junk` (impossible allowance) | 0 | 1 | CTL-JUNK 0, exit 1 — **matches** |
| **F4-M1 (all-thirteen whitelist)** | **4** | **0** | **RED — DOES NOT MATCH** |
| F4-M3 (247:0-only whitelist) | 2 | 1 | red — matches (2/4) |
| F4-M4 (strict subset) | 2 | 1 | red — matches (2/4) |

**The F4-M1 mutant is GREEN in the controls path.** The claims state M1 "must be **RED** —
red by the frozen rule-shape clause `law_shape_ok`", but that clause is not evaluated
anywhere in the controls path, so the mutant passes and the kill rule ("any mutant green
that should be red → stop before the data run") **cannot fire**. My independent measurement
confirms M1's `law_shape_ok` is indeed `False` (reasons: `removed.silent['char-device']`
names 13 device details; `required[char-device]` is `True`, not `false`) — the clause is
right, it is simply not wired into `controls_mode`.

**Fix:** `controls_mode` must evaluate `law_shape_ok` on the named rule and make it part of
its verdict (e.g. exit 1 with `law_shape_ok: false` and the shape notes), or the control
driver must evaluate the binding itself from the rule it passes. Either way the control
receipt must carry the binding, so the kill rule is decidable from the receipt.

### Two further measured defects in the controls path

**(i) `--controls` requires `--rev`** — `usage: --controls requires --root --rev`, exit 2.
The wave-1 control driver (`ExecControls/c1-controls.py`) **does not pass `--rev`**, so
every one of its 18 arms exits 2. Its own expectation table then marks CTL-OLD, CTL-NEW and
CTL-JUNK **"misbehaved"** — not because the rules misbehave, but because the invocation
never ran. Measured with `--rev` added, the same counter produces exactly the values the
claims expect (table above).

**(ii) `--gap-rule` must be a lane-relative git path** — it is resolved with `git show` at
`--rev`, so an absolute path yields `controls: rule <abs> absent at <rev>` and exit 2. The
wave-1 driver passes an absolute path.

With both fixed (add `--rev`, use a lane-relative rule path), the driver would score
CTL-OLD 2/4, CTL-NEW 4/4, CTL-JUNK 0/4 — the claims' expected values. **The driver's
expectation table is right; its invocation is not.**

**Also still missing (medium):** F2 promises the counter exposes `--provenance-base` and
`--receipt-fresh-base` "so the control driver pins the round-50 values"; neither flag exists
(`--controls`, `--gap-rule`, `--receipts` do). Without them the driver cannot pin the
round-50 provenance prefix and freshness base.

---

## 3. Findings that the L1 has already addressed (kept for the record)

**(a) The claim string — FIXED.** The v1 counter hardcoded `claim != 'R50-C1'` in both
`gap_rule_model` and `carriers_spec`; a round-51 rule carrying `"claim": "R51-C1"` made
`gap_rule_ok` and `carriers_spec_ok` **false**, so the predicate would have exited 1 with
`carriers_matched == 4` and every other binding true — an honest miss that looks like a
success. The amended counter now accepts `{R50-C1, R51-C1}`
(`tools/round-51/c1-counter.py:839`). Verified.

**(b) The rule must enforce the law, not merely tolerate it — FIXED (F3).** The sibling's
pre-amendment draft kept `"allowed": {"char-device": ["unpublished-entry"]}`, so a receipt
that **does** report a gap for a char-device row scored **green** — the rule tolerated a
device disposition the law says cannot exist. Measured with a synthetic `dev/led` gap
injected into each carrier's gap list and scored with the frozen counter's own
`disposition_check`: that draft → **green on all four**; the F3 shape (device kinds admit
no gap kind) → **red on all four**. The amended rule uses the F3 shape, and
`law_shape_ok` additionally requires the empty `allowed` list. Both my finding and the
L1's F3 now agree; the amended battery confirms the F3 shape is green on all four carriers
and green with a fourteenth device.

**(c) The control driver's rule fixtures — still defective in the draft.** The wave-1
`ExecControls/c1-controls.py` `rule_fixtures()` builds `new` from the **old** rule with
`removed['silent']['char-device'] = list(DETAILS_13)` — a per-detail whitelist of exactly
the kind the claims reject. Worse, with `required['char-device'] = False` the whitelist is
**inert**: the disposition checker skips non-required kinds, so the whitelist never reaches
the clause. Measured with the frozen counter's own `disposition_check` over the four
committed envelopes, the draft's fixtures score:

| fixture | carriers green | the driver expects |
|---|---|---|
| `old` | 2/4 (Cable green, FRITZ!Box red) | 2 — correct |
| `new` | 4/4 | 4 — correct |
| `junk` | 0/4 | 0 — correct |
| `require-char-device` | **4/4** | red — **wrong** |
| `only-247-0` | **4/4** | red — **wrong** |
| `strict-subset-01` … `strict-subset-12` | **4/4 each** | red — **wrong** |

Every mutation arm is green because the mutation never turns `required.char-device` back
on. **The mutation fixtures must set `required.char-device = true`** — that is the only
way the whitelist mutations bite, and it is what the F4 set now does (F4-M1/M3/M4). If the
L1 keeps this driver, its fixtures must be rebuilt against the F4 set; my §1 table gives the
expected values for each.

**(d) The driver's expectation table is correct — its invocation is not.** Its arms expect
CTL-OLD 2 / CTL-NEW 4 / CTL-JUNK 0 and the mutation arms red; measured against the real
counter with a working invocation, the counter produces exactly those numbers for `old`,
the law and `junk` (§2). The driver fails only because it omits `--rev` and passes an
absolute `--gap-rule` path (§2, defects i and ii).

---

## 4. Corrections to the sibling draft `ExecRuleDerive/census-law.md`

- **"All four receipts record zero diagnostics" is false.** The envelopes carry
  `MaliciousSymlinkRemoved` diagnostics: **c6430 = 1, c6490 = 1, g7581 = 3, g7582 = 3**
  (targets `usr/www/avm/cgi-bin/system_status` on the Cable class, plus `dev/log` and
  `usr/www/avme/cgi-bin/system_status` on the FRITZ!Box class). The committed round-50
  counter receipt agrees (`diagnostics: 1`, `gaps_note: "... 1 removals, 1 silent ..."`).
- Consequently the sibling's `mutations.md` row for `drop-symlink-removal` ("not fully
  decidable from aggregate fields") **is** decidable: dropping the removal clause is **red
  on all four carriers**, unaccounting exactly **1 / 1 / 3 / 3** symlinks (measured in the
  pre-amendment battery, M4).
- `census-law.md` also states "Each receipt has 1 structural `depth-limited` gap and **19**
  path-resolved unpublished-entry gaps". The envelopes carry **567 / 612 / 636 / 636**
  path-resolved gaps (568/613/637/637 total). The 19 is wrong.
- The sibling's `require-char-device` row (red on all four) is **confirmed** when the
  mutation is stated as `required=true` with **no** silent whitelist (the Cable `dev/led`
  is then unaccounted on all four).
- The sibling's `mutations.md` correctly notes that whitelist variants must turn
  `required.char-device` on; that note is exactly right and is the fix for §3(c).

---

## 5. What the L1 should do

1. **Wire `law_shape_ok` into `controls_mode`** (the blocker). Without it the F4-M1 mutant
   is green in the controls path and the kill rule cannot fire (§2). The control receipt
   must carry the binding and its shape notes.
2. **Fix the control driver's invocation**: pass `--rev`, and pass `--gap-rule` as a
   **lane-relative** git path (§2, defects i and ii). As written, all 18 arms exit 2 and the
   driver reports the three correct controls as "misbehaved".
3. **Rebuild the control driver's rule fixtures against the F4 set** (M1/M3/M4), with
   `required.char-device = true` in every whitelist mutation (§3c).
4. Add `--provenance-base` and `--receipt-fresh-base` to the counter (F2's text promises
   them and the driver needs them to pin the round-50 values).
5. Use the §1 table as the frozen expected-value set: CTL-OLD 2/4 exit 1, CTL-NEW 4/4
   exit 0, CTL-JUNK 0/4 exit 1, F4-M1 **red** (via `law_shape_ok`), F4-M3 2/4, F4-M4 2/4,
   and the fourteenth-device fixture green under the law / red under a whitelist.

## 6. Scope and limits

- No REA run and no counter scoring run this wave (forbidden); no network; no lane write.
  The battery is pure table math over the committed envelopes and frozen census tables.
- The verdict is the **disposition clause** plus the **`law_shape_ok` binding**. The
  counter's other clauses (carrier bytes, rerun projection, freshness, docs bindings) are
  the L1's to score.
- `receipt_fresh` note for the L1: the round-50 envelopes were added by commit
  `646d29c9df4ef77499248f95589cb9526c6dea19`, an **ancestor** of any round-51 freeze, so
  `receipt_fresh` is **false** for them at the round-51 freeze (measured). The controls
  therefore need the offline `--controls` path, not `measure()` — which is what F2 says.
- The freshness guard, as amended by F1: `tools/round-50/carriers.json` now joins
  `PRIOR_CARRIER_TABLES` and the four pins are in the round-51 table's `prior_pins`, with a
  frozen `re_scored_pins` allow-list. I measured the **pre-amendment** state (the four
  round-50 pins were in none of the prior-pin sources) and did not re-measure the amended
  counter's `re_scored_pins` path, which the L1 added during wave 1.
- The fourteenth-device fixture is **synthetic**: one extra census row (`dev/ttyS0`,
  `char-device`, `4:64`) appended to a committed carrier's census in memory. It is not
  committed and not in the lane tree.
- No tool was installed or upgraded this wave (nothing needed one).

## 7. Exact commands (all read-only against the lane tree)

```
S=/fast/scratch/hyaku/kaidoku-r51/w1-MutGapRule; mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
python3 <W1>/amended-law-battery.py --out "$S/amended-battery.json"      # exit 0
python3 <W1>/gap-rule-mutation-battery.py --out "$S/battery.json"          # exit 0
python3 <W1>/law-enforcement-probe.py "$S/probe.json"                      # exit 1 (pre-amendment findings)
python3 -I -B <lane>/tools/round-51/c1-counter.py --root <lane> --rev f04b51dd… \
  --controls --gap-rule tools/round-50/gap-rule.json \
  --receipts corpus/evidence/round-50/c1        # --gap-rule MUST be lane-relative;
                                                # run from the lane root.  exit 1, 2 of 4
```

Exact argv, exit codes, stdout/stderr sha256 and UTC times: `MutGapRule/receipts.json`.
