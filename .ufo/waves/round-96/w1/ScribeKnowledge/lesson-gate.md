# Draft — the `## Gate` section for `corpus/lessons/round-96.md`

Seat ScribeKnowledge, round 96 attempt 1, lane kaidoku. This is the seat draft of the
`## Gate` section; the L1 lands it in `corpus/lessons/round-96.md`. The file does not
exist at the declaration commit `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`; the L1
creates it and lands the S321 row in the same commit, so the row's `used-by` path
exists on disk at the landing (fleet census finding `E11`).

---

## Gate

Source opened this round (CORPUS.md rule 1). Access date 2026-11-05 for each.

| row | source | access date | bytes / sha256 / measurement | located quote (≤25 words) | used for |
|---|---|---|---|---|---|
| S321 (new) | `/usr/bin/printf` — host binary, little-endian x86-64 ELF (own-work measurement, no network fetch) | 2026-11-05 (opened this round) | 76 088 B / sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`; packable by upx 5.2.0 (packed sha256 `95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6`, `deterministic true`); receipt `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json` | `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True` | the held-out arm's second fresh source: closes the round-93 carried limit "the fresh-pack arm has one source"; the source-diversity property of the round-93/96 repair chain, measured through the unchanged round-92 helpers |

Measurement evidence for the S321 row (all committed, not re-derived by this seat):

- `sha256sum /usr/bin/printf` → `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`; the
  same digest is the last line of the committed pin file `.ufo/waves/round-96/pins.sha256`.
- `tools/round-96/fresh-source2-check.py` (sha256
  `124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9`) drives the
  unchanged round-92 helpers (`stop-boundary-battery-v2.py`, sha256
  `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`; and
  `stop-boundary-repair-battery.py`, sha256
  `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`); the frozen v3
  verdict code and its `FRESH_SOURCES` pin are untouched.
- The committed receipt `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`
  (measured at the base `0ea695e826f2dca53dd55ac0bafead93de26b173`) reads `exit 0`,
  `met_target true`, `label "fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1"`,
  `counts {far: 2, far_refused: 2, near: 2, repaired: 2}`, `deterministic true`,
  `collides_public_packed false`, `intact_identity true`, `blocks 5`, `packed_sha256
  95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6`.
- The independent re-measurement in this wave is `.ufo/waves/round-96/w1/ExecFreshSource.md`:
  its own clone reproduces the receipt field-for-field (after rewriting `revision`) and
  its own double-pack of `/usr/bin/printf` yields the same `95f2bebe…` digest twice.

Admit / reject. Admitted: **S321 only** — the host binary `/usr/bin/printf` as the
held-out arm's second fresh source, one located measurement line, tier A because the
scope (source diversity of the held-out arm) is exactly what the measurement
establishes and the row's locator is a re-measurable digest rather than a prose claim.
Used by `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` and this lesson.

**Not admitted from the same measurement family: the `/usr/bin/head` supplementary run.**
The executor's seat report `.ufo/waves/round-96/w1/ExecFreshSource.md` step 4 records
that `/usr/bin/head` (sha256
`313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1`) passes the same
`fresh-source2-check.py` with the same label (`fresh-source2 repaired 2 of 2;
far-refused 2 of 2; intact 1 of 1 met True`, exit 0; `packed_sha256
b93ac38db8b61a8739adf596268e44b6b36c8e0ffdaaa7d6df0902beef4e9cc0`, `blocks 5`,
`deterministic true`, `collides_public_packed false`, `intact_identity true`). It is
recorded here as a **supplementary** measurement and is **NOT admitted as a registry
row**, for two reasons that are stated, not assumed:

1. no landed entry cites it. The round's declared sourced step is S321 alone
   (`plans/round-96-claims.md`, "Sourced claim (frontier step)"; `.ufo/waves/round-96/claims.json`
   `sourced_claim.row` = `S321`), and CORPUS.md rule 1 makes a row a claim about a
   source the round actually opened and used. The head run is a supplementary
   diversity probe inside the executor's own seat, not a source any claim rests on.
2. the round-93 carried limit it would serve — "the fresh-pack arm has one source" —
   is already closed by the second source S321. A third source adds no distinct
   property to the closed limit: the property claimed is *source diversity*, which one
   second source establishes.

Flip condition (stated so the refusal is reversible): **admit `/usr/bin/head` as a row
(S322) if a later claim rests on the held-out arm's behaviour being a property of at
least three distinct host binaries rather than two** — for example a claim that the
fresh-pack arm's near/far cell classification is source-independent, or any claim whose
predicate names head specifically. A one-line supplementary measurement alone does not
flip it; a claim that needs it does.

Row changes (CORPUS.md rule 2, old → new, logged here):

- **S321 appended** (`mined`, opened 2026-11-05, recheck `on-release`, kind `tool`,
  tier `A`, used-by `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`). The
  draft row is `.ufo/waves/round-96/w1/ScribeKnowledge/sources-row.md`.
- **No existing row is edited this round.** Rows S001–S320 keep their `status`,
  `recheck` and `used-by` cells unchanged; there is no old→new cell change to log.
- Registry row count: **225 → 226** (`tier.A` 205 → 206, `status.mined` 201 → 202).
- **Landing order requirement.** The census's `E11` finding fires for a `mined` row
  whose `used-by` path is absent from disk. At the declaration neither
  `corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` nor
  `corpus/lessons/round-96.md` exists, so the row, the knowledge entry and this lesson
  file must land **in one commit**. Measured by this seat in its own scratch clone
  (`.ufo/waves/round-96/w1/ScribeKnowledge/verify.md`): with the row present and the
  consumer absent the validator reports `E11 S321 missing used-by
  corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` (exit 1); with the consumer
  present the same registry validates with **exit 0** and no E-code against S321.

Assimilation: `Assimilation: none` (`merge/kaidoku/` is absent; the lane has no
`considerthese/` directory).

---

*Draft provenance: seat ScribeKnowledge, round 96 attempt 1. No lane file outside the
seat directory is edited by this seat; the L1 lands this section, the S321 row and the
knowledge entry together.*
