# ReviewQuality4849 — QUALITY rows 48–49 and mistakes M30-1..M30-5: grounded, falsifiable, "shown able to fail"?

Seat `KaidokuR30.ReviewQuality4849` (reviewer, wave 2). Lane HEAD read: `3502b94c5b93d86c5d67866035fd150899456295`.
Window 2026-10-23T03:12Z–03:18Z UTC. Read-only on the lane except this report. Every Git write and fixture ran
in the sandbox clone `/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewQuality4849/clone`, with GIT_DIR,
GIT_WORK_TREE and GIT_INDEX_FILE unset. I ran no REA, executed no carrier or mutant, and ran no tool on a
shared carrier or mutant: I only read their bytes with `cp` and `sha256sum`. No LSP server serves `.md`, `.tsv`
or this Python, so callers and definitions were checked by reading the code and with `rg`/`git grep`. Treat
those results as text matches, not semantic proof.

## Verdicts

| item | grounded (receipts exist and say it) | falsifiable | "shown able to fail" true? | verdict |
|---|---|---|---|---|
| QUALITY 48 | yes | partly: the gate checks a narrower thing than the row's sentence | for the gate's form checks, yes. For the row's sentence, **no**: five sandbox fixtures meet the gate (exit 0) while breaking the row | **fails as worded** (the gate's exit 0 does not show the row's sentence holds) |
| QUALITY 49 | yes (M30-2 receipts) | the re-hash clause yes; the immutability clause has no check | re-hash yes (4 seats exit 2). Immutability: not shown in the lane; **I showed it here** (`chattr +i` blocks the exact tool) | **holds for carriers; fails for mutants.** Round 30 did not apply it to mutants, and the C2 counter cannot run on immutable mutants |
| M30-1 | yes (pointers `:44,50-56,123-124` resolve exactly) | yes | yes for the gate's form checks, reproduced byte for byte. Not shown for the misfit class itself | **holds narrowly; the fix does not catch the M30-1 class** (fixture F1) |
| M30-2 | yes, except one count | yes | "five control seats' first counter runs exited 2" is **false: four**. "before any REA call" omits one seat that did call REA on altered bytes | **holds with two factual errors** (count; restore time 02:44:00Z, not "about 02:46Z") |
| M30-3 | yes (code `c2-rust-refusals.py:246-255`; CtlC2Sequence `matches=16`) | yes | it says "Not yet shown able to fail" — **honest** | **holds** |
| M30-4 | yes (receipt exit 1 → exit 0) | yes | not stated in the row, but the receipts show `skill_ok` failing and then passing | **holds**; "final revision" is loose wording (see below) |
| M30-5 | yes (correction line at HEAD in all 5 named files) | weakly: no check | no "shown able to fail" statement, and nothing enforces it | **holds as a correction; no fail-able fix** |

## Findings by severity

### High — QUALITY row 48: the gate's exit 0 does not establish the row's sentence (falsified, 5 fixtures)

Row 48 (`corpus/QUALITY.md:58`) says: "Every claim's counter is scored, before data, on the do-nothing, junk-row,
all-false, no-reader and id-keyed shortcut controls, with receipts committed before the first data commit
(`tools/round-30/axis-fit-gate.py` exits 0); a control that meets the target forces a re-design before data."
The parenthetical presents gate exit 0 as the evidence for this sentence. These sandbox fixtures meet the gate
(exit 0) while breaking the sentence. The gate under test is lane `tools/round-30/axis-fit-gate.py`, sha256
`1390a007…6c63`. Commands are in `fixtures.sh`, plus the inline F4/F5 commands quoted below. Fixtures were
built on clone branch `fixtures` from `3502b94c`.

- **F1: zero controls scored, and the round-29 misfit passes** (observation, exit 0, 03:15:36Z). This is the
  round-29 `claims.json` copied verbatim to round 31. I added the filler `"surface": "PROVINCE Frontier bullet
  EVM bytecode (extended)"` and `"unmoved_command": "true"`, plus a header-only `receipts.tsv` committed before
  the envelopes. Output: `verdict PASS findings [] required_controls 0 rows 0 ordering earlier notes
  ['controls_required_before_data absent: no control is named']`.
- **F2: a control that met the target passes** (observation, exit 0, 03:15:36Z). These are round 30's real
  claims and its 10 receipt rows, with row 2 changed to `R30-C1|do-nothing|0|no` (counter exit 0, meaning the
  target was met, but labelled `no`). Output: `verdict PASS findings [] … notes ['row 2: counter_exit 0 with
  met_target no']`. The gate trusts the `met_target` label, so "forces a re-design" is not enforced.
- **F3: `controls_required_before_data: []` passes** (observation, exit 0, 03:15:36Z). Round 30's claims with an
  empty list and header-only receipts give `verdict PASS findings [] required_controls 0 rows 0 … notes []`.
  This produces no note at all; only an absent key produces one (`axis-fit-gate.py:228-229`).
- **F4: receipts committed after the data pass when the data are not under `envelopes/`** (observation, exit 0,
  03:16:53Z). The data commit `ef686239` (ct 1792725413) adds `corpus/evidence/round-34/c2/db/openchain-x.json`.
  The claims and receipts commit `3cb5e4de` (ct 1792725473) comes later. Output: `verdict PASS findings []
  ordering no-envelopes notes ['no envelope path is committed yet: the ordering clause is vacuous']`. Round 29's
  own C2 data lived under `corpus/evidence/round-29/c2/db/`, which is exactly this shape.
- **F5: rows written after the data pass when an empty placeholder was committed first** (observation, exit 0,
  03:17:11Z). Empty `receipts.tsv` at `255a80c8` (ct …431), then envelopes at `0efb8554` (…491), then the 10 rows
  at `2be5555b` (…551). Output: `verdict PASS findings [] ordering earlier first_add 255a80c8 rows 10`. Ordering
  is by the path's first add (`first_add`, `axis-fit-gate.py:93-99`, `--diff-filter=A`), not by when the rows
  first appear. Round 30 shows the same pattern harmlessly: receipts were first added at `004053d6` in a shape the
  gate rejects (my run at `004053d6`: exit 1, `RECEIPTS_HEADER_INVALID` plus 10× `CONTROL_MISSING`, rows 0). They
  were reshaped at `f39f4530`, and the gate credits `004053d6` (`first_add 004053d6` at every later revision).
  Both commits precede the data commit `24da3459`, so round 30 itself is not affected.

The gate's docstring (`:42-48`) and `ExecAxisFitGate.md:170-177` disclose that row truth, absent lists and the
envelope pattern are not checked. **QUALITY row 48 does not carry those limits.** Inference: the row should say
what exit 0 proves (the two fields are present and nonempty; receipts for the named controls are first added
before the first `envelopes/` add; rows are labelled `no`). Alternatively, the gate should check a fixed control
set, counter_exit ≠ 0, any data path, and the commit where rows first appear. I did not edit anything.

### Medium — M30-1's fix catches round 29's missing fields, not the round-29 mistake

M30-1's "Shown able to fail" holds as stated, reproduced byte for byte (observation, 03:15:15–16Z, clone):

- `axis-fit-gate.py --root clone --round 29 --rev HEAD`: exit 1,
  `['SURFACE_MISSING','UNMOVED_COMMAND_MISSING','SURFACE_MISSING','UNMOVED_COMMAND_MISSING','RECEIPTS_ABSENT']`.
- `--round 30 --rev 4ee65c67…`: exit 1, `['RECEIPTS_ABSENT']`. The output file's sha256 is `3436951a…b4e6`,
  identical to `ExecAxisFitGate.md`'s `run-round30.txt`.
- `--rev f39f4530`, `24da3459`, `HEAD`: exit 0, `[]`.
- `--selftest`: exit 0, `selftest cases=18 failures=0` (sha256 `4a23a799…`, identical to ExecAxisFitGate's
  `selftest.out`).

The M30-1 class, however, is "a re-score of an already-held rule on new author-built inputs was labelled
coverage" and "its completeness-only target was also met by the trivial baseline". Fixture F1 is round 29's own
claims with two filler strings (`unmoved_command: "true"`), and it passes. None of the five named controls is a
trivial-baseline rule; round 29's `openchain_first` baseline (`round-29-verifier-spotcheck.md:44`) is not among
them. Inference: the round-29 rejection was an axis-fit judgement, and the gate checks only that the fields
exist, not that the axis fits. One wording issue: the lesson cites `axis-fit-gate-before-data.txt` for both the
exit 1 at the freeze and the exit 0 after. That file holds only `exit=0`; the freeze-time exit 1 is in
`w1/ExecAxisFitGate.md:110-118`.

### Medium — QUALITY row 49: round 30 does not meet it for mutants, and the C2 counter cannot

Row 49 (`corpus/QUALITY.md:59`) says: "Frozen inputs shared by a wave's seats (carriers, mutants, fixtures) are
made immutable (`chattr +i`, or a copy per seat) before dispatch, and every counter re-hashes them on each run".

- **Mutants are shared, not immutable, and there are no per-seat copies** (observation, 03:12Z). `lsattr
  /fast/scratch/hyaku/kaidoku-r30/mutants/` shows `----------------------` on all 19, against `----i…` on all
  16 carriers. Wave 2 was dispatched at `03:11:45Z` (`w2-dispatched-at.txt`). The mutants were rewritten at
  `00:12:49 -0300` = 03:12:49Z by the C2 build step, run by the authorised seat (`w2/ReRunC2.md:18`: "mode 0444,
  no `chattr` flags … the counter's build step rewrote them"). Wave 2 protects the mutants with a seat-exclusivity
  rule, which is neither of row 49's two options.
- **The C2 counter is incompatible with `chattr +i`** (observation, 03:15:59–16:00Z). This was a private copy of
  `c2-rust-refusals.py` with only `MUT_DIR` changed to my scratch `muts/` (copy sha256 `233f6d3a…`). `--build
  --root clone` gave exit 0, `mutants=19 rebuilt pin_mismatch=0`. After `sudo chattr +i muts/r-empty`, the same
  command gave exit 1 with `PermissionError: [Errno 1] Operation not permitted: '…/muts/r-empty'` at
  `os.chmod(p, 0o644)` (`c2-rust-refusals.py:302`). That exit 1 is the same code as "measured, not met".
- **For mutants, "re-hashes on each run" regenerates rather than detects** (inference from code,
  `c2-rust-refusals.py:299-308`). `do_build` overwrites each mutant and hashes the bytes it generated (`h =
  sha(b)`), never the bytes that were on disk. A mutant altered between runs is silently repaired and never
  reported. CriticTargetsControls `:67` makes a related point.
- **The C2 base-carrier pin exits 1, not 2** (observation, 03:16:00Z). `c2-rust-refusals.py:285` raises
  `SystemExit("PIN base carrier altered")`. Running `python3 -I -B -c 'raise SystemExit("PIN base carrier
  altered")'` printed the message and exited 1. The docstring (`:20-21`) says "exit 2 when a pinned input is
  absent or altered". The C1 counter's pin exits 2 (`c1-rust-positive.py:221-222`, confirmed by four seats).
  The C2 pin is therefore indistinguishable from "measured, not met".
- **For carriers the row holds, and the immutability mechanism works** (observation, 03:15:44Z, private copies
  only). I made two copies of carrier `elf-x86_64-uvx` (sha256 `2e9105ad…890d`), both mode 0444:
  - On copy A (no `+i`), `llvm-objcopy --dump-section .dep-v0=A.dump A` exited 0 and **A became
    `9f41e2d43ca0…03a1`**. That is the drifted hash recorded in `w1/CtlC1ShortcutIds.md:60-66`. This
    independently reproduces M30-2's mechanism and its attribution.
  - On copy B (`sudo chattr +i`), the same command printed `llvm-objcopy: error: Operation not permitted`,
    exited 1, and left B at `2e9105ad…890d`.
  - I cleared `+i` on B afterwards.
  - Neither row 49 nor M30-2 committed a demonstration like this; this report supplies the first one.
- Row 49 has no "Fails when" sentence and no tool reads `lsattr`. `rg chattr|immutable tools/round-30` matches
  no counter or gate, so the immutability clause is enforced only by procedure.

### Low — M30-2: "five control seats" should be four; restore time; one REA call on altered bytes

- **Count** (observation, from the committed reports). Lesson `:45`: "five control seats' first counter runs
  exited 2 on the altered bytes before any REA call". `rg -l 'absent or altered|base carrier altered'
  .ufo/waves/round-30/` finds counter output only in **four** seats:

  | seat | time (UTC) | exit | report |
  |---|---|---|---|
  | CtlC1AllFalse | 02:42:59Z | 2 | `:112,122` |
  | CtlC1DoNothing | 02:43:03Z | 2 | `:48,53` |
  | CtlC1NoReader | 02:43:31Z | 2 | `:80,83` |
  | CtlC1JunkRow | 02:43:46Z | 2 | `:84,87` |

  The other two hits are proposal or quote text: ScribeRegistryRows and MutC2Builder (the latter says "No
  `PIN base carrier altered` … run was observed"). The fifth control seat, CtlC1ShortcutIds, says "It was not a
  PIN-blocked run" (`:73`). SentinelNoExec says the "pre-restoration PIN-blocked run is unknown for this seat"
  (`:41`). CtlC2Sequence's exit 2 is the predictions-file pin (`:124`), not the carriers.
- **REA on altered bytes.** CtlC1ShortcutIds made an REA call on the altered `elf-x86_64-uvx` at
  02:42:42–02:42:43Z, exit 0. Its envelope's subject sha256 is `9f41e2d4…` (`:56-69`). That was control
  construction, not measurement. It was re-seeded at 02:46:06Z on the restored bytes (`:75`). So "before any REA
  call" is true for the four PIN-blocked runs only.
- **Restore time.** The lesson says "chattr +i at about 02:46Z". The carriers' ctime is `23:44:00.44 -0300` =
  **02:44:00Z** for all 16 (`stat -c '%z'`), and the four restored files' mtimes are 02:44:00.0–.38Z. Consistent
  with this, CtlC2Sequence's pristine run at 02:44:19Z passed the base pin. These are observations; that ctime
  equals the `chattr` instant is an inference.
- **"No measurement used altered bytes" holds** (observation plus inference). `corpus/evidence/round-30/c1/runs.tsv`
  first start is `2026-10-23T02:59:33+00:00`; C2 runs start at 03:00:36Z. The carriers had been `+i` since
  02:44:00Z, and the C1 counter re-hashes all 16 before its REA loop (`c1-rust-positive.py:221`).

### Low — M30-4 wording: "the round's final revision"

`after/c2-rust-refusals-at-24da3459.txt` ends `skill_ok=0 (no new SKILL.md line names inspect-rust-binary with
the entry)` / `exit=1`. `after/c2-rust-refusals-at-92b1dd2d.txt` ends `skill_ok=1 (ok)` / `exit=0`. `git diff
24da3459 92b1dd2d -- SKILL.md` adds only the lead line at `SKILL.md:970` naming both the verb and the entry.
The check is therefore shown able to fail and then pass (observation). `92b1dd2d` is not the lane's final
revision: HEAD is `3502b94c`, and wave 2 will add more commits. However, `git diff --stat 92b1dd2d 3502b94c`
touches only receipts, `w2-spec.json`, LOG.md and SCORECARD.md, none of which the counters read. Inference: the
measurement still holds at HEAD; the wording should name `92b1dd2d`. The fix column states no "shown able to
fail" answer, even though the receipts above supply one. Note also that `skill_ok` is a test for two strings on
one line; the fix satisfies it with a real lead line for the table.

### Info — M30-3 and M30-5 hold as written

- **M30-3.** `committed_agrees` (`c2-rust-refusals.py:246-255`) compares `ok`, and checks `evidence_id` only
  `if l_ok`. For a predicted refusal, the committed record is therefore checked only on its ok flag (observation,
  code). `w1/CtlC2Sequence.md:26,456` shows `predictions-copied-as-observations` at `mutants=19 matches=16
  target=19`, exit 1. `w1/RevPredicateIdentity.md:92,122` marks clause 14 "partial" for the same reason. The
  lesson's "Not yet shown able to fail" is accurate. One mislabel: `controls/receipts-detail.tsv` files this
  control under `no-reader`, while the frozen claims list "predictions copied as observations" under the
  `shortcut keyed on ids/labels` control. The gate accepts either short-id head, so the gate is unaffected.
- **M30-5.** The pointer `round-29-verifier-spotcheck.md:127` is routed defect 5 ("15 of 16 C1 carriers have
  unopened interface provenance"). `git grep -c 'R29-C1 carrier provenance' HEAD` finds the correction line in
  PROVINCE.md (`:340`), the round-29 entry (`:108`), corpus/README.md (`:233`), SCORECARD.md (`:3230`) and
  LOG.md (`:3020`). The old "published" lines remain (for example `corpus/README.md:79,177` and the entry's
  `:5,10,82`), as the append-only policy requires. The fix states no "shown able to fail", and no check would
  flag a new "published" overclaim. This is recorded as a gap, not a defect.

## Residual risk and verification gaps

- **Unknown.** Whether the L1 holds a fifth PIN-blocked receipt outside the committed reports, such as a seat
  message. Only committed `.ufo/waves/round-30/` reports were searched.
- **Not evaluated.** Whether lane-level rows 1–47 require a "Fails when" sentence. Rows 45–47 carry one; rows
  48–49 do not. No meta-criterion in `corpus/QUALITY.md:1-89` requires it, so this is noted, not scored.
- **Not run.** The C2 counter in measure mode, and any REA call (seat bound). My C2 copy ran `--build` only, on
  a private `MUT_DIR`. The shared mutants were never touched.
- **Gap.** The gate's ordering uses committer timestamps (disclosed limit). I did not test timestamp forgery,
  since F4 and F5 already falsify the row without it.

## Sources (all local reads, access date 2026-10-23)

| path (lane at `3502b94c` unless noted) | sha256 | located quote (line) |
|---|---|---|
| `corpus/QUALITY.md` | `fbbe223b…653b` | `:59` "a seat tool that can rewrite its input in place (e.g. `llvm-objcopy --dump-section` without an output file) runs only on a private copy" |
| `corpus/lessons/round-30.md` | `a2aa1be6…fb50` | `:45` "Shown able to fail: five control seats' first counter runs exited 2 on the altered bytes before any REA call." |
| `corpus/lessons/round-29-verifier-spotcheck.md` | `78e4febf…ac76ad` | `:44` "The trivial baseline does at least as well as the primary rule." |
| `tools/round-30/axis-fit-gate.py` | `1390a007…6c63` | `:228-229` "if required is None: notes.append('controls_required_before_data absent: no control is named')" |
| `tools/round-30/c2-rust-refusals.py` | `1c357fca…2a6b` | `:285` "raise SystemExit(\"PIN base carrier altered\")" |
| `tools/round-30/c1-rust-positive.py` | `e07563d6…ed2a` | `:222` "print(\"PIN carrier %s absent or altered at %s\" % (r[\"id\"], r[\"path\"]))" |
| `.ufo/waves/round-30/controls/receipts.tsv` | `46d4cb34…b7f` | `:2` "R30-C1 do-nothing 1 no" |
| `.ufo/waves/round-30/controls/receipts-detail.tsv` | `20bdbf43…120` | `:10` "predictions copied as observations (fabricated refusal records + oracle-fabricated acceptances): matches=16" |
| `.ufo/waves/round-30/controls/axis-fit-gate-before-data.txt` | `049a9726…86dd` | `:2` "exit=0" |
| `.ufo/waves/round-30/after/c2-rust-refusals-at-24da3459.txt` | `69b7766b…374c` | `:22` "skill_ok=0 (no new SKILL.md line names inspect-rust-binary with the entry)" |
| `.ufo/waves/round-30/after/c2-rust-refusals-at-92b1dd2d.txt` | `2a125173…22b6` | `:22` "mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)" |
| `.ufo/waves/round-30/w1/ExecAxisFitGate.md` | `86d7380c…570c` | `:47` "Absent/empty `controls_required_before_data` names no control: a note, not a finding" |
| `.ufo/waves/round-30/w1/RevOracleVsReadobj.md` | `88b6aaf9…4fac` | `:9-10` "invocations were run **without an output-object argument**. llvm-objcopy then" |
| `.ufo/waves/round-30/w1/CtlC1DoNothing.md` | `500c9fc5…aa90` | `:53` "PIN carrier elf-x86_64-uvx absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx" |
| `.ufo/waves/round-30/w1/CtlC1AllFalse.md` | `b732e878…790b` | `:122` "PIN carrier elf-x86_64-uvx absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx" |
| `.ufo/waves/round-30/w1/CtlC1JunkRow.md` | `f33fb541…6279` | `:84` "`2026-10-23T02:43:46Z`–`2026-10-23T02:43:47Z`; counter exit **2**." |
| `.ufo/waves/round-30/w1/CtlC1NoReader.md` | `e9af5526…5e14` | `:80` "Observation, 2026-10-23T02:43:31Z–02:43:31Z; counter exit 2." |
| `.ufo/waves/round-30/w1/CtlC1ShortcutIds.md` | `203727e5…3708` | `:73` "It was not a PIN-blocked run." |
| `.ufo/waves/round-30/w1/CtlC2Sequence.md` | `de1148a5…d94e` | `:456` "mutants=19 matches=16 target=19 entry_ok=1 (ok) skill_ok=1 (ok)" |
| `.ufo/waves/round-30/w1/RevPredicateIdentity.md` | `959b2832…377d` | `:122` "`committed_agrees` (c2:253) checks `evidence_id` equality only `if l_ok`." |
| `.ufo/waves/round-30/w1/CriticTargetsControls.md` | `299dfc8b…746f` | `:67` "C2's builder validates generated bytes against the ID/hash pairs in the current predictions file" |
| `.ufo/waves/round-30/w1/ScribeR29Provenance.md` | `c1b34476…bd23` | `:5` "All five affected files should receive the same correction line at EOF, preserving the old statements." |
| `.ufo/waves/round-30/w1/SentinelNoExec.md` | `2a315085…6391` | `:41` "The requested pre-restoration PIN-blocked run is **unknown for this seat**" |
| `.ufo/waves/round-30/w1/MutC2Builder.md` | `fe03fa18…22f6` | `:236` "No `PIN base carrier altered`/carrier-PIN-blocked run was observed in this seat" |
| `corpus/evidence/round-30/c1/runs.tsv` | `70dd83fc…3fb` | `:2` "elf-x86_64-uv 2026-10-23T02:59:33+00:00" |
| `.ufo/waves/round-30/w2/ReRunC2.md` (untracked, wave 2) | not hashed | `:18` "mode 0444, no `chattr` flags" |

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r30/seats/w2/ReviewQuality4849/`, sha256)

| artifact | sha256 |
|---|---|
| `fixtures.sh` (F1–F3 builder and runner) | `239751da26910d13cc19d01707e0dc64695866522e6fcb5e85d7d2dd273266b6` |
| `fixtures.out` | `a09c41c29e97023a53d7a2a91f22346e933b2b4414c2c70da711ec46366502fa` |
| `fixture-r31.txt` (F1) | `984de620b4d8835e2fd2466ac3ee51f132ce6e524ee738852d96e8656229e133` |
| `fixture-r32.txt` (F2) | `ae45fdfb00286276b2cf799273c8416d2d2405cbcb24625f28a765578c03fd60` |
| `fixture-r33.txt` (F3) | `4bb1e84c2e296a9c2477e21a96166f35906b6a92580997d9454a4ab0717c7886` |
| `fixture-r34.txt` (F4) | `8a0f79420536132f1cd217ceee6f6a221d924aab95e7b44fbfc93c9e17187614` |
| `fixture-r35.txt` (F5) | `c3556bfe79e2e7166b14044d51aa33ef5895daecf167c677fc2b51d8b07e168d` |
| `fixtures-log.txt` | `da1646a34138ede1a5993e6e929cf87a955939933b87f76d1dfe4d620ca893ea` |
| `run-r29-HEAD.txt` | `21381127b418a15c912300097013d2e425e34bb827ac03ce301ba967eca1e243` |
| `run-r30-4ee65c67….txt` | `3436951ab5e996c88f2693e35847caef4906a4ce3cb48e4c887c139fbd51b4e6` |
| `run-r30-004053d6.txt` | `b7e6c3039fbd731d4314193e12c36c3a2c2f22b28e41d9816070a0e34729a18c` |
| `run-r30-f39f4530.txt` | `081060459a9854ca3ea8a16b5a6adc5cbbff2a1cdd1deec7b1408975ed7d4e84` |
| `run-r30-24da3459.txt` | `15be69e68bc61fa0802c3a9cbfb7318a61bc8f4c53b786424c4b7751fe462649` |
| `run-r30-HEAD.txt` | `a1c09c5d63f0aa41c21ccc0580a6e24522183beff62218ca9c582b9c5aed1ecf` |
| `selftest.txt` | `4a23a799dc25228a6106a0bded6014485d9a49317d6b5b144760db07948b5e00` |
| `chattr/A` (0444 copy after the in-place rewrite) | `9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1` |
| `chattr/B` (`+i` copy, unchanged; `+i` cleared after the test) | `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d` |
| `chattr/A.dump`, `chattr/B.dump` | `ca01bd2a28ae28d6b3f4b64f54eb003061e7bf2584756bb6148c1d4e6383547e` (both) |
| `c2copy/c2-rust-refusals.py` (`MUT_DIR` only changed) | `233f6d3ae46502dc3942100c81ea22ad2d759ff772cba7dc936d3a1d00927292` |
| `c2copy/rust_dep_oracle.py` (unchanged copy) | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` |
| `muts/*` (19 private mutants, `pin_mismatch=0`) | listed in `artifacts.sha256` |
| `clone/` | sandbox clone. Branch `fixtures` = `3502b94c` + fixture commits `e54504af`, `ef686239`, `3cb5e4de`, `255a80c8`, `0efb8554`, `2be5555b`. `main` is checked out and clean |

Installs and updates: none. Processes: none left running (`pgrep` empty at 03:17Z). `sudo` was used only for
`chattr ±i` on my own scratch copies (`chattr/B`, `muts/r-empty`); both are cleared (`lsattr` shows no flags).
No agents were spawned and no messages were sent.
