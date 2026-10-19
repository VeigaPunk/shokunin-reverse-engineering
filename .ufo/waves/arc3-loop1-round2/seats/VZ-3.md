# SEAT VZ-3 — chain c3, role convergence — arc3-loop1-round2

Seat line: poll the seats dir every 60s (max 25 checks); reconcile C3 seats into
`claims/c3/verdict.md`: VERIFIED or NOT-VERIFIED + evidence + named debt. Seat
report last.

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD
`14b1682b1128d2e41085ebc79c9addeb8786d420` (no git mutation by this seat; the
parent commits). Chain target under verdict: `.ufo/gates/custody-pair/` —
`custody-pair.py` 889 lines / 39,157 B / sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` + `README.md`
sha256 `fa484d573b0debb0d2ed134d076cb9593e7c3ee910ad4487d99cb9f3a8239bba`
(re-hashed by this seat at 12:27Z; unchanged since 12:05:19Z). Write scope held:
this seat wrote only its seat dir (`claims/c3/VZ-3/**`) and this report; scratch
under `/var/tmp/vz3-scratch/` (`/tmp` never used).

## 1. Work performed (evidence pointers)

- **Deliverable — the chain verdict:**
  `.ufo/waves/arc3-loop1-round2/claims/c3/verdict.md`, 216 lines, sha256
  `589919181995fd729f69595e587ff5fd11726e3c1eaebec813045ade91525fe7`
  (identity re-derived after the last edit — the D2 first-hand reproduction;
  rule-#14 discipline). Verdict: **VERIFIED** (filesystem level), with the
  "committed"/"records commit" clauses named as parent-side and 11 named debt
  items (D1–D11), ticketed closing procedure, and the per-component evidence
  table.
- **Polling (the seat line):** 60 s poller from 12:00:37Z, checks 1–19, exited
  early at **ALL-LANDED 17/17** 12:18:37Z (log archived:
  `claims/c3/VZ-3/evidence/poll-log.txt`; well inside the 25-check budget).
  During polling this seat read every C3 seat report as it landed (EX-31,
  EX-32, EX-33, EX-34, EX-35, EX-36, EX-37, EX-38, EX-39, EX-40, PL-3, SC-4,
  CR-4, RV-11, RV-12, RV-13, RV-14) plus their key artifacts, and the round-1
  tree for the origin readings (round-1 `claims/c3/verdict.md`,
  `claims/cross/consistency.md:365-373`, `RV-11.md attack 3`).
- **Own verification runs (all against the landed bytes):**
  `independent-capture-T0.txt` (12:01:26Z, own stat+sha harness
  `vz3-independent-capture.sh`); tool selftest re-run; live captures T1
  (`evidence/vz3-T1.txt`) and T2 (`live-T2.txt`, sha `73b0fab7…`); cross-checks
  T1/T2′ vs T0 and of EX-31/EX-32 receipts via
  `vz3-compare-receipt-vs-independent.py`; TZ label run; v1 stanza + sums
  verifies; a 3-fixture rewrite cycle (`evidence/cycle-ref-receipt.txt`,
  `evidence/cycle-verify-transcript.txt`); the v1-blindness staging
  (`evidence/attack3-staging.log`, `v1-style-sha-{before,after}.txt`); and a
  first-hand EACCES reproduction (`evidence/eacces-repro.txt`).
- Cross-checks of peers' identities quoted in the verdict were re-derived, not
  copied: EX-31 sidecars (`sha256sum -c` OK), EX-32's pre-pair payload diffed
  byte-equal to EX-31's capture, census/probe exit files re-read
  (`EX-37/runs/v10-head.exit` = 0, `h1h3-head.exit` = 0; `EX-38/after-probe-*`).

## 2. Proposed changes

**None** — convergence seat, no patch text authored (the chain's write target
belonged to EX-31 alone). The verdict's §"Closing procedure" lists the parent's
integration steps: commit the two gate files (pycache excluded); land **one
merged** registry row (PL-3 + EX-36, with the v1 exit-split and real exit map);
records from SC-4's draft, pin-free, with the census re-run after C2 settles;
optional re-capture/annotation of the pre-pair (D8).

## 3. Before → after measurement (chain c3 claim: custody receipt v2)

Independently measured by this seat; every command below is first-hand (the
verdict carries the full table):

- **T0 reference** (`independent-capture-T0.txt`, 12:01:26Z): 5 paths; devin
  sha `16f496e6…`, epoch `1792011200`, local render `17:53:20 -03` — the
  defect arithmetic (`gmtime(1792011200)` = `2026-10-14T20:53:20Z`, my own
  derivation).
- **Selftest**: `CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`.
- **Live captures T1/T2**: both `OK paths=5/5 exit=0`; T1↔T2
  `MATCH 5/5 drift=0 exit=0`; T2 vs T0 **AGREE 6/6 fields × 5 paths**;
  5/5 digests still equal the round-1 pins ⇒ zero drift, custody read-only.
- **Label (after vs before)**: `TZ=Asia/Tokyo` capture keeps
  `MTIME_UTC_RENDER: 2026-10-14T20:53:20Z` (UTC, TZ-independent) while the
  local render `+09:00` is carried separately; the round-1 canonical v1 receipt
  re-verified against live → exit 12, 5× `LABEL-DEFECT`, `SHA256-CONTRACT: 5/5`.
- **v1 verifiability**: sums-form → `MATCH-V1-PARTIAL 5/5`, exit 0; stanza-form
  → exit 12 with the sha contract intact (the exit-code nuance ruled in the
  verdict, answering EX-32 F4 / EX-35 A7 / RV-12 A7).
- **Same-content rewrite (scratch cycle)**: rename-over → `REWRITE-DRIFT
  moved=inode`; in-place with mtime restored → `REWRITE-DRIFT moved=ctime_ns`;
  untouched control `MATCH`; **all three states sha-identical**
  (`5eaa96da…`), `SHA256-CONTRACT 3/3`, overall exit 11.
- **v1 blindness leg (staging)**: same-content rewrites under the v1 surface —
  `v1-style-sha-before.txt` vs `-after.txt` diff **EMPTY** while inode
  (10950841 → 10964595) and ctime moved ⇒ the v1→v2 movement is exactly the
  identity pins, not a content side effect.
- **Headline before→after (chain roll-up in the verdict):** same-content
  rewrite visibility **v1 0/13 → v2 13/13** attack forms (CR-4 matrix; EX-33
  6/6; VZ-3 2/2; RV-12, RV-13, PL-3, EX-40 corroborating), label defect
  reproduced-as-declared and fixed, pre/post pair captured (EX-32 pre 12:04:06Z
  + EX-31 pair + wave-spanning payload identity across 4 seats).

## 4. Attacks / refutations attempted, with verdicts

| # | Attack / refutation (this seat) | Verdict |
|---|---|---|
| A1 | "the UTC render is localtime again (the v1 defect)" | **REFUTED** — TZ=Asia/Tokyo run keeps the UTC render byte-identical; the v1 defect is *reproduced and named* by the tool's LABEL-DEFECT class |
| A2 | "sha256-only is enough; the rewrite class is not real" | **REFUTED** — v1 staging diff EMPTY vs v2 exit 11 on the same rewrite; the cycles' sha contract stays 3/3 (detection is not content) |
| A3 | "the comparator is vacuous (everything MATCHes)" | **REFUTED** — rewrite cycle: 2 REWRITE-DRIFT + 1 MATCH in one run; EX-31/33/CR-4 mutation batteries corroborate (selftest S1–S3 sabotage DIRTY exit 3, RV-11) |
| A4 | "v1 receipts verify cleanly (exit-0 promise)" | **REFINED, ruled** — sums exit 0; time-carrying stanza/pipe exit 12 *by design* with 5/5 sha contract; both numbers must be quoted together |
| A5 | "the receipts are stale self-identities" | **REFUTED for the landed revision** — every receipt embeds `112d01dc…` = current sha; EX-32's authoritative pre-pair embeds superseded `4862f642…` (**D8** debt: annotate or re-capture; payloads byte-identical) |
| A6 | "EX-31's same-instant pre/post pair spans the wave" | **REFINED** — both captures are 12:06:26Z (label-only difference); the wave-spanning zero-drift claim rests on payload identity across EX-32 pre / EX-31 post / RV-12 C-final / VZ-3 T1–T2 (all MATCH) |
| A7 | "the pass path is clean; fail-open classes don't exist" | **REFUTED first-hand** — reproduced EX-40's D2: EACCES path → capture `PARTIAL paths=0/1 exit=13`, `verify --live` **MATCH exit 0** (`compared=0/11`); chmod-000 candidate → `PermissionError` traceback exit 1 (`custody-pair.py:219` via `:168`), outside the declared map |
| A8 | "peer-reported holes are enough without my run" (evidence discipline self-test) | **CORRECTED** — D2 was re-run first-hand before being carried; D1/D3/D4/D5 stand on the named seat artifacts (CR-4 `toctou-measurement.py`, EX-35 A5, EX-33 §4.1, CR-4 attacks 4–6), each cited with its file |

## 5. Blockers

- **None** for this seat; the poll budget was not exhausted (19/25 checks,
  ALL-LANDED at 12:18:37Z) and all 17 C3 reports landed.
- Named for the parent (not blockers): the tool is **untracked**
  (`?? .ufo/gates/custody-pair/`), so the claim's "committed" word closes at the
  parent's commit; the post-pair trip wire
  (`verify claims/c3/receipts/config-pre-pair-v2.txt <post>` → expected
  `MATCH 5/5 drift=0 exit 0`) is unrunnable until a post-pair lands (VZ-3 T2 and
  RV-12 C-final are the current stand-ins); pycache residues must be excluded
  from the wave-artifacts commit (D9); and the cross-chain flag D11 (census G2
  SUSPECT on the in-flight revision at untouched HEAD, SC-4 §3) belongs to C2 —
  the records commit must re-run the census after that landing settles.
