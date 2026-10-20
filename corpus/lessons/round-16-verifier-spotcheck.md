author: hyaku closure (non-author integrator, @m_strong)

# Round 16 — independent closure and admit/reject spot-check

Date: 2026-10-20. Status **ok**; **admitted** for the bounded C1 depth and C2 calibration claims. No promotion, mint, `[x]`, target-recovery result, Java equivalence or new capability is authorized.

## Revisions and scope

- Baseline B: `6235498b4112350eebce0812a74af1781fc0ee88`.
- Measured source S: `27b8fc13156230981312c44380cddab1f2bd318d`.
- Delivered A: `2fc1d6f355d14a507c95483fa3497b45d5e9a3fd`.
- Fleet report: `.ufo/reports/round-16/kaidoku.md`, committed as kaidoku-shokunin in `2d0274bd30003904fdfb38d50559b6316f1bed54`.
- Independent read-only reviewers: `CloseKaidokuR16.ClosureDepth`, `CloseKaidokuR16.ClosureCalibration`, `CloseKaidokuR16.ClosureWaveFloor`. Their findings were adjudicated by this non-author integrator; no author-side seat is treated as outside review.

Committed dispatch/completion digest (the mutable watchdog log is not the durable pointer):

```text
2026-10-20T05:06:58-03:00 launch kaidoku round=16 pgid=2466383 driver=hyaku-inline attempt=1
2026-10-20T05:43:22-03:00 complete kaidoku round=16; hyaku-inline attempt=1
```

I executed independent Git-object censuses and the required shared source-census command. I did **not** execute selection.py, selfcheck.py, measure.py, controls.py, quote-fidelity, citation-drift, or any sibling-owned gate. Gate/selftest outputs below are committed evidence verified, not fresh executions. No tools installed or updated.

## Step-1 conformance

Observed commands and outputs:

```text
git -C /home/vgpnk/Projects/shokunin log --format='%an %H %aI' -- .ufo/reports/round-16/kaidoku.md
kaidoku-shokunin 2d0274bd30003904fdfb38d50559b6316f1bed54 2026-10-20T05:43:00-03:00

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain
(empty, before closure writes)
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-list --count @{u}..HEAD
0
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
2fc1d6f355d14a507c95483fa3497b45d5e9a3fd
```

All three cited lane revisions B/S/A are commit objects and `git merge-base --is-ancestor <REV> HEAD` returned 0 for each. The report commit is likewise an ancestor of fleet HEAD. S was authored 05:35:55-03:00, receipt timestamp is 08:36:33Z, A was authored 05:40:52-03:00, and the report 05:43:00-03:00: source, execution evidence, delivery and report ordering are consistent. The report has the required sections, real LOG-linked changes, and exactly four `[~]` lines under `## SHONEN`; it is not a marker.

The dispatched prompt is tracked. Rendering `templates/round-prompt.md` with lane=kaidoku, round=16, fleet root, the exact declared axes, and its lane working directory gives an exact prefix of the prompt before §6. Mission/axes binding, claims/frontier, L2 floor, all report items, commit/push order, push scope and L0 channel are present. The addendum supplies the explicit operator-authorized two-wave and L1-planner mappings. Role buckets in MISSION are advisory; current host routing is not inferred from an old prompt snapshot.

### L2 floor despite 28 failed seats

Own read-only review of committed `wave*-spec.json`, `wave*-dispatch.json`, registrations, results, outcomes and metadata confirms:

| Wave | Dispatched original seats | Completed original seats | Failed | Completed role mix |
|---|---:|---:|---:|---|
| w1 | 64 | 36 | 28 | executor6, scribe6, reviewer12, critic6, revenger3, sentinel3; scout0, connector0 |
| w2 | 32 | 32 | 0 | executor8, scout6, connector2, reviewer8, critic4, scribe4 |
| round | 96 | 68 | 28 | failed originals are never counted as successful work |

W1 dispatch mix: executor6/scribe6/scout14/connector8/reviewer12/critic12/revenger3/sentinel3. All14 scouts and8 connectors failed credit routing; 6 critics failed capacity routing. W2 used operator-repaired routes with new original seats. Both taskCall task arrays contain only agent/name/task keys, no per-seat model; each dispatch is one batched payload. The dispatch policy objects carry w1 band64–100 and w2 band32–64. L1 holds the canonical planner seat under the explicit operator ruling.

**The numeric L2 floor holds:** MISSION requires at least8 **dispatched**, not successfully completed, in one batch; w1 dispatched64 and even completed36. There is no replacement/completion quota. The prompt's dispatch-role split was present in w1; lost scout/connector output must not be claimed as reviewed coverage. W2 restores completed scout/connector work, not the 28 dead identities. The required two waves are not an impermissible split: the operator expressly required sequential build/falsify waves. No provider cascade behavior is proven or blamed on this lane by these artifacts.

The review suggestion that “follow-ups retained original identities” contradicts new w2 spawns is not adopted: `wave2-outcomes.json` expressly refers to follow-ups of w2 seats, not w1 identities; the report separately declares96 originals and28 unreplaced failures. The uncompleted TypeLookup/FunctionLookup work items do not support a landed lookup-semantics claim; no such claim was made. Failed-seat reports are absent, and dispatch does not substitute for their substantive work. Shared-context delivery and precise failure timing cannot be independently reconstructed from payload/task text alone.

## Independent structural remeasurements

These were my own stdlib Python/Git-object counts, **not execution of the lane's measurement or gate scripts**. Reproduction recipe (run Python with this body; B/A above are literal revisions):

```python
from pathlib import Path
from collections import Counter
import subprocess, re
R = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
B = '6235498b4112350eebce0812a74af1781fc0ee88'
A = '2fc1d6f355d14a507c95483fa3497b45d5e9a3fd'
def g(*args):
    return subprocess.check_output(['git', '-C', R, *args])
def txt(rev, path):
    return g('show', rev + ':' + path).decode()
for rev in (B, A):
    files = g('ls-tree', '-r', '--name-only', rev).decode().splitlines()
    rows = [[c.strip() for c in line.split('|')[1:-1]]
            for line in txt(rev, 'corpus/SOURCES.md').splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', line)]
    paths = ['corpus/knowledge/2026-10-20-r16-go-selection-preview.md',
             '.ufo/waves/round-16/selection.py',
             '.ufo/waves/round-16/selection-fixtures.json',
             '.ufo/waves/round-16/selfcheck.py']
    sk = txt(rev, 'SKILL.md'); sh = txt(rev, 'SHONEN.md')
    kn = txt(rev, 'corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md')
    row = next(line for line in sk.splitlines()
               if line.startswith('| quote-fidelity |'))
    markers = [('Round-16 correction' in kn and
                'python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py' in kn),
               '.ufo/waves/round-15/boundary-fixtures/expected.json' in row,
               '.ufo/waves/round-16/controls.py' in files,
               'historical 2026-10-15' in sh]
    names = [Path(p).stem for p in files
             if p.startswith('corpus/knowledge/') and p.endswith('.md')]
    index = txt(rev, 'corpus/README.md')
    print(rev, [int(p in files) for p in paths],
          len(names), sum(n in index for n in names), len(rows),
          dict(Counter(r[3] for r in rows)),
          dict(Counter(r[7] for r in rows)),
          sum(markers), sh.count('this round'),
          len(re.findall(r'^\|\s*18\s*\|', txt(rev, 'corpus/QUALITY.md'), re.M)))
```

Observed before→delivered: C1 four presences `[0,0,0,0]→[1,1,1,1]`; knowledge/map93/93→94/94, no missing token; source rows23→23, tiersA21/B1/C1 unchanged, mined22/rejected1 unchanged; four route indicators0→4; SHONEN “this round”1→0; QUALITY18 presence0→1. An initial closure probe used the wrong guessed fixture subpath; directory discovery identified `selection-fixtures.json`, and the exact path census above corrected that probe. No lane artifact or claimed measurement was changed by it.

Additional own Git-object comparisons: LOG old prefix retained; all18 old lessons and93 old knowledge prefixes preserved; all4 prior verifier files byte-identical; QUALITY rows1–17 equal17/17. `git diff B A -- SCORECARD.md` is append-only56 lines, no score reduction or inflated capability row. All owned numeric proxies remain10.0; calibration therefore satisfies the tied-lowest obligation. The lowest-axis review seat's failure does not remove these committed values.

Own `git diff --name-only S A` on r16 producers/fixtures, old quote tools/frozen fixtures and citation-drift paths is empty. SHA-256 over committed delivered producer/fixture blobs matches the receipt map20/20. Original quote frozen expected.json hashes match9/9 referenced manifests/source excerpts; supplemental frozen hashes match3/3. These are identity comparisons, not new gate verdicts or proof of temporal stability.

## Claims and committed execution evidence

### C1 depth — improved

The structural delta is remeasured above. Substance is evidence-verified and source-reopened: S003 `GoApiSnapshot.java:102-166` gets patch-zero base, short-circuits missing base, then searches requested patch downward; `read:229-239` skips empty/null arches and preserves requested search order. It actually applies a selected diff in Java; the Python preview does not.

Committed `.ufo/waves/round-16/verification.json` names S, B and timestamp2026-10-20T08:36:33Z, retains argv/cwd/exit/stdout/stderr, and reports the ten-input developer run154/154 exit0. Independent reviewer counted154 authored cases,154 unique IDs, and verified the10 selection stdouts equal `selections.json`. These are stored executions, not closure reruns. Model/fixture bytes are identical S→A.

Observed retained contrasts:1.24.5→exact5 despite installed6;1.24.7 and1.24.10→fallback6;1.19.20→13;1.25.7/1.25.0→base0;1.26.8→missing base. Windows omits unix; linux/riscv64 yields linux/unix/all;1.15.0 darwin/arm64 yields darwin/unix/arm64/all. Independent reviewer reopened installed inventory and plain JSON keys, hand-derived these choices, and recomputed selected file sizes/hashes. In particular diff5 is106091 bytes, SHA256 `5743f4335615fdc5aa8d7e3c2516a8223a3eb769ffd306b3344b79bef4ea7053`; diff6 is118810 bytes, `e169e8dd0a1922b292159c56d85688cb84b0e47b44211aa4a3dd3fb1dd9cded6`.

This is a modest, concrete increase in usable technical detail on **held** ground, not discovery of the existing selector law, compiled-runtime parity, patch application, target recovery or a capability acquisition. Parser/shape, one-root, caller-platform and quiescent-file limits remain explicit. No exploratory judgment is needed.

### C2 calibration — improved

All four previous outside routes verify, not merely their0/4→4/4 markers:

1. The r15 named append corrects its header as an unexercised relative/non-isolated variant; the actual `python3 -I` absolute argv matches the r15 receipt. Existing inventory registry now uses that exact spelling.
2. Existing quote-fidelity row points to the supplemental r15 `boundary-fixtures/expected.json`; original and supplemental baselines remain unchanged and digest-pinned.
3. New `controls.py` output retains producing command, original interpreter argv, isolation flag and resolved B/S. Its stdout equals committed controls.json; independent object counts agree with18/18 lesson prefixes,93/93 knowledge prefixes,126/126 pre-existing frozen/evidence blobs,17/17 bounded craft ranges. The old r15 undocumented producer is not retroactively invented.
4. SHONEN box3 explicitly names historical2026-10-15 operator-steered round1, not “this round”; all4 marks remain `[~]`.

QUALITY18 cites the genuine r15 outside lesson; rows1–17 remain intact. The named r14 append also qualifies the old statement that all promotion gates were closed. Residual invocation and temporal-provenance defects below remain routed rather than hidden; neither invalidates these four bounded repairs.

### Gate evidence, not gate execution

At S the committed receipts show quote selftest28/28 exit0, original frozen7 matched exit0, supplemental frozen2 matched exit0, and strict citation clean0 findings exit0. The supplemental rendered control is an ordinary expected raw-substring failure, not a representation classifier. Registry rows, expected-value paths, verdict maps and ownership exist in SKILL. The strict citation receipt names S explicitly. Source→delivered producer/fixture identity and independently checked frozen digests preserve comparability; no delivered-HEAD fresh run is claimed. The new selection and structural tools are explicitly probes/developer checks, not gates or promotion instruments.

## Outside discernment sample

Sources reopened2026-10-20. Sampled the round lesson's actual Gate decisions, treating its selected candidates as admits only after the recorded executions and this independent review:

| Item | Gate decision | Reopened source | Outside decision | Reason |
|---|---|---|---|---|
| Explicit request-bounded selection preview | select/admit within source-model scope | Installed Base-src.zip member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:102-166,229-239`; delivered knowledge decision table and retained selection outputs | agree | Base-first, downward same-minor diff choice and ordered unpatched projection are concretely materialized, with clear non-parity limits. |
| Base bucket projection equals patched effective content | reject | Same member:130-143 applies JsonPatch/JsonPatchApplier before Java returns provider content; delivered preview entry:38-49 explicitly omits patch application | agree | A names-only base projection cannot establish post-patch content or successful type lookup. |
| Requested-version label authenticates exact patch bytes | reject | Same member:111 passes original GoVer after fallback;239 constructs snapshot with that version | agree | Requested label is not selected input identity; fallback and file digests remain distinct. |

### Source-row and quote recheck

There were **zero newly written registry rows**: own B→A source diff shows only used-by extensions for existing S003/S023 plus search-log append; no row quota is imposed. Thus a literally new-row sample is inapplicable, not fabricated. I sampled **newly reused/extended S023**, as well as S003, instead.

- Reopened S003 source raw line122: `GoVer baseVer = goVer.withPatch(0);` — exact contiguous4-word quote; raw line109: `IS_GOOS_UNIX.contains(goOS) ? "unix" : "", goArch, "all");` — exact7-word quote. Both are≤25 words. Own archive SHA256 is `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, matching registry.
- Reopened S023 JSON query `.all.Types["runtime.moduledata"].Fields[1]` returned `{"Name":"pcHeader","DataType":"*runtime.pcHeader"}`. The round's quoted contiguous raw fragment `"Name":"pcHeader","DataType":"*runtime.pcHeader"` is present at raw line1, below25 words, and supports its scoped generic-pointer teaching, not provider execution. Reviewer independently checked file SHA256 `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`.

Required command independently executed:

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku\tok\t/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

## Axis and trend verdicts

| Axis | Verdict | Scope/evidence |
|---|---|---|
| depth | improved | C1 concrete selected-file computation and source-grounded decision detail; no numeric inflation |
| calibration | improved | C2 four genuine outside routes repaired, historical assertions qualified, current receipt limits separated |
| coverage | unchanged |93/93→94/94 is index integrity on held Go ground, not new domain breadth |
| operability | unchanged | No new held REA/domain operation; developer154-case receipt and existing gate evidence remain bounded |
| freshness | unchanged | Installed source/data reopened, not broad runtime revalidation |
| adjacency | unchanged | No sibling/provider/host ownership absorbed |

- **expansion: unchanged** — no newly held frontier/capability; new knowledge stays on held Go ground.
- **quality: improved** — bounded selector detail now has retained computations; old invocation/promotion claims receive explicit corrections. Temporal overstatement is marked and routed here, not accepted as proof.
- **discernment: improved** — the previous non-author routes became lesson-backed QUALITY18/fixes, and this round's outside sample agrees on admits and rejects.

No axis harm is established within the declared and explicitly limited claims. C1/C2 are independently verifiable; admission does not certify every historical corpus statement. SHONEN is **not** fully checkable by this review: complete semantic craft/instruction execution and accurate current province need their own non-author evidence. Operator alone owns promotion.

## Routed defects and adjudicated limits

Route both defects to **kaidoku next round**; aggregator/integrator should mirror them in its durable routed-defect queue. They are status-neutral and do not undo C1/C2:

1. **R16-PROVENANCE — unsupported temporal stability wording.** verification.json retains one20-entry hash map and `pins_unchanged_during_run:true`, but no before/after maps, per-command hashes, or before/after timestamps. The report, lesson, LOG and scorecard say pins stayed unchanged during execution. Independent comparison proves only that recorded hashes match committed S/A bytes20/20, not that files were stable throughout the run. Append named corrections across all such statements: say “map matches committed source-revision blobs; temporal stability not evidenced,” or retain actual pre/post records for any future stronger statement. Never rewrite filed report/LOG bytes or treat the boolean as a measurement.
2. **R16-INVOCATION — remaining citation-drift registry variant.** SKILL.md citation-drift row:448 still advertises `python3 ... --root .` without `-I`, whereas r16's exercised strict argv is isolated and absolute. Unlike the repaired inventory row, this surviving variant is not identified as unexercised. Align future runnable guidance with an actual receipt, or explicitly distinguish intended vs exercised invocation, with a lesson/QUALITY18 link. This pre-existing generalization gap is not one of the four specific r15 routes, which are closed.

The preview registry's abbreviated two-fixture command explicitly points to the retained full ten-input argv; it does not claim that abbreviated command produced154 results. No separate defect is invented for that documented distinction. One-root/Java/Gson/patch/atomicity limitations are intentionally held limits, not repair claims. Dead-seat coverage, fallback internals and precise “immediate” failure timing remain unverified; no unavailable seat output is admitted. No operator action beyond routing these defects and retaining promotion ownership is needed for this closure.
