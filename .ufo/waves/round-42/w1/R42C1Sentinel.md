**DEFECTS FOUND** — the v3 chain itself is sound in the places round 41 was attacked (in-tool hashing/carving is race-free, poisoned caches fail closed), but the draft's C1 design cannot be scored as written on a v3 carrier (the lane reader refuses major 3), its oracle rule is unsatisfiable on any image with a symlink (measured: 7-Zip calls links regular files and rewrites their targets), its "sasquatch -be|-le" property has no binding at all (measured: a `sasquatch` shim delegating to `unsquashfs` produces a byte-identical projection), and six paths it reads are outside its frozen set (one of them makes the freshness clause forgeable).

# R42C1Sentinel — C1 carrier chain and freeze design, attacked

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`. Every number below is from a probe in
`artifacts/R42C1Sentinel/probe-log.md` (P1–P10) or a source line I quote. No REA, unblob,
sasquatch or any extractor was run on a published image or on anything carved from one; the
extractor runs in P5 are on unblob 26.6.4's MIT v3/v4 fixtures, which the round designates C2
development inputs. Nothing was installed or upgraded.

Severities: **Blocking** = the draft predicate cannot pass or cannot be evaluated at the freeze;
**High** = a forged or substituted result can score; **Medium** = a real write/read primitive or a
frozen-path hole with a narrower trigger; **Low** = calibration; **Info** = recorded for the L1.

| id | axis | finding | sev |
|---|---|---|---|
| B1 | 3 | `tools/round-41/sqfs-list.py` refuses major 3 (exit 2); `layout_ok`, `carve_ok` and `oracle_rederived` all depend on it, and the draft's frozen list omits any v3 reader | **Blocking** |
| B2 | 3 | the ported `compression_coverage` binding (gzip **and** xz) is unsatisfiable for a v3 family — xz does not exist in v3 | **Blocking** |
| B3 | 4/oracle | "two non-sasquatch readers agree file-for-file" cannot hold on a carrier with a symlink: 7-Zip misclassifies links and rewrites their targets | **Blocking** |
| H1 | 4 | no clause binds the extractor binary; a `sasquatch` shim delegating to `unsquashfs` gives an identical projection (measured) | **High** |
| H2 | 1 | the scored tool never fetches; the carrier `url` is checked for key presence only, so "published third-party" is unverified prose | **High** |
| H3 | 3 | `PRIOR_CARRIERS` (freshness input) is outside the frozen set: delete a pin post-freeze and a re-used carrier becomes "fresh" | **High** |
| H4 | 3 | `XPIN = tools/round-27/xpin-attribute.mjs` is executed for `evidence_id_ok` and is not frozen; the REA package it imports (`--pkg65`) is a mutable npm cache path | **High** |
| H5 | 3 | C2's predicate reads the round-41 C1 receipts/oracles; they are in neither claim's frozen set | **High** |
| M1 | 1 | symlink-following cache writes (round-41 D5) survive if `fetch-carrier.py` is a port of `fetch-vendor.py` | Medium |
| M2 | 1 | `fetch()` follows cross-origin redirects, records only the final status, has no scheme/host allowlist and no size cap (measured) | Medium |
| M3 | 2 | no binding scans the tree for carrier bytes; the 5 MB artifact bound is larger than a v3 image (measured 1.84/1.90 MB) | Medium |
| L1 | 2 | 15,697,248 B of host distro binaries (3 distinct, committed 3× each) and a 2,276,644 B wheel are already committed with no licence text | Low |
| L2 | 1 | pin and image-digest strings are joined into paths before any `SHA_RE` check in the fetcher | Low |
| L3 | 3 | `frozen_drift` builds its set from the spec's optional keys; a carrier without `oracle`/`nonregular` escapes drift | Low |
| L4 | 3 | `receipt_fresh` only constrains the *first* add commit; a rewrite of an added `after.json` is invisible | Low |
| D1 | 5 | no mechanical pre-run detector exists; the four channels that do exist and what each can prove | Info (design) |

---

## 1. Axis 1 — carrier fetch: cache, TOCTOU, symlinks, redirects

### H2 — the carrier URL is never exercised at score time

`c1-counter.py:636` requires the *keys* `('url','image_sha256','member','member_sha256', …)` in an
external carrier and nothing else. `grep -n "'url'|\"url\"|https|scheme"` over the whole counter
returns that one line plus a selftest fixture; there is no `urlopen`, no re-fetch, no scheme test,
no host test. The counter reads `--carrier-cache/<pin>.bin` and hashes it.

Exploit path: a seat writes its own four-file v3 image, pins it, and gives any plausible URL (the
publisher's download page, honestly reached, from which it downloaded *something*). Every C1 clause
then passes: `carrier_pin_ok` (its own bytes), `layout_ok` (its own superblock), `oracle_hits_ok`
(an oracle made from the same image), `carrier_fresh_ok` (a pin round 40/41 never had). "Four
**published third-party images**" rests entirely on the reader's honesty, and H3 makes even the
freshness half forgeable.

Smallest remediation (all decidable offline):
1. `carriers.json` grows `"kind": "published"`, `"source_id": "S###"` and the frozen `fetch`
   receipt filename; `carriers_spec` rejects any carrier without `external` (today a
   `path`-committed carrier satisfies the same schema, which is how round-41's two lane-built
   carriers scored).
2. `fetch-carrier.py` writes `fetch-<id>.json` = `{url, final_url, http_status, content_length,
   etag, last_modified, image_sha256, member, member_sha256, carve_len, pin, tool_sha256}`; the
   receipt is frozen with the claim, and a new binding `fetch_receipt_ok` requires
   `http_status == 200`, `final_url == url` (no redirect), `sha256(url) → image → member → carve →
   pin` recomputed from the frozen fields, and the SOURCES row named by `source_id` to carry the
   same host.
3. Reject `file://` and any non-`https` scheme; the round's own harness already uses `file://` for
   probes (round-41 wave 2 did), so the restriction belongs in the frozen tool, not in policy.

### M2 — redirects, scheme, size (measured)

`fetch()` (P10) follows a 302 to another port/host, returns the final hop's `200`, caches the body
under the *pinned* digest, and records no chain. Integrity still rests on `image_sha256`, so this is
not a substitution primitive by itself — it is a provenance one: nothing a receipt can show
distinguishes "published by the vendor whose page I cite" from "served by any host that the pinned
URL redirected me to". `r.read()` is also unbounded, and the cache write is unbounded.

Remediation: one opener with `HTTPRedirectHandler` subclassed to a zero-redirect policy (or recording
the chain and requiring `final_url == url`), `status == 200` asserted rather than recorded, a
`Content-Length` and total-read cap (the largest legitimate carrier here is ≈33 MB; cap at 512 MiB),
and `urlparse(url).scheme in ('https',)`.

### M1 — symlink write-through survives a port

Round-41 wave 2 demonstrated `open(out+'.part','wb')` and `open(image_cache/want+'.image','wb')`
following a planted symlink (30 MB of vendor firmware written through it, exit 0). The draft puts
`tools/round-42/fetch-carrier.py` in the frozen set without saying it changes. If it is a port, the
primitive is unchanged and now writes *published third-party images*, which is the redistribution the
licence rule forbids — with `image_cache` a caller-chosen path.

Remediation: `os.lstat` refusal (`stat.S_ISLNK`) plus `os.open(..., O_CREAT|O_EXCL|O_NOFOLLOW|
O_WRONLY, 0o600)`, `os.replace` kept (it replaces a symlink rather than following it), cache dir
created with `dir_fd`-relative `os.mkdir` after refusing a cache `realpath` inside the lane or any
`git rev-parse --show-toplevel`, and `lstat` before every cache *read* (round-41 D7: `<pin>.bin` →
`/dev/zero` OOMed the counter before hashing).

### L2 — path joins before validation

`materialise` uses `ext['image_sha256']` as a cache filename and `pin` as `pin+'.bin'` *before* any
64-hex test; the only gate is the digest compare. A 64-char traversal pin still fails at the compare
(round-41 wave 2 measured it), but the fetcher should never build the path: apply `SHA_RE` (the
counter's own regex, `c1-counter.py:317`) at spec load. Server-side this matters for `--spec`
inputs a seat authors.

### What is already right (do not "fix" it)

In-tool TOCTOU is absent: the image bytes are read once into memory, hashed, the member and the carve
are cut from the same object, and the pin is compared *before* `makedirs`/write; a swapped cache file
is caught by the counter's own re-hash (`carrier_pin_ok`), so a poisoned cache can only block a score.
The `.part` + `os.replace` ordering is correct. Keep all three properties when the new tool is written.

---

## 2. Axis 2 — licence: what is actually committed

### Inventory (>1 MB blobs at the base)

51 blobs, 156,406,692 B total. Full table `artifacts/…/scan-large-blobs.tsv`.
Binary content: **10 blobs, 17,973,892 B**:

| path | size | what it is |
|---|---|---|
| `corpus/evidence/round-34/elf/e10.bin` + `.ufo/waves/round-34/prep/…/elf/e10.bin` + `…/elf-meta/m10.bin` | 3 × 2,939,928 | copy of the build host's `/usr/lib/libstdc++.so.6.0.36` |
| `corpus/evidence/round-34/elf/e05.bin` + 2 prep copies | 3 × 1,195,144 | copy of `/usr/bin/bash` |
| `corpus/evidence/round-34/elf/e11.bin` + 2 prep copies | 3 × 1,097,344 | copy of `/usr/bin/net` (Samba) |
| `.ufo/waves/arc3-loop1-round4/claims/c1/EX-02/pycryptodome-3.24.1-…manylinux…whl` | 2,276,644 | third-party wheel |

Everything else >1 MB is text: REA envelopes (`after.json`; keys are `path, relative_path, size,
sha256, mime_type, …` — no bodies), unblob/ghidra logs, diffs, `*.tsv` and JSON receipts, and one
2.29 MB interactive-session transcript.

Third-party *firmware*: none. I scanned all 24,019 blobs in `corpus/evidence` + `.ufo/waves` for a
squashfs superblock at offset 0: 479 hits, **max 447,853 B, none ≥ 1 MiB, none equal to a round-41
carrier pin**, all lane-built synthetic images under `.ufo/waves/round-3x|4x/*/carriers/`
(`scan-squashfs-magic.tsv`). The base is clean of image bytes; the round-41 wave-2 byte-run test and
this magic test agree.

### M3 — the rule is prose, and the size bound does not help

No scored clause looks at the tree for carrier bytes (round-41 D3, still true: `grep` for
`ls-tree|committed|licen` over the frozen round-41 tools hits docstrings only). Two measured reasons
this is not theoretical for r42:

* the round's artifact bound is 5 MB, and a v3 image is **below** it — `HEAD` on the designated
  development class gives 1,839,104 B and 1,904,640 B for Kamikaze 7.09 squashfs `.trx` builds (P9);
* the point of C1 is four carriers from four publishers, i.e. four separate distribution licences
  (DD-WRT GPLv2 with no source offer in the tree, OpenWrt GPLv2, vendor EULA).

Smallest remediation: a binding `no_committed_carrier_bytes` over the `--rev` tree that (a) compares
every blob digest to the four pins and to every oracle row, (b) runs `carrier.find(blob)` for every
carrier against every blob ≥ 32 B (round-41's cost: 1,678 blobs / 41 MB ≈ 5 s), and (c) **skips
zero-length oracle rows** — V3's `tmp/mtab` is the empty file and 6 zero-byte blobs legitimately
collide with its digest. Then the claim is scored, not asserted.

### L1 — the lane already holds redistributed binaries without notices

15,697,248 B of host distro binaries, each committed three times (corpus + two prep trees), plus a
2.28 MB wheel, with no `LICENCE`/`COPYING`, no source offer and no NCSA-style attribution anywhere
in the tree (`grep -rn "licen|GPL|copyright"` over `.ufo/waves/round-34` hits only upstream source
files a seat read *about*, not notices for the committed copies). Private harness, unmodified bytes,
so the practical exposure is small — but the round's own licence sentence ("third-party images are
never committed", C1) reads as a policy the tree does not follow for binaries. Either add
`corpus/evidence/round-34/README.md` with per-file origin (`/usr/bin/bash` etc.), package version and
licence, or move the ELFs to a fetch-on-demand step like C1 uses. Do not do this inside round-42's
claim surface; record it as a lane defect and fix it as housekeeping.

---

## 3. Axis 3 — the frozen-path list: what must be added

The draft's C1 list is "this file; `tools/round-42/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-carrier.py}`
and the oracle tools; `.ufo/waves/round-42/c1/{carriers.json,gap-rule.json}`; every carrier pin,
oracle and non-regular table." Concretely missing, in the order they can hurt:

### B1 (Blocking) — the v3 reader

`tools/round-41/sqfs-list.py:243` refuses anything but 4.0 (P3, exit 2 on both v3 fixtures). The
counter's `layout_probe` (line 682) is also a hardcoded **v4** 96-byte parser whose `ok` needs the
AVM block-length endianness test, so `layout_ok`/`carve_ok` are unreachable for v3; and `c1-extra.py`
re-derives the oracle through `READER = 'tools/round-41/sqfs-list.py'`.

So round 42 must ship a v3-capable structural reader and freeze it. Two shapes:
* extend `sqfs-list.py` to `(3,0)` (superblock prefix through `s_major/s_minor` is shared; the
  directory/inode tables and the metadata block header are not), or
* add a small frozen `tools/round-42/sqfs-probe.py` that returns only
  `{magic, major, minor, compression, bytes_used, size}` for whichever layout, and use it for
  `layout_ok`; drop `carve_ok` to `bytes_used == size` for external carriers.

Either way **name it in the frozen list**, and state in the predicate whether `oracle_rederived`
survives for v3 (if it does not, say so — silently dropping a clause is the R41-CL-class mistake).

### B2 (Blocking) — `compression_coverage` cannot pass on v3

`c1-counter.py:298-299` `GZIP_ID = 1`, `XZ_IDS = (2,4)`, and the binding requires *some* carrier with
gzip **and** *some* carrier with xz. SquashFS 3 has no xz (gzip id 1, lzma id 3). A four-carrier v3
round therefore scores `met_target=false` no matter how clean the extraction is. Replace with
per-carrier `compression == the value frozen in carriers.json` (which is what the draft's own
"superblock reads the frozen … compression" says) plus, if a coverage notion is wanted, a v3-family
binding such as "both endian spellings seen" or "at least two of {`squashfs_v3`, `_ddwrt`,
`_broadcom`, `_nonstandard`}". The replacement must be in the predicate text at the freeze, not
discovered by the counter.

### H3 (High) — `PRIOR_CARRIERS` is a judgement input outside the freeze

`c1-counter.py:290` reads `.ufo/waves/round-40/c1/carriers.json` at the *measured revision* to build
`prior_pins`, and `carrier_fresh_ok` is false iff the pin is in that set. It is not in `FROZEN_PATHS`.
Attack: at any commit in `FREEZE..REV`, edit that file (drop round-41's V3 pin) and re-pin the same
AVM v3 image — `carrier_fresh_ok` passes and the "four FRESH" sentence is false. Second, smaller
point: round-41's pin list is not consulted at all, so round-41's own V3 (a v4 AVM rootfs) is
"fresh" for r42; if r42's four carriers may not repeat any earlier carrier, the prior set must be
every earlier round's `carriers.json`, frozen by digest in the r42 table.

Remediation: freeze a `tools/round-42/prior-pins.json` (the union of round 38–41 pins, each with the
file and commit it came from) and have the counter read *only* that; add it to `FROZEN_PATHS`.

### H4 (High) — the evidence-id tool and the REA package

`XPIN = 'tools/round-27/xpin-attribute.mjs'` (line 289) is read from the freeze tree and *executed*
with `node … --pkg65 <package root> …` (line 408) to recompute `evidence_id`. The mjs is not in
`FROZEN_PATHS`, so a commit in `FREEZE..REV` can edit it and bend `evidence_id_ok` without touching a
frozen path. Worse, `--pkg65` is the mutable package under `~/.npm/_npx/…` (the same user can write
it; nothing hashes it), so the *rule being recomputed* is attacker-controlled even when the mjs is
byte-identical.

Remediation: add `XPIN` and a frozen `rea-pkg.json` (`{root_name, package_lock_sha256,
tree_sha256}`) to the frozen set; `evidence_ids` refuses a package whose `package-lock.json` digest
differs; resolve `node` and `npx` by absolute path (see X2).

### H5 (High) — C2 reads C1's round-41 receipts, which nobody freezes

P42-C2 says "the round-41 C1 receipts (real AVM rootfs envelopes) … get the evaluator's pair". Those
are `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` (+ oracle/nonregular tables). They are
committed at the base, they are C1's *outputs* (so C1's draft list need not freeze them), and C2's
frozen list does not name them either. A seat can therefore edit a round-41 receipt after the freeze
to change C2's expected pairs — or, more plausibly, to make a failing class pass.

Remediation: freeze their sha256 in the C2 tables (`heldout` manifest already has a pins section) and
have `c2-counter.py` verify before reading; alternatively copy the four receipts into
`corpus/evidence/round-42/c2/r41-inputs/` and freeze that directory.

### P6 — the oracle producer and its readers

The draft says "the oracle tools" — that is not a path. Round 41 froze **no** oracle producer: its
`oracle-run.json` records `reader.path = tools/round-40/sqfs-list.py`, `reader.sha256`, argv and
selftest, and `c1-run.sh`'s "oracle" arm was `sqfs-list.py --layout avm` cross-checked by
`sasquatch-v4be -f` — i.e. the second producer was *sasquatch itself*, the extractor the oracle is
supposed to be independent of. For r42 freeze:
* `tools/round-42/oracle.py` (the producer, invoked as a frozen argv),
* `unsquashfs -version` / `7z i` output and the resolved absolute paths in the committed
  `oracle-run.json`,
* the exact `unsquashfs -lls` invocation **with `-d`**, because the row prefix is the extraction root
  name: default `squashfs-root/`, the `-d` value when given (P4). Without a frozen `-d` the oracle's
  paths are off by one segment and round-41's D5 segment-bounded rule fires on every carrier.

### L3 — `frozen_drift` only sees the keys the spec happens to carry

`frozen_drift` (line 1189) adds `path`, `oracle`, `nonregular` **when present**. A carrier entry that
omits `oracle` (the schema tolerates it; `parse_oracle(None)` returns `'absent'` later) is not
drift-checked at all, so its oracle can be rewritten after the freeze. Require both keys in
`carriers_spec` and add them to the drift set unconditionally.

### L4 — receipts are not drift-checked

`receipt_fresh` (line 1593) requires the first-add commit to be a strict descendant of the freeze; a
later rewrite of an already-added `after.json` is not observed (it cannot be: the file does not exist
at the freeze). Accept this and disclose it, or (better) have the L1's score receipt of record carry
the `after.json` sha256 — round-41 closure D4's pattern, extended from the counter to the evidence.

### P9 — gap-rule kinds for the v3 family

`gap_rule_ok` fails on any observed non-regular kind not in the frozen model's `allowed`. Round-41's
`gap-rule.json` was shaped on AVM v4 rootfs; the v3 family's diagnostics differ in name
(`empty-target`, `MaliciousSymlinkRemoved`, and for a failed body `ExtractorDependencyNotFoundReport`
/ `ExtractCommandFailedReport`) and in the fact that a v3 chunk can be `squashfs_v3_ddwrt` etc. Freeze
a v3-shaped `allowed` map and a v3-shaped `structural` set, and prove it by the dry run (QUALITY 84)
on the dev arm — otherwise the first genuine v3 carrier fails on an uncovered kind and the round
reads it as a defect in the extractor.

---

## 4. Axis 4 — PATH hygiene of the counter's REA rerun

### H1 (High) — which `sasquatch` runs is unbound, and substitution is projection-invisible

Mechanism, from the installed code:
* unblob builds `Command('sasquatch', '-le'|'-be', '-no-exit-code','-f','-d',{outdir},{inpath})`
  (`handlers/filesystem/squashfs.py:21-66`); the executable is a bare name, so
  `subprocess.run(list, …)` resolves it through the child's `PATH` at exec time
  (`extractors/command.py:52-58`).
* the counter's rerun copies `os.environ` and overrides only `REA_UNBLOB_COMMAND` and `TMPDIR`
  (`c1-counter.py:1427-1429`): **the child PATH is inherited**, exactly as the round-41 harness
  documents ("The child PATH is the inherited PATH and MUST resolve sasquatch-v4be", `c1-run.sh:8-10`).
* the committed receipt cannot show the extractor: `environment: null`, `raw_result.execution` carries
  unblob's absolute command, args (`--log <scratch>/unblob.log`) and `--version` output, and the
  string `sasquatch` occurs **nowhere** in a successful envelope (P5, E2). On the failure path only,
  `diagnostics[].report.command` shows the *invoked name* — a shim reproduces that trivially.

Measured (P5): with `PATH=$S/fake:$PATH` and `$S/fake/sasquatch` a 10-line shim that execs
`/usr/bin/unsquashfs -processors 1 -f -q -d "$outdir" "$inpath"`, REA returns `ok:true`, handler
`squashfs_v3`, `extraction_failed:false`, and the pinned projection (files/rel+sha256+size, chunks,
gaps, diagnostics) is **identical** to the real-sasquatch run. `envelopes/e2-baseline.json` vs
`envelopes/e4b-shim-substituted.json`.

Impact: the C1 line "extractor `sasquatch -be|-le`, never `sasquatch-v4be`", and C2's step 3/6 labels
that depend on which extractor was reachable, have no evidential support. The rerun catches only the
*payoff* case (a shim rescuing a carrier the real extractor fails), because the real extractor's
failure then changes the projection — and it catches that only while the rerun's PATH is clean, which
it is today only by accident (the shim lives in the seat's scratch). The harmless-but-false case (a
shim that agrees with the real extractor) is invisible, and it is the case that lets a seat produce
"REA extracted four v3 rootfs with sasquatch" when it did not.

Smallest remediation (three cheap additions):
1. `c1-run.sh` sets an explicit `PATH` (`/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin`, no
   inheritance) for the REA child, and `make_real_runner` does the same, so the run and the rerun use
   the same pinned order. A seat can still run REA outside the harness — see D1 — but the *scored*
   rerun is then the fixed one.
2. `c1-run.sh` writes `extract-env.json` next to `after.json`:
   `{sasquatch:{path,sha256,version}, sasquatch-v4be:{path,sha256,version}, unblob:{path,sha256,version},
   path:"…", unblob_log:{command_line, sha256}}`, and the unblob `--log` file itself (it is small; the
   extract command line is in it — P8 shows the format).
3. a binding `extractor_bin_ok` in the counter recomputes the same digests under the fixed PATH and
   requires: equality, `sasquatch-v4be` **absent** from every v3 carrier's `unblob_log.command_line`,
   and the log's `-le`/`-be` matching the carrier's endianness. This is the only way the claim's own
   sentence becomes true of the bytes.

Bounded value to add: `sasquatch` and `sasquatch-v4be` digests I measured on this host —
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` and
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`; unblob
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` (`~/.local/bin/unblob` is a
symlink to the uv-tool venv binary, so hash the realpath).

### X2 (Medium) — `npx` and `node` come from PATH, the package from a mutable cache

`make_real_runner` uses `shutil.which('npx')` and `argv[0]='npx'`; `evidence_ids` runs `node`. Both
resolve through PATH, and the package they load is `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
— writable by the same user, never hashed. A poisoned package changes `evidence_id` recomputation
(H4) and could change the envelope normalization itself. Remediation: absolute `node`/`npx` paths
frozen in `extract-env.json`, plus `rea-pkg.json` (H4). `npx -y` also re-resolves the registry when
the cache is cold; the freeze should record whether the run was served from cache.

### X3 (Info) — what the claim text asserts vs what the harness asserts

Round-41's claim asserted "sasquatch-v4be 4.5.1 reachable on the child PATH" as a *precondition*
while `c1-run.sh` only `command -v`s it and writes `{path,sha256,version}` into `oracle-run.json` for
the oracle arm — never for the `after` arm, and never rebound by the counter. The r42 draft repeats
the wording ("unblob 26.6.4, sasquatch 4.5.1 on the child PATH") without a binding. Treat "on the
child PATH" as a claim you must make scorable, not as a comment.

### X4 (Info, usable) — the PATH-strip technique works and names the dependency

P5/E3: with `$HOME/.local/bin` removed, the envelope has `extraction_failed:true`, gap
`missing-extractor-dependency` with `handler:"squashfs_v3"` and `dependencies:["sasquatch"]`, and a
diagnostic `ExtractorDependencyNotFoundReport`. That is the dev arm C2's `dep-missing-le` class needs,
and it confirms the gap carries the handler family (so F is available from G's own rows).

---

## 5. Axis 5 — could a seat pre-run REA on a candidate unnoticed, and would the round see it?

**Yes, and today the round would not.** What exists (all measured):

| channel | what it can prove | limit |
|---|---|---|
| `parameters.output_directory` + task paths in the envelope (P5) | which scratch segment produced the receipt; `run_provenance_ok` requires `/kaidoku-r41/` and must become `/kaidoku-r42/` | blocks cross-round reuse only; a wave-1 seat's own r42 scratch passes |
| `receipt_fresh` (first-add commit after the freeze) | the receipt was *committed* after the freeze | says nothing about when the run happened; the envelope has **no timestamps at all** (P7) |
| `unblob.log` in the extractor's cwd | a run whose cwd was the work tree leaves a debug log naming the input and the exact `sasquatch …` command line — the lane root **already has one tracked from round 38** (P8) | only fires when cwd is the lane; REA passes `--log` into its own task dir, and the seat's scratch is deleted |
| `~/.npm/_npx/<hash>` directory mtime | *an* REA invocation happened; my own run bumped it to 18:55:31 while `.package-lock.json` stayed at 01:12 (P7) | no input identity, no count, no time beyond the mtime, and a cold cache perturbs it anyway |
| seat transcript (`history://<id>`) | the whole command, including the input path | honesty; it records a seat that *deleted* its scratch just as well — this is the only channel that binds a run to a carrier |

Because there is no mechanical proof, the draft's reservation ("never run REA … on a candidate") is
unenforceable as written, and a seat that pre-runs gets exactly the receipt it wanted, committed after
the freeze, with a fresh-looking first-add commit.

Smallest design fix, in the shape the round already uses for honesty controls:
1. Before the freeze, each `R42C1Img*` seat files `prefreeze-exposure.md`: candidate URL + sha256 +
   *every* reader command it ran (the reserved-carrier rule already allows `unsquashfs -s/-lls/-d`,
   `7z l/x`, pure readers) and the sentence "no REA/unblob/sasquatch invocation on this image or
   anything carved from it".
2. The L1 runs three cheap checks before freezing and records them in the freeze-receipt:
   `git status --porcelain` + `git log --name-only` for `unblob.log`, `*_extract/`, `carrier.bin` in
   the lane; a transcript grep over the `R42C1Img*` seats for `extract-firmware|unblob |sasquatch`
   (my own transcript would trip it — correct behaviour, I ran on fixtures); and a `stat` of
   `~/.npm/_npx/ad9a3fdbcad992c6` at wave start vs freeze, recorded as a range, not a verdict.
3. Freeze the declarations with the claim, and give the counter a binding that at least makes the
   *committed* receipt self-dating: `parameters.output_directory` must contain the seat's declared
   scratch name from `prefreeze-exposure.md`, so a receipt produced in someone else's or an
   undeclared directory fails.

---

## 6. Confirmations and corrections to the draft (wave-1 answers the draft asked for)

**C1 — draft step 3 stands; the mechanism is not the one the source first suggests.**
`missing-extractor-dependency` names exactly one executable: `Command.get_dependencies()` returns
`[self._executable]` (`extractors/command.py:101`), not the handler's
`[EXECUTABLE, V4BE_EXECUTABLE]` (which only feeds the CLI's `--show-external-dependencies` banner).
Measured `dependencies:["sasquatch"]` on a v3 chunk (P5/E3). My working hypothesis that D always
carries both names — which would have made "else" unreachable — is **falsified**. Keep step 3 as
written; the discriminating fact is which executable was attempted, i.e.: `sasquatch-v4be` only for
a v4 **BE** non-AVM chunk (`match endian, version` in `SquashFSExtractor.extract`); everything else
(`-le` for any version, `-be` for v1–v3) resolves plain `sasquatch`. So the draft's parenthetical
"every v1–v3 chunk and every v4 LE chunk resolves plain `sasquatch`" is correct — delete the
"[to be confirmed]" caveat and cite the source lines instead.

**C2 — the v3 handler family is four names, and v1/v2 share the v3 extractor.** Measured from the
installed package: `squashfs_v3` (0x73717368), `squashfs_v3_ddwrt` (0x74717368 `tqsh`),
`squashfs_v3_broadcom` (0x71736873 `qshs`), `squashfs_v3_nonstandard` (0x73716c7a `sqlz`); and
`squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard` all carry `SquashFSExtractor(version=3)`,
i.e. they are extracted by the v3 sasquatch — which is exactly why R41-CL4's `no-squashfs-chunk`
cause text was wrong. C2's step 6 "a v1–v3 handler" must be a frozen enumerated set of those seven
names; prose will drift, and the labels `legacy-body-failure`/`cross-read-legacy` hang off it.

**C3 (Blocking, oracle) — two readers do not agree file-for-file on a carrier with symlinks.** 7-Zip
26.04 reads v3 (LE and BE; `File System = SquashFS 3.0`), so the support premise is true — but its
listing has no type column: it prints a symlink as a regular file with `size` = target length
(`badlink`, 38 B, `Attr "....."`), and `7z x` **rewrites** an absolute link target to an absolute path
inside the output dir (`…/x7/etc/ssl/private/ssl-cert-snakeoil.key`) while `unsquashfs` keeps
`/etc/ssl/private/ssl-cert-snakeoil.key`. Every real rootfs has symlinks, so the draft's "must agree
file-for-file before a carrier freezes" is either unsatisfiable or will be satisfied by silently
dropping the link rows — the worst outcome, because it weakens `nonregular_ok` invisibly.
Freeze the authority split instead: **types and sizes from `unsquashfs -lls` alone** (single
authority), **content digests from both readers' extraction over the regular-file intersection**,
**non-regular table from `unsquashfs` only**, and a recorded, expected divergence list containing the
7-Zip target rewrite. A lane stdlib v3 reader as the second producer (the draft's alternative) makes
the oracle circular — round-41's `oracle_rederived` already is, and it cannot even run on v3 (B1).

**C4 — `unsquashfs -lls` prefix.** The row prefix is the extraction root name: `squashfs-root/` by
default, the `-d` argument when given (P4). Freeze the `-d` value and the one-component strip rule, or
every oracle path is one segment deep and round-41's D5 segment-bounded rule rejects the receipt.

**C5 — `--max-depth 1` produces a structural `depth-limited` gap on a two-file v3 image** (P5/E2), so
the draft's "at most one structural `depth-limited`" allowance is load-bearing on every carrier, not
an edge case; keep it and make the gap rule's `structural` set v3-shaped (P9).

---

## 7. Limits

* I did not run REA/unblob/sasquatch on any published image or anything carved from one; every
  extractor run was on unblob's MIT fixtures. No candidate URL was downloaded.
* The 7-Zip symlink measurement is on a v4 fixture (reader semantics are version-independent); a v3
  carrier with symlinks should be re-confirmed by R42C1Oracle under the reserved-carrier allowance
  before the freeze leans on C3.
* My licence test is hash + superblock-magic at the base; I did not repeat round-41's byte-run
  (`carrier.find(blob)`) test on the 24 k blobs, and no r42 carrier existed when I ran.
* "A seat can pre-run and get away with it" is a statement about the *scored* clauses I read; a
  mechanical detector outside the lane (host audit) is out of my scope.
* The 5 s / 24 k-blob scan cost is this machine's; treat the binding's cost estimate as order-of.
* Everything about `fetch-carrier.py` is about a file that does not exist yet; I attacked the tool it
  will be ported from and the clauses that must bind it.

## 8. Artifacts

`artifacts/R42C1Sentinel/` — `probe-log.md` (P1–P10 with commands and outputs),
`scan-large-blobs.tsv`, `scan-squashfs-magic.tsv`, `redirect-demo.py` (+ its output in
`fetch-redirect-demo.txt`), `fake-sasquatch.sh` (the shim, sha256 `bed77079…714ffc`),
`envelopes/{e2-baseline,e3-stripped-path,e4b-shim-substituted}.json`, and `fixtures/`
(`squashfs_v3_le.bin`, `squashfs_v3_be.bin`, `bad_symlink.squashfs` — MIT, 4096 B each).

## 9. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r42/R42C1Sentinel; mkdir -p $S; cd $S; export TMPDIR=$S
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
B=https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs
curl -s -o v3le.bin $B/squashfs_v3/little_endian/__input__/squashfs_v3_le.bin
python3 -I -B $L/tools/round-41/sqfs-list.py --layout le --files /dev/null --nonregular /dev/null v3le.bin   # EXIT=2, "need 4.0"
unsquashfs -lls v3le.bin; 7z l v3le.bin
env REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
    --format json --full-output --max-depth 1 v3le.bin $S/out-full > $S/e2.json
env PATH="$S/fake:$PATH" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 \
    extract-firmware --format json --full-output --max-depth 1 v3le.bin $S/out-shim > $S/e4b.json
python3 -I -B $L/.ufo/waves/round-42/w1/artifacts/R42C1Sentinel/redirect-demo.py
```

---

## 10. Amendment (same session, after peer IRC; supersedes the named clauses)

Two peers replied with corrections to B2 and C3. I re-measured both instead of adopting them, and one of
their corrections lands on **my** text: my "7-Zip's listing has no type column" is wrong for
`7z l -slt`. Everything below is measured after the first submission; the earlier sections stand except
where this section says otherwise. New fixtures and envelopes are in
`artifacts/R42C1Sentinel/fixtures/` and `…/envelopes/e5-padded-1k.json`.

### A1 — `unsquashfs` cannot produce an oracle for an **lzma-adaptive** v3 image (confirms R42C1OracleCheck)

```
unsquashfs -s   squashfs_v3_le.lzma.bin  -> "Found a valid little endian SQUASHFS 3:0 superblock", rc 0
unsquashfs -lls squashfs_v3_le.lzma.bin  -> "gzip uncompress failed with error code -3"
                                            "FATAL ERROR: read_inode: failed to read inode 132:64", rc 1
7z l                                     -> File System = SquashFS 3.0, Method = LZMA Spec, both files listed
sasquatch -le -lls                       -> rc 0, both files listed (stderr shows the decompressor probe)
sasquatch -be -lls (wrong endian)        -> rc 1, "FATAL ERROR: Block size or block_log too large"
```

**Correction to the first version of this section (my error, kept visible):** I first wrote that
`sasquatch` "never tries lzma-adaptive, rc 141". That was a SIGPIPE artifact — I had piped the
command into `head -6` and read `PIPESTATUS[0]`, which records 141 when the writer dies on a closed
pipe. Re-run without a pipe, `sasquatch -le` on the same fixture is **rc 0 and lists both files**, and
REA `--max-depth 1` on that image succeeds end to end (`handler squashfs_v3`, `extraction_failed:
false`, 2 files — `envelopes/` and P15). The substantive point below is unaffected but its reason
changes: it is not that nothing can extract lzma v3, it is that the only readers that can are the
extractor under test (sasquatch) and a lossy one (7z).

So `unsquashfs` can validate the superblock of any v3 image but **cannot list or extract an
lzma-adaptive one** (rc 1, no stdout). Consequence for C3: the "types+sizes from `unsquashfs -lls`
alone" authority is only available for **gzip v3**. A carrier that is lzma-adaptive (the OpenWrt
Kamikaze 7.09 rootfs are, per R42C1OracleCheck) has *no* two-reader oracle that can produce the
non-regular table: unsquashfs cannot read it, 7z cannot give targets, and sasquatch is the extractor
under test. Extraction through unblob does work (`envelopes/e5`/P15: handler `squashfs_v3`, no failed
chunk, 2 files), so the constraint is on the **oracle**, not on C1's ability to extract — which makes
it a carrier-selection rule the freeze must state, not an extraction claim. The draft must therefore either (a) constrain C1 carriers to gzip v3 — declare it and
bind it — or (b) say in the claim what the oracle is when the only faithful reader is the extractor
under test. Silently swapping in the lane's own v3 reader is the circular case C3 already rejects.
`[INFERENCE]` the LZMA-block v3 fixture is what Kamikaze's `lzma-adaptive` images look like to
readers; R42C1OracleCheck measured the real Kamikaze rootfs directly, which is the stronger evidence.

### A2 — correction to my C3: `7z l -slt` **does** expose the type

```
7z l -slt bad_symlink.squashfs  -> Path = badlink / Mode = lrwxrwxrwx / Size = 38   (no target string)
7z l    bad_symlink.squashfs  -> Attr "....." / Size 38                              (default table: no type)
```

So 7-Zip can serve as a **type cross-check** via `-slt Mode`; what it never exposes is the link
**target**. My sentence "its listing has no type column" is withdrawn to "its default `l` table has no
type column; `-slt` has `Mode` but no target". The rest of C3 stands and is now sharper: the
**target** column of the non-regular table is single-reader (unsquashfs), which is exactly the reader
A1 removes for lzma v3.

### A3 — 7-Zip extraction diverges in **three** classes, all measured on one 4 KiB image

Built here (`mksquashfs`, v4, `fixtures/sentinel-symlink-divergence.sqfs`, sha256 `9299517…fdb1`) with
`abs -> /etc/passwd`, `up -> ../outside`, `same -> hello.txt`:

| entry | `unsquashfs -d out` (rc 0) | `7z x` |
|---|---|---|
| `abs -> /etc/passwd` | target preserved | symlink **rewritten** to `<outdir>/etc/passwd` |
| `up -> ../outside` | target preserved | **dropped**: `ERROR: Dangerous link path was ignored : up : ../outside`, replaced by a **0-byte regular file** |
| `same -> hello.txt` | target preserved | preserved, target unchanged |
| exit | 0 | non-zero (1 sub-item error) |

This confirms R42C1OracleCheck's `../`-drop on Kamikaze (80 such links) and answers their open question
about absolute links: **absolute targets are rewritten, not dropped** (my earlier `bad_symlink`
measurement, same class). Two operational consequences the oracle producer must encode: (i) any
content comparison on the 7z side must exclude links entirely, and (ii) the producer must require
`7z x` exit 0 (or count its sub-item errors) — a producer that discards 7z's stderr will compare a
silently reduced set and call it agreement.

### A4 — the v3 superblock has no compression field at the v4 offset (confirms R42C1EntryDraft, and it kills my B2 remedy as written)

```
v3 LE fixture, bytes 0x18-0x27: 0000 0000 0300 0000 0000 1000 4001 00f5
                                      ^0x1c s_major=3 (u16)  ^0x1e s_minor=0
v3 LE 1kpad fixture, same window: 0000 0000 0300 0100 …   -> s_major 3 at 0x1c, s_minor 1 at 0x1e ("3.1")
v3 BE fixture, same window:       0000 0000 0003 0000 …   -> s_major 3 at 0x1c (big-endian u16)
offset 0x14 (the v4 `compression` u16) = 0x0000 in all three, on images whose data decodes as ZLIB/LZMA
v3 `bytes_used` is NOT at the v4 offset 40:48: on the LE fixture raw[40:48] = c0 9c 61 40 00 00 00 00,
  while the value (258) first occurs at offset 63
```

`file(1)` calls the same image "uncompressed" while 7z calls it `ZLIB` and `unsquashfs` prints "Inodes
are compressed" — three readers, three labels, no field to arbitrate. So the predicate's phrase "their
superblock reads the frozen magic/major/compression" is **not implementable for v3 as to
compression**; my B2 remedy ("per-carrier compression from `carriers.json`") must be narrowed to
"declared in `carriers.json` and **witnessed behaviourally**" — e.g. the oracle producer records the
reader/decoder that decoded the data blocks and the counter requires that witness, or the carrier is
required to be gzip v3 (A1) and the 'compression' cell is the declared-and-witnessed pair.

**Correction to the first version of A4 (R42C1EntryDraft's bytes, re-checked here, peer right, me
wrong):** I wrote that `s_major` sits at 0x1e and that `layout_probe`'s `raw[28:30]` returns 3 only by
coincidence. 0x1c **is** 28 — I conflated the decimal offset with the hex digit — and the field order
is `s_major` at 0x1c, `s_minor` at 0x1e, as the byte windows above show (the 3.1 fixture's minor is the
`01` at 0x1e). A reader written to my 0x1e offset would read the minor as the major. What *does* stand:
the v4 `compression` field at 0x14 is 0 in v3, and `layout_probe`'s `bytes_used` at 40:48 is the wrong
offset for v3 (measured value there: `0xc09c6140`), so `carve_ok`'s `bytes_used`/`size` test is
mis-derived for a v3 carrier even before `version_v4` rejects it.

### A5 — a padded carrier's chunk is longer than `bytes_used`, so the ported `carve_ok` rejects real images

```
fixtures/squashfs_v3.le.1kpad.bin (1024 B): superblock says version 3.1, bytes_used 320
REA --max-depth 1 -> chunks[0].range = {offset 0, length 1024}, root_file_range same, files 4, handler squashfs_v3
```

unblob's `calculate_chunk` (`handlers/filesystem/squashfs.py:77-98`) masks
`(start_offset + bytes_used) & 0xFFFFFFFF` (line 82) and then extends the chunk to
`round_up(bytes_used, 1024|4096)` when that padding is zeros. Round-41's `carve_ok` required
`ext.length == bytes_used == size`; on any padded published image (the normal case for a vendor image)
that is false and a correct carrier fails. The r42 port must accept `bytes_used <= size <=
round_up(bytes_used, 4096)` with `size - bytes_used` all zero, and must not require the chunk length to
equal `bytes_used`. Note also that the padded fixture is **3.1**: the frozen per-carrier handler and
the "magic/major" clause must state whether minor 1 is admissible (handler name is the same,
`squashfs_v3`).

### A6 — effect on my findings table

B2's premise stays true (no xz in v3) but its *remedy* is corrected by A4/A5; C3 is corrected by A2 and
narrowed by A1/A3; B1 is unaffected and now has a second consumer (the oracle needs a v3 reader for the
target column on lzma carriers). Nothing in the High findings changes.

### A7 — REA does extract an lzma-adaptive v3 image; the wrong endianness fails loudly

```
REA --max-depth 1 fixtures/squashfs_v3_le.lzma.bin
  -> ok true, handler squashfs_v3, extraction_failed false,
     files firmware.bin_extract/{apple.txt (6), orange.txt (7)}, one structural depth-limited gap
sasquatch -be (wrong endian, LE image) -> rc 1, "FATAL ERROR: Block size or block_log too large"
sasquatch -le (matching)               -> rc 0
```

Three consequences: (i) an lzma v3 carrier is extractable through the REA path, so C1's failure mode on
one would be an *oracle* failure, not an extraction failure — the predicate must not conflate them;
(ii) a forced wrong endianness fails with a distinctive message, so C2's `legacy-body-failure` class
can distinguish "extractor invoked with the wrong endian" from "body damage" — worth a feature if the
dev arm can produce it, since unblob derives endianness from the magic and a REA run should never hit
it; (iii) my own P11 `rc 141` reading was a pipe/SIGPIPE artifact (see A1) — recorded here because the
same mistake would silently corrupt any seat's exit-code evidence: read exit codes without a pipe, or
via `PIPESTATUS` **and** a distinguishing check that the failure text is not `head`'s.

### A8 — the frozen `layout_probe` on real v3 images (source-level evidence for B1)

Called directly from `tools/round-41/c1-counter.py` (`python3 -I -B`, one call per fixture):

| fixture | `ok` | `reason` | `magic` | `major` | `compression` | `bytes_used` |
|---|---|---|---|---|---|---|
| `squashfs_v3_le.bin` | false | `inode_table_start 72057594037928190 outside the file` | `hsqs` | **768** | 0 | 13879075079154827264 |
| `squashfs_v3_be.bin` | false | `inode_table_start 65280 outside the file` | `sqsh` | 3 | 0 | 11295291748235870208 |
| `squashfs_v3.le.1kpad.bin` | false | `inode_table_start 72057594037927996 outside the file` | `hsqs` | **768** | 0 | 14700701910562766848 |
| `squashfs_v3_le.lzma.bin` | false | `inode_table_start 72057594037928189 outside the file` | `hsqs` | **768** | 0 | 17235104525010862080 |

Three read-offs the L1 should take from this, because each one is a way to mis-write the port:

* Offset 28 **is** the v3 `s_major` field (A4 correction), but `layout_probe` reads it big-endian
  unconditionally, so an LE v3 carrier reports `major: 768` = 0x0300. A v3 reader must apply the
  filesystem's endianness; a check like "`major == 3`" on the probe's output would reject every LE v3
  carrier for the wrong reason, and a check like "`major != 4`" would accept a BE one by luck.
* The first rejection is not the version test: `inode_table_start` (`raw[64:72]`, a v4 field) is
  validated *before* the magic/version tests, so the recorded `reason` on every v3 carrier names a
  field the format does not have there. A receipt that surfaces `ok: false` with that reason looks like
  a corrupt carrier, not like a tool limitation — exactly the kind of text that gets explained away.
* `bytes_used` (40:48) and `compression` (20:22) are v4 offsets; both are garbage/0 on v3. Anything
  that derives `carve_ok` from them fails A5's padded carriers as well.

### A9 — the draft moved under me; the parts I attacked did not

Lane HEAD is now `fdabdfa4` ("round-42: draft claims (not frozen), start census, wave-1 spec/generator/dispatch")
and `plans/round-42-claims.md` has an uncommitted A1 rewrite. Checked directly:

    git diff -U0 HEAD -- plans/round-42-claims.md | grep ^@@
    @@ -66,3 +66,17 @@   @@ -71,16 +85,23 @@   @@ -91,7 +112,10 @@   @@ -99,2 +123,5 @@   @@ -103,2 +130,7 @@

Every hunk starts at old line ≥ 66, i.e. inside `## R42-C2`. The R42-C1 predicate and bullets
(`superblock reads the frozen magic/major/compression`, the Oracle bullet "unsquashfs 4.7.5 (reads v1–v3 gzip)
and a second reader … must agree file-for-file") and the whole `## Frozen paths (draft)` block (line 144) are
byte-identical to what §1–§9 attacked, so B1, B2, H1–H5 and M1–M3 all apply to the text the L1 would freeze
today. `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` are unchanged between the base and HEAD, so the
landing anchors in §3 are unaffected.

One of my §6 confirmations is now already in the draft: A1's feature list defines
`L = {squashfs_v1, squashfs_v2, squashfs_v2_nonstandard, squashfs_v3, squashfs_v3_ddwrt, squashfs_v3_broadcom,
squashfs_v3_nonstandard}` — exactly the seven-name set I derived from the installed handlers (§6 C2). That item is
closed; H5 is not — line 120 still has C2 reading "the round-41 C1 receipts", and those receipts remain outside
both claims' frozen sets.
