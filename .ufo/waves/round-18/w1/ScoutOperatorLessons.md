# ScoutOperatorLessons — operator lessons + the r12–r16 routed-defect ledger (round 18, W1)

Verdict: **no `corpus/lessons/operator-*.md` exists; two earlier verifier obligations are still open at
`9011581d84527ba34c675f9cf912e54d2e72d470` — both are r12 debts on the r12 C1 knowledge entry.**
The eight numbered routes in r14/r15/r16 are discharged. Read-only: no REA/provider/analyze call, no
Ghidra, no carrier execution, no lane gate executed, no tool installed or updated.

Axes named before measuring:
- **calibration** — does the lane's claim that prior routed items are closed match the bytes at the baseline?
- **operability** — is an open obligation reachable by a later round's tool/check, or is it invisible?
- **depth** — does the actual routed target (entry, registry, filed evidence) change, not just a nearby note?

Labels: `[OBS]` = worktree/Git bytes at the baseline; `[INF]` = inference.

## 1. Operator lesson files

`[OBS]` `ls corpus/lessons/operator-*.md` → `No such file or directory`, exit 2.
`[OBS]` `find corpus/lessons -maxdepth 1 -iname '*operator*'` → empty, exit 0.
No operator-prefixed lesson exists; `corpus/lessons/round-17.md:127` independently records
"No `corpus/lessons/operator-*` file exists."

## 2. What the five spot-checks route

| file | routed items | anchor |
|---|---|---|
| round-12-verifier-spotcheck.md | no `## Routed defects` section; 3 named debts + 1 axis clause in the adjudication | `:17` |
| round-13-verifier-spotcheck.md | none; S017/S018 corrections were made in-round | `corpus/lessons/round-13.md:63-67` |
| round-14-verifier-spotcheck.md | 2 | `:171`, `:172` (section `:169`) |
| round-15-verifier-spotcheck.md | 4 | `:185-188` (section `:181`) |
| round-16-verifier-spotcheck.md | 2 | `:183-184` (section `:179`) |

Twelve obligations checked in total (4 r12 + 8 numbered routes); 10 discharged, 2 open. r12 is the only
file that uses "debt" rather than "routed defect"; because it is that spot-check's sole disposition, its
named obligations are audited here as routed items.

## 3. Open items

### O-1 — r12 C1 entry never received the routed `S###` source row

- Routing: `corpus/lessons/round-12-verifier-spotcheck.md:17` — "Debts carried to round 13: create
  `corpus/SOURCES.md`; **give the C1 entry an `S###` source row**; disclose the unpaired custody legs in
  the entry."
- Target: `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` (30 lines).
- Discharge search:
  - `git log --oneline -S"give the C1 entry an \`S###\` source row" --all -- corpus/SOURCES.md` → empty,
    exit 0.
  - `grep -n 'arc3-r12-go-evidence-id-domain' corpus/SOURCES.md` → no output, exit 1.
  - `grep -c 'arc3-r12' corpus/SOURCES.md` → 0, exit 1.
  - `git log --oneline -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` → `4072ebb` only,
    exit 0 (the entry was never touched again).
  - `grep -nE 'S[0-9]{3}' <entry>` → no output, exit 1: the entry cites no `S###` row at all.
  - Registry at HEAD has 32 rows (`grep -c '^| S0'` → 32); none has a `used-by` cell naming the entry.
- Context: round 13 did create the registry (`5ac7860`, `--diff-filter=A` on `corpus/SOURCES.md`), so one
  of the three r12 debts is genuinely closed. No r13–r17 lesson/LOG records a withdrawal or a different
  discharge of this row.
- Verdict: **OPEN** `[OBS]` no row/used-by exists. `[INF]` the debt was dropped, not discharged; the
  structural census (`sources-census.sh validate`, reported `ok` in the r13–r17 closures) validates row
  shape/tier/status, not whether an admitted knowledge entry is reachable through a row.

### O-2 — r12 C1 entry omits the routed custody-leg disclosure

- Routing: same line, "**disclose the unpaired custody legs in the entry**."
- Checks: `grep -c 'custody' corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` → 0, exit 1;
  the only "receipt" hit (`:25`) is "retained receipt" for a mutation check, unrelated to custody.
  Entry history is still `4072ebb` only.
- Counter-evidence: the facts are disclosed outside the entry — `SCORECARD.md:2086-2088` ("no pre-pair …
  two post-only receipts"), `corpus/lessons/round-12.md:14`, `LOG.md:1710`.
- Verdict: **OPEN against the literal routed target** (the knowledge entry). `[INF]` If "the entry" meant
  the LOG entry, this is closed; the same sentence's antecedent "the C1 entry" makes the knowledge entry
  the natural referent. Confidence medium-high. A reader of the admitted entry alone is not told the live
  legs were unpaired, although no paired-custody claim is made there either.

## 4. Discharge ledger (not open)

| obligation | routing anchor | discharging commit (`git log -S` / `--diff-filter=A`) | current-state anchor |
|---|---|---|---|
| r12 create `SOURCES.md` | `round-12-verifier-spotcheck.md:17` | `5ac7860` | `corpus/SOURCES.md:1` (32 rows) |
| r12 axis add/withdraw | same `:17` | no add commit; `## Owned axes` still lists 3 axes, r12 C3 labelled "(fleet)" | `SCORECARD.md:19-25`, `:2058`; `[INF]` withdrawn by record |
| r14 advisory evidence correction | `round-14-verifier-spotcheck.md:171` | `856d193` | `corpus/lessons/round-14.md:144-166`; `LOG.md:1847-1855` |
| r14 manual-only input boundary | `:172` | `856d193` | `corpus/QUALITY.md:27` ("must not be submitted as machine-gradeable") |
| r15 invocation consistency | `round-15-verifier-spotcheck.md:185` | `27b8fc1` | r15 entry `:76-86`; `SKILL.md:487` exact `python3 -I` absolute argv |
| r15 supplemental baseline discoverability | `:186` | `27b8fc1` | `SKILL.md:450` cites `.ufo/waves/round-15/boundary-fixtures/expected.json` |
| r15 count-command provenance | `:187` | `27b8fc1` (`controls.py`), `2fc1d6f` (`controls.json`) | `controls.json` `invocation.orig_argv` = `python3 -I <abs controls.py> <B> <A>` |
| r15 historical SHONEN wording | `:188` | `27b8fc1` | `SHONEN.md:10` "historical 2026-10-15 operator-steered round 1"; `grep -c 'this round'` → 0, exit 1 |
| r16 R16-PROVENANCE | `round-16-verifier-spotcheck.md:183` | `da64646` | `round-17.md:96-99` 4/4 line-exact corrections; `LOG.md:2059-2062`; fleet `.ufo/reports/round-17/kaidoku.md:53` erratum |
| r16 R16-INVOCATION | `:184` | `da64646` | `SKILL.md:448` isolated absolute argv + probe variant explicitly "unexercised" |

Filed r16 statements remain unqualified in place by design (append-only; `round-16.md:154`,
`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, `LOG.md:2012`, `verification.json:419`);
the r16 route permitted exactly that form of correction. The fleet-report site is corrected only in the
r17 report (`:53`), not by rewriting the filed r16 report.

## 5. Axis read

- **calibration** — the r14–r17 closures are accurate for their own rounds, but the earlier queue was not
  drained: two r12 obligations survived five rounds with no withdrawal record. The r18 C1 claim and
  `.ufo/waves/round-18/contract.md` cover only the six R17 defects (`claims.json` C1; contract C1
  `routed-defects.py`), so the r18 before/after `6 → 0` cannot see these two `[OBS]`.
- **operability** — the open `S###` row has no enforcing check: `sources-census.sh validate` checks the
  registry, and the closure recounts count rows/tiers/status, not entry→row reachability `[INF]`. Adding
  either a row/used-by or a recorded withdrawal is a one-file edit with a testable predicate.
- **depth** — both open items are on the admitted r12 knowledge artifact, not on the surrounding records
  (SCORECARD/LOG already disclose custody). Fixing the entry or the registry is what makes the corpus
  self-describing; a nearby LOG note does not.

Workspace note: at scout start `git status --porcelain` showed only `?? .ufo/waves/round-18/`. By report
close, concurrent round-18 seats had modified `.ufo/gates/citation-drift/citation-drift-probe.py` and
several `.ufo/waves/round-17/tools/*` files (`carrier-run.py`, `compare.py`, `log-extract.py`,
`verify.py`); the set was still changing. None is used as evidence here; this scout wrote only this report.

No tool installs/updates.

## 6. Commands and exit codes (observed)

```text
$ git rev-parse HEAD
9011581d84527ba34c675f9cf912e54d2e72d470
EXIT=0

$ ls corpus/lessons/operator-*.md
ls: cannot access 'corpus/lessons/operator-*.md': No such file or directory
EXIT=2

$ find corpus/lessons -maxdepth 1 -iname '*operator*'
(no output)
EXIT=0

$ grep -n 'arc3-r12-go-evidence-id-domain' corpus/SOURCES.md
(no output)
EXIT=1

$ grep -c 'arc3-r12' corpus/SOURCES.md
0
EXIT=1

$ grep -c 'custody' corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
0
EXIT=1

$ grep -nE 'S[0-9]{3}' corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
(no output)
EXIT=1

$ wc -l corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
30 corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
EXIT=0

$ git log --oneline -S'give the C1 entry an `S###` source row' --all -- corpus/SOURCES.md
(no output)
EXIT=0

$ git log --oneline -S'arc3-r12-go-evidence-id-domain' --all -- corpus/SOURCES.md
(no output)
EXIT=0

$ git log --oneline -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
4072ebb round-12: arc3-loop1-round12 work — inspect_go_binary ev_ entry ...
EXIT=0

$ git log --oneline -S'unpaired custody legs' --all
1170f71 round-12 verifier spot-check (integrator, kaika): non-author admit/reject sample + adjudication
EXIT=0

$ git log --oneline -S'custody' -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md
(no output)
EXIT=0

$ grep -c '^| S0' corpus/SOURCES.md
32
EXIT=0

# discharge pickaxes — each printed one commit (or the stated result), EXIT=0
$ git log --oneline --diff-filter=A -- corpus/SOURCES.md
5ac7860 kaidoku-shokunin: arc3-loop1-round13 source registry
$ git log --oneline -S'Round-15 correction — virtual-dispatch advisory' -- corpus/lessons/round-14.md
856d193 round-15: pin Go snapshot selection and close review defects
$ git log --oneline -S'Named correction — virtual-dispatch advisory' -- LOG.md
856d193 ...
$ git log --oneline -S'Supersedes #16' -- corpus/QUALITY.md
856d193 ...
$ git log --oneline -S'Round-16 correction — r15 recheck invocation' -- corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md
27b8fc1 round-16: source-model selection and outside-route provenance
$ git log --oneline -S'.ufo/waves/round-15/boundary-fixtures/expected.json' -- SKILL.md
27b8fc1 ...
$ git log --oneline -S'historical 2026-10-15 operator-steered round 1' -- SHONEN.md
27b8fc1 ...
$ git log --oneline --diff-filter=A -- .ufo/waves/round-16/controls.py
27b8fc1 ...
$ git log --oneline --diff-filter=A -- .ufo/waves/round-16/controls.json
2fc1d6f round-16: measured evidence and calibrated verdicts
$ git log --oneline -S'unexercised variant' -- SKILL.md
da64646 round-17: carrier runs, integrated tools, corpus and registry corrections (pre-falsify)
$ git log --oneline -S'R16-PROVENANCE:' -- corpus/lessons/round-17.md
da64646 ...
$ git log --oneline -S'R16-PROVENANCE:' -- LOG.md
da64646 ...
```
