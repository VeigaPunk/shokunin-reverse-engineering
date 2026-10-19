### arc3-loop1-round3 — coverage: EVM optimizer-enabled dispatch shapes + operability: custody-pair hardening + freshness: citation-drift table extension (2026-10-19)

- Dispatch: 64 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  24+24+12+4, every name exactly once; the items-array assertion held at
  dispatch, the counting lesson's wire-it gate); `alibaba-token-plan/
  deepseek-v4.1-flash` (token-plan key 1 of 3 — operator directive: the
  deepseek-v4.1-flash swarm waves ride the token-plan lanes). Delivered
  [[FILL: N]]/64 per the roster reconciliation (count the items array, never
  the intent).
- C1 coverage (owned) — EVM family extension, the r1 entry's named Unknown
  ("optimizer-enabled dispatch shapes beyond the smoke compile"): the wave-1
  receipted solc prefix was REUSED (no install; receipt re-verified —
  tarball sha256 `0e1a1ab6…575a51`, `soljson.js` `221d7a66…abad4c` re-hashed
  this round) and four carrier families were compiled on-host with the pinned
  solc and probed with `inspect-evm-interface`, each with a same-source
  optimizer-off control where feasible: an optimizer-enabled library-bound
  `VaultB` (K=13; runtime 1,621 B optimized vs 3,163 B off), an
  optimizer-enabled multisig carrier (K=11; 1,850 vs 3,872 B; the first pure
  leg in this family — the probe's state-mutability inference separates
  mutating from non-mutating, not pure from view), an optimizer-enabled
  mixed-mutability `CarrierB` (K=8) plus its falsification twin with planted
  custom-error constants (K=8, zero false positives — byte-level census), and
  the r1 token recompiled optimizer-on (K=5; 1,943 → 978 B). Every runtime
  leg recovered its planted set K/K with zero missing / zero extra,
  `dispatch:"abi"`, offsets landing on JUMPDESTs; the raw-on-hex-text trap
  reproduces as parsed-and-empty (not an error); cross-pin legs (both pins) ×
  both encodings agree; r1's canonical recheck re-derived its sealed
  `ev_45849c8b…` and the new opt200 primary re-derived `ev_d409bd50…` (both
  re-run first-hand by the scribe seat, envelopes byte-identical to the
  seats' captures). The `ev_` id measured path-sensitive for this verb family
  (three-way same-bytes/different-path; no formula claimed). Result lands as
  `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` (RESULT-class,
  family-scoped, no availability→holding) + the coverage-map token
  line-neutral (`corpus/README.md:38`, 190 → 190, one line differs); command A
  82/82 → 83/83, prior 82 byte-identical, rules 14/14 (the wave rehearsed the
  pair on a scratch tree: 83/83, missing [], dangling [])
  [[FILL: parent re-measure at the records commit]].
- C2 operability — custody-pair hardening (the r2 verdict's named debt: D2
  EACCES fail-open + `--live` traceback, D3 partial-reference verify, the
  write-guard scope finding VZ-4, D6 selftest scratch traceback). **Before-state
  independently reproduced at HEAD `c07af80` by this scribe on a scratch copy of
  the committed instrument** (889 lines, r2 identity `112d01dc…`;
  `/var/tmp/sc4-r3/before-injections.out`, captured-utc 2026-10-19T13:07Z; no
  custody path touched — captures ran over scratch fixtures only):
  (i) a capture over an exists-but-EACCES file died with a raw `PermissionError`
  traceback, exit 1, outside the declared class table (the file is opened for
  hashing outside its stat guard);
  (ii) a path inside an EACCES directory recorded `EXISTS: no` + `STAT-ERROR:
  [Errno 13] Permission denied` — and that receipt then read `MATCH … exit 0`
  against both itself and the live tree (`compared=0/11`, `SHA256-CONTRACT:
  0/0`): the fail-open shape, reproduced;
  (iii) `verify --live` over a candidate that had become unreadable (file
  chmod 000 after a clean capture) tracebacked with the same `PermissionError`,
  exit 1;
  (iv) a reference carrying 1 of the canonical 5 custody paths verified clean —
  `MATCH paths=1/1 drift=0 exit=0` — in both receipt-vs-receipt and `--live`
  modes: reference coverage is unaccounted for;
  (v) the canonical-5 write guard held (`capture --out <a custody path>` →
  `USAGE: refusing to write a receipt over a custody path`, exit 2) while the
  override form `--paths X --out X` **clobbered the measured file** — X was
  replaced by the receipt text (guard scope = the 5 canonical paths only);
  (vi) `selftest --scratch <missing parent>` died with `FileNotFoundError`,
  exit 1, outside the declared map.
  After: re-run by this scribe against the latest observed worktree revision (the
  target churned through 19 distinct repo-path identities — the r2 landed base
  plus 18 in-window revisions, the union of five watcher logs; list in this
  chain's `SC-4/evidence/churn-union3.txt` — and the gate README through 6;
  the observation is pinned to the revision stable from 13:13:34Z — `7cd19c3c…`,
  1155 lines, README `f30df42e…`; the parent re-derives the landed identity per
  rule #14):
  the EACCES-file capture now writes the receipt with a `READ-ERROR` stanza and
  reports `UNEVALUABLE paths=1/1 exit=14`; the EACCES-directory shape reads
  `UNEVALUABLE paths=0/1 exit=14`; the both-sides-unevaluable `verify` and the
  unreadable-candidate `--live` run both read `UNEVALUABLE exit=14` — the
  fail-open `MATCH` and the tracebacks are gone; the 1-of-5 reference still
  reads `MATCH` by design, while the new declared gate `--require-paths 5`
  refuses it at `exit 2`; the write guard now refuses the canonical aim, the
  `--paths X --out X` self-aim (X left intact) and a hardlink alias of a guarded
  path, all `exit 2`; `selftest --scratch <missing parent>` reads the declared
  usage class `exit 2`. Selftest 15 → **22** cases:
  `CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0` (the new
  cases cover unreadable and stat-blocked paths, `unevaluable-never-matches` in
  both receipt-vs-receipt and parsed-reference forms, the require-paths coverage
  gate, the scoped and hardlink write-guard arms, and the unusable-scratch usage
  exit), run
  by this scribe on a scratch copy that keeps the tool's basename (an earlier
  in-flight run showed one selftest FAIL — a harness artifact of a renamed copy,
  not a tool defect; recorded so it is not miscounted). [[FILL: re-derive the
  landed identities at the records/work commit (rule #14) and confirm the
  registry row landed in the SAME commit; measured at draft close (13:26Z):
  tool `7cd19c3c…` (1155 L) and README `f30df42e…` (185 L) present in the
  worktree; `SKILL.md` still at its base identity `c134afcb…` (390 L, zero
  `UNEVALUABLE` / `require-paths` hits), so the registry row (patch text in this
  chain's tree: `claims/c2/EX-30/registry-row.patch.md` + `readme.patch.md`;
  implementer form `claims/c2/EX-21/proposed-skill-registry-row.patch.md`) is
  apply-ready and NOT yet applied — the same-commit coupling is open at draft
  close]]. The round's own
  live pre/post pair: pre-pair captured before any other round-3 live work by
  another seat — `claims/c2/receipts/config-pre-pair-v2r3.txt`, sha256
  `d31ece6f…` = its sidecar, captured-utc 2026-10-19T13:06:57Z, 5/5 present
  exit 0, and it verifies MATCH 5/5 against the live tree
  (`claims/c2/EX-29/verify-pre-roundstart-vs-live.out`, re-run by this scribe
  against the revised instrument with the same verdict), with a non-vacuous
  control (a mutated copy of that receipt reads `CONTENT-DRIFT` on exactly the
  mutated path, exit 10); post-pair
  `claims/c2/receipts/config-post-pair-v2r3.txt`, sha256 `4969133b…` = its
  sidecar (both re-derived by this scribe; `sha256sum -c` OK), captured-utc
  2026-10-19T13:17:23Z by the revised tool (its own header self-pins
  `7cd19c3c…`), 5/5 present exit 0, verifying MATCH 5/5 against the live tree,
  against the round-start pre-pair and against the revised pre-pair, with and
  without `--require-paths 5`
  (`claims/c2/EX-29/verify-post-vs-live.out`, `verify-post-vs-live-require5.out`,
  `verify-roundstart-vs-post.out`, `verify-pre-vs-post.out`). Every
  receipt self-pins the instrument's sha256 — header re-derived from the
  post-pair receipt's own bytes: `# tool: custody-pair.py  sha256
  7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, equal to
  an independent `sha256sum` of the tool re-run at 13:23:40Z. v1 receipts remain sha256-verifiable: the round-1
  sums-shape receipt re-read by the revised instrument reports
  `SHA256-CONTRACT: 4/5` with `MATCH-V1-PARTIAL` on the four unmoved paths and
  `CONTENT-DRIFT` on one (exit 10), and the time-carrying v1 stanza and pipe
  shapes report the same 4/5 contract with `METADATA-DRIFT` on the four unmoved
  paths (their stored times no longer match) — the single content drift is the
  operator-side churn recorded below, not a tool failure.
  **In-window custody drift:** the round-2 pre-pair
  receipt vs this round's pre-pair receipt agree 4/5 on sha256 — the third
  custody path (a client config) moved between rounds
  (`claims/c2/EX-29/verify-roundstart-vs-r2receipt.out`, `CONTENT-DRIFT … exit
  10`): the operator-side interactive-session churn class documented since arc2,
  recorded verbatim, not repaired (operator-owned surface). The five custody
  paths stayed READ-ONLY for every seat (capture/verify only; the clobber demo
  ran on a scratch write target).
- C3 freshness (fleet) — citation-drift pointer-table extension to the arc3-era
  citations. **Wave-start baseline measured independently by this scribe at
  `c07af80`** (matches the chain's own before-receipt EX-44 byte-for-byte, two
  separate runs): table `.ufo/gates/citation-drift/pointer-table.json` sha256
  `738b3a56…` carrying 31 entries (+4 quoted, 3 exempt); `expected.json` sha256
  `ff47bfd6…` pinning the table digest; probe `.ufo/gates/citation-drift/
  citation-drift-probe.py` sha256 `e2665074…`; probe findings 0 in **both**
  modes (`reported` rc 0 / `--strict` `clean` rc 0); selftest 13/13 exit 0;
  command A 82/82, rules 14/14. The named gap (round-1 C2 note + the round-10
  extension precedent): the 31 entries did not cover the arc3-era in-repo
  citations — the round-1 EVM knowledge entry and its map row, the arc3
  scorecard sections' pinned needles where applicable, the round-2 registry
  rows, and the custody receipt conventions.
  Landed at the work tree (EX-41; re-measured by this scribe): entries
  31 → 57 (+26 added, none removed), quoted unchanged (4), exemptions 3 → 8 —
  the NO-ENTRY causes materialized (append-only round reports; wave-internal
  provenance as a class; the five operator paths, which rule #11 forbids
  pinning; current-state count tokens; LOG prose) — with every pinnable arc3
  citation table-covered or NO-ENTRY with cause per the r10/r4 precedent
  (EX-41 `claims/c3/EX-41/03-census-dispositions.md` maps each row; the census
  surface is the four arc3 r1/r2 commits' non-wave added lines; one measured
  stale row is a round record's citation — `SKILL.md:371` moved to `:389`
  when round 2 inserted the rule-#14 block; adjudicated NO-ENTRY as an
  append-only round record, not repaired). The table digest is re-pinned in
  the expected-values file in the SAME commit (the F3 coupling) — measured:
  its only change is the pinned table digest, from `738b3a56…` to
  `bfc42f1b…` (expected-file sha256 `d97dd60a…`, re-derived after EX-41's final
  rewrite of that file at 13:13:28Z — an earlier measurement in this draft read
  a mid-window revision `179db3c7…` and was corrected by re-derivation per rule
  #14); the frozen-run revision,
  verdict and expected finding, the snapshot digest and the 13-case selftest
  table are byte-unchanged, and the frozen-run baseline was re-derived at its
  pinned revision (`failed findings=32 exit=1` with the expected
  `citation_dead` present — `06-frozen-run.txt`, 13:12:50Z).
  Post-landing measurements (this scribe, independently + EX-41
  `04-after-probe-and-selftest.txt`): probe findings 0 in both modes at the
  work tree; selftest 13/13 unchanged; digest re-derivation MATCH through
  EX-46's independent check tool; tamper checks re-run — a byte-changed table,
  an absent table, an unpinned baseline and a dead revision each hit
  could-not-evaluate exit 2 (`08-tamper-checks.txt`); command A unchanged
  (82/82, 14/14, 10.0/10.0, measured against the pre-round commit archive).
  Attacks attempted with verdicts: the extension has teeth where the old table
  was blind — at the same real drift revision the 31-entry table reads clean
  while the extension reports 2 dead citations (EX-43
  `drift-blind.txt`/`drift-caught.txt`); a needle+pointer mutation battery
  reddens every new entry (EX-41 `07-nonvacuity.txt` — "OK" on every case,
  rc 1, `citation_dead`); a neutered needle reports rather than repairing
  (EX-44 `neuter-proof.txt`); a stale pin and a one-byte tamper each exit 2
  (EX-46 simulations). [[FILL: RV-11/RV-12/CR-5/VZ-3 verifier confirmations and
  any residual they raise — not all landed at this draft's last poll]]. Scribe
  cross-check (not the chain's verification): an independent append simulation
  of the round's scorecard section measured 0 new census loci, PASS 0/0/0/0,
  with a planted-pin control FAILing (see
  `claims/c3/records-drafts/scorecard-section-draft.md` §3).
- Custody: [[FILL per CU-1 / the C2 landing: pre-pair capture time + 5/5, post-pair
  capture time + 5/5, the in-window drift comparison; any operator-side churn
  recorded verbatim, not repaired; the connector independently reproduced the
  four before-injections against the committed revision and their declared
  after-classes against the in-window revision on scratch fixtures]].
- Scope: kaidoku repo only; no pushes (standing rule); no installs (C1 reuses
  the round-1 receipted compiler prefix; receipt re-verified); custody paths
  read-only; scratch under `/var/tmp` or `/dev/shm` (the host `/tmp` quota
  exhaustion is standing — no recipe in this round uses `/tmp`).
