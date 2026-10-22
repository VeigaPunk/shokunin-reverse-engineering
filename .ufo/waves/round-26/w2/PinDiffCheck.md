# R26 wave 2 — PinDiffCheck: entry section "Pin dependence"

Seat: KaidokuR26.PinDiffCheck (leaf, read-only lane). All times UTC, 2026-10-22.
Judged bytes: lane HEAD 003de8cc38a86a914c0348ded674091d47d71fc1 (13:07:21Z, `git rev-parse HEAD`). Entry blob 68519852d98ce78caf49a745e538f6869606584d, sha256 1ba5d5d909eecb2db638677388f9bcc0429b5263469905a936fc3c2a6185a941; `git hash-object` on the working copy matched the HEAD blob, so the working copy equals the judged commit.
Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/PinDiffCheck/ (scripts/, out/, tmp/). No tool installed or upgraded: node v24.21.0, Python 3.14.8 and the rea-agents 6.5.0 and 6.7.0 npx caches were already present. No external sources used.
Package roots (read-only): 6.5.0 at ad9a3fdbcad992c6 (package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c); 6.7.0 at a1722018f28f9df2 (sha256 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570). `npx -y rea-agents@6.5.0 --version` printed 6.5.0 and `@6.7.0 --version` printed 6.7.0 (exit 0, 13:05Z).

## Verdicts

- S1, relationship_coverage difference: HOLDS (observed). Two corrections below.
- S2, function profile "parameter names" change: HOLDS for values, WRONG for names (observed). The keys are identical.
- S3, stored 6.7.0 arc3 envelopes recompute only under the 6.7.0 rule: FAILS as worded (observed). 133 of 145 hold; 12 recompute under both rules.
- S4, live pairs quoted in the section: HOLDS (observed, four live calls, all exit 0, ids identical to the entry).

## S1 relationship_coverage

- `diff -u <6.5.0>/dist/domain/evidence.js <6.7.0>/dist/domain/evidence.js` exit 1 at 13:00:34Z, 43 lines. The only hashed-projection hunk: 6.5.0 lines 175-177, `...(evidence.relationship_coverage === null ? {} : { relationship_coverage: evidence.relationship_coverage })`, become 6.7.0 line 178, `relationship_coverage: evidence.relationship_coverage,`.
- Schema hunk, not hashed: 6.5.0 line 113 `.nullable().default(null)`; 6.7.0 line 116 `.nullable()`.
- Live pair `npx -y rea-agents@6.5.0 inspect-binary-layout /usr/bin/jq --format json --full-output`: exit 0 at 13:04:36Z, id ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd. The same call at 6.7.0: exit 0 at 13:04:41Z, id ev_d1256a9649ddcb43a9251b202eb4dafb049ab50c11f92f907915899fa3d4cb2a. `jq -S 'del(.meta)' | diff` exit 1, one differing line (evidence_id). Both carry `relationship_coverage: null`.
- Package-native check (`node scripts/native-parse.mjs <root> <list>`, exit 0 for each package): for `inspect-binary-layout`, each package's parseEvidence accepts its own live record and rejects the other pin's record with "Evidence semantic identifier does not match its record".

Corrections: the 6.5.0 omission is at lines 175-177 and the 6.7.0 emission at line 178, not "175-178 in each package". "Always emits" should read "emits whenever the key is present". Missing from the entry: 6.7.0 removed the schema default, so its parser rejects a record without the key (19 records, "relationship_coverage: Invalid input: expected object, received undefined"); 6.5.0 accepts them (observed).

## S2 function profile

- Source, 6.5.0 `dist/ghidra/GhidraAnalysisProfile.js` lines 141-142 (executable branch): `instruction_references: "exact-address-incoming-v1"`, `function_boundary_observations: "ghidra-function-boundary-limitations-v3"`. 6.7.0 lines 155-156 use constants at lines 13-14: `"ghidra-function-boundary-limitations-v4"` and `"exact-address-incoming-without-synthetic-entry-v2"`. Unchanged: `call_relationship_coverage` "function-body-call-coverage-v5" (line 12 in both).
- Live `npx -y rea-agents@<pin> function /usr/bin/jq 0x103fa0 --format json --full-output`: 6.5.0 exit 0 at 13:04:55Z, id ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5; 6.7.0 exit 0 at 13:05:04Z, id ev_177586c695241d1e2552be2ca7def13c291756b00ae13c226875c6c615915be8. Both coverage status "complete".
- `jq -r 'keys[]'` on both analysis_profile.parameters: identical 25 keys (diff exit 0). `diff` of the sorted values: exit 1, two changed values, the two named above (observed). Live profiles equal the wave-1 stored profiles.
- Native check: both packages accept both function records (4 of 4 ok). So for `function` the id difference comes from profile values, and the projection rule is inert because coverage is non-null (inference from this measurement).
- Bundled CLI copies also show DOS-MZ `load_image_evidence` moving from `independent-mz-mapping-relocations-v1` to `-v2` (grep, not exercised on jq).
- Wording fix: replace "changed analysis_profile.parameters names" with "changed two analysis_profile.parameters values (version identifiers); keys unchanged".

## S3 stored 6.7.0 arc3 envelopes

Population: 164 JSON files in rounds 7, 10, 11, 12 hold a top-level or `.data` Evidence id (`out/arc3-envelope-candidates.txt`). Non-envelope tables (dispatch-census.json, id-recompute*.json) and text logs were excluded after shape checks.
Pin attribution (inference from call records): rounds 10, 11 and 12 mention only rea-agents 6.7.0 (census `grep -rhoE` at 13:05:49Z: no 6.4.0 or 6.5.0 text). Round 7 mentions 6.4.0 and 6.7.0. Envelopes carry no pin.
Tests: `node scripts/native-parse.mjs` for each package (exit 0 at 13:02:42Z) and `python3 -I -B scripts/rules.py` (both rules, copy of the lane tool, exit 0, same time).

| group (6.7.0 by attribution) | n | 6.7.0 rule / native 6.7.0 | 6.5.0 rule / native 6.5.0 |
|---|---|---|---|
| r7 null coverage | 20 | match / ok | no / id-mismatch |
| r10 null coverage | 32 | match / ok | no / id-mismatch |
| r11 null coverage | 25 | match / ok | no / id-mismatch |
| r12 null coverage | 56 | match / ok | no / id-mismatch |
| r12 analyze_function, non-null coverage (CR-2 3, EX-1 6 incl. rerun, EX-7 3) | 12 | match / ok | match / ok |

Excerpts: `non-null n=12 native650=Counter({'ok': 12}) native670=Counter({'ok': 12})`; `null n=133 native650=Counter({'id-mismatch': 133}) native670=Counter({'ok': 133})`. Joined categories: `6.5.0-rule+6.7.0-rule: 31`, `6.7.0-rule: 133`, none 6.5.0-only (`scripts/join.py`, exit 0, 13:03:00Z).

Reading (observed):
- Recomputes under the 6.7.0 rule: 145 of 145.
- Never under the 6.5.0 rule: 133 of 133 null-coverage records. Fails for the 12 round-12 analyze_function records, which recompute under both rules, because the two rules differ only when coverage is null. Their 6.7.0 pin still matters through profile content (inference, from S2).
- Round 7 has 19 more records with the key absent: 16 attributed to 6.4.0 (in-directory 6.4.0 mentions or 64- names: CR-1 2, CR-2 6, EX-4 6, EX-3 2); 3 in CN-1/evidence/vyper with no stated pin (unknown). Native 6.5.0 accepts all 19; native 6.7.0 rejects all 19 at schema. The mirror gives 19 of 19 under the 6.7.0 rule only if absent keys are dropped; with null inserted it gives 0 of 19 (`scripts/absent-null.py`, exit 0, 13:07:53Z). So wave-1's claim that the 6.7.0 rule misses the 64- pair holds only under null insertion. These 19 are not 6.7.0 products (inference).

Proposed wording: "Stored 6.7.0 arc3 envelopes from rounds 7, 10, 11 and 12 (145 records) recompute under the 6.7.0 rule. The 133 with null relationship_coverage never recompute under the 6.5.0 rule. The 12 round-12 analyze_function records with non-null coverage recompute under both rules."

## Residual risk and gaps

- The 145 pins rest on round-tree mentions and file names, since envelopes carry no pin. The round-7 subset of 20 rests on in-directory mentions.
- CN-1 vyper pin unresolved (3 records, key absent).
- No arc3 REA calls were re-run. S3 is offline over stored bytes plus each package's own parser. The 6.7.0 treatment of absent keys is a mirror assumption the native parser cannot reach.
- No 6.4.0 package on host; nothing about 6.4.0 was measured here.
- My four live calls are single runs, as the entry says of its own 6.7.0 calls. The same-path and copy relations at 6.7.0 were not measured and remain inference.
- RAW_ONLY_ARCHITECTURES (6.7.0 `binaryTargetTypes.js` line 18) changes the subject schema, not the hash; not tested.

## Artifacts (sha256)

- scripts/native-parse.mjs d10790f1bbb814836439e46095c7c4beeac46b1bb908a1ada121755977e49f94
- scripts/rules.py 33b29a6054a0ccca68feab22d280af6aee072a6e27935059a109ac3f9e3e3f42
- scripts/join.py 8bbaac1dd9e7ab527baa5770f29a1a8cdb8cbc2dbf2a99856d4af16f9f2a2726
- scripts/absent-null.py 2f2d0864f4bfd0772a4a5760e462d4d90103bfd5c1f973eb70355e96939ba269
- scripts/recompute-ids-copy.py 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b (equals lane tools/round-26/recompute-ids.py at HEAD)
- out/native-650.tsv 32ac3780a30e17284313dce5db7b620730d5abe27de75f5a0830a7f5ebd8ea61; out/native-670.tsv 4d9b528f5ff3ce9deca16c320186ac50e347293138a513f7b9fe2002c7f37ffb
- out/rules.tsv c15a92f9a5688e499f21762b7886e0b2079755a9877819d31daa68f59dfb9a3f; out/joined.tsv d58c8aba5047a799444f79719f2683ef5cf5c6cc4a8295de4a4c79a788777f43
- out/arc3-candidates-abs.txt 1755ce34383c532b2606f93d240a9006cc3ef2a1be072cc2e24bf17772116651
- out/evidence-js.diff 5d216acf4fb591e1181d5489a8432a584f0589381e3780961989cc9d63d1e666
- out/live-layout-650.json cdf9e0ccde1bffa3cb887cc8cf0ec21a246722682c650a17240edfeb6c2a6d03; out/live-layout-670.json 7acf4e3e6c440a56e51ce8b0ed7ce809ca7d83423ced44ff729829c2a1ec6d63
- out/live-function-650.json 1b91c57991f8ebcade068361a022d8503702d1ee6cecc9fecc0c486240f89be6; out/live-function-670.json dce49013ba265162e7f73c4e652668f0932ff0fac94fc54ceb6eea0bdabf7aaa
- out/fn-profile-650.json e7861d67d1f4eff698ec237dcc0660a9a31bdffbd01071c9453c8921b191fdf5; out/fn-profile-670.json 966a91de7e2cc5ce8fb879f8f894204649ff09da98048b94fd75620284330fc9
