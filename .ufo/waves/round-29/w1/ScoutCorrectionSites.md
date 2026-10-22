# Round 29 w1 — earlier corpus statements the round-29 findings bear on

Seat `KaidokuR29.ScoutCorrectionSites`. Assignment: find earlier corpus statements (at measured tip
`18be864a528873b2b70d8c94e31f880290249e90`) about openchain's `filtered` flag, the canonical list
("the signature it keeps", "canonical signature"), the round-25 rule's recall, or REA's inferred
argument types (`bytes32`/`uint256`, `string`/`bytes`) that round 29 corrects or sharpens. This
report lists them; **no edits were made to any lane file**.

Instruments: `read`, `grep -n` and `git cat-file`/`git show` (read-only) plus three offline Python
recomputations over committed bytes. No network, no REA, no LSP: the targets are Markdown prose, a
JSON dataset and a TSV, which no language server answers, so text search is the only instrument and
its output is not presented as semantic proof of code (the code rule itself is S084/S087, already
read by R28-C2/R29-C2, not re-opened by this seat). No tools were installed. Every command below
ran in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Verdicts used: **CORRECTS** (the earlier text is wrong or superseded as stated), **SHARPENS**
(true but incomplete or sample-bound in a way round 29 changes), **CONFIRMS** (round 29 supports it
unchanged), **EXECUTED** (a proposed next step that round 29 carried out).

Labeling: every “Current text” quote is an observation of the named file's bytes at the tip
revision (E1); every count in a Bearing is an observation carrying its evidence block below;
causal or generalising statements in a Bearing are inference unless the quoted round-29 entry
states them as its own reading. Items marked unknown are listed under Unknowns.

## Evidence blocks

### E1 — every cited surface is the tip revision's bytes

Command (utc 2026-10-22T20:24:18Z, exit 0): for each cited file, compare
`git cat-file -p 18be864a…:<f> | sha256sum` with `sha256sum <f>`.

```
MATCH PROVINCE.md bc153a5c89f5fae5892fb6b1900fe373cc48da3ecffa3a87e7f30ae2d8300748
MATCH SKILL.md 889b0d04ed2f55b10e922c7dc2c9e3292526788e2a16005981856e8954630c8b
MATCH corpus/SOURCES.md 68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed
MATCH corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md cba9f566c76dc257dc58be385e4602fc582fb5f2beea498bb0d5e0e38f6d20c9
MATCH corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md 964e19bac43d089447945df13492af154bbc05cc09954502c0fe8aa66c5be9bd
MATCH corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md 3d4816078434e47aff7f7cc5e0721e6ed0436eb7e42c033384abeee044925826
DRIFT corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md rev=9233ac85b2c94790e2da5a2fd14986b59692fca09cd93db93329e6b6f97ff1d2 wt=39d8eaff2a5964fb58de387aca6d85b81d03757894c2d73ef9cba997fb80fe60
MATCH corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md 3a66ee2f927ff19b9e001de174c3dc4eeb0c496137cb068ba81a57ff152fdc4d
MATCH corpus/evidence/round-29/c2/canonical-signatures.json 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2
MATCH corpus/evidence/round-29/c2/selectors.tsv 3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d
MATCH corpus/evidence/round-29/c1/tally.json dc1eddf0a03f36c9e7eaa70fa8f63264aa05fa14e65428b5c6bee125cfa9b1da
```

Observation: the round-29 C1 entry changed under this seat at 20:24Z (sibling edit; `git diff`
shows a 2-line clarification of the `string[]` example at its lines 53-54). All line numbers and
quotes below for that file are the **tip revision's** bytes (printed by `git show` in E9), not the
moving worktree.

### E2 — independent recomputation of the R29-C2 `filtered` rule

Command (utc 2026-10-22T20:24:18Z, exit 0): `python3 -I -B
/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScoutCorrectionSites/verify-c2-rule.py` — reads only the
pinned list, `selectors.tsv` and the 178 saved responses, shares no code with the lane counter.

```
canonical {"entries": 53, "mismatches": 0, "no_candidate": 4, "observed_true": 38, "predicted_true": 38, "selectors": 26}
c1        {"entries": 199, "mismatches": 0, "no_candidate": 0, "observed_true": 0, "predicted_true": 0, "selectors": 152}
all       {"entries": 252, "mismatches": 0, "observed_true": 38, "predicted_true": 38, "selectors": 178}
```

Observation: independent of the lane counter, the code rule `filtered = name !== kept signature`
(for keys carrying one) predicts all 252 saved flags.

### E3 — the canonical list's shape recomputed

Command (utc 2026-10-22T20:24:18Z, exit 0): `python3 -I -B …/verify-miskeyed.py` — keccak via
`tools/round-25/a2/resolve-selectors.py` `selector_of`, loaded by path.

```
keys 36
no_signature 5 ['0x60806040', '0x60a06040', '0x60c06040', '0x60e06040', '0x61010060']
mis_keyed 6
0x0d0f30c6 keeps token1() which is 0xd21220a7
0x1a686502 keeps uniswapV3SwapCallback(int256,int256,bytes) which is 0xfa461e33
0x89035730 keeps flash(address,uint256,uint256,bytes) which is 0x490e6cbc
0xc45a0155 keeps mint(address,int24,int24,uint128,bytes) which is 0x3c8a7d8d
0xfc6f7865 keeps uniswapV3MintCallback(uint256,uint256,bytes) which is 0xd3487997
0x8abf6077 keeps proxyOwner() which is 0x025313a2
```

### E4 — R29-C1 abstention causes recomputed from the committed tally

Command (utc 2026-10-22T20:24:18Z, exit 0): `python3 -I -B …/verify-c1-reasons.py`.

```
rows 152
primary_no_name 30
args_mismatch_rows 27
args-match-and-still-ambiguous 3
bytes32-read-as-uint256 24
string-read-as-bytes 3
```

### E5 — cited saved responses

Command (utc 2026-10-22T20:24:38Z, exit 0): `python3 -I -B …/verify-examples.py`.

```
0xc45a0155 entries=2 filtered_true=2
    True factory()
    True transfer_attention_tg_invmru_ec11fa8(uint256,bool)
0x60806040 entries=6 filtered_true=6
0x60a06040 entries=4 filtered_true=4
0x7ecebe00 entries=3 filtered_true=0
    False nonces(address)
    False _$_$$_$__$$$$$$$$__$__$$_$$$_$$$(address)
    False transfer_attention_tg_invmru_5811b86(uint256,address,address)
0xd21220a7 entries=4 filtered_true=0
    False token1()
0x0d0f30c6 entries=0 filtered_true=0 raw_is_null=True
```

### E6 — the round-29 counters' own receipts at the tip

Command (utc 2026-10-22T20:24:38Z, `cat`, exit 0; counter runs at 20:16:35Z/20:16:37Z, each exit 0):

```
c1: primary rule openchain_sole_unfiltered_args_consistent: named 122, right 122, wrong 0, no_name 30
    runs_ok=16/16 rows_complete=152/152 tally_equal=1 entry_ok=1   exit=0
c2: responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1   exit=0
```

### E7 — line locations

Commands (utc 2026-10-22T20:24:18Z, each exit 0): the `grep -n` calls recorded in
`out/transcript.txt` (`grep-n` on PROVINCE.md, SKILL.md, the three knowledge entries, SOURCES.md).

### E8 — SKILL.md has no bearing statement

Same grep (exit 0): `grep -n -E "filtered|canonical|openchain|4byte|selector|EVM" SKILL.md` matches
only capability, custody, Go-selection and registry lines — e.g. `54:| EVM bytecode | …
held (selector recovery) |`, `286:  r4, the EVM bullet's Vyper wording depended on C1's corpus
entry`, `492:materializes the existing selector law; it does not discover a new recovery`, and the
round-28 gate rows `954:`/`955:`. None states the `filtered` rule, the canonical list's contents,
a recall figure, or an argument-type claim. **No SKILL.md correction site.**

### E9 — tally rules and tip-revision line numbers

Command (utc 2026-10-22T20:25:24Z, exit 0): `python3 -I -B -c …` over
`corpus/evidence/round-29/c1/tally.json`, then `git show 18be864a…:<entry> | awk` for the two
round-29 entries.

```
fourbyte_first named 152 right 116 wrong 36 no_name 0
fourbyte_sole_args_consistent named 123 right 123 wrong 0 no_name 29
openchain_first named 152 right 152 wrong 0 no_name 0
openchain_sole_unfiltered named 116 right 116 wrong 0 no_name 36
openchain_sole_unfiltered_args_consistent named 122 right 122 wrong 0 no_name 30
args_match_abi 125 truth_in_some_database 152
```

(Full tip-line excerpts are in `out/tally-and-tip-lines.txt`.)

## Findings

### PROVINCE.md (Frontier)

**P-1 — `PROVINCE.md:94` — CORRECTS (superseded).**
Current text: “openchain's `filtered` flag is set only for selectors on Sourcify's 36-key
canonical list; it was re-observed on 10 of those keys, the deployed revision is not identified,
and the test is not held out”.
Bearing: R29-C2 froze the **26 canonical keys with no openchain response anywhere in the lane at
the base** and fetched once after the freeze (preseen `overlap=0`): 178 selectors, 252 entries,
`predicted_true=38`, mismatches 0, both branches unseen (E2, E6). The “not held out” and “10 of
those keys” clauses describe round 28 only and are now superseded. The first clause is also
imprecise: the code sets the flag **per candidate under** a key, by comparing the name with one
stored string (`filtered = name !== expectedCanonical.signature`), so on the 5 keys with no stored
signature every candidate is filtered (E3, E5) — not “set for selectors”. The deployed revision
remains unidentified (unknown, U2).
Round-29 evidence: `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md:15-34,65-71`;
E2, E3, E5, E6.

**P-2 — `PROVINCE.md:91-94` — SHARPENS.**
Current text: “names are labelled candidates from saved signature-DB lookups, never verified” and
the round-28-only numbers (“named 137, right 137, wrong 0”).
Bearing: R29-C1 adds a second out-of-sample point on **published** interfaces: named 122 of 152
(80%), right 122, wrong 0, no name 30; 27 argument-list mismatches all abstained
(`…r29-evm-fresh-selector-naming.md:62-63`); the 30 no-name
rows split 24 `bytes32`, 3 `string`, 3 spam ties (E4, E6, E9). “Never verified” still holds.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:33-43,97-101`.

### corpus/SOURCES.md (mined rows; the ticket named S085's teaches cell)

**S-1 — `corpus/SOURCES.md:91`, S085 teaches field (7th pipe field) — CORRECTS.**
Current text: “The 36 selectors whose candidates the service filters at that commit, **with the
signature it keeps for each**; not the deployed list”.
Bearing: 5 of the 36 keys carry no `signature` at all, and 6 of the remaining 31 kept strings do
not hash to their own key (`0x0d0f30c6` keeps `token1()`, which is `0xd21220a7`; the other five in
E3). “With the signature it keeps for each” therefore overstates the list: 5 have none and 6 keep
another selector's signature. The row's own value column (36 keys; `0xd55ec697` `upgrade()`) is
unchanged.
Round-29 evidence: `…r29-openchain-filtered-unseen.md:25-34`; E3.

**S-2 — `corpus/SOURCES.md:91`, S085 teaches field — SHARPENS.**
Current text: “Only these 36 selectors can ever carry `filtered: true`; for any other selector the
flag is false by construction (S084), so a filter step adds nothing there.”
Bearing: the first clause holds (E2: 0 of 199 entries filtered on the 152 non-canonical c1
selectors). “Adds nothing there” is true but incomplete: on 6 of the 36 keys the filter step is
actively wrong — it drops the true name (`factory()` under `0xc45a0155` is `filtered: true`, E5) —
and on the 5 no-signature keys it drops every candidate. The teachable rule needs the added check
“kept signature hashes to the key”.
Round-29 evidence: `…r29-openchain-filtered-unseen.md:65-71,94-98`.

**S-3 — `corpus/SOURCES.md:90`, S084 teaches field — SHARPENS.**
Current text: “A candidate is marked filtered only when its selector is a key of the canonical list
(S085) and its name differs from that key's signature; every other candidate keeps `filtered:
false`, and `filter=true` drops only the marked ones.”
Bearing: for the 5 keys without `signature` the comparison is `name !== undefined`, so every
candidate is marked without any name comparison; “that key's signature” can be a string belonging
to another selector (6 cases, E3); and when the kept string is not among the stored candidates,
every candidate is marked and a `filter=true` request returns nothing (`…unseen.md:23-24`). The
last clause (“drops only the marked ones”) remains true.
Round-29 evidence: E2, E3, E5.

### corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md

**F-1 — `…r28-openchain-filtered-flag.md:5` — CORRECTS.**
Current text: “# openchain's `filtered` flag marks only non-canonical names of 36 canonical
selectors”.
Bearing: under the 6 mis-keyed keys the flag marks the true name too — `factory()` under
`0xc45a0155` is `filtered: true` (E5), and it is R29-C1 carrier n08's ABI name for that selector; under the 5 `system:magic` keys there is no canonical name to be
“non-canonical” and every candidate is marked (E5: 6/6 and 4/4). The unconditional title fails for
11 of the 36 keys.
Round-29 evidence: `…unseen.md:20-34,67-71`.

**F-2 — `…r28-openchain-filtered-flag.md:16-19` — SHARPENS.**
Current text: “it sets each candidate's `filtered` to `name !== canonical signature` (`:47-48`) …
With `filter=true`, the service then drops the candidates marked `filtered`.”
Bearing: round 29 names the right-hand side `expectedCanonical.signature` and pins three
consequences (no-signature keys; kept signature absent → `filter=true` returns nothing; 6 mis-keyed
strings). The comparison is against an arbitrary stored string, not a validated canonical name.
Round-29 evidence: `…unseen.md:15-34`; E3.

**F-3 — `…r28-openchain-filtered-flag.md:21-22` — SHARPENS.**
Current text: “It is true exactly when the selector is one of the 36 canonical keys and the
candidate's name differs from that key's kept signature.”
Bearing: literally code-accurate, but “that key's kept signature” may be another selector's
signature (6/31, E3), and absent for 5 keys (the entry itself notes this at 22-24). The sentence
must not be read as “the kept signature is this selector's canonical name”.
Round-29 evidence: E3; `…unseen.md:25-34`.

**F-4 — `…r28-openchain-filtered-flag.md:43-45` — SHARPENS.**
Current text: “The filter step only acts on the 36 canonical selectors. The 59 flagged entries sit
there; one example is `__$$____$_$___$_$_$_$_$__$$___()` under `0x06fdde03` `name()`.”
Bearing: “only acts on the 36” is true but understates the consequence: on 6 of them the step
removes the true name, and on the 5 magic keys it removes everything. A filter step is not merely
“extra flagged junk”; it can make the true name unrecoverable (`factory()` for `0xc45a0155`).
Round-29 evidence: `…unseen.md:65-71`.

**F-5 — `…r28-openchain-filtered-flag.md:59-62` — SHARPENS (alternative disconfirmed).**
Current text: “In all 10 responses the canonical name was listed first, so "canonical key and not
first in the list" fits the data equally well”.
Bearing: round 29's never-fetched keys separate the alternatives in both directions: under
`0xc45a0155` the **first** candidate `factory()` is filtered (so “not first” predicts false), and
on the c1 set the rule predicts false for all 199 entries while several selectors have non-first
spam (e.g. `0x7ecebe00`'s three candidates are all false), so “mark every non-first candidate”
would mismatch. R29-C2's Separation section makes the same argument.
Round-29 evidence: `…unseen.md:75-78`; E5.

**F-6 — `…r28-openchain-filtered-flag.md:73-74` — EXECUTED (superseded next step).**
Current text: “26 of the 36 canonical keys stay untested. A held-out test would freeze a list built
from those 26 keys before fetching anything.”
Bearing: R29-C2 did exactly that — the 26 keys with no openchain response in the lane at the base,
frozen at `dbd87cfa` before any fetch, `overlap=0` — and obtained 53 entries, 38 predicted-true,
mismatches 0 (E2, E6). The limitation is closed for the flag rule; the deployed-revision question
stays open (U2).
Round-29 evidence: `…unseen.md:36-53`.

**F-7 — `…r28-openchain-filtered-flag.md:78-81` — CORRECTS the first bullet.**
Current text: “Read `filtered: true` as "not the canonical name for one of 36 well-known
selectors". It is not a general spam verdict.”
Bearing: for the 6 mis-keyed keys a `filtered: true` candidate **may be the true name** (`factory()`
under `0xc45a0155`), so the suggested reading mislabels it; the second bullet (“`filtered: false`
… is the default” for non-canonical selectors) is confirmed (E2: 199/199 false). The round-29 Use
section replaces the gloss with “differs from the one string Sourcify stored” plus the hash check.
Round-29 evidence: `…unseen.md:65-71,94-98`; E5.

### corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md

**T-1 — `…r25-evm-selector-name-resolution.md:29-31` — SHARPENS.**
Current text: “The openchain lookup takes a `filter` parameter described as "Whether or not to
filter out junk results"; each match carries `filtered` and `hasVerifiedContract` flags (S076).”
Bearing: the API description must not be read as junk filtering. `filter=true` drops candidates
that differ from one stored string; under the 6 mis-keyed keys it drops the true name, and under
the 5 no-signature keys it drops every candidate (`…unseen.md:20-24`; E5). S076's wording is the
service's own gloss, now superseded by S084/S087 code for the lane's use.
Round-29 evidence: E2, E3, E5.

**T-2 — `…r25-evm-selector-name-resolution.md:81-84` — SHARPENS (recall).**
Current text: “On these carriers that label went to 49 of 69 rows (31 of 43 distinct) with none
wrong, and 20 rows got no label.”
Bearing: r29 gives a second, pre-registered out-of-sample recall point on published names: 122 of
152 rows named (80%), none wrong, 30 no-name; the abstentions are now classified as 24
`bytes32`→`uint256`, 3 `string`→`bytes`, 3 same-argument spam ties (E4, E6, E9). The 20-row cost in
r25 was a property of that carrier set, not of the rule.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:33-43,48-60`; E4.

**T-3 — `…r25-evm-selector-name-resolution.md:98-99` — SHARPENS (framing).**
Current text: “Neither flag is a verifier. `filtered=false` still let through 4 wrong candidates
out of 40 distinct unfiltered ones”.
Bearing: outside the 36 keys `filtered` is false unconditionally, so the flag never had screening
power there to “let through” anything — r29 confirms 0 of 199 entries filtered on 152
non-canonical selectors, where `openchain_first` was nonetheless right 152/152 and
`fourbyte_first` wrong 36 (E2, E9). The underlying warning (“not a verifier”) is right; the
mechanism sentence should say the flag is uninformative outside the list and can be perverse inside
it.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:67-70`; `…unseen.md:65-71`.

**T-4 — `…r25-evm-selector-name-resolution.md:115-118` — CORRECTS/SHARPENS (argument types).**
Current text: “**REA's argument inference is often wrong on Vyper.** REA 6.5.0 inferred an argument
list different from the ABI on 12 of 69 rows: 11 on the two Vyper carriers (mostly `address` read
as `uint256`) and 1 on solc `carrierb` (`note(bytes32,uint256)` read as `uint256,uint256`).”
Bearing: on 152 fresh solcjs-0.8.37 rows the mismatches are 27, of which **24 are `bytes32` read
as `uint256`** (e.g. `getRoleAdmin(bytes32)`, most of TimelockController and ENS) and 3 are
`string` read as `bytes`; 0 of the 27 were named (`…r29-evm-fresh-selector-naming.md:62-63`;
E4, E9). The dominant out-of-sample failure is
therefore a solc `bytes32` collapse, and the single solc row r25 recorded is that same class, not
an isolated instance. The Vyper `address` cause stands, but the heading overfits the r25 sample;
the generalisable statement is the two collapse classes at EVMole 0.9.3.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:50-54,97-101`; E4.

**T-5 — `…r25-evm-selector-name-resolution.md:162-167` — SHARPENS.**
Current text: “returned exactly the `filtered=false` subset for every selector, so rules 4 and 5
give the same counts either way on this snapshot. That equality is observed here, not documented
by S076.”
Bearing: the equality now has a documented mechanism (S084/S087: `filter=true` drops marked
candidates) and is **not general**: when a key's kept string is not among the stored candidates,
every candidate is marked and `filter=true` returns nothing — e.g. `0xc45a0155` keeps a string that
is not among its two stored candidates, both of which are filtered (E5). On the 43 selectors the
two sets coincided because the probed canonical names were present.
Round-29 evidence: `…unseen.md:23-24,65-71`; E5.

**T-6 — `…r25-evm-selector-name-resolution.md:20-21` — SHARPENS.**
Current text: “It also says argument types are "likely ABI types inferred from calldata use".”
Bearing: at EVMole 0.9.3 the inference is not merely “likely”: `bytes32`→`uint256` (24 rows) and
`string`→`bytes` (3 rows) are systematic collapses on fresh solc carriers (E4). The quote is
EVMole's own text, so the correction belongs to the lane's use of it: treat the inferred list as a
deterministic map with two known lossy classes.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:50-54`; E4.

**T-7 — `…r25-evm-selector-name-resolution.md:122-123` — CONFIRMS.**
Current text: “When REA's arguments are wrong, the parameter-list check rejects the true name.”
Bearing: r29: 27 mismatch rows, 0 named (E4, E9). No change.

### corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md

**H-1 — `…r28-evm-heldout-selector-naming.md:66-68` — SHARPENS (recall cost).**
Current text: “The round-25 primary rule kept a zero error count out of sample (0 of 137), at a
cost of 50 unnamed rows: 49 rows that were run, plus h09's row, which has no run.”
Bearing: the zero-error result replicates (0 of 122 on r29), but the cost is population-dependent:
30 of 152 unnamed here, 27 of them from argument inference and 3 from spam ties (E4, E6). The
no-name count is not a stable property of the rule; it tracks ABI types and database collisions.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:48-60`.

**H-2 — `…r28-evm-heldout-selector-naming.md:53-54` — SHARPENS.**
Current text: “The 145 → 143 → 137 steps come from the sole-candidate check (2 rows) and the
argument check (6 more rows).”
Bearing: on r29's rows the profile inverts: the argument check costs 27 rows and the sole-candidate
check 3 (E4). The sentence is a property of round 28's carrier set and should not be generalised.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:48-65`; E4.

**H-3 — `…r28-evm-heldout-selector-naming.md:38` — SHARPENS.**
Current text: “For 167 selectors, REA's inferred arguments match the ABI.”
Bearing: r29: 125 of 152 match; the 27 mismatches break into the two named collapse classes
(E4). Round 28 reported the rate without the classes; round 29 supplies them.
Round-29 evidence: `…r29-evm-fresh-selector-naming.md:50-54`; E4.

**H-4 — `…r28-evm-heldout-selector-naming.md:51-52` — CONFIRMS.**
Current text: “None of the 187 held-out selectors is one of Sourcify's 36 canonical keys (S085).
The service marks `filtered` only on those keys (S084), so on these rows "sole unfiltered" equals
"sole".”
Bearing: r29's 152 c1 selectors are likewise none canonical, and 0 of 199 entries are filtered
(E2); “sole unfiltered” again equals “sole”. No change.

### SKILL.md

**K-1 — no correction site — observation.**
`grep -n -E "filtered|canonical|openchain|4byte|selector|EVM" SKILL.md` (E7/E8, exit 0) finds no
statement about the `filtered` rule, the canonical list, the round-25 rule's recall, or REA's
argument types. The nearest lines are capability status (`:54` “held (selector recovery)”), a
co-landing rule about the r4 Vyper wording (`:286`), a Go selector-law note (`:492`), and the
round-28 gate registry rows (`:954-955`). None is contradicted or sharpened by round 29.

## Reverse-direction note (round-29 entry wording, not an earlier site)

**N-1 — `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md:18` — observation.**
Current text: “Three consequences the round-28 entry did not state:”.
Bearing: the first listed consequence (a key with no `signature`, so every candidate is filtered)
**is** stated by the round-28 entry at `…r28-openchain-filtered-flag.md:22-24`: “Five of the 36
keys (…) have no `signature` field, so every candidate for them is marked”. Only the second
(kept signature absent → `filter=true` empty) and third (6 mis-keyed strings) are new. Suggested
integration wording: “Three consequences the round-28 entry did not **test**”. Evidence: E7 grep
plus the quoted lines; no edits made.

## Unknowns

- **U1** The cause of `bytes32`→`uint256` and `string`→`bytes` at EVMole 0.9.3 is not established
  by round 29; the r25 cause covers only `address` under Vyper. Label: unknown.
- **U2** The deployed revision behind `api.openchain.xyz` remains unidentified
  (`…unseen.md:84-85`); the staging/master equality is source-side only. Label: unknown.
- **U3** Whether the 6 mis-keyed canonical entries are a defect or intentional is not established;
  r29-C2 states the 6-of-31 count is an L1 reading over the pinned list, not a counter output
  (`…unseen.md:89-90`). This seat's E3 independently reproduces the 6 keys. Label: observation of
  the bytes, unknown as to intent.
- **U4** The round-29 test cannot separate a list equal on the 26 tested keys but different on the
  other 10 (`…unseen.md:79-80`). Label: unknown for those 10 keys.
- **U5** This seat verified R29-C1's tally figures from the committed `tally.json` and receipts, not
  by re-deriving the 152 rows from the 304 saved lookups; an independent C1 recount is a sibling
  seat's item.

## Scratch artifacts (outside the lane)

Base `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScoutCorrectionSites/`:

| file | sha256 |
|---|---|
| `transcript.sh` | `38ed168ea5842775eac0df95f9d1ac002e057bbb71d7757bfc4ab70bdc748c53` |
| `verify-c2-rule.py` | `e9304aa735a32bfa0164f16159d94ec2281cf86ca1979a5e7f96a196b5465115` |
| `verify-c1-reasons.py` | `203aef088d65a6ae7334841a6ddf99521b51589bb2b0e4386bf6da286c26fa1c` |
| `verify-miskeyed.py` | `94e457f49a0fa19d360eb2223b1b37f87f7bd0e17f72f24e9173ea94680efd66` |
| `verify-examples.py` | `b226b71195f9a0380fc4411ba259c9c3bd6b554813da3fe29af41e958b6ba719` |
| `out/transcript.txt` | `49fc8fc0a120b9bdbb8fcadb05e2b0b3259e4092f25f19b230edcbda2f79adcc` |
| `out/examples-and-receipts.txt` | `4834842953e6b738daa951c74de6879fa220088db3f80b23e4319b12e30741d3` |
| `out/tally-and-tip-lines.txt` | `ed45b18ead379d1f56a8d1090b6a5361ae02a5519ffb2c01a72a60d6bede321c` |
| `out/verify-c2-rule.txt` | `4d97b40cd22e1ab7f66be056a2b2c70af941e5a9fa05801894ef9fea2b6ded5e` |
| `out/verify-c1-reasons.txt` | `2593315960cc5ed7ef5e56f0077e606bb0153f34cfc84e7c069ceea04fa50c67` |
| `out/verify-miskeyed.txt` | `245246b12f30db9de39e1c48632f85e5297b11efc4c7dec3ff997a8f87ba1c30` |

No installs, no network requests, no REA runs, no lane edits. The only lane write is this report.
