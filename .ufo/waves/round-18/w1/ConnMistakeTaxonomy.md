# ConnMistakeTaxonomy — kaidoku r14–r17 `## Mistakes` vs the kaika taxonomy

Seat: connector (author-side advisory), round 18. Read-only; the only write is this file.
No `jj`; read-only git only. No REA/Ghidra/analyzeHeadless, no carrier execution. No installs.
`LANE` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; `B` = `9011581d84527ba34c675f9cf912e54d2e72d470`
(`refs/heads/main`). Fleet files are cited as `ufo:` = `/home/vgpnk/Projects/shokunin`.

**Question.** Map this lane's recurring mistake classes across the r14–r17 lessons onto the 13
kaika classes (`ufo:.ufo/waves/kaika-w1/mistakes.md:70-97`) and identify which classes recur
*after* capture, i.e. where the fix is not shown able to fail (L1, `:412-418`; command appendix,
`:513`).

Legend: **O** = observation (read/run here), **I** = inference. `red?` = the fix names a state in
which its own check exits non-clean for the named reason. `—` = none named. `partial` = a red
exists but on a different surface/artifact than the recurrence.

---

## 1. Command ledger (pasted with exits)

`grep -n '^| ' corpus/lessons/round-1[4-7].md` → **exit 0**; Mistakes rows at
`round-14.md:74-78`, `round-15.md:64-70`, `round-16.md:54-59`, `round-17.md:81-92`.

`for f in round-1[4-7].md; do … awk '/^## Mistakes/…' $f; done` → **exit 0**; header-inclusive
table lines 6 / 8 / 7 / 13, minus one header row each = **5 / 7 / 6 / 12 = 30 rows**.

`grep -c 'Able to fail' corpus/lessons/round-1[4-7].md` → **exit 0**; `round-14.md 0`,
`round-15.md 0`, `round-16.md 0`, `round-17.md 10` (rows 81–90; rows 91 provider and 92 scope
carry none).

```bash
python3 - <<'PY'   # C2 lint rule over its own scan roots at B; exit 0
import subprocess, ast, re
R="9011581d84527ba34c675f9cf912e54d2e72d470"
pat=re.compile(r'rev-parse[^\n]*HEAD|default="HEAD"|\'HEAD\'|symbolic-ref|--abbrev-ref|--show-current|"HEAD:"')
names=subprocess.run(["git","ls-tree","-r","--name-only",R],capture_output=True,text=True).stdout.split()
scope=[f for f in names if re.match(r'^\.ufo/(gates|rounds)/|^\.ufo/waves/round-1[4-8]/',f) and f.endswith(('.py','.sh'))]
live=fix=0
for f in scope:
    src=subprocess.run(["git","show",f"{R}:{f}"],capture_output=True,text=True).stdout
    hit=[i+1 for i,l in enumerate(src.splitlines()) if pat.search(l)]
    if not hit: continue
    fs=[]
    if f.endswith('.py'):
        try: fs=[(n.name,n.lineno,n.end_lineno) for n in ast.walk(ast.parse(src)) if isinstance(n,ast.FunctionDef)]
        except SyntaxError: pass
    for ln in hit:
        enc=[n for n in fs if n[1]<=ln<=n[2]]; enc.sort(key=lambda t:t[2]-t[1])
        fn=enc[0][0] if enc else "<module>"
        ctx="fixture" if f.endswith('.py') and re.search(r'selftest|fixture',fn,re.I) else "live"
        live+=ctx=="live"; fix+=ctx!="live"
        print(ctx, f"{f}:{ln}", fn)
print("LIVE",live,"FIXTURE",fix)
PY
```
→ **exit 0**; `LIVE 7 FIXTURE 6` at
`citation-drift-probe.py:477`, `custody-pair.py:327`, `round-17/controls.py:442` (`_commit`),
`round-17/verify.py:59`, `round-17/w2/audit-attack.py:91` (`build_repo`),
`round-17/w2/temporal-attack/fixtures/rebuild.sh:9,11`.

```bash
python3 - <<'PY'   # R17-PINMAP substance at B; exit 0
import subprocess, json
R="9011581d84527ba34c675f9cf912e54d2e72d470"
paths=subprocess.run(["git","ls-tree","-r","--name-only",R],capture_output=True,text=True).stdout.split()
rc=[p for p in paths if p.startswith(".ufo/waves/round-17/runs/") and p.endswith("/receipt.json")]
n=0; keys=set(); ms=0
for p in rc:
    d=json.loads(subprocess.run(["git","show",f"{R}:{p}"],capture_output=True,text=True).stdout)
    pc=d.get("steps",{}).get("analyze",{}).get("pin_checks",[])
    n+=len(pc)
    for c in pc: keys|=set(c)
    ms+=json.dumps(d).count("map_sha256")
print("receipts",len(rc),"mid_checks",n,"union_keys",sorted(keys),"map_sha256",ms,
      "pins_dirs",sum(1 for p in paths if p.startswith(".ufo/waves/round-17/runs/") and "/pins/" in p))
PY
```
→ **exit 0**; `receipts 8 mid_checks 29 union_keys ['changed','entries','equal','missing','taken_at_utc'] map_sha256 0 pins_dirs 0`.

`git show B:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -c 'comparator verdict'`
→ `0`, **exit 1** (no match). `git show B:.ufo/waves/round-17/tools/carrier-run.py | grep -c map_sha256`
→ `0`, **exit 1**. `git show B:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c carriers.tsv`
→ `0`, **exit 1**. `git show B:corpus/QUALITY.md | grep -c R17-PINMAP` → `0`, **exit 1**.
`git rev-parse --verify refs/heads/main` → `9011581…`, **exit 0**.
`git status --porcelain` → 3 lines (`M round-17/tools/compare.py`, `M round-17/verify.py`,
`?? .ufo/waves/round-18/`), **exit 0** — wave-1 work in flight.

---

## 2. Row ledger — 30 rows, primary class, capture, red, recurrence

| row | lane class | kaika | capture | red? | next recurrence |
|---|---|---|---|---|---|
| `round-14.md:74` | quote-splice / attribution | C01 | SOURCES v1 r1 + non-author re-open | yes (`round-14.md:109-112`) | `r15:70`, `r16:54-55`, `r17:82` |
| `round-14.md:75` | reference-drift | C01 | CORPUS quote-location; outside | yes (`:111-112`) | same |
| `round-14.md:76` | causal-overreach | C03 | QUALITY #5 (missed at write time) | — | `r15:64`, `r17:84` |
| `round-14.md:77` | scope / instrument | C03 (+C08) | domain boundary; QUALITY #16 | — | `r15:65` — #17 supersedes #16 |
| `round-14.md:78` | edit-anchor | C10 | hashline guard | partial: rejected once, but `r15:66` shows warn-and-accept | `r15:66` |
| `round-15.md:64` | “provider” (dispatch chain) | C03 | QUALITY #1/#5; outside trace | — | — |
| `round-15.md:65` | scope / representation | C03+C08 | outside check | yes (rendered/raw pair) | — |
| `round-15.md:66` | edit-anchor | C10 | “tool policy should have refused” | — | — |
| `round-15.md:67` | landing / premature used-by | C09 | CORPUS existence | partial (census) | `r17:85` |
| `round-15.md:68` | number-drift / survivor | C02+C07 | CORPUS count-command; cross-check | partial (123 vs 98/114) | `r16:56` |
| `round-15.md:69` | unexecuted static review | C04 | none | yes (retained traceback) | — |
| `round-15.md:70` | reference-drift | C01 | registered citation strict | yes (exit 1, named code) | `r16:54-55`, `r17:82` |
| `round-16.md:54` | ref-drift / invocation | C01 | QUALITY #18; outside | — | `r17:82` |
| `round-16.md:55` | ref-drift / registry | C01 | Gate registry discoverability | — | — |
| `round-16.md:56` | number-drift / provenance | C02 | CORPUS count-command | partial (argv retained, no red) | `r17:89` |
| `round-16.md:57` | stale-premise | C06 | SHONEN historical discipline | — | `r17:84` |
| `round-16.md:58` | vacuous / marker sufficiency | C04 | author-side critic | yes (`documentation-red`, 0/4) | `r17:81/86/88/90` |
| `round-16.md:59` | provider (402 credits) | C13 | host | n/a | `r17:91` |
| `round-17.md:81` | vacuous/number — R16-PROVENANCE | C04+C02 | none (#18 needs producer, not instants) | yes | `r17:90` same round; R17-PINMAP routed |
| `round-17.md:82` | survivor/ref-drift — R16-INVOCATION | C07+C01 | QUALITY #18 | yes (baseline 2 variants) | in-round 2→11, final 0/17 |
| `round-17.md:83` | scope — contract undercount | C03 | author critics | yes (selftest 2, 3, 3b) | — |
| `round-17.md:84` | stale-premise — contract law | C06 | author review | yes (Java diff 27→0) | — |
| `round-17.md:85` | landing — `__pycache__` | C09 | none | yes (import without guard) | — |
| `round-17.md:86` | vacuous — non-discriminating field | C04 | none | yes (`compare-route-red`) | — |
| `round-17.md:87` | attribution — unbound logs | C10 | none | yes (fuzz reds) | — |
| `round-17.md:88` | vacuous/survivor — wrong shape | C04+C07 | none (selftest used the wrong artifact) | yes, but fixture-shaped | — |
| `round-17.md:89` | number-drift — commit token | C02 | none | one-off `git rev-parse` only | — |
| `round-17.md:90` | vacuous — R16-PROVENANCE inside r17 | C04+C07 | #18 missed it; #19 added | yes | R17-PINMAP routed |
| `round-17.md:91` | provider — dead seats | C13 | host | n/a | — |
| `round-17.md:92` | scope — routed site list | C03 | outside route vs lane search | **—** | r18 C2 (see §5) |

Primary totals: C01 6 · C03 6 · C04 6 · C02 3 · C10 3 · C06 2 · C09 2 · C13 2 · C07 0 primary
(3 dual) · C08 0 primary (2 dual). C05, C11, C12: none in `## Mistakes` (C05 is handled in
`round-16.md:24` as a Gate decision; every round ships an outside `*-verifier-spotcheck.md`).

The lane's `provider` label covers three different mechanisms: source-call-chain overreach
(`round-15.md:64`), unexecuted verification (`round-15.md:69`), and host/provider aborts
(`round-16.md:59`, `round-17.md:91`). I mapped by mechanism, which is why C13 holds only two of the
four `provider`-labelled rows; a class word that does not discriminate cannot be counted or learned.

---

## 3. Answer — which classes recur after capture

**Every captured class recurs in this window** — C01, C02, C03, C04, C06, C09, C10 all have a
later-round instance. The discriminating question is therefore narrower: **six of the seven recur
on a surface where the capturing fix is not shown able to fail — C01, C02, C03, C04, C06, C10.**
C09 is the one exception: the class moved (registry reference → gitignored `__pycache__`), but the
r17 fix is a real filesystem gate with a demonstrated re-creation (`round-17.md:85`) and the r15
capture's path-existence census can fail for its own surface. C07 and C08 recur with **no capture
at all**; C05 has no `## Mistakes` rows (Gate decision, `round-16.md:24`).

Red coverage: **10/30** rows name a fail-arm — 0/5 (r14), 0/7 (r15), 0/6 (r16), 10/12 (r17)
(`grep -c 'Able to fail'`, §1). The vocabulary arrives only in r17, and six defects were still
routed against that round's outputs (`round-17-verifier-spotcheck.md:137-147`): ten fail-arms did
not cover the surfaces the claims landed on.

| class | captured | post-capture rows | verdict |
|---|---|---|---|
| C01 reference drift | r14 (`round-14.md:74-75`) | r15:70, r16:54, r16:55, r17:82 | **recurs; red mis-scoped** — the red/fixed pair parses quote manifests; every recurrence is a registry/SKILL/invocation pointer |
| C02 number drift | r15 (`round-15.md:68`) | r16:56, r17:89 (+81 dual) | **recurs; no standing red** — r17:89's “able to fail” is a one-off `git rev-parse`, no tool runs it |
| C03 scope | r14 (`round-14.md:76-77`) | r15:65, r17:83, r17:92 | **recurs; one capture was itself wrong** (#16→#17) and the last row has no red |
| C04 vacuous verification | r16 (`round-16.md:58`) | r17:81, 86, 88, 90 | **recurs most (4 in one round); reds are fixture-shaped** |
| C10 attribution / edit anchor | r14 (`round-14.md:78`) | r15:66 | **recurs; guard is advisory** (warn, not refusal) |
| C07 unbounded closure | never | r17:82, 88, 90 (dual) | unowned: “survivor” labels three different mechanisms |
| C08 fix-induced regression | never | r15:65 (correction of a correction), r17:82 (2→11 mid-round) | unowned: no red for corrections-of-corrections |
| C06 stale premise | r16:57 | r17:84 | **recurs; r16 fix had no red.** r17:84's Java differential (27→0) is a real but local fail-arm for the parsing law, not a premise-freshness gate |
| C09 evidence landing | r15:67 | r17:85 | **recurs on a new surface** (registry ref → gitignored `__pycache__`); both fixes carry real fail-arms (path census; `__pycache__` gate) — migration, not vacuity |
| C13 operational abort | by design no gate | r16:59, r17:91 | host, not unlearned science |

### Mechanisms (O/I)

1. **Surface migration (C01/C03).** The instrument's parse surface is narrower than the claim
   surface. r14 instrument: manifests (`round-14.md:109-112`). r16 recurrences: registry rows
   (`round-16.md:54-55`). r17 recurrence: SKILL rows plus a *receipt* the audit accepts if any
   JSON array is named `argv` (`.ufo/waves/round-17/w2/CriticC1Admission.md:48-68`). Each fix makes
   the old surface green and leaves the next one unobserved.
2. **Number copied from prose, not measured (C02/C03).** r17:92 already states the rule (“Sites are
   found by search at the pinned baseline, not copied from a prose list”). Round 18's C2 repeats
   it — see §5.
3. **Fixture ≠ producer artifact (C04).** `round-17.md:88`: the validator's selftest passed on a
   *list* fixture while the producer emits an *object* shape; all 8 real receipts were rejected
   (`unrecognized_shape`). A negative control green on the wrong shape is itself a vacuous
   verification.
4. **Red = fix absent, not defect present (C04/C07/C08).** Round 18's C1 selftest builds “one
   commit where all six are open … a second where all six are closed”
   (`.ufo/waves/round-18/contract.md:46`): that proves the checker sees marker text, not that the
   defect is remedied.
5. **Advisory guard instead of fail-closed gate (C10).** `round-14.md:78` says the hashline guard
   “prevented an unanchored edit”; `round-15.md:66` records the same tool accepting a stale tag
   with a warning. The capture was a process rule, not a refusal.

---

## 4. Round-18 pre-registered recurrences (O, then I)

**(a) C1 can close by markers.** All four R17-PINMAP predicates are substring presence:
`R17-PINMAP`+`comparator verdict` in the entry (`contract.md:29-30`), the same in `SCORECARD.md`
(`:30`), `round-17-verifier-spotcheck.md`+`R17-PINMAP` in a QUALITY why-cell (`:30-31`), and the
literal `map_sha256` in `carrier-run.py` (`:32`). At `B` the substantive defect is fully present:
8 receipts, 29 mid checks whose union key set is `{changed, entries, equal, missing, taken_at_utc}`,
zero `map_sha256`, zero `pins/` directories (§1). **I:** adding four lines and one literal yields
`open_count 0` whether or not the correction's content is true of the artifacts: the predicate reads
the marker, not the claim. (Append-only keeps the false original sentence at entry lines 28–33; only
the appended correction carries the truth.) The selftest (`contract.md:46`) cannot expose this: its
red commit is baseline-shaped, not defect-replay.

**(b) C2's before-number contradicts its own rule.** `claims.json:20` says “live HEAD-as-revision
call sites **3** at 9011581 -> 0”. Applying the contract's site definition (`contract.md:61-70`) to
its own scan roots at `B` yields **7** live sites. Excluding only the helper-mediated
`controls.py:442` (`_commit`), the count is **6**: `citation-drift-probe.py:477` (`default-HEAD`),
`custody-pair.py:327`, `verify.py:59`, `audit-attack.py:91`, `rebuild.sh:9`, `rebuild.sh:11`. The
claim's three are a subset of every reading; no reading of the contract's own rule returns 3.
This is `round-17.md:92` recurring in the contract text before any tool exists; if the lint is
written to reproduce “3”, the rule will have been fitted to the number (the r17 F2 pattern,
`CriticC1Admission.md:48-68`).

---

## 5. Proposed move (one, bounded)

**Define C1's red as defect-replay on the lane's real artifacts, copying C2's `jj-red-before.py`
method into `routed-defects.py`.** A check is closed only if it flips open when the defect is
re-introduced into a fixture built from the `REV` artifacts; a check that cannot flip is not a
check. One witness read is required where the current predicates never look — R17-PINMAP:

- closed iff either (i) every `steps.analyze.pin_checks` entry carries `map_sha256` and the named
  `runs/<label>/pins/mid-<n>.json` blob exists at `REV` with that digest, **or** (ii) every key set
  is a subset of the five measured keys **and** the correction line reads “mid-run instants retain
  the comparator verdict against the retained pre map, not the map”;
- replay: from the closed fixture, restore the sentence “each pin map is retained … pre, every
  30 s … and post” while the receipts still lack maps → the check must go open.

Scope: `contract.md` C1 only (predicates + the `:46` selftest sentence). No new tool, no network,
no carrier execution, no write outside `mkdtemp`. The in-flight `w1/DraftPinmapCorrection.md`
already states exactly the artifact-true correction (29 checks, five keys, no map), so predicate
(ii) passes the drafted text; the move adds the false-claim replay, not new lane content.

Affected axes: **calibration ↑** (the six-defect metric becomes artifact-entailed; marker-only
closure blocked); **operability ↔/↑** (same Git-object reads, stdlib only, no runtime);
**depth ↔** (C3 untouched). No axis harmed.

---

## 6. Risks

1. **R17-S032-DIGEST has no local witness** (GitHub HTML is dynamic). Its replay must be a negative
   text predicate: the row may carry the digest only with a fetch-time qualifier; replay restores
   the unqualified claim. Text-based, label the limit.
2. **R17-VALIDATE16's witness is a round-18 artifact authored by this lane** → C05-shaped
   self-attestation. Mitigate by recomputing `len(receipts)` and requiring int `exit`; still
   self-authored.
3. **R17-PRODUCER-REV** has no receipt field proving which `carrier-run.py` bytes produced a pass.
   Strongest feasible predicate: the line carries two distinct 40-hex hashes, both
   `git cat-file -e`-resolvable; replay reverts one to `2716747` (fatal).
4. **C2's count.** Either amend the claim to 7→0 (fix or annotate the extra sites) or write the
   fixture-context rule (helper-mediated calls and `fixtures/` shell scripts) into the contract
   *before* the lint, so the rule is not retro-fitted to “3”.
5. Cost: ~60 lines and 6 replay fixtures; no conflict with in-flight code (`round-18/tools/` holds
   only `revpin.py`; `routed-defects.py` does not exist yet).
6. Closing C1 cannot be blocked by the move: the only newly-read artifact is the receipt set, and
   the drafted correction is already true of it.

---

## 7. Verification (commands and expected outcomes)

1. `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` → `SELFTEST: CLEAN
   cases=14`, exit 0 (8 existing + 6 replay).
2. `… --root LANE --rev 9011581` → `open_count 6`, exit 0; `--strict` exit 1.
3. `… --root LANE --rev <delivered>` → `open_count 0`, exit 0.
4. Six `mkdtemp` clones of the delivered revision, each with one defect re-introduced (PINMAP
   sentence restored; SUMS line removed; `2716747` restored; `Write scope:` removed; `436c0f63`…
   restored unqualified; one hash removed) → per clone `open_count 1` for the named id, `--strict`
   exit 1. Clones removed.
5. `git status --porcelain` in `LANE` unchanged before/after; no `__pycache__` under `.ufo`.

## 8. Limits

Read-only; `routed-defects.py` was not run (it does not exist at `B`). Rows are unique incidents by
primary mechanism; duals are named, not double-counted. Counts are of *recorded* rows, so the
kaika §7 caveat applies unchanged. The critic's anchor `round-17.md:26/:73` no longer resolves at
HEAD (the lesson was revised after `CriticC1Admission.md` was written) — an example of C01/C06 that
is itself outside my row ledger because it is a w2 artifact, not a `## Mistakes` row.

## 9. Host tooling

None installed or updated; no pacman transaction attempted. Python 3 stdlib and read-only `git`
sufficed.

Report: `.ufo/waves/round-18/w1/ConnMistakeTaxonomy.md`
