# Round 14 — independent closure and discernment spot-check

author: hyaku closure (non-author integrator, @m_strong)
date: 2026-10-20
scope: kaidoku round 14 only; no lane-authored files, gates, or SHONEN marks changed.

## Decision and revision boundary

**status: ok; admitted: true.** C1 depth and C2 calibration verify within their expressly bounded claims. No owned axis is harmed. This is not promotion or proof of historical Go recovery causality.

- Before: `767adafb97e2eef6980e2ad873d357e16721c467`.
- Delivered after: `9d4e51188102483f48feca302c19a9dbd67f3399`.
- Source/work revision measured by the author: `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`.
- Fleet report commit: `55e5f8c212e7db3520755ee7e2cbef679470e287`, author `kaidoku-shokunin`, 2026-10-20T02:37:29-03:00.
- Independent read-only reviewers: `CloseKaidokuR14.GoClaimReview` and `CloseKaidokuR14.QuoteEvidenceReview`. They are closure seats, not the round author's L2 seats. Their findings were adjudicated below. Neither closure nor its reviewers executed a lane-owned gate/selftest.

Committed dispatch/completion digest supplied with this closure assignment:

```text
2026-10-20T02:11:49-03:00 launch kaidoku round=14 pgid=1493554 driver=hyaku-inline attempt=1
2026-10-20T02:37:45-03:00 complete kaidoku round=14; hyaku-inline attempt=1
```

## Step-1 conformance

Commands used (L is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; F is `/home/vgpnk/Projects/shokunin`):

```sh
git -C "$F" log --format='%an %H %aI' -- .ufo/reports/round-14/kaidoku.md
git -C "$F" log --format='%H %an' -- .ufo/prompts/kaidoku-round-14.md
git -C "$L" status --porcelain
git -C "$L" rev-list --count '@{u}..HEAD'
git -C "$L" rev-parse HEAD
git -C "$L" merge-base --is-ancestor 3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22 HEAD
git -C "$L" merge-base --is-ancestor 9d4e51188102483f48feca302c19a9dbd67f3399 HEAD
git -C "$L" diff 767adafb97e2eef6980e2ad873d357e16721c467 9d4e51188102483f48feca302c19a9dbd67f3399 -- SCORECARD.md
```

Observed: report author/hash/date as above; prompt committed at `4c8f2f636aca235e192239a7cc2d5bc4ee87cf3d` by kaidoku-shokunin; status output empty; ahead count 0; HEAD equals delivered after; both cited work hashes exist and ancestry checks exit 0. Baseline ancestry also exits 0. Work commits carry kaidoku-shokunin and precede the report (02:32:55 and 02:35:53 -03:00). SCORECARD diff is 58 insertions, no deletions; it preserves all three owned 10.0 proxies and states their limits.

The report has the six required headings in order and four separately marked `[~]` SHONEN lines. It names real committed work and measurable artifacts, so it is not a marker. A literal Python template rendering (LANE=kaidoku, ROUND=14, FLEET_ROOT=F, AXES as dispatched, `<kaidoku-repo>` resolved to `kaidoku-shokunin`) matched the prompt prefix exactly: `template_exact_prefix=True`. The campaign addendum adds write scope, report-last ordering, planner mapping and host mechanics without replacing the template contract.

Committed dispatch evidence contains 32 tasks, no `model` parameter, with 6 scout / 6 executor / 4 connector / 6 reviewer / 4 critic / 2 scribe / 2 sentinel / 2 revenger. `task-result.json` records the 32-seat call. The report explicitly maps L1 to the planner seat under the campaign ruling. These are conformance artifacts, not independent discernment evidence.

## Independent claim recount

I ran a fresh stdlib Python census over immutable Git bytes, not the lane's `measure.py` or a verdict script. Reproducible counting core:

```python
import subprocess, pathlib, re, json, hashlib
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
B = '767adafb97e2eef6980e2ad873d357e16721c467'
A = '9d4e51188102483f48feca302c19a9dbd67f3399'
def git(*args):
    return subprocess.check_output(['git', '-C', L, *args], text=True)
def get(rev, path):
    return git('show', f'{rev}:{path}')
for rev in (B, A):
    paths = set(git('ls-tree', '-r', '--name-only', rev).splitlines())
    files = {pathlib.Path(p).stem for p in paths
             if p.startswith('corpus/knowledge/') and p.endswith('.md')}
    section = get(rev, 'corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    rows = [s.split('|') for s in get(rev, 'corpus/SOURCES.md').splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', s)]
    print(rev, 'C1', int('corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md' in paths),
          'C2 instrument', int('.ufo/waves/round-14/tools/quote-fidelity.py' in paths),
          'C2 criterion', int('quote-fidelity' in get(rev, 'corpus/QUALITY.md')),
          'knowledge/mapped', len(files), len(files & mapped),
          'missing/dangling', sorted(files-mapped), sorted(mapped-files),
          'rows', len(rows), 'tiers', {t: sum(r[4].strip()==t for r in rows) for t in 'ABC'},
          'statuses', {s: sum(r[8].strip()==s for r in rows) for s in ('queued','mined','rejected')})
    craft = get(rev, 'SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    resolved = 0
    for rule in rules:
        refs = re.findall(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?', rule)
        valid = bool(refs)
        for name, first, last in refs:
            n = len(get(rev, 'corpus/knowledge/' + name).splitlines())
            valid = valid and 1 <= int(first or 1) <= int(last or first or 1) <= n
        resolved += valid
    print('craft', hashlib.sha256(craft.encode()).hexdigest(), len(rules), resolved)
```

Observed results, matching the report:

| Observable | Before | Delivered after |
|---|---:|---:|
| C1 diagnostic entry | 0 | 1 |
| C2 quote instrument | 0 | 1 |
| C2 criterion presence | 0 | 1 |
| Knowledge files / mapped | 91 / 91 | 92 / 92 |
| Missing / dangling | empty / empty | empty / empty |
| Source rows | 22 | 22 |
| Tiers A/B/C | 20/1/1 | 20/1/1 |
| Status queued/mined/rejected | 0/21/1 | 0/21/1 |
| Craft rules / resolved citations | 17/17 | 17/17 |

Craft hash on both sides: `e12b60ce0c71316e457680c65ae8273487deac9c68db3f80a084814a8ad765e6`. A reviewer's different extraction boundary gave a different hash but the same cross-revision equality; the existing command-A boundary above reproduces the report's exact digest. These are presence/range counts, not semantic proof. Semantic grounding was checked separately by reopening the entry, criterion, prior outside lesson and source control flow.

### C1 — depth: improved (re-measured and source-verified)

The new entry accurately separates the advisory range warning from snapshot lookup and conditional struct-registration failure. S003 archive source confirms `GoRttiMapper.java:170-176`, `:353-365`, the `getType` override at `:380-386`, and `GoTypeManager.java:448-449` snapshot dependence. S004's upstream support commit changes more than the range: snapshot JSON, moduledata lookup, pcHeader presence and map handling. Source-reading is not represented as a historical target replay.

The previous historical entry receives a 17-line append-only correction; PROVINCE and both README summaries qualify the old causal explanation. The precise old failure remains UNKNOWN because its analyzer log was not retained. The new file deepens already-held Go ground and earns no expansion credit. One advisory review artifact contains an incorrect mechanism explanation; the admitted entry does not repeat it (routed below).

### C2 — calibration: improved (re-measured presence; capability evidence-verified)

At the measured source revision, SKILL registers the gate command, exit map 0/1/2, selftest, pinned expectation path, owner and write scope. QUALITY #16 cites the prior genuine outside S017/S018 findings and limits machine evidence to captured raw substring/section consistency. Its criterion is grounded, not established merely by the presence count.

`verification.json` is committed at delivered after and names source revision `3e99fbd6f05dc05341bdfbbd7e3b2b86785abc22`. It records:

- CLI selftest: `CLEAN cases=28 passed=28 failed=0 exit=0`.
- Frozen run: seven exact expected exit/finding lists matched; `manifests=7 findings=0 exit=0`.
- S017 quote-only control: red exit 1 `quote_not_contiguous@S017-Q1`, fixed exit 0.
- S018 section-only control: red exit 1 `quote_location_mismatch@S018-Q1`, fixed exit 0.
- Corrected combined manifest: two quotes, zero findings, exit 0.
- Citation-strict: clean, zero findings, exit 0. Scoped census: PASS with stale/ambiguous/undeclared/unresolved 0/0/0/0.

The read-only gate reviewer independently hashed the script, measure script, expected file, seven manifests and two excerpts against committed pins: all match at the source revision and delivered after. The expectation set pins every current manifest/source input. The records-only second commit does not change gate/fixture/SKILL/QUALITY bytes. Static review confirms real CLI subprocess tests and explicit expected exits/IDs; this is evidence verification, not a closure rerun.

The capability is deliberately regression coverage for two known defects, not independent population accuracy, general quotation parsing, authenticity, source completeness or semantic support. Producer-authored expectations do not establish those broader properties. Raw excerpts remain inspectable; full-page hashes/provenance and live upstream checks are not a guarantee of permanent remote availability.

## Outside discernment sample

Access date: 2026-10-20. At least one admit and one reject below are from this round's `## Gate`, not invented new decisions.

| Item | Lane decision | Re-opened source | Outside result | Reason |
|---|---|---|---|---|
| Source-conditional Go bootstrap diagnosis | admit | Installed S003 `Base-src.zip`, `GoRttiMapper.java:170-176,353-386`; `GoTypeManager.java:438-455`; S004 https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174 | agree | Advisory range continues; snapshot-dependent lookup is a later mechanism; upstream support is a bundle. The entry does not claim to reproduce the lost historical cause. |
| “SUPPORTED_VERSIONS itself rejects Go 1.26” | reject | Same S003 `GoRttiMapper.java:170-176` | agree | The out-of-range branch logs and continues to snapshot lookup; no throw/return makes this the rejecting branch. |
| “Source reading proves the precise historical inventory cause” | reject | Historical entry and its appended correction, new entry `:81-99`, S003 control flow | agree | No retained historical analyzer log or target replay; the source path has multiple relevant conditions and cannot select that old run's cause. |
| Local raw-quote/heading regression instrument | admit as bounded demonstration | Committed `verification.json`, pinned fixtures and static gate code; S017 raw README https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md; S018 https://research.checkpoint.com/2026/breaking-the-seal-static-deobfuscation-of-jsceals-compiled-v8-bytecode/ | agree | Exact known-defect red/fixed controls support the stated narrow capability. Upstream re-fetches matched recorded hashes; no semantic-generalization credit given. |

**Source-row quote sample:** no new rows were written (ID-set difference empty on both sides), so a newly added-row sample is inapplicable, not fabricated. I sampled newly used-by-touched S007 instead. Its lesson quote, “Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.”, is 17 whitespace-delimited words and an exact contiguous substring at installed `docs/ChangeHistory.md:585`, under `Ghidra 12.0 Change History` → `Improvements`. The source entry's digest pins matched fresh `sha256sum`:

```text
S001 c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0
S003 f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804
S007 c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4
```

I also ran the required shared source validator (not a sibling-owned gate):

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

The source diff changes only six permitted used-by cells, with exact old→new values logged in the lesson. No immutable row field or source tier was rewritten.

## Per-axis and learning-trend verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | Source-conditional diagnosis, decision table and explicit historical causal correction; citation control remains 17/17. |
| calibration | improved | Grounded criterion plus evidence-verified regression capability, without numeric-score inflation or broad accuracy claims. |
| coverage | unchanged | 92/92 map integrity, but the Go surface was already held; no new domain coverage claimed. |
| operability | improved | The committed actual-CLI/frozen/control evidence supports a newly runnable local instrument; this is not an additional REA target operation. |
| freshness | unchanged | Reopened/pinned sources support the diagnosis; no new live-provider freshness claim. |
| adjacency | unchanged | No sibling admission method, provider installation or configuration ownership taken. |

- **expansion: unchanged** — same held Go ground; a file count or local bookkeeping instrument is not new REA domain ground.
- **quality: improved** — unsupported historical causal explanation is explicitly superseded by stronger source-conditional reasoning; active summaries qualify it, and the admitted entry passes this source re-check.
- **discernment: improved** — this closure now supplies the required fresh outside admit/reject agreement. Prior outside findings also became a grounded criterion and exercised regressions. The round's earlier “pending” text correctly distinguished author evidence from this closure; an author-side trend statement alone would not have completed the current-round sample.

## Routed defects and adjudication

1. **kaidoku, next round — advisory evidence correction (status-neutral).** `.ufo/waves/round-14/w1/ReviewGoInference.md:57-61` says snapshot absence only selects wording and `registerStructures` does not consult the snapshot. That ignores the mapper's virtual `getType` override and `GoTypeManager` snapshot lookup. The lesson Gate row 1 cites that artifact as preserving conditional control flow. Append a named correction to the lesson/LOG and qualify the advisory pointer; preserve the filed evidence. Do not propagate the erroneous mechanism. The admitted knowledge entry already gives the correct mechanism, so C1 survives and no owned axis is harmed.
2. **kaidoku, next round — clarify manual-only input boundary (status-neutral).** QUALITY #16 says the local instrument “does not grade” markup-spanning quotations. Its raw-substring code has no special unsupported-input classification: if such a rendered quote is submitted, it can return exit 1 as absent. The report and gate docstring correctly disclose raw UTF-8 behavior, and the criterion directs these inputs to manual checking. Clarify that these inputs must not be submitted as machine-gradeable, or align the documented exit behavior and add an appropriate control. This ambiguity does not falsify the two retained raw-quote regression controls; no rendered-quote capability is admitted.

Reviewer concerns about producer-authored expected values, closed-world frozen inventories, and presence-only measurement are limits, not failures of the declared narrow claim; static source review and the fresh outside sample supply grounding beyond those counts. The scoped census was a recorded worktree run at the source commit, not an immutable host replay; no stronger claim is credited. Installed JSON inventory could deepen a future diagnosis, but no missing-JSON cause is inferred for the historical run here.

SHONEN boxes are not all established by this bounded check: full-province accuracy/version alignment and independent executable-instruction review remain outside it. No `[x]`, promotion or mint is authorized or written. Tool installs/updates: none (closure and reviewers).
