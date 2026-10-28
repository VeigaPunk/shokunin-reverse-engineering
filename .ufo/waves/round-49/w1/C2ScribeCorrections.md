# Round 49 wave 1 — C2ScribeCorrections (pre-freeze, R49-C2 calibration)

Seat: C2ScribeCorrections. Lane `kaidoku-shokunin`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Scope: attack the DRAFT `c2-mismatch.py`, re-open the two sources, draft the C2 landing text, verify it in scratch clones. Nothing in the lane tree was edited, staged, committed or moved with a mutating git command. No tool was installed or upgraded. `c1-run.sh --data-run` was not run. No subagent was dispatched.

## Verdict

**Landing text: green.** The drafted `## Corrections to round 48` lines (A1–A7), the S147/S148 supersession rows, the two search-log entries and the `## Record corrections — round 49` section make the draft counter exit 0 with `mismatches 0`, `battery.failing []`, eleven of eleven mutations flipping exactly their own atom, and a do-nothing overlay with nine atoms red. At the freeze the same counter reports `mismatches 9`, exit 1.

**Draft counter: not freeze-ready as written.** Under the plan's counting command (`--battery`), six forgery arms return exit 0 with `mismatches 0`: F1 (A2 `dead` hash not bound), F2 (A8 `identified` not derived), F3 (A3 pointer set incomplete), F5 (A6 snapshot not tied to the source), F7 (A4 reads a mutable round-48 artifact at REV), F8 (A5 reads a mutable receipt at REV). Two more (F4 duplicate A1 line, F6 inverted A7 teaches) pass their atom and turn exit 1 only by accident of the battery. Section 2 has the exact arms.

**Patch.** `proposed/c2-mismatch.py` (diff `proposed/c2-mismatch.patch`) closes F1, F2, F3, F4, F6, F7, F8 (exit 1, the right atom red), keeps F9 (freeze tool edit, exit 2) and keeps the genuine landing green. F5 cannot be closed offline; it is a disclosed limit (section 5).

**Plan sentences must change with the counter.** The plan is the rule, so the same pre-freeze commit must amend the sentences in section 4.

## 1. Values re-derived from base bytes (independent of the draft lesson)

| atom | value | how derived (base `e4f2cfa5`) | matches draft |
|---|---|---|---|
| A1 declared | `b6f7ca2a6391964dfdedd477cd560bd42159873a` | `git show e4f2cfa5:SCORECARD.md` line 3730, `## Round 48` `**Declared freeze:**` | yes |
| A1 stale | `0f06251bf6a3a6964c715f67243d4df12e854258` | `git show e4f2cfa5:corpus/lessons/round-48.md` line 4 (file sha256 `db4ea9bd…8901`, 5742 bytes) | yes |
| A2 dead | `663f30ee7516942a0120e7de68fe88356e680822` | `git cat-file -e …^{commit}` fails (not a commit); quoted in `corpus/lessons/round-48-verifier-spotcheck.md` line 16 | yes |
| A2 actual | `663f30ee751694fb0970e7de68fe88356e680822` | commit (subject "round-48: the one inherited receipt above 1 MiB"), ancestor of base | yes |
| A3 `log_2e785632` | 3440,3441,3445 | line scan of base `LOG.md` (3450 lines) | yes |
| A3 `log_33f65a91` | 3440,3441,3444 | same scan | yes |
| A3 unnamed | 577a02a5, 8847042a | no base `LOG.md` line contains them | yes |
| A4 seats / reports / missing | 75 / 72 / C1Meaning, C1Battery, ScribeReportNumbers | `r48-w1-results.json` (75 names, no duplicates) against `ls-tree -r` of `.ufo/waves/round-48/w1` (`C1Battery-2/` is a directory, not the seat) | yes |
| A5 c1 raw | `6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e` | `git show e4f2cfa5:.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json \| sha256sum` | yes |
| A5 c1 stripped | `3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77` | same bytes minus one trailing `\n` (the closure's `3cc2d72d`) | yes |
| A5 c2 raw | `d1bb87d883ebfc25210d10073f00e98edf7e83c8a21417e4dc62a0bc28a23914` | same, c2 receipt | yes |
| A5 c2 stripped | `c30628ae7c439754f570476d570ed57db3361c1a3b5178ecb1c97f065c1e1ce8` | same | yes |
| A6 snapshot | `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` (118135 B) | re-fetched live, section 5 | yes |
| A6 quote | 21 words, present in the snapshot, under heading `2. Backdrop to Popper’s Thought` | counter's `html_norm` / `section_of` on the snapshot | yes |
| A7 snapshot | `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` (12725 B) | re-fetched live, section 5 | yes |
| A7 quote | 22 words, present; the snapshot carries `#define EX_USAGE 64`; the quote sits under DESCRIPTION | counter on the snapshot | yes |
| A8 round 48 | rows 144 → 146 (base `61b87d74`, tip `8847042a`); included 1 (S145, `mined`), excluded 1 (S146, `rejected`); no round-48 entry in the search log at either revision | `grep -cE` on both revisions; `grep -c 'Search log'` | yes |
| A8 round 49 | rows 146 → 148 (base `e4f2cfa5` has 146 rows; S147/S148 new, both `mined`) | derived | yes |

S145 and S146 at base have 11 cells each. S145 `used-by` is `corpus/lessons/round-48.md`; S146 status is `rejected`.

## 2. Findings: forgery arms against the DRAFT counter

Each arm: clone the green fixture (FREEZE `8007db6b`, REV `7a79b0a5`), one edit, commit in the scratch clone, run the counter plain and with `--battery`. Driver `forge.py`; raw results `receipts/draft-forge-results.json`, log `receipts/forge.out`.

| arm | edit | draft plain | draft `--battery` | verdict | defect | patched plain / battery |
|---|---|---|---|---|---|---|
| F1 | A2 `dead=` → `663f30ee00000000000000000000000000000000` (non-commit, same 8-hex prefix) | exit 0, mismatches 0 | exit 0 | **FAIL: vacuous** | `dead` is not bound to the round-48 record; the closure quotes `663f30ee7516942a…`, which the counter never reads | exit 1, A2 red / exit 1 |
| F2 | A8 round-49 `Identified 2` → `Identified 57` | exit 0 | exit 0 | **FAIL: vacuous** | `identified` is only checked as `identified >= screened`; plan section says every number is re-derived from the registry | exit 1, A8 red / exit 1 |
| F3 | A3 drop `log_33f65a91=3440,3441,3444` | exit 0 | exit 0 | **FAIL: vacuous** | A3 checks only the keys present, not that the set of named hashes is complete | exit 1, A3 red / exit 1 |
| F4 | A1 wrong duplicate line placed before the true one | exit 0 | exit 1 (`A1 swap … red []`: mutation misses the true line) | **FAIL: accidental** | `out[key] = kv` keeps the last line; a duplicate is silently dropped | exit 1, A1 red / exit 1 |
| F5 | forged `popper.html` carrying the quote and the heading; S147 pin rewritten to its sha256 | exit 0 | exit 0 | **disclosed limit** | A6 trusts committed bytes and their pin; nothing ties the pin to the fetched source | exit 0 / exit 0 (not closable offline) |
| F6 | A7 teaches `EX_USAGE is 64, not 2` → `EX_USAGE is 2, not 64` | exit 0, mismatches 0 | exit 1 (`mutation set incomplete: 10 of 11`) | **FAIL: accidental** | A7 checks token presence (`EX_USAGE` and `64`); the inverted statement passes the atom, and the battery fails only because its mutation string no longer exists | exit 1, A7 red / exit 1 |
| F7 | `r48-w1-results.json` drops `C1Meaning` (74 seats); lesson updated to match | exit 0 | exit 0 | **FAIL: vacuous** | A4 reads the round-48 artifact at REV, not at LANE_BASE; the artifact is not frozen | exit 1, A4 red / exit 1 |
| F8 | `c1-final-33f65a91.json` gets one extra space before its final newline; lesson `c1_raw`, `c1_stripped`, `report_c1` re-digested | exit 0 | exit 0 | **FAIL: vacuous** | A5 reads the receipt at REV, not at LANE_BASE | exit 1, A5 red / exit 1 |
| F9 | append a comment to `tools/round-49/c2-mismatch.py` after the freeze | exit 2, `frozen_path_changed` | exit 2 | **holds** | freeze integrity is enforced as specified | exit 2 / exit 2 |

Patched results: `receipts/patched-forge-results.json`, log `receipts/forge-patched.out`.

Other checks on the draft counter:

- The do-nothing overlay is red on all nine atoms, but only because it removes the lesson file, so every lesson-dependent atom reads "absent". It proves nothing per atom; the per-atom mutations do that work, and they are sound.
- The eleven battery mutations are guarded by a count check (`mutation set incomplete`), so a silently missing mutation cannot pass.
- The freeze walk (`git log -m --diff-merges=first-parent` over `FREEZE..REV` plus the blob comparison) behaves as specified (F9).

## 3. The patch (verified: `proposed/c2-mismatch.py`)

Seven edits, each the direct fix for one arm:

1. Constants `CLOSURE` and `LOG_KEYS = ('2e785632', '33f65a91')`. A2: `dead` must occur in `corpus/lessons/round-48-verifier-spotcheck.md` at LANE_BASE (F1).
2. A3: the set of `log_` keys must equal `LOG_KEYS` (F3).
3. A4: `RESULTS48` and the `w1/` tree are read at LANE_BASE, not REV (F7).
4. A5: the two receipts are read at LANE_BASE, not REV (F8).
5. A7: the teaches cell must contain `EX_USAGE is 64` (`\b`-bounded) (F6).
6. A8: `identified` must equal the number of new registry rows, `want[2] + want[3]` (F2).
7. `lesson_lines`: a duplicated `- A<n>` key becomes `{'__dup__': '1'}`, which turns that atom red (F4).

Verified: the genuine landing (REV `cdc19e47`) is exit 0, mismatches 0, battery green, 11/11 mutations, do-nothing 9 red. The freeze state (FREEZE `5183ac41`) reports mismatches 9, exit 1. The counter's own `counter_sha256` is `e9067d7f…7cccee`.

## 4. Plan sentences to amend in the same pre-freeze commit

The plan must match the counter, or the freeze binds a sentence the counter does not check. Suggested wording:

- **A1**: each `- A<n>` key appears once in the section; a duplicate is a mismatch.
- **A2**: "`dead` must be the hash the round-48 closure (`corpus/lessons/round-48-verifier-spotcheck.md`, LANE_BASE) quotes; it is not a commit, the real one is, is an ancestor of REV, and both share the first 8 hex."
- **A3**: "line `A3` states exactly the round-48 pointer keys `2e785632` and `33f65a91`, each with its LOG.md line numbers at LANE_BASE; the unnamed list is `577a02a5,8847042a`."
- **A4 and A5**: "re-derived from LANE_BASE (`e4f2cfa5`), not REV", for `r48-w1-results.json`, the `w1/` tree and the two receipts.
- **A7**: "the teaches cell contains `EX_USAGE is 64`" (not "names `EX_USAGE` and `64`").
- **A8**: "`identified` equals the number of new registry rows in the window; `screened` = included + excluded; rows and included/excluded are re-derived from the registry." The current plan sentence says every number is re-derived; the counter cannot do that for `screened` without the search itself, so the plan should say which numbers are derived.

## 5. Sources re-opened today (2026-10-28, live)

| source | command | HTTP | bytes | sha256 | matches pin |
|---|---|---|---|---|---|
| SEP Popper | `curl -sSL -o popper.live.html https://plato.stanford.edu/entries/popper/` | 200 | 118135 | `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` | yes; `cmp` identical to the snapshot |
| man7 sysexits.h.3head | `curl -sSL -o sysexits.live.html https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` | 200 | 12725 | `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` | yes; `cmp` identical |

Re-open time: 2026-10-28T21:11:49Z. Both snapshots are copied to `snapshots/` in this directory.

Source-content findings:

- The S145 base locator `2. The Problem of Demarcation` is wrong: the S145 quote sits under `2. Backdrop to Popper’s Thought` (the counter's `section_of` on the snapshot), as the closure said.
- The draft's S147 teaches cell says the quote sits "directly before §3". That is false: the quote ends roughly 540 characters before the `3. The Problem of Demarcation` heading, and the §2 paragraph continues between them. The landing text says "ahead of §3". The closure's "immediately before §3" is equally loose.
- S148's quote is verbatim in the snapshot under DESCRIPTION. The snapshot also carries `#define EX_USAGE 64`, which the S148 teaches cell cites.

## 6. Landing text (drafted in full, real values, no markers)

Directory: `.ufo/waves/round-49/w1/C2ScribeCorrections/`

- `lesson-corrections.md`: `## Corrections to round 48` with `- A1` … `- A7`.
- `scorecard-section.md`: `## Record corrections — round 49` with the A9 line and three sentences of prose: calibration harmed (the false declared-freeze header) and quality harmed (the S145/S146 record errors), what the corrections repair, and what stays routed.
- `search-log.md`: the round-48 late entry (`identified 2, screened 2, included 1, excluded 1; rows 144 → 146`) and the round-49 entry (`identified 2, screened 2, included 2, excluded 0; rows 146 → 148`).
- `sources-rows.md`: S147 (supersedes S145; anchor `2. Backdrop to Popper’s Thought`; snapshot sha pin) and S148 (supersedes S146; anchor `DESCRIPTION`; teaches `EX_USAGE is 64, not 2`; snapshot sha pin). Both have 11 cells, tier A, status `mined`, opened `2026-10-28`, used-by `corpus/lessons/round-49.md`.
- `apply.py`: applies all of the above to a clone (snapshots, lesson file, rows, search log, SCORECARD) and commits there only.
- `forge.py`: the forgery driver (section 2). `proposed/`: the patch.

Notes for the L1 landing:

- The counter reads the lesson at `corpus/lessons/round-49.md`. The L1 writes that file with the corrections section drafted here; it must exist at REV, or A6/A7 `used-by` fails.
- Commit the two snapshots under `corpus/evidence/round-49/c2/`; the rows pin their sha256.
- S147/S148 go after the last S row; S145/S146 stay byte-identical to base.
- The C1 drafts add no registry row and no search-log entry (grep of `artifacts/R49C1Doc/` and `artifacts/R49EntryDraft/` finds no SOURCES.md or search-log text; the knowledge entry mentions S138/S139 only). If the C1 landing ever adds a registry row, A8's round-49 count goes red and must be re-counted.

## 7. Receipts (`receipts/`)

Each counter run used the stated command in a scratch clone of the lane; the exit is the process exit code; the sha256 is over the raw stdout (the counter prints its JSON there). Per-run UTC times are not recorded individually; all runs fall in 2026-10-28 between about 21:05 and 21:25 UTC (file mtimes read 18:xx local, UTC-3).

| run | command | exit | stdout sha256 | FREEZE / REV (fixture) |
|---|---|---|---|---|
| freeze, draft | `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev <F> --freeze <F> --json-out …` | 1 (`mismatches 9`) | `bb2381c30f2d42c4133ec3d3d0152190e2770141722a39fcdb6082053091c0ac` | `77803eaa` / `77803eaa` (first clone) |
| after, draft, battery | `--rev <REV> --freeze <F> --battery` | 0 | `ff9a3c516855219d9f5cdb8e0e60cdba6774aed22c766e31950bb4ea63153158` | `8007db6b` / `7a79b0a5` |
| after, patched, battery | `proposed/c2-mismatch.py … --battery` | 0 | `f294ee99cc36a9d6ad381bcffda652bb4ae24c767de22441ddd84e3c7db155b5` | `8007db6b` / `7a79b0a5` |
| freeze, patched | `proposed/c2-mismatch.py --rev <F>` | 1 (`mismatches 9`) | `e548ba1acca3882760fc4be633778458531fbca85ac5d98224aa268f54a80a39` | `77803eaa` / `77803eaa` |
| **final, draft, plain** | `--rev <REV>` (no battery) | 0, `mismatches 0` | `de30b6239704f48b25c056442a262a1fe963020f689a51fc419a5d440bbb2959` | `5183ac41` / `cdc19e47` |
| **final, draft, battery** | `--rev <REV> --battery` | 0; `battery.failing []`; 11/11 mutations; do-nothing 9 red | `fa82ffb63be1a09182795a2d88a5f542ff7369ce039c453347baecca8e555c6a` | `5183ac41` / `cdc19e47` |
| final, draft, freeze | `--rev <F>` | 1 (`mismatches 9`) | `140299752461f810363b38822319b673e8c19c90fc18540148ad07125a5d9dea` | `5183ac41` / `5183ac41` |
| final, patched, battery | `proposed/c2-mismatch.py … --battery` | 0; same | `6a68da4b3b1d12c71a43d79b1ac239e2eab62b89cbba01adcad68cf49a76d45c` | `5183ac41` / `cdc19e47` |
| final, patched, freeze | `proposed/c2-mismatch.py --rev <F>` | 1 (`mismatches 9`) | `a3110d64705867e19686cfae7b410c21ff7b86117d6372a9e3e125d1247434f8` | `5183ac41` / `5183ac41` |
| forgeries, draft (results / log) | `forge.py` (plain and battery per arm) | section 2 | results `00e2d365bc3abf344d3c4530120350fd938d3212c8c8573a7a4ffba1e54eddea`; log `04ddb50ebcb76e8ebd5f3e98707861203ad1f10a884203e5a8f7b232170f1d52` | `8007db6b` / `7a79b0a5` |
| forgeries, patched (results / log) | `CTR=proposed/c2-mismatch.py forge.py …` | section 2 | results `1aa02f3d3927c2b1287ba9b83d9ff16745f8e9b1b62991db85d10051ec2c233b`; log `c185180972c1f851f0ff42c71fe6c93c59b858711d0a343689ae0f88971e6d8b` | `8007db6b` / `7a79b0a5` |

Caveat on the forgery arms: they ran against the `7a79b0a5` fixture, built before one SCORECARD prose revision. The revision changed only the prose of the `## Record corrections — round 49` section, not its A9 line, and no atom reads that prose. The final fixture (`cdc19e47`) reran the genuine green check after the revision.

Deliverable digests (sha256):

- `lesson-corrections.md` `45733999969f3e1c4eca815e318fb63e46a8881aac2a9b8ef8e09983eefb8056`
- `scorecard-section.md` `ba5e72397ab099c2e93924a0ec76dc23a195a8e89db134484329edfb675f36be`
- `search-log.md` `18d5b34e294f200a669528e5b7e101e9d33dc509680cccfc9ac1edb70321e4c7`
- `sources-rows.md` `b331e388c07e1bad43bc8c878e1b35d65405a9cc9cd2abb7b365b7534b5c98c2`
- `apply.py` `91daffc45065d9ca5421c9b8be69188ec1d1b3719cd22c0a0e459f4600d5fd88`
- `forge.py` `3eb8f66e2491d1678a46a5dc05e14b1c2deac55a54cb4ff5be3c120ec7988bd8`
- `proposed/c2-mismatch.py` `e9067d7fe5e02febdccaf106a10027680eca0eedaa58688d15eeadfa1e7cccee`
- `proposed/c2-mismatch.patch` `72dc9d06a0a4bb922a785177c1cc11191642dc31cc205a316a7d7ae6aa8ef5c3`
- draft `tools/round-49/c2-mismatch.py` `90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f`

## 8. Not run / out of scope

- `c1-run.sh --data-run` was not run; no C1 counter was run.
- The counters never touch the network. The live re-open in section 5 is a separate `curl`, the only network activity in this seat.
- The external truth of the S145/S147 and S146/S148 quotes and teaches was checked only by today's live re-open, not by a committed fetch receipt. The counter cannot check it (F5). Wave 2 should re-fetch both URLs and compare the sha256 pins.
- No tool was installed, upgraded or removed. The scratch directory `/fast/scratch/hyaku/kaidoku-r49/C2ScribeCorrections` was removed after the receipts were copied here.

## 9. Routed to the L1 (single freeze)

1. Fold the seven counter patches (section 3) into `tools/round-49/c2-mismatch.py`, and the plan sentences (section 4) into `plans/round-49-claims.md`, in the same pre-freeze commit.
2. At the freeze, `--rev <FREEZE>` must report `mismatches 9`, exit 1. After landing, `--battery` must exit 0 with `battery.failing []`.
3. Decide F5 explicitly: disclose the A6/A7 snapshot pins as self-consistent only (the plan's limits paragraph says the counter does not judge prose, which does not cover this), or add a committed fetch receipt and state exactly what it proves.
4. Use the landing text as drafted, or re-run `apply.py` on a clone plus the battery after any change to it.

## 10. Disclosure: draft bytecode cache

My first `importlib` probe of `tools/round-49/c2-mismatch.py` (run without `-B`) wrote bytecode into `.ufo/waves/round-49/draft/tools/round-49/__pycache__/`. When I removed that cache it also removed two sibling-seat bytecode files for `c1-counter` and `c1-run` (created 18:09–18:10 local by other seats' imports; regenerable cache, no source changed). No draft source, plan, or snapshot was modified. Later counter runs used `-I -B`.
