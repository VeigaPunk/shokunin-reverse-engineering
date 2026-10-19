# RV-8 consumer inventory — citation-drift probe (arc3-loop1-round1, c2 reviewer)

Sweep method: `git ls-files | xargs grep -l citation-drift` (tracked-file census),
plus directory walks over `.ufo/`, and content greps for the probe filename,
`CITATION_DRIFT_*` tokens, and `--table` invocation shapes. HEAD at sweep:
`e845c2b524ad2e59871e004c51a1386e192a74ab`.

## A. Live consumers (non-record)

| # | Site | Shape | Evidence |
|---|---|---|---|
| 1 | `SKILL.md:371` — registry row (canonical recipe) | `--root . --rev <REV> --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json`; `--selftest`; `--strict` semantics declared | `SKILL.md:371` |
| 2 | Scripts | **none invoke the probe.** Only tracked `*.sh` is `.ufo/waves/luna-round-5/receipts/census-pre.sh` (probe-free: contains no `citation-drift` token) | `git ls-files '*.sh'` → 1 file; grep → 0 |
| 3 | Hooks / CI / Makefile | none exist (no `.github/`, no hooks beyond samples, no Makefile) | repo root `ls -a`; `.git/hooks` empty of non-samples |
| 4 | Sibling gate `.ufo/gates/c1-census-v10.py` | probe-free (`grep -c citation-drift` → 0); no coupling | command output |
| 5 | `corpus/`, `PROVINCE.md`, `README.md`, `MINT.md`, `SHONEN.md`, `AGENTS.md`, `EXAMPLE.kama.md`, `.ufo/continuation`, `.ufo/rounds`, `.ufo/interactive-sessions` | 0 references | tracked-file census: matches only in `LOG.md` (1), `SCORECARD.md` (1), `SKILL.md` (1), `.ufo/` (220) |

Records only (no runnable commands, no parsers): `SCORECARD.md` narrative rows
(:815, :853, :873-874, :907, :918-919, :925-926 the frozen-run debt, :990,
:1054, :1267, :1297-1303) and `LOG.md:1079,1134-1135`.

## B. Historical consumer shapes (wave recipes r5–r10) — the operating patterns

1. **Default recipe** (committed table + committed expected), probe + `--strict`
   + `--selftest`: r9 V1:13, r10 C1:61-67, C2:59-65, V1:190-196, V2:64-71,
   V3:67-78, V4:96-103, RV-6 `J-selftest.out` this round.
2. **Custom `--table` + committed `--expected`** (draft/extension/experiment
   tables, verdicts 0/1 expected):
   - r10 E16:117-119 `--table table-E8.json --expected .ufo/gates/citation-drift/expected.json --strict` → `clean findings=0 exit=0`
   - r10 CR2:91 `--table /var/tmp/.../t-faithful.json --expected …/expected.json --strict`
   - r10 C4:153-159 `--table /var/tmp/arc2-l10r10-C4/pointer-table-extended.json` → `reported findings=0 exit=0` / `findings=19` at frozen rev
   - r10 E22:144-150 `--table /var/tmp/arc2-l10r10-E22/c2-candidate-table.json --strict` → clean/failed 0/1 verdicts
3. **Committed table at the frozen rev `679af5d…`** (frozen-run leg): r10 P3:51-54,
   V1:194-196, C2:139-149; RV-8 re-run this round → `reported findings=16 exit=0`
   (table has grown since r10's 6; count is table-version-dependent).
4. **Parse patterns in use:**
   - `tail -1` for the verdict line (S1 r10:61, CR2 r10:44, RV-6 harness `last=$(… | tail -1)`)
   - `grep -c "^CITATION_DRIFT:"` for finding count (RV-6 harness)
   - verbatim verdict-line equality in one scratch harness (E58 r6:329 `ln.startswith("CITATION_DRIFT_VERDICT:")`, :591 exact-string compare) — historical, not live
5. **TMPDIR redirection for `--selftest`** (quota avoidance): r9 V1:13
   `TMPDIR=/var/tmp/arc2-l9r9-V1-…`, r10 V4:101, RV-6 `J`; RV-8 T3 first attempt
   hit `/tmp` quota (`Disk quota exceeded`, git init rc 128) and passed under
   `TMPDIR=/var/tmp/rv8/tmp` → 11/11.

## C. Flag surface (compatibility contract)

Probe argparse (`citation-drift-probe.py:443-453`):
`--root --rev --table --expected --snapshot-dir --selftest --strict`.
Every consumer invocation above uses only these; no consumer passes a
nonexistent flag. No consumer passes `--snapshot-dir` (committed table has no
`@` targets: `grep '"@' pointer-table.json` → 0 hits).

## D. Output surface (parse contract)

- `CITATION_DRIFT_ROOT|REVISION|TABLE:` header lines (`:300-302`), finding lines
  `CITATION_DRIFT: <id> entry=<eid> <detail>` (`:304`), verdict **last**:
  `CITATION_DRIFT_VERDICT: <label> findings=N exit=M` (`:308-309`), labels
  `reported|clean` / `failed` / `could-not-evaluate` (`:306-307`).
- Selftest: `SELFTEST_CASE:` rows + final
  `CITATION_DRIFT_SELFTEST: <CLEAN|FAILED> cases=N passed=N failed=N exit=…`
  (`:427-438`).
- Exit map: 0 clean/reported, 1 failed (strict), 2 could-not-evaluate.

## E. Guard compatibility constraints (for the C2 frozen-run guard)

1. Keep all 7 flags accepted; do not require a new mandatory flag for the
   measured consumer shapes.
2. Verdict line stays the last stdout line, same format; existing labels and
   exit codes for existing cases unchanged; the new tampered-table class must
   surface as exit 2 with a verdict line (declared CNE class), never as
   `reported findings=0 exit=0`.
3. **The load-bearing risk:** a guard that pins the digest of *any* table path
   passed via `--table` against the committed `expected.json` converts the
   established r10 shape B (custom table + committed expected) into exit 2.
   Scoping the digest check to the committed table (the probe's sibling
   `pointer-table.json`, i.e. `DEFAULT_TABLE`/`HERE`) preserves shape B and
   still closes the silent-green class on the committed artifact (fixtures can
   tamper the table at the default path inside an isolated tree copy, where
   `HERE` resolves to the fixture).
4. Selftest: the 11 existing case ids/exit codes unchanged; the two new cases
   appended (13 total per the claim); must stay green under redirected TMPDIR.
5. The registry row patch (`SKILL.md:371`) must state the guard semantics and
   11 → 13 cases. It is safe to edit: `skill-registry-row`
   (`pointer-table.json:107-112`) is an unpinned anchor on the *sibling* row
   (`interactive-r1-recovery | gate / kaidoku`), not on the citation-drift row
   text.
