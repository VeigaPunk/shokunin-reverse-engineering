<!-- Draft: two rows for corpus/README.md. Placement notes are not part of either row.
     State at this seat's read (2026-11-03 23:45): the L1 has already appended a round-69
     Knowledge row at corpus/README.md:120 (the round-68 row now sits at :121); no round-69
     Coverage-map row exists yet. -->

## 1. Coverage-map row

Placement: **missing at this seat's read** — append it after the last row of the `## Coverage map`
table (currently the round-68 row, `corpus/README.md:115`, before the blank line that precedes
`## Knowledge`). `grep -n 'round 69\|Round 69\|round-69' corpus/README.md` matches only the Knowledge
row at :120, so this row is still to be added. Do not edit any existing row.

| UPX-packed ELF route contract (round 69) | `2026-11-03-r69-packed-route-contract` | **Core** — the route's gate becomes falsifiable (a pure `evaluate_carrier()` seam, a 20-case selftest with one false model per arm, and the five round-68 mutation survivors killed, each kill naming its declared case), typed (exit-2 `missing_tool`/`work_unusable`/`packer_mismatch` classes, an enforced UPX 5.2.0 version+sha256 pin, per-carrier `format`/`packing_mode` records, 6 of 6 probe arms) and wider by one carrier class (a pinned packed shared object, `/usr/lib/libz.so.1.3.2`, `carriers_matched 3 of 3` under per-class ceilings, the highest ratio 0.6522); the route's scope is unchanged |

## 2. Knowledge-index row

Status: a row for this entry is already below the delimiter (currently `corpus/README.md:120`, first
data row). This draft is the **corrected replacement** for that row: source cell `S270, S269` — the
`help.cpp`/`main.cpp` code row. Two artifacts currently disagree about `S270`: `corpus/SOURCES.md:187`
(staged, uncommitted) stages `doc/upx.1` as S270, while `corpus/lessons/round-69.md:19-20` and the
landed entry read S270 as the code row with `doc/upx.1:164` as its secondary locator. This draft
follows the lesson/landed-entry reading; landing it requires replacing the staged S270 row with
`row.S270.md` (the scout's validated replacement, `.ufo/waves/round-69/w1/ScoutSource/`). The
alternative is to append the code row as S271 and keep S270 = `doc/upx.1`; then this cell becomes
`S271, S270, S269`. The phrase "default packing" is dropped (the receipt records `upx --best`). Four
cells: entry | topic | source | verified-at.

| `2026-11-03-r69-packed-route-contract` | The packed-ELF route's gate rather than its scope: the `evaluate_carrier()` arm seam and the five mutants a 20-case selftest kills, the typed exit-2 preflight with an enforced UPX 5.2.0 version+sha256 pin and per-carrier format/packing-mode records, and a pinned packed shared object (`/usr/lib/libz.so.1.3.2`) beside the two executables — 3 of 3 carriers under per-class ceilings (ratios 0.0599, 0.101, 0.6522) | S270, S269; `tools/round-69/packed-elf.py`, `mutation-check.py`, `contract-probe.py`; receipts `.ufo/waves/round-69/` | 2026-11-03 |
