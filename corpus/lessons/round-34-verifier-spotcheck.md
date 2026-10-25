# kaidoku round 34: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_flash)

Session `ClosureKaidoku34`, 2026-10-25. Range `f432c8e3bc58934887c83f1db2b26f9910a9d87f..2e8a775849f5f4a8e6363d835c85ed8ef2154149`
(base of the round's original attempt `ec3125ad3d130d92f888a4128dfaa2982f36fff7`). Report
`.ufo/reports/round-34/kaidoku.md` in the fleet repo (`23cf8e41`, by the lane identity; it supersedes the
run-5 attempt-1 report `27322359`, which stays in history). Claims read: **R34-C1** (inherited, stopped in
run 5) and **R34-C2** (declared and stopped in this re-dispatch).

No seat was dispatched: every re-check below was run inline by this session. No lane counter, gate,
selftest, parser, reader or REA tool was executed here — PROTOCOL §Gate standard, Closure consequence
(verify committed evidence, never execute a sibling's gate). No jj command was run except
`scripts/hyaku/jj-lane.sh state` (read-only, pure git), and no jj transaction was opened. No `/fast/scratch`
path was opened. Nothing was installed or updated.

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-10-23T07:19:48-03:00 launch kaidoku round=34 pgid=8630 driver=hyaku-inline attempt=1
2026-10-23T08:22:51-03:00 complete kaidoku round=34; hyaku-inline attempt=1
2026-10-23T20:41:32-03:00 complete kaidoku round=34; hyaku-inline attempt=1
2026-10-25T03:33:31-03:00 launch kaidoku round=34 pgid=1973081 driver=hyaku-inline attempt=1
2026-10-25T04:57:43-03:00 complete kaidoku round=34; hyaku-inline attempt=1
```

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an %ae %H %ad' -- .ufo/reports/round-34/kaidoku.md` (fleet) | `kaidoku-shokunin kaidoku@shokunin.local 23cf8e41… 2026-10-25 04:56:55 -0300`; 16 commits touch the path, all by `kaidoku-shokunin` | pass |
| filed bytes are the committed bytes | `git diff --stat HEAD -- .ufo/reports/round-34/kaidoku.md` | empty | pass |
| `SHONEN` heading, one line per box | `grep -c '^- \[' SHONEN.md` = 4; report `## SHONEN` | 4 lines, all `[~]` with pointers; `SHONEN.md` unmodified in the round diff | pass |
| cited lane commits exist and are ancestors | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> main` for all 23 cited hashes (`ec3125ad c79bbe7b cd75b92e 66b84027 5a0435ff b917ea64 417a8211 b62b4767 1675a8d8 2eafca42 39f433b2 c05984e7 06afa9e7 6ae73906 dc7384ec debc8dad 6e2f9b79 f8f3758a b839f611 35152484 2e8a7758 54a87a51 f432c8e3`) | 23/23 resolve, 23/23 `anc=yes`; authors `kaidoku-shokunin` except the pre-round base `ec3125ad` (`protocol-shokunin`) | pass |
| report not filed before its commits | `git log --format='%h aI=%aI cI=%cI'` on both repos | lane tip `2e8a7758` 04:57:15 -0300; report commit `23cf8e41` author 04:56:55, **committer 04:57:23** -0300 — the report's bytes were finalized and committed 8 s *after* the tip it cites. The earlier author timestamp is inherited from the pre-amendment content; no cited hash postdates the report commit in committer order | pass |
| lane repo clean and pushed | `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `git -C … status --porcelain` | `branch=main local=2e8a7758 remote=2e8a7758 ahead=0 behind=0 head=detached tracked=0 untracked=0`; status empty | pass |
| prompt carries the round contract | read `.ufo/prompts/kaidoku-round-34.md` (481 lines) against `templates/round-prompt.md` | §1 MISSION/AXES + 1–3 claims + lowest-axis rule; §2b frontier step with the census command; §3 L2 floor 8; §4 report contract with report path, `SHONEN`, commit-hash citation rule; §5 commit-then-push, push scope, L0 channel; §6 hyaku addendum (waves 32–64, routes, capacity, seat paths, write scope). All five child-lane items present | pass |
| not a marker | report content | work performed, 11 distinct `.ufo/waves/round-34/…` paths + 45 `w1/…`/`w2/…` seat reports all resolve on disk, landed-changes table tied to commits, `LOG.md` entry appended (+11 lines, no deletions) | pass |

Conformance defects are recorded under **Routed defects** (D-1, D-2, D-3, D-4); none of them changes the
lane-round status.

## Claims — re-derived against `2e8a7758`

### R34-C2 (depth, capability acquisition) — falsified measure, honest stop

The claim's counting command is the lane's own; I re-derived its before→after from committed bytes
only, then tested the claim's central assertion against the decisive counterexample source.

| step | command I ran | observed |
|---|---|---|
| before: gate absent at the base | `git ls-tree -r --name-only ec3125ad \| grep -c 'tools/round-34/'` | `0` — no gate, no config, no fixture at the base. The committed before receipt `before/c2-at-base.txt` reads `GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad3d13… gate_path=tools/round-34/replay-gate.py`; its exit 2 is carried by `claim-stop.json`'s `frozen_counter_verdict` context and by the SCORECARD row, and the `.txt` receipt is a one-line verdict with no exit field — a receipt-shape limit of the same family as QUALITY 73, disclosed with the round |
| after: the frozen instruments exist and are the pinned bytes | `sha256` over `git cat-file -p c79bbe7b:<path>` for all 26 entries of `.ufo/waves/round-34/r34b/instruments.json`, then again at `2e8a7758` | 26/26 match at both revisions, 0 missing; `claims.json` digest `de3afbfb…` equals the container's `frozen_claims_sha256` at both revisions |
| after: the six clauses | `after/c2-at-instruments.json` | `measured_revision=c79bbe7b…`, `exit 0`, `selftest_failures=0`, `selftest_exit=0`, `mutants_killed=3`, `red.verdict=REPLAY_GATE_REFUSED` (exit 2), `green.verdict=REPLAY_GATE_CLEAN`, `green.positive_matched=8`, all six `clauses` true — identical to the report's verdict line |
| five pre-data controls all miss | `controls/*.json` | `gate-always-clean` 4/6 (`red_refused`, `selftest_clean` false), `gate-junk-clean` 5/6, `gate-no-positive-check` 4/6, `gate-vacuous-no-floor` 5/6, `do-nothing` `gate_absent`; each names its failing clause, exit 1 (2 for do-nothing) |
| the decisive class is real and blind | `sha256sum w1/CtlMultiset-files/nameset.py`; read the source | `2e8feaea92eedb8d…` (matches the report and `claim-stop.json`); the file regex-scans NUL-terminated SONAME tokens, sorts the set, and replays a stored `name→(flags,value)` table — it decodes no header field, no record entry and no `name_off` |
| it scores the same target the gate clears on | `w1/CtlMultiset-files/nameset-green-receipt.json` vs `gate-config-mini.json` | the receipt's `argv` runs `tools/round-34/mini-fix/mini-counter.py --control-reader nameset.py` at seeds `kaidoku-r34-mini-v1 alt-1 alt-2 alt-3`, each `matched 8 / target 8 / met_target true`, exit 0; `gate-config-mini.json`'s `counter.argv` is that same counter, and `counter_sha256 43ef669f…` equals its pin. The counterexample therefore reaches the gate's own green surface, not a lookalike |
| the stop's premise holds | `LOG.md`/lesson claim: registering the class flips the gate to REFUSED | evidence-verified, not re-executed (`claim-stop.json`, `w1/ExecRedReproduce.md`, `w2/ACounterexample2.md`); consistent with the config's `{reader}` slot and the refusal branch |

Consequence: the claim's demonstration — that the frozen fixture set forces structural record traversal —
is falsified by a class the freeze did not register. The six clauses being true is exactly what the round
records and what it refuses to bank. **No score, no capability row** (the `## Capabilities` table still
ends at the round-27 rows; no R34 row anywhere in `SCORECARD.md`). Axis verdict: `unchanged`.

### R34-C1 (depth, inherited stop) — unchanged, untouched

| step | command | observed |
|---|---|---|
| the frozen counter did not move | `sha256` over `git cat-file -p <rev>:tools/round-34/version-needs-counter.py` at `54a87a51` and `2e8a7758` | `d7f0a8cf3ca08562…` at both revisions, equal to the digest the lesson cites |
| five named artifacts byte-identical | `git diff --name-status f432c8e3 2e8a7758 -- <five paths>`; blob OIDs both ends | empty; `claims.json d56fb8d7…`, `claim-stop.json 9e487015…`, `version-needs-counter.py ac89ecd0…`, `elf-version-needs.py f69688ed…`, `size_lookup.pristine.py 784fc60a…` — identical OIDs at both revisions |
| the decisive control met the target | `w1/CtlLabels-files/size-pristine.receipt.json` + `size-summary.json` | `matched 12`, `exit 0`, `documents_ok true` on **both** schedules, `translated_inputs 11`, `395` fixed-slice reads / `5,741` bytes per schedule, `counter_sha256_before = _after = d7f0a8cf…`; the mutant control is killed (`matched 1`, exit 1) and restoration is byte-exact |
| no production reader ran | report + `RevR34C1Untouched.md` (183 execve, all `/usr/bin/python3`; two independent methods on the five artifacts) | evidence-verified; the seat's own limit (a python reader is arbitrary code) is disclosed in the lesson, so the claim is "no scoring hit", not "no execution" |

The inherited stop stands and the re-dispatch added nothing to it. Axis verdict: `unchanged`.

## Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| depth | unchanged | both claims stopped; `SCORECARD.md` own axis row stays `10 → 10` and its 17/17 queue-drain proxy is 17/17 either way; no depth claim verified |
| coverage | unchanged | `PROVINCE.md` absent from `git diff --stat f432c8e3 2e8a7758`; one knowledge entry on instrument ground, no domain surface, no frontier row moved |
| calibration | unchanged | no measured self-assessment claim; the round's own record defects (D-1, D-2, D-3, D-4) are disclosed against interest, and three self-descriptions still disagree with the repository |
| operability / freshness / adjacency | unchanged | not claimed; the SKILL registry rows are runnable commands but no operability measure moved; the S106 recheck dates the only freshness touch |

No axis is harmed: `SCORECARD.md` gained one additive section (`git diff --numstat f432c8e3 2e8a7758` → `27 1`; the single deleted line is the round-34 C1 section's QUALITY-pointer sentence, a docs correction, not a frozen byte), `LOG.md` `11 0` append-only, `SKILL.md` `14 0`, `corpus/QUALITY.md` `19 0`, `corpus/README.md` `4 0`, `corpus/SOURCES.md` `6 1` (the S106 row plus the search-log line; the deletion is the leads-line rewording), `PROVINCE.md` and `SHONEN.md` untouched, no capability row entered.

## Discernment spot-check

Sources re-opened live by this session (`curl`), not merely read from the capture:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S106 binutils `readelf.c` @ `binutils-2_47` | admit, tier A, scope "section-header decode only" | `https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=6ce87bbc…` — HTTP 200, 689,644 bytes, sha256 `7e81eedf19b2…` = the row's capture digest | agree | line 14149 is exactly `warn (_("Missing Version Needs information\n"))` (6 words, ≤25); the anchored locations are right: `:14020` `case SHT_GNU_verneed:`, `:14056` the `endbuf` bound, `:14058` the `sh_info` loop, `:14072-14076` the Verneed field order, `:14102-14106` the Vernaux field order, `:467-470` the `DT_STRTAB`-derived string resolution. Three `\f` bytes in the file confirm the row's `+3` line-number caveat |
| S103 LSB 5.0.0 symbol versioning | admit, tier A, layout only | `https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html` — HTTP 200, sha256 `982fe1208c76…` = the row's capture digest | agree | line 717 carries the quoted 21-word sentence verbatim; the scope sentence correctly refuses numeric section constants and loader behaviour |
| S104 glibc 2.42 `elf/elf.h` | admit, tier A, layout and widths | `https://raw.githubusercontent.com/bminor/glibc/d2097651…/elf/elf.h` — HTTP 200, 195,524 bytes, sha256 `fd6e7f3e3c74…` = the row's capture digest | agree | the capture is the row's revision; the row's refusal to adopt the stale `vna_other /* Unused */` comment and its pointer to S103 for the field meaning is the right call |
| S105 System V gABI draft | reject, reason "no GNU version-needs definition", with a flip | `https://www.sco.com/developers/gabi/latest/contents.html` — HTTP 200, sha256 `860a6916…` = the row's capture digest | agree | line 3 is `System V Application Binary Interface - DRAFT - 10 June 2013`; `grep -ciE 'verneed\|vernaux\|gnu\.version\|symbol version\|sht_gnu'` over the four committed chapters (`gabi-contents`, `gabi-sheader`, `gabi-symtab`, `gabi-dynamic`) = 0, 0, 0, 0. A real reject, and the flip is stated |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0,
`ok` line plus 9 × `W04` duplicate-url warnings. Counted myself: rows 105 → 106, malformed 0,
tier `A=99 B=5 C=1` → `A=100 B=5 C=1`, status `mined=101 rejected=4` → `mined=102 rejected=4`. S106 is the
only added row (`A +1`), S105 is intact, no existing row's status/recheck/used-by changed.

## Trend verdicts

- **expansion: unchanged.** `PROVINCE.md` untouched; the one new knowledge entry is instrument/self-work on
  ground the coverage map already holds; no frontier bullet moved; no capability entered. The round says the
  same and does not claim otherwise.
- **quality: improved.** Instrument defects were disclosed and routed to new criteria rather than patched in
  frozen bytes (`corpus/QUALITY.md` +19 lines: 68–74 plus the 75/76 corrections, each citing its lesson and
  its evidence), the 26-pin container is enforced and I re-verified all 26 digests, the S105 row was restored
  after its accidental overwrite, and the admitted round-34 C1 entry gained an appended pointer narrowing its
  `sh_link` wording (append-only, no rewrite). No admitted entry is left false or unmarked. The D-3 provenance
  defect is new-entry hygiene, not a failed re-check; it does not reverse the trend but must not recur.
- **discernment: improved.** The round stopped on its own counterexample instead of banking a
  registry-relative CLEAN, and my outside spot-check **agrees on all four decisions** (three admits, one
  reject), so the LEARNING.md condition — agreement on admits *and* rejects — is met. Residual: the stop's own
  record needed two rounds of attack to reach its final form, and the final report still overstates its seat
  settlement (D-2).

## Routed defects — kaidoku must fix next round

- **D-1 (frontier census receipt).** `census-start.txt` is byte-identical to `census-end.txt`
  (`cmp` exit 0; both carry 9 `W04` lines), and it was committed by `66b84027` — the same commit that added
  S106. A genuine round-start census over the 105-row base blob prints the same 9 `W04` rows: re-running
  `sources-census.sh validate` against a fixture root holding `f432c8e3:corpus/SOURCES.md` gave the identical
  nine-warning set. The report's start row (`105 rows … 0 (8 × W04 duplicate-url warnings)`,
  `.ufo/reports/round-34/kaidoku.md:107`) therefore describes an artifact that does not exist and a warning
  count that cannot occur. Fix: capture the start census into its own file before the first registry edit and
  report the count observed.
- **D-2 (seat accounting).** The report's final accounting says `66 settled, 0 dead, 0 refused, 34/34 and
  32/32 reports on disk`. `w2-seat-map.json` has 32 entries but `ls .ufo/waves/round-34/r34b/w2/*.md | wc -l`
  = 31; the missing seat is `AAdjacencyCite`, whose prompt is committed and whose scratch directory
  `AWaveAccounting.md` records as empty and removed. Correct the count to 31/32 and record that seat as
  unreported, not settled — the same class QUALITY 76/M34-16 exists to capture.
- **D-3 (knowledge entry provenance trio).** `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`
  opens `author: / status: / sources: / revisions:` and carries no `source:` / `verified-at:` / `recheck:`
  line (`grep -c '^source:'` = 0, `^verified-at:` = 0, `^recheck:` = 0). CORPUS.md §Additional corpus rules
  requires the trio first, and it is the only one of the lane's last 17 entries without it — freshness sweeps
  read those fields. Fix with an appended block that states the trio against S106 and the receipt paths; do
  not rewrite the entry.
- **D-4 (instrument registry row fields).** The new SKILL.md registry section (and the two that precede it)
  uses `tool | purpose | command | exit codes | selftest`. PROTOCOL §Gate standard requires, per row,
  `gate|probe`, verdict map, self-test command and spelling, **pinned-value path**, **write scope** and
  **owner**. The round followed the lane's five-column habit and so extended a pre-existing lane-wide gap.
  The claim did not rest on the gate (it stopped), so this is status-neutral.
- **D-5 (protocol lane, not kaidoku).** The run-6 re-dispatch replaced the attempt-1 report's bytes at the
  contract path `.ufo/reports/round-34/kaidoku.md` (the 120-line `27322359` content is only recoverable from
  history); the replacement is labelled and cites the superseded commit, so it is not a silent rewrite, but
  the template gives a re-dispatched round no per-attempt report filename and no erratum convention. Route to
  the protocol lane: a `-attempt2` path or an appended erratum rule.

## SHONEN note for the operator (promotion stays operator-owned)

This session did **not** write any `[x]` and did not edit `SHONEN.md`. Reading the four boxes against the
evidence: box 1 (craft content with cited sources) now has a non-author verifier — the instrument registry
landed with a three-verdict table, an exit-code map and the S106 row, and I verified the registry and the
source; box 3 (executable without oral context) is checkable — five seats reproduced the receipts from fresh
clones and the counting commands are in SKILL.md, with D-4 the residual gap; box 4 (no cross-domain bleed) is
checkable — `PROVINCE.md` unchanged, kake's earlier `lookup_control_check.py` and the tsukuroi/mado/chousa/
kama/mori family cited, not absorbed. Box 2 (an end-to-end domain task logged) is **not** checkable from this
round: the round is instrument-only and the last end-to-end domain run is the historical libjq smoke.

## Limits of this spot-check

Gates and counters were not executed (PROTOCOL §Gate standard); every measurement above is over committed
bytes, committed receipts, or a live re-fetch of a cited URL. The decisive counterexample's 8/8 was read from
its committed receipt and bound to the gate's own counter by config and digest, not re-run here. The
`183/183` execve tally and the `REFUSED`-on-registration flip are evidence-verified from seat reports, not
re-executed. Paths under `/fast/scratch` were not opened; the receipts' scratch cwd is provenance only.
