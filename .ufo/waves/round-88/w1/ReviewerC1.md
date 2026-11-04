# ReviewerC1 — R88-C1 scoped findings (round 88, kaidoku, 2026-11-04)

Full report with commands, tables and receipts: `.ufo/waves/round-88/w1/ReviewerC1/report.md`.
All numbers below were measured this session with the frozen counter
(`tools/round-88/upx-chain-battery.py`, sha256 `a01ed622…` verified equal to the
`claims.json` pin; lane HEAD `d190c5b57`, tracked tree clean). No tools installed.

**Claim verdict: SOUND** — rerun of the frozen counter on
`tools/round-88/upx-chain-repair.py` reproduced `recovered 4 of 4`, controls
N1/N2/N3 all true, regression `8 of 8` met, exit 0. Independent fixtures measured true
block0 `sz_cpr` jq 252 / xxd 249 / libz 201 / dinit 226; the repair derives exactly
those and its outputs are byte-equal to the clean packed files (libz accounts 98,592 of
u_len 108,560 — named limit 1 confirmed).

**Findings**

1. **Counter limit (forgeable label).** A packer-oracle repair (`R7`) — ascending
   structural candidate fills, keep the first that makes `upx -t` pass, no chain
   geometry — scores `recovered 4 of 4`, controls true, regression 8/8, exit 0, with
   outputs byte-identical to the claimed repair on all four carriers. Cost: 1 upx call
   per carrier (2 on dinit). Named limit 3 admits carrier-repack provenance blindness;
   R7 is cheaper and needs no carrier at all. The "names/reads/hashes a carrier source
   path or pin" kill clause is audit-only and does not cover this. Exact command in the
   full report §3; script kept at
   `.ufo/waves/round-88/w1/ReviewerC1/attacks/rules/R7-oracle.py`.
2. **No cheaper structural rule passes.** All scored by the frozen counter, controls
   true everywhere: first-plausible-no-sentinel `3 of 4`; u_len-key-without-sentinel
   `3 of 4`; sentinel-only-smallest `3 of 4`; `sz_cpr := p_blocksize` `0 of 4`;
   `sz_cpr := c_len − 12·blocks` `0 of 4`; global scan-and-fill `0 of 4`. The only
   separator is dinit, which carries a sentinel-reaching decoy at derived = 136 inside
   block0's payload (`upx -t`: `compressed data violation`); on jq/xxd/libz the first
   structural candidate already equals the truth. The capability is one carrier deep.
3. **Regression arm is class-blind.** An r87-class-only repair (real path, no geometry)
   scores regression `8 of 8` met, rc 0, while the main class is `0 of 4` — measured.
   The regression arm contributes no evidence about the T3-chain class.
4. **`field_only` passes under a no-op** — the frozen identity control receipt shows
   `field_only: true` on all four carriers. It certifies nothing alone.
5. **Plan-prose drift (3 items).** (a) The claim sentence's "the **smallest** offset …
   whose own chain reaches the sentinel yields `sz_cpr`" is falsified on dinit (R3:
   136, `upx -t` fails); the operative rule is the u_len-accounting winner, as the code
   and the prompt one-liner implement. (b) "under block0's method" — the code also
   accepts the PackHeader's method; unexercised on this population (m0 == ph.method
   measured 2/2/2/8). (c) "a candidate claiming more than `u_len` is impossible" — the
   code deprioritizes via the `fits` key but does not reject. Label/arms/control keys
   otherwise match the predicate word-for-word.
6. **Counter wart.** For builtin `--repair-cmd` values (identity/naive-global/
   r87-anchor) the regression arm is unevaluable, not measured (builtin name passed as
   a path to the r87 counter → `missing_repair`, rc 2; visible in
   `c1-control-r87-anchor-at-base.json`). No plan falsehood, but the r87-anchor control
   never exercised the regression arm.

**Files written**

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1/report.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1/attacks/{build.py,vcommon.py,manifest.json}`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1/attacks/rules/R{1..8}*.py`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-88/w1/ReviewerC1/attacks/results/{claimed,R1-first-plausible,R2-ulen-no-sentinel,R3-sentinel-only-smallest,R4-pblocksize,R5-clen-12n,R6-global-scanfill,R7-oracle,R8-r87-only}.json`
