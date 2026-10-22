# ReopenS079: wave-2 falsify seat, kaidoku round 26

Seat KaidokuR26.ReopenS079 (leaf, no subagents). Target: SOURCES row S079 and its round-26 Gate line. Every source was opened 2026-10-22 (UTC).
Revision judged: HEAD `003de8cc` (checked 13:07Z). The row and Gate-line bytes are identical at landing `ebe2cb4a`, at `fe3eb4ed` (HEAD when the run began) and at `003de8cc`, and in the working tree. Between `fe3eb4ed` and `003de8cc` six corpus files changed, including the used-by knowledge entry (which still cites S079 twice); the S079 row, the Gate line and the SOURCES and lesson blobs did not change.
Lane edits: none; this report is the only file written. Installs or upgrades: none. REA calls: none (a static reopen needs none).

## Verdict
- Quote: **holds.** Both Gate quotes appear verbatim at their located lines in the installed 6.5.0 `dist/domain/evidence.js`. The second quote joins three physical lines (F5).
- Hashes: **holds.** All six sha256 values equal the SOURCES anchor and the Gate line. The installed package tree is byte-identical to the registry tarball (1650 files).
- Cells: **9 of 11 hold; 2 fail the literal CORPUS.md contract.** `source` has no canonical URL or DOI (F2). `used-by` omits the lesson that cites S079 (F1).
- Related: the search-log note that admitted S079 lacks the rule-5 counts (F3).
- Residual risk: F1 to F3 do not change the frozen R26-C1 counter result. Inference from the rule text: `entry_ok` reads only the Gate id, the `opened` cell and the `source:` line.

## Checks run (all read-only; exit codes are the shell's)
- C1 `sha256sum` on the six `dist/` files, exit 0, 12:59:33Z. All six match the anchor and the Gate line.
- C2 `python3 -I -B reopen_s079.py fe3eb4ed`, exit 0, 13:04:18Z: 73 checks, 71 pass, 2 fail (`S079-source-has-URL-or-DOI`, `S079-used-by-lists-every-citing-knowledge-or-lesson-file`). Re-run at `003de8cc`, exit 0, 13:07:27Z, same two failures. Exit 0 means the script ran; the verdicts are in its `failed` list.
- C3 `git show <rev>:corpus/SOURCES.md | awk '/^\| S079 \|/' | sha256sum`, exit 0. Row `9dd3ae9cf18cc2a57d2ac142748d79f1fe058ee3b6cb6964d6cad9b72a3eae98` at `ebe2cb4a`, at `fe3eb4ed` (earlier run, before 13:04Z), and at `003de8cc` and worktree (13:07:08Z). Gate line `991945ea20083a96eb4cc29972e020f719496ec4c56537eaf8395cbd477f4341` at the same four.
- C4 `bash scripts/sources-census.sh validate --today 2026-10-22 <lane>`, exit 0, 13:04:03Z (again 13:07:27Z, identical bytes). Output: five pre-existing W04 warnings (S033, S047, S054, S062, S069) and `ok`. Nothing for S079.
- C5 `curl -fsSL https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, exit 0, 13:05:01Z, 5,634,033 bytes. The sha512 integrity equals the string quoted in lesson line 28 for S080; the sha1 equals lesson line 29. I did not reopen the registry version document (S080's seat).
- C6 `diff -rq <tarball package> /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, exit 0, 13:05:06Z, no output; 1650 files each side.
- C7 `cmp` of rows S001 to S078 at `a0639d8e` and HEAD, exit 0, 13:05:00Z: identical (SOURCES blob unchanged through `003de8cc`). This supports the lesson claim that no older row changed (stronger: no older row text changed at all).

## Cell verdicts (row has 11 cells; NF=13; contract: CORPUS.md SOURCES contract v1)
| cell | value | verdict | basis |
|---|---|---|---|
| id | S079 | holds | `S` plus digits; one occurrence; follows S078 |
| source | "Installed `rea-agents@6.5.0` ... package root `/home/vgpnk/...`" | **fails** | no https or DOI; kind is code, not own-work; CORPUS.md:90 requires "canonical URL or DOI" |
| kind | code | holds | in enum |
| tier | A | holds | source code is an A kind for the 6.5.0 minting scope |
| scope | 6.5.0 minting and projection; excludes per-verb outcomes | holds | scoped |
| anchor | version 6.5.0; 23 line checks at cited endpoints and key lines; six sha256; opened 2026-10-22 | holds | all cited endpoints and key lines checked (C2) |
| teaches | `ev_` plus SHA-256 of canonical-JSON projection | holds | code-checked, see below |
| status | mined | holds | used-by path exists and cites S079 |
| opened | 2026-10-22 | holds | ISO; matches anchor and Gate header |
| recheck | on-release | holds | symbolic cadence allowed by the recheck rule |
| used-by | knowledge entry only | **fails** | `corpus/lessons/round-26.md` cites S079 at lines 21, 27, 35; CORPUS.md:107 covers "knowledge entries or lessons citing the row" |

Teaches check (observation, code): `evidence.js:182` mints `ev_` plus `digestCanonicalValue(semanticProjection(...))`; `canonicalDigest.js:9` is `createHash("sha256")` and `:63` sorts keys. The projection (`:156-180`) keeps only subject `digest`, `format` and `architecture` (`:160-162`), with no `path`, `local_path` or `name` token, and hashes `parameters` (`:168`), `raw_result` (`:169`), `normalized_result` (`:170`) and `locations` (`:178`). The normalizer spreads those fields to top level (`:266-313`). That a path inside them changes the id follows from hashing (inference; no runtime replay here).

## Findings (by severity)
F1, medium: `used-by` omits `corpus/lessons/round-26.md`.
- Evidence: C2 `"missing": ["corpus/lessons/round-26.md"]`. HEAD, 13:08:19Z, exit 0: `S079 used-by = corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` but `S080 used-by = ..., corpus/lessons/round-26.md`. Lane practice at HEAD `003de8cc`: 77 of 80 rows list a lesson path (awk, 13:10:15Z).
- Fix path: in-place change is allowed for `used-by` (CORPUS.md:116), logged old to new in the round lesson.

F2, medium: `source` has no canonical URL or DOI, and the census cannot catch it.
- Evidence: C2 `S079-source-has-URL-or-DOI` gives `"url": false, "doi": false, "kind": "code"`. C4 exits 0 with no S079 line. `scripts/sources-census.sh` lines 601-605 return "" when there is no https token, and line 629 `u=url_of(source)`, so the duplicate-URL checks skip the row (excerpt at 13:08:19Z).
- The Gate line has the same gap: no https token.
- Fix path (inference): `source` may not change in place (CORPUS.md:116). A correction would need a new row opening `supersedes S079 —`, or a disclosed contract decision. The tarball URL in C5 is a candidate canonical URL with a matching sha512. The wave-1 CensusCheck idea of a "local repo-path/command source" to skip the census checks is not a conformance route (CORPUS.md:90 allows a repo path or command only for own-work).

F3, low: the search-log note that admitted S079 lacks the rule-5 counts.
- Evidence: `git show HEAD:corpus/SOURCES.md | awk 'NR==149{print gsub(/identified|screened|excluded/,"&")}'`, exit 0, 13:08:19Z, prints `0`. Line 149 says "Rejected: none" with no sweep. CORPUS.md:127 requires "identified / screened / included / excluded counts, exclusion reasons".
- Wave-1 `SourceRowRegistry.md` line 26 drafted counts for S080 (identified 1, screened 1, included 1); they did not land.

F4, low: wave-1 `CounterC1.md` lines 188-190 say "the Gate row carries a URL and a quote". That holds for S080's Gate rows (lesson lines 28-31) but not for S079 (C2 finds no https token in S079's Gate line). Producing command: `awk 'NR>=188 && NR<=190' CounterC1.md`, exit 0, 13:06:57Z.

F5, low (content exact): the Gate quote "digest: evidence.subject.digest, format: evidence.subject.format, architecture: evidence.subject.architecture" is located at `:160-162`. Those lines end in commas; the quote drops the last comma and the indentation, and the Gate does not disclose the join. C2: `gate-quote2-verbatim-after-joining-160-162` ok; `info:gate-quote2-matches-one-physical-line` false.

F6, info: `on-release` is valid, but the census never judges symbolic cadences overdue (script header lines 36-37). `sha256sum` on the 6.7.0 root's `dist/domain/evidence.js`, exit 0, 13:08:19Z, gives `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`, not the 6.5.0 value. S079's facts therefore do not carry to 6.7.0; the row scopes itself to 6.5.0, which is correct.

## Verification gaps and limits
- Static check only. The teaches claim is confirmed by reading code, not by replaying an id. Per-verb verdicts belong to the C1 table and other seats.
- The "opened 2026-10-22" date is the author's claim. The bytes match, which fits the claim but does not prove the open date (unknown: no access log).
- The C1 counter does not read S079's quote, hash, used-by completeness or source form (wave-1 `C1Sizing.md` S16 and S17; `MutR25Coverage.md` N-M9 survived). Only this seat checked them.

## Sources (all opened 2026-10-22)
- Six installed files under `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/`, sha256: `domain/evidence.js` f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff; `domain/canonicalDigest.js` f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9; `application/DirectAnalysis.js` 09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617; `application/binaryDiagnostics/BinaryLayoutService.js` b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4; `domain/analysisView/analysisView.js` 2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363; `domain/analysisView/binaryLayoutView.js` 5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070. Quote, `evidence.js:182`: "const computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`;" (7 words).
  Other located quotes, one per file: `canonicalDigest.js:9` `const hash = createHash("sha256");`; `BinaryLayoutService.js:61` `parameters: input.data,`; `DirectAnalysis.js:72` `return createEvidence(value.subject ?? undefined, value.provider, {`; `analysisView.js:504` `const parentDigest = (evidenceId) => evidenceId.slice(3);`; `binaryLayoutView.js:73` `parent_digest: parent.evidenceId.slice(3),`.
- Registry tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz`, sha256 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699. Same quote as tar member `package/dist/domain/evidence.js:182`.
- `CORPUS.md` (fleet root), sha256 88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8. Line 90: "canonical URL or DOI (a repo path or command for `own-work`)." (11 words)
- `corpus/SOURCES.md`, sha256 945900936762151ad8544c8a0f66179d5c119aefe562e82a067b1085f6ae4657. Line 149: "Rejected: none. Stop: the minting rule and the package identity each have a located source" (15 words)
- `corpus/lessons/round-26.md`, sha256 28f55b8fd0238ffbc3dd36b88b6071e0f8fd6fb1152fc7619ac4f19f1a9af6d3. Line 21: "Sources opened on 2026-10-22. Each quote is contiguous and at most 25 words." (13 words)
- `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`, sha256 1ba5d5d909eecb2db638677388f9bcc0429b5263469905a936fc3c2a6185a941. Line 1: "S079 installed `rea-agents@6.5.0` Evidence-ID minting and projection source (opened 2026-10-22)" (10 words)
- `scripts/sources-census.sh` (fleet root), sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30. Lines 36-37: "symbolic cadences (e.g. on-release) are reported, never judged overdue." (9 words)
- Wave-1 reports read and attacked, sha256: `w1/CounterC1.md` e805d0238034815927f86d5be92723988b5925aab2f03bdc07e0bbb2828a76a7; `w1/CensusCheck.md` 1bbdb082961a8500d35a15a0f9f74f00ff73f11a32a2c7e5d04772245fdbcd1e (lines 90-91: "S079 can be a local repo-path/command source, which skips both checks" (11 words)); `w1/SourceRowEvidence.md` d9a6b8729e2b4320928a548b9447d4438557130401796ef0fabacc0bf3df38c8; `w1/SourceRowRegistry.md` 936c6c9a0fdf9a9651e0676359961cd907cfcc39b6ecc72a26450210fbc15810; `w1/C1Sizing.md` fd000c02675d6c883a97a9b41292bf9a8cf56c42162714928dcd16d15c98fad3.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReopenS079/`, sha256)
- `reopen_s079.py` da088c3f2287fd2720540d829117e809c9ac76043ccea4938d540070da9c25bd
- `reopen-output.json` (rev `fe3eb4ed`) 452e36484785a3fcb8ae48d5a981b34e5f11c6bf796f5de7759c5a86480bcbfd
- `reopen-output-003de8cc.json` 23ced01c841c54c75de1c684aa14c74f9a4a366db1bb8e62e3319f202777a889
- `census-validate.tsv` and `census-validate-003de8cc.tsv` b18181b1d67f9978948f9e08cf7be914ed0c14055e9eda66894fcc979ebbd07c (identical)
- `base78.txt` and `base-rows.txt` 60bfff94f54424fe9d0fe2edca6bc0f97aa69a307b06f0062530cc51e38f5935; `head-rows.txt` b1f6ed5a29b29f492c1f8c8e05cf6f37e14f6a1e4987c42e010f780c91e2dcfe
- `tree-diff.txt` and the empty stderr files e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- `registry/rea-agents-6.5.0.tgz` 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699; `registry/extract/` (1650 files, unpacked)

## Installs and bounds
No tool installed or upgraded; no pacman transaction; no lane file edited; no git write; no jj command; no subagent; no REA call.
