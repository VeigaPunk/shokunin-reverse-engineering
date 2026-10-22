# R26-C1 falsify seat: rows read-bytes and inspect-binary-layout

Seat: KaidokuR26.ReplayLayoutBytes (wave 2, leaf). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Judged bytes: commit ebe2cb4a. Lane HEAD moved to 003de8cc during my run; I read HEAD only for entry line 5 (F3). Access date for every source: 2026-10-22. Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/ReplayLayoutBytes/

## Verdicts

| Row | Table verdict | Fresh verdict (frozen rule) | Fresh ids against table.tsv | Verdict |
|---|---|---|---|---|
| read-bytes | content-keyed | content-keyed | base, repeat and copy all equal the table cells | holds |
| inspect-binary-layout | path-sensitive | path-sensitive | base and repeat equal the table; copy differs from the table copy cell, as expected for a different path string | holds |

Fresh ids:
- read-bytes, base = repeat = copy: ev_99b0c6e1f03c73c81930c41b729579b8c000f0911a5bafeda0c5fe068947500c
- inspect-binary-layout, base = repeat: ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd
- inspect-binary-layout, copy: ev_acede390ca4902658ebd07f7fa5855d98f1405c20a1f976785e6e58128e53bc8 (table copy cell ev_52da4b3df64645306a8046c6571ce7849fd2ae4383e8d05f16601fefcdccd161 was made at the claim's alternate path)

## Runs

- Copy, 13:00:44Z: `cp -p /usr/bin/jq <scratch>/alt/jq`. `cmp` exit 0. Both sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806, 30800 bytes.
- Six calls, one at a time, each `TMPDIR=<scratch>/tmp timeout 600 npx -y rea-agents@6.5.0 <frozen argv>`. The timeout wrapper adds no argument. Exact log (out/run.log):

```
1 read-bytes base path=/usr/bin/jq utc=2026-10-22T13:01:06Z exit=0 bytes=3347
2 read-bytes repeat path=/usr/bin/jq utc=2026-10-22T13:01:12Z exit=0 bytes=3347
3 read-bytes copy path=/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReplayLayoutBytes/alt/jq utc=2026-10-22T13:01:18Z exit=0 bytes=3401
4 inspect-binary-layout base path=/usr/bin/jq utc=2026-10-22T13:01:23Z exit=0 bytes=80065
5 inspect-binary-layout repeat path=/usr/bin/jq utc=2026-10-22T13:01:24Z exit=0 bytes=80065
6 inspect-binary-layout copy path=/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReplayLayoutBytes/alt/jq utc=2026-10-22T13:01:25Z exit=0 bytes=80281
```

- All six: `ok` true, and subject sha256 equal to the carrier (eval cell, run after 13:02:08Z; that output has no clock).

## Findings

No counterexample for either row. No high or medium finding.

F1 (low, observation). The frozen invocations in claims.json name no host variables, yet both rows need some. read-bytes runs on the Ghidra provider and needs GHIDRA_INSTALL_DIR. inspect-binary-layout runs on the pwntools provider and needs an absolute REA_PWNTOOLS_PYTHON. Source: dist/native/pwntools/PwntoolsDecoder.js lines 115-116 (grep tool, no shell exit code, between 13:02:08Z and 13:05:12Z): "Set REA_PWNTOOLS_PYTHON to an absolute caller-supplied Python executable". My shell had GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC and REA_PWNTOOLS_PYTHON=/home/vgpnk/.local/share/kaidoku-pwnenv/bin/python. The committed entry covers this in general (ebe2cb4a line 5): "the verbs need `GHIDRA_INSTALL_DIR` and the `REA_*` provider variables that `~/.bashrc` exports". Unknown: the error envelope when REA_PWNTOOLS_PYTHON is unset (not run; no seventh REA call).

F2 (info, observation). The inspect-binary-layout copy id follows the path string. The alternate path sits in three id-bearing fields: data.parameters.path, data.locations[0].path and data.normalized_result.artifact.path. data.subject.local_path is outside the id. Replacing the alternate string with /usr/bin/jq in every string of my copy envelope restores the base id, for both verbs (eval cell; out/recompute-ids.txt). read-bytes has no path in an id-bearing field, so its copy id equals base. Source: dist/application/binaryDiagnostics/BinaryLayoutService.js lines 54-68 writes `parameters: input.data` and `locations: [{ kind: "artifact-path", path: value.artifact.path }]`. Inference: "path-sensitive" describes this verb's contract (the path is an input echoed to output), not a difference in what the reader found. CacheConfound.md says the same.

F3 (info, a wave-1 claim does not hold for the commit). ReplayA.md F1 says the entry's recheck line names TMPDIR but not the GHIDRA or REA variables. The committed text at ebe2cb4a (sha256 b03fcdc4...) and HEAD 003de8cc (sha256 1ba5d5d9...) both name them on line 5 (grep tool, between 13:02:08Z and 13:07:55Z). ReplayA read a working-tree draft before the commit, so its F1 is stale.

F4 (info, pin). Recomputing ids with the 6.5.0 projection rule (omit relationship_coverage when null; dist/domain/evidence.js lines 175-177) reproduces 12 of 12 envelope ids checked: fresh and committed, both verbs. The always-emit rule, which the entry attributes to 6.7.0, reproduces 0 of 2 fresh base envelopes (eval cell; out/pin-rule-check.txt). The 6.7.0 id values in the entry (lines 85-95) are the entry's report; I did not re-measure them.

F5 (info, reproducibility). Envelope bytes vary run to run; ids do not. Base and repeat differ only in meta.duration (5024ms vs 5110ms for read-bytes; 179ms vs 142ms for inspect-binary-layout). Fresh base and committed base also differ only in meta.duration (5024ms vs 5500ms; 179ms vs 194ms). This matches entry lines 41-43.

## Recomputation (no REA calls)

- Rule: id = "ev_" + SHA-256 of canonical JSON of the semantic projection (evidence.js lines 156-182; encoder canonicalDigest.js). Reimplemented in Python in the eval cell.
- Recomputed id equals the envelope id in 12 of 12 cases: fresh base, repeat and copy for both verbs, and committed base, repeat and copy for both verbs. Committed ids also equal the table cells (6 of 6).
- read-bytes base vs copy: differing leaves are data.subject.local_path and meta.duration only.
- inspect-binary-layout base vs copy: data.evidence_id, data.locations[0].path, data.normalized_result.artifact.path, data.parameters.path, data.subject.local_path, meta.duration.
- Same-path repeat vs base: meta.duration only, both verbs.

## Residual risk and verification gaps

- One fresh triple per verb in this seat. Cross-checks: committed ebe2cb4a envelopes reproduce the table cell by cell; ReplayB.md (wave 1) reports a cross-session base match, not re-run here.
- Not tested: REA_PWNTOOLS_PYTHON unset; mtime (my copy used cp -p, so mtime was not varied; ReplayB F3 reports mtime excluded, not replicated); symlink and relative path forms; other carriers, pins, addresses and parameters (outside the claim).
- npx resolution not captured directly. Inference: the calls used cache root ad9a3fdbcad992c6 (package.json version 6.5.0, mtime 2026-10-22T05:22:00). No new npx cache root appeared during my runs (newest root mtime 10:05). F4 supports 6.5.0.
- The pwntools provider version in the envelope (pwntools@4.15.0;pyelftools@0.33;unicorn@2.1.2) is self-reported. The interpreter at REA_PWNTOOLS_PYTHON reports the same versions (importlib.metadata, 13:05:12Z, exit 0).
- Lane counting instrument not run (not in my assignment).

## Sources opened (access 2026-10-22; local reads and read-only git only)

| Source | sha256 | Located quote |
|---|---|---|
| rea-agents 6.5.0 dist/domain/evidence.js (cache ad9a3fdbcad992c6) | f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff | line 181: "Hash semantic content, including raw results and excluding display-subject fields." |
| dist/domain/canonicalDigest.js | f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9 | lines 5-6: "JSON object keys follow RFC 8785's UTF-16 code-unit order in both" |
| dist/application/binaryDiagnostics/BinaryLayoutService.js | b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4 | line 67: `locations: [{ kind: "artifact-path", path: value.artifact.path }],` |
| dist/native/pwntools/PwntoolsDecoder.js | 34b16b05bf13e4aac00c9a1968bd924d0e7442c28f5fa10ffdabe60d9b5b8a79 | line 116: "Set REA_PWNTOOLS_PYTHON to an absolute caller-supplied Python executable" |
| lane .ufo/waves/round-26/claims.json | 1137c312d9d1a4aa83ec4f7b167bcd03423de955d89ede1e53f3c6bf6bfbcb5f | field invocation: "TMPDIR=<seat scratch>/tmp npx -y rea-agents@6.5.0 <argv>" |
| lane entry at ebe2cb4a (also copied to scratch) | b03fcdc450869e65337a81b009ca0f67008c4864d32630dfd858da5e99143a20 | line 5: "the verbs need `GHIDRA_INSTALL_DIR` and the `REA_*` provider variables that `~/.bashrc` exports" |

## Artifacts (scratch; sha256)

- alt/jq e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
- out/read-bytes-base.json 9c796c72623800696b364617220f898e4e302b07398cb55bada928b10bb432d4; repeat 114606d62d0f98f43a5499ea18e5c6556d5852ea1b261e2ae4bba3199b3e661b; copy a8a79467d6408cb46bab2329d108f24ff2010d35d02bd5e059f4bf430bc8964d
- out/inspect-binary-layout-base.json 40c68cbd753a33599b2c967bcbbf4e78413a0a7cbe6474162551847839c2110a; repeat 4cd9bce7e4a58cc4eac56b5140601f6b75ec674fec3217f3cb70a30f4b646047; copy d6e53d831994f9d70b8136063db48c8df22fb1b9a6814f92c7fe28266980ff0f
- out/*.err (six, all empty) e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- out/run.log fe8cf7dfb5bc34f09b33dbe64cbb0f1e5547ba4b6cd12f23b70e6fe6b51f4ef9
- out/analysis.txt c7906a08c65ce5ab0f19035c08c1e16f389774dae484706ee99db0b4fe6e3d69
- out/recompute-ids.txt e7f43ce39d84c538596471c1e69e265b64342bb1f35f325ea43cf18fba02567c
- out/checks.txt 1fafe185460ab3773d025ced8877c30fe6bf91283a3f6ee2567fc8ec8379b7c3
- out/pin-rule-check.txt 52c7b0aee69ffed46991f79843fa661e2dce67c1efee4cf904ab96860539ad93
- entry-HEAD.md (copy of 003de8cc entry) 1ba5d5d909eecb2db638677388f9bcc0429b5263469905a936fc3c2a6185a941
- Committed at ebe2cb4a (git show | sha256sum): table.tsv 89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df; read-bytes base 3eb2f92c3d98761c421c3867b22aaceefb8a5299585b73fc93b4b59f9c711552, repeat b6fa9c4eae2be4507a3f5f158f85366acde36669338abd85de1a126ac219aaa1, copy 5a893e0e0b5dcb136a6d2051d9b187f54f455110a91b775f73845aac068618de; inspect-binary-layout base 4a256cc73b54529b3eae4b9bafa6724a358be55bf5056867c4557f5357dfbb8f, repeat 98a1a229f20ed41867b8ea13a5d8812f158a589c99fb3798e631c13a72b30ebf, copy bfa78b4d3a4174256e8fde069c4671ab9f40b02d9689d72983fc7b89c50e46e9

## Tools

None installed or upgraded. Used: npx (rea-agents@6.5.0, existing cache), cp, cmp, sha256sum, stat, date, read-only git (show, log, rev-parse), Python in the eval tool for JSON parsing and id recomputation, and the REA_PWNTOOLS_PYTHON interpreter for a read-only version import. Lane writes: this report only.
