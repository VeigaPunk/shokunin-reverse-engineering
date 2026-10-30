# CritCounterV2 — R51-C1 counter v2 design attack (round 51, wave 1)

**Verdict: the v2 counter design cannot, as specified, certify the claim it is
built to certify — and the defect is now in the *amended* claims, not the
original.** **Three** blocking findings (F13, F14, F15) would each make a
correct implementation stop the round as a miss, or let an unverified landing
pass. Four further findings survive the amendment and must be fixed before the
freeze.

All findings are **measured offline** against the committed round-50 receipts and
oracle tables — no REA run, no network, no lane mutation.

**Findings:** `.ufo/waves/round-51/w1/CritCounterV2/findings.md` (15 numbered
findings F1–F15, each with the demanded fix).

**Note on concurrency:** `plans/round-51-claims.md` was amended in the working
tree while this seat was probing (`git diff`: +148/−36; the amendment record
credits **CritRuleDerive F1–F11**, a different attack round). This report was
re-read against the amended text at 02:18 and every finding is re-scoped against
it. My F3 (`run.json` vs `after.json`), F6 (v1 already gates drift at exit 2),
F7 (`carrier_fresh_ok`), F8 (claim label), F11 (law width) were **absorbed** by
that amendment — my measurements are what justified them, and the L1 should read
them as the evidence for the amendments. F1 and F5 are partly absorbed. The
findings marked **OPEN** below are what still needs work.

## The one that matters most

**F13 (OPEN, blocking) — the amended control verdict omits the only clause that
separates the law from a whitelist.** The amendment adds the right rule shape
(`allowed` for device kinds = empty list, `required['char-device'] = false`), a
`law_shape_ok` clause, and a mutation set M1–M4. But the amended controls score
**`(gaps_ok ∧ nonregular_unpublished_ok)`**, while `law_shape_ok` sits in the
**predicate** — and the kill rule ("any mutant green that should be red → stop
before the data run; report as a miss") is applied to the control verdict.
Measured on the four committed envelopes: **M1 (the all-thirteen whitelist) is
GREEN under the control verdict** — the whitelist admits every device row
silently, so nothing is unaccounted — and `law_shape_ok` is the *only* clause
that rejects it. A correct implementation, scored exactly as specified, **stops
the round as a miss**. The same holds for M4: measured, a strict-subset
whitelist is green whenever `required` stays `false` (the whitelist is
unreachable dead code once `required` is false), so M4 must be stated as
`required=true` + partial whitelist, or its redness must be attributed to
`law_shape_ok` alone.

**Smallest safe correction:** the control verdict becomes
`(gaps_ok ∧ nonregular_unpublished_ok ∧ law_shape_ok)`, M4 is restated against
`required=true`, and the amendment's M2 fixture is asserted in the frozen
control fixtures (it is load-bearing — it is the only *data* discriminator
between the law and a whitelist).

## Still open

- **F15 (coverage, new, blocking) — the promotion itself is unverified, and three
  of the claims' landing bindings have no check at all.** The v1 `frontier_note`
  binding is "a note line exists somewhere in `PROVINCE.md`" (measured: the
  counter never reads the `## Frontier` section — `"## Frontier"` occurs **0**
  times in it). Run against two `PROVINCE.md` texts differing **only** in whether
  the Frontier list still carries `- **LE AVM members (`hsqs`)** — still Frontier.`,
  the binding returns **True for both**. So a landing that adds the Core section
  and a frontier note while **leaving LE AVM in the Frontier** passes every
  binding — and the claims assert the opposite ("LE `hsqs` leaves the Frontier
  list"). Also unbacked: "names the fresh receipts" (no receipt-path check),
  "SCORECARD coverage head names 141/141" (`SCORECARD` referenced 0 times),
  "LOG entry" (`LOG.md` referenced 0 times) — while the claims promise each is
  "re-derivable by the counter".
- **F14 (coverage, new, blocking) — the amendment's `--gap-rule` override masks
  the rule's provenance.** In v1 the rule always comes from the frozen path
  (`plan_raw = show(root, freeze, GAPRULE)`), so `gap_rule_unchanged` and the
  `gap_rule_ok` binding both describe **that** file — and the receipt carries no
  rule sha256 at all (only `counter_sha256`). Under `--gap-rule <file>` the
  receipt can therefore report `gap_rule_unchanged: true` and `gap_rule_ok: true`
  while the disposition verdict came from an **unpinned, unrecorded** file. The
  seat brief's "can rule-override masking a stale rule bytes pin go unnoticed?"
  — **yes, it can today.**
- **F4 (coverage)** — the round-51 draft's frozen walk drops
  `tools/round-41/sqfs-list.py` (**the producer of the frozen oracle tables**),
  `fetch-vendor.py`, `xpin-attribute.mjs` (read at the freeze to recompute every
  receipt's evidence id), `prior-pins.json`, `rea-pkg.json`, and the whole
  `tools/round-50/` prefix. The counter would verify a table whose producer is
  mutable and an evidence-id check whose tool is mutable. The v1 counter froze
  all of them; the draft drops them by omission.
- **F9 (calibration)** — `OPENED_DATES = ('2026-10-30',)` **excludes**
  S243/S244/S245/S249 (measured: opened 2026-10-28), and the v1 `sourced`
  binding is existential — so the claims' "cites S243/S244/S245/S249 **and** the
  round-51 SOURCES row(s)" is not checked at all: an entry citing only an
  unrelated 2026-10-30 row passes, and the four required ids can never satisfy
  the binding.
- **F5 (coverage, half)** — the amendment's `--provenance-base` /
  `--receipt-fresh-base` flags fix the round-50-vs-round-51 tree confusion, but
  the `--receipts` **directory** parameter still accepts an absolute path or
  `..`, and reads from the filesystem rather than from the committed tree at REV.
- **F10 (calibration)** — the v1 selftest has **154** cases and **none**
  exercises `char-device` (the fixtures use the fictional `'device'`). Eight
  demanded cases remain uncovered, and the amendment's own M2 does **not** test
  the law's other half ("a gap landing on a device row turns the rule red") —
  that needs a receipt whose gap names a device row, measured red under the law
  rule and green under the permissive cheat. Add it as M5.
- **F12 (calibration, low)** — the before-arm and after-arm differ in more than
  the rule (the committed round-50 receipt's argv carried `--pkg65` and
  `--carrier-cache`; the round-51 predicate carries neither).

**Not run / not claimed:** no REA run, no network fetch, no lane mutation, no
counter selftest executed (the drafts still lack `--controls`/`--receipts`/
`--gap-rule` — the claims' predicate command run verbatim against the draft
exits **2** with a usage error). Scratch removed per contract.

## The three blockers in one line each

- **F13** — the amended control verdict `(gaps_ok ∧ nonregular_unpublished_ok)`
  omits `law_shape_ok`, so the amended **M1** (all-thirteen whitelist) is
  **green** and the kill rule stops a correct round.
- **F14** — `--gap-rule` (mandated by the amendment) lets the receipt report
  `gap_rule_unchanged`/`gap_rule_ok` about the **frozen** rule while the
  verdict came from an **unpinned, unrecorded** file; no rule sha256 in the
  receipt.
- **F15** — `frontier_note` **cannot distinguish "promoted" from "not
  promoted"** (the counter never reads `## Frontier`), so the claim's
  Frontier → Core substance is unverified, and three landing bindings have no
  check at all.
