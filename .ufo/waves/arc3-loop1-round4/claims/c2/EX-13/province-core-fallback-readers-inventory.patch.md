# PROVINCE.md repair — Core "Host fallback readers" row: the absent-tool inventory is falsified

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified first-hand)

`PROVINCE.md` Core table row `Host fallback readers`, final cell, current bytes:

> absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib

Five of those are **present** on this host. First-hand `command -v` sweep
(2026-10-19):

```
7z          /usr/bin/7z          (7-Zip 26.03 x64)
xxd         /usr/bin/xxd         (tinyxxd)
radare2     /usr/bin/radare2     (6.2.0, git.6.2.0 2026-09-04)
strace      /usr/bin/strace      (7.0)
upx         /usr/bin/upx         (5.2.0)
cabextract  ABSENT
rizin       ABSENT
ltrace      ABSENT
paccheck/pactree/pacfiles  ABSENT   (pacman-contrib)
```

Cause, measured: `pacman -Qo` + `pacman -Qi` show all five are owned packages
installed in one batch — `7zip`, `tinyxxd`, `radare2`, `strace`, `upx`, each
`Install Date: Tue 13 Oct 2026 01:52:22 PM -03`. The row was written from an
earlier 2026-10-13 sweep and never re-derived after that install.

The row is falsified **even under a same-day DATED reading**: the admitted
corpus entry `corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md` (verified
2026-10-13) already records "7z 26.03, zstd, binwalk 3.1.0 present" and its
`--show-external-dependencies` table lists `7z` among the present extractors.
`corpus/knowledge/2026-10-13-pe-surface.md` (the row's own source sweep) is the
now-superseded observation — it reads "missing: rabin2, r2, radare2, rz-bin,
mono, monodis, pedump, xxd".

## Change (same-line replacement, line count held at 1)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx | `command -v <tool>` | absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib |
+| Host fallback readers | `file`, `readelf`, `objdump`, `llvm-readobj`, `nm`, `strings`, `unzip`, `tar`, `gdb`, `eu-stack`, `coredumpctl`, `pacman`, `zstd`, `gpg`, `python3`, node/npx; re-swept 2026-10-19: `7z`, `xxd`, radare2, `strace`, `upx` present | `command -v <tool>` | absent: `cabextract`, rizin, `ltrace`, pacman-contrib |
```

## Census conformance

- Line-neutral: 1 → 1 line (a table row); `PROVINCE.md` stays at 162 lines, so
  no declared row boundary moves.
- Needle-free: the replacement adds no `rea-agents@x.y.z`, no bare `6.x.y`
  (the instrument's bare-version regex requires a literal `6.` with a
  non-digit/non-dot lookbehind — `26.03`, `6.2.0`, `5.2.0`, `7.0` do not
  match it), and no `~`/`/`-absolute `path:line`. The version strings were
  therefore kept **out** of the replacement text: the present-tool names carry
  the repair, and the numbers live in this patch text's evidence block.
- This row sits inside the DATED scope row `("PROVINCE.md", 45, 62, "DATED", 45,
  r"2026-10-13")`. The census therefore treats it as a historical record and
  raises no locus for it either way (a prose inventory carries no needle). The
  repair is offered on the reading that a **negative existence claim about the
  host** must not survive its own falsification; if the parent adjudicates the
  DATED class as sheltering it, record **NO-CHANGE with this cause** instead —
  the two dispositions are both defensible and the choice is the parent's.

## Scope note for the parent

This is the one item in this seat's census that falls outside the narrowest
reading of the claim's own words ("every PROVINCE Frontier bullet and
surface-summary claim"): it is a Core-table surface row. It is included because
it is a surface claim about this host that the admitted corpus and a first-hand
sweep both contradict. The six Frontier repairs are the claim-scoped set.
