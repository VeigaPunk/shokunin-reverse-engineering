# EntryOverreach — does the R26-C1 entry claim more than its evidence?

Seat: KaidokuR26.EntryOverreach, wave 2 (falsify), round 26 attempt 1. Judged at lane commit
`fe3eb4edf410244eff46151a148c8f754be1ce80`. Between `ebe2cb4a` and `fe3eb4ed`, `git diff --stat` printed nothing for the entry, `corpus/README.md`,
`corpus/lessons/round-26.md` and `corpus/SOURCES.md`, so these files are the same at both commits. Blob sha256 values at `fe3eb4ed`: entry
`b03fcdc4…143a20`, README `ff5fc422…fecc00`. No REA call was made. No tool was installed.

**Verdict: fails.** The entry overreaches in four places. The scope it measured, and mostly states in its Limits, is
one carrier, one pin, one address, the same file name and one Ghidra build. The title, the first Use bullet and two
README rows say more than that. All four can be fixed by editing wording. No measurement needs repeating.

## Overreaches, each with the smallest correction

**O1. The title says "the eight native reader verbs", as if they were the whole family** (entry line 7; SCORECARD line 3073 and LOG line 2965 say "of the eight native reader verbs" too).
- Observation: "native reader" is not a term in the package (`rg -i 'native.?reader'` over the 6.5.0 package root found only two unrelated files). The eight were
  chosen by the round-25 seat `.ufo/waves/round-25/a3/w1/PlannerWalk.md:40`, candidate C-C. The 6.5.0 `CLI_COMMANDS` table
  (`dist/cli-runtime/reconstructionObligationLedgerSchemas-Bao0xMr-.js`, sha256 `81d775c4…99f5`) lists more verbs that read
  native binaries. Excerpt from lines 817-821: `searchBytes: "search-bytes"`, `addressToFileOffset: "address-to-file-offset"`,
  `inspectNativeInstruction: "inspect-native-instruction"`. Lines 777-900 also list `search`, `inspect-native-api`, `inspect-native-data-type`,
  `inspect-native-load-image`, `resolve-native-call-targets` and `trace-native-values`. Command: `sed -n '777,900p' … | rg -i 'native|search|…'`, exit 0, 2026-10-22T13:00:55Z.
- The Limits section does say "No claim is made for … other verbs", but "the" in the title reads as complete.
- Correction: change "the eight native reader verbs" to "eight native reader verbs". Add one sentence saying the set is the
  round-25 PlannerWalk C-C selection, and name `search-bytes` and `inspect-native-instruction` as examples left out.

**O2. "Compare ids only within one pin" leaves out the Ghidra build, which also feeds the id** (entry line 93; README line 206; the first Use bullet, entry lines 99-101).
- Observation: the hashed projection includes `provider` and `analysis_profile.provider`, whose `version` field is `12.1.4` for the
  Ghidra verbs and is nested in `upstream_analysis_profile` for `analyze` and `inspect`. Command: `jq -c '{provider:.data.provider,…}' env/<verb>-base.json`, exit 0.
- Observation: I changed only that version string, then recomputed the id with the lane's own `recompute_ids.py` (`provider_mutation.py`,
  exit 0, 2026-10-22T13:00:55Z). Every id changed. Excerpt: `decompile … '12.1.4'->'12.1.5' mutated=ev_544956e32eef changed=True`.
  The same happened for `analyze` and `read-bytes`. Before mutation, every stored id recomputed exactly.
- Observation from the 6.5.0 source, `dist/ghidra/GhidraInstallationPolicy.js` (sha256 `94976ae6…0879`): line 39 classifies
  other 12.1.x builds as `"compatible"`. Line 44 says "The observed version stays on the provider identity." Line 50 says
  "other … builds are accepted and the observed version is reported". This host runs `ghidra_12.1.4_PUBLIC`
  (`application.version=12.1.4`).
- Inference: at the same 6.5.0 pin, another host with Ghidra 12.1.3 or 12.1.5 would get different ids for the same bytes and
  the same request. That covers the five Ghidra verbs, plus `analyze` and `inspect` through their upstream profile. Its envelopes would also carry
  an extra hashed limitation. `inspect-binary-layout` is not affected: its provider version is a package constant
  (`dist/native/pwntools/PwntoolsRelease.js:5-6`, sha256 `f10bf01d…a828`).
- The Limits section lists "one pin" but not "one Ghidra build", even though the Why section names the provider as a hashed field.
- Correction: in the Pin section, README line 206 and the first Use bullet, write "compare ids only within one pin and one Ghidra
  build (`.data.provider.version`)". In Limits, add "one Ghidra build (12.1.4)".

**O3. The first Use bullet's advice for `inspect-binary-layout` cannot work as written** (entry line 100).
- The bullet says: "compare `.data.subject.digest.sha256` and the parameters instead, because the same bytes at another path get another id".
- Observation: that verb's only parameter is the run path. Base gives `{"path":"/usr/bin/jq"}`, and copy gives
  `{"path":"/fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq"}`. Command: `jq -c '.data.parameters' env/inspect-binary-layout-{base,copy}.json`, exit 0.
- Counterexample: the committed base and copy envelopes. They are the same bytes and the same request, but their parameters
  differ, so following the bullet's advice reports them as different.
- Correction: replace "and the parameters" with "and the parameters other than `parameters.path`". At 6.5.0 that leaves
  `.data.subject.digest.sha256` alone.

**O4. Two places drop the scope the entry measured.**
- The entry title (line 7) gives no carrier and no address, and it calls the seven verbs "content-keyed" without saying how that was tested.
  Only the directory changed between runs: the file name and the content stayed the same.
- README line 75 says "on one carrier (`/usr/bin/jq`), three runs each". It leaves out the single address `0x103fa0` that the five
  address-taking verbs used.
- Correction for the title: "Evidence-ID identity of eight native reader verbs at REA 6.5.0 on `/usr/bin/jq` — seven keep their
  id in another directory, `inspect-binary-layout` does not".
- Correction for README line 75: insert "one address (`0x103fa0`) for the five address-taking verbs,".

## Claims that hold

- README line 206 states the carrier and "a byte-identical copy at another directory with the same file name".
  README line 75 states "different file names not tested". The entry's Limits (lines 108-113) state the
  file-name gap, the single address and the other verbs. The Pin section separates measured relations from inferred ones.
- Use bullets 2 and 3 (lines 102-104) stay within the evidence.
- README line 166 is an index row and points to the entry. This holds, apart from the "eight native reader verbs" wording covered in O1.
- I looked for a counterexample to the file-name gap and found none. In the hashed projections of the seven verbs, the
  only `jq` tokens come from strings inside the binary itself, such as `'jq: error (at %s): %s\n'` in `function`
  and the `decompile` pseudocode. None is a file name or a path. `inspect-binary-layout` carries the run path in
  `/parameters/path`, `/normalized_result/artifact/path` and `/locations/0/path`. All 24 envelopes recomputed exactly.
  Command: `name_in_projection.py`, exit 0, 2026-10-22T12:59:31Z.
  Inference: renaming the file is unlikely to change these seven ids, but that is unmeasured. Seat ReplayRenamedCopy owns the live test.

## Impacted axes

- Depth (R26-C1): the claim's counter is unaffected. The table, ids and verdicts re-derive. Only the wording of the entry and README overreaches.
- Calibration: O2 is a missing scope dimension in a "how to use" rule. It should go to the L1 as a routed fix, not a reject.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/w2/EntryOverreach/)

| file | sha256 |
|---|---|
| recompute_ids.py (copy of the lane tool at fe3eb4ed) | 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b |
| name_in_projection.py | 07fe32e506251f849f36e9ec8e60631632c2dc90b123d6c091457adc94bf0884 |
| name_in_projection.out | 76b7580acf9c1dde8dbb70717329cd5b337abcbb0085e14efa688dcee824dbd8 |
| provider_mutation.py | 4552db96ea4a9f6675a575aba4614895e5d9a5537a75d0d372dd5f5c4add0f64 |
| provider_mutation.out | ca7e07c7349373c6a4c76785564ca56e36cbbe2048987992a8dfbca1e97543ba |
| cli-commands-native.txt | d4a3ce2941d246704eb7d8afa65d61468b44db784194dba48137d22ffcdd7c93 |
| cli-file.sha256 | 50c4dac5205614745efc1b21bccaad39919ac06209acef87b1c6997c9f555d54 |
| provider-policy.sha256 | 5e9fc202322a036ada14fd96aa82bea10be5d1c7d99e2daabd29e3f6025d5fcb |
| env/ (the 24 envelopes from `git show fe3eb4ed:`) | listed in the lane's runs.tsv |
