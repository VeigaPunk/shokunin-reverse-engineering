# R26 w2 PinEvidence: do the C1 envelopes come from rea-agents 6.5.0?

Seat KaidokuR26.PinEvidence, falsify wave, leaf. Lane base a0639d8e61e486e2a716ff94cddd89a73200a02c; claims frozen at c27f445e70cedbaf5300b2fd0a53e821d9b659a9. Times are UTC, 2026-10-22. Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/PinEvidence/. Lane untouched; no git or jj writes.

## 1. Verdict
- Attacked claim, "the 24 C1 envelopes come from rea-agents 6.5.0": HOLDS, with the limits in section 5. All 24 match the 6.5.0 id rule and the 6.5.0 validator; live 6.5.0 reruns reproduce all eight stored base ids; 6.4.0 and 6.7.0 are excluded for every envelope.
- Entry claim, "the pin rests on the call records and the resolved package root" (corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md, lines 127-128; line 3 gives only the package root): FAILS as worded. runs.tsv records only the verb argv, with no npx spec and no resolved root. The attribution rests on envelope content and reproduction.

| verb | coverage | 6.5.0 id rule (base, repeat, copy) | 6.7.0 id rule | 6.7.0 validator | payload marker | live 6.5.0 rerun | per-verb pin verdict |
|---|---|---|---|---|---|---|---|
| analyze | null | 3/3 | fails | rejects, id only | workflow_revision 3, no source_limitations; nested v3 and v1 literals | equal | 6.5.0 |
| inspect | null | 3/3 | fails | rejects, id only | same as analyze | equal | 6.5.0 |
| decompile | null | 3/3 | fails | rejects, id only | v3 and v1 literals | equal | 6.5.0 |
| xrefs | null | 3/3 | fails | rejects, id only | v3 and v1 literals | equal | 6.5.0 |
| read-bytes | null | 3/3 | fails | rejects, id only | v3 and v1 literals | equal | 6.5.0 |
| instructions | null | 3/3 | fails | rejects, id only | v3 and v1 literals | equal | 6.5.0 |
| function | non-null | 3/3 | passes (rules agree) | accepts | v3 and v1 literals; live 6.7.0 gives v4 and a different id | equal | 6.5.0; the literal decides, not the id |
| inspect-binary-layout | null | 3/3 | fails | rejects, id only | none (analysis_profile is null) | equal | 6.5.0; projection rule alone |

## 2. Evidence (producing command, exit code, UTC)
- A. Lane tool, 6.5.0 rule: `python3 -I -B tools/round-26/recompute-ids.py --dir <envelopes>`; exit 0 at 13:02:58; stderr empty; last line `recomputed ids: 24 match of 24 total`.
- B. Package-code oracle (`oracle.mjs`, node v24.21.0) loads each package's own `parseEvidence` and `digestCanonicalValue` from the read-only _npx trees; exit 0 at 13:02:22. 6.5.0: 24 of 24 ids and 24 of 24 validator accepts. 6.7.0: 3 of 24 (function only). The other 21 fail only with "Evidence semantic identifier does not match its record"; no schema issue.
- C. Independent Python recompute of both rules (`recompute_both.py`, exit 0 at 13:03:06): 24 of 24 under 6.5.0, 3 of 24 under 6.7.0, zero disagreements with B. Each envelope sha256 equals the runs.tsv envelope_sha256 (24 of 24); each subject sha256 is e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 (24 of 24).
- D. npx resolution: npm 11.19.0 under fnm is the npx in the login shell, cache /home/vgpnk/.npm. libnpmexec/lib/index.js:250-261 names the directory by sha512 of the sorted spec list, first 16 hex characters. Reproduced at 13:01:55: `rea-agents@6.5.0` gives ad9a3fdbcad992c6 (the 6.5.0 tree); `rea-agents@6.7.0` gives a1722018f28f9df2 (the 6.7.0 tree).
- E. 6.5.0 tree custody: _npx.packages is ["rea-agents@6.5.0"]; installed package.json version 6.5.0 (sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c). Lock integrity sha512-C6BG7L...A== equals `npm view rea-agents@6.5.0 dist.integrity` (13:09:29) and the cached tarball (5,634,033 B; sha512 verified). All 1,650 tarball files equal the installed files (0 mismatches). Four tracked files hash the same before the first live call (13:04:28), after it (13:04:39) and at the end (13:09:29).
- F. Live reruns, login environment, sequential, `npx -y rea-agents@6.5.0 <frozen argv> --format json --full-output`; all exit 0, stderr empty. Layout 13:04:28, function 13:04:53, analyze, inspect, decompile, xrefs, read-bytes and instructions 13:06:47 to 13:07:20. All eight ids equal the stored base ids: layout ev_294a449c, function ev_b2b7e9e4, analyze and inspect ev_14f9d92f, decompile ev_03d78618, xrefs ev_d591ef8c, read-bytes ev_99b0c6e1, instructions ev_b20a0f25.
- G. Live 6.7.0 contrast: layout at 13:05:12 gives ev_d1256a96 (the wave-1 PinSourceDiff value); function at 13:05:20 gives ev_177586c6 with the v4 and exact-address-incoming-without-synthetic-entry-v2 literals. The 6.7.0 layout output equals the stored 6.5.0 layout after removing evidence_id and meta (sorted JSON; both sha256 e4d36446b7ab53af76819f8fcbfab88f3f1d417dda91c8f0e775aa455c1648df).
- H. Controls (`controls.mjs`, exit 0 at 13:10:17): each live pin's output passes its own validator; the other pin rejects the null-coverage outputs with the id message; the live 6.7.0 function output passes both.
- I. 6.4.0 (`npm pack rea-agents@6.4.0` into a scratch cache, exit 0 at 13:05:57): integrity equals the registry value; evidence.js sha256 690dc0355ce8dd64417b8ebb1ebd4a06c6b5ece648eeb7caf6978638b880de39 equals the value wave 1 recorded. The whole 6.4.0 dist has no relationship_coverage or relationshipCoverage string; its record schema is .strict() without that member; its projection omits coverage; workflow_revision is 2 for binary_overview; it has no ghidra-function-boundary-limitations-v* or exact-address-incoming* literal.
- J. Live 6.5.0 layout without --full-output (exit 0 at 13:08:33): the bare record is 79,984 B and carries the key. The cited 6.4.0 bare record (corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md line 26) is 79,955 B. The 29 B difference equals the length of "relationship_coverage":null, . This is inference only: the cited /tmp file no longer exists.

## 3. Rule and literal sources
- 6.5.0 dist/domain/evidence.js:175-177 omits relationship_coverage when null; 6.7.0 :178 always includes it. Schema: 6.5.0 .nullable().default(null) at :113, 6.7.0 .nullable() at :116. Both check the id in authenticatedEvidenceSchema (6.5.0 :133-141, 6.7.0 :136-144).
- canonicalDigest.js is byte-identical in 6.4.0, 6.5.0 and 6.7.0 (sha256 f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9).
- 6.5.0 GhidraAnalysisProfile.js:68-69 emits ghidra-function-boundary-limitations-v3 and exact-address-incoming-v1 (also in the bundles). 6.7.0 GhidraAnalysisProfile.js:13-14 emits -v4 and exact-address-incoming-without-synthetic-entry-v2; no v3 or v1 string appears anywhere in the 6.7.0 dist.
- 6.5.0 dist/application/InvestigationProviders.js:12 gives workflow_revision 3 for binary_overview; 6.7.0 :11 adds source_limitations and :13 gives revision 4. REA_WORKFLOW_PROVIDER version "1" is the same in both, so it does not discriminate.

## 4. Wave-1 reports and the entry
- PinSourceDiff.md: its 6.5.0 and 6.7.0 values reproduce (F, G). Its 6.4.0 point holds for ids (null coverage hashes identically) but not as a basis for matching records: all 24 C1 records carry the key, which 6.4.0 cannot emit (I, J).
- CacheConfound.md: no cache effect found; eight of eight ids reproduce across fresh processes (F).
- RecomputeIds.md: no conflicting pin claim; its instrument is pinned to 6.5.0 as it states.
- Entry lines 125-126 ("6.4.0 and 6.5.0 agree" for layout): true for the id only. Entry lines 127-128 overstate the call records (section 1).

## 5. Limits
1. The npx spec is not recorded: runs.tsv has verb argv only and envelope meta has command and duration. Attribution is by content and reproduction. The 6.5.0 tracked files are dated 05:22 local (08:22 UTC), before the C1 runs (12:11:50 to 12:15:45 per runs.tsv), and unchanged since, which suggests the same tree during the C1 window. That is inference.
2. Pins tested: 6.4.0, 6.5.0, 6.7.0. Not tested: 6.3.0 and earlier. 6.6.0 is absent from the registry version list (npm view, 13:05:42). Any other build with the same projection and literals cannot be separated here.
3. The 6.4.0 exclusion is static (grep and schema) plus a size difference against a file that no longer exists. No 6.4.0 run was made; the 6.4.0 tree is not in the npx cache and I did not install it.
4. One carrier (/usr/bin/jq), default parameters, the frozen address, the copy at the alt path. No MCP calls, no error envelopes.
5. inspect-binary-layout has no payload marker; its 6.7.0 exclusion rests on the projection rule plus the live 6.7.0 output.
6. The _npx/ad9a3fdbcad992c6 directory mtime moved at 13:04:28, 13:04:35 and 13:08:49 UTC during the session; cause not identified. No tracked file changed (E).
7. The ids include provider.version 12.1.4. Live reruns equal the stored ids, so the same Ghidra version string was used today; the Ghidra binary itself was not checked.

## 6. Tooling and cache use
- Installed or upgraded: none. Used the existing npm 11.19.0 (npm pack, npm view). `npm view rea-agents versions` (13:05:42) used the default cache, so registry metadata may sit in ~/.npm/_cacache; no tarball or install went there.
- REA calls: 11 CLI calls (9 at 6.5.0, 2 at 6.7.0), all on /usr/bin/jq, sequential, no MCP, no background jobs. Two shell calls failed on quoting before any REA call ran.

## 7. Artifacts (sha256), /fast/scratch/hyaku/kaidoku-r26/seats/w2/PinEvidence/
- 0ba2c0ef2ffb40dd91d7c291bfd3e7e92be97568c41748844f0e4d6129b5df67 oracle.mjs; 42b3f80908ed401ddc78a15ec2d2222918b2b040a75082ac4268202c31c7d710 oracle-out.json
- 2410a3fc8325c6cf1484a26c9f4b66175bf6379ed8b1517a6b254ad2cea30276 recompute_both.py; d914dede534892ed61e8b15e5d222fa329d7bcb4bcf67945acb199d2f4391550 recompute_both.out
- f66e59f43b5552ab35f0bb554ab7ff24b4144dfa6b3e07c9d12fc2fc32f74ee0 lane-recompute.txt; 0e8384be7cb9e65e7b76ae4a544cd4c7ba3b6269bf7007dd3cd09b81283ec3e0 live650.sh
- 9ba3ce695ac7ab71b5b1ccb1ca2b6c40efd7b2c34eb11bdfd5bf19cadad70805 live-650-analyze.json; 12d5854bbb6d843a578bcaf209eb2b2d1ef3b88baf5e86a405299ccb4ce5c5fe live-650-inspect.json
- af4a84251bcd779fbfb4f74f6a334dfaae8c929b2228b17507852a963518bc49 live-650-decompile.json; eaf81d0f73683782499190764982d002fccb5482e2a305593419ef3f408b5eb8 live-650-xrefs.json
- cb16784272f4424fe5dee6aee924f81fc9a0d2c02a0bc3e9e92217aa938b49f6 live-650-read-bytes.json; dd5d93b6dc27365e54dc5d02c8b6c20279594ebb4a5f575ae0c6f98266532e3a live-650-instructions.json
- 0db8fc9578bbb6f67a6aaf530b9611dff0cd9d18c701f412b47ff90386b61d00 live-650-function.json; 28b52596c09004c06c9171fe6fad8438f3adb1623f5e9a5a628ab60c1298c51b live-650-layout.json
- 0ea537046d4d4d636a89fc62d148d15a80e11466ab4d4ea5c7c0cfb00a5543e3 live-650-layout-nofull.json; 1c3f717dd03e1fa7dd014245e46e6df9439f20feadc64c9f43541cbe539b44bb live-670-layout.json
- 5419ed044357f7dbb710373a731c3ed7813573080ba9ae9d3692fc2aa46b9b2d live-670-function.json; 85d7e71e07dd48198e4a86d8813591e8b2f0b2474acbca4cb5c686215a364d7b pack/pack-640.json
- 59eb1604b8db75f522d4a975c36ce6b4a2ad465e43bad165f9a8f728391db9b8 pack/rea-agents-6.4.0.tgz; fdc6a9a1cf01e1133c3afc7ee1606767f0afc3a31f757cf0f68c8b2a9acf1136 manifest-650-before.sha256 (identical to manifest-650-after.sha256)
- e4d36446b7ab53af76819f8fcbfab88f3f1d417dda91c8f0e775aa455c1648df l650-noid.json (identical to l670-noid.json); 71b580a2baa725b1e0494bfb7fa72a23fc725aab90df1626443995e1e538ae8d controls.mjs
- 6bdb41b89419df8672f9507cb3c365e7e3b7098bf1d113d5a34adb6856c5e714 controls-out.txt; 0a384274397876e2c4ef6465a375e74b11d5dcd1bc7213ad5f8f25dcadce2cba artifacts.sha256 (the full list)
- The .err files from the live runs are all 0 bytes.

## 8. Residual risk and checks for main
- No finding changes any C1 verdict; the table rows match the derived verdicts (24 of 24).
- Recommended: record the npx spec and the resolved _npx directory in runs.tsv or envelope meta; reword entry lines 127-128 to cite envelope content and reproduction.
- Not run by me (outside the assignment): c1-id-identity.py and c2-calibration.py.
