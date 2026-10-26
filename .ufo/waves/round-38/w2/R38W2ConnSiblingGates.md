# R38W2ConnSiblingGates — Sibling-pattern scan: freeze-drift / frozen-instrument-integrity gates

**VERDICT: CONFIRMED** — kaidoku's `tools/round-38/freeze-drift.py` + QUALITY 79/80 **extend** the fleet's freeze-integrity pattern; no sibling lane holds an equivalent standalone "first-freeze-bytes are the rule" audit gate. No duplication found; no defect in the landing surfaced from the sibling comparison.

## 1. Scope and method

- Scanned all sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (18 lanes; lanes with `tools/`: chousa, kama, kotodama, mado, mori, souji, tameshi, tsukuroi, kaidoku).
- Grepped `tools/`, `corpus/QUALITY.md`, `corpus/lessons/`, `corpus/evidence/` for `freeze|frozen|drift|amend|post-scoring|first freeze|kumitate`.
- Read headers/docstrings of the closest sibling tools: `mori-freeze-order.py`, `mori-source-drift.py`, `mori-census.sh --pin/--drift`, `souji-rev-pin.py`, `kotodama replay-frozen.py`, `check-judged-object.py`, `check-supersession-settlement.py`, `kama error-verdict-census.py`, `prereg-time-check.py`, `round33-gate-receipts.py`, `pin-watch.py`, `tsukuroi check-revision-binding.py`, `check-freshness-r17.py`, `chousa research-gate.sh`, `quote-reopen.py`, `tameshi pin-disposition.py`, `mado-tripwire.py`, `audio r79b_freeze_order.py`, `lore dependency_freeze.py`.
- Verified kaidoku's own in-lane lineage: `tools/round-31/freeze-integrity.py` (QUALITY 55), `tools/round-24/freeze-gate.py` (QUALITY 33), and the wave-1 receipts `.ufo/waves/round-38/l1/freeze-drift-077e212b.json`, `freeze-drift-cb4326b2.json`, `freeze-drift-gen-controls.json`.
- Read-only; no sibling tool was executed (behavioral claims below are from source/docstrings — marked `[INFERENCE]` where not explicit).

## 2. What siblings hold (closest patterns)

| Lane | Tool / criterion | Mechanic | Relation to freeze-drift.py |
|---|---|---|---|
| kotodama | QUALITY criterion 25 (rounds 73/74) | Counter takes `--freeze <40hex>` and **refuses to grade** (exit 2, `FAIL legs=0/<n> (refused: …)`) when `<freeze>` is not an ancestor of `<lands>` on the first-parent chain, when `<lands>` equals the frozen base, when frozen claims cannot be read at `<freeze>`, etc. Zero junk landings shipped with the freeze. | Preventive in-counter gate: rejects a measured revision outside the freeze lineage. Does **not** list post-freeze amendment commits over an arbitrary kill-rule path set; kaidoku's gate is the audit-side counterpart. |
| kotodama | lesson `round-74.md` R74-M9 | "Three freeze commits, not one: `de93d91c…` (first freeze), `3595c919…` (re-freeze), `00c408a0…` (operative freeze)" — same failure class as kaidoku M38-1 (instrument changed after scoring). | Documents the failure mode; no CLI for it. |
| kotodama | `tools/check-judged-object.py` | Packet key records entry-byte sha256 + judged id set at build; at closure compares key vs entry at measured revision (exit 1 = mismatch). | Frozen-through-adjudication digest check; single judged object, not a commit-range drift list. |
| chousa | `tools/research-gate.sh` pin/drift mode | Behavioral baseline of the gate's own output (`--pin` writes normalized baseline; `--drift` diffs; `MORI_DRIFT: none` exit 0). Header says adapted from mori-shokunin r10 `tools/mori-census.sh --pin/--drift`. | Detects drift of the *census's own behavior*, not amendment of a frozen claim rule. |
| chousa | lesson `round-46-verifier-spotcheck.md:58` | Adjudicates a freeze-time sentence/code gap vs a §9 post-scoring rule change **by hand** (widening judged a repair, not a rule change). | Manual adjudication of the exact question QUALITY 79 automates. |
| mori | `tools/mori-freeze-order.py` | Checks frozen claim inputs **predate** their implementation commits (register-driven ordering). | Ordering direction, not post-freeze amendment detection. |
| mori | `tools/mori-source-drift.py` | Re-fetches each `SOURCES.md` row; classifies committed copy vs today's body (fresh/excerpt/drifted). | Source copy drift, not claim-instrument drift. |
| kama | `tools/error-verdict-census.py` | `FROZEN_SOURCE_SHA256` digests; a frozen-instrument digest mismatch raises `CensusFault`. | Frozen-byte pin of instruments, but check is a digest equality, no commit-range enumeration. |
| kama | `tools/prereg-time-check.py` | Flags `frozen_at_utc` guesses after the measured commit. | Time-consistency probe, not a drift gate. |
| souji | `tools/souji-rev-pin.py` | Resolves revisions to durable refs only; refuses non-durable revisions; `input_snapshot` binds owned files to committed blob bytes. | Revision-resolution integrity; not amendment detection. |
| tsukuroi | `tools/check-revision-binding.py` | Counts whether every `--revision` gate binds to a landed/pushed revision (refuses unlanded/unpushed/ambiguous). | Binding strength, not drift. |
| tameshi | `tools/pin-disposition.py` | Read-only probe that worktree content still equals recorded sha256 pins at pinned commits. | Pin-content probe; explicitly "not a verdict transfer". |
| lore | `corpus/tools/dependency_freeze.py` | Pins per-fixture dependency inventories + content digests; verification refuses foreign paths (`DIGEST-MISMATCH`). | Frozen-input integrity, scoped to fixture inventories. |
| mado | QUALITY 7/9/13/24 | "Bind each audit verdict to a commit or frozen-copy sha"; "treat a recheck target as landed only at the named commit". | General principle, no CLI. |
| audio / game-dev-3d | `r79b_freeze_order.py`, `adv1-C-declared-drift.sh` | "freeze instant" in experiment design; "drift" in mutation names. | Name collisions only; unrelated. |

## 3. The exact same-mechanic search

No sibling tool enumerates commits between a freeze and a measured revision touching a kill-rule path set and emits a drift verdict for scoring. The closest mechanics:

- kotodama criterion 25's `--freeze` descendant check — but it runs **inside** the counter and refuses grading; it does not list amendment commits or cover arbitrary paths.
- kaidoku's own `tools/round-31/freeze-integrity.py` (QUALITY 55) — already contains the exact mechanic: after locating the freeze commit (first commit adding `.ufo/waves/round-<N>/claims.json`) it runs `git log freeze..rev -- <path>` per pinned path and prints `commits_after_freeze`. `freeze-drift.py` is a within-lane generalization: drops the digest-pin requirement, takes an arbitrary path set (default: claims doc, both counters, carriers manifest, oracles), adds `--json-out`, and carries the policy verdict ("score with first-freeze bytes; report the amendment, never adopt").

## 4. Judgment: duplicates vs extends

**Extends.** The fleet already had (a) preventive in-counter lineage checks (kotodama 25), (b) ordering gates (mori-freeze-order), (c) frozen-instrument digest pins (kama error-verdict-census; lore dependency_freeze), (d) durable revision binding (souji, tsukuroi), and (e) manual post-scoring-adjudication rules (chousa r46; kama r28 spotcheck "It is still a post-scoring rule"; kotodama R74-M9; kumitate r42 amendment-admissibility rule referenced by chousa/kama). Kaidoku 79/80 **synthesize** these into a standalone, machine-checkable listing gate with an explicit "first freeze is the rule" criterion, plus the generator-path extension (80) that no sibling covers. Wave-1 receipts prove live use: `freeze-drift-077e212b.json` (exit 1, drift = `79f69347`, `f1010f67`), `freeze-drift-cb4326b2.json` (exit 0), `freeze-drift-gen-controls.json` (exit 1, drift = `efd5c47a`).

## 5. Calibration limits

- No sibling tool was executed; behavior descriptions are from source/docstrings (`[INFERENCE]` where not explicit).
- Grep limited to `.md`/`.py`/`.sh`; binary or non-UTF8 files could hide patterns.
- The kumitate r42 rule (referenced by chousa `gen-w1-spec.py` and kama lessons) is defined in `kumitate-shokunin/corpus/lessons/round-42.md` (counter-amended-after-data mistake; plan-amendment admissibility with timestamp). It is the fleet's closest *policy* antecedent to QUALITY 79 but is not machine-checkable; 79 operationalizes it for the round-38 instance.

## 6. Evidence (exact commands)

- `ls /home/vgpnk/Projects/shokunin/{chousa,kama,kotodama,mado,mori,souji,tabi,tameshi,tsukuroi}-shokunin/tools`
- `grep -rn -i "first freeze|first-freeze|post-scoring|kumitate r42|pre-scoring" {chousa,kama,kotodama,mado,mori,souji,tameshi,tsukuroi}-shokunin --include="*.md" --include="*.py"`
- `grep -n -i "freeze|frozen|drift|amend|post-scoring" kaidoku-shokunin/corpus/QUALITY.md` (rows 79, 80)
- `cat kaidoku-shokunin/.ufo/waves/round-38/l1/freeze-drift-077e212b.json`, `freeze-drift-gen-controls.json`
- `head -63 kaidoku-shokunin/tools/round-31/freeze-integrity.py`
- `find /home/vgpnk/Projects/shokunin -name "*.py" -o -name "*.sh" | grep -i "freeze\|drift" | grep -v kaidoku-shokunin`
