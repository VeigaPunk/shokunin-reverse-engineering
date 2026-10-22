# ReviewFreezeRow: round-27 claim-freeze row against the freeze gate

Seat: KaidokuR27.ReviewFreezeRow (wave 2, round 27, attempt 1). Read-only on the lane.
Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Tip checked: main = 4084d8975b684a8837b1c858eea0008ce9ab49e0 (HEAD is detached at that commit).
Freeze commit a4f674b343d8564e21f7eb8984630a95089c82d6. Pointer revision 97358f759a531f7ebc0354fb937d546da8d3b8bd. Base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0.
Attacked: the round-27 findings set in corpus/claim-freezes.tsv, and the row's facts (freeze commit, pins, receipt paths, probe, critic record).

## Verdicts

1. Findings set: HOLDS. The gate at main reports FLAGGED with INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED. The ledger row has the same verdict and the same sorted codes. The same codes come out at 97358f75, the row's pointer revision.
2. Pins: HOLD. Both counters match their claim pins at the freeze and at main. No commit after the freeze touches a counter or the claims file.
3. Receipt paths and probe: HOLD. Every path the row names exists at main. Receipt contents match the frozen before values. The probe envelope's sha256 and evidence ID match the claim.
4. Row wording "red selftests and before receipts ... sha256-pinned before any data": FAILS in part. They are committed at the freeze (holds). No sha256 pin exists for them in the frozen claims: claims.json pins only the two counters. The only sha256 values on record come from wave-1 CriticFreeze.md, whose checks ran from 14:56:19Z (its items 3 and 4), during or after the C1 data runs (14:54:51Z to 14:56:43Z).
5. Gap not disclosed in the row: tools/round-27/assemble-c1.py, added in commit 9dca26df after the freeze, wrote runs.tsv and table.tsv (its docstring calls it an L1 integration step). The frozen claims never name it, so the gate cannot see it. Only wave-1 seat reports mention it ("not mine"). Partial mitigation: the frozen counter re-derives each table verdict (tools/round-27/c1-rename-identity.py lines 311-312; selftest case table-verdict in before/c1-selftest.txt line 11).
6. Outside this item: the whole-file gate exits 1 at main. The only mismatched row is round-26 (ledger FLAGGED INSTRUMENT_ABSENT; gate FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED). The round-27 row is not the cause. The same round-26 mismatch appears at 97358f75.

Overall: the round-27 findings set holds; the sha256 wording fails in part; the assembler is a gate blind spot.

## Checks

Assignment gate command, run from the lane root:
`python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev main --disclosures corpus/claim-freezes.tsv`
C-rows run `python3 -I -B round27-row-compare.py` (scratch copy) with read-only git calls inside. Exit is that command's exit; git return codes are quoted where used.

| ID | Command | Output excerpt | Exit | UTC 2026-10-22 | Verdict |
|---|---|---|---|---|---|
| G1 | assignment gate command | "exact":13,"of":14,"mismatched":["round-26"],"missing":[],"stray":[] | 1 | 15:43:30 | exit caused by round-26 only |
| G2 | same command, --rev 97358f75 | "exact":12,"mismatched":["round-26"],"missing":["round-27"] (row added at 4084d89) | 1 | 15:43:30 | round-27 codes equal row |
| C01 | compare script on G1 JSON and git show main ledger | ledger=FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED; gate= same | 0 | 15:43:30 | holds |
| C02 | compare script on G2 JSON | gate@97358f75 = same three codes | 0 | 15:43:30 | holds |
| C03 | compare script, disclosure block | mismatched=['round-26'] missing=[] stray=[] | 0 | 15:43:30 | holds for round-27 |
| C04 | compare script, round-26 row | ledger FLAGGED INSTRUMENT_ABSENT; gate ...INSTRUMENT_ABSENT,INSTRUMENT_REVISED | 0 | 15:43:30 | fails (outside item) |
| C05 | git show FREEZE:counter, sha256 | c1 e0a079955c16a759 = pin = main; c2 d8de667ff82a46d5 = pin = main | 0 | 15:43:30 | holds |
| C06 | git rev-list FREEZE..main -- counters, claims | commits=none for all three | 0 | 15:43:30 | holds |
| C07 | git log --diff-filter=A; merge-base --is-ancestor | adds ['a4f674b3...']; parent cd32264f; ancestor checks true | 0 | 15:43:30 | holds |
| C08 | git show --name-only --format= FREEZE | claims, 2 counters, 4 receipts or selftests (7 files) | 0 | 15:43:30 | holds |
| C09 | pins key set against row wording | pins cover 2 counters only; not pinned: before/c1-at-cd32264f.txt, before/c2-at-cd32264f.txt, before/c1-selftest.txt, before/c2-selftest.txt | 0 | 15:43:30 | fails (wording) |
| C10 | git show rev:receipt, sha256, at freeze and main | 6095b5f8, 549f85ba, fb6679a3, ecd4a2a3 at both revisions and in CriticFreeze.md lines 87-91 | 0 | 15:43:30 | holds; wave-1 record is post-data |
| C11 | parse before receipts against frozen before | C1 rows_complete=0/16 entry_ok=0 rev=cd32264f exit=1; C2 r26_rows_ok=0/24 red_ok=0/3 capability_row=0 source_row=0 exit=1 | 0 | 15:43:30 | holds |
| C12 | rev-parse blob, sha256, rev-list, receipt | blob 19c6d77a at base, 97358f75, main; sha256 89afa375...; no commit after freeze; after/recompute-pin.txt has the full sha | 0 | 15:43:30 | holds; UNPINNED accurate |
| C13 | git cat-file -e FREEZE:tools/round-27/xpin-attribute.mjs; git log --diff-filter=A | git rc 128 (absent at freeze); added only by 97358f75 | 0 | 15:43:30 | holds |
| C14 | git show main:probe, sha256; jq .data.evidence_id | sha 936601375c6b87b0... = claim; ev_8af5c38f4d26... = claim; added by 9dca26df (after freeze) | 0 | 15:43:30 | holds |
| C14b | probe utc against git log -1 --format=%cI FREEZE | probe 14:45:23Z; freeze commit 11:51:23-03:00 (14:51:23Z) | 0 | 15:43:30 | holds |
| C15 | runs.tsv utc_start column at main | 48 rows; earliest 14:54:51Z; none before freeze | 0 | 15:43:30 | holds |
| C16 | git cat-file -e FREEZE:tools/round-27/assemble-c1.py; claims text search | absent at freeze; not named in claims; added by 9dca26df | 0 | 15:43:30 | gap |
| C17 | git show rev:freeze-gate.py; working-tree sha256 | identical 8a71fe84b943... at 97358f75, main and working tree | 0 | 15:43:30 | holds |
| C18 | git diff --name-status FREEZE main -- tools corpus .ufo, script types | A tools/round-27/assemble-c1.py; A tools/round-27/xpin-attribute.mjs | 0 | 15:43:30 | info |
| P1 | git cat-file -e main:path for CriticFreeze.md, after/recompute-pin.txt, pre-freeze-probe/, before/* | all present | 0 | 15:38:11 | holds |

## Residual risk and verification gaps

- The gate reads only paths named inside claim strings (freeze-gate.py lines 45-47 and 77-115; documented limit). It cannot see unnamed producers such as assemble-c1.py, and it never checks selftest or receipt bytes.
- Timing rests on commit dates, which the gate says are not authenticated. The freeze commit's author date (11:02:27-03:00) precedes the recorded probe run (14:45:23Z), so the commit was rewritten after the probe ran. This is not a defect, but commit dates are not proof.
- Round 24's own claims pin two instruments (count-c1.py and freeze-gate.py) and no producer. I found no lane rule requiring unnamed producers to be pinned.
- I did not re-run the counters or any REA call. Counter results belong to the C1 and C2 seats.
- I did not audit the round-26 row prose beyond its codes.
- C15 rests on self-reported runs.tsv timestamps. REA envelopes carry no wall-clock time, so the start-time gate cannot check them. Wave-1 CriticFreeze.md counterexample A (sandbox, its lines 51-56) shows a probe envelope recorded with a forged utc_start (14:52:00Z) raises no base reason. Its scratch scan (its item 7) found no run envelope older than the freeze; I did not re-run that scan.
- C12 caveat: the counter loads tools/round-26/recompute-ids.py from Git at the counted revision (c1-rename-identity.py lines 110-113), and the freeze holds no pin for it. The gate's REVISED check is the only guard against a later change. Wave-1 counterexample B (sandbox, its lines 57-62) shows a weakened copy removes the "does not recompute" reason for a forged evidence ID.
- The critic's note that the probe envelope lived only in scratch (its item 6) is closed: commit 9dca26df commits it, and its sha256 matches the claim (C14).

## Lane touch and tooling

- Installs or upgrades: none. Tools used: python3 3.14.8, /usr/bin/jq 1.8.2 (already on the host), git read commands, sha256sum.
- Lane writes: this report only. One early `git status --short` (15:36:08Z) ran without --no-optional-locks; it can refresh the index stat cache. It listed only untracked files. I changed no tracked content, ref, commit or index entry.
- Working tree at 15:45:48Z (`git --no-optional-locks status --short`): six tracked files are modified and uncommitted (PROVINCE.md, SCORECARD.md, SKILL.md, corpus/README.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md). They appeared after 15:36Z and were not evaluated. The ledger, the gate, claims.json and both counters are not in that list, and the checks read Git objects at main, so the verdicts above stand for main.
- No REA calls, no subagents, no background jobs.

## Artifacts (scratch: /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewFreezeRow/)

- round27-row-checks.log e019a08ee3259107e2eea90271fb7f9fc6b6a4aeb93e0d41c851ef3bdf121043
- round27-row-checks.sh a26b84628457cb13b39d68430a51c3339099f63f215676556a3c9fdadf0953ef
- round27-row-compare.py b91f1b493718baebc24d19e585b49344eff4c7445a5fc0e4f72c2a9b17e337f1
- gate-main-final.json 1bcae80e3c8f3dc6f21d588e3b4051eb444a1d7d320ec3a4ca0ca79d31e6951c (same as first run gate-main.json)
- gate-main-final.err e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- gate-97358f75-final.json 1f5ce4e9c96fdd5dfdbbae8d5805e4b5168f8815d2aa3afa7b21e09b09b59ce1 (same as first run)
- gate-97358f75-final.err e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- freeze-to-main-tools-corpus-ufo.name-status.txt c0dfffd5d1d825d5e230b5514a37785ec82e4bcc21912a3e1cee350e9f959e7d
