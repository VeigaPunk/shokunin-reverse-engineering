# CriticC3Rule-3 — falsification of the frozen C3 decision rule (freeze `a1140e7`)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (`$LANE`). All paths below relative to `$LANE`.
Target: attack the frozen C3 rule at `a1140e7` against the observed run outcome
("vet 13902080 H1-only, compare 1, seven silent"), test mechanism overfit after prescan,
verify freeze-before-runs and absence of hindsight edits.

## Verdict (one line)

**Not overfit and not hindsight-edited — but the "confirmed" mechanism verdict is the weakest,
pre-registered-but-loose clause, and it coexists with a per-label compare MISMATCH on the only
discriminating carrier.** The attack does not overturn the claim; it lowers its credit on
calibration (verdict-vs-mismatch duality, post-run amendment with a self-inconsistent
timestamp) and depth (the H1/H0 discrimination rests on exactly one index value on one of
eight carriers).

## Timeline (observation — all commit/log timestamps local -0300)

| event | time | evidence |
|---|---|---|
| baseline + emulator prescan committed | 15:37:18 | `85589ac` "…baseline census and emulator prescan" |
| superseded draft commit `2bbbf2cd` (same parent, same second, empty subject; NOT on main) | 15:57:44 | `merge-base --is-ancestor 2bbbf2cd main` → **NOT on main** (exit 1) |
| freeze commit `a1140e7` on main: predictions, decision rule, runner "(pre-run)" | 15:57:44 | `git show a1140e7` name-status lists all `predictions/*` as `A` |
| carrier runs 15:57:51 → 16:07:07 | runs | `runs/run-log.txt` first/last lines; vet window 16:06:14–16:07:07, `compare=1` |
| run evidence + claims amendment committed | 16:09:17 | `4f6c73f` (contains `runs/`, and the `claims.json` `amendments` block per `git log -S amendments`) |
| wave-2 records | 16:10:41, 16:15:31 | `5e364bd`, `d0690fd` (main tip) |

Freeze precedes every analyze: runs started 7 s after the freeze commit.
`runs/` is tracked (`git ls-files` → 144 paths) and was committed at 16:09:17, after the runs — correct direction.

## Freeze integrity (observation)

`git rev-parse` on the `predictions/` tree and on the two rule files gives identical object
hashes at `a1140e7`, `2bbbf2cd`, and `main` (`d0690fd`):

- `predictions/` tree = `fab2abdb47a4d1e59b11c7e1a851a1e50221d115` at all three revs.
- `predictions/t1250-vet.prediction.json` = `10f49dba…`, `predictions/decision-rule.json` = `09899450…`, identical at freeze and main.
- `git diff a1140e7 -- .ufo/waves/round-19/predictions` (worktree) → empty.
- `git status --porcelain -- .ufo/waves/round-19` → only `wave2-registration.json`, `wave2-registry.json` modified and untracked `w2/`; predictions/runs clean.

→ The prediction blobs and the decision rule are byte-identical to the freeze. **No hindsight
edit to the rule or predictions is detectable.** The binding gate ("prediction blob unchanged
from the freeze commit", `decision-rule.json:3`) is satisfied.

## Per-carrier outcome (observation)

`for d in runs/t1250-*; compare.json + observation.json` summary — exits from `*.exit` files:

| label | compare all_match | compare.exit | analyzer_errors | invalid_index_reads | eof |
|---|---|---|---|---|---|
| asm, cgo, compile, cover, go, gofmt, preprofile | true | 0 | [] | [] | [] |
| vet | **false** | **1** | `["Go analysis failure …InvocationTargetException"]` | `[13902080]` | [] |

So "compare 1" = vet's `compare.exit` = 1 with `all_match: false`; "seven silent" = 7 non-D
labels fully clean; `t1250-link` excluded pre-freeze (no Go build info, `decision-rule.json:10-18`).

## Mechanism verdict under the frozen rule (inference from frozen text + observed log)

`decision-rule.json:5` — `confirmed` requires (a) ≥1 observed Invalid index ∈
`h1_only_invalid_indexes` {13902080, 852107777} (`:21-26`), (b) no observed index outside the
frozen H1 list {13902080, 852107777, 1801722468838924630}, (c) all non-D silent.

Observed: vet's bound `ghidra.log` line 229 `Caused by: java.io.EOFException: Invalid index: 13902080`
(stack through `MemoryByteProvider.ensureBounds`, `:229-232`) → (a) yes, 13902080 ∈ H1-only;
(b) the sole observed index is in-list; (c) seven labels silent.
→ `confirmed` per the frozen text. `h0_consistent` (`:20`) does NOT apply: the shared walk
index 1801722468838924630 was never observed. `refuted` (`:28`) does not apply.

Binding checks (observation):
- carrier sha256 `9b9d776e…3bf7` == `receipt.json` sha256_pre/post == `prediction.json` carrier sha256 (all identical).
- bound log sha256 `a5de7622…9c2` == `observation.json:log_sha256`; log path under `runs/t1250-vet/logs/`.
- `evidence/receipt-validation/t1250-vet.json`: `valid: 1, invalid: 0, exit: 0, require_mid_maps: true` → binding gate's receipt-validate clause passes.

## Attack 1 — is the mechanism "confirmed" an overfit artifact? NO, but it is the weakest clause

The index sets are prescan-derived: `evidence/prescan/kr19-sm-vet.json:2677-2681`
`predicted_invalid_index_reads_h1 = [13902080, 852107777, 1801722468838924630]`,
`:2674-2676` `_h0 = [1801722468838924630]` — produced by the **unchanged** round-18 emulator
(`main:.ufo/waves/round-18/tools/swiss-misread.py` sha256 `14924bd6…60` == the sha pinned in
`predictions/t1250-vet.prediction.json:19`; the file's last touching commit is `eb6c266`,
round-18 freeze). The map-path H1-only subset {13902080, 852107777} was re-derived on this
held-out artifact, not tuned.

Why `confirmed` still discriminates: under H0 vet must fail at 1801722468838924630 (the only
H0 index); the real run failed at 13902080, which H0 never predicts. The observation partitions
the two hypotheses exactly as designed. **Overfit of the rule to the observation is ruled out
by the timeline** (rule byte-frozen 9 min before vet's log was written) and by blob equality.

Residual weakness (depth axis, fixable characterization, not a falsification):
- Ghidra halts on the first failure, so 2 of the 3 predicted H1 indices are structurally
  unobservable. The effective test is "first failure index ∈ H1-only set" — an N=1 draw. The
  `confirmed` clause's "at least one" quantifier (`decision-rule.json:5`) is the right
  semantics for a halting analyzer, but it means one index value carries the whole
  mechanism confirmation for the whole cohort.
- `D = {t1250-vet}` is a single diagnostic carrier; seven correct silent predictions support
  coverage, not discrimination. The H1-vs-H0 evidence is exactly one number: 13902080.

## Attack 2 — "compare 1" is a real per-label miss, correctly reported

`runs/t1250-vet/compare.json:51-60` records `extra.invalid_index_reads` **match: false**
(observed `[13902080]` vs predicted `[13902080, 852107777, 1801722468838924630]`),
`all_match: false` (`:2`), exit 1. The claim's falsifiable wording
("match or not is reported per label", `claims.json:27`) and `measure.py` (which copies
`all_match` without re-deriving — `measure.py:95-97`) report this honestly: C3 lands 8/8
bound labels but 7/8 matched. No laundering found — but any summary that quotes "confirmed"
without "vet compare MISMATCH (2/3 predicted indices unobserved)" overstates the result.
Smallest correction: quote both numbers together; the judge should treat the C3 mechanism
verdict as confirmed-with-1-mismatch, not clean-8/8.

## Attack 3 — claims.json amendment: post-run edit, self-inconsistent timestamp (finding)

The `amendments` block (`claims.json:34-42`) was added by `4f6c73f` at **16:09:17 — after
the last run finished 16:07:07** — yet its own `"at"` field reads **"2026-10-20T16:20:00-03:00"**,
10 min in the future of the commit that contains it. Observed via
`git log -S 'amendments' main -- claims.json` → only `4f6c73f` matches.

Assessment: the amendment text faithfully restates the frozen rule (verified clause-by-clause
against `decision-rule.json`: same D set, same {13902080, 852107777}, same 1801722468838924630
h0_consistent clause — which already exists at `decision-rule.json:20`, predating the runs),
so it is NOT a hindsight rule change. But it was drafted **with run knowledge** and carries a
timestamp that cannot be its commit-side author time. Calibration nit: the parenthetical
"before any after-revision measurement" is true for measurements, yet the restatement itself
was integrated post-observation. Smallest correction: an appendix note recording that the
amendment text was committed at 16:09:17 after the 16:07:07 run end, and that `decision-rule.json`
(not the amendment) is the operative frozen authority — which the binding gate already enforces.

## Minor graph observation

`2bbbf2cd` (empty subject, same parent `85589ac`, same second 15:57:44) is a superseded draft
sibling of `a1140e7`, unreachable from main (`merge-base --is-ancestor` exit 1). Its
`predictions/` tree is byte-identical to the freeze (`fab2abdb…` above) — no competing rule
content exists anywhere reachable.

## Commands and exits (verbatim)

- `git log --all --format='%H %ci %d %s' -- .ufo/waves/round-19/predictions` → a1140e7, 2bbbf2cd (exit 0)
- `git diff --stat a1140e7 2bbbf2cd -- …/predictions` → empty (exit 0); `git diff a1140e7 -- …/predictions` → empty (exit 0)
- `git status --porcelain -- .ufo/waves/round-19` → `M wave2-registration.json`, `M wave2-registry.json`, `?? w2/` (exit 0)
- `git merge-base --is-ancestor a1140e7 main` → ancestor (exit 0); `…2bbbf2cd refs/heads/main` → exit 1 (not on main)
- `git log -S 'amendments' main -- claims.json` → `4f6c73f` only (exit 0)
- `sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet` → `9b9d776e…3bf7` (exit 0)
- `sha256sum runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log` → `a5de7622…79c2` (exit 0)
- `grep -n 'Invalid index' runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log` → `:229` only (exit 0)
- `sha256sum` of `main:.ufo/waves/round-18/tools/swiss-misread.py` → `14924bd6…5b60` (exit 0)
- per-carrier `compare.exit` read: 7×`0`, vet `1`; aggregate `runs/run-log.txt` "aggregate exit=1" (all reads exit 0)
- `git log main -- .ufo/waves/round-18/tools/swiss-misread.py` → last touch `eb6c266` (round-18 freeze; exit 0)

## Impacted axes

- **calibration**: hit. "Confirmed" must be carried alongside vet's `all_match:false`/exit 1,
  and the amendment's impossible 16:20 timestamp inside a 16:09:17 commit is a provenance
  defect in a document that anchors provenance.
- **depth**: hit. Mechanism discrimination = one observed index on one carrier; the other two
  H1-only indices are unobservable under a halting analyzer. The claim stands, but its
  evidentiary mass is a single integer.
- **freshness**: clean. Every checked provenance value (emulator sha, carrier sha, log sha,
  tree equality, prescan lineage) is current and self-consistent.

## Counterexample strongest available

"Rule overfit after prescan" fails: the frozen text predates the observation by 9 minutes,
its H0/H1 partition is mechanistically derived from the unchanged r18 emulator, and the
observation (13902080 ∈ H1-only, H0 index absent) is a genuine discrimination, not a
set-membership tautology — H0 predicts failure at 1801722468838924630, which did not occur.
The honest defect is thinness (N=1 discriminating observation; 2/3 predicted H1 indices
unobservable; sole-D-carrier cohort), plus a post-run claims.json amendment carrying a
self-inconsistent timestamp. Defect class: **fixable** (report both numbers; annotate the
amendment's real commit time); not grounds for rejection.
