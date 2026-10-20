# AttackTrends — round-14 trend-verdict critique (critic, author-side)

Seat: `KaidokuR14.AttackTrends`. This seat was dispatched by L1, so it is **author-side**. Per `LEARNING.md:46` (“A subagent the lane dispatched is still the lane.”), nothing here counts as the outside spot-check. Date: 2026-10-20. Axes: coverage and calibration. I edited nothing except this report. No build, test, or gate run was performed, and I installed no tools.

## Verdict summary (recommended, defensible)

| Trend | Recommended r14 verdict | Condition that flips it |
|---|---|---|
| expansion | **unchanged** by default | Becomes `improved` only if C1's map row names a question that README:35, PROVINCE:52 and r4-10 do not already hold, and an outside judge agrees. C2's gate/capability never counts as expansion. |
| quality | **improved**, but only under two conditions: C1 describes the mechanism correctly (F2), and r4-10 gets an append-only pointer | Becomes **harmed** if C1 says `SUPPORTED_VERSIONS` refuses or gates Go 1.26 recovery, because the entry would then fail its own bar. |
| discernment | **improved, bounded** — only via LEARNING clause 2, from the r13 *outside* disagreement (S017/S018) turning into a grounded QUALITY criterion | Becomes **unchanged** if the criterion only restates CORPUS “A quote names its location” or does not supersede r13's “no extra QUALITY criterion” note. No r14 seat agreement can count. The r14 admit+reject outside sample is still pending. |

## F1 — C1 is curation and diagnosis of ground the lane already holds, not uncovered expansion (impacted: coverage/expansion)

**Counterexample.** The Go 1.26 recovery collapse, and a causal attribution for it, are already held in three places:
- the coverage map, `corpus/README.md:35`;
- PROVINCE core, `PROVINCE.md:52`;
- the r4-10 entry, `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73,102-118`.

r4-10:70-71 states: “Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout”. It also records the transient `Missing Go bootstrap type info` log as “observed-not-cited”. A source-backed explanation of *why* that happens is what LEARNING's quality row describes (“a weaker entry is superseded by a stronger one”, `LEARNING.md:34`). It is not ground “the coverage map did not hold” (`LEARNING.md:33`).

Lane precedent points the same way. arc2-r3 refused “a re-run dressed as a move” (`SCORECARD.md:808-809`). r13 accepted the critic's point that curation is not expansion (`SCORECARD.md:2164-2166`; fleet `.ufo/waves/kaika-w3/kaidoku-r13-critic.md:7-9`). The r13 plan also gates r14 on “the matching uncovered coverage-map question remains” (`SCORECARD.md:2174-2175`).

**Smallest safe correction.** Choose one of two options:
- **(a)** Record C1's trend credit as quality, and add an append-only pointer on r4-10.
- **(b)** Keep the coverage label, but write a new coverage-map row for a question that is actually distinct. The narrowest admissible one: “installed-vs-upstream Go-analyzer support boundary and pre-run diagnosis (12.1.4 snapshot set vs GP-6528 vs GoReSym README range)”. Expansion stays `unchanged` until a non-author admits it.

The `0 → 1` count observable may still verify as a count. It does not by itself establish that the ground was uncovered.

## F2 — calling it a “version gate” overclaims; the installed source treats the range as advisory (impacted: coverage/quality, calibration)

I reopened the installed source, `Base-src.zip`, SHA-256 `f00d29c2…a8d804`, which matches the S003 pin.

- **The range check is a soft log.** `GoRttiMapper.java:170-171`: `if (!SUPPORTED_VERSIONS.contains(goVer) ) {` → `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`. Execution then continues to `GoApiSnapshot.get`. The only other use of the range is `getAllSupportedVersions()` at :269-275, and no other Go-package or analyzer class calls it. I checked by grepping the extracted `golang/*` and `analysis/Golang*` sources.
- **The hard failure comes from the missing snapshot.** `GoApiSnapshot.get` returns EMPTY when no `typeinfo/golang/go<major.minor>.0.json` exists. Its javadoc says: “possibly an {@link #EMPTY} instance if no matching snapshot file is found”. The installed `data/typeinfo/golang/` directory holds `go1.15.0.json` … `go1.25.0.json` and has **no `go1.26.0.json`**. When structure registration fails with an invalid snapshot, `GoRttiMapper.java:358-359` throws “Missing Go bootstrap type info, unable to extract Go RTTI info.” `getSharedGoBinary` (:114-116) then warns and returns null. That message matches r4-10's observed log line. `[INFERENCE]` With an EMPTY snapshot on 1.26, registration fails; this was not executed here.
- **Upstream confirms a two-part cause.** GP-6528 (`385e8cd9…`, fetched through the GitHub API on 2026-10-20) adds `+data/typeinfo/golang/go1.26.0.json||GHIDRA||||END|`, widens the range to `"1.15-1.26"`, and changes struct mappings for 1.26:
  - `GoPcHeader` `textStart` becomes `@FieldMapping(presentWhen = "1.18-1.25")`;
  - `GoMapType` gains `group` for `"1.26-"` and drops `bucket`/`keysize`/`elemsize`/`bucketsize`.

  So r4-10's “layout” attribution is **incomplete, not false**. The cause has two parts, a missing snapshot and struct changes, and the range check only logs.
- **Smallest safe correction.** The C1 entry should say: “the installed 12.1.4 range is advisory (‘Untested Go version’ log); recovery fails through the missing go1.26 API snapshot → BootstrapInfoException; upstream GP-6528 adds both the snapshot and 1.26 struct mappings.” Label the 1.26 failure on 12.1.4 as `[INFERENCE]` from source plus r4-10's uncited log. Do not claim that a newer Ghidra release contains GP-6528; `SOURCES.md:50` lists later release notes as unopened.
  - claims.json's “version-gate” wording and the S003 row's “version gate” scope should be read as “version check + snapshot bootstrap”.
  - If the entry asserts a hard gate, it fails QUALITY #2/#5. Under `LEARNING.md:33` that makes expansion **harmed**.
- **GoReSym bound.** Its README covers “pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20.” The upstream mapping shows a 1.26 pcHeader change, so the entry must not extend GoReSym's stated range to 1.26. `[INFERENCE]` from Ghidra's mapping annotations, not from Go's own spec.
- **S006 (BSim) relevance.** BSim is a matching route, not evidence about the version check. If it is cited in a diagnosis entry, it should be scoped as an alternative cross-version matching route. Otherwise it pads the source list.

## F3 — the C2 demonstration depends on fixtures; both prior sources are HTML, not Markdown (impacted: calibration)

The gate contract requires “exact Markdown heading text including #”. Neither prior source has `#` headings:
- **S017.** The pinned View8 `README.md` (fetched 2026-10-20; git blob `2a0c5a60…` equals the r13 reviewer's sha; sha256 `191621cd…619b`) uses HTML headings. Line 20 is `<h3>Command-Line Arguments</h3>`, and the corrected quote sits in an `<li>` at :40 after `<code>--normalize</code>:`. The splice's first half is at :82 as `Use <code>--normalize</code> to replace…`.
- **S018.** The capture `w1/s018-raw.html` (355,603 B, sha256 `31b82315…dd5e`, mtime 2026-10-20 02:14 -0300) uses `<h1 class="wp-block-heading">`. The quote is at byte 98554, between `Introduction` (96000) and `Distributed payloads` (99208); `Decompiled output` is at 106823. This confirms the r13 relocation independently of the reader's line numbers 77/87, which depend on the converter.

**Consequence.** The fixture producer's HTML→Markdown transform decides heading levels and markup stripping. A manifest `sha256` pins that derived excerpt, not the source. An honest quote with markup stripped (r13's reviewer allowed stripping backticks/bold) could trigger `quote_not_contiguous` if the excerpt keeps `<code>`. The splice is caught either way.

**Smallest safe correction.** The manifest or report should record each raw capture's sha256 and a deterministic transform recipe next to the excerpt digest. C2's `limits` should say “normalized excerpts of HTML sources”.

**Robustness counterexample for the code owner (not run).** Duplicate heading text, such as the empty `<h1>` before `Introduction` in S018, can make “section = heading text” ambiguous. The gate should either require a unique heading match or emit a stable finding for ambiguous ones.

## F4 — the QUALITY criterion must supersede r13's disposition and not duplicate CORPUS (impacted: calibration/discernment)

`corpus/lessons/round-13.md:76` says: “The existing CORPUS/SOURCES quote rule caught both defects; no extra QUALITY criterion was added.” But the outside reviewer caught the defects, not the author's gate. The “captured-by” cells in Mistakes #3/#4 overstate the existing rule.

Location is already required by CORPUS “A quote names its location” (`CORPUS.md:42`) and Contract v1 rule 1. **Contiguity** exists only as lesson text (Mistake #3 fix: “Quote one contiguous source substring”).

**Smallest safe correction.**
- The QUALITY row should cite `round-13.md` Mistakes #3/#4 and `kaika-w3/kaidoku-r13-review.md` §4.
- It should state the new requirements: a contiguous verbatim substring, inside the named heading's section, checked mechanically.
- The r14 lesson should append that r13's “no extra criterion” note is superseded, and why.

Without that, the lane has two authorities that contradict each other (the r13 lesson and the r14 QUALITY row). Under `LEARNING.md:35`, a criterion that only duplicates location adds no grounded learning.

## F5 — the outside-check boundary (impacted: calibration/discernment)

- All 32 w1 members (`w1/swarm-registry.json`) are `KaidokuR14.*` spawns. ReviewS017, ReviewS018, ReviewGoInference and this seat therefore cannot be cited as `agree`/`disagree` non-author evidence (`LEARNING.md:42-48`).
- LEARNING requires a per-round sample of “at least one admit and one reject”. r14 should record at least one honest reject so that sampling is possible, for example rejecting the “hard version gate” framing or BSim as diagnosis evidence.
- The r14 spot-check is still the orchestrator's to do. Stating that it is pending is not harm. Claiming it as done would be false provenance.
- The r13 discernment credit (S003/S008/S022 agreement, `SCORECARD.md:2167-2170`) is a separate event from the clause-2 credit. Neither may be counted twice.

## Checks actually run

These were read-only, local or fetched. Nothing was executed against a target, and no REA session was used.

- `sha256sum` of `Base-src.zip`; `unzip -p` reads of `GoRttiMapper.java` (:79, :98-132, :140-200, :262-275, :335-370) and `GoApiSnapshot.java` (javadoc and `get`).
- Usage grep of `SUPPORTED_VERSIONS` / `getAllSupportedVersions` over the extracted Go and analyzer sources.
- `ls` of the installed `data/typeinfo/golang/`.
- GitHub API commit `385e8cd9…` (files and patches).
- `curl` of the pinned View8 `README.md`, plus `git hash-object`.
- Byte offsets in `s018-raw.html` via `grep -bo`.
- `git status` on the lane (only `.ufo/waves/round-14/` untracked) and on the main checkout's `LOG.md`. The r13 reviewer's one-line residue is gone: clean, empty diff.

The quote gate does not exist yet, so its selftest and verdicts were **not** run. No C1 entry draft was present in `w1/` to inspect.

## Sources opened (2026-10-20)

| Source | Location | Quote (≤25 words, contiguous) |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/LEARNING.md` | :33 expansion row | “net new admitted entries on uncovered ground, each citing its coverage-map row” |
| same | :46 | “A subagent the lane dispatched is still the lane.” |
| `/home/vgpnk/Projects/shokunin/CORPUS.md` | :123 rule 4 | “Expansion is knowledge, not rows.” |
| `corpus/lessons/round-13.md` | :76 | “The existing CORPUS/SOURCES quote rule caught both defects; no extra QUALITY criterion was added.” |
| `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` | :70-71 | “Ghidra 12.1.4's Go analyzer cannot parse the Go 1.26 moduledata/pclntab layout” |
| `SCORECARD.md` | :2174-2175 | “Round 14 may mine one source-backed knowledge entry only if the matching uncovered coverage-map question remains.” |
| `Base-src.zip` → `GoRttiMapper.java` | :358-359 | “Missing Go bootstrap type info, unable to extract Go RTTI info.” |
| GitHub API, commit `385e8cd923d09f10b1a7874108e71748875fa174` | `GoRttiMapper.java` patch | `GoVerRange.parse("1.15-1.26");` |
| View8 README @ `ef39099b` | :20 | `<h3>Command-Line Arguments</h3>` |
| `.ufo/waves/kaika-w3/kaidoku-r13-critic.md` | :7 | “A new source registry/capability is valuable curation, but it is not the contract's expansion unit.” |

## Limitations

- Source text does not prove what REA or Ghidra does on a target. The 1.26 failure path on 12.1.4 is `[INFERENCE]` from source plus r4-10's uncited log.
- I did not open a GoReSym release newer than `d7f23b7a`, any Ghidra release after 12.1.4, or BSim internals.
- The GitHub API patch listing can be truncated for large files; it was complete for this 9-file commit.
- These verdicts are recommendations; the canonical judge decides.
