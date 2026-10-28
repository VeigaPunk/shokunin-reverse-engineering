# R46W1RegD — instrument-registry rows (tag `reg-d`) and C2 predicate attack

Seat `R46W1RegD`, round 46 wave 1. Read-only on the lane; all receipts in
`w1/R46W1RegD/receipt.md`. Freeze `31820472784284727546808acc31b3ea1e73919b`.

## 1. Delivered

`w1/R46W1RegD/rows.md` (sha256 `cf4c12bdbdbd905f9f9e02676edff36686dfe22730808268d33be62aa4e09dbd`,
three rows, format self-check exit 0). Rows verbatim:

| `tools/round-41/c2-controls.py` | R41-C2 control builder and scorer: builds CTL-C2-3/5/7, then scores SKILL.md and every CTL-*.md in --out with the frozen v3 interpreter against the independent evaluator on the dev set and reports the kill rule | 0=no control reaches n/n so the kill rule does not fire; 1=a control reaches n/n so the kill rule fires, or an uncaught crash; 2=argparse usage error, nothing evaluated | none | .ufo/waves/round-41/controls/c2/dev-scores-prefreeze.json | --out control docs and --json-out receipt only; never the lane | kaidoku |
| `tools/round-42/c2-counter.py` | R42-C2 counter: scores the SKILL v4 triage table against the frozen independent evaluator over held-out and legacy envelopes, with merge-aware freeze-integrity arms and its own fixture selftest | 0=target met, met_target true with every claim binding true; 1=not met, a pair miss or a binding false, receipt still written; 2=unevaluable, frozen path changed, unknown revision, or an absent or failed generator, evaluator or interpreter | python3 -I -B tools/round-42/c2-counter.py --selftest | corpus/evidence/round-42/c2/heldout/manifest.json | --json-out receipt and $HYAKU_SCRATCH/kaidoku-r42 scratch; no lane writes | kaidoku |
| `tools/round-44/c1-run.sh` | R44-C1 after-freeze data driver: pins PATH and the scratch base, then execs c1-run.py, refusing the committed evidence root unless --data-run or KAIDOKU_C1_DATA_RUN=1 states the freeze is in place | 0=every carrier ran and produced a receipt; 1=at least one carrier failed, by REA exit, no receipt, or a pin mismatch; 2=could not evaluate, usage, environment, missing sibling tool, or an occupied evidence dir | none | tools/round-44/carriers.json | corpus/evidence/round-44/c1 only under --data-run or KAIDOKU_C1_DATA_RUN=1, plus the $HYAKU_SCRATCH/kaidoku-r44 scratch | kaidoku |

All three paths are in the frozen census and are byte-identical at the freeze and at HEAD
(blob ids in receipt), so the semantics below are the semantics that run today.

## 2. What each row rests on (measured, not read off prose)

| row clause | evidence | exit |
|---|---|---|
| c2-controls 0 | `--root . --dev .ufo/waves/round-41/controls/c2/dev --out $S/ctl --json-out …` | 0, `kill_rule_fires False` |
| c2-controls 1 | same + a control that is a copy of `SKILL.md` | 1, `controls_at_full ['CTL-C2-9-skill-copy.md']` |
| c2-controls 1 (crash) | `--root` a dir with no `SKILL.md` | 1, `FileNotFoundError` traceback, empty stdout |
| c2-controls 2 | `--bogus`; also `--selftest` (no such option) | 2 both |
| c2-controls `none` in the self-test cell | `--help` lists `-h --root --dev --out --json-out --build` only | option absent |
| c2-controls pinned path | rerun reproduces the pinned receipt for every file present in both: `SKILL.md 52/52`, CTL-C2-3 `2/52`, CTL-C2-5 `31/52`, CTL-C2-7 `44/52`, `lookup_rows 12`, `kill_rule_fires false` | identical to `dev-scores-prefreeze.json` |
| c2-counter selftest cell | `--selftest` | **0**, `cases=79 green=18 red=61 pass=79 fail=0` (123 s) |
| c2-counter 2 | no args → `usage: --root --rev --freeze required`; `--bogus` | 2 both |
| c2-counter 0/1 | asserted per case inside the 79-case selftest (green cases require exit 0 **and** `met_target`; red cases exit 1) | selftest pass 79/79 |
| c1-run.sh 0 | `--dry-run` | 0; lane status hash identical before/after (`c2d28487…`) |
| c1-run.sh 1 | `--carrier v1le --evidence-root $S/ev --fake-rea /bin/false` | 1, `# v1le: exit 1, receipt False`, wrote only `$S/ev` |
| c1-run.sh 2 | bare invocation (guard); `--bogus`; frozen copy with no sibling `c1-run.py` | 2 for all three |
| c1-run.sh `none` in the self-test cell | wrapper has no option of its own; `c1-run.py` has no `--selftest` | absent |

No instrument takes an exit code outside `{0,1,2}`. (`c2-counter.py` contains `sys.exit(3)`/`sys.exit(9)`
only inside the stub tool sources it writes into selftest fixtures — child processes, not the counter.)
All three do conflate an **uncaught crash** with exit 1; only row A says so, because its 1 has no other
failure path (`c2-controls.py` has no handler at all — measured), while B and C document a failure
meaning for 1 and catch their evaluable errors into 2.

## 3. C2 predicate attack — the frozen instrument cannot score green

### F1. The frozen directory moved after the declared freeze: both counters must exit 2

`tools/round-46/` is edited by two commits after `3182047`:
`50862e4a` ("complete the freeze … declared as the authoritative freeze because the first freeze commit
did not carry the final bytes") and `65678df0`. Blob ids:

| file | freeze | HEAD |
|---|---|---|
| tools/round-46/registry.py | 6581c1b2… | c95128c9… |
| tools/round-46/gate.py | d7cd9aac… | 9ab7e2a3… |
| tools/round-46/attest.py | 25883520… | 936910fe… |

Measured with the **frozen** `gate.freeze_state(lane, 3182047…, "HEAD", plans/round-46-claims.md)`: exit 2,
`frozen_path_changed = ['tools/round-46/', 'tools/round-46/attest.py', 'tools/round-46/gate.py',
'tools/round-46/registry.py']`. Same verdict at rev `e3dfdbad`, at rev `17a72375` and at rev
`04252247` (HEAD advanced three times during the wave; the claims file did not).

The claims' own re-derivation `git log --format=%H -1 -- plans/round-46-claims.md` still returns
`3182047…`, because the later commits touched the **directory** and not the claims file. So the
"authoritative freeze" that `50862e4a` declares is invisible to the derivation the claims specify: the
freeze-integrity rule ("A touch makes the counter exit 2 `frozen_path_changed` and print no
`met_target`") is violated by the lane's own history at every rev from `50862e4a` onward. R46-C1 and
R46-C2 both cannot score, whatever `SKILL.md` says.

### F2. C2 clause 6 is unsatisfiable: the battery's v1 arm can reach at most 5 of 7

The frozen `registry.py` reads `strict_cell` and `strict_exit` from the **spec**, not from the profile
(`score()`, lines 141/179/194: `hard = profile == "v2"` gates the marker/header clauses only), while
the battery scores each forgery with `score(..., "v1", ...)` and clause 6 requires `v1_green == 7`.
Two forgeries are red under v1 by construction:

- `substring-cell` rewrites every `| \`path\` |` cell to `see \`path\` (wrapper)`; `strict_cell` then
  registers nothing → `unregistered: N of N`.
- `prose-exit` rewrites the first `0=…` cell to `0 rows, 1 column, 2 bytes`; `strict_exit` requires
  `\b[012]\s*[=:]` → `thin verdict-map cells: 1`.

Measured on the frozen bytes, three sections:

| section | forgeries_total | v1_green | v2_green | genuine_green | verdict |
|---|---|---|---|---|---|
| my 3 rows, 3-path census | 7 | **5** | 0 | 1 | exit 1, `battery v1_green 5 != 7` |
| my 3 rows, real 38-path census, `--no-battery` | — | — | — | — | exit 1, only `unregistered: 35 of 38` (other reg seats); `thin []`, `absent_at_rev []`, `registered` = my three |
| 38 **canonical** rows from the frozen `house_row`, real census | 7 | **5** | 0 | 1 | exit 1, `battery v1_green 5 != 7` |

The third row is the control: the shortfall is independent of my row wording and of row count, so the
genuine landed section will fail clause 6 as well. The claims' "Before" text ("The v1 clause set scores
all seven forgery classes green (`controls/ctl-c2-1-v1-profile.json`)") is therefore not reproducible
with the frozen instrument. This is the discriminating property inverted: the forged copies are scored
red (good), but so is the genuine artefact, and the counter can never print `met_target`.

### F3. The preflight command in the claims does not run, and its value is stale

`registry.py --selftest` (the exact command in `## Satisfiability preflight`) exits **2**: `--root`,
`--freeze` and `--rev` are `required=True` and only checked after `parse_args`. With dummy args the
frozen bytes print `REGISTRY_SELFTEST: cases=12 failures=0`; the claims say `cases=11 failures=0`.
`attest.py --selftest` has the same required-args shape (bare → exit 2); with args it prints
`cases=15 failures=0`, which does match the claims' value. The 12 registry cases never exercise the
battery, which is why the selftest passes while clause 6 cannot.

### F4. Two controls the C2 "Before" section cites do not exist

`## R46-C2 — Before` cites `controls/ctl-c2-1-v1-profile.json` and `controls/ctl-c2-2-ghost-tool.json`.
The tree holds `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v1-scope.json`, `ctl-c2-fidelity.json` — neither
cited name exists. `ctl-c2-1-v1-scope.json` is a round-45-spec artefact (scope 6, no `spec`/`profile`
fields, `met_target true`) and cannot stand in for a v1-profile battery receipt. The C1 section likewise
cites `controls/ctl-c1-1-v1-profile.json`, which is absent (the C1 file present is `ctl-c1-fidelity.json`).

### F5 (minor). Unevaluable write errors exit 1, not 2

With a `--json-out` whose parent directory does not exist, the frozen `registry.py` raises
`FileNotFoundError` inside `gate.emit` and exits **1** with a traceback — an unevaluable condition
reported as "not met". `gate.emit` does not create the parent directory.

### F6 (minor). `restored` mislabels genuinely changed files

`blob_changed()` records a changed **directory** as `'tools/round-46/'`, while `restored` compares the
file paths the history arm saw against that set, so `attest.py`, `gate.py` and `registry.py` are listed
as `restored` ("blob arm finds clean") although their blob ids differ between freeze and HEAD. The net
exit code stays 2, but a diagnostic reader of `restored` is misled in exactly the direction the arm
exists to prevent.

## 4. Reconciliation with sibling seats

- The 38-path census makes `unregistered` the only structural failure for a partial registry; my three
  rows contribute `thin []` and `absent_at_rev []`. When the other reg seats' rows land, the section
  should satisfy clauses 1–5 — I verified this on the 3-path fixture (`unregistered []`, exit 0 up to
  the battery).
- Row B's pinned path (`corpus/evidence/round-42/c2/heldout/manifest.json`) and row C's
  (`tools/round-44/carriers.json`, `sha256` per carrier) are present at the freeze.
- I did not touch `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`,
  or any sibling lane; my only lane writes are this report, `rows.md` and `receipt.md`.

## 5. Assessment

The three rows are ready to paste and every cell is backed by a command I ran. The predicate they feed
is not: **R46-C2 as frozen can never report `met_target`** — first because the frozen directory was
edited after the declared freeze (exit 2 `frozen_path_changed`, F1), and second because clause 6's
`v1_green == 7` exceeds the maximum the frozen battery can produce, 5 (F2). Landing block 23 and the
registry rows without addressing those two will produce a red counter on a genuine artefact and a
`frozen_path_changed` exit 2 before it. Both findings are reported with the exact commands and values,
not fixed.

Reproduction: `w1/R46W1RegD/receipt.md` probes 15–23; fixtures `fx` (3-path census),
`fx3` (real census), `fx4` (38 canonical rows), built under
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegD` and removed after the receipts were copied.
