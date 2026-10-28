# W2Scratch — round 49 wave 2: scratch discipline (read-only pass)

Lane root: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Landing revision 29883d4ec35a31a8393c4ffb220888c44c0bb022. Scope: scratch discipline only. Nothing was deleted, moved, or written under /fast/scratch/hyaku/kaidoku-r49 or /tmp by this seat. I created no `$S`, so there was nothing of mine to remove. Receipts are in `.ufo/waves/round-49/w2/W2Scratch/`.

Time base: `date` reports local time at UTC-3. The local clock and `ls` timestamps are local; UTC is local + 3h.

## Verdict

Scratch discipline is adequate. Capacity is not at risk: `/fast/scratch/hyaku` was 46% used with 434.2G free, and `/tmp` was 21% used with 101.7G free (disk-guard status, exit 0). The root peaked at 35G allocated (`du -h -d 1`, 22:47 UTC) and fell to 14G apparent size by 22:56 UTC. Sibling seats removed their own scratch while this pass ran. I found no round-49 leftovers in `/tmp` and no live process holding round-49 scratch at 22:52 UTC. Two items need L1 attention: the un-measured W2C1Drift fixture tree (removed before I could measure it) and an unattributed 188M `/tmp/cl40`.

## Findings table

Owner is taken from the name prefix. Unprefixed names are inferred to be L1 or wave-1 seats and are not confirmed. "Live" uses the 22:52 UTC `/proc` fd/cwd scan (`owner-live.txt`, sha256 e2a985607e6cf40655ca0afd9c8f5f5fd5fc4b7640f566d110cd75ce62f66709) and the 22:51 UTC `pgrep`. Sizes come from `du -h -d 1` at 22:49 UTC (`du-d1.txt`) and `du -sh` (`du-sh.txt`).

| path | size (22:49 UTC) | owner seat | live process? | safe to delete? |
|---|---|---|---|---|
| /fast/scratch/hyaku/kaidoku-r49/l1 | 10G | L1 (KaidokuR49) | no (fd/cwd scan 0 hits) | Only after L1 lands. L1 removes the root after landing. |
| /fast/scratch/hyaku/kaidoku-r49/l1z | 4.9G | inferred L1 | no | Same as l1. |
| /fast/scratch/hyaku/kaidoku-r49/l1x | 713M | inferred L1 | no | Same as l1. |
| /fast/scratch/hyaku/kaidoku-r49/W2C1Drift | 17G (fx/: 90 fixture entries) | W2C1 (wave-2 drift) | no at 22:52; **gone at 22:53 UTC** | Already removed by its owner. Not measured before removal (see F3). |
| /fast/scratch/hyaku/kaidoku-r49/W2C1Forge | 311M | W2C1 | no | **Gone at 22:53 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/W2C1Receipts | 747M | W2C1 | no | **Gone at 22:53 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/W2C2Forge | 753M | W2C2 | yes at 22:51 UTC: pid 3424730 `python3 matrix.py`, cwd W2C2Forge. Not in the 22:52 scan. | Owner's call after its process exited. Still present at 22:53 UTC. |
| /fast/scratch/hyaku/kaidoku-r49/W2Honesty | 1.5G | W2Honesty | no | Owner's call. Still present at 22:53 UTC. |
| /fast/scratch/hyaku/kaidoku-r49/W2Sentinel | 120M | W2Sentinel | no | **Gone at 22:53 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/W2Consistency | 228K | W2Consistency | no | Owner's call. Still present at 22:53 UTC. |
| /fast/scratch/hyaku/kaidoku-r49/W2Chronology | 1.6M | W2Chronology | no | **Gone at 22:53 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/W2Plan | 2.6M | W2Plan | no | **Gone by 22:50 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/W2Coverage | 3.2M | W2Coverage | no | **Gone by 22:50 UTC** (owner removed). |
| /fast/scratch/hyaku/kaidoku-r49/C1OracleIndep | 188K | unprefixed, wave-1 C1 (inferred) | no | Yes after L1 lands. |
| /fast/scratch/hyaku/kaidoku-r49/C2SourcesReopen | 288K | unprefixed, wave-1 C2 (inferred) | no | Yes after L1 lands. |
| /fast/scratch/hyaku/kaidoku-r49/C1Simplify-ast.py | 4K | unprefixed, wave-1 C1 (inferred) | no | Yes after L1 lands. |
| /fast/scratch/hyaku/kaidoku-r49/counter | 0 | unprefixed (inferred L1) | no | Yes after L1 lands. |
| /fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run | 0 | unprefixed (inferred L1) | no | Yes after L1 lands. |

Root total at 22:56 UTC: 14G apparent (`du -sh --apparent-size`, `root-du-final.txt`). Final listing at 22:53 UTC is in `ls-now.txt` (sha256 f750ac624628e893a4f396c9691ccc95892acbf74eea2f511ddfe27957f8532a).

## Other findings

| # | finding | exact command | exit | receipt sha256 |
|---|---|---|---|---|
| F1 | Scratch root listed at 19:50 local, then 19:53 local. The root moved between the two listings: W2Plan and W2Coverage disappeared by 19:50 local, and W2Sentinel, W2C1Forge, W2C1Receipts, W2C1Drift and W2Chronology disappeared by 19:53 local. Sibling owners removed their own dirs. | `ls -la /fast/scratch/hyaku/kaidoku-r49` at both times (`ls-scratch.txt`, `ls-now.txt`) | 0 | ls-now.txt f750ac62… |
| F2 | disk-guard: `/fast/scratch/hyaku` 46% used, 434.2G free. kaidoku-r49 is the top consumer at 35.2G. `/tmp` 21% used, 101.7G free. | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | disk-guard.txt ff7db0c4… |
| F3 | W2C1Drift held 90 fixture entries under `fx/`. `du -a` at 22:49 UTC put `fx/fx17-copy` at 762 MB. Its `.git` is 5.9M, with `objects/info/alternates` pointing at the lane `.git/objects`. So the fixture is a shared-object clone, but the worktree holds about 756 MB I did not identify. The tree was deleted before my second pass, so the 762 MB was never broken down (`fx17-children.txt` and `fx-sizes.txt` are empty). Scratch hygiene defect: a 762 MB per-fixture worktree with no recorded reason. | `du -a .../W2C1Drift \| sort -rn \| head -12` (`w2c1drift-top.txt`); `git -C .../fx17-copy count-objects -vH` (`fx17-probe.txt`) | 0 | w2c1drift-top.txt (sha not recorded; first 12 lines shown) |
| F4 | No round-49 leftovers in `/tmp` by name. The find for files newer than `gen-w1.py` (18:02 local) owned by vgpnk returned 40 entries, none named round-49/kaidoku-r49/R49. Names point to other rounds (`cl40`, `r51cl`, `sources-round40-*`, `wr3211/3212.log`, `have.txt`, `wr_smoke.log`, `idx_full.json`, `map_hash_*`) and to harness files (`zcode-bash-*`, `ecc-metrics-*`, `claude-tool-count-*`, `playwright_firefoxdev_profile-*`). `find` hit no 50-line cap. | `find /tmp -maxdepth 2 -newer .../round-49/gen-w1.py -user "$(id -un)"` (`tmp-mtimes.txt`, 40 entries) | 0 | tmp-mtimes.txt 956cb4c0… |
| F5 | `/tmp/cl40` (188M, created 18:34 local, after `gen-w1.py`) has an unattributed name. Content is round-census copies across many rounds. It matched round-49 markers (`round-49`/`R49`) only inside other rounds' census text. L1 should decide who owns it and whether to remove it. | `grep -rlE 'kaidoku-r49\|round-49\|round 49\|R49' /tmp/cl40 /tmp/r51cl /tmp/sources-*` (`grep-r49-tmp.txt`) | 2 (grep hit a missing path, `/tmp/r41c1-5dunsqgk`, which vanished between `find` and `grep`) | grep-r49-tmp.txt ffe15ef7… |
| F6 | `/tmp` consumers in disk-guard (kasegi-r42-judge 61.5G, verif-kasegi-r42 25.4G, r43-work 3.8G, kaidoku-before, r50tip/r50clone/r50base, k57, frz, afterchk, basefull) are not round-49 leftovers. Their mtimes are before `gen-w1.py` (10-27 16:33 to 10-28 17:40 local), so they predate this round. | `stat -c '%y %U %s %n'` on eight of them (`tmp-disk-guard-entries.txt`) | 0 | tmp-disk-guard-entries.txt |
| F7 | Live processes: `/proc` scan for cwd or fd under `kaidoku-r49`. At 22:51 UTC only pid 3424730 (`python3 matrix.py`, cwd W2C2Forge) matched. At 22:52 UTC nothing matched. | `/proc/*/cwd`, `/proc/*/fd` scan (`live-procs.txt`, `owner-live.txt`) | 0 | live-procs.txt 3637aef1…; owner-live.txt e2a98560… |
| F8 | No "live" check was possible for `/proc` entries outside my uid. Only my own processes were visible to the scan. | (same scan) | — | — |

## Receipts

Everything is in `.ufo/waves/round-49/w2/W2Scratch/`. Hash file: `sha256-receipts.txt`.

- ls-scratch.txt, ls-now.txt, root-du-final.txt, du-sh.txt, du-d1.txt
- disk-guard.txt (exit 0)
- tmp-mtimes.txt (40 entries + exit line), tmp-leftovers.txt
- tmp-disk-guard-entries.txt, grep-r49-tmp.txt (grep exit 2 from a vanished path)
- owner-live.sh, owner-live.txt (exit 0), live-procs.txt (exit 0), pgrep.txt (exit 1 = no match)
- w2c1drift-top.txt, w2c1drift-fx-count.txt (90), fx17-probe.txt, fx17-children.txt (empty, tree already gone), fx-sizes.txt (empty), fx-names.txt
- recent-writes.txt (19:51 local snapshot)

Other files in the same directory (`blob-match.txt`, `clone-objects.*`, `find-*.txt`, `proc-kaidoku-r49.*`, `ls-du.*`) are from earlier passes of this seat. I did not analyse them and do not cite them.

## Limits

- Live-process detection covers only processes visible to my uid through `/proc`.
- The W2C1Drift fixture worktree (762 MB per `fx17-copy`) was deleted by its owner before I could measure it. F3 is therefore a recorded gap, not a measured number.
- Owner attribution for unprefixed names is inferred from name shape, not confirmed.
- No command was run against the frozen counters, the lane tree, or any commit. Every command here is read-only (`ls`, `du`, `find`, `stat`, `grep`, `readlink` on `/proc`, `disk-guard.sh status`, `git count-objects`, `git rev-parse`).

## Tooling

No tools were installed or upgraded in this pass. No pacman, no `uv`, no `npm`, no changes to `~/.local/bin`. Nothing was committed, staged, or pushed.
