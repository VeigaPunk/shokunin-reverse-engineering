# proposed patch text — section-key needles in anchor form (CR-5, NOT applied)

Artifact: `.ufo/gates/citation-drift/pointer-table.json`. Status: **proposal only** —
the real file is EX-41's write target; this seat writes nothing there.

## What and why (measured)

The two added needles `sc-arc3r1-section-key` / `sc-arc3r2-section-key` pin the
arc3 SCORECARD section headers with `kind: "exact"` **and a line number** into
`SCORECARD.md`, a file the lane appends to (and rewrote once already this line —
the r10 records merged an 8-line insertion that moved every `LOG.md` pin).
`SCORECARD.md`'s own head section is a rewrite site; one inserted line at `:13`
fires 13 findings, two of which are these entries (`receipts/section-key-anchor-variant.txt`).

The citation they grade is a *section-key* reference (SKILL.md rule #14 cites
"`SCORECARD.md`'s `arc3-loop1-round1` section, the 'fresh identity recorded'
line"), i.e. a content-anchor citation by nature. The table's own precedent for
exactly this case is `skill-registry-row` ("its LINE is deliberately not pinned
… Anchor semantics: content anywhere"). The variant below keeps the same
must_match and moves the form; measured on the head-rewrite simulation:
**landed form 13 findings → anchor variant 11 findings** (both non-vacuous: the
anchor fires when the header sentence is removed).

## Replacement objects (both entries, drop-in)

```json
{
  "id": "sc-arc3r1-section-key",
  "kind": "anchor",
  "file": "SCORECARD.md",
  "must_match": "^## arc3-loop1-round1 — coverage \\+ operability \\+ freshness",
  "note": "the arc3-r1 round section's key, the form SKILL.md rule #14 cites it by; content-anchor semantics so append-managed SCORECARD growth cannot move the needle (the skill-registry-row precedent)."
},
{
  "id": "sc-arc3r2-section-key",
  "kind": "anchor",
  "file": "SCORECARD.md",
  "must_match": "^## arc3-loop1-round2 — depth \\+ freshness \\+ operability",
  "note": "the arc3-r2 round section's key; content-anchor semantics (see the r1 entry's note)."
}
```

## Landing note

Any edit to the table must re-pin `pointer_table.sha256` in `expected.json` in the
same commit (the r1 F3 coupling), then re-run default + `--strict` + `--selftest`.
Re-pinning changes the table digest: `738b3a56…` (pre-round) → `bfc42f1b…`
(EX-41's landing) → the variant's own digest if this patch is taken.

## Verdict if NOT taken

No claim clause is violated: the claim's acceptance test is findings=0 at the
work commit, and the landed form is consistent with the pre-existing
`sc59/sc68/sc270/sc622` style of line-pinned SCORECARD needles. This is a
robustness refinement, not a defect. If the parent prefers to keep EX-41's
landing frozen, record this as declined-by-choice in the round report.