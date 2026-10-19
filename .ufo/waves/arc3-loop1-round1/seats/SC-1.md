# Seat report — SC-1 (chain c1, role scribe)

Wave `arc3-loop1-round1` · 2026-10-19 · HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(unchanged throughout; `git rev-parse HEAD` re-checked at every capture).
Writes by this seat: this report + `claims/c1/receipts/chain-ledger.draft.md`
only. No git mutations, no LOG/SCORECARD/corpus writes, no custody-path edits.
Scratch: attempted under `/tmp`, blocked by usrquota EDQUOT (evidence below);
abandoned — **no scratch files persisted anywhere** (my empty `/tmp/sc1-poll.sh`
was removed).

## 1. Work performed

- **Ledger artifact** (the seat's deliverable): `claims/c1/receipts/chain-ledger.draft.md`
  (sha256 `6d9427ccfe1b238dfba8d794e70d4a9fbdae61073bff7753de33d583f772b553`,
  computed 10:20Z; full hash in §3) — one row per frozen step
  (install → compile → probe(raw|hex) → reconciliation → control → rerun) plus
  two boundary rows (custody pre-pair, landing/close), each row carrying
  artifact paths + sha256 computed by this seat, producer seats, and
  status (LANDED/PARTIAL/GAP/VOID).
- **Baseline hash capture** 09:57–10:19Z: every sha256 in the ledger was
  computed by me with `sha256sum` — including 14 pins of EX-07's reconciliation
  table recomputed from disk (all matched), the npm prefix tree, the custody
  receipts, and all probe-leg JSONs. Totals at 10:19Z: 414 files under
  `claims/c1/` (excl. `_scratch/applytest` + `__pycache__`), 46 seat reports.
- **Independent before-state** (frozen recipe, SCORECARD.md:92-124, read-only
  `git show` on `e845c2b`): `{"citation_resolved_rules": 13, "coverage_score":
  10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 81, "mapped":
  81, "missing": [], "revision": "e845c2b…", "rule_blocks": 13}` — matches
  EX-11's landed file `claims/c1/EX-11/command-A-before.txt` (`8787e0c4…`,
  identical except EX-11 wrote literal `HEAD`).
- **Independent registry check** (read-only, 09:58Z): `npm view solc version` →
  `0.8.37`; `npm view solc dist.tarball` → the same tarball URL as EX-02's
  receipt (`https://registry.npmjs.org/solc/-/solc-0.8.37.tgz`).
- **Independent cross-checks** (all recomputed, none copied):
  - prefix `solc.js` `188c3fdc…` / `soljson.js` `221d7a66…` byte-identical to
    the ambient fnm-node-v24.21.0 tree (both files, both trees);
  - EX-07 pin table: all 14 recomputes MATCHED (`kdx-runtime.hex` `69a15782…`,
    `.bin` `9c40940e…`, ABI `40ad881e…`, planted-K `063eb723…`, six probe JSONs);
  - rerun envelope: `jq -c '.data'` identical sha256 `0144b17d…` (9935 B) across
    all four rerun files (EX-05 ×2, EX-09 ×2) — id `ev_4dd5ea20…` stable;
  - `cmp CR-2/recheck-ok-disk-tmpdir.json RV-2/probe-runtime-hex-6.4.0.json` →
    BYTE-IDENTICAL (cross-seat envelope identity);
  - exit-code hash decode: `9a271f2a…` = `0\n`, `4355a46b…` = `1\n` (EX-08
    edge-battery exits, and EX-26's census exit = 0);
  - `/tmp` mount: `tmpfs ... usrquota`; my own `tee` to `/tmp` failed
    `Disk quota exceeded` (09:58Z) — the fleet-wide hazard, independently
    reproduced.
- **Polling** (as instructed): inline re-lists of `claims/c1/` + `seats/` at
  ~60s cadence from 09:57Z to 10:19Z (no file-based poller — `/tmp` blocked;
  inline output retained in-session). Wave state grew 43 → 414 c1 files and
  2 → 46 seat reports across my window; ledger v1 (10:07Z) → v3 (10:19Z)
  tracked it.
- **Gaps named, not assumed closed**: R8 landing (knowledge entry + README
  edit + command A at records commit + custody post-pair) is parent-side and
  GAP at my capture; the ledger says so in the row and the footer.

## 2. Proposed changes

- None applied. Parent-facing patch-text artifacts produced by other seats
  (named here for the integrator, hashes in the ledger):
  `EX-02/proposed-receipts-solc-install.patch.md` `1ffde4b2…` →
  `receipts/solc-install.txt`; `EX-12/knowledge-entry.patch.md` `d662c195…`
  (+ CR-1 `knowledge-entry-additions.patch.md` `d117fcfe…`) →
  `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`;
  `EX-13/_scratch/map-token.patch` `ddfe0116…` (= `RV-4/map-token.frozen.patch`)
  → `corpus/README.md` map token; `CR-2/proposed-fixes.patch.md` `a62067dd…`;
  `CR-1/EX-07-reconcile-unwrap.patch.md` `f5e58cf6…`.
- This seat's own change surface is the ledger file only.

## 3. Before→after measurement (chain-claim relevant)

Commands + outputs (all run by this seat; outputs verbatim):

- **Ledger coverage before → after**:
  - 10:00Z first capture: rows landed 1/7 core (R1 install), 43 c1 files.
  - 10:19Z final capture: **7/7 core rows LANDED** (R0-R7), R8 drafts-only;
    414 c1 files (excl. scratch), 46 seat reports.
- **Command A before** (recipe verbatim at `e845c2b`): `knowledge_files 81,
  mapped 81, missing [], dangling [], rules 13/13, coverage/depth 10.0` —
  reproduced independently of EX-11/VZ-1/SC-2/PL-1.
- **Command A tree-level after** (CR-2 scratch clone + EX-12 patch applied,
  cited from `CR-2/command-A-runs.txt` `2405729c…`): `knowledge_files 82,
  mapped 82, missing [], dangling [], rules 13/13` — the claim's (e) shape at
  tree level; the records-commit run remains parent-side.
- **Ledger artifact hash** (this seat's own output):
  `sha256sum .ufo/waves/arc3-loop1-round1/claims/c1/receipts/chain-ledger.draft.md`
  → `__LEDGER_SHA__` (see §3 addendum below — computed at close).

## 4. Attacks / refutations attempted (with verdicts)

1. **Copy-vs-recompute attack on the whole chain**: recomputed every EX-07
   cited pin from disk rather than trusting the reconciliation md — all
   matched. Verdict: no refutation of EX-07's pins.
2. **Stale self-reference attack**: EX-07's `reconciliation.md` cites
   `reconcile.py` `c1be2731…`; disk measured `647395a0…`. Verdict: catch
   recorded (stale self-reference; CR-1 independently landed a wrap-fix
   patch, `f5e58cf6…`) — no effect on the reconciliation verdict, which rests
   on the driver outputs, not the md's own file hash.
3. **Rerun byte-identity attack**: EX-09's "byte-identical envelope" checked by
   my own extraction — identical `.data` bytes across all four runs
   (`0144b17d…`, 9935 B). Verdict: claim holds; EX-09's exact canonical hash
   `729c4881…` was not reproduced by my projection (recorded as their
   canonicalization, identity independently confirmed).
4. **Revision-resolution attack**: RV-4's preview cites revision `295cd30a`;
   `git rev-parse 295cd30a` → unknown revision (not an object in this repo).
   Verdict: preview is a simulation, its revision field is not repo-addressable
   — flagged, and the preview's token-only dangling=1 remains a valid negative
   control.
5. **Verdict-copy attack**: root `claims/c1/verdict.md` (`5f4b76ef…`) vs
   `VZ-1/verdict.md` (`ccbad891…`) — `cmp` DIFFERS at byte 13531/line 163.
   Verdict: root copy is stale; flagged so the parent reads VZ-1's final.
6. **Manifest-check attack**: EX-14's `MANIFEST.draft.check.sha256` is 0 bytes
   (`e3b0c442…`); `verify.log` records FAIL (`no properly formatted checksum
   lines found`). Verdict: check pair void as landed; flagged for regeneration.
7. **In-flight churn attack**: EX-08 exit files changed (1 → 0) during my
   window; ledger pins the 10:07Z state explicitly rather than asserting a
   single value.
8. **/tmp scratch rule**: refuted by environment (EDQUOT) — reproduced with
   `mount` + my own failed write; relocated per fleet practice, nothing
   persisted.

## 5. Blockers

- None blocking for this seat. Named boundaries: (a) `/tmp` scratch unusable
  (usrquota EDQUOT) — worked around with zero persisted scratch; (b) R8
  landing + records-commit command A + custody post-pair are parent-side by
  rule and are GAP in the ledger — partial evidence (patch texts, tree-level
  82/82, frozen verifier selftests) is in the ledger rows and must be
  re-checked at integration, not assumed closed.
