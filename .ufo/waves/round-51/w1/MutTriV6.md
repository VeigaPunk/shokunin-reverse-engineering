# MutTriV6 — round 51 wave 1 (build)

**Verdict: the v6 mutation battery is specified and every table-scope expectation is
MEASURED (not asserted); the two code-guard mutants cannot be executed yet because no v6
instrument exists (`ExecTriV6`'s draft is still a byte-copy of v5).**

Deliverables: `.ufo/waves/round-51/w1/MutTriV6/battery.md` (the spec),
`.ufo/waves/round-51/w1/MutTriV6/probe/` (4 probe scripts + their JSON + stdout/stderr),
`.ufo/waves/round-51/w1/MutTriV6/receipts/probe-receipts.tsv` (command, exit, stdout
sha256, UTC).

## The three findings that change what the L1 freezes

1. **The v5 carryovers do NOT all keep their round-50 numbers under v6 — two of them
   change by +1, and freezing the old numbers would fire the kill rule spuriously.**
   Measured over the round-50 control surfaces with the v6 evaluator: do-nothing
   **19 → 20**, action-swapped **51 → 52**; guard-deleted **26 → 26** and junk
   **126 → 126** hold. The v5 evaluator reproduces the committed receipts exactly
   (19/26/51/126), so the baseline is confirmed. The +1 is the ddwrt route change
   itself (`dmg_Z3_v3ddwrt_inode_table`). **Freeze 20 and 52.**

2. **Precedence is load-bearing, and the wrong order makes a required control a NO-OP.**
   Measured: with the new `legacy-body-unreadable` row **below** `legacy-body-failure`,
   the "ddwrt glob broadened back into `legacy-body-failure`" mutant flips both
   detectors (D1=1, D2=1); with the new row **above**, the same mutant is **GREEN
   (0/0)** — nothing observes it, so the guard around it is dead. The port must also
   drop `squashfs_v3_ddwrt` from the legacy row's failing-handler cell.

3. **The executability audit alone is NOT a complete guard, and the deleted-guard
   mutants are no-ops without a fail-closed gate.** Measured: deleting the new row
   flips the pair detector (1) but leaves the audit at **0** (the body falls to
   `preserve-failure`, which prescribes no cross-read) — so a coordinated table+evaluator
   mutation is invisible to both. And deleting the audit code, or the census check,
   would report "0 violations / 0 outside" and go green unless the instrument fails
   closed (receipt key required + verdict refused without the detector + a
   clone-and-delete selftest case). The audit's own reader census is a new trust
   boundary: flipping it disables D2 silently and needs its own binding to the
   round-49 `v3-readers` receipt.

Also measured and reported: the **before-arm** at `1aa27369…` (= `f04b51dd…`, same
SKILL.md bytes) is D1(v5)=0, D1(v6)=1, **D2=1 naming `dmg_Z3_v3ddwrt_inode_table`**,
**D3=13** (55 registered, 42 in `census2.json`) → exit 1, exactly as the claim says;
and two landmines — the before-arm cannot carry the round-51 `--freeze` (the v5
instrument refuses a non-ancestor freeze, exit 2), and `census3.json` must be derived
from the **staged** freeze SKILL.md, or the freeze scores D3 = the number of new
round-51 registry rows.

Not run: no REA, no data run, no downloads, no lane write outside this seat directory,
no git mutation. Tools installed: none.

## Mistake (mine, disclosed and repaired) — fleet-root stray, M50-9 class

* **class**: seat path composition — a hand-built absolute path dropped the
  `kaidoku-shokunin/` component, so a seat's own artifacts were written into the
  **FLEET** repo at `/home/vgpnk/Projects/shokunin/kaidoku-r51/w1/MutTriV6/` instead of
  the lane seat dir (17 files: 4 probe scripts, 4 stdout, 4 stderr, 4 JSON, 1 TSV).
* **evidence**: `git -C /home/vgpnk/Projects/shokunin status --porcelain` showed
  `?? kaidoku-r51/` (5 dirs, 17 files) after the probe run; the lane seat dir held only
  `battery.md`. All 17 files were copied **byte-exact** into
  `.ufo/waves/round-51/w1/MutTriV6/` and `cmp`-verified (`cmp` rc=0 for all 17; the two
  sha256 manifests match pair for pair — the fleet-side and lane-side
  `sha256sum` listings are identical). The fleet copy was then deleted (the one
  permitted fleet deletion) and `git -C /home/vgpnk/Projects/shokunin status
  --porcelain` is **empty** again.
* **captured-by**: MutTriV6.
* **fix**: the lane seat path is now the single source
  (`.ufo/waves/round-51/w1/MutTriV6/`); the probe scripts and their receipts are
  committed there. The L1 should append the matching row to
  `corpus/lessons/round-51.md` `## Mistakes` (class · evidence · captured-by · fix)
  and may fold it into the `tools/round-51/misroot-sweep.sh` control's fixture set:
  **the stray is detected by content, and its path (`kaidoku-r51/w1/<seat>`) is
  distinguishable from a lane path only by the missing `.ufo/waves/round-51/w1/` prefix
  — the sweep must classify on the `kaidoku`/`round-51` content, not on the prefix.**
