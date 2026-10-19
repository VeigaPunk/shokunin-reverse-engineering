# C1 execution plan — queue-drain rule #14, self-identity re-derivation discipline (PL-1)

Seat PL-1, chain c1, planner. Wave `arc3-loop1-round2`, 2026-10-19. Frozen claim:
`.ufo/waves/arc3-loop1-round2/claims-frozen.md:20-32` (C1 — depth).

**Status: de-risked end-to-end on scratch clones by PL-1.** Every command in §5
was run by this seat against clones of the lane repo at HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420`; raw output is the transcript
`rule-14-sim.txt` (same directory). The lane repo was never written by this seat
outside `claims/c1/PL-1/` + `seats/PL-1.md`; no git mutation ran in it; no
custody path was read beyond the plain `sha256sum` discipline.

Artifacts beside this file: `rule-14.patch.md` (the rule patch text — NOT
applied), `rule-14.diff` / `rule-14-block.txt` (the exact hunk and the exact
block bytes), `shonen-refresh.patch.md` / `shonen-refresh.diff` (the coupled
SHONEN.md:6 refresh), `rule-14-sim.txt` (measurement transcript),
`command-a-recipe.py` (the command A recipe as run).

---

## 1. Claim restated, and the before-state it must move

Claim (frozen): after the round's commit, the queue-drain craft section carries
**14 rules** (from 13), **14/14 citation-resolved** at the work commit under
command A, with the prior 13 rules byte-identical; rule #14 says an artifact that
records its own byte-identity must re-derive that identity after every revision,
that a stale self-identity voids the verification block and not the work, and
that the integrator records the fresh identity at landing.

Before-state, measured by this seat at HEAD `14b1682` (recipe A, §5.1):

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [],
 "revision": "14b1682", "rule_blocks": 13}
```

The craft section is `SKILL.md:81-241` (heading `## Queue-drain craft (rounds
5-12, distilled in round 13)`, 13 `- **` blocks, last one `A mitigation claim
carries its natural control`). `SKILL.md` at HEAD: 371 lines / 27,390 bytes /
sha256 `483b0eba…`; the 13 prior rule blocks are untouched by every move below.

---

## 2. The rule text (final draft, 23 lines)

Full text: `rule-14-block.txt`. Block identity: **1,736 bytes / 23 lines /
sha256 `51a87ef6c2fe18295db31a0b34285e937ebed4aeba0d6474b9111b32e75caa0e`**.
Condensed skeleton (as frozen, then as drafted):

> **An artifact that records its own byte-identity must re-derive that identity
> after every revision — a stale self-identity voids the verification block, not
> the work; the integrator records the fresh identity at landing.** *[measured
> arc3-round-1 instance, four identities + citations]* None of the three was a
> lie when written — that is the failure mode: a self-identity expires silently
> on the next edit. Re-derive size, line count, and sha256 from the bytes you are
> handing over, never from an earlier revision, and re-derive again after the
> last byte changes; the cost is one `wc -c -l` + `sha256sum`. On a mismatch,
> void the self-identity claim only — the artifact's evidence and findings stand
> — and record the fresh identity at landing *[records, by section key]*.
> Deleting the claim does not discharge the rule; an artifact's numbers for
> another file (carrier, patch output) re-derive the same way.

Design decisions, each defensible from the frozen claim or from a measured
artefact:

1. **The lead sentence is the frozen wording.** The bold face is exactly the
   claim's rule sentence, so a verifier can diff claim text against landed text
   without interpretation.
2. **The incident is stated as a sequence, not a single stale claim** — because
   measurement forced it (see §9 Q3): the same patch text carried 8,316 B /
   `f95c5a05…` (its own step-4 claim, superseded), the applied bytes were
   8,598 B / `d8d85949…`, an intermediate revision applied to 9,513 B / 32 lines
   / `a5119120…`, and the landed entry is 10,225 B / 33 lines / `dd986f56…`.
   Three different self-identities inside ~20 minutes.
3. **"Voids the verification block, not the work"** is the lane's standing
   disposition shape (the round-1 verdict applied it; the config-custody SOP uses
   the same "drift disposes the claim, not the config" form).
4. **The deletion clause is load-bearing**: without it, an artifact could dodge
   the rule by dropping its identity claim.
5. **Cost sentence** ("one `wc -c -l` + `sha256sum`") makes the rule executable
   without a tool; no instrument is required to comply.
6. **Scope boundary**: the rule covers numbers an artifact states about *itself*
   and (by the final clause) about a file it produces; it explicitly does not
   claim authority over another seat's artifact. This last clause is the one
   place the draft goes a half-step past the frozen wording — flagged in §9 Q6
   for the parent to strike if strict freeze-scope is preferred.
7. Style: dense-evidence form of the existing rules (bold lead, measured
   instance with hashes, then the prescription); all lines ≤ 79 chars, the
   current craft-section maximum.

---

## 3. Citations, and the rule-#11 form

| # | Cited | Kind | Form as written | Why it is stable |
|---|---|---|---|---|
| 1 | `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md:5-7` | in-repo immutable entry (header block: `source:` / `verified-at:` / `recheck:`) | bare line range — the lane's form for corpus entries, and the only form command A can count | entry is append-only: `end ≤ line count` holds under any future errata append; the range is the exact block the mid-wave revision rewrote (CR-2's `entry-version-diff.txt` shows the `-`/`+` pairs on those lines) |
| 2 | `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/proposed-fixes.patch.md` §**F2** | round-1 wave artifact | path + section key, **no line number** | artifact frozen at round-1 close (sha256 `a62067dd…`, 6,812 B, re-verified this session); the key names the finding, so it survives any reflow |
| 3 | `.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt` | round-1 measurement receipt | path (whole-file receipt) | 890 B, sha256 `d1128ec6…`; states both identities (8,316 / `f95c5a05…` claimed vs 8,598 / `d8d85949…` applied) |
| 4 | `.ufo/waves/arc3-loop1-round1/claims/c1/verdict.md` §**E7/D9** | round-1 convergence verdict | path + section key | the independent re-apply of both revisions (9,513 B / 32 lines / `a5119120…`; D9 names the stale block) |
| 5 | records: `LOG.md`'s arc3-round-1 entry; `SCORECARD.md`'s `arc3-loop1-round1` section | repo records | **section/entry key, no line numbers** | rule-#11 form: both files are mutable surfaces; the landing record names the fresh identity (`10,225 B`, `dd986f56…`) by key, and a reader re-derives it from the bytes |

Mechanical compliance checks on the draft (all run, §5.8):
`grep -cE '(config\.toml|mcp\.json|bashrc|profile|SCORECARD\.md|LOG\.md):[0-9]+'`
→ **0** bare line numbers into mutable files; `grep -cE '[0-9]+\.[0-9]+\.[0-9]+'`
→ **0** version pins (so the census's gated-token classes cannot trip on it).

Command A's citation grammar (`corpus/knowledge/<stem>.md[:start[-end]]`) means
citations 2–5 are *not counted* by command A — only #1 is. That is intended: #1
is the countable citation; #2–#5 are the evidence a human verifier follows. The
rule block resolves only because #1 is present — proven, not assumed, by the
`noc` control in §5.5 (citation removed → 13/14).

---

## 4. Insertion point and byte-stability contract

- **Anchor**: the last line of rule #13, `SKILL.md:239` —
  `kernel-OOM-killed (\`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37\`).`
  The new block is inserted immediately after it (i.e. before the craft
  section's trailing blank run and `## Config custody for live-probe rounds
  (SOP)` at `:242`). No blank line is added between rule #13 and rule #14
  (matching the rule-12→13 boundary); one blank line follows rule #14's last
  line, preserving the section's original two-line tail.
- **Byte contract** (measured, §5.6): first divergence at byte 17,215; inserted
  1,738 bytes; `old[:d] == new[:d]` and `old[d:] == new[d+delta:]` both true →
  **every byte of the base file survives unmodified**; `git diff --numstat` =
  `24 0 SKILL.md`; zero removed lines in a `-U0` diff.
- **Measurement trap for the claim**: the rule splitter attributes the section's
  trailing blank run to the *last* block, so raw block-equality reads
  **12/13** while rstrip-normalized reads **13/13**. Implementers and verifiers
  must state the claim as "pure insertion, 0 deletions, rstrip-normalized 13/13"
  — a raw block-equality assertion would falsely report a regression (§9 Q7).

---

## 5. Falsifiable before → after (the claim's acceptance test)

All commands were run by this seat; transcript `rule-14-sim.txt`. Scratch:
`/var/tmp/pl1r5` (disk-backed — `/tmp` is quota-exhausted, EDQUOT). Clones:
`repo-sim` (draft rule), `repo-atk` (control: citation out of range),
`repo-noc` (control: citation removed); base = `14b1682`.

1. **command A, before** — `13/13`, 82/82, 10.0/10.0 (JSON in §1).
2. **command A, after** — `{"citation_resolved_rules": 14, ..., "rule_blocks":
   14, "missing": [], "dangling": [], "coverage_score": 10.0, "depth_score":
   10.0}` at clone rev `173d167d…`.
3. **Non-vacuity control A (out-of-range citation `:5-99`)** — `13/14`,
   `depth_score 9.29`, rev `90885856…`. The check is live on the new block.
4. **Non-vacuity control B (citation deleted)** — `13/14`, `depth_score 9.29`,
   rev `13eed292…`. The corpus citation is load-bearing.
5. **Side effects, citation-drift probe** (frozen table + expected from the lane
   repo, `--root` = the clone, `--rev` = the clone rev): base / sim / atk / noc
   all `reported findings=0 exit=0`; `--strict` at sim `clean findings=0 exit=0`.
   The SKILL.md pointer-table entry is an anchor and the SHONEN one is
   extracted, so neither drifts on a mid-section insertion.
6. **Side effects, census** (instrument sha256 pinned at read time — see §6.4):
   base **PASS 0/0/0/0**, sim **PASS 0/0/0/0**; `SKILL.md lines=395 loci=2`,
   `current-ok loci per file … SKILL.md=3` on both sides — the insertion changes
   no locus. The instrument at read time was
   `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` (322→ the
   worktree-modified v11-in-progress; see §6.4).
7. **SHONEN coupling** — refreshing `SHONEN.md:6` (`13/13` → `14/14`, range
   `81-243` → `81-265`) keeps command A at 14/14, the probe at `findings=0`
   (default + strict), and the pointer-table needle (`A mitigation claim carries
   its natural control` must sit inside the stated range) hitting **1** time
   inside `SKILL.md:81-265`.
8. **Rule-#11-form scan** on the draft: 0 bare line numbers, 0 version pins;
   longest line 79 chars (craft-section maximum is 79; whole file's is 1,607 —
   the registry row).
9. **Hashes for the record**: base `SKILL.md` 371 lines / 27,390 B /
   `483b0eba…`; sim `SKILL.md` 395 lines / 29,128 B /
   `11647e6da48ccbbfd3ac557d1860d4e267997deddb989aaafc1c941209c47b14`; rule-14
   block 1,736 B / 23 lines / `51a87ef6…`.

---

## 6. Integration conditions (parent-side; what must land together)

1. **The SKILL.md hunk** — `rule-14.patch.md` (patch text; seats are barred from
   `SKILL.md` this round). Apply after the wave's last craft-section write, then
   re-derive the anchor (§4) before applying; if the craft section changed,
   re-add the block and re-run §5.2–5.4.
2. **The SHONEN.md:6 refresh in the same commit** — `shonen-refresh.patch.md`.
   Without it, `SHONEN.md:6` asserts `13/13` and `SKILL.md:81-243`, i.e. the
   landing commit would itself contain a self-referential count that went stale
   — the exact defect class rule #14 names. (The probe does not redden either
   way; this is fidelity, and the arc2 r7/r9 precedent refreshes it in-commit.)
3. **Records must stay pin-free for the census.** The new `SCORECARD.md` section
   and `LOG.md` entry must carry no undeclared `6.x.y` / `rea-agents@` token —
   round-1's connector demonstrated that such a token flips the records-commit
   census to `FAIL undeclared=1` (`.ufo/waves/arc3-loop1-round1/claims/cross/consistency.md`
   §3b). The rule text itself carries none (§5.8). Do not re-key the census scope
   to absorb a token; write the record pin-free.
4. **Census readings are version-scoped this round.** `.ufo/gates/c1-census-v10.py`
   is the C2 chain's write target this wave and was `M` (worktree-modified) during
   this session; a census read taken mid-write returned `FAIL /
   BLIND-INSTRUMENT` with `SKILL.md=0` and did **not** reproduce minutes later
   (recorded in `rule-14-sim.txt` §8 + the version-pinned re-run in §12 of the
   transcript). Every census reading in the round records must carry the
   instrument's sha256 at read time; re-run after both land.
5. **command A at the work commit** must read `14/14` (and the round's map /
   knowledge denominators, 82/82 unchanged here). The wave's RV-2 owns that
   re-measurement post-landing; the rehearsal number is not a landing proof.
6. **Do not widen the citation-drift pointer table** (the r4 laundering
   precedent). No table edit is needed: the probe is clean by measurement (§5.5).
   No re-pin of `expected.json` is needed either, since no pinned input changes.
7. **Do not edit `corpus/`**: the countable citation target already exists and
   is immutable; the incident evidence already exists in the round-1 wave tree.

---

## 7. Chain work split (c1: PL-1, EX-01…EX-06, SC-1, RV-1, RV-2, CR-1, VZ-1)

| Seat | Task | Deliverable under `claims/c1/<SEAT>/` |
|---|---|---|
| EX-01 | Finalize the rule text at the wave's HEAD: re-anchor (§4), re-apply, re-derive block bytes/lines/sha256; emit the authoritative patch text | `rule-14.patch.md`, `rule-14-block.txt` |
| EX-02 | SHONEN refresh patch: recompute the range from the landed `SKILL.md` (heading → heading+1_shift), re-run the needle check | `shonen-refresh.patch.md`, `needle-check.txt` |
| EX-03 | Re-derive the four incident identities from the durable artifacts (landed entry; CR-2's receipt; the current EX-12 patch's step 4) — raw `sha256sum`/`wc -c -l` output only | `incident-identities.txt` |
| EX-04 | command A before/after on a fresh scratch clone; record both JSONs + the clone revs | `command-a-before.txt`, `command-a-after.txt` |
| EX-05 | Byte contract + non-vacuity: prefix/suffix identity proof, `--numstat`, `-U0` deletion count, rstrip-normalized 13/13, and both negative controls (`:5-99`; citation removed) | `byte-contract.txt`, `controls.txt` |
| EX-06 | Side-effect battery: citation-drift probe (default + strict) and census at base/after, each with the instrument's sha256 + mtime at read time | `probe-runs.txt`, `census-runs.txt` |
| SC-1 | Independent replication of §5.2–5.6 in its own clone; report disagreements, not summaries | `replication.txt` |
| RV-1 | Independent re-derivation of the rule's quoted numbers vs the artifacts (does not read EX-03 first) | `identity-audit.txt` |
| RV-2 | Post-landing command A at the work commit + confirm the SHONEN refresh landed in the same commit + confirm prior-13 preservation | `after-landing.txt` |
| CR-1 | Adversarial attacks (see §9) — especially Q1 (vacuousness), Q3 (the rule's own self-identity), Q6 (scope overreach) | `attacks.md` |
| VZ-1 | Convergence verdict over the above; name gaps; state whether the claim's before→after is measured or only rehearsed | `verdict.md` |

Parallelism: EX-01 → (EX-02, EX-04/EX-05/EX-06) → SC-1/RV-1/CR-1 → VZ-1. Every
leg is sub-second; no containment needed. Nothing here requires a probe of the
REA surface, an install, or a custody write.

---

## 8. Honest-stop branches (pre-written)

- **H1 anchor missing** (the craft section changed before landing): do not
  fuzzy-insert. Re-anchor by heading (`## Queue-drain craft …` → next `## `) and
  re-run §5.2–5.4; if the section no longer ends with the natural-control rule,
  report the divergence.
- **H2 after < 14/14**: the citation is the failing component. Re-derive the
  target's line count; never widen the range into another file, never retarget
  the citation to a file that "happens to resolve".
- **H3 probe or census reddens after the insertion**: report the instrument's
  sha256 at read time, do not edit the instrument, do not widen the table. The
  hunk does not land while an instrument is red on it.
- **H4 SKILL.md unwritable** (this round's freeze holds to the end): the claim
  reports *patch text delivered, after-state rehearsed on a clone* — not landed.
  The rehearsal numbers are then the claim's ceiling.
- **H5 rival craft-section edit lands first**: re-derive the anchor and the
  block hashes; never merge rival rule texts; if two rule-#14 candidates exist,
  one text wins by code-truth (round-1's merged-registry-row precedent).

---

## 9. Adversarial questions (with this seat's attempts and verdicts)

- **Q1 — Is rule #14 a rule or an anecdote?** Attempt to absorb it into rule #7
  ("tool acceptance ≠ correctness") and rule #11 (citation form). **Verdict:
  separable.** #7 governs a tool's own validation; #11 governs citations into
  operator-mutable files; neither names an artifact's self-identity under
  revision. Residual: compliance is *not* machine-graded — command A counts
  blocks and citation resolvability, not discipline; enforcement rests on the
  reviewing seats checking identity claims in the artifacts they read.
- **Q2 — Is it redundant with what round 1 already did?** Round 1 recorded the
  fresh landing hash (`SCORECARD`'s `arc3-loop1-round1` section: "fresh identity
  recorded (10,225 B, sha256 `dd986f56…`)") — but that was parent improvisation
  *after* a critic (CR-2 F2) and a convergence seat (D9) caught the stale block;
  no standing rule required it, and the same wave's entry patch still carries a
  superseded identity in step 4 today. **Verdict: not redundant; the rule
  converts a caught incident into a standing check** — the depth-axis move.
- **Q3 — Does the rule text itself carry a stale self-identity?** It quotes four
  identities of one wave artifact. **Measured today**: the current
  `EX-12/knowledge-entry.patch.md` (18,701 B, sha256 `d662c195…` — the same value
  VZ-1 recorded at 07:15) still claims `9,513 B / 32 lines / a5119120…`, i.e. its
  self-claim is stale *again* against the landed bytes (`10,225 B / 33 lines /
  dd986f56…`). **Verdict: the rule's premise is confirmed by fresh measurement**;
  the quoted numbers are historical quotes anchored to the receipts (citations
  2–4), and the rule says so. Residual: if the wave tree were pruned, the quotes
  lose their anchors — the receipts are the durable evidence and are cited by
  path.
- **Q4 — Line-range robustness.** `:5-7` stays resolvable under append-only
  growth; if the entry's header were rewritten to different content with ≥7
  lines, command A still resolves while the semantic anchor drifts. **Verdict:
  accepted, named.** Mitigation: the draft names the block ("the header block the
  mid-wave revision rewrote"), so the reader re-locates it by content; and the
  lane already declares command A "resolvability, not semantic audit".
- **Q5 — Could an artifact dodge by deleting its identity claim?** Closed
  explicitly in the rule's final sentence (the integrator records the landed
  identity either way).
- **Q6 — Scope overreach.** The final clause extends the discipline to numbers
  an artifact states about a produced file. The frozen wording covers
  self-identity only. **Verdict: keep, but flagged.** The incident's step 4 *was*
  a produced-file identity; striking the clause would leave that half unnamed.
  Parent may strike for strict freeze-scope — the acceptance test is unaffected.
- **Q7 — Does "prior 13 rules byte-identical" survive literally?** Raw block
  equality is **12/13** because of the section's trailing blank run; the diff has
  **0 deleted lines** and the prefix/suffix proof shows every base byte survives.
  **Verdict: the claim must be measured as pure insertion + rstrip-normalized
  13/13** — otherwise an honest verifier will report a false regression.
- **Q8 — Instrument drift from moving 24 lines in a 371-line file?** Measured:
  probe `findings=0` (both modes) at base and after; census `PASS 0/0/0/0` both
  sides with `SKILL.md` loci/current-ok counts unchanged. **Verdict: no drift.**
  The registry row is a content anchor; the SHONEN range pointer is extracted
  (self-updating) and its needle still hits inside both the old and refreshed
  ranges.
- **Q9 — Same-commit coupling.** If the SKILL.md hunk lands without the SHONEN
  refresh, `SHONEN.md:6` keeps a stale `13/13` (a self-referential count — the
  rule's own defect class). **Verdict: refresh must be in the same commit**
  (§6.2). No other file couples: the census's C2 target is a different file, and
  the probe's pinned inputs are untouched.
- **Q10 — Is the incident evidentiary basis real, or a transcription?**
  Re-checked this session, first-hand: CR-2's receipt is byte-stable (890 B,
  `d1128ec6…`) and states both identities; VZ-1's verdict §D9 records the third
  revision; the landed entry re-hashes to 10,225 B / 33 lines / `dd986f56…`; the
  current patch text still carries the `a5119120…` claim. **Verdict: the incident
  stands on reproduced facts; nothing in the rule is asserted from memory.**

---

## 10. De-risk evidence, hygiene, and what this seat did not do

- Transcript with raw output: `rule-14-sim.txt` (command A ×4, byte contract,
  block identity, probe ×5, census with version pinning, SHONEN coupling,
  hashes, source-repo-untouched check).
- Clones (scratch, `/var/tmp/pl1r5`): `repo-sim` `173d167d…` (+ SHONEN commit
  `962aea2b…`), `repo-atk` `90885856…`, `repo-noc` `13eed292…`; base
  `14b1682b1128d2e41085ebc79c9addeb8786d420`.
- Hygiene: `/tmp` never used (quota-exhausted; all scratch disk-backed under
  `/var/tmp`); the lane repo shows the same HEAD (`14b1682`) and the same five
  pre-existing dirty entries before and after this seat's work; no git mutation
  ran in it (clones created by `git clone`, commits only inside the clones); the
  five custody paths were not opened, hashed, or touched by this seat.
- Not done (by design): no `SKILL.md`, `SHONEN.md`, `LOG.md`, `SCORECARD.md`,
  `corpus/` or gate write; no pointer-table or census edit; no installs; no REA
  probe; no attempt to convert the rehearsal into a landing claim.

---

## 11. Reconciliation with the chain's landed work (added after the wave ran ahead)

The c1 chain executed while this plan was being written: **EX-01 landed a rule
#14 patch text** (`claims/c1/EX-01/rule14.patch.md`), RV-1 graded it against a
seven-item fidelity list, CR-1 attacked the rule formation, EX-02 ran stale-twin
and parser controls, EX-04 measured the SHONEN geometry. This section replaces
"which text" as an open question: **EX-01's payload is the landing candidate;
the text in §2 of this plan is a merge candidate, not a rival.**

**Independent replication by this seat** (scratch `/var/tmp/pl1r6/repo-ex01`;
method: extract the payload strictly between EX-01's HTML markers, insert after
`SKILL.md:239`, commit in the clone):

| Quantity | EX-01's claim | PL-1's replication |
|---|---|---|
| payload | 1,071 B / sha256 `6cc388cb…` | **identical** (1,071 B / `6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f`) |
| patched `SKILL.md` | 387 lines / sha256 `a8170b96…` | **identical** (387 lines / 28,462 B / `a8170b96450f871282027b9adbc89cde08611457deb3a506cae3567701cd7e28`) |
| command A | 14 rules, 14/14, 82/82, 10.0/10.0 | **identical** |
| prior rules | prefix 1–239 byte-identical | **confirmed** (`lines[:239]` equal to base) |
| rule #14 geometry | — | first line `:240`, last line `:254`, next heading `:258` |
| probe / census | 0 findings / PASS | **0 findings** (`reported findings=0 exit=0`) / **PASS 0/0/0/0**, `SKILL.md lines=387 loci=2` |

**Divergence the chain must resolve before landing (measured, not inferred):**
EX-04 measured a *different* patched artifact for the same append — 385 lines /
sha256 `19057c13…`, rule #14 at `:240-252`, and therefore proposes SHONEN
`81-252`. EX-01's payload, re-applied by this seat, gives 387 lines and rule #14
at `:240-254`. The two differ by two lines (a trailing-blank/separator
difference). EX-04's own convention ("stated end == last rule line") is the right
one — so the SHONEN end is **254** for EX-01's payload and 252 only for EX-04's
variant. The refresh must be computed from the bytes that actually land, after
landing, not from either seat's rehearsal.

**Delta between EX-01's payload and this plan's draft, ranked:**

1. **Citation form (recommend merge).** EX-01's block cites `SCORECARD.md:1366-1368`
   and `LOG.md:1411-1412` by bare line numbers; measured here: 2 bare refs into
   mutable repo records, no operator-mutable path, no version token. No
   instrument grades them (probe 0 findings either way), so this is fidelity, not
   gate-passing — but rule #11's own discipline prefers the section/entry key
   (`SCORECARD.md`'s `arc3-loop1-round1` section; `LOG.md`'s arc3-round-1 entry)
   exactly because those records' line numbers are the kind that drift.
2. **Laundering closure (recommend merge).** EX-01's text does not close the
   "delete the identity claim" dodge; one clause does it ("Deleting the claim
   does not discharge the rule"), which is also the only mechanical-anchor a
   reviewer has for CR-1's "norm with no instrument" objection.
3. **Cross-file clause (do not merge).** This plan's final clause ("an
   artifact's numbers for another file re-derive the same way") is already
   covered by EX-01's "claim binds the bytes it describes" — merging it would
   duplicate, and it was flagged as a freeze-scope stretch (§9 Q6). Drop it.
4. **Cost/executability sentence (optional merge).** "the cost is one
   `wc -c -l` + `sha256sum`" makes the rule executable without a toolchain.
5. Kept from EX-01 regardless: the re-establishment clause ("the voided block is
   re-established by re-running its checks against the current bytes") and
   "never a revert, never a carried-over number" — both satisfy RV-1's fidelity
   items 3 and the measured disposition; this plan's draft lacked them.

**Consequences if the merge is taken:** the payload grows by ~2–3 lines; the
patched `SKILL.md` identity, the rule's line span and the SHONEN end must be
re-derived after the merged text is frozen (EX-01's `87`-line numbers and EX-04's
`252` become history). The acceptance test is unchanged: command A 14/14,
pure-insertion with prior 13 rules rstrip-identical, probe 0 findings, census
PASS with loci unchanged.

**Merged variant, built and measured (not left as a recommendation):**
`claims/c1/PL-1/merged-rule-14.patch.md` (+ `merged-rule-14-block.txt`) — EX-01's
payload with exactly deltas 1 and 2 applied. Measured on a scratch clone:
patched `SKILL.md` 392 lines / 28,711 B / sha256 `0cf18464…`; command A 14/14,
82/82; rule #14 at `:240-259`, next heading `:263` → **SHONEN end 259**; probe
`findings=0`; census `PASS 0/0/0/0`, `SKILL.md lines=392 loci=2` (instrument sha
`d0772ce892223690…` at read time); block 1,319 B / 20 lines / sha256 `5a235f18…`;
0 needle tokens. The variant is this seat's, not the chain's: EX-01's text stays
the landing candidate unless the chain accepts the deltas.

**Instrument-state note (this session):** `.ufo/gates/c1-census-v10.py` moved
again between readings (`df9ffdf9…` → `a4c16763…`), confirming §6.4 — every
census reading in the round's records must carry the instrument's sha256 at read
time.
