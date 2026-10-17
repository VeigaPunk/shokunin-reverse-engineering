## CLAIM
Landing manifest for luna-round-9: the four append-only texts, each with home and post-landing invariants, copy-paste-ready.

## METHOD
Static compile at HEAD `a280e07` from the wave receipts (Z1–Z5, Q1–Q4, H/H4, X4, C1–C4, D1–D4, E1, R5, CB4–CB7, HB2, RB3, TB1, VB4, T1–T2, G2–G4, F3, P0–P2); primary reads: `PROVINCE.md:114-116`; r4-16 `:750-753,:925`; r12-01 `:97-120`; r2-jq `:12,:217-219,:236-237,:242`; `SCORECARD.md:453-460,:559`. Base hashes via `sha256sum`. Only write: this file.

## FINDINGS
**1 — L197 pointer → `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md`, EOF append after `:925`** (base 64,080 B, sha256 `622e3661d3e7f824393554b7cb428a233cc607a890ef77b4dfebeb24cce1d22e`; Q1 clause-verified; “7 values” attributed):
> - **L197 normalization cross-reference:** the two-site summary above (`:751-752`) is historical; see r12-01’s round-12 audit (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:99-104`) and round-5 freshness erratum (`:110-120`). The corrected account is two variance classes across `files[].path`, `output_directory`, `chunks[].provider_id`, and `derivations[].provider_blob_id`; “7 values” is attributed, not re-derived because the `/tmp` receipts are gone (`:115-118`).

**2 — census known-limits → `SCORECARD.md`, in a new `## luna-round-9 — freshness: carried-spill queue, 2026-10-16` section appended after `:559`** (base 34,819 B, sha256 `0c7229367ba4e27083eff465a2ae3cf0f917b9f4424e2306add65ddb55a05734`; home SCORECARD per X4/B4; B3 guard appended):
> Known census-instrument limits (rounds 4–5): SIZES normalized punctuation in source text but not comma-grouped needles, so it could not match correct `29,367,752` / `84,258,816` values (`.ufo/waves/luna-round-5/X1.md:32`; `CB4.md:11`). Round-4 F18 was structurally unsatisfiable (`.ufo/reports/luna-round-4/kaidoku.md:43-45`); the round-5 README-opener detector matched the retained “Runtime-obs extended” opener, not corrected content (`.ufo/reports/luna-round-5/kaidoku.md:63-67`). Treat these as census limitations, not content verdicts; validate claims against cited sources.
> Status: ADJUDICATED (not PASS); matchers unrepaired — future findings stay evidence-adjudicated (B3).

**3 — `/tmp` disposition → the same round-9 SCORECARD section + the `LOG.md` round entry (`P2.md:8-17`)** (no corpus append, no deletions):
> - **`/tmp` dependence (round-9 audit):** no current kaidoku instruction, registered gate, or landed `recheck:` requires pre-existing `/tmp` contents; `/tmp` is transient scratch (`PROVINCE.md:48`; `.ufo/rounds/interactive-r1/verify-recovery.py:123`). Labeled residuals: historical `verify:` recipes cite prior `/tmp` outputs (`corpus/knowledge/2026-10-13-r3-renderer-asar.md:11,19`; `corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:40-42`) — archival debt, not a current dependency; L7-01’s npm-cache pre-existence untested (`corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:5`). The ~1.2 GB litter remains operator hygiene; no deletion authorized or performed (C2).

**4 — jq qualification → `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md`, EOF append after `:242`** (base 16,295 B, sha256 `541f3499c811b023f4a19e1aacef0129ef34222990f928de9f3d0a54fe4dbf2e`; Z4 text, `:12`/`:219` broadenings per Q4/D4/VB4):
> - **Safety-verdict scope (round 9):** Here, “benign” (historical wording, not a present endorsement) refers only to the entry’s recorded SHA-256 byte-identity match between `~/.local/bin/jq` and the upstream jq-1.8.2 `jq-linux-amd64` release artifact (`corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:10-13,204-219`). It is not a verdict that the upstream artifact is safe, trustworthy, or licensed for reuse; identity and provenance do not establish those properties (`PROVINCE.md:114-116`). “Not binary compromise” (`:219`) likewise asserts only no recorded byte difference — not a security verdict. This note qualifies, but does not rewrite, the historical wording at `:12`, `:217-219`, `:236-237`.

**Invariants (post-landing):** command A (`SCORECARD.md:92-123`) = 79/79, 9/9, 10.0/10.0, empty missing/dangling (exact JSON `G2.md:9-11`); README coverage-map token set 79 unique, unchanged (use TB1-corrected token sha256 `bd70aa5f…750c4`); targets are pure tail appends — new blob starts with its base blob, `head -c <base size>` = sha256 above (G4/T1); changed paths ⊆ {r4-16, r2-jq, SCORECARD, LOG}, zero deletions, other tracked files byte-identical; `PROVINCE.md` blob `8a1cec88b50f0e9aa928b0c042354a017217ad47` unchanged.

## THREATS
Compiled, not re-adjudicated: no census rerun, no `/tmp` inventory; “7 values” stays attributed. Z1’s “append to the r12-01 erratum block” is compiled as an EOF tail (prefix identity) — parent’s placement call; H4/CB4 would trim text 1 to pointer-only. Residuals, not landed: r3-jq bleed (`2026-10-13-r3-jq-provenance.md:60,136`) and stale `:107-109` pointers (`SCORECARD.md:79`; `corpus/lessons/2026-10-15-round-1.md:149-153`). No landing executed.

## VERDICT
CLEAN — manifest compiled: four texts, homes, invariants; landing and post-checks remain the parent’s.
