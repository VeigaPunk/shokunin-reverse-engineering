# CriticC1HonestStop — attack on the L1's "15 of 16, honest stop" disposition of R27-C1

Seat: KaidokuR27.CriticC1HonestStop (critic, leaf, round 27 wave 2). Attacked: the L1's report that R27-C1 is missed at 15 of 16 rows, with the tinyxxd `inspect-binary-layout` base and repeat runs kept as measured, the extra run not used, and the result written as missed wherever the round reports it. Lane tip 4084d8975b684a8837b1c858eea0008ce9ab49e0. All times are UTC. Scratch timestamps were stored in local time (-03:00) and are converted here.

Overall verdict: **holds**, with one disclosure gap that is a fixable defect (check 6). Under the frozen rules a miss is the only allowed result (check 7).

## Checks

1. **The pinned counter gives 15 of 16 at the measured revisions.** Observation. Command: `git clone -q <lane> <seat>/clone`, then in the clone `python3 -I -B tools/round-27/c1-rename-identity.py --root . --rev <REV>`. Counter sha256 `e0a07995…bb7` is the same as the frozen value in claims.json. Run at 15:35:53Z to 15:36:39Z.
   - 97358f75: exit 1, `rows_complete=15/16 entry_ok=1`. 4084d897: exit 1, `rows_complete=15/16 entry_ok=1`.
   - 9dca26df: exit 1, `rows_complete=15/16 entry_ok=0` (`entry: entry absent`). c6d619a3: exit 1, `15/16 entry_ok=1`.
   - The only INCOMPLETE line at each revision is: `INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run`.
   - Verdict: holds.
2. **The base and repeat runs were two separate calls.** Observation for the file facts, inference for the conclusion. Command: `TZ=UTC stat` plus `cat` of the `.times`, `.exit` and `.argv` receipts under `seats/RunTxD/envelopes/`, plus a read of `run-tinyxxd.sh`, at 15:35:28Z, exit 0.
   - The base and repeat envelopes are different files (inodes 1485150810 and 1485150815).
   - Base: created 14:55:49.736, last written 14:55:50.467. Repeat: created 14:55:50.494, last written 14:55:51.205.
   - Each stderr file was created at the same nanosecond as its envelope (49.736460073 and 50.494463547). The script redirects both output streams of one `npx` call, which creates both files together.
   - Each envelope was last written about 0.7 s after it was created. That fits output landing when the `npx` process exits. A plain `cp` writes 51 KB almost instantly and does not create a stderr file.
   - Receipts: `.times` base `14:55:49Z 14:55:50Z`, repeat `14:55:50Z 14:55:51Z`; `.exit` 0 for both; the two `.argv` values are the same frozen template. The base `.times` file was written at 50.4935 and the repeat envelope was created about 1 ms later, which matches the script running one call after the other.
   - `run_one` skips any run whose envelope file already exists, so the script cannot overwrite a run.
   - All stderr files are 0 bytes (sha256 `e3b0c442…b855`).
   - Verdict: holds. This is an inference from scratch metadata; no committed lane byte proves a call happened (already disclosed from `MutC1Time.md` in the lesson). The REA `tmp/` folder holds only the Node compile cache, so it gives no separate per-call trace (unknown).
3. **The lane `runs.tsv` matches the seat records, and only one envelope sha256 is shared.** Observation. Command: `git show 4084d897:corpus/evidence/round-27/c1/runs.tsv | grep … | cut …` and `cut -f10 | sort | uniq -d`, at 15:37:13Z, exit 0.
   - The base and repeat rows have exit 0, times 14:55:49Z–14:55:50Z and 14:55:50Z–14:55:51Z, and the same sha256 `f601872b…3130`.
   - The file has 49 lines (header plus 48 runs). The only duplicated sha256 is `f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130`.
   - The lane's committed base and repeat blobs are both `7a34b312…`, and their sha256 is `f601872b…`, the same as the scratch originals.
   - Verdict: holds.
4. **The extra run was not substituted.** Observation. Commands: `git hash-object` of the extra envelope, then `git ls-tree -r 4084d897 | grep -c <blob>` and `git grep -l 81a069abb9c70a860d 4084d897`, at 15:37:13Z, exit 0.
   - The extra envelope's blob `647a35a1…` appears in the tree 0 times.
   - Its sha256 `81a069ab…` appears only in `.ufo/waves/round-27/w1/RunTxD.md`, as a disclosure.
   - Its meta is `{'command': 'inspect-binary-layout', 'duration': '171ms'}` and its id is the same `ev_aeeab0db…`. `cmp -l` against the base shows 2 differing bytes, both inside the duration value.
   - Timing: `counter-sandbox.out` (the refusal) was written at 15:06:54Z, `duration-collision-proof.out` at 15:07:24Z, and the extra run happened at 15:09:45Z. So the extra run was made after the refusal was known, which means it was picked with the outcome in view. Using it would have been exactly the reuse or outcome selection the gate exists to refuse.
   - Verdict: holds.
5. **Every surface that reports R27-C1 says missed and never counts it as met.** Observation. Commands: `git grep -n -i -E 'R27-C1|15 of 16|15/16|…' 4084d897 -- <surfaces>`, plus reads of the lesson, the entry, PROVINCE and the `corpus/README.md` diff, at 15:36:01Z to 15:37:26Z, exit 0.
   - SCORECARD:3090 heading says "honest stop, 15 of 16". The SCORECARD:3096 verdict says "target missed: honest stop … No run was substituted." SCORECARD:3101 says "The claim as frozen is not met, and this card does not count it." Holds.
   - LOG:2972 says "honest stop, 15 of 16". LOG:2977 says "15 of 16 rows, entry_ok 0 → 1, exit 1 (missed by one row; honest stop …)". Holds.
   - Entry Limits, lines 88-92: "Counter result at the data commit `9dca26df…`: 15 of 16 rows complete … the frozen counter refuses …". This matches check 1 at 9dca26df. The entry never says "met". Holds.
   - Lesson `corpus/lessons/round-27.md`: it never says met. It also never states the R27-C1 outcome: the `## Claims` section gives only the before value, and the miss shows only indirectly through M27-2. The round-26 lesson has no outcome line either, so this is the lane's existing pattern, not a regression. Holds narrowly.
   - `claim-freezes.tsv:15` and QUALITY row 40 contain no met wording. Holds.
6. **PROVINCE and `corpus/README.md` are silent about the miss.** Observation for the text, inference for the impact.
   - PROVINCE:311-318 is a dated Core addition saying "10 of 16 content-keyed, 6 rename-sensitive, 0 unstable".
   - `corpus/README.md` adds a map row marked "held narrowly" and the same "10 of 16 … 0 unstable" line.
   - Neither says that R27-C1 missed, or that one of the 16 verdicts comes from the ids by hand because the counter did not accept that row.
   - They do not count the claim as met. But they present the full 16-pair result as settled lane knowledge, while SCORECARD says the card does not count it.
   - Verdict: **fails narrowly (disclosure gap).** Counterexample: a reader of PROVINCE alone cannot tell that the 16-row table missed its frozen gate.
7. **Is calling it a miss too harsh or too lenient?** Inference, grounded in the frozen text.
   - Too harsh? No. claims.json `rules` says "distinct envelope sha256 equal to the file bytes", and the counter's own header says "all 48 differ". The target is 16/16 with exit 0.
   - A 6.5.0 envelope carries no wall-clock time; only `meta.duration` varies. So the bytes cannot tell a genuine tie from a copy, and the counter has a red selftest case for exactly that (`reuse-one-run`, "shared with another run").
   - The only ways to a pass were a post-freeze counter change or the outcome-selected extra run (check 4). Both are forbidden. The strongest case for the L1 is that the claim's substance re-derives on all 16 rows. That is a real tradeoff, not a defect the judge can fix: the claim is defined "as coded in the pinned counter".
   - Too lenient? Partly, on surfaces outside the scorecard. SCORECARD and LOG are exact. But check 6 shows the missed claim's whole result promoted to PROVINCE Core without qualification.
   - LOG:2977 calls the repeat "genuine" without an inference label. Check 2 supports that word only from uncommitted scratch metadata.
   - Verdict: the miss is correct and is neither too harsh nor too lenient on the scorecard. It is slightly lenient in PROVINCE and the README map.

## Impacted axes

Depth (R27-C1 reporting), and calibration (the PROVINCE and README map wording against the SCORECARD verdict). There is no impact on R27-C2.

## Smallest safe correction (for the L1; this seat edits nothing)

- Append one sentence to the PROVINCE:311 bullet and to the `corpus/README.md` round-27 row and update line: "Claim R27-C1 missed at 15 of 16 under the frozen counter (tinyxxd `inspect-binary-layout` repeat byte-identical to base); that row's verdict re-derives from its ids by hand only."
- Label "genuine" at LOG:2977 as `[INFERENCE]`, citing the RunTxD scratch file times.
- Optionally, add one outcome line to the lesson's `## Claims` section ("after: 15/16, entry_ok 1, exit 1, missed").

## Artifacts (/fast/scratch/hyaku/kaidoku-r27/seats/w2/CriticC1HonestStop/; the sandbox clone was deleted after use)

- 30e5ce027cfe9da8ca9c9f4a8d710445b096e60fd1aeae976e0b13b00b072640 counter-97358f759a531f7ebc0354fb937d546da8d3b8bd.out
- a02047192099a8546be7162dbff293fd108e8357be225be30f67fa0e463ccfb8 counter-4084d8975b684a8837b1c858eea0008ce9ab49e0.out
- 2f8842285e86565fb2349522164ea9966ebc95c474b99708c3134ed857ab6882 counter-9dca26df135a2c558aaa575534ad42662b372d5d.out
- 1233fa550ef115cf44c00770bfa8b42db7a72857f4c5ce4505b70a6b444d4d64 counter-c6d619a3c50e39dbb830de28146362e360d170d7.out

No tool was installed or upgraded, no REA call was made, and nothing in the lane was written except this report. In the lane I used only read-only git commands; nothing was run with jj.
