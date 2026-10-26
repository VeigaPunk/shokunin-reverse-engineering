# R38ExecRecountBase — pre-claim recount of the frozen R38 counters

Seat scope: score the frozen counters `tools/round-38/{c1,c2}-counter.py` at the base and
freeze revisions to record the do-nothing (pre-claim) state, and report the receipts' key
fields. Advisory only — no counter, predicate, carrier, oracle or lane surface was modified.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Revisions read:
base `77091b492cc53f8743bd0701b1e7d5e66123dd84`, freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`,
landing tip `9c9d496b` (`round-38: wave-1 spec/dispatch`). Both claims docs read
(`plans/round-38-claims.md`) and the round-37 verifier spot-check
(`corpus/lessons/round-37-verifier-spotcheck.md`).

## 1. Runs and exit codes

All runs used `python3 -I -B` with `HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r38/R38ExecRecountBase`
and `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`.

| # | counter | `--rev` | `--freeze` / `--base` | exit | receipt |
|---|---|---|---|---|---|
| 1 | c1-counter.py | `77091b49` (base) | freeze `e059ca93` | **1** | `.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/c1-at-base.json` |
| 2 | c1-counter.py | `e059ca93` (freeze) | freeze `e059ca93` | **1** | `…/R38ExecRecountBase/c1-at-freeze.json` |
| 3 | c2-counter.py | `77091b49` (base) | base `77091b49` | **1** | `…/R38ExecRecountBase/c2-at-base.json` |
| 4 | c1-counter.py | `9c9d496b` (tip) | freeze `e059ca93` | 1 | `…/R38ExecRecountBase/c1-at-tip.json` |
| 5 | c2-counter.py | `9c9d496b` (tip) | base `77091b49` | 1 | `…/R38ExecRecountBase/c2-at-tip.json` |

Runs 1–3 are the assigned three. Runs 4–5 are extra (cheap, no REA) to show the wave-1
spec/dispatch commit moved neither counter: the do-nothing class still holds at the tip.

**Deviation from the dispatch text (receipt fact, not a defect of the counter).** The
assignment predicted exit **2** for run 1 ("claim data absent at base"). Observed exit is
**1**. `c1-counter.py` returns 2 only from the `Unevaluable` path (`git()` with `check=True`,
lines 34-38 and 141-151), which triggers on an invalid revision or on `carriers.json` absent
*at the freeze*, never on absent claim data: with no `corpus/evidence/round-38/c1/K*/after.json`
the per-carrier loop simply records `after_present: false` and `met_target: false` → exit 1.
Two probes confirm the 2-path (both exit 2, both evaluated nothing):

```
$ c1-counter.py --rev e059ca93 --freeze 77091b49  # freeze predates carriers.json
{"unevaluable": "carriers.json absent at freeze"}                                EXIT=2
$ c1-counter.py --rev deadbeef…deadbeef --freeze e059ca93
{"unevaluable": "git cat-file -e deadbeef…^{commit}: fatal: Not a valid object name …"}  EXIT=2
```

The frozen text is consistent with the observation — `plans/round-38-claims.md` §R38-C1 says
"the counter below at the base **exits non-zero**", and the selftest case `do-nothing (freeze
files only)` expects **1**. Only the dispatch's "expect exit 2" wording is off.

## 2. Receipt key fields (verbatim from the JSON)

**Run 1 — c1 at base `77091b49`, exit 1**
```json
{"revision":"77091b492cc53f8743bd0701b1e7d5e66123dd84","carriers_matched":0,
 "carriers_unchanged":false,"met_target":false,
 "bindings":{"coverage_map_row":false,"entry_present":false,"entry_source_ids":[],
             "frontier_note":true,"opened_source_rows":[],"province_core_row":false,
             "province_core_section":false,"sourced":false}}
```
Per carrier (`carriers{}`): K1 oracle_files 5, K2 3, K3 4, K4 4; all four `oracle_frozen: true`,
`after_present: false`, `matched: false`. `carriers_unchanged: false` because
`git cat-file -e 77091b49:.ufo/waves/round-38/c1/carriers.json` → rc 128 (the file is
introduced by the freeze commit), so `show(rev, CARRIERS) = None ≠ frozen`.

**Run 2 — c1 at freeze `e059ca93`, exit 1**
```json
{"revision":"e059ca9391642d5b71b6662cabcbdce0d9308719","carriers_matched":0,
 "carriers_unchanged":true,"met_target":false,
 "bindings":{"coverage_map_row":false,"entry_present":false,"entry_source_ids":[],
             "frontier_note":true,"opened_source_rows":[],"province_core_row":false,
             "province_core_section":false,"sourced":false}}
```

**Run 3 — c2 at base `77091b49`, exit 1**
```json
{"revision":"77091b492cc53f8743bd0701b1e7d5e66123dd84","mismatches":1,"guards_ok":false,
 "met_target":false,"unresolved":[["prov_core:REA MCP server","evidence/doctor/"]],
 "assertions":7,"assertion_mismatches":[],
 "guards":{"base_pointers":48,"pointers_not_fewer":true,"missing_units":[],
           "base_unresolved":[["prov_core:REA MCP server","evidence/doctor"]],
           "unrepaired":[["prov_core:REA MCP server","evidence/doctor"]]},
 "observed":{"command_a":{"knowledge_files":124,"mapped":124,"rule_blocks":17,"resolved_rules":17},
             "command_b":[9,9],"craft_range":[81,314],"adjacent_range":[97,125]}}
```

**Run 4 — c1 at tip `9c9d496b`, exit 1**: `carriers_matched 0, carriers_unchanged true,
met_target false`, bindings identical to run 2 (`frontier_note: true`, all else false).
**Run 5 — c2 at tip `9c9d496b`, exit 1**: `mismatches 1, guards_ok false, met_target false,
unresolved [["prov_core:REA MCP server","evidence/doctor/"]]`, `observed` and `guards`
identical to run 3.

Field-by-field, run 2 and run 3 reproduce the frozen do-nothing controls exactly
(`.ufo/waves/round-38/controls/ctl-c1-0-do-nothing.json`, `ctl-c2-0-do-nothing.json`): every
key in the control's `output` block is equal (`revision, carriers_matched, carriers_unchanged,
bindings, met_target` for C1; `revision, mismatches, guards_ok, met_target, unresolved,
assertion_mismatches` for C2), and both controls' `exit` field is 1. Both controls are
target-not-met, so neither claim is stopped by a frozen control that meets the target.

Claim data is absent at all three revisions: `corpus/evidence/round-38/c1` holds no tracked
file (`git ls-files corpus/evidence/round-38 | wc -l` → 0) and `K1..K4/after.json` are absent
from the worktree. The C1 counter therefore never invoked the evidence-id path (with no
envelopes, `evidence_ids()` returns `{}` before any `node` call — no REA/xpin subprocess ran).

## 3. Frozen-counter selftests (calibration of the instruments themselves)

```
$ python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 <rea-agents>
{"selftest":"c1-counter","cases":15,"green_ok":1,"red_ok":14,"failures":[]}            EXIT=0
$ python3 -I -B tools/round-38/c2-counter.py --selftest
{"selftest":"c2-counter","cases":14,"green_ok":1,"red_ok":13,"failures":[]}            EXIT=0
```
Case counts and green/red split match `plans/round-38-claims.md` (15 = 1 green + 14 named red;
14 = 1 green + 13 named red). The C1 selftest ran in 1.5 s and used its own fixtures
(`tools/round-38/selftest/{dev-after.json,dev-before.json,dev-le-xz.sqsh,dev-oracle.tsv}`),
never a carrier.

## 4. Falsifier findings on the frozen C1 predicate (advisory; nothing repaired)

**F1 — `frontier_note` is already true before the claim, so the do-nothing control is green on
that binding.** The counter's frontier element is a whole-file scan for any line containing both
`big-endian` and `superseded` (c1-counter.py, `b['frontier_note']` in `measure`), with no
section scoping. At the base, `PROVINCE.md:156-157` already reads:

```
- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback
  covers the carved-image path today. [2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; big-endian/AVM stays here.]
```

That line is a round-36 **LE** supersession note whose second clause says big-endian/AVM
*stays* Frontier — the opposite of the round-38 statement P38-C1 requires. Confirmed green
pre-claim: run 1 (base) `frontier_note: true`, run 2 (freeze) `true`, `ctl-c1-0` output `true`.
So the P38-C1 element "the round-38 frontier note supersedes the big-endian Frontier bullet"
carries no discriminating power against do-nothing, and a landing that never writes a round-38
frontier note would still satisfy it. By contrast `province_core_row` *is* section-scoped
(`CORE_HEADING`), which is why that binding is correctly false pre-claim.

**F2 — no carrier bytes are read at the measured revision.** `measure()` reads only
`c['id']` and `c['sha256']`; the string `c['path']` never appears in `c1-counter.py`
(`grep -c "c\['path'\]"` → 0). The counter never confirms the carrier file exists, or hashes to
its pin, at `--rev`. The selftest makes this explicit: its green fixture (`base_files`) writes
`XPIN`, `CARRIERS` and the four `oracle.tsv` files **and no carrier image at all**, and still
returns exit 0. The only carrier-related check is that the receipt's *self-declared*
`subject.digest.sha256` equals the pin, so a receipt could assert the pinned digest while the
committed carrier bytes differ. Material is honest today — I re-hashed the committed bytes at
the base and all four pins match:

```
K1 1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e  match
K2 403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  match
K3 9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0  match
K4 a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed  match
```

(git show 77091b49:<carrier path> | sha256sum). This is a detector gap, not a live mismatch;
it belongs to the verdict as a disclosed blind spot, in the same class as the carried-forward
R36-CL3/R36-CL5 blind spots.

**F3 — `carriers_unchanged` conflates "absent" with "modified".** At the base the field is
`false` only because `carriers.json` does not exist yet at `77091b49` (`cur = None ≠ frozen`),
not because any carrier was altered. Any reader comparing the base and freeze receipts must not
read `carriers_unchanged: false` at the base as drift.

## 5. C2 pre-state (calibration axis)

The single observed mismatch at the base is the one the claims doc predicts: the PROVINCE
Core `REA MCP server` row's backticked pointer `evidence/doctor/` does not resolve (the
document lives at `.ufo/waves/round-19/evidence/doctor/`). `guards_ok` is `false` for the same
reason — `guards.unrepaired` still lists it while `--rev == --base`, so both `mismatches == 0`
and `guards_ok` remain to be earned by the landing. `missing_units` is empty and
`pointers_not_fewer` true at the base (48 pointers), and all 7 internal assertions agree
(`assertion_mismatches: []`), so the counter's own stated counts (command A 124 knowledge
files / 124 mapped / 17 rule blocks / 17 resolved rules; command B [9,9]; craft range
[81,314]; Adjacent range [97,125]) are self-consistent at the base.

## 6. Limits, risks, blockers

- No REA invocation, no network, no installs, no VCS mutation. Nothing was installed or
  upgraded, so there is no tooling ledger entry for this seat.
- Only reads: `git show`/`cat-file`/`ls-files`/`log`, the counter scripts, the selftest, the
  controls and the two frozen documents. Lane worktree status untouched (`git status
  --porcelain` at the start of the seat showed only the L1's own untracked wave-1 paths).
- Neither claim is stopped by a frozen control: both do-nothing controls are target-not-met
  and exit 1, and I reproduced both exactly. C1's remaining work is the four after-receipts,
  the knowledge entry, the SOURCES row and the three surface edits; C2's is the doctor-pointer
  repair plus count/range upkeep. F1/F2 do not block landing but they do mean the C1 verdict
  must not lean on `frontier_note` or on carrier-byte identity as evidence of work done.
- Blocker: none. `[INFERENCE]` If the L1 wants the base-run exit to be a hard 2, the counter
  would need to treat absent after-receipts as `Unevaluable`; that is a post-freeze change and
  therefore forbidden this round — the recorded exit 1 is the frozen behaviour.

## 7. Scratch

`/fast/scratch/hyaku/kaidoku-r38/R38ExecRecountBase` was created for `HYAKU_SCRATCH` and any
counter temp dirs, and was removed at the end of the seat. Every artifact cited above lives
under `.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/`:

```
75126d16fcbb9810ee2bad6f7e0aceda5993acf43ef8151fb7439e16c97b25b1  c1-at-base.json
6293f9734a60272b000f80beca7b10c4a499ace50a1059f8864bcefea8ad150c  c1-at-freeze.json
f163289c68c4d243b40f5b14ed2a16c278a52d794cb52b86f7f78b53d74b0a65  c1-at-tip.json
a7c78d1053c903105bd3b48d5b7c19e4d5b4e2283bf845570be91dc87f2db6de  c2-at-base.json
03b1153c60d37dc3740a4a611bd373eb8039cf2ad4f086603f59964f19f352f2  c2-at-tip.json
```
