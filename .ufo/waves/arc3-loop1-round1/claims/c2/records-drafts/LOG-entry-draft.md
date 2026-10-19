# LOG.md entry — DRAFT (arc3-loop1-round1, C2 chain records)

Status: DRAFT by seat SC-5 (C2 chain, scribe) — **NOT APPLIED**. Parent
integrates after the wave. Every `[[FILL: …]]` must be replaced from the
wave's sealed receipts (or the sentence rewritten to the honest-stop branch)
before landing. The C1/C3 paragraphs are shape-only: fill from those chains'
records (SC-3's `claims/c1/records-drafts/` and SC-6/SC-7 drafts + chain
receipts). The pasteable text is the block below the horizontal rule; the
evidence inventory at the bottom is SC-5's poll notes, not part of the entry.

---

### arc3-loop1-round1 — coverage (EVM real-bytecode) + operability (probe guard) + freshness (census disposition)

- Motivating evidence: `PROVINCE.md:91-93` Frontier "EVM bytecode (extended)" —
  selectors held on a synthetic 81-byte dispatcher only (r3-07); "real
  solc/vyper-compiled bytecode untested". C2: the citation-drift probe's
  frozen-run guard (`SCORECARD.md:925-926`, arc2-loop1-round4 carried debt;
  r5 disposition `:1054-1060`). C3: the census scope-table drift (E22;
  `SCORECARD.md` arc2-loop1-round3). Round declaration:
  `.ufo/waves/arc3-loop1-round1/claims-frozen.md` (64-seat roster frozen
  PRE-DISPATCH, per the r9 wire-it amendment).
- Dispatch: 64 seats (items array == frozen roster, counted at dispatch),
  `opencode-go/deepseek-v4.1-flash` (opencode-go key 1 of 7 — round robin
  starts here). Delivered [[FILL: n/64]].
- C1 coverage — [[FROM C1 CHAIN: real solc-compiled bytecode, first held;
  install receipt + K/K selectors + knowledge entry + command A 81 → 82;
  see SC-3's draft for the fill shape]]
- C2 operability — the citation-drift probe's frozen-run guard lands (R6
  debt closes; measured before and after). Before at HEAD `e845c2b`: selftest
  11/11 exit 0, probe `reported findings=0 exit 0`, and `expected.json`
  carries no table digest (`RV-7/verify-pre.log`: "pin-for-table-digest in
  expected.json: NONE") — a valid-JSON tampered table (entries emptied, `{}`,
  `must_match` weakened to `.*`) reads **silent `findings=0 exit=0` in both
  modes** (EX-20; RV-6 `harness-pre.out` cases B/C/F/G; SC-4 `verify-before.txt`
  §4/§5; RV-8 T5/T5b). The debt's "gate-blocking if ever promoted" clause is
  now measured: at the frozen revision `679af5d…` the real table yields 16
  findings (`failed exit=1` strict) and the emptied table yields
  `clean findings=0 exit=0` — a hand-edit erases a failed gate verdict
  (RV-6 attack 5; EX-19 matrix). After (EX-16 landed PL-2's patch verbatim —
  `claims/c2/EX-16/landing-diff.md`, probe +41/−9, expected.json one-line;
  landed sha256 probe `e2665074…`, expected `ff47bfd6…`, table unchanged
  `738b3a56…`): `expected.json` pins `pointer_table.sha256` =
  `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`; the
  preflight order is expected-load → pin-read (absent/malformed →
  `pointer_table_unpinned`, exit 2) → table-bytes read (absent →
  `pointer_table_unreadable`, exit 2) → digest check (mismatch →
  `pointer_table_tampered`, exit 2) → JSON parse — all before any entry is
  graded, so a tampered table can never produce silent findings, in probe or
  `--strict` mode; drift reporting unchanged (frozen-rev 16 findings, probe
  rc 0 / strict rc 1). Selftest 11 → 13 cases: `table_tampered` (exit 2,
  `pointer_table_tampered`), `table_absent` (exit 2,
  `pointer_table_unreadable`); the harness pins each case's table digest, so
  the 11 existing cases stay CLEAN on the guard-pass path. Landed matrix
  (EX-16 `after-injections.txt` A–K; independently re-run by SC-5 on the
  landed files — `claims/c2/SC-5/after-verify.log`): selftest 13/13 exit 0;
  tampered/whitespace-append/absent/unpinned/malformed/type-confused tables
  each exit 2 with the declared ids; byte-identical table copy rc 0; custom
  table + custom pinned expected rc 0 (the experiment escape hatch). Guard
  additivity: with the ORIGINAL pre-guard pins, all 7 baseline legs are
  byte-identical (EX-19 `stability.md`; AST fingerprint: 10/13 top-level
  nodes unchanged, 4 hunks confined to the guard surface). The `SKILL.md:371`
  registry row states the preflight semantics and 13 cases — patch text only
  (protected file): planner wording `claims/c2/PL-2/frozen-run-guard.patch.md`
  (patch 3); variant `claims/c2/EX-20/registry-row.patch.md` (old row
  `6413e8dc…` → new `08be1ec2…`; `patch -p1` rc 0, line count 371, RV-6
  patchtest reproduced); **parent must apply the row in the records commit**
  or the claim's registry-row clause is unmet. Named consequences/debt:
  (a) any invocation with a custom `--table` and the new `expected.json`
  reads exit 2 `pointer_table_tampered` — r10-style custom-table recipes must
  pin their own digest (the escape hatch above) or use the committed table
  (EX-19 attack 6; RV-8 D1/D2 measured; EX-16 case I); (b) the pin chain
  terminates at `expected.json` itself (same trust class as the case table —
  R1 in EX-24's recommendation: registry-level pin, parent-written;
  fail-closed unpinned adopted per R2); (c) the frozen-run clause's outcome
  half stays open: the `frozen_run` block's `expected_findings:
  ["citation_dead"]` is already false at the admitted reading (16 findings,
  4 classes — CR2's r10 mismatch), and `revision: 679af5d` + the current
  table describes a state that never existed (the gate postdates the rev by
  5 commits); the faithful-replay inputs (r4-era table `edaa4e59…`, any
  pre-pin expected) now read exit 2 under the guard — CR-3's clause patch
  (`table_scope` + `history[]`, `claims/c2/CR-3/guard-vs-frozen-run.patch.md`)
  is proposed, not applied; (d) pin hardening beyond bytes-on-disk
  (TOCTOU/symlink/`O_NOFOLLOW`; EX-18's symlink-to-stale shape) is patch text
  only (EX-22), not landed; (e) the claim's parenthetical reads as the
  guard-pass path on the existing `clean` fixture + 2 new cases = 13 (EX-24
  §6 count note; EX-23's false-positive census of honest-edit re-keys —
  every table edit must re-pin in the same commit, per the probe header the
  patch adds).
- C3 freshness — [[FROM C3 CHAIN: the E22 scope-table finding dispositioned
  by measurement at HEAD; census v10 verdict before → after; see SC-6/SC-7
  drafts]]
- Custody: pre-pair `claims/cross/receipts/config-pre-pair.txt`
  (2026-10-19T09:57:18Z, 5/5, HEAD `e845c2b`); post-pair [[FILL: path/time,
  5/5]]; zero drift [[FILL]]; the frozen prediction held — no `config.toml`
  drift [[FILL: receipt corroboration]].
- Process notes: `/tmp` (tmpfs, usrquota) exhausted mid-wave — writes fail
  `Disk quota exceeded` (EDQUOT/Errno 122) fleet-wide; seats moved scratch to
  `/home`-side dirs, `/var/tmp`, `~/.cache`, or wave-local tmp (EX-02, EX-11,
  EX-19, EX-23, EX-24, PL-2, RV-6, RV-7, RV-8, SC-4 all recorded the wall;
  the r4 `/tmp-quota abort` defect class). Untracked
  `.ufo/gates/__pycache__/` appeared during the wave (a concurrent census
  import) — keep out of the commit (PL-2 §8; SC-4 changeset note). The wave
  ran with EX-16's landing absent through most seat windows — reviewers
  (RV-6/RV-8/EX-19/EX-23/EX-24/SC-4) froze one-command after-harnesses so the
  post-landing re-measure is a rerun, not a re-derivation.
- Carried debt (named): [[FILL: e.g. the custom-`--table` re-pin contract; the
  registry-level pin (R1) if adopted; plus C1/C3 debts]].
- Retired: [[FILL: e.g. the R6 frozen-run-guard debt (SCORECARD.md:925-926)
  closes; or none]].
- Scope: no config edits, no pushes, repo-local.

---

## SC-5 poll notes (not part of the entry)

Evidence inventory at draft time, with SC-5's own re-verification where
possible. **EX-16's real-target landing arrived mid-draft** (`claims/c2/EX-16/`
present; worktree files modified, uncommitted; the parent commits at records
time) — every after-value above is landed-measured on the real files, and
SC-5 re-ran the full matrix independently (`claims/c2/SC-5/after-verify.log`).
Remaining [[FILL]]s: the landing/records commit sha, the delivered count, the
post-pair custody receipt.

- Before-state (SC-5 re-ran on a scratch copy; matches EX-25/SC-4/RV-6/RV-8):
  HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`; selftest
  `CLEAN cases=11 passed=11 failed=0 exit=0`; probe `reported findings=0
  exit=0`; `--strict` `clean findings=0 exit=0`; file sha256s probe
  `3067621a…`, expected `4e28ba90…`, table `738b3a56…` (SKILL.md `5c93c7c1…`).
- Prototype (PL-2's patch applied by SC-5 to a scratch copy via
  `patch -p1`; reproduced PL-2's stated hashes exactly — probe `e2665074…`,
  expected `ff47bfd6…`): selftest 13/13 CLEAN exit 0; real table rc 0;
  emptied table exit 2 `pointer_table_tampered` (both modes); absent exit 2
  `pointer_table_unreadable`; unpinned exit 2 `pointer_table_unpinned`;
  frozen rev `679af5d…` 16 findings rc 0 / strict rc 1; byte-identical copy
  rc 0. Log: `claims/c2/SC-5/pl2-verify.log`.
- EX-21's earlier prototype (different pin key `table_sha256`, skip-on-unpinned)
  also verified by SC-5 (`claims/c2/SC-5/proto-verify.log`): 13/13, tampered
  exit 2, but **unpinned + tampered reads silent rc 0** — PL-2's fail-closed
  `pointer_table_unpinned` supersedes it; the landed design must be PL-2's,
  not EX-21's, or the unpinned hole stays open and EX-20's row text is wrong.
- The three coupling tokens the parent must reconcile against EX-16's landed
  code before applying any row patch (EX-20 §Coupling, RV-6 §2): the
  digest-mismatch id (`pointer_table_tampered` per PL-2/EX-21),
  the absent-table id (kept `pointer_table_unreadable`), the unpinned clause
  (present per PL-2; absent per EX-21), and the case count (13).
- Chain evidence files: `claims/c2/PL-2/plan.md` + `frozen-run-guard.patch.md`;
  `claims/c2/EX-19/stability.md`; `claims/c2/EX-20/registry-row.patch.md`;
  `claims/c2/EX-21/tmp/proto/`; `claims/c2/EX-23/falsepositives.md` +
  `harness/`; `claims/c2/EX-24/pin-mutability.md`; `claims/c2/EX-25/` (before
  logs + replay driver); `claims/c2/RV-6/harness-pre.out` + poll log;
  `claims/c2/RV-7/verify-pre.log`; `claims/c2/RV-8/consumer-inventory.md` +
  `guard-compat-matrix.md` + `baseline-transcripts.txt`;
  `claims/c2/SC-4/verify-before.txt` + `changeset.md`.
- Custody pre-pair: `claims/cross/receipts/config-pre-pair.txt` (CU-1,
  2026-10-19T09:57:18Z, 5/5, HEAD `e845c2b`). Post-pair not yet landed at
  draft time.
- The frozen claim's after-shape (claims-frozen.md:46-54) is the authority for
  every [[FILL]] above; SC-5 verified the before-values, the prototype
  behavior, and the artifact inventory listed here.
