# Round 79 — the gate's selftest detectors close, and the record's pointers bind at their lines

Base: `29d2ca30b83a6a0d85b0aa979de0138fde1660e6`.
Declaration: `a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d`.
Freeze: `ed68cd0a6cc790cca342380a2d80d1927a668c8c`.
Contract: `plans/round-79-claims.md` and `.ufo/waves/round-79/claims.json`.
Axes: calibration (R79-C1, the round-78 mutation survivors close under one declared case each)
and freshness (R79-C2, five record pointers bound at the line or range they name).

## Gate

Every source below was opened this round with one GET each; snapshots, byte counts and sha256s are
in `.ufo/waves/round-79/l1/sources/`. Quotes are literal contiguous excerpts with their snapshot
line. Two URLs were opened, two rows admitted; no source was refused this round (the duplicate
check ran before the append: neither host appears in `SOURCES.md`).

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S295, POSIX.1-2024 `grep`, admit (mined) | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/grep.html | 2026-11-04 (HTTP 200, 21 316 B, sha256 `9473205c…`) | "Precede each output line by its relative line number in the file, each file starting at line 1." (18 words; OPTIONS `-n`, snapshot line 97) | A `path:line` pointer names the file's own 1-based line, reset per file. Grounds `tools/round-79/pointer-bind.py`'s line rule: the binder reads the named line instead of searching the file for the token, so a moved line is a mismatch. |
| S296, cargo-mutants book, Welcome, admit (mined, tier B) | https://mutants.rs/ | 2026-11-04 (HTTP 200, 22 602 B, sha256 `d056b2b3…`) | "quality by finding places where bugs can be inserted without causing any tests to fail" (17 words; Welcome to cargo-mutants, snapshot lines 184-186) | Mutation-testing vocabulary: a surviving mutant is an inserted defect no test failure catches. Grounds the survivor rule in `tools/round-79/gate-mutation.py`; tier B because it is a tool's book, not the technique's specification. |

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` at round
start: exit 0, 200 rows, 23 W04 warnings (`l1/census-start.txt`). After the append, mid-round:
exit 0, the same 23 W04 warnings, no new warning class. The round-end receipt is `l1/census-end.txt`.

**Spot-check (non-author).** The round's outside discernment check is the closure session's
document, not this lane's: it should re-open S295 and S296, and the sample of evidence it should
re-derive is `pre/c1-at-base.json` (survivors 3), `l1/scores/c1-at-landing.json` (survivors 0),
`pre/c2-at-base.json` (mismatches 2) and `pre/controls/c2-path-only.json` (mismatches 0 on the
same stale record).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| **survivor — a detector that does not exist counted as a pass** (the round-78 wave's `m03` and `m08`). | Round-78 `w1/MutGate/mutation-receipt.json`: both mutants `killed false`, `detectors_failed []`; the gate's selftest had no case for an unparsable near-miss spelling (`NEAR_MISS_RE`'s `near is None` branch) and none for `validate_receipt`'s refused-without-a-reason guard. | QUALITY Row 138 (new) and the round-78 closure's routed mutation survivors. | `tools/round-79/gate-mutation.py` scores a mutant killed only when its DECLARED case is present and failing; an absent case is a survivor. Shown able to fail: at base the same battery reports `survivors 3` naming `m03`, `m05`, `m08` (`pre/c1-at-base.json`), and at the freeze `survivors 0` with each of the three a sole detector (`l1/scores/c1-at-landing.json`). |
| **reference-drift — a pointer compared by its path, never its line.** | `tools/round-78/surface-recheck.py:201-208` compares `pointer.split(":")[0]`; the OMP pin moved `:8` → `:12` and the Kimi pin `:4126` → `:4722`, and the round-78 recheck scored both green. | QUALITY Row 139 (new); the round-78 non-author spot-check §6 item 3. | `tools/round-79/pointer-bind.py` reads the pointed line/range and requires the declared token there; `PROVINCE.md`'s two pointers are rebound. Shown able to fail: `pre/c2-at-base.json` names both moved pointers, and `pre/controls/c2-path-only.json` reports `mismatches 0` on the same record. |
| **vacuous — a control that cannot fail used as a claim's rule.** | `pre/controls/c2-path-only.json`: the path-only comparison returns `mismatches 0` on the record whose two pointers are stale. | QUALITY Row 139; the §9 control rule. | The control is committed as the explicit reason it is not the counter: the claim's predicate names the line-bound rule and records the control's zero. The instrument's `--selftest` carries `red-stale-line`, `red-past-end`, `red-no-line`, `red-backwards` and `red-range-token-outside` beside their green look-alikes. |
| **reference-drift — an instrument's final selftest tally lived only in a seat's prose.** | `corpus/lessons/round-78-verifier-spotcheck.md` §6 item 4: the round-78 26-case tally was in `w1/MutGate.md` and the SKILL row, not in a machine receipt at the final revision. | QUALITY Row 92 (a counter is registered when it lands); the receipt clause. | `pre/selftest-gate.txt` is committed in the declaration and records `SELFTEST cases=29 failures=0` at the instrument revision the claims pin; the SKILL registry rows cite their own selftest runs. |

| **reference-drift — a printed counting command that was never run as printed.** | `plans/round-79-claims.md:85-86` and `.ufo/waves/round-79/claims.json` (`R79-C2.counting_command`, `predicate`) print `pointer-bind.py --root . --rev <measured> --json-out <receipt>`; the instrument required `--battery`, so the frozen sentence exited 2 (`w1/ReviewerC2/receipt.json`; `w1/SentinelScope/sentinel-receipt.json` F1). | QUALITY Row 118 (the round-76 executable printed counting command) and §2 item 4 (a command you can paste into the report). | The instrument now runs its battery whenever `--rev` is supplied, so the frozen text runs verbatim (`pointer-bind.py`, disclosed in `claims.json` `instrument_supersessions`); the mode flags, counter, target and kill rule are unchanged. The standing duty: run a plan's printed command through `tools/round-76/plan-command.py` before the freeze, not after the wave. |
| **vacuous — a seat prompt carried a malformed counting command.** | `gen-w1.py`'s ScribeSources item wrote `grep -oE 'S[0-9](3,)'` (POSIX ERE grouping, not an interval); the seat reported zero matches and corrected it to `S[0-9]{3,}` (`w1/ScribeSources/receipt.json` `next_ids`). | the source seat's own re-derivation (a prompt is not evidence until its command runs) and QUALITY Row 118's principle applied to prompts. | The corrected command and its output are in the seat receipt and cited in this round's Sources & frontier; the next wave's prompts are checked by running each embedded regex once before dispatch. |
| **ordering — a duplicate check read the registry after the append.** | `w1/ScribeSources/receipt.json` `duplicate_check` reports "refused reuse — both URLs are already held" at lines 212-213: the seat read the working tree after the L1 had already appended S295/S296, so its verdict describes the post-append state. | CORPUS.md rule 2 (append-only, no duplicate URL) plus the pre-append check's *order*. | The pre-append state is re-derived from committed bytes at the freeze rev (`.ufo/waves/round-79/l1/pre-append-url-check.txt`: 200 rows, neither host present); the seat's quotes and snapshots independently confirm both rows. |

## In-round repairs the wave forced

Disclosed in `.ufo/waves/round-79/claims.json` `instrument_supersessions`: the R79-C2 counting command now
runs as printed (battery is the default when `--rev` is supplied); a `--control` receipt records `would_pass`
and never `ok`; each pointer must also name the declared live object (round 78's `same_path` rule), with a red
self-pointer case; R79-C1's `ok` and `--validate` score the pristine `29 cases` conjunct and the three named
sole detectors (not every mutant: `m01`/`m06`/`m07` are legitimately multi-detector); both receipts carry the
producing instrument's digest, a timestamp and a 40-hex rev, and `--validate` re-derives them. Predicates,
counters, kill rules and targets are byte-unchanged.

## Wave evidence (drafts landed by the L1)

`r79-w1` evidence is committed under `.ufo/waves/round-79/w1/` (`r79-w1-results.json`: 12 seats,
12 non-empty outputs, 0 dead); the seat accounting and each
seat's material finding are in the round report's Wave paragraph. The independent re-derivations
that bound the claims: `ExecBaseArm` (second mutation implementation, 8 mutants, survivor set
identical), `ExecCaseInventory` (26 -> 29 cases, three added, each the sole failure of its mutant),
`ExecRebind` (second parser/binder, digests converge, base 2 mismatches, freeze 5/5),
`ReviewerC1` (17 forged receipts, all refused), `ReviewerC2` (sixteen attack shapes; the
counting-command defect above), `MutInstruments` (six instrument mutants; four `validate_receipt`
guards and the `battery()` cell survive, routed), `SentinelScope` (no secret-bearing field; path
and scratch findings F2-F8 routed), `ScribeSources` (both quotes exact and both snapshots
byte-identical), `ScribeLesson` and `ScoutRouted`/`ConnectorSibling` as filed.
