# ReviewerC2 — independent re-derivation of R78-C2 (freshness)

Seat: ReviewerC2 (leaf, no dispatch). Date: 2026-11-04. Lane: `kaidoku-shokunin`.
Working tree HEAD at run time: `ffcb47d13f0340f88397af6c8d2707a9554abab3` (the freeze commit).
Instrument identity: `sha256(tools/round-78/surface-recheck.py) =
e7ea1717176f3dce2660a10197056b359311c25c5f2490bf9bfbd256c6681a13` — equals the pin frozen in
`.ufo/waves/round-78/claims.json`. The receipt below is derived from the frozen bytes.

## 1. Battery re-run at base (the counter, re-measured)

Command (from the frozen claim's counting command):

```
python3 -I -B tools/round-78/surface-recheck.py --battery --root . \
  --rev 6205ec8c575fb070243c0c40e34a2b0daacde46a \
  --json-out .ufo/waves/round-78/w1/ReviewerC2/receipt-base.json
```

Exit **1**. Receipt (`receipt-base.json`): `checks_total 8`, `matched 6`, `mismatches 2`,
`unparsed 0`, `unparsed_ids []`, `validate {checks: 8, defects: []}`, `ok false`, `exit 1`,
`checked_at 2026-11-04T09:12:35-03:00`, `instrument.sha256 e7ea1717…` (self-consistent).
Unmatched checks: `omp-rea-disable`, `jdk-version` — exactly the frozen before-arm.
Selftest: `--selftest` → `SELFTEST cases=12 failures=0`, exit 0.

## 2. Independent re-derivation of the two mismatches (different commands than the instrument)

**jdk-version.** Record side: `git show 6205ec8c…:PROVINCE.md | grep -n openjdk` → line 25:
`java -version 2>&1 | head -n 1` returned `openjdk version "21.0.12.1" 2026-08-18`.
Live side: `java -version 2>&1 | head -n 1` → `openjdk version "21.0.13" 2026-10-20`.
**Recorded `21.0.12.1`, live `21.0.13` — mismatch confirmed.**

**omp-rea-disable.** Record side, line 18: "The operator disabled the OMP rea entry for the hyaku
phase (10:12 -03); that rewrite dropped the `enabled: false` key, so **the live OMP file no longer
records the disable**" → the record claims the disable is NOT recorded (parsed claim `False`).
Live side (independent `python3 -c` JSON read, keys only): `/home/vgpnk/.omp/agent/mcp.json` →
`disabledServers: ['rea']` (recorded ⇒ `True`); the `rea` entry carries the package token
`rea-agents@6.7.0` and keys `args/command/env/type` (no `enabled` key). File digest
`fa3517758a5ae4596ac53dfb679b3236b49c88570ab3e099e2ef862251057ab6` (no env contents recorded,
per the round-72 rule). **Record says not-recorded; live records it — mismatch confirmed.**

## 3. Parse audit — recorded text vs the value the parse claims

Matched spans re-derived with the instrument's own regex objects (full dump:
`parse-quotes.txt`). For every check, the recorded text DOES state the value the parse claims:

| check | recorded matched text (base rev) | live line |
|---|---|---|
| devin-rea-pin | ``Devin `rea-agents@6.7.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`)`` | rea args token `rea-agents@6.7.0` |
| omp-rea-pin | ``OMP `rea-agents@6.7.0` (`/home/vgpnk/.omp/agent/mcp.json:8`)`` | rea args token `rea-agents@6.7.0` |
| kimi-rea-pin | ``Kimi `rea-agents@6.7.0` (`~/.kimi-code/config.toml:4126`)`` | rea args token `rea-agents@6.7.0` |
| omp-rea-disable | "no longer records the disable" (RE_DISABLE_ABSENT, 1 hit; RE_DISABLE_PRESENT 0 hits) | `disabledServers: ['rea']` |
| ghidra-version | `application.version=12.1.4` | `application.version=12.1.4` (props) |
| ghidra-dir | `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` | `.bashrc:28` `export GHIDRA_INSTALL_DIR="$HOME/.local/opt/ghidra_12.1.4_PUBLIC"` |
| jdk-version | ``openjdk version "21.0.12.1"`` | `openjdk version "21.0.13" 2026-10-20` |
| java-home | `JAVA_HOME=/usr/lib/jvm/java-21-openjdk` | `.bashrc:29` `export JAVA_HOME=/usr/lib/jvm/java-21-openjdk` |

No check whose recorded text fails to state its parsed value. Latent parse fragilities (not
defects at base): scalar regexes use **first** match — the record carries two occurrences each of
`application.version=` (lines 25, 46) and `JAVA_HOME=` (lines 25, 47), identical today; the pin
map takes the **last** `RE_PIN` match per client — opposite direction, one pin block today.

## 4. Pointer rule — falsified with a fixture repo (scratch, 3 commits, never the lane)

Fixture: temp git repo under scratch, `git rev-parse --show-toplevel` asserted equal to the
fixture dir before each commit; base `PROVINCE.md` copied from `git show 6205ec8c…:PROVINCE.md`.

1. **Foreign file, absolute form** (`4349061b97cd59884060aa096ba64211fdbbe229`): Devin pointer →
   `/home/vgpnk/.config/devin/other.json:7`. → `devin-rea-pin` REFUSED despite pin equality
   (record `6.7.0` == live `6.7.0`), note: `record points at /home/vgpnk/.config/devin/other.json`;
   mismatches 2→3 (`receipt-pointer-probe.json`).
2. **Forged token + do-nothing control** (`34caaaaa53151fad82061407b854161578ea330b`):
   `application.version=8.5`. Typed compare REFUSES it (record `8.5` vs live `12.1.4`, mismatches
   4, `receipt-forged-8.5.json`); `--control token-grep` ACCEPTS it (`matched: true`, live
   `token present` — `8.5` occurs in the same props file as `application.gradle.min=8.5`,
   `receipt-token-grep-forged.json`). The control also reports `omp-rea-disable` matched with
   live `not searched` — it cannot see the disable at all. Both control behaviors are exactly the
   frozen claim's description; the control fails in the declared way.
3. **Wrong file, `$HOME`-relative form** (`701b8179aefc8dcdc80f8506f67f20f055befe4f`): Kimi
   pointer → `~/.omp/agent/mcp.json`. → `kimi-rea-pin` REFUSED, note `record points at
   ~/.omp/agent/mcp.json`, mismatches 5 (`receipt-pointer-tilde-wrongfile.json`) — the comparison
   goes through `expand`+`resolve`, not string equality.

The instrument therefore compares the record's named path against the declared live source and
refuses every wrong-pointer shape probed.

## 5. `checked_at` semantics

Base receipt `checked_at = 2026-11-04T09:12:35-03:00` (offset-bearing local time, seconds
resolution). The record side is pinned by `--rev` (immutable git object), so only the live side
is time-fragile. A live change **after** `checked_at` does not make the receipt false — the
instrument dates it deliberately ("a live value is an observation at the receipt's `checked_at`",
module docstring). But the before-arm's measured numbers (`mismatches 2`, live `21.0.13`, live
`disabledServers: ["rea"]`) are reproducible only while that host state persists: a JDK update or
a config edit that removes the disable changes a fresh battery's counts (e.g. dropping the
disable would make `omp-rea-disable` match). So the base-arm claim is **time-bound**: this
receipt is valid evidence of the observation, and any later verifier must re-run the battery
rather than treat these counts as current.

## Findings

1. **No defect found.** All measured counts match the frozen before-arm exactly; `unparsed 0`;
   `validate` defect-free; pointer refusals, `$HOME`-relative handling, and both control failure
   modes behave as the frozen predicate declares.
2. [low, latent] Scalar parses take the first regex match, pin parses the last; duplicate anchors
   in `PROVINCE.md` currently agree, but a stale historical sentence placed earlier would silently
   win (or a later pin block would overwrite). Not triggered at base.
3. [low] `ghidra-version` reads the props file that the **live** `.bashrc` export names; the
   record's own props pointer (`application.properties:17`, line 25) is never compared. Line-number
   drift is tolerated by design; noted for completeness.
4. [info] `token-grep` scores `omp-rea-disable` as matched whenever the claim parses
   (`matched = claim is not None`) — the disable is invisible to the control by construction; the
   typed compare is the only check that sees it.

## Evidence (all under `.ufo/waves/round-78/w1/ReviewerC2/`)

- `receipt-base.json` — the §1 battery receipt (exit 1, mismatches 2).
- `receipt-token-grep.json` — control on the genuine base record (accepts the disable blindly,
  refuses ghidra-dir/jdk-version tokens).
- `receipt-pointer-probe.json`, `receipt-forged-8.5.json`, `receipt-token-grep-forged.json`,
  `receipt-pointer-tilde-wrongfile.json` — §4 fixture probes.
- `parse-quotes.txt` — §3 matched spans and live lines.

No tool installs were needed (python3 stdlib only); no pacman transactions; no git writes outside
the scratch fixture; scratch `/fast/scratch/hyaku/kaidoku-r78/ReviewerC2-10/` removed at close.
