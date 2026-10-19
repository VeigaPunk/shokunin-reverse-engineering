# LOG.md entry draft — C3 records (SC-4, arc3-loop1-round2)

Seat SC-4 · chain c3 · role scribe · 2026-10-19. **Draft for the PARENT; LOG.md
was not touched by this seat.** Append at EOF (after the `arc3-loop1-round1`
entry, `LOG.md:1396-1430`; HEAD at draft time `14b1682`). `⟨…⟩` = parent-fill
slots; the **C3 bullet is drafted complete** and evidence-cited where the
round-2 evidence already exists; values that only other C3 seats can produce
are marked `⟨FILL: …⟩` with the producing seat named.

LOG.md is not read by the census instrument (its SCOPE table names only
`PROVINCE.md`, `SKILL.md`, `SCORECARD.md` — `.ufo/gates/c1-census-v10.py:139-161`),
and an EOF append shifts no line, so no pin moves. The SCORECARD-side section
for this round is drafted in `scorecard-section-draft.md` (same directory) and
**is** census-scoped: it is written pin-free and measured with the instrument
(see that file §3).

## Literal entry text (append as-is; fill `⟨FILL⟩`/`⟨PARENT-FILL⟩` slots first)

<!-- BEGIN LITERAL ENTRY TEXT -->
### arc3-loop1-round2 — depth rule #14 (self-identity re-derivation) + census fail-closures (absent-file guard, positive floor) + custody receipt v2 (epochs + inode/ctime) (2026-10-19)

- Dispatch: 64 seats frozen PRE-DISPATCH (roster = the round's
  `claims-frozen.md`; items array == roster, the r9/r10 assertion held before
  dispatch); opencode-go/deepseek-v4.1-flash (opencode-go key 2 of 7 — rotation
  advanced after round 1). Delivered ⟨PARENT-FILL: N⟩/64 per the roster
  reconciliation (count the items array, never the intent).
- C1 depth — queue-drain rule #14 (self-identity re-derivation discipline):
  ⟨PARENT-FILL from the C1 records draft (`claims/c1/records-drafts/`): rules
  13 → 14, 14/14 citation-resolved at the work commit, prior 13 rules
  byte-identical, citations in rule-#11 stanza form⟩.
- C2 freshness — census fail-closures H1 (absent-file guard) + H3 (positive
  floor): ⟨PARENT-FILL from the C2 records draft (`claims/c2/records-drafts/`):
  instrument v11 sha, the declared FAIL classes for absent CURRENT-only scoped
  files and for a zero-locus non-empty scope, round-1 injections reproducing as
  declared FAILs, HEAD PASS 0/0/0/0, creep audit 0 flags, scope-diff externa
  audit as the H4 certificate⟩.
- C3 operability — custody receipt v2 (sha256 + mtime epoch UTC-rendered and
  correctly labeled + inode + ctime). Measured origin (arc3-loop1-round1 cross
  seats): the canonical pre-pair receipt printed each path's modification time
  in the host's local zone (UTC-3) under a UTC label — `stat` epoch
  `1792011200` = `2026-10-14T20:53:20Z`, printed `2026-10-14 17:53:20` — a
  3-hour label defect that left the sha256 digests unaffected (round-1
  `claims/cross/receipts/config-pre-pair-metadata.txt`; CN-1 reproduction,
  round-1 `claims/cross/consistency.md:365-373`; re-reproduced this round from
  `os.lstat` ground truth by RV-14, capture-utc `2026-10-19T12:03:14Z`,
  `claims/c3/RV-14/receipts/label-defect-repro.txt`); and sha256-only custody
  is blind to a same-content rewrite — inode/ctime move while the digest does
  not (round-1 attack 3, `seats/RV-11.md`). Landed at the work commit:
  `.ufo/gates/custody-pair/custody-pair.py` (887 lines at first observation,
  churning in-window: sha256 `b10ad1c8…` at 09:03-03 — a revision whose verify
  path raised `KeyError: 'sha_agree'` at the summary line — and `112d01dc…` at
  09:05:19 -03, selftest-clean; **the parent re-derives the landed identity per
  rule #14: these shas are observations, not pins**) emits a v2 receipt per
  path — sha256 + `MTIME_EPOCH` + `MTIME_UTC_RENDER` (strict `gmtime` render,
  TZ-independent by construction) + `MTIME_LOCAL_RENDER` recorded separately +
  `CTIME_EPOCH`/`CTIME_NS` + `INODE` + mode/uid/gid — with declared exit
  classes (0 MATCH; 10 CONTENT-DRIFT; 11 REWRITE-DRIFT; 12 METADATA-DRIFT
  incl. LABEL-DEFECT; 13 ABSENT; 2 USAGE; 3 SELFTEST-FAIL) and v1
  compatibility for three v1 receipt shapes (stanza / `sha256sum` / pipe). The
  label defect is measured gone: epoch `1792011200` renders
  `2026-10-14T20:53:20Z` in the v2 receipt and the render is invariant across
  `TZ=UTC/-3/+5` (selftest case `label-utc-render-tz-independent`).
  **Independent selftest run by this scribe** (scratch `/var/tmp/sc4`):
  `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`, output
  sha256 `de6f7f81…` — this is a scribe-level spot check, not the chain's
  verification. A same-content rewrite is detected with no content change:
  selftest cases `same-content-rewrite-inplace-ctime-pin` (only `ctime_ns`
  moved → REWRITE-DRIFT, exit 11) and
  `same-content-rewrite-rename-inode-pin` (inode moved → exit 11) and
  reproduced on **live scratch copies** by three seats: EX-31 A1 (in-place,
  mtime restored, only `ctime_ns` moved → exit 11) and A2 (temp+rename, inode
  moved → exit 11) plus A3–A6 (content flip exit 10; absent exit 13; a mutated
  copy of the round receipt exit 10 — the comparator is non-vacuous; a mutated
  v1 sums entry exit 10) in `claims/c3/EX-31/attacks.out`; EX-32 battery A
  (stages A/B/C on `/var/tmp` scratch: in-place → REWRITE-DRIFT, rename →
  REWRITE-DRIFT, `battery-A-rewrite.log`); PL-3 C1/C2 (`measurements.txt`);
  RV-14 battery §8 on synthetic fixtures with a sandboxed fake home — rewrite →
  exit 11 with real paths untouched, write-guard rc 2, tool hash stable across
  its battery (`receipts/independent-battery.out`). EX-33's dedicated attack
  ladder (pinned `112d01dc…`, 13 receipts, `claims/c3/EX-33/attack-rewrite.md`)
  closes the class: six same-content rewrite forms (in-place, forged-mtime,
  rename-over, hardlink swap, delete+recreate, same-second) — sha256-only
  comparison silent on all six, the tool flags REWRITE-DRIFT exit 11 on every
  one, carried by inode / `mtime_ns` / `ctime_ns`, and by `ctime_ns` alone
  under a forged mtime; controls behave (content flip exit 10, absent exit 13,
  chmod exit 12); EX-33 also independently re-ran EX-31's live pre/post pair
  and RV-12's capture against it — MATCH 5/5 exit 0, sidecars OK, field-for-
  field agreement. v1 receipts remain verifiable: EX-35's
  back-compat re-check of the round-1 canonical receipt re-derived sha256,
  size, mode, uid, gid, mtime epoch, inode and ctime sidecar values — 5/5
  MATCH (`claims/c3/EX-35/backcompat-v1-standard.out`), and the tool's
  `_label_audit` reproduces the v1 label defect as a declared LABEL-DEFECT →
  METADATA-DRIFT exit 12. The round's own live pre-pair pair was captured by
  the tool before any other C3 live work:
  `claims/c3/receipts/config-pre-pair-v2.txt` (5/5 present, exit 0,
  captured-utc `2026-10-19T12:04:06Z`, HEAD `14b1682`, receipt sha256
  `fa9706c6…` = its sidecar; the header records tool sha256 `4862f642…` at
  capture time — an earlier revision than the settled one, so the parent
  should note which revision produced the pair); post-pair captured by the
  settled revision: EX-31's own pair `capture-pre.txt` (`3f3db73e…`) →
  `capture-post.txt` (`c0674f99…`) verifies MATCH 5/5, exit 0, zero drift
  (`claims/c3/EX-31/verify-pre-vs-post.out`; re-run `.rerun.out`); CU-1's
  corroboration: the authoritative pre-pair receipt replays byte-equal from the
  held earlier revision, and a same-revision pair (captured 12:06:53Z and
  12:08:12Z) agrees with CU-1's independent ledger 50/50 field-classes ×5
  paths, with empty normalized diffs and ns fields matching GNU stat renders
  (`claims/cross/CU-1/`). The five custody paths stayed READ-ONLY: the tool
  refuses to write a receipt over a custody path (selftest case
  `refuses-to-write-over-custody-path`) and independent sha256+inode/ctime
  captures agree (RV-12 `independent-pre.txt` 5/5, capture-utc
  `2026-10-19T12:01:12Z`; VZ-3 `independent-capture-T0.txt`). No
  corpus/knowledge edit in this claim; no scope-bound widening anywhere.
- Custody: pre-pair ⟨PARENT-FILL per CU-1: time, 5/5⟩; independent pre-captures
  landed this round — RV-12 (sha256 + inode + ctime + mode/uid/gid, 5/5,
  capture-utc `2026-10-19T12:01:12Z`, `claims/c3/RV-12/independent-pre.txt`) and
  VZ-4's capture script; post-pair ⟨PARENT-FILL⟩; in-window drift ⟨PARENT-FILL:
  expected none — state the measured comparison⟩.
- Carried debt (named): ⟨PARENT-FILL C1/C2 merges⟩; C3 adds three measured
  residuals — (i) a `capture` over an **unreadable** path raises an uncaught
  `PermissionError` traceback (exit 1, outside the tool's declared class table:
  the file is opened for hashing outside the stat guard — EX-40
  `real-tool-unreadable.txt` + `.traceback`, tool sha `112d01dc…`), so the
  capture path is not yet injection-total the way the verify path is;
  (ii) `verify` does not authenticate the receipt itself — a tampered receipt
  returned `MATCH` exit 0 (the capture-time sidecar digest catches it, but
  `verify` never reads the sidecar; a reader must run the sidecar check or trust
  the committed copy — EX-33 §4.1, `receipts/real/J/verify-tampered.txt`); a
  patch-text suggestion (verify reads `<receipt>.sha256` when present) is
  EX-33's, not landed; (iii) `selftest --scratch <nonexistent>` dies with a
  traceback instead of a usage error (EX-33 §6). The whole-second
  time-granularity boundary EX-33 measured is closed in the landed tool by the
  nanosecond fields (not debt). The round's census residual H4
  (self-certification — the instrument cannot detect its own scope widening)
  stays named until an external audit lands.
- Scope: kaidoku repo only; no pushes; no installs this round (standing
  round-2 rule); scratch under `/var/tmp` or `/dev/shm` (the host `/tmp` quota
  stays exhausted — standing hazard, `SCORECARD.md:991`).
<!-- END LITERAL ENTRY TEXT -->

## Notes for the parent

- **Do not restate client version pins or `config.toml`-style `path:line`
  pointers in the LOG entry either**, for consistency with the SCORECARD-side
  section; LOG is not census-scanned today, but keeping both records in one
  pin-free voice avoids a future re-scoping surprise. The C3 bullet above names
  no client config path and no version literal.
- The C1/C2 bullets must come from this round's C1/C2 records drafts; if those
  seats did not land, mark their evidence as a named gap (an unrun check has
  not passed) rather than paraphrasing the frozen claim as if measured.
- The C3 bullet's `⟨FILL⟩` slots are all C3-chain artifacts (EX-31 real-target
  tool; EX-33/CR-4 attacks; EX-32 v1-recheck; RV-11..RV-14 verification;
  CU-1/VZ-4 custody). Fill them from the landed artifacts, not from the frozen
  claim text.
- Delivery count: take it from the roster reconciliation, never from the
  declared 64 (counting lesson `corpus/lessons/2026-10-18-wave-dispatch-counting.md`).
