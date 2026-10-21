# CriticProvider — falsify the 93 inherited dead W1 seats (loss disclosure, ≤200 total, no replacement claim)

Seat: `KaidokuR22R.CriticProvider-6` (critic, author-side, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, baseline B `7787fea4d6fd718726de92ed20759d11ce7b8b48`.
Read-only. No REA, target execution, build, test, lint or install run. No tools installed or updated.
Judged on current authored evidence only. Any W2 report that arrives later is not considered.

## Verdict

| Assertion | Result | Axis |
|---|---|---|
| ≤200 total seats | **Survives.** 93 W1 + 64 W2 = 157. No resumes. | calibration |
| No replacement claim | **Survives.** No W2 name equals a W1 name. `resumeSends` is `[]`. No W1 output is credited. | coverage, calibration |
| Loss disclosure | **Fails at the committed revision.** Committed text cites W1 records that are untracked and absent at `2ee3d9f`. The per-seat record also misses the lane's own QUALITY #22 fields. | calibration |

The C1 and C2 counters never read any W1 record (`claims.json:37`, separability). So no counter verdict changes here. The dead-seat guarantees are prose and records only, not machine-checked.

## Finding 1 (defect): the committed loss disclosure cites records absent at its revision

**Observation.** `git cat-file -e 2ee3d9f:<path>` reports each of these as absent. `git status --short` lists them as `??` (untracked):

- `.ufo/waves/round-22/wave1-dispatch-result.txt`
- `.ufo/waves/round-22/wave1-terminal.json`
- `.ufo/waves/round-22/recovery-authority.json`
- `.ufo/waves/round-22/wave1-dispatch-attempts.json`
- `.ufo/waves/round-22/gen-wave1.py`
- `.ufo/waves/round-22/verify/frida-unsupported-env.json`
- all `wave2-*.json`, `wave2-slot.txt`, `w1/`, `w2/`

The committed text depends on those records:

- `2ee3d9f:LOG.md:2464-2468`: "lost W1 dispatched93 … `wave1-terminal.json` records each identity/cause … All dispatch refusals are retained."
- `2ee3d9f:corpus/lessons/round-22.md:21`: the Mistakes row cites `.ufo/waves/round-22/wave1-dispatch-result.txt` ("records93 successful spawns") and `wave1-terminal.json`.
- `2ee3d9f:corpus/lessons/round-22.md:22`: cites "inherited gen-wave1.py ScribeMistakeAdb".
- `2ee3d9f:corpus/lessons/round-22.md:26`: "W1 spec/generator/launch attempts and acknowledgement are preserved as evidence".

**Counterexample.** A reader at `2ee3d9f` cannot reproduce "93 dispatched / 93 dead / 0 reports". The headline count has no per-seat record at that revision. QUALITY #22 (`2ee3d9f:corpus/QUALITY.md:32`) says exactly this case is inadmissible: "A headline count with no per-seat record is inadmissible." The same shape was a prior lane defect: R18-DEADSEAT-RECORD, "no committed wave file held a cause", cited in that same row.

**Impacted axis.** Calibration. The disclosure is honest in content but unverifiable at the revision that states it.

**Smallest safe correction (for L1).** Track and commit, unchanged, in the next integration commit:

- `wave1-terminal.json`, `wave1-dispatch-result.txt`, `wave1-dispatch-attempts.json`, `wave1-spec.json`, `wave1-dispatch.json`, `gen-wave1.py`, `recovery-authority.json`, `w1/swarm-registry.json`
- the W2 dispatch records: `wave2-spec.json`, `wave2-dispatch.json`, `wave2-spawn*.json`, `wave2-retry-summary.json`, `wave2-accepted.json`, `wave2-slot.txt`, `w2/swarm-registry.json`

Then cite that commit, not `2ee3d9f`, as the revision of the disclosure. Do not edit the `2ee3d9f` text; add an append-only erratum if a pointer is needed.

## Finding 2 (defect): `wave1-terminal.json` lacks QUALITY #22's cutoff and cause-pointer fields

**Observation.**

- Top-level keys are only `round`, `observation`, `authority`, `seats`.
- `authority` is "parent Main message: 93 W1 seats terminated with coordinator on Anthropic429; no reports will arrive". That message is not retained in the lane.
- All 93 seats are uniform: `status=dead_parent_provider_death`, `cause="parent KaidokuR22 Anthropic429 terminated child session"`, `report=null`, `launch_record=.ufo/waves/round-22/wave1-dispatch-result.txt`.
- There is no observation-cutoff timestamp anywhere in the file.
- `launch_record` points at the spawn acknowledgement, not at a terminal error line or transcript.
- `recovery-authority.json` has `"source": "parent Main messages during replacement session"` and also has no time.

The ID set is clean: 93 unique IDs, exactly equal to the 93 `` `KaidokuR22.*` (job `` IDs in `wave1-dispatch-result.txt`, with no extras either way.

**Counterexample.** QUALITY #22 requires each reportless seat to have either "its retained cause (the terminal error line and its transcript or result pointer)" or "`cause unknown` with what was tried". It also requires an observation cutoff. The record has a paraphrased cause, no retained source line, no transcript pointer and no cutoff. A later seat or late report cannot be separated from "dead at cutoff".

- `w1/swarm-registry.json` has `updatedAt 2026-10-21T12:53:55.689Z`, after `wave1-terminal.json` was written (mtime 09:39:07 -03 = 12:39:07Z). So the registry changed after the terminal record, and nothing records what changed.

**Impacted axis.** Calibration.

**Smallest safe correction.** Leave the 93 seat entries unchanged and add top-level fields:

- `observed_cutoff`: the time of the parent message, or the file-write time if that is unknown, labelled as such.
- `cause_source`: say that the cause is the parent Main's statement and that no child transcript or error line is available to the lane.
- `tried`: the empty `agent://` reads and the absent report/scratch checks already described at lessons `:26`.

That meets the "`cause unknown` with what was tried" branch of QUALITY #22 without inventing an error line.

Check to run after the fix: `.ufo/waves/round-19/tools/wave-outcomes.py --registration .ufo/waves/round-22/w1/swarm-registry.json --report-dir .ufo/waves/round-22/w1 --causes <causes.json> --out <json>`, from `SKILL.md:598`. I did not run it; the `--causes` input shape is unverified.

## Finding 3 (calibration gap): the ≤200 bound has no retained source, and the only issued grant says cap=240

**Observation.**

- The 200 bound appears only in untracked `recovery-authority.json`, as `"remaining_seat_budget": 107` (= 200 − 93). That value is attributed to unretained parent messages.
- `claims.json` has no seat budget.
- Neither W1 nor W2 spec context contains `200`, `107`, `<=` or "seat budget" (searched with a regex over `context`).
- The one machine-issued grant has a different ceiling: `wave2-slot.txt` says `granted lane=kaidoku wave=round-22-w2 seats=64 live=46 pending=128 cap=240`, and `wave2-retry-summary.json` repeats `cap=240` for tries 5 and 6.
- Unlike prior rounds, `2ee3d9f:LOG.md` states no round total. Prior rounds did: `LOG.md:2403` "The round total is 147 seats", `:2543` "Total 162", `:2723` "Total132 seats".

**Measured total (survives).**

- W1: 93 spawned, all dead. Three earlier attempts were full refusals: `wave1-dispatch-attempts.json` tries 1–3 `refused: 93`, try 4 `refused: 0`.
- W2: five full refusals of 64 each, then 64 spawned on try 6:
  - `wave2-spawn.json` and `wave2-spawn-try2..5.json`: 0 started, 64 "Background job limit reached (100)" each.
  - `wave2-spawn-try6.json`: 64 started.
- `w2/swarm-registry.json` has 64 `kind: spawn` members.
- `wave2-dispatch.json` counts `{spawn: 64, resume: 0, total: 64}`.
- Round total: 157 ≤ 200, leaving 43 of the stated 107. Refused launches are not seats, which is consistent with lessons `:26`.

**Minor.** `wave2-retry-summary.json` records only tries 5 and 6. Tries 1–4 exist only as `wave2-spawn*.json` files. `wave1-dispatch-attempts.json` try 4 has no `spawned` field; the 93 is shown only by `wave1-dispatch-result.txt`.

**Smallest safe correction.** In the round-22 LOG/SCORECARD entry, state the round total with its parts: W1 93 dead + W2 64 = 157 seats, 3 W1 and 5 W2 whole-batch launch refusals not counted. Name the bound's source ("parent-assigned 200, not retained") next to the observed grant `cap=240`, so a reader does not take one for the other.

## Counterexamples tested that survived

1. **A dead seat's intended output is counted as C1 evidence.** This was the strongest local candidate. W1 seat `KaidokuR22.ExecFlutterNegative-4` (`wave1-spec.json`, item `ExecFlutterNegative`) was assigned the same verb on the same Godot `android_release.apk` that the committed C1 evidence uses. It did not hold:
   - The W1 spec required a scratch copy and a relative argv (`identify-flutter-build android_release.apk … > identify-godot-negative.json` in `/home/vgpnk/Projects/kaidoku-r22-scratch/ExecFlutterNegative/`).
   - The committed `evidence/c1/identify-godot-run.json` argv uses the absolute original path `/home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_release.apk`, and the file names differ (`identify-godot.*`).
   - `ls /home/vgpnk/Projects/kaidoku-r22-scratch` returns "No such file or directory"; `find … -type f | wc -l` returns 0.
   - The C2 receipts come from `tools/capture-probes.py`; its retained invocation is in `verify/capture-probes.json`, exit 0.
   - The C2 ADB receipts use `REA_ADB_PATH=/usr/bin/false`, whereas W1 `ExecProbeAdbA` required real adb with a listener bracket. So they are not W1-shaped either.
   - **Residual [INFERENCE]:** attribution rests on these differences. Neither the C1 `run.json` (keys `argv, exit, stdout, stderr`) nor the C2 `runs.json` (`verb, argv, env_overrides, exit, stdout, stderr, ok, error, meta`) records a producer session or timestamp. `count-c1.py:44-48` filters source rows only by `S051+`, `mined` and `opened 2026-10-21`, a date W1 shares. This is a latent tradeoff, not a live defect, because no W1 output exists. The frozen counter needs no change. If the lane wants this provable, add a `producer` field (session ID and `capture-probes.py` digest) to future run records.
2. **The recovery wave resumes or renames dead seats.**
   - After stripping the `-N` suffix, no W2 item name matches any of the 93 W1 names.
   - `wave2-dispatch.json` has `resumeSends: []` and `counts.resume: 0`.
   - The W2 context says "NEVER resume or replace them … not a claim those lost seats returned".
   - Lessons `:7` and `:26` and `LOG.md:2465-2466` credit no W1 output.
   - The `PROVINCE.md:173-205` dispositions and narrow static ground attribute nothing to W1; only the replacement's probes are cited (`:181`, `:201-204`).
   - `claims.json:4` names the frozen declarer "KaidokuR22 (L1, attempt 1)". That is the dead coordinator's declaration, kept as frozen, not a seat-replacement claim.
3. **Commit dating fabricates order.** `2ee3d9f` has author date 08:41:57-03:00, which is before the W1 dispatch at 08:57:30. Its committer date is 09:55:04-03:00, and the reflog says "export from jj". The author date is jj's change-creation time, and the committer date is after all evidence mtimes (09:38–09:43). This is a tool convention, not false provenance.

## Commands run (all read-only; exit 0 unless noted)

- `wc -l` on the three named targets and `PROVINCE.md`; `ls` of the round-22 directories; `git rev-parse HEAD` → `2ee3d9f…`.
- `git status --short`; `git log --oneline -8`; `git log -3 --format='%h author=%ad committer=%cd' --date=iso-strict`; `git reflog -15 --date=iso`.
- `for p in …; do git cat-file -e 2ee3d9f:"$p" || echo ABSENT_AT_2ee3d9f; done`: every W1 and recovery record absent (each `cat-file` exited nonzero; the loop exited 0).
- `git show 2ee3d9f:{LOG.md,SCORECARD.md,corpus/QUALITY.md,SKILL.md,corpus/lessons/round-22.md}`, read with `grep -n`/`awk`.
- `git diff 2ee3d9f -- corpus/lessons/round-22.md`: the working tree only appends two Mistakes rows and the section "Exercised counter and probe corrections". Lines 21 and 26 are unchanged; they are at `:21` and `:28` in the working tree.
- `python3` JSON fact pipelines over `wave1-terminal.json`, `wave1-dispatch-result.txt`, `wave1-spec.json`, `wave2-spec.json`, `wave2-dispatch.json`, `wave2-spawn*.json`, `wave2-retry-summary.json`, `w1/` and `w2/swarm-registry.json`, and the evidence `run.json` files. The counts quoted above come from these.
- `stat -c '%y %n'` on the dispatch, terminal and evidence files.
- `ls -la /home/vgpnk/Projects/kaidoku-r22-scratch` → "No such file or directory".

No blocker. Findings 1–3 are author-side inputs for L1, not admission.
