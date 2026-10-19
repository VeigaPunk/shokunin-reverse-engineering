# RV-14 — review: EX-36's `custody-pair` registry row vs the actual tool

Seat RV-14, chain c3, reviewer · 2026-10-19 · wave `arc3-loop1-round2`.

Artifacts reviewed
- row artifact: `claims/c3/EX-36/registry-row.patch.md`
  (sha256 `c114ade81fe662c260d1eb8b789d3e007bfbe030aee653f7e1cb4d3ce05500d8`),
  row text `claims/c3/EX-36/evidence/row.txt`
  (raw sha256 `61e70a3a…`, content sha256 `f4ff2f4c46325c7081fc370e5de1468a452f907e033aaf89b14cc4e9f52b47f2` —
  re-derived, matches the patch text's own identity claim), diff `evidence/registry-row.diff`
  (`db652720…`).
- tool reviewed against: `.ufo/gates/custody-pair/custody-pair.py`, sha256
  `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, 889 lines
  (unchanged before and after every run in this review; EX-36's own bracket agrees).

Verdict: **VERIFIED — every claimed behavior exists and behaves as the row
words it**, with three named precision notes (§3) and two unexercised branches
(§4). No row sentence was found false.

## 1. Claim-by-claim (row text → my measurement)

| # | row clause | method | result |
|---|---|---|---|
| 1 | `capture --out <receipt> [--label <L>]` reads the five operator paths read-only | full `lstat` of all 5 paths before vs after a capture (inode/mtime/ctime/size/mode/uid/gid) | identical — no movement; receipt records the label (`# capture-label: rv14-readonly`) |
| 2 | v2 receipt fields: `SHA256`, `MTIME_EPOCH/NS`, `MTIME_UTC_RENDER` + `MTIME_LOCAL_RENDER` separately, `CTIME_EPOCH/NS`, `INODE`, `MODE/UID/GID` | stanza parse + independent ground truth (`hashlib`, `os.lstat`) | all present and equal to ground truth on all 5 paths |
| 3 | "the v1 local-under-`MTIME_UTC` defect gone" | grep of a live receipt | 0 lines matching `^MTIME_UTC:`; 5 `MTIME_UTC_RENDER`; UTC render is TZ-independent (`TZ=UTC/UTC+5/UTC-3` → same `2026-10-15T06:12:07Z`, local render moves correctly) |
| 4 | "the receipt self-pins the instrument's sha256 and receipt-version 2" | header of my live receipt vs `sha256sum` of the tool | `# tool: … sha256 112d01dc…` == current tool sha; `# receipt-version: 2` |
| 5 | "+ a `.sha256` sidecar" | capture run | sidecar written, its digest == receipt digest |
| 6 | "`paths` prints the canonical five" | `paths` | 5 lines, fixed order, rc 0 |
| 7 | `verify <a> <b>` and `verify <a> --live` | both forms run | both work; `MATCH 5/5 exit 0` on the clean pair, twice (idempotent) |
| 8 | exit `0 MATCH` | round-trip + EX-31's own live pair re-verified by me | `MATCH paths=5 MATCH=5 exit=0` |
| 9 | `10 CONTENT-DRIFT (sha256 moved)` | synthetic fixture flipped after capture | `CONTENT-DRIFT paths=1 exit=10` |
| 10 | `11 REWRITE-DRIFT (sha256 equal, inode/ctime/mtime moved)` | in-place same-bytes rewrite with mtime restored; rename form | `REWRITE-DRIFT exit=11 moved=ctime_ns` (in-place) and `moved=inode` (rename, selftest case) — sha unchanged |
| 11 | `12 METADATA-DRIFT` sub-classes: mode/uid/gid/size/type | selftest case `metadata-drift-detected` | PASS (mode); size/type branch source-read (`custody-pair.py:457-462`), not separately fired |
| 12 | `12 … extra path` | candidate receipt carrying a path the reference lacks | `METADATA-DRIFT ... moved=EXTRA-PATH` (overall verdict `ABSENT exit=13` — precedence holds) |
| 13 | `12 … inconsistent epoch/render` | crafted v2 receipt, epoch vs `MTIME_UTC_RENDER` mismatch | `LABEL-INCONSISTENT(ref): epoch … renders 2026-10-19T12:10:35Z, receipt says 1999-01-01T00:00:00Z`; `METADATA-DRIFT exit=12` |
| 14 | `12 … reproduced v1 LABEL-DEFECT` | round-1 CU-1 `config-pre-pair.txt` vs live | `exit=12`, 5× `LABEL-DEFECT … localtime(epoch 1792011200); gmtime(epoch) is 2026-10-14 20:53:20` |
| 15 | `13 ABSENT` | capture/verify against a missing path | `ABSENT exit=13`, receipt still written with `EXISTS: no` |
| 16 | `2 USAGE (bad args / unreadable / unparsable receipt / refused write)` | no subcommand; nonexistent receipt; junk receipt; guard case; non-writable out-dir | 2 / 2 / 2 (selftest case) / 2 (sandboxed HOME) / 2 (`write failed … Permission denied`) |
| 17 | precedence `CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH` | source `SEVERITY` (`:127-134`) + one empirical pair (ABSENT > METADATA-DRIFT) | consistent; full ordering is structural (`max()` over row severities), not fired in one run |
| 18 | "capture is 0 at 5/5, else 13 with the receipt still written" | live capture; missing-path capture | `OK paths=5/5 exit=0`; `PARTIAL paths=0/1 exit=13`, receipt + sidecar written |
| 19 | "refuses to write a receipt over a custody path" | `HOME=<sandbox>` capture with `--out <sandbox>/.bashrc` | `USAGE: refusing to write a receipt over a custody path`; sandbox file unchanged (real paths never approached) |
| 20 | "v1 receipts still compare on their sha256 — sums-form reads `MATCH-V1-PARTIAL` exit 0" | in-repo round-1 sums file (`arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt`) vs live | `SHA256-CONTRACT: 5/5`; `MATCH-V1-PARTIAL paths=5 exit=0` |
| 21 | "a v1 stanza reproducing the round-1 label defect reads `METADATA-DRIFT`/`LABEL-DEFECT` exit 12 with its sha256 contract intact (5/5)" | round-1 CU-1 stanza receipt vs live | exactly as written; also true for the pipe-shape (`config-pre-pair-metadata.txt`, 10× LABEL-DEFECT) |
| 22 | self-invocation "same command with `selftest`" | run | works; 15 cases |
| 23 | "15 fixture cases — [enumerated categories]" | case list + per-case result | 15/15 PASS, exit 0; every named category maps to a case (`capture-ok-exit-0`, `receipt-shape-v2-fields`, `sidecar-self-hash`, `verify-receipt-vs-live-clean`, `same-content-rewrite-inplace-ctime-pin`, `same-content-rewrite-rename-inode-pin`, `content-drift-detected`, `absent-path-detected`, `metadata-drift-detected`, `label-utc-render-tz-independent`, `v1-stanza-compat-and-mutation`, `sums-v1-compat`, `pipe-v1-compat`, `unparsable-receipt-usage-exit`, `refuses-to-write-over-custody-path`) |
| 24 | "scratch root `$CUSTODY_PAIR_SCRATCH` else `/dev/shm` else `/var/tmp` (`/tmp` never — EDQUOT hazard)" | env set to an existing dir → honored; env unset → `/dev/shm`; env = `/tmp` → `USAGE: /tmp is excluded scratch (EDQUOT hazard) exit 2`, zero `custody-pair-selftest-*` dirs created under `/tmp` | as written for the selection chain |
| 25 | "exit 3 if any case fails, 0 clean" | source `:825-829`; 0 measured | 0 measured; 3 source-read only (not fired — §4) |
| 26 | "five path identities are pinned in the instrument (`CUSTODY_PATHS`, fixed order, printed by `paths`)" | source `:111-117` + `paths` output | exactly `~/.config/devin/mcp_config.json`, `~/.omp/agent/mcp.json`, `~/.kimi-code/config.toml`, `~/.bashrc`, `~/.profile` |
| 27 | "normal entry writes nothing under the custody paths — opened for reading only, never renamed, mtime never touched" | stat-identical proof (#1) + source (read-only open, `lstat`, no `utime`) | held |
| 28 | "writes only the requested receipt + `.sha256` sidecar … and, under selftest, its isolated fixture root" | scratch copy of the tool, all four subcommands run there | only `r.txt` + `r.txt.sha256` appeared; no `__pycache__` from normal entry |
| 29 | "`--paths` exists for fixture runs only" | `capture --help` | flag exists (`override paths (default: the 5 custody paths)`); "fixture runs only" is stated policy, not an enforced restriction |

Patch mechanics (my own run, on a `SKILL.md` copy under `/var/tmp`):
`patch -p1 --dry-run` rc 0; `patch -p1` rc 0; patched file sha256
`2ff458dd…` and 372 lines — both re-derive EX-36's claims exactly; repo
`SKILL.md` unchanged (`483b0eba…` == `git show HEAD:SKILL.md`, working tree
clean for that path). Row insertion is byte-identical to `row.txt`'s content
line; the preamble rewrite is 3→3 lines.

## 2. Adversarial attempts against the row

- **"self-pin is stale"** — receipt captured at 12:10Z pins `112d01dc…`; tool
  re-hashed after every run in this review: still `112d01dc…`. No staleness
  (the tool *did* churn three times earlier: `4862f642…` → `b10ad1c8…` →
  `112d01dc…`; I observed `b10ad1c8…` at 12:04:50Z, which EX-36's history line
  does not list — its history is incomplete, its conclusions are not).
- **"the row flattens v1 compatibility"** — refuted: the row already splits the
  sums form (exit 0) from the label-defective stanza form (exit 12). EX-36's own
  A2 records catching the earlier blanket wording pre-landing.
- **"row promises an `expected.json` pin like the citation-drift row"** —
  refuted: the row claims only the in-code `CUSTODY_PATHS` constant and the
  receipt self-pin, both of which exist; no pin file is claimed.
- **"row's exit map is aspirational"** — refuted class-by-class (§1 rows 8–16);
  every class was produced by a run except `3 SELFTEST-FAIL`.
- **"the row's `--selftest` wording"** — the row says `selftest` (subcommand),
  matching the code; the *seat line* said `--selftest`; EX-36 names the
  deviation explicitly in its patch text §preamble. Verified: no `--selftest`
  flag exists.

## 3. Precision notes (not refutations)

1. **`(/tmp never …)` is a statement about selection, not about every path.**
   The default/env chain never selects `/tmp` and the env case is refused
   (measured). An *explicit* `--scratch /tmp/x` (args path) bypasses the guard
   (`custody-pair.py:621-623` only fires when `args.scratch` is unset), and
   `capture --out /tmp/...` merely warns (`:534-536`). The row's parenthetical
   reads as absolute; the selection chain it describes is exact.
2. **An absent `--scratch` dir is not covered by "2 USAGE (bad args …)".**
   `selftest --scratch <nonexistent>` dies with an unhandled `FileNotFoundError`
   traceback, exit 1. EX-36 found this itself (A3, `evidence/selftest-badscratch.out`);
   I reproduced it earlier in this seat. It does not touch any row clause that
   was written (the row names the resolution order, whose roots exist), but the
   USAGE clause should not be read as covering it.
3. **`__pycache__/custody-pair.cpython-314.pyc` in the tool directory** is not
   produced by any normal entry (verified in a scratch copy); it came from a
   seat importing the module. It was present in every poll from 12:02:11Z to
   12:08:57Z and gone by 12:12:11Z, so the tree now carries only
   `custody-pair.py` + `README.md`. The row's write-scope clause says "normal
   entry writes only …", which stays true either way; the residue is named here
   so the chain close can confirm what lands in the commit.

## 4. Unexercised branches (named, per evidence discipline)

- `3 SELFTEST-FAIL` — source-read only (`custody-pair.py:827-828`); would
  require a broken case.
- Full severity ordering in a single run — structural (`max()` over
  `SEVERITY`); only `ABSENT > METADATA-DRIFT` was fired empirically.
- `size`/`type` metadata sub-branch — source-read (`:457-462`); only the mode
  case was fired.

## 5. Reproducibility

- battery: `claims/c3/RV-14/independent-battery.sh`, output
  `receipts/independent-battery.out` (`0b9a774d…`)
- row lint: `claims/c3/RV-14/row-lint.py`, output `receipts/row-lint.out`
- label-defect reproduction: `receipts/label-defect-repro.txt` (`d681cde5…`)
- live 5-path capture: `receipts/rv14-live-5path-2026-10-19T12:02:57Z.txt`
- patch mechanics + edge runs: `/var/tmp/rv14/rowchecks/`, `/var/tmp/rv14/battery/`
- tool-side detail: `tool-verification.md`
