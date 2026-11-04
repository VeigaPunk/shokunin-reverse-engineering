# SentinelScope — round 66 / w1 scope, secret and provenance audit

Seat: SentinelScope. Read-only over the lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(`git rev-parse --show-toplevel` → the lane; `HEAD` = `7b63dd5d5199ed30bc3f213573d8594434a18eb6`,
detached; `refs/heads/main` = `7b63dd5d`). Fleet root `/home/vgpnk/Projects/shokunin` is a
separate repo. Scratch `$S=/fast/scratch/hyaku/kaidoku-r66/SentinelScope` (deleted before yield).
No lane edit was made by this seat; no tool was installed.

Round commits audited: `b5b02e1f`, `78fa9666`, `7b63dd5d` (the operative freeze —
`git log --diff-filter=A --format=%H -- .ufo/waves/round-66/claims.json` prints exactly `7b63dd5d…`).

## Verdicts

| # | Item | Verdict |
|---|---|---|
| 1 | Write scope of the three round commits | **clean** — 14 paths, all lane-relative, none in the fleet root, none outside the lane |
| 2 | Secret material in new/changed bytes | **clean** — 0 credential-shape hits; every 32+ hex value resolves to a named git object or named-file sha256 |
| 3 | Toolchain integrity and file count | **clean** — manifest exit 0, entries 30, cache empty; 105 files, delta 0 vs the r65 freeze count |
| 4 | Frozen-path integrity (4 paths) | **clean** — blob at freeze = blob at lane tip = bytes on disk, and each sha256 equals its `claims.json` pin |
| 5 | Registry rows for `tools/round-66` | **clean** — 2 rows at tip, 7 cells each, no escaped pipe, 0/1/2 verdict maps named |

Two observations that are *not* findings against this round are recorded at the end.

---

## 1. Write scope — clean

Method (per commit; the multi-tree form was also tried and is recorded for auditability):

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff-tree --no-commit-id --name-status -r <c>   # c = b5b02e1f, 78fa9666, 7b63dd5d
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show --stat --format='%H' <c>
```

`diff-tree` with several tree-ishes in one call (`… b5b02e1f 78fa9666 7b63dd5d`) printed **0 paths**
(exit 0) because it compares adjacent trees; the enumeration below is the per-commit form and agrees
with `show --stat` line for line.

| Commit | Status | Path (lane-relative) |
|---|---|---|
| b5b02e1f | M | `LOG.md` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/controls/c1-do-nothing.json` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/controls/c1-do-nothing.py` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/controls/c2-do-nothing.json` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/controls/c2-do-nothing.py` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/pre/dryrun-c1-verify.json` |
| 78fa9666 | A | `.ufo/waves/round-66/l1/pre/dryrun-c2-selfcheck-at-base.json` |
| 78fa9666 | M | `SKILL.md` |
| 78fa9666 | A | `tools/round-66/closure-boundary.py` |
| 78fa9666 | A | `tools/round-66/coverage-selfcheck.py` |
| 7b63dd5d | A | `.ufo/waves/round-66/claims.json` |
| 7b63dd5d | A | `.ufo/waves/round-66/l1/pre/selftest-c1.txt` |
| 7b63dd5d | A | `.ufo/waves/round-66/l1/pre/selftest-c2.txt` |
| 7b63dd5d | A | `plans/round-66-claims.md` |

- 14 distinct paths, no path touched by two commits; insertions only (`show --stat`: +8 / +1531 / +230,
  deletions 0), which matches the append-only claims in `LOG.md` and the two added registry rows.
- Absolute-path entries: **0** (`awk '{print $2}' … | grep -c '^/'` → 0). `..`-escaping entries: **0**.
- Every path resolves under the lane: `realpath -m <lane>/<path>` stays inside
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- No fleet-root path: the fleet root does not contain these commits at all —
  `git -C /home/vgpnk/Projects/shokunin cat-file -t b5b02e1f` → `fatal: Not a valid object name`, exit 128
  (same for `7b63dd5d`). Lane commits are structurally incapable of naming fleet-root paths.
- `LOG.md` and `SKILL.md` here are the **lane's** copies, not the fleet root's (proved by the lane
  toplevel; the fleet root's own `LOG.md`/`SKILL.md` are untouched by these commits).

Out-of-commit activity, listed for completeness and **not** attributed to the round's claims:
the lane has untracked wave machinery (`.ufo/waves/round-66/{gen-w1.py, l1/records/, r66-w1-dispatch.{json,err},
r66-w1-spec.json, r66-w1.ready*, w1/}`), and the fleet root has 5 non-lane status entries
(`.scratch/goal-20261103-hyaku-run15.md` M, `.scratch/run15-state.json` M, `.scratch/run13-state.json`,
`.scratch/run15-kernel.py`, `after`). Those are orchestrator/seat artefacts, untouched by this seat.

## 2. Secret material — clean

Files scanned: the 14 paths above (worktree bytes are identical to the tip for every tracked file —
`git status --porcelain` shows no modified tracked file) plus the *added lines only* of the three
commits (1783 `+` lines) so that pre-existing `LOG.md` history is not re-credited to this round.

Sweeps and results:

```
# A private-key headers, op:// references, cookie jars
grep -nE -- '-----BEGIN [A-Z ]*PRIVATE KEY-----|op://|netscape-?cookie|cookiejar|\.cookies\.txt' <files>      -> 0 hits (rc=1)
# B bearer/token/password assignments
grep -nEi -- '(bearer[ _-]?[A-Za-z0-9._-]{8,}|(api[_-]?key|secret|token|passwd|password|credential)[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{6,})' <files>  -> 0 hits (rc=1)
# C provider token shapes
grep -nEi -- 'ghp_|gho_|github_pat_|sk-[A-Za-z0-9]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|-----BEGIN|ssh-rsa AAAA|age1[0-9a-z]{20,}|BEGIN OPENSSH' <files>  -> 0 hits (rc=1)
# D long base64 runs (>=100 chars)
grep -nEo '[A-Za-z0-9+/]{100,}={0,2}' <files> | wc -l                                                        -> 0
```

Every `32+` hex value on the round's added lines, accounted for (10 distinct values):

| Value | Where | What it is | Verification |
|---|---|---|---|
| `311079d8…` (40) | claims.json:4,32; plans:3; dryrun-c2:* | the round base rev | git object, `git log -1` resolves to `round-65 verifier spot-check…` |
| `b5b02e1f…` (40) | claims.json:5 | carry-in commit | `git cat-file -t` → commit |
| `78fa9666…` (40) | claims.json:5 | instrument commit | `git cat-file -t` → commit |
| `3c5cfb03…` (64) | claims.json:7; plans:38 | sha256 of `tools/round-66/closure-boundary.py` | `sha256sum` → identical |
| `1be9d046…` (64) | claims.json:8; plans:77 | sha256 of `tools/round-66/coverage-selfcheck.py` | `sha256sum` → identical |
| `3abcfe0d…` (64) | claims.json:9 | sha256 of `l1/controls/c1-do-nothing.py` | `sha256sum` → identical |
| `1787cd29…` (64) | claims.json:10 | sha256 of `l1/controls/c2-do-nothing.py` | `sha256sum` → identical |
| `79a4dca4…` (64) | closure-boundary.py:66; c1-do-nothing.py:30; selftest-c1.txt:1; dryrun-c1-verify.json:70; claims.json:35 | sha256 pin of the frozen `tools/round-65/jsc-closure-matrix.py` | `sha256sum tools/round-65/jsc-closure-matrix.py` → identical |
| `1d697af1…` (64) | dryrun-c2-selfcheck-at-base.json:41 | value of the key `recipe_a_block_sha256` — the sha256 of the SCORECARD recipe-A block | named by its own key; not a credential |
| `ba7816bf…` (64) | coverage-selfcheck.py:367; selftest-c2.txt:26 | `sha256("abc")`, the NIST test vector, used as a selftest oracle | `printf 'abc' \| sha256sum` → identical |

No hit is a credential. The only absolute paths in the new counters are the toolchain root
(`closure-boundary.py:80`) and a selftest node path (`:455`) — see observation O2.

## 3. Toolchain integrity — clean

```
S=/fast/scratch/hyaku/kaidoku-r66/SentinelScope
TMPDIR=$S python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-65/jsc-closure-matrix.py \
  --manifest --toolchain-root /home/vgpnk/.local/share/kaidoku-jsc \
  --probe /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-64/inputs/probe-electron.jsc
  -> exit 0, stderr empty, stdout:
     {"cache_present": [], "entries": 30, "findings": [], "missing": [], "ok": true, "pin_mismatch": []}
```

`entries` 30, `ok` true, `cache_present` empty, no missing/pin-mismatched file — the frozen manifest
re-derives from the read-only toolchain root.

File count:

```
find /home/vgpnk/.local/share/kaidoku-jsc -type f -not -path '*/.git/*' | wc -l   -> 105
```

**Delta vs the r65 freeze count (105): 0.** Composition, to show the 105 is the same set and not a
coincidence of drift: 3 d8 builds × {`d8`, `snapshot_blob.bin`, `icudtl.dat`} = 9, `inputs/` 1,
`jsc2js-src/` 72 (12-file View8 tree + 60 files of the rest of the checkout), `venv/` 23 →
9 + 1 + 72 + 23 = 105. The `jsc2js-src/.git/` objects (28 files) are excluded by the `-not -path`
filter, exactly as in the r65 count; including them the tree holds 133 files.

Cache-free and not written by this seat: `find … \( -name __pycache__ -o -name '*.pyc' \)` → 0;
`find … -type f -mmin -20` → 0; newest file in the tree is `jsc2js-src/.git/index` at 19:43, older than
this seat's session. The manifest was run with `-I -B` and `TMPDIR=$S`, and the seat wrote no byte
into `/home/vgpnk/.local/share/kaidoku-jsc`.

## 4. Frozen-path integrity — clean

`frozen_paths` from `.ufo/waves/round-66/claims.json`, compared freeze-rev blob vs lane-tip blob vs
worktree `hash-object`, with `sha256sum` cross-checked against `claims.instruments`:

| Path | blob @7b63dd5d | blob @main (=tip) | disk `hash-object` | sha256 = claims pin |
|---|---|---|---|---|
| `tools/round-66/closure-boundary.py` | `3d36f91a` | `3d36f91a` | `3d36f91a` | yes (`3c5cfb03…`) |
| `tools/round-66/coverage-selfcheck.py` | `3751998c` | `3751998c` | `3751998c` | yes (`1be9d046…`) |
| `.ufo/waves/round-66/l1/controls/c1-do-nothing.py` | `2dd5f178` | `2dd5f178` | `2dd5f178` | yes (`3abcfe0d…`) |
| `.ufo/waves/round-66/l1/controls/c2-do-nothing.py` | `f95aabe6` | `f95aabe6` | `f95aabe6` | yes (`1787cd29…`) |

No post-freeze edit of any frozen path; the freeze commit is the tip, and the working tree agrees with
the tip on all four. (The claim's ordering atom also holds: `git merge-base --is-ancestor b5b02e1f
7b63dd5d` → exit 0, and the same for `78fa9666` → exit 0.)

## 5. Registry rows — clean

Rows at the tip of `SKILL.md`:

```
1856: | `tools/round-66/closure-boundary.py` | … | 0=verified (all five arms pass) / 1=not verified (… ) / 2=could-not-evaluate (… ) | … | … | … | kaidoku |
1857: | `tools/round-66/coverage-selfcheck.py` | … | 0=verified (… ) / 1=not verified (… ) / 2=could-not-evaluate (… ) | … | … | … | kaidoku |
```

- Both rows exist at `7b63dd5d` (they arrive in `78fa9666`, `M SKILL.md`, +2 lines, deletions 0).
- Cell count: each row has 8 `|` (7 cells); `awk -F'|'` → `NF=9` (two edge empties), identical to the
  table header at `SKILL.md:1782` (`| tool | gate or probe - purpose | verdict map (exit codes) |
  self-test command | pinned-value path | write scope | owner |`, also `NF=9`). Rows and header align.
- Escaped pipe: `grep -o '\\|'` on each row → **0**; no cell is silently split.
- Verdict map (cell 4) names 0/1/2 in both rows, with the 2-arm's could-not-evaluate conditions spelled
  out (closure: absent/drifted r65 instrument, absent toolchain root, unreadable fixture interpreter;
  coverage: no coverage-map section, unreadable Owned-axes row, absent recipe-A block, unknown
  revision, failed git call).

---

## Observations (no verdict impact, recorded for the owner)

**O1 — pre-existing table break at `SKILL.md:1822`.** A blank line sits inside the instrument registry
between the round-46 rows and the round-47 rows. It is identical at the base revision
(`git show 311079d8:SKILL.md` line 1822 is blank), so it predates round 66 and lies outside this
round's write scope; the two new rows sit after it in a headerless continuation run. Rendering
consequence only (a GFM parser ends the table at a blank line); not a round-66 defect. Flagged because
any future cell-count sweep that assumes one contiguous table will mis-handle it.

**O2 — hardcoded selftest node path.** `tools/round-66/closure-boundary.py:455` defaults `--node` to
`/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node`. It is a path, not a
secret, and `--node` is overridable; worth knowing that on a host without that exact fnm version the
selftest arm degrades rather than silently passing. The toolchain default at `:80`
(`DEFAULT_TOOLCHAIN = /home/vgpnk/.local/share/kaidoku-jsc`) is the seat-specified root and is
expected.

**O3 — write-scope claim spot-check (confirms the registry's write-scope cell).** Every filesystem
write call site in the two counters lands on `--work`/`--out`/`TMPDIR` scratch:
`closure-boundary.py:175,176,213,327` (fixture root, fixture module, work mkdir, `--out` receipt) and
`coverage-selfcheck.py:199,285,365,397` (equiv script, `--out` receipt, selftest temp, scratch mkdir);
`shutil.rmtree` is confined to those same scratch roots. No write path targets the toolchain root or
the lane tree. Subprocess use is argv-only (no `shell=True`, no `os.system`), and the only git
subcommands invoked are read-only (`show`, `ls-tree` at `coverage-selfcheck.py`).
