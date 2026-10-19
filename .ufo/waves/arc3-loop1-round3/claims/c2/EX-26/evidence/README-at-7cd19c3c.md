# custody-pair (v2 custody receipt instrument)

Seat EX-31 (chain c3, wave `arc3-loop1-round2`), revised by seat EX-21 (chain c2,
wave `arc3-loop1-round3`). Operator-owned custody for the five paths the
province freezes:

```
~/.config/devin/mcp_config.json
~/.omp/agent/mcp.json
~/.kimi-code/config.toml
~/.bashrc
~/.profile
```

`custody-pair.py` is the committed instrument. It is **read-only over every path
it inspects**: files are opened for reading only (sha256), never for writing,
never renamed, and no `utime` is ever called on them. Capturing a receipt changes
nothing about the paths it records.

## Usage

```sh
# capture a v2 receipt (default set = the 5 custody paths)
python3 custody-pair.py capture --out /path/receipt.txt [--label "pre-install"] [--paths ...]

# verify two receipts (any mix of v1/v2 shapes)
python3 custody-pair.py verify receipt-A.txt receipt-B.txt

# verify a receipt against the live filesystem
python3 custody-pair.py verify receipt-A.txt --live

# verify with a coverage gate: exit 2 when the reference carries fewer than N paths
python3 custody-pair.py verify receipt-A.txt --live --require-paths 5

# fixture-based selftest (never touches a custody path)
python3 custody-pair.py selftest [--scratch /dev/shm]

# print the 5 canonical paths
python3 custody-pair.py paths
```

`capture` also writes a `<receipt>.sha256` sidecar (the receipt's own digest, so
every receipt carries a re-derivable identity). Scratch defaults come from
`$CUSTODY_PAIR_SCRATCH`, then `/dev/shm`, then `/var/tmp` — **never `/tmp`**
(quota-exhausted on this host, EDQUOT).

`capture` refuses to write its receipt over any path it is measuring or any of
the five custody paths — by resolved path *or* by inode (a hardlink alias is
refused too). `selftest --scratch` requires an existing, non-`/tmp` directory;
anything else is a declared USAGE exit 2.

## Receipt fields (v2)

Per path: `EXISTS`, `TYPE`, `SIZE`, `SHA256`, `MTIME_EPOCH`, `MTIME_NS`,
`MTIME_UTC_RENDER`, `MTIME_LOCAL_RENDER`, `CTIME_EPOCH`, `CTIME_NS`,
`CTIME_UTC_RENDER`, `CTIME_LOCAL_RENDER`, `INODE`, `MODE`, `UID`, `GID`.

Two contracts hold here:

- **Content identity is `SHA256`.** Unchanged bytes ⇒ unchanged digest.
- **Rewrite identity is `INODE` + `CTIME` (+`MTIME_NS`).** A user can restore
  mtime (`utime`), but ctime cannot be set, so any write, chmod, or replace
  moves at least one of these fields. A symlink is captured with `lstat`, its
  type recorded, and `SHA256` then covers the link target string.

`atime` is deliberately **not** captured: reading a file (including this
instrument's own sha256 pass on a relatime mount) can move it, which would make
the instrument non-idempotent over its own use.

## The two v1 defects this instrument closes

1. **Label defect.** The round-1 canonical receipt printed the local `-03`
   mtime string under an `MTIME_UTC` label (round 1 measured: epoch `1792011200`
   = `2026-10-14T20:53:20Z` = `2026-10-14 17:53:20 -03`; the receipt printed
   `2026-10-14 17:53:20` as `MTIME_UTC` — off by 3 h). v2 renders UTC strictly
   from the epoch via `time.gmtime()` into `MTIME_UTC_RENDER` and records the
   local render separately under `MTIME_LOCAL_RENDER`. The UTC render is
   TZ-independent by construction (selftest case
   `label-utc-render-tz-independent`).
2. **Sha-only blindness.** sha256-only custody cannot see a same-content
   rewrite (round-1 attack 3). v2 detects it through `INODE`/`CTIME_NS`/
   `MTIME_NS` even when the digest and the mtime are unchanged (selftest cases
   `same-content-rewrite-inplace-ctime-pin`, `same-content-rewrite-rename-inode-pin`).

## Exit codes (declared)

| code | class | meaning |
|---|---|---|
| 0 | `MATCH` / `MATCH-V1-PARTIAL` | every compared path agrees on every comparable field |
| 10 | `CONTENT-DRIFT` | `SHA256` differs on ≥1 path |
| 11 | `REWRITE-DRIFT` | digest equal but `inode`/`ctime`/`mtime` moved on ≥1 path (same-content rewrite) |
| 12 | `METADATA-DRIFT` | digest + identification times equal but `mode`/`uid`/`gid`/`size`/`type` differ, or an `EXTRA-PATH` appears on the candidate side, or a receipt's own epoch/render pair is inconsistent (`LABEL-INCONSISTENT`), or a v1 label defect is reproduced (`LABEL-DEFECT`) |
| 13 | `ABSENT` | ≥1 reference path is missing on the candidate side |
| 14 | `UNEVALUABLE` | a path exists but could not be evaluated (`EACCES` on open, or a stat error other than `ENOENT`): the receipt records `READ-ERROR`/`STAT-ERROR` and is still written; `verify` never reads such a path as `MATCH` |
| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, a refused/failed write, fewer reference paths than `--require-paths N` demands, or an unusable `selftest --scratch` base |
| 3 | `SELFTEST-FAIL` | a selftest case failed |

`capture` exits `0` with every requested path present (5/5 for the default set),
`14` when at least one requested path is present-but-unevaluable, else `13` when
at least one requested path is absent — the receipt is written either way.

Severity precedence for the verdict of a `verify` run: `CONTENT-DRIFT` >
`UNEVALUABLE` > `ABSENT` > `REWRITE-DRIFT` > `METADATA-DRIFT` > `MATCH`. The
report always prints
per-path classes, a `SHA256-CONTRACT: n/m paths agree on sha256` line, and a
final `CUSTODY_PAIR_VERIFY: <class> paths=… drift=… exit=…` line.

## v1 compatibility

Three v1 shapes are parsed and compared on the fields they actually carry:

| shape | example in-tree | compared fields |
|---|---|---|
| `stanza-v1` | `arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | sha256, size, mode, uid, gid |
| `sums-v1` | `arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt` | sha256 |
| `pipe-v1` | `arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt` | sha256, size, inode |

A v1 comparison prints `MATCH-V1-PARTIAL` (severity `MATCH`) when all comparable
fields agree and reports the field count; a sha256 mismatch is still
`CONTENT-DRIFT`. An unparsable receipt is a `USAGE` (exit 2) — never a silent
pass. When a v1 time string sits next to a live epoch, the instrument renders the
epoch both ways and reports `LABEL-DEFECT` if the v1 string matches the local
render and not the UTC render.

## Selftest

`selftest` builds all fixtures in a scratch dir (never a custody path) and runs
22 cases: the round-2 fifteen (capture shape + sidecar identity, receipt-vs-live
clean, same-content rewrite in place (ctime pin) and via rename (inode pin),
content drift, absent path, mode drift, TZ-independence of the UTC render,
v1-stanza/v1-sums/v1-pipe compatibility with mutation detection,
unparsable-receipt usage exit, refusal to write a receipt over a custody path)
plus the round-3 seven: `unreadable-path-is-unevaluable`,
`unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches`,
`partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`,
`selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias`.
It ends with

```
CUSTODY_PAIR_SELFTEST: CLEAN cases=22 passed=22 failed=0 exit=0
```

## Round evidence

`../waves/arc3-loop1-round2/claims/c3/EX-31/` holds the live pre/post pair
(`capture-pre.txt`, `capture-post.txt` + sidecars, both 5/5 exit 0), the
matching `verify` runs, the v1-compat runs, the six-attack harness
(`attacks.sh` → `attacks.out`), and the selftest transcript.
