# merged records text — arc3-loop1-round3 (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2 from the chains' literal drafts (C1 = SC-2
`records-drafts.md`; C2 = SC-4; C3 = SC-5 — all spliced verbatim,
placeholder-normalized; sources + shas in the outline's merge-delta table).
**Pasteable text only** — nothing here is applied; the parent lands R1/R2.
The section is PIN-FREE by construction and measured (outline §6.4); identity
of this file: receipts/identity.txt (rule #14 — not inlined).

## Literal SCORECARD section (append at EOF after the round-2 section)

<!-- BEGIN LITERAL SECTION TEXT -->
## arc3-loop1-round3 — coverage + operability + freshness: [[FILL: verdict phrase per the parent's admission]], 2026-10-19

Round 3 of arc 3 (loop 1; 3/10). Axis set: **coverage (owned)**,
operability (fleet), freshness (fleet); all three owned proxies stay tied at
10.0 with none retired, so the owned claim is selected by the standing
most-falsifiable-next-claim tie-break. The claims are causally separable — the
corpus knowledge surface, the custody tool and the probe's pointer table share
no edit target. Roster frozen PRE-DISPATCH (mechanically enumerated, 24+24+12+4
= 64, every name exactly once; the items-array assertion held at dispatch);
the wave rides the token-plan lane per the operator's deepseek-v4.1-flash swarm
directive (recorded in the round-2 records).

- Wave: 64 seats; `alibaba-token-plan/deepseek-v4.1-flash` (token-plan key 1 of
  3); reports `.ufo/waves/arc3-loop1-round3/`; round report
  `.ufo/reports/arc3-loop1-round3/kaidoku.md`. Delivered [[FILL: N/64 per the
  roster reconciliation (VZ-4), never the declared count]]. Landed at [[FILL:
  work / wave-artifacts / records commits]].
- C1 coverage (owned) — EVM optimizer-enabled dispatch shapes, the r1 entry's
  named Unknown: four carrier families compiled on-host with the REUSED
  receipted solc prefix (no install; receipt re-verified) and probed across
  the two REA pins and both encodings — an optimizer-enabled library-bound
  vault carrier (K=13; runtime 1,621 B optimized vs 3,163 B not), an
  optimizer-enabled multisig carrier (K=11; 1,850 vs 3,872 B; first pure leg —
  the state-mutability inference reads view for a pure function, i.e. it
  separates mutating from non-mutating only), an optimizer-enabled
  mixed-mutability carrier (K=8) plus a purpose-built falsification twin with
  planted custom-error constants (K=8, zero extras), and r1's own token
  recompiled optimizer-on (K=5; 1,943 → 978 B). Every runtime leg K/K, zero
  missing / zero extra, offsets on JUMPDESTs; same-source optimizer-off
  controls recover the same sets; r1's canonical recheck re-derived its
  sealed id (and the new primary its own) first-hand. Landed as
  `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` + the
  line-neutral map token (same physical line, 190 → 190) [[FILL: names/hashes
  at landing]]. Measured before → after: command A knowledge files 82/82 →
  83/83, missing [], dangling [], rules 14/14 ([[FILL: parent re-quote at the
  work/records commit]]; the wave's scratch rehearsal reads 83/83 with the
  prior 82 byte-identical).
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
  exit). [[FILL: re-derive the landed identities at the records/work commit
  (rule #14) and confirm the registry row landed in the SAME commit; measured
  at draft close (13:26Z): tool `7cd19c3c…` (1155 L) and README `f30df42e…`
  (185 L) present in the worktree; `SKILL.md` still at its base identity
  `c134afcb…` (390 L; zero `UNEVALUABLE` / `require-paths` hits), so the
  registry-row patch (`claims/c2/EX-30/registry-row.patch.md`; implementer form
  `claims/c2/EX-21/proposed-skill-registry-row.patch.md`) is apply-ready and NOT
  yet applied — the same-commit coupling is open at draft close]]. The
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
- C3 freshness (fleet) — the citation-drift pointer table extends to the
  arc3-era citations. Wave-start baseline (independent scribe re-measurement
  at the pre-round commit, byte-identical to the chain's own before-receipt):
  the table carried 31 entries (plus 4 quoted records and 3 exemptions), its
  digest pinned in the expected-values file; probe findings 0 in both modes;
  selftest 13/13. The named debt (round-1 C2 note; the round-10 extension
  precedent): the table did not cover the round-1 EVM entry and its map row,
  the arc3 scorecard section keys, the round-2 registry rows, or the custody
  receipt conventions. Landed at the work tree (EX-41; re-measured by this
  scribe): entries 31 → 57 (+26 added, none removed), quoted unchanged (4),
  exemptions 3 → 8 — the NO-ENTRY causes materialized (append-only round
  reports; wave-internal provenance as a class; the five operator paths, which
  rule #11 forbids pinning; current-state count tokens; LOG prose) — with every
  pinnable arc3 citation table-covered or NO-ENTRY with cause per the round-4
  precedent. The digest is re-pinned in the expected-values file in the same
  commit (the F3 coupling): measured, its only change is the pinned table
  digest, from `738b3a56…` to `bfc42f1b…`; the frozen-run revision, verdict and
  expected finding, the snapshot digest and the 13-case selftest table are
  byte-unchanged, and the frozen-run baseline was re-derived at its pinned
  revision (failed, the expected finding present — EX-41's dispositions file
  records the run). Post-landing: probe findings 0 in both modes at the work
  tree; selftest 13/13 unchanged; an independent digest re-derivation reads
  MATCH; the declared preflight classes re-verified on a byte-changed table, an
  absent table, an unpinned baseline and a dead revision (each could-not-
  evaluate exit 2); command A unchanged (82/82, 14/14, 10.0/10.0, measured
  against the pre-round commit archive). Verifier confirmations [[FILL: RV-11/RV-12/CR-5/VZ-3 receipt paths and verdicts — not all landed at this
  draft's last poll]]. Attacks recorded with verdicts: the extension has teeth
  where the old table was blind — at the same real drift revision the 31-entry
  table reads clean while the extension reports 2 dead citations (executor's
  drift-injection pair); a per-entry needle and pointer mutation battery
  reddens every new entry (non-vacuity); a neutered needle and a one-word flip
  each report `citation_dead` rather than repairing; a stale pin and a
  one-byte tamper each exit 2. The probe remains advisory by kind: drift is
  reported, never failed; `--strict` restores the gate map.
- Measured at the records commit: [[FILL: command A at the settled tree;
  probe selftest + findings both modes; census PASS 0/0/0/0; custody post-pair
  MATCH 5/5]]. The connector's own pre-landing measurements: the records text
  appended to scratch copies of the scoped files reads census PASS 0/0/0/0 with
  an injected-pin control FAILing (`undeclared=1`), the PIN-FREE checker reads
  CLEAN on both literal bodies, and the C2 registry-row patch text projected
  in place (with the section appended) also reads PASS.

| Axis | Before → after | Verdict |
|---|---|---|
| coverage (owned) — C1 | knowledge 82/82 → 83/83 (four optimizer-enabled / non-ERC-20 carrier families recovered K/K; zero false positives incl. a falsification carrier; optimizer-off controls agree; r1 canonical id re-derived; proxy held at the larger denominator) | improved [[FILL: parent confirm]] |
| operability (fleet) — C2 | the committed instrument's four named holes — an EACCES path reading absent and verifying `MATCH` (fail-open) plus a raw traceback on unreadable capture/live-verify; reference coverage unaccounted (1-of-5 reads clean); a write-guard scoped to the canonical paths only (`--paths X --out X` clobbered X); a selftest scratch traceback — → each closed at the settled revision: `UNEVALUABLE` exit 14 on all three unevaluable shapes (no fail-open `MATCH`, no traceback), the declared `--require-paths` coverage gate (exit 2 on a 1-of-5 reference), the write guard refusing the canonical aim, the self-aim and a hardlink alias (all exit 2, X left intact), `selftest --scratch` misuse exit 2; selftest 15 → 22 cases CLEAN; registry row + README re-landed in the same commit; the round's live pre/post pair captured and verifying MATCH 5/5 | improved |
| freshness (fleet) — C3 | 31 entries, no arc3-era coverage → [[FILL: N]] entries with every pinnable arc3 citation table-covered or adjudicated NO-ENTRY; digest re-pinned in the expected-values file in the same commit; findings 0 in both modes at the work commit; selftest 13/13 unchanged | improved |
| depth | [[FILL: unchanged, with the measurement recipe at the records commit]] | unchanged |
| calibration | [[FILL: unchanged, with the measurement recipe at the records commit]] | unchanged |

Learning trends: coverage — the r1 Unknown narrows by measurement, with
same-source optimizer-on/off controls agreeing on the recovered sets while the
runtime bytes shrink (1,943 → 978 B and 3,163 → 1,621 B and 3,872 → 1,850 B),
and zero false positives re-confirmed at the byte level including a
purpose-built falsification carrier; the family's id is measured
path-sensitive (no formula claimed). the round closed four
named holes in the round-2 instrument by first re-measuring each one at HEAD on
a scratch copy and then re-running the same injections against the revised tool
— the fix verified by the attack that motivated it, with the before/after pair
kept as one artifact set rather than a prose claim.
the table extension was
coupled to its own integrity pin in one commit — the probe's frozen-run guard
(a round-1 landing) forces new table bytes and the expected-values digest to
move together, so the extension cannot land half-pinned; and the acceptance
test is the arc3-citation census with its adjudications, not the entry count.
Planned: [[FILL: round 4 per schedule; token-plan key 2 of 3]].
Carried debt (named): the stale province EVM frontier bullet (doubly stale
across two real-compiler rounds — candidate one-line refresh, protected file,
not landed); optimizer runs values other than 200 / the `viaIR` pipeline /
vyper (Unknowns); the sealed-id domain measured only as path-sensitive. C2
keeps named: D1 (capture TOCTOU — misclassification, not an undetected
tamper), D4 (receipt self-authentication — the sidecar is not an anchor for a
tampered receipt), D5 (out-of-band/root class: the tool is a tripwire for
attribution, not an integrity control against an actor sharing its trust
domain), and D7 (write-guard hardlink evasion — named as precision, not
severity). C3 adds [[FILL: the adjudicated NO-ENTRY items that stay named debt,
with causes]]. Standing: the host `/tmp` quota exhaustion (the EVM rechecks
fail EDQUOT under a `/tmp`-defaulted run — a disk-backed scratch is a recipe
requirement, not advice); the pre-existing dirty
`.ufo/waves/arc2-loop1-round10/C3.md` (not this round's). Retired: [[FILL: none
/ list]].
<!-- END LITERAL SECTION TEXT -->
