# R36ReviewerQualityBar — QUALITY.md criteria audit of the round-36 instruments and the C1 entry

Seat: R36ReviewerQualityBar (reviewer, wave 1, leaf — no subagents). Date: 2026-10-26.
Scope: `corpus/QUALITY.md` read in full; every criterion that binds the frozen round-36 instruments
(`tools/round-36/c1-counter.py`, `c2-counter.py`, `c1-run.sh`, selftest fixtures), the frozen
carriers/oracle/receipts (`corpus/evidence/round-36/c1/`), the controls
(`.ufo/waves/round-36/controls/`), and the planned/landed C1 entry
(`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`) is listed below with
met / not met / not applicable and file:line evidence.

## Observation revisions (the tip moved during this review)

- Freeze `790561d4` (2026-10-26T01:21:38-03:00) — claims, counters, carriers, oracle, before receipts.
- Control receipts `6a870b92` (01:22:29); C1 after receipts `3310d8fa` (01:22:59); C2 landing
  `d2e46ef5` (01:27:16); C1+assimilation landing `ffc81341` (01:47:30); lesson/LOG/report landing
  `01a44dbf` (01:50:56). Base `cab59f22`.
- Instrument structure was reviewed at `d2e46ef5` state; counters re-scored at `ffc81341`;
  instrument digests verified unchanged `790561d4..01a44dbf`:
  c1-counter `5533e17d…81b5`, c2-counter `f079aff1…078f` (identical at freeze and tip;
  `git diff 790561d4 ffc81341 -- tools/round-36/` is empty). Working-tree digests at review time:
  c1-run.sh `16907dca…f4d4`, plans/round-36-claims.md `2c9cbde7…d6c0`.

## Method

- No `lsp` device is mounted in this session's tool inventory; all caller/definition/diagnostic
  checks were done by file reads and read-only git (`show`, `log`, `diff`, `cat-file`). Recorded
  here per the reviewer contract; no grep output is offered as semantic proof.
- Only lane writes: this report. No VCS mutation; fixture git repos (selftests) run in scratch.
- Tooling authorization (operator 2026-10-19): **no tools installed or upgraded**; used preinstalled
  python3, git, jq, curl, sha256sum only.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ReviewerQualityBar` used for counter runs and the
  K3/K4 download check; **removed before finishing** (verified absent). All cited bytes are
  committed in the lane or quoted below.

## Independent verification runs (exact commands, results)

| check | command (abridged) | result |
|---|---|---|
| C1 selftest | `python3 -I -B tools/round-36/c1-counter.py --selftest --pkg65 ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | `{"cases":14,"green_ok":1,"red_ok":13,"failures":[]}`, exit 0 |
| C2 selftest | `python3 -I -B tools/round-36/c2-counter.py --selftest` | `{"cases":13,"green_ok":1,"red_ok":12,"failures":[]}`, exit 0 |
| C1 at mid-wave HEAD | `c1-counter.py --root . --rev HEAD --freeze 790561d4… --pkg65 …` (at `d2e46ef5`) | exit 1, `carriers_matched 4`, `carriers_unchanged true`, all lane bindings false (entry/Core row/registry rows unlanded) — honest mid-wave state |
| C1 at landing | same, `--rev ffc81341` | **exit 0, `met_target true`**: 4/4 carriers matched, S107–S109 opened 2026-10-26 used-by entry, PROVINCE Core row + coverage-map row present |
| C2 at landing and tip | `c2-counter.py --rev d2e46ef5 --base cab59f22`; `--rev ffc81341` | exit 0 both: `mismatches 0`, `guards_ok true` (36 pointers at tip; base 3 mismatches as frozen) |
| Per-carrier detail at `d2e46ef5` | json-out inspected | K1 3/3, K2 4/4, K3 2130/2130, K4 2130/2130 after-oracle hits; before gap `missing-extractor-dependency[sasquatch]` ×4, before hits 0 ×4; all 8 evidence ids recompute |
| Controls | `.ufo/waves/round-36/controls/*.out` | all 7 exit 1 (`met_target false`); ctl-c1-0 at base shows `carriers_unchanged false`, all bindings false; ctl-c2-0 shows the 3 frozen base mismatches (`116/116` vs `[122,122]`, `receipts-B/`, `ScoutSkillPlacement.md`) |
| Freeze gate | `python3 -I -B tools/round-31/freeze-integrity.py --root . --round 36 --rev ffc81341` | exit 2: `ERROR no commit adds .ufo/waves/round-36/claims.json` (round-35 sanity run: exit 0 CLEAN — gate works) |
| Timestamps | `python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root . --rev HEAD --path corpus/evidence/round-36 --strict` | exit 0, `findings: []`, 30 text blobs scanned, 5 binary skips each named |
| Carrier identity K3/K4 | downloaded both release assets from `https://github.com/neovim/neovim/releases/download/v0.12.6/…` into scratch, `sha256sum` | `b644d034…f29fb` and `8efcec73…e1c2` — **equal to carriers.json** (GitHub API returned 403 from this host; asset download used instead) |
| Oracle independence K1 | `sha256sum corpus/evidence/round-36/c1/fixtures/k1-src/*` vs `K1/oracle.tsv` | digest-identical (README.txt `88dc952a…`, etc/config.ini `bf53724a…`, payload.bin `5b61b326…`) |
| Entry arithmetic | `wc -l` / `cut -f2 … sort -u` / `awk -F'\t'` on oracle.tsv | K1 3 rows sum 70086 B; K2 4 rows sum 273971 B; K3 2130 rows, 2116 distinct digests — all equal the entry's stated numbers |
| Fixtures vs carriers.json | `sha256sum corpus/evidence/round-36/c1/fixtures/*.sqsh` | equal to the frozen digests |
| Instruments vs freeze | `git show 790561d4:tools/round-36/c1-counter.py \| sha256sum` (and c2), `git diff 790561d4 ffc81341 -- tools/round-36/` | unchanged; empty diff |

## Criterion-by-criterion verdicts

### Admission criteria (QUALITY.md `## Admission criteria`, rows 1–78)

| # | criterion (short) | verdict | evidence |
|---|---|---|---|
| 1 | resolvable source | **met** | entry `source:` lines cite S107–S109; rows committed `corpus/SOURCES.md:113-115` with URLs; K3/K4 bytes re-fetched by me and digest-equal |
| 2 | falsifiable | **met** | `plans/round-36-claims.md:22-27` (P36-C1), `:67` (P36-C2); counters are executable falsifiers; controls + selftests frozen |
| 3 | domain-specific | **met** | sasquatch/unblob/squashfs-specific throughout; no generic agent advice |
| 4 | artifact named by path + stable identity | **met** | `carriers.json` sha256 ×4; `K*-run.json` carrier abs path + sha256; oracle-run.json records offset + unsquashfs version |
| 5 | observation/inference/unknown separation | **met** | entry sections "Oracle method and its limits" and "What this is not claimed to show"; envelope `limitations` retained (`K1/after.json` key `limitations`) |
| 6 | REA claims cite Evidence ID / reproducing call | **met** | entry Receipts table lists all 8 `ev_` ids; counter recomputes stored ids via the xpin bytes pinned at the freeze commit (`c1-counter.py:60-84,182`) |
| 7 | names what was NOT examined | **met** | entry limits: regular files only, LE v4 only, no BE/AVM, no 7z fallback, nothing executed, K4 runtime not run (no qemu) |
| 8 | capability claims pin tool/provider versions | **met** | `rea-agents@6.5.0` (`c1-run.sh:16,81` + run records), unblob 26.6.4 (envelope `provider.version`), unsquashfs 4.7.5 (`K*/oracle-run.json`), sasquatch 4.5.1 path+sha256+version (`K*/after-run.json`) |
| 9 | runtime-behavior provenance | **n/a** | no execution claims; entry: "Nothing was executed" |
| 10 | held only for verbs run on carriers this round | **met** | extract-firmware run on 2 synthetic + 2 shipped carriers this round; PROVINCE Core row `PROVINCE.md:372` grounded in exactly those receipts |
| 11 | zero findings: parsed-and-empty vs excluded | **met** | entry states K1/K2 `before` publish `files: []` with the input chunk `extraction_failed: true` — shape stated, not silence |
| 12 | synthesized carriers: exact bytes or recipe | **met** | K1/K2 committed byte-exact (`fixtures/k1-le-xz.sqsh` 93802938…, `k2-le-gzip.sqsh` ce5bf60e…) plus committed source trees; byte-exactness claimed only against the pinned digests |
| 13 | occurrence counts `grep -o \| wc -l` | **met** | C2 command A uses `re.findall` (`c2-counter.py:110-130`); no `grep -c` counting in any instrument; tallies use `grep -o \| wc -l` (`w1/R36ConnAssimilationTheme.md:229`) |
| 14/15/37/41 | evidence-id identity domain | **met (in scope)** | no universal-formula or cross-path identity claim made; ids compared only stored-vs-recomputed at one freeze, one provider build (`c1-counter.py:182`) |
| 16/17/42 | Gate quote fidelity (contiguous, ≤25 words, located) | **met** | `corpus/lessons/round-36.md` Gate: S107 9-word quote, S108 lines 58-62 argv fragment (code checked manually per #1, not submitted as machine-gradeable), S109 3 words, S110 line 49, S111 line 12; each with locator; no quote-fidelity manifest required (none submitted as machine-checked) |
| 18 | execution evidence: argv, revision, stdout/stderr, exit | **partial** | `K*-run.json` retains mode/carrier/sha/utc/exit/stderr-head + producer pins (`c1-run.sh:87`); producing command is committed harness line `c1-run.sh:81`; counter receipts record argv + revision. **Gap:** run records carry no lane revision field |
| 19 | temporal-stability form | **n/a** | no across-run stability claim; the identical `continuation_id` across four receipts is stated as an observed per-receipt fact, receipts retained |
| 20 | provider-log observation binding | **n/a** | no provider-log claims; `stderr_head` retained (empty) |
| 21 | retention statement names recomputed keys | **met** | counter receipts carry argv + the fields the counter recomputed; controls' `.out` name only exit + verdict fields |
| 22 | seat-status statements | **pending** | round-record seat accounting lands at filing (row 76 duty); w1 reports + `swarm-registry.json` committed at `01a44dbf` |
| 23 | evidence timestamps ≤ committer time, `--strict` | **met (at reviewed revs)** | strict run exit 0 over `corpus/evidence/round-36` (30 files, 5 named binary skips); landing touched no evidence-tree file; zoneless `verified-at: 2026-10-26` in entry is unchecked — stated here as unchecked per the row |
| 24 | no-execution guard record | **n/a** | no no-execution contract claimed for C1 |
| 25/26 | held-verb id+operation in one supported record | **met** | counter requires `operation == extract_firmware` and `provider.id == unblob` inside each envelope (`c1-counter.py:173`); typed refusal/error envelopes cannot match the oracle-hit and gap conditions |
| 27 | null first-failure envelope | **n/a** | no first-failure claims |
| 28 | independent control not derived from validator's fixture builder | **met (note)** | red controls separately authored and committed before data (`ctl-*.json` at `6a870b92`, 01:22:29 < after data 01:22:59); positive-control envelope/oracle fixtures are frozen committed files (`tools/round-36/selftest/dev-*`), only the doc templates are in-code — acceptable as selftest, and receipt provenance is independently carried by `w1/R36ExecReproK{1..4}.md` |
| 29 | counter verifies source linkage (opened, mined, used-by) | **met** | `c1-counter.py:217-224` requires `status` row with `opened == 2026-10-26` and used-by naming the entry; red cases "source row opened earlier", "used-by lacks entry" (`c1-counter.py:310-325`). **Note:** no explicit red case for a cited row absent from the registry (covered only indirectly) |
| 30 | unavailable-client control scoping | **n/a** | no unavailable-client claims |
| 31 | CLI-held envelope preservation | **met** | original REA envelope JSON retained verbatim as `K*/{before,after}.json`; continuations quoted verbatim in the entry |
| 32 | revision-bound measurement, pinned helper, frozen inputs | **met (gap noted)** | counters read only git objects at `--rev`/`--freeze`; xpin helper bytes taken at the freeze commit (`c1-counter.py:62-64`); selftest fixtures frozen at the instrument commit. Gap: no run-start/commit-time refusal (see 38) |
| 33 | instruments committed before claims, pinned by sha256 (`instruments`), freeze ledger | **not met** | instruments and claims first appear in the **same** commit `790561d4`; `plans/round-36-claims.md` contains **zero** occurrences of `instruments` (`grep -c` = 0) and no `claim_row`; `corpus/claim-freezes.tsv` has no round-36 row yet. Lane precedent flags this exact shape: round-35 row in that ledger is `FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED` for first-committing counter and freeze file together |
| 34 | red receipt ≠ pass; original frozen result decides | **met** | all 7 controls recorded `exit 1` + `met_target false`; frozen instrument bytes unchanged through `01a44dbf` (diff empty), no revised-instrument substitution |
| 35/36 | reversals traceable both ways | **met** | lesson Gate records the AppImage-Spec rejection with flip condition; assimilation Decisions 2–4 REFUSE with flips; quarantine slice re-checked with dispositions |
| 38 | instrument + red fixtures + before receipt before data; instrument refuses pre-instrument data | **partial** | commit graph satisfies ordering: instrument/fixtures/oracle/before at `790561d4` (01:21:38) ≤ data `3310d8fa` (01:22:59); red fixtures ship in the instrument commit. **Not met clause:** neither counter refuses runs started, or evidence files first committed, before the instrument commit (no timestamp or commit-time checks in `c1-counter.py`); actual timestamps are consistent (before runs 04:17:49Z < freeze 04:21:38Z < after 04:22:42Z, commit 04:22:59Z) |
| 39 | per-call resolved package version + package.json sha256; instrument rejects mismatches; red fixtures before data | **not met** | run records carry only the requested pin string `rea-agents@6.5.0` (`c1-run.sh:87`); neither the resolved version nor the package's own `package.json` sha256 (`a5003023…a6c` on this host) is recorded anywhere; `c1-counter.py` reads no run record and no version/digest field; no red fixture demonstrates such a rejection. (Envelope `provider.version` covers unblob 26.6.4 only; the entry separately pins the engine `executable_sha256`.) |
| 40 | green look-alike case for duplicate/refused-evidence refusal | **n/a (residual risk noted)** | the counter has no duplicate-envelope predicate; roles (before/after) and carrier digests disambiguate. No green legitimate-duplicate case exists; risk is low but the class is unexercised |
| 43 | carriers screened with the tool's own input check before freeze | **met** | all four `before.json` envelopes frozen in `790561d4` show the tool parsed each carrier and emitted the typed `missing-extractor-dependency` gap (not `invalid_format`) — the screen output is the freeze content; counter confirms `before_sasquatch_gap true` ×4 |
| 44 | held-out rule-test declared before data | **n/a** | C1 is not presented as a held-out test; pre-freeze dev probes are disclosed in the claims file |
| 45 | claims file names `claim_row`; counter accepts only that row | **not met** | claims file names no row id (`grep claim_row` = 0; only prose descriptions at the "Sourced claim" bullet); `c1-counter.py:217-224` accepts **any** registry row opened 2026-10-26 whose used-by names the entry; the selftest green case uses an arbitrary `S107`, and the round-29-style red case "cites another valid new row" is absent from the 14 cases (`c1-counter.py:310-325`). No material harm at landing (S107–S109 cited consistently), but the frozen instrument does not enforce the specific rows |
| 46 | freeze audit covers every claims file, `--disclosures` at filing | **pending** | no `claims.json` for r36 and no ledger row yet; both freeze gates + `--disclosures` owed at prefile (#47) |
| 47 | prefile-check exit 0 immediately before report commit | **pending** | filing-time duty; M36-5 fix additionally gates filing on `ls-remote` final hash + per-wave WAVE-DONE |
| 48 | surface named + unmoved command; five control classes scored before data | **partial** | surface + unmoved command met (`plans/round-36-claims.md:26`; `ctl-c1-0-do-nothing.out` exit 1 at base, committed pre-data); controls scored before data with receipts committed first (`6a870b92` 01:22:29 < `3310d8fa` 01:22:59), all exit 1, kill rule not triggered. **Not met in full:** #48's five classes — C1 lacks a junk-row control and a no-reader (unevaluable/exit-2) control; C2 lacks a no-reader control |
| 49 | frozen inputs immutable or copy-per-seat; counter re-hashes each run | **met** | run records show per-seat copies (`carrier: /fast/scratch/hyaku/kaidoku-r36/L1/carriers/k1-le-xz.sqsh` in `K1/*-run.json`); the counter re-derives carriers/oracle from git objects at rev vs freeze on every run (`c1-counter.py:143-152`); fixture digests re-verified by me; no `chattr +i` (copy branch satisfied for the only carrier runner) |
| 50 | (supersedes 48's gate clause) controls reviewed from reports themselves | **met** | every control receipt re-run and inspected by this seat; each `.out` shows exit 1 with the expected failure field |
| 55 | frozen input checked at measured revision AND for any post-freeze touching commit | **partial** | carriers/oracle are compared rev-vs-freeze by the counter each run; **instrument digests are pinned nowhere** (no `instruments` map), and the lane's freeze-integrity gate cannot evaluate r36 at all (exit 2, no `claims.json`) — post-freeze instrument integrity is currently shown only by ad-hoc digests (this report: sha256 + empty diff `790561d4..01a44dbf`) |
| 56/57 | unmoved-command / novelty spelling sweep | **n/a** | no unmoved-command or "never run" novelty claim about a command surface; the moved surface is prose rows whose movement the counter itself enforces; old Frontier wording kept as dated history (`README.md:233`, `PROVINCE.md:156`) |
| 58 | calibration counter distinguishes faithful self-assessment from denial/word bags; both controls scored before data | **not met (applicable in part)** | C2 scored do-nothing / junk-count / delete-bad-pointers / substitute-other-document controls before data (base 3 mismatches shown), but **no explicit-denial and no vocabulary-only-bag control**; the counter reads wording only through pointer/count/range regexes, so a surface rewritten to vacuous text with resolving pointers and correct counts would meet P36-C2. Lane-disclosed: M36-3 (`corpus/lessons/round-36.md:17`), mitigated by wave-2 re-derivation of the C2 verdict by a stricter non-counter check |
| 59 | durations, not future execution timestamps | **met** | entry `recheck: 180d` (duration); no future instants; #23 strict green |
| 60 | literal scratch `find`/`du` restriction in every wave context | **not met** | `w1-spec.json` and `w1-dispatch.json` contain no `find`/`du` restriction (grep = 0; the only "find" hits are prose "first find the tag" / "find the cheapest input"); this seat's own context also lacked it. Lane self-caught as M36-6 (`corpus/lessons/round-36.md:20`, R33-N1 recurrence) with a wave-2 fix and red/green check |
| 61 | relied-upon gate self-invokes via outer CLI, asserts exit + stable findings on isolated fixtures | **met** | `c1-counter.py --selftest` 14/14 exit 0; `c2-counter.py --selftest` 13/13 exit 0 (both run by this seat); fixtures are isolated git repos with a toplevel assertion; exit semantics asserted per case (`c1-counter.py:354`, `c2-counter.py:324`). Note: cases call `measure()` in-process rather than re-invoking the counting CLI per case |
| 65 | unchanged-file assertion names base/tip + per-file result | **met** | `carriers_unchanged` / `oracle_frozen` are per-file byte comparisons against the freeze blobs (`c1-counter.py:143-152`), not tree summaries |
| 66 | freeze-integrity gate rejects absent/malformed instrument maps; map-free claim unevaluable, never CLEAN | **demonstrated gap** | `freeze-integrity.py --round 36` → exit 2 `no commit adds .ufo/waves/round-36/claims.json`: the r36 freeze is map-free and therefore **unevaluable** by the lane's own gate. The gate correctly refuses (no vacuous CLEAN), but the round cannot currently show instrument-pin integrity through any gate |
| 67 | structure-blind replay before freezing a structural-decoding counter | **n/a** | no ELF structural-decoding counter; M36-4 notes #67 covers readers, not receipts |
| 68 | predicate byte-identical across claim/config/counter/receipt; command re-hashes pins and reads predicate from claim file | **not met** | counters embed the predicate sentence only in docstrings (`c1-counter.py:4`, `c2-counter.py:4`, "same sentence in plans/round-36-claims.md") and echo id constants into receipts (`c1-counter.py:141`, `c2-counter.py:171`); **no code path reads `plans/round-36-claims.md`** (`show(root…claims)` absent from both); docstring-vs-claim byte identity is verified by no instrument; the claims file has no `instruments` container. Partially mitigated by commit-identity pinning (everything measured is read at the freeze commit) and by the new round-36 instrument registry in `SKILL.md:1258` |
| 69–72 | replay-class-set gates / mutant triples / receipt-reading gates | **n/a** | no replay-class gate in r36; no lane gate yet consumes the r36 counter receipts (`.ufo/waves/round-36/after/*.json` are recorded receipts, not gate inputs) |
| 73 | receipt states argv, reader digest, commit, UTC instant | **partial** | counter receipts: argv + measured commit ✓, reader digest ✗, UTC instant ✗; run records: UTC + producer pins ✓, revision ✗. No single record type carries all four fields |
| 74 | registry edit verified by row count + per-status/tier tallies; anchor re-read | **partial-met** | per-status tallies before/after recorded (`w1/R36ScribeSources.md:144`: `mined=102 rejected=4 → mined=105 rejected=4` for S107–S109); assimilation tracked `existing_rows: 105`, collision `S106`, renumber map (`w1/R36ConnAssimilationTheme.md:33,264`); census validate exit 0 on the mirror (`.ufo/waves/round-36/assimilation/validate-mirror.txt`). Tier tallies and the consolidated final tallies + end census are owed in the round report |
| 75 | axis label checked against measured bytes before freeze | **met** | C1 labelled coverage; moved surface is the PROVINCE/README catalog + coverage map; SCORECARD Owned axes tied 10/10/10 (`SCORECARD.md:19-25`), lowest-axis rule satisfied; no depth claim made (R33-2 reason stated in the lesson) |
| 76 | seat accounting in the stop commit | **pending** | filing-time duty; M36-5 fix binds filing order |
| 77 (new this round) | self-assessment counters enumerate every occurrence, keep duplicate units, bound base populations, repair against the intended document | **added; r36 C2 counter does not satisfy it** | `units()` keys by first cell so a duplicate row/box shadows the original (`c2-counter.py:59-90`); disclosed as M36-3, fix routed to the wave-2 re-derivation; binds future counters |
| 78 (new this round) | receipt integrity ≠ provenance; provenance from independent non-author re-run comparing semantic payload; receipt names the recompute package root | **added; satisfied for the C1 receipts** | `w1/R36ExecReproK{1..4}.md` reproduce the semantic payload; counter receipts name `--pkg65` in argv. The C1 counter's integrity check alone is formally insufficient (fabricated-and-rehashed envelope reaches `met_target`, M36-4/F1) — disclosed, frozen bytes left unedited |

### Signals of weak material (applied)

- Signal 4 (catalog-listed ≠ held): met — the gap and the fix are grounded in live typed envelopes on
  four run carriers, not in docs or `available:true` declarations.
- Signal 6 ("tool X missing" without the spawn wrapper): met — the missing dependency is unblob's own
  `get_dependencies()` report (S108), and the harness sets `REA_UNBLOB_COMMAND` to the real binary
  (`c1-run.sh:16,79`).
- Signal 2/3 (unscoped negatives, unbound artifacts): none found — negatives are method-scoped, all
  artifacts carry path+sha256.

## Findings by severity

**H1 — Freeze is map-free: instruments not pinned by sha256 in the claims file, and the freeze
gate cannot evaluate the round (#33, #55, #66, #68).**
`plans/round-36-claims.md` (sha256 `2c9cbde7…d6c0`) contains no `instruments` map and no `claim_row`;
counters + claims + carriers + oracle + before receipts first appear together in `790561d4` (not
"before"); `freeze-integrity.py --round 36` exits 2 (`no commit adds .ufo/waves/round-36/claims.json`);
neither counter reads the claims file or re-hashes instrument bytes. Materially: post-freeze
instrument integrity is shown today only by ad-hoc digests (this report). Mitigations in place:
content-level pinning of carriers/oracle at every measure, empty instrument diff through `01a44dbf`,
`SKILL.md:1258` instrument registry. Disposition options before filing: append a disclosed
`instrument_supersessions`-style entry + `corpus/claim-freezes.tsv` row naming the same-commit
custody defect (round-35 precedent is a `FLAGGED` row), and/or add the instruments container in a
disclosed commit with a re-taken before record.

**M1 — #45: no `claim_row` pin; the counter accepts any qualifying new source row.**
`c1-counter.py:217-224` + selftest green on arbitrary `S107`; no "cites another valid new row" red
case. Landing used S107–S109 consistently, so no material harm; the frozen instrument nevertheless
under-constrains the predicate it claims to enforce.

**M2 — #39: REA call records lack the resolved package version and the package.json sha256; the
counter has no rejection path and no red fixtures.**
`c1-run.sh:87` records the requested pin string only; `c1-counter.py` reads no run record. Row 78's
"receipt names the package root the recompute used" is met for the counter's own receipts (argv
`--pkg65`) but not for the REA call records.

**M3 — #48: control classes incomplete.** C1 lacks junk-row and no-reader (exit-2) controls; C2
lacks a no-reader control. Kill-rule safety unaffected (all seven committed controls exit 1, scored
before data).

**M4 — #58/#77: calibration counter blind spots (lane-disclosed).** No denial/word-bag controls;
dict-key shadowing (`c2-counter.py:59-90`). Disposition already recorded: QUALITY 77 added; C2
verdict to be re-derived by a stricter non-counter check in wave 2 and not cited alone until then
(`corpus/lessons/round-36.md:17`).

**M5 — #60: wave contexts missing the literal `find`/`du` restriction** (spec, dispatch, and this
seat's context). Self-caught as M36-6 with a wave-2 fix; the wave-2 context must carry the sentence
and the red/green grep.

**L1 — #38 refusal clause unimplemented** (no pre-instrument run/commit-time rejection in the
counter); actual timestamps are consistent, so no data harm.
**L2 — #73: field split** — no single receipt type carries argv+reader digest+commit+UTC.
**L3 — #40:** no green legitimate-duplicate look-alike case (no duplicate-refusal predicate; low
residual risk).
**L4 — #29:** no explicit red case for a cited row absent from the registry (covered indirectly).
**L5 — #74:** tier tallies and consolidated final tallies + end census owed in the round report.

## Residual risk and verification gaps

- K4's aarch64 AppImage runtime could not be executed on this host (no qemu) — the oracle for K4 is
  `unsquashfs` 4.7.5 alone, same code family as sasquatch 4.5.1; the entry states this limit and K3
  is corroborated by the runtime's own `--appimage-extract` (lane-disclosed).
- GitHub API returned 403 from this host during review; K3/K4 identity was verified by downloading
  both release assets and hashing (equal to the frozen digests) — equality to the *published digest
  fields* shown on the release page rests on S109/the scout receipts, not on my API read.
- The tip moved twice during this review (`ffc81341`, `01a44dbf`); counters were re-scored at
  `ffc81341` (both `met_target true`) and instrument bytes verified unchanged through `01a44dbf`,
  but the final prefile duties (#23 re-run at final rev, #46 `--disclosures`, #47 prefile exit 0,
  row-76 seat accounting, end census) remain open at filing time by design.
- QUALITY rows 77–78 were added by this round's own lesson; they bind the wave-2 re-derivation and
  future counters. This audit scored the r36 instruments against the rows that existed at the
  freeze, with the two disclosed deviations (M36-3, M36-4) noted where the lane itself routed them.

Scratch removed. No tools installed or upgraded. No VCS mutation; no lane writes except this report.
