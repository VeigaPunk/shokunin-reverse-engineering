# CriticFreeze: attack on the round-27 instruments-first freeze (a4f674b3)

Seat: KaidokuR27.CriticFreeze (critic, leaf). Attacked: lane commit a4f674b343d8564e21f7eb8984630a95089c82d6,
claims file .ufo/waves/round-27/claims.json, both counters and both before receipts.
Overall verdict: the freeze **holds** on timing, pins and receipts. It **fails** cleanliness in two places:
the lane gate flags it, and two counterexamples succeed in a sandbox clone. Ledger verdict: **FLAGGED**.
No REA run was made. No lane file was written except this report. No tools were installed or updated.

## Checks (all commands run in the lane read-only unless marked sandbox; Python 3.14.8, node v24.21.0)

1. Freeze commit files and time. Observation.
   `git log -1 --format=... a4f674b3; git diff --name-status cd32264f a4f674b3`, exit 0, 14:54:51Z.
   Excerpt: "parents cd32264f..." / "author 2026-10-22T11:02:27-03:00" / "committer 2026-10-22T11:51:23-03:00".
   Exactly 7 files are added (A): claims.json, the 4 before files, and the 2 counters. main, HEAD and origin/main all equal a4f674b3.
   Committer time is 14:51:23Z and matches the stated 14:51Z. Author time is 14:02:27Z (the time the jj change was created).
2. Counter sha256 against claims.json `instruments`. Observation, holds.
   `git show <rev>:<path> | sha256sum` for rev a4f674b3 and main, exit 0, 14:55:00Z.
   Excerpt: "c1-rename-identity.py e0a079955c16...43bb7", "c2-xpin-check.py d8de667ff82a...09bd3". Both match the pins at both revisions and in the working tree.
3. Before receipts re-run at cd32264f. Observation, holds.
   `python3 -I -B tools/round-27/c1-rename-identity.py --root <lane> --rev cd32264f...` (and the same for c2-xpin-check.py), 14:56:19Z-14:56:20Z.
   Both exit 1. `diff` against `git show a4f674b3:.ufo/waves/round-27/before/c{1,2}-at-cd32264f.txt` gives diff_exit=0 for both (byte-identical).
   Excerpts: "rows_complete=0/16 entry_ok=0 rev=cd32264f..." and "r26_rows_ok=0/24 red_ok=0/3 capability_row=0 source_row=0".
4. Red selftests re-run (extra). Observation, holds.
   `c1-rename-identity.py --selftest` and `c2-xpin-check.py --selftest`, 14:58:14Z-14:58:20Z, exit 0 both.
   C1 is byte-identical ("selftest cases=22 failures=0"). C2 differs only in the stub `rev=` field (cd32264f, now a4f674b3), because the stubs run against lane HEAD.
   Inference: the receipt was taken while HEAD was still the base. The cosmetic count "cases=6" covers 10 PASS lines (code: len(cases)+2).
5. Lane freeze gate (QUALITY row 33). Observation, **fails clean**.
   `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root <lane> --rev a4f674b3 --disclosures corpus/claim-freezes.tsv`, exit 1, 14:58:55Z.
   Round-27 excerpt: "findings":[{"INSTRUMENT_UNPINNED","path":"tools/round-26/recompute-ids.py"},{"INSTRUMENT_ABSENT","path":"tools/round-27/xpin-attribute.mjs"}],"verdict":"FLAGGED".
   Disclosures: "missing":["round-27"], "mismatched":["round-26"]. The existing round-26 row says INSTRUMENT_ABSENT; the gate derives INSTRUMENT_ABSENT,INSTRUMENT_REVISED.
   The round-26 mismatch is pre-existing and outside this seat; it is reported for the L1.
   Sandbox (clone, xpin-attribute.mjs added in one commit) at 14:59:33Z: "FLAGGED", "INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED", exit 1.
6. Pre-freeze probe disclosure. Observation, mostly holds.
   `sha256sum /fast/scratch/hyaku/kaidoku-r27/l1/probe-function.json`, 14:56:29Z, gives 936601375c6b...5cc0, equal to `envelope_sha256`.
   `jq` on the probe: ok true, command "function", duration "6091ms", evidence_id ev_8af5c38f...01fc, subject.name "tinyxxd", subject sha 7b1e5d0c...ae65.
   procedure.address "0x103d40", name "entry", body.total_bytes 38. Every claims.json `pre_freeze_probe` field is confirmed.
   The file mtime is 11:45:30-03:00, which is consistent with utc 14:45:23Z plus 6.1 s. That is before the committer time and after the author time.
   Gap: the envelope lives only in L1 scratch, not in Git, so the disclosure can be checked only while scratch survives.
   The probe evidence_id equals all three RunTxC tinyxxd/function ids (base, repeat, renamed).
   Inference: the L1 knew one of 16 base ids before the freeze. The claim does not depend on which verdict a row gets, so this gives no outcome advantage.
7. Could round-27 data predate the freeze? Observation: no, except the disclosed probe.
   Git: `git log --all -- corpus/evidence/round-27 tools/round-27 .ufo/waves/round-27 ...` returns only a4f674b3 and three jj keep refs. All four have committer time 11:51:23-03:00.
   The keep refs 0ac9637d, b1d456d1 and f6e99b45 are siblings off cd32264f; 26a60eb4 is a child of a4f674b3. Their instrument and claims bytes equal the freeze, and they hold no round-27 data.
   The counter's commit-time test walks only the ancestry of REV, so the keep refs are irrelevant to it.
   Scratch: `find /fast/scratch/hyaku/kaidoku-r27 ! -newermt '2026-10-22 14:51:23Z'` (excluding npm unpack trees, which have the fixed 1985 mtime, and the node compile cache), 14:57:11Z.
   Only l1/probe-function.json, l1/tmp, and Git objects hardlinked into seat clones are older than the freeze. The renamed carriers are 11:51:33-03:00 and hash to the frozen sha256 values.
   Run seats: the earliest runs.tsv utc_start is 14:54:51Z (RunJqB) and the earliest envelope mtime is 11:54:57-03:00. The probe sha appears in no seat file (`rg -l` gives no hits).

## Counterexamples (sandbox clone /fast/scratch/hyaku/kaidoku-r27/seats/CriticFreeze/clone, branch from a4f674b3)

A. Pre-freeze probe accepted as a row with a forged start time. Verdict: **fails**. Fixable, and it needs no counter edit.
   Commit 89337448: probe bytes as envelopes/tinyxxd-function-base.json; runs.tsv utc_start 14:52:00Z (forged); commit time after the counter.
   `c1-rename-identity.py --rev 89337448` at 14:59:59Z, exit 1. Excerpt: "INCOMPLETE tinyxxd function: table has 0 rows; repeat: ...; renamed: ...". There is no base reason at all.
   Control commit cffd0d2e (honest 14:45:23Z) gives "base: utc_start 2026-10-22T14:45:23Z not after counter commit".
   Cause: REA envelopes carry no wall-clock time (only meta.duration), so the start-time gate rests on self-reported utc_start plus the commit date.
   Impacted: R27-C1 provenance. The claims.json freeze_kind wording "refuses runs that started ... before" overstates this; it refuses runs *recorded* as starting before.
B. Unpinned recompute dependency. Verdict: **fails**. Fixable.
   Commit 9102ea42 (forged evidence_id, honest recompute-ids.py) gives "base: evidence_id does not recompute under the 6.5.0 rule".
   Commit 0a71b19f also appends `compute_evidence_id` returning data["evidence_id"] to tools/round-26/recompute-ids.py (sha 410f866f...). The base reason disappears. Exit 1 both (other rows absent), 14:59:59Z.
   C2-xpin-check.py loads the same file at REV for its "independent" recompute. Inference, not tested: the same weakening affects R27-C2.
   Mitigation that exists: the freeze gate would report INSTRUMENT_REVISED on any post-freeze change to that file.
   recompute-ids.py is unchanged since ebe2cb4a (89afa3756a9b...208b at both cd32264f and a4f674b3).

## Smallest safe corrections (for the L1; nothing here edits the frozen claims or counters)

- At integration, assert that no runs.tsv envelope_sha256 equals 936601375c6b...5cc0. Commit the probe envelope outside corpus/evidence/round-27/c1 (for example .ufo/waves/round-27/pre-freeze/) so the disclosure is checkable from Git.
- At the counting REV, assert `git show REV:tools/round-26/recompute-ids.py | sha256sum` = 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b. Equivalently, require that the freeze gate show no INSTRUMENT_REVISED on that path.
- Disclose each xpin-attribute.mjs commit in claims.json instrument_supersessions (path, commit, reason), or accept INSTRUMENT_REVISED in the ledger row. In either case the ledger findings must equal the gate's set at the REV where the row lands.
- Tradeoff, not a defect: xpin-attribute.mjs is the C2 product, so INSTRUMENT_ABSENT is structural to this claim design. The Rust judge should treat it as disclosed, not as a hidden instrument change.

## Draft ledger row (also in draft.md)

Expected at integration, after the C2 tool lands (if measured at a4f674b3 itself, drop INSTRUMENT_REVISED):

```
round-27	FLAGGED	INSTRUMENT_ABSENT,INSTRUMENT_REVISED,INSTRUMENT_UNPINNED	instruments-first freeze a4f674b3: both counters committed and pinned in the freeze commit (sha256 equal at a4f674b3 and main), before receipts re-run byte-identical at cd32264f; flagged because the counters load tools/round-26/recompute-ids.py (89afa375) at REV without a pin, and the C2 product tools/round-27/xpin-attribute.mjs is named in the claim but absent at the freeze by design and added after; pre-freeze probe 93660137 disclosed in claims.json pre_freeze_probe, envelope not committed; .ufo/waves/round-27/w1/CriticFreeze.md
```

Why FLAGGED: the lane's own gate (QUALITY row 33) derives FLAGGED from the frozen bytes, and counterexample B shows that the unpinned finding has teeth.
Impacted axes: R27-C1 depth (provenance of rows), R27-C2 capability (independence of the checker recompute), and the calibration ledger (exact disclosure).

## Seat artifacts (/fast/scratch/hyaku/kaidoku-r27/seats/CriticFreeze/)

| file | sha256 |
|---|---|
| draft.md | ba50d46fd381987530fda765523bcda9f87c6e782d484cef2874be2d80cb705b |
| raw/c1-at-cd32264f.rerun.txt (= committed copy) | 6095b5f80562097ee0c4f9dd3087f0873db8098ae203ba4b5b18a023437618e2 |
| raw/c2-at-cd32264f.rerun.txt (= committed copy) | 549f85bad7f45706eb5b193b530c7856cf2c87438ea914631eed2b910a27e3d6 |
| raw/c1-selftest.rerun.txt (= committed copy) | fb6679a3d6d82ca8b0ab2a10792dddbfd28c4ce2d30ad58dcafb28c0b692b0b4 |
| raw/c2-selftest.committed.txt | ecd4a2a3941021f38c21461b663d1cd452249049918d31a180f8de107e667f17 |
| raw/c2-selftest.rerun.txt | 51670ca83c2f0669d24f6d2fefbfc6d4b87c40fa9ba96bb7e630fdf23eea0406 |
| raw/freeze-gate-at-a4f674b3.json | 8fc28af80452fe95d5da58039f191a2b90baf6f7c5a4b69dcb6c471e2ee10c9e |
| raw/freeze-gate-sandbox-tool-landed.json | fde72d1a8df2114765fdc1bddf83a35487fb8258bb7f0e5a6461b082be8dc981 |
| raw/sandbox-counterexamples.txt | 89d2d2f98f0f3fc559e23e72d06e8808e00417c91d7104b134f28df4045a76c4 |
| clone/ (sandbox; commits 89337448, cffd0d2e, 9102ea42, 0a71b19f, gatecheck branch) | Git directory, not hashed |
