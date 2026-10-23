# A2ReverseDomain — static C2 statement-set and reverse-domain audit

UTC: 2026-10-23T06:45:20Z–2026-10-23T06:49:29Z.

**Finding: the four frozen keys omit no observed capability item, but the reverse selector omits 11 actual kaidoku closure records because those records identify the lane through maps rather than a scalar `lane` field.** No counter/control was executed; no target-achieving receipt or exercised FALSIFIED result is asserted.

## Axes and bounds

- **Calibration:** statement completeness, treatment of rejected rounds, reverse false-credit detection, and round-identity provenance.
- **Coverage/depth:** not evaluated or changed by this seat. Historical-record coverage below is a property of C2's calibration measurement, not a new owned-axis score.
- Static inspection only. No clone, counter import/execution, selftest, build, REA call, carrier execution, judge/runtime invocation, repair, or Git/jj write. The held item was not inspected. No tools were installed or updated.
- Only this report is written. All started command processes finished; no child process remains to kill.

## Pinned sources

All sources reopened on 2026-10-23. Locations below are local source URLs; revisions and SHA-256 identify the actual bytes, not merely their worktree names.

| ID | Source URL | Revision | SHA-256 |
|---|---|---|---|
| M | `file:///home/vgpnk/Projects/shokunin/MANIFEST.json` | `cef00867ab3279ac2c2d10421e3e62c0e5d693f3` | `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f` |
| S | `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md` | `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525` | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` |
| K | `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py` | `f382e3b7978e6091a19ca93277c15a75c0016b43` | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| F | `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json` | `f382e3b7978e6091a19ca93277c15a75c0016b43` | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| C1 | `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json` | `9a73680a` | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |

No sandbox revision exists: this assignment expressly excluded a control clone. The source revisions above are the audited revisions.

## 1. Forward statement selection: exhaustive at this pin

The immutable MANIFEST contains 34 records with scalar `lane == kaidoku`. Their complete `capabilities_added` item count is four. Broadening the census to records identifying kaidoku through `lanes` or `lane_rounds` produces 45 related records but **still four items**. There is no fifth observed capability item hidden by the scalar-lane selector or by a frozen key.

Full relevant statement output from the immutable JSON census (array indices are zero-based):

| MANIFEST index | Round | Admitted | Capabilities item, verbatim | Matching frozen key round | Source |
|---|---:|---|---|---:|---|
| 315 | 13 | true | source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | 13 | M:6311 |
| 332 | 14 | true | local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | 14 | M:7195 |
| 358 | 17 | true | retained REA Ghidra-session log capture | 17 | M:8293 |
| 467 | 27 | false | cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | 27 | M:13932 |

Each item matches exactly its own round's frozen pattern. K:146–149 checks every selected item and returns a pin error if a key does not cover it; K:197–199 also rejects an item-count change. These are fail-closed checks, not silent key-based removal of unmatched MANIFEST items.

The base card has eight capability-table data rows overall: five in the summary at S:619–623 and three outside it at S:2136,2208,2375. The three outside rows correspond to the round-13/14/17 statements. The summary contains the round-27 first-cell/round candidate. This is a structural observation, not an execution of the full anchored-description/evidence predicate.

**Smallest safe correction:** none to the four keys or target. Do not invent an omitted capability item, and do not equate this four-item ledger with the lane's entire historical repertoire.

## 2. Rejected rounds: included correctly, without converting rejection into admission

At the pin, scalar-lane closures with `admitted: false` are rounds **24, 27, 28, 29**. All four enter K's reverse closed set. Round 27 also contributes the fourth forward statement; rounds 24/28/29 contribute no capability item.

Reopened source quotes:

- K:74: `if r.get("admitted") is not None:`
- K:76–77: `for item in r.get("capabilities_added") or []:` / `stmts.append((r["round"], item))`
- M:13916–13917: `"admitted": false` / `"verdict": "rejected-honest-stop"`

Thus neither forward capability selection nor reverse closure membership requires admission to be true. M:13931–13933 explicitly credits the attribution capability despite the round-level rejection. Omitting round 27 on a truthiness filter would lose observed credited state; the frozen code does not make that mistake.

**Smallest safe correction:** preserve the distinction between a credited capability and admission of its containing round. No selector repair is indicated for these four rejected rounds.

## 3. Counterexample: real closure records disappear from the reverse domain

The reverse domain is **not all pinned kaidoku closures**. K:71–75 first applies a scalar field filter:

```python
if r.get("lane") != "kaidoku":
    continue
if r.get("admitted") is not None:
    closed.add(r["round"])
```

The pinned MANIFEST also contains the following 11 records. Every one has `type: closure`, `admitted: true`, `lanes: {kaidoku: ok}`, and a matching `lane_rounds` entry; every one lacks scalar `lane` and `capabilities_added` fields. Their notes identify arc3-loop1 rounds. These are observed existing closure records, not fabricated fixtures.

| MANIFEST index | Round / `lane_rounds.kaidoku` | Immutable source span |
|---:|---:|---|
| 252 | 1 | M:4360–4383 |
| 255 | 2 | M:4432–4455 |
| 260 | 3 | M:4553–4576 |
| 262 | 4 | M:4602–4625 |
| 265 | 5 | M:4680–4703 |
| 275 | 6 | M:4924–4947 |
| 280 | 7 | M:5050–5073 |
| 283 | 8 | M:5129–5152 |
| 286 | 9 | M:5208–5231 |
| 290 | 10 | M:5317–5340 |
| 292 | 11 | M:5362–5385 |

Concrete reopened example: M:4924–4947 is round 6, type closure, `lanes.kaidoku == ok`, `lane_rounds.kaidoku == 6`, admitted true. Its note starts with the short quote `arc3-loop1-round6 ADMITTED` at M:4946. There is no scalar `lane` in that complete object. K therefore discards it before inspecting admission.

Full relevant domain census:

```text
TOTAL_KAIDOKU_RELATED_RECORDS 45
TOTAL_KAIDOKU_RELATED_CLOSURES 31
EXACT_LANE_CAPABILITY_ITEMS 4
RELATED_LANE_CAPABILITY_ITEMS 4
CLOSED_DOMAIN [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
ADMITTED_FALSE_DOMAIN [24, 27, 28, 29]
MISSING_ADMISSION_ROWS 14
```

The last count refers to the 34 scalar-lane records: 14 historical train records lack admission, while the other 20 are closures. It does not describe the 11 omitted map-identified closures, which all have admission true.

At K:180 the reverse operation is the short quote `named = rounds_named(cells[-1]) & closed`; K:181 only flags an unused row if that intersection is nonempty. **[INFERENCE, static code consequence; not a control run]** An extra summary row credited to actual arc3 round 6 cannot trigger this reverse check, because 6 is absent from `closed`. Its first cell need not match any frozen capability key. This demonstrates reverse-domain undercoverage independently of whether the four forward rows have been repaired. No complete passing scorecard was constructed or measured here.

**Impacted axis:** calibration, specifically false-credit sensitivity for already-observed closure state. This is a selector/schema defect under an assertion covering every kaidoku closure; it is not an observed failure of forward key completeness.

**Smallest safe correction:** report this missing reverse-domain coverage under the unchanged freeze. Do not edit the counter, predicate, keys, pin, or target in this attempt. A future separately frozen measurement would need explicit normalization of scalar/map lane identity before closure selection; it would also need the namespace treatment below. A mere scalar-filter change is not a safe current repair.

## 4. Historical summary rows: bounded exclusion, but not a namespace-aware join

Exact static parsing of every base summary row's last cell gives:

| S line | Observed last cell | Parsed integer | Intersection with K's `closed` |
|---:|---|---:|---|
| 619 | `luna-round-6` | 6 | empty |
| 620 | `luna-round-8` | 8 | empty |
| 621 | `arc2-loop1-round2` | 2 | empty |
| 622 | `arc2-loop1-round7` | 7 | empty |
| 623 | `round 27` | 27 | 27 |

Four genuine historical summary rows are outside both the four forward items and the effective reverse domain. That limitation is consistent with F:27's declared exclusion of luna/arc summary rows from the statement set. It is **not evidence that those capabilities were rejected, removed, or reverified**. Preserving them is not duplicate credit for one of the four statements.

However, the implementation does not distinguish luna/arc namespaces. K:54's regex extracts a `round` suffix anywhere in a cell; K:140–141 returns only integers. Actual source shows that integer identities are not globally unique:

| Integer | First pinned record | Other pinned record |
|---:|---|---|
| 12 | M:2840–2853: train record whose note begins `luna-round-8 of 10` | M:5406–5445: kaika closure for arc3-loop1-round12 |
| 13 | M:2854–2867: train record for luna round 9 | M:6280–6322: kaika source-registry closure |
| 14 | M:2868–2882: train record for luna round 10 | M:7167–7209: hyaku quote-audit closure |

The ledger's scalar round 12 and a scorecard tag's luna-round-8 identify the same old train record at M:2840–2853, while another scalar round 12 is an unrelated later closure. Consequently a general reverse join cannot safely use only the integer suffix. Conversely, admitting all map-identified old closures into the current integer set would also sweep the four historical summary suffixes 2/6/7/8 into that set, even though their source eras differ from the arc3 closures. Those are distinct provenance problems, not a reason to delete historical summary rows.

**[INFERENCE]** Current exclusion of the four historical rows is achieved by the observed scalar-field/domain shape, not by an enforced historical-namespace rule. It must not be generalized into namespace correctness or whole-repertoire calibration.

F:27's description of MANIFEST coverage as hyaku-numbered rounds only is too broad as a factual account: M:6283 identifies the round-13 statement's campaign as `kaika`, and the ledger contains the older train and map-identified closure records above. This does not invalidate the explicitly frozen four-item denominator, but it matters when describing what `reverse_mismatch=0` establishes.

**Smallest safe correction:** retain the old rows and describe the result narrowly as alignment of the four explicit pinned capability items. Disclose that the reverse check covers scalar-lane closure numbers 12–31, not all kaidoku closures or historical namespaces. Any stronger completeness/provenance assertion remains unsupported by this instrument; disposition belongs to the canonical judge, not this seat.

## Command and evidence receipt

All external commands below exited **0**, with empty stderr. Git subprocess environment removed `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE`; `GIT_OPTIONAL_LOCKS=0`. Every Git argv used an absolute `-C` path. The commands only read objects. Python Eval performed JSON decoding, source-span extraction, and regex/data enumeration; it did not import or execute K. The relevant stdout is reproduced in the tables and census above; raw source output sizes/hashes below identify the complete immutable blobs without pasting unrelated MANIFEST prose.

Exact argv, UTC receipt times, and stdout:

1. 06:45:20Z: `["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]` → `2026-10-23T06:45:20Z`.
2. 06:45:49.842831Z: `["git", "-C", "/home/vgpnk/Projects/shokunin", "show", "cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json"]` → 1,242,275 stdout bytes; SHA-256 M above.
3. 06:45:49.841505Z: `["git", "-C", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "show", "283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md"]` → 274,232 stdout bytes; SHA-256 S above.
4. 06:45:49.841337Z: `["git", "-C", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "show", "f382e3b7:tools/round-32/c2-capability-calibration-v3.py"]` → 15,665 stdout bytes; SHA-256 K above.
5. 06:45:49.841078Z: `["git", "-C", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "rev-parse", "--verify", "f382e3b7^{commit}"]` → `f382e3b7978e6091a19ca93277c15a75c0016b43` followed by newline.
6. 06:48:36.331517Z: `["git", "-C", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "show", "f382e3b7978e6091a19ca93277c15a75c0016b43:.ufo/waves/round-32/claims-v3.json"]` → 4,870 stdout bytes; SHA-256 F above.
7. 06:48:36.331802Z: `["git", "-C", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "show", "9a73680a:.ufo/waves/round-32/claims.json"]` → 8,341 stdout bytes; SHA-256 C1 above.
8. Worktree hash command: `["sha256sum", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md", "/home/vgpnk/Projects/shokunin/MANIFEST.json"]`. Full stdout:

```text
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py
bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md
2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f  /home/vgpnk/Projects/shokunin/MANIFEST.json
```

9. 06:49:29Z: `["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]` → `2026-10-23T06:49:29Z`.

No build/test timeout, fixture-size, disk-rebuild, or memory-limit condition was triggered: no fixture or build was launched. A broad filename-discovery glob timed out; direct root listing located MANIFEST, and immutable-object reads completed normally. There was no refusal, model switch, held-item retry, or unresolved data-access blocker.

Report: .ufo/waves/round-32/a2audit/A2ReverseDomain.md
