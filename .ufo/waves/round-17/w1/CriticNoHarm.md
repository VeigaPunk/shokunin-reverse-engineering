# CriticNoHarm (round 17, w1): attack on "no axis harmed"

Author-side advisory critic. Read-only on the lane. I wrote only this file. Baseline is `b563c799`, and `git status` shows only `.ufo/waves/round-17/` untracked.

Method (OBSERVATION): I ran the real citation-drift probe with `--strict` at the baseline. I then ran it against single-edit simulations: a temp `git clone --shared` at `b563c79`, one edit committed, probe run, clone deleted. Census G21 was replayed in memory from `.ufo/gates/c1-census-v10.py:292-313,427-470` on `git show b563c79:PROVINCE.md`. No import was used, so no pycache was written. Scratch `/tmp/cnh-*` was removed. No installs.

## Baseline (OBSERVATION)
- Command: `python3 -I -B <abs>/citation-drift-probe.py --root <abs> --rev b563c79… --table <abs> --expected <abs> --strict`.
  - Result: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.
  - The table sha256 is `7994eec7…789d1`, which equals the `expected.json` `pointer_table.sha256`.
- Census G21 `frontier_check` on baseline PROVINCE returns `[]`.

## Findings: what this round can break

| # | Counterexample (edit L1 might make) | Evidence | Breaks | Smallest safe correction |
|---|---|---|---|---|
| F1 | Add a round-17 row to the README Lessons table (155-168), or any new line in README 1-180 | Sim: strict exit 1, 4× `citation_dead`: `sc69-readme-177` (SCORECARD.md:69→README:180), `readme175-sc1217/-r7range/-r8e2`. Precedent: commit `6a35398` "restore pinned line numbers (README lessons row removed…; 5 citation_dead)". | calibration (pinned citations die). Append-only SCORECARD cites can't be repaired. | Use only the in-place token on `corpus/README.md:35` (sim: clean) plus an optional bullet after :181. This matches `w1/draft-readme.md` Edit 1/2. Never add a Lessons/Knowledge row. |
| F2 | Put QUALITY #19 anywhere other than directly after row 18 | Rows 1-18 = `corpus/QUALITY.md:11-28`, blank :29. Sim "insert before row 11": exit 1, `r7wall-recheck-quality25` (pe-wall.md:7→QUALITY:25) + `arc3r1-entry-quality-11` (→QUALITY:21). Sim "after :28": clean. | calibration | Insert at new line 29 only (`w1/draft-quality-19.md:5` is correct). |
| F2b | Stale anchor in drafts: "rows end at 18 (`corpus/QUALITY.md:26`)" | `w1/draft-lesson-gate.md:17`, `w1/DraftLessonGate.md:28`. `QUALITY.md:26` is row **16**; row 18 is `:28`. | calibration (false citation if copied into the r17 lesson) | Cite `corpus/QUALITY.md:28`. |
| F3 | Any line added or removed in SKILL.md above :254 (e.g. a new craft rule, or a multi-line registry row edit above it) | `skill-rule14-*` entries pin citing lines `SKILL.md:246,248,252,254`. Sim "+1 line at 241": exit 1, 4× `citation_dead`. `SHONEN.md:6` range `SKILL.md:81-314` must still contain the rule at :233. | calibration | All SKILL edits must sit at :448 (in place, one physical line) or after :507. Sim of "row 448 rewritten in place + new registry row after :450": clean. `w1/draft-skill-section.md:4-5` matches. |
| F4 | Rewrite the citation-drift row and drop the phrase "frozen-run preflight" | Anchor entry `skill-registry-citation-drift-row`. Sim: exit 1, `no line matches 'frozen-run preflight'`. Sibling anchors: `interactive-r1-recovery \| gate / kaidoku`, custody-pair precedence regex. | calibration | Keep all three anchor strings. The draft row at `draft-skill-section.md:13` keeps the phrase, is one line, and has 7 cells (same as :448) (OBSERVATION). |
| F5 | Add any line to PROVINCE.md above :163 (e.g. a Go Core row in table 42-62, or a Go frontier bullet) | Census G21 hard-codes bullet spans `PROVINCE.md:75-162` (`c1-census-v10.py:292-308`; "any frontier edit re-keys the register"). Replay "+1 line at 53": `REQUIRED 'oldest-first' absent`, `:83 unregistered bullet`, etc. A Go bullet appended at :163: `unregistered bullet (FRONTIER-UNEVALUABLE)`. Citation-drift: +1 line at 53 is clean; +3 lines push :114 past `SHONEN.md:12`'s `PROVINCE.md:88-116` (`shonen-province-range` dead); +1 above :18 kills `prov18-*`. | operability/calibration (census gate fails; SHONEN pointer dies) | Make the PROVINCE amendment in place on `:52` only (the site `w1/ReviewProvinceGo.md` names), with line count unchanged. Otherwise re-key G21 in the same commit. |
| F6 | **Already happened:** a round-17 seat wrote into the frozen round-16 dir | `.ufo/waves/round-16/__pycache__/selection.cpython-314.pyc`, mtime `2026-10-20 10:32:31 -0300` (after `claims.json` `declared_at` 10:25). `git status --ignored` shows `!! .ufo/waves/round-16/__pycache__/`. Repro in a tmp dir: `spec_from_file_location`+`exec_module` under `python3 -I` writes `__pycache__`. `PYTHONDONTWRITEBYTECODE=1` is **ignored** under `-I`; only `-B` suppresses it (Python 3.14.8). | identity/provenance: violates `contract.md:7` "Never write outside the paths a CLI is given". It is invisible to blob-based controls (`round-16/controls.py:6-7` "evidence_class git_object_bytes"), and `.gitignore` hides it. | Set `sys.dont_write_bytecode = True` in `predict.py`/`retain.py`/`carrier-run.py` before importing, or run with `python3 -I -B`. L1 should record the stray `__pycache__` as a round-17 write, then remove it. Add an untracked/ignored control (C5). |
| F7 | Sweep N→0 declared from a regex/file set that misses sites (premature saturation) | `contract.md:91-93` regex misses `LOG.md:2012` "Producer/fixture hashes remain unchanged across execution." File set omits `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` "Producer and fixture pins were unchanged during the run". Matched sites: `corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`. Also, one line holding `R16-PROVENANCE` + every path marks all sites corrected (`contract.md:94-95`). | calibration | Widen the regex (`across\|throughout\|during`) and add the r16 knowledge file. Require one correction line per site that cites `path:line`. Corrections are append-only (knowledge prefix and LOG prefix preserved). Never touch `verification.json` (frozen r16 dir). |
| F8 | Reopen S003/S023 by editing their cells in place | `round-16/controls.py:216-243` flags every cell except `used-by` (index 11) as `immutable_violations`. Header `corpus/SOURCES.md:5`. | calibration | When reopening, change only `used-by`, plus new rows S024+ (`draft-sources-rows.md:37` already says S003/S007 are cited as existing anchors only). |
| F9 | Generalized controls copy r16's narrow scope | `round-16/controls.py:32` `APPEND_ONLY=["LOG.md"]` (SCORECARD has no prefix check). `:35-39` frozen prefixes omit `.ufo/waves/round-16/`, `.ufo/gates/` (sha-pinned `pointer-table.json`/`expected.json`, census), `.ufo/rounds/`. | discernment of the control itself | See C3. |
| F10 | Registry M→0 regressed by the round's own new rows | `invocation-audit` classes any row lacking a matching receipt and the word `unexercised` as `unlabelled_variant` (`contract.md:85-88`). Draft adds 7 rows, all labelled "unexercised" (`DraftSkillSection.md:50`). If L1 later edits a label to the argv without a receipt, M grows again. | calibration | Run the audit at AFTER over **all** rows, including new ones. Remove a label only with a retained receipt argv. |

Log identity (cross-reference, not new): the "new `/tmp/rea-ghidra-*` dir" heuristic is not identity. Binding exists in the log at `pilot/shfmt-log/ghidra.log:82` (`target-58f765638eed.bin`) and `pilot/esbuild-0.25.12-log/ghidra.log:46` (`target-bab29b2ca7a9.bin`), both sha256 prefixes. See `w1/SentinelPollRace.md:17-36`. The receipt should assert `target-<sha256[:12]>.bin`.

## Bounded no-finding (searched, no harm path found)
- `.ufo/waves/round-14/fixtures/expected.json` pins only fixture-local manifests and HTML, not lane docs. `.ufo/rounds/interactive-r1/expected.json` pins only `/usr/lib/libjq.so.1.0.4`. Round 17 does not touch either.
- I grepped SOURCES/PROVINCE/README/SHONEN/QUALITY/SKILL, the r16/r15 lessons, `2026-10-20-*` knowledge and `.ufo/gates`. There is no live line-pin into `SKILL.md:255-507` or into `corpus/SOURCES.md` (the only hits are exempt doc text in `pointer-table.json`). `SKILL.md:278` cites `QUALITY.md:21`, which is stable under F2's placement.
- Sim: appending at SCORECARD.md EOF is clean (SCORECARD pins are :59-1435, all well before EOF :2348). LOG append at EOF is the drafted placement (`draft-log-entry.md:7`).

## Controls L1 must run (BEFORE=`b563c79`, AFTER=landing commit)
- **C1 Citation-drift.** Use the strict isolated absolute argv above at both BEFORE and AFTER. Expect `findings=0 exit=0`. Default (non-strict) probe mode exits 0 even when drift is found (`SKILL.md:448` "drift is reported, never failed"), so in that mode exit 0 is not a clean signal. This is wrong as written in `w1/DraftReadmeRow.md:21` and `w1/draft-readme.md` step 2 (no `--strict`, relative path). Also check that the `pointer-table.json` sha256 is unchanged.
- **C2 Line-shape invariants at AFTER** (git objects):
  - `SKILL.md:1-447` byte-identical, and the craft sha256 equals BEFORE (`round-16/controls.py:103-133`).
  - `corpus/README.md:1-181`: same line count, and only `:35` differs.
  - `corpus/QUALITY.md:1-28` identical, row 19 at `:29`, Signals table identical.
  - `PROVINCE.md:1-162` line count unchanged.
  - `SHONEN.md` byte-identical.
- **C3 Generalized `controls.py`:**
  - Append-only prefix for `LOG.md` **and** `SCORECARD.md`.
  - Prefix check over every old `corpus/lessons`/`corpus/knowledge` `.md`.
  - Prior `*-verifier-spotcheck.md` byte-identical.
  - Frozen blobs under `.ufo/waves/round-14/`, `round-15/`, **`round-16/`**, **`.ufo/gates/`**, **`.ufo/rounds/`** and `evidence/round-1-2026-10-15/`.
  - SOURCES: no change to any cell other than `used-by` in S001-S023.
  - QUALITY rows 1-18 unchanged.
  - Retain argv/orig_argv and the resolved revisions.
- **C4 Census G21.** Run `frontier_check` on AFTER PROVINCE and expect `[]`. Replicating it is enough if L1 avoids running the full census, which reads operator client configs.
- **C5 Out-of-tree write control.** Take `git status --porcelain --ignored` and a recursive listing of `.ufo/waves/round-1[4-6]` before and after every tool run. Expect no new entries outside `.ufo/waves/round-17/`. F6's pycache already exists and must be recorded.
- **C6 Audits at AFTER.** Run `invocation-audit.py` and `temporal-sweep.py` with the F7 scope fix. Report per-site `path:line` corrections, not just the count.
- **C7 Regression.** Run `quote-fidelity.py --frozen .ufo/waves/round-14/fixtures/expected.json` once at AFTER (r16 recorded frozen 7+2). Expect unchanged.

Impacted axes: **calibration** (F1-F5, F7, F8, F10), **depth provenance** (F6, plus the log binding). No axis harm is established yet. All harms above are conditional on landing choices, except F6, which is observed.
