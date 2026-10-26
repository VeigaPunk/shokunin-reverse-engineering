# R41W2LocalSrc — S126 durability fix (round-40 closure D1)

Verdict: **CONFIRMED** — D1 is closed for S126. Attacked: the three committed copies' digests against the row pins, the sidecar map and the live host files; the gate `tools/round-41/local-source-gate.py` at base `49096c7e`, tip `7a24ff74` and worktree HEAD, plus the per-revision *tree* state in sandbox checkouts; the gate's ability to fail on the real map (corrupted-copy negative control); the `--selftest`; and the residual host-local row list the gate still reports.

All commands below ran with `S=/fast/scratch/hyaku/kaidoku-r41/R41W2LocalSrc` as cwd/TMPDIR; lane `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No VCS mutation anywhere (read-only `git show/log/diff/rev-parse` in the lane; sandbox clones verified `git rev-parse --show-toplevel` == the clone dir before use; scratch removed afterwards). No tools installed (system `python3` + `git` only).

## 1. Digest verification (independent of the gate)

| body | sha256 | agrees with |
|---|---|---|
| `corpus/evidence/round-41/s126/lead1-avm-image.tsv` | `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0` | map `sha256` **and** map `source_sha256`; the S126 URL-cell pin; the live source `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv` (`cmp` clean) |
| `corpus/evidence/round-41/s126/lead1-avm-image.tsv.sha256` (sidecar) | file digest `9cd1382366c718f…47e63b` | content `f205807d…  lead1-avm-image.tsv`; `sha256sum -c` in the s126 dir → `lead1-avm-image.tsv: OK`, exit 0 |
| `corpus/evidence/round-41/s126/avm-be.squashfs` (4 096 B) | `c7f74691b3e8d767…faed32d32` | the digest pinned in S126's `teaches` cell; the live `…/round11/work/avm-be.squashfs` (`cmp` clean) |
| `corpus/evidence/round-41/s126/unblob.log` (17 lines) | `352e0d794143df9c…18aed5d7` | the digest pinned in S126's `teaches` cell; the live `…/round11/work/unblob.log` (`cmp` clean) |

Instrument bytes: gate `sha256 cafe232a196dd844…a45a4ece7`, map `d0d562df9e1e97d8…cc6ad289dd`. Both first added in the freeze `d764389e` (git log: no other commit on `main` touches them); `git diff 7a24ff74..HEAD` on both is empty and `git status --porcelain` is clean, so every run below used the same bytes as the committed tip. The S126 row itself is byte-identical at base, tip and worktree (registry append-only respected; base..tip adds only S127/S128, both https-only cells).

The log copy is the retained original run (references the shokuknow path, no exit status — matching the round-40 registry note that a recheck must never read it as "exit 0"), and its content agrees with the tsv it accompanies: handler `squashfs_v4_be`, command `sasquatch-v4be -no-exit-code -f -d …` with no `-be`.

## 2. Gate runs (exit codes and rows)

| # | command (cwd `$S`) | exit | rows total / out-of-lane | S126 | failed rows |
|---|---|---|---|---|---|
| 1 | `python3 -I -B $L/tools/round-41/local-source-gate.py --root $L --rev 49096c7e… --json` | **1** | 126 / 19 | `ok [resolved/url-cell] <- corpus/evidence/round-41/s126/lead1-avm-image.tsv  src[file]` | 18 (§4) |
| 2 | same with `--rev 7a24ff74…` | **1** | 128 / 19 | same `ok … src[file]` | same 18 |
| 3 | same, no `--rev` (worktree HEAD `e1c83313`) | **1** | 129 / 19 | same `ok` | same 18 |
| 4 | sandbox clone checked out at base, gate `--root <clone>` (no `--rev`) | **1** | 126 / 19 | **FAIL `[map-missing]`, url-cell pins `f205807de801…`** | 19 (the 18 + S126) |
| 5 | sandbox clone checked out at tip, gate `--root <clone>` | **1** | 128 / 19 | `ok [resolved/url-cell] … src[file]` | 18 |
| 6 | negative control: sandbox tip clone, one line appended to the copy | **1** | 128 / 19 | **FAIL `[copy-digest-mismatch] expected f205807de801 actual abdc5b5638ba`** | 19 |
| 7 | `python3 -I -B $L/tools/round-41/local-source-gate.py --selftest` | **0** | — | — | 23/23 cases PASS |

Reading of the two modes (a property worth keeping in mind, not a defect): `--rev` reads `corpus/SOURCES.md` from git but the map from the **worktree** (documented in the tool docstring — the map is the current fix), so run 1 shows "base table under today's map" (S126 already green); run 4 checks out the base *tree* and reproduces the lesson's claim verbatim: at the base the map and copies do not exist and S126 is red (`[map-missing]`), at the tip it is green. `corpus/lessons/round-41.md` M41-2 ("S126 unresolved at the base, resolved at the tip; the gate still exits 1 on 18 other host-local rows") is accurate on both halves, and the closure table row `D1 | fixed for S126 | M41-2` holds.

The negative control (run 6) shows the gate fails closed against the real map and real row, not only against selftest fixtures: a corrupted copy is caught as `copy-digest-mismatch` with the URL-cell pin echoed.

## 3. D1 disposition for S126

D1 (`corpus/lessons/round-40-verifier-spotcheck.md` §5): *"S126 and the AVM entry's lineage point at `/home/vgpnk/Projects/shokuknow/…` … Commit a copy or a digest-pinned extract under `corpus/evidence/`, or mark the row host-local."*

- The remedy taken is "commit a copy": all **three** bodies MH-1 says the row cites (`lead1-avm-image.tsv`, `avm-be.squashfs`, `unblob.log`) now sit byte-exact under `corpus/evidence/round-41/s126/` (four files with the sidecar), each matching the digest its citation pins and the live host file (§1).
- The URL-cell path — the only path the gate's convention scans — is bound by the committed map and resolves at the tip and at HEAD (`resolved/url-cell`, pin scope `url-cell`, `source_digest_check: file`).
- The row text was not edited (append-only respected); the "mark the row host-local" alternative was not needed.
- **D1 is closed for S126.** Residuals below are outside S126's URL cell or outside the gate's scan scope.

## 4. What remains

1. **R41-CL3 (routed into round 42, `corpus/lessons/round-41.md`)** — the gate still exits 1 on **18 rows / 21 paths** with host-local URL cells and no map entry (`no-copy-named`), identical lists at base, tip and HEAD:
   - No public URL in the cell (the D1 class proper — not re-derivable without this host): S001, S002, S003, S006, S007, S023, S040, S048, S056, S066, S070 (11 rows; `~/.agents/skills/reverse-engineer-anything`, `~/.local/opt/ghidra_12.1.4_PUBLIC`, `~/.local/opt/go-1.25.0`/`go-1.24.6` for S035's two paths, `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).
   - Public URL in the cell (re-derivable in principle): S035 (2 paths, go1.25.0 tag), S079, S083, S090, S092 (rea-agents 6.5.0 tgz), S081 (rea-agents 6.7.0 tgz), S082 (3 paths, archlinux tinyxxd + sync db).
   - Of the 21 paths, **20 sources are still present on this host; 1 is gone**: S081's `~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` no longer exists, so the public 6.7.0 tarball is the only remaining derivation path for that row.
2. **Gate scan scope = URL cell only.** S126's `teaches` cell also pins `avm-be.squashfs` (`c7f74691…`) and `unblob.log` (`352e0d79…`) at shokuknow paths. In-lane copies of both exist and I verified their digests directly (§1), but they are **not bound by the map** (the map has exactly one entry), so the gate cannot detect their removal or corruption, and no gate run covers them. Same for the `source:` lineage lines of `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md` and `2026-10-26-r41-avm-be-squashfs-core.md`, which still name the shokuknow tsv path and do not cite the in-lane copy — a fresh-checkout reader of those entries hits a dead path unless they also consult the map.
3. Nit (unscored prose): the map's `note` says the digest is "pinned in the S126 URL cell **and in the S126 anchor**"; in the row the digest appears exactly once — the URL cell. The `anchor` column carries no digest (the pin is re-confirmed by the round-40 spot-check instead).

## 5. Artifacts

`​.ufo/waves/round-41/w2/artifacts/R41W2LocalSrc/`: `gate-base.txt`/`gate-base.json` (run 1), `gate-tip.txt`/`gate-tip.json` (run 2), `gate-worktree.txt` (run 3), `gate-base-tree.txt` (run 4), `gate-tip-tree.txt` (run 5), `gate-neg.txt` (run 6), `selftest.txt` (run 7), `S126-row.txt` (full row, `corpus/SOURCES.md:132`), `digests.txt` (all sha256sums, `cmp` and `sha256sum -c` outputs). No vendor or firmware bytes copied (the 4 096-byte lane-built `avm-be.squashfs` is lane-own work already committed in the tree; cited by digest here).
