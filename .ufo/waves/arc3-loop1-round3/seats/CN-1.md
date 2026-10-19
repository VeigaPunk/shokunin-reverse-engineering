# SEAT CN-1 — chain cross — connector — late join (arc3-loop1-round3)

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Task as given: verify or
complete the cross-chain consistency sweep — the three chains' instrument
readings must not contradict (command A before-state, custody digests vs the 5
paths, probe/census states) — and add the provider-substitution note to the
cross-cutting record.

Writes by this seat: this report, `claims/cross/consistency.md` (the canonical
cross record — it already existed as a stale revision, see §1), and
`claims/cross/CN-1/**` (4 new receipts). Scratch `/var/tmp/cn1-latejoin` and
`/dev/shm/cn1-latejoin`; `/tmp` never written. No git mutation. Custody paths
read-only (sha256/stat); the live `verify` runs read the paths, never write.
No LOG/SCORECARD/SHONEN/corpus/SKILL/README edit — proposed record amendments
are prose inside `consistency.md` §6a, as patch text, not applied.

## 1. Work performed (evidence pointers)

**Inputs read first:** `claims-frozen.md`; both pre-existing copies of
`claims/cross/consistency.md`; `claims/cross/CN-1/**`; `seats/EX-31.md`;
`claims/cross/{wave-summary,records-outline}.md`; the four instruments.

**Disposition of the pre-existing work — VERIFIED + COMPLETED, not redone:**

- The canonical `claims/cross/consistency.md` was the **stale 13:15Z revision**
  (`e548edb4…`, 283 L). `claims/cross/CN-1/consistency.md` (`03ad481f…`, 311 L)
  was its superset: +6 §2 agreement rows, the §3f `/tmp`-policy addendum, the
  §3g "structurally forced" paragraph, the 13:15Z state snapshot. I promoted the
  superset to canonical (byte copy, `03ad481f…` → then appended §6 below).
- **Missing deliverables I completed:** `seats/CN-1.md` (this file); the
  **provider-substitution note** (§6a) — no cross-cutting artifact carried it,
  though `seats/EX-31.md:7` and `claims/c2/EX-31/census.md:168` state the same
  event locally; four late-join receipts (§6b table).
- **Existing claims I re-derived independently rather than trusting:** every row
  of §3 below. Where I could not re-derive, I say so (§7).

**New receipts** (`claims/cross/CN-1/receipts/`):

| file | what |
|---|---|
| `latejoin-rederivation.txt` | worktree state, command A at HEAD, census, probe ×3, custody selftest — one transcript |
| `latejoin-custody.txt` | 5-path sha256/stat, `verify` pre-pair `--live`, `verify` post-pair `--live`, three sidecars |
| `latejoin-collision.txt` | §3g re-run twice (C2 patches alone; C2 + C1 landing), with all artifact hashes at run time |
| `latejoin-c1-rehearsal.txt` | my own C1 landing rehearsal: literal entry extract, README patch, single-line diff, command A tree-mode + git-mode control |

**Live watchers still appending at this report's time** (inherited from the
pre-interruption CN-1 run, not restarted by me): `receipts/custody-watch.txt`
(18 checks 13:08–13:25Z, **0/5 drift on every check**) and
`receipts/tool-revision-watch.txt` (15 checks, tool stable at `7cd19c3c…` since
13:13Z).

## 2. Proposed changes (patch text paths or "none")

**none** as separate patch files. Two record-text amendments are proposed as
prose in `claims/cross/consistency.md` §6a (parent's call, not applied):

1. `claims/cross/CN-2/merged-LOG-entry.md:17-19` and
   `merged-SCORECARD-section.md:25-27` still name the wave's lane as
   `alibaba-token-plan/deepseek-v4.1-flash` with **no substitution clause** —
   they need the mid-run lane change recorded. Precedents to imitate:
   `LOG.md:1282-1288`, `SCORECARD.md:647-652` (arc2-loop1-round1).
2. The registry-row landing (§4.3) — the parent's call among the three
   reconciliation options; I state the cheapest and why.

## 3. Before → after measurement for this chain's claim

**Chain claim (cross/CN-1):** the three chains' instrument readings must not
contradict. **Before = the state as the interrupted run left it; after = the
state this seat re-derived.** No chain moved a measured value between the two
points; the only "after" deltas are my own additions.

| reading | before (interrupted run / frozen freeze) | after (this seat, 13:25Z) | verdict |
|---|---|---|---|
| command A at HEAD | 82/82, 14/14, 10.0/10.0 (`receipts/commandA-t0.txt`, 13:07Z) | `{"knowledge_files":82,"mapped":82,"missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14}` — identical | **consistent** |
| knowledge substrate | 82 files, list digest `6bcf3bad…` | 82 files, **all 82 per-file digests byte-identical**; `6bcf3bad…` re-derived | **consistent** |
| census | `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0 | identical | **consistent** |
| probe | `findings=0` both modes; selftest 13/13; table `738b3a56…` → landed `bfc42f1b…` | `reported findings=0 exit=0`; `clean findings=0 exit=0`; `cases=13 passed=13 failed=0 exit=0` | **consistent** |
| pointer table | 31 → 57 entries, quoted 4, exempt 3 → 8 | 57 (exact 17 / extracted 25 / anchor 15), quoted 4, exempt 8, no dup ids | **consistent** |
| F3 pin | expected re-pinned to `bfc42f1b…` | table sha256 == `expected.json` pin; `frozen_run` still `679af5d7…`/failed/`[citation_dead]` | **consistent** |
| custody tool | selftest 15/15 → 21/21 → 22/22 across ≥11 in-window revisions | landed `7cd19c3c…` (1155 L) selftest `CLEAN cases=22 passed=22 failed=0 exit=0` | **consistent** |
| custody 5-path | t0 capture 13:07:56Z | digests/inodes/modes/mtimes **identical**; 18 watcher checks 0/5 drift | **consistent** |
| live pair | pre-pair `112d01dc…` 13:06:57Z; post-pair `7cd19c3c…` 13:17:23Z | `verify` both `--live` → **MATCH 5/5 exit 0**; 3 sidecars OK | **consistent** |
| C1 landing projection | CN-1's earlier rehearsal: 83/83 on a scratch tree | my own rehearsal: literal entry 37 L `3b5f371e…` + rev-2 additive-only PRIMARY token → README 190→190, one line differs → tree-mode **83/83, missing [], dangling [], 14/14** | **consistent** |
| collision (§3g) | 1 finding with C2's drafted row | **1 finding**, and **still 1 with C1's landing also applied**; control 0 | **consistent — hazard live** |

**The chain's claim holds: no contradiction found in any shared reading.** The
one live hazard is not a contradiction between chains but a **pending collision
that fires on landing** (§4.3).

## 4. Attacks / refutations attempted, with verdicts

**4.1 — "The consistency sweep is stale: its numbers were captured before the
worktree edits landed."** *Attempted, partly confirmed, then repaired.*
The canonical copy was the 13:15Z revision and its §2 lacked the C3-landing,
C1-rehearsal and registry-row rows that the 13:17Z copy carries. I promoted the
superset AND re-derived every shared number at the current worktree state
rather than accepting either copy. Verdict: **stale-copy hazard was real, now
closed** — the promoted file's §6b carries the current-state re-derivation.

**4.2 — "The instrument readings I re-derive are copies of the receipts, not
independent measurements."** *Attempted, refuted.* Every number in §3 was
produced by me from the instrument itself in this session (transcript:
`latejoin-rederivation.txt`, run 13:24:33Z). Specifically: command A's recipe was
re-extracted from `SCORECARD.md:94-122` at HEAD, not taken from
`receipts/commandA-t0.txt`; the 82 knowledge digests were recomputed from
`git show`; the custody digests were recomputed with `sha256sum`/`stat`.

**4.3 — "C2's drafted registry-row rewrite breaks a C3 entry — is the finding an
artifact of stale drafts?"** *Attempted, refuted (the finding is structural).*
CN-1's receipt recorded the drafts at `8efd8a87…`/`a82d0071…`; at my run time
they are `03832723…`/`42b07ee5…` (both drafts were revised after the receipt).
**The finding is identical in both worlds** — same id
(`skill-registry-custody-pair-row`), same class (`citation_dead`), same reason
(no line matches the round-2 precedence string). I then ran it a third time with
C1's landing also applied: **still exactly 1 finding**, so C1's edit does not
mask or add to it. Control over unmodified HEAD reproduces the probe's clean
result (0), so the evaluator is calibrated. Verdict: **CONFIRMED COLLISION,
structural.** The entry is `kind: anchor`, `file: SKILL.md`, `must_match`
`precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`;
C2's row writes `… > UNEVALUABLE > …` in that position. Both texts are correct
alone; together one must move. Cheapest fix remains CN-1's option 1 (C3
re-anchors that single entry to a revision-stable form + re-pins
`expected.json`, the F3 coupling the C3 claim already grants). **The collision
has not fired yet** — SKILL.md is still `c134afcb…` with the round-2 row at
`:390` (re-derived).

**4.4 — "`6bcf3bad…` (the knowledge 'list digest') is reproducible, so the
baseline is sound."** *Attempted; the label was wrong, the value is right.*
Hashing the name list, the digest list, or `git ls-tree` output gives four
different digests. `6bcf3bad…` is the sha256 of the **concatenated content** of
the 82 sorted files — I found it by brute force over plausible serializations
and then confirmed by recomputation. Recorded in §6b.1 so nobody "repairs" a
phantom.

**4.5 — "The seat census can be quoted."** *Attempted, refuted as a stable
number.* Seats landed while I worked: 43 → 47 reports between 13:24 and 13:25Z.
Roster identity is intact (every delivered name in the frozen 64; no dupes; no
extras — checked mechanically), but the count is not an acceptance test. §6b.3
carries it with its timestamp.

**4.6 — "The provider-substitution note belongs in the chains' records."**
*Attempted, refuted.* The substitution is cross-cutting, and the two record
drafts that name the lane (CN-2's LOG/SCORECARD merge outputs) predate the
event. It belongs in the cross record with a pointer to the drafts that need
amending — that is where I put it.

**4.7 — Attack on my own citations.** I wrote three wrong citations into §6a on
first pass and caught all three before finalizing: the stale stamp in
`map-token-patch.md` is at `:4-5` (not `:8`); `PROTOCOL.md` **does not exist
in this repo** — the `SCORECARD.md:647-652` text quotes `PROTOCOL.md:14-17` from
the parent workspace, so §6a now cites it as a quoted clause, not a live path;
and the SCORECARD substitution precedent is arc2-loop1-**round1** (its section
heading at `:636`), not the round I first wrote.

## 5. Blockers

**None.** Everything in the seat line was verifiable and verified. Two
conditions are worth the parent's attention but block nothing:

- The two live watchers are still running (they append to `receipts/`); a
  reader at commit time should take their final tails, not my quoted 18/15
  check counts.
- §4.3's collision is a **pre-registered gate**, not a blocker: if C2's row
  lands unamended, the probe at the work commit will read `findings=1`.

## 6. Explicit completion/verification statement

- **COMPLETED (missing work):** `seats/CN-1.md`; the canonical cross record's
  late-join addendum (§6a provider substitution, §6b re-derivation table, §6b.1
  digest-method note, §6b.2 stale-stamp flags, §6b.3 timestamped census); four
  late-join receipts; the promotion of the superseded canonical copy.
- **VERIFIED (independently re-derived, not copied):** every row of §3 —
  command A, the 82-file substrate, census, probe (both modes + selftest), table
  shape + F3 pin, custody selftest, the 5-path capture, both live verifies and
  sidecars, the C1 landing projection, and the §3g collision.
- **NOT re-derived (stated, not claimed):** the round-2 debt taxonomy D1–D7; the
  `compare N/300` TOCTOU; the EACCES/type-swap case matrix (C2's CR-3 owns it);
  the carrier-level K/K probes (C1's EX-* own them); C3's entry-by-entry census
  (EX-43/EX-41 own it). I checked their **arithmetic consistency** against each
  other (§3), not their underlying compilations.

## 7. Identity discipline (rule #14)

Every sha256 I quote in §3 and §6a was re-derived in this session by
`sha256sum`, `git show | sha256sum`, or an explicit recomputation — none was
copied from a seat report. `claims/cross/consistency.md` was re-hashed after
its last edit (`5d157288…`, 423 L) — this seat does not claim that file's
byte-identity beyond that derivation, since the watchers and the parent may
append to sibling files.

*Written 2026-10-19T13:26Z. Scratch `/var/tmp/cn1-latejoin`,
`/dev/shm/cn1-latejoin`. No `/tmp` write, no git mutation, no custody-path
write, no LOG/SCORECARD/SHONEN/corpus/SKILL/README edit.*
