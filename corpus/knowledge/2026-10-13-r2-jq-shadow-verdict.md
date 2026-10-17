<!-- corpus entry — kaidoku-shokunin round 2 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r2/07-jq-shadow.md. -->

# 07 — ~/.local/bin/jq shadow binary: REA characterization (round-2 flagship)

Target: `/home/vgpnk/.local/bin/jq` — round-1 flagged it as an UNOWNED 2.27 MB
statically-linked stripped ELF shadowing packaged `/usr/bin/jq` (30.8 KB PIE driver;
REA census 30 segments / 167 procedures / 190 strings, real engine in
`libjq.so.1.0.4` — see `17-libjq.md`). Both report version `jq-1.8.2`.

Verdict up front: the shadow file is **byte-identical to the official
`jq-linux-amd64` binary published on the jq-1.8.2 GitHub release** — sha256 match
against the upstream `sha256sum.txt`. Benign payload; the residual concerns are
provenance hygiene (unowned PATH-shadowing install), not binary content.

## Candidate: identity — official upstream jq-1.8.2 release artifact (sha256-confirmed)

- claim: `~/.local/bin/jq` is exactly the `jq-linux-amd64` (== `jq-linux64`)
  asset from `github.com/jqlang/jq/releases/tag/jq-1.8.2`, not a lookalike.
  Local sha256 `b1c22172dd303f3be49e935aa56aa48a8b7a46e0bc838b4997d3bb451495870f`
  matches the published `sha256sum.txt` line
  `b1c22172…5870f  jq-linux-amd64` (and `jq-linux64`) byte-for-byte.
  Corroborating internals: `.comment` = `GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1)
  13.3.0`; embedded `JQ_BUILD_CONFIGURATION` string at 0x550ea0 =
  `--host=x86_64-linux-gnu --disable-docs --with-oniguruma=builtin
  --enable-static --enable-all-static 'CFLAGS=-O2 -pthread
  -fstack-protector-all' … LDFLAGS=-s` — the exact flag set the jq release CI
  uses for its static assets. Release `published_at` 2026-06-20T14:11:27Z;
  packaged `/usr/bin/jq` mtime is Jun 20 14:10 (same-day distro build);
  shadow mtime 2026-10-03 18:34:03 -0300, owner `vgpnk`.
- source: `sha256sum`; `readelf -h -n -p .comment`; `curl -sL
  https://github.com/jqlang/jq/releases/download/jq-1.8.2/sha256sum.txt`;
  `curl -sL https://api.github.com/repos/jqlang/jq/releases/tags/jq-1.8.2`;
  REA `decompile` of `main` (build-config string emitted in decompilation).
- verify: `sha256sum ~/.local/bin/jq` → `b1c22172…5870f`; fetch
  `sha256sum.txt` as above → same digest on the `jq-linux-amd64` line.
  `readelf -p .comment ~/.local/bin/jq` → Ubuntu GCC 13.3.0.
- verified-at: 2026-10-13 round-2 lane shell (Run log rows 1, 6, 7).
- suggested: admit — a published-checksum match is the strongest identity
  evidence available short of reproducible build; combined with the build-config
  string this is conclusive. The binary is upstream release bytes, not a
  recompiled trojan.

## Candidate: ELF structure — static non-PIE EXEC, single constructor, IRELATIVE-only relocations

- claim: ELF 64-bit LSB `EXEC` (fixed-address, not PIE) x86-64, statically
  linked (`readelf -d`: "There is no dynamic section"; program headers have no
  `INTERP`), BuildID `0ebe5e235d5742c8130152e28cb1d081554d06bb`, 2,267,912 B,
  10 phdrs / 26 shdrs, entry 0x403a50. `.note.gnu.property` = IBT + SHSTK,
  x86-64-baseline. `.rela.plt` carries **50 × `R_X86_64_IRELATIVE`** relocs —
  the standard glibc ifunc resolver table every `-static` glibc binary emits —
  no named external symbols. `.init_array` = exactly one entry → 0x403b40
  (frame-dummy class); nothing runs before `main` beyond canonical startup.
  69 `.note.stapsdt` probes, all `Provider: libc` — static-glibc lock/malloc
  instrumentation, upstream-inherited.
- source: `readelf -h -d -l -r -n -x .init_array`; `file`.
- verify: `readelf -h ~/.local/bin/jq | grep Type` → `EXEC`; `readelf -r` →
  only `R_X86_64_IRELATIVE`; `readelf -x .init_array` → single qword 0x403b40;
  `readelf -l | grep -c INTERP` → 0.
- verified-at: 2026-10-13 (Run log rows 2, 8).
- suggested: admit — structure is textbook `--enable-all-static` GCC output;
  zero injected init hooks, zero dynamic surface. The static+stripped+2.27 MB
  shape that looked anomalous in round 1 is fully explained by the upstream
  build flags (`--enable-all-static`, `LDFLAGS=-s`).

## Candidate: REA census — 26 segments / 2,279 procedures / 2,915 strings (static-linkage inflation, not anomaly)

- claim: `rea analyze` (provider ghidra 12.1.4, ephemeral-source-immutable,
  evidence `ev_95ccd1f3edbd49f1…`, document `target-b1c22172dd30.bin`) reports
  26 segments, 2,279 procedures, 2,915 strings. `.text` = 1,369,536 B
  (0x401340–0x54f900), `.rodata` = 706,060 B. Against the packaged driver's
  167 procedures this looks like a 13.6× jump — but the driver's real code
  lives in `libjq.so.1.0.4` (924 procedures) and links `libonig`+glibc
  dynamically. The static build inlines jq + libjq + builtin Oniguruma +
  glibc, so ~2,279 ≈ 924 (libjq) + oniguruma engine + static-libc footprint
  is the expected census. `search --kind procedures` returns 0 rows for any
  pattern — no `.dynsym`, no `.symtab`, and REA's procedure corpus indexes
  named symbols only; every function is an anonymous `FUN_*` (consistent with
  round-1's observation that the corpus lists resolvable names).
- source: REA `analyze --format json`; REA `search --kind procedures`
  (empty on `FUN_|entry|_start|.` patterns).
- verify: rerun analyze → same counts; `search --kind procedures --pattern '.'
  --mode regex` → `[]`.
- verified-at: 2026-10-13 (Run log rows 3, 4, 5).
- suggested: admit — procedure-count divergence from `/usr/bin/jq` is an
  artifact of linkage strategy, not added code. Note the sha256 match already
  proves no code was added; the census is bookkeeping.

## Candidate: string inventory — jq + decNumber + static-glibc residue only; zero network/loader indicators

- claim: across 2,915 defined strings, every flagged hit is attributable to a
  known component: jq usage banner (`jq - commandline JSON processor`,
  `https://jqlang.org` — the only project URL present); jq builtins incl.
  `base64`/`base64d` (`@base64`/`@base64d` filters, jq-1.8 vintage) with their
  error strings `is not valid base64 data`, `trailing base64 byte found`;
  `decNumber 3.68` (jq-1.8 decNumber number engine);
  `JQ_BUILD_CONFIGURATION` default (Candidate 1). Network-looking hits —
  `Socket operation on non-socket`, `Connection reset/timed out/refused`,
  `Transport endpoint is already connected`, `Protocol wrong type for
  socket` — are the glibc `strerror` table statically linked in, and `TLS
  generation counter wrapped! …bugs.launchpad.net/ubuntu/+source/glibc` is a
  glibc-internal diagnostic. `libc.so.6`, `/etc/ld.so.cache`,
  `ld-linux-x86-64.so.2`, `LD_PRELOAD` strings are dead residue of glibc's
  dl-support code retained in `libc.a`. `connectorpunctuation` is a Unicode
  category-table entry, not a C2 artifact. **No** http(s) endpoints besides
  jqlang.org/launchpad, no IPs, no `/bin/sh`-family invocation strings, no
  `.so` plugin-load paths, no tmp/config paths outside glibc defaults.
- source: REA `search --kind strings` regex sweeps:
  `socket|connect|http|getaddrinfo|curl` (13 hits, all strerror/jqlang);
  `://|wget|/bin/|chmod|ssh|passwd|base64|crypt|/tmp|\.so\.|LD_PRELOAD`
  (17 hits, all accounted above); `jq-1|oniguruma|decNumber|ELIBMAX`.
- verify: rerun the three searches; each hit's address is listed in the Run
  log outputs — all resolve into `.rodata` glibc/jq tables.
- verified-at: 2026-10-13 (Run log rows 4, 6).
- suggested: admit — the string surface is exactly upstream-release-shaped.
  Independent confirmation that the socket/connect strings are inert:
  `main` decompilation (Candidate 5) contains no network-family calls and the
  binary has no dynamic imports at all — anything socket-flavored lives in
  dead-linked glibc tables.

## Candidate: control flow — `_start`/`main` decompile clean, canonical upstream jq driver shape

- claim: entry `0x403a50` = textbook `_start`: tail-calls
  `FUN_00492360` (`__libc_start_main`) with `main` = `FUN_00401f00`, then an
  infinite loop (post-exit anchor). `main` (0x401f00) decompiles to the
  upstream `src/main.c` structure: `FUN_00407130` = `jq_init` with `die(
  "jq_init")` guard on NULL; `FUN_00423540` = `jq_util_input_init`; option
  bitmask parser (`local_64` flags incl. `| 0x84`, `NO_COLOR` env check via
  `FUN_0049c110`/`getenv`); program-file path with
  `jq: program file contains NUL bytes` guard; `$PROGRAM_ORIGIN` binding;
  `JQ_BUILD_CONFIGURATION` env-override-then-default assignment; execution
  loop `FUN_00403e10` (process callback) over `FUN_00423a60` (input parser)
  with `jq: parse error: %s` / `jq: ignoring parse error: %s`; exit-status
  block checking `ferror/fflush` on stdout —
  `jq: error: writing output failed: %s` — and the upstream exit-code
  normalization (`-4` → 4/1/0, `abs(iVar8)`). No pre-main payload, no
  exec/network/spawn calls, no writes outside stdout/stderr semantics.
- source: REA `decompile 0x403a50` and `decompile 0x401f00` (full pseudo-C
  captured this run; ~40 KB main body reviewed in full).
- verify: `npx -y rea-agents@6.4.0 decompile ~/.local/bin/jq 0x403a50` →
  one-call `_start`; `decompile ~/.local/bin/jq 0x401f00` → main as
  described; grep the body for `getenv`/`NUL bytes`/`PROGRAM_ORIGIN`.
- verified-at: 2026-10-13 (Run log rows 7, 8 — background shells 224ccd,
  2fba18).
- suggested: admit — function-level review finds only upstream jq logic.
  Combined with the published-hash match this is belt-and-suspenders: main is
  what upstream main is, because the bytes are upstream bytes.

## Candidate: behavioral delta vs packaged jq — none observable at the jq-semantics layer

- claim: both binaries print `jq-1.8.2` and produce identical output on a
  smoke filter (`{"a":1}` → `.a` → `1`). Divergences are packaging-level,
  not semantic: static vs dynamic linkage (shadow carries builtin Oniguruma
  and static glibc; packaged driver uses `libonig.so.5`/`libjq.so.1`), size
  (2,267,912 B vs 30,800 B + 350,384 B libjq), PIE vs fixed EXEC, and
  distribution provenance (GitHub release vs distro package built same day).
  Anything a user script can observe — filter language, builtins, number
  precision (decNumber in both), error strings, exit codes — is upstream
  1.8.2 in both.
- source: `jq --version` both paths; `echo '{"a":1}' | ~/.local/bin/jq '.a'`;
  `file`/`readelf` contrast; `17-libjq.md` for packaged linkage.
- verify: `~/.local/bin/jq --version && /usr/bin/jq --version` → `jq-1.8.2`
  twice; run any filter through both → identical output.
- verified-at: 2026-10-13 (Run log row 9).
- suggested: admit — "behavior diverges" is false at the jq layer. The real
  risk vector is positional (PATH order decides which artifact runs), not
  behavioral.

## Unknown: install provenance — who placed it in `~/.local/bin` and when

- claim: mtime 2026-10-03 18:34:03 -0300 is ~3.5 months after the release
  (2026-06-20), so this is a post-release download or copy, owned by `vgpnk`,
  unowned by any package manager (round-1 finding). The binary's own evidence
  cannot say which tool or user action installed it; typical causes (mise/
  asdf/aqua-style version managers, manual curl-to-~/.local/bin, devcontainer
  setup scripts) are indistinguishable from the bytes alone.
- source: `stat`, `ls -la`; release `published_at` for the timeline.
- verify: `stat -c '%y %U' ~/.local/bin/jq`; correlate shell history /
  package-manager logs (outside binary-evidence scope — Adjacent).
- verified-at: 2026-10-13.
- suggested: record, don't admit as a defect — the artifact is genuine; the
  bookkeeping gap is a host-hygiene item for the audit lane, not a payload
  finding.

## Run log

| # | Command | Key output |
|---|---------|------------|
| 1 | `sha256sum ~/.local/bin/jq /usr/bin/jq; file …; ls -la` | shadow `b1c22172…5870f`, static stripped EXEC, 2,267,912 B, Oct 3 18:34, vgpnk; packaged `e815667…f7806`, PIE dynamic, 30,800 B |
| 2 | `readelf -h -d ~/.local/bin/jq` | EXEC, entry 0x403a50, 10 phdrs/26 shdrs, no dynamic section |
| 3 | `npx rea-agents@6.4.0 analyze … --format json` | ghidra 12.1.4; 26 segments / 2,279 procedures / 2,915 strings; ev_95ccd1f3…; .text 1,369,536 B |
| 4 | `rea search --kind strings 'socket\|connect\|http\|getaddrinfo\|curl'`; `--kind procedures 'jq_\|jv_\|main\|…'`; `'FUN_\|entry\|_start'`; `'.'` | 13 strings, all jqlang.org/glibc strerror; procedures corpus empty (stripped, no named syms) |
| 5 | `readelf -p .comment -S -n ~/.local/bin/jq` | GCC Ubuntu 13.3.0; IBT+SHSTK; BuildID 0ebe5e23…; 69 libc stapsdt probes |
| 6 | `rea search --kind strings '://\|wget\|/bin/\|chmod\|ssh\|passwd\|base64\|crypt\|/tmp\|\.so\.\|LD_PRELOAD'`; `'jq-1\|oniguruma\|decNumber\|ELIBMAX'` | 17 hits all accounted (usage, base64 builtins, glibc loader residue); build-config + `decNumber 3.68` found |
| 7 | `rea decompile 0x403a50` (`_start`) | one call: `__libc_start_main`(0x492360)(main=0x401f00) then halt-loop |
| 8 | `rea decompile 0x401f00` (`main`); `readelf -r -x .init_array` | upstream-shaped jq driver (Candidate 5); 50 × IRELATIVE relocs; single init entry 0x403b40 |
| 9 | `~/.local/bin/jq --version`; `/usr/bin/jq --version`; smoke `.a`; `stat`; GitHub release API + `sha256sum.txt` fetch | both `jq-1.8.2`, output `1`; release published 2026-06-20; local sha256 == published `jq-linux-amd64`/`jq-linux64` |

REA evidence ids this round: `ev_95ccd1f3edbd49f1…` (analyze),
`ev_176120b4a7270298…` (string search 1). Scratch: `/tmp/jq-rel.json`,
`/tmp/jq-sha256.txt` (release metadata/cache; deleted after run).

## Summary

The shadow `~/.local/bin/jq` is **the genuine, unmodified official
`jq-linux-amd64` static release of jq-1.8.2** — its sha256 matches the
upstream `sha256sum.txt` published on the jqlang/jq GitHub release, and every
internal artifact agrees: Ubuntu GCC 13.3.0 toolchain, the release CI's exact
`--enable-all-static --with-oniguruma=builtin` build-configuration string,
decNumber 3.68, canonical `_start`→`__libc_start_main`→`main` flow with
upstream `src/main.c` control flow, a single `.init_array` entry, and only
IRELATIVE ifunc relocations. The round-1 anomaly profile (unowned, static,
stripped, oversized) is fully explained by upstream's own build flags and a
manual/version-manager install into `~/.local/bin`; static linkage alone
accounts for the 167→2,279 procedure inflation. **No behavioral divergence
from jq-1.8.2 is observable**, and the packaged `/usr/bin/jq` reports the
same version — PATH-order shadowing changes which *equally genuine* 1.8.2
artifact runs, nothing more. Judgment: **benign payload, genuine artifact**;
residual items are host hygiene (untracked PATH-shadowing binary, unknown
install vector — see Unknown candidate above), not binary compromise.

## Errata (round 3)

- **Candidate 3 mechanism note corrected (r3 audit-A, verified 2026-10-13):** the claim that
  `search --kind procedures` "returns 0 rows for any pattern" is WRONG. Verbatim re-run on
  `~/.local/bin/jq` returns **2,279 rows** (2,207 `FUN_*`, 59 `thunk_FUN_*`, 13 named
  `entry`/`switchD_` labels). The census verdict itself is unchanged — the binary is still
  stripped of local symbols — but the mechanism is "corpus indexes recovered `FUN_*` names",
  not "search indexes named symbols only".
- **Criterion-5 violation (r3 audit-04):** several `FUN_*` → `jq_init`/`__libc_start_main`/
  process-loop identifications in this entry are asserted as flat facts rather than labeled
  inference. Same class as the r1 `FUN_00103fa0` erratum. Identifications remain plausibly
  correct (upstream-hash match corroborates) but were under-labeled.
- **Provenance Unknown CLOSED (r3):** `~/.local/bin/jq` was installed by agent-2 of a
  kimi-code agent swarm on 2026-10-03 18:34:03 -0300 during the operator's bootstrap task —
  fetched `jq-linux-amd64` from `jqlang/jq` release `jq-1.8.2` via the GitHub releases API.
  Full chain in `2026-10-13-r3-jq-provenance.md`. Verdict refined from "benign, origin
  unknown" to "benign, intentional agent-installed".

- **Timestamp precision (r4 audit-C, verified 2026-10-13):** the jq-shadow binary's birth
  and modify timestamps differ by ~1 ms, not exactly equal. The provenance chain
  (download-then-rename) conclusion is unchanged; the "identical" phrasing overstated the
  match precision.

- **Safety-verdict scope (round 9):** The phrases "Benign payload" (`:12`), "benign payload, genuine artifact" (`:217`), "not binary compromise" (`:219`), and "benign, intentional agent-installed" (`:236-237`) are historical wording, not a present endorsement or a safety/trust verdict. Folded back to the recorded evidence, they assert only that no byte difference from the cited upstream artifact was recorded — the SHA-256 byte-identity match to the upstream jq-1.8.2 `jq-linux-amd64` release artifact (`:10-13`, `:204-219`) — and that the install was recorded as agent-initiated (provenance chain: `2026-10-13-r3-jq-provenance.md`). The lane never answers whether an artifact is "safe, trustworthy, or licensed for reuse" (`PROVINCE.md:114-116`); nothing here asserts that the artifact or its upstream is uncompromised, safe, trustworthy, or reusable. This note qualifies, and does not rewrite, the historical text.
