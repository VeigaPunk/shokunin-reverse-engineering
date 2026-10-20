# Round 14 — ReviewRegistry: used-by additions for S003–S006

Seat: `KaidokuR14.ReviewRegistry` (leaf reviewer, author-side; cannot provide non-author admission).
Scope: registry conformance of prospective `used-by` additions for S003–S006 and whether all four must be reopened. No new source rows, no knowledge entry drafted, no shared file written. Access date for every source below: 2026-10-20.
Tools: none installed or upgraded. No builds, tests, linters, or the `scripts/sources-census.sh` CLI were run; only read-only awk/grep counts and hash checks.

## 1. Canonical rules that govern this check

Contract text: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 64–148 (frozen SOURCES Contract v1); corpus-wide rules lines 22–62 and 163–184.

- `CORPUS.md:107-108` — `used-by` is "repo-relative paths of the knowledge entries or lessons citing the row, comma-separated, or `—`."
- `CORPUS.md:103` — `mined` means "cited by ≥1 path in `used-by`."
- `CORPUS.md:112-115` (Rule 1) — "Write it only after opening the source in the round that writes the row." This governs **new** rows.
- `CORPUS.md:116-118` (Rule 2) — "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson." `opened` and `anchor` are immutable.
- `CORPUS.md:123-125` (Rule 4) — no row quota; expansion counts admitted knowledge entries citing a `mined` row.
- `CORPUS.md:129` (Rule 6) — no credentials or `op://` references.
- `CORPUS.md:163-170` — a new knowledge entry opens with `source:`, `verified-at:`, `recheck:`; external sources cite their `S###` row with URL and anchor.
- `CORPUS.md:19` — each `lessons/round-<N>.md` carries a `## Gate` section.
- `CORPUS.md:61-62` — each round's review emits a per-repo verdict, `conformant` or `not conformant`, naming the failed rule and the command that shows it.
- `CORPUS.md:179-184` — a claimed fix ships a red-before state.
- `corpus/QUALITY.md:4-5` — criteria are appended as new rows naming what they supersede, never rewritten.

## 2. Answer: must all four be reopened?

**Not by the `used-by` rule itself.** Adding a path to `used-by` is an in-place change permitted by Rule 2. It does not write a row, so Rule 1's open-before-write obligation is not triggered. The round lesson must log the change old→new.

**What is required is quote-level verification of whatever the knowledge entry carries.** The C1 entry will make claims that rest on all four sources, so each quote it uses must be checked at its pinned revision. The entry's `verified-at:` must equal the date its quotes were actually verified. Rows keep `opened` = 2026-10-19; a 2026-10-20 check is recorded in the entry and the lesson, not in the row.

**Recommendation: reopen all four at write time.** The reopen cost is low: two local files (hash plus line), and two commit-pinned URLs. C2 also needs a captured local excerpt with a digest for every cited source. This seat reopened all four on 2026-10-20 (section 3); that is author-side checking, not non-author admission.

## 3. Sources opened by this seat (2026-10-20)

| id | location | verified |
|---|---|---|
| S003 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` | `sha256sum` = `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, matches row. Member `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` (`unzip -p`): line 79 `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");`; line 171 `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));`; line 176 `apiSnapshot = GoApiSnapshot.get(...)`; line 359 `"Missing Go bootstrap type info, ..."`. Member `GoApiSnapshot.java`: line 115 `return GoApiSnapshot.EMPTY;`; line 242 `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());`. |
| S004 | `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174` (reader) | Title `# GP-6528 add support for golang 1.26`; author date 2026-03-03T19:52:38Z. Diff hunk `@@ -76,7 +76,7 @@` on `GoRttiMapper.java`: `-…GoVerRange.parse("1.15-1.25");` / `+…GoVerRange.parse("1.15-1.26");`. Also adds `data/typeinfo/golang/go1.26.0.json` and edits `GoPcHeader`, `GoMapType`, `GoTypeFlag`. |
| S005 | `https://github.com/mandiant/GoReSym/tree/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` (reader); `https://api.github.com/repos/mandiant/GoReSym/commits/d7f23b7a3e8e259ae7dd0bec9a94eec66df6257d` | Commit author/committer date `2026-02-17T15:14:48Z` (matches row). README `# Version Support`: "This library current handles the `pclntab` layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20." README `# Changes`: "Added parsing support for Go 1.24 binaries while retaining compatibility with older 1.2 layouts." Same commit's `main_test.go` patch changes the test versions to `"122", "121", … "15"`. |
| S006 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/GhidraClass/BSim/BSimTutorial_Intro.md` | `sha256sum` = `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e`; 88 lines. Line 13 `# How Does BSim Work?`; line 19: "Certain attributes, such as values of constants, names of registers, and data types, are intentionally not incorporated into the features." |

Other files read: `corpus/SOURCES.md` (rows S003–S006 at lines 9–12), `CORPUS.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/lessons/round-13.md`, `corpus/lessons/round-13-verifier-spotcheck.md`, `.ufo/waves/round-14/{claims,spec,dispatch}.json`.

## 4. Round-13 quotes re-checked against source

| id | round-13 Gate quote | status | note |
|---|---|---|---|
| S003 | `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` at `GoRttiMapper.java:79` | exact, line 79 confirmed | Code, not Markdown. |
| S004 | "GP-6528 add support for golang 1.26" (commit title) | exact | Title is `# GP-6528 add support for golang 1.26` in the reader output. |
| S005 | "This library current handles the pclntab layouts pre 1.2, 1.2, 1.16, 1.18, and 1.20." | **not verbatim** | Source has backticks around `pclntab`. Strict contiguity fails unless the gate normalizes inline-code markers. See F4. |
| S006 | "names of registers, and data types, are intentionally not incorporated into the features." | exact, line 19 | Row anchor says lines 15–22; the Gate says 15–20. Both contain line 19. Cite line 19. |

## 5. Current census (read-only awk from CORPUS.md:133-148, run 2026-10-20)

- rows: 22 (`grep -cE`)
- malformed (NF≠13): 0
- tiers: A=20 B=1 C=1
- statuses: mined=21 rejected=1
- duplicate ids: none
- enum violations or tier inflation: none
- mined rows whose `used-by` paths are missing: none

S003–S006 are `mined`, each with `used-by` = `corpus/lessons/round-13.md`, which exists. **Current on-disk state: conformant on every census check run.** The CLI `scripts/sources-census.sh` was not run; L1 should run it once after integration.

## 6. Prospective additions: findings

**F1 — target paths do not exist yet (blocking ordering).** `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` and `corpus/lessons/round-14.md` both return "No such file" (`ls`, 2026-10-20). `CORPUS.md:46` ("write the row when the file exists, not before") and the census `missing:` check mean `used-by` must be written after the entry exists. Writing it earlier turns the census red.

**F2 — `used-by` must match citations exactly.** Each row may list only paths that actually cite it. Target `used-by` values, assuming the entry cites a row, for each row the entry cites:
- `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
- add `corpus/lessons/round-14.md` only if the round-14 lesson cites that row (its Gate or Mistakes section).
- Check: `grep -c 'S00N' corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` ≥ 1 for each row listed. Do not list a row that the entry only mentions as a lead.

**F3 — S006 is scope-risky for a version-gate entry.** The row's scope is "Ghidra BSim feature-vector similarity for candidate function matching," with `teaches` on which properties BSim abstracts away. It does not cover Go version gating. Cite it only for a bounded limitation (names and types are intentionally dropped, so name-free similarity is candidate matching only). Citing it for version-gate diagnosis would be scope inflation. Use `S006` only if the entry carries that limitation.

**F4 — quote-fidelity gate needs a backtick policy and a non-Markdown policy (affects C2).**
- S005's quote contains backticks in the source. The round-13 Gate dropped them. C2 must either quote with backticks or define an explicit normalization for inline-code markers. Without that, a faithful quote fails `quote_not_contiguous`.
- S003 is Java inside a zip. The gate's model (Markdown excerpt, `section` = exact heading incl. `#`) cannot express a Java line. A captured excerpt file with its own `section` anchor and digest, plus a documented `source` mapping to `Base-src.zip`, is needed. Otherwise S003 is ungateable.
- S004 is a Markdown-converted diff. Its section is the file heading (`### Ghidra/Features/Base/src/.../GoRttiMapper.java`), which works.

**F5 — S005 is internally inconsistent; the entry must not state a ceiling without it (calibration, high).** The pinned README's `# Version Support` lists pclntab layouts only "pre 1.2 … 1.20". Its own `# Changes` bullet says "Added parsing support for Go 1.24 binaries", and the same commit's `main_test.go` tests versions up to 122. An entry that quotes "1.20" as GoReSym's ceiling without the Changes bullet is a misreading. An entry that claims 1.26 support from S005 is unsupported (the row already says so). Cite both bullets or neither.

**F6 — the installed gate logs, it does not reject (calibration, high for C1 content).** From S003 lines 171, 176, 115, and 242: a Go version outside `SUPPORTED_VERSIONS` produces `Msg.error("Untested Go version …")` and processing continues. A missing snapshot yields `GoApiSnapshot.EMPTY`, which has an invalid version. `BootstrapInfoException("Missing Go bootstrap type info…")` at line 359 fires only when struct mapping fails with an invalid snapshot. An entry that says the gate "rejects" 1.26 contradicts line 171. The S003 row's anchor lists `GoApiSnapshot.java:get` (a method name, not a line). The entry should cite lines 115, 171, and 176 directly. Do not edit the row (Rule 2). This is cross-lane with ReviewGoInference; flagged here because it decides whether the `used-by` addition is true.

**F7 — provenance trio and immutable columns.**
- The entry opens with `source:` (cites S003–S006 with URL and anchor), `verified-at:`, and `recheck:` (`CORPUS.md:163-170`). `verified-at: 2026-10-20` is valid only if the quotes used are checked that day (section 3).
- Do not change `opened` (stays 2026-10-19), `anchor`, `teaches`, or `scope` (`CORPUS.md:116`).
- Log the `used-by` change old→new in `corpus/lessons/round-14.md` `## Gate`: old `corpus/lessons/round-13.md`; new `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (plus the round-14 path if cited).

**F8 — S006 anchor and reproducibility (non-blocking).** The row lacks a SHA-256 (S003 has one). Its anchor is "lines 15–22" and the quote is at line 19. The entry should record `a23562a3…c33e` in its own `source:` line and cite line 19. Do not rewrite the row.

**F9 — expansion ground (non-blocking).** No coverage-map row in `corpus/README.md` covers the Go version gate. The nearest entries are `2026-10-13-r4-10-real-version-pair` (Go bump collapses symbol recovery) and `2026-10-19-arc3-r12-go-evidence-id-domain`. The entry counts toward expansion only if it cites a `mined` row on uncovered ground (`CORPUS.md:123-125`). Any README coverage or Knowledge row is written after the file exists (`CORPUS.md:46`).

**F10 — C2 red-before and QUALITY row (for L1).**
- The gate must show a red-before state (`CORPUS.md:179-184`): exit 1 with `quote_location_mismatch` or `quote_not_contiguous` on the S017 splice and S018 mislocation fixtures, with the observed text committed.
- The QUALITY criterion must be a new appended row (16), citing round-13 lesson Mistakes #3 and #4 (`corpus/lessons/round-13.md` addendum). Its supersedes cell is `—` unless it actually replaces row 1 (`QUALITY.md:4-5`).
- Round-14 `## Mistakes` may cite existing mistakes #3 and #4 rather than re-minting them (`CORPUS.md:171-178`).

## 7. Exact conformance checklist (write order)

1. Confirm `corpus/lessons/round-14.md` `## Gate` exists before any `used-by` change (`CORPUS.md:19`).
2. Create `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` with `source:`, `verified-at:`, `recheck:` first (`CORPUS.md:163-170`). Cite S003 lines 79, 115, 171, 176 and S004 hunk `-76,7`; S005 README `# Version Support` and `# Changes` (both bullets); S006 line 19 only if cited. Record the S006 SHA-256 if cited.
3. Cite only quotes that exist verbatim at the stated location, and at most 25 words each (`CORPUS.md:114`).
4. Verify each cited row with `grep -c 'S00N'` on the entry (F2).
5. Change `used-by` in place for each cited row only: S003, S004, S005 (and S006 only if cited). Keep `opened`, `anchor`, `teaches`, `scope` unchanged. Status stays `mined`. Recheck changes only with a logged reason.
6. Log each change old→new in `corpus/lessons/round-14.md` `## Gate` (`CORPUS.md:116-118`).
7. Run the awk census (`CORPUS.md:133-148`) read-only: malformed 0; duplicate ids none; enum/inflation none; mined `used-by` missing none. Then run the CLI once (L1).
8. Add the README Knowledge row only after the entry file exists (`CORPUS.md:46`).
9. Emit the per-repo verdict in the round report: `conformant` or `not conformant`, with the rule and command (`CORPUS.md:61-62`).

## 8. Verdict and limits

- **Pre-write state (on disk now):** conformant on every census check run (section 5).
- **Prospective state:** conformant only if checklist items 1–9 are done and F4, F5, F6 are resolved in the entry text. Not established: the entry itself (not yet written), the C2 gate's behavior (not run), and any non-author admission.
- **Limits:** S004 and S005 were read through the GitHub reader and API, not a local clone. The S006 and S003 checks are local. The round-13 non-author review (`KaidokuR13Review`, 2026-10-19) covered the S003 and S008 admissions and all 22 rows; this seat's check does not replace that sample.
- **Installs:** none. No `RULES.md` read was needed.
