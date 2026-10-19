# CN-1 round-2 baseline — independent instrument readings at HEAD `14b1682`

Wave arc3-loop1-round2 · chain cross · seat CN-1 (connector) · 2026-10-19 · all
captures read-only, scratch under `/dev/shm/cn1r2` (`/tmp` quarantined, EDQUOT).

Captured **before reading any round-2 seat artifact** (first capture 12:00:06Z;
this file written 12:0xZ). Purpose: the round-B baseline every chain's recorded
reading is checked against.

## 1. Revision + instrument identities (worktree == HEAD blob for all)

| item | sha256 | source |
|---|---|---|
| HEAD | `14b1682b1128d2e41085ebc79c9addeb8786d420` | `git rev-parse HEAD`; `git log -1` = "arc3-loop1-round1: records — …" |
| `.ufo/gates/c1-census-v10.py` | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (490 L) | worktree == `git show HEAD:` blob |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` (499 L) | idem |
| `.ufo/gates/citation-drift/expected.json` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` | idem |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` (331 L) | idem |
| PROVINCE.md | `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 L) | idem |
| SCORECARD.md | `a7c72950094ecae0e67204668dac21138c1d5d613bb9e36f1bec241b834f4a93` (1417 L) | idem |
| SKILL.md | `483b0eba27458c138fdbe760d83a33f0da54b251ec028f033d83a5ae3d0175eb` (371 L) | idem |
| corpus/README.md | `6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577` (190 L) | idem |
| knowledge list digest | `e20d8b1fd87d72267a57ac803b23c4ddf34693698e4b9fa76d62ca221feaf2dc` (83 paths, path+NUL+blob) | CN-1 script, `baseline/knowledge-sha256.txt` |

`git status --porcelain`: ` M .ufo/waves/arc2-loop1-round10/C3.md` (pre-existing,
not this wave), `?? .ufo/gates/__pycache__/` (untracked, present at capture —
round-1 close had it removed; re-appeared before this wave), `?? .ufo/waves/arc3-loop1-round2/`.

## 2. command A — `SCORECARD.md:92-124` recipe, REV = `14b1682…`, verbatim

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "14b1682b1128d2e41085ebc79c9addeb8786d420",
 "rule_blocks": 13}
```

→ **82/82 files, 13/13 rules, 10.0/10.0.** Raw: `baseline/commandA-t0.txt`.
Round-2 expectation: C1 moves rules 13 → 14 (claim text); C2/C3 must leave
82/82 + 13/13 untouched (their edit surfaces are outside recipe A's read
surfaces: corpus/knowledge/, corpus/README.md map section, SKILL.md craft
section). Any C1 record stating 82/82 **before** its rule lands, or any C2/C3
record stating 14/14, is a contradiction.

## 3. census — `.ufo/gates/c1-census-v10.py` copy of `6f1d19ff…` (baseline v10)

```
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1417 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)   exit=0
```

JSON: `baseline/census-t0.json` (`verdict PASS`, `scope_errors []`, `g7 []`,
`g11 []`, `g2_ok true`, `unreadable` field absent — that field is the C2 after-leg).
`current_ok` blocks = **5** (PROVINCE:44, SCORECARD:619, :699, :732, :753).
Note for H3's floor: 5 > 0, so a strict `len(current_ok) > 0` floor does not
break the HEAD run.

Cross-round control (worth keeping straight): the same instrument run over a
scratch root built from `e845c2b`'s three files (`baseline/root-e845c2b`) also
reads **PASS, 6/9/2 loci, current_ok 5** — so the round-1 records append
(SCORECARD 1336 → 1417) added no locus. CR-5's round-1 record "current-ok loci:
10" is a different counting unit than the instrument's `len(current_ok)` blocks;
both are > 0, so no floor conflict either way.

## 4. citation-drift probe — copies of the committed gate

| run | result |
|---|---|
| `--selftest` | `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0` (cases incl. `table_tampered` → exit 2 `pointer_table_tampered`, `table_absent` → exit 2 `pointer_table_unreadable`) |
| `--root <repo> --rev HEAD` (default) | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` |
| `--root <repo> --rev HEAD --strict` | `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` |

## 5. custody — 5 paths, two independent capture methods

`sha256sum` (12:00:06Z) and the C3 v2 tool's capture (12:04:36Z) agree 5/5:

| path | sha256 | mtime epoch | inode |
|---|---|---|---|
| `~/.config/devin/mcp_config.json` | `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4` | 1792011200 | 11341318 |
| `~/.omp/agent/mcp.json` | `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b` | 1792011200 | 11341316 |
| `~/.kimi-code/config.toml` | `8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d` | 1792376443 | 34530637 |
| `~/.bashrc` | `7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598` | 1792168396 | 25991953 |
| `~/.profile` | `6c6be761d3b199c964c95e724d7cdc9f4f902e0c3bdd6a532361b20a53db4f30` | 1792044727 | 40274 |

All five digests are **byte-identical to every round-1 capture** (round-1
`cross/consistency.md` §1; CU-1 pre-pair, EX-01 3-impl recompute, EX-02 pre/post,
EX-15 T0/T1) — no custody path has moved since round-1 close. UTC renders:
devin/omp `2026-10-14T20:53:20Z`, kimi `2026-10-19T02:20:43Z`, bashrc
`2026-10-16T16:33:16Z`, profile `2026-10-15T06:12:07Z` (local = -03).

## 6. Cross-chain expectations this baseline fixes

1. **Census baseline**: PASS 0/0/0/0, exit 0, counts 162/6 · 1417/9 · 371/2,
   instrument `6f1d19ff…`, at `14b1682`. Pre-EX-16 readings must match this; the
   C3 chain additionally runs the census *after* EX-16's edit, where the count
   identity must hold and the verdict must stay PASS (C2's claim: ordinary runs
   at HEAD stay PASS 0/0/0/0).
2. **Custody**: the 5 digests above are the contract. C3's v2 tool must
   reproduce them live (5/5) and v1 receipts remain verifiable via sha256 fields.
3. **command A**: 82/82 · 13/13 · 10.0/10.0 at baseline; C1's after-reading is
   14/14 with prior 13 rule blocks byte-identical; C2/C3 after-readings stay 13/13.
