# ReviewR30R29Fixes — routed round-30 defect fixes 3, 4, 5, 7, 8

Seat: `KaidokuR31.ReviewR30R29Fixes` (leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Lane base `c369242fee9f559f895e3f7956b1242076c7b1be`; lane tip `1288285eed81395e6af7c279a173b117b2c2eaa3`.
Review run 2026-10-23, report written `2026-10-23T04:32:03Z`. Read-only on the lane; no tools installed
(no pacman/uv/npx/cargo action); no REA run; no git/jj writes.

Targets (frozen in `.ufo/waves/round-31/claims.json` at lane commit `35ba7c522dba55f9be27eb161d4254eacaa24330`):
1. appended correction in `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (pointers 302/306/139/143 vs `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js`; l7-02:10 citation);
2. appended line in `corpus/lessons/round-30.md` (restore ≤02:44:44Z vs round-30 evidence);
3. owned-axes coverage/depth rows in `SCORECARD.md` vs recipe A at `c369242f`;
4. docstring-only change of `tools/round-29/c1-fresh-naming.py` (`git diff c369242f 1288285e -- tools/round-29/c1-fresh-naming.py`, ast equality);
5. appended supersession in `.ufo/waves/round-29/claims.json` (commit field = the commit that changed the file; `git diff --numstat` additions only);
6. pre-existing lines of those files not altered.

---

## Item 1 — knowledge-file pointer correction (defects 3 & 4): **HOLDS**

Command: `git diff c369242f 1288285e -- corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` → `1 file changed, 2 insertions(+), 0 deletions(-)`, pure append (hunk `@@ -54,3 +54,5 @@`). Pre-existing lines unaltered.

Appended paragraph (exact, lines 55–56) matches the wave-1 draft in `ScribeR30Corrections.md:13` verbatim:
- `r-two-roots` `RustAuditableReader.js:151-153 → RustAuditableReader.js:302`
- `r-index-outside` `RustAuditableReader.js:154-157 → RustAuditableReader.js:306`
- `r-inflate-ratio` `RustAuditableReader.js:128-129 → RustAuditableReader.js:139`
- `r-not-zlib` `RustAuditableReader.js:131-134 → RustAuditableReader.js:143`
- cites `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md:10` and `corpus/lessons/round-30-verifier-spotcheck.md:146-147`, evidence `ScribeR30Corrections.md`.

Frozen prediction rows (`grep -nE 'r-two-roots|r-index-outside|r-inflate-ratio|r-not-zlib' corpus/evidence/round-30/c2/predictions.tsv`):
```
9:r-not-zlib	refuse	Dependency section is not a complete zlib stream	…	RustAuditableReader.js:131-134 inflateFailure Z_*
12:r-inflate-ratio	refuse	Inflated dependency JSON exceeds the size limit	…	RustAuditableReader.js:73,128-129 RUST_INFLATE_RATIO
19:r-two-roots	refuse	Dependency JSON declares more than one root package	…	RustAuditableReader.js:151-153 rootIndex
20:r-index-outside	refuse	Dependency index 584 from package 0 is outside the package list	…	RustAuditableReader.js:154-157 rootIndex
```
Installed reader (`sha256sum ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js`) =
`1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505` (matches S090's quoted `1f3748c9…` prefix; 309 lines). Read of the four target lines:
- `:139` `return new RustAuditableResourceFailure({ resource: "memory", reported_limits: { maximum_bytes: maximum } }, "Inflated dependency JSON exceeds the size limit");`
- `:143` `return new RustAuditableFormatFailure("malformed", "Dependency section is not a complete zlib stream");`
- `:302` `throw new RustAuditableFormatFailure("malformed", "Dependency JSON declares more than one root package");`
- `:306` `throw new RustAuditableFormatFailure("malformed", \`Dependency index ${String(outside)} from package ${String(index)} is outside the package list\`);`

All four corrected lines carry the exact predicted messages. `l7-02:10` (read) holds the limits: "Guards — 256 MiB file, 1 MiB section, min(8 MiB, 64× section) inflated JSON, 8 MiB report — are tool bounds, not OS limits." `round-30-verifier-spotcheck.md:146-147` are exactly routed defects 3 and 4. `ScribeR30Corrections.md` exists and records the same observation.

## Item 2 — lesson restore-time correction (defect 7): **HOLDS**

Command: `git diff c369242f 1288285e -- corpus/lessons/round-30.md` → `1 file changed, 2 insertions(+), 0 deletions(-)`, pure append at end (line 48). Pre-existing lines unaltered. Appended paragraph is verbatim the draft line of `ScribeR30Restore.md:11`.

Counter-claim exists: `RevOracleVsReadobj.md:15` (read) — "restored all 4 from wheel members at ~02:46Z and set chattr +i — verified:".

Evidence cites verified at the cited lines (all read):
- `round-30-verifier-spotcheck.md:37` — "The restored files carry 02:44:00Z mtimes, and reruns pass the input pin from 02:44:44Z."; `:41` flags the ~02:46Z inconsistency.
- `CtlC1AllFalse.md:113` — `pristine-repaired | 4ee65c67 | 2026-10-23T02:44:44+00:00 → 2026-10-23T02:44:58+00:00 | 1`; stdout reaches per-carrier `P1-fail` (not PIN), proving pin passed at 02:44:44Z.
- `CtlC1JunkRow.md:98` — `2026-10-23T02:44:52Z`–`2026-10-23T02:45:07Z`; counter exit 1 (full stdout, no PIN).
- `CtlC1ShortcutIds.md:73` — "passed the pinned-input checks and measured all 16 carriers"; `:147` — `UTC 2026-10-23T02:44:58+00:00–2026-10-23T02:45:12+00:00; exit 1`; `:195` — `UTC 2026-10-23T02:44:58Z–02:45:12Z. Exit 1`.
- `CtlC1NoReader.md:90` — `2026-10-23T02:45:05Z–02:45:18Z; counter exit 1` (full stdout).
- `CtlC1DoNothing.md:94` — rerun "passed the counter's carrier-identity validation … rather than a PIN exit"; `:102` — `UTC start: 2026-10-23T02:45:41+00:00. UTC end: 2026-10-23T02:45:52+00:00. Counter exit 1`.

All five first post-repair start times in the correction (02:44:44/52/58, 02:45:05/41Z) match the cited lines; the earliest passing-pin run is AllFalse at 02:44:44Z and restored mtimes are 02:44:00Z, so "complete no later than 02:44:44Z" is sound. Defect 7 of the verifier file (`:150`) matches.

## Item 3 — SCORECARD owned-axes rows vs recipe A at `c369242f`: **HOLDS**

Command: recipe A (`python3` over `git show` at `c369242fee9f559f895e3f7956b1242076c7b1be`, read-only) output:
```
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 116, "mapped": 116, "missing": [], "revision": "c369242fee9f559f895e3f7956b1242076c7b1be", "rule_blocks": 17}
```
Row claims match exactly: coverage row "116/116 knowledge files mapped at `c369242f` … (recount, round 31 …)" → 10.0; depth row "17/17 queue-drain rule blocks have resolvable file/range citations at `c369242f` …" → 10.0. The rows' own qualifiers (coverge "index integrity only, **not** fraction of the REA domain held"; depth "**not** semantic correctness …") are consistent with what recipe A measures.

Observation: `git diff c369242f 1288285e -- SCORECARD.md` = 29 insertions (new round-31 section) and 2 deletions — the two owned-axes rows were replaced (not appended) with the refreshed `c369242f`-measured text. That replacement is the sanctioned fix for defect 5 ("refresh or annotate the stale owned-axes rows"), and the replacement content verifies against recipe A at `c369242f` as above.

## Item 4 — `c1-fresh-naming.py` docstring-only change (defect 8): **HOLDS**

- `git log --format='%h …' --follow tools/round-29/c1-fresh-naming.py` → `0007731e` (round-31 entries), `dbd87cfa` (freeze), `87d3dfb6` (round-28). Only `0007731e` changed the file after the freeze.
- `git diff c369242f 1288285e -- tools/round-29/c1-fresh-naming.py` → exactly 2 lines changed, both inside the module docstring (current lines 14 and 27): `corpus/evidence/round-28/c1` → `corpus/evidence/round-29/c1` in the `runs_ok` and `tally_equal` definitions. Docstring spans line 2 to line 40; both changed lines are within it. No other line touched.
- AST equality: `ast.parse` of freeze bytes (`dbd87cfa`) vs tip bytes; both have a module docstring, and `ast.dump` with the module docstring stripped is identical (`True`).
- Hashes: freeze `dbd87cfa` = `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` (= `sha256_old`); `0007731e` and tip = `eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b` (= `sha256`).
- Evidence file cited by the supersession, `ExecR29Docstring.md`, exists.

## Item 5 — `claims.json` supersession (appended): **HOLDS**

- `git diff dbd87cfa 1288285e -- .ufo/waves/round-29/claims.json` is purely additive: hunk `@@ -65,5 +65,9 @@` adds 4 lines, 0 deletions (the round-30 M29-3 entry added at `004053d6` plus the round-31 entry). Base→tip (`c369242f`→`1288285e`) is 1 insertion, 0 deletions — the round-31 addition only.
- File at tip parses (`json.load`); `instrument_supersessions` has 2 entries. The round-31 entry (line 71): `{"path": "tools/round-29/c1-fresh-naming.py", "commit": "0007731eec3a00c19808e6d522dc4e91e07e71b3", "sha256_old": "6ad79d109…", "sha256": "eb685d236…", "round": "round-31", …}`.
- Commit field = `0007731e` = the only post-freeze commit that changed the file (item 4) ✓.
- `sha256_old` = freeze bytes; `sha256` = `0007731e`/tip bytes (item 4) ✓.
- `instruments` pin unchanged at line 14: `tools/round-29/c1-fresh-naming.py` still `6ad79d109…` (frozen bytes) ✓.

## Item 6 — pre-existing line preservation: **HOLDS** (with one observed replacement)

| File | base→tip diff | pre-existing lines |
|---|---|---|
| `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` | 2 insertions, 0 deletions | unaltered |
| `corpus/lessons/round-30.md` | 2 insertions, 0 deletions | unaltered |
| `.ufo/waves/round-29/claims.json` | 1 insertion, 0 deletions | unaltered |
| `tools/round-29/c1-fresh-naming.py` | 2 changed lines, both in module docstring | functional lines unaltered |
| `SCORECARD.md` | 29 insertions (new round-31 section), 2 deletions (the two owned-axes rows) | only the two axes rows replaced; replacement content verified in item 3 |

---

## Verdicts

| Item | Verdict |
|---|---|
| 1. knowledge-file pointer correction (defects 3/4) | holds |
| 2. lesson restore-time correction (defect 7) | holds |
| 3. SCORECARD owned-axes coverage/depth rows vs recipe A at `c369242f` | holds |
| 4. `c1-fresh-naming.py` docstring-only change (defect 8) | holds |
| 5. `claims.json` appended supersession (additions-only, commit field) | holds |
| 6. pre-existing lines unaltered | holds |

No finding fails any acceptance criterion; no counterexample.

## Residual risk / verification gaps

- **Observation (not a defect):** the SCORECARD owned-axes rows were *replaced*, not appended (2 deletions). The replacement text verifies against recipe A at `c369242f`; this is the defect-5 remedy. The rows' historical sub-claims (109/109 and 17/17 at `ebe2cb4a`, round 26) were not re-run against recipe A at `ebe2cb4a` (out of the requested check scope).
- The physical carrier restoration itself (wheel-member re-extraction, `chattr +i`) was not re-executed by this seat (lane bounds); the ≤02:44:44Z bound rests on the cited round-30 committed evidence (mtimes 02:44:00Z; first passing-pin run 02:44:44Z), all verified at the cited lines.
- `r-inflate-ratio`'s frozen pointer also carries a second range (`:73 RUST_INFLATE_RATIO`) not mentioned in the correction; the correction addresses the message location (`:139`) that was wrong, and the extra `:73` reference is unrelated to the string location. Not a defect in the correction.
- The supersession's `reason` cites `ExecR29Docstring.md`; it exists, and this seat independently reproduced the stated AST-equality result.
- No commands in this review modified any lane file; the only lane write is this report. Scratch artifacts (two git-extracted file versions) are listed below.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReviewR30R29Fixes/`)

| Artifact | SHA-256 | bytes |
|---|---|---|
| `r29_old.py` (`git show dbd87cfa:tools/round-29/c1-fresh-naming.py`) | `6ad79d1099730185bf867d98f6bb4f32c4a4a910bb346669fa2860b36993fdda` | – |
| `r29_new.py` (`git show 1288285e:tools/round-29/c1-fresh-naming.py`) | `eb685d236fdbfeba4ccb74922c447be14b5130879fc5ecd901c813adf9fae93b` | – |

No tools installed or updated (tooling directive: nothing needed). No process trees left running.

Report: `.ufo/waves/round-31/w2/ReviewR30R29Fixes.md`
