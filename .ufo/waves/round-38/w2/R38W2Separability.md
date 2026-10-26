# R38W2Separability — causal separability of R38-C1 / R38-C2 on the landed bytes (wave 2)

**Verdict: FALSIFIED (one direction).** C1 is causally separable from C2 — its verdict is
byte-identical with C2's pointer repair reverted and with C2's whole bookkeeping commit absent.
C2 is not separable as landed: its `126/126` count and its `## Owned axes` pointer both depend on
C1's knowledge entry, and the literal counterfactual the seat asked for — "C2 landed, C1 never
landed", C1 entry + README rows + receipts dropped, coverage restated — makes the frozen C2
counter exit **1** (`mismatches 1`, the row's pointer into the deleted C1 entry). C2 returns to
`exit 0` only after its *prose* is also de-coupled from C1 (proven state, receipt `c2-a2.json`).

Seat: `R38W2Separability` (leaf, advisory). Instrument: the **first-freeze** counters only
(`e059ca9391642d5b71b6662cabcbdce0d9308719`, sha256 `a7a62b09…` C1 / `7f137b66…` C2 — copies and
hashes in `artifacts/R38W2Separability/`). Nothing in the lane, the freeze, the carriers or the
oracle was modified; every measurement ran against a scratch fixture repo.

## 1. What was run

Fixture repo built per bounds (`mktemp -d` + `git init`, toplevel verified, lane fetched
read-only, fixture-only commit identity). Two directions were constructed:

- **"C2 landed, C1 never landed"** (parent = landed tip `0fc61133`; drop the C1 entry
  `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`, its README rows, and
  `corpus/evidence/round-38/c1/`; re-state the coverage count).
- **"C1 data landed, C2 not"** (revert the PROVINCE `## Core` `REA MCP server` doctor pointer to
  the base `evidence/doctor/`, on both the C1 verdict revision `3b960fe5` and the landed tip).

Full command lines, fixture commit map and variant definitions: `artifacts/R38W2Separability/REPRODUCE.md`.
Every receipt cited below is a full frozen-counter JSON in that directory. My independent runs
reproduce the L1's own receipts exactly: `c1-landed_c1.json` == `l1/scores/c1-v1-at-3b960fe5.json`
and `c2-landed_c2.json` == `l1/scores/c2-at-0fc61133.json` after dropping `argv`/`revision`.

## 2. C2 with C1's landing removed or altered (frozen `c2-counter.py`)

| fixture | state under test | exit | mismatches | detail |
|---|---|---|---|---|
| base `77091b49` | before (no C1, no C2) | 1 | 1 | `[["prov_core:REA MCP server","evidence/doctor/"]]`, `guards_ok false`, O1 124/124 |
| landed `0fc61133` | C1 + C2 | **0** | 0 | O1 126/126, `guards_ok true`, pointers 52 |
| `a3` | C2 landed, **C1 receipts dropped only** | **0** | 0 | O1 126/126 — C2 does not read C1's receipts |
| `a0` | entry+coverage row+receipts dropped, **count left 126/126** | 1 | 2 | O1 `stated [126,126] observed [125,125]` **and** unresolved `[["owned:coverage","corpus/knowledge/2026-10-26-r38-…-recursion.md"]]` |
| `a1` | as `a0`, count restated 125/125 (prose keeps both entry names) | 1 | 1 | O1 passes (125/125); the **pointer** into C1's entry still dangles |
| `a1b` | literal instruction: entry + **all three** README lines naming the stem + receipts dropped, count 125/125 | **1** | 1 | same dangling `owned:coverage` pointer |
| `a2` | `a1b` + SCORECARD prose de-coupled ("one entry … `unblob-format-matrix`") + PROVINCE:157 round-38 note reverted | **0** | 0 | O1 125/125, `guards_ok true`, pointers 51 (base 48) |
| `a4` | C1 entry **present**, its coverage-map row missing | 1 | 1 | O1 `stated [126,126] observed [125,126]` |
| `a5` | C1 landed, C2's count **not** restated (row left 124/124) | 1 | 1 | O1 `stated [124,124] observed [126,126]` |
| `b` | C1 data landed, C2's pointer **and** count not landed (pre-round 124/124) | 1 | 2 | O1 `[124,124]` vs `[126,126]`, doctor pointer unresolved, `guards_ok false` |

**Answer:** C2 does *not* verify without C1 in the state the seat prescribed. The single reason is
the C2 landing's own coverage row, which names `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`
(SCORECARD.md:23) — a pointer into C1's claim artifact. The frozen counter catches it
(exit 1, `mismatches 1`), so no false `met` is possible; but the landed C2 verdict is
**conditionally true on C1's landing**, not independently true.

The reverse arithmetic is equally sharp: C1's landing *alone* falsifies C2's pre-existing count
(`b`: stated 124, observed 126). C2's `met` therefore requires a restatement that is a function of
C1's landing; the pair is order-coupled (C1 → count) even though the counters are read-disjoint.

## 3. C1 with C2's repair reverted (frozen `c1-counter.py`)

| fixture | state under test | exit | carriers_matched | bindings |
|---|---|---|---|---|
| `3b960fe5` | C1 verdict revision (C1 data + C2's pointer repair) | 1 | 3 | `core_section false`, `core_row false`, `frontier_note true`, `entry true`, `sourced true`, `coverage_map true` |
| `0fc61133` | landed tip (+ C2's SCORECARD/LOG/lesson commit) | 1 | 3 | identical |
| `b` (`7889156b`) | doctor pointer **reverted** at `3b960fe5` | 1 | 3 | identical |
| `b2` (`a6404602`) | doctor pointer **reverted** at the landed tip | 1 | 3 | identical |
| base `77091b49` | before | 1 | 0 | `frontier_note true` (see F2), all other bindings false |
| `a2` | C2 landed, C1 never landed | 1 | 0 | `frontier_note true`, `entry/coverage_map/sourced false` |

`c1-landed_c1.json`, `c1-landed_c2.json`, `c1-b.json`, `c1-b2.json` are identical JSON after
dropping `revision`/`argv` (verified by dict comparison, `True` for all three pairs). K2 remains
the only carrier miss: 3/3 oracle files published, handler `squashfs_v4_be`, `after_gaps_empty`
false on one `unpublished-entry` gap for the in-tree symlink `firmware.bin_extract/var/lib/run-link`
(`c1-landed_c1.json` → `carriers.K2`).

**Answer:** the C1 verdict does not change when C2's doctor-pointer repair is reverted — not the
carrier count, not a single binding. C1 is verifiable without C2.

## 4. Findings

**F1 (defect, calibration — the seat's target). C2's landed verdict is conditional on C1's
landing, in two channels.** (a) The stated count: `126/126` is only observable because C1's entry
exists (`a5`/`b` exit 1 with 124 stated, 126 observed). (b) Provenance: the same row carries a
pointer to C1's entry, so removing C1's data breaks pointer resolution (`a1`/`a1b` exit 1). The
frozen separability sentence — "C2 … never touches C1's receipts or carriers. C1 reads none of
SCORECARD/SHONEN." — is *literally true and empirically confirmed* (`a3` exit 0 with C1's receipts
deleted; source greps of both frozen counters for the other's surfaces return no lines), but it
does not cover C1's **knowledge entry**, which C2 both counts and points at. Severity: no false
`met` landed (the counter would fail first); the exposure is a future C1 unwind silently
falsifying the landed C2 record.

**F2 (calibration — C1 instrument).** `frontier_note` is satisfied by pre-existing round-36 bytes:
`true` at the base `77091b49` and `true` in `a2`, where C1's PROVINCE:157 round-38 extension was
reverted to the base text. The binding cannot distinguish a moved frontier from an unmoved one,
so the predicate clause "the round-38 frontier note supersedes the big-endian Frontier bullet" is
not measured by the frozen counter. (Does not change C1's verdict — it fails on other conjuncts.)

**F3 (calibration — verdict granularity).** The C1 honest-stop verdict has **three** unmet
conjuncts, not one: K2's `unpublished-entry` gap *plus* `province_core_section == false` and
`province_core_row == false` — PROVINCE has no `## Round-38 additions to Core` section at all
(`git diff 77091b49 3b960fe5 -- PROVINCE.md` touches only line 44 and line 157; `grep -n 'Round-38' PROVINCE.md`
matches only the appended note inside line 157). The SCORECARD round-38 row states "Core-row
bindings false" correctly; the lesson's verdict sentence (`corpus/lessons/round-38.md`, "K2 fails
on one `unpublished-entry` gap") and the wave-2 dispatch's paraphrase name only the gap.

**F4 (landing granularity, informational).** Claim-level revert is impossible at commit
granularity: `3b960fe5` carries C1's data *and* C2's pointer repair (PROVINCE.md:44) in one commit,
and C2's count restatement is in the next commit (`0fc61133`). Separation exists only at file
level. This is why the `b` fixture is the faithful "C2 not landed" state and not a plain revert of
`0fc61133`.

**F5 (scope, informational).** C2's predicate scores only `## Owned axes`, `## Capabilities`,
SHONEN boxes and PROVINCE `## Core`/`## Frontier`. Its own `## Round 38` section, which cites C1's
receipts and scores files, is outside every scored unit — so the round's own record pointers are
not checked by the calibration counter (consistent with the wave-1 C2 critic's disclosed blind
spots; recorded here only as the reason F1's pointer channel is invisible except through the
coverage row).

## 5. Impacted axes

- **calibration (C2's axis):** the verdict is conditional on a sibling claim's landing, and the
  round's own C1 verdict sentence understates its failed conjuncts (F1, F3).
- **coverage (C1's axis):** unaffected — C1's counter output is invariant to every C2 write tested
  (F4 shows why byte-level edits, not commits, are the separable unit).
- **coverage proxy (C2's O1):** C1's landing moves the very number C2 asserts (124 → 126), so the
  coverage proxy and the calibration claim are coupled one-way through `corpus/knowledge/`.

## 6. Smallest safe correction

1. **Lesson (one line).** In `corpus/lessons/round-38.md`'s verdict sentence, name all three unmet
   C1 conjuncts (K2 gap + `province_core_section` + `province_core_row`); the SCORECARD row is
   already correct.
2. **Restatement note on the C2 record.** Where the round states `126/126`, record that the count
   and the two-entry list hold only while the R38-C1 entry exists; withdrawing C1's landing
   requires restating the row to `125/125` with the C1 entry name dropped. That state is proven
   green: fixture `a2`, `exit 0`, `mismatches 0`, `guards_ok true`, O1 125/125
   (`artifacts/R38W2Separability/c2-a2.json`).
3. **Freeze-level guard for later rounds (optional, structural).** Either keep counted surfaces
   free of sibling-claim artifact names, or make the validation step run each frozen counter once
   against a fixture with the sibling claim removed — `a1b` is the ready-made red case
   (`exit 1`, `mismatches 1`) for such a self-test.

No change to any frozen predicate, counter, carrier, oracle or control is proposed.

## 7. Author-verdict calibration (adjacent, checked because it is the round's calibration claim)

- **R38-C2 "met"** — **CONFIRMED**: my run of the first-freeze counter at `0fc61133` is byte-identical
  to `l1/scores/c2-at-0fc61133.json` (`mismatches 0`, `guards_ok true`, exit 0, O1 126/126).
- **R38-C1 "honest stop"** — **CONFIRMED, under-described** (F3); `carriers_matched 3`, `met_target
  false`, exit 1, with three failed conjuncts rather than one.
- The wave-1 seat `R38ConnSeparability`'s source-level conclusion (read/write disjointness, no
  causal loop) is **reproduced** here and extended with the counterfactual runs: the disjointness
  holds, but verdict-level separability does not, for C2.

## 8. Limits

- [INFERENCE] The `a2` state is my construction of "C1 never landed"; the lane's actual history
  landed C1 before C2, so no false claim is on record. The finding is about conditional
  verifiability, not about the landed bytes being wrong at their own revision.
- The fixtures are single-edit constructions from the landed tree; I did not enumerate every
  possible C1 unwind (e.g. keeping the entry while deleting only its receipts is covered by `a3`,
  and deleting only the coverage row by `a4`).
- Read/write disjointness is established by source grep plus the `a3`/`b` runtime probes, not by a
  syscall trace; both counters are short, constant-path scripts whose only writes are `--json-out`
  and a `tempfile.mkdtemp` under `$HYAKU_SCRATCH/kaidoku-r38` (removed in `finally`).
- No tool was installed or upgraded; `nix`/`pacman` untouched (pacman paused host-wide). REA was
  not invoked — the C1 counter reads committed receipts and recomputes evidence ids through the
  frozen `tools/round-27/xpin-attribute.mjs` at the freeze.

## 9. Bounds compliance

- Wrote only this report and `artifacts/R38W2Separability/` (plus the scratch dir, removed on exit;
  nothing cited lives there). No lane surface, tool, counter, carrier or VCS state was modified;
  the lane was read with `git show`/`ls-tree`/`diff` and a read-only `fetch` **into the fixture**.
- No subagents, no background jobs, no `agent://all` messages.
