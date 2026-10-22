# MutR25Calib — mutation test of the round-25 calibration instrument (routed defect 3)

Seat: KaidokuR26.MutR25Calib (mutation-tester, leaf). Date 2026-10-22 (UTC). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`.
Instrument under test: `tools/round-25/a2/c1-calibration.py` (round-25 R25-C1, five items I1-I5).
Sandbox clone: `/fast/scratch/hyaku/kaidoku-r26/seats/MutR25Calib/clone` (branches `mut/*`).
Seat scratch: `/fast/scratch/hyaku/kaidoku-r26/seats/MutR25Calib/`.

## Verdict

**Routed defect 3 confirmed by mutation.** The round-25 instrument accepts eight of nine
mutants (exit 0, `mismatches: 0`) whose self-assessment statements are false at the mutated
commit. Only the control mutant M8 (same broken coverage row, no decoy) is rejected (exit 1),
so the instrument does discriminate on that path and the decoy is what makes the difference.
Every mutant is a single plausible edit; each was committed in the sandbox clone on top of
`c27f445e` and read by the instrument from the Git blob at that commit.

## Method (commands, all run in the sandbox clone)

- Build: `git checkout -B mut/<id> c27f445e…`, edit one file, `git commit`.
- Detect: `python3 -I -B tools/round-25/a2/c1-calibration.py --root . --rev <mutant rev>`.
- Package: `git format-patch -1 --stdout > fixtures/<id>-<slug>.patch`.
- Restore: `git reset --hard c27f445e… && git clean -xdf`, then re-run the detector and re-hash
  the five touched files (hashes below are identical to the pristine values after every mutant).
- Extra check for M5: SCORECARD recipe A (command A) run verbatim at the mutant commit.

Pristine baseline (2026-10-22T12:11Z): `mismatches: 0`, exit 0 — so a mutant that still exits 0
is a false accept, not a broken detector.

## Mutant table

| id | mutation (file) | round-25 instrument result | verdict | fixture (sha256) |
|---|---|---|---|---|
| M1 | decoy `\| coverage \|` row inserted before `## Owned axes`; owned-axes coverage row changed to 99/99 (SCORECARD.md) | I4 `stated [108,108] observed 108`, exit 0 | survived — false accept | M1-decoy-coverage-row-before-owned-axes.patch (c114b14c749e51ba29e6d93d8974dced1e7131e480def713905feab62ed706ef) |
| M2 | SHONEN boundary pointer `PROVINCE.md:95-116` → `PROVINCE.md:119-160` (SHONEN.md:12) | I5 `stated [119,160]` inside `observed [95,266]`, exit 0 | survived — false accept | M2-shonen-pointer-to-core-tables-inside-adjacent.patch (694d0fc588abca6812c12ef301316360fa02a2a6e58a4795a81b5db622771e4e) |
| M3 | SCORECARD round-24 verdict line negated, both tokens kept (SCORECARD.md:3048) | I1 `match true`, exit 0 | survived — false accept | M3-scorecard-negated-r24-verdict.patch (8244ff5c131203b881d846b1eaa7013a116ea00266b6789496b896d1df215b6e) |
| M4 | QUALITY row 34 replaced by a background mention of the spot-check, no criterion (corpus/QUALITY.md:44) | I3 `match true`, exit 0 | survived — false accept | M4-quality-mention-not-criterion.patch (5bdf37d52dff8c533725b8ac79ac93d6101d3b6606628cd5219cf5aec909b30a) |
| M5 | README `## Coverage map` drops the round-25 EVM stem; SCORECARD still says 108/108 (corpus/README.md:74) | I4 `stated [108,108] observed 108`, exit 0 | survived — false accept | M5-readme-map-stem-removed.patch (2717e45220ed7df87a83a93d6e4ef4f5cdc4fadb828598f4c3890425f706cee3) |
| M6 | SHONEN no-cross-domain-bleed box `- [~]` → `- [x]` (SHONEN.md:11) | I5 `match true`, exit 0 | survived — false accept | M6-shonen-box-promoted-to-checked.patch (3c5f4d46d2ea5c64536be2889804d7b35d7a8bea6174866e52b02a7c06eeddcd) |
| M7 | LOG round-24 verdict line negated, both tokens kept (LOG.md:2954) | I2 `match true`, exit 0 | survived — false accept | M7-log-negated-r24-verdict.patch (932ac18d3e5adefb79535fdad55ff44896fd632e516e140c8f63beed2cc370fe) |
| M8 | control: owned-axes coverage row 99/99, no decoy (SCORECARD.md:23) | I4 `stated [99,99] observed 108`, exit 1 | killed | M8-control-wrong-owned-axes-coverage-row.patch (e99a2566b22898803b24cec033889ccfe926b3e5f64724371825efd34c37397b) |
| M9 | SHONEN box `- [x]` and "alignment is contested" rewritten as "settled by the 6.5.0 observations" (SHONEN.md:11-12) | I5 `match true`, exit 0 | survived — false accept | M9-shonen-box-checked-contested-settled.patch (15e5c7b5aa87139522fc1e0072349fd7e3f314552ba57cbe06dea859413757bb) |

## Why each survivor is a real defect (observation)

- M1 — the instrument takes the **first** `| coverage |` line in the file (`next(... score.splitlines() if ln.startswith("| coverage |"))`),
  so a decoy above `## Owned axes` shadows the owned-axes row. The owned-axes row at the mutant says 99/99
  while the tree holds 108 knowledge files (command A at `c27f445e`: `knowledge_files 108`).
- M2 — I5 only requires the pointer to lie inside PROVINCE's first `## Adjacent` span (95-266). PROVINCE.md:119-160
  holds `### Round-4 additions to Core` tables, not the refusal list the SHONEN line names. C1Cherrypick predicted this
  exact false accept path ("a pointer such as `PROVINCE.md:119-131` … would pass I5").
- M3 / M7 — `records_verdict` is a same-line token test (`SPOT in ln and "rejected-honest-stop" in ln`); a negated
  sentence keeps both tokens, so a card that says it does **not** record the round-24 verdict still counts as recording it.
- M4 — I3 asks only whether some `^\| \d+ \|` QUALITY row mentions the spot-check file; a row that names the file as
  background and derives no criterion satisfies it, while the round-24 disagreement again has no QUALITY criterion.
- M5 — I4 counts `corpus/knowledge/*.md` files and never reads `corpus/README.md`. At the mutant, command A gives
  `mapped 107`, `knowledge_files 108`, `missing ["2026-10-22-r25-evm-selector-name-resolution"]`, so the row's
  "108/108 knowledge files mapped" is false while the instrument still reports `observed 108`.
- M6 / M9 — I5 never reads the box mark or the asserted wording, so `- [x] No cross-domain bleed (PROVINCE.md still
  accurate)` passes. In M9 the following line also turns the stale contested clause into "settled by the 6.5.0
  observations", which the live PROVINCE pins (6.7.0/207/153) contradict.

## Coverage findings for the frozen round-26 rule text (inference; CounterC2's instrument decides)

Seat-local preview of the claims.json K1-K6 text (`k-preview.py`, base `c27f445e`: 5 mismatches of 6, K3 holds,
matching the frozen before expectation):

- K4 as frozen sees M1 and M5 (it reads the coverage row inside `## Owned axes` and reads the README map).
- K6 does not see M2 (a pointer inside PROVINCE's line count passes) nor M6/M9 (no rule reads the box mark or the
  asserted wording; in the preview M9 makes K6 pass outright).
- No K rule reads SCORECARD/LOG/QUALITY verdict-recording lines, so M3, M4 and M7 are outside the K1-K6 scope.
- At base the craft span is `SKILL.md:81-314` (heading line 81, next heading 319, last non-blank line 314); K2 wants the
  literal string `SKILL.md:81-314`, while the depth evidence cell says `SKILL.md:81-318`.

## Restoration evidence

After each mutant the clone was reset to `c27f445e` and re-measured: detector `mismatches 0`, exit 0, `git status`
empty. Pristine sha256 (identical before and after every mutant): SCORECARD.md
`cfe8b5257c90b14b3f7cbe1349d6117a78494632096ab1fa2594e189038d977a`, SHONEN.md
`120cd2b3bb5f9e0c2bcc943bf8cf74c6c35cf887e85fe2caa660901d36ff2ddb`, LOG.md
`60dc8c45c4f6637de56d96aa91e8e1ac47a7184023f3ac82da43c729e8dd18f6`, corpus/QUALITY.md
`e200c853a31c00fc15ff56c6889f2bffa01a612393a4ee115188c35c4e9cbfb0`, corpus/README.md
`8369cb9c20611df8ba9f4df6b9c6981231c542daeba2d48aaed6f4bfb2624797`.

## Artifacts (all under the seat scratch; the L1 integrates and commits)

- `fixtures/*.patch` — the nine mutation patches (sha256 in the table above).
- `runs/M1.json` (467d5572bdad7be37c946071d06ff996af962b3aaa439d1a6c78544cd0e38ce0), `runs/M2.json`
  (1b00b4ae4115884bea003beabdb2ef9c729b0b252b3b957f1d4c66d3ebd37982), `runs/M3.json`
  (fcf9169bbc2ea57adb748a548e85c4fe7d6c1c4ec1c9a7780ffc90d0fcc52565), `runs/M4.json`
  (eee91d52e379f26e07daee92d0b4e95d0ab61b84ad8e1ce1453fcff14d4af50f), `runs/M5.json`
  (979f67cd46981b2c8fe7835aa103f46eb423aa0b3b4060b42bb92052586d0309), `runs/M6.json`
  (0af72653f238d36d102f42278a8cf914e5f611920c90246d34547832bc54025c), `runs/M7.json`
  (dbb96a805bd1cd41afe9777d6ad1d50e78166e6df38001655bfbd339590c299b), `runs/M8.json`
  (fbc9a52369b8381ec3a2e4c92a91d5116964049e648bd9211ee49154619a24f1), `runs/M9.json`
  (6285eeb93ef3106dcb39a2edc82e39a0ab3f163b35e8c40211ff9f0b9b423dea) — detector output plus exit code, UTC stamped.
- `runs/M5-commandA.json` (f07c2ae4a6ebc7c1ccc25cb8365c887bb6fb68e33cb24138030e5e2a537f2c6f) — command A at the M5 commit.
- `runs/k-preview.json` (1dd75b7fc5b4c78fc7b0aa5bcc9067e3f12f654c36b6c8318b5ef4888ad0cd61) and `k-preview.py`
  (f9df636be802dd6142f078eb046dc6e139f82d222acea11db2753e2476d11053) — seat-local K1-K6 preview.
- `clone/` — sandbox clone holding the nine mutant commits on branches `mut/*`; left at pristine `c27f445e`.

## Cross-check by peer seat (reported, not re-run here)

`KaidokuR26.CounterC2` states that the nine patches were applied in their sandbox and measured with the new
round-26 instrument (`tools/round-26/c2-calibration.py`, seat copy sha256
`3b0f6507e7f77fd1763fc26f2b68922bdb09f8e8f3f27149d0899a21b3a37e8e`): M1, M5 and M8 killed by K4 (M1, M5 and M8
rebuilt as selftest cases), M6 killed by K6, M3, M4 and M7 not observable to K1-K6, M2 and M9 surviving as
disclosed limits. Their base count (items 6, mismatches 5, exit 1, K1/K2/K4/K5/K6 failing, K3 passing) matches my
seat-local preview. This seat did not run or edit that instrument; that measurement is their report. Precision
point relayed: M6's K6 kill is inherited from the base word "contested", not from the box mark, so M9 (which
removes that word) is the sharper probe of the box-mark gap.

## Bounds, tooling, sources

This seat wrote exactly one lane file, this report; all mutant edits were applied inside the sandbox clone only
(`git diff corpus/README.md | grep -c 'entry not listed in the map'` returns 0, so no mutant text reached the lane).
Concurrent lane changes now visible in `git status` (corpus/README.md, corpus/SOURCES.md and the new round-26
corpus files) belong to sibling seats and were not touched here; the lane HEAD is still `c27f445e`. No Git or jj
write was issued in the lane or at the fleet root, no tool was installed or upgraded, no web source was opened
(the mutant study needs none), and REA was not invoked.
