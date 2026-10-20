# Round 15 — independent closure and discernment spot-check

author: hyaku closure (non-author integrator, @m_strong)
date: 2026-10-20
scope: kaidoku round 15 only; no lane-authored file, gate, or SHONEN mark changed.

## Decision and revision boundary

**status: ok; admitted: true.** C1 depth and C2 calibration verify within their declared source/data and documentation boundaries; no axis is harmed. Installed-data inventory is not target execution, historical-cause proof, or a provider repair. The requested-label/fallback-data distinction is admitted as explicitly labelled **source inference**, not a measured patched-output identity or an inventory-computed fallback selection.

- Before: `9719dd232687f5ee78a4ed323b37f8810e833d10`.
- Delivered after: `ee43ddd059ce7b89a6c5c7a19cde326d5cf5ba18`.
- Repaired probe/retained controls revision: `7ad23fe1735cd868ec203d93deb13bb2c42889ad`.
- Final author-measured source revision: `ba3b2195d080d3083d339a67c35359855ad164a5`.
- Fleet report: `.ufo/reports/round-15/kaidoku.md`, commit `c8b09484ae53bbdf3f22235d90f1a645b0180ee7`, author `kaidoku-shokunin <kaidoku@shokunin.local>`, 2026-10-20T04:20:37-03:00.
- Dispatched prompt: `.ufo/prompts/kaidoku-round-15.md`, commit `16cafba4e5001b60121ae45d27f17b3f4aff840e`.
- Independent read-only closure reviewers: `CloseKaidokuR15.Conformance`, `CloseKaidokuR15.SnapshotSemantics`, `CloseKaidokuR15.CalibrationEvidence`. They are not the author's L2 seats. Their findings were adjudicated below; no closure seat executed a lane-owned gate/selftest.

Dispatch/completion digest supplied by the orchestrator, copied here rather than depending on the mutable watchdog log:

```text
2026-10-20T03:52:01-03:00 launch kaidoku round=15 pgid=2188641 driver=hyaku-inline attempt=1
2026-10-20T04:20:52-03:00 complete kaidoku round=15; hyaku-inline attempt=1
```

## Step-1 conformance

Commands executed by this closure (L = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; F = `/home/vgpnk/Projects/shokunin`):

```sh
git -C "$F" log -1 --format='%H %an <%ae> %aI' -- .ufo/reports/round-15/kaidoku.md
git -C "$F" log -1 --format='%H %an <%ae> %aI' -- .ufo/prompts/kaidoku-round-15.md
git -C "$L" status --porcelain
git -C "$L" rev-parse HEAD
git -C "$L" rev-list --count '@{u}..HEAD'
git -C "$L" merge-base --is-ancestor <each hash below> HEAD
git -C "$L" diff 9719dd232687f5ee78a4ed323b37f8810e833d10 ee43ddd059ce7b89a6c5c7a19cde326d5cf5ba18 -- SCORECARD.md
```

Observed: report and prompt hashes/authorship as above; lane status empty; HEAD equals delivered after; ahead count 0. All five hashes resolve and ancestry exits 0: baseline, `856d193b8c21d3f7aeff3cb8a27b55a715ab897e`, repaired probe, final measured source, delivered after. The conformance reviewer independently found the report in `origin/master`, lane HEAD equal to `origin/main`, and the four round commits lane-authored. SCORECARD diff is 59 insertions and no deletions; all owned proxies remain 10.0. The report names checkable committed work, so it is not a marker.

All six required report headings occur in order, with four separately assessed `[~]` SHONEN lines. The dispatched prompt carries the claims, frontier, L2, report and commit/push contract. The conformance reviewer compared rendered template sections 3–5, including report section 4, with the dispatched bytes and observed empty diffs. The campaign's L1-planner ruling is explicitly recorded. Committed spec/dispatch/result/registry artifacts agree on one 32-seat call, no model parameter, and role mix 6 executor / 6 scout / 4 connector / 6 reviewer / 4 critic / 2 sentinel / 2 revenger / 2 scribe. This meets the **dispatched round-15 32–64 band**, not the later 64–100 policy. Author seats do not become independent reviewers.

## Independent claim recount — committed bytes, not lane scripts

I ran fresh stdlib Python measurements in the closure session, using `git show`/`git ls-tree`. I did not execute `measure.py`, the inventory probe, the quotation gate, or the citation probe. Reproducible counting core:

```python
import subprocess, pathlib, re, json, hashlib, collections
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
B = '9719dd232687f5ee78a4ed323b37f8810e833d10'
A = 'ee43ddd059ce7b89a6c5c7a19cde326d5cf5ba18'
def get(rev, path):
    return subprocess.check_output(['git', '-C', L, 'show', f'{rev}:{path}'])
for rev in (B, A):
    paths = set(subprocess.check_output(
        ['git', '-C', L, 'ls-tree', '-r', '--name-only', rev], text=True).splitlines())
    quality = get(rev, 'corpus/QUALITY.md').decode()
    lesson = get(rev, 'corpus/lessons/round-14.md').decode()
    readme = get(rev, 'corpus/README.md').decode()
    section = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    knowledge = {pathlib.Path(p).stem for p in paths
                 if p.startswith('corpus/knowledge/') and p.endswith('.md')}
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    rows = [l.split('|') for l in get(rev, 'corpus/SOURCES.md').decode().splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', l)]
    row17 = next((l for l in quality.splitlines()
                  if re.match(r'^\|\s*17\s*\|', l)), '')
    print(rev,
          int('corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md' in paths),
          int('.ufo/waves/round-15/snapshot-inventory.py' in paths),
          int(bool(row17) and 'must not be submitted' in row17.lower()),
          int('Round-15 correction — virtual-dispatch advisory' in lesson),
          len(knowledge), len(knowledge & mapped),
          sorted(knowledge-mapped), sorted(mapped-knowledge), len(rows),
          dict(collections.Counter(r[4].strip() for r in rows)),
          dict(collections.Counter(r[8].strip() for r in rows)))
```

Observed values match the report, now recounted against **delivered after**, not merely the earlier measured source:

| Observable | Before | Delivered after |
|---|---:|---:|
| C1 entry / inventory probe presence | 0 / 0 | 1 / 1 |
| C2 explicit row-17 manual-only wording / named r14 correction | 0 / 0 | 1 / 1 |
| Knowledge files / mapped | 92 / 92 | 93 / 93 |
| Missing / dangling | empty / empty | empty / empty |
| Source rows | 22 | 23 |
| Tiers A / B / C | 20 / 1 / 1 | 21 / 1 / 1 |
| Status mined / rejected | 21 / 1 | 22 / 1 |

Presence controls are not semantic proof. The source reviews and outside sample below provide the grounding.

### C1 depth — improved; independently re-measured and source-verified

A fresh installed-file census, independent of the probe, found 11 `go*.json` bases and 123 `patchverdiffs/go*.json.diff` files. Histogram: 1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14, 1.21:13, 1.22:12, 1.23:12, 1.24:6. I compared all 134 installed file sizes/SHA-256s with committed inventory entries: **134/134 match**; every parsed base contains `all`, **11/11**. Counting/pin core executed:

```python
R = pathlib.Path('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang')
bases = sorted(R.glob('go*.json'))
diffs = sorted((R/'patchverdiffs').glob('go*.json.diff'))
print(len(bases), len(diffs), dict(collections.Counter(
    re.match(r'go(\d+\.\d+)\.', p.name)[1] for p in diffs)))
inv = json.loads(get(A, '.ufo/waves/round-15/inventory.json'))
pins = []
for kind in ('base_json', 'patch_diffs'):
    for item in inv[kind]['files']:
        p = pathlib.Path(item['path']); raw = p.read_bytes()
        pins.append(len(raw) == item['size'] and
                    hashlib.sha256(raw).hexdigest() == item['sha256'])
print(len(pins), sum(pins), sum('all' in json.loads(p.read_bytes()) for p in bases))
print(len(inv['patch_diffs']['files']),
      sum(type(x['patch']) is int for x in inv['patch_diffs']['files']),
      sum(isinstance(x['patch_structure'], dict) for x in inv['patch_diffs']['files']))
```

Last output is **123 / 123 / 123**. Committed `inventory.json` SHA-256 is `ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`; both retained inventory stdout strings are byte-identical. The S023 fresh JSON query reproduced 27 buckets, `all` 29,041 functions / 3,741 types, moduledata/pcHeader 45/13 fields. These count resource records, not recovered target functions.

Reopened S003 `GoApiSnapshot.java:108-165,205-239` confirms mandatory same-minor base, backward search for one diff, base-only fallback, original requested version passed to `read`, and `new GoApiSnapshot(ver, results)`. The independent source reviewer also checked `GoRttiMapper.java:178-181,379-396` and `GoTypeManager.java:402-455`. Thus requested-version metadata does not establish exact patch-byte identity. The inventory does **not** apply a diff, emit a patched-result digest, calculate target GOOS/GOARCH applicability, or demonstrate compiled provider behavior. Bootstrap details are retained for selected bases, not every installed base. Those are limits, not extra capabilities credited here.

### C2 calibration — improved; independently re-measured wording, evidence-verified controls

QUALITY #17 expressly supersedes #16's ambiguity, retains contiguous located quote obligations, prohibits code/JSON/rendered/etc. inputs as machine-gradeable, and voids the raw result for an excluded claim even if ordinary raw rules return 0/1/2. It does not pretend the unchanged tool detects representations. The prior outside defects are actually discharged: named append-only advisory corrections include the virtual `getType` dispatch and snapshot-backed lookup; the active raw/manual boundary is explicit and lesson-grounded.

Gate evidence is verified, **not re-executed**. At delivered after, committed `verification.json` names `7ad23fe1735cd868ec203d93deb13bb2c42889ad` and contains:

| Recorded invocation/control | Observed committed result |
|---|---|
| quote-fidelity `--selftest` | `CLEAN cases=28 passed=28 failed=0 exit=0` |
| original `--frozen round-14/fixtures/expected.json` | `clean mode=frozen manifests=7 findings=0 exit=0` |
| rendered boundary manifest | exit 1, `quote_not_contiguous@raw-literal` |
| raw boundary manifest | exit 0, clean, no findings |
| boundary `--frozen round-15/boundary-fixtures/expected.json` | `clean mode=frozen manifests=2 findings=0 exit=0` |
| strict citation at repaired probe revision | exit 1, `citation_dead@sc-arc3r2-cites-shonen` |
| strict citation in `final-recheck.json`, revision `ba3b2195d080d3083d339a67c35359855ad164a5` | exit 0, clean findings 0 |

The gate reviewer matched all eight measurement pins and the frozen input digests against committed bytes; the final two boundary manifests differ only in quote text, with the same source and ID. These producer-authored synthetic controls establish the disclosed raw-input limitation, not upstream authenticity, semantic truth, population calibration, or a new classifier. SKILL's existing quote-fidelity registry retains the command, 0/1/2 map, selftest, pinned original baseline and write scope; supplemental baseline discoverability is routed below.

### No-harm controls

Independently reproduced from Git objects: LOG, round-14 lesson and r14 knowledge entry retain their baseline bytes as prefixes; old advisory, prior outside verifier, old quote script and original frozen expected file are byte-identical. QUALITY #16 is unchanged. S023 is the only added source ID; none removed; S003/S007 change only cell 11 (`used-by`), exactly as logged.

For craft control, I split SKILL after `## Queue-drain craft ` and before the next `\n## `, split rules with `(?m)^- \*\*`, extracted `corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?`, and checked each cited range against `len(get(rev,path).splitlines())` for both revisions. Observed **17 rules / 17 resolving blocks** on each; both section SHA-256s equal `e12b60ce0c71316e457680c65ae8273487deac9c68db3f80a084814a8ad765e6`. This is citation-range integrity, not a complete semantic audit.

## Outside discernment sample

Access date: 2026-10-20. Candidates below are from round-15 lesson `## Gate`, not replacement decisions invented by closure.

| Item | Lane decision | Re-opened source | Outside result | Reason |
|---|---|---|---|---|
| Installed Go inventory and source selector decision record | admit after execution | S023 installed `go1.25.0.json`; all 134 inventory file identities; S003 `GoApiSnapshot.java:108-165,205-239`; retained execution receipts | agree | Actual generic definitions and exact installed-byte identities deepen held diagnosis; source inference remains distinct from target/provider execution and patch application. |
| Requested patch version equals matching patch snapshot bytes | reject | S003 `GoApiSnapshot.java:111,122-165,239` in installed `Base-src.zip` | agree | A base or lower patch diff can supply bytes while original requested version labels the object; no equality follows from the label. |
| Snapshot validity merely changes error wording | reject | Reopened S003 call chain, source reviewer: `DataTypeMapper.java:176,310-313`, `GoRttiMapper.java:379-396`, `GoTypeManager.java:402-455` | agree | Overridden type lookup reaches `apiSnapshot.getTypeDef`; the prior advisory's snapshot-independent explanation omitted virtual dispatch. |
| Raw quote failure automatically classifies fabrication/unsupported input | reject | QUALITY #17, unchanged gate source, pinned rendered/raw manifests, committed control stdout | agree | The rendered form receives ordinary raw-substring exit 1, not a representation-classification result. Manual-only submission policy is the correction. |

**New source-row quote sample S023:** reopened installed `go1.25.0.json`, queried `.all.Types["runtime.moduledata"].Fields[1]`, and independently searched its raw bytes. Quote `"Name":"pcHeader","DataType":"*runtime.pcHeader"` is contiguous on raw **line 1**, at the claimed JSON field; **1 whitespace-delimited word**, below 25. Fresh SHA-256: `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`. It grounds the row's generic-pointer statement, not provider execution. JSON was manually source-checked, not submitted to the raw prose gate.

Required shared source validator executed by closure (not a sibling-owned gate):

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

## Per-axis and learning-trend verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | New data-byte identities, selected bootstrap detail and source-labelled requested-version/fallback distinction; independent 134-file identity check and source trace. |
| calibration | improved | Both prior genuine outside duties discharged by grounded active criterion/corrections; current independent admit/reject sample agrees. No numeric or classifier credit. |
| coverage | unchanged | 93/93 map integrity, but added entry deepens already-held Go ground. |
| operability | unchanged | Initial actual inventory failure repaired and retained; clean final output evidence, no residual harm or new held target operation. |
| freshness | unchanged | Installed sources/data reopened; no new live-provider freshness demonstration. |
| adjacency | unchanged | No sibling ownership or upstream/provider/configuration authority absorbed. |

- **expansion: unchanged** — no uncovered ground or new target capability; rows and files alone are not expansion.
- **quality: improved** — stronger source/data diagnosis, actual original failures retained, and both erroneous/ambiguous explanations qualified rather than left unmarked.
- **discernment: improved** — this non-author sample agrees on admits and rejects; prior outside disagreements also became a grounded criterion and named corrections. Author-seat agreement is not counted as outside evidence.

## Routed defects and reviewer adjudication

Status-neutral, assigned to **kaidoku next round**, not reasons to rerun or reject the declared claims:

1. **Invocation consistency:** new knowledge entry `recheck:` omits `-I`, whereas retained actual execution uses `python3 -I` and an absolute script path. Align future recheck guidance with the exercised isolation flag, or explicitly distinguish intended recheck from recorded argv. Closure ran neither spelling and claims no unobserved equivalence.
2. **Supplemental baseline discoverability:** add a reference to `.ufo/waves/round-15/boundary-fixtures/expected.json` from the existing quote-fidelity registry row. The supplemental controls are pinned and cited in receipts/lesson/LOG, but the registry's pinned-values cell currently points only to the original round-14 baseline. No new gate or classifier is required.
3. **Count-command provenance:** retain a producing command/snippet alongside future `no-harm-controls.json` booleans and structural tallies. The current record lacks its own command for every supplemental field. Closure and its gate reviewer reproduced the values; that establishes these narrow facts, not that the author's original undocumented check was a retained invocation. The independent recount above supplies the command basis for closure.
4. **Historical SHONEN wording:** box 3's “this round” points to the round-1 lesson; name the historical round explicitly when next updating its evidence line. Current report correctly distinguishes new local inventory/control execution from historical native execution, and all marks remain `[~]`.

Reviewer concerns were not accepted wholesale. SHONEN is not an append-only lesson: canonical seed regeneration permits changing its title/evidence and removes extra footer prose. LOG:1868-1870 and lesson:105-107 disclose moving the older 17/17 footer qualification into box-1 evidence; the indented canonical seed excludes the unindented protocol `Marks:` explanation. There is no undisclosed append-only deletion here. The changed Go decision-row substance is logged at LOG:1861-1863 and cited at report:10. Final measurement addenda are records, and the report explicitly names the earlier measured source; closure does not invent a delivered-HEAD gate run. Source-inferred fallback identity is admitted only under its explicit inference label; selected-only bootstrap retention, key-set-level architecture inventory, unanalysed GDTs, duplicate-key limits and unapplied patches receive no broader credit.

SHONEN boxes are **not all independently established** by this bounded closure: complete-province/version accuracy and independent executable-instruction review remain outside it. No promotion, mint, or `[x]` authorization. Tool installs/updates: **none** by closure and its reviewers.
