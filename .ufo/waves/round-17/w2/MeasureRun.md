# MeasureRun — wave-2 falsify: measure.py outputs at baseline vs head

Seat: `KaidokuR17.MeasureRun` (author-side advisory). Scope: run `measure.py` on
both pinned revisions, save stdout, report deltas and pre-claim hazards.
Commands run exactly as assigned; both exited 0, stderr empty.

```
python3 -I -B .ufo/waves/round-17/measure.py b563c799d97774aae4351276fe43cb897311e349
  > .ufo/waves/round-17/w2/measure-base.json     (1216 bytes)
python3 -I -B .ufo/waves/round-17/measure.py da64646adcb19c1ede7537b799b8c7d283fe43da
  > .ufo/waves/round-17/w2/measure-head.json     (1985 bytes)
```

## Presence/count deltas (base → head)

| field | base | head | delta |
|---|---|---|---|
| `tools_present` | 0 | 11 | +11 (all 11 `TOOLS` blobs exist; sizes 8.9–25 KB per `git ls-tree -l`) |
| `measure_py` | 0 | 1 | +1 |
| `controls_py` | 0 | 1 | +1 |
| `C1_quality_row19` | 0 | 1 | +1 |
| `C2_knowledge_entry` | 0 | 1 | +1 (blob `f4796cb`, 10,986 B — non-empty) |
| `C2_scorecard_capability_row` | 0 | **0** | unchanged |
| `scorecard_capability_rows_matching` | 0 | 0 | 0 |
| `skill_registry_rows_new_tools` | 0 | 12 | +12 (see F2 — 2 are not new) |
| `run_receipts` | 0 | 8 | +8 (see F1 — all 8 fail the wave's own validator) |
| `knowledge_files` | 94 | 95 | +1 |
| `mapped` | 94 | 95 | +1; `missing`/`dangling` empty at both |
| `sources_rows` | 23 | 30 | +7 (S024–S030) |
| `tiers` | A21 B1 C1 | A26 B2 C2 | A+5 B+1 C+1 |
| `statuses` | mined 22, rejected 1 | mined 28, rejected 2 | mined +6, rejected +1 |

## Findings

### F1 — All 8 retained receipts fail the wave's own `receipt-validate.py` (`unrecognized_shape`, exit 1). [OBSERVATION]

`measure.py:54,147` counts 8 `runs/*/receipt.json` blobs. Re-validating each
(blob extracted via `git show <head>:…/receipt.json`):

```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py <receipt>
→ {"counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "exit": 1}
  finding: {"code": "unrecognized_shape",
            "detail": "receipt matches neither retain nor carrier shape"}
```

identical for all 8 (`calib-esbuild-0.25.12`, `calib-shfmt`, `pro-aether`,
`pro-containerd-shim`, `pro-esbuild-0.21.5`, `pro-esbuild-0.27.7`,
`pro-notesmd-cli`, `pro-op`). Cause is a producer/validator schema
disagreement shipped in the same wave:

- `tools/carrier-run.py:275` initialises `"steps": {}` and `:312,:317,:331,:338,:349`
  store named keys (`inspect-go-binary`, `analyze`, `search:<name>`) — `steps`
  is a **dict** in every emitted receipt (verified by reading one).
- `tools/receipt-validate.py:98-101` classifies `carrier` only when
  `steps` is a **list**; its selftest fixture (`:470`) also builds a list.
- The `retain` fallback (`:102`) requires an `argv` key; emitted receipts carry
  `orig_argv` instead → kind `unknown` → `unrecognized_shape`.

`contract.md:43` says "every step {argv, cwd, …}" without fixing dict-vs-list,
so one side is wrong and the contradiction was committed undetected. Per-leg
`carrier-run.exit`/`compare.exit`/`observation.exit` all contain `0` and
`runs/run-log.txt` shows `carrier-run=0 compare=0` — the runs genuinely
completed; it is the receipts' validation status that is broken. This directly
undermines claim C2's gate "receipt validates" (`claims.json` C2
`falsifiable_before_after`).

### F2 — `skill_registry_rows_new_tools` counts stale rows and masks two unregistered tools. [OBSERVATION]

Head reports 12 names, but only 10 are new round-17 rows (`SKILL.md:532-541`).
`citation-drift` (`SKILL.md:448`) and `custody-pair` (`SKILL.md:449`) are
pre-existing registry rows — present at baseline without any round-17 text —
that merely gained `.ufo/waves/round-17/verification.json` mentions in their
cells; `REGISTRY_R17` (`measure.py:53`) matches *anywhere* in the row text, so
the field named `*_new_tools` counts rows that are not new. Simultaneously,
two committed round-17 tools have **no** registry row at all:
`tools/retain.py` and `tools/carrier-census.py` — the only non-prose mention of
`carrier-census` in the wave is `contract.md:110-111`; `grep 'retain\|census'
SKILL.md` shows no `|`-row for either. The inflated 12 accidentally hides both
missing registrations. (Command:
`git show <head>:SKILL.md | grep -c round-17` on baseline rows = 0 for the two
stale names.)

### F3 — `C2_scorecard_capability_row` stays 0; claim C2's capability entry is unmet at head. [OBSERVATION]

SCORECARD.md is **byte-identical** to baseline — it does not even appear in
`git diff --stat base head` (only SKILL.md, corpus/QUALITY.md, corpus/README.md,
corpus/SOURCES.md changed), and `grep 'round-17' SCORECARD.md` returns nothing
across all 2,348 lines. The drafted conditional row exists only in
`w1/draft-scorecard.md:44` ("retained REA Ghidra-session log capture…",
marked "NOT entered unless the demonstration runs"). The claim's condition
"only if … its receipt validates" (`claims.json` C2) is consistent with
non-entry **given F1** — but that means the depth claim's capability leg is
not discharged at the integrated revision, whichever side of the F1
disagreement is at fault.

### F4 — Retained-evidence completeness gap: `runs/run-log.txt` records 7 end-lines for 8 run dirs. [OBSERVATION, minor]

The log has 8 `== <label> start` / `… end … carrier-run=0 compare=0` pairs
except `calib-shfmt`, which has neither a start nor an end line despite a
complete run dir (all exits 0, 108,303-byte receipt). Either the shfmt run
predated the log's append discipline or a write was lost; the run dirs are
correct, so impact is bookkeeping-only. (Command: `git show
<head>:.ufo/waves/round-17/runs/run-log.txt`.)

## Predicates satisfiable by text alone (pre-claim hazards)

Every hazard below is *by construction* — the docstring (`measure.py:8-15`)
explicitly disclaims semantic pass — but these are the exact fields a reader
could still treat as discharged:

| field | predicate (measure.py:line) | text-only satisfaction |
|---|---|---|
| `C2_scorecard_capability_row` | `CAPABILITY_TEXT` substring in any `|`-line inside the `## Capabilities` section (`:46`,`:128-129`) | adding the literal phrase `retained REA Ghidra-session log` to any row — a section comment row, a different capability's text — flips 0→1 with no run, no receipt, no Ghidra log. Currently 0 *and* SCORECARD.md untouched, so hazard is latent, not exploited. |
| `C1_quality_row19` | first line matching `^\|\s*19\s*\|` anywhere in QUALITY.md (`:48`,`:116-118`) | any `| 19 |` line satisfies; no content/topic check. Also: **row 20 was added this same wave** (`corpus/QUALITY.md` diff, +2 rows) and is invisible to the metric — a bool on the first match. |
| `skill_registry_rows_new_tools` | row's 2nd cell is `probe|gate|tool / kaidoku` AND row text contains `.ufo/waves/round-17/` (`:52-53`,`:144-145`) | editing any old row to mention a round-17 path counts it (F2's citation-drift/custody-pair inflation — already realized, not hypothetical). |
| `run_receipts` | path regex `runs/[^/]+/receipt\.json` (`:54`,`:147`) | an empty/invalid blob counts; realized today — all 8 are `unrecognized_shape` under the wave's own validator (F1) yet report as 8. |
| `tools[*]`, `measure_py`, `controls_py`, `C2_knowledge_entry` | path membership in `ls-tree` (`:149`,`:154-156`) | a zero-byte or garbage blob at the path satisfies. Currently all blobs are real (sizes verified via `ls-tree -l`). |
| `mapped`/`missing`/`dangling` | `2026-10-\d{2}-[a-z0-9-]+` tokens anywhere in the coverage-map section (`:50`,`:103`) | a bare date-stem in prose (not a `knowledge/…` cell target) maps an entry or creates a dangling without being a link. Currently clean. |
| `sources_rows`/`tiers`/`statuses` | `^\|\s*S\d{3,}\|` rows; fixed cell indexes 4/8 (`:49`,`:113-114`,`:169-174`) | a malformed row silently counts with `""` tier/status. Verified all 30 rows have 11 cells at head — no defect now. |

### Brittleness notes (not defects at head)

- `measure.py:94` splits `## Coverage map\n` literally — a trailing space or
  `###`-level heading → exit 2. Same for `## Capabilities\n` at `:120-123`;
  additionally if Capabilities were the *last* section, the `\n## ` split
  would IndexError → exit 2 (currently Saturation follows).
- `RECEIPT_PATH` (`:54`) requires exactly `receipt.json`; `run-log.txt` and
  any `*receipt*.json` variant under a run dir are invisible.
- `resolve()` (`:68-72`) pins `^{commit}` correctly; `argv`/`orig_argv` in
  output are informational only.

## Boundary

Did not verify temporal-sweep/invocation-audit predicates (C1's other
falsifiables belong to sibling seats), did not validate receipt *contents*
beyond shape classification, did not execute any carrier. Measure outputs are
byte-exact stdout; repo-relative anchors cite `measure.py` at worktree HEAD and
committed blobs at `da64646`.
