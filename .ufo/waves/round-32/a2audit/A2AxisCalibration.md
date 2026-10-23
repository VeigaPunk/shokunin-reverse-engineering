FALSIFIED (formal counterexample, not exercised): C2v3 target attainment alone does not distinguish truthful capability self-assessment from an explicit capability denial containing the same five anchor words.

# A2AxisCalibration — C2v3 calibration review

- UTC review window: 2026-10-23T06:45:20Z–2026-10-23T06:48:41Z.
- Role: read-only critic. No canonical judgment, admission, integration, or production repair performed.
- Scope: formal distinguishability and calibration-axis fit; no duplicate control, counter, selftest, REA session, build, or carrier execution launched.
- Base: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- C1 freeze: `9a73680af21b002e3b99956c89234b2bbde2a71b`; C2v3 freeze: `f382e3b7978e6091a19ca93277c15a75c0016b43`.
- Fleet statement pin: `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- Unique scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration`.

## Axes and bounded finding

| Axis | Relevant distinction |
|---|---|
| calibration | Primary: does the self-declared repertoire agree with supported repo state, rather than merely contain the expected strings? |
| operability | A resolving historical script path does not prove a currently runnable capability or a capability restoration. This review did not exercise either. |
| freshness | Historical demonstration and present availability must remain distinguishable. The round-17 row itself requires rechecking on REA/Ghidra releases. |
| depth | Original descriptions and limiting conditions carry substance that a five-word overlap does not preserve. |
| coverage | Restoring three summary omissions is not three new domain surfaces or capabilities; C1's ARM64X move is separate and not assessed here. |
| adjacency | No sibling capability absorption is needed or established by this table reconciliation. |

The source definition of calibration is “Self-assessment quality: gaps named honestly, confidence graded, overreach caught” (`AXES.md:15`, local source URL and hash below). A truthful restoration of an incomplete current summary can improve this axis without adding a capability. Conversely, counting copied words alone cannot establish that improvement. Cheapness is not itself a defect; loss of truth discrimination is.

## Evidence actually inspected

### 1. Do-nothing is distinguished from the frozen target

The existing pre-data receipt, not rerun by this seat, records:

```text
utc=2026-10-23T06:09:57Z cmd=python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root . --rev 283aad7f
round-13	P2-mismatch	no `## Capabilities` row matches /source(-curation)? registry/ naming round 13
round-14	P2-mismatch	no `## Capabilities` row matches /quote.{0,40}regression audit/ naming round 14
round-17	P2-mismatch	no `## Capabilities` row matches /Ghidra-session log capture/ naming round 17
round-27	P2-match	row 5 anchor evidence tools/round-27/xpin-attribute.mjs; description words 16
statements=4 match=1 target=4 reverse_mismatch=0
exit=1
```

Source: `.ufo/waves/round-32/before/c2v3-capability-calibration-at-283aad7f.txt:1-7`, SHA-256 `203261b9d73dc49767e2a7e85f3f0150726110e68483f246790ccb900423105a`.

The separately retained selftest receipt records `do-nothing: base section (only round 27)` with `match=1 reverse=0`, and its overall `selftest cases=18 failures=0`, `exit=0`. These are inherited records, not a newly exercised result. The baseline receipt suffices to reject the claim that literally doing nothing meets the target.

The opened worktree `SCORECARD.md` hashes identically to the base Git object. Thus the inspected summary at lines 615–625 and append-only records at lines 2134–2139, 2206–2213, and 2373–2387 are also base evidence, not a post-data reconstruction. The existing correction at line 3116 already identifies the three-summary-row omission; line 3125 distinguishes the now-five-row summary from eight card-wide rows. C2 addresses the summary, not an absence of all three capabilities from the card.

### 2. The outside statement set is four capabilities, not four admitted rounds

At the pinned fleet object, `capabilities_added` contains precisely these four relevant items:

| Round | Item / closure identity |
|---|---|
| 13 | source-curation registry; `admitted=true`, verdict `admitted-capability-only`; reviewer `KaidokuR13Review` |
| 14 | local raw-quote/heading regression audit; `admitted=true`, verdict `admitted`; non-author `hyaku-closure` reviewer |
| 17 | retained REA Ghidra-session log capture; `admitted=true`, verdict `admitted`; non-author `hyaku-closure` reviewer |
| 27 | cross-pin evidence-ID attribution; `admitted=false`, verdict `rejected-honest-stop`; non-author `hyaku-closure` reviewer |

Important provenance distinction: round 27's rejection is not evidence that its capability failed. Its pinned verification records the C1 miss separately from a successful C2 tool recheck. The statement collector reads every `capabilities_added` item, independently of the round admission flag (`c2-capability-calibration-v3.py:68-78`). Dropping round 27 or calling all four rounds admitted would change the frozen population or misstate provenance. Neither is a safe correction.

The source of statement identity is the pinned non-author closure record. Most description words, however, come from the author's base scorecard rows as well (`:129-137`). Repeating those words creates no additional independent capability evidence.

### 3. What the counter actually observes

Opened actual source: `tools/round-32/c2-capability-calibration-v3.py`, verified byte-identical to its C2v3-freeze object and to the instrument hash in `claims-v3.json:48`.

- `:125-137`: descriptions become case-folded sets of alphabetic/hyphenated tokens; the comparison is an intersection of word sets.
- `:154-170`: unique key, exact named round, resolving frozen anchor, and at least five shared words are the row conditions.
- `:178-183`: the reverse condition concerns unmatched rows naming MANIFEST-closed round numbers.
- `:186-201`: revision-dependent inputs are `SCORECARD.md` and the set of tree path names. `exists(p)` is implemented as `p in tree`.
- `:209-211`: four matches and an empty reverse list produce the frozen target and return 0.

No capability artifact contents, semantic polarity, command result, or current demonstration are read by this decision. `claims-v3.json:27` explicitly limits the evidence check to anchor presence/resolution and assigns substantive pointer reopening to wave seats. That limitation is material, not an implicit semantic guarantee.

## Strongest cheap counterexample: polarity is unobservable

This is a paper construction only. No fixture, candidate revision, or control result was created.

Start from the base and leave its five summary rows, including the passing round-27 row, unchanged. Insert these three synthetic rows inside `## Capabilities`, before the next `## ` heading:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| curated source registry for existing REA frontier | Cannot perform this capability: opened scoped study sources ordered. | `corpus/SOURCES.md` | round 13 |
| local raw-quote/heading regression audit | Cannot perform this capability: rejects retained splice wrong section. | `.ufo/waves/round-14/tools/quote-fidelity.py` | round 14 |
| retained REA Ghidra-session log capture | Cannot perform this capability: pinned carrier session retained receipt. | `.ufo/waves/round-17/run-carriers.sh` | round 17 |

The selected five words in each description occur in its actual base description (`SCORECARD.md:2136`, `:2208`, `:2375`). They are selected tokens, not quotations purporting to be source sentences. The three key cells match exactly one frozen key each; the three last cells each name exactly the correct round. Each evidence path is a frozen anchor and an actual base blob (identities below).

[INFERENCE — direct evaluation of the inspected predicates, not observed stdout] Each added row passes. The original round-27 row remains passing. Every added round-naming row is used by its corresponding forward statement; the unchanged baseline reverse list is empty. Therefore the constructed revision would return the unchanged target:

```text
statements=4 match=4 target=4 reverse_mismatch=0
```

with inferred return code 0. This line was **not printed by an executed control**.

Now replace only `Cannot perform` with `Can perform` in those three cells. The five-word overlap, key/round/evidence conditions, and reverse condition remain satisfied. The two opposed self-assessments receive the same result. For a fixed actual capability state, they cannot both be truthful. This establishes a formal false-positive possibility without needing to assume which present capability state is true, and without running a duplicate shortcut control.

Accordingly:

- **Do-nothing versus shortcut:** distinguishable: inherited do-nothing is 1/4; the constructed shortcut is formally 4/4.
- **Shortcut versus truthful reconciliation:** not distinguishable by C2v3 alone. A copied, accurate description can legitimately be the repair, but lexical overlap cannot determine that it is accurate.
- **Failure classification:** the false-positive acceptance is an instrument limitation under the frozen predicate, not permission to repair that predicate after results. No judgment of the actual, not-yet-inspected repair is made here.

## Capability-restoration proof is a separate obligation

Let `C(R)` denote the counter output. With the fixed MANIFEST and base, any two revisions having identical scorecard text and identical path-name sets receive identical `C(R)`, even if the capability script bodies differ. Replacing an anchor's body with inert content while retaining its path is therefore invisible to this counter. This mutation was not performed.

A credible **summary-restoration** chain is:

1. The pinned closure identifies the exact capability, original first-working round, and independent verification.
2. The base append-only row supplies the actual bounded description and evidence pointers.
3. Reopened original evidence supports those same words and limitations; it is not merely a path whose filename exists.
4. The restored current summary faithfully represents that evidence, including historical/current status where relevant.

That is calibration of an existing repertoire record, not acquisition or operational restoration of three capabilities. A claim that a capability has actually been restored to operation would additionally require an appropriate passing demonstration of the real implementation; path membership and word overlap do not provide it. This seat ran no such demonstration and makes no present-operability finding.

The distinction matters locally:

- Round 13's base row explicitly separates source text from held-capability evidence.
- Round 14 limits the audit to retained raw substrings/headings, not semantic support or whole-registry validation.
- Round 17 limits the capture to a polling prefix and an undocumented REA session location, with release rechecks required.
- Round 27's appended correction at `SCORECARD.md:3126` limits attribution to a stored ID-rule fit, not proof of a 6.7.0 run. Its known stale-selftest observation at `:3127` must not be relabeled as capability loss or hidden by this summary repair. It was not rerun here.

## Smallest safe correction; no post-score relabel

**Fixable data defect:** the three supported historical capability records are omitted from the current summary. Restore their faithful descriptions, original first-working rounds, and actual evidence pointers in that summary; preserve original limitations. Treat the append-only rows as historical provenance, not independent corroboration or new round-32 acquisitions. Keep the existing round-27 identity and its mixed round-admission/capability outcome intact.

**Necessary evidential restraint:** report the lexical count as the lexical count, alongside substantive pointer-review findings. A true 3→0 summary-omission reduction can support bounded calibration; merely obtaining four matches cannot. Do not claim improved coverage, new capabilities, current operational restoration, a stagnation-window reset, or axis saturation from that count.

**Frozen boundary:** keep C2v3's counter, predicate, label, anchor set, pin, and `4/4; reverse=0` target unchanged. Its freeze rule (`claims-v3.json:15`) requires misses to remain misses. If a shortcut meets the target, retain that falsification evidence; do not add a semantic gate or change the description threshold under the same claim. If the canonical judge finds the proposed move only lexical bookkeeping, report that result; do not recast it as exploratory or change axes after scores. No canonical decision is issued by this critic.

## Reproducibility and source identities

All Git commands were executed only in the two new scoped scratch clones, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` explicitly unset and an absolute `git -C` argument. No lane/fleet Git or jj write was performed. The clones used `--no-checkout --shared`; they were only sources for immutable-object reads. Metadata commands completed successfully (exit 0); none was a control/test/build. No tool was installed or updated, and no process started here remains running.

### Exact setup argv and observed stdout

```text
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration
[exit 0; no stdout]

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration clone --no-checkout --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin lane
[exit 0; tool output]
Cloning into 'lane'...
done.

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration clone --no-checkout --shared /home/vgpnk/Projects/shokunin fleet
[exit 0; tool output]
Cloning into 'fleet'...
done.

date -u '+%Y-%m-%dT%H:%M:%SZ'
[exit 0; first call stdout]
2026-10-23T06:45:20Z
[same argv, final call stdout; exit 0]
2026-10-23T06:48:41Z
```

### Exact revision argv and full stdout

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane rev-parse HEAD 283aad7f 9a73680a f382e3b7
[exit 0]
f382e3b7978e6091a19ca93277c15a75c0016b43
283aad7fe56d82f4ed4f8e43f099c2e1ceed5525
9a73680af21b002e3b99956c89234b2bbde2a71b
f382e3b7978e6091a19ca93277c15a75c0016b43

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/fleet rev-parse HEAD cef00867ab3279ac2c2d10421e3e62c0e5d693f3
[exit 0]
575bcedac44943fae1cd43f9030aea7662ddb6be
cef00867ab3279ac2c2d10421e3e62c0e5d693f3
```

The fleet clone's HEAD differs from the measurement pin; the explicit pin, not HEAD, was used in every MANIFEST read.

### Exact closure-projection argv and full relevant stdout

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/fleet show cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json | jq -c '.rounds[] | select(.lane == "kaidoku" and ((.capabilities_added // []) | length) > 0) | {round, admitted, verdict, reviewer:.verification.reviewer, spotcheck:.verification.spotcheck}'
[exit 0]
{"round":13,"admitted":true,"verdict":"admitted-capability-only","reviewer":"KaidokuR13Review (all22 rows reopened, admit/reject agree; 2 citation errata appended)","spotcheck":null}
{"round":14,"admitted":true,"verdict":"admitted","reviewer":"hyaku-closure (@m_strong session, non-author)","spotcheck":"kaidoku-shokunin/corpus/lessons/round-14-verifier-spotcheck.md@9719dd232687f5ee78a4ed323b37f8810e833d10"}
{"round":17,"admitted":true,"verdict":"admitted","reviewer":"hyaku-closure (@m_opus session, non-author)","spotcheck":"kaidoku-shokunin/corpus/lessons/round-17-verifier-spotcheck.md@9011581d84527ba34c675f9cf912e54d2e72d470"}
{"round":27,"admitted":false,"verdict":"rejected-honest-stop","reviewer":"hyaku-closure (@m_opus session, non-author)","spotcheck":"kaidoku-shokunin/corpus/lessons/round-27-verifier-spotcheck.md@935c36608008f79e3dea4f1ed191df3c89e3b848"}
```

The full `verification` objects were separately opened from this same pin; longer recheck narratives are paraphrased above, not presented as new executions.

### Exact anchor-identity argv and full stdout

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane ls-tree 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 corpus/SOURCES.md corpus/lessons/round-13.md .ufo/waves/round-14/fixtures/expected.json .ufo/waves/round-14/tools/quote-fidelity.py .ufo/waves/round-14/verification.json .ufo/waves/round-17/run-carriers.sh tools/round-27/xpin-attribute.mjs
[exit 0]
100644 blob b7b68ca703be68c58e1dc9b7b3c9dcc5510405b1	.ufo/waves/round-14/fixtures/expected.json
100755 blob c00c2e641bf35b8143563e38d16ba94e6b5d2d0c	.ufo/waves/round-14/tools/quote-fidelity.py
100644 blob 708333b6d8cd657f341a4de4fc8109cd897a4b18	.ufo/waves/round-14/verification.json
100755 blob 0c14757cb7c50a56ef2c25c7ac2222bc6942294a	.ufo/waves/round-17/run-carriers.sh
100644 blob e9e8ff2875fb2752d975d061a60fa22f46078bf9	corpus/SOURCES.md
100644 blob b588e4ef3617301c21ccb9b0e93013b9300841a1	corpus/lessons/round-13.md
100755 blob 403c3819d3f6ce811e1da945be2c18f5d680ecd3	tools/round-27/xpin-attribute.mjs
```

### Immutable-object SHA-256 argv and full stdout

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane show 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525:SCORECARD.md | sha256sum
[exit 0]
bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3  -

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/fleet show cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json | sha256sum
[exit 0]
2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f  -

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane show f382e3b7978e6091a19ca93277c15a75c0016b43:tools/round-32/c2-capability-calibration-v3.py | sha256sum
[exit 0]
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  -

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane show f382e3b7978e6091a19ca93277c15a75c0016b43:.ufo/waves/round-32/claims-v3.json | sha256sum
[exit 0]
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  -

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2AxisCalibration/lane show 9a73680af21b002e3b99956c89234b2bbde2a71b:.ufo/waves/round-32/claims.json | sha256sum
[exit 0]
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  -
```

### Opened local sources and hashes

Read date for every source below: 2026-10-23 UTC. Lane-relative paths refer to `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/`; MANIFEST is the explicitly pinned Git object, not its moving worktree file.

| Source / location | SHA-256 |
|---|---|
| `file:///home/vgpnk/Projects/shokunin/AXES.md#L15` and `#L57-L64` | `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993` |
| `SCORECARD.md:615-643,2134-2139,2206-2213,2373-2387,3113-3128` (worktree = base object) | `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3` |
| `.ufo/waves/round-32/claims.json:1-49` (worktree = C1 freeze object) | `8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435` |
| `.ufo/waves/round-32/claims-v3.json:15,20-27,48` (worktree = C2v3 freeze object) | `a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d` |
| `tools/round-32/c2-capability-calibration-v3.py:68-211,245-284` (worktree = C2v3 freeze object) | `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f` |
| `.ufo/waves/round-32/before/c2v3-capability-calibration-at-283aad7f.txt:1-7` | `203261b9d73dc49767e2a7e85f3f0150726110e68483f246790ccb900423105a` |
| `.ufo/waves/round-32/before/c2v3-capability-calibration-selftest.txt:1-21` | `211dd1c630d5899696d97b4d9df4cc75b0d32078540ec5ad306896face8877b9` |
| `.ufo/waves/round-17/run-carriers.sh:1-39` | `acc2769354d452733bd7b70b3a09fadead423a7b5b390758ce589e71eb4d093b` |
| `corpus/lessons/round-13.md:1-77` | `b2ae45a87e574a25a0ba1505014b9909d3b3dd1a3741db01e20a9a260994ffb3` |
| Fleet `MANIFEST.json` at `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`, `/rounds` entries with lane `kaidoku`, rounds 13/14/17/27 | `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f` |

Worktree hashes were obtained with these exact successful argv; the hash values are fully retained in the table:

```text
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims-v3.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/claims.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/c2v3-capability-calibration-at-283aad7f.txt /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-32/before/c2v3-capability-calibration-selftest.txt
sha256sum /home/vgpnk/Projects/shokunin/AXES.md /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/run-carriers.sh /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-13.md
```

No held item was inspected or retried. No runtime/model switch was requested or used. No production files, counter, predicate, target, routing, or Git/jj state outside the unique scratch clones were modified. The only lane write was this assigned report.

Report: .ufo/waves/round-32/a2audit/A2AxisCalibration.md
