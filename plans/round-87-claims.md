# kaidoku — round 87 claim declaration (frozen before data)

Round 87, attempt 1. Base `99f8b6a8979978fe02dc3c8f674ce4fdee3ab44b` (lane tip at round start; the
round-86 non-author spot-check commit). Lane axes: coverage, depth, calibration — all at 10.0 on
their finite proxies. Coverage is tied-lowest and is worked here. No stagnation waiver: round 84
entered capability rows, so the 10-round window has not lapsed.

**One claim.** Rounds 85 and 86 were rejected on claims about the lane's own records. The round-86
spot-check routes SHONEN box 2 ("no end-to-end domain task this round") and V86-1 (claims on an
unowned axis). This round declares one domain claim on an owned axis: a PROVINCE Frontier class
moves to Core by a measured end-to-end reverse-engineering task. No second claim is declared;
the routed record defects (V86-6, V86-7) stay named debt, not claims.

---

## R87-C1 — coverage (capability) — UPX-packed ELF whose `UPX!` magic words are tampered

**Surface (named by surface, not by number):** the Frontier line of `corpus/README.md` § Frontier
(round-68 note) "still Frontier: any other packer, an anti-UPX stub whose magic or entry is altered".
The lane's packed-ELF route (rounds 68–73) recovers a UPX-packed carrier only while the packer's
markers are intact. A packer-tampered file still RUNS (observed: `jq.t1 --version` prints
`jq-1.8.2` with every `UPX!` word zeroed) while `upx -t`, `upx -l` and `upx -d` answer
`NotPackedException: not packed by UPX`. This claim moves the magic-altered edge class (not the
entry-altered one, not another packer) from Frontier to Core with a new tool,
`tools/round-87/upx-magic-repair.py`, that restores the magic words from the packer's own
structures and nothing else.

**Population (frozen in the counter):** the four round-70 carriers (`jq`, `xxd`, `libz.so.1.3.2`,
`docker-init`; sha256-pinned, kinds executable/executable/shared-object/static-exe) packed with the
pinned packer (`upx --best`, UPX 5.2.0, sha256 `cf2f6e7c…c969`), each tampered two ways:
`T1-zero` (every `UPX!` word → `00 00 00 00`) and `T2-foreign` (every `UPX!` word → `KDK!`). 8 cases.
Precondition per case: `upx -t` on the tampered file exits non-zero, else exit 2.

**Predicate (frozen sentence, repeated verbatim in `claims.json` and as the receipt label):**

> `tools/round-87/upx-tamper-battery.py --repair-cmd tools/round-87/upx-magic-repair.py` reports
> `recovered 8 of 8` with `controls_ok` all true and exit 0, where a case is recovered only when the
> repair exits 0, changes bytes only inside windows that now read `UPX!`, `upx -t` passes, `upx -d`
> restores the carrier's pinned sha256, and REA 6.5.0 `analyze` of the restored bytes reports the
> carrier's declared original procedure count.

**Target:** `recovered` 0 of 8 (no repair; do-nothing control) → 8 of 8 at the measured revision,
with controls N1 (repair refuses each plain original, 4/4), N2 (T1 tamper plus one flipped payload
byte is never recovered, 0/4) and N3 (an intact packed file is left byte-identical, 4/4).

**Kill rule:** recovered < 8; any control false; a case recovered through a change outside a
`UPX!` window; a repair that names, reads or hashes any carrier source path or pin (it must take
only `--in`/`--out`); a counter, population, tamper value, arm or control changed after this
declaration (the counter is pinned by sha256 in `claims.json`); REA package pin drift.

**Counting command (the closure's one command):**

```sh
python3 -I -B tools/round-87/upx-tamper-battery.py --root . \
  --repair-cmd tools/round-87/upx-magic-repair.py --upx /usr/bin/upx \
  --pkg <rea-agents 6.5.0 package dir, package.json sha256 a5003023…0a6c> \
  --work <scratch> --json-out <receipt>
```

**Controls scored before the freeze (committed with this declaration):**

- Do-nothing (`--repair-cmd identity`, input copied unchanged — what `upx -d` sees with no repair):
  `.ufo/waves/round-87/pre/c1-control-identity-at-base.json` → `recovered 0 of 8`, exit 1.
- Cheap rule (`--repair-cmd naive-global`: replace every occurrence of the 4 bytes at `len-36` with
  `UPX!`): `.ufo/waves/round-87/pre/c1-control-naive-global-at-base.json` → `recovered 4 of 8`
  (all four T2 cases; every T1 case fails `upx -t` with `bad e_phoff`), N1 false (it refuses
  nothing), exit 1. The target is therefore failable by the cheap rule: it needs the zeroed
  class, which only a structural repair reaches.
- Counter selftest: `python3 -I -B tools/round-87/upx-tamper-battery.py --selftest` →
  `SELFTEST cases=8 failures=0`.

**Named limit (declared now):** the counter scores bytes, not provenance. A "repair" that re-packed
the original carrier would emit the same correct bytes; the kill rule's "names, reads or hashes any
carrier source path or pin" clause is checked by review of the repair source, not by the counter.

**Sources (frontier step; opened this round before the knowledge entry cites them):** UPX v5.2.0
`src/stub/src/include/linux.h` (`struct l_info`, `struct p_info`, `struct b_info`) and
`src/p_unix.cpp` (the end-of-chain `b_info` whose `sz_cpr` is the magic; `sz_cpr must be h->magic`),
both at `https://raw.githubusercontent.com/upx/upx/v5.2.0/…`.

**Capability row (enters only on a passing demonstration):** `UPX magic-tamper repair` —
restores `UPX!` words from l_info/p_info/b_info/PackHeader structure so the pinned packer unpacks
a magic-tampered ELF to its original bytes.
