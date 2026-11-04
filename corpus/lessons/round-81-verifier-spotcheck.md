# Round 81 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

## Scope and conformance

Reviewed the dispatched closure prompt and report, frozen declaration `plans/round-81-claims.md`, and committed base `5b59ae615a2ab68e3b421820d1c72751e1185385` → final lane revision `6bbf775a4e0ce69a334e9cf5f2c19320af67d0c5`. This is independent closure, not lane-authored improvement or promotion.

- Real report, not marker: all required sections, checkable committed work, `## SHONEN`, four `[~]` lines matching the four checklist boxes. `SHONEN.md` is unchanged. The apparatus-only demonstration does not newly establish every promotion box; operator-owned promotion is not requested.
- `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %cI %H' -- .ufo/reports/round-81/kaidoku.md` observed `kaidoku-shokunin <kaidoku@shokunin.local> 2026-11-04T11:51:03-03:00 9a24b8754355a16fe135e1071a020dd4857b9ba0`. Report attribution is the lane's; filing follows the final lane push and precedes driver completion.
- `jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin` observed `branch=main local=6bbf775a4e0ce69a334e9cf5f2c19320af67d0c5 remote=6bbf775a4e0ce69a334e9cf5f2c19320af67d0c5 ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` emitted nothing before this spot-check was written. Fleet scratch changes are unrelated operator work, not lane debt.
- All nine Landed-changes hashes, base, and cited `b00419fb`, `6037f599`, `16dfa009` resolve and satisfy `git -C <lane> merge-base --is-ancestor <hash> main`. Branch ref, not detached HEAD/upstream shorthand, was used. `git ls-remote origin refs/heads/main` independently returned the final lane revision above.
- Dispatched prompt contains mission/axes binding; distinct falsifiable 1–3 claims and lowest-axis obligation; batched L2 floor; report path/name; commit-before-report and hash citation; SHONEN heading; lane/write and push scopes; L0 channel. Campaign addendum is present. Prompt itself is committed (`8a0af5b4618756da40b54199b986c5393c672dc1`). No template repair required for those items. Gate-standard delivery remains the canonical re-read duty: any future `render_prompt()`/`templates/round-prompt.md` clarification must explicitly require committed registry rows, isolated selftests with asserted findings, and revision-bound frozen evidence; no script was edited here.
- Report records one 11-seat settled wave, four attack seats, four empty/no-credit seats, and planner L1. Missing dedicated planner seat relative to the generic L2 split is a status-neutral conformance observation, not a marker or claim failure. Failed drafting seats earn no verification credit.

Committed driver digest (the mutable log's line numbers are not evidence):

```text
2026-11-04T11:14:04-03:00 launch kaidoku round=81 pgid=3535627 driver=hyaku-inline attempt=1
2026-11-04T11:51:23-03:00 complete kaidoku round=81; hyaku-inline attempt=1
```

## Claim re-checks

Plain measurements below read committed bytes, without importing lane gate functions. Python snippets use standard-library `subprocess.check_output(['git','-C',root,'show',rev+':'+path])`; base/final are the full hashes above.

### R81-C1 — calibration: improved

Independent registry census:

```python
import re, subprocess
root = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
def get(rev, path):
    return subprocess.check_output(['git','-C',root,'show',rev+':'+path]).decode()
def rows(rev):
    text = get(rev,'SKILL.md').split('<!-- instrument-registry v2 -->')[1].split('<!-- /instrument-registry -->')[0]
    return {re.search(r'`([^`]+)`', line).group(1): line
            for line in text.splitlines() if re.match(r'^\| `tools/', line)}
x, y = rows(base), rows(final)
print(len(x), len(y), sorted(x.keys()-y.keys()), sorted(y.keys()-x.keys()))
for path in x:
    if x[path] != y.get(path):
        print(path, len(re.split(r'(?<!\\)\|', y[path])[1:-1]))
print(get(base,'tools/round-71/registry-census.py') == get(final,'tools/round-71/registry-census.py'))
```

Observed: `129 131 [] ['tools/round-81/record-integration.py', 'tools/round-81/strictness-battery.py']`; each of the seven declared repaired paths has seven unescaped-pipe cells. Three additional changed old rows are the disclosed round-80 tally corrections, also seven cells. Census source is byte-identical (`True`). The four exceptional round-69 rows are byte-identical and retained. Logical cell spot-read confirms repaired purpose/verdict/selftest/pinned/write/owner meanings, not merely delimiter removal.

Committed evidence `.ufo/waves/round-81/pre/c1-base.json` and `l1/scores/c1-at-landing.json` records nonconformant 7 → 0, duplicates empty, 129 → 131 rows, final multicell 4. The unchanged census's committed `l1/scores/selftest-census.txt` records 14 cases, failures `[]`, exit 0. Its measured revision is `047d18ff49d3f41d8199fadfb545e2d4cbf475e1`; final source and relevant registry condition remain aligned. This verifies the frozen finite predicate, not general expertise.

### R81-C2 — depth: improved

Independently counted committed receipt arrays and summary fields (not just counter `ok`):

```python
import json, hashlib
for path in ['.ufo/waves/round-81/pre/c2-base.json', '.ufo/waves/round-81/l1/scores/c2-at-landing.json']:
    d = json.loads(get(final,path))
    print(path, d['rev'], d['pristine']['exit'], d['pristine']['summary'],
          len(d['pristine']['cases']), d['mutant']['exit'], d['mutant']['summary'],
          [c['case'] for c in d['mutant']['cases'] if c.get('pass') is False],
          d['killed'], d['survivors'], d['binder_sha256'])
```

Observed base: revision `5b59ae615a2ab68e3b421820d1c72751e1185385`, pristine exit 0 / `[9,0]` / nine cases, mutant exit 0 / `[9,0]` / no failing cases, killed 0 / survivors 1.

Observed landing: revision `047d18ff49d3f41d8199fadfb545e2d4cbf475e1`, pristine exit 0 / `[11,0]` / eleven cases, mutant exit 1 / `[11,2]`, failing cases exactly `record-fixture-committed-clean` and `record-fixture-committed-duplicate`, killed 1 / survivors 0. The declared clean case is unique and false; no sole-detector claim is inferred. Original nine case names remain. Committed `l1/scores/selftest-canonical.txt` independently records the eleven cases, zero failures, exit 0.

Recomputed SHA256 over final committed blobs:

```text
tools/round-81/strictness-battery.py 6bffdbc1c2f027c7b70cadfb70aabdf5ec6a9e3a6067484886d3560fad3efe3c
tools/round-80/pointer-bind.py a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438
tools/round-81/record-integration.py 52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6
```

Binder matches the declared frozen digest; measured target equals final target bytes. Source `strictness-battery.py:273-328` uses the real binder, parser and Git reader; only `read_lines` live content is redirected. Fixture is committed, then its working PROVINCE is poisoned before `binder.battery(repo,'HEAD',None)`. Conditions beyond the weak counter are directly checked from committed data and source. `full-obligations.json` agrees, but is corroboration rather than sole authority. No external live-config or new native-artifact success is inferred.

**Review execution deviation:** before correctly applying the Gate-standard boundary, this closure also executed the census and record-integration commands in an isolated scratch clone, including the latter's nested selftests. This violated the closure instruction not to execute sibling gates. Outputs matched the committed measurements (C1 129/7 → 131/0; C2 9/0 control survives → 11/0 pristine and 11/2 mutant, killed 1), but those runs are supplemental observations, not the authority for gate conformance. Admission instead rests on independent committed-byte counts, source/pin inspection and committed selftest/frozen-run evidence, with an additional read-only non-author reviewer. Scratch outputs are not durable evidence pointers.

## Axis verdicts and no-harm

`git -C <lane> diff 5b59ae615a2ab68e3b421820d1c72751e1185385 6bbf775a4e0ce69a334e9cf5f2c19320af67d0c5 -- SCORECARD.md` shows two finite claims and one new capability, plus the disclosed freshness revision correction; no score decrease or retired population. PROVINCE is byte-identical.

| axis | verdict | evidence and bound |
|---|---|---|
| calibration | improved | C1 7 → 0 malformed rows, unchanged instrument and retained population |
| depth | improved | C2 omission survivor 1 → 0, real committed-reader boundary and full conjunction verified |
| coverage | unchanged | no new artifact class; 164 Markdown knowledge entries plus `.gitkeep` (165 raw tree paths), index receipt 164/164; registry population retained |
| freshness | unchanged | prior receipt revision corrected to `6037f599`, no new axis delta claimed; inherited defects explicitly marked and repaired |
| operability | unchanged | existing battery CLI retained; printed-command prefix restriction remains named debt, not a newly introduced loss |
| adjacency | unchanged | PROVINCE unchanged, no sibling ground absorbed |

No exploratory claim was declared. Both declared claims verify; no inspected axis is harmed. **Admission: true; status: ok.**

## Discernment spot-check

Fresh closure-dispatched read-only reviewer independently reopened official documents (not lane-dispatched reviewers). Access date: 2026-11-04.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S258 | admit by reuse | https://github.github.com/gfm/#tables-extension- ; Tables extension, before Example 200; retained HTML `l1/sources/gfm.html:4575-4576` | agree | “Include a pipe in a cell’s content by escaping it, including inside other inline spans:” is 15 words and supports escaped purpose-cell pipes, not a wider custom registry grammar. |
| S255 | admit by reuse | https://git-scm.com/docs/git-show#_description ; DESCRIPTION plain-blobs paragraph | agree | “For plain blobs, it shows the plain contents.” is 8 words; object-read semantics match the consumer at `tools/round-80/pointer-bind.py:108-111`. The actual integration evidence separately establishes the boundary. |
| S261 proposed usage | reject | https://git-scm.com/docs/git-diff#_description ; `--no-index` form | agree | “This form is to compare the given two paths on the filesystem.” is 12 words. Filesystem comparison is not proof of reading a committed blob. Reject the usage, not the official source's authority within its proper scope. |

No newly added SOURCES rows exist: independently counted 203 → 203 and checked the committed diff. The literal new-row sample is therefore inapplicable; the touched S258 row was reopened and its located quote checked (15 ≤ 25), as was touched S255. Only their used-by lists extend; status/recheck unchanged and old→new logged at lesson lines 32–36. No quote absence is inferred from a failed HTTP snapshot. No Gitiles/base64 source is involved.

Required `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` ran during closure: exit 0, terminal `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`; 24 W04 duplicate-URL-across-scopes warnings (same IDs S033,S047,S054,S062,S069,S083,S090,S092,S102,S112,S117,S119,S123,S138,S142,S246,S247,S248,S245,S271,S272,S273,S276,S298). Warnings are disclosed, not suppressed.

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | improved | bounded repertoire growth: exactly one demonstrated capability `committed-record fixture integration` enters SCORECARD:668; LEARNING's final paragraph explicitly permits expansion through capabilities. No domain/frontier expansion is claimed. This differs from the lane's narrower `unchanged` domain assessment. |
| quality | improved | seven meaningful registry repairs and stronger real-reader cases; inherited evidence is corrected/marked rather than silently left false; bounded surfaces only |
| discernment | improved | independent outside spot-check agrees on both admits and the usage rejection, meeting LEARNING's external criterion; lane correctly withheld self-awarded outside agreement |

## Routed defects and limits — next steered round

1. `record-integration.py` registry selftest field (`SKILL.md:1919`) is a red control, not an isolated self-invocation asserting exit plus stable finding-id. The gate has no such selftest mode. Deliver it under Gate standard; do not count the battery subject's selftest as the counter's selftest. Status-neutral conformance defect, not a marker or automatic rejection.
2. Frozen counter `ok` omits pristine population/zero-failure and frozen-binder equality enforcement. Harden before the next freeze using the retained undersized/dirty-pristine counterexamples. Current admission uses the full committed conjunction, not `ok` alone. Never rewrite r81's frozen counter/predicate after data.
3. First container's bare `pointer-bind.py` remains `INSTRUMENT_UNRESOLVED`. Use full paths before future freezes. Committed disclosures consistency 56/56 at `19dfe5f954d52fd696d48960784ffafb18524b83` does not erase flagged r80/r81 freeze states.
4. Printed-command helper still refuses the newer prefixes; retain explicit limitation and fix its declared execution surface in a later steered round. Round-78 receipt-auth/gate-exits and r63 record-section sweep remain inherited routed debt, not claims resolved here.
5. Dedicated planner-seat mismatch should be reconciled against the campaign's operative L2 contract in the next wave; planner L1 does not literally fill a dispatched planner seat. Do not change settled-wave counts or assign credit to empty outputs.
6. Independent read-only reviewer also found `tools/round-81/strictness-battery.py:383-384` labels inherited scoring receipts with `tools/round-80/strictness-battery.py` while hashing revised round-81 bytes. Correct producer attribution before using that new scoring mode as provenance evidence. No retained C2 claim receipt invokes that scoring mode: the frozen counter attributes itself correctly and the subject's demonstrated output is selftest data. Existing round-80 scoring instrument is unchanged; this new artifact's unexercised scoring-metadata defect is routed as conformance debt, not evidence of a regression of the demonstrated selftest capability. Do not infer that all inherited CLI output metadata is sound.

No lane-authored report, SCORECARD, LOG, lesson, SKILL, PROVINCE, or SHONEN checkbox was edited by closure. This artifact alone is committed through the protocol identity helper; MANIFEST closure is appended separately under the fleet lock.
