# Round 27 — renamed-copy and second-carrier evidence-ID identity; cross-pin attribution tool

Author: kaidoku L1, round 27, attempt 1 (in-session hyaku lane subagent). Lane-round base
`cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`. Claims, both counters, their red selftests and the
before receipts were frozen together at `a4f674b343d8564e21f7eb8984630a95089c82d6`
(`.ufo/waves/round-27/claims.json`), before any data they count.

## Claims

- R27-C1, depth (learning claim): a 16-row evidence-ID identity table (8 verbs on `/usr/bin/jq`
  and `/usr/bin/tinyxxd`; base, same-path repeat and a copy with another directory, file name and
  extension) at `rea-agents@6.5.0`, and entry
  `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`. Before 0 of 16, entry 0.
- R27-C2, operability (capability acquisition): `tools/round-27/xpin-attribute.mjs` attributes a
  saved envelope to the 6.5.0 rule, the 6.7.0 rule, both or neither, with each installed
  package's own code; checker `tools/round-27/c2-xpin-check.py`. Before 0/24, 0/3, rows 0.
- Not claimed: calibration. The 11 stale SCORECARD statements are corrected as hygiene.

## Gate

Sources opened on 2026-10-22. Each quote is contiguous and at most 25 words. S081 and S082 are
new rows. S079 (installed 6.5.0 package) was re-opened for one more file of the same package.

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js`; opened 2026-10-22 | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | `relationship_coverage: evidence.relationship_coverage,` | `dist/domain/evidence.js:178` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js`; opened 2026-10-22 | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;` | `dist/domain/evidence.js:183` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js`; opened 2026-10-22 | `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` | `export const digestCanonicalValue = (value, context = "Comparison") => {` | `dist/domain/canonicalDigest.js:8` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json`; opened 2026-10-22 | `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570` | `"version": "6.7.0",` | `package.json:4` |
| S081 | npm registry tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz`, member `package/dist/domain/evidence.js` unpacked under the seat directory; opened 2026-10-22 | tarball `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90` (sha1 `11f23ba377303a5c28b3162180cf2bf3f3643708`) | `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;` | `package/dist/domain/evidence.js:183` |
| S082 | local pacman desc `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc`; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "Alexander F. Rødseth <xyproto@archlinux.org>" | `%PACKAGER%` |
| S082 | same desc file; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "1790704346" | `%BUILDDATE%` |
| S082 | same desc file; opened 2026-10-22 | a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456 | "https://github.com/xyproto/tinyxxd" | `%URL%` |
| S082 | local pacman mtree `/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree`, gzip; opened 2026-10-22 | compressed a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58; decompressed cd9ad639309eccbeadcaa05425a64b19b54c9802feb58cba61a2f80efe2cd36b | "./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65" | mtree entry for `./usr/bin/tinyxxd` |
| S082 | pacman sync database `/var/lib/pacman/sync/extra.db`, member `tinyxxd-1.3.17-1/desc`; opened 2026-10-22 | database file 0b07b40310883996d6313f0980e841757a4832eb1ef0c8785477f5875a95fd63; member bytes a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941 | "3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce" | `%SHA256SUM%` |
| S082 | https://archlinux.org/packages/extra/x86_64/tinyxxd/ ; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Build Date: 2026-09-29 17:52 UTC" | `Build Date` |
| S082 | same package page; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Last Packager: Alexander Rødseth" | `Last Packager` |
| S082 | same package page; opened 2026-10-22 | 4e5fff126b0d2092999add67cc30413bbfb3a95ea60970578162a5e6494b7d89 | "Upstream URL: https://github.com/xyproto/tinyxxd" | `Upstream URL` |
| S082 | https://archlinux.org/packages/extra/x86_64/tinyxxd/json/ ; opened 2026-10-22 | 30e4c4102da6f6e485b18dbc6d25c14ba1a80e5224306c60bc6f7158463162fb | "\"build_date\":\"2026-09-29T17:52:26Z\"" | `build_date` |
| S079 | Installed `rea-agents@6.5.0` package source — `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/ghidra/GhidraTargetSnapshot.js`; re-opened 2026-10-22 | `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b` | `const snapshotPath = join(runtimeRoot, `target-${expectedSha256.slice(0, 12)}${suffix}`);` | `dist/ghidra/GhidraTargetSnapshot.js:14` |
| S079 | same file; re-opened 2026-10-22 | `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b` | `return /^\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : ".bin";` | `dist/ghidra/GhidraTargetSnapshot.js:78` |
| S083 | Installed `rea-agents@6.5.0` bundled runtime `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/binary-BVOr2mgE.js`; opened 2026-10-22 (after wave 2) | `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df` | `return /^\.[A-Za-z0-9]{1,12}$/u.test(extension) ? extension : ".bin";` | `dist/cli-runtime/binary-BVOr2mgE.js:5318` |
| S083 | same file; opened 2026-10-22 | `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df` | `targetPath = await realpath(input.targetPath);` | `dist/cli-runtime/binary-BVOr2mgE.js:293` |
| S083 | Installed 6.5.0 `bridge/ghidra/ReaGhidraBridge.java`; opened 2026-10-22 | `db16aed4d16ab94da883843281ef7a8a33a244cd8379bd4013e8dee479c0a105` | `result.add(currentProgram.getName());` | `bridge/ghidra/ReaGhidraBridge.java:1975` |

Search: which installed code decides the 6.7.0 evidence-ID projection, which package record
ties the second carrier's bytes to a named package, and which 6.5.0 code puts the file extension
into hashed output. Identified 6 candidate sources (6.7.0 installed tree, 6.7.0 tarball, 6.7.0
version document, tinyxxd local and sync pacman records, Arch package page and JSON, 6.5.0
`GhidraTargetSnapshot.js`); screened 6; included 3 as rows or row re-opens (S081 covering the
installed 6.7.0 tree and its byte-identical tarball, S082 covering the pacman and Arch records,
S079 re-opened); excluded 1 (the 6.7.0 version document, already row S037's dataset family).
Rejected: none.

Decision reversed from round 26, as QUALITY row 36 asks: the round-26 Gate declined a row for the
installed 6.7.0 code because it "is already row S037's family" (`corpus/lessons/round-26.md:37`).
The round-26 spot-check disagreed (`corpus/lessons/round-26-verifier-spotcheck.md:165`, routed
defect 1 at `:197`): S037 is the 6.7.0 registry record and its scope excludes runtime behaviour.
S081 is the code row, the 6.7.0 analogue of S079.

Row changes (old → new): S081 absent → added (status `mined`, used-by
`tools/round-27/xpin-attribute.mjs, corpus/lessons/round-27.md`); S082 absent → added (status
`mined`, used-by the round-27 entry and this lesson). S079 cells unchanged; its re-open is logged
here and the round-27 entry cites it.

## Mistakes

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M27-1 | counting instrument committed after its data despite the freeze promise | `corpus/lessons/round-26-verifier-spotcheck.md:201-204`; `.ufo/waves/round-26/w2/RerunC1Counter.md:55-61` | partial: `corpus/claim-freezes.tsv:14` flags INSTRUMENT_ABSENT, but M26-1..M26-7 do not mine this ordering failure | Round 27 freezes both counters, red selftests and before receipts together at `a4f674b343d8564e21f7eb8984630a95089c82d6`. `tools/round-27/c1-rename-identity.py:244-258` refuses older run starts and envelope first commits; the frozen red receipt is `.ufo/waves/round-27/before/c1-selftest.txt:5`. Running `/fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/probe.py` on an unchanged real round-26 analyze envelope and its recorded start produces exit 1 and `base: utc_start 2026-10-22T12:11:51Z not after counter commit`; changing only that timestamp removes that reason. Both partial-population runs still exit 1, so this demonstrates the ordering gate, not a complete green claim. |
| M27-2 | a forgery gate frozen without a green edge case: the R27-C1 counter refuses any envelope sha256 shared by two runs, and two genuine runs returned byte-identical envelopes | `corpus/evidence/round-27/c1/runs.tsv` (tinyxxd `inspect-binary-layout` base 14:55:49Z and repeat 14:55:50Z, both `envelope_sha256` `f601872b…3130`, both `meta.duration` `132ms`); counter output at `9dca26df135a2c558aaa575534ad42662b372d5d`: `INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run`; seat report `.ufo/waves/round-27/w1/RunTxD.md`; the same coincidence was seen for jq the same day (`.ufo/waves/round-27/w1/FreshnessR26.md`: today's layout envelope equals the round-26 repeat envelope) | none: QUALITY rows 32 and 36 ask for red cases, no rule asks a forgery gate to show it accepts a legitimate duplicate | Not repaired in round 27: the counter is frozen and the row stays incomplete (R27-C1 measures 15 of 16). For a later counter: tell duplicate bytes apart by the call record (distinct `utc_start`, seat, stderr file) and add a green selftest case of two byte-identical genuine runs. Shown able to fail on real bytes: the frozen counter refuses this committed row |

## Falsify-wave findings kept as disclosures (wave 1)

- R27-C1 counter: it reads only the first `source:` line (`.ufo/waves/round-27/w1/MutC1Entry.md`,
  `ReviewC1Counter.md` F3); it never compares the table's row set with the 16 frozen pairs, so an
  extra 17th row is invisible, and it never reads `utc_end` (`MutC1Verdict.md` m05, m10); it checks
  `subject.name` only when present and accepts the subject sha256 from
  `normalized_result.artifact.sha256` (`ReviewC1Counter.md` F1, F2); it loads
  `tools/round-26/recompute-ids.py` from the measured revision without a pin, so a weakened
  recompute file lets a forged id pass (`SiblingOverlap.md`, `CriticFreeze.md`). Receipt: that file
  is byte-identical (`89afa375…208b`) at the base and the data commit (`git diff --exit-code`).
- `utc_start`, `pkg_version` and `pkg_json_sha256` are labels written by the seat; no committed
  byte shows when a run really happened or which package really ran it (`MutC1Time.md`). The
  pre-freeze probe envelope is now committed at `.ufo/waves/round-27/pre-freeze-probe/` and its
  sha256 `93660137…5cc0` appears in no `runs.tsv` line.
- R27-C2 checker: the tool's exit code is printed but not counted; a tool with a retyped
  projection passes; for records that lack the `relationship_coverage` key its 6.7.0 rule inserts
  `null` where the 6.7.0 code drops the key, so it would disagree with a correct tool on 6.4.0
  records (none is among the 24 counted) (`ReviewC2Checker.md` F1-F3, `CriticNovelty.md`).
- Claim width: "At rea-agents@6.5.0" rests on the invocation and the per-call `package.json`
  read; a 6.7.0 `function` envelope would fit the 6.5.0 rule too, because the two rules agree
  whenever `relationship_coverage` is set (`CriticClaimWidth.md`).

## Corrections after the falsify wave (wave 2, `.ufo/waves/round-27/w2/`)

- Claim outcome: R27-C1 missed (15 of 16 rows, `entry_ok` 1, exit 1 at `97358f75`); R27-C2 met (24/24, 3/3, rows 1 and 1, exit 0 at `97358f75` and at the tip `4084d897`). Re-derived by seats `RecountC1`, `RederiveC1Own` and `RecountC2`.
- Gate, S082: the Arch JSON quote is `"build_date": "2026-09-29T17:52:26Z"` in the served bytes (one space after the colon; the line above dropped it). The three Arch page quotes ("Build Date: …", "Last Packager: …", "Upstream URL: …") are rendered-text composites of a table label cell and its value cell, not contiguous byte strings, and the page sha256 `4e5fff12…` does not reproduce because the page carries a per-request CSP nonce. The S082 anchor cell repeats the composed Build Date string and is read the same way. The local `desc`, `mtree` and sync-database lines reproduce byte for byte (`ReopenS082.md`).
- Gate, S081: all five quotes and hashes reproduce; the anchor range `canonicalDigest.js:8-25` omits the closing line 26 (`ReopenS081.md`).
- Falsify-wave note on the "six `both` rows": they are the `function` verb, operation `analyze_function` (`XpinOnR27Envelopes.md`).
- Live checks added in wave 2: a name-only copy kept the `analyze` id and an extension-only copy changed it (`FalsifyExtensionOnly.md`); a 13-character extension mapped to `.bin` (`FalsifySuffixMapping.md`).
- Dead seats: six wave-2 mutation-tester seats died at spawn with "Error: No model selected." and were not replaced, so QUALITY rows 38-40 and the M27 fixes got no wave-2 mutation test this round; their "shown able to fail" evidence is the real-byte runs cited in each row.

- Sources after wave 2 (`ReopenS079Snapshot.md`): re-opening S079 for a file outside its listed set was handled as a Gate note; under the SOURCES contract only `status`, `recheck` and `used-by` change in place, so the file now has its own row S083 (with the bundled runtime the CLI actually runs and the bridge line that makes the snapshot name the `document`), and the two S079 Gate lines above are read as S083 evidence. Row changes (old → new): S083 absent → added (status `mined`); S079 `used-by` `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md, corpus/lessons/round-26.md` → that value plus `corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md, corpus/lessons/round-27.md`.
- Freeze row wording (`ReviewFreezeRow.md`): the `round-27` ledger row says the red selftests and before receipts were sha256-pinned at the freeze; they were committed in the freeze commit, but `claims.json` pins only the two counters. `tools/round-27/assemble-c1.py` (added at `9dca26df`, after the freeze) wrote `runs.tsv` and `table.tsv` and is named in no claim; the pinned counter re-derives every table verdict from the envelopes.
- Search-log counts corrected (`ReviewGate.md`): of the 6 candidates identified and screened, 5 were included in 3 rows (S081: installed 6.7.0 tree and its tarball; S082: pacman records and Arch page with JSON; the snapshot file, first logged as an S079 re-open, now S083 after wave 2) and 1 was excluded (the 6.7.0 version document, S037's family). Stop rationale: each claim's mechanism and carrier identity then rested on a primary code or package record, so no further family was needed. The consumer-code search for that exclusion (`grep -rn "relationship_coverage"` over the 6.7.0 `dist/`, 74 hits in 25 files) is recorded in the S081 search-log note of `corpus/SOURCES.md`.
