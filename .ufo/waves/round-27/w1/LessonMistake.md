# Round 27 wave 1 — LessonMistake

Seat KaidokuR27.LessonMistake. Scope: one new mistake row and one alternate; no product integration.
Axes: evidence accuracy and lesson novelty. Observation: the ordering repair already exists at a4f674b343d8564e21f7eb8984630a95089c82d6; no round-wide after-value is claimed here.

## Drafted row, verbatim

| M27-1 | counting instrument committed after its data despite the freeze promise | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:201-204`; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w2/RerunC1Counter.md:55-61` | partial: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/claim-freezes.tsv:14` flags INSTRUMENT_ABSENT, but M26-1..M26-7 do not mine this ordering failure | Round 27 freezes both counters, red selftests and before receipts together at `a4f674b343d8564e21f7eb8984630a95089c82d6`. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-27/c1-rename-identity.py:244-258` refuses older run starts and envelope first commits; the frozen red receipt is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/before/c1-selftest.txt:5`. Running `/fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/probe.py` on an unchanged real round-26 analyze envelope and its recorded start produces exit 1 and `base: utc_start 2026-10-22T12:11:51Z not after counter commit`; changing only that timestamp removes that reason. Both partial-population runs still exit 1, so this demonstrates the ordering gate, not a complete green claim. |

## Commands, pointer checks, outcomes

Exact argv, individual UTC times, exit codes and complete outputs are retained in /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/commands.json. Pointer text and source digests are retained in /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/source-audit.json.

1. Observation, 2026-10-22T15:03:50Z–15:03:51Z: `python3 -I -B /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/probe.py`, exit 0. It clones the lane into /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone and makes two sandbox-only fixture commits; no lane write or ref update occurs.
2. Observation, 15:03:51.397333Z and 15:03:51.398156Z: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s '--format=%H %ct %cI %s' ebe2cb4a` and the same command with `bd0c84bc`, each exit 0. Excerpts: `2026-10-22T09:47:57-03:00` data; `2026-10-22T09:49:24-03:00` instrument. These are 12:47:57Z and 12:49:24Z: data precedes instrument by 87 seconds.
3. Observation, 15:03:51.399968Z: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show --format= --name-only bd0c84bc`, exit 0. Exact affected-file excerpts: `tools/round-26/c1-id-identity.py` and `corpus/evidence/round-26/after/c1-at-ebe2cb4a.json`. Instrument and its after receipt landed together.
4. Observation, 15:03:51.398913Z: the commit-time command in item 2 with `a4f674b3`, exit 0, reports `2026-10-22T11:51:23-03:00` (14:51:23Z). Its subject is `round-27: freeze claims; commit both counters, red selftests and before receipts before any data`.
5. Observation, 15:04:19Z: `python3 -I -B /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/audit.py`, exit 0, opens and checks every drafted-row pointer. Exact excerpts follow:
   - /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:202: `after-measurement"; C1's instrument landed with its after receipt, after the data. The round-25`.
   - /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w2/RerunC1Counter.md:55: `- ` followed by the listed revisions and `absent, git exit 128.`; :61 records `ebe2cb4a -> 46ebfd2f -> bd0c84bc` inside the longer chain.
   - /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/claim-freezes.tsv:14: `round-26` / `FLAGGED` / `INSTRUMENT_ABSENT`, with `C1 at bd0c84bc after the C1 data at ebe2cb4a`.
   - /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-27/c1-rename-identity.py:245: `if start is None or start < counter_time:`; :257: `if added is None or added < counter_time:`.
   - /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/before/c1-selftest.txt:5: `PASS run-before-counter: exit 1 (want 1) expects 'not after counter commit' rows_complete=15/16 entry_ok=1 rev=HEAD`.
6. Inference, grounded in item 5's complete M26-class extraction: this is not a duplicate. M26-1 concerns missing red demonstrations for round-25 counters; M26-2 undispatched wave; M26-3 wrong before anchor; M26-4 non-failing QUALITY criterion; M26-5 forged evidence; M26-6 same-path generalization; M26-7 misroot. None mines round 26's instrument/data commit ordering. The ledger disclosure is not itself an M26 mistake row.

## Real-byte failure and differential control

Observation: the probe reads the real round-26 analyze base envelope and call row via `git -C /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone show ae8bcd86:corpus/evidence/round-26/c1/envelopes/analyze-base.json` and the analogous runs.tsv command (15:03:50.512891Z / 15:03:50.511972Z, exits 0). The envelope remains byte-identical, sha256 3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb. Only adapter columns required by the new header are added; no historical package-version observation is inferred from those supplied fields.
The actual new counter is invoked twice: `python3 -I -B /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone/tools/round-27/c1-rename-identity.py --root /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone --rev HEAD`.
At 15:03:51.292034Z, exit 1: `INCOMPLETE jq analyze: table has 0 rows; base: utc_start 2026-10-22T12:11:51Z not after counter commit; repeat: runs.tsv has 0 lines; renamed: runs.tsv has 0 lines`.
At 15:03:51.352221Z, exit 1, after changing only utc_start to 15:00:00Z: `INCOMPLETE jq analyze: table has 0 rows; repeat: runs.tsv has 0 lines; renamed: runs.tsv has 0 lines`.
Verdict on attack “reuse a real pre-counter call”: HOLDS for the older-start gate; the dedicated reason appears on real recorded bytes and disappears under the timestamp-only control. Neither state is a full green population. The committed selftest receipt was read, not rerun. The envelope-first-commit branch was inspected, not independently attacked here.
Known limit: the code uses `<`, not `<=`; equal-second times are accepted. Declared timestamps are not independently authenticated by this probe.

## Alternate candidate

Observation from the same 15:04:19Z audit, exit 0: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26.md:36-37 says the 6.7.0 package was read, but `is already row S037's family; no new row for it`. /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26-verifier-spotcheck.md:197-200 says its installed code has no SOURCES row and S037 excludes runtime behaviour. This is routed defect 1, a source-family conflation, also not an M26 class.
Supporting prior falsifier: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w2/PinDiffCheck.md:17 records the changed projection field, `relationship_coverage: evidence.relationship_coverage,`.
The current-round repair is drafted in /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/w1/SrcS081.md:7,47: `drafts the S081 row`. Inference: this is a strong alternate, but the selected ordering repair already has a committed fix and a directly exercised gate. Unknown here: final integration of S081; a sibling draft is not landing evidence.

## Opened source provenance

All opened by local reads on 2026-10-22; full-file sha256 and located quotes, each under 25 words. Additional exact lines are in the source audit.

| absolute path | sha256 | quote and location |
|---|---|---|
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/claims.json | ff45e9ce64b417f11bea12884feb26499d30ce30766bec674f9f0d03a37662b2 | `instruments-first`, :6 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26-verifier-spotcheck.md | d83238ab13f13226a0734a766066405b6d02e3fd264e70497e6fdcc5cb531efe | `C1's instrument landed with its after receipt, after the data.`, :202 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-26.md | 9dd3b569e45993564c0dd047df33551bd31a6f9f3fe807b41f2847aa385f2c08 | `no new row for it`, :37 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/claim-freezes.tsv | db5b0de723dc5c91b0ee7d09f637556bbf488165731505c79918fa1feb252231 | `INSTRUMENT_ABSENT`, :14 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/before/c1-selftest.txt | fb6679a3d6d82ca8b0ab2a10792dddbfd28c4ce2d30ad58dcafb28c0b692b0b4 | `not after counter commit`, :5 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-27/c1-rename-identity.py | e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7 | `not after counter commit`, :246 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w2/RerunC1Counter.md | eb618c82a992a6f19ffb47cc8cf6a70efcc61af7cb8add1d809b03c8de5340fe | `absent, git exit 128.`, :55 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w2/PinDiffCheck.md | 8021f210f17d3b63b932e88daeac7d3905bf5394d51e477e83f0415a1fe96628 | `The only hashed-projection hunk`, :17 |
| /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-27/w1/SrcS081.md | 71ab68d4dcfecd28e6d2d978d14970943158715e5c46688a8170e9fd06aac829 | `drafts the S081 row`, :7 |

## Artifacts and touched surfaces

SHA256 values below were produced by sha256sum, exit 0. The clone is a sandbox only; its three added fixture files are listed. All original cloned files remain reference material, not integration deliverables.

| absolute artifact path | sha256 |
|---|---|
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/draft.md | 4b021ed4f35dd6774a99cc56fe6adebaf68fc55933ca48055ddde680171c8ac8 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/probe.py | 4f498191aa7c5ec874a2605b0a3f018f83aab6a1a70b096b658c049ad37a23e2 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/audit.py | 05fe1c0ba0008add0a0f7f9e88b3f0a2396ce1c7d136730251e57a90b74f4b5e |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/commands.json | 556db70ae1f60c9ac9ae26f75dc81bac34ba0411a124cb9f4a103b672adbf813 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/source-audit.json | 6e50e467fca13c6520a90a1fc4d7ec04979b1f469fe2675dda8f65d10cba378f |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/summary.json | 3ad14b8f88c69c914a93585dbefeda7141cd80e9397f21d3f7802a30640d8fb8 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/real-pre-counter.txt | 32d2ee37b72105d616aeab004f9a765b3a545aae2ecc93422e8f9b6ab92aa673 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/later-time-control.txt | 90ce0098218262627349a954e95982fcc1b48e75081682d5a6b8aa07838c1fe0 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone/corpus/evidence/round-27/c1/runs.tsv | 919a682f97f1454650c01aff69a635e22c53302f9789f5ab91f1a48066ea65d5 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone/corpus/evidence/round-27/c1/table.tsv | d5c2e5de60e8e01d71f8553140f31858e9df532baee447c6e0b0586acbbb15e8 |
| /fast/scratch/hyaku/kaidoku-r27/seats/LessonMistake/clone/corpus/evidence/round-27/c1/envelopes/jq-analyze-base.json | 3b7c5e4acf86e41402803cc763da8cc66b64626798d9d2ee39ae919788efc2fb |

Only this report was written inside the lane. Product files, counters, source ledger, lessons, lane index and refs were not edited. Sandbox commits are not lane commits and were not pushed. No REA invocation, package install, upgrade, delegated agent, background job, canonical judge, deployment or publication occurred. No broad tests or builds were run. Out of scope: integration into the round-27 lesson, S081 landing, full C1/C2 acceptance and calibration claims.
