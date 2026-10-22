# CriticCapabilityRow — the SCORECARD `## Capabilities` row for cross-pin attribution

Seat `KaidokuR27.CriticCapabilityRow`, wave 2, critic, leaf. 2026-10-22, all times UTC. Lane tip `4084d8975b684a8837b1c858eea0008ce9ab49e0`.
Attacked: `SCORECARD.md:623` ("attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code"), entered at `97358f75`.
Read `/home/vgpnk/.omp/agent/RULES.md`; nothing installed or upgraded. No REA call. Lane read-only. The checker makes and removes its own temp dir under `/fast/scratch/hyaku` (its code, `c2-xpin-check.py:247`).

## Verdicts

| Check | Verdict |
|---|---|
| 1. Demonstrated running before the row entered | holds (with a provenance gap) |
| 2. One-line description does not overstate | fails: fixable defect, not a tradeoff |
| 3. New against round-26 scratch scripts | holds only as a committed tool; fails as a new method |

## Check 1 — demonstrated before entry

- `git log -S'cross-pin evidence-ID attribution for saved REA envelopes' -- SCORECARD.md` (15:36Z, exit 0): only `97358f75 … 2026-10-22T12:15:28-03:00`, which is 15:15:28Z committer time. The tool, the four receipt TSVs and the row were all added in that one commit (`git log --name-status`, exit 0). Observation.
- Seat runs came before that commit: `BuildXpinTool.md` gives a sandbox checker run at 15:12:01Z, a checker run at 15:13:39Z and a direct run at 15:13:46Z. File times in the seat folder agree: `keyless-default.tsv 12:13:46.34 -0300` and `xpin-attribute.mjs 12:05:54 -0300` (`ls --time-style=full-iso`, exit 0). Observation. The author dates are not usable: each commit's author time equals the previous commit's committer time.
- The committed tool is byte-identical to the seat copy: both hash to `8ea63837…f708` (`sha256sum`, exit 0). Committed `keyless-default.tsv` (`ccb42b03…`) and `keyless-parse.tsv` (`e44ba858…`) equal the seat files. Committed `r26-attribution.tsv` equals the seat's `r26-direct.tsv` once the path prefix is added (`diff` → `SAME_MODULO_PREFIX`, exit 0). Observation.
- Reproduction with the tool taken from `97358f75` (15:37:09-10Z): all four committed TSVs come out byte-identical. Output was `R26_IDENTICAL`, `R27C1_IDENTICAL`, `KD_IDENTICAL`, `KP_IDENTICAL`, every run exit 0 (`cmp`). Observation.
- Checker `python3 -I -B c2-xpin-check.py --root <LANE> --rev R` (15:37:12-14Z):
  - at `97358f75` and at `4084d897`: `r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081)`, exit 0;
  - at `c6d619a3` (the commit before the row): `FAIL tools/round-27/xpin-attribute.mjs absent at REV … r26_rows_ok=0/24`, exit 1.
  These match `.ufo/waves/round-27/after/c2-at-97358f75.txt`. Observation.
- Gap 1: no file in the seat folder, `/fast/scratch/hyaku/kaidoku-r27/l1/` or the receipts folder records a command or a time for `r27-c1-attribution.tsv`. The receipts folder holds four bare TSVs with no commands, exit codes or times. The content is real tool output (it reproduces), but when it was made before the row is unknown.
- Gap 2: in the lane's receipts the `6.7.0` label never appears on real data: 0 of 109 rows (`r26` 21/3, `r27-c1` 42/6, `keyless` 37 `both`; `cut -f5 | uniq -c`, exit 0). The only `6.7.0` output the lane shows is the checker's red envelope, whose id is minted by the checker's own copy of the rule.
  I ran the tool myself on the 164 arc3 files that round 26 had attributed (`PinDiffCheck/out/joined.tsv`) at 15:37:34-45Z. On the 95 files that have a `.data` record it printed `83 6.7.0` and `12 both`, which agrees with round 26 on all 95 (`py65=no py67=yes tool=6.7.0` ×83; `py65=yes py67=yes tool=both` ×12). So the `6.7.0` output does work on real records. This is my observation, not a lane receipt.

## Check 2 — does the one-line description overstate

The row is literally true only as a fit to two id rules. Every limit that README `corpus/README.md:210-211` and `PROVINCE.md:319-324` state is missing from the row. Four counterexamples:
1. Records without the key get `both` while 6.7.0 rejects them. All 37 lane records that lack `relationship_coverage` print `both` in default mode, and `--parse` prints `parseEvidence-6.7.0 reject:Invalid input: expected object, received undefined` for every one (committed receipts, reproduced 15:37:10Z). The 19 bare round-7 records without the key, once wrapped, also print `both` ×19 with 6.7.0 `reject` ×19 (15:38:06Z, exit 0). CriticNovelty.md puts 16 of those 19 as 6.4.0 output. So on 56 lane records produced by neither pin, the row's "both" reads as a provenance answer the 6.7.0 package itself refuses. The row does not mention `--parse` at all. Observation for the outputs; that these records are 6.4.0 output is inference carried over from round 26.
2. Records with the key set always print `both`. Examples: the 3 round-26 `function` envelopes (made by 6.5.0) and the 12 round-12 `analyze_function` records (made by 6.7.0) (15:37:45Z). The tool can tell the pins apart only when the coverage value is null. The row's "6.5.0 … 6.7.0 … both" reads as a pin answer for any envelope. Observation.
3. It is a rule fit, not a run. README and PROVINCE both say it is "a rule fit … no 6.7.0 run was made" (`PROVINCE.md:323-324`); the row has no such clause. Inference: a reader of `## Capabilities` alone would take "attributes … to the 6.7.0 rule" as attribution to the producer.
4. "A saved envelope" covers only envelopes whose record sits under `.data`. 69 of the 164 arc3 Evidence files are bare records, and the tool exits 2 on them with `envelope has no ".data" evidence record` (69 lines, `grep -c`, exit 0). One such file stops the whole batch (`process.exitCode = EXIT_INPUT` in the top-level catch). The row's heading "saved REA envelopes" is narrowly accurate, but its body never says that bare records are refused. Observation.
"From its bytes" is loose: the tool reads `JSON.parse(...).data`, not the raw bytes. This is minor.
Impacted axes: operability (the description of the capability) and calibration (false provenance labels on 6.4.0 records).

## Check 3 — novelty against round-26 scratch scripts

- `git ls-tree -r` at `4084d897`, filtered to scripts that name both pins (15:38:42Z): only `tools/round-27/c2-xpin-check.py`, `tools/round-27/xpin-attribute.mjs` and `.ufo/waves/round-19/tools/province-pins.py`. The last one checks PROVINCE pin lines; it has 0 `evidence_id`, `digestCanonical` or `semanticProjection` hits (exit 1 = no match). So no committed two-pin evidence-ID tool existed before. Observation.
- The round-26 scratch scripts, none of them committed (hashed 15:38:29Z):
  - `r.mjs` `8a87288b…314a`: 12 lines; one folder; prints counts only; retyped projection; puts `null` in for 6.7.0.
  - `oracle.mjs` `0ba2c0ef…df67`: 114 lines; for each record, prints both ids and both `parseEvidence` results; retyped projection; folder fixed to the round-26 envelopes.
  - `native-parse.mjs` `d10790f1…9f94`: 57 lines; any list of files; reads bare records, `.data` records and `.gz`; uses each package's own `parseEvidence`, and so its own `computeEvidenceId`; one pin per run.
  Running `native-parse.mjs` once per pin and joining the two results already gave the four-way attribution, for all 164 arc3 files (`PinDiffCheck.md` S3, `joined.tsv`). Observation.
- Counterexample: the committed tool reads fewer input shapes than `native-parse.mjs`, because it refuses the 69 bare records. Its default mode is also a weaker test than `native-parse.mjs`: it fits the projection and skips the schema, which is why 56 records without the key print `both`. What is new is a durable, committed tool with a stated output contract that loads each pin's own projection text. Observation for the shapes; "weaker" is my judgement.

## Smallest safe correction (for the L1; this seat edits nothing)

Append a correction under the round-27 section, leaving line 623 as written. It should say:
- the result is a fit of the projection and digest rules over the `.data` record, not a 6.7.0 run;
- records whose `relationship_coverage` is set or absent fit both rules, so default mode prints `both`;
- `--parse` gives each package's own accept or reject;
- bare records exit 2.
Also add one receipt of the tool on the 95 arc3 `.data` files (83 `6.7.0`, 12 `both`), with its command and time, so that the lane shows the `6.7.0` output on real records. The C2 counts (24/24, 3/3, row 1, S081) still hold.

## Artifacts (`/fast/scratch/hyaku/kaidoku-r27/seats/w2/CriticCapabilityRow/`, sha256)

- `xpin-97358f75.mjs` 8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708
- `c2-xpin-check-97358f75.py` d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3
- `out/r26.tsv` b3c15281…4bbc, `out/r27c1.tsv` 751bbce4…4599, `out/keyless-default.tsv` ccb42b03…8ec0, `out/keyless-parse.tsv` e44ba858…104f
- `out/check-97358f75.txt` 9b2fa4c1…a32e, `out/check-4084d897.txt` b6841f92…5315, `out/check-c6d619a3.txt` 4e2e7fad…f195
- `out/arc3-list.txt` aad3b669c7799bec31dffdb6476e051753908febc4b6ce58edba5385eebe6a0e
- `out/arc3-default.tsv` 701a95539dc216f16ba70d9ec44a6e5442c87a2a48302451c481f91a5a2c1752
- `out/arc3-err.txt` 64d0c54796d4c4cc597b7999967a9f24f72cf62505f73a5e0c30bf897bb58d0f
- `out/wrap-map.tsv` 361a343c22efe6c21c5a4bdad62f06f94456856dfd60ebeb3bd9c07d13f3b770
- `out/wrapped-default.tsv` bc6d5fdcd29c4c3d4832b8cca76c763f33ef018b9c4a2775d6721590fcbf5bc8
- `out/wrapped-parse.tsv` 4e8a55403341b61091402e05a073fbc6e4043c8116a6e162bb357974091feb72
- `out/wrapped-joined.tsv` b5f9da46a3828dd0733b436a3e10a9afc370bf61652c7e9fbc21d03477020d8d
- `wrapped/`: 69 copies of the bare records, each wrapped as `{data: record}`
