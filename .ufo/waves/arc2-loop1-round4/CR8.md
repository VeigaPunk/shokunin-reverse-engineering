# CR8 (critic) — provenance attack on the C2 gate artifacts

Seat CR8, wave `arc2-loop1-round4`, 2026-10-18, session window 19:04Z–19:2xZ
(`date -u` reading inline). Read-only on every repo and home file; **this report
is my only write**. Scratch: `/var/tmp/arc2-l4r4-CR8/` (moved from `/tmp` when
the tmpfs hit its per-user quota — see §2.6). No git mutation, no config edits,
no installs, no network. Every command excerpt below was run by this seat this
session.

## 0. Verdict

**CHAIN PARTIALLY TRUSTWORTHY — the byte-identity link verifies 3-way with an
independent positive control, and the five custody paths verified 5/5 at my
leg; but one committed transcript line (§5.5's landing selftest, E15.md:206)
is false against the surviving bytes, §5.2 reproduces only modulo backslash
normalization, the `landing/` copy is a divergent build, and the frozen-run
block is unenforced. The parent can land C2 from the `/tmp` root bytes, not
from `landing/`, and must re-pin at the work commit.**

The trust chain that holds: E15.md:232-235 pins four sha256 digests → the
`/tmp/arc2-l3r3-E15/` root bytes verify 4/4 against them → six *independent*
seat copies (E17 and CR7 in round 3; E17, R2, R5, R6 in round 4) hash
identically → the gate's live run at `679af5d` reproduces §5.2's finding set
10/10 → and the snapshot digest pin is *enforced*: a tampered snapshot yields
`snapshot_tampered … exit=2`, reproducing E15.md:186-187. What breaks the chain:
`landing/` diverges (two of four files), and E15.md:206's committed transcript
for that copy is not reproducible from the surviving bytes.

## 1. What I verified (the chain that holds)

### 1.1 The four pins vs the root bytes — 4/4

```
$ sha256sum /tmp/arc2-l3r3-E15/citation-drift-gate.py /tmp/arc2-l3r3-E15/pointer-table.json \
            /tmp/arc2-l3r3-E15/expected.json /tmp/arc2-l3r3-E15/config-toml-landmarks
0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f  citation-drift-gate.py
d7bf0eb340a652950fb49a5cb5e62adc4c3e7097376bdd45dbaa0ecd23db059b  pointer-table.json
6ebada28259262da835c8371b9bfccfcebe4500c22fdd19716933a62fbca1beb  expected.json
387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154  config-toml-landmarks
```

These equal `.ufo/waves/arc2-loop1-round3/E15.md:232-235` byte-for-byte (same
run read back: `sed -n '232,235p'`). Line counts 415/169/26/3322 also match.

### 1.2 Independent copies — 8 locations, one hash

I hashed every surviving copy of the gate this session:

```
0c5350b1…  /tmp/arc2-l3r3-E15/citation-drift-gate.py            (root)
0c5350b1…  /tmp/arc2-l3r3-E17-verify/citation-drift-gate.py     (E17's copy, mtime 15:07)
0c5350b1…  /tmp/arc2-l3r3-CR7-gate.py                           (CR7's copy, mtime 15:16)
0c5350b1…  /tmp/arc2-l4r4-E17/citation-drift-gate.py            (round-4 E17)
0c5350b1…  /tmp/arc2-l4r4-R2/gate/citation-drift-gate.py        (round-4 R2)
0c5350b1…  /tmp/arc2-l4r4-R5/citation-drift-gate.py             (round-4 R5)
0c5350b1…  /tmp/arc2-l4r4-R6-work/citation-drift-gate.py        (round-4 R6, ×2 incl. snap-tamper/)
1e4a734d…  /tmp/arc2-l3r3-E15/landing/.ufo/…/gate/citation-drift-gate.py   ← divergent
```

E17's copy additionally matches all four pins
(`/tmp/arc2-l3r3-E17-verify/{pointer-table.json,expected.json,config-toml-landmarks}`
= d7bf0eb3…, 6ebada28…, 387e1f08…). This is the strongest available provenance
link: six independent copies across four seats and two rounds, taken at
different times (15:07 → 19:xx), all landing on the same digest. Committed
corroboration:
`.ufo/waves/arc2-loop1-round3/E17.md:179-199` (its own reproduction),
`.ufo/waves/arc2-loop1-round3/V2.md:119-125` (four-hash re-run),
`.ufo/waves/arc2-loop1-round3/CR7.md:235-243`,
`.ufo/waves/arc2-loop1-round4/S1.md:92-100`,
`.ufo/waves/arc2-loop1-round4/E22.md:254-258`,
`.ufo/waves/arc2-loop1-round4/E20.md:267-269`.

### 1.3 Positive control — the pin actually fires

A one-byte append to a copy of the snapshot (`tamperdir/`, digest 091c23c5…)
produces, verbatim:

```
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . --rev 158a966 \
    --table …/pointer-table.json --expected …/expected.json --snapshot-dir …/tamperdir
CITATION_DRIFT: snapshot_tampered entry=@config-toml-landmarks sha256 091c23c5… != pinned 387e1f08…
CITATION_DRIFT_VERDICT: could-not-evaluate findings=11 exit=2
```

This reproduces E15.md:186-187 (the report abbreviates the hashes with `…`;
the prefixes match my full digests). So the digest comparison is live, not
decorative. The `unpinned_legacy` branch also exists at
`/tmp/arc2-l3r3-E15/citation-drift-gate.py:141-146`.

### 1.4 Live run at `679af5d` — finding set reproduces 10/10

```
$ python3 /tmp/arc2-l3r3-E15/citation-drift-gate.py --root . \
    --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f \
    --table /tmp/arc2-l3r3-E15/pointer-table.json \
    --expected /tmp/arc2-l3r3-E15/expected.json --snapshot-dir /tmp/arc2-l3r3-E15
CITATION_DRIFT_VERDICT: failed findings=10 exit=1        (9 citation_dead + 1 citation_historical_ok)
```

After normalizing backslash escaping (`s/\\\\/\\/g`; see §2.2), the sorted
finding sets of my run and `E15.md:144-154` are **identical, 10/10**
(`diff` empty). Selftest at the root bytes: `CLEAN cases=10 passed=10 failed=0
exit=0` (E15.md:132). The `no --snapshot-dir` path: `findings=11 exit=2`
(E15.md:188-189). All three entry classes behave as declared.

### 1.5 The snapshot still matches the live config today

```
$ grep -n . config-toml-landmarks | sed … | sha256sum        → 3c44c0ed…
$ awk 'NR==3296||3297||3298||3299||3301||3302||3303' ~/.kimi-code/config.toml | sha256sum → 3c44c0ed…
FIDELITY-MATCH   (7 non-blank snapshot lines == 7 live lines; config.toml = 3322 lines)
```

So the snapshot's line-number fidelity claim holds against the live operator
file at this session's position — the numbers in it are not stale. Secret scan
re-run: `grep -icE 'token|key|secret|oauth|password|api' config-toml-landmarks`
→ `0`.

### 1.6 Custody receipt at my leg

`.ufo/waves/arc2-loop1-round4/receipts/config-pre-pair.txt` (stamp
`2026-10-18T19:03:02Z`, 6 lines, 5 hash lines): `tail -n +2 … | sha256sum -c -`
→ **5/5 OK, rc=0**; self-hash `231edd7d83cdfe7787e91d8b6f672f89551a6fe50013df23a5421f5ffadafc62`
(matches E23.md:57 and V3.md:7). I ran no REA probe, so nothing from this seat
wrote to any custody path.

## 2. The holes

### 2.1 The `landing/` copy is a divergent build — and its committed transcript is false

```
$ sha256sum /tmp/arc2-l3r3-E15/landing/.ufo/waves/arc2-loop1-round3/gate/*
1e4a734d58a6db6035278e47264579fce9f0f9927fafa45c1fc33bfed63f7438  citation-drift-gate.py   (406 lines)
62b59166289823865067964c2816d3e9d552a05da14fa3e14064480bff6fe51c  expected.json            ( 25 lines)
d7bf0eb340a652950fb49a5cb5e62adc4c3e7097376bdd45dbaa0ecd23db059b  pointer-table.json       (169 lines)   ← matches
387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154  frozen/config-toml-landmarks        ← matches
```

The gate diff removes exactly the `no_snapshot_dir` handling (`:129-133`) and
its selftest case (`:323-326`, `:376-377`). The landing `expected.json` has 9
selftest cases vs the root's 10 (`no_snapshot_dir` missing). Consequences,
both re-measured this session:

```
$ python3 "$L/gate/citation-drift-gate.py" --selftest --expected "$L/gate/expected.json"
CITATION_DRIFT_SELFTEST: CLEAN cases=9 passed=9 failed=0 exit=0     ← E15.md:206 claims cases=10
$ python3 "$L/gate/citation-drift-gate.py" --root . --rev 158a966 … (no --snapshot-dir)
CITATION_DRIFT_VERDICT: failed findings=10 exit=1                  ← root build: could-not-evaluate exit=2
```

So **E15.md:206's committed line "cases=10 passed=10 failed=0 exit=0" for the
landing copy is not reproducible from the bytes that exist**: the copy on disk
reads `cases=9`, and without `--snapshot-dir` it mis-maps a configuration error
onto the declared `failed` code. The `find` listing at E15.md:198-202 and the
live-run line at E15.md:204 do reproduce. Z1.md:225-232 caught the 9-case
divergence independently (same /tmp tree, different seat) — my run is a fresh
execution that confirms it, and Z1.md:489-491 records the same landing warning.

### 2.2 The §5.2 transcript is normalized, not byte-exact

E15.md:144-154 renders regex escapes with single backslashes
(`lacks '\[mcp_servers\.rea'`); the gate's actual stdout carries Python-repr
doubled backslashes (`lacks '\\[mcp_servers\\.rea'`), verified byte-wise with
`od -c` on both. Semantically identical (both are the repr of the same regex),
so this is a transcription convention, not a false claim — but it means the
committed block cannot be `diff`ed byte-for-byte against a fresh run without
normalization. Anyone asserting "byte-identical reproduction" from this block
should state the normalization.

### 2.3 `frozen_run` is documentation, not enforcement

`grep -c 'frozen_run' /tmp/arc2-l3r3-E15/citation-drift-gate.py` → `0`; the only
key read from `expected.json` is `"snapshots"` (`:141`). Mutation test (mine):
rewriting `frozen_run.verdict` → `"clean"` and `frozen_run.revision` →
`deadbeef…` in a copy of `expected.json` changed nothing — the run still prints
`failed findings=10 exit=1`. So "the revision the verdict was measured against"
(`expected.json` `_doc`) is not checked by any code path. CR7.md:253-264 found
the same; my mutation run independently confirms the non-enforcement.

### 2.4 The pointer table does not survive round-3's C1 repair

At the current tree (HEAD `1692acb`, i.e. after round-3's `fd30b9c` re-anchors),
two entries stop extracting and their message class becomes misleading:

```
158a966: citation_dead entry=province-18-kimi-pin PROVINCE.md:18 states no resolvable pointer (pattern 'relocated it to :([0-9]+)' absent)
158a966: citation_dead entry=scorecard-59-pin-receipted SCORECARD.md:59 states no resolvable pointer (pattern 'config\.toml:([0-9]+)' absent)
679af5d: (both extract a number; scorecard-59 is citation_historical_ok)
```

Both exit 1 either way, and this is *not* a gate defect — it is the
`extracted` design correctly noticing that the citing sentence was rewritten.
But C2 must know: (a) the two patterns need updating to the content-anchor
form, and (b) the table's 8 `@config-toml-landmarks` entries (province-18,
scorecard-698, scorecard-59, mcpreg-11/12/18/88, r416-43) carry config.toml
**line numbers**, which C2's own constraint forbids — those must be reworked to
content-anchor form from E16's table, not copied. The five remaining entries
(scorecard-270 ×2, scorecard-69, scorecard-72, skill-registry-row) are the
in-repo-pinneable subset.

### 2.5 The chain has no durable home — only `/tmp` holds the bytes

`git grep -l 'citation-drift-gate' -- .` matches only report `.md` files; no
gate/pointer-table/snapshot bytes exist anywhere in the repo
(`find . -name pointer-table.json -o -name config-toml-landmarks` → nothing
outside `.git`). PROTOCOL.md:341-345 bars tmpfs pointers from landed evidence.
The one precedent of a committed artifact is `e16-table.json` at the repo root
(commit `1692acb`), which byte-matches `/tmp/arc2-l3r3-E16/e16-table.json`
(`89eddae0…` both) — so the C2 landing should copy the gate bytes in the same
commit that first cites them, exactly as E15.md:243-245 ("copy those files
rather than retype them") says. Until then, the chain is verifiable only while
the `/tmp` scratch survives.

### 2.6 Environment note (`/tmp` quota — explains a transient `rc=120`)

Mid-leg, redirects into `/tmp/arc2-l4r4-CR8/` began failing with
`tee: … Disk quota exceeded` and the shell reported `rc=120` for pipelines
whose output was empty. The gate itself was never at fault: the same command
run with stdout on the terminal exits 1 with full output, and a fresh small
write to `/tmp` later succeeded. `df` shows `/tmp` at ~80% (12–13 GB used,
tmpfs). All my later captures went to `/var/tmp/arc2-l4r4-CR8/`. Round-4 seat
V3.md:7 reports the same resource observation independently.

## 3. Text for the parent to land VERBATIM

C2 landing checklist — copy, do not retype; re-verify at the work commit:

````text
C2 gate landing — provenance recipe (CR8, round 4)

1. COPY the bytes, source = /tmp/arc2-l3r3-E15/ root files (NOT landing/):
     citation-drift-gate.py  0c5350b1c9a937fe9b3fd0942705edf77ecbe8c573f0965a81171e6b0eb79d8f  (415 lines)
     pointer-table.json      d7bf0eb340a652950fb49a5cb5e62adc4c3e7097376bdd45dbaa0ecd23db059b  (169 lines)  [rework before landing, step 3]
     expected.json           6ebada28259262da835c8371b9bfccfcebe4500c22fdd19716933a62fbca1beb  ( 26 lines)
     config-toml-landmarks   387e1f082dda6e77f5ea63677b15f67aef7d49d8820dc8d140a62c0d1096f154  (3322 lines, 7 non-blank)
   The landing/ directory under /tmp/arc2-l3r3-E15 is a STALE 9-case build
   (gate 1e4a734d…, expected 62b59166…): copying it silently drops the
   no_snapshot_dir case and mis-maps a configuration error onto exit 1.

2. VERIFY after copying (all four digests must match the list above; then):
     python3 <gate> --selftest --expected <expected.json>   -> cases=10 passed=10 exit=0
     python3 <gate> --root . --rev <WORK_COMMIT> --snapshot-dir <frozen dir>
       -> expected at the work commit: "failed findings=10 exit=1" if the round-3
          repairs are not yet applied, "clean findings=1 exit=0" if they are;
          either is a valid declared verdict — the point is the run reproduces.
     Tamper control: one appended byte to the frozen snapshot -> snapshot_tampered, exit=2.

3. REWORK pointer-table.json before landing (two changes, both required by C2's
   own constraint and by round-3's C1 re-anchors):
   a. province-18-kimi-pin and scorecard-59-pin-receipted no longer contain an
      extractable line number after fd30b9c (they read "states no resolvable
      pointer"); update their patterns to the content-anchor form.
   b. the 8 entries targeting @config-toml-landmarks by line number
      (province-18, scorecard-698, scorecard-59, mcpreg-11/12/18/88, r416-43)
      must become content-anchor/symbol entries per C2 ("NO config.toml line
      numbers"); E16's committed e16-table.json (89eddae0…) is the source of
      symbol-form rows.

4. PIN the landed copies: add the four sha256s (post-rework for the table) to
   the round-4 report and re-run step 2 at the landing commit, so the chain
   report -> bytes -> verdict is closed in-repo before the report lands.
````

## 4. Conclusions

- **OBSERVATION** — Root bytes verify 4/4 against E15.md:232-235; 6 copies
  across 4 seats hash to `0c5350b1…`; selftest 10/10; live run reproduces
  §5.2's set 10/10 modulo backslash normalization; tamper → exit 2;
  no-snapshot-dir → exit 2; `unpinned_legacy` branch exists; snapshot matches
  live config landmarks today (3c44c0ed… both sides).
- **OBSERVATION** — `landing/` diverges on two of four files; its selftest runs
  9/9 and E15.md:206's "cases=10" line for it is false; its no-snapshot-dir
  path exits 1.
- **OBSERVATION** — `frozen_run` is read by nothing; mutation changes nothing.
- **OBSERVATION** — At post-`fd30b9c` HEAD, two table entries read "states no
  resolvable pointer"; 8/13 entries use config.toml line numbers.
- **OBSERVATION** — No gate bytes in the repo; `e16-table.json` is the sole
  committed artifact of the family. `/tmp` tmpfs is near quota.
- **INFERENCE** — The provenance question ("what makes the committed copies
  trustworthy") is answered by the conjunction of: report pins + multi-seat
  re-hash agreement + a reproducible positive control + selftest reproducibility.
  It is NOT answered by the report's own landing transcript (§5.5), which is
  the one committed line that fails reproduction. Landing from `landing/` is
  the single most likely way for the parent to ship a silently weaker gate.
- **INFERENCE** — Copying root bytes and re-running step 2 at the landing
  commit closes the chain; no redesign is needed for the engine. The pointer
  table is the part that needs rework (step 3), not the gate.
- **UNKNOWN** — Whether the `landing/` bytes were ever the 10-case build (the
  mtimes say landing 15:04:24 < root 15:04:41, i.e. landing is an earlier
  build; whether §5.5's line was written against a since-overwritten landing
  copy cannot be determined from surviving state). Whether the parent's C2
  rework of the pointer table will keep all five non-config entries
  byte-stable — unmeasured here.
