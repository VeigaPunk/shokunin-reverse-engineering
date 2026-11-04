# Round 88 — claim critique (CriticClaims, kaidoku)

Critic seat, round 88. Target: falsify R88-C1 and R88-C2 **as claims** — the cheapest cheat that
reaches each frozen target without the claimed work, axis fit, causal separability, and the sizing
rules. I did not judge the wave, edit the claim, or touch the lane's instruments; every number below
was measured on this host in this seat.

Pins used: `/usr/bin/upx` sha256 `cf2f6e7c…c969` (`upx 5.2.0`); carriers `/usr/bin/jq`
`e8156675…`, `/usr/bin/xxd` `7b1e5d0c…`, `/usr/lib/libz.so.1.3.2` `6c78c5e5…`, `/usr/bin/docker-init`
`0bd49c8d…`; `rea-agents@6.5.0` package.json `a5003023…0a6c`; instruments at their `claims.json`
pins (`upx-chain-repair.py` `59ee51b0…`, `upx-chain-battery.py` `a01ed622…`, `depth-blocks.py`
`458eeabd…`, `field-tamper-matrix.py` `0e055486…` — all four re-hashed and equal). Selftests re-run:
11/6/11/7 cases, 0 failures (matches the plan).

Receipts and cheat instruments are under `receipts/` and `cheats/` in this seat dir; the scratch
tree was deleted after they were copied. A receipt that names a deleted path is a claim, so the
cheat scripts are committed with the receipts and each receipt is re-derivable by re-running the
battery with the committed script (the population is regenerated from the pinned carriers).

---

## R88-C1 — coverage, capability acquisition. Verdict: **weakened**

**What holds.** The claimed artifact really does the claimed work. I re-derived every carrier
independently (`receipts/c1-candidate-crosscheck.json`): derived `sz_cpr` 252 / 249 / 201 / 226 on
jq / xxd / libz / dinit, output byte-equal to the packed file in all four, 0.03–0.13 s each. The
geometry record matches the plan: jq accounted 30,800 of `u_len` 30,800; libz 98,592 of 108,560
(single structural candidate, 201); dinit has three structural survivors — 136 (accounted
123,942,159 > `u_len`, impossible), 226 (851,288) and 440 (850,696) — and the accounting bound
picks 226. The measured receipt `.ufo/waves/round-88/l1/scores/c1-at-a14f0a42.json` is
`recovered 4 of 4`, controls true, regression 8/8, exit 0 with the pinned repair sha `59ee51b0…`.

**Cheat 1 (scored): the packer as an oracle — no geometry at all.**
`cheats/oracle-repair-v2.py` composes the round-87 anchor repair (as the candidate does), locates
block0 by the `u_file_size` redundancy (a plain byte scan, not the claimed derivation), then tries
`sz_cpr = 1..sz_unc` and keeps the first value for which `upx -t` and `upx -d` both succeed. No
b_info plausibility test, no sentinel walk, no `u_len` accounting.

```
python3 tools/round-88/upx-chain-battery.py --root . \
  --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/oracle-repair-v2.py \
  --upx /usr/bin/upx --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch> --json-out .ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-oracle-v2.json
```

Result: `recovered 4 of 4`, `controls_ok` all true, regression `recovered 8 of 8`, exit 0 — the
exact frozen label. On jq alone the oracle needed 252 probes and 0.54 s. (A first version that used
the round-87 `find_linfo` to locate block0 scored `0 of 4`: that locator walks the chain and cannot
take the first step, `receipts/cheat-c1-oracle.json` — which is itself the evidence that the *new*
locator is the `u_file_size` scan, not the chain.)

**Cheat 2 (scored): the counter hands the repair its own answer.**
The battery writes, per carrier, `packed`, `n3.out` and `chain.repaired` — the exact expected output
— in the same directory as `chain.tampered`, the repair's `--in`. `cheats/sibling-repair-v2.py`
locates block0 by the same redundancy scan and copies any sibling that differs from `--in` **only
inside the 4-byte `sz_cpr` window**. Zero geometry, zero `upx` probes.

```
python3 tools/round-88/upx-chain-battery.py --root . \
  --repair-cmd .ufo/waves/round-88/w1/CriticClaims/cheats/sibling-repair-v2.py \
  --upx /usr/bin/upx --pkg <REA 6.5.0 dir> --work <scratch> \
  --json-out .ufo/waves/round-88/w1/CriticClaims/receipts/cheat-c1-sibling-v2.json
```

Result: `recovered 4 of 4`, `controls_ok` all true, regression 8/8, exit 0 — again the exact frozen
label. The crude version (any sibling within 4 differing bytes) is caught by N2 (`4 of 4`,
`N2-corrupt-payload False`, `receipts/cheat-c1-sibling.json`), so the N2 control does work against
the careless copy; the window-restricted version passes it because the corrupt-payload byte lies
outside the window.

**Why the kill rule does not catch either cheat.** Neither repair names, reads or hashes a carrier
source path or pin; neither changes a byte outside the `sz_cpr` window. The plan's named limit 3
("the counter scores bytes, not provenance") concedes the first cheat, and the round's own lesson
already records it as M88-4. The second cheat is *not* in M88-4: it is a harness answer leak, not a
packer oracle, and no limit or kill clause names it.

**Axis fit.** Good on the r29 test: the claim names the surface it moves (a new corruption class —
first `b_info` `sz_cpr` zeroed, `CantUnpackException: b_info corrupted`) and the command that shows
it unmoved at base (the same battery with `--repair-cmd r87-anchor` → `0 of 4`; `identity` → `0 of
4`). It is a new edge class, not a re-score of the round-87 magic rule. Coverage is the right axis.

**Causal separability.** Yes: the C1 counter reads only `tools/` and the carriers; it never reads
`SKILL.md`, so it is verifiable with C2 absent. (The reverse fails — see C2.)

**Sizing rules.** One concrete value ✓; no universal clause ✓; the do-nothing cannot reach 4/4 ✓;
controls were committed before the freeze ✓ (pre receipts `7fbe16d45` at 19:58:56, freeze
`70d6f7dec` at 19:59:02). The weakness is not a sizing rule but the evidence rule: the frozen
label is mechanism-blind, and the round's own premise ("M87-3 … defines what this round must not
repeat") is repeated on the new class.

**Contradictions found.**
1. The plan's C1 sentence still says "the smallest offset above `block0 + 12` … yields
   `sz_cpr`". On dinit the smallest structural candidate is 136, not the written 226; the artifact
   and M88-3 use the accounting bound. The sentence is stale, and a reader taking it literally
   would write 136, which the counter's `upx -t` arm rejects.
2. `PROVINCE.md` `## Round-88 additions to Core (verified 2026-11-04)` was written before the
   wave's measured revision and cites the declaration-time receipt
   (`pre/c1-candidate-at-declaration.json`), not `c1-at-a14f0a42.json`. The capability is real, but
   the promotion is dated "verified" ahead of the measured receipt.
3. The counter's `met_target` does not pin the repair bytes; the predicate names the path and the
   container pins the sha, but the battery will certify any `--repair-cmd` (my two cheats have
   different shas and both score `met=True`). A reader must cross-check the receipt's
   `repair_sha256` by hand.

**Smallest safe correction.** (a) Move the expected output out of the repair's reach: pass `--in`
from a directory containing only the tampered file (or copy `packed`/`n3.out` to a path the repair
is not given) — this alone kills cheat 2. (b) Add the M87-3-style control the plan promised: a
frozen non-geometry repair (the oracle) must score `< 4 of 4` under the frozen counter, or the
claim must say in its predicate that the label is mechanism-blind. (c) Correct the "smallest
offset" sentence to the accounting rule (M88-3 already records the miss).

---

## R88-C2 — depth. Verdict: **falsified (as a frozen predicate)**

**What holds.** The depth artifact is real. Craft block 28 is a nine-row decision table
(`upx -t` answer → fields → cells → move), and its cell counts match the measured matrix exactly
(`receipts/…`; matrix receipt `c2-matrix-at-declaration.json`: 68 cells, 63 effective, 0
unclassified; header 35, b_info 8, corrupt b_info 4, p_info 4, compressed 4, bad-method 4, bad-seek
1, tolerated 3, noop 5 = 68). Axis fit on the "adds a table or rule" test: yes.

**The predicate is not what the counter checks.** `depth-blocks.py` computes
`met_target = not unresolved`; it has no target and no count condition. Measured:

```
python3 tools/round-88/depth-blocks.py --root . --rev 0cf8e3243059e0bc510b90c880d13d191e78d732
{"blocks": 27, "met_target": true, "resolved": 27, "unresolved": [], ...}
rc=0
```

`receipts/c2-base-rev.json`. The claim's kill rule says `resolved < 28` kills; the counter's own
success flag and exit code are **already true at base**, with 27 blocks. The pre-freeze control
receipt `c2-depth-at-base.json` records the same thing: `blocks 27`, `met_target: true`. A control
that is supposed to show the target unmet records the target met. This is the freeze-rule
violation the round's own prompt names: the plan sentence, the counter's code and the receipt's
label are not the same condition.

**Cheat (scored): a one-line citation-only block.** Insert inside the `## Queue-drain craft`
section, before the next `## ` heading:

```
- **Cheat block: any citation works.** see corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md:1
```

```
python3 tools/round-88/depth-blocks.py --root <copy-of-SKILL.md-and-corpus> --worktree
{"blocks": 28, "met_target": true, "resolved": 28, "unresolved": [], ...}
rc=0
```

`receipts/cheat-c2-oneline-block.json`. No table, no matrix, no refusal signature, no repair move —
the exact frozen label. The counter cannot distinguish the landed nine-row table from this stub.

**The claim's evidence link is unenforced.** The block cites the matrix receipt path and
`corpus/QUALITY.md` rows 154–155; the counter's citation regex matches only
`corpus/knowledge/<name>.md[:line]`, so neither is checked. A block citing only a base-present
knowledge file resolves with no matrix at all.

**Causal separability is weaker than declared.** The plan says the new block cites the r87 file
(present at base) and the matrix receipt, "so R88-C2 is verifiable without R88-C1 having landed."
The landed block also cites `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` — absent at
base, committed with C1's entry at `a14f0a42`. C2's resolution therefore depends on a C1 artifact;
the plan's sentence is contradicted by the block. (The two *counters* remain separable.)

**Record drift.** The plan's C2 sentence was edited in the worktree after the freeze (uncommitted
`M plans/round-88-claims.md`): "closed 7-label vocabulary" → "10-label vocabulary — v1 left 5
unclassified; v2 supersession". The container predicate is unchanged and the edit is disclosed as
M88-6, but the frozen plan is no longer byte-frozen, and a reader at the freeze commit sees the
stale sentence. The v1→v2 supersession itself is legitimate (v1 conflated no-op with tolerated).

**Sizing rules.** One concrete value ✓ in prose (`blocks 28`); the counter's condition is not that
value (freeze-rule violation above); the label is reachable without the claimed work (cheat above);
controls were committed before the freeze ✓. The "target a do-nothing cannot reach" test fails at
the counter's own signal: the do-nothing exits 0 and `met_target` true.

**Smallest safe correction.** (a) `met_target = (blocks == target and resolved == target and not
unresolved)` with `target` pinned to 28, so the base receipt exits 1. (b) Add a content arm: the
block must carry the matrix receipt path and at least the signature table (e.g. require a
`--require` substring or a minimum row count inside the block), so a citation-only stub fails.
(c) Either cite only base-present files in the block, or drop the separability sentence. (d) Re-freeze
the plan sentence or restore it and keep the supersession in the container only.

---

## Summary

| claim | verdict | reason |
|---|---|---|
| R88-C1 | **weakened** | The capability is real and independently reproduced (252/249/201/226; dinit 226 of 136/226/440; libz 98,592/108,560), and the base state is 0/4. But the frozen label is reachable without the geometry by two scored repairs: a `upx -t`/`upx -d` oracle (4/4, all controls) and a copy of the counter's own `packed` sibling restricted to the `sz_cpr` window (4/4, all controls). M88-4 discloses the oracle; the sibling leak is new and uncaught by the kill rule. |
| R88-C2 | **falsified (as a frozen predicate)** | The nine-row table is real and axis-fitting, but the counter's `met_target`/exit are true at base with 27 blocks (`c2-base-rev.json`), the kill rule's `resolved < 28` is not in the code, and a one-line citation-only block scores `blocks 28, resolved 28`, exit 0. The block also cites a C1 artifact absent at base, contradicting the declared separability. |

No axis is harmed by this critique: it changes no lane file, no instrument and no claim; it supplies
the missing controls and the measured cheats for the next freeze.
