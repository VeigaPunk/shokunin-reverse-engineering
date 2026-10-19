# SEAT VZ-4 — chain cross, role wave-integrator (arc3-loop1-round2)

Wave `arc3-loop1-round2`, 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
· lane HEAD `14b1682b1128d2e41085ebc79c9addeb8786d420` at every sample (seats do not
commit; the parent integrates). Deliverables: `claims/cross/wave-summary.md` (sha256
`bba0137f7ad60d741a3f5cc9cf650f53d64044e3638522ecc23efbf6931c2093`, 344 lines — fresh
identity re-derived after the last revision, rule #14) and this report, plus evidence
under `claims/cross/VZ-4/`.

No git mutation; no custody path written, renamed, or `utime`d (read-only sha256/stat
capture only); no install; scratch `/var/tmp/vz4` and `/var/tmp/vz4/c1*` (never `/tmp`
— standing EDQUOT record). Nothing outside `claims/cross/VZ-4/*`,
`claims/cross/wave-summary.md` and `seats/VZ-4.md` was written by this seat.

## 1. Work performed (evidence pointers)

**Polling (seat line: every 60 s, max 30 checks).** Two independent pollers plus
direct listings:

- 60 s poller of `seats/`: `claims/cross/VZ-4/poll-log.txt` — checks 1–21,
  12:00:41Z → 12:20:41Z (0 → 54 seat reports). **The poller process terminated at
  check 21 without its `POLL DONE` marker** (`/var/tmp/vz4/poll.log` has 21 `poll=`
  lines, no trailer) — reported as observed, not smoothed over.
- 30 s watcher of the real targets + seat count: `claims/cross/VZ-4/watch-log.txt` —
  52 samples 12:04:01Z → 12:29:32Z, continuous through the poller's death; this is the
  record that shows the census sha moving and the seat count rising 0 → 63.
- Closing poller 12:30→12:33Z (`/var/tmp/vz4/close-poll.log`).
- ~25 additional direct `ls seats/` listings between samples. Combined, the seats dir
  was observed more than 30 times across 12:00→12:30Z, including the rising phase and
  the close.

**Mechanical census (not hand-counted).** `claims/cross/VZ-4/roster-census.py` parses
the frozen roster out of `claims-frozen.md:84-96` (12+30+18+4 = 64) and diffs it
against `seats/`, reporting per-chain delivered/undelivered, strays and zero-byte
files. Closing result: **64/64** — C1 12/12, C2 30/30, C3 18/18, Cross 4/4 (the
closing poller `close-poll-log.txt` shows 63 at 12:30:09Z → 64 at 12:31:09Z when this
seat's own report landed; the 12:27Z census that drafted `wave-summary.md` §1 read
63/64 with VZ-4 outstanding). No strays, no empty reports. Note (correction): CN-1's
seat report *does* exist (`seats/CN-1.md`, 12:20Z, status COMPLETE) — an earlier
draft of this report inferred otherwise from a stale listing; the closing census
reads 64/64 with all four cross seats present.

**First-hand re-verification of all three chains** (own harnesses, bound to sha256):

| Harness | Target | Key outputs (paths under `claims/cross/VZ-4/`) |
|---|---|---|
| `commandA.sh` | command A at HEAD | `commandA-before.txt`: `rule_blocks 13, resolved 13, 82/82, 10.0/10.0` |
| `c1-rulecheck.py` | per-rule citation resolution + block hashes | `c1-rules-before.txt` (13 rules, 13 resolved) |
| `c1-verify.sh` | EX-01's rule-#14 patch, applied to scratch | `c1-verify-out-v3.txt`: payload `6cc388cb…`/1,071 B ✓, patched SKILL.md 387 L `a8170b96…` ✓ (matches EX-01's claim), lines 1–239 byte-identical, rules 13→14 and 13→14 resolved, census PASS `lines=371→387, loci=2` |
| `c2-verify.sh` | census revisions, round-1 injections | `c2-verify-before.txt` (both silent PASS at `6f1d19ff…`), `c2-verify-after-snap1.txt` (at `82fb807e…`), `c2-verify-after-snap2-blockunit.txt` (**over-fail caught at `c95a5cf3…`**), `c2-verify-closing-final.txt` (all clauses at `d0772ce8…`) |
| `c3-attacks.sh` | custody-pair at `112d01dc…` | `c3-attacks-out.txt`, `c3-selftest.txt` (15/15 CLEAN), `c3-capture-frozen-112d01dc.txt`, `c3-capture-post-vz4.txt` |
| `custody-capture.sh` | 5 custody paths, stat+sha | `custody-pre.txt` (12:01:47Z) |
| VZ-4 fixed-variant build | C1 landing candidate | `c1fix` scratch: payload 1,118 B `6a483c84…` → 388 L `47505059…`, 14/14 resolved, census PASS `lines=371→388` |

## 2. Proposed changes (patch-text paths)

**None authored by this seat** — the integrator role produced no patch text of its
own; the wave's patch texts are the chains' (`claims/c1/*/*.patch.md`,
`claims/c2/*/*.patch.md`, `claims/c3/*/*.patch.md`). The parent-facing landing
instructions are consolidated in `claims/cross/wave-summary.md` §4, the load-bearing
one being: **C1 must land a form-fixed payload, not EX-01 rev B verbatim** (VZ-1's
blocking condition, re-verified at source here: rev B's payload line 15 cites
`` `SCORECARD.md:1366-1368` `` bare).

## 3. Before→after measurement (cross-chain / wave level)

Cross carries no frozen claim of its own; the wave-level before→after is the seats
census and the three chains' instruments.

```
before  seats delivered = 0/64        (12:00:41Z, poll=1)
after   seats delivered = 64/64       (12:31:09Z, close-poll; this seat's report closes it)
        at 12:29:32Z the count was 63/64 with only VZ-4 outstanding
```

Shared-instrument before→after at VZ-4's hand (identical inputs, so no chain can have
moved another's numbers):

| Instrument | before | after |
|---|---|---|
| command A (`commandA.sh`, REV=`14b1682b`) | `13/13, 82/82, 10.0/10.0` | unchanged — SKILL.md is unpatched at close; the 14/14 state exists only as verified projections (§C1 of the summary) |
| census (`c1-census-v10.py`) | `PASS 0/0/0/0` (`6f1d19ff…`, 490 L) | `PASS 0/0/0/0` (`d0772ce8…`, 610 L) — same verdict, new classes armed |
| custody receipts | round-1 v1 (label defect) | v2 (`112d01dc…`): label correct, inode/ctime pinned, same 5 digests |

## 4. Attacks / refutations attempted (verdicts)

| # | Attack | Verdict | Receipt |
|---|---|---|---|
| A1 | C2 premise: absent SKILL.md at round-1 v10 | **CONFIRMED silent PASS exit 0** | `c2-verify-before.txt` |
| A2 | C2 premise: neutered needles at v10 | **CONFIRMED silent PASS** | `c2-verify-before.txt` |
| A3 | C2 after-state at the landed revision | **CLAUSES HOLD** (HEAD PASS; H1 → `UNREADABLE`; H3 → `G2 SUSPECT`) | `c2-verify-closing-final.txt` |
| A4 | C2 intermediate revision `c95a5cf3…` (block-unit floor) | **REFUTED as shippable — ordinary HEAD run FAILs** (SKILL.md has 0 current-ok *blocks*); caught in flight, fixed downstream, re-verified PASS | `c2-verify-after-snap2-blockunit.txt` |
| A5 | C2 creep audit | **REFUTED** — 20 rows, 0 added/removed/changed, CREEP FLAGS [] | `c2-verify-closing-final.txt` |
| A6 | C2 H2 boundary (fabricated `9.9.9` pin + inline marker at the landed revision) | **CONFIRMED still open** (`PASS`, `historical (inline marker)`) — named residual | §C2 caveat 3 of the summary |
| A7 | C3 same-content in-place rewrite (scratch) | **DETECTED** `REWRITE-DRIFT exit 11`; content sha identical — sha-only custody provably blind | `c3-attacks-out.txt` A |
| A8 | C3 rename-swap with mtime restored | **DETECTED** (`moved=inode,mtime_ns`) | `c3-attacks-out.txt` B |
| A9 | C3 v1 receipt unverifiable by the v2 tool | **REFUTED** — `SHA256-CONTRACT 5/5` + 5× `LABEL-DEFECT` on round-1's canonical receipt | `c3-attacks-out.txt` C |
| A10 | C3 UTC render is localtime in disguise (the v1 defect repeated) | **REFUTED** — independent `gmtime` re-derivation, 0 mismatches on 5/5 paths | `c3-attacks-out.txt` D |
| A11 | C3 write-guard covers everything it measures | **REFUTED (scoped)**: the canonical 5 are protected; `capture --out X --paths X` clobbers X (scratch demo). Recommendation filed, not a claim failure | `c3-attacks-out.txt` F |
| A12 | C1 patch identity claims | **REPRODUCED exactly** (payload + patched-file identities); prior-rule bytes identical; 14/14 resolvable. My first harness run *dropped the payload's trailing newline* and appeared to mismatch — **my artifact, fixed**, not EX-01's error | `c1-verify-out-v3.txt` |
| A13 | C1 citation FORM (rule #11: no bare line numbers) | **REFUTED for rev B** at source: payload line 15 cites `SCORECARD.md:1366-1368` bare → rev B must not land verbatim; my own form-fixed variant lands clean (388 L, 14/14, 0 flags) | summary §C1 caveat 3; `c1fix` scratch |
| A14 | Custody drift across the wave | **REFUTED** — two independent pairs MATCH 5/5 exit 0 (EX-31's, mine 12:10→12:20Z); digests equal round 1 | `c3-capture-post-vz4.txt` |
| A15 | "The wave's after-states are asserted, not measured" | **REFUTED for all three chains by this seat's own runs** (C1 projection, C2 landed bytes, C3 frozen revision) | the six harness outputs above |

## 5. Blockers

None for this seat's deliverables; the summary and report are written. Items the
parent must handle (all named in `claims/cross/wave-summary.md` §4/§7):

1. **Three real targets are uncommitted**: `.ufo/gates/c1-census-v10.py` (`d0772ce8…`),
   `.ufo/gates/custody-pair/{custody-pair.py,README.md}` (`112d01dc…`/`fa484d57…`).
   SKILL.md is untouched (patch-text landings only).
2. **C1's landing must use a form-fixed payload** (VZ-1's blocking condition), plus
   `SHONEN.md:6` refresh and the C1 records drafts; then command A at the records
   commit.
3. **CN-1 delivered** (`seats/CN-1.md` + `claims/cross/consistency.md`); its four
   ranked flags are folded into the summary (F1 revision churn in C2 records, F2/C1
   citation-form, F3/C1↔SHONEN same-commit coupling, F4/C3 v1-exit-12 wording).
   **CU-1/EX-32's post-pair section** remains formally pending (materially verified).
4. **Process hygiene observed by this seat** (not blockers, recorded for the round):
   my 60 s poller died at check 21; the census file was rewritten 8+ times inside the
   wave and custody-pair 5 times, so every pin recorded mid-wave (including the two
   chain verdicts' earlier pins) is stale by construction — re-derive at landing.
   Two untracked `__pycache__` dirs under `.ufo/gates/` must be excluded from the
   commit, and `.ufo/waves/arc2-loop1-round10/C3.md` was already dirty pre-wave.
