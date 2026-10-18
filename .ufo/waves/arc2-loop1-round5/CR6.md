# CR6 — critic: separability attack (arc2-loop1-round5)

## Verdict

**CONDITIONAL COUPLING: C2 and C3 name the same 60/64 dispatch-defect debt. Separability is not established unless the register explicitly prevents one protocol lesson from being counted as two independent moves. C1 can be independently re-derived when each measurement is pinned to its cited commit; one R4 freshness measurement passed that test, but this does not complete the four-round audit.**

## Evidence — commands run and observed output

### C2's cross-round input is also R4's carried-debt item

I queried each cited SCORECARD commit, rather than treating the current summary as a re-derivation:

```console
$ python3 - <<'PY'
import re, subprocess
for rev in ['679af5d','158a966','0e8c96b']:
    text=subprocess.run(['git','show',f'{rev}:SCORECARD.md'],check=True,text=True,capture_output=True).stdout
    hits=[(n,line.strip()) for n,line in enumerate(text.splitlines(),1) if re.search(r'60 reports delivered|60 seat reports|60/64|4 non-completions',line,re.I)]
    print(f'{rev}: {len(hits)} matching lines')
    for n,line in hits: print(f'  {n}: {line}')
PY
679af5d: 2 matching lines
  710: - Wave: 64 seats dispatched on `devin/deepseek-v4-1-flash-max`; 60 seat reports
  711: delivered (4 non-completions recorded as a dispatch defect; every claim
158a966: 3 matching lines
  710: - Wave: 64 seats dispatched on `devin/deepseek-v4-1-flash-max`; 60 seat reports
  711: delivered (4 non-completions recorded as a dispatch defect; every claim
  774: seats dispatched, 60 reports delivered (4 non-completions, second consecutive
0e8c96b: 6 matching lines
  710: - Wave: 64 seats dispatched on `devin/deepseek-v4-1-flash-max`; 60 seat reports
  711: delivered (4 non-completions recorded as a dispatch defect; every claim
  774: seats dispatched, 60 reports delivered (4 non-completions, second consecutive
  859: admitted.** Parent-integrated; 64 seats dispatched, 60 reports delivered
  860: (4 non-completions, third consecutive — the dispatch defect class is now
  923: rubric.json:61` same class; the 60/64 dispatch defect class (3 rounds
```

These queried objects are the R2/R3/R4 record revisions. The underlying citations resolve at `SCORECARD.md:710-712` (R2), `:774-775` (R3), and `:859-861` / `:923-925` (R4). R2–R4 state one consecutive 60/64 class; R4 explicitly carries it as debt. The second R4 record also names an existing missed item, rubric citation drift, in the same carried-debt list (`SCORECARD.md:920-925`). The round-5 C2 target is the dispatch class; C3's stated R1–R4 register necessarily encounters that already-carried R4 item unless its scope says otherwise.

### C1 archive discipline / one C3 counterfactual

I materialized the exact work and record commits using the instructed archive method, then ran the read-only v10 instrument against both trees:

```console
$ mkdir -p /var/tmp/arc2-l5r5-CR6-265e1aa /var/tmp/arc2-l5r5-CR6-0e8c96b && git archive 265e1aa | tar -x -C /var/tmp/arc2-l5r5-CR6-265e1aa && git archive 0e8c96b | tar -x -C /var/tmp/arc2-l5r5-CR6-0e8c96b
$ python3 /var/tmp/arc2-l5r5-CR6-265e1aa/.ufo/gates/c1-census-v10.py --root /var/tmp/arc2-l5r5-CR6-265e1aa --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=854  loci=9
SKILL.md       lines=348  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
$ python3 /var/tmp/arc2-l5r5-CR6-0e8c96b/.ufo/gates/c1-census-v10.py --root /var/tmp/arc2-l5r5-CR6-0e8c96b --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=933  loci=9
SKILL.md       lines=348  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

The first result re-derives R4's cited v10 PASS at `265e1aa` (also recorded at `SCORECARD.md:880-888`); the second is a read-only current-tree comparison at `0e8c96b`. Same verdict/counters despite the appended R4 record (SCORECARD 854→933 lines) shows this one metric can be audited from an immutable cited tree without relying on C3's current register. It is not a re-derivation of every R1–R4 claim.

The instrument prints only live pin versions; its source says it re-derives anchors from client config files (`.ufo/gates/c1-census-v10.py:20-23,124-134`). No REA/MCP session or write was performed. This was a read-only instrument run, not evidence of config custody.

Other resolving pointers: R4 assigns the same axes to C2 operability and C3 freshness at `SCORECARD.md:872-893,905-907`; R4's earlier CR6 measured edit-level interactions among C1/C2/C3 (`.ufo/waves/arc2-loop1-round4/CR6.md:20-38`). Those are prior-round findings, not proof of a round-5 interaction.

## Text for the parent — VERBATIM

```text
CR6 separability ruling (arc2-loop1-round5): C2×C3 overlap on the same named debt unless the register makes ownership explicit. I re-read the cited SCORECARD trees: 679af5d records 64 dispatched / 60 reports / 4 non-completions; 158a966 records the second consecutive 60/64; 0e8c96b records the third and carries “the 60/64 dispatch defect class” as debt (SCORECARD.md:710-712, 774-775, 859-861, 923-925). C2's required corpus lesson is the natural safe landing for that exact item. If C3 classifies it landable-now, do not count the same lesson as two independent moves; either C2 owns the lesson and C3 records the disposition without counting its landing, or record the C2/C3 coupling. If C3 instead marks it named-debt/operator-owned, state the evidence and reason; do not silently omit it from the R1-R4 register.

C1's historical audit can be tested independently only at the cited immutable revision for each measurement. As a spot-check, I archived and ran v10 at 265e1aa: PASS 0/0/0/0, matching the R4 C3 claim; at 0e8c96b it remains PASS 0/0/0/0. This supports archive-pinned re-derivation for this one metric, not completion of the full R1-R4 audit. Keep C1's audit findings/dispositions distinct from C3's register/landing count; report any item that legitimately serves both rather than counting its evidence twice.
```

## Conclusions (labeled)

- **Observation:** The three cited SCORECARD trees contain the successive 60/64 reports; R4 labels the repeated class as carried debt. My archive-based v10 rerun at `265e1aa` passes with counters 0/0/0/0; the rerun at `0e8c96b` also passes with 0/0/0/0.
- **Inference:** The R4 dispatch item is in the natural subject matter of C3's R1–R4 missed-item register and is exactly C2's stated target. If its disposition is landable-now and C2's protocol is the landing, one artifact/action cannot substantiate two distinct moves without explicit ownership accounting. This is the strongest separability attack; shared evidence alone does not prove coupling.
- **Inference:** C1's commit-pinned audit and C3's current register need not be coupled: the one tested census result survives the appended record. R4 CR6 also documented that same-round edits can couple claim instruments (`.ufo/waves/arc2-loop1-round4/CR6.md:20-38`), so C1 must keep each historical run tied to the exact cited tree rather than re-run every old claim against HEAD.
- **Unknown:** The actual R5 register's membership/disposition for the 60/64 item and whether C2's lesson is counted among C3's “safe landings”; whether the full C1 inventory has a commit and instrument identified for every historical measurement; whether other R1–R4 carried items overlap the C2 lesson.
- **Scope:** No tracked repository files changed by this seat; no git mutation, config write, install, network access, or REA/MCP session. Archive/scratch paths are `/var/tmp/arc2-l5r5-CR6-*`; the only intended repo write is this report.
