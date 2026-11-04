# ExecGeomCross — R88-C1 independent geometry re-derivation

Seat: `ExecGeomCross` (executor), wave `r88-w1`, round 88, lane `kaidoku`.
Claim under test: **R88-C1** (coverage/capability) — chain-geometry repair of a zeroed first
`b_info` `sz_cpr`. Lane axes: coverage, depth, calibration.

**Verdict: agreement 4/4.** My from-scratch derivation reproduces the committed repair's
`sz_cpr` on every pinned carrier, and on all four it recovers exactly the pre-tamper value.
No carrier contradicts the claim. Two findings qualify the *wording* (F1) and the *calibration*
(F2) of the frozen plan; neither breaks the measured predicate.

## What I ran (exact commands)

```
/usr/bin/upx --best -o /fast/scratch/.../pack/<name>.packed /fast/scratch/.../pack/<name>.orig
python3 geomx.py inspect pack/jq.packed pack/xxd.packed pack/libz.so.1.3.2.packed pack/docker-init.packed
python3 geomx.py derive /usr/bin/jq                 <workdir>/jq            --repair-tool <lane>/tools/round-88/upx-chain-repair.py
python3 geomx.py derive /usr/bin/xxd                <workdir>/xxd           --repair-tool ...
python3 geomx.py derive /usr/lib/libz.so.1.3.2      <workdir>/libz.so.1.3.2 --repair-tool ...
python3 geomx.py derive /usr/bin/docker-init        <workdir>/docker-init   --repair-tool ...
python3 validate_committed.py        # python3 -I -B tools/round-88/upx-chain-repair.py --in <tampered> --out <out> --json
python3 summarize.py                 # -> cross.json
/usr/bin/upx -t <file> ; /usr/bin/upx -d -o <out> <file>
```

Every carrier copy was `cp`'d into scratch and packed there; the host objects were never modified
(`sha256sum` of `/usr/bin/jq`, `/usr/bin/xxd`, `/usr/lib/libz.so.1.3.2`, `/usr/bin/docker-init`
match the seat's pins after the run).

## Method (independence)

`geomx.py` was written for this seat and **imports neither `tools/round-88` nor `tools/round-87`**
(it is a single stdlib-only file; `summarize.py` imports `geomx.py`, not the lane's tools).
Disclosure: I read the round-87 module's docstring for the on-disk structure definitions before
writing; the code paths are mine and the anchor selection differs (see below).

* **PackHeader** — last 32-byte window in the file tail where `byte[31] == sum(byte[4:31]) % 251`,
  `10 <= version <= 20`, non-DOS format, `u_len > 0`, `0 < c_len <= size`, `u_file_size > 0`.
  Found at 14000 / 19524 / 65544 / 357748.
* **l_info** — located from **its own `UPX!` magic word** (a different anchor from the committed
  tools, which locate it from the `p_filesize == u_file_size` redundancy), validated by
  `l_version`/`l_format` against the PackHeader and `p_filesize == u_file_size`.
  A second, `u_file_size`-anchored locator is implemented as a cross-check: **both locators return
  exactly one candidate and agree on all four carriers**, and both match the committed tool's
  `geometry.l_info` (556 / 556 / 9284 / 556) and `geometry.block0` (576 / 576 / 9304 / 576).
* **b_info chain** — own `block_at`/`walk`/`is_sentinel`/`reach`: a block is plausible when
  `0 < sz_cpr <= sz_unc`, it fits before the PackHeader and its method is in
  `{block0.method, PackHeader.method}`; the sentinel is `sz_unc == 0` with `method/ftid/cto8/unused`
  zero; where a run stops short of the sentinel the walk resumes at the best later offset whose own
  run ends at one.
* **Rule** — `sz_cpr0 = candidate - (b0 + 12)` over every plausible offset above `b0 + 12` whose
  patched chain reaches the sentinel, `0 < sz_cpr <= sz_unc0`; winner by
  `(fits_u_len, accounted total, -derived)`.

## Results

| carrier | packed | b0 | sz_unc0 | intact `sz_cpr` | **derived** | committed | agree | offsets scanned | structural | sentinel-reaching | others passing `upx -t` | others passing `upx -d` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `/usr/bin/jq` | 14,036 | 576 | 904 | 252 | **252** | 252 | **true** | 13,399 | 1 | 1 | 0 | 0 |
| `/usr/bin/xxd` | 19,560 | 576 | 904 | 249 | **249** | 249 | **true** | 18,923 | 1 | 1 | 0 | 0 |
| `/usr/lib/libz.so.1.3.2` | 65,580 | 9,304 | 680 | 201 | **201** | 201 | **true** | 56,215 | 1 | 1 | 0 | 0 |
| `/usr/bin/docker-init` | 357,784 | 576 | 736 | 226 | **226** | 226 | **true** | 357,147 | 3 | 3 | 0 | 0 |

Totals: agreement 4/4 · derived == intact pre-tamper value 4/4 · 445,684 offsets scanned ·
`upx -t` on the repaired file exit 0 on 4/4 · `upx -d` restores the pinned carrier sha256 on 4/4 ·
the committed repair's output is **byte-identical to the intact packed file** on 4/4 ·
committed `--json` records `upstream_sha256 = 96da7d8e…` (the r87 pin) on 4/4.

Tamper premise confirmed: with block 0's `sz_cpr` zeroed, `upx -t` and `upx -d` both refuse with
exactly `CantUnpackException: b_info corrupted` on 4/4, and write no output.

## Ambiguity evidence

**docker-init is the only carrier with more than one candidate**, and there the rule's ordering is
load-bearing:

| derived | next block | accounted `sz_unc` | vs `u_len` 851,288 | `upx -t` | `upx -d` |
|---|---|---|---|---|---|
| **226** | 814 | **851,288** | equal | **0** | **0**, restores `0bd49c8d…` |
| 440 | 1028 | 850,696 | short by 592 (the skipped block) | 1, `compressed data violation` | 1, same |
| 136 | 724 | 123,942,159 | over by 123,090,871 | 1, `compressed data violation` | 1, same |

Ablation on that candidate set:

* smallest-derived only → **136** (wrong)
* largest-accounted-total only → **136** (wrong, it does not fit `u_len`)
* `fits_u_len` → largest total → smallest derived → **226** (right, and the only value `upx -t`
  accepts)

So on docker-init **both** `fits_u_len` and the "largest accounted total" tie-break are
load-bearing; the packer itself is an independent oracle for the winner.

Neighbourhood probe (±3 around the true value, 7 values × 4 carriers = 28 `upx -t` runs):
**only the true value passes**; every neighbour fails with `compressed data violation`.

## Findings

**F1 — the rule as worded needs the loader-resume step, and the plan does not say so.**
The literal contiguous reading ("the next plausible `b_info` whose chain reaches the end-of-chain
sentinel") yields **zero candidates on 4/4 carriers** (`strict_contiguous_candidates_total = 0`).
In every carrier the `b_info` chain stops at the embedded loader before the sentinel:

| carrier | first-segment stop | resume | sentinel | gap |
|---|---|---|---|---|
| jq | 10,097 | 13,228 | 13,988 | 3,131 B |
| xxd | 15,630 | 18,756 | 19,509 | 3,126 B |
| libz.so.1.3.2 | 60,127 | 62,944 | 63,717 | 2,817 B |
| docker-init | 352,674 | 355,828 | 357,734 | 3,154 B |

The working rule is "the candidate's chain **with loader-resume** reaches the sentinel" — the
round-87 resume walk is a required component of R88-C1, not an incidental detail. The committed
repair and my independent one both do this and both recover 4/4, so the measured predicate stands;
the frozen plan/`claims.json` sentence should be amended to name the resume step.

**F2 — the rule's ordering is only exercised by docker-init; two simpler orderings pick a value the
packer rejects.** See the ablation above. On the other three carriers the structural filter already
yields exactly one candidate, so they carry no calibration weight for the tie-break.

**F3 — "only changed bytes inside the 4-byte window" is measured as exactly one byte.**
The tamper zeroes the whole word, so the restore writes `0x000000FC` and only offset `b0 + 4`
differs from the tampered input (jq/xxd/docker-init: 580; libz: 9308), inside the window
`[b0+4, b0+7]`. The claim's window condition holds; the diff is one byte, not four.

**F4 — `fits_u_len` is an upper bound, not equality.** libz's chain accounts for 98,592 of 108,560
declared bytes (90.82 %); the plan's named limit 1 says exactly this and my independent measurement
confirms it (98,592 ≤ 108,560, so `fits_u_len` true). A rule demanding equality would refuse libz.

**F5 — the method-set arm is not exercised by this population.** docker-init packs with method 8,
the other three with method 2; block 0's method equals the PackHeader's method on all four, so no
mixed-method chain appears. The `{block0.method, PackHeader.method}` set is a round-87 arm, not
something these four carriers stress.

**F6 — search cost.** 357,147 offsets scanned on docker-init; the whole four-carrier pipeline runs
in <1 s wall. Consistent with named limit 4 (linear scan of a hostile file).

## Risks / limits of this cross-check

* One tamper class per carrier (`sz_cpr → 0`); non-zero wrong values are not derived (by design).
* "Uniqueness" is bounded evidence: the full structural candidate set plus a ±3 neighbourhood, not
  an exhaustive 2^32 sweep (impossible).
* My derivation shares the PackHeader-checksum law with the committed tool; a tampered checksum byte
  is out of class for both.
* Reading the round-87 docstring for structure layout is disclosed; no code was imported or called.

## Reproducibility

`cross.json` was regenerated from the archived evidence alone after the scratch tree was removed:

```
GEOMX_WORK=<seat>/evidence python3 <seat>/summarize.py
```

and is **byte-identical** to the wave-time copy (`sha256 87c3db5d…a8425`). `geomx.py derive
<carrier> <workdir> --repair-tool <lane>/tools/round-88/upx-chain-repair.py` regenerates the whole
chain from the pinned carriers (pack, tamper, derive, ambiguity, committed comparison);
`validate_committed.py` must run after such a derive with `GEOMX_WORK=<workdir>`.

## Tooling

No installs, no upgrades, no pacman transaction. Host `/usr/bin/upx` 5.2.0, pin
`cf2f6e7c…c969` verified before and after. Python 3 stdlib only.

## Files written

* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross/report.md`
* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross/cross.json`
* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross/geomx.py`
* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross/summarize.py`
* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross/validate_committed.py`
* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ExecGeomCross.md`
* evidence under `.ufo/waves/round-88/w1/ExecGeomCross/evidence/` (inspect.json, four `*.derive.json`,
  neighbourhood.json, committed_validation.json, segments.json, tampered_d.json, losers_d.json,
  diffs.json, summary.txt)
