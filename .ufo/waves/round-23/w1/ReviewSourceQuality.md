# ReviewSourceQuality — R23-C1

Axes: **calibration** (source attribution, quote fidelity, and limits on what manual/code sources establish) and **coverage** (whether the inherited quote/source-link rules are applied to the new primary-source boundary). Author-side review only; no integration or admission is claimed.

## Findings

- **LOW — unresolved `used-by` destination.** `corpus/SOURCES.md:64-66` currently lists `corpus/lessons/round-23.md` in S058-S060 `used-by`; reading that exact path returned `No such file` at this review cutoff. This is an incomplete source-registry reference until the lesson is added or the cells are corrected. No census was run and no census failure is claimed.
- `corpus/QUALITY.md:26-27` (#16/#17) require contiguous, located research Gate quotations. Machine checking is limited to pinned raw prose excerpts with supported headings; code members, commit objects, JSON, command output, and rendered text require manual source checking. A verdict on an excluded representation is explicitly void for the manual-only claim.
- `corpus/QUALITY.md:39` (#29) requires a new held-verb entry to cite an opened, mined source row whose `used-by` names that entry and to bind the row verb to the exact producing command. `corpus/QUALITY.md:41` (#31) adds original-envelope, exact-command, supported-record, file-citation, refusal-ancestry, and pinned producer-operation requirements. `count-c1.py:80-84,107` implements the declared source-link predicate and explicitly leaves source relevance manual/no-authentication; that matches frozen `claims.json:37-38` rather than claiming semantic source proof.
- Current `corpus/SOURCES.md:64-66` identifies S058 as the pinned sigrok-cli manual, S059 as the pinned sigrok-dumps README, and S060 as the original REA envelopes; the new entry's `source:` line cites all three (`corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:1`). The source declarations are appropriately scoped: S058 disclaims REA output semantics, S059 disclaims observed hardware acquisition/lossless decoding, and S060 disclaims hardware state, executable authenticity, and complete UART correctness. I manually checked the S058 input-file wording against retained `evidence/sources/sigrok-cli.1:110-115` and opened the pinned S059 raw README; both match the attributed limits.
- `SignalRawFormat.md:21-29` quotes the raw binary-format page's `<pre>` body contiguously; I opened the raw wikitext and confirmed the body. `SignalCarrierAlternatives.md:36-55` quotes one contiguous passage from the pinned README (URL at `:28`), confirmed against that raw README. Neither report claims a quote-fidelity verdict; their underlined/plain-text or markup/code representation is not submitted as machine-gradeable QUALITY #17 prose.
- The code-source boundary in `UartSemantics.md:8-10,245-247` is manual, not gate-graded: the report pins the official release/tag/commit and source-file digest with line anchors. I opened the local `pd.py` cited ranges (`:85-123,391-402,501-507`) and sigrok-cli `parsers.c:429-479`; their cited declarations, stop-bit emission, and numeric option conversion match. `pd.py` and its tag copy hash to `51a29d0e51f9af21a60bcee2d2fb66410c90e348010ab3ab44898bdc1e97da62`; `parsers.c` hashes to `0d2cffb62f3e1162126f3e17955b09832c60c37c98210844b8b33493c9a19b7e`. These code-source notes are not cited by the new knowledge entry as proof of a runtime decode.
- **LOW — superseded source-ID proposal remains in a report.** `w1/CoverageMap.md:213-220` still proposes S058 as own-work and S059 as a tool pin; current `corpus/SOURCES.md:64-66` assigns those IDs to the manual and dataset and uses S060 for own-work. The landed knowledge entry cites S058/S059/S060 correctly, so this is not a current entry misbinding; the stale proposal must not be reused for later registry edits.

## Residual risk

The landed S058-S060 rows and their cited offline-signal entry were available and manually reviewed. The source-to-claim boundary is appropriately divided among the sigrok-cli manual (input/decoder options), the pinned dataset README (author-declared channel/settings), and original REA envelopes (measured tool records). The two code-source investigations (`SignalRawFormat.md` and `UartSemantics.md`) remain report-level work and are not cited as runtime evidence by this knowledge entry. Remaining risk is source-registry completeness: the three rows also point to a lesson path that was absent at review time, and the source-ID proposal in `CoverageMap.md` is now stale. Manual source relevance is not mechanically proven by `count-c1.py` and remains a reviewer duty, as its own `limit` states.

## Verification gaps

- No language-server route is exposed in this session. I attempted `read xd://lsp`; it returned “No such tool: xd://lsp” and listed the mounted devices, which contain no LSP device. Therefore no LSP status, references, definition, or diagnostics checks were possible. Any text searches were used only to locate material, not as semantic proof.
- S058-S060 and `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md` were present at the later review pass; the exact source rows and their entry linkage were read. The cited lesson path remains unresolved as described under Findings. No round-23 lesson or final source census result was available in this review.
- No builds, tests, linters, formatters, REA probes, or source-code executions were run for this review.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewSourceQuality.md` — report file; its final SHA-256 is included in the delivery message.

## Installs

None.

## Open risks

The current source records are well-bounded, but final registry closure remains open until `corpus/lessons/round-23.md` exists or is removed from the `used-by` cells and the required census is run by the integration owner. The `CoverageMap.md` source-ID proposal is superseded by the current S058-S060 rows and should not be reused. This review is not outside verification or an admission.