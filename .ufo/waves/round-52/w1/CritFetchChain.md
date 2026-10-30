# CritFetchChain — round 52 wave r52-w1 (attempt 1) — carrier re-fetch chain attack

Seat: CritFetchChain (critic). Role: attacker of the carrier re-fetch chain design.
Scope: `tools/round-50/fetch-vendor.py`, `tools/round-50/carriers.json`,
`plans/round-52-claims.md` data-run bullet (lines 154-160) and routed defect 4
(lines 248-251); the consumer side `tools/round-50/c1-counter.py`
(`--carrier-cache` read at 2239-2243, `carrier_fresh_ok` at 2250).
Full findings with numbered severities: `.ufo/waves/round-52/w1/CritFetchChain/findings.md`.

## Verdict

**The chain's hash discipline is sound, but the chain is NOT fail-closed in the
sense the claims assert.** Eight findings: 3 HIGH, 3 MEDIUM, 2 LOW. The two
that must be fixed before the round-52 freeze are F2 and F3 (the data run can be
green without the vendor ever being contacted) and F1 (routed defect 4 is not
actually satisfied by the file it names).

## What holds (F0 — measured, not assumed)

* **Image sha256 IS verified before member extraction.** With a wrong
  `image_sha256` and a perfectly valid tar, the run exits 1 with
  `link=image_sha256` and `tar_member` is called **0 times**. So an AVM
  re-publish of a changed image fails closed before any member is read — this is
  the question the task asked, and the answer is *yes, correctly ordered*.
* **Each hash link is genuinely able to fail and is genuinely covered.** Mutants
  that delete the image-sha / member-sha / carrier-pin comparison each turn the
  selftest red (15/16, 15/16, 14/16).
* **The member extraction needs no privilege and cannot hit device nodes.**
  `tar_member()` reads one regular member in memory via
  `tf.extractfile(m).read()`; there is no `extractall`, no `extract`, no `mknod`,
  no fifo, no disk write. A synthetic tar containing a `CHRTYPE` and a `FIFOTYPE`
  member: both `isfile()==False`, both skipped. The SquashFS is never extracted
  by the fetcher at all — only carved as bytes. (The device-node question belongs
  to the counter's `unsquashfs -lln` oracle arm, not to this chain.)
* **All four vendor images are live and byte-identical to the frozen pins as of
  2026-10-30T11:09:30Z** (HTTP 200; observed `Last-Modified`/`ETag` equal the
  `notes` values pinned per carrier in `carriers.json`). The round-52 data run is
  feasible; vendor drift is real but currently dormant.
  Receipt: `.ufo/waves/round-52/w1/CritFetchChain/vendor-liveness-receipt.json`.

## The three findings the L1 must act on

**F2 (HIGH) — a stale `<pin>.bin` survives a failed re-fetch and the counter
reads it as a fresh carrier.** Measured: after a successful fetch, a *second*
fetch into the same cache dir that fails at `member_sha256` (upstream member
changed) leaves the previous `<pin>.bin` in place, still sha-correct against the
pin. The counter reads exactly that file and checks only `carrier_present` (file
exists) and `carrier_pin_ok` (sha matches) — both true for the stale file. It
reads **no** fetch receipt, no mtime, no run id. This is fatal for round 52
specifically because the claims waive `carrier_fresh_ok` for exactly these four
pins (`re_scored_pins`), so the one clause doing anti-replay work is disabled
and nothing else binds the bytes to *this* run's fetch. **Correction:** remove
the stale entry on any broken link; make the counter read a committed per-run
fetch receipt and require `fetch == 'http <status>'`; bind the receipt to the
bytes with a UTC time and the observed `Last-Modified`/`ETag` (the pinned
`notes` already carry the expected values, so the comparison is available).

**F3 (HIGH) — `--image-cache` satisfies the whole chain with zero network
contact.** Measured with the HTTP opener booby-trapped to raise on any access:
`rc=0, ok=True, fetch='cache'`. `fetch()` returns early from the image cache
when `sha256(cached) == want`, and because the cache is keyed by the *expected*
image sha256 it is self-verifying — which is exactly why it is dangerous: the
only signal that the vendor was not contacted is the `fetch` field of a receipt
that nothing reads. **Correction:** record the fetch mode per carrier and
require `http <status>` on the data-run path (or drop `--image-cache` for it;
the round-52 cache dir is new, so it costs nothing).

**F1 (HIGH) — routed defect 4 is not satisfied by the file it names.** The
round-50 selftest never calls `fetch()`'s guard or the redirect handler: every
case routes through the `fake` fetcher, and the `'bad-url'` case relies on the
*fake* raising. Measured mutants: deleting the https+host guard → selftest
**rc=0, 16/16 pass**; deleting the redirect guard → **rc=0, 16/16 pass**;
deleting both → **rc=0, 16/16 pass**. The routed defect requires *guard deleted
→ selftest red*. A verbatim port would attest to a property it cannot test.
**Correction:** add offline cases that invoke the real `fetch()` guard and
`_AvmOnlyRedirect.redirect_request` with fixture URLs and assert refusal — not
through the `fake` fetcher.

## Also worth the L1's attention

* **F4 (MEDIUM)** the guard checks *hostname*, so `https://download.avm.de:8443/x`
  and userinfo URLs pass — in the initial-URL guard **and** the redirect guard
  (same predicate). The opener's handler list contains `_AvmOnlyRedirect` and no
  default `HTTPRedirectHandler`, so this is the only origin control in the
  chain. Fix: compare netloc (host+port), reject userinfo, and use one shared
  predicate for both guards so they cannot drift apart again.
* **F5 (MEDIUM)** one unreadable carrier raises an uncaught `tarfile.ReadError`
  out of `run()`: no `--json-out` receipt at all, no per-carrier `link=`, and a
  **partial cache dir** left behind (carrier A written before carrier B aborted).
  The L1 would get a traceback instead of a receipt and could not tell "AVM
  republished one carrier" from "my tool crashed". Fix: catch `tarfile.TarError`
  in `tar_member()` and return the existing `link=` shape.
* **F8 (MEDIUM)** the claims reference "the round-52 carrier table" (line 80)
  but **never name it as a file**, while both the fetcher
  (`CARRIERS = 'tools/round-50/carriers.json'`) and the counter
  (`c1-counter.py:374`) hard-code the round-50 path — which the claims also say
  must *join* `PRIOR_CARRIER_TABLES`. Two authorities on one table. The claims'
  Registry clause ("no other code files land under `tools/round-52/`") makes the
  omission consequential: the porting seat will guess a path. Fix: name the
  file, give it a registry row, point both instruments at it.
* **F6 (LOW)** the `<pin>.bin.part` write follows a pre-planted symlink — the
  victim file's contents were overwritten by the carrier bytes in the probe.
  Low severity (the cache dir is under `/fast/scratch`, L1-created) but it sits
  exactly where the claims harden the cache path. Fix: `os.open(..., O_CREAT|
  O_EXCL|O_NOFOLLOW)`.
* **F7 (LOW)** a carrier without an `external` key is silently dropped and the
  run still exits 0 (`carriers_in_spec=2 recs_emitted=1 rc=0`). Relevant because
  a round-52 carrier table is being authored this round. Fix: assert the
  materialised count/ids match the spec.

## Note on the "round-50 cache no longer exists" premise

The claims' provenance says the round-50 cache was removed by the run-11
sweep. That is true of the carrier-cache *directory*
(`/fast/scratch/hyaku/kaidoku-r50/carrier-cache` is gone) but **not** of the
symlink farm: `/fast/scratch/hyaku/kaidoku-r50/controls-work/cache-c{1,2,3,4}/`
still hold four symlinks each named exactly `<pin>.bin`, pointing at the removed
directory. They are currently dangling (verified for all four pins in all four
dirs), so they serve no bytes today — but they are a repopulation hazard under
the exact `<pin>.bin` names the counter reads, and the round-52 cache dir the
claims name does not exist yet. The sweep should remove the symlinks too.

## Impacted axes

F1, F2, F3, F4, F6, F8 → **honesty** (a green receipt must mean the guard ran
and the bytes came from the vendor this round). F5, F7 → **depth** (the chain
must diagnose *which* carrier broke, not abort or drop silently). None of these
touch the device-accounting law: F0 confirms the fetcher never extracts a
filesystem, so it never creates a device node and needs no privilege.

**Do not narrow the claim.** F2/F3 mean a round-52 data run can report
`carriers_matched == 4` without contacting download.avm.de once. That is a
defect in the *chain*, repairable inside `tools/round-52/fetch-vendor.py` plus
one counter clause — not a tradeoff to accept. The claims' own promise ("no
cached byte is trusted without its pin") is not kept by the current code, and
the `re_scored_pins` waiver removes the clause that was doing the anti-replay
work.

## Evidence (all receipts carry command, exit code, stdout sha256, UTC time)

Seat dir `.ufo/waves/round-52/w1/CritFetchChain/`:
`findings.md` (numbered findings + severities + corrections),
`probe-evidence.py` (P1, MUT-A/B/C, P4, P5, P6, P7, P8, P9, P10),
`probe-evidence-2.py` (P3 corrected, P7/P11 corrected),
`probe-guard-predicate.py`, `probe-results.json`, `probe-results-2.json`,
`vendor-liveness-receipt.json`.

All probes offline (no network) except the four live GETs in the liveness
receipt, which used only the URLs already pinned in `carriers.json`
(ALLOWED_HOST `download.avm.de`); the bytes were hashed and discarded, never
copied into the lane tree. No REA run was invoked. No lane file was modified,
staged or committed; the only writes are this seat directory and this report.
Tooling: none installed, none upgraded (no tool was needed).
