# ReplayA: independent replay of R26-C1 verdicts (analyze, decompile, xrefs)

Seat: KaidokuR26.ReplayA (leaf, no delegation). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin at HEAD c27f445e. Carrier: /usr/bin/jq, 30,800 bytes, sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806. REA: rea-agents@6.5.0 (package.json line 4: "version": "6.5.0"). Access date for every source: 2026-10-22.

## Result

- analyze: holds. decompile: holds. xrefs: holds. For each verb the base run, the same-path repeat and the alt2 copy give one identical evidence id, so the frozen rule derives content-keyed.
- Cross-session stability: yes for all three verbs. My base id equals the run seat's base id.
- Path dependence beyond one alternate: none seen. My alt2 id equals the run seat's copy id (carrier/alt path) for all three verbs.
- Problems found: a provider-environment precondition the entry omits (F1), a wrong provider count (F2), an incomplete field list (F3) and an unsupported function name (F4). None changes a verdict.

## Ids and comparison with run seats

| verb | my id (base = repeat = copy) | RunAnalyzeInspect / RunDecompileFunction / RunXrefsInstructions base | copy at carrier/alt | repeat |
|---|---|---|---|---|
| analyze | ev_14f9d92f41c6a4218108768927a622dbd7057ade4bcd305d083e0d6826b3d328 | equal (RunAnalyzeInspect) | equal | equal |
| decompile | ev_03d786185306c84bf588fcc66cb7f02c74c9af179a31a90adf403f45026014df | equal (RunDecompileFunction) | equal | equal |
| xrefs | ev_d591ef8c4f9a0af3627a756dca2d56ddb5c9b54b12d6cd1e416f475c0796b27c | equal (RunXrefsInstructions) | equal | equal |

The run seats' envelopes also agree with their own runs.tsv id columns (parsed; all equal).

## Runs (nine calls: six specified plus three repeats)

Script run-calls.sh, run sequentially from the bash session environment. All exit 0, all ok true, all subject sha256 equal the carrier sha256. "alt2" means /fast/scratch/hyaku/kaidoku-r26/seats/ReplayA/alt2/jq.

| verb | run | path | UTC start | envelope bytes | envelope sha256 | provider |
|---|---|---|---|---|---|---|
| analyze | base | /usr/bin/jq | 12:16:55Z | 7559 | 467c253621f138f140bef369dc3bb4e1c7a449099ae7270e016d79139810fcbb | rea-workflow |
| analyze | copy | alt2 | 12:17:00Z | 7601 | efc196efd9d801af06cc78efe149f125062e0fbf29c3c3968eb9ff2f2df9775d | rea-workflow |
| analyze | repeat | /usr/bin/jq | 12:17:29Z | 7559 | 3d83993077c53f30acc12ca34532a4d30d39faeff47880cdbfb467df1350704a | rea-workflow |
| decompile | base | /usr/bin/jq | 12:17:06Z | 13032 | 20df26c34e21a629e9504d3d72647a9931ad7a82e74e5ca6b8f462831989c5e4 | ghidra |
| decompile | copy | alt2 | 12:17:12Z | 13074 | 04aaaa73305048474b81445405df6ee859dea0504b793a6ca8bbb2ff3c306452 | ghidra |
| decompile | repeat | /usr/bin/jq | 12:17:34Z | 13032 | 06ca77c9aaad9e411e9d5e3203ef6801b4b5f9fe99dafaafd119e5990fdcdc90 | ghidra |
| xrefs | base | /usr/bin/jq | 12:17:17Z | 3089 | d6c42ba046a7e493457a25cf8598599cd75bc57fc1a0e66f6ea0b704006ac7b3 | ghidra |
| xrefs | copy | alt2 | 12:17:23Z | 3131 | 9cbd9f4a174c283d160b15049a297dd82c9b3b8907872186a03c74609ec7bb62 | ghidra |
| xrefs | repeat | /usr/bin/jq | 12:17:40Z | 3089 | 2ae4678a28d838403e9109dce93cbea3084a9a6bea35ed729cd3645f6760f112 | ghidra |

Scope notes:
- The six specified calls ran unchanged. The three same-path repeats are my addition: the frozen rule marks a verb unstable when base differs from repeat, so a three-run derivation needs them.
- alt2 is a cp of /usr/bin/jq made in this seat. cmp exit 0; sha256 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 for /usr/bin/jq, alt2 and carrier/alt.
- A first attempt of nine calls from the Python kernel environment failed on all nine (F1). It is kept under failed-kernel-env/ and not used for any verdict.

## Verdict basis

Frozen rule: no-id if any envelope lacks a string ev_ id; else unstable if base differs from repeat; else content-keyed if copy equals base; else path-sensitive. All three verbs derive content-keyed. "Holds" means that derivation re-runs in this seat for this carrier, pin, address 0x103fa0, default parameters and the provider environment in F1. It says nothing about the other five verbs or other pins.

## Findings

F1 (medium, reproduction precondition). The frozen invocation needs ambient provider settings.
- Command: TMPDIR=.../ReplayA/tmp npx -y rea-agents@6.5.0 analyze /usr/bin/jq --format json --full-output, run from the Python kernel. Exit 1. Nine calls ran 12:15:32Z to 12:15:39Z, all exit 1.
- Excerpt: {"ok":false,"error":{"code":"provider_unavailable", ... "provider_id":"ghidra","code":"not_configured","reason":"Set GHIDRA_INSTALL_DIR to an extracted Ghidra 12.1.x release directory."
- Cause: the kernel environment has no GHIDRA_ or REA_ variable (0 matching keys of 35, 12:25:01Z, eval). The bash environment has GHIDRA_INSTALL_DIR (directory exists) and seven REA_ variables (names only, in env_names_bash.txt).
- Effect: all nine calls would be no-id, not content-keyed. The entry's recheck line (entry line 5) names TMPDIR but not these variables, so a live recheck in a clean environment fails. The offline counter is not affected.

F2 (low). The entry misstates the provider split. Entry lines 55-56 say "The seven Ghidra-backed verbs". The lane's base envelopes give, by jq -r '.data.provider.id' (exit 0, 12:21:29Z): analyze rea-workflow; inspect rea-workflow; decompile, xrefs, read-bytes, function and instructions ghidra; inspect-binary-layout pwntools-elf. So five are ghidra and two are rea-workflow. Whether rea-workflow runs Ghidra internally, and whether the private byte copy claim holds, I did not check (unknown).

F3 (low). The mechanism list is incomplete. Entry lines 50-53 name the kept fields as parameters, normalized_result and locations. The projection in dist/domain/evidence.js lines 156-180 also keeps subject digest, format and architecture, provider, analysis_profile, predicate_type, operation, raw_result, confidence, authority, environment, limitations, relationship_coverage when non-null, and evidence_links. "Path-sensitive exactly when the path enters a kept field" holds only over the full list. Source read by the read tool (no exit code; time not captured).

F4 (low). The function name is not in these envelopes. Entry lines 20-21 call 0x103fa0 the static function `process`. My decompile-base normalized_result text begins "int FUN_00103fa0(undef" (jq key query, exit 1, 12:21:29Z: string has no keys). A search of decompile-base, analyze-base and xrefs-base for "process" and for the version string returned No matches found (same batch, 12:21:29Z). The sum 0x100000 + 0x3fa0 = 0x103fa0 holds. The name rests on AddressCheck.md, which I did not open. The no-version-string claim at entry lines 88-89 is consistent with these three envelopes.

F5 (info; entry correct). analyze and inspect share one id: both carry operation binary_overview and parameters {} (jq, exit 0, 12:21:29Z, analyze-base and RunAnalyzeInspect inspect-base). Entry lines 42-45 say this.

F6 (info; limits the copy test). In all three verbs, base versus alt2 copy differs only in .data.subject.local_path and .meta.duration, and base versus repeat differs only in .meta.duration (Python structural diff, between 12:17:46Z and 12:19:46Z). The only path-like string in .data of analyze-base, decompile-base and xrefs-base is /usr/bin/jq (jq query, exit 0, 12:21:59Z). So content-keyed is close to built in for these verbs. The copy test bites only when a path reaches a kept field, which is the inspect-binary-layout case (not replayed here).

F7 (info; gate). Nothing is committed yet. git cat-file -e c27f445e:corpus/evidence/round-26/c1/table.tsv returned "fatal: path ... exists on disk, but not in 'c27f445e'", exit 128, 12:25:01Z. The committed corpus/evidence/round-26 at c27f445e holds only before/census-start.txt (git ls-tree, exit 0). tools/round-26/c1-id-identity.py is absent (test -e, exit 1, 12:23:09Z). The entry file is present in the working tree (test -e, exit 0, 12:20:46Z). A counter run at REV would see no C1 rows until the L1 commits.

## Lane working-tree table cross-check (uncommitted; Python read, exit 0, between 12:19:46Z and 12:21:29Z)

- For all 8 rows: the table verdict equals the verdict derived from the lane's three envelopes (8 of 8); id cells equal envelope ids (8 of 8); ok true (8 of 8); subject sha256 equals the carrier (8 of 8).
- Table verdicts: seven content-keyed; inspect-binary-layout path-sensitive (not replayed here).
- For analyze, decompile and xrefs, the table id cells equal my ids (3 of 3).

## Residual risk and verification gaps

- Not replayed: inspect, read-bytes, function, instructions, inspect-binary-layout. Run-seat files were used only for the three verbs.
- Not tested: a renamed copy (the entry says so too), TMPDIR or working-directory changes, pin 6.7.0 for these verbs, other addresses or parameters.
- Not evaluated: the counter (absent), the row count at REV (zero until commit), entry_ok (SOURCES row and lesson ## Gate section).
- Cross-session comparison uses the run seats' recorded files; I did not re-execute their runs.
- F1 shows what a missing environment does (no-id). It does not show what a different GHIDRA_INSTALL_DIR does to an id. The analysis profiles hold no install path (F6 check), which suggests no effect; this is inference.

## Sources opened (access 2026-10-22)

1. /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js, sha256 f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff. Quote, line 181: "Hash semantic content, including raw results and excluding display-subject fields." (11 words). Projection read at lines 150-203.
2. /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json, sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Quote, line 4: "version": "6.5.0",

Lane and run-seat files read as data (hashes for the record): .ufo/waves/round-26/claims.json 1137c312d9d1a4aa83ec4f7b167bcd03423de955d89ede1e53f3c6bf6bfbcb5f; corpus/evidence/round-26/c1/table.tsv 89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df; c1/runs.tsv 250a00a8ddda82eb712def66300fdfeef185d5296afde6dfe040c8784040d6c5; corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md 06baae417bc37bb67d1a2c92ad3ec1e9cb39dbc73349e1207b0dc601621e59ed; RunAnalyzeInspect/runs.tsv d885e43581a7607590aaf3ff62f39468ac000b3210219d06881d3d8b01b05944; RunXrefsInstructions/runs.tsv 2c6783ea51c14a13def632099b5c3a8be030a1cb21555d9a65feb568e4d369b1; RunDecompileFunction/runs.tsv 3d820933ac0870927d39dac4aff8f0f08357552d69c87a26b22cc047622c68b6.

## Tools and installs

Nothing installed or upgraded. Used: npx -y rea-agents@6.5.0 (npx cache root ad9a3fdbcad992c6, package version 6.5.0); cp, cmp, sha256sum, stat and date; system jq (/usr/bin/jq, the carrier binary) as a read-only JSON reader, never as an REA target; git cat-file, ls-tree and rev-parse, read-only. No jj, no lane writes, no sibling changes.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/ReplayA/)

- alt2/jq e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
- run-calls.sh e63a8ccbbeab9bfb4a9f55375fbda8e29b2755b8864fe10715a9f6296c2db87f
- run_calls.tsv 1c1f810d79694ed82920c3388c679d06a15080a13838c10f0e037777249c192e
- runs_table.tsv 6df25e5c1e94971561b3d0514e0eb2fb4b170c151354599e4ec314aed8f7b93f
- derived_verdicts.json 6cac2a746e2be476cbdfa4e22645a3613684bb2eb5f76fc44b2a1215c3202a5c
- env_names_bash.txt c7095767a401747d384fd59053c79c58719b0df97e68d305b47bb04d4183c908
- MANIFEST.sha256 0047195bbf3a63e4a5ffbc270cf7364429439e176e8d9fc91111a98e27f1cf39 (covers the nine envelopes, nine stderr files and the files above)
- failed-kernel-env/run_calls_kernel_env.tsv d3a314bf44b66fe1dfc9f6a0c4dd1bed5e893c0a4349d6070b831e4eb90a936e
- failed-kernel-env/MANIFEST-failed-kernel-env.sha256 eb51fa52caa244d4538745203f0a33193f2d3c8f4c06061d2c072d7528414b60 (covers nine failed envelopes and nine stderr files)
