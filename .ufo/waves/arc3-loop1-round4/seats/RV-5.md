# RV-5 — seat report (chain c2, reviewer) — wave `arc3-loop1-round4`

Seat RV-5 · chain c2 · role **reviewer** · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `015e1bab914713568f339fd53999bc180459cc40`
(unchanged; no git mutation issued). Lane: devin (`devin/deepseek-v4-1-flash-max`) —
the declared fallback dispatch recorded in `claims-frozen.md:11-15`, not a lane signal.

**Task as frozen:** *adversarial audit of the adjudications — independently re-check
each NO-CHANGE item; is any actually stale?*

**Verdict: two of the chain's eighteen `current` rows are FALSE, and one of the two
`adjudicated` rows is under-classified. The chain's headline `stale=6` is wrong: the
true reading on the same 26-row unit is `stale=8` (F1b, F2, F2b, F3, F5b, X1, X2, C1)
plus one decayed-evidence row (F1a). The named repairs are correct as far as they go;
the failure mode is the *census's test construction*, not the repairs.**

Writes by this seat: this report + `claims/c2/RV-5/**` only. No git mutation. The real
`PROVINCE.md` was **read only** and is byte-identical to its HEAD blob
(`d075a3c6…`, 162 lines) at report time; every apply ran on a `/var/tmp` scratch copy.
Custody paths were never opened. Scratch `/var/tmp/rv5-r4` (never `/tmp` — standing
EDQUOT rule).

## 1. Work performed (evidence pointers)

All artifacts under `.ufo/waves/arc3-loop1-round4/claims/c2/RV-5/`:

| artifact | sha256 | what |
|---|---|---|
| `evidence/audit-summary.txt` | `2a7c4ec6…` | the 26-row table: chain verdict vs this seat's verdict, row by row |
| `evidence/f2b-knob-measurement.txt` | `2f109e56…` | **the decisive falsifier** — the cap-raising knob exists, 7 legs (A-G) |
| `evidence/x2-falsifier.txt` | `5bd99ed1…` | the admitted pairs beyond expac + the census test that missed them |
| `evidence/f1a-evidence-decay.txt` | `08b5d8a0…` | the r3-08 target is gone from disk (same class as F2) |
| `evidence/census-ptr-blindness.txt` | `72423d20…` | zero `ptr` assertions emitted; `ptr_check` called directly |
| `evidence/census-ptr-sabotage.txt` | `37f2e126…` | causal proof: a beyond-EOF pointer reads PASS |
| `evidence/vz2-census-rerun.txt` | `bdefd8c6…` | this seat's re-run of the chain's own census instrument |
| `evidence/patch-apply-and-census.txt` | `d6816677…` | my two repair patches applied on scratch, census PASS, 162→162 |
| `evidence/pointer-anchors-on-patched-tree.txt` | `45480ea0…` | the 3 PROVINCE/SHONEN pointer-table anchors on my patched tree |
| `evidence/probe-on-patched-tree.txt` | `b383f0b2…` | the citation-drift probe's own result on a scratch root |
| `evidence/identity-rederivation.txt` | `b01c148a…` | every identity re-derived at write time (rule #14); content is repo-target/instrument hashes only, so the file is idempotent — re-run it and it re-derives itself |
| `proposed-f2b-cap-knob-repair.patch.md` | `9b6f7974…` | patch text: the F2b existential clause |
| `proposed-x2-pacman-pairs-repair.patch.md` | `52945aa9…` | patch text: the X2 clause (+ carries EX-13's first-clause repair) |

**Method note (rule #14).** No seat's tally was adopted. The chain's census instrument
(`claims/c2/VZ-2/evidence/province-staleness-census.py`, sha256 `e6eef574…`) was read in
full, re-run by this seat on the real tree and on patched scratch trees, and each of its
26 rows re-derived against admitted corpus state or a live command. The two rows this
seat calls false were then falsified by **live probes**, not by reading.

## 2. Proposed changes (patch-text paths)

1. **`proposed-f2b-cap-knob-repair.patch.md`** (`9b6f7974…`) — repairs the F2b clause
   `Needs a cap-raising knob or partial-core intake — neither exists`, which is false
   (§3.2). **This also supersedes EX-13's `province-frontier-recorded-crashes-organic.patch.md`
   on its second half**, which repairs the first half correctly but carries the same
   false existential clause forward verbatim ("No cap-raising knob or partial-core
   intake."). Landing EX-13's patch alone leaves a falsified claim in a scoped file.
2. **`proposed-x2-pacman-pairs-repair.patch.md`** (`52945aa9…`) — repairs the X2 clause
   `multi-version pacman pairs beyond expac unexercised`, which is false (§3.3). The
   patch carries EX-13's first-clause repair too, because both target the same four
   physical lines and cannot land as two independent hunks.
3. **Flag (not a patch): F1a's named evidence artifact has decayed off the host**
   (§3.4). The bullet is still true as a *held* claim, but its cited target no longer
   exists — the same class the chain used to adjudicate F2, applied to a row the chain
   did not check. The parent's call whether to re-ground it or leave it.

Everything else: **none**.

## 3. Before → after measurement for the chain's claim

Frozen falsifiable form: *the staleness census → stale count N → 0; PROVINCE line count
unchanged; census PASS at the work tree after the parent applies the patches.*

### 3.1 The 26-row audit (the deliverable)

| id | chain | RV-5 | basis (first-hand) |
|---|---|---|---|
| F1a | current | **DECAYED** | cited target `cli-arm64.exe` no longer on disk (§3.4) |
| F1b | stale | stale | agreed |
| F2 | adjudicated | **STALE** | a 17.6 MB organic core inspects (this seat re-derived `ev_913e9789…`, 53 segments); the bullet's own first clause is false as written |
| F2b | current | **STALE** | **the knob exists** (§3.2) |
| F3 | stale | stale | agreed |
| F4, F5a, F5c | current | current | agreed |
| F5b | stale | stale | agreed (doubly) |
| X1 | stale | stale | agreed |
| X2 | current | **STALE** | **pairs beyond expac exercised** (§3.3) |
| G1, S1-S4, S6, S7 | current | current | agreed (S1-S4 live `doctor` re-derived here) |
| S5 | adjudicated | adjudicated | agreed, **with caveat** (§4 A6) |
| C1 | stale | stale | agreed (found independently before reading VZ-2's row) |
| R1-R6 | current | current | agreed |

Headline: chain `stale=6 adjudicated=2 current=18` → RV-5 `stale=8` + 1 decayed + 1 adjudicated.

### 3.2 F2b — the cap-raising knob EXISTS (the strongest finding)

The row asserts `Needs a cap-raising knob or partial-core intake — neither exists`.
The chain's evidence was `corpus_has(corpus, "No flag to raise the cap is exposed")` —
a sentence about the **verb schema**. Measured on a real 36,360,192-byte core
(`coredumpctl dump 1214442`; git SIGBUS 2026-10-19 09:05 −03):

| leg | command | result |
|---|---|---|
| A | 6.7.0, no knob | refused `invalid_request`/`out_of_range` |
| **B** | **6.7.0 + `REA_PWNTOOLS_MAX_INPUT_BYTES=40000000`** | **exit 0**, `ev_367c6cb419b75675348d7fb16f8673f743133e15d547fadf86a78f5eae56057e`, `elf-core`, 49 segments, 1 thread |
| C | 6.5.0, no knob | refused |
| **D** | **6.5.0 + knob** | **exit 0**, `ev_0ed48c73e94bf032f9214b6b5183f5df7438b6d8d77585726f66c4059bebfe9d`, 49 segments |
| E | 6.4.0 + knob | refused — key absent in 6.4.0's dist |
| F | dist grep | key present in **4 files** in 6.7.0 and 6.5.0; **0** in 6.4.0 |
| G | `--schema` | no size/limit option — the r2 sentence holds, *scoped to the schema* |

So the true statement is: *the verb schema exposes no cap flag; the cap is raised by
`REA_PWNTOOLS_MAX_INPUT_BYTES` on 6.5.0/6.7.0.* The row's existential clause is false.

### 3.3 X2 — pacman pairs beyond expac WERE exercised

`corpus/knowledge/2026-10-13-r2-version-diff-compare.md:11-18` — the entry the row
cites — records **three** pairs: `op` 2.34.1→2.40.0, `expac`, and **`bwrap`
0.11.2→0.12.0**. Admitted at `corpus/README.md:33` and `:91` (the map row's probe cell
reads "live compares on expac/**bwrap** pairs"). `r4-10` adds `op` + `qpdf`
12.3.2→12.4.1 through the full pipeline (admitted at `:35`, `:140`); `r4-09` adds the
obsidian pair.

**The defect, named exactly.** VZ-2's row reads:

```python
add("X2", ..., corpus_has(corpus, "expac")[:3], "current",
    "no corpus entry claims a further pacman version pair")
```

`corpus_has(corpus, "expac")` is a **presence test** — satisfied by the very file that
lists `bwrap` two lines below the word. The instrument returns a hit on its own
falsifier, and the note's assertion is contradicted by `corpus/README.md:91`.

### 3.4 F1a — the same decay class, unchecked

`PROVINCE.md:82-83` cites `cli-arm64.exe` (r3-08). The corpus row's own source pointer
(`corpus/knowledge/2026-10-13-r3-pe-arm64.md:15`) names
`/home/vgpnk/.cache/uv/archive-v0/M1E0QXq07p7Gx3Fp/setuptools/cli-arm64.exe` — **gone
from disk**, and a host-wide hunt finds no `cli-arm64.exe`. The *claim* survives (a
sealed past run), but the evidence pointer no longer resolves — precisely the class the
chain used to adjudicate F2, applied to a row it read `current`. Contrast: r7's target
is still present (91,662,336 B, `7a2ccd68…`).

### 3.5 The repairs themselves — measured, not read

- **Reproduced independently:** applying EX-14's v2 candidate
  (`0b8ad045…`) on a fresh scratch tree yields
  `69ceea9b5f9aa5958af45d85a1f757b943a6be553f378d44b51c809b0787c9c5`, 162 lines —
  **byte-exact match to VZ-2's claim**.
- **My two patches:** applied with RV-4's `prose-apply.py` (1 hunk each, 3-/3+ and
  4-/4+), `162 → 162` lines, census **PASS 0/0/0/0**, all three pointer anchors HOLD
  (`prov18-stamp-named`, `prov18-pin-value`, `shonen-province-range`), DATED markers at
  :40/:45/:119 intact, `:18` needles intact. After-digest `1391927d…`.
- The census on my patched tree reads `undeclared=0` — i.e. the new line
  `REA_PWNTOOLS_MAX_INPUT_BYTES` is needle-free (`\brea\b` does not match inside it),
  **measured**, not reasoned.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the chain's `current` rows are trustworthy because they cite corpus" | **refuted twice** — F2b and X2 are false. The shared cause: rows whose truth is an *existential/negative* proposition were graded by a *keyword-presence* test |
| A2 | "the census gate backstops the census instrument" | **refuted, measured** — the gate is blind to all of this by construction: PROVINCE 72-118 and 132-162 are UNDECLARED, and the gate's `REA_GATE` never fires on the EVM/crash bullets. It reads PASS on the real tree *and* on my patched tree identically |
| A3 | "`ptr_check` covers the `config.toml:3298` pointer" | **refuted, and made causal** — zero `ptr`-kind assertions are emitted anywhere in the run; `ptr_check` is reached only when a clause carries no pin. Called directly it returns `stale` for `:3298` and `ok` for `:3546`. **Sabotage proof:** rewriting the pointer to `config.toml:999999` (beyond EOF of a 3,570-line file) still reads `VERDICT: PASS`. (The same sabotage arm also reproduced the known H2 masking when a version token shares the line — a separate, already-named residual) |
| A4 | "the knob finding is a 6.7.0-only artifact / not a real capability" | **refuted** — it fires on **6.5.0** as well (leg D), and both are live pins. It is absent on 6.4.0 (the historical pin), so the finding is version-scoped, and I state it that way |
| A5 | "EX-13's F2 patch already covers the crash bullet, so nothing more is needed" | **partially sustained, then refuted** — it repairs the inventory half correctly and I credit it; but it **carries the false existential clause forward verbatim**, so the bullet would still be false after landing. My patch supersedes it on that half |
| A6 | "S5's adjudication is sound as written" | **agreed with a caveat** — the citation is receipt-stamped and the *value* claim is current (live pins re-read here: devin/omp `6.5.0`, kimi `6.7.0`). Caveat: the named receipt file `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt` is a 6-line hash receipt that **does not itself carry `:3298`** — the pointer lives in the round-3 seat records. So "historical-by-declaration" is right, but the declaration is the round-3 record, not the receipt. Worth one clause at landing; not a false claim |
| A7 | "F2's adjudication ('the text is not false') survives scrutiny" | **refuted** — the bullet's first clause ("all 3 organic cores exceed the cap") is false as written: a 17.6 MB organic core inspects (re-derived here: `ev_913e9789…`, 53 segments, exit 0). EX-13 independently found and patched this; the chain nonetheless left it `adjudicated`, not `stale` |
| A8 | "my own patches are cosmetic / would break a gate" | **refuted, measured** — both apply cleanly, hold 162 lines, PASS the census, and hold all three pointer anchors (§3.5) |
| A9 | "the probe validates the patched tree" | **could-not-evaluate, recorded honestly** — the citation-drift probe requires a Git work tree and refused a scratch root (`root_unreadable … exit=2`); its selftest is `13/13 CLEAN`. I substituted an anchor-level equivalent check on the same three PROVINCE/SHONEN entries rather than claiming a probe run I did not get |

## 5. Blockers, if any

1. **The chain's census needs its two defective rows re-keyed, not just re-run.**
   `province-staleness-census.py` rows `X2` (keyword-presence) and `F2b`
   (schema-sentence) cannot reach their own falsifiers. Re-running the instrument after
   the repairs land will still read them however the patch is written, because the
   `ANCHORS` are the old literals. This is a **chain c2 instrument** — its owner's call;
   I have not edited it (no seat writes another seat's instrument).
2. **F1a's decay is a class, not an instance.** Any bullet whose evidence is a host
   artifact can decay silently. The chain found this for F2 and did not generalize it.
   Named for the parent; no patch proposed (the claim itself is true).
3. **The C1 Vyper coupling is real and unchanged.** My patches add no dependency on it;
   EX-14's v2 `Vyper 0.4.3 (r4)` clause remains conditional on C1's corpus entry landing
   in the same commit, exactly as VZ-2's verdict states. I did not re-litigate it.
4. **The custody README/tool are dirty in the worktree** (`M .ufo/gates/custody-pair/*`)
   — another seat's authorized in-flight writes, not mine; noted so the parent does not
   attribute them here.

## 6. Files written by this seat

- `.ufo/waves/arc3-loop1-round4/seats/RV-5.md` (this report)
- `claims/c2/RV-5/proposed-f2b-cap-knob-repair.patch.md`
- `claims/c2/RV-5/proposed-x2-pacman-pairs-repair.patch.md`
- `claims/c2/RV-5/evidence/` — 12 files (sha256s in §1)
