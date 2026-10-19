# SC-2 — seat report (chain c2, role scribe)

Wave `arc3-loop1-round4` · lane devin (declared fallback; the hyper lane returned
402 out-of-credits on all 48 seats — recorded in the freeze, not a lane signal) ·
2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`015e1bab914713568f339fd53999bc180459cc40` at every read.

Task (seat line): "records drafts for the parent (not applied): LOG + SCORECARD
section drafts, PIN-FREE. `claims/c2/records-drafts/` (two files)."

**Verdict: delivered.** Two draft files plus a measured pin-free simulation and
its receipts. Nothing outside this seat's write scope was touched; no git
mutation; no custody path opened; scratch under `/var/tmp/sc2-r4` only (never
`/tmp` — standing EDQUOT rule).

---

## 1. Work performed (evidence pointers)

**Deliverables (2 files, as specified).**

| file | bytes | content |
|---|---|---|
| `claims/c2/records-drafts/LOG-entry-draft.md` | 13,362 | the LOG.md entry as literal text between BEGIN/END markers + parent notes |
| `claims/c2/records-drafts/scorecard-section-draft.md` | 18,333 | the SCORECARD.md section, same shape, plus the measured §3 simulation table |

**Supporting evidence (this seat's own, under the same directory).**

| artifact | what |
|---|---|
| `evidence/commandA-head.json` | command A re-run first-hand at HEAD (SCORECARD recipe A, verbatim) |
| `evidence/census-{base,records,control}.json` | the three gate captures (raw `--json`) |
| `evidence/pin-free-simulation.txt` | the simulation summary + the five-revision trail |
| `evidence/SHA256SUMS` | re-derived at write time; `sha256sum -c` OK |

**First-hand measurements taken by this seat (not copied from any peer).**

1. **Baseline at HEAD.** Command A (recipe A verbatim, reading immutable Git
   objects):
   `{"knowledge_files": 83, "mapped": 83, "missing": [], "dangling": [],
   "citation_resolved_rules": 14, "rule_blocks": 14, "coverage_score": 10.0,
   "depth_score": 10.0, "revision": "015e1bab…"}` — `evidence/commandA-head.json`.
2. **Gate baseline.** `.ufo/gates/c1-census-v10.py` → `VERDICT: PASS
   (stale=0 ambiguous=0 undeclared=0 unresolved=0)` exit 0, scope-errors `[]`,
   unreadable `[]`, G2 floor 17/14/3; instrument sha256 `d0772ce8…`, 610 lines.
   `PROVINCE.md` 162 lines, sha256 `d075a3c6…`.
3. **Independent content census of the Frontier + surface summary.** Every bullet
   of both Frontier sections checked against admitted corpus state with its
   falsifying file named (the table is in both drafts). Findings: the PE-subtypes
   reserve was consumed; the ">90 MB PE wall" bullet's advice was overtaken and
   its absolute "Not OOM" no longer holds as a statement about the target (a later
   round measured that target memcg-OOM-killed at a 7 GiB cap with ten decompile
   workers, surfaced by the provider as a cancellation — the recorded mislabel
   class); the JEB half of the alternate-providers bullet is superseded by a
   later probe; the EVM bullet's "untested" is falsified for the solc half; the
   cross-version-residuals bullet is falsified outright; the recorded-crashes
   bullet's claim holds but its named exemplar expired (re-measured population:
   656 MB / 172.8 MB / 36.4 MB decompressed, all over the cap; the no-knob clause
   re-confirmed against the verb's own `--schema`, which exposes only a path and
   a debugger-context input).
4. **The one-row reconciliation.** A Core host-fallback-readers row lists five
   tools as absent that are present and package-owned (`7z`, `xxd`, radare2/r2,
   `strace`, `upx` — all `command -v` resolved; install epoch 2026-10-13 13:52
   -03 from the package manager's own log) while `cabextract`, `rizin`,
   `ltrace`, `pacman-contrib` are genuinely absent. I re-read the gate's declared
   scope table and the row's git history: the row sits in a **DATED** range and
   is a Core table row, so it is outside the claim's **narrow** unit (Frontier
   bullets + surface-summary claims). Both drafts state the resulting boundary
   explicitly: **6 stale under the broad reading** (the chain verifier's, which
   the drafts quote) and **5 under the narrow one**, with the difference being
   exactly that row.
5. **The gate's certificate boundary, measured.** The gate's `REA_GATE` needle
   family does not match the EVM bullet's text, so the bullet under repair emits
   **zero** loci in both the baseline and the patched state — the gate neither
   validates nor refutes that repair. Both drafts say so, and both name the
   census table (not the PASS) as the claim's certificate. A reviewer seat
   measured the same thing independently.
6. **C3's landed values, re-derived first-hand** before folding them into my
   drafts: tool `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`
   (1343 lines), README `9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`
   (272 lines), and a selftest re-run on a scratch copy with the tool's basename
   preserved → `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`.

**Pin-free simulation (the drafts' own gate).** Three scratch roots under
`/var/tmp/sc2-r4/sim5` holding HEAD copies of the three gate-scoped files:
`base` untouched; `records` carrying both literal blocks appended; `control`
carrying the same plus one planted pin line. Gate identity bracketed before and
after every run.

| tree | SCORECARD lines | loci | verdict | exit | output sha256 |
|---|---|---|---|---|---|
| base | 1580 | 9 | PASS 0/0/0/0 | 0 | `7cb9b513412f47b0…` |
| records | 1744 | 9 | PASS 0/0/0/0 | 0 | `990598ba5bb3bfe4…` |
| control | 1745 | 10 | FAIL undeclared=1 | 1 | `4b8e7970c2113fd0…` |

PROVINCE.md (162/6) and SKILL.md (390/2) unchanged in all three trees; the G2
per-file floor unchanged between base and records. **Added loci: 0.** The control
proves the detector is live on the appended region.

## 2. Proposed changes (patch-text paths, or "none")

**No patch text and no target write by this seat** — the scribe role writes
records drafts only. The two deliverables are drafts for the parent to append at
EOF; every `⟨FILL⟩`/`⟨PARENT-FILL⟩` slot names its producing seat or is a
landing-time value.

- `claims/c2/records-drafts/LOG-entry-draft.md`
- `claims/c2/records-drafts/scorecard-section-draft.md`

Neither draft was applied. `LOG.md`, `SCORECARD.md`, `PROVINCE.md`, `SKILL.md`,
`corpus/`, any README and `SHONEN.md` were **not** touched by this seat (verified
by the fact that the gate's baseline capture reproduces byte-identically across
every run and the three scoped files' shas are unchanged at close).

## 3. Before → after measurement for the chain's claim

The frozen C2 claim: *every PROVINCE Frontier bullet and surface-summary claim is
census-checked against the admitted corpus state; every stale item is repaired
same-line (line count held) or adjudicated NO-CHANGE with cause; the census
instrument reads PASS at the records commit; the repairs land as patch texts
applied by the parent.*

| unit | before (HEAD `015e1bab…`) | after (patched scratch tree) |
|---|---|---|
| chain verifier census (count of record) | 26 rows: **stale 6**, adjudicated 2, current 18 | **stale 0** (the six repaired; the two adjudicated stay NO-CHANGE with cause) |
| this seat's narrow-unit reading | 5 stale | 0 |
| gate verdict | PASS 0/0/0/0 exit 0 | **PASS 0/0/0/0 exit 0** (and byte-identical verdict surface across every scoped-file patch, measured by the reviewer seat) |
| PROVINCE line count | 162 | **162 (held)** — line-neutrality is load-bearing: a patch that shifts the DATED row's marker line reads a marker SCOPE-ERROR → FAIL |
| PROVINCE sha256 | `d075a3c6…` | ⟨parent: re-derive after applying the patch set⟩ |
| command A | 83/83, 14/14, 10.0/10.0 | unchanged (C2 touches no corpus file) |

**Honest status of the "after" column.** The after-values above are the ones this
seat could measure: the gate's PASS on patched scratch trees (measured here and
independently by the reviewer), and the chain's staleness count driven to zero by
the landing candidate patch set. **The patches are not applied to the real tree
by any seat** — that is the parent's landing step — so the PROVINCE sha256 in the
drafts' slots is deliberately left unfilled rather than guessed. An unrun check
has not passed.

## 4. Attacks / refutations attempted, with verdicts

| # | attack / check | result |
|---|---|---|
| 1 | **Re-classify the false-absence row as an in-unit CURRENT-scope claim.** | **refuted** — the row sits in a DATED range (PROVINCE 45-62) and is a Core table row, not a Frontier bullet or surface-summary claim. Revision 1 of my draft had it wrong; the drafts now carry the boundary (6 broad / 5 narrow) instead of a single silent number. |
| 2 | **Count the recorded-crashes bullet as stale** (its named exemplar is gone). | **partly refuted** — the class claim holds on the surviving population and the no-knob clause holds against the verb's own schema; only the exemplar expired, by the retention-decay rule the bullet itself declares. Adjudicated NO-CHANGE with the exemplar flagged for a same-line refresh. |
| 3 | **Is the "Not OOM" clause really falsified?** | **sustained, with wording narrowed** — the clause was written as an absolute about the target; a later round measured that target memcg-OOM-killed at a 7 GiB cap with ten decompile workers. I first wrote "falsified" flatly, then narrowed it to "no longer holds as a statement about the target" because the original run's own observation (RSS ~2.36 GB at kill) was true for its envelope. |
| 4 | **Is the EVM bullet's defect really "untested", or is the Frontier placement the defect?** | **the word, not the placement** — both EVM entries state "RESULT-class, no Core promotion" verbatim, so a Frontier bullet is the correct home; the falsified token is "untested". This is also why a demo patch that wrote a Core promotion into that line was **sustained as a content defect** by the reviewer seat — an assertion the corpus's own scope lines disclaim. |
| 5 | **Does the gate certify the repair?** | **refuted** — measured: the bullet emits zero loci in both states (its text never matches the needle family). Both drafts state the certificate boundary. |
| 6 | **Is the pin-free property asserted or measured?** | **measured** — three-tree simulation, zero added loci, with a planted-pin control that flips to FAIL undeclared=1 exit 1. Re-measured after every one of five revisions. |
| 7 | **Do my drafts introduce a gated token when the parent fills the slots?** | **not closed by me — flagged** — the control shows one planted pin line is enough to FAIL; both drafts instruct the parent to re-run the simulation after filling. |
| 8 | **Peer-count disagreement** (my 5 vs the chain verifier's 6). | **reconciled as a stated boundary, not smoothed** — the difference is exactly one row and its unit classification; both drafts report both numbers and why. |
| 9 | **Did the drafts survive their own revisions?** | **yes, re-measured each time** — the five-revision trail (with each revision's census outputs) is in `evidence/pin-free-simulation.txt`; the earlier outputs are kept rather than overwritten so the self-correction is auditable. |

## 5. Blockers

**None for this seat's deliverable.** Two dependencies the parent owns, named in
both drafts:

1. **C1's corpus entry is still patch text.** The C2 repair of the EVM bullet
   asserts a Vyper holding; C1 landed its measurement (five carriers, 15/15, 7/7,
   22/22 K/K; the C1 scribe's scratch-tree rehearsal of entry+token reads 84/84
   with the prior 83 byte-identical) but its corpus entry is not in
   `corpus/knowledge/` (still 83 files). **Land the C2 repair and C1's entry in
   the same commit, or fall back to the solc-only wording.** The round's own
   apply-and-measure seat and its reviewer flagged this independently.
2. **The Frontier region is undeclared in the gate's scope table.** A repair that
   must carry a version needle there needs a same-commit scope re-key of
   `.ufo/gates/c1-census-v10.py` — chain c1's instrument, not a c2 seat's to edit.
   Every repair in the round's set avoids this by being prose-only.

**Not a blocker, recorded:** the README under the custody tool churned four times
inside the landing window (`f30df42e…` → `91fd386b…` → `125e7e02…` → `9d9400da…`,
the last after the first citation), so the parent must re-derive the settled bytes
at the records commit rather than quoting an in-window value.

**Peer outputs used, and their status at my close.** The chain verifier's census
instrument and its 26/6/2/18 count (landed); the reviewer's independent re-apply
matrix and its two structural findings (landed); the C3 scribe's ledger and
records drafts (landed, values re-derived by me before folding in); C1's records
drafts (landed, entry still patch text). `seats/` held 32 of 48 reports at my
close — the C2 planner and several C2 executors had not landed when I wrote, so
the drafts' C2 bullet is drafted from the instruments that did land and does not
wait on them.
