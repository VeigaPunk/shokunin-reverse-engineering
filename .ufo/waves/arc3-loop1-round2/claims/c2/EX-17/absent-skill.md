# EX-17 artifact — post-landing injection: absent SKILL.md (chain c2, executor)

Wave `arc3-loop1-round2`, 2026-10-19. Seat task: run the **post-landing** fixture
— a root that matches HEAD except SKILL.md is absent — against a `/var/tmp` copy
of the landed census, expecting the **declared FAIL class**, captured verbatim.

This seat wrote no repo target. The census (`.ufo/gates/c1-census-v10.py`) is
EX-16's write; every run below executes a `/var/tmp/ex17r2` copy. Scratch is
`/var/tmp/ex17r2` (never `/tmp`).

## 1. Instrument identity (the target moved during the wave)

| revision | sha256 | bytes/lines | copy taken (UTC) | role here |
|---|---|---|---|---|
| pre-landing v10 | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | 23939 / 490 | 12:01:31 | before-column instrument |
| v11 rev A | `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` | 31207 / 601 | 12:13:55 | first landed revision measured; EX-16's receipt names it (12:12:15Z) |
| v11 rev B | `a4c167631269e5110fbdcf323b6be2a779eaa1e0ca79c98201419261ba9c6bfb` | 31364 / 603 | 12:17:09 | header/usage self-description change only |
| v11 rev C | `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` | 31906 / 610 | 12:18:43 | latest measured (hash re-verified 12:20:24Z); G20 docstring wording only. **EX-16's seat report (written later) declares this revision FINAL and behaviourally identical to rev A** — independent corroboration of this artifact's binding |

Rev C vs rev B diff is docstring-only (the G20 floor's unit note: current-ok
**detections**, not blocks or rows); no guard-logic change, and the sweep
verdicts are identical across rev A/B/C (`after-table.txt`, `after2-table.txt`,
`after3-table.txt`). **Churn note for the integrator:** the target moved at least
five times during landing (CR-2's timeline: `6f1d19ff → 2a89793a → 82fb807e →
09e270c2 → c95a5cf3 → df9ffdf9 → a4c16763 → d0772ce8`); any seat or certificate
that recorded the instrument's identity before 12:18 holds a superseded value
(rule-#14 discipline: re-derive at landing).

## 2. Fixture lab (all under /var/tmp/ex17r2, byte-identical inputs to HEAD)

PROVINCE.md `d075a3c6…`, SCORECARD.md `a7c72950…`, SKILL.md `483b0eba…` —
sha256 of every fixture file in `manifest-fixtures.txt`. Roots:

| root | SKILL.md state |
|---|---|
| `root-present-all` | byte-identical copy (control) |
| `root-absent-skill` | **absent** (the seat's designated fixture) |
| `root-empty-skill` | present, 0 bytes (`e3b0c442…`) |
| `root-truncated-skill` | present, first 5 lines only (`3d1fcd00…`) |
| `root-unreadable-skill` | present, mode 000 (EACCES) |
| `root-skill-is-dir` | present as a directory |
| `root-dangling-skill` | symlink to `/nonexistent/nothing` |
| `root-blank-skill` | present, 371 lines, scoped lines 10–20 blanked to `x` (`b83e8168…`) |
| `root-all-absent` | all three scoped files absent |

Driver: `sweep.sh` (runs `<instrument> --root ROOT --quiet`, captures
stdout+stderr+exit verbatim per root). The repo tree itself is run as `head`.

## 3. Before (pre-landing v10, `6f1d19ff…`) — silent PASS on the designated fixture

`pre-absent-skill.txt` (verbatim):

```
$ python3 v10-pre.py --root /var/tmp/ex17r2/root-absent-skill --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=0    loci=0

SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit=0
```

`pre-table.txt` / the `pre-*.txt` logs: **nine of ten** roots PASS exit 0
(absent, empty, truncated, EACCES, is-a-dir, dangling, blank). The tenth,
`all-absent`, already exited 1 — but only through the DATED rows'
marker-uncheckable SCOPE-ERRORs (`pre-all-absent.txt`); nothing named the
missing file, and a CURRENT-only scoped file (SKILL.md) left no trace at all.
Full report: `before-absent-skill-full.txt`; json: `before-absent-skill-json.txt`.

## 4. After (landed rev C `d0772ce8…`) — declared FAIL, captured verbatim

`after3-absent-skill.txt` (quiet, primary fixture):

```
$ python3 v11-landed3.py --root /var/tmp/ex17r2/root-absent-skill --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=None loci=None

SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=0; total loci=15; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: ['UNREADABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
exit=1
```

`after3-absent-skill-full.txt` carries the full text report (per-locus
dispositions); `--json` (`after3-absent-skill-json.txt`) carries
`"SKILL.md": {"lines": null, "loci": null}`, `"verdict": "FAIL"`,
`"unreadable": ["SKILL.md: FileNotFoundError"]`,
`"declared_fail_classes": ["UNREADABLE"]`, `"g2_floor": "1/readable-file"`,
`"current_ok_per_file": {"SKILL.md": 0, …}`.

`sweep.sh` matrix, rev C (`after3-table.txt`; rev A/B identical — `after-table.txt`,
`after2-table.txt`):

| root | before (v10 `6f1d19ff`) | after (v11 rev C `d0772ce8`) |
|---|---|---|
| head (repo) | PASS 0/0/0/0 exit 0 | **PASS 0/0/0/0 exit 0** |
| present-all | PASS exit 0 | PASS exit 0 |
| **absent-skill** | **PASS exit 0, `lines=0 loci=0`** | **FAIL exit 1, `UNREADABLE ['SKILL.md: FileNotFoundError']`** |
| empty-skill | PASS exit 0 | FAIL exit 1, `'SKILL.md: 0 lines < declared max 20 (rows beyond EOF)'` |
| unreadable-skill (EACCES) | PASS exit 0 | FAIL exit 1, `'SKILL.md: PermissionError'` |
| truncated-skill (5 lines) | PASS exit 0 | FAIL exit 1, `'SKILL.md: 5 lines < declared max 20 …'` |
| skill-is-dir | PASS exit 0 | FAIL exit 1, `'SKILL.md: IsADirectoryError'` |
| dangling-skill | PASS exit 0 | FAIL exit 1, `'SKILL.md: FileNotFoundError'` |
| blank-skill (readable, 0 loci) | PASS exit 0 | FAIL exit 1, `BLIND-INSTRUMENT` (per-file floor `SKILL.md=0`) |
| all-absent (3 files) | FAIL exit 1, marker SCOPE-ERRORs only; unreadability **unnamed** | FAIL exit 1, three `FileNotFoundError` entries in `UNREADABLE` + the same marker SCOPE-ERRORs |

The declared class drives the verdict (exit 1), it is not a printed note:

```
ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \
     and (not g11) and g2_ok and (not unreadable)          # rev C, c1-census-v10.py:561-563
```

## 5. Attacks attempted, with verdicts

1. **Designated fixture (absent SKILL.md)** — before: silent PASS (`lines=0
   loci=0`, `SCOPE-ERRORS []`); after: FAIL `UNREADABLE`, exit 1. **CLOSED.**
2. **Empty (0-byte) file** — v10 silent PASS; rev C FAILs via the
   `len(lines) < declared max end` branch (not via OSError). **CLOSED.**
3. **Truncated file (rows beyond EOF)** — FAIL, same branch. **CLOSED.**
4. **EACCES / is-a-directory / dangling symlink** — all FAIL `UNREADABLE`. **CLOSED.**
5. **All three scoped files absent** — FAIL `UNREADABLE` ×3 (plus the
   pre-existing marker SCOPE-ERRORs, not masked). Before-state nuance: this root
   already exited 1, but the *unreadability* was unnamed; the class is the new
   part. **CLOSED.**
6. **Readable-but-blind file** (`root-blank-skill`: 371 lines, scoped needle
   lines blanked) — FAIL `BLIND-INSTRUMENT` exit 1
   (`after3-blank-skill.txt`). A per-file collapse is caught while the other two
   files stay loud — refutes the "tree-level floor swallows it" worry. **CLOSED.**
7. **All needles neutered** (neutered clone `v11-landed3-blind.py`) — FAIL
   `BLIND-INSTRUMENT` exit 1, `total loci=0`
   (`after3-blind-present-all.txt`). The H3 half of the claim independently
   reproduces. **CLOSED.**
8. **PIN needle alone neutered** (`v11-landed3-pinblind.py`) — **PASS exit 0**,
   counts unchanged (loci 6/9/2; current-ok 17/14/3): bare-version needles carry
   those loci, so PIN-only blindness moves no count. This is the H4/self-
   certification residual EX-16 declares in the landed header (rev C
   `c1-census-v10.py:63-80`); the frozen claim's floor clause is about *zero*
   loci in a non-empty scope, so this is **residual confirmed as declared**, not
   an undeclared hole. Named for the integrator: only the external
   scope-diff/locus-count audit sees this class.
9. **Ordinary-run regression** — repo HEAD and `present-all` read PASS 0/0/0/0
   exit 0 on rev A/B/C: the fail-closures do not fire on the honest tree.

## 6. Reproduction

```bash
cp .ufo/gates/c1-census-v10.py /var/tmp/ex17r2/v11-landed3.py     # landed copy
python3 /var/tmp/ex17r2/v11-landed3.py --root /var/tmp/ex17r2/root-absent-skill [--json]
# root built once:  mkdir -p .../root-absent-skill; cp PROVINCE.md SCORECARD.md there (no SKILL.md)
```

Evidence in this directory: `pre-*.txt` + `pre-table.txt` (before column),
`after-*.txt` / `after2-*.txt` / `after3-*.txt` (rev A / B / C),
`before-absent-skill-full.txt`, `before-absent-skill-json.txt`,
`manifest.txt`, `manifest-fixtures.txt`, `poll-ex16.sh`, `sweep.sh`,
`run-fixture.sh`, and instrument copies `v10-pre.py`, `v11-landed{,2,3}.py`,
`v11-blind.py`, `v11-landed{,2,3}-blind.py`, `v11-pin-blind.py`,
`v11-landed{,2,3}-pinblind.py`.
