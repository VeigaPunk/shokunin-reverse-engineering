# ExecSweep command log — round-72 w1 (seat ExecSweep, 2026-11-04)

Every command executed by this seat, in order, with exit code. Full stdout/stderr retained
per command in the sibling `*.out` / `*.err` / `*.rc` files and aggregated in `sweep.json`.
All commands run with cwd = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` except where noted.
Scratch root: `/fast/scratch/hyaku/kaidoku-r72/ExecSweep` (created once, deleted before yield).

| # | command | rc | receipt |
|---|---|---|---|
| 1 | `git status --porcelain` | 0 | sweep.json (`git-status`) |
| 2 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `sources-census.out/.err/.rc` |
| 3 | `python3 -I -B tools/round-71/registry-census.py --root . --rev 56241b1c8baff95862730c008f1ae5132b03388e --generate --out /fast/scratch/hyaku/kaidoku-r72/ExecSweep/registry.json` | 0 | `registry-census.out/.err/.rc` + `registry.json` |
| 4 | `python3 -I -B tools/round-72/packed-elf.py --selftest` | 0 (35 cases, 0 failed) | `selftest-packed-elf.out/.err/.rc` |
| 5 | `python3 -I -B tools/round-72/seam-probe.py --selftest` | 0 (10 cases, 0 failures) | `selftest-seam-probe.out/.err/.rc` |
| 6 | `python3 -I -B tools/round-72/mutation-check.py --selftest` | 2 (no --selftest mode; argparse usage error) | `selftest-mutation-check.out/.err/.rc` |
| 7 | `python3 -I -B tools/round-72/capsule-audit.py --selftest` | 0 (13 cases, 0 failed) | `selftest-capsule-audit.out/.err/.rc` |
| 8 | `python3 -I -B tools/round-72/capsule_audit.py --selftest` | 0 (silent; library module, no CLI) | `selftest-capsule_audit.out/.err/.rc` |
| 9 | `python3 -I -B tools/round-72/controls.py --selftest` | 2 (no --selftest mode; required-args usage error) | `selftest-controls.out/.err/.rc` |
| 10 | `python3 -I -B tools/round-71/registry-census.py --selftest` | 0 (14 cases, 0 failures) | `selftest-registry-census.out/.err/.rc` |
| 11 | `python3 -I -B tools/round-70/packed-elf.py --check-receipt .ufo/waves/round-72/l1/pre/route-at-declaration.json --root . --rev 6316c1053f927a1a1cdc3e0960b70acab5f56381` | 1 (expected producer-binding rejection; R72 receipt offered to the R70 checker) | `receipt-audit-r72.out/.err/.rc` |
| 12 | `python3 -I -B tools/round-72/mutation-check.py --root . --rev 6375afe687bc03603eab8387f2defc4fa1248054 --tool tools/round-72/seam-probe.py --patch-set r72 --work /fast/scratch/hyaku/kaidoku-r72/ExecSweep/mc-work --json-out /fast/scratch/hyaku/kaidoku-r72/ExecSweep/mutation-check-r72.json` | 0 (mutant killed naming a10-binding-from-checker; survivors 0) | `mutation-check-r72.out/.err/.rc` + `mutation-check-r72.json` |
| 13 | no-/tmp scan via regex search over `tools/round-72/*.py` + per-file literal count | — | counts in ExecSweep.md §2 (capsule-audit 1, capsule_audit 0, controls 0, mutation-check 0, packed-elf 6, seam-probe 5) |

No git/jj write commands, no pacman, no tool installs. Only writes: this directory,
`../ExecSweep.md`, and the scratch root (deleted).

Report: .ufo/waves/round-72/w1/ExecSweep.md
