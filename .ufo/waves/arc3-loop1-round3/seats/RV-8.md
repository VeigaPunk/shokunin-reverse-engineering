# Seat RV-8 — chain c2 — reviewer — wave arc3-loop1-round3

Task as frozen: review EX-30's patch texts against the revised tool line by line
(every claimed class exists). Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`;
HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`; no seat commits; no write to any
real target by this seat.

Artefacts under review (EX-30's, re-emitted mid-review — both revisions checked):

- `claims/c2/EX-30/readme.patch.md` — reviewed `8941cbd9…`, re-reviewed
  `07bff2086d6f7ec0c110fdbd2acb24c0a35edadee1ccc764678400c253a660ed`
- `claims/c2/EX-30/registry-row.patch.md` — reviewed `9c5ff61a…`, re-reviewed
  `153cc48c7ab3d01f7c7f6487f54655020b228dfd194d0f0e232816f311ebb591`

Instrument revision the review pins:
`.ufo/gates/custody-pair/custody-pair.py` sha256
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`
(1155 lines; `selftest` `CLEAN cases=22 passed=22 failed=0 exit=0`) — the same
revision EX-30's re-emission names. Review transcript:
`claims/c2/RV-8/evidence/claims-run.txt` (sha `dd683225…`); before-state:
`claims/c2/RV-8/evidence/before-112d01dc/`.

## 1. Work performed (evidence pointers)

- **Before-state reproduced first-hand at r2 revision `112d01dc…`** (scratch
  `/var/tmp/rv8/inj/before-112d01dc`; copies in `evidence/before-112d01dc/`):
  blocked-dir path → receipt `EXISTS: no` + `STAT-ERROR`, capture exit 13, then
  `verify --live` **MATCH exit 0** (the fail-open); mode-000 file → capture
  `PermissionError` traceback exit 1; 1-of-5 receipt vs live → `MATCH 1/1 exit 0`;
  `--paths X --out X` → **clobbered**, exit 0; `selftest --scratch <missing>` →
  `FileNotFoundError` traceback exit 1; control selftest `CLEAN cases=15 exit 0`.
- **Line-by-line claim check of EX-30's pair against the revised tool** —
  `evidence/claims-run.txt` §C-1…§C-12. Each claimed class was located in the
  bytes (file:line) **and** fired by command. Result: 14/16 clauses verified,
  **2 refuted**, 1 wording nuance. Detail in `rv8-corrections.patch.md`
  (sha `34902a8b…`).
- **Identity re-derivation of the pair** (rule #14): extracted both fenced diffs,
  applied to their named bases (`SKILL.md` `c134afcb…` from the worktree;
  `README.md` `fa484d57…` from `git show HEAD:` — the worktree README has been
  superseded by EX-21, see §4 A3), and re-derived every digest: `registry-row.diff`
  8 lines `dbd79a6377…` → patched SKILL `62de392295…`/390 lines (line-neutral);
  `readme.diff` 114 lines `3a7e45dae8…` → patched README `a82d0071fe…`/180 lines.
  All match EX-30's tables exactly (script + transcript in
  `evidence/ex30-apply.sh`, run under `/var/tmp/rv8/ex30-apply-v2`).
- **Command A at HEAD** (verbatim SCORECARD.md recipe, git-object mode):
  `{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [],
  "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
  "rule_blocks": 14}` — `evidence/commandA-head-c07af80.txt`.
- Revision watch: 12 tool revisions snapshotted (`112d01dc, 7b848eaf, 460a01f0,
  d5e72049, 08fb6833, 57dffff1, 03bd6242, 89bfebec, 7cd19c3c, …`) under
  `/var/tmp/rv8/rev/`; the two gap findings persisted at `03bd6242`, `89bfebec`
  and `7cd19c3c`, so they are not revision churn.

### Claim-by-claim verdicts (EX-30 pair vs tool `7cd19c3c`)

| EX-30 clause | tool evidence | verdict |
|---|---|---|
| exit map gains `14 UNEVALUABLE`; precedence `CONTENT-DRIFT > UNEVALUABLE > ABSENT > …` | constants `EXIT_UNEVALUABLE` :161, `SEVERITY` :171, `EXIT_FOR` :180; transcript §C-1 | EXISTS |
| capture `0` at 5/5, `14` when ≥1 present-but-unevaluable, else `13` | `cmd_capture` :633-641; blocked-dir and mode-000 capture both exit 14 (§C-11) | EXISTS |
| verify classifies unevaluable before the both-absent branch; never a fail-open MATCH | `compare_section` :489; `VERDICT: UNEVALUABLE … exit=14` live and receipt-vs-receipt (§C-11; selftest cases 13/14/15) | EXISTS |
| `verify … [--require-paths <N>]` flag exists | parser :1137; `verify --help` (§C-2) | EXISTS |
| `REFERENCE-COVERAGE: n/N paths present in reference; unaccounted: <list>` + exit 2 | `reference_coverage` :591-599, call :677-687; 1-of-5 → exit 2 + the line (§C-4) | EXISTS |
| "applies to v1 and v2 references alike" | sums-v1 reference under the flag → exit 2 + line (§C-5) | EXISTS |
| "without it, coverage is reported but not enforced" | **0** `REFERENCE-COVERAGE` lines without the flag; `VERDICT: MATCH exit=0` (§C-3); the call site is inside the flag branch | **REFUTED (gap 1)** |
| guard covers `set(--paths) ∪ CUSTODY_PATHS` by resolved path and inode; `--paths X --out X` refused | guard :648-649; capture exit 2, scoped file byte-intact (§C-6) | EXISTS |
| hardlink alias refused (inode arm) | `_same_file` :214; exit 2, target intact (§C-7) | EXISTS |
| "refuses … to write a receipt **or sidecar** over any path it is measuring" | **sidecar path (`out.name + ".sha256"`, :657) is never guarded**; `--paths X.sha256 --out X` → exit 0 and the sidecar overwrites the measured file (§C-8) | **REFUTED (gap 2)** |
| `selftest --scratch` missing/unusable → declared USAGE exit 2, not a traceback | :726; exit 2 + `USAGE:` line, no traceback (§C-10) | EXISTS |
| selftest grows 15 → ≥17; row's exact landed count | `CLEAN cases=22 passed=22 failed=0 exit=0` (§C-9); the 7 closure cases exist by name in the bytes | EXISTS (22) |
| "recorded with `READ-ERROR`/`STAT-ERROR`, never silently as absent" | stat-blocked receipt: `EXISTS: no` **plus** `STAT-ERROR: …`; class 14, not silent (§C-12) | EXISTS with wording nuance (§ in corrections file) |

Claim-gap repairs are supplied as red/green text in
`claims/c2/RV-8/rv8-corrections.patch.md`: gap 1 — replace the clause or print
the coverage line unconditionally; gap 2 — drop "or sidecar" or extend the guard
to the sidecar path. Both have a measured, minimal form.

## 2. Proposed changes

- No write to any real target (reviewer seat; `SKILL.md` and the gate README are
  EX-21's/EX-30's surfaces, not mine).
- Correction text for EX-30's two clauses:
  `.ufo/waves/arc3-loop1-round3/claims/c2/RV-8/rv8-corrections.patch.md`.
- Nothing else proposed. The re-emitted pair is otherwise verified: its diffs
  apply cleanly to their named bases and reproduce every claimed digest.

## 3. Before → after measurement (chain c2 claim)

Reviewer-side, independent of EX-30's own §7 table:

| hole (r2 debt) | before, `112d01dc…` (this seat) | after, `7cd19c3c…` (this seat) |
|---|---|---|
| D2 EACCES (blocked parent dir) | capture exit 13 (`EXISTS: no` + `STAT-ERROR`); verify `MATCH … exit=0` | capture exit 14 `UNEVALUABLE`; verify `UNEVALUABLE … exit=14` |
| D2 EACCES (mode-000 file) | capture `PermissionError` traceback, exit 1 | capture exit 14, receipt written, `READ-ERROR` recorded |
| D3 1-of-5 reference | `MATCH 1/1 exit 0` | unchanged without the flag (`MATCH 1/1 exit 0`); `--require-paths 5` → exit 2 + `REFERENCE-COVERAGE: 1/5 …` (v1 references included) |
| write-guard scope | `--paths X --out X` clobbered X, exit 0 | refused exit 2, X byte-intact; hardlink alias refused exit 2 |
| D6 scratch guard | `FileNotFoundError` traceback exit 1 | `USAGE: …` exit 2 |
| selftest | `CLEAN cases=15` | `CLEAN cases=22 passed=22 failed=0 exit=0` |
| command A (inertness) | — | 82/82 files, 14/14 rules, 10.0/10.0 at HEAD `c07af80` — the landing is outside command A's read set (repo files, not corpus) |

## 4. Attacks / refutations attempted

- **A1 claim-existence (the seat's core attack).** Every behavioral clause of
  the pair was mapped to code + a live command. Two clauses have no implementing
  code: the un-flagged coverage report and the sidecar arm of the write guard.
  Verdict: **both refuted**; the rest stand at `7cd19c3c`.
- **A2 apply-integrity.** Both diffs applied to their named bases reproduce the
  claimed outputs byte-for-byte (`62de3922…`, `a82d0071…`); a second apply is
  refused (no silent double-apply). Verdict: identities intact.
- **A3 stale-base.** EX-30's bases stay correct against HEAD (`c134afcb…`,
  `fa484d57…`); but the worktree README has already been rewritten by EX-21
  (currently `f30df42e…`, exit-14 table and `cases=22` present). Applying
  EX-30's README diff on top of EX-21's worktree file would conflict; the parent
  should land one README text, not both. Verdict: base drift is real, declared
  by EX-30; landing must not double-apply.
- **A4 revision/identity churn (rule #14).** 12 revisions observed in ~15 min;
  the pair was re-emitted under me. I re-derived all identities against the
  re-emitted bytes; the digest the pair pins (`7cd19c3c`) equals the digest of
  the tool I reviewed. The two revisions EX-30 lists that I did not sample
  (`d164d49f`, `d9be407d`) are historical, not landing values. Verdict: handled;
  landing must re-derive once more.
- **A5 selftest has teeth for the new classes.** Names of the 7 closure cases
  confirmed in the bytes; whole run CLEAN 22/22; the earlier mid-edit revision
  (`08fb6833`) failed its own selftest (DIRTY 1/15) and its scratch guard was
  still missing while the docstring claimed it — i.e. the "docstring claims vs
  code" check this seat ran is load-bearing, and the landed revision passes it.
- **A6 write-guard endpoint probes.** Receipt-over-measured-path refused;
  hardlink alias refused; **sidecar-over-measured-path not refused** (gap 2).

## 5. Blockers

- None that stop the review. Residual: the tool/README revisions were live
  during the whole seat; this review pins `7cd19c3c…` and the parent must
  re-derive at landing (the pair's own token table says the same). If the parent
  lands EX-21's README text instead of EX-30's, gaps 1 and 2 do not ship (EX-21's
  current text says "Opt-in: without the flag the comparison is exactly the
  reference's paths, unchanged" and makes no sidecar claim); if EX-30's text is
  landed, apply the two corrections first.

## Self-identity (rule #14)

- `rv8-corrections.patch.md` sha256 `34902a8bb90ee13a8bf3e29079b52b5ca6bb725e168fc743869d42da607dbd3d`
- `evidence/claims-run.txt` sha256 `dd683225cb6020b69bbfffc471f904f265654679f25c4b88e6e61a618f6b1579`
- `evidence/commandA-head-c07af80.txt` sha256 `9de3cbddb68f19ad99003ad329b87b6670c6c83eb7b6f7aef14e1f7af7473cc1`
- instrument reviewed: `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 lines)
- EX-30 pair reviewed: `07bff208…` / `153cc48c…` (as above)