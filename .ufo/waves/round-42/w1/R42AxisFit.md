# R42AxisFit — axis-fit attack on the round-42 draft, pre-freeze

Verdict: **DONE** — R42-C1 is a coverage move (CONFIRMED), R42-C2 is a depth move (CONFIRMED, with two freeze-time conditions), they are causally separable (CONFIRMED), no do-nothing control can reach either target (CONFIRMED), each after-state is one value one command re-derives over committed bytes (CONFIRMED), and 2 universal clauses in the draft are not enumerated by the counting commands (C2 step-3 sentence; C2 "whole SquashFS handler family" until per-handler pins are bound) — text fixes below.

Audited inputs: `AXES.md`; prompt `kaidoku-round-42.md` §6 item 9 (l.464–486); `plans/round-42-claims.md` (commit `fdabdfa4`, draft); round-41 closure `corpus/lessons/round-41-verifier-spotcheck.md` §5 (D1–D5); `corpus/lessons/round-41.md` `## Routed defects into round 42` (R41-CL1..CL4) and `## Mistakes`; round-41 tools (`c1-counter.py`, `c2-counter.py`, `sqfs-triage-v3.py`, `indep-eval-v3.py`, `heldout-gen-v3.py`, `c2-controls.py`, `c1-run.sh`); round-41 wave-2 findings (`R41W2C2Table.md`, `R41W2C2Combos.md`); round-41 receipts (`corpus/evidence/round-41/c1/V3/after.json`, manifest `corpus/evidence/round-41/c2/heldout/manifest.json`); unblob 26.6.4 installed source (`squashfs.py`); unblob fixture tree (GitHub API, tree `1fcc7a0a584a70a96c31f5a276c20944d199a089`); tool availability (`unsquashfs` 4.7.5, `7z` 26.04, `sasquatch`/`sasquatch-v4be` 4.5.1). No write outside this report and `.ufo/waves/round-42/w1/artifacts/R42AxisFit/`; no REA/unblob/sasquatch run on any candidate or carrier; no tool installed (no channel change).

---

## 1. Axis fit (Q1)

### R42-C1 — coverage: CONFIRMED

AXES.md defines coverage as "fraction of the domain's real surfaces the skill governs (repo paths, tools, edge classes)". Prompt §6.9: "Name the axis by the surface the round changes… A coverage claim names the surface it moves (frontier → core, a new tool, operation or edge class) and the command that would show it unmoved."

The surface the round changes is exactly the v3 extraction outcome edge class:

- `PROVINCE.md` today holds v1–v3 only as an unmeasured producer statement and as the v3 table's `no-squashfs-chunk` cause text. Verified: the Core rows are round-36 LE v4, round-39 standard BE v4, round-41 AVM-BE v4 (`PROVINCE.md:372-408`); the round-4 `sasquatch` bullet was superseded for LE/BE v4 but "Big-endian/AVM and vendor-mangled images stay Frontier" (`PROVINCE.md:374-376`). No v3 REA run exists in the corpus (claims draft l.25–29 states this; the knowledge entry `2026-10-26-unblob-format-matrix.md` explicitly marks v1–v3 as a "producer's coverage statement, not outcome").
- The move is Frontier → Core naming the `squashfs_v3*` handler family, a knowledge entry, a README coverage-map row, and SOURCES rows for the carriers' publishers — the exact four surfaces §6.9 asks for.
- Command that shows it unmoved: the frozen C1 counter at the freeze exits 1 (no round-42 receipts, no Core row). Carriers are published third-party images, sourced (SOURCES rows), fresh (never scored — v3 has never been scored). Not a re-score of a held rule.

Verdict: coverage. One condition (below, §5): the per-carrier handler name and the "no failed chunk" enumeration must be pinned exactly.

### R42-C2 — depth: CONFIRMED (two freeze-time conditions)

AXES.md defines depth as "verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources". The round changes SKILL.md's `## Queue-drain craft` by adding rule block 21 with `<!-- sqfs-triage-table v4 -->`, a knowledge entry, and a supersession sentence for block 20. That is a new decision table (new rows, new actions: `legacy-body-failure`/`cross-read-legacy`, reworked `no-squashfs-chunk` semantics) — a depth move, not a re-score:

- R41-CL4 is the routed defect: the v3 table's handler cell `none` (= no `squashfs*` chunk) and precedence step 2 (no `squashfs_v4_*` handler) diverge on a v1–v3-only chunk (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-25`; executed in `R41W2C2Table.md` F5: interp `(unclassified, none)` vs eval `(no-squashfs-chunk, inspect-input)`). The draft repairs the by redefining F = the set of ALL `squashfs_` handler names in H and step 2 F=∅. That is new decision detail on a superset of the family, plus a new legacy-failure row (step 6) and widened combos whose factors include the handler family.
- R41-CL1 (declared-tuple key: generator wrote `declared`, counter read `class_expected.features`/`features`/`declared_features` only — `c2-counter.py:1497-1503` vs `heldout-gen-v3.py:1370-1475`; verified in the manifest: combo carriers carry `declared`, `class_expected` null) is fixed by one key `declared_features`.
- The round-41 `planned` row named depth first (refreeze the triage claim); R41-CL4 is stated as the reason this is a new table and not a re-score. Consistent.

Two conditions (else the claim degrades toward quality or fails to verify):
1. The new decision rows must actually fire on the dev arm: the draft's step-3 sentence ("every v1–v3 chunk and every v4 LE chunk resolves plain sasquatch") and step-6 row are bracketed "[to be confirmed by wave 1]". The freeze target already includes legacy-family classes built from the v1–v3 fixtures (clean per handler, dependency missing, zero-file, partial body damage), so the new rows will be exercised by construction if those damage shapes generate successfully — the wave-1 dry run (QUALITY 84) must demonstrate it end-to-end before the freeze.
2. Step 6's "failing handler a v1–v3 handler" needs failing-chunk (HF) semantics; the v3 table grammar cannot express it (see §6, F2-class trap). The v4 interpreter must implement HF; otherwise interpreter/evaluator diverge on multi-chunk legacy envelopes.

---

## 2. Causal separability (Q2): CONFIRMED

C1 frozen paths: `plans/round-42-claims.md`, `tools/round-42/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-carrier.py}` + oracle tools, `.ufo/waves/round-42/c1/{carriers.json,gap-rule.json}`, every carrier pin/oracle/non-regular table. C1 reads PROVINCE/README/SOURCES/knowledge, its receipts, carriers, oracles, reruns.

C2 frozen paths: `plans/round-42-claims.md`, `tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,heldout-gen-v4.py,c2-counter.py}`, writer + fixture pins, the SKILL v4 block, control tables. C2 reads SKILL.md, its interpreter/evaluator/generator/controls, pinned unblob fixtures (never C1 carriers), and the round-41 C1 receipts.

- Shared artifact: only the plans file itself (both claims' predicates live there; a post-freeze edit blocks both — intended, not a data coupling).
- Carriers disjoint: C1 = published third-party images; C2 = unblob test fixtures (explicitly "belong to C2 and are never C1 carriers", draft l.47–48). Development inputs (OpenWrt Kamikaze 7.09, round-41 carriers) are designated development, never C1 carriers.
- C2 reading the round-41 C1 receipts (`corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json`) is an explicit, older-round data read; the separability sentence "Neither reads the other's round-42 data" (draft l.107–110) holds.
- One hygiene point: the C2 counter's declared-tuple reader must read ONLY `declared_features` (no `class_expected.features`/`features`/class-level fallback aliases as in `c2-counter.py:1497-1503`); otherwise the R41-CL1 one-key fix is not actually one-key.

---

## 3. Do-nothing control reach (Q3): CONFIRMED unreachable for both

- C1: CTL-C1-0 (do-nothing at the freeze): no round-42 receipts exist and no Core row exists at the freeze → counter exits 1, `carriers_matched 0` (round-41 executed the identical design: `controls/c1/ctl-c1-0-do-nothing.json` = 0/4, exit 1). CTL-C1-1 (relabelled round-41 receipts) is blocked by the freshness clause (`carrier_fresh_ok` / `receipt_fresh`: first-add must be a strict descendant of the freeze; `c1-counter.py:91-96,117-118`). CTL-C1-2 (oracle-only fabricated receipt) is blocked by the counter-time rerun projection clause (`projection_ok`, `c1-counter.py:149-153,198-247`). No path reaches `met_target`.
- C2: CTL-C2-0 (base SKILL, no v4 marker): interpreter exits 2 (unevaluable) → no score. CTL-C2-0b (v3 table under the v4 marker): legacy-chunk envelopes get `no-squashfs-chunk` or `unclassified`, which the evaluator does not assign → mismatch, cannot reach `matched == n`. Kill rule: any control at full score on the development envelopes stops C2 before held-out generation. No do-nothing reach.

---

## 4. After-state as one re-derivable value (Q4): CONFIRMED

- C1: `carriers_matched == 4` (plus the binding receipt), re-derived by one command over committed bytes: `python3 -I -B tools/round-42/c1-counter.py --root <lane> --rev <REV> --freeze <FREEZE> --pkg65 <rea-pkg>`. Environment dependency: the rerun arm needs REA 6.5.0, unblob 26.6.4, `sasquatch` on the child PATH, and the carrier bytes fetchable by pin — same shape as round-41 (accepted there); the projection-equality specification must be frozen in-code (as `c1-counter.py:207-241` did: files/chunks/gaps/unpublished/diagnostics multiset) rather than left to prose.
- C2: `matched == n` (n determined by the frozen seed via `heldout-gen-v4.py --seed <FREEZE>`), re-derived by `python3 -I -B tools/round-42/c2-counter.py --root <lane> --rev <REV> --freeze <FREEZE>`.
- Both receipts record the scorer's exit code and the counter file's sha256 (freeze-integrity rule, draft l.19–21; round-41 closure D4).

---

## 5. Universal words vs the counting commands (Q5)

Full occurrence list: `artifacts/R42AxisFit/universals-occurrences.tsv` (scanner `scan-universals.py`, run over `plans/round-42-claims.md`). Per-line enumeration status: `artifacts/R42AxisFit/universals-enumeration.tsv`.

Findings:

1. **Not enumerated — C2 step-3 sentence** (draft l.73): "every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch` [to be confirmed by wave 1 on real REA envelopes; label wording may change]". No counting command enumerates "every chunk" of the real world; it is a proposition about future REA runs. Fix: replace with a bounded statement over the frozen dev-arm runs ("on the frozen dev-arm runs of the pinned v1–v3 and v4-LE fixtures, every recorded dependency set D = {sasquatch}") or drop it from the predicate; keep step 3's decision rule dependent only on observed D membership. Also mark it non-normative so the independent evaluator does not read it as a rule.
2. **Not enumerated until pinned — C2 "whole SquashFS handler family"** (draft l.58). The family IS enumerable: unblob 26.6.4 `squashfs.py` defines exactly 10 handler NAMEs (`squashfs_v1`, `v2`, `v2_nonstandard`, `v3`, `v3_ddwrt`, `v3_broadcom`, `v3_nonstandard`, `v4_le`, `v4_be`, `v4_broadcom`; lines 101–549), and the unblob fixture tree has an input dir for each of the 10 plus a `squashfs_v3_adaptive/` dir that binds to NO handler class with that NAME in 26.6.4 (orphan; LFS lzma inputs). The draft does not yet require per-handler pins for all 10 names nor a counter binding that each pinned handler appears in ≥1 held-out class. Fix: bind the 10-name set in the generator/manifest (fixture pins per handler), add a coverage binding, and explicitly exclude or resolve the adaptive orphan.
3. **Partially enumerated — C1 "names a `squashfs_v3*` handler (the one frozen per carrier) with no failed chunk"** (draft l.35). The handler set is enumerable if the freeze pins one exact handler name per carrier (note: `squashfs_v3*` covers four distinct handlers; the v3/v3_ddwrt/v3_broadcom/v3_nonstandard magics differ — `squashfs.py` lines 245–429). "No failed chunk" requires the counter to enumerate EVERY chunk in the receipt and define "failed" (`extraction_failed == true`, plus any failure not represented in `chunks[]`). Fix: freeze exact per-carrier handler NAMEs; define chunk enumeration + failure predicate in the counter.
4. Enumerable universals (all fine, listed in the artifact): "no commit in FREEZE..REV touches a frozen path" (git log over frozen paths); "every regular file of the oracle … same sha256 and size" and "no non-regular oracle entry as a file" (full-table comparison against oracle.tsv/nonregular.tsv, round-41 exact-path rule); "accounts for every non-regular oracle row" + "at most one structural depth-limited" + "no unknown-chunk-handler" (nonregular.tsv × gap-rule.json, gap counts); "has a subject digest equal to the carrier pin"; "the carrier bytes hash to the pin and their superblock reads the frozen magic/major/compression" (single values; magics per variant — freeze the constants); "a counter-time REA rerun has the same projection" (freeze the projection spec in-code); "PROVINCE, entry, README row and a SOURCES row absent at the base whose used-by lists the entry exist"; "no frozen C1 path changed after the freeze"; "gives every held-out envelope the same (label, action) pair as the frozen evaluator" (matched == n); "every envelope's observed feature tuple equals the tuple the manifest declares under ONE key (`declared_features`)" (R41-CL1); "carriers regenerate byte-identically"; "the v4 table bytes equal the freeze bytes"; "the round-41 C1 receipts and the round-42 dev-arm real legacy envelopes get the evaluator's pair".

---

## 6. Additional findings (smallest safe corrections)

- **F2-class multi-chunk trap must not be re-imported into v4.** `R41W2C2Table.md` F2 showed the v3 table grammar (handler cell fnmatch against any member of H) cannot express "the failing chunk's handler"; the evaluator reads HF (`extraction_gaps[].handler` where kind == `extractor-failure`, with H fallback) — `indep-eval-v3.py:260-269,366-374`. Draft step 6 ("failing handler a v1–v3 handler") is exactly this shape. The v4 interpreter must implement HF (or the legacy row must be restricted to single-chunk envelopes). Recommend an explicit selftest pair: multi-chunk legacy envelope where the failing chunk is v3 and another chunk is v4 → legacy row; failing chunk v4_be with BE=no,P=0 → avm row.
- **Evaluator independence guard.** "Expected labels come from a frozen INDEPENDENT evaluator written only from the draft's precedence text" — make it checkable: the evaluator freezes with the freeze (like `indep-eval-v3.py`, which reads only the precedence list + envelope shape); add a guard that it never reads SKILL.md, the interpreter, the generator, or the table (r41 precedent: `indep-eval-v3.py:12-18`).
- **Combo widening must be validated BEFORE the freeze.** r41 measured 8/12 for CTL-C2-7 (`R41W2C2Combos.md`); target is now <50%. The <50% guarantee can only be proven on the held-out combos, which are generated after the freeze — so wave 1 must generate candidate combo families dev-side, measure CTL-C2-7 on them, and iterate until <50% BEFORE freezing; otherwise the target may be unreachable or trivially met (freeze-time calibration).
- **Carrier/superblock phrasing.** "The carrier bytes hash to the pin and their superblock reads the frozen magic/major/compression" — for vendor images whose SquashFS is nested (e.g., a TRX/`tqsh` image), the carrier bytes are the whole published blob; the magic check applies to the extracted chunk, not offset 0 of the image. Define whether carrier = whole published blob + carved filesystem, and which chunk is the oracle root (round-41 `oracle_root` key pattern).
- **c1-run.sh port.** For v3 the child PATH must resolve `sasquatch` (never require `sasquatch-v4be`); carry the R41-CL2 ARG_MAX fix (`--slurpfile`); keep `--max-depth 1` and the `REA_UNBLOB_COMMAND` absolute-path env.
- **C2 counter one-key hygiene.** Remove the fallback alias chain (`c2-counter.py:1497-1503`) — generator writes `declared_features`, counter reads only `declared_features`.

---

## 7. Verdict summary

| Item | Verdict |
|---|---|
| R42-C1 axis (coverage) | CONFIRMED — Frontier→Core on the v3 handler family; unmoved command defined; fresh published carriers |
| R42-C2 axis (depth) | CONFIRMED — new v4 table over the whole family, R41-CL4 repair, legacy row; two freeze-time conditions (§1, §6) |
| Causal separability | CONFIRMED — disjoint data/frozen paths; only the plans file shared; C2 reads only round-41 (older) C1 receipts |
| Do-nothing control reach | CONFIRMED unreachable for both (CTL-C1-0/1/2; CTL-C2-0/0b + kill rule) |
| After-state single value | CONFIRMED — `carriers_matched == 4`; `matched == n` (seed); receipts carry exit code + counter sha256 |
| Universal words not enumerated | 2: C2 step-3 sentence; C2 whole-family set until 10 handler names pinned (plus precision fixes: failed-chunk enumeration, HF semantics for step 6, per-carrier handler NAMEs, per-variant superblock constants, projection spec freeze) |

Artifacts: `artifacts/R42AxisFit/scan-universals.py`, `universals-occurrences.tsv`, `universals-enumeration.tsv`, `handler-family.tsv`.
