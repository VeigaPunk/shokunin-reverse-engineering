# LessonReview: round-26 lesson Gate and Mistakes (wave 2, falsify seat)

Seat: KaidokuR26.LessonReview (leaf, no subagents). Checks ran 2026-10-22, 12:59Z to 13:08Z.
Judged bytes: corpus/lessons/round-26.md at lane HEAD fe3eb4ed (blob f6d65b63, file sha256 28f55b8f). The file is byte-identical at ebe2cb4a and c327772.
Lane tree: uncommitted edits to .ufo/waves/round-26/w1/ files and corpus/QUALITY.md (adds row 36), plus untracked wave files (git status --porcelain, exit 0). Not judged.
Scratch: /fast/scratch/hyaku/kaidoku-r26/seats/w2/LessonReview/ (clone/ at fe3eb4ed, out/, out/mut/).
Installs or updates: none. Used curl, python3 standard library and jq, all already present. No REA call, no MCP, no jj, no Git write in the lane. This file is the only lane write.

## Per-row verdicts

Gate header: sources opened 2026-10-22; each quote contiguous and at most 25 words. Length holds (quotes are at most 7 words). Contiguity does not hold (G2).

- S079, line 27 (six installed rea-agents 6.5.0 files): PASS with defect G1.
  - Source: all six paths exist; package.json reads 6.5.0.
  - Date: "opened 2026-10-22" is self-reported and not checkable from the bytes.
  - sha256: 6 of 6 match computed bytes (python3 hashlib, exit 0).
  - Quote 1 (7 words): verbatim at evidence.js:182.
  - Quote 2 (6 words): matches evidence.js:160-162 only after whitespace normalisation (G1).
  - Section cell: supported by evidence.js:156-180 (projection holds subject digest, format and architecture, no path).
- S080 integrity, line 28: PASS with G2. Version document fetched 2026-10-22T13:01:01Z, curl exit 0, 21,678 B, sha256 52184d31 matches.
- S080 shasum, line 29: PASS with G2. Same document; dist.shasum equals the quoted value (jq exit 0).
- S080 packument time, line 30: PASS with G2. Packument fetched 13:01:01Z, 327,312 B, sha256 bfa6974e matches; time["6.5.0"] equals the quoted value.
- S080 attestation, line 31: PASS with G2 and G3. Attestation fetched 13:01:01Z, 14,481 B, sha256 af5a2c20 matches. The SLSA v1 predicate (attestation index 1) holds gitCommit 3b79af28 at resolvedDependencies[0].digest.gitCommit.
- Search paragraph, lines 33-37: S037 is the rea-agents 6.7.0 row (grep, exit 0), as stated. SOURCES.md diff a0639d8e..HEAD removes zero lines (exit 0), so no older row changed.

Gate defects:
- G1 (Low): S079 quote 2 spans three lines (evidence.js:160-162, indented, trailing comma). `grep -n` finds no single line containing it. Content is correct.
- G2 (Low): all four S080 quotes differ from raw bytes by one space after the colon. Raw registry JSON is compact: `"integrity":"sha512-…"` occurs once, the spaced form zero times; same for shasum, time and gitCommit (byte counts, python3, 13:01Z). Values match. The header's "contiguous" claim is false for 5 of 6 quotes.
- G3 (Info): the attestation index is not named in the pointer.

M26-1, line 43: PARTIAL.
- Pointers resolve and match at HEAD: C1Mutation.md:38, :61, :89; C2Mutation.md:42, :51, :59, :112; round-25-verifier-spotcheck.md:190-192; QUALITY.md:39, :42, :43 (git show HEAD, sed, exit 0). Exception: `.ufo/reports/round-25/kaidoku.md:19` (F3).
- Row 29 is described as limited to "a red repair demonstration". Row 29 has no such limit; row 32 does (F6).
- C1 red runs: shown. Selftest 16 cases, failures 0, 12 red cases exit 1. Base receipt rows_complete 0 of 8, entry_ok 0, exit 1.
- C2 red runs: shown at base. Selftest 18 cases, failures 0. Base receipt 5 of 6 mismatches (K1, K2, K4, K5, K6), K3 passes.
- C2 decoy red case: not shown as stated (F1).
- Status sentence "Not yet observed": wrong at HEAD (F2).

M26-2, line 44: PASS for pointers and counts. Evidence is a hand count (F9).
- Pointers resolve and match: spot-check :18-23; LOG.md:2960 (path elided with an ellipsis); w2-dispatch.json counts {"spawn":32,"resume":0,"total":32}; w2 registry has 32 members, all agentId null; w2/ holds only that file; wave-dispatch-counting.md:21 (rule 1).
- Counts reproduce (jq, exit 0): w1 registry 65 members, 32 null and 33 set; 33 .md report files in w1; w1 dispatch spawn 33; w2 registry 0 spawned.
- Not checked: the "8 attack seats (reviewer 4, critic 2, mutation-tester 2)" split, which needs the round-25 task result.

M26-3, line 45: PARTIAL. Red run NOT SHOWN (F4).
- Counts reproduce (git show REV:corpus/SOURCES.md | grep -cE, exit 0): 72 at 18e7eb6d; 74 at 7ef837a4; 78 at 1e064f9b, cce7504a and a0639d8e; 80 at ebe2cb4a and HEAD.
- Pointers: spot-check :49-52 and :198-199 match; claim-freezes.tsv line 13 reads round-25 FLAGGED. Fleet report :49 and fleet prompt :109-110, :111-114 match, but only in the fleet root (F3).
- No counter for this check exists in tools/round-26/ (c1-id-identity.py, c2-calibration.py, recompute-ids.py), and before/ holds no red run for it.

## Findings

Medium
- F1, M26-1 decoy. The named fixture does not discriminate. m1-decoy-row-before-owned-axes exits 1, but its decoy row reads 99/99 with evidence "decoy" and no measured revision. A whole-file first-match reader also exits 1 on it.
  - Mutant A (whole file, first match, no uniqueness): selftest exit 1, failing only k4-duplicate-row-inside-owned-axes (out/mut/st-c2-mutA-wholefile-firstmatch.json).
  - Round-25 shape (correct decoy 2/2 with measured hash above wrong live 99/99; out/mut/m9shape2.out, 13:06Z): shipped exit 1 failing K4 (correct); mutant A exit 0 (false accept reproduced); mutant B exit 1.
  - The round-25 shape is not a suite case. Fix: add it, and give m1 a correct decoy value and a measured hash.
- F2, M26-1 status. Line 43 says the red runs are "not yet observed" and an L1 "obligation". The C2 receipts were committed at 81f63f36, an ancestor of ebe2cb4a (`git merge-base --is-ancestor`, exit 0), before the lesson. The C1 receipts came later, at bd0c84bc. Fix: state the commit and output of each run.
- F3, pointer root. The lane has no .ufo/reports/round-25/ and no .ufo/prompts/. `git ls-tree -r --name-only HEAD -- .ufo/reports/round-25` is empty; `git log --all -- .ufo/reports/round-25/kaidoku.md` is empty (13:02Z). Both files exist only in the fleet root: .ufo/reports/round-25/kaidoku.md (sha256 ba4d9095) and .ufo/prompts/kaidoku-round-25.md (sha256 c134f584). Pointers at line 43 (:19) and line 45 (:49, :109-110, :111-114) do not resolve from the lane root, and the lesson names no root. Fix: name the root or cite lane copies.
- F4, M26-3 not shown. "Shown able to fail this round" names a counter run and a red fixture; neither exists in the lane, and before/ holds none. Fix: add the counter with its recorded red run, or drop the claim.

Low
- F5 (G1, G2): Gate quotes are not all contiguous as the header states.
- F6, QUALITY wording (line 43): rows 29 and 32 are said to be limited to red repair demonstrations. Only row 32 is (line 42, "in every red repair demonstration"). Row 29 (line 39) is not.

Info
- F7 (G3): attestation index not named.
- F8: lane working tree dirty; not judged.
- F9 (M26-2): the shown-failing evidence is a hand count with no before/ output. The counts reproduce.

## Rerun results (clone at fe3eb4ed; TMPDIR in scratch; outputs in out/)
- c1 --selftest: exit 0; 16 cases; failures 0; byte-identical to before/c1-selftest.txt (13:02:52Z).
- c2 --selftest: exit 0; 18 cases; failures 0; byte-identical to before/c2-selftest.txt.
- c1 --rev a0639d8e: exit 1; rows_complete 0; entry_ok 0; byte-identical to before/c1-at-a0639d8e.json.
- c2 --rev a0639d8e: exit 1; mismatches 5 (K1, K2, K4, K5, K6); identical to the receipt once the root field is removed (jq -S).
- c1 --rev fe3eb4ed: exit 0; rows 8 of 8; entry_ok 1.
- c2 --rev fe3eb4ed: exit 0; mismatches 0; command A mapped 109 (C1 added one knowledge file, as claims.json predicts).
- Mutant A selftest: exit 1; failing k4-duplicate-row-inside-owned-axes only (13:05:46Z).
- Mutant B selftest: exit 1; 11 cases failing, including decoy-outside-owned-axes.

## Sources opened (access 2026-10-22)
- Installed package, six files under /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/. Hashes as in the lesson. Quote at domain/evidence.js:182 (verbatim).
- https://registry.npmjs.org/rea-agents/6.5.0: sha256 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde; quote "shasum": "7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3" (value matches; spacing re-rendered, G2).
- https://registry.npmjs.org/rea-agents: sha256 bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450; "6.5.0":"2026-10-14T12:56:14.513Z" (compact bytes).
- https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.5.0: sha256 af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b; decoded gitCommit 3b79af28e80785afce9f5998d8f03289402a1847.

## Artifacts (sha256, scratch out/ and out/mut/)
- check_gate.py 9b7e7b10; rea-6.5.0-version.json 52184d31; rea-packument.json bfa6974e; rea-attestation.json af5a2c20.
- c1-selftest.rerun.txt 208a14f3; c2-selftest.rerun.txt 272b0c9e; c1-base.rerun.json fcb49c34; c2-base.rerun.json 39640d96; c1-head.rerun.json 4a57e912; c2-head.rerun.json 7121462f.
- mut/make_mutants.py a2b3c17a; mut/c2-mutA-wholefile-firstmatch.py 03e3d1cb; mut/c2-mutB-wholefile-unique.py 1305e22e; mut/st-c2-mutA-wholefile-firstmatch.json 5a5957da; mut/st-c2-mutB-wholefile-unique.json 153aaebd; mut/m9shape2.py 508cd107; mut/m9shape2.out f20ba94f.

## Residual risk and gaps
- Not checked: the "ran after the freeze" timing (M26-1); the 8/33 attack-seat split (M26-2); the round-25 base 18e7eb6d, taken from spot-check text (the object exists); the fleet root's own Git state (file reads only there).
- S079 lives in an npx cache that can be pruned; the registry copies are the durable check.
- S079 quote 2 and the S080 quotes were checked by normalised match only.

Recommendation (not an admission): the Gate hashes and values hold, and the C1 and C2 base receipts are real. Fix F1 to F4 before M26-1's decoy claim and M26-3's "shown able to fail" stand.
