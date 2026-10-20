# custody-pair (v2 custody receipt instrument)

Seat EX-31 (chain c3, wave `arc3-loop1-round2`), revised by seat EX-21 (chain c2,
wave `arc3-loop1-round3`) and again by seat EX-21 (chain c3, wave
`arc3-loop1-round4`). Operator-owned custody for the five paths the province
freezes:

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

# verify with a coverage gate: exit 2 when the reference carries fewer than N
# distinct resolved paths
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

`capture` refuses to write its receipt **or its derived `<receipt>.sha256`
sidecar** over any path it is measuring or any of the five custody paths — by
resolved path *or* by inode (a hardlink alias is refused too) — and refuses a
receipt or sidecar aimed at the sidecar-shaped neighbour (`<measured> +
".sha256"`) of a measured path. `selftest --scratch` requires an existing,
non-`/tmp` directory; anything else is a declared USAGE exit 2.

## Receipt fields (v2)

Per path: `EXISTS`, `TYPE`, `SIZE`, `SHA256`, `MTIME_EPOCH`, `MTIME_NS`,
`MTIME_UTC_RENDER`, `MTIME_LOCAL_RENDER`, `CTIME_EPOCH`, `CTIME_NS`,
`CTIME_UTC_RENDER`, `CTIME_LOCAL_RENDER`, `INODE`, `MODE`, `UID`, `GID`.
An unevaluable stanza replaces `SHA256` with `READ-ERROR` (exists but
unreadable) or `STAT-ERROR` (lstat failed) and is exit class 14, never a pass.
A cleanly-absent stanza (`EXISTS: no`, no error key) is the declared `MATCH`
case on both sides — see "The both-absent `MATCH`" below.

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

## Round-3 hardening (arc3-loop1-round3, seat EX-21)

Four round-2 named debts closed, each with a declared exit class (patch sources
in `.ufo/waves/arc3-loop1-round3/claims/c2/PL-2/`):

- **D2 → `UNEVALUABLE` (14).** An exists-but-unreadable path (`READ-ERROR`) or a
  stat-blocked path (`STAT-ERROR`) is recorded, the receipt is still written,
  and `verify` classifies it `UNEVALUABLE` **before** the both-absent `MATCH`
  branch — live, and receipt-vs-receipt (the parser reads both error keys). The
  round-2 tool read an EACCES path as `MATCH exit 0` and crashed on a mode-000
  file.
- **D3 → `--require-paths N` (USAGE 2).** A reference carrying fewer than N
  **distinct resolved paths** is a USAGE exit with a `REFERENCE-COVERAGE: n/N …
  unaccounted: …` line. Opt-in: without the flag the comparison is exactly the
  reference's paths, unchanged. (The distinct-path basis is round 4's fix for
  residual (c); the round-3 revision counted stanzas.)
- **Write-guard scope (VZ-4 A11 + RV-11 D7) → USAGE 2.** `--out` is refused when
  it resolves to, or shares an inode with, any measured path or any custody
  path: `--paths X --out X` no longer clobbers X, and a hardlink alias is
  refused. Self-harm guard, not a security boundary (TOCTOU residual named).
  Round 4 extends the same guard to the derived sidecar path and to
  sidecar-shaped neighbours of the measured paths (residual (a) above).
- **D6 → USAGE 2.** `selftest --scratch` on a missing / non-directory / `/tmp`
  base is a declared USAGE exit with a message, not a raw traceback.

The round-3 live receipt pair (`verify pre post --require-paths 5` → `MATCH
5/5 exit 0`) and the full before→after matrix live in
`.ufo/waves/arc3-loop1-round3/claims/c2/EX-21/`.

## Round-4 hardening (arc3-loop1-round4, seat EX-21)

Three residuals the round-3 verdict named, each re-measured on the round-3
landed revision before this revision was written, each closed with a declared
exit class:

- **(a) sidecar / neighbour scope → USAGE 2.** The guard examines the receipt
  path **and** its derived sidecar path, each against the measured paths and the
  five custody paths by resolved path and by inode, and refuses a receipt or
  sidecar landing on the sidecar-shaped neighbour (`<measured> + ".sha256"`) of
  a measured path. Before: `capture --out X --paths X.sha256` exited **0** and
  the sidecar write destroyed `X.sha256` — the file the same run had just
  measured. The sidecar name is derived inside the guarded region, so an `--out`
  with no usable name (`''`, `'.'`) is a USAGE exit 2, not a `ValueError`
  traceback.
- **(b) receipt-directory failures → USAGE 2.** `out.parent.mkdir(...)` runs
  inside a guarded block: a non-directory component, a symlink loop (ELOOP), or
  any other `OSError` is a declared USAGE exit 2 with a message. Before:
  `capture --out <regular-file>/sub/r.txt` died with a raw `NotADirectoryError`
  traceback at exit 1, outside the declared map.
- **(c) coverage-gate basis → USAGE 2.** `--require-paths N` counts **distinct
  resolved paths**, the same basis as its own `unaccounted:` list. Before: five
  duplicate stanzas for one path satisfied `--require-paths 5` silently (exit 0,
  no coverage line printed, the other four custody paths unexamined).

The before→after injections, the 28-case selftest transcript, the live receipt
pair captured by the revised tool, and the round-3 regression battery re-run
live in `.ufo/waves/arc3-loop1-round4/claims/c3/EX-21/`.

## The both-absent `MATCH` (ruling, arc3-loop1-round4)

Ruling text authored by seat EX-26 (chain c3, wave `arc3-loop1-round4`), adopted
here by seat EX-21 with one clause corrected: EX-26's closing sentence described
the coverage gate as a *stanza* gate, which residual (c)'s closure above makes
false — the gate is a distinct-resolved-path gate as of this revision.

The round-2 D2 debt named the `MATCH exit 0` on a both-sides-absent path as part of
the fail-open class. This instrument adjudicates that reading, and the adjudication
is the declared design: **only error-carrying stanzas are `UNEVALUABLE`; a cleanly
absent stanza on both sides is `MATCH`.**

- *Cleanly absent* means the stanza records no `SHA256` and carries no
  `READ-ERROR`/`STAT-ERROR` on either side. The `MATCH` rests on the two stanzas'
  own recorded existence state (`EXISTS: no` on both) — that is the fact the
  both-absent branch tests, and it is the only branch that can produce this row.
  The row prints `compared=0/11` because there is nothing further to compare, not
  because the comparison is empty. Absence on one side only is `ABSENT` (13): a
  reference path that appears later is still caught.
- *Error-carrying* is the fail-open class the debt named: a stanza carrying
  `READ-ERROR` or `STAT-ERROR` on either side is `UNEVALUABLE` (14), classified
  **before** the both-absent branch, so an unreadable path can never read as a
  `MATCH`. This holds receipt-vs-live and receipt-vs-receipt (the parser reads both
  error keys).
- Severity is unchanged: a cleanly-absent stanza never outranks `UNEVALUABLE` or
  `CONTENT-DRIFT` in the verdict — a mixed pair reports the worst class it found.

A receipt pair over cleanly-absent paths is therefore a positive record ("absent on
both sides"), not a vacuous pass — but it is a weak witness by construction: no
content is compared. Pair an all-absent reference with a present-path reference
when the witness is meant to carry content. Closing this with a flag was
considered and rejected: the round-3 evidence is that the fail-open lived in the
error-carrying form, which the `UNEVALUABLE` class already closes. The coverage
gate is a distinct-path gate since round 4 (residual (c) above), so padding a
reference with duplicate stanzas no longer satisfies `--require-paths N`.

## Exit codes (declared)

| code | class | meaning |
|---|---|---|
| 0 | `MATCH` / `MATCH-V1-PARTIAL` | every compared path agrees on every comparable field |
| 10 | `CONTENT-DRIFT` | `SHA256` differs on ≥1 path |
| 11 | `REWRITE-DRIFT` | digest equal but `inode`/`ctime`/`mtime` moved on ≥1 path (same-content rewrite) |
| 12 | `METADATA-DRIFT` | digest + identification times equal but `mode`/`uid`/`gid`/`size`/`type` differ, or an `EXTRA-PATH` appears on the candidate side, or a receipt's own epoch/render pair is inconsistent (`LABEL-INCONSISTENT`), or a v1 label defect is reproduced (`LABEL-DEFECT`) |
| 13 | `ABSENT` | ≥1 reference path is missing on the candidate side |
| 14 | `UNEVALUABLE` | a path exists but could not be evaluated (`EACCES` on open, or a stat error other than `ENOENT`): the receipt records `READ-ERROR`/`STAT-ERROR` and is still written; `verify` never reads such a path as `MATCH` |
| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, a refused/failed write (including a receipt or sidecar aimed at a measured path, a custody path, or the sidecar-shaped neighbour of a measured path, and a receipt directory that cannot be created), fewer distinct reference paths than `--require-paths N` demands, or an unusable `selftest --scratch` base |
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
31 cases: the round-2 fifteen (capture shape + sidecar identity, receipt-vs-live
clean, same-content rewrite in place (ctime pin) and via rename (inode pin),
content drift, absent path, mode drift, TZ-independence of the UTC render,
v1-stanza/v1-sums/v1-pipe compatibility with mutation detection,
unparsable-receipt usage exit, refusal to write a receipt over a custody path),
the round-3 seven: `unreadable-path-is-unevaluable`,
`unevaluable-never-matches`, `parsed-unevaluable-reference-never-matches`,
`partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`,
`selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias`,
and the round-4 six: `coverage-gate-rejects-duplicate-stanzas`,
`coverage-gate-passes-distinct-five`, `refuses-sidecar-over-measured-file`,
`refuses-receipt-over-sidecar-neighbour`,
`out-parent-not-a-directory-usage-exit`,
`both-sides-absent-is-agreement-match`,
the round-18 two: `repo-header-off-branch-tip-no`,
`repo-arg-and-lane-root-default`,
and the round-19 red case `repo-root-is-toplevel-not-subdir-arg` (a `--repo`
subdirectory argument must print the repository top level as `repo-root` and
keep the argument as `repo-arg`).
It ends with

```
CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0
```

## Round evidence

`../waves/arc3-loop1-round2/claims/c3/EX-31/` holds the live pre/post pair
(`capture-pre.txt`, `capture-post.txt` + sidecars, both 5/5 exit 0), the
matching `verify` runs, the v1-compat runs, the six-attack harness
(`attacks.sh` → `attacks.out`), and the selftest transcript.

`../waves/arc3-loop1-round3/claims/c2/EX-21/` holds the round-3 revision's
evidence: the before→after injection matrix (PL-2's harness run on the base blob
and on the landed revision), the 22-case selftest transcript, the live
pre/post pair captured **by the revised tool** (both receipts self-pin its
sha256) verified `MATCH 5/5` with and without `--require-paths 5`, the
cross-revision check (round-start receipt captured by the previous revision vs
the revised-tool post receipt → `MATCH 5/5`), the v1-shape control runs, and the
round-2 six-attack harness re-run (identical classes).

`../waves/arc3-loop1-round4/claims/c3/EX-21/` holds the round-4 revision's
evidence: the before probes (all three residuals reproduced on the round-3
bytes), the anchored patch generator, the 28-case selftest transcript, the
three-injection before→after matrix, the round-3 regression battery re-run
(41/41 rows hold, including the live pair `MATCH 5/5` and the receipt
self-pin), the cross-seat drivers' after-runs (EX-23's sidecar probe, RV-7's
probe, SC-3's injection harness), and the fresh sha256 of the landed tool.
