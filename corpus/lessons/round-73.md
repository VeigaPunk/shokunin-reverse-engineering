# Round 73 — the kernel's record, the record audit, and the reader-seam battery

author: KaidokuR73 (L1), lane kaidoku-shokunin
round: 73, attempt 1
base: `05bf065684e52d72ea25aad95f7acb71fcd7874c`
declaration: `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b` (six instruments + the plan + the
census-start receipt); instrument fix `d36c6ee00122e9c991d7c8efc2e179dc0a10d9ed`; hardening
`55cac1d2ea38bf3cf0c96525268471c1f9f715ff`; container corrections `73b29fdb…`
freeze: `8b928422b51e2f03039ab365f7bafa838389c6d2` (the first commit adding `claims.json`; the
round-29 gate audits it **FLAGGED** on `INSTRUMENT_PIN_MISMATCH` — see M73-3)
landing: the round-73 record commit; the measured receipts are
`.ufo/waves/round-73/l1/scores/*.json` and the wave evidence is `.ufo/waves/round-73/w1/`

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| **A witness claim named its producer's channel and called the gap a boundary** — round 72's A11 read the shim's own dump and the checker's own log; both are claims, so a shim that writes a clean four-key dump under the caller's 275-key environment satisfies every clause. The round-72 entry recorded that as "a class boundary", i.e. as a fact about wrappers rather than a missing channel. | `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md` (Limits); round-72 `MutReaders`/`CriticClaims`; the round-73 base world: `pre/c1-at-base.json` (the probe cannot see `/proc`) and `ExecC1Base`'s `a11-forged-world.json` (a fabricated dump passes `a11_verdict`). | none at the time — QUALITY 123/125 bound a capture claim to *which* children and *whether the summary is the witness*, but no row required the witness to be producer-independent or named its channel. | A12 (`kernel_witness`, `a12_verdict`) with an in-arm forged control; QUALITY 129; the knowledge entry's channel table. |
| **A frozen before-arm named a comparator the instrument could not produce** — the plan said "the same probe against `--tool tools/round-72/packed-elf.py` reports 11 of 12"; measured, it reports 8 of 12, because the route receipt is bound to the round-73 producer and the round-72 route rejects it (A2/A10/A11 false as well). A12 cannot be a route-differential at all: it measures the probe and passes whenever the genuine sub-run's checker accepts the receipt. | `pre/c1-at-base.json` (8/12); erratum 1 in `.ufo/waves/round-73/claims.json`; `pre/c1-at-base-r72probe.json` (the round-72 probe: 11 arms, 11 passed). | none at freeze — the plan's base-arm sentence had no receipt of its own and no control that ran it before the freeze; the freeze gate checks pins, not comparators. | erratum 1 discloses the measured 8/12 and re-stipulates the base arm at the probe level before any landing data; QUALITY 132. |
| **The freeze pinned two producer digests that are not the blobs at the freeze** — `loaded_by_counter` named `973d504b…` for `tools/round-72/packed-elf.py` and `7f46e3ef…` for `tools/round-72/seam-probe.py`; the blobs are `330ecf89…` and `602b305d…` (the latter is the very value routed defect 1 was about). The freeze gate reports `INSTRUMENT_PIN_MISMATCH` and reads pins from the freeze commit, so the finding is permanent for this freeze. | `.ufo/waves/round-73/l1/scores/gate-at-freeze.json`; `gate-at-record.json`; ledger row `round-73 FLAGGED INSTRUMENT_PIN_MISMATCH`; erratum 3. | the gate itself, at the record run — but after the freeze, so it could only flag, not repair. | pins corrected at the record revision and the finding recorded in the ledger and this table; planned item (d): pin producers from the blobs at the freeze, verified before the freeze commit (QUALITY 130). |
| **A mutation patch site named the pre-supersession bytes** — the `r73base` implicit-capsule patch was written against the round-72 *freeze* block and matched 0 times at the measured revision; `b` (readelf) was written at the call site, which a case that calls the seam cannot exercise; and the two seam cases shared one `seen` file, so dropping the git reader's env made the readelf case carry the failure. | `pre/c3-at-base.json` (the pre-fix run was `unevaluable`), `ExecC3` and `MutBattery` seat reports, supersession entries at `d36c6ee0`. | the battery's `Unevaluable` (fail-closed) for the first; the seats for the other two. | patch sites re-derived at the measured revision; the readelf mutation moved into the seam body; per-seam record files. |

## Gate — sources opened this round

| row | URL | opened | quote (≤25 words) | snapshot |
|---|---|---|---|---|
| S277 | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | 2026-11-04, HTTP 200 | "Think of this file as the command line that the process wants you to see." (15 words, end of DESCRIPTION) | 7 918 B, sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`; man-pages 6.19 splits `proc(5)`, and `proc_cmdline(5)` is the kernel's own boot command line — not this page |

S277 is the round's sourced claim (R73-C1 cites it through
`corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`). S275 (proc_pid_environ) was opened
in round 72 and is cited, not re-registered. ScoutSource independently resolved the `proc(5)`
split and fetched the index page.

## What the wave found

- **SentinelScope** (blocking, fixed in-round, supersession `55cac1d2`): the kernel poller
  selected by argv alone (a decoy elsewhere on the host could be sampled), the Perl shims
  interpolated scratch paths into source (a quote or newline in a path would be code), and the
  sample record kept HOME/TMPDIR *values* (QUALITY 128's key-census rule). Fixes: ancestry
  guard (`_descends_from`), sidecar `<shim>.cfg`, booleans only.
- **CriticClaims** (real, fixed): a clean *decoy* process satisfies a name-only selector (the
  ancestry guard is the fix), and D1 accepted a correction that repeated only the wrong token
  (the atom now requires the measured digest in the correction block). Its four "wrong
  implementations pass all 38 selftests" mutants are routed (planned item (a)/(c)).
- **MutProbe** (real, routed): ten A12 mutants, four killed, six survivors — dropping
  `forged_detected`, `lie_clean`, the canary or the genuine-rc conjunct leaves the selftest
  green. Named debt, one case per conjunct next round.
- **MutBattery / ExecC3** (pre-fix measurements): both measured the *declaration* instruments
  and correctly reported the defects the fix `d36c6ee0` closes (readelf survivor, wrong-case
  kill, stale `r73base` anchor). Their reports are retained as the pre-fix record.
- **ExecSweep** independently reproduced the pre-fix numbers and the receipt-rebinding trap
  (declaration probe 11/12 with A2 false; base probe 8/12; audit 6 both sides).
- **ExecC2** independently re-derived all seven atoms and flagged D7 as semantically
  false-green (it does not check the report/SCORECARD pointer disagreement) — routed.
- **ExecC1Verify** built its own observer and reproduced both worlds: clean genuine samples,
  and a forged run whose dump is clean while the kernel census is dirty (its own sampling of
  pid 1532214/ppid 1532213).
- **ExecC1Base** measured the base boundary: zero kernel reads in the round-72 probe, a
  fabricated A11 world passing, and the 11-arm target.
- **ScoutSource** resolved the `proc(5)` split and produced the S277 row and snapshot.
- **ConnectorCross** found sibling owners for the surfaces (kama's external environ observer,
  chousa's record audit, mado's recorded/measured reconciliation) and proposes a provenance
  crosswalk; no absorption.
- **ScribeKnowledge / ScribeLesson / ScribeRecord** drafted the entry, lesson and record
  fragments; the L1 rewrote them against the post-fix facts.

## Non-author closure

`[L1 — filled by the non-author closure.]`
