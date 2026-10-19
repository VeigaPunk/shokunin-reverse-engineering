# LOG.md entry draft — C2 records (SC-4, arc3-loop1-round3)

Seat SC-4 · chain c2 · role scribe · 2026-10-19. **Draft for the PARENT; LOG.md
was not touched by this seat.** Append at EOF (after the `arc3-loop1-round2`
entry, `LOG.md:1432-1455`; HEAD at draft time `c07af80`, file 1455 lines).
`⟨…⟩` = parent-fill slots; the **C2 bullet is drafted complete where evidence
already exists** — the before-state was independently reproduced by this seat on
a scratch copy (see `§2`), the rest carries `⟨FILL: …⟩` with the producing seat
named. Everything quoted came from a landed file, a command output, or a sha256.

**Pin-free discipline (kept deliberately).** LOG.md is not census-scanned
today (the census scope names `PROVINCE.md`, `SKILL.md`, `SCORECARD.md` only),
but this entry is written in the same pin-free voice as the SCORECARD-side
section: no client version literal, no `@`-pin, no `absolute/path.toml:NNN`
pointer, no client config filename. The five custody paths are named as what
they are — "three client configs + two shell profiles".

## Literal entry text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round3 — ⟨PARENT-FILL: C1 short phrase⟩ + custody-pair hardening (EACCES fail-closure, reference coverage, write-guard scope, selftest scratch-guard) + ⟨PARENT-FILL: C3 short phrase⟩ (2026-10-19)

- Dispatch: 64 seats frozen PRE-DISPATCH (roster = the round's
  `claims-frozen.md`; items array == roster, the r9/r10 assertion held before
  dispatch); the token-plan lane (key 1 of 3 — the operator's deepseek-v4.1-flash
  swarm directive recorded in the round-2 records). Delivered ⟨PARENT-FILL: N⟩/64
  per the roster reconciliation (count the items array, never the intent).
- C1 coverage — ⟨PARENT-FILL from the C1 records draft
  (`claims/c1/records-drafts/`): the optimizer-enabled + non-ERC-20-shaped
  carrier, planted selectors recovered K/K by the probe on-host with the reused
  receipted solc prefix, the new knowledge entry + map token, command A
  82 → 83 with the prior 82 byte-identical⟩.
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
  not a tool defect; recorded so it is not miscounted). ⟨PARENT: re-derive the
  landed identities at the records/work commit (rule #14) and confirm the
  registry row landed in the SAME commit; measured at draft close (13:26Z):
  tool `7cd19c3c…` (1155 L) and README `f30df42e…` (185 L) present in the
  worktree; `SKILL.md` still at its base identity `c134afcb…` (390 L, zero
  `UNEVALUABLE` / `require-paths` hits), so the registry row (patch text in this
  chain's tree: `claims/c2/EX-30/registry-row.patch.md` + `readme.patch.md`;
  implementer form `claims/c2/EX-21/proposed-skill-registry-row.patch.md`) is
  apply-ready and NOT yet applied — the same-commit coupling is open at draft
  close⟩. The round's own
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
- Custody: ⟨PARENT-FILL per the cross seat: pre-pair time + 5/5, post-pair time
  + 5/5, in-window drift statement⟩.
- Scope: kaidoku repo only; no pushes (standing rule); no installs (C1 reuses
  the round-1 receipted compiler prefix; receipt re-verified); custody paths
  read-only; scratch under `/var/tmp` or `/dev/shm` (the host `/tmp` quota
  exhaustion is standing — no recipe in this round uses `/tmp`).
<!-- END LITERAL ENTRY TEXT -->

## Notes for the parent

- **Fill the `⟨FILL⟩` slots from landed artifacts, not from the frozen claim.**
  The frozen claim is an intention; if the landing landed differently (or did
  not land), say so in the entry — an unrun check has not passed.
- The before-state block is this seat's own independent measurement and may be
  kept verbatim; if another c2 seat's before-repro (e.g. RV-5's
  `before-112d01dc` artifacts) contradicts or refines a number here, the
  contradiction is the finding — quote both.
- Keep the entry pin-free after filling (same reason as the SCORECARD-side
  section: one voice across both records, and no future re-scoping surprise).
  In particular: quote receipt **sha256s and epochs**, never a client config
  path or a version literal.
- Delivery count: take it from the roster reconciliation, never from the
  declared 64 (counting lesson `corpus/lessons/2026-10-18-wave-dispatch-counting.md`).