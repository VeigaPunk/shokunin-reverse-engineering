# R27-C1 recount (wave 2, seat RecountC1)

Scope: re-run the R27-C1 counter at 97358f75 and at the tip, compare the reruns with the frozen receipt, and check the counter sha256 against claims.json instruments. Read-only on the lane. No commits, no index writes, no REA calls.

Verdict: holds. The counter reproduces the lead's receipt exactly at 97358f75 and at the tip: 15 of 16 rows complete, entry_ok 1, exit 1. The one incomplete row is the one the lead names. The counter sha256 matches claims.json.

## Identifiers
- Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
- Frozen rev: 97358f759a531f7ebc0354fb937d546da8d3b8bd
- Tip: main = HEAD = 4084d8975b684a8837b1c858eea0008ce9ab49e0
- Claims frozen at a4f674b343d8564e21f7eb8984630a95089c82d6
- Tools: /usr/bin/python3 3.14.8 and git 2.56.0, both already present. Installed or updated: nothing.
- Seat scratch: /fast/scratch/hyaku/kaidoku-r27/seats/w2/RecountC1/
- The brief's "--rev 97358f75 and --rev main" was read as two runs; "and" was taken as a stray word.

## Checks

1. Counter at 97358f75, command as written: `cd <lane> && python3 -I -B tools/round-27/c1-rename-identity.py --root <lane> --rev 97358f759a531f7ebc0354fb937d546da8d3b8bd` (TMPDIR set to the seat tmp folder).
   Output excerpt: `INCOMPLETE tinyxxd inspect-binary-layout: base: envelope_sha256 shared with another run; repeat: envelope_sha256 shared with another run` then `rows_complete=15/16 entry_ok=1 rev=97358f759a531f7ebc0354fb937d546da8d3b8bd`
   Exit 1. UTC 2026-10-22T15:38:23Z to 15:38:24Z. Verdict: holds. The seat script rerun at 15:39:17Z gave the same stdout.

2. Counter at the tip, same command with `--rev main`.
   Output excerpt: the same 16 row lines, then `rows_complete=15/16 entry_ok=1 rev=4084d8975b684a8837b1c858eea0008ce9ab49e0`
   Exit 1. UTC 2026-10-22T15:38:23Z to 15:38:24Z. Verdict: holds. Compared with the 97358f75 run, the only changed line is the final rev= line (difflib, 15:39:17Z).

3. Comparison with the frozen receipt .ufo/waves/round-27/after/c1-at-97358f75.txt (sha256 dd1fc53fa83708cf815780f3f2671fb2a8f8c24249073df3fd62c639d9650dc6; 19 output lines plus a final line `exit=1`).
   Method: difflib between the receipt body and the 97358f75 rerun body (recount_c1.py).
   Output: 0 diff lines. The receipt's final line `exit=1` equals the rerun exit 1.
   UTC 2026-10-22T15:39:17Z. Verdict: holds (identical).

4. Counter sha256 against claims.json instruments.
   Commands: `sha256sum tools/round-27/c1-rename-identity.py`; `git show <rev>:tools/round-27/c1-rename-identity.py | sha256sum` for main, 97358f75 and a4f674b3; the same instruments object read from claims.json at a4f674b3.
   Output: working tree e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7; claims instruments value for this path e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7; committed copies at main, 97358f75 and a4f674b3 all match. The claims file at a4f674b3 has the same instruments object as the working-tree claims file.
   Exit 0 on each git call. UTC 2026-10-22T15:36:43Z and 15:39:17Z. Verdict: holds.
   Extra, not in the brief: tools/round-27/c2-xpin-check.py, working tree and committed copies, sha256 d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3, matches claims. Holds.

5. Counter inputs unchanged between the frozen rev and the tip.
   Command: `git diff --name-status 97358f75 main -- corpus/evidence/round-27/c1 tools/round-26/recompute-ids.py tools/round-27/c1-rename-identity.py corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md corpus/SOURCES.md corpus/lessons/round-27.md`
   Output: empty. The range 97358f75..main holds one commit, 4084d897 ("round-27: SCORECARD round-27 section with hygiene corrections, LOG entry, claim-freezes row, after receipts, wave-1 spec, dispatch, registry and seat reports").
   Exit 0. UTC 2026-10-22T15:39:17Z. Verdict: holds. This is why the tip count equals the frozen count.

6. Cause of the one incomplete row.
   Commands: `git show <rev>:corpus/evidence/round-27/c1/envelopes/tinyxxd-inspect-binary-layout-{base,repeat,renamed}.json | sha256sum`; reads of runs.tsv and table.tsv at both revs.
   Output: base and repeat are both 51287 bytes, sha256 f601872bf55d5f92f806f1c25e019d8d836a625c5723df4ea9a1db96b5083130. Renamed is 51523 bytes, sha256 bbfbc309da6016f5ab0ffc21a4f624db9cf74f5ab7cfe923e24b23c12f9e929c.
   runs.tsv: 48 rows, 47 distinct envelope_sha256 values; the only shared value is the base and repeat pair.
   table.tsv row: verdict rename-sensitive; base_id and repeat_id ev_aeeab0db1f5c0d0822ee68f0ffa499d456e69b308937865014ba3f526daf7ca6; renamed_id ev_02e910c6b112a96422a5d93a29285de131aea2dcd3a8c758c5e99c1750f21891.
   Counter code: lines 249-250 refuse any envelope hash used by more than one run; docstring line 8 says all 48 must differ. The reasons logged for base and repeat list only that refusal. No identity, path, argv, package, subject or recompute check failed for any of the three runs.
   Exit 0. UTC 2026-10-22T15:37:59Z and 15:39:17Z. Verdict: holds. The lead's description of the cause is accurate.

7. Lane state after my runs.
   Command: `git --no-optional-locks status --porcelain`, at 15:36:43Z and at 15:39:18Z.
   Output: the same four untracked paths both times: .ufo/waves/round-27/w2-dispatch.json, w2-spec.json, w2-task-result.json and w2/. Those belong to other seats. My runs created no lane files; the counter runs with python -B, TMPDIR is the seat folder, and that tmp folder is empty afterwards.
   Verdict: holds for my runs. Other seats may change the four paths.

8. Not run. The counter's --selftest is outside the brief, and it writes test repositories under /fast/scratch/hyaku, outside this seat's folder. No REA call was made: the counter's main path runs only git and in-process Python (lines 86-122 and 204-331).

## Observations
- The 15 of 16 result comes from the frozen byte-uniqueness rule, not from a change in identity. The deterministic repeat is the only case where base and repeat bytes match. [observation]
- Inference, not tested: if that rule allowed a byte-identical repeat, the same data would give 16 of 16 and exit 0. The other checks passed for all three runs, and the table verdict agrees with the envelopes. I did not run a changed counter; the counter is frozen. [INFERENCE]
- Unknown, not examined: why the other 15 base and repeat pairs differ in bytes while this pair does not.
- The two literal reruns ran in parallel through the bash tool; the second reported a temporary-shell note. Exit codes and outputs matched the script rerun.

## Artifacts (sha256), all under /fast/scratch/hyaku/kaidoku-r27/seats/w2/RecountC1/
- recount_c1.py  2530af4f75db22a659ef23420191910ba73de26441a2fde639c89f4bb3fadb30
- recount-c1.log  b6e7d50b7e3d9052d3283b8cbc73241f1ddba2e2d9e87793997bdabc38ba5dee
- c1-97358f75.out  30e5ce027cfe9da8ca9c9f4a8d710445b096e60fd1aeae976e0b13b00b072640
- c1-97358f75.err  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- c1-main.out  a02047192099a8546be7162dbff293fd108e8357be225be30f67fa0e463ccfb8
- c1-main.err  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- Frozen receipt, read only: after/c1-at-97358f75.txt  dd1fc53fa83708cf815780f3f2671fb2a8f8c24249073df3fd62c639d9650dc6

## Residual risk and gaps
- Git reads used committed objects. The working-tree counter has the same hash as the committed copies, so the run and the committed code are the same.
- Files other seats wrote under w2/ were not examined.
- Not run: selftest, other verbs, other carriers.
