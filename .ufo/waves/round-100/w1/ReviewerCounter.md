# ReviewerCounter — R100 w1 review of the two frozen counters (F = 8e24c29a)

Scope: counter-source review + attack probes. Counters read at F via `git show` (worktree byte-identical;
c2 sha256 496a4979ecd6…, c1 8f148d336e6f…); dynamic probes in a `--shared` clone at A2 = cbd224ef…
(toplevel asserted). No tool installs. Revision used: F bytes, scored at A2; lane HEAD was A2 throughout.
Supporting: `ReviewerCounter/probes.md` (full transcript), `ReviewerCounter/c2-at-a2-review.json`,
`ReviewerCounter/c1-forgery-filename.json`, `ReviewerCounter/w1-review-forgery.py`.

## Reproductions (run by this seat)
- C2 selftest: `SELFTEST cases=22 failures=0`, rc 0.
- C2 full at A2 (frozen command, root=my clone): `rows 93; claimed 93 of 93; green 93 of 93; counted 93
  of 93; agree 93 of 93; mismatches 0`, met True, rc 0, 1m49s. After the run: `git status --porcelain`
  in the clone shows only my own probe file — 93 self-tests wrote nothing into the clone (cwd=clone,
  scrubbed env, c2.py:147-150); the CANARY.txt planted in `--work` was deleted (rmtree, c2.py:254).
- C1 full battery with a review forgery (see F6): full TARGET label, met True, rc 0, 154 traced
  invocations, 0 exec violations.

## Findings (severity-ranked)

**F6 [Medium — named limit of C1] Refusal check is output-shaped; a filename-keyed forgery passes.**
Corrupt/truncated cells verify only candidate rc 2 + keyword (`checksum`/`truncated`) + no `--out`
(c1.py:401-403, 384-385); the decision procedure is unobservable. I committed
`clone/tools/round-100/w1-review-forgery.py` (sha256 e9f2ac412dba0e35…): it refuses any input whose
basename contains `.corrupt-`/`.trunc-` from the FILENAME alone — the file is never opened — with
hardcoded strings, while doing real content repairs (adler-validated PackHeader scan + section-rename
reversal) for every other arm. Frozen battery result: full TARGET label, met True, exit 0
(c1-forgery-filename.json: corrupt 40/40, truncated 40/40, static 1/1, exec 1/1). The h0–h6 fixtures
cover other forgery classes (h5 = length-only rule) but not input keying. Recommendation: commit this
forgery (or equivalent) as an h-control so the red-fixture family tracks content-blindness too. Inherent
limit — no output-shaped counter can fully close it — hence named limit, not a block.

**F2 [Low — C2] A mismatch can hide behind a trailing count line; pin atom is the real defense.**
OBS_RE takes the LAST match (c2.py:61, 120-124): a tool printing its real `cases=17 failures=3` and then
a trailing `cases=18` banner is counted 18; JSON precedence (c2.py:108-118) prefers an integer `cases`
key, and if the dict lacks one, the regex matches inside string values (`{"detail":"cases=5"}` → 5).
Exploitation requires editing the pinned tool — all 93 rows pin the executed script's sha256 (verified:
95/95 pinned files == B bytes == A2 bytes) — but the pin does not cover READ dependencies: r70/r71
forged-receipts rows execute only their own pinned file while reading `tools/round-69/packed-elf.py`
via `--base-tool` (unpinned in their pin dicts, c2.py ~337-347); helper drift at a future rev could move
printed counts without failing any pin (fail-open for agree, fail-closed for disagree).

**F1 [Low — C2] Frozen argv ≠ documented command for 4 of 93 rows.** r53 sqfs-triage-v6 and r55
v6-block-digest document `python -X utf8 -I -B …` (counter runs `python3 -I -B`, c2.py POPULATION);
r96 kill-rule-v2 and r96 stop-boundary-repair-battery-v6 document `--selftest --work <dir>` (counter
drops `--work`). All four counted == claimed at A2 (L1 receipt + my rerun), so no scoring impact today;
the docstring's "argv of the documented self-test" (c2.py:23) is not literally true for these 4.

**F7 [Low — C1] Exec leg accepts a vacuous log.** A strace log with ZERO exec lines still passes
(execs[1:] == [], c1.py:223-224; leg = `bool(EXEC_LOG) and not violations`, c1.py:435-436) — a silently
broken strace (no per-log witness that even the interpreter's exec was seen) would pass the leg.
Unreachable today: a failing strace pollutes candidate rc, failing the recovered/intact arms first.
Hardening: require ≥1 exec line per log.

**F8 [Low — C1] Exec-leg evasion surface (analytic + probes).** Caught (strace probes, same argv shape
as c1.py:216-227): os.execv self-restart, posix_spawn, subprocess — each leaves a 2nd execve line; failed
exec attempts also count. fork/clone-without-exec is invisible but cannot execute an external oracle.
NOT covered: a networked oracle (socket to a pre-started daemon — no FORBIDDEN token covers sockets,
c1.py:121-123) or an embedded codec; strace filter is execve/execveat only (c1.py:221). FORBIDDEN is a
declared text screen (`getattr(os,'system')` passes it).

**F11 [Low — C1] Candidate runs with inherited cwd and full env.** run() (c1.py:139-144) sets neither
cwd nor env, so every candidate invocation executes in the battery's cwd — per the frozen command that
is the lane checkout — with the seat's full environment. Unlike C2 (cwd=clone + PATH/HOME/scratch env,
c2.py:147-150). A candidate writing relative scratch files would dirty the lane worktree; today's
candidate is the lane's own trusted repair. Hardening: run candidates with cwd=--work, TMPDIR=--work.

**F3 [Low — both] Receipt-write failure conflates exit codes.** `--json-out` with a missing parent →
FileNotFoundError; `--json-out` an existing dir → IsADirectoryError (probed on c2.write_receipt); both
uncaught → traceback + exit 1, i.e. "predicate failed" instead of exit 2 could-not-evaluate (c2.py:177
before print at 286-287; c1.py:448 before print at 459-460 — for C1 this discards the label only after
the full battery ran). mkstemp+fsync+os.replace+finally-unlink itself is sound: no `.receipt-*` litter
after failed probes.

**F10 [Info — C1] Corrupt-arm range verified exactly correct on the real carriers.** On all 10 pinned
carriers packed with upx 5.2.0 `--best`: first `UPX!` is the PackHeader; `c_len` at i+20;
zlib.adler32(data[i+32 : i+32+c_len]) == c_adler at i+12 on 10/10 (the S327 `ph_decompress` rule,
getPackHeaderSize()=32); i+32+c_len ≤ filesize 10/10; decoy window eligible 9/10 (sevenzip64dll's
j+4/j+5 nonzero → decoy_cells 9, matching TARGET's 9). `randbelow(c_len)` keeps offsets in
[i+32, i+32+c_len) (c1.py:245-250); the XOR byte is always nonzero, so every draw changes the adler →
`effective` is deterministic for the corrupt arm. ph_fields itself does no validation (c1.py:236-243) —
acceptable for oracle-packed pinned carriers; a stray earlier `UPX!` would corrupt the range (none here).

**F9 [Info — C1] `effective` arithmetic correct.** 30 (recovered) + 9 (decoy) + 40 (truncated) + 40
(corrupt) = 119, summed only from measured `upx -t rc != 0` (c1.py:348, 354, 381, 399). The decoy
denominator is runtime `decoy_cells` against TARGET's literal `9` → packer drift fails closed. The a/b
corrupt draws may coincide (no uniqueness guard) — harmless, each cell still effective.

**F4 [Info — C2] Parser edges, all fail-closed.** CLAIM_RE first-match wins (`selftest 3 cases; suite
covers 18 cases` → 3); accepts `#cases=9` (lookbehind allows `#`); rejects flag-shaped
`--max-cases 5`/`sub_cases=7`. A count stated in any other column than the self-test cell (cells[3],
c2.py:95-98; short rows join cells[1:]) yields claimed=None → mismatch, never a false pass.
registry_rows skips indented rows (startswith("| `"), c2.py:85) — a population row hidden that way fails
the row atom; doubled/missing markers → exit 2. Post-freeze rows outside the frozen population are out
of scope by construction (label counts len(POPULATION)).

**F5 [Info — C2] `--work` is destroyed at start.** shutil.rmtree(work) (c2.py:254; c1.py:283): the
counter deletes the given directory's contents (canary deleted in my run). Seats pass dedicated scratch
dirs per the lane rules, so no incident; worth a docstring warning.

**F12 [Info — C1] Battery preflight/pin hygiene good.** Carriers sha256-pinned (10/10 verified on this
host), upx version pinned 5.2.0, strace path checked, candidate bytes read via `git show rev:path`
(worktree mode only on explicit `--rev worktree`), repair_sha256 + counter_sha256 in receipt. L1 receipt
cross-checked: 154 traced invocations, 0 violations, full label.

## Verification gaps
- I did not rerun the full C1 battery against the real candidate (upx-pe-repair.py) — that reproduction
  belongs to ExecReproC1/ExecGraderV9; my C1 run exercised the battery with the review forgery.
- No probe of strace behavior under ptrace restrictions or seccomp (host allows strace; guards not
  exercised).
- r70/r71 helper-drift scenario (F2) is structural: today `tools/round-69/packed-elf.py` is unchanged
  B→A2 (pin of its own row holds), so no live effect.

## Bottom line
Both counters are faithful to their frozen definitions: C2's population/pins are exact (93 == 93, seven
stated counts match the claims plan, 95/95 pins hold B→A2), C1's corrupt range and `effective` math are
verified against the packer's own rule on the real carriers, and both reproduce met/exit-0 at A2 in a
clean clone. The one substantive gap is F6: the corrupt/truncated refusal is enforced only through
output shape, and a filename-keyed forgery passes the whole battery — recommend freezing that forgery as
an additional red control next round. Nothing here blocks the L1 scores at A1/A2.
