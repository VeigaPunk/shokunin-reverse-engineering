# XpinKeyless: round 27 wave 2 falsify report

Seat: KaidokuR27.XpinKeyless. Leaf seat, no delegation, no background jobs.
Run: 2026-10-22, 15:37Z to 15:43Z (UTC).
Lane tip attacked: 4084d8975b684a8837b1c858eea0008ce9ab49e0 (main; HEAD equals main).
Claim attacked: corpus/README.md line 211, the round-27 attribution limit (37 keyless records). The sentence is identical at main and in the working tree (checked 2026-10-22 15:46:19Z). The README file itself has uncommitted edits elsewhere; those were not examined.
Scratch (raw output, probe scripts, sandbox copies): /fast/scratch/hyaku/kaidoku-r27/seats/w2/XpinKeyless/

## Verdicts on the items attacked

1. "37 keyless records", counted as envelopes with data.evidence_id and no relationship_coverage key: holds (Checks 1, 2).
2. "Default mode reports both for all 37": holds, 37 of 37. The committed TSV reproduces byte for byte (Check 3).
3. "--parse separates them: 6.5.0 accepts all 37, 6.7.0 rejects all 37": holds (Checks 3, 5).
4. "All 37 such lane records" read as the full set of keyless records: fails under a recursive reading. There are 49 occurrences in 40 files; 12 are nested in three round-23 files the tool cannot read (Checks 2, 12; F1).
5. "A record without the key fits both id rules": holds literally for the stored bytes, but it is a digest artifact. 6.7.0 never mints such a record (Checks 6, 9, 13, 14; F2, F3).
6. "6.7.0 rejects because of the missing key": holds for all 37. Each has exactly one 6.7.0 issue, at relationship_coverage. Incomplete: adding the key alone does not pass 6.7.0 (Checks 5, 7, 8; F5).
7. "6.4.0-era" label: could-not-evaluate for 35 of 37 (Check 15; F7).

## Checks (command; excerpt; exit; UTC; verdict)

1. Python: git ls-tree, then git cat-file --batch over the 4087 committed .json files at main. Excerpt: "with relationship_coverage key: 204", "keyless (data.evidence_id, no relationship_coverage key): 37"; list sha256 f426c918..., the same sha256 the wave-1 report BuildXpinTool.md records for its keyless-main-list.txt. Exit 0; 15:37:41Z. Verdict: holds.
2. git --no-pager grep -l evidence_id main (2319 files), then a recursive JSON and JSON-lines scan. Excerpt: "records found (any file type): 254", "keyless record-occurrences: 49 | distinct files: 40", "only-old: []". Exit 0; 15:40:40Z. Verdict: the 37 are complete for envelopes, not for all records (F1).
3. node tools/round-27/xpin-attribute.mjs --pkg65 <6.5.0 root> --pkg67 <6.7.0 root> <37 paths>, run on committed bytes; then the same with --parse. Excerpt: "[default-committed] ... exit=0 stdout_lines=37 ... sha256=ccb42b03..."; "[parse-committed] ... exit=0 ... sha256=e44ba858..."; both files byte-identical to the main TSV blobs. Exit 0 both; 15:38:03Z. Verdict: holds.
4. Byte comparison of the 37 working-tree files with their main blobs. Excerpt: "working tree == committed for 37/37". Exit 0; 15:41:35Z. Verdict: holds (the tool reads the same bytes either way).
5. node issues.mjs (scratch probe): imports each pin's own parseEvidence and lists every zod issue with its path. Excerpt: "T1 rows: 37 | 6.5.0 accept: 37 | 6.7.0 reject: 37"; "37 (('invalid_type', 'relationship_coverage', 'Invalid input: expected object, received undefined'),)". Exit 0; 15:39:56Z. Verdict: holds; the rejection is the missing key.
6. diff -u of evidence.js, canonicalDigest.js, binaryTargetTypes.js and relationshipCoverage.js across the two packages. Excerpt: evidence.js has 4 hunks (default null removed; projection always includes the key; subject architecture exclusion; new import). canonicalDigest.js identical (sha256 f46d6bd4...). binaryTargetTypes.js adds m68k and hexagon, RAW_ONLY = [6502, m68k]. relationshipCoverage.js uses fixedTupleSchema in 6.7.0. Exit 1 for differing files, 0 for canonicalDigest.js; 15:38:56Z to 15:41:47Z. Verdict: the pins differ in more than the key (F6).
7. Sandbox A (sandbox/T2): ok-full.json with "relationship_coverage": null added, evidence_id unchanged. Tool default, then the probe. Excerpt: tool row "ok-full.json ev_2d55... ev_2d55... ev_0c17... 6.5.0"; 6.7.0 rejects with one issue, ('custom', 'evidence_id', 'Evidence semantic identifier does not match its record'). Exit 0; 15:39:46Z. Verdict: the key alone does not pass 6.7.0 (F5).
8. Sandbox B (sandbox/T3): sandbox A with evidence_id set to the 6.7.0 value (a test construction, not a real record). Excerpt: tool row attribution "6.7.0"; probe: 6.7.0 accept, 6.5.0 reject on evidence_id only. Exit 0; 15:39:46Z. Verdict: no other 6.7.0 schema problem in this record.
9. Sandbox C (all 37 with key null) and sandbox D (all 37 with key null plus 6.7.0 values). Excerpt: "[R default] attribution after adding rc null: {'6.5.0': 37}"; "[R3] 6.7.0 accept: 37 | 6.5.0 reject: 37 | ... Counter({(('custom', 'evidence_id'),): 37})". Exit 0; 15:41:35Z. Verdict: adding the key flips every record; no version of these records passes both pins with this construction.
10. Controls on committed bytes: tinyxxd-inspect-base.json (round-27 C1, key null) and .ufo/waves/arc3-loop1-round12/claims/c1/CR-2/evidence/base.json (key object). Excerpt: key null: 6.5.0 accept, 6.7.0 reject on evidence_id; key object: both accept. Exit 0; 15:39:56Z. Verdict: committed key-null envelopes fail 6.7.0 on identity; they are outside the 37.
11. Sandbox E (subject architecture m68k) and sandbox F (subject architecture hexagon). Excerpt: E under 6.7.0 lists subject.architecture and relationship_coverage (two issues); F under 6.5.0 rejects, under 6.7.0 accepts. Exit 0; 15:40:56Z. Verdict: zod lists every top-level issue, so one issue per record is complete; the pins disagree on subject architecture (F6).
12. node tools/round-27/xpin-attribute.mjs on the three nested-record files. Excerpt: "xpin-attribute: .ufo/waves/round-23/frozen/fixture.json: envelope has no \".data\" evidence record". Exit 2; 15:40:56Z. Verdict: nested records are outside the tool's population (F1).
13. Checker convention: tools/round-27/c2-xpin-check.py lines 94-100 applied to the 37, recompute module read from main. Excerpt: "attribution of the 37 keyless records: {'6.5.0': 37}"; "python id65 == stored for: 37 / 37"; "python id67 (null inserted) == JS tool id67 with rc null for: 37 / 37". Exit 0; 15:42:30Z. Verdict: checker and tool disagree on the 37 (F3).
14. Read only: 6.7.0 evidence.js lines 235-241 and 298-300. Excerpt: "...(observation.relationshipCoverage === undefined ? { relationship_coverage: null } : ...)"; createEvidence hashes the normalized record. Exit not applicable; 15:42:54Z. Verdict: 6.7.0 never mints an id for a record without the key (F2).
15. Read of ok-full.json meta; git --no-pager grep -n -e '6\.4\.0' main over the wave folders and lane docs (output cut by head; exit 141 is SIGPIPE from head, not a git failure). Excerpt: meta {"command":"inspect-evm-interface","duration":"102ms"}; EX-05/README.md line 45 ties rv2.640.raw.json and line 46 ties recon.640.json to rea-agents@6.4.0. Exit 141 on the search; 15:41:47Z. Verdict: could-not-evaluate for the other 35 of 37 (F7).

## Findings

F1 medium, scope wording. "37 such lane records" counts top-level envelopes; the wave-1 filter (37 files) matches that. A recursive scan finds 49 keyless occurrences in 40 files: 37 envelopes plus 12 nested records (fixture.json holds 6 under documents; each metadata-red-green.json holds 3 under comparisons[].envelope). Fix: say "37 envelopes", or list the 12 and say why they are excluded.
F2 medium, "fits both id rules" is a digest artifact. canonicalDigest skips keys whose value is undefined (canonicalDigest.js lines 63-66, identical in both pins). 6.5.0 drops a null key from its projection (evidence.js lines 175-177); 6.7.0 keeps it (line 178). 6.7.0 always writes the key (Check 14). So "both" describes a form 6.7.0 rejects. Adding the key moves all 37 to "6.5.0" (Check 9). Reword.
F3 medium, two instruments, two answers. c2-xpin-check.py lines 97-98 set the key to null when absent. Its id67 matches the tool's (37 of 37, Check 13), but its attribution for the 37 is "6.5.0" where the tool says "both". The checker's inputs are 24 round-26 envelopes and generated red envelopes, none of the 37, so no reported result is wrong. The convention is undocumented, and keyless input passes silently.
F4 low, --parse hides the field. xpin-attribute.mjs lines 226-229 print only issues[0].message, so keyless-parse.tsv does not name relationship_coverage. The path appears only in the probe (Check 5).
F5 low, the rejection has two steps. Missing key first (Check 5). With the key present, the identity check fails (Check 7). Only a re-minted identity passes (Check 8), and then 6.5.0 rejects the record (Check 9). "Rejects because the key is missing" is true but incomplete.
F6 info, pin differences the 37 do not exercise. Subject architecture: 6.7.0 adds m68k and hexagon and excludes 6502 and m68k; 6.5.0 excludes only 6502 (Check 11). relationshipCoverage: 6.7.0 uses fixedTupleSchema; no keyed object appears among the 37.
F7 info, "6.4.0-era" has no record-level evidence. EX-05/README.md ties two of the 37 (recon.640.json, rv2.640.raw.json) to rea-agents@6.4.0 (Check 15). The other 35 are not tied.

## Answer to the assignment question

6.7.0's rejection of the 37 is the missing key: each has one issue, at relationship_coverage, and no other 6.7.0 problem appears (Checks 5, 8). The key cannot be added alone, because the 6.7.0 identifier hashes the key. Key and identifier must change together (Check 9), and 6.5.0 then rejects the record.

## Residual risk and gaps

- No REA CLI, REA verb or MCP call was made. Probes import each pin's parseEvidence in-process with node, read only.
- Sandbox B and D set evidence_id by hand; these are test constructions, not real records.
- No lsp device is in this seat's tool list. Caller and definition checks were read by hand plus text search. Text search is not semantic proof.
- Provenance of the other 35 records is unchecked.
- Unparsed scan: 22 .py and 1 .md file mention evidence_id and data; none is a JSON record.

## Tooling and bounds

No installs, updates or upgrades. Host node v24.21.0 used as found; no pacman, npm, npx install or uv call. Both REA package roots were read only (package.json versions 6.5.0 and 6.7.0 confirmed).
Lane files untouched. This report is the only lane write. No git writes, no jj, no subagents, no messages.

## Artifacts (scratch, sha256)

issues.mjs 6810263bc84ed8c7bb0155550174337e5a472ea4dacf66ac5344d1b26e9a1ce0
tool/xpin-attribute.mjs (from main) 8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708
default-committed.out ccb42b03f6b9e6024d6b102c7d3e7939b05fc19e38664e857e62f29001df8ec0
parse-committed.out e44ba85836c57b9a04aac6cd2d683d10fb2e15fc2972c5555dafa380b7b9104f
keyless-committed-list.txt f426c918b323207b35511319bcc737bb4a4c5f0f538851b9e794e6bdba334930
keyless-committed-all-filetypes.txt 758f341e2a58dfea46cb51653d4ef934039e12f5f1e83cd246c7dd5b34a41da5
committed-json-with-data-evidence_id.tsv cc1edb0c295fac9749f96d1c6b9a29b8143aa0366e18834d504325869cec4b67
issues-T1-committed37.json 4bedf4b1e3395ef036caa5dcacf5cb26bbf93acc0cc044312da7812bbad25d66
issues-sandbox-controls.json e5188f29165bbf0a09908c22913af7234a2889865416fe615185a1bea85ba6a7
issues-T4-T5.json 661569ebbad97d2daf18351fd9c2648b12768c8502aee1b92866a4b594c2d376
issues-R3-37.json 0e8323b1d076185d19ca18b448d090b4d0aed885614a71e639821c8f8d31c8ed
R-rc-null-default.out 88b6dde9297fb2bb1a9531626578b51cd7f50461879a7ccbdccc6a69dfd79954
sandbox/T2/ok-full.json c4c69c769094255b209f6aed0bb6f158291c33d25c4efa171742b5458678b096
sandbox/T3/ok-full.json 0bbc83ed70543936f3f252f69151ab51cabe023abd0f332e79fdff98e54d4bd7
checker-convention-keyless.tsv f66ad70e7aa3c2f38df80116bc064ee243457b32ad5063016d5ba753122620eb
diff-evidence-6.5.0-to-6.7.0.diff 5d216acf4fb591e1181d5489a8432a584f0589381e3780961989cc9d63d1e666
diff-relationshipCoverage-6.5.0-to-6.7.0.diff 734af174e9ca77ec03600ddfaf429ed4b268ed5ab452a6cb73d5c77dd862499b
diff-canonicalDigest-6.5.0-to-6.7.0.diff (empty; files identical) e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
