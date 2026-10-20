# Round 18 registrations vs reports

Axes: calibration, freshness, depth.

## Observations

Across both requested revisions, the registration-to-report crosswalk is identical:

| Revision | Wave | Registered members / unique non-null agent IDs | `.md` reports | Matched | Missing registered reports | Extra report basenames |
|---|---:|---:|---:|---:|---|---|
| `a245bb00c581ae3423a10a055c77d4bc873918df` | W1 | 89 / 89 | 89 | 89 | 0 | 0 |
| `a245bb00c581ae3423a10a055c77d4bc873918df` | W2 | 98 / 98 | 94 | 94 | `GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY` | 0 |
| `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` | W1 | 89 / 89 | 89 | 89 | 0 | 0 |
| `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` | W2 | 98 / 98 | 94 | 94 | `GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY` | 0 |

Registration sources identify the report directories and member maps at `kaidoku-shokunin/.ufo/waves/round-18/wave1-registration.json:2-9,987-989` and `wave2-registration.json:2-9,1086-1088`; the four W2 registered entries are at `wave2-registration.json:64-67,86-89,97-100,933-936`. Report files are the `.md` files under the corresponding `w1/` or `w2/` directory; the counts below exclude the auxiliary `swarm-registry.json`. The matched/missing sets show every W1 registration has exactly one same-basename report, and W2 has 94 same-basename reports, four missing, no extras. **Inference:** 187 registered seats (89+98) correspond to 183 reports (89+94), a net gap of four.

**Command and exit code (same crosswalk run against both revisions and waves):**
```sh
python3 -I -B -c 'import json,subprocess as s; root="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; base=".ufo/waves/round-18/"; revs=("a245bb00c581ae3423a10a055c77d4bc873918df","8a8da7e19375aadc66c6bcbff0bbcbb596048fb0"); [print("REV",r,"WAVE",w,"registered",len(m),"unique non-null IDs",len({v.get("agentId") for v in m.values()}-{None}),"markdown reports",len(rep),"matched",len(set(m)&rep),"missing",sorted(set(m)-rep),"extra",sorted(rep-set(m))) for r in revs for w in (1,2) for m in [json.loads(s.check_output(["git","-C",root,"show",f"{r}:{base}wave{w}-registration.json"],text=True))["members"]] for lines in [s.check_output(["git","-C",root,"ls-tree","-r","--name-only",r,"--",f"{base}w{w}"],text=True).splitlines()] for rep in [{p.rsplit("/",1)[1][:-3] for p in lines if p.endswith(".md")}]]'
# EXIT=0
```
Output:
```text
REV a245bb00c581ae3423a10a055c77d4bc873918df WAVE 1 registered 89 unique non-null IDs 89 markdown reports 89 matched 89 missing [] extra []
REV a245bb00c581ae3423a10a055c77d4bc873918df WAVE 2 registered 98 unique non-null IDs 98 markdown reports 94 matched 94 missing ['GatePRODUCERREV', 'GateSUMSRUNLOG', 'ShonenLines', 'TruthREGISTRY'] extra []
REV 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 WAVE 1 registered 89 unique non-null IDs 89 markdown reports 89 matched 89 missing [] extra []
REV 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 WAVE 2 registered 98 unique non-null IDs 98 markdown reports 94 matched 94 missing ['GatePRODUCERREV', 'GateSUMSRUNLOG', 'ShonenLines', 'TruthREGISTRY'] extra []
EXIT=0
```

The registration files and report directories do not differ between the two requested commits. **Command:**
```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --name-status 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 a245bb00c581ae3423a10a055c77d4bc873918df -- .ufo/waves/round-18/wave1-registration.json .ufo/waves/round-18/wave2-registration.json .ufo/waves/round-18/w1 .ufo/waves/round-18/w2
# EXIT=0; no output
```

## Comparison with the scorecard and fleet erratum

- **Observation:** `SCORECARD.md:2462` correctly gives W1 as 89 seats and 89/89 reports; it also notes `SwissMisreadTool` aborted after writing its report. This is a report-presence count, not a claim that all 89 ended normally; the author-side outcome audit records 88 `stop` and one `aborted` final assistant state at `w2/WaveEvidenceComplete.md:59-65`.
- **Observation:** The scorecard's W2 clause is an integration-time status: 98 seats, one dead (`GateSUMSRUNLOG`), and four not yet returned then (`GatePRODUCERREV`, `TruthREGISTRY`, `DecisionRuleApply`, `ShonenLines`), `SCORECARD.md:2462`. The fleet report later records `DecisionRuleApply` as returned late and integrated, alongside `AetherDualPath` and `SiblingOverlap2`, while `TruthREGISTRY` and `ShonenLines` were still not returned at integration (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:83-85`). Thus `DecisionRuleApply` is not among the four missing report files.
- **Observation:** The fleet erratum updates the terminal outcome: `TruthREGISTRY` later died; W2 had three dead seats (`GateSUMSRUNLOG`, `GatePRODUCERREV`, `TruthREGISTRY`), and `ShonenLines` had not returned when the erratum was written (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:99-101`). Those four names exactly equal the four W2 registrations with no `.md` report at either commit. The scorecard and erratum therefore reconcile when the integration-time list is separated from later outcomes.

No tools were installed or updated.
