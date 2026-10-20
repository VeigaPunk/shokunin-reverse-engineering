# LessonMistakesAudit — round-18 `## Mistakes` falsify (wave 2)

PARTIAL

Audited rev: b2aad08ceeee8dd125ce0d316056d8bd766c7f94 (lane worktree was byte-identical to it at audit start; it was concurrently modified, uncommitted, mid-audit — see F3). All path:line anchors below are at that rev unless stated. Read-only; only this file written. Python run as `python3 -I -B`. No REA analyze/search/decompile, no Ghidra, no carrier execution, no jj, no git writes in the lane.

Target: `corpus/lessons/round-18.md:60-69` (`## Mistakes`, 8 rows). Vocabulary checked against `/home/vgpnk/Projects/shokunin/CORPUS.md:173-174` (`vacuous, survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider`).

## Row-by-row

| # | class ok | evidence resolves at REV | captured-by right | fix red/green executed | verdict |
|---|---|---|---|---|---|
| 1 vacuous / R17-PINMAP | yes | `round-17-verifier-spotcheck.md:108` and `:137` resolve; **`carrier-run.py:475` does not** (F2) | yes (`corpus/QUALITY.md:29` #19 requires retained pin maps; "not applied / self-attestation" matches) | red+green+forge all observed | holds minus stale anchor |
| 2 number-drift / R17-VALIDATE16 | yes | defect id routes to `round-17-verifier-spotcheck.md:139-141`; `SCORECARD.md:2364` ("all 16 receipts … exit 0") resolves | yes (`corpus/QUALITY.md:28` #18) | red+green observed | holds |
| 3 attribution / R17-PRODUCER-REV | yes | routes to `round-17-verifier-spotcheck.md:142-143` | yes (#18 "measured revision") | red observed, reason matches row text verbatim | holds |
| 4 landing / R17-SUMS-RUNLOG | yes | routes to `round-17-verifier-spotcheck.md:144-146`; missing line reproduced | yes (`none` honest) | red observed, byte-exact missing line | holds |
| 5 reference-drift / R17-REGISTRY+S032-DIGEST | yes | routes to `round-17-verifier-spotcheck.md:147` | yes (`corpus/QUALITY.md:14` #4; PROTOCOL `/home/vgpnk/Projects/shokunin/PROTOCOL.md:398-405` defines "write scope" as a row field) | red+green observed | holds |
| 6 vacuous (this round) / C1 counter | yes | `.ufo/waves/round-18/w1/CriticC1.md:9` ("token-only commit flips all six defects to closed") resolves | yes (`none` honest) | **stated observable `--selftest` CLEAN 17 is false at REV** (F1) | **fails** |
| 7 number-drift (this round) / C2 | yes | `.ufo/waves/round-18/claims.json` present at REV; `w1/CriticC2.md:64` ("the rules give live = 8") resolves | yes (`/home/vgpnk/Projects/shokunin/CORPUS.md:34` "A count carries its command") | baseline 3 live/8 fixture/10 excluded reproduced exactly; REV live 0 | holds |
| 8 stale-premise (this round) / C3 | yes | `.ufo/waves/round-18/predictions/decision-rule.json` present at REV, unchanged since freeze | yes (`none` honest) | freeze-before-run verified; carriers exist | holds |

## Commands run and exit codes

All from lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

1. Green — six defects closed at REV:
```
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
→ exit=0; open_count 0, named 0, substance 0; R17-PINMAP/VALIDATE16/PRODUCER-REV/SUMS-RUNLOG/REGISTRY/S032-DIGEST all "closed"
```
2. Red — same command at baseline (rows 2–5's claimed red; `--strict` for non-clean exit):
```
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470 --strict
→ exit=1; open_count 6, named 6, substance 6
```
Named reasons match each row's parenthetical: row 3 — `[substance] scorecard/knowledge/log-names-pinned-revs: no line containing 'R17-PRODUCER-REV' + '271167473d…' + '95e34db6…'`; row 4 — `[substance] sums-restored-from-2711674: 1 historical line(s) missing: b'8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv'`; row 5 — `[substance] skill-scope-{go-route-compare,receipt-validate,pins,go-buildinfo-probe}: no 'Write scope:' in 5th cell`, `[named] skill-row-citation-drift: 2nd cell is 'probe / kaidoku'`, `[substance] s033-anchor-commit: no superseding row`, `[substance] s032-digests-evidence: … absent at rev`; row 2 — `[named] validate16-summary: .ufo/waves/round-18/evidence/validate16/summary.json absent at rev`.
3. Row 1 red:
```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-17/runs/{calib-esbuild-0.25.12,calib-shfmt,pro-aether,pro-containerd-shim,pro-esbuild-0.21.5,pro-esbuild-0.27.7,pro-notesmd-cli,pro-op}/receipt.json
→ exit=1; counts {invalid: 8, receipts: 8, unreadable: 0, valid: 0}; findings {'mid_map_missing': 29}
```
(29 findings = the "29/29 second-pass checks" of the defects section. Footnote: `.ufo/waves/round-17/runs/run-log.txt` is a file, so `runs/*/receipt.json` also globs `run-log.txt/receipt.json` and turns the run into exit 2 "unreadable: 1" — invocation hazard, not a lane defect; the 8 explicit receipts are the honest red.)
4. Row 1 green:
```
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/{calib-aether,calib-notesmd-cli,real-kimi-webbridge,s1246-noswiss-methods,s1246-noswiss-nethttp,s1246-noswiss-nomethods,s1246-swiss-methods,s1246-swiss-nethttp,s1246-swiss-nomethods,s1250-noswiss-methods,s1250-noswiss-nethttp,s1250-noswiss-nomethods,s1250-swiss-methods,s1250-swiss-nethttp,s1250-swiss-nomethods}/receipt.json
→ exit=0; {invalid: 0, receipts: 15, unreadable: 0, valid: 15}
```
5. Row 1 forge (direct, outside the lane):
```
python3 -c "…load .ufo/waves/round-18/runs/calib-aether/receipt.json; set steps.analyze.pin_checks[0].entries 152→999999; dump /tmp/k18forge/receipt.json"
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py /tmp/k18forge/receipt.json
→ exit=1; findings [('mid_entries_mismatch', '$.steps.analyze.pin_checks[0]'), ('mid_map_entries_mismatch', …)]
```
Also `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --selftest` → `SELFTEST: CLEAN cases=18`, exit=0 (row 1's "(selftest)" anchor holds).
6. Row 7 tool:
```
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470
→ exit=0; files_scanned 27, live 3, fixture 8, annotated 0
live: (.ufo/gates/citation-drift/citation-drift-probe.py:477 default-HEAD), (.ufo/gates/custody-pair/custody-pair.py:327 rev-parse-HEAD), (.ufo/waves/round-17/verify.py:59 rev-parse-HEAD); excluded 10 files (all round-17 w2 seat dirs)
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
→ exit=0; files_scanned 39, live 0, fixture 15, annotated 6
```
Matches `claims.json` amendment C2 and the Gate cell "3 live / 8 fixture / 10 excluded files at 9011581" exactly.
7. Row 6 stated observable — **fails at REV** (see F1):
```
python3 -I -B /tmp/k18revtool/routed-defects.py --selftest   # /tmp copy of git show REV:.ufo/waves/round-18/tools/routed-defects.py
→ exit=1; "SELFTEST: FAILED closed-fixture-cli: … opened=['R17-PINMAP','R17-PRODUCER-REV'] broken=['receipt-validate-mid-finding','producer-revs-are-ancestors']; closed-fixture-inprocess: open_count=1 broken=['receipt-validate-mid-finding']; token-only-R17-{VALIDATE16,PRODUCER-REV,SUMS-RUNLOG,REGISTRY,S032-DIGEST}: … extra_open=['R17-PINMAP']"
```
Identical output from the in-lane copy before the concurrent edit (verified `git show REV:…routed-defects.py | diff -q - <worktree file>` → identical, immediately after that run).
8. Row 8 freeze ordering (observations):
```
git show -s --format='%h %cI' eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 → "eb6c266 2026-10-20T13:23:55-03:00" (=16:23:55Z)
git diff --stat eb6c2668… b2aad08… -- .ufo/waves/round-18/predictions/ → empty (predictions unchanged since freeze)
.ufo/waves/round-18/runs/calib-aether/receipt.json: steps.inspect-go-binary started_at_utc 16:24:07.22Z, steps.analyze 16:24:08.04Z, analyze pin_checks ×3 with map_path+map_sha256, len(pins_pre.entries)=152
```
Freeze (16:23:55Z) precedes the first run step (16:24:07Z) ✓; decision-rule.json carries `diagnostic_set_D`, `confirmed` rule, `binding_gate` ✓.

## Findings

### F1 (major — row 6's fix does not hold at REV)
`corpus/lessons/round-18.md:67` claims the C1 fix is "shown able to fail" with "`routed-defects.py --selftest` CLEAN 17". At REV the tool's selftest exits 1 with 7 of 17 cases failing (command 7 above). Root cause [observation]: the selftest's own closed fixture still uses the placeholder validator token — REV `routed-defects.py:914` area defines `RECEIPT_VALIDATE: "FINDING = \"mid_map_mismatch\"…"` in `_closed_files()`, while the as-built check it must satisfy (REV `:277-285`, "L1 amendment … contract.md's placeholder `mid_map_mismatch` was never an id") requires both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch` in non-comment code. So case 3/4 ("closed" fixture) fails `receipt-validate-mid-finding`, and 5 token-only cases fail their "no extra open defect" assertion because R17-PINMAP stays open in the fixture. The six token-only fixtures do individually stay open (the row's headline mechanism is real), but the cited observable "CLEAN 17" is not reproducible from the audited revision. [Inference] The fixture was written before the L1 check amendment and never updated — the exact fixture/check drift class row 6 claims to have fixed.

### F2 (minor — row 1 evidence anchor stale at REV)
`corpus/lessons/round-18.md:62` cites "`carrier-run.py:475` even tagged '(QUALITY #19)'". At REV the tag is at `.ufo/waves/round-17/tools/carrier-run.py:482` (and a second mention at `:496`); line 475 is `poller.scan()` inside the timeout loop. The pointer is correct against the baseline blob (`git show 9011581…:…/carrier-run.py` → tag at `:475`) and drifted when eb6c2668 added the mid-map retention code above it. Resolves in substance, not at the stated line.

### F3 (info — concurrent worktree mutation during this audit)
Mid-audit, the lane worktree moved from byte-identical-to-REV to 5 modified tracked files (uncommitted): `.ufo/gates/custody-pair/custody-pair.py`, `.ufo/waves/round-17/verify.py`, `.ufo/waves/round-18/tools/routed-defects.py`, `.ufo/waves/round-18/verify.py`, `SKILL.md`. The `routed-defects.py` delta (4+/3−) is exactly the F1 fixture fix (`mid_map_mismatch` → the two real finding ids, at diff hunks `@@ -911,9 +911,10 @@` and `@@ -1142,7 +1143,7 @@`); with it applied `--selftest` prints `SELFTEST: CLEAN cases=17` exit 0. I did not make this edit and made no lane edits. Consequence: F1's fix exists only uncommitted, post-REV — the audited revision still fails its own row-6 reproducer. HEAD remains b2aad08; `corpus/lessons/round-18.md` itself is unmodified.

### F4 (info — misroot re-run differs from wave-1-close claim)
The lessons file's misroot sweep is time-scoped ("at wave-1 close") and says "re-run before the report". Current re-run: `git -C /home/vgpnk/Projects/shokunin status --porcelain | grep -iE 'kaidoku|round-18'` → `?? .ufo/state/kaidoku.report-baseline`. [Observation] one fleet-level untracked file now matches; [inference] plausibly created by this wave's report-baseline machinery, so the wave-1 claim is not falsified, but the current state no longer matches the sweep's "no untracked file naming kaidoku".

## Residual risk and verification gaps
- `jj-red-before.py` not re-run (it builds a jj sandbox; jj availability and runtime cost unverified here). Its receipt at REV (`.ufo/waves/round-18/evidence/jj-red-before.json`) declares `all_held: true`, 14 expectations, `not_runnable: []` — checked by reading, not by execution.
- Rows 2/3/4/5 cite their evidence by routed defect id rather than inline path:line; resolution goes through `round-17-verifier-spotcheck.md:137-147` (verified present) plus the defect section's own anchors (`SCORECARD.md:2364`, `corpus/lessons/round-17.md:88,122` — verified). Acceptable, but a row-level anchor would be sturdier.
- `receipt-validate.py` validation proves digests of bytes present now (its own recorded limitation); I did not re-derive r17 pass-1 history beyond what the tools check.
- All red runs use the REV tool against the baseline rev via `--rev` (the tool reads `git show REV:path` only), so "the fix as the only delta" holds as a rev delta; no second worktree checkout was needed.
- Tool installs: none (no new tools needed; pacman untouched).
