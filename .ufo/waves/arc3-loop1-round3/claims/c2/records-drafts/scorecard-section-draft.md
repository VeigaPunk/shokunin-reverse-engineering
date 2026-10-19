# SCORECARD.md round-section draft — C2 records (SC-4, arc3-loop1-round3)

Seat SC-4 · chain c2 · role scribe · 2026-10-19. **Draft for the PARENT;
SCORECARD.md was not touched by this seat.** Append at EOF (after the
`arc3-loop1-round2` section; HEAD at draft time `c07af80`, file 1496 lines).
`⟨…⟩`/`⟨FILL⟩` = parent-fill slots; the **C2 bullet, the C2 verdict row, the C2
learning sentence and the C2 carried-debt clause are drafted complete where
evidence already exists** (the before-state was independently reproduced by this
seat, §2); values only the implementing seat can produce are marked
`⟨FILL: …⟩` with the producing seat named. The C1/C3 slots are left to the
parent per the frozen plan.

**Pin-free discipline (measured, load-bearing).** The census instrument
(`.ufo/gates/c1-census-v10.py`) declares a fixed scope table over
`PROVINCE.md`, `SKILL.md` and `SCORECARD.md`; the last declared SCORECARD row
ends well before the current EOF, and a locus past that bound reads UNDECLARED →
FAIL. A locus exists only where a `REA_GATE` line also carries an `@`-pin, a
bare `6.x.y` literal, or an absolute `path.json|toml|yaml:NNN` pointer. The C2
text below therefore carries **no version literal, no `@`-pin, no `path:line`
pointer, and no client config filename** — it refers to "the five custody paths
(three client configs + two shell profiles)". §3 records the simulation that
measures this (PASS with zero added loci, plus a planted-pin control that FAILs).

## Literal section text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL SECTION TEXT -->
## arc3-loop1-round3 — coverage + operability + freshness: ⟨PARENT-FILL: verdict phrase per the cross seat's outline⟩, 2026-10-19

Round 3 of the arc (3/10), on the token-plan lane (key 1 of 3 — the operator's
deepseek-v4.1-flash swarm directive recorded in the round-2 records; the lane
rotation is an operator steer, not a lane choice). All three owned proxies stay
saturated at 10.0; coverage is the owned axis (three-way tie,
most-falsifiable-next-claim tie-break per the luna-round-2 precedent);
operability and freshness ride the standing fleet-axis recording ruling. Roster
frozen PRE-DISPATCH (64 = 64, the r9 assertion held before dispatch).

- Wave: ⟨PARENT-FILL: reports path, wave-artifacts / work / records commits,
  delivery ⟨N⟩/64 per the roster reconciliation⟩.
- C1 coverage (owned) — ⟨FILL from the C1 records draft: the optimizer-enabled
  and non-ERC-20-shaped carriers compiled on-host with the reused receipted
  compiler prefix, planted selectors recovered K/K by the probe, the new
  knowledge entry + map token, command A 82 → 83 with the prior 82
  byte-identical⟩.
- C2 operability (fleet) — custody-pair hardening: the r2 verdict's named debt
  D2 (unreadable-path fail-open + `--live` traceback), D3 (reference-coverage
  gap), the write-guard scope finding, and D6 (selftest scratch traceback).
  **Before-state independently reproduced by this seat at HEAD `c07af80`** on a
  scratch copy of the committed instrument (889 lines at its r2 identity
  `112d01dc…`; `/var/tmp/sc4-r3/before-injections.out`, captured-utc
  2026-10-19T13:07Z, scratch fixtures only — no custody path touched):
  a capture over an exists-but-EACCES file died with a raw `PermissionError`
  traceback (exit 1, outside the declared map — the file is opened for hashing
  outside its stat guard); a path inside an EACCES directory recorded
  `EXISTS: no` + `STAT-ERROR` and that receipt then read `MATCH … exit 0`
  against itself and against the live tree (`compared=0/11`, `SHA256-CONTRACT:
  0/0`) — the fail-open shape; `verify --live` over a candidate that had become
  unreadable tracebacked identically; a reference carrying 1 of the canonical 5
  custody paths verified clean (`MATCH paths=1/1 drift=0 exit=0`) with the other
  four unexamined; the canonical-5 write guard held (`USAGE: refusing to write a
  receipt over a custody path`, exit 2) while the override form
  `--paths X --out X` **clobbered the measured file** (X replaced by the receipt
  text — guard scope = the canonical paths only); `selftest --scratch <missing
  parent>` died with `FileNotFoundError`, exit 1. **After: re-run by this seat
  against the latest observed worktree revision** (the target churned through
  19 distinct repo-path identities — the r2 landed base `112d01dc…` plus 18
  in-window revisions — measured as the union of five watcher logs, the list in
  `SC-4/evidence/churn-union3.txt`; the gate README moved through 6 revisions
  beyond its landed base. The observation below is pinned to the revision stable
  from 13:13:34Z —
  `7cd19c3c…`, 1155 lines, README `f30df42e…`, 185 lines — and the parent
  re-derives the landed identity per rule #14 rather than trusting this
  observation): a capture over the EACCES file now writes the receipt and
  exits 14 `UNEVALUABLE` (the stanza carries `READ-ERROR: …`, no digest); the
  both-sides-unevaluable `verify` reads `UNEVALUABLE` exit 14 in both modes — the
  fail-open `MATCH` is gone; the EACCES-directory path and the `--live`
  unreadable-candidate case read `UNEVALUABLE` exit 14 (no traceback anywhere);
  the 1-of-5 reference still reads `MATCH` by design, while the declared gate
  `--require-paths 5` refuses it `exit 2`; the write guard now refuses the
  canonical aim, the `--paths X --out X` self-aim (X left byte-intact) **and** a
  hardlink alias of a guarded path, all exit 2; `selftest --scratch <missing
  parent>` reads the declared `exit 2` usage class with a named message. Selftest
  15 → **22** cases, `CLEAN cases=22 passed=22 failed=0 exit=0` (the new cases
  cover unreadable and stat-blocked paths, `unevaluable-never-matches` in both
  receipt-vs-receipt and parsed-reference forms, the require-paths coverage gate,
  the scoped and hardlink write-guard arms, and the unusable-scratch usage
  exit). ⟨PARENT: re-derive the landed identities at the records/work commit
  (rule #14) and confirm the registry row landed in the SAME commit; measured
  at draft close (13:26Z): tool `7cd19c3c…` (1155 L) and README `f30df42e…`
  (185 L) present in the worktree; `SKILL.md` still at its base identity
  `c134afcb…` (390 L; zero `UNEVALUABLE` / `require-paths` hits), so the
  registry-row patch (`claims/c2/EX-30/registry-row.patch.md`; implementer form
  `claims/c2/EX-21/proposed-skill-registry-row.patch.md`) is apply-ready and NOT
  yet applied — the same-commit coupling is open at draft close⟩. The
  round's own live pre/post pair was captured by the committed tool: pre-pair
  `claims/c2/receipts/config-pre-pair-v2r3.txt`, sha256 `d31ece6f…` = its
  sidecar, captured-utc 2026-10-19T13:06:57Z before any other round-3 live work,
  5/5 present exit 0, verifying MATCH 5/5 against the live tree with the revised
  instrument and with a non-vacuous control (a mutated copy reads
  `CONTENT-DRIFT` on exactly the mutated path, exit 10); post-pair
  `claims/c2/receipts/config-post-pair-v2r3.txt`, sha256 `4969133b…` = its
  sidecar (both re-derived by this seat; `sha256sum -c` OK), captured-utc
  2026-10-19T13:17:23Z by the revised tool — its own header self-pins
  `7cd19c3c…` — 5/5 present exit 0, verifying MATCH 5/5 against the live tree
  and against the round-start pre-pair, with and without the coverage gate
  (`claims/c2/EX-29/verify-post-vs-live.out`, `verify-post-vs-live-require5.out`,
  `verify-roundstart-vs-post.out`, `verify-pre-vs-post.out`). Every receipt
  self-pins the instrument's sha256 — header re-derived from the post-pair
  receipt's own bytes: `# tool: custody-pair.py  sha256
  7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, equal to
  an independent `sha256sum` of the tool re-run at 13:23:40Z. v1 receipts
  remain
  sha256-verifiable: the round-1 sums-shape receipt re-read by the revised
  instrument gives `SHA256-CONTRACT: 4/5` with `MATCH-V1-PARTIAL` on the four
  unmoved paths and `CONTENT-DRIFT` on one, exit 10 — the one drift is the
  operator-side content churn recorded below, not a tool failure; the
  time-carrying v1 stanza and pipe shapes read `METADATA-DRIFT` on the four
  unmoved paths (their stored times no longer match), the same 4/5 contract,
  exit 10. **In-window custody drift, recorded not repaired:** the round-2
  pre-pair
  receipt and this round's pre-pair receipt agree 4/5 on sha256 — the third
  custody path (a client config) moved between rounds
  (`CONTENT-DRIFT … exit 10`), the operator-side interactive-session churn class
  documented since arc2. The five custody paths stayed READ-ONLY for every seat
  (capture/verify only; the clobber demonstration ran against a scratch write
  target). No corpus/knowledge edit in this claim; no scope-bound widening.
- Measured at the records commit: ⟨PARENT-FILL per the cross seat's outline —
  command A; probe selftest + findings; census PASS; custody post-pair 5/5⟩.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage (owned) — C1 | ⟨PARENT-FILL from the C1 records draft⟩ | ⟨PARENT-FILL⟩ |
| operability (fleet) — C2 | the committed instrument's four named holes — an EACCES path reading absent and verifying `MATCH` (fail-open) plus a raw traceback on unreadable capture/live-verify; reference coverage unaccounted (1-of-5 reads clean); a write-guard scoped to the canonical paths only (`--paths X --out X` clobbered X); a selftest scratch traceback — → each closed at the settled revision: `UNEVALUABLE` exit 14 on all three unevaluable shapes (no fail-open `MATCH`, no traceback), the declared `--require-paths` coverage gate (exit 2 on a 1-of-5 reference), the write guard refusing the canonical aim, the self-aim and a hardlink alias (all exit 2, X left intact), `selftest --scratch` misuse exit 2; selftest 15 → 22 cases CLEAN; registry row + README re-landed in the same commit; the round's live pre/post pair captured and verifying MATCH 5/5 | improved |
| freshness (fleet) — C3 | ⟨PARENT-FILL from the C3 records draft⟩ | ⟨PARENT-FILL⟩ |
| calibration | ⟨PARENT-FILL: unchanged, with the measurement recipe at the records commit⟩ | unchanged |

Learning trends: ⟨PARENT-FILL C1/C3 sentences; C2's:⟩ the round closed four
named holes in the round-2 instrument by first re-measuring each one at HEAD on
a scratch copy and then re-running the same injections against the revised tool
— the fix verified by the attack that motivated it, with the before/after pair
kept as one artifact set rather than a prose claim.
Planned: ⟨PARENT-FILL⟩. Carried debt (named): ⟨PARENT-FILL C1/C3 merges⟩; C2
keeps named: D1 (capture TOCTOU — misclassification, not an undetected tamper),
D4 (receipt self-authentication — the sidecar is not an anchor for a tampered
receipt), and D5 (out-of-band/root class: the tool is a tripwire for
attribution, not an integrity control against an actor sharing its trust
domain); the round closes the write-guard hardlink alias (D7) alongside the
scope finding, and the D8 revision-churn lesson is applied — the landed identity
is re-derived at the commit point rather than taken from any in-window
observation.
Retired: ⟨PARENT-FILL: none / list⟩.
<!-- END LITERAL SECTION TEXT -->

## Notes for the parent

- **Fill the `⟨FILL⟩` slots from landed artifacts, not from the frozen claim.**
  If a slot has no landed evidence, say so in the section rather than asserting
  it (an unrun check has not passed) — the C2 claim is only as strong as its
  weakest filled slot.
- The before-state block is this seat's own independent measurement and may be
  kept verbatim; if the implementing seat's (or a verifier's) before-repro
  contradicts a number here, the contradiction is the finding — quote both.
- **Keep the section pin-free after filling.** Quote receipt sha256s and epochs,
  never client config paths or version literals, and do not introduce a
  `path.toml:NNN`-shaped pointer — a single such line moves the census verdict
  (measured, §3 control). If the merged text cannot stay pin-free, the census
  scope must be re-keyed in the same commit as a DATED row — not measured here.
- The C1 and C3 bullets/rows must come from this round's C1/C3 records drafts so
  the three chains' numbers stay single-sourced; if those seats did not land,
  mark the gap rather than paraphrasing the frozen claim.

## §2. Before-state injections (SC-4, `/var/tmp/sc4-r3`) — MEASURED

Method: `bash /var/tmp/sc4-r3/before-injections.sh` against a scratch copy of
the committed instrument (`/var/tmp/sc4-r3/tool-head.py`, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, 889 lines),
transcript `/var/tmp/sc4-r3/before-injections.out`, captured-utc
2026-10-19T13:07Z. All inputs are scratch fixtures under `/var/tmp/sc4-r3`;
the one canonical-path case (write guard) aims `--out` at a custody path —
refused by the tool before any write, exit 2, nothing touched.

| # | injection | observed at HEAD (r2 instrument) | exit |
|---|---|---|---|
| D2a | capture over an exists-but-EACCES file | `PermissionError` traceback (`sha256_file`, opened outside the stat guard) | 1 |
| D2-stat | path inside an EACCES directory | receipt records `EXISTS: no` + `STAT-ERROR: [Errno 13]`; that receipt then reads `MATCH` in both modes (pass-2 run: `before-d2stat.out`, captured-utc 13:25:22Z) | 13 / 0 |
| D2b | that receipt vs itself and vs live | `MATCH paths=1 MATCH=1` / `MATCH paths=1/1 drift=0`, `compared=0/11` | 0 |
| D2c | `verify --live`, candidate unreadable after a clean capture | `PermissionError` traceback | 1 |
| D3 | reference with 1 of the canonical 5 paths, verify vs itself and vs live | `MATCH paths=1/1 drift=0` in both modes | 0 |
| WG | canonical-5 target (`--out <custody path>`) | `USAGE: refusing to write a receipt over a custody path` (guard holds) | 2 |
| WG | `--paths X --out X` on a scratch file | X replaced by the receipt body (clobber) | 0 |
| WG | hardlink alias of the measured path as `--out` (pass-2, same-dir link) | `OK … exit=0`, the measured file replaced by the receipt text (`hl-before.out`) | 0 |
| D6 | `selftest --scratch <missing parent>` | `FileNotFoundError` traceback | 1 |
| — | `selftest` (ordinary, basename-preserving copy) | `CLEAN cases=15 passed=15 failed=0` (`selftest-before.out`, 13:25:41Z) | 0 |

Two shapes were re-measured in a **pass-2** run after the drafts' first
transcript was found to lack them: the EACCES-directory shape (pass 1 never
executed it — the row above previously rested on a peer's transcript) and the
hardlink-alias arm (the pass-1 `ln -f` silently failed cross-device, so no arm
ran). Both pass-2 transcripts are in this seat's evidence dir
(`SC-4/evidence/before-d2stat.out`, `hl-before.out`; sha256s in §4).

This is a scribe-level re-measurement of the frozen claim's before-column, not
the chain's verification; the implementing seat's own before/after pair remains
the authority. Cross-corroboration: seat EX-22 recorded the same three shapes
independently earlier in the wave (its `claims/c2/EX-22/transcripts/` show the
EACCES receipt reading `MATCH … exit 0`, the EACCES-directory shape as
`EXISTS: no` + `STAT-ERROR`, and the unreadable `--live` candidate tracebacking
out of the same hashing call), and seat RV-5 kept its own pre-revision copy of
the instrument under `claims/c2/RV-5/before-112d01dc/` — three independent
before-reproductions of the same defects (the frozen rule "an unrun check has
not passed" is satisfied by all three; none of them is quoted as the other's
evidence).

### After-state re-run against the revised instrument

Method: `bash /var/tmp/sc4-r3/after-injections.sh`, transcript
`/var/tmp/sc4-r3/after-latest.out`, captured-utc 2026-10-19T13:14:06Z, against a
scratch copy of the worktree revision stable from 13:13:34Z — **`7cd19c3c…`,
1155 lines** (full run repeated on the earlier `03bd6242…`, 1109 lines, with the
same verdicts; an in-flight revision `9860149d…` was also probed). In-window
churn observed on this target (repo-path identities; union of five watcher
logs — this seat's 15 s watcher, EX-24's stable-poll, EX-29's stability-watch,
EX-33's poll and legC, EX-28's gate snapshots; list in
`SC-4/evidence/churn-union3.txt`): `112d01dc` (r2 landed) → `68e30768` →
`d164d49f` → `d5e72049` → `460a01f0` → `a8f81dcf` → `d9be407d` → `a991f976`
→ `9860149d` → `b645b90c` → `08fb6833` → `a611ede4` → `f2412aaa` → `ec2b2d48`
→ `57dffff1` → `03bd6242` → `dc841464` → `89bfebec` → `7cd19c3c` (19 distinct;
the order is the watchers' observed order, not necessarily the write order).
The gate README moved `fa484d57` (r2 landed) → `3d6f1a21` → `68458081` →
`039993ed` → `752032cf` → `83f07f83` → `f30df42e` (7 identities). Every
identity here is a timestamped **observation**;
the parent re-derives the landed pair at the commit point (rule #14 — this is
the r2 D8 lesson applied, not re-learned). The tool's own selftest was run on a
scratch copy that keeps the tool's basename, so the TZ case re-invokes the right
file — the earlier in-flight run's one selftest FAIL was a harness artifact of my
renamed copy, recorded here so it is not mistaken for a tool defect.

| # | injection | after (latest observed revision) | exit |
|---|---|---|---|
| D2a | capture over an exists-but-EACCES file | receipt written, stanza carries `READ-ERROR`, capture reports `UNEVALUABLE paths=1/1` | 14 |
| D2-stat | path inside an EACCES directory | `UNEVALUABLE paths=0/1` | 14 |
| D2b | that receipt vs itself / vs live | `UNEVALUABLE` in both modes — no fail-open `MATCH` | 14 |
| D2c | `verify --live`, candidate unreadable after a clean capture | `UNEVALUABLE`, no traceback | 14 |
| D3 | 1-of-5 reference, plain / `--require-paths 5` | `MATCH` by design / refused | 0 / 2 |
| WG | canonical-5 target | refused (`USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode)`) | 2 |
| WG | `--paths X --out X` | refused, X left byte-intact (`alpha`) | 2 |
| WG | hardlink alias of the measured path as `--out` (pass-2, same-dir link) | refused — `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode): alias.txt`, `alpha` intact (`hl-after.out`) | 2 |
| D6 | `selftest --scratch <missing parent>` | `USAGE: scratch base is not a directory: …` — declared usage class | 2 |
| — | `selftest` (ordinary, `/dev/shm`) | `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0` | 0 |
| — | receipt header self-pin | `# tool: custody-pair.py  sha256 7cd19c3c…` | — |
| — | round pre-pair receipt vs live | `MATCH paths=5/5 drift=0` | 0 |
| — | round-1 v1 sums receipt vs live | `SHA256-CONTRACT: 4/5`, `MATCH-V1-PARTIAL` ×4, `CONTENT-DRIFT` ×1 (the drifted client config) | 10 |
| — | round-2 pre-pair vs round-3 pre-pair | `SHA256-CONTRACT: 4/5`, `CONTENT-DRIFT` ×1 on the same path | 10 |
| — | post-pair vs live (with and without `--require-paths 5`) | `MATCH paths=5/5 drift=0` | 0 |
| — | round-start pre-pair vs post-pair (both directions, with and without the gate) | `MATCH paths=5/5 drift=0` | 0 |

## §3. Pin-free census simulation (SC-4, `/var/tmp/sc4-r3`) — MEASURED

Method (round-2 SC-4 precedent): copy the three scoped files at HEAD into
scratch roots (`/var/tmp/sc4-r3/sim-rev1/{base,records,control}`), append the
literal section text (re-extracted between the BEGIN/END markers) to the records
tree, and append it plus one planted pin literal to the control tree, then run
the census with `--root` per tree. Instrument identity bracketed around the
runs (identical before and after every run): `.ufo/gates/c1-census-v10.py`
sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(610 lines), so the pairings are exact.

Revision history (this section's text is re-derived after every revision —
rule #14 discipline; all revisions measured 2026-10-19 ~13:09Z):

- revision 1 — skeleton with the C2 bullet/row drafted and the C1/C3 slots
  open, section sha256
  `27301ac9a20c2e9e783e452a7c07f579970184755aa4fd8f1b340bd2b30fcf35` (84 lines)
  → base output `c8d97713…`, records output `673c2dd1…`, control output
  `50e79bee…`.
- revision 2 — after-state measured and folded into the C2 bullet/row/carried
  debt (the text below), section sha256
  `510513722436707edaad0ce1f12fde2fa8873daeced6f39ab6a5469fe303d0dd` (107
  lines) → base output `c8d97713…` (unchanged: the base tree is untouched),
  records output `066811cb…`, control output `c1b7e4d3…`. Still **zero** added
  loci (9 → 9), still PASS; the filled text adds no needle hit.
- revision 3 — after-values refreshed to the latest observed revision of the
  target (the target churned again after revision 2; the timeline in §2 now
  carries both observations), section sha256
  `9858a850fa9622e55fe709c0b32e656e73b8496506786851de46d2dd5d513892` (110
  lines) → base `c8d97713…` (unchanged), records `f3164122…`, control
  `76b23dac…`. Zero added loci again (9 → 9), PASS preserved.
- revision 4 — late-join completion (this pass): churn counts corrected to the
  watcher-union figures, the D2-stat and hardlink before/after rows re-measured
  and sourced, the post-pair slots filled from the landed receipts, and the
  registry-application state recorded (open at draft close), section sha256
  `a7071f65bb3fd6a43e35e690d15b210a764effcf63183dc03b9b079bd49b6837` (123
  lines) → base `c8d97713…` (unchanged), records `43110ec5…`, control
  `4dadd23c…`. Zero added loci again (9 → 9 in SCORECARD; PROVINCE 6, SKILL 2),
  PASS preserved; the control still flips to FAIL on one planted pin.
- revision 5 — churn union recomputed mechanically (19 repo-path tool
  identities / 7 README identities, `SC-4/evidence/churn-union3.txt`) and the
  §2 timeline extended to all 19; section sha256
  `93b221ca9c16d73db1fa5461036ee6ab6ddcefc19b6a8d50c10906951b66dd9c` (124
  lines) → base `c8d97713…` (unchanged), records `a9817f14…`, control
  `a5dd6dcb…`. Zero added loci again (9 → 9), PASS preserved; control FAILs as
  expected.
- revision 6 (late join, final) — the §4 evidence manifest and the §2/§3
  sourcing notes were added **outside** the BEGIN/END markers; the literal
  section is byte-identical to revision 5 (`93b221ca…`, 124 lines) and the
  census outputs are the revision-5 values verbatim (re-run confirmed: base
  `c8d97713…` / records `a9817f14…` / control `a5dd6dcb…`). ⟨PARENT: re-measure
  after the remaining `⟨PARENT-FILL⟩` slots are filled and again at the records
  commit — the current revision is the late-join state, not the merged state⟩.

| Tree | SCORECARD lines | loci (SCORECARD) | VERDICT | exit | output sha256 (rev 5) |
|---|---|---|---|---|---|
| sim-base (HEAD files) | 1496 | 9 | PASS 0/0/0/0 | 0 | `c8d97713…` |
| sim-records (+124-line section) | 1621 | 9 | PASS 0/0/0/0 | 0 | `a9817f14…` |
| sim-control (+1 planted `@`-pin) | 1623 | 10 | FAIL undeclared=1 | 1 | `a5dd6dcb…` |

- The drafted section adds **zero loci** (9 → 9 in SCORECARD; PROVINCE 6 and
  SKILL 2 unchanged) and does not perturb the per-file G2 floors
  (PROVINCE 17 / SCORECARD 14 / SKILL 3) — the pin-free property is measured,
  not asserted.
- The control shows the detector is live on the same appended region: one
  planted pin literal flips the run to UNDECLARED → FAIL exit 1.
- Caveat for the parent: re-run at the records commit and quote the
  then-current instrument sha; the drafted text's pin-free property does not
  depend on the instrument revision, since the appended region contains no
  locus under the current semantics. **Any `⟨FILL⟩` text added later must be
  re-measured** — the control above fails on a single planted line.

## §4. Evidence manifest (SC-4, late join) — all paths under this chain's tree

| artifact | sha256 | what it is |
|---|---|---|
| `SC-4/evidence/before-injections.out` | `27aab791…` | pass-1 before transcript (D2a/D2b/D2c/D3/WG/D6 on the r2 blob) |
| `SC-4/evidence/before-d2stat.out` | `1754cf97…` | pass-2 before: EACCES-directory shape + fail-open verify (this seat's own run) |
| `SC-4/evidence/hl-before.out` | `511d46d0…` | pass-2 before: hardlink-alias clobber (exit 0, X replaced) |
| `SC-4/evidence/selftest-before.out` | `e66f6031…` | before selftest, basename-preserving copy: 15/15 CLEAN |
| `SC-4/evidence/after-latest.out` | `e2b4bfd1…` | after transcript at `7cd19c3c…` (all after rows in §2) |
| `SC-4/evidence/hl-after.out` | `396962f6…` | pass-2 after: hardlink-alias refused, X intact |
| `SC-4/evidence/churn-union3.txt` | `b49db29d…` | the 19-identity tool union (§2 timeline) |
| `SC-4/evidence/tool-churn.log`, `polls.log`, `churn-union-raw.txt` | `af7b0188…`, `d9787883…`, `abfcd1b9…` | the watcher logs the union is derived from |

Full 64-hex digests: `SC-4/evidence/SHA256SUMS` (re-derived at write time).
Raw transcripts remain under `/var/tmp/sc4-r3/`; the copies here are byte-equal
(cp at 13:24Z).
