# ExecC1 — R72-C1 landing-side re-derivation with an independent harness

Seat: ExecC1 (executor), wave r72-w1, lane `kaidoku-shokunin`. Date: 2026-11-04.
Scope: re-derive the R72-C1 landing-side child-environment evidence with MY OWN
launcher/PATH-shim/env-parser harness. I did not run `tools/round-72/seam-probe.py`
(not read either, to keep the harness independent) and I do not rely on any lane
receipt as evidence; the pre receipt `route-at-declaration.json` is used only as
the `--check-receipt` specimen named in the seat command.

## Harness

- Scratch: `/fast/scratch/hyaku/kaidoku-r72/ExecC1/` (deleted after this report;
  everything evidenced was first copied into `.ufo/waves/round-72/w1/ExecC1/`).
- Shims: `git` and `readelf` shell scripts, shim dir first on PATH. Each records
  the exec-boundary environment and then `exec`s the real tool by absolute path
  (`/usr/bin/git`, `/usr/bin/readelf`; `cat`/`date` resolved to `/usr/bin/...`).
- v2 shim (operative) opens the witness with the shell itself:
  `exec 3</proc/self/environ; /usr/bin/cat <&3 > <record>; exec /usr/bin/<tool> "$@"`.
- Caller environment: `KAIDOKU_ENV_CANARY=ExecC1-r72-canary-9f3a7b` exported
  (presence in the caller env proven by `caller-env.txt`, count 1), shim-first
  PATH, run from the lane root.

Run (both subruns identical argv):

```
python3 -I -B tools/round-72/packed-elf.py --root . \
  --rev 6316c1053f927a1a1cdc3e0960b70acab5f56381 \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r72/ExecC1/work \
  --check-receipt .ufo/waves/round-72/l1/pre/route-at-declaration.json \
  --child-env-log <scratch>/checker2.jsonl \
  --nonce-commitment 2532bd5bd8bbf48b5576821b29f35d90b55ab136a9e7179eff989cf961b84fd5
```

Instrument bytes pinned: working-tree `tools/round-72/packed-elf.py` sha256
`973d504b415c58c1cc84896057322ce99c2db2762551de3b13f0c87f17ffefe7` — equals the
`claims.json` instrument pin. The checker itself re-derived the same blob sha at
rev `6316c105…` (the `instrument.sha256` clause passed, `failing: []`).

## Result — R72-C1 landing-side evidence CONFIRMED (green), both subruns

Checker: rc=0, `met: true`, `failing: []`, clauses all true
(`run_nonce`, `run_binding`, `run_root`, `child_env_observed`, `receipt_capsule`).

My independent exec-boundary witness (subrun 2, v2 shims; 5 records):

| class | count | keys (every record) | canary | HOME | TMPDIR |
|---|---|---|---|---|---|
| git | 1 | HOME, LANG, PATH, TMPDIR (exactly) | absent | `<work>/home` | `<work>/tmp` |
| readelf | 4 | HOME, LANG, PATH, TMPDIR (exactly) | absent | `<work>/home` | `<work>/tmp` |

- `<work>` = `/fast/scratch/hyaku/kaidoku-r72/ExecC1/work` (the checker's
  `--work`); every HOME/TMPDIR is exactly the builder's `<work>/home`,
  `<work>/tmp` — contained, never `/tmp`, no sibling-prefix games.
- `LANG=C` in all records; PATH is the caller PATH with the shim dir first
  (the allowlist constrains keys, and the value is the inherited caller PATH).
- Census: mine `{git: 1, readelf: 4}` == the checker's `checker_child_env`
  census `{git: 1, readelf: 4}`; `records 5 == 5`.
- Cross-proof per child: the launcher-side JSONL env (`subrun2-checker-launcher.jsonl`)
  is dict-identical to my shim's exec-boundary record for the same child
  (`pairs_env_identical: true`, argv[0] class agrees on all 5).

Against the frozen predicate atoms (A2 / claim sentence R72-C1):

1. both shim classes' key sets exactly HOME/LANG/PATH/TMPDIR — TRUE (5/5 records);
2. canary key absent from every shim record — TRUE (despite the exported canary);
3. HOME and TMPDIR under the checker's run root (`--work`) — TRUE (exactly its
   `home/` and `tmp/` subdirs);
4. the checker's own `checker_child_env` records ≥2 records whose census
   contains `git` and `readelf` — TRUE (5 records; git 1, readelf 4);
5. `A11_checker_env`-side state: every checker-mode child ran under the
   four-key allowlist — TRUE, no extra key, no canary, no out-of-root
   HOME/TMPDIR in any record.

Every checker-mode child this revision spawns in `--check-receipt` mode is
`git -C . show <rev>:tools/round-72/packed-elf.py` (1) and `readelf -h <pinned
source>` (4, one per carrier). All five ran under the allowlist. R72-C1's
landing-side evidence is independently re-derived GREEN.

## Harness defect found and corrected (wave-relevant)

Subrun 1 (superseded, receipts kept) used the naive `cat /proc/self/environ`
inside a `#!/bin/sh` shim. On this host `/bin/sh -> bash`, and a plain
`cat /proc/self/environ` measures **the cat child's** exec environment: bash
augments it with `_=/usr/bin/cat`, `SHLVL=1`, and an updated `PWD` before exec.
Those 7-key records (HOME, LANG, PATH, PWD, SHLVL, TMPDIR, _) are a
**shim-authored artifact**, not checker pollution — the checker's launcher JSONL
showed exactly 4 keys in the same run. The v2 shim opens `/proc/self/environ`
with the shell itself (`exec 3<`) so the fd holds the shim's true initial exec
block; those records match the launcher env byte-for-byte. Any seat or probe
whose shim uses a plain `cat /proc/self/environ` inside a shell must account for
`_`/`SHLVL`/`PWD` before calling an extra key a violation.

## Provenance & bounds

- No tools installed (operator 2026-10-19 authorization unused); no pacman.
- Read-only git access only (`git` was exec'd by the instrument itself for
  `git show`, and my shims wrapped it); no writes, no commits, no checkouts.
- Writes: only `.ufo/waves/round-72/w1/ExecC1/`, `.ufo/waves/round-72/w1/ExecC1.md`
  (this file) and my scratch (deleted). The lane's `claims.json` pin block and
  the frozen plan were read as ground truth for the predicate, not modified.

## Receipts (all under `.ufo/waves/round-72/w1/ExecC1/`)

- `subrun2-fd-records/*.environ` — the operative exec-boundary witness (5 files).
- `subrun2-checker-launcher.jsonl`, `subrun2-checker-stdout.json`,
  `subrun2-checker-stderr.txt` (empty), `subrun2-rc.txt` (rc=0),
  `subrun2-analysis.json` (my parser verdict, `c1_verdict: true`).
- `subrun1-rawcat-records/`, `subrun1-*` — the superseded artifact run
  (`analysis.json` shows `mine_keys_exact: false` for the documented reason).
- `shims-v2-fd/` (operative), `shims-v1-rawcat/` (superseded, documented).
- `caller-env.txt` — caller environment incl. the canary and shim-first PATH.
- `sha256sums.txt` — digests of the evidence artifacts.

## Risks

- The verdict covers the `--check-receipt` child census at this revision
  (git+readelf only; `score` mode additionally spawns upx/node, out of seat scope).
- `receipt_capsule: true` was observed as a crossover with R72-C3 but not
  independently re-audited here (capsule tamper battery is another seat's scope).
- `child_env_log` paths: relative `--child-env-log` values are resolved under the
  checker's work root by the instrument; my run passed absolute paths.
