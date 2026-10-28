# Proposed QUALITY rows (W2C2Quality, not applied; corpus/QUALITY.md is not edited by this seat)

Numbering: the admission table ends at row 88 at `29883d4e`. Rows 89 and 90 are unused in the table.
Narrative rows "75"–"79" in the appended round-34 section collide with table rows 77–79 (see report F7).

## Row 89 — supersedes the header clause of row 88 only

| 89 | **Row 89 (a filed header may name a superseded freeze only with a dated pointer).** The declared-freeze header of a filed lesson may keep naming a superseded commit only when its line carries the pointer `correction YYYY-MM-DD: final declared freeze <40-hex> (<path>:<line>)` and the named later record carries the append-only correction line. A round's four freeze strings (lesson header, that round's SCORECARD `**Declared freeze:**` line, the LOG entry, and each counter's `--freeze` receipt field) are compared for the round the row names; a round with no SCORECARD `**Declared freeze:**` line is a finding. The freeze atom reads the SCORECARD at the measured revision, not at the base. | `corpus/lessons/round-48.md:4` (`0f06251b…` kept; SCORECARD `:3730` `b6f7ca2a…`); `tools/round-49/c2-mismatch.py` A1 reads `LANE_BASE` for the SCORECARD and the round-49 lesson is not read; fixtures X1/X2/X3 in `.ufo/waves/round-49/w2/W2C2Quality/` | 88 (header clause only) |

Note: a repaired round-48 header (fixture X3) is red under the frozen A1 (`A1 stale != lesson header freeze`, `no disagreement to correct`, `round-48 lesson rewritten`), so row 89 cannot be met for round 48 until a successor counter exists. Round 49 records this as a miss.

## Row 90 — a control is red for the binding it names; a property clause meets a literal-satisfying forgery

| 90 | **Row 90 (red means the named binding, and a property clause has a forgery that passes its literal test).** Before the freeze, each control in a claim's control set names the binding, or the listed set of bindings, it must turn false. A control counts as red only when its receipt shows that binding false and names it; exit 1 alone is not a red control. A clause that names a property (provenance, origin, authorship, freshness) faces a pre-freeze control that satisfies the clause's literal test and differs from the genuine run only in the named property. If that control passes, the clause is restated to what the counter measures (row 87) before data. A counter ported from an earlier round re-enters this battery for each inherited clause. Fails when a red control's stated reason is absent from its receipt, or when a property clause has no control that could fail it. | `corpus/lessons/round-49.md` M49-3 (`w1/C1ControlsReview.md` findings 2–3: CTL-C1-5 planted bytes the counter never reads; CTL-C1-4 planted round-42 envelopes); M49-2 (`w1/C1ProvCritic.md` F1–F6, `w1/C1GoldForgery.md`, `w1/C1RunMut.md`: relabelled round-44 receipts score `carriers_matched 4`) | sharpens 71, 78 (narrative 78(b)), 87 |

## Appended correction (non-rewriting) for the numbering collision

Under `## Corrections appended — round 49`: the narrative items headed "Row 75 added after the round", "Row 76 …", "Row 77 …", "Row 78 …" and "Row 79 added after round 48" (QUALITY lines 136–144) are not admission rows. The admission table has no row 75 or 76, and uses 77, 78 and 79 for other criteria. Until a superseding row re-keys them, cite them by title. Row 88's "sharpens … 79" means table row 79 (first freeze bytes).

## Non-QUALITY repairs the L1 may append (LOG/SCORECARD are not frozen)

LOG.md, round-49 entry (row 36 requires it): "Outside closure of round 48, `corpus/lessons/round-48-verifier-spotcheck.md`: calibration harmed (`:107`), quality harmed (`:125`), discernment improved at decision level only (`:126`); disagreements recorded at `:114` (S145 locator) and `:116` (S146 rationale/flip). Verdict record: SCORECARD `## Record corrections — round 49`, A9."

SCORECARD `## Record corrections — round 49`, appended line: "- A9b quality=harmed discernment=improved(decision-level only) source=corpus/lessons/round-48-verifier-spotcheck.md:124-126; supersedes the round-48 entry's `quality improved` and `discernment improved (A1–A8 …)` trend words (SCORECARD `:3740`) for those two axes only."
