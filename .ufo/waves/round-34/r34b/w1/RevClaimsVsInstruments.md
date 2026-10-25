# RevClaimsVsInstruments — R34-C2 pin audit (round 34, r34b w1)

Seat: `L1Kaidoku34-2.RevClaimsVsInstruments` (leaf, no subagents).
Scope: every path and sha256 in `.ufo/waves/round-34/r34b/claims.json` → `claims[0].pins`, read at
`c79bbe7b0959132b9873ff3431cf5eb313b58b33`, compared to the declared digest. Depth extensions kept
only where they test the *claim's own* declarations against the frozen bytes.
All timestamps UTC. Lane VCS read-only throughout: only `git show` / `git ls-tree` / `git log` /
`git cat-file` / `git clone --shared` were issued; no worktree, index, ref or jj mutation.

## 1. Result

**26 pins checked — 26 match, 0 mismatched, 0 missing.** The byte-level freeze holds exactly at
`c79bbe7b`.

| # | path | declared (first 16) | measured at c79bbe7b | status |
|---|---|---|---|---|
| 1 | `tools/round-34/c2-shortcut-gate-counter.py` | `41d597036eb60f2e…` | `41d597036eb60f2e…` | OK |
| 2 | `tools/round-34/gate-config-mini.json` | `4483f3852429b439…` | `4483f3852429b439…` | OK |
| 3 | `tools/round-34/gate-config-naive.json` | `72b1294171b58ecb…` | `72b1294171b58ecb…` | OK |
| 4 | `tools/round-34/mini-fix/build.py` | `c67180515bcb1b77…` | `c67180515bcb1b77…` | OK |
| 5 | `tools/round-34/mini-fix/expected.json` | `5ebb5349fd21eb3e…` | `5ebb5349fd21eb3e…` | OK |
| 6 | `tools/round-34/mini-fix/fixtures/alpha.mrec` | `d1de0e6f50eca499…` | `d1de0e6f50eca499…` | OK |
| 7 | `tools/round-34/mini-fix/fixtures/beta.mrec` | `a8547fcf1764611f…` | `a8547fcf1764611f…` | OK |
| 8 | `tools/round-34/mini-fix/fixtures/delta.mrec` | `79ff7036235a0263…` | `79ff7036235a0263…` | OK |
| 9 | `tools/round-34/mini-fix/fixtures/epsilon.mrec` | `82f03f991a99b730…` | `82f03f991a99b730…` | OK |
| 10 | `tools/round-34/mini-fix/fixtures/eta.mrec` | `5bcabeb2711ead28…` | `5bcabeb2711ead28…` | OK |
| 11 | `tools/round-34/mini-fix/fixtures/gamma.mrec` | `ffb57ecdad76f624…` | `ffb57ecdad76f624…` | OK |
| 12 | `tools/round-34/mini-fix/fixtures/theta.mrec` | `b1f87d7cb8147c5c…` | `b1f87d7cb8147c5c…` | OK |
| 13 | `tools/round-34/mini-fix/fixtures/zeta.mrec` | `19ff407420ab8028…` | `19ff407420ab8028…` | OK |
| 14 | `tools/round-34/mini-fix/mini-counter.py` | `43ef669ff6ea9fe7…` | `43ef669ff6ea9fe7…` | OK |
| 15 | `tools/round-34/mini-fix/naive-counter.py` | `087c97f77ec15e23…` | `087c97f77ec15e23…` | OK |
| 16 | `tools/round-34/mini-fix/readers/all_false.py` | `e1a509b09d5a4df5…` | `e1a509b09d5a4df5…` | OK |
| 17 | `tools/round-34/mini-fix/readers/digest_keyed.py` | `87577e187f1cbb7f…` | `87577e187f1cbb7f…` | OK |
| 18 | `tools/round-34/mini-fix/readers/fixed_slice.py` | `8a1d1ce58cf86473…` | `8a1d1ce58cf86473…` | OK |
| 19 | `tools/round-34/mini-fix/readers/label_keyed.py` | `f727c1527052d1fd…` | `f727c1527052d1fd…` | OK |
| 20 | `tools/round-34/mini-fix/readers/label_replay_full.py` | `c772227e608fb3c2…` | `c772227e608fb3c2…` | OK |
| 21 | `tools/round-34/mini-fix/readers/record_order_replay.py` | `11d655afef4e1f43…` | `11d655afef4e1f43…` | OK |
| 22 | `tools/round-34/mini-fix/readers/size_keyed.py` | `740a7f7e95287428…` | `740a7f7e95287428…` | OK |
| 23 | `tools/round-34/mini-fix/readers/string_scan.py` | `4a46f5e2536d4393…` | `4a46f5e2536d4393…` | OK |
| 24 | `tools/round-34/mini-fix/readers/structural.py` | `2f399cab36450c05…` | `2f399cab36450c05…` | OK |
| 25 | `tools/round-34/mini-fix/spec.json` | `3cb59080167d8e3a…` | `3cb59080167d8e3a…` | OK |
| 26 | `tools/round-34/replay-gate.py` | `8fa94b2332a6574c…` | `8fa94b2332a6574c…` | OK |

Full 64-hex digests, both sides: `/fast/scratch/hyaku/kaidoku-r34b/w1/RevClaimsVsInstruments/pin-audit.json`.
Load-bearing five in full: `replay-gate.py` `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558`;
`c2-shortcut-gate-counter.py` `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72`;
`gate-config-mini.json` `4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c`;
`gate-config-naive.json` `72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428`;
`readers/structural.py` `2f399cab36450c052f72c996ef6f3cbb5a57914a2053a6f2a9a31c214eb9b4b6`.

## 2. Commands, exit codes, UTC

| step | command | exit | UTC |
|---|---|---|---|
| A | pin loop: `git -C <lane> show c79bbe7b:<path>` → `hashlib.sha256` for all 26 pins (script `tools`-free, read-only) | 0 | 2026-10-25T07:18:13Z |
| B | `git rev-parse HEAD`, `git status --porcelain`, `git show <rev>:claims.json \| sha256sum` | 0 | 07:18:2xZ |
| C | `git ls-tree -r c79bbe7b -- tools/round-34/` (blob modes) | 0 | 07:18:2xZ |
| D | fixture sizes at rev via `git show … \| wc -c` | 0 | 07:18:2xZ |
| E | `git clone --shared <lane> cA && git -C cA checkout c79bbe7b`; `python3 -I -B cA/tools/round-34/c2-shortcut-gate-counter.py --root cA --rev 0000000000000000000000000000000000000000 --json-out P1-bogus-rev.json` | **0** | 07:19:04Z |
| F | clone `cB`; remove 3 shortcut classes from `gate-config-mini.json`; same counter, `--rev c79bbe7b…` | **0** | 07:19:16Z |
| G | clone `cC`; append no-op comment to `structural.py`, newline to `gate-config-mini.json`; same counter | **0** | 07:19:17Z |
| H | `python3 -I -B cA/tools/round-34/freeze-integrity.py --root cA --round 34/r34b --rev c79bbe7b…` (also with explicit `--claims`) | **3** | 07:19:39Z |
| I | `… freeze-integrity.py --root cA --round 34 --rev c79bbe7b…` | **0** (`CLEAN pins=21`) | 07:19:48Z |
| J | predicate identity matrix (claims vs both configs vs counter constant vs receipt) | 0 | 07:20:0xZ |

Receipts: `P1-bogus-rev.json`, `P2-dropped-classes.json`, `P3-noop-tamper.json`, `pin-audit.json`
in the scratch dir above. No tool was installed or upgraded; nothing to record.

## 3. Corroborating checks that passed

- **Live bytes are the audited bytes.** `HEAD == c79bbe7b0959132b9873ff3431cf5eb313b58b33`;
  `git status --porcelain` shows only untracked receipt dirs (`r34b/after`, `before`, `controls`,
  `w1/`, …) — no tracked-file drift. Re-hashing the 26 pinned paths from the worktree gives 26/26
  `SAME`.
- **The pins audited are the frozen pins.** `claims.json` on disk and `git show c79bbe7b:…claims.json`
  are the same blob, `sha256 de3afbfb61d70fee177392b256719bb665ad07d999303999381442120facd828`.
- **Freeze ordering.** `claims.json` and all instruments were added in the *same* commit,
  `c79bbe7b` at `2026-10-25T04:13:11-03:00` (07:13:11Z). Production receipt mtime
  `04:13:24.883-03:00` (07:13:24Z), controls `04:13:52-03:00` — i.e. after the freeze, as claimed.
- **`before` state is true.** At base `ec3125ad…`, `replay-gate.py`, `c2-shortcut-gate-counter.py`
  and `mini-fix/spec.json` are all `ABSENT` (`git cat-file -e`); the before receipt's
  `finding=gate_absent` at `ec3125ad…` matches.
- **Pin-set hygiene.** 26/26 digests distinct (no copy-paste aliasing); every pin path relative, no
  `..`; every pinned entry is a regular blob at the rev (modes only `100644`/`100755` — no symlinks,
  no submodule gitlinks). All eight fixtures are exactly 512 bytes.
- **Runtime reader closure is closed.** Registered readers (8: `structural` + 7 shortcuts in both
  configs) ⊆ pinned readers (9); nothing is registered that is not pinned. The fixture set is driven
  by the keys of the pinned `expected.json` (`mini-fix/mini-counter.py:102-111`), not by a directory
  glob, so no unpinned file can enter the scored set by enumeration.
- **Control receipts are controls, not production.** All five record `gate_path` under
  `.ufo/waves/round-34/r34b/controls/gates/` (or `absent-gate.py`), `met_target=false`; verdicts are
  the four planned `MISS` shapes plus `do-nothing` `UNEVALUABLE`/exit 2, with the failing clauses named
  (`red_refused`, `selftest_clean`, `mutants_killed`). The production receipt alone records
  `gate_path = tools/round-34/replay-gate.py`.
- **Independent reproduction.** On pristine clone `cA` at `c79bbe7b` the counter emitted
  `GATE_COUNTER_OK … selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED
  green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`, exit 0 — byte-identical verdict
  line to the production receipt's clauses.
- **`scores_unchanged.depth`** is consistent with `SCORECARD.md:24` (`depth | 10 → 10`).

## 4. Findings

### F1 — HIGH — the 26 pins are declarative only: no instrument enforces or can verify them

The pin map lives at `claims[0].pins`. Nothing reads it:

- `c2-shortcut-gate-counter.py` checks *presence* only —
  `gate_present: (root / args.gate).is_file()` (line 74) and
  `missing = [path for path in CONFIGS.values() if not (root / path).is_file()]` (line 83). No digest
  is computed anywhere: `grep -c hashlib` → `replay-gate.py:0`, `c2-shortcut-gate-counter.py:0`,
  `naive-counter.py:0` (the 3 hits in `mini-counter.py` are opaque-path naming, lines 114/127).
- The lane's own strict pin verifier cannot see this document at all:
  `freeze-integrity.py:92-98` requires a top-level `instruments` object and the r34b claims file has
  none —
  `freeze-integrity: ERROR schema code=instruments_missing claims=.ufo/waves/round-34/r34b/claims.json where=instruments`,
  **exit 3** (probe H, both with `--round 34/r34b` and with explicit `--claims`).
- The only file the verifier *does* accept is `.ufo/waves/round-34/claims.json` (top-level
  `instruments`, 21 pins) and it verifies `CLEAN pins=21 freeze=54a87a51a865 rev=c79bbe7b…`, exit 0
  (probe I) — but its three `tools/round-34/*` pins are the **inherited R34-C1** instruments
  (`elf-version-needs.py`, `freeze-integrity.py`, `version-needs-counter.py`). It pins **zero** R34-C2
  instruments; the two maps overlap on nothing under `tools/round-34/`.

Proof the gap is exploitable (probe G): appending a no-op comment to `readers/structural.py` and a
newline to `gate-config-mini.json` moves their digests to
`e3e578f909f112671c14264cd74692ac9a1fc41f19aa4bccceda9468df77a40a` and
`b42671e1942eaaaa28d2ea9a6f1657713769f1eb67996cb33e8c2b62a58de54f` (pins: `2f399cab…`,
`4483f385…`) and the counter still prints `GATE_COUNTER_OK`, exit 0, all six clauses true. Byte drift
of any pinned instrument — including the gate itself — is invisible to every lane instrument. Today
the freeze holds because `HEAD` is the frozen commit and the worktree is clean (verified here); the
guarantee is manual, and this report is the only digest check that exists.

### F2 — HIGH — the kill_rule's "no shortcut class may be dropped to reach CLEAN" is not instrument-enforced

`kill_rule`: "…no shortcut class may be dropped to reach CLEAN." Probe F: starting from the frozen
green config I removed `all-false`, `size-keyed`, `fixed-slice`, leaving four classes — above the
gate's own floor `MIN_SHORTCUTS = 3` (`replay-gate.py:31`, enforced at line 58). Result:

```
GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3
red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-
exit 0   met_target true   green.shortcuts_below_target = 4
```

with the green config's digest at `7e60adcee421bae1e7faa991ecfb33e396ed2fcd6775db80fac7a9f02ea93977`
(pin `4483f385…`). No clause compares the executed class set to a frozen set; the counter has no
expected-count or expected-name check, and `MIN_SHORTCUTS = 3` silently permits dropping up to four of
the seven registered classes. The drop *is* observable in the receipt field
`green.shortcuts_below_target` (7 → 4) and in the gate's `rows`, but only to a reader who already
knows the answer is 7 — no clause fails. Any future run of this counter from a modified tree can reach
`CLEAN` on a narrowed shortcut population and still satisfy every frozen clause. F2 is a consequence
of F1: with the config pin enforced, the drop would be caught before scoring; as shipped, nothing
catches it.

### F3 — MEDIUM — `predicate_identity` is false as written

`claims.json` `predicate_identity`: "The same sentence is the gate config's `predicate` field, the C2
counter's PREDICATE constant and the receipt label."

Measured (probe J): the sentence is **not** the same.

| locus | length | sha256 (16) |
|---|---|---|
| `claims.json` `claims[0].predicate` | 237 | `7c6c17f0cca6c680` |
| `gate-config-mini.json` `predicate` | 237 | `7c6c17f0cca6c680` |
| `gate-config-naive.json` `predicate` | 237 | `7c6c17f0cca6c680` |
| `c2-shortcut-gate-counter.py` `PREDICATE` (line 23) | 351 | `8340aea51154fc0e` |
| `after/c2-at-instruments.json` `predicate` | 351 | `8340aea51154fc0e` |

The identity holds config↔claims and counter↔receipt; it fails claims↔counter. The counter constant is
a *different, narrower* statement (it names the label-keyed red case and the "eight fixtures" green
surface — `PREDICATE = ("P34-shortcut-replay: the committed replay gate refuses the shape-only
counter whose " … )`, line 23). No clause reads `predicate`, so this does not change the measured
verdict, but the frozen claim asserts a byte identity that does not hold and should not be restated by
any downstream seat as fact.

### F4 — LOW — declared `target` is not the target the instrument carries

`claims.json` `target` has five fields including `green_positive_matched: 8`; the counter's `TARGET`
(lines 28-29) has four — `green_positive_matched` is absent and the 8 is enforced by a literal
`receipt["green"]["positive_matched"] == 8` in the clause. The production receipt's `target` block
therefore cannot corroborate the declared fifth field, and an edit of that literal to another value
would leave `claims.json`'s target and the counter's TARGET mutually consistent while disagreeing with
the clause. Behaviour today is correct (positive matched = 8, probe E); the shapes simply do not line
up field-for-field.

### F5 — LOW — one pinned reader is registered nowhere (dead pin)

`tools/round-34/mini-fix/readers/label_keyed.py` (`f727c152…`) is pinned but appears in **neither**
config's `shortcuts`/`positive_control` and is referenced nowhere under `tools/round-34/`
(`grep -rn label_keyed tools/round-34/` → no hits). Effect is harmless — the pin set is a superset of
the executed set, which is the safe direction — but two consequences deserve recording: the "eight
readers" phrasing counts *executed* readers (8) while the pin map freezes nine; and the dead pin can
never fail, because nothing loads it.

### F6 — INFO — `--rev` is an input echo, not a measurement

`receipt["measured_revision"] = args.rev` (line 73); the value is never compared to `HEAD`, to the
worktree, or to any pinned digest. Probe E: `--rev 0000000000000000000000000000000000000000` at
`HEAD = c79bbe7b` still yields `measured_revision 0000000000000000000000000000000000000000`,
`met_target true`, exit 0. So the production receipt's `measured_revision: c79bbe7b…` is the operator's
declaration. It happens to be true — I verified `HEAD` and a clean tracked worktree independently — but
the receipt cannot demonstrate it on its own, and neither can it demonstrate the bytes were the pinned
ones (F1).

## 5. Residual risk

- **Freeze integrity is a manual invariant.** F1/F6 mean the frozen instruments are protected only by
  the fact that the lane's tree has not moved since `c79bbe7b`. The round-level strict verifier covers
  R34-C1 only. A successor round should move the R34-C2 pins into the schema `freeze-integrity.py`
  accepts (top-level `instruments`) or teach that verifier the `claims[].pins` shape, and have the C2
  counter compare each instrument digest to the pin map before scoring (refuse with
  `pinned_digest_mismatch`, exit 2).
- **Class-dropping is detectable only by reading `shortcuts_below_target`.** F2 needs either an
  expected-class-set check or a clause pinning the count at 7 (and `MIN_SHORTCUTS` raised to match).
- **The two predicate sentences will be quoted as one** unless F3 is carried into the round record;
  the counter's statement is the stronger and narrower one, the config/claims sentence the weaker.

## 6. Verification gaps (stated, not papered over)

- I did not verify the *semantics* of any reader (structural vs shortcut) or that the eight fixtures
  actually encode the record chains in `expected.json`; that is the gate's and other seats' surface.
  I verified bytes, closure, and the claim's declarations against instrument bytes.
- The R34-C1 production reader and its twelve carriers were not executed or scored; the round-level
  `freeze-integrity` CLEAN (probe I) merely hashes their bytes, which is a file read, not a run.
- `git status` shows untracked receipt dirs only; I did not inspect every untracked file in
  `.ufo/waves/round-34/r34b/` beyond the receipts named in the assignment and the control set.
- Checks I ran are listed with exit codes in §2. Nothing unrun is presented as passed.

**VERDICT: PIN_AUDIT PASS on bytes — 26/26 pins match at c79bbe7b0959132b9873ff3431cf5eb313b58b33, 0
mismatched, 0 missing; the freeze does NOT hold as an enforceable property (F1, F2: digest drift and
shortcut-class dropping both reach `GATE_COUNTER_OK`/exit 0), and one frozen assertion is false (F3:
`predicate_identity` conflates a 237-byte and a 351-byte sentence). C2's measured clauses reproduce;
its anti-drift guarantee rests on manual audit only.**
