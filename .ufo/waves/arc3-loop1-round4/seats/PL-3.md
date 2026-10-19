# SEAT PL-3 — chain c3 · planner · wave arc3-loop1-round4

**Task (seat line).** Plan C3 (custody residuals): the four closures — (a) sidecar
scope-check, (b) `out.parent.mkdir` guard, (c) distinct-path coverage counting,
(d) the both-sides-absent MATCH ruling text; selftest 22 → ≥24 design; patch
sources `round3/claims/c2/{EX-24,CR-3,CR-4,RV-8}/`. Artifact
`claims/c3/PL-3/plan.md`.

Lane note read and honored: the hyper lane's 402 out-of-credits is a
declared-fallback dispatch recorded in the freeze, not a lane signal.

**Deliverable:** `.ufo/waves/arc3-loop1-round4/claims/c3/PL-3/plan.md`,
sha256 `adacdcc7af9e77fe9dee0badee54fe7362290dd17ee565f84bb86076c8f68369`.

---

## 1. Work performed (evidence pointers)

All paths relative to the repo root. `$D` = `claims/c3/PL-3`. Scratch `/var/tmp/pl3`
only (never `/tmp` — EDQUOT). No git mutation. Custody paths opened read-only
(hash/stat) throughout; every injection ran on scratch copies.

| # | work | evidence |
|---|---|---|
| 1 | Read the freeze (roster, rules, lane-substitution note), the r3 c2 verdict, and all four patch sources in full: `EX-24/proposed-coverage-count.patch.md`, `CR-3/typeswap-declarations.patch.md` §3, `CR-4/proposed-write-guard.patch.md` items 1/5/6/8, `RV-8/rv8-corrections.patch.md` | `$D/plan.md` §0-2 |
| 2 | Pinned the before-state: tool `7cd19c3c…` (1155 L), README `f30df42e…` (185 L), selftest 22/22 CLEAN, probe `findings=0`, census PASS, command A 83/83 14/14 | `evidence/identities.txt` |
| 3 | **Reproduced all four residuals first-hand** on a scratch copy (a) sidecar clobber, (b) mkdir traceback ×2 shapes, (c) padded reference passing the gate, (d) both-absent MATCH — plus a vector no patch text named: the **symlinked sidecar** | `evidence/a-sidecar.txt`, `b-mkdir.txt`, `c-coverage.txt`, `d-both-absent.txt` |
| 4 | Built this seat's own anchored candidate (12 anchors, each asserted unique) from the pinned base; validated it (26/26 CLEAN) | `gen-candidate.py` `e40e0d95…`; `candidate/` |
| 5 | **Detected the mid-wave landing**: the generator refused on a moved base, which is how the real target's change was found rather than assumed | `evidence/live-vs-base.diff` (283 lines) |
| 6 | Re-measured all four closures **base → landed** on the landed bytes `29bb45ae…` / `9d9400da…` | `evidence/a|b|c|d-*.txt` |
| 7 | Built four sabotage mutants from the landed bytes and proved each new selftest case load-bearing (each fails exactly its own case, 27/28) | `evidence/g4-sabotage-arms.txt`; builder `evidence/g4-mutant-build.py` |
| 8 | Searched every r4 artifact for the two gaps below to establish they are not already recorded | `evidence/g1`, `g3`; grep transcripts in §4 |
| 9 | Re-ran the no-harm instruments after the landing: probe `findings=0`, census PASS, command A 83/83, live pair `MATCH 5/5` (r3 pair and a fresh pair) | §3 table; `evidence/g3-stale-surfaces.txt` |

## 2. Proposed changes

**Patch-text paths: none required for (a)-(d)** — C3's designated writer (EX-21)
landed all four closures in the real target during this wave (tool `29bb45ae…`
1343 L, README `9d9400da…` 272 L). This seat wrote nothing to the real target.

Proposed for the parent, in priority order:

1. **Apply EX-21's row patch** `claims/c3/EX-21/patch/skill-registry-row.patched.md`
   (`8e56f3d9…`, line-neutral 390 → 390) in the same commit as the gate pair —
   `SKILL.md` is still `5eec51c0…` and its row still says "22 fixture cases".
   (Independently reached by VZ-3 §R1; this seat re-verified line counts, the
   single `| custody-pair |` row, and anchor survival.)
2. **G1 — close or declare the unstattable fail-open** (§4). Needs a new tool
   revision, which voids the receipts self-pinning `29bb45ae…`; the cheaper
   correct move is the contract-sentence amendment now + the fix next round.
3. **G3 — one-word fix** to the emitted `REFERENCE-COVERAGE` line ("paths
   present" → "distinct paths") and its docstring twin; cosmetic, next revision.

## 3. Before → after measurement for the chain's claim

Instrument: `7cd19c3c…` (before) → `29bb45ae…` (after), both copied to scratch and
re-hashed at use.

| claim element | before | after (landed) |
|---|---|---|
| (a) `--out X --paths X.sha256` | exit 0, **measured file clobbered** `e5e88eba…`→`3cc33fc7…` | **exit 2**, sha unchanged |
| (a) symlinked sidecar (this seat's vector) | exit 0, measured file clobbered | **exit 2**, intact |
| (a) mirror `--out X.sha256 --paths X` | exit 0 | **exit 2** |
| (b) `--out <file>/rec.txt` | `FileExistsError` traceback, exit 1 | **USAGE 2**, 0 traceback lines |
| (b) `--out <file>/sub/r.txt` | `NotADirectoryError` traceback, exit 1 | **USAGE 2** |
| (b) `--out ''` / `'.'` / `'/'` | USAGE 2 (base correct) | USAGE 2 (trap still closed) |
| (c) 5× duplicate stanza `--require-paths 5` | exit 0, `MATCH paths=1`, 0 coverage lines | **exit 2**, `REFERENCE-COVERAGE: 1/5 …` |
| (c) 5 distinct paths control | exit 0 | exit 0 (no false positive) |
| (d) both-sides-absent | `MATCH compared=0/11 exit 0`, no caveat | same class, **+ run-output note**; asymmetry reads `ABSENT 13` |
| selftest | `CLEAN cases=22` | **`CLEAN cases=28 passed=28 failed=0 exit=0`** (claim bar ≥24) |
| sabotage arms | — | **4 mutants, each fails exactly its own case** (27/28) |
| live pair (revised tool) | — | `MATCH 5/5`; EX-21's pair self-pins `29bb45ae…`, both sidecars `OK`; this seat's own fresh pair `MATCH 5/5`; the r3 pair re-verifies `MATCH 5/5` |
| command A | 83/83, 14/14, 10.0/10.0 | **unchanged** |

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the landed fixes are exit-code theatre" | **REFUTED** — every before-state was destructive or traceback-class; after: bytes unchanged, declared class, gate refuses |
| A2 | "the new selftest cases are decorative" | **REFUTED** — four mutants, each failing exactly its own case |
| A3 | "the (a) fix over-refuses ordinary runs" | **REFUTED** — fresh parents, cross-dir neighbours, distinct-5 references, canonical 5/5 pair all stay exit 0 |
| A4 | "the (a) fix reintroduces the `--out ''` ValueError (CR-4 item 6)" | **REFUTED** — `''`/`'.'`/`'/'` are declared USAGE 2 |
| A5 | "the (c) fix breaks legitimate references" | **REFUTED** — distinct-5 `MATCH 5/5 exit 0`; canonical pair still `MATCH 5/5` gated |
| A6 | "the (d) ruling is a costume over a fail-open" | **PARTIALLY SUSTAINED, bounded** — the both-absent MATCH is vacuous (`compared=0/11`, `SHA256-CONTRACT: 0/0`) and an all-absent reference passes the gate; bounded by the declared ruling + run note; records must not quote it as a content witness |
| A7 | "the landed contract sentences are true as written" | **REFUTED for one class (G1)** — the inode arm does not refuse when the measured path is unstattable: hardlink alias clobbered at **exit 14**. `grep -rli unstattable` over `.ufo/waves/arc3-loop1-round4/` returns only this seat's own evidence file — no other r4 artifact names it |
| A8 | "the distinct-path gate is a distinct-file gate" | **REFUTED (G2)** — five hardlink names, one inode (`12115289`), gate passes `MATCH 5/5 exit 0`. Declared unit is names; matches VZ-3 §R5 |
| A9 | "the landing is complete, row included" | **REFUTED (G4)** — `SKILL.md` byte-unchanged, row still "22 fixture cases" (count 1), no "distinct" token |
| A10 | "PL-3's absence blocked the chain" | **REFUTED as a blocker, SUSTAINED as a schedule fact** — EX-21 proceeded on the named patch texts per its seat line's fallback and landed a correct revision; this plan is therefore gap analysis, and G1 is what it adds that no other seat measured |

## 5. Blockers

None for this seat's own task. Two facts the parent must carry:

1. **The landing already happened** before this plan could be written (tool
   `29bb45ae…`, README `9d9400da…`, re-derived by this seat at write time). This
   plan is post-landing verification + gap list, not a pre-landing patch plan.
2. **G1 is unrecorded elsewhere and needs a tool revision to close** — which voids
   every receipt self-pinning `29bb45ae…` (EX-21's live pair and the round's
   records). Cheapest correct path: amend the contract sentences now, fix next
   round with a fresh pair. Decision is the parent's.

## 6. Identity manifest (rule #14 — re-derived at write time)

| artifact | sha256 |
|---|---|
| `plan.md` | `adacdcc7af9e77fe9dee0badee54fe7362290dd17ee565f84bb86076c8f68369` |
| `gen-candidate.py` | `e40e0d953162365807cc9e9a128e2282a4c80ff499fc75a434ed823eaf81142a` |
| `candidate/custody-pair.py` | `35d0c2f09af19b109ad4e31a0cc8c97c5d96c59fa9d5c2fc14c98d99d6a281f1` |
| `candidate/README.md` | `5b048ebcb34a408c55681dc7ca698b1a1dd788df1710d1085f6fa2b097f00110` |
| `evidence/identities.txt` | `dcb73619be60e1b9272d62a9e88a6dc3fc12f958291c820d1f73890cc20fce1f` |
| `evidence/a-sidecar.txt` | `b9fa5e7054e17053804dc4a210074cba30bdf72a805571dddd8a8394e065d84a` |
| `evidence/b-mkdir.txt` | `466b65c0811954314eead77152809a4d219e866a31314d946295366d329cceb0` |
| `evidence/c-coverage.txt` | `f2e3c782f605cb1734b398d529649568b90063a7bbabb4f5158b3de149852f50` |
| `evidence/d-both-absent.txt` | `90ae00f7e8e3d86eb0ffbd1f75e0644d10bee63c4020e7136a81b8b820664e7c` |
| `evidence/g1-unstattable-failopen.txt` | `ad0ab5c3b1f53e3f9263c0ff777a77abe9145aa28ee26f22bd3a57f1dd81b4e6` |
| `evidence/g2-hardlink-coverage.txt` | `a72dd73f7e8ec4470fd13cec0b464c538f64cc16fc0d72b75bd52fc5c1e7b209` |
| `evidence/g3-stale-surfaces.txt` | `790b308e618fe5d1c721f353aaa1f9fd08bd3863f1a25ca47ff272a840b124dc` |
| `evidence/g4-sabotage-arms.txt` | `530576c38adc95b5ee0030ea469abd80fce2d505fe9ebde8eae48358a0a3729a` |
| `evidence/g4-mutant-build.py` | `8c5997654f4e707553739c2eb8076b23d635892010b68c2e0bf9956db51ca8fe` |
| `evidence/live-vs-base.diff` | `1bef563892bf4b6da2f264de7cbc6dc9d2314234cef638430ae7383ec54d3298` |
| mutant `M1-no-sidecar-arm` | `7a15ddab8c52b73519876344aac8b9b5157b2c9ac0eff0be6adb7742e5ac3d06` |
| mutant `M2-stanza-count` | `ca3680dd63dc09bab7005e0e082d8d94946180944eef63e3b7172327e400010d` |
| mutant `M3-unguarded-mkdir` | `b252f5f45ee8c9df3d7b2999463ad75545d572a7470e2150fcd45789e91e2664` |
| mutant `M4-no-absent-note` | `e10e9fe8d06c0b64993709beacd8997c386a4318d23c15d7cf2164b2f8536d38` |

Objects cited but owned by other seats (re-derived by this seat at write time, not
trusted): tool `29bb45ae…` (1343 L), README `9d9400da…` (272 L), `SKILL.md`
`5eec51c0…` (390 L), r3 base tool `7cd19c3c…` (1155 L), r3 base README
`f30df42e…` (185 L).

This report cannot carry its own post-edit digest without circularity; the digests
above are the authoritative pointers, re-derived from the files as they stood when
it was written.
