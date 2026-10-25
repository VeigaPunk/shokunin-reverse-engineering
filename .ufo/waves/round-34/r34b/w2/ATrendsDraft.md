# ATrendsDraft — R34-C2 trend verdicts and SHONEN draft (round 34, r34b, wave 2)

Seat: `L1Kaidoku34-2.ATrendsDraft` (scribe). Assignment: draft the report's `Trend verdicts`
(expansion / quality / discernment, evidence per axis) and four `SHONEN` boxes for a stopped
round, each `[~]` or `[ ]` with a resolvable pointer; no `[x]` without a named non-author
verifier. No score, label, target, clause, frozen instrument, `claims.json` or `claim-stop.json`
is touched by this seat. All writes are this report and `/fast/scratch/hyaku/kaidoku-r34b/w2/ATrendsDraft/`.

Lane tip moved while this seat ran (`cd75b92e` → `66b84027` → `5a0435ff`); every assertion below
carries the UTC at which it was observed. No peer was messaged; `agent://all` was not used.

## Axes named (Godspeed)

- **A1 expansion** — did the round add verified domain ground, a Core/PROVINCE row, or a
  capability row? (proxy: command A mapping, PROVINCE diff, fixture provenance)
- **A2 quality** — did the round improve records/instruments with red/green or recomputable
  evidence, and are its remaining limits disclosed? (proxies: receipts, pin hashes, predicate
  hashes, QUALITY rows, the gate's own class set)
- **A3 discernment** — did the lane refuse credit it had not earned, against interest?
  (proxies: stop record, score deltas, disclosure of defects, wave-2 corrections)
- **A4 SHONEN pointer resolvability** — does each box's pointer resolve to committed bytes at
  the stated revision?
- **A5 no-score / no-capability integrity** — 10→10, delta 0, no capability row.

## Probes actually run (exact argv, exit, UTC; Python 3.14.8, git 2.56.0)

All from cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `date -u` printed in the same
invocation as each probe unless noted. No ELF carrier or reader was executed as a program of
interest; the R34-C1 production reader and its twelve carriers were not executed.

| # | command | exit | UTC | observed |
|---|---|---|---|---|
| P1 | `sha256sum tools/round-34/c2-shortcut-gate-counter.py tools/round-34/replay-gate.py tools/round-34/gate-config-mini.json tools/round-34/gate-config-naive.json tools/round-34/mini-fix/mini-counter.py tools/round-34/mini-fix/build.py tools/round-34/mini-fix/expected.json .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` | 0 | 07:28:54Z | 8/8 digests equal the `claims.json` pins / stop `source_sha256` (counter `41d59703…`, gate `8fa94b23…`, configs `4483f385…`/`72b12941…`, mini `43ef669f…`, build `c6718051…`, expected `5ebb5349…`, nameset `2e8feaea…`) |
| P2 | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34/r34b --claims .ufo/waves/round-34/r34b/instruments.json --rev HEAD` | 0 | 07:30:09Z | `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=HEAD`; 26× `ok … commits_after_freeze=0` |
| P3 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out /fast/scratch/hyaku/kaidoku-r34b/w2/ATrendsDraft/c2-at-c79bbe7b-w2.json` | 0 | 07:30:09Z | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-` (2.50 s) |
| P4 | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed <kaidoku-r34-mini-v1|alt-1|alt-2>` (3 runs) | 0 each | 07:30:21Z | `{"finding":"records_match","matched":8,"met_target":true,...}` each seed — decisive counterexample reproduced |
| P5 | inline `python3 -I -B` recomputing `sha256(text)` for the three sites in `predicate-reconciliation.json` | 0 | 07:35:29Z | A `7c6c17f0cca6c680…`, B `8340aea51154fc0e…`, C `09988625205de2eb…`; `all_match=True` |
| P6 | `python3 /fast/scratch/.../cmdA.py <rev>` (verbatim SCORECARD "Measurement recipes — A", `SCORECARD.md:94-122`) for `ec3125ad`, `66b84027` | 0 each | 07:35:11Z | base: `knowledge_files 120, mapped 120, coverage 10.0, rule_blocks 17, citation_resolved_rules 17, depth 10.0`; tip: `122/122, 17/17, 10.0/10.0` |
| P7 | same command A for `5a0435ff`, `HEAD` | 0 each | 07:35:54Z | `5a0435ff`: `122/122, 17/17, 10.0/10.0`, missing `[]`, dangling `[]`; `HEAD` identical |
| P8 | read-only `git rev-parse HEAD`, `git log --oneline`, `git status --porcelain`, `git show <rev>:corpus/SOURCES.md \| grep -c '^| S'`, `git diff --stat ec3125ad..HEAD -- PROVINCE.md` | 0 | 07:33:56–07:37:20Z | tip `5a0435ffb9a8921206144e0b61fe3c12a89b59c2`; PROVINCE diff empty at `5a0435ff`; SOURCES rows: `ec3125ad 102`, `c79bbe7b 105`, `66b84027 105`, `5a0435ff 105`, worktree `106` |
| P9 | `sha256sum` on the addendum's five artifacts | 0 | 07:37:25Z | all five digests equal `claim-stop-addendum.json`: nameset receipt `fa6e8f09…`, payload receipt `23e26fe4…`, `payload_keyed.py` `0e125169…`, pin receipt `d68e4e17…`, nameset source `2e8feaea…` |

Tool installs/updates: **none** (no `uv`, `npx`, pacman, cargo or npm invocation).

## Draft — `## Trend verdicts`

> Paste-ready; replace the existing one-line "Learning trends" if the L1 prefers prose. Every
> pointer is to committed bytes at `5a0435ff` unless marked worktree.

- **expansion: unchanged.** Round 34b added an instrument and its stop, not domain ground:
  `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:3` states "instrument
  retained; **capability denied**"; `corpus/README.md:88` holds it "as a tool, not as capability";
  the eight `MREC` fixtures are synthetic and `claims.json` `instrument_notes` says they "are never
  domain evidence and no ELF carrier is reused from R34-C1"; R34-C1's twelve carriers were not
  executed. No PROVINCE or Core row changed: `git diff --stat ec3125ad..5a0435ff -- PROVINCE.md`
  is empty (exit 0, P8), and the scorecard enters no capability row (`SCORECARD.md:3361-3363`,
  coverage/depth/calibration 10→10). Command A at `5a0435ff` measures `122/122` knowledge files
  mapped, 10.0, and 17/17 craft rule blocks, 10.0 (P7, exit 0, 07:35:54Z): two new entries are
  indexed, so the proxy does not move — curation, not coverage. S106 is admitted as an instrument
  source (`corpus/SOURCES.md:111`), scoped "not any carrier, not a gate verdict".
- **quality: improved, bounded.** The improvement is record-side and recomputable: (a) five record
  defects are disclosed with repair state (`claim-stop.json` `record_defects_disclosed` F1–F5);
  (b) F1 now has a committed receipt — `after/freeze-integrity-instruments.txt` prints
  `CLEAN pins=26 freeze=b917ea64ebbe rev=66b84027…`, and this seat independently reproduced
  `CLEAN pins=26` (P2, exit 0, 07:30:09Z); (c) F5 is closed by `b917ea64` (`git ls-files
  .ufo/waves/round-34/r34b/{before,after,controls}` = 3 + 14 files); (d) F2's three predicate
  hashes recompute exactly (P5, exit 0); (e) the wave-2 addendum binds the decisive class to an
  exact-argv/UTC/seed receipt (`w1/CtlMultiset-files/nameset-green-receipt.json`, four seeds) and
  commits a second class source (`payload_keyed.py`, `0e125169…`); all five addendum artifact
  digests verify (P9, exit 0, 07:37:25Z); (f) the frozen counter's six
  clauses reproduce at the freeze bytes (P3, exit 0); (g) QUALITY 74 and the appended corrections
  to 68/70 narrow claims the wave-2 attack disproved. **Bounds:** the gate's *evidence set* is
  thin — `w1/MutShortcutClasses.md` F2 measures four of the seven registered classes as
  non-competitive even on the shape-only red counter, and F4 shows `met_target` is trusted without
  `met_target == (matched == target)`; `--rev` is an argv echo; class-count equality cannot detect
  an unregistered class (QUALITY 70 correction); no frozen instrument was repaired (correct); and
  at the committed tip the S105 restore is worktree-only (finding F3). The verdict is improved for
  disclosure/receipt discipline, **not** for the green surface or the capability.
- **discernment: improved.** The lane stopped on its own counterexample before production and
  before any credit: no capability row, no score movement (10→10, delta 0), no target/class/label
  change (`claim-stop.json` `kill_rule_applied`, `not_claimed`). The decisive class is independently
  reproducible (P4: 8/8 at three seeds, exit 0, 07:30:21Z) and now receipt-bound with exact argv and
  UTC (`nameset-green-receipt.json`; `claim-stop-addendum.json`), which supersedes the stop record's
  "approximate" `l1_rerun_utc`. Against interest, the lane then let wave 2 attack its own record and
  accepted the result: wording correction D1 ("decodes no header field…" replaces "reads no
  header"), D2 (three predicate sites, not two), QUALITY 70 narrowed, M34-12/QUALITY 74 added for a
  row swap it caused. **Debit:** the stop's authority is cited as "§9 of the round contract"
  (`corpus/knowledge/…-stop.md:48`, `LOG.md:3098`) with no in-lane pointer, and the freeze's only
  transform was layout-only, which `w1/ExecRedReproduce.md` §5.1 proves cannot exclude a
  layout-invariant key — a design-quality debit, not a reason to re-open or re-score.

## Draft — `## SHONEN (operator note)`

> All four boxes `[~]`; no named non-author verifier exists, so no box is `[x]`.

```
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  asserted: `SKILL.md:81-314` (craft section; heading at 81, last non-blank line 314, next
  heading at 319), freshly measured by command A (`SCORECARD.md:94-122`) at `5a0435ff`:
  `rule_blocks 17, citation_resolved_rules 17, depth_score 10.0`, exit 0, 2026-10-25T07:35:54Z;
  round-34 instrument registry `SKILL.md:1209-1221` routes its limits to QUALITY 68-74; S106 at
  `corpus/SOURCES.md:111`. Resolvable citations only, not a semantic audit; no promotion verifier.
- [~] At least one end-to-end domain task executed and logged in LOG.md
  asserted: historical 2026-10-15 libjq open → instruction decode → export → close, `LOG.md:425`,
  `corpus/lessons/2026-10-15-round-1.md`, bundle `evidence/round-1-2026-10-15/rea-bundle.json`
  (18,991 bytes). Round 34b executed no end-to-end domain task: C2 is instrumentation and C1 was
  stopped before production, so this box rests on the historical record; no independent verifier.
- [~] Instructions executable by an agent without oral context
  asserted: command A (`SCORECARD.md:94-122`) was executed verbatim by this non-author seat at
  `ec3125ad`, `66b84027` and `5a0435ff`, exit 0 (P6/P7, 07:35:11–07:35:54Z); the bounded reader
  recipe at `SKILL.md:1177-1179` was not executed this round, and the historical round-1 execution
  is author-side. Partial, not a non-author run of the lane's end-to-end instructions.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
  asserted boundary only: `PROVINCE.md:97-118` (`## Adjacent` refusal list, safety refusal at
  :116-118); `git diff --stat ec3125ad..5a0435ff -- PROVINCE.md` is empty; round-34b artifacts are
  in-domain (S106 binutils `readelf.c`; synthetic `MREC` fixtures declared non-domain). Province
  version pins at `PROVINCE.md:8-14,24` were not re-measured; no complete-accuracy claim.
```

Rationale for no `[ ]`: each box is still supported by committed evidence at a named revision, with
the specific gap stated in-line; none is contradicted. Rationale for no `[x]`: no non-author
verifier is named for any box.

## Findings (constraints on the report, not repairs)

- **F1 — closed during this seat (receipt now exists).** At `66b84027` no committed
  `freeze-integrity` receipt existed for the 26-pin container; only a seat scratch run
  (`w1/ScribeSkillRegistry.md:111`, 07:24:45Z) and this seat's P2. At `5a0435ff` it is committed:
  `after/freeze-integrity-instruments.txt`, `CLEAN pins=26 freeze=b917ea64ebbe rev=66b84027…`.
  Note `freeze=b917ea64`, not `c79bbe7b`: the container was created after the freeze because the
  frozen `claims.json` did not carry the accepted shape — stated verbatim in
  `claim-stop-addendum.json` `enforced_pin_receipt.note`.
- **F2 — corrected, not a defect anymore.** `predicate-reconciliation.json` lists three sites, not
  two: A `7c6c17f0…` (31 words), B `8340aea5…` (46), C `09988625…` (26, the green counter's own
  label). All three recompute (P5). The report must not repeat the old "one predicate, two
  sentences" framing.
- **F3 — open at the committed tip.** Lesson M34-12 states S105 was "restored verbatim … end
  recount 106 rows", but at `5a0435ff` `corpus/SOURCES.md` has **105** rows and **no S105 row**
  (`git show 5a0435ff:corpus/SOURCES.md | grep -c '^| S'` = 105, exit 0, 07:35:54Z); the worktree
  has 106 rows including S105 (`M corpus/SOURCES.md`, 07:35:54Z). Cite the restore as worktree
  state until it is committed, or the report will assert a committed fact that is not there.
- **F4 — open.** The stop's governing rule is cited as "§9 of the round contract"
  (`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:48`; `LOG.md:3098`)
  and `claim-stop.json` states only "Frozen before data: a target met by a control that skips the
  claimed work is not an improvement." No in-lane file defines §9 (bounded search of
  `SCORECARD.md`, `LOG.md`, `corpus/**`, `.ufo/waves/round-34/**`); name the round-contract file or
  quote the rule inline in the report.
- **F5 — wording bound on the quality verdict.** `SCORECARD.md:3365` says "the six routed
  criteria" (QUALITY 68-73) while `5a0435ff` adds 74; and "quality improved" must be read with
  `w1/MutShortcutClasses.md` F2 (four of seven registered classes non-competitive) and F4
  (`met_target` trusted) as explicit limits. Do not let the trend line imply the green surface or
  the class set improved.
- **F6 — stop-record wording, now corrected at the source of truth.** The stop's
  `decisive_counterexample.why_this_falsifies_the_surface` says the shortcut "reads no header,
  walks no record array and reads no name_off"; the file reads the whole buffer and regex-scans
  (`nameset.py:48-53`). The addendum's D1 replaces this with "decodes no header field…" and notes
  blindness is content-contingent. Use D1's wording in the trend section.
- **F7 — moving tip.** HEAD was `cd75b92e` at 07:28Z, `66b84027` at 07:33:56Z, `5a0435ff` at
  07:35:29Z. Probe timestamps above are authoritative; a later tip may change F3's status.

## Out of scope / not run

- No adjudication of the stop, no score, no capability, no re-freeze, no target/class change, no
  edit to frozen instruments, `claims.json`, `claim-stop.json`, SCORECARD/LOG/SKILL/PROVINCE or
  corpus. No VCS mutation; no git/jj write command.
- Not run: the R34-C1 production reader and its twelve carriers; a non-author verifier for
  SHONEN; a fresh PROVINCE version-census; `SKILL.md:1177-1179` recipe execution; the gate's
  registered-class strengthening (other seats' scope). These are marked unrun, not passed.
- Peer wave-2 reports landed during this seat (`w2/ACounterexample1.md`, `AStaticBlindness.md`,
  `AStopCompleteness.md`, …) were read only for state reconciliation where their content is bound
  into `claim-stop-addendum.json`; this seat did not audit them.

## Artifact paths

- Report: `.ufo/waves/round-34/r34b/w2/ATrendsDraft.md` (this file).
- Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/ATrendsDraft/` — `cmdA.py` (verbatim recipe A),
  `c2-at-c79bbe7b-w2.json` (P3 receipt).

**TRENDS_DRAFT verdict:** `expansion=unchanged; quality=improved(bounded); discernment=improved;
SHONEN=4/4 [~], 0 [x]; scores 10/10/10 unchanged, delta 0; no capability; tip=5a0435ff; probes
P1–P9 exits 0 at 2026-10-25T07:28:54Z–07:37:25Z; open items F3 (uncommitted S105 restore),
F4 (unpointed "§9"), F5 (quality wording bound), F6 (use corrected blindness wording).`
