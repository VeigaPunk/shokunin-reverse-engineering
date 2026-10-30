# CritBand — round-52 w1 attack on the round shape

Scope: wave accounting (64 seats + falsify wave), per-seat status.json, the dispatch
interpolation check, and the falsify-under-<32 residual path. Read-only on the lane.
Probes and receipts: `probe-receipts.txt` (11 receipts: command, exit, stdout sha256, UTC);
inputs in `inputs/`. Snapshot taken mid-wave (59 seat dirs present, 49 settled at last read).

Severity: HIGH = a stated gate can pass a defect it claims to catch, or a claimed round path
violates a binding rule. MED = visibility or definition gap that will mislead the L1's count.
LOW = hygiene.

## Answers to the four attack questions

1. **Round total <=128 and round-wide attack share.** Every defined outcome stays <=128:
   w1 64 + falsify 32..64 = 96..128; w1 64 + residual <=8 = 65..72 (falsify and residual are
   exclusive by the claims). It holds only while the falsify is hard-capped at 64 and no
   residual co-occurs; no tool enforces this (see F9). Attack share, definition used:
   **attack role = reviewer, critic, mutation-tester, labrat, sentinel, revenger** (the claims'
   own list, the broadest reading). w1 = 24/64 = 37.5%. Round-wide under that definition
   is >=25% only if the falsify is attack-heavy: with a falsify of N zero-attack seats the
   share is 24/(64+N), which falls below 25% at N=33 (24.7%) and is 18.8% at N=64. Under the
   r51 three-role definition (critic, reviewer, mutation-tester) w1 is 19/64 = 29.7%. Three
   definitions are in circulation (see F12). ANSWER: met in every outcome only if the falsify's
   composition is fixed; not guaranteed by the claims text.
2. **Dead / partial status.json.** Partial JSON is VISIBLE (lands in `unknown` and
   `parse_errors`; probe B1). A missing status.json inside an existing seat dir is VISIBLE
   (`missing`). A seat that never created its directory is INVISIBLE (F3). A seat that reports
   `blocked` PASSES `--check` (F4). The r51 lesson is therefore only half-kept.
3. **Interpolation check blind spots.** The checker is vacuous on the artifact that actually
   spawns seats (F1) and blind to lowercase, single-character and angle-bracket placeholders (F2).
4. **Falsify finds <32.** The claims leave items 9-31 with no compliant path (F7), the
   "residual <=8 `task` call" is prohibited by the lane addendum (F6), and a 32-63-seat falsify
   cannot be a v2 wave (waveMinLanes 64) so the falsify is a mixed-policy round that the
   addendum's shape rule does not list (F8).

## Findings

**F1 HIGH — the dispatch placeholder check cannot fail on the rendered dispatch.**
`ExecWaveCheck/check-dispatch.py` reads only top-level `context` and `items[].prompt` (the spec
schema). The file that spawns seats is `w1-dispatch.json`, whose text lives under
`taskCall.context` and `taskCall.tasks[].task`. Probe A1 (receipt `A1`): a rendered dispatch
with `{LANE}`, `{W1}` and `{UNRESOLVED_X}` planted in `taskCall` returns "clean", exit 0. The
gate passes on any input without `items`, so it is vacuous for dispatch. The selftest covers
only spec-shaped fixtures. Also `gen-w1.py` does not pass the rendered file as the second
argument, so the ready file is never gated on the rendered text. Fix: scan `taskCall.context`
and `taskCall.tasks[].task` as well; exit 2 (could-not-evaluate) on an input with neither
`items` nor `taskCall`; add a selftest on a `taskCall` fixture that must go red. The current
spec itself is clean for `{UPPER}` markers (checked: 0 hits in context and all 64 prompts),
so the r51 defect did not recur in the spec, but the gate that claims to stop it cannot fail.

**F2 HIGH — placeholder blind spots pass as clean.** Probes A2: `{lane}` (lowercase) exit 0;
`{X}` (single character) exit 0; `<BASE>` (angle) exit 0; `<BASE>` inside a command
exit 0. The regex `\{[A-Z_0-9]{2,}\}` is the only detector. Live spec uses angle tokens in
executable commands that the context never defines: ExecCensusCheck `--rev <BASE>` (the seat
resolved it to `ab0eafed` in its receipt, so the defect is latent, not realised), and
ExecMisrootSweep `git -C <fleet>` (no definition in context). Other angle tokens
(`<stem>` in ScribeBlock27, `<SeatName>`, `<YourSeatName>`, `<role>` in the contract prose) are
intentional templates and cannot be told apart from unresolved ones by a regex. Nested braces
`{{LANE}}` are caught (probe D; flagged as `{LANE}`) because the render leaves single braces.
Fix: an explicit allow-list of intended angle tokens, every other `<...>` in an item or command
fails; a fixed set of required definitions in `context` (`<BASE>`, `<fleet>` must be defined
or removed from executable text); lowercase and single-char brace tokens fail.

**F3 HIGH — never-started seats are invisible in the accounting.** `ExecStatusHelper`
`summarize()` enumerates directories only. `seats_total` = dir count (live: 59, spec: 64) with
no `expected` field. `--check` reads the expected names, exits 1 when any fails, and prints
only the summary, not which expected seat failed. Probe B1: a named expected seat
`NeverStartedSeat` with no directory is absent from output; exit 1 is the only signal. Probe
B4 against the real 64 names: the output's `missing` list names only directory-holders
without status (`CritBand`, `CritTriV6`, `MutControlsV2`, `ScoutCensusRecheck`,
`ScoutV6Corpus`). At the first read (~10:50Z, 07:50 local) 12 spec seats had no directory at
all; the accounting does not name them, so that absence is invisible in the evidence.
This is the exact r51 failure mode ("dead seats stay dead in the evidence"). Fix: output
`expected` (count from the expected file), `absent` (expected names with no directory,
named), and `not_settled` (name + status) on every run; `seats_total` from `expected`.

**F4 MED — `--check` accepts `blocked`.** `VALID = {settled, failed, blocked}`. Probe B3:
a blocked-only expected set returns exit 0. The claims and the addendum describe the gate as
"parseable settled|failed"; the code and the doc disagree. Also a `failed` seat passes the
gate, so the exit code means "reported", not "succeeded". Fix: exit codes separate
"all settled" (0), "reported but non-settled present" (3), "expected seat unreported or
unparseable" (1); print the non-settled list.

**F5 MED — roles are self-reported; the spec role is not checked.** `by_role` counts the
seat's `status.json` role. Seven seats disagree with the spec: ExecCounterV2 (self `task`,
spec `executor`); LB1V5Audit (self `reviewer`, spec `executor`); LB2OfflineClause (self
`mutation-tester`, spec `executor`); LB3CensusIdem (self `task`, spec `executor`); LB4Mknod
(self `labrat`, spec `executor`); RevCounterEscape and RevExtractor (self `reviewer`, spec
`revenger`). Attack share computed from self-report would be wrong (LB2 and LB4 add attack
roles that the spec does not give them). The `by_role` output already contains roles the
spec does not have (`task`: 2). Fix: `by_role` keyed by the spec's role from the expected
map; self-report mismatch reported as its own finding.

**F6 MED — round-shape conflict: the residual `task` call is prohibited.** The claims say "one
residual `task` call of <=8 reviewer/critic seats" (routed defect 1). `lane-addendum.md`
line 140-142 (binding inline handoff): "NEVER call `task` / `tool.task` yourself for a wave or
a residual call." The claims route contradicts the binding rule. A <=8-seat wave also fits
neither listed shape ("one v2 wave of 64-128, or two v1 waves (32-64 each)"; addendum line
78); v2 waveMinLanes is 64 and v1 is 32, so <=8 is below both bands. Fix: the residual must be
expressed as a validated wave, which cannot be <=8 under either band; the claims must either
drop the residual or declare it as a non-band exception with an addendum amendment.

**F7 HIGH — no compliant path for 9..31 distinct attack items.** The claims trigger the
falsify wave on `>=32 distinct attack items` and the residual on `<32` with "<=8 seats". Items
9..31 have no compliant route: a residual of 9..31 breaks the <=8 cap, and a falsify below 32
breaks the 32-64 band. "Distinct" is undefined (dedupe key, who counts). Fix: define the
threshold on the count the falsify will actually dispatch (e.g. `N = min(distinct, 64)`
requires N >= 32 under v1), and state the outcome for N < 32 as a stop or a declared
exception, not a residual of arbitrary size.

**F8 HIGH — falsify under v1 after a v2 w1 is a mixed-policy round the shape rule does not
list.** Addendum line 78 lists exactly two shapes: one v2 wave (64-128), or two v1 waves
(32-64 each). The claims' w1 is v2 (64) and w2 is v1 (32-64). Under v2, a falsify of 32-63 is
below waveMinLanes 64 and a falsify of 64 for fewer than 64 items is padding (forbidden by the
addendum: "never pad"). Fix: w1 is already a dispatched v2 wave, so it cannot be
re-banded. The only shapes that remain compliant are: (i) an addendum amendment that declares
"one v2 wave + one v1 falsify (32-64)" as a legal mixed round with the <=128 total stated; or
(ii) a falsify that is a v2 wave of exactly 64 seats, which is padding whenever the distinct
attack count is below 64 (forbidden). The claims must pick (i) or drop the falsify; (ii) is not
an option under the "never pad" rule. Option (i) also needs the amendment in the freeze commit.

**F9 MED — the <=128 cap is enforced by nothing.** No script sums waves. Proof the cap can be
broken silently: 30 of 64 dispatched seats carry runtime-deduplicated ids (`<name>-2`..`-4`
in `w1.ready.dispatched`). If someone counts ids rather than seats, the w1 count reads 64+35
= 99 spawns. These suffixes are name collisions (F10), not replacements; the cap has no tool.
Fix: `round-total` check in the accounting: spec seats + falsify seats + residual <= 128,
counted by policy seat name, never by runtime id.

**F10 MED — name collisions with round 51.** 28 of the 30 suffixed dispatch ids reuse round-51
seat names (`ExecCounterV2`, `ScribeEntryC1`, `CritRuleDerive`, ...). The dispatcher's
`live(name, run)` matches by name, and `adopt()` falls back to names when handles are lost. A
live round-51 agent with the same name can be read as this wave's seat. Fix: round-52 seat
names unique within the lane (`R52` prefix or a per-wave suffix) before the falsify wave.

**F11 LOW — status artifacts are not verified.** 4 of 294 referenced artifacts do not exist:
`CritRetry/receipts.json`, `ScribeScorecard/ScribeScorecard/section.md`,
`ScribeScorecard/ScribeScorecard/receipts.json`, `ScribeScorecard/ScribeScorecard/v5-baseline-claims-draft.json`
(the last three are nested under the seat's own name: a relative-path mis-nesting). The
accounting counts these seats as settled. Also 3 summaries exceed the 40-word limit
(ScoutCarrierChain 65, ScoutQualRows 51, SentSecrets 50); not checked. Fix: `--check` asserts
each artifact exists inside its seat dir (no `..`, no absolute paths) and the summary is <=40
words.

**F12 MED — attack-share definition is not frozen.** Three definitions appear:
(a) claims text: reviewer, critic, mutation-tester, labrat, sentinel, revenger = 24/64 = 37.5%;
(b) r51 accounting: critic, reviewer, mutation-tester = 13/36 = 36%;
(c) the spec generator (`gen-w1.py` final line): critic, reviewer, mutation-tester, labrat
= 19/64 = 29.7%. Round-wide, see answer 1 (falsify composition decides). Fix: freeze one
definition in the claims text and the accounting script, and require the falsify's composition
such that (24+a)/(64+N) >= 0.25 holds.

**F13 LOW — dispatched text differs from spec text.** The dispatcher appends trailers to each
seat's task (e.g. ExecCounterV2: "Lane bounds: leaf member — no subagent dispatch except your
single labrat", a milestone line, a `Report:` line). The spec prompt does not contain them, so
spec-level audits (SentWaves, the placeholder check) do not see the text the seat receives.
Fix: audit the dispatched `taskCall` text, not only the spec.

## Verified-clean (for the record)

- The current spec has no `{UPPER}` placeholders (0 hits, 64 prompts + context). The r51 M51-6
  defect did not recur in the spec.
- `LOG.md` now contains commit `646d29c9` (grep count 1): r51 spotcheck item 1 is resolved.
- `SHONEN.md` body equals the PROTOCOL.md seed block with `<name>` = `kaidoku-shokunin`
  (byte-identical after stripping the comment header; checked): r51 spotcheck item 2 resolved.
- r51 spotcheck item 3 (C3 freeze-drift not gating) is NOT yet evidenced for round 52:
  `ExecCounterV2/status.json` says the drift-selftest semantics "remain unimplemented"; no v6
  or counter draft in the wave gates drift. Route to the L1 as open.
- Snapshot of the seats that matter for the freeze (at ~11:10Z): ExecCounterV2 failed,
  ExecControls blocked, ExecFetchVendor blocked (offline guard witnesses not implemented).
  Snapshot only; these are the L1's to act on.

## Observed fleet-root state (not touched)

`git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all` shows two
modified tracked files and no untracked strays: ` M .scratch/goal-20261029-hyaku-run12.md`,
` M .ufo/l0-questions.md`. Operator-side; not mine; not written by this seat.

## Scope note

Read-only on the lane. Wrote only under `.ufo/waves/round-52/w1/CritBand/` and
`.ufo/waves/round-52/w1/CritBand.md`. Nothing committed, staged, or pushed. No REA, no
--data-run, no vendor download. Tooling: none installed.
