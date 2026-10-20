# Round 15 — raw/render quote boundary fixtures

author: KaidokuR15.BoundaryFixtures (leaf executor)
date: 2026-10-20
scope: synthetic limitation control for the round-14 quote-fidelity gate; no gate, corpus, QUALITY, or round-14 fixture change
status: fixtures written and digest-pinned; gate **not executed** by this seat

## Claim boundary

This control demonstrates one narrow property of the already-installed gate: its quote test is
a literal raw-UTF-8 substring test, so a sentence copied from *rendered* HTML is rejected even
when it is the correct reading of the raw source. It adds no gate branch, no normalization, no
instrument capability, and no accuracy or semantic-support claim. Both quote inputs are
synthetic; nothing was fetched from an upstream page.

## Files (absolute paths; digests computed with `sha256sum`)

| path | bytes | sha256 |
|---|---:|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-source.md` | 34 | `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json` | 627 | `95c995035ebf539e4e3cce3410a8e52461f5f7c88d5b58563381f0cd19cd4537` |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json` | 620 | `bc97c4699bfcc06d5f6197d63592982f5a9ee245dd787c06ba6ca336746399e3` |

`raw-source.md` is byte-exactly:

```text
## Intro

Use <em>raw</em> bytes.
```

i.e. `## Intro\n\nUse <em>raw</em> bytes.\n` (34 bytes, trailing LF). Static inspection shows the
raw form occurs once at line 3 and the rendered form `Use raw bytes.` occurs nowhere. Both
manifests pin the same source digest above; each carries a top-level `provenance` object stating
`origin: synthetic`, `upstream: false`, and that the source is hand-authored, never fetched.
Those provenance fields are fixture metadata, not gate-enforced evidence.

## Observed gate behavior (source anchors)

All anchors are in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py`.

- `:16-22` — documented manifest shape is `sources` (id → relative path + sha256) and `quotes`;
  every source is hashed before any quote is graded.
- `:34-36` — "An exact contiguous substring of the section body; no whitespace, tag or
  punctuation normalization is applied to the quote or the source."
- `:39-41` — stable classes: `quote_too_long` (>25 words), `quote_not_contiguous` (absent from the
  whole source), `quote_location_mismatch` (section absent or quote outside it).
- `:75` — Markdown headings are matched by `^(#{1,6})[ \t]+(.+?)[ \t]*\Z`; `:239-247` takes the
  body to the next heading of the same or higher level.
- `:173-203` — `parse_manifest` reads only `sources` and `quotes`; unknown top-level keys are
  ignored. This is why the `provenance` object does not invalidate the manifests.
- `:250-258` — `grade_quote` checks the word limit, then whole-source literal membership,
  returning `quote_not_contiguous` before any heading lookup.
- `:259-268` — heading selector is exact tuple membership, then quote-in-section-body.
- `:78` and `:97-100` — `quote_not_contiguous` is not a CNE class, so a manifest containing it
  exits 1 (only `invalid_manifest`, `source_tampered`, `snapshot_tampered` exit 2).
- `:279-297` — source digest verification precedes the quote loop; stdout format is
  `emit_row`/`run_manifest` at `:403-418`.

## Derived expectations (static derivation, NOT executed)

| manifest | quote id | quote | words | whole-source literal | section `## Intro` | expected exit | expected findings |
|---|---|---|---:|---|---|---|---|
| `raw-accepted.json` | `raw-literal` | `Use <em>raw</em> bytes.` | 3 | present (line 3) | one heading, exact; quote in body | 0 | none |
| `rendered-rejected.json` | `rendered-text` | `Use raw bytes.` | 3 | **absent** | not reached | 1 | `quote_not_contiguous@rendered-text` |

Derivation chain for the rendered case: 3 words ≤ 25, so `:252-254` does not fire; literal
membership at `:256` fails because the raw bytes contain `<em>raw</em>` between `Use ` and
` bytes.`, so `:257` emits exactly one finding and returns. Because `quote_not_contiguous` is not
in `CNE_FINDINGS` (`:78`), `exit_code` returns 1 (`:97-100`), not 2. No heading or section check
runs, so the classification is `quote_not_contiguous`, not `quote_location_mismatch`.

Derived stdout (paths are what `os.path.abspath` yields for these absolute invocations):

```text
QUOTE_FIDELITY_MANIFEST: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json
QUOTE_FIDELITY_VERDICT: clean quotes=1 findings=0 exit=0
```

```text
QUOTE_FIDELITY_MANIFEST: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json
QUOTE_FIDELITY: quote_not_contiguous ident=rendered-text no contiguous occurrence in source
QUOTE_FIDELITY_VERDICT: failed quotes=1 findings=1 exit=1
```

These two outcomes are the assigned control: raw 0, rendered 1. They are **derived from the
control flow above and remain unobserved** until L1 runs the gate; this seat did not execute it.

## Proposed L1 checks (not run here)

Run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

1. Inventory: `sha256sum` the three files and compare with the table. Any source-byte change
   invalidates both manifests (`source_tampered`, exit 2), and either manifest-byte change
   invalidates the report pins.
2. Positive control:
   `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest "$PWD/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json"`
   → exit 0, exactly the two stdout lines above, no `QUOTE_FIDELITY: ` finding line.
3. Boundary control:
   `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest "$PWD/.ufo/waves/round-15/boundary-fixtures/rendered-rejected.json"`
   → exit 1, exactly the three stdout lines above (one finding, id `rendered-text`).
4. Scope check: `git status --porcelain` should show only the new round-15 fixture/report paths;
   no round-14 bytes, gate bytes, `corpus/`, or `QUALITY.md` change should appear.

No frozen-expectations file was written: the assignment bounds this seat to one source and two
manifests. If L1 wants a single pinned observation, that is a new integration artifact and an
L1 decision, not something this seat silently adds to the round-14 `--frozen` inventory.

## Limits, risks, and calibration

- **Synthetic, not upstream.** The fixture exercises the gate's raw comparison only. It supplies
  no evidence about any real captured page, quotation authenticity, source completeness, or
  semantic support. The existing S017/S018 controls remain the evidence for real raw sources.
- **A rendered quote is indistinguishable from a fabricated splice here.** Both fail the same
  whole-source test (`:256-258`). That is the documented limitation, not a capability: manual
  rendered/code/JSON inputs must stay out of raw machine grading, which is the round-14 routed
  defect this control supports (this seat did not edit `QUALITY.md` or the gate).
- **Provenance is advisory.** The gate ignores top-level keys (`:173-176`); if a future gate adds
  a strict schema, both manifests would become `invalid_manifest` (exit 2). Current behavior is
  observed from source, not executed.
- **Byte-exact coupling.** Both manifests pin the same 34-byte source; any edit yields
  `source_tampered` for both, so the positive and boundary controls cannot silently diverge.
- **No capability or score claim.** No gate code, test, corpus row, manifest expectation, or
  owned proxy was changed. This is a calibration-depth control only; no numeric axis movement
  is asserted.
- **No installs.** No tool was installed or updated for this work.

Blockers: none.
