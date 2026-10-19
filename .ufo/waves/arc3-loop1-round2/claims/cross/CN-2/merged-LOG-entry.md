# merged LOG entry — arc3-loop1-round2 (seat CN-2, cross connector)

Assembled 2026-10-19 by seat CN-2 from the three chains' literal LOG drafts (C1
= SC-1, C2 = SC-3, C3 = SC-4). **Pasteable text only** — the parent lands it as
R1. Placeholder convention normalized to `[[FILL: …]]`; the entry keeps the
pin-free voice (LOG is not census-scanned today — the instrument's SCOPE names
only the three scoped files — but one records voice avoids a future re-scoping
surprise).

## Literal LOG entry (append at EOF after the round-1 entry)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round2 — depth rule #14 (self-identity re-derivation) + census fail-closures + custody receipt v2 (2026-10-19)

- Dispatch: 64 seats frozen PRE-DISPATCH (roster enumerated mechanically —
  12+30+18+4, every name once; a pre-dispatch draft freeze was discarded for a
  hand-arithmetized miscount before any seats were dispatched — the r5 lesson
  applied to the wave's own freeze); `opencode-go/deepseek-v4.1-flash`
  (opencode-go key 2 of 7 — rotation advanced after round 1). Delivered
  [[FILL: N/64 per the roster reconciliation; count the items array, never the
  intent]].
- C1 depth — queue-drain rule #14, the self-identity re-derivation discipline:
  an artifact that records its own byte-identity (size/hash/line count) must
  re-derive that identity after every revision; a stale self-identity voids the
  verification block, not the work; the integrator records the fresh identity
  at landing. Origin (round 1): the entry patch churned mid-wave and its own
  "Verification performed" identity still described the superseded revision —
  caught by the round-1 critic (F2) and the convergence seat (D9); the landed
  bytes were re-derived at landing (10,225 B, `dd986f56…`). Landed: [[FILL: the
  landed rule-#14 block / patch-text path — appended at the craft-section tail
  after the natural-control rule, citations in the section's anchor-keyed
  (stanza key + receipt) form]]. Measured: craft rules 13/13 resolved → 14/14
  resolved [[FILL: quote the command-A run at the work commit]]; prior 13 rule
  blocks byte-identical [[FILL: the C1 block-digest baseline + an independent
  citation audit verdict]]; citation-drift probe re-run [[FILL: findings=0]];
  the rule's own instrument demonstrated live [[FILL: stale-twin catch /
  landed-pair fresh verdicts]]. Coupling recorded: the promotion assertion that
  names the craft section's range and the prior count goes stale with the
  append (the probe's range needle stays resolvable); refresh drafted as patch
  text [[FILL: path]]. The critic's parser run recorded the metric's limit: a
  wave-tree-only rule text scores 13/14 (depth 9.29) and a decoration-only text
  scores 14/14, so the verdict rests on the live catch, not the count.
- C2 freshness — the census fail-closures H1 (absent-file guard) and H3
  (positive floor) landed in the instrument (round-1 latent holes, patch texts
  in the round-1 tree). Before at HEAD `14b1682` (round-1 instrument,
  `6f1d19ff…`): ordinary run PASS 0/0/0/0 exit 0; an absent scoped file reads
  silent PASS exit 0 (`lines=0 loci=0` — both its declared rows CURRENT, no
  marker assertion fires); needles neutered reads all-zero loci with the old
  vacuous guard and PASS exit 0. After [[FILL: the instrument sha256 re-derived
  at the records commit — the writer was still iterating in-window; CN-2
  observed `2a89793a…` → `59975ae0…` → `82fb807e…` → `762bfebe…` →
  `c95a5cf3…`, and the last two FAIL the ordinary HEAD run — see the
  records-outline's W1 finding]]: an absent/unreadable/short scoped file is
  the declared class `UNREADABLE` (`lines=None`, carried in the report and
  `--json`, exit 1); a zero-locus scoped file is the declared class
  `BLIND-INSTRUMENT`, exit 1 (independent CN-2 re-measure:
  `claims/cross/CN-2/receipts/census-h1h3-before-after.txt`). So the round-1
  silent-PASS injections reproduce as declared FAILs where the floor is
  evaluated; the ordinary HEAD run is PASS 0/0/0/0 at the revision that
  satisfies the floor [[FILL: quote the records-commit run — precondition: the
  landed revision must PASS at HEAD, see W1]]. Scope bounds otherwise
  byte-stable — external diff audit (scope-diff form) [[FILL: flags=0 output
  path]] as the chain's certificate. Named residual: the census cannot certify
  its own scope (self-certification) — the external audit is the certificate;
  the inline-marker excusal and gate-free-statement classes stay carried debt.
- C3 operability — custody receipt v2 landed as a committed tool under the
  gates directory. Measured origin (round 1): the canonical pre-pair receipt
  printed each path's modification time in the host's local zone under a UTC
  label (recorded epoch `1792011200` = `2026-10-14T20:53:20Z`, printed as the
  local render — a 3-hour label defect; digests unaffected); and sha256-only
  custody is blind to a same-content rewrite — inode/ctime move, the digest
  does not. Landed at the work commit: a v2 receipt per path — sha256 + mtime
  as an epoch rendered in UTC under a correct label (local render recorded
  separately) + inode + ctime (+ mode/uid/gid) — with declared exit classes
  (0 MATCH; 10 CONTENT-DRIFT; 11 REWRITE-DRIFT; 12 METADATA-DRIFT incl.
  LABEL-DEFECT; 13 ABSENT; 2 USAGE; 3 SELFTEST-FAIL) and v1 compatibility for
  three v1 receipt shapes [[FILL: re-derive the tool sha256 at the records
  commit — `112d01dc…` at CN-2 measurement time]]. Independent CN-2 checks:
  selftest CLEAN 15/15; the label defect measured gone (epoch renders
  `2026-10-14T20:53:20Z`, TZ-invariant by selftest case); a live same-content
  rewrite on a scratch copy is detected — in-place with mtime rolled back →
  `REWRITE-DRIFT moved=ctime_ns` exit 11, remove-and-recreate with identical
  bytes → `moved=inode,mtime_ns` exit 11, and in both `SHA256-CONTRACT: 1/1
  paths agree` (the digest alone would not have seen it); v1 receipts stay
  verifiable on the sha256 field (round-1 canonical receipt → 5/5 agree, with
  the v1 label defect surfaced as a declared LABEL-DEFECT → METADATA-DRIFT
  class). The round's own live pre-pair was captured by the tool before any
  other C3 live work (5/5, exit 0, `fa9706c6…` = its sidecar, captured with an
  earlier tool revision `4862f642…` — the parent re-derives identities at
  landing). The five custody paths stayed READ-ONLY for every seat (hash/stat
  capture only; the tool refuses to write a receipt over a custody path;
  independent captures agree 5/5).
- Custody: pre-pair [[FILL: receipt path, capture time, 5/5 — the v2 pair from
  the C3 tool, plus the independent captures]]; post-pair [[FILL: path, time,
  5/5]]; in-window drift [[FILL: expected none — state the measured
  comparison]].
- Process notes: scratch discipline this round was `/var/tmp` + `/dev/shm`
  (the host default scratch mount's per-user quota is exhausted — standing
  record); the wave's freeze miscount was caught pre-dispatch by mechanical
  enumeration; the instruments' real targets were the census file (freshness
  chain) and the new custody-pair directory (operability chain) plus the
  craft-text append (depth chain); `.ufo/gates/__pycache__/` untracked residue
  is present (and this round also produced one inside the new gate directory)
  — keep both out of the commits.
- Carried debt (named): [[FILL: C1 items — the promotion range/count coupling
  until its patch text lands]]; [[FILL: C2 items — scope self-certification
  (external audit as certificate), inline-marker excusal, gate-free statement
  classes, and the per-file floor's own residual (partial per-needle blindness
  keeps each file above zero and reads PASS; only an external count/scope
  audit sees it)]]. [[FILL: C3 items — EX-31's stated residuals, and the
  pre-pair receipt's earlier tool revision if it is kept as the canonical
  round-2 pair]]; the host scratch-quota hazard and the `__pycache__` residue
  class stay standing. Retired: [[FILL: the round-1 census latent holes H1/H3
  retire on the landed guards — conditional on W1 being resolved so the landed
  revision passed the ordinary run at the records commit; else "none"]].
- Scope: kaidoku repo only; no pushes (the standing no-push rule holds); no
  installs this round; scratch under `/var/tmp` or `/dev/shm`.
<!-- END LITERAL ENTRY TEXT -->
