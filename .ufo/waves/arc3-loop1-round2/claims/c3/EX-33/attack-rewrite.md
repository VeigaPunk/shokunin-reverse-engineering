# EX-33 — same-content-rewrite attack on custody receipt v2

Seat EX-33 · chain c3 · role adversary-executor · wave arc3-loop1-round2 · 2026-10-19.
Task (seat line): on SCRATCH copies under `/var/tmp` — create file, capture v2
receipt, rewrite identical bytes (new inode), verify the v2 verify-mode flags the
drift where sha256 alone cannot; document precisely what is and is not detected.

Chain claim under attack (frozen, `.ufo/waves/arc3-loop1-round2/claims-frozen.md:52-64`):
a live same-content rewrite of a custody path is detected (inode/ctime movement).

**Verdict: the v2 instrument detects every same-content rewrite form this seat
constructed (6 forms, one class each), while sha256-only comparison is silent on
all six; the detection is carried by `inode` / `mtime_ns` / `ctime_ns`, and in the
forged-mtime case by `ctime_ns` alone. Two scope boundaries are measured and named:
receipt self-integrity is not authenticated by `verify` (tampered receipt → MATCH),
and a whole-second time format is blind to a same-second in-place rewrite (the v2
tool's ns fields close this). One operability nit (selftest `--scratch` must exist)
and one compatibility fact (a v1 receipt verifies on sha256 5/5 but verdicts
`METADATA-DRIFT` exit 12 with declared LABEL-DEFECT, not a silent pass).**

## 0. Tool pin (and a mid-session revision)

| | |
|---|---|
| target | `.ufo/gates/custody-pair/custody-pair.py` (chain c3's real target; this seat read/exec only) |
| pinned revision | sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, 39157 bytes, mtime 2026-10-19 09:05:19.448 -0300 |
| earlier revision observed | sha256 `72d5231f7cfc52628f214e03f6ba80d33acff75a87db8ead8939bddd5bd5c5d0` (38651 bytes) at 12:04:40Z; superseded before the ladder ran |
| revision evidence | every receipt the tool writes embeds its own hash; all 13 receipts captured this session carry `# tool: custody-pair.py  sha256 112d01dc…` (one revision throughout the ladder) |

The tool edits itself live (EX-31 working concurrently before its seat report);
this artifact pins one revision and states it, per the chain's own rule.

## 1. Method

Two instruments, same attack matrix:

- **Reference harness** `/var/tmp/arc3-l1r2-EX-33/v2ref.py` (scratch, not the chain
  target) — capture/verify with the v2 field model (sha256 + mtime epoch/UTC +
  inode + ctime), plus a `--sec` variant that stores whole-second times only, to
  measure the granularity boundary.
- **Real tool** `custody-pair.py capture --out … --paths …` / `verify … --live`
  and receipt-to-receipt `verify A B`, on scratch fixtures under
  `/var/tmp/arc3-l1r2-EX-33/real/`.

No custody path was written, touched, or copied; the only reads of the real
custody paths in this seat are `sha256sum`/`stat` (hash/stat capture, §5).

## 2. Attack matrix — real tool (revision 112d01dc)

Payload is 24 bytes, identical in pre- and post-rewrite states; every rewrite is
"same content, same size, sha256 unchanged"; `sha256-alone` is what a v1-style
sha-only comparison sees.

| # | rewrite form | sha256-alone | tool finding | moved= | exit |
|---|---|---|---|---|---|
| R-A | control, no rewrite | silent | MATCH | — | 0 |
| R-B | in-place truncate+write (same inode) | **silent** | REWRITE-DRIFT | mtime_ns,mtime_epoch | 11 |
| R-B2 | in-place + forged mtime back (`touch -d @old`) | **silent** | REWRITE-DRIFT | ctime_ns | 11 |
| R-C | rename-over (new inode) + forged mtime | **silent** | REWRITE-DRIFT | inode | 11 |
| R-C2 | `ln -f` hardlink swap of identical bytes | **silent** | REWRITE-DRIFT | inode | 11 |
| R-E | delete + recreate + forged mtime | **silent** | REWRITE-DRIFT | inode | 11 |
| R-D | same-second in-place + forged mtime | **silent** | REWRITE-DRIFT | ctime_ns | 11 |
| R-H | receipt-to-receipt pre/post pair over an in-place rewrite | **silent** | REWRITE-DRIFT | ctime_ns | 11 |
| R-G | different bytes (control, must fire) | sha DRIFT | CONTENT-DRIFT | sha256 | 10 |
| R-I | path deleted after capture | n/a | ABSENT | exists | 13 |
| R-K | chmod-only, content untouched | silent | METADATA-DRIFT | mode,ctime_ns | 12 |

Raw outputs: `receipts/real/<case>/verify.txt` (this artifact's tree); ladder log
`logs/run-real.log`.

Mechanism, per form: an in-place rewrite moves `mtime` and (unforgeable)
`ctime`; forcing a new inode via rename/link/delete-recreate moves `inode`.
`ctime` cannot be restored by any user-space call (`utimensat` sets mtime/atime
only), so after an mtime forgery the residue is `ctime`. In R-B2 the receipt's
`ctime_epoch` equals live (same whole second) while `ctime_ns` differs — the
detection in that case rested on sub-second precision (see §3).

## 3. Boundary: whole-second time format is blind to a same-second rewrite

Reference harness, one process, rewrite provably inside the receipt's ctime second,
mtime forged back to the recorded value (so inode/sha/size/mtime all match):

```
attempt=1 SAME-SECOND confirmed: ctime 1792411443(.660339018) -> 1792411443(.676761687)
inode 10969169 -> 10969169 (unchanged: True); sha256 identical on both writes
--- --sec receipt verify (whole-second fields) ---
VERDICT: MATCH          exit=0        <- blind
--- ns receipt verify (nanosecond fields) ---
... v2-fields-changed=['CTIME_UTC']
VERDICT: DRIFT          exit=1        <- flagged
```

Same construction against the real tool: `REWRITE-DRIFT … moved=ctime_ns`, exit 11
(`receipts/real/D/`). So the `ctime_ns` field is load-bearing: a v2-shaped receipt
that stored times at whole-second granularity would silently MATCH this exact
attack. The real tool does not have that hole.

Inode-reuse probe (reference harness, delete + 200 fresh file spawns): the
pre-rewrite inode was reused **0/200** times; and even a reused inode would carry a
fresh `ctime_ns` from creation. No practical blind spot found on this filesystem.

## 4. What is NOT detected (measured where possible)

1. **Receipt tampering (MEASURED — the significant one).** After an in-place
   rewrite, this seat edited the receipt's own mtime/ctime fields to the live
   values; `verify --live` then returned **MATCH exit 0**
   (`receipts/real/J/verify-tampered.txt`). The tool does write a sidecar
   (`<receipt>.sha256`) at capture, and that sidecar *does* catch the tamper
   (`sha256sum -c j.v2.json.sha256` → `FAILED`), but `verify` never reads the
   sidecar (sidecar references in the tool: `custody-pair.py:545-577` capture-side
   and `:653-655` selftest only). Consequence for custody use: a receipt is only
   as trustworthy as its storage; an audit must run the sidecar check (or the
   receipts must be committed) before treating a MATCH as evidence. Suggested
   (not landed, patch-text-only suggestion): `verify` should check
   `<receipt_a>.sha256` when present and exit non-zero on mismatch.
2. **Between-capture activity.** capture→verify is point-in-time, not monitoring:
   a rewrite that is reverted before the verify is unobservable by construction.
3. **Root / offline attacker.** An actor who can set the system clock or rewrite
   ctime offline (e.g. `debugfs`) is outside the tool's threat model; the receipt
   is unkeyed and unsigned. Named, not tested (no root, no installs this round).
4. **Whole-second storage formats** lose §3's protection (measured on the
   reference harness; not a defect of the real tool).
5. **Benign metadata movement is indistinguishable from hostile movement** in the
   exit code: chmod-only → METADATA-DRIFT exit 12 (R-K). Not blindness — noise.

## 5. v1 compatibility and the live custody set (read-only checks)

- v1 receipt field inventory: the round-1 canonical receipt
  (`arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt`) contains
  `INODE:` 0 times, `CTIME` 0 times — v1 cannot express the rewrite pins at all.
- v1 receipt vs fresh v2 capture of the 5 custody paths:
  `SHA256-CONTRACT: 5/5 paths agree on sha256`,
  `VERDICT: METADATA-DRIFT paths=5 … exit=12`, with per-path
  `LABEL-DEFECT: MTIME_UTC says '…17:53:20' = localtime(epoch …); gmtime(epoch) is '…20:53:20'`
  (`logs/v1-vs-v2.txt`). Reading: v1 receipts **are** verifiable on the sha256
  contract, and the tool does not silently pass the v1 label defect — it declares
  it. A caller that expects exit 0 on a pristine v1 receipt should expect 12.
- Independent sha256/stat of the 5 custody paths at 12:05Z: all five sha256 match
  the round-1 receipt (no drift on the custody set).
- False-positive check: v2 receipt vs v2 receipt over the live 5 paths, ~2 minutes
  apart → `MATCH paths=5/5 exit=0`.
- Label fix confirmed on v2 output: `MTIME_EPOCH: 1792000000` →
  `MTIME_UTC_RENDER: 2026-10-14T17:46:40Z` (= gmtime(epoch)) with the local render
  recorded separately as `MTIME_LOCAL_RENDER: 2026-10-14T14:46:40-03:00`.

## 6. Tool's own teeth (independent run)

`custody-pair.py selftest` (scratch dir `/var/tmp/arc3-l1r2-EX-33/selftest`) →
`CUSTODY_PAIR_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0`
(`logs/selftest-run.txt`), including `same-content-rewrite-inplace-ctime-pin` and
`same-content-rewrite-rename-inode-pin`. This seat's ladder is the independent
reproduction plus the tamper/boundary probes the selftest does not cover.
Operability nit: with `--scratch <nonexistent>`, selftest dies with a Python
traceback (`FileNotFoundError`, `custody-pair.py:630`) and exit 1 instead of a
usage error; the scratch parent must exist.

## 7. Reproduction

```bash
# reference harness ladder (scratch)
bash /var/tmp/arc3-l1r2-EX-33/attack.sh | tee /var/tmp/arc3-l1r2-EX-33/run.log
# real-tool ladder (scratch fixtures)
bash /var/tmp/arc3-l1r2-EX-33/attack_real.sh | tee /var/tmp/arc3-l1r2-EX-33/run-real.log
# same-second boundary
python3 /var/tmp/arc3-l1r2-EX-33/same_second.py
python3 /var/tmp/arc3-l1r2-EX-33/same_second_real.py
# v1 compatibility
python3 .ufo/gates/custody-pair/custody-pair.py verify \
  .ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt \
  /var/tmp/arc3-l1r2-EX-33/custody-live.v2.json          # exit 12, sha 5/5
# selftest
python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/arc3-l1r2-EX-33/selftest
```

Evidence inventory with sha256: `manifest.sha256` (this directory). Ladder logs,
harness sources, all fixture receipts, tool pins, and the v1-compat output are
copied under this artifact directory; the scratch tree remains at
`/var/tmp/arc3-l1r2-EX-33/`.

## 8. Independent audit of the landed live pre/post pair (claim acceptance item)

Run by this seat at 12:09:26Z against `.ufo/waves/arc3-loop1-round2/claims/c3/EX-31/`
(the implementer's landing pair), tool pinned `112d01dc`; full log
`logs/ex31-pair-audit.txt`:

| check | command | result |
|---|---|---|
| tool pin consistency | headers of both receipts | both `# tool: … 112d01dc…` |
| A pair-internal | `verify capture-pre.txt capture-post.txt` | `MATCH paths=5/5 drift=0 exit=0` |
| B post vs live | `verify capture-post.txt --live` | `MATCH paths=5/5 drift=0 exit=0` |
| C sidecar self-integrity | `sha256sum -c capture-{pre,post}.txt.sha256` | both `OK` |
| D cross-seat capture agreement | `verify EX-31/capture-pre.txt RV-12/rv12-capture-A.txt` | `MATCH paths=5/5 drift=0 exit=0` |

Reading: the claim's "live pre/post pair (exit 0, 5/5)" item holds on independent
re-execution; two independently captured receipts (EX-31, RV-12) agree field-for-
field, and the receipts verify against their own sidecar digests — i.e. the pair
passes the §4.1 integrity audit that a bare MATCH does not cover.

