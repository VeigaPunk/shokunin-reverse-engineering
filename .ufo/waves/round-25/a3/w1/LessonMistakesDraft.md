# R25-A3-W1 — LessonMistakesDraft: three candidate Mistakes rows for round 25

Seat `KaidokuR25a3.LessonMistakesDraft` (leaf scribe; no delegation, no background jobs).
Target: candidate rows for the `## Mistakes` table of `corpus/lessons/round-25.md`.
Lane read-only: the only lane file written by this seat is this report. No git write, no jj, no
network fetch, no REA run.

Lane tip when the measurements were taken: `dc31f9c441528cfff1070c0574eea9669fd47e64`
("round-25: wave-1 corrections to the EVM selector-naming entry …"). The tip advanced from
`08c7a729` to `dc31f9c4` at 2026-10-22T10:53Z, mid-seat; every number below is stated at the
revision it was measured at.

The lesson already carries `M25-1…M25-9` at that tip (`corpus/lessons/round-25.md:70-73` and
`:393-397`). The three rows below are **candidates for the next ids** (`M25-10`, `M25-11`,
`M25-12`), not renumberings of the landed rows. Each row names the class, the evidence pointer,
what captured it, the fix, and **how the fix was shown able to fail** — a runnable command with an
exact output excerpt, exit code and UTC time.

---

## Draft rows (paste-ready)

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M25-10 | seat accounting read from the roster instead of the spawn result | `.ufo/waves/round-25/a2/w1-refusal-1.json` (attempt 1, `2026-10-22T08:26:23Z`): `seats_requested: 37`, `spawned: 0`, `refused: 37`, reason `Background job limit reached (100)` named 37 times — while `.ufo/waves/round-25/a2/w1/swarm-registry.json` carries **37 members, 0 with an `agentId`** and `.ufo/waves/round-25/a2/w1-dispatch.json` still declares `counts: {"spawn": 37, "total": 37}` | none in the lane: the attempt-2 wave-1 refusal is committed (`46d2613d`) but `corpus/lessons/round-25.md`, `SCORECARD.md` and `LOG.md` at `dc31f9c4` contain no line naming it (grep for `w1-refusal\|37 seats\|job limit\|Background job` returns nothing in all three); the precedent exists and is not applied — `corpus/lessons/2026-10-18-wave-dispatch-counting.md` rule 1 ("Count the items array, not the intent"), `corpus/lessons/round-23.md` / `.ufo/waves/round-23/w1/CriticLifecycle.md:51` ("Seat counts must be taken from the spawn result, never from the slot grant"), `.ufo/waves/round-22/final-wave-outcomes.json` (`refused_zero_spawn_batches: {"w1": 3, "w2": 5}`), and `corpus/lessons/round-24-verifier-spotcheck.md:51` ("zero spawned, not 85 dead or a completed heavy swarm … without counting refused jobs as work") | Credit seats only from the spawn result: a wave with `spawned: 0` contributes **0** seats, and the refusal receipt stays the terminal record of the batch. **Shown able to fail** by `python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonMistakesDraft/check_seat_accounting.py --wave <lane>/.ufo/waves/round-25/a2/w1 --refusal <lane>/.ufo/waves/round-25/a2/w1-refusal-1.json --spec <lane>/.ufo/waves/round-25/a2/w1-spec.json --dispatch <lane>/.ufo/waves/round-25/a2/w1-dispatch.json` → **exit 1** at 2026-10-22T11:08:39Z, `credited_seats: 0`, `naive_seats_if_registry_counted: 37`, problems `["registry lists 37 members but the spawn result records 0 spawned; crediting the roster would invent 37 seats", "dispatch counts claim spawn=37 while the spawn result says 0"]`. The checker is not a constant-failure detector: `python3 -I -B …/test_seat_accounting.py --checker …/check_seat_accounting.py` → **exit 0** at 2026-10-22T11:08:30Z, three controls pass — a clean 4-requested/4-spawned wave exits 0, a 4-member roster with `spawned: 0` exits 1, and a refusal whose text lost the machine-readable reason exits 1. |
| M25-11 | self-assessment number allowed to drift out of the corpus | `corpus/evidence/round-25/a2/before/c1-calibration.json` item I4 at `9dcd11ec`: `stated [78, 78]` against `observed 107`; the repair (`0e333eb2`) rewrote the row to `107/107`, and `08c7a729` rewrote it again to `108/108` — the number is re-typed by hand each time the corpus grows, so it drifts again on the next addition | none: the retained command-A mapping counts files but never compares the count with the row's own text, so the row is unverified prose until an instrument happens to read it; `corpus/QUALITY.md` row 34 (the round-25 outside-decision criterion) requires the SCORECARD to carry the decision but no row binds a count to a corpus revision | The coverage row's `N/N` must equal the knowledge-Markdown count **at the revision the row is written for**, and the row must say which revision it is for. `tools/round-25/a2/c1-calibration.py` item I4 performs that comparison; it is 0 mismatches at `dc31f9c4` (`stated [108, 108]`, `observed 108`). **Shown able to fail** by mutation in a sandbox clone (`git clone -q <lane> …/clone`), each mutation a separate commit off `dc31f9c4` so no mutation inherits another: `python3 -I -B …/mutate_calibration.py --clone …/clone --lane <lane>` → **exit 0** at 2026-10-22T11:07:41Z with all three mutations red — M-A add one knowledge entry (row untouched) `stated [108, 108]` vs `observed 109`, exit 1; M-B set the row back to `78/78` `observed 108`, exit 1; M-C remove the round-25 EVM entry (row untouched) `stated [108, 108]` vs `observed 107`, exit 1. The instrument is therefore not a constant-red detector: the unmutated clone at `dc31f9c4` gives **exit 0**, `mismatches: 0`. |
| M25-12 | producing command and tool version not retained with the evidence | `corpus/evidence/round-25/a2/c2/*/rea-run.txt` (6 files) keep `rea_exit`, `utc`, `sha256` and `carrier_sha256` but **no argv and no version**: `grep -c argv` is 0 for all six, and the string `rea-agents` or `6.5.0` occurs nowhere under `corpus/evidence/round-25/a2/` (recursive grep, 0 hits). The saved `envelope.json` files do not carry it either: `provider.version` is `evmole@0.9.3` (the provider, not the CLI) and `environment` is `null` in all six | `corpus/QUALITY.md` row 31 ("CLI-held evidence preserves the original producer envelope: success status, **exact command**, one supported record, exact file citation") — the criterion existed; the attempt-2 receipt did not satisfy it | Every CLI receipt keeps the exact argv and the tool version beside its digests, and the argv must be **bound** to the artifact it produced, not merely present. Attempt 3 keeps the argv in `corpus/evidence/round-25/a3/c2/rea-replay/runs.txt` (6/6 lines, `npx -y rea-agents@6.5.0 inspect-evm-interface <path> hex --format json`) and the bound replay envelope is byte-identical to the saved a2 envelope for all six carriers. **Shown able to fail** by `python3 -I -B …/check_argv_custody.py --runs <lane>/corpus/evidence/round-25/a3/c2/rea-replay/runs.txt --replay-dir <lane>/corpus/evidence/round-25/a3/c2/rea-replay --envelope-dir <lane>/corpus/evidence/round-25/a2/c2` → **exit 0** at 2026-10-22T11:04:21Z on the unmutated receipts (`all_bound: true`, 6/6 `argv_matches_envelope_subject`, 6/6 `saved_equals_replay`), and **exit 1** on each of three single-field mutations of the same receipts: argv field removed (11:04:33Z, "no parseable argv= field" ×6), the two carriers' subject paths swapped (11:04:44Z, "argv subject … != envelope subject …" for rv2token and kdxtoken), and the version downgraded to `rea-agents@6.4.0` (11:04:44Z, "argv does not name rea-agents@6.5.0" ×6). The equality claim in `compare.json` is sensitive too: flipping one selector in a copied `rv2token` replay makes `parsed_json_equal` false for that carrier only. |

---

## Evidence, command by command

### M25-10 — seat accounting

Commands (lane read-only; the checker opens the lane for reading only):

```
2026-10-22T11:08:39Z  python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonMistakesDraft/check_seat_accounting.py \
    --wave  <lane>/.ufo/waves/round-25/a2/w1 \
    --refusal <lane>/.ufo/waves/round-25/a2/w1-refusal-1.json \
    --spec   <lane>/.ufo/waves/round-25/a2/w1-spec.json \
    --dispatch <lane>/.ufo/waves/round-25/a2/w1-dispatch.json
exit 1
```

Verbatim excerpt from the receipt:

```json
"registry_members": 37, "registry_members_with_agent_id": 0, "spec_items": 37,
"requested": 37, "spawned": 0, "refused": 37,
"refusal_reason": "Background job limit reached (100)", "refusal_per_seat_mentions": 37,
"credited_seats": 0, "naive_seats_if_registry_counted": 37,
"problems": [
  "registry lists 37 members but the spawn result records 0 spawned; crediting the roster would invent 37 seats",
  "dispatch counts claim spawn=37 while the spawn result says 0"
]
```

Controls (`test_seat_accounting.py`, exit 0 at 2026-10-22T11:08:30Z): C1 clean wave
(4 requested / 4 spawned / no refusal) → exit 0; C2 roster of 4 with `spawned: 0` → exit 1;
C3 refusal whose `error_text` no longer carries `Background job limit reached (N)` → exit 1.
The checker is discriminating, not a constant-red.

Facts behind the row, all read from committed lane blobs:

- `.ufo/waves/round-25/a2/w1-refusal-1.json`: `wave kaidoku25a2-w1`, `attempt 1`,
  `utc 2026-10-22T08:26:23Z`, `seats_requested 37`, `spawned 0`, `refused 37`; the
  `error_text` names 37 seat names, each with `Background job limit reached (100)`.
- `.ufo/waves/round-25/a2/w1/swarm-registry.json`: 37 members, all `kind: "spawn"`, **all
  `agentId: null`**, `createdAt 2026-10-22T08:24:37.808Z`.
- `.ufo/waves/round-25/a2/w1-dispatch.json`: `counts: {"spawn": 37, "resume": 0, "total": 37}`.
- `.ufo/waves/round-25/a2/w1-spec.json`: 37 items — so the roster covers the request exactly;
  the defect is not a miscount of the items array but crediting the roster after a zero spawn.
- `.ufo/waves/round-25/a2/w1/` holds **only** `swarm-registry.json`; no seat report exists for
  any of the 37.
- The refusal receipt is committed (`46d2613d`, "attempt 3 commits attempt-2 wave-1 spec,
  dispatch, registry and job-limit refusal as evidence (zero spawned)") — the evidence exists;
  the lesson does not cite it. `grep -n "w1-refusal\|37 seats\|job limit\|Background job"`
  over `corpus/lessons/round-25.md`, `SCORECARD.md` and `LOG.md` at `dc31f9c4` returns **no
  match in any of the three** (the lesson's existing refusals at lines 86 and 164 are about
  attempt 1's distiller seat, a different event).

Live recurrence in this very wave (observation, not a finding against a person): the attempt-3
wave-1 registry at `.ufo/waves/round-25/a3/w1/swarm-registry.json` holds **65** members —
the union of the 33 wave-1 spec names (all with an `agentId`) and the 32 wave-2 spec names
(all with `agentId: null`, no wave-2 report yet) — while `w1-dispatch.json` declares
`spawn: 33`. The union was confirmed by set equality, not by eyeballing. A roster-only count
of that registry would say 65 seats for a 33-seat wave.

### M25-11 — coverage-row drift

Baseline (lane, read-only):

```
2026-10-22T10:47:12Z  python3 -I -B <lane>/tools/round-25/a2/c1-calibration.py --root <lane> --rev 9dcd11ec
exit 1   "mismatches": 5, I4 "stated": [78, 78], "observed": 107
```

That rerun is **byte-identical** to the saved receipt
`corpus/evidence/round-25/a2/before/c1-calibration.json`
(sha256 `24c295c2377ff46bebec02325aaa82d1360c08b890a0569af30319a1c8affb53`, `diff` clean).

At the current tip:

```
2026-10-22T11:01:34Z  python3 -I -B <lane>/tools/round-25/a2/c1-calibration.py --root <lane> --rev dc31f9c4
exit 0   "mismatches": 0, I4 "stated": [108, 108], "observed": 108
2026-10-22T11:01:35Z  python3 -I -B <lane>/tools/round-25/a2/c2-coverage.py --root <lane> --rev dc31f9c4
exit 0   "knowledge_md": 108, "entry_sourced": 1, "qualifying_rows": ["S075","S076","S077","S078"]
```

Mutation harness (`mutate_calibration.py`, 2026-10-22T11:07:40Z–11:07:41Z, exit 0 = every
mutation went red). Each mutation is an independent commit off `dc31f9c4`; the harness resets
the clone before each one, so no mutation inherits another's edits:

| mutation | rev | I4 stated | I4 observed | exit |
|---|---|---|---|---|
| M-A add one knowledge `.md`, row untouched | `4272037260cf02ba29eac09e2d93d3270e4385d8` | [108, 108] | 109 | 1 |
| M-B set the coverage row back to `78/78` | `4c5e38b532af8ed77b0383ac8bbd5e79cafd6a4a` | [78, 78] | 108 | 1 |
| M-C remove the round-25 EVM entry, row untouched | `34ffbeb0a42f1f57d8b126c20611cc07f60f9212` | [108, 108] | 107 | 1 |

Unmutated clone at `dc31f9c4`: **exit 0**, `mismatches: 0` (so the check is not always-red).
The clone was reset to `dc31f9c4` afterwards and `git status --porcelain` in it is empty.

Why the class is "drift", not "one wrong number": the row is re-typed by hand. `git show
0e333eb2:SCORECARD.md` reads `107/107 knowledge files mapped`; `git show
08c7a729:SCORECARD.md` reads `108/108 knowledge files mapped` — two manual rewrites in two
commits, each time because the corpus grew. The row also now carries the provenance inline
("recount 107/107 … at `7ef837a4` … 108/108 after the round-25 EVM selector-naming entry"), which
is the direction the fix should keep going.

### M25-12 — argv and version custody

`corpus/evidence/round-25/a2/c2/*/rea-run.txt` (6 files, verbatim, one shown):

```
rv2token rea_exit=0 utc=2026-10-22T08:27:59Z sha256=ed4a1118dfc7a180fac794541371019ce8bc2272908860bc1fd4bf99ad2cbf50 carrier_sha256=d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f
```

`grep -c argv` → 0 for all six. Recursive `grep -ra "rea-agents\|6\.5\.0"` over
`corpus/evidence/round-25/a2/` → **0 hits**. The saved envelopes do not fill the gap:
`provider.version` is `evmole@0.9.3` for all six and `environment` is `null` for all six — the
provider version, not the CLI version, and no host provenance.

Attempt-3 receipts (`corpus/evidence/round-25/a3/c2/rea-replay/runs.txt`) keep the argv on all
6 lines, e.g.

```
rv2token exit=0 utc=2026-10-22T09:25:30Z argv=npx -y rea-agents@6.5.0 inspect-evm-interface /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json
```

Binding check, `check_argv_custody.py`, exit 0 at 2026-10-22T11:04:21Z on the unmutated
receipts: 6/6 `argv_matches_envelope_subject` (the argv's `.hex` path equals the envelope's
`subject.local_path`), 6/6 `saved_equals_replay` (the attempt-2 saved envelope equals the
attempt-3 replay as parsed JSON). Independently, `sha256sum` shows the attempt-3 replay file and
the attempt-2 `envelope.json` are **byte-identical** for all six carriers
(rv2token `ed4a1118…`, kdxtoken `1bc65b6f…`, vaultb-opt200 `506c9101…`, carrierb `95e86017…`,
stewardtoken `1de20e96…`, carrierv `a2e7ba7b…`).

Three mutations, each a single-field change to a copy of the receipts, each **exit 1**:

| mutation | UTC | first problem reported |
|---|---|---|
| `argv=` field removed from all 6 lines | 11:04:33Z | `line 1: no parseable argv= field` (×6) |
| rv2token's and kdxtoken's subject paths swapped | 11:04:44Z | `rv2token: argv subject '…/EX-05/kdx-runtime.hex' != envelope subject '…/RV-2/Rv2Token.runtime.hex'` |
| `rea-agents@6.5.0` → `rea-agents@6.4.0` on all 6 lines | 11:04:44Z | `rv2token: argv does not name rea-agents@6.5.0` (×6) |

`compare.json`'s equality claim is sensitive as well: copying the replay dir and flipping one
selector (`095ea7b3` → `deadbeef`) in `rv2token.json` makes `parsed_json_equal` **false** for
rv2token and leaves the other five **true** — the comparison is per carrier, as claimed.

## Limits and what I did not do

- **The three rows are candidates, not edits.** I did not touch `corpus/lessons/round-25.md`;
  ids `M25-10`/`M25-11`/`M25-12` are my proposal for the next free ids and the L1 owns numbering
  and wording. `M25-5` (stale self-assessment number) and `M25-7` (argv not retained) already
  exist at `dc31f9c4` and cover the same two subjects from the attempt-3 angle; `M25-11` and
  `M25-12` are **candidate extensions** of those rows — they add the seat-spawn-vs-roster
  distinction and the argv-*binding* obligation (not merely argv presence) — not replacements.
  The L1 may prefer to fold them into `M25-5`/`M25-7` instead of adding new ids.
- **Not written to the lane:** the two checkers and the mutation harness live in scratch. They
  are proposals for lane-side tools; landing them is the L1's call. The lane's own instruments
  (`tools/round-25/a2/c1-calibration.py`) are unmodified and were run read-only against the lane
  and against the sandbox clone.
- **The a3 wave-2 seats are in flight**, not refused: `.ufo/waves/round-25/a3/w2/` holds only
  `swarm-registry.json` at 2026-10-22T11:12:00Z. I record the 65-member union as a *shape*
  observation, not as a refusal finding. No refusal receipt exists for attempt 3 at all
  (`find .ufo/waves/round-25/a3 -name "*refus*"` → nothing), so whether wave 2 was dispatched,
  is running, or was silently dropped is **unknown** to me; I did not run jj or inspect the
  harness's job ledger.
- **No REA run and no network fetch** by this seat. The REA replay bytes are credited to the
  attempt-3 replay seats (`C2ReaReplayA`, `C2ReaReplayB`) and to the committed a3 evidence; I
  only compared bytes and hashes.
- The claim in `M25-10` that the lane "contains no line naming the refusal" is a **negative
  observation** over three files at one revision (`dc31f9c4`), by grep, not a proof of absence
  anywhere in the lane.
- The claim "the argv's `.hex` path equals the envelope's `subject.local_path`" holds for 6/6
  by string equality. It does not prove the argv was the one that produced the envelope —
  byte-identity of the replay to the saved envelope is the stronger link and is what I cite.

## Tooling

No tool was installed, upgraded or removed. Everything used (python3 3.14.8 stdlib, git
read-only, coreutils) was already present, so the host-wide pacman pause was untouched: no
pacman, `uv`, `npm` or cargo transaction was performed. Nothing to record on that axis.

## Artifacts (outside the lane; the L1 integrates)

Base path `/fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonMistakesDraft/`.

| file | sha256 |
|---|---|
| `mutate_calibration.py` | `500f3d0e63090c8f17e6df9065a8997dbaa2179ad74800e1fae08662178c9bee` |
| `check_seat_accounting.py` | `bdac6ff06dc4528e64adc58ac1f2f685ccb5ed0c59a57a3ccccc87d8d842ef7c` |
| `test_seat_accounting.py` | `6fe1e2769b41b3e9e25df9ddd1f4f9258590a8adce1fcd13749aa8efb2dfb92c` |
| `check_argv_custody.py` | `5ef6eaf211028356585997a8dae52dc0a9829c32e4f40e199160dc8c77e1d4d4` |
| `logs/mutate-calibration.jsonl` | `6a0f8602ee6b07ead8aa17cb73abcabb074263a4a00e8ffa217550e87ea3f293` |
| `logs/seat-accounting-a2w1.json` | `e39599a4966b1a38573facdd2c2e8ab3bf59ebd2631111a19293a5a8556d62a3` |
| `logs/seat-controls.jsonl` | `4a43339caddd13f44a7c5f31be007bcebc69c661e0e77f31bec83472347d2015` |
| `logs/argv-custody-a3.json` | `55bae8784665aca04a5b5cef79f510d224bea4744f02dd52c091bde007a2ea34` |
| `logs/argv-mut-stripped.json` | `38ea241b6b5898592172e868942f2ff770d1c1528efc56ba503ad0b277ebf3c4` |
| `logs/argv-mut-swapped.json` | `1742c54bf5f39faff12b7d927d3737d0b0202e28d71781b72f3052e7e5469bcc` |
| `logs/argv-mut-oldver.json` | `169c9c54e33c9ee0948af1f36413a6086546b9ee6400cbcd38e429c4f481ee63` |
| `logs/c1-at-9dcd11ec-rerun.json` | `24c295c2377ff46bebec02325aaa82d1360c08b890a0569af30319a1c8affb53` |
| `logs/c1-at-dc31f9c4.json` | `8d06bcd2c32824e9881a6f72ab3b581a387b3eea1719d04157202b6a42e6ae30` |
| `logs/c2-at-dc31f9c4.json` | `212a92254c357a897f878570b9450852b8089786f8b3f2111d0b2bb7610d6e58` |
| `logs/clone-baseline-c1.json` | `d6be83a566570f0abd6ad8b0dbc38bc83cea7bbd6e2c095e697426229ba91591` |

The sandbox clone lives at `…/seats/LessonMistakesDraft/clone` (a plain `git clone -q` of the
lane) and was left reset to `dc31f9c4` with a clean `git status --porcelain`.

Report: .ufo/waves/round-25/a3/w1/LessonMistakesDraft.md
