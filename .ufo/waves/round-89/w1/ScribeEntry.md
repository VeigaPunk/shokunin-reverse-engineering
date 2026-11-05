# ScribeEntry — round-89 knowledge entry draft (kaidoku, R89-C1 / R89-C2)

Full report: `.ufo/waves/round-89/w1/ScribeEntry/report.md`. Drafts:
`.ufo/waves/round-89/w1/ScribeEntry/knowledge/2026-11-04-r89-binfo-field-value-class.md` (101 lines)
and `.ufo/waves/round-89/w1/ScribeEntry/README-rows.md`. Receipts: `…/ScribeEntry/receipts/`.

1. **Entry draft (101 lines, limit 120)** covering the class definition (an in-range but wrong block-0
   `b_info.sz_cpr`), why the packer's arithmetic gate stays silent and the refusal surfaces at the
   payload stage (`Exception: compressed data violation`), the stored-value-blind derivation and its
   accounting bound (`(fits_u_len, total, -derived)` over the PackHeader's `u_len`), the
   `intact`/`chain-geometry`/`field-value` classes, the refusal set, the named limits, and a `source:`
   line naming S311 and S312 (the rows opened this round) plus S306, S309, S310 and the three
   base-present knowledge entries.

2. **Every number is receipt-backed.** `recovered 4 of 4` / exit 0 / four controls true and the
   round-88 regression arm: `pre/c1-candidate-at-declaration.json`; the before-arm `0 of 4` and the
   `compressed data violation` text on all four carriers: `pre/c1-base-r88-repair.json`; `identity`
   and `naive-global`: `pre/c1-control-identity.json`, `…/c1-control-naive.json`; the 8-of-8 and
   4-of-4 class regressions: `l1/scores/c1-r87class-regression.json`, `…/c1-r88class-regression.json`;
   the nine field classes / 18 cells: `l1/scores/block29-cells.json`; docker-init's 136/226/440
   accounting: `.ufo/waves/round-88/w1/ExecGeomCross/evidence/docker-init.derive.json`. The
   round-89 repair's own cost curve is marked **unmeasured** — no committed receipt states it.

3. **README rows drafted in the tables' declared shape**, with a shape note: the coverage-map table
   has 3 columns but the landed round-89 row has 4; the Knowledge table has 4 columns but the
   round-88 row has 2 and the landed round-89 row has 3. The drafts use the declared shape, not the
   round-88 row's literal shape.

4. **The repair was revised in-round while this seat worked** (declared `332917f2…` -> landed
   `664b973a…`, L1 commit `7edab6ae5`). The entry states the refusal set for both revisions, with a
   receipt for each; the declared bytes' third refusal was an untyped rc-1 traceback that the landed
   revision converts to rc 2. The class, rule, survivor key, classes and limits are identical in both.

5. **The refusal message is carrier-dependent** (libz answers `corrupt b_info` where jq/xxd answer
   `header corrupted` for the same class) — recorded as an `[observation]`; the class, not the
   message, is the stable key.
