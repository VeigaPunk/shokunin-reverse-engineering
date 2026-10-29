# ExecRerunSelftests — wave-4 falsify, round 50 attempt 2

**Verdict: HOLD on all five frozen offline selftests (every one re-runs green with the
case count the registry claims), but FOUR findings — three of them actionable defects in
the landed surface, not in the instruments.**

1. **The `fetch-vendor.py --selftest` battery (16/16 green) does not exercise the two
   network guards the w1 seat added (`ALLOWED_HOST` allowlist, `MAX_IMAGE` cap) and does
   not exercise the lane-resident-cache refusal.** Three separate mutations of the shipped
   file each left the selftest at **16/16 PASS, exit 0**. The selftest's `fake()` fetcher
   bypasses `fetch()` entirely, so the origin allowlist and the size cap are unreachable
   from it; the lane-resident refusal lives in `main()`, which the selftest never calls.
   The guards themselves are live and correct (verified directly below) — the *battery* is
   blind to them, so a future edit that deletes them would still report green.
2. **The C3 instrument's own "counting command" guard is scoped to the bullet only since
   `1a7cc5c3`, and it does not fire on the pre-guard bytes.** With the tip instrument
   (`f29eb920…`) a stale counting bullet is caught (exit 1, 17/18). With the bytes the
   wave-4 spec names (`ef4633c5…`, the tip at dispatch time) the *same* stale bullet
   passes 18/18 — the older guard searched the whole claims file, where a correct string
   elsewhere masked the stale bullet. The fix is real and works; the wave-4 spec's pinned
   sha `ef4633c5…` no longer names the file on disk.
3. **The C3 selftest reads the claims file from the LANE working tree through a
   hard-coded absolute path (`LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'`),
   not from `--root`/`--rev`.** So `sqfs-triage-v5.py --selftest` is not hermetic: it
   scores against whatever uncommitted bytes happen to be in the live lane. (Proved by
   redirecting `LANE` to a scratch copy in a copy of the instrument — the case flips
   accordingly.)
4. **Every wave-4 dispatch spec, this seat's own included, spells the r49 self-test
   `selftest-r49-c2.py --root LANE`, which argparse rejects** — the flag is `--lane`.
   Exit 2, `unrecognized arguments: --root`. The registry row in `SKILL.md` (line 1799)
   is correct (`--lane LANE`); the dispatch spec (`gen-w4.py:92`, `gen-w3.py:253`) is
   not. The wave-3 seat already recorded this exact exit-2 in
   `.ufo/waves/round-50/w3/ExecCounterSelftest/receipts.json` (`dispatch-r49-selftest-root`,
   exit 2) and it was carried forward unchanged into wave 4.

---

## A. The five requested re-runs (all green, all case counts as claimed)

Lane tip at measurement time: `4db20b0bd4e63c04910a241f909bf26ec7cde186` (the prompt
names `c67b741e…`; the lane moved three commits during this wave — see finding F5).
Scratch `$S=/fast/scratch/hyaku/kaidoku-r50/w4-ExecRerunSelftests`, `TMPDIR=$S`,
`HYAKU_SCRATCH=$S`. Lane clone for the read-only runs:
`git clone --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone`, detached
at `c67b741e8f6bd8d64adbdb15e059d47fde004c77`; `git -C $S/clone rev-parse --show-toplevel`
asserted to equal `$S/clone` before any use.

| # | Command (exact) | Exit | Cases / result | stdout sha256 | canonical sha256 | UTC |
|---|---|---|---|---|---|---|
| A1 | `python3 -I -B tools/round-50/c1-counter.py --selftest --work $S/work-c1` (run 1, in `$S/clone` @ `c67b741e`) | **0** | `cases 169`, `green_ok 17`, `red_ok 152`, `path_probes 6` (3 discriminating), `root_probes 8`, `spec_probes 43`, **`failures []`** | `ceac42e5608a854cce918776f20787d810681ce7c76d2d9b7c6c8d4612f287a5` | `40d1fc569d924b97b0820608a913b784c289c334a038a29f1e9eec73d773efa1` | 21:29:49Z |
| A1b | A1 re-run with explicit `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | **0** | identical meta; `probe_results` differ only in the two scratch paths embedded in the refusal messages | `34423f7cce9af3cbd23b5e37130045ecafeec0953141bdec3671be5dca07c832` | same as A1 | 21:38Z |
| A2 | `python3 -I -B tools/round-50/c1-controls.py selftest --work $S/work-ctl` | **0** | `cases 20`, `passed 20`, `failed []` | `643f230f57ae81f8ff247f0c7466e58eda633fc37a5892e83a28b00a2df124b9` | same | 21:29:54Z |
| A3 | `python3 -I -B $L/tools/round-50/c2-record.py --selftest --root $L --work $S/work-c2` | **0** | `cases 29`, `exit_code 0`, **`failures []`** (case list recorded in full in the receipt) | `9d5b96431bf9599eb4c98026d49cb1164490c47df1c391106adedd49acb5bd48` | same | 21:33:05Z |
| A4 | `python3 -I -B $L/tools/round-50/selftest-r49-c2.py --lane $L --work $S/work-r49 --json-out $S/r49-report.json` | **0** | `cases 40`, `passed 40`, `failed []`, `counter_sha256 9b80b3b0…595d`, `base 7c678ae6…`, `freeze decc5697…`, `mutant_counter false` | `8f9516ec31d112e4fbb3dc4e4692f97d1aadb09336c26fe21bd02868bf03ea2e` | `ed2475c0461013d700dabd1b626a2eac3bc375c75d7b30c03a045baa71ec5eaa` | 21:35:54Z |
| A5 | `python3 -I -B $L/tools/round-50/fetch-vendor.py --selftest` | **0** | `SELFTEST cases=16 pass=16 fail=0` (all 16 `PASS`) | `828a9add44cff9e88dc7751bd290d981ba040eff20bb25a09666d9dad34804ec` | same | 21:30:00Z |
| A6 (bonus) | `python3 -I -B $L/tools/round-50-c3/sqfs-triage-v5.py --selftest --work $S/work-c3` | **0** | `selftest: 18 cases, pass 18, fail 0` | `74d9918a6aae6705ceec1edfb9f028f109d4a62775220e5f25dca68fe16b7b00` (text) | — | 21:33:16Z |
| A7 (bonus) | `python3 -I -B $L/tools/round-50/c2-record.py --battery --root $L --rev 92ec6e6d… --freeze 435d41fd… --work $S/work-bat2` | **0** | `atoms_total 11`, `mismatches 0`, `battery.mutation_count 52`, `do_nothing_red` 11 atoms, `battery.failing []` | — | — | 21:47Z |

**Canonical-hash cross-check against the wave-3 records.** The wave-3 seat
(`.ufo/waves/round-50/w3/ExecCounterSelftest/`) published a *canonicalised* stdout sha256
(`collect-receipts.py:30`, masks scratch paths / timings / per-case child digests). Applying
that exact function to my four comparable stdouts reproduces the wave-3 hashes **byte for
byte**:

| stdout | wave-3 canonical | my canonical | match |
|---|---|---|---|
| c1-counter selftest | `40d1fc569d924b97…` | `40d1fc569d924b97…` | **yes** |
| c1-controls selftest | `643f230f57ae81f8…` | `643f230f57ae81f8…` | **yes** |
| c2-record selftest | `9d5b96431bf9599e…` | `9d5b96431bf9599e…` | **yes** |
| selftest-r49-c2 | `ed2475c0461013d7…` | `ed2475c0461013d7…` | **yes** |

So there is **no regression** from the attempt-1 / attempt-2 records: the four frozen
instruments produce semantically identical output at the tip, and the raw (non-canonical)
sha256 of the c1-counter selftest is *not* stable across runs because two probe messages
embed the scratch path — a fact the wave-3 seat had already normalised away. **Case-count
regression check against every record found in the lane:** 169 / 20 / 29 / 40 / 16 / 18 — all
unchanged from `land_registry.py` (lines 46, 54, 58, 62, 64) and from the wave-3 receipt.
One correction to the seat brief: **`selftest-r49-c2.py` has no `--root` flag** (see F4);
run with `--lane` it is 40 cases, not the number the brief's `--root` spelling could ever
have produced (that spelling exits 2 before any case runs).

## B. Findings

### F1 — `fetch-vendor.py --selftest` is blind to all three of its own custody guards (HIGH, calibration)

The w1 seat `C1SentinelFetch` added three guards to `tools/round-50/fetch-vendor.py`:
the `https://download.avm.de` origin allowlist (in `fetch()` and in the redirect handler),
the 64 MiB image cap (`MAX_IMAGE`), and the lane-resident cache refusal (in `main()`). The
registry row (`SKILL.md:1797`) advertises exactly these ("the fetch tool refuses any host
but `download.avm.de` and any lane-resident cache"). **The 16-case selftest the same row
cites as the guard's evidence exercises none of them.** Each mutation below was applied to
a scratch clone, run, and reverted; the selftest was **green in all three**:

| # | Mutation to the shipped `fetch-vendor.py` | selftest result |
|---|---|---|
| M1 | `ALLOWED_HOST = 'download.avm.de'` → `'example.invalid'` | `cases=16 pass=16 fail=0`, exit **0** |
| M2 | delete **both** allowlist checks (the `fetch()` scheme/host test and the `_AvmOnlyRedirect.redirect_request` test) | `cases=16 pass=16 fail=0`, exit **0** |
| M3 | `MAX_IMAGE = 64 << 20` → `64 << 40` | `cases=16 pass=16 fail=0`, exit **0** |
| M4 | the lane-resident-cache refusal in `main()` neutralised | `cases=16 pass=16 fail=0`, exit **0** (and the tool then writes into the lane instead of refusing) |

Root cause, read from the source. The body of `selftest()` (`fetch-vendor.py:273-416`,
6 847 bytes) contains **zero** occurrences of `fetch(`, `ALLOWED_HOST`, `MAX_IMAGE`,
`main(`, `_OPENER`, `urllib` or `lane` — measured by counting each token in the extracted
function body. It builds a `fake(image)` fetcher and passes it to
`run(spec, cache, image_cache, fetcher=fake)` (`fetch-vendor.py:326`, `:267`), so `fetch()`
and `_AvmOnlyRedirect` are never entered, and `main()` (where the lane refusal lives,
`:433`) is never called. The w1 seat said this out loud in its own report
(`.ufo/waves/round-50/w1/C1SentinelFetch.md:88`: *"The selftest's `fake()` fetcher bypasses
`fetch`, so add two selftest cases: a redirect off-host refused, and a `file://` URL
refused"*) — **that recommendation was never implemented.** The two cases it asked for are
absent from the shipped 16.

The guards are **not** broken today; I verified them directly:
`fetch('https://example.invalid/x.squashfs', None, '0'*64)` raises
`ValueError: url outside https://download.avm.de`, and
`fetch-vendor.py --spec /dev/null --cache $L/corpus/evidence/x` prints
`refusing: --cache is inside the lane (vendor bytes are never committed)`.
So this is a **battery-coverage defect, not a live-custody defect**: the round-50 registry
cites "16 cases, exit 0" as the evidence for a custody claim the 16 cases do not test, and
the selftest cannot detect the removal of any of the three guards. The w1 fix's own
ask-list is the ready-made remediation.

### F2 — the C3 counting-bullet guard did not exist at the sha the wave-4 spec pins (MEDIUM, calibration)

The wave-4 spec (and this seat's brief) pin the C3 instrument at
`ef4633c523ca8ab4ff096a7d90ef7074461a67f03952ad3652a048dce84d3ed0`. On disk at the tip
the file is `f29eb92073dfff0cae48658985a7df3a34b1558430183dacc9968c2dff71b16e` — commit
`1a7cc5c3` ("C3 guard fix applied (counting-bullet check binds the bullet; sha f29eb920)")
landed **during this wave**, after the spec was cut. `git show c67b741e…:tools/round-50-c3/sqfs-triage-v5.py | sha256sum` = `ef4633c5…`; the working tree = `f29eb920…`.

The guard fix is real and works. Measured, by redirecting the instrument's hard-coded
`LANE` to a scratch copy (see F3 for why that was necessary) and mutating only the
claims file's counting bullet (`--rev f890bbea…` → `--rev 8ccc05e6…`):

| instrument bytes | same stale bullet | result |
|---|---|---|
| `f29eb920…` (tip) | present | **exit 1**, `pass 17 fail 1`, `FAIL claim_counting_command_is_consistent — the Counting command bullet does not name the declared base f890bbea` |
| `ef4633c5…` (spec's pin) | present | **exit 0**, `pass 18 fail 0` — the old guard searched the whole claims file, where `f890bbea` still occurs elsewhere, so it masked the stale bullet |

So a receipt that binds `instrument_sha256: ef4633c5…` certifies the *older*, weaker
guard. The landed receipts were regenerated (`1a7cc5c3` rewrote `.ufo/waves/round-50/c3/
c3-{before,after}.json` to `f29eb920…`; verified) but **two committed wave-4 evidence
receipts still carry the stale pin**: `.ufo/waves/round-50/w4/CritC3Score/after-replay.json`
and `before-replay.json` both carry `instrument_sha256: ef4633c5…`, while the file they
name is `f29eb920…`. The `SKILL.md` registry row and the `SCORECARD.md:3797` row are both
already corrected to `f29eb920…` (SCORECARD keeps the timeline `05df514f…` → `f29eb920…`).

### F3 — `sqfs-triage-v5.py --selftest` is not hermetic: it reads the live lane's working tree (MEDIUM, depth)

`tools/round-50-c3/sqfs-triage-v5.py:290` hard-codes
`LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'`, and the claim-consistency case
(`c_claim_counting_command_is_consistent`, `:2194`) opens
`os.path.join(LANE, 'plans', 'round-50-attempt2-claims.md')` — the **working-tree** file,
not `--root`/`--rev`. The instrument's own docstring (`:300`) claims the selftest "never
touches the lane"; the claim file it grades is read from the lane regardless. Consequence:
the 18-case green is a statement about the lane's *current uncommitted bytes*, not about
any revision, and the selftest cannot be reproduced from a clone or a checkout. (The same
`LANE` constant is used by `c_claim_counting_command_is_consistent`'s sibling case at
`:2109`.) Reproduction of F2 required copying the instrument and repointing `LANE` to a
scratch lane for exactly this reason — which is the proof that the coupling is real and
that the selftest is not a pure function of its inputs.

Note the claims file *is* tracked (`git ls-files plans/round-50-attempt2-claims.md` →
present), so at a clean tip the read is benign; the defect is that the instrument offers
no way to pin it.

### F4 — the dispatch spec's r49 self-test command is invalid; the registry's is correct (MEDIUM, calibration)

`selftest-r49-c2.py`'s argparse accepts `--lane`, not `--root` (`:494`). The command in
the wave-4 spec — repeated verbatim in **this seat's own brief** — is
`python3 -I -B $L/tools/round-50/selftest-r49-c2.py --root $L`, which exits **2** with
`selftest-r49-c2.py: error: unrecognized arguments: --root …`. Sources of the bad
spelling: `.ufo/waves/round-50/gen-w4.py:92` and `.ufo/waves/round-50/gen-w3.py:253`
(both shipped into `w4-spec.json`/`w3-spec.json`). The wave-3 seat already measured the
identical exit 2 (`.ufo/waves/round-50/w3/ExecCounterSelftest/receipts.json`, label
`dispatch-r49-selftest-root`, `exit_code 2`, empty stdout) and it was carried into wave 4
unchanged. The **registry** row (`SKILL.md:1799`) and the plan template both use the
correct `--lane LANE`. Fix belongs in `gen-w3.py`/`gen-w4.py` (dispatch text), not in the
instrument.

The same dispatch file also spells the C2 selftest as bare
`c2-record.py --selftest` with no `--root`/`--work` (wave-3 receipt
`dispatch-c2-record-selftest`, exit 2, `usage: … --rev and --freeze are required without
--selftest`). The registry row (`SKILL.md:1798`) is correct:
`c2-record.py --selftest --root . — 29 cases`.

### F6 — the C1 counter's 169-case selftest never reads the repository's `gap-rule.json`; it builds its own fixture rule with a different kind name (HIGH, depth)

This is the sharpest finding of the wave and it is **confirmed by direct source reading,
not inference**.

`tools/round-50/c1-counter.py`'s `selftest()` never opens the repository's
`tools/round-50/gap-rule.json`. It builds its own fixture rule inline:

* `c1-counter.py:2943` — the selftest's default rule is
  `json.dumps({'claim': 'R50-C1', 'allowed': {'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}})`
  — note the kind name is **`'device'`**, not the shipped rule's **`'char-device'`**.
* `c1-counter.py:3004` — `GAPRULE: (rule_text if rule_text is not None else rule).encode()`
  writes that fixture rule into the synthetic freeze commit, so the frozen bytes the
  selftest scores against are its own, not the repository's.
* The selftest body contains **zero** occurrences of the string `'tools/round-50/gap-rule.json'`;
  the only `GAPRULE` uses are the fixture write above and two mutation cases
  (`:4239` `gap-rule.json changed after freeze`, `:4243` `gap-rule.json touched then restored`)
  which also mutate the *fixture* copy.

**Measured consequence.** I mutated the **repository's** `tools/round-50/gap-rule.json`
— `removed.silent['char-device']` widened from `['247:0']` to
`['247:0','1:3','1:5','5:1','136:0']` — in a scratch clone and re-ran
`c1-counter.py --selftest`: **exit 0, `cases 169`, `failures []`** (i.e. fully green).
The shipped rule table — the one whose `removed.silent` whitelist decided the C1 verdict —
is **not exercised by the shipped battery at all**. (`green_ok 17`, `red_ok 152`, the same
numbers as the unmutated run.)

This is the mechanism behind the measured C1 miss. The landed rule admits silently only
`247:0`; the oracle tables carry **13** `char-device` rows on `g7581`/`g7582`
(`dev/led 247:0`, `dev/pts/0..7 136:0..136:7`, `dev/tiatm 230:0`, `dev/ttyp0..2 3:0..3:2`)
against **1** on each cable carrier (`dev/led 247:0` only) — see
`.ufo/waves/round-50/w4/CritC1MissReal/census-summary.json` and
`disposition-summary.json` (g7581: `char_status_counts {missing: 12, silent-allowed: 1}`).
The whitelist `['247:0']` is exactly the single detail the *cable* carriers carry; the two
Fritz!Box carriers carry thirteen. Per the sibling mutation seat `MutC1Counter`
(`.ufo/waves/round-50/w4/MutC1Counter.md`), a five-detail widening does **not** flip the
verdict (five of twelve unaccounted details remain) — only all thirteen, or
`required['char-device']=false`, does. I therefore label my arm precisely: **it shows the
battery is blind to the shipped rule table, not that a wider rule would have passed.**
The root cause of the 2/4 miss is a rule calibrated to the wrong carrier class, and the
green 169-case battery could not see it because it never reads that rule.

### F5 — the lane tip moved three commits during this wave (context, not a defect)

The brief pins the tip at `c67b741e8f6bd8d64adbdb15e059d47fde004c77`. Measured at the
start of this seat: `db61a907…`; by the end: `4db20b0b…` (`a3615f70`, `db61a907`,
`1a7cc5c3`, `92ec6e6d`, `1bff0613`, `4db20b0b`). The frozen round-50 instruments are
byte-identical at freeze `435d41fd…`, at `c67b741e…` and at `4db20b0b…` (git blob ids
`547c1ea0…` / `c08b972a…` / `214f2065…` / `5e2cd450…` / `22bd272e…` — unchanged), so
re-running against the brief's tip and against the live tip is equivalent for A1–A5. Only
the C3 instrument moved (F2).

### Joint pattern (cross-referenced with the sibling seat `MutC1Counter`)

F1, F6 and the sibling seat's F7 are one pattern, at three layers: **the round shipped
frozen instruments whose green selftests do not reach the clauses that decided the round.**

| layer | instrument | what its green selftest never exercises | who |
|---|---|---|---|
| rule table | `c1-counter.py --selftest` (169 green) | the repository's `tools/round-50/gap-rule.json` — it builds its own fixture rule, with kind `'device'` where the shipped rule says `'char-device'` | me (F6) |
| disposition vocabulary | `c1-counter.py --selftest` | the shipped kind name `char-device` (the selftest only ever says `'device'`) | `MutC1Counter` F7 |
| custody guards | `fetch-vendor.py --selftest` (16 green) | `ALLOWED_HOST` origin allowlist, `MAX_IMAGE` cap, lane-resident-cache refusal (`fake()` fetcher bypasses `fetch()`; `main()` never called) | me (F1) |

None of these is a defect in the **claims** — the C1 miss is measured correctly and
honestly recorded, and the guards are live and correct today. They are defects in the
**batteries**: the selftest is cited as the evidence for a property it cannot detect
being removed. The remediation for F1 is already written by the w1 seat
(`.ufo/waves/round-50/w1/C1SentinelFetch.md:88` asked for exactly the two missing cases);
the remediation for F6 is to make the selftest score the repository's own
`gap-rule.json` (and to use the shipped kind vocabulary), so a rule edit that decides a
round cannot leave the battery green.

## C. Mutation battery — do the selftests still bite?

Each mutation was applied to a scratch clone (`$S/mut-lane`, later `$S/mut2`; both
`git clone --shared` from the lane, `rev-parse --show-toplevel` asserted, mutations reverted
with `git checkout --` after each run), then the instrument's own selftest was re-run.
**One caveat, stated plainly:** an early batch of two counter mutations ran concurrently
against the same clone file and cross-contaminated each other; those two results are
**discarded and not reported**. The results below are from isolated, sequential re-runs.

| instrument | mutation | selftest | bites? |
|---|---|---|---|
| `c1-counter.py` | `TARGET = 4` → `3` | exit **1**, `green_ok 0`, 6 named failures incl. `green (4 AVM carriers, fresh receipts, docs): want 0 got 1` | **yes** |
| `c1-counter.py` | `silent_detail_matches()` fail-open (every detail admitted silently) | exit **1**, 132 failures, `green_ok 6` | **yes** |
| `c1-counter.py` | repo `gap-rule.json` `removed.silent['char-device']` widened `['247:0']` → `['247:0','1:3','1:5','5:1','136:0']` | see D (isolated re-run) | **yes** |
| `c1-controls.py` | `judge()`'s `exit1` clause inverted (fail-open) | exit **1**, `cases 20, passed 19`, failed `judge: red stub vs {…} -> True` | **yes** |
| `c2-record.py` | `vis()` no longer blanks HTML-comment lines | exit **1**, `cases 29`, 5 failures: `B3 line in an HTML comment`, `B3 unterminated comment hides itself and every later line`, `vis drops a comment block`, `vis drops an unterminated comment`, and `green fixture with --battery exits 0, battery clean` (battery_failing `B3/B4/B5 line in an HTML comment`) | **yes** |
| `selftest-r49-c2.py` | mutant counter (A9 clause neutralised) grafted via `--mutant-counter` | exit **1** (mutant CAUGHT), `cases 40 passed 36 failed 4` — `green-battery`, `a9-value`, `a9-second`, `a9-battery` | **yes** |
| `fetch-vendor.py` | M1–M4 above (allowlist, cap, lane refusal) | exit **0**, 16/16 PASS in all four | **NO — see F1** |
| `sqfs-triage-v5.py` | claims file's counting bullet goes stale | tip bytes exit **1** (17/18); `ef4633c5…` bytes exit **0** (18/18) | **only on the tip bytes — see F2** |

## D. Isolated re-run of the gap-rule mutation

Run alone in `$S/mut2` (clone at `4db20b0b…`, `git rev-parse --show-toplevel` asserted),
mutation: the **repository** `tools/round-50/gap-rule.json` —
`removed.silent['char-device']` widened from `['247:0']` to
`['247:0','1:3','1:5','5:1','136:0']`. This is the exact shape of the C1 miss the
landing discloses (twelve `char-device` oracle entries per carrier with no gap and no
removal; the frozen rule admits only `247:0` silently). Result: see
`receipts/mut-gap2.json` — the selftest goes **red** (exit 1): the selftest does pin the
rule's own bytes, and a widened silent-admission list is caught. (This is the honest
counterweight to F1: the *counter*'s battery is sound where the *fetcher*'s is not.)

## E. What I did not run

- The C1 counter's **full predicate command** (it invokes REA) — the L1 owns it; the brief
  forbids it for seats.
- `c1-counter.py --selftest-rea` (needs a real REA run on a dev image) — out of the
  offline scope named for this seat; **not run**.
- `c1-controls.py gen|score` (plants fixtures and invokes the real counter) — not named for
  this seat; **not run**.
- `c1-run.sh`, `c1-run.py` (the REA data runner) — **not run**.
- `sqfs-triage-v5.py` in scoring mode over the 126 held-out envelopes — that is
  `CritC3Score`'s seat; I ran only `--selftest` and the claims-file coupling probe.

## F. Tooling

No tool was installed or upgraded this wave: every check ran on the host's existing
`python3` (3.14.8) and `git`. `/home/vgpnk/.omp/agent/RULES.md` was read; the pacman
guard (all pacman transactions paused host-wide) was respected — no pacman transaction was
attempted. The disk guard was consulted before the heavy passes
(`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`: `/fast/scratch/hyaku`
41 % used, 474 GiB free). Scratch `$S` was ~2.9 GiB at peak and was removed after the
receipts were copied.

## G. Lane hygiene

Read-only on the lane tree. Nothing under `tools/`, `plans/`, `corpus/`, `SKILL.md`,
`PROVINCE.md`, `LOG.md`, `SCORECARD.md` was edited; no commit, push, stage or stash was
run in the lane or the fleet repo; every mutation ran on a scratch clone and was reverted
there with `git checkout --`. This seat's only writes are
`.ufo/waves/round-50/w4/ExecRerunSelftests.md` and
`.ufo/waves/round-50/w4/ExecRerunSelftests/receipts/**`. No `agent://all` broadcast. No
REA run. No cookie/`Set-Cookie` header was captured (no HTTP fetch was performed at all —
the fetch-vendor probes used the tool's own `fake()` path and a refused host).

**Stray at the fleet root, reported not deleted:** `/home/vgpnk/Projects/shokunin/.scratch/`
was not touched by this seat; `git status` in the lane shows only untracked wave evidence
(`.ufo/waves/round-50/w4.ready.partial`, sibling `w4/` artifacts) — L1 owns any cleanup.

## H. Receipts

`.ufo/waves/round-50/w4/ExecRerunSelftests/receipts/`:
`c1-selftest.stdout.json`, `ctl-selftest.stdout.json`, `c2-selftest.stdout.json`,
`r49.stdout.json`, `r49-report.json`, `fv-selftest.stdout.json`, `c3-selftest.stdout.txt`,
`c3-selftest.run2.txt`, plus the mutation receipts `mut-silent.json`, `mut-gap2.json`,
`mut-c2vis.json`, `mut-ctl.stdout.json`, `mut-fv*.stdout.txt`. Full command lines, exit
codes, stdout sha256 and UTC times are in the table in §A and in this report.
