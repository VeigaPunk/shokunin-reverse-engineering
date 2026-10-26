# R41C1Sentinel — adversarial review of the R41-C1 vendor chain and the freeze design

**Verdict: DEFECTS FOUND** — 10 findings (3 High, 4 Medium, 3 Low). The round-41 C1 draft is
scoreable in principle, but as written it (a) claims a fetch-chain link that is not implemented or
required by the frozen code, (b) makes V4's carrier choice depend on a pre-freeze REA measurement
that its own untouched-before-freeze clause forbids, and (c) does not close the routed R40-CL2
receipt-provenance hole while keeping the round-40 `/kaidoku-r40/` provenance segment. The
licence question is clean: no vendor bytes are committed anywhere at the base revision.

**The single most damaging defect is not in this report**: the draft has no carrier
identity/freshness clause, so re-pinning round-40 carriers and tables under V3/V4/L3/L4 scores 4/4
without any new extraction — measured by the wave-1 seat `R41CritC1Draft` (§(a2), §(e1));
§7 records the reconciliation, and my F3 is cost there, not the gate.

Base `49096c7e6f226af0c750c4b003be58883cb6049f`. Every command below ran read-only against the lane;
nothing in the lane, the fleet, `~/.local/bin` or `~/Projects/shokuknow` was written. No REA or
unblob run was performed (no reserved carrier was touched, not even read by an extractor).

---

## 1. Findings

Severity: **High** = a frozen claim could read MET without the stated property holding, or the
freeze would breach its own stated constraint. **Medium** = published provenance/evidence is
weaker than it reads, or a local write primitive exists. **Low** = hardening / calibration.

| id | finding | severity |
|---|---|---|
| F1 | `member_sha256` is never compared (R40-CL6 still open); the spec validator does not require the key; `provenance.json` already publishes it as a verified chain link | High |
| F2 | V4's "if it fits REA's entry budget at depth 1" needs a pre-freeze REA run, which the carrier rule forbids; the member is also left as an unresolved either/or | High |
| F3 | Receipt provenance is unverified: receipts are outside the freeze-drift set, `receipt_fresh` checks only first-add ancestry, and `PROV_SEGMENT = '/kaidoku-r40/'` is a spoofable substring test (R40-CL2 not closed) | High |
| F4 | Engine/depth pins are unbound: `--max-depth 1`, unblob 26.6.4 and sasquatch-v4be 4.5.1 are asserted in prose but never checked against frozen values | Medium |
| F5 | PATH hygiene: 12 of 20 PATH entries are user-writable and precede `/usr/bin`; `node`/`npx` resolve into a per-shell fnm shim; unblob resolves `sasquatch-v4be` by bare name through that PATH | Medium |
| F6 | `npx -y rea-agents@6.5.0` is an unpinned network/cache resolution at every scoring run; `npm_config_cache` steers the package-root lookup | Medium |
| F7 | `fetch-vendor.py` write side follows symlinks in `--cache`/`--image-cache`: a planted `<pin>.bin.part` symlink turns the fetch into an arbitrary-file write of vendor bytes (demonstrated) | Medium |
| F8 | `fetch-vendor.py --rev` is a git option-injection vector; no URL-scheme allowlist; unbounded `read()`; `image_sha256` is used as a filename component before any shape check | Low |
| F9 | The proposed exact-path rule (prototype diff) is fail-closed but silently depends on the receipt grammar "first path component is the chunk extract root"; 10/11 semantic cases pass, the miss is that grammar | Low |
| F10 | `layout_probe` accepts `bytes_used < len(carrier)`; the draft says the V3/V4 carrier is carved *to* `bytes_used` | Low |

### F1 — the member link of the fetch chain does not exist (High)

P41-C1 (draft) requires "the fetch chain checks image sha256 → member sha256 (R40-CL6) → carrier
sha256". At the base revision the chain has two links, not three:

```python
# tools/round-40/fetch-vendor.py:100-118 (materialise)
rec['image_sha256'] = sha256(image);  if rec['image_sha256'] != ext['image_sha256']: ...
body, detail = carve(image, ext['member'], ext['length'])      # sha256(member) only lands in a STRING
rec['carrier_sha256'] = sha256(body);  if rec['carrier_sha256'] != pin: ...
```

`carve()` returns `'member %d bytes, sha256 %s'` — the member digest is *reported*, never compared.
The frozen validator does not require the key either: `carriers_spec()` requires
`('url','image_sha256','member','length')` and nothing else.

Reproduced hermetically against the lane tool (loaded by path, no copy, `python3 -I -B`):

```
correct  member_sha256=56059d4d ok=True link=None
WRONG    member_sha256=00000000 ok=True link=None      <- pin ignored
absent   member_sha256=ABSENT   ok=True link=None      <- key not needed
```
(`artifacts/R41C1Sentinel/demo-member-sha256.py` + `.out`)

Exploit path / impact. `corpus/evidence/round-40/c1/V1/provenance.json` already publishes
`chain.member_sha256: 334e56…` under the note "vendor bytes are not committed; fetch with
fetch-vendor.py", i.e. the evidence asserts a verified three-link chain that the tool does not
perform. A round-41 spec whose `member_sha256` is stale, wrong or absent scores exactly like a
correct one, so the R40-CL6 repair is not observable and the claim's own wording is unmeasured.
(Residual risk is bounded: `image_sha256` transitively pins the member, so the *bytes* are safe —
this is a false-provenance defect, not a byte-substitution defect.)

Smallest remediation. In `materialise()`, after `carve()`, recompute the whole-member digest inside
`carve()` and require `sha256(member_bytes) == ext['member_sha256']` (link `member_sha256`); add
`member_sha256` to the `carriers_spec()` required keys with a `SHA_RE` shape check; add two
selftest cases (`member_sha256` wrong → exit 1 `link=member_sha256`; absent → exit 1). Note the
carve is a prefix, so the check must hash the *member*, not the carve.

### F2 — V4's condition requires the very measurement the carrier rule forbids (High)

Draft, V4: "the nested `filesystem_core.squashfs` of `FRITZ.Box_5491-07.31.image` (the full rootfs)
**if it is AVM-BE and fits REA's entry budget at depth 1**; fallback the 5491 wrapper member."
And the predicate: "each of the four frozen carriers … none of which any REA or unblob run touched
before the freeze".

"Fits REA's entry budget at depth 1" is only knowable by running REA on it (the budget is
`parameters.max_output_files` / `max_output_bytes`; observed round-40 receipts use
`max_output_files: 10000`, `max_output_bytes: 268435456`, and V1 published 697 files with a
`depth-limited` gap even at depth 1). So the V4 decision either (a) is made from a REA run, which
breaches the untouched clause, or (b) is made blind, in which case the predicate's "fits" clause is
undecided at freeze. The same clause also leaves the carrier identity as an either/or, which cannot
be frozen as a pin.

Related, measured: the full-rootfs choice is a real budget risk. V1 (5.4 MB, 697 files) fits
comfortably; a 5491 rootfs is materially larger, and a `max-output` truncation publishes fewer files
than a *full* independent oracle holds, which would make `oracle_hits_ok` unsatisfiable while a
truncated oracle would make the oracle no longer independent of REA.

Smallest remediation. Decide V4 from reads that are not extraction: download the 5491 image, list
the tar members, superblock-read each candidate `sqfs` member with `sqfs-list.py --layout avm`, and
freeze exactly one `(member, length, member_sha256, carrier sha256)`. Drop the "fits REA's entry
budget" condition; instead pre-register the risk explicitly — either freeze `--max-output-files`
large enough that the budget cannot bind, or state in the claim that a `depth-limited`/`max-output`
gap is allowed by the frozen gap rule and build the oracle as the *full* table. If the team wants a
REA-based decision, the predicate's untouched clause must be amended to name that single measurement
as an allowed exception (and then V4 is no longer a "fresh never-touched" carrier — say so).

### F3 — receipt provenance is still the R40-CL2 hole (High)

`frozen_drift()` protects `FROZEN_PATHS` plus each frozen carrier's `path`, `oracle`, `nonregular`.
Receipts are added by no key: `carriers.json` has no `receipt` entry, so the default
`'%s/%s/after.json' % (AFTERDIR, k)` is read at REV and is **not** in the frozen set. `receipt_fresh`
only asks whether the first-add commit is a strict descendant of the freeze:

```python
add = first_add(root, rev, rpath); d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)
```

So a receipt produced by a dev run *before* the freeze and committed *after* it satisfies
"fresh", and any later edit in `FREEZE..REV` is invisible because no drift rule covers the path.
`provenance_ok()` is a substring test on an attacker-chosen `parameters.output_directory`:

```python
if PROV_SEGMENT not in output_directory: return False        # PROV_SEGMENT = '/kaidoku-r40/'
```

Any scratch path containing the string `kaidoku-r40` passes — including `$S/kaidoku-r40/run-x/extract`
under a seat's own scratch, and including a round-40 run directory. The round-41 port that copies
this constant would accept a round-40-scratch receipt for byte-identical L3/L4 carriers (L3/L4 are
built deterministically by `mk-l-carriers.py`, so pre-freeze dev runs of the same bytes are easy and
explicitly allowed).

Partially mitigating: the counter-time REA rerun compares the `plus-extractor` projection, so an
*edited* receipt mostly breaks equality. What remains open is exactly what R40-CL2 named — the
receipt is evidence of a run that nobody proves happened on the frozen bytes at the frozen
parameters after the freeze.

Two limits of this fix, which the freeze text must respect (cross-checked with `R41CritC1Draft`):
`evidence_id_ok` is *well-formedness* (a self-consistent re-mint passes), and binding `run.json`
raises the cost of a fake but cannot prove a run happened — a copier rewrites the record too.
Neither this binding nor the peer's `carrier_fresh_ok` closes that: a receipt *fabricated from the
oracle* on genuinely fresh bytes still passes, because the rerun agrees with it. So the claim must
state provenance is **not** proven (keep the R40-CL2 wording), and this fix belongs in the freeze
as cost, not in any "provenance" sentence.

Smallest remediation (all data already recorded by `c1-run.sh`). Bind the committed
`run.json`: require `carrier.sha256 == pin`, `carrier.path` to be the fetched cache file,
`start_utc >= ` the freeze commit's committer date, `argv` to carry `--max-depth 1` and the same
carrier basename, `unblob.sha256` / `sasquatch_v4be.sha256` equal to frozen pins, and
`run_provenance_segment_ok is true` with `outdir` under the *round-41* segment. Add the derived
receipt path **and** `…/run.json` (and `provenance.json`) to `frozen_drift()`'s set. Change
`PROV_SEGMENT` to `/kaidoku-r41/` and make it a path-prefix test on the resolved absolute path, not
a `in` test.

### F4 — the predicate's environment is asserted, not checked (Medium)

P41-C1 names `--max-depth 1`, REA 6.5.0, unblob 26.6.4, sasquatch-v4be 4.5.1. The counter's clauses
never compare any of these to a frozen value:

- depth: `REPLAY_PARAMS` replays `parameters.max_depth` **from the receipt**; the round-40 selftest
  even asserts the opposite of a pin — `add('rerun passes the receipt max_depth (3) to REA', …)` and
  `add('rerun takes max_depth from the receipt, not a constant', …)` (c1-counter.py:1917-1920).
- engine: `projection(..., 'plus-extractor')` includes `engine = [name, version]`, but the comparison
  is committed-vs-fresh on the same host — it detects a *changed* engine, not a *wrong* one. The
  receipt's `engine.executable_sha256`
  (`0ce7b624…`, unblob) and `run.json`'s `sasquatch_v4be.sha256` (`fac88740…`) are never compared to
  a frozen expectation.
- `pkg65` (the rea-agents package root used to recompute evidence ids) is a live directory argument,
  not a digest.

Impact: a MET can be produced by an environment that does not match the claim text; the sentence
about 26.6.4/4.5.1 is unfalsifiable at scoring time. A depth-2 receipt replays depth 2 and passes
today. Fix: one frozen table checked as a single clause `rea_params_ok` —
`max_depth == 1`, `max_output_bytes`/`max_output_files` within frozen bounds, provider version
`unblob 26.6.4` with the *resolved* unblob binary's sha256 equal to the frozen pin
(`0ce7b624…`), and `run.json`'s `sasquatch_v4be.version == 4.5.1` and `.sha256 == fac88740…` —
plus a digest-of-package-tree check for `pkg65`.

### F5 — PATH hygiene (Medium): every external binary, and where it resolves today

`make_real_runner()` passes `dict(os.environ)` through with only `REA_UNBLOB_COMMAND` and `TMPDIR`
changed; `c1-run.sh` likewise exports `REA_UNBLOB_COMMAND` (`realpath`'d, good) and leaves `PATH`
inherited, recording it as `child_path`. unblob itself resolves the extractor by bare name, so the
child PATH is load-bearing:

```
unblob/handlers/filesystem/squashfs.py:25  EXECUTABLE = "sasquatch"
unblob/handlers/filesystem/squashfs.py:26  V4BE_EXECUTABLE = "sasquatch-v4be"
unblob/dependencies.py:30                  is_installed = shutil.which(command) is not None
```

Measured on this host (`artifacts/R41C1Sentinel/external-binary-inventory.txt`): **13 of the 20**
PATH entries are user-writable, and the first **9** of them precede `/usr/bin` (three
`/run/user/1000/fnm_multishells/<sid>/bin` shims — one holds the 126 MB `node` binary —
`~/.local/share/fnm`, `~/.opencode/bin`, `~/.local/bin`, `~/.local/share/mise/installs/node/latest/bin`,
`~/.local/share/mise/shims`, `~/.local/share/omarchy/bin`). Resolutions:

| binary | resolved | sha256[:16] | pin status today |
|---|---|---|---|
| `git` | `/usr/bin/git` | 2912a2a32f408c9b | bare name (counter, fetch-vendor, c1-extra, score-receipt) |
| `python3` | `/usr/bin/python3` | 375532f83be62028 | bare (c1-run.sh, mk-carriers.py via `which`) |
| `node` | `/run/user/1000/fnm_multishells/5071_1793027685454/bin/node` | 7fde7b8afa198da6 | bare, PATH-only |
| `npx` | `/run/user/1000/fnm_multishells/5071_1793027685454/bin/npx` | 237adf8f3747cad8 | bare, PATH-only |
| `sasquatch-v4be` | `~/.local/bin/sasquatch-v4be` | fac88740f49b3460 | `command -v` in c1-run.sh (recorded, not enforced); `shutil.which` in the counter selftest |
| `sasquatch` | `~/.local/bin/sasquatch` | ad02d27a3d8424b2 | PATH-only (unblob's LE handler) |
| `unblob` | `~/.local/bin/unblob` → uv tool | 0ce7b624f540c219 | absolute (`REA_UNBLOB_COMMAND`), sha recorded |
| `jq` | `~/.local/bin/jq` (jq-1.8.2) | b1c22172dd303f3b | bare, PATH-only |
| `find`, `sed`, `realpath`, `timeout`, `sha256sum` | `/usr/bin/*` | dd7db3e8…, c16be69e…, 5f6c63c5…, 629cb6e8…, e0a612db… | bare |

Exploit path: anything that can write one of those directories (a seat's own scratch is on
`/fast/scratch`, but `~/.local/bin`, `~/.local/share/mise/shims` and the fnm shim dirs are all
user-writable, and 9 of them precede `/usr/bin`) can shadow `node`, `npx`, `sasquatch` or `jq` for
every scoring run; a shadowed `sasquatch-v4be` would also shadow the *rerun*, so receipt and rerun
agree and `projection_ok` stays true — only the frozen oracle constrains it, and a
superset-producing impostor would pass `oracle_hits_ok` as well. Recommend, in priority order:

1. verify `sha256(resolved sasquatch-v4be) == frozen pin` and `sha256(resolved unblob) == frozen pin`
   inside the counter (fail closed), and record both in the result;
2. build the child environment's PATH explicitly: `/usr/bin:/bin:<single verified dir>` (or absolute
   argv where the tool allows it), never inherit;
3. pin `git`, `node`, `npx`, `python3`, `jq` to absolute paths (`/usr/bin/git`, `/usr/bin/python3`
   with `-I -B`, `/usr/bin/jq`); note `npx`/`node` currently come from a `/run/user` shim, which is
   the weakest link.

### F6 — unpinned REA resolution (Medium)

`REA_PIN = 'rea-agents@6.5.0'` is a version, not an integrity pin. `npx -y` resolves it from the
network or the local npm cache on every run, executes the package's `postinstall` hooks, and the
package root is then located with

```bash
find "${npm_config_cache:-$HOME/.npm}/_npx" -maxdepth 5 -path '*/node_modules/rea-agents/package.json'
```

`npm_config_cache` is caller-controlled, so the recorded `rea.package_root` can be made to point at
any tree. Observed package root: `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(`package.json` 6.5.0, `bin.rea = scripts/rea.mjs`, no `_integrity` field).

Impact: a registry/cache substitution changes the extractor and the evidence-id rule while every
clause still evaluates. Fix: resolve the package once into a frozen, digest-pinned directory; seed
`npm_config_cache` from the frozen value rather than the environment; run
`node <pinned>/scripts/rea.mjs` directly; record and check a digest of the package tree (the file
the evidence-id rule lives in) both in `run.json` and in the counter.

### F7 — fetch-vendor writes through planted symlinks (Medium, demonstrated)

```python
with open(out + '.part', 'wb') as fh: fh.write(body)      # out = cache/<pin>.bin; .part is attacker-named
os.replace(out + '.part', out)
...
open(os.path.join(image_cache, want + '.image'), 'wb').write(b)   # same pattern
```

`open(..., 'wb')` follows a symlink. Demonstrated (`artifacts/R41C1Sentinel/demo-cache-symlink-write.py`):

```
ok = True
victim now 5504 bytes, starts b'sqshVENDORBY' (was 18 bytes ascii)
```

i.e. a pre-planted `cache/<pin>.bin.part` symlink makes the tool write vendor firmware bytes over an
arbitrary path the user can write, and report success. Impact: licence breach (vendor bytes landing
in a committed path or a shared scratch file) and silent corruption of another seat's evidence, if
`--cache`/`--image-cache` is shared, world-writable or pre-populated. Fix: `os.makedirs(cache,
mode=0o700, exist_ok=True)` then create with `os.open(path, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,
0o600)`; refuse a cache path that is inside any `git rev-parse --show-toplevel` (it must never be
the lane); verify the pin again by re-reading the written file before printing `ok`.

### F8 — fetch-vendor argument/host surface (Low)

- `git -C <root> show <rev>:<path>` — `--rev` is interpolated as a single argv element, so a value
  beginning with `-` is parsed by git as an option (`--rev=--output=/somewhere` yields
  `git show --output=/somewhere:.ufo/…`). Validate `^[0-9a-f]{40}$`.
- `urllib.request.urlopen(url)` has no scheme allowlist: `file://` and `data:` URLs turn the tool
  into a local-file/hash oracle (the image digest still gates content, so analysis-only).
- `r.read()` is unbounded (a 5 GB body OOMs the fetcher); cap at the expected image size or a
  fixed ceiling.
- `image_sha256` is used as a filename component before any shape check; add `SHA_RE` validation in
  `materialise()` (the counter validates it, the tool does not).
- `fetch-vendor.run()` returns 0 when the spec simply omits a carrier: demonstrated
  `V4 entry dropped from the spec → rc=0, materialised=3` and
  `V4 lost its external block → rc=0, materialised=3`
  (`artifacts/R41C1Sentinel/demo-fetch-exit-semantics.py`). Do not use this exit code as a
  four-carrier gate; the round-41 counter must keep `carriers_matched == 4` as the gate (it does),
  and `carriers_spec()` should additionally require every expected id to carry an `external` or
  `path` block (it already requires one of the two per entry, but not that the *set* materialised).

### F9 — the exact-path rule depends on an unstated grammar (Low, calibration)

The prototype fix
`w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff` replaces
`candidate == rel or candidate.endswith('/' + rel)` with `extract_rel(candidate) == rel`, where
`extract_rel` drops the **first** component only when it ends with `_extract`, and its docstring
documents nested extraction (`a_extract/b_extract/x → b_extract/x`). That is the correct repair of
R40-CL1 and it covers all three call sites (`oracle_hits`, `nonregular_published`, `gap_check`'s
path-resolved branch) because they all go through `same_rel`.

I unit-tested the two functions in isolation (`artifacts/R41C1Sentinel/demo-exact-match.py`):
11 cases, 10 pass — both R40-CL1 directions now fail (`usr/bin/busy` vs `bin/busy`, and the
reverse), `$output/` prefixes, `..` climbing, empty rows and `None` all behave; the miss is
`/abs/out/firmware.bin_extract/etc/version` (extract root not the first component) → `False`.
That is **fail-closed**, so it cannot inflate a score — but it means a genuine oracle row could be
missed if the receipt grammar ever changes.

Correction to my own first reading (measured by `R41CritC1Draft`, §(c) "Does exact extract-root
matching need special cases?", and item (iv) of its replacement predicate; I did not re-run it):
"the first component is the extract root" holds **only for a chunk that covers `[0,len)`**. A carve
or a mid-file chunk is extracted under `<staged>_extract/<start>-<end>.squashfs_v4_be_extract/…`, so
the receipt path carries **two** `_extract` components; `extract_rel` drops only the first and the
inner root stays in the compared path — fail-closed, but every oracle row would miss. Observed V1/L1
receipts are `[0,len)` chunks (`firmware.bin_extract/<rel>`), which is why the prototype is adequate
for the four round-41 carriers (all carves at offset 0). The rule and the predicate must therefore
derive the root **per chunk** from `normalized_result.chunks[].range` — never from the carrier's file
name — and `handler_ok` must be "exactly one `squashfs_v4_be` chunk", because a two-chunk carrier
produces two null-path `depth-limited` gaps against a structural allowance of 1.

Recommendation: state the per-chunk derivation in the predicate, and add two selftest cases — an
offset-chunk receipt path (`firmware.bin_extract/8192-…_extract/<rel>`) and a two-chunk envelope
(two `depth-limited` gaps, allowance 1) — the prototype diff tests both collisions and `$output/`,
but neither of these.

### F10 — carve-is-exactly-`bytes_used` is not asserted (Low)

`layout_probe()` requires BE `sqsh`, v4.0, `mkfs_time == bytes_used`, `0 < bytes_used <= len(raw)`
and LE metadata block length — which correctly rejects the marker-only standard-BE body from round
39. It does not require `bytes_used == len(raw)`. The draft says V3/V4 are "carved to `bytes_used`",
i.e. the pin should cover exactly the image. Adding `bytes_used == len(raw)` for the two vendor
carriers makes the carve self-binding (and would catch a spec `length` that is longer than the
filesystem image).

---

## 2. Answers to the five assigned questions

**(1) fetch-vendor cache poisoning / TOCTOU; nested-file trust.**
No TOCTOU exists on the hash→carve path: `materialise()` hashes the in-memory image, compares, and
then carves *that same object*; the carve bytes are hashed again in memory before the write, and the
counter re-verifies the pin on the cache file it reads (`carrier_pin_ok`, and `projection_ok` is
`False` when the carrier is absent or the pin fails — no vacuous pass). Cache *reads* are also
safe: `fetch()` re-hashes a cached image and falls through to the network on mismatch. The real
problems are on the write side (F7, arbitrary-file write through a planted `.part` symlink), the
exit code (F8: 0 with a carrier missing), and the missing member link (F1).
Nested-file trust: `carve()` opens `tarfile` in `r:` mode, requires `m.isfile()` (so symlink members
are rejected), never extracts to disk (no path-traversal surface), and bounds `length` by
`len(data)`. Ambiguity risk is duplicate member names — `names = {m.name: m …}` keeps the *last*,
so a crafted tar with two members of one name is decided by the pin (fails closed). Measured: the
two rebuilt images have no duplicate member names (V1 image: 21 members, one regular
`./var/remote/var/tmp/filesystem.image` 5,443,592 B plus a second `x86/filesystem.image`
28,200,968 B; V2 image: 11 members, one regular 26,013,704 B). No issue in practice; note the
duplicate-name selection if the round-41 images gain members.

**(2) Could a committed artifact carry vendor bytes?**
No, by three independent tests at the base revision
(`artifacts/R41C1Sentinel/scan-committed-vendor-bytes.py`, exit 0, `clean: true`):
- **pin equality**: 0 of 28,693 blobs (402,448,242 B) match any pin in
  `.ufo/waves/round-40/c1/carriers.json` — neither the two carrier pins, the two `member_sha256`
  values, nor the two `image_sha256` values.
- **size**: 0 files > 1 MiB under `.ufo/waves/round-40/` or `corpus/evidence/round-40/` (the
  largest round-40 evidence file is `V1/after.json`, 383,481 B; the two committed `carrier.sqsh`
  files are the lane-built L1/L2, 230,884 B and 241,390 B). A carve (5,442,392 B / 26,013,550 B)
  or a member (5,443,592 B / 26,013,704 B) cannot hide under those limits.
- **window sharing**: 192 random 128-byte windows from the two rebuilt vendor carriers, searched in
  every blob of the whole lane at base: 0 hits.
For completeness, the round-40 `c1-run.sh` copies only `after.json`, `run.json`,
`after.envelope.json`, `oracle.tsv`, `nonregular.tsv`, `oracle-check.tsv`, `oracle-run.json` into the
evidence directory — metadata, digests and paths only (`c1-run.sh:375-377, 539, 549, 598`); it
never copies the extraction tree.

**(3) Must the frozen-path list include the five tools and the oracle tables?**
Yes to all five, and the current list is incomplete in three places.

Already in `FROZEN_PATHS` (c1-counter.py:206-218): `plans/round-40-claims.md`, `c1-counter.py`,
`c1-extra.py`, `c1-run.sh`, `fetch-vendor.py`, `sqfs-list.py`, `gen-squashfs.py`,
`mk-l-carriers.py`, `carriers.json`, `gap-rule.json`. Oracle/non-regular/carrier files are covered
*transitively* through `frozen_drift()`, which adds each frozen carrier's `path`, `oracle` and
`nonregular` — that works only because those keys are in `carriers.json`; it is not obvious and it
breaks the moment a carrier uses a different key.

Missing for round 41:
1. **`mk-carriers.py`** — it generates the manifest; round-40 froze the *output* but not the
   generator (a post-freeze manifest regeneration would not be flagged as drift, though
   `carriers_unchanged` would catch a content change).
2. **receipts** — `corpus/evidence/round-41/c1/<id>/after.json`, `run.json`, `provenance.json`.
   The derived path is used by default (`receipt` key absent) and is in **no** frozen set (F3).
3. **the oracle tables on their own** — add the explicit paths (not only through spec keys), so a
   carrier entry that renames or omits `oracle` cannot drop its table out of the drift set. Keep the
   `frozen_drift()` "uncovered kinds" cross-check (`gap_rule_ok`) as the second line of defence.

Also freeze the round-41 constants themselves: with `PLANS = plans/round-41-claims.md` first, the
claim text must be inside the drift set (round 40 did this correctly). Frozen paths must **not**
include the claim *surfaces* (`PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/…`,
`corpus/SOURCES.md`) — those are exactly what the claim moves; the counter reads them at REV.

**(4) Licence: does the round publish only paths/sizes/digests?**
Confirmed for the round-40 corpus and the round-40 wave trees (see (2)). Every vendor-carrier
artifact is metadata: `oracle.tsv` (relpath, sha256, size), `nonregular.tsv` (relpath, kind,
detail), `after.json` (paths, digests, chunk/gap bookkeeping, engine info, stdout/stderr text),
`run.json` (argv, pins, timings), `provenance.json` (the chain). Vendor bytes live only in the
operator's scratch cache (`$S/cache/<pin>.bin`) and are cited by sha256 + rebuild command — the
behaviour the AVM note prescribes. Two caveats to keep the property in round 41: (a) the fetch cache
must never point inside the lane (F7's guard would enforce it); (b) `after.envelope.json` is written
by `c1-run.sh` but was not committed in round 40 — if round 41 starts committing it, re-run the
window scan, because an envelope carries more of the run's text than `after.json`. R40-CL7 (the
terms also purport to forbid analysis) remains an operator question, unchanged by this review.

**(5) PATH hygiene of the counter: external binaries and absolute-pin recommendations.**
Full inventory and resolution table in §1 F5 /
`artifacts/R41C1Sentinel/external-binary-inventory.txt`. Binaries reachable from the C1 chain:
`git`, `python3`, `node`, `npx`, `unblob` (absolute via `REA_UNBLOB_COMMAND`), `sasquatch`,
`sasquatch-v4be`, `jq`, `find`, `sed`, `realpath`, `timeout`, `sha256sum`, plus everything unblob
itself shells out to through `PATH`. Recommended pins: `REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob`
(already) with a frozen sha256 (`0ce7b624…`) checked in the counter; `sasquatch-v4be` by absolute
path with a frozen sha256 (`fac88740…`) and a restricted child `PATH` (`/usr/bin:/bin:<verified
dir>`) so unblob's `shutil.which` cannot pick an impostor; `git=/usr/bin/git`, `python3=/usr/bin/python3`
(`-I -B`), `jq=/usr/bin/jq`; and replace `npx`/`node`-from-PATH with the resolved absolute node
binary of a pinned version (today `/run/user/1000/fnm_multishells/…/bin/node`, a per-shell shim).

---

## 3. Port checklist for the round-41 counter (constants that must change)

`tools/round-40/c1-counter.py` is frozen and hardcodes round-40 state in ten places; a mechanical
copy silently keeps it:

| line | constant | round-41 value |
|---|---|---|
| 188-189 | `CARRIERS`, `GAPRULE` | `.ufo/waves/round-41/c1/…` |
| 190 | `AFTERDIR` | `corpus/evidence/round-41/c1` |
| 191-193 | `ENTRY`, `STEM`, `CORE_HEADING` | `2026-10-26-r41-avm-be-squashfs-core`, `## Round-41 additions to Core` |
| 194 | `FRONTIER_MARK` | `Round-41 frontier note` |
| 199 | `IDS` | `('V3', 'V4', 'L3', 'L4')` |
| 200 | `PROV_SEGMENT` | `/kaidoku-r41/` **and** prefix-tested, not `in` |
| 208-219 | `FROZEN_PATHS` | see §2 (3) |
| 265, 111-166 | scratch `kaidoku-r40` | `kaidoku-r41` |
| 403, 452 | `claim != 'R40-C1'` | `R41-C1` (fails closed today, but every binding fails) |
| 206-207 | `DEV_AVM_IMAGE` (`~/Projects/shokuknow/…`, outside the lane — closure D1) | a scratch-passed path or a committed digest-pinned fixture |

Two structural points: (a) `same_rel` must be replaced by the prototype's `extract_rel` equality
*and* the selftest must keep both collision directions (the diff does); (b) `TARGET = 4` stays, but
"four carriers" must be gated on `carriers_matched` and on the spec's id set, never on
`fetch-vendor`'s exit code (F8).

---

## 4. What I checked and found sound (negative results)

- `same_rel` at base really is the R40-CL1 defect (`candidate.endswith('/' + rel)`, line 606-607) and
  it is used by `oracle_hits`, `nonregular_published` and `gap_check` — the prototype diff fixes all
  three at once; no fourth call site exists (`grep -n same_rel` → lines 606, 638, 647, 682).
- `layout_probe()` correctly rejects a marker-only standard-BE body (requires LE metadata by
  plausibility or identity, not just `mkfs_time == bytes_used`), and requires `0 < bytes_used <= len`.
- `projection_ok` fails closed when the carrier is absent or its pin fails (`projection_skipped`).
- `frozen_drift()` raises `FrozenPathChanged` (exit 2) before any clause runs, so a touched frozen
  path can never read MET; `carriers_unchanged` / `gap_rule_unchanged` double-check content.
- Vendor cache reads by the counter are pin-verified (`carrier_pin_ok`), so a *read-side* poison
  cannot score.
- `c1-run.sh` clears `CDPATH`, resolves `unblob` with `realpath`, hashes it, and records the whole
  child `PATH` in `run.json` (`child_path`) — the data F3 needs is already collected.
- The tar member chosen for V1/V2 is unambiguous (no duplicate names, `isfile()` guard).

---

## 5. Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r41/<seat>; mkdir -p "$S"; cd "$S"; export TMPDIR="$S"
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
A=$L/.ufo/waves/round-41/w1/artifacts/R41C1Sentinel

# vendor bytes (dev inputs: 6490 Cable 07.57, 6820v1 LTE 07.30) — never copied into the lane
python3 -I -B $L/tools/round-40/fetch-vendor.py --root $L \
  --rev 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --cache "$S/cache" --image-cache "$S/imgcache"
#   exit 0, V1 ac4098bd… (5,442,392 B), V2 5ccc7614… (26,013,550 B)   → $A/fetch-vendor-rebuild.json

python3 -I -B $A/scan-committed-vendor-bytes.py --lane $L \
  --rev 49096c7e6f226af0c750c4b003be58883cb6049f --cache "$S/cache"
#   exit 0, "clean": true, 28,693 blobs / 402,448,242 B, 192 windows, 0 pin/size/window hits
python3 -I -B $A/demo-member-sha256.py          # member pin ignored: 3/3 ok=True
python3 -I -B $A/demo-cache-symlink-write.py    # 18-byte victim clobbered with 5504 carrier bytes
python3 -I -B $A/demo-fetch-exit-semantics.py   # rc=0 with V4 dropped from the spec
python3 -I -B $A/demo-exact-match.py            # 11 cases, 10 pass; the miss is fail-closed
```

Digests: `fetch-vendor.py` `ccc4dc2364892e7cc5f716cd461c4ce1a4f62d059c05f79ba94bf2ad7e5a69f1`;
`unblob` `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` (26.6.4);
`sasquatch-v4be` `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` (4.5.1);
rea-agents package root `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (6.5.0).

## 6. Tooling record

No tool was installed, upgraded or moved (pacman transactions are paused host-wide; nothing was
needed). Used, unmodified: `python3` 3.14.8 (`-I -B`, no bytecode written into the lane), `git`
2.56.0, `unblob` 26.6.4 and `sasquatch-v4be` 4.5.1 **read/identified only** (no extraction run), and
`fetch-vendor.py` (a downloader, not an extractor) on the two allowed 07.57/07.30 development
images. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C1Sentinel` was removed after the artifacts were
copied; no vendor bytes are in this report or in the artifacts directory.

## 7. Wave-1 cross-seat reconciliation (with `R41CritC1Draft`)

Read-only cross-check of `R41CritC1Draft.md` §(a2),(d),(e),(i) and its `attack-controls.py`; I did
**not** re-run their prototypes, so their carrier digests and entry counts below stay attributed.

**D1 (theirs, decisive — not replaced by anything in this report).** The draft has no carrier
identity/freshness clause: pinning the round-40 carriers and oracle tables under V3/V4/L3/L4 and
copying their receipts post-freeze scores 4/4 with no REA run, because the counter-time rerun then
runs on the re-pinned bytes, so `subject_pin_ok`, `projection_ok` and `evidence_id_ok` are satisfied
*by construction*. `carriers_spec()` has no concept of a previously used pin, and the draft's carrier
names live only in prose. Their `carrier_fresh_ok` (carrier pins must differ from every pin committed
at or below the freeze, plus a frozen `prior_pins`, four pairwise-distinct) is the gate; my F3 and
their e12 raise cost only. Evaluate the forbidden set **at the freeze** (immutability makes it
deterministic), not by a REV-time scrape; the set is previous C1 carrier pins + previous C1 receipt
subject digests + a frozen `prior_pins`. Drop oracle-table digests — a carrier pinned to an oracle
table's digest already fails `layout_ok` (not a `sqsh`), so the entry is noise — and drop "evidence
envelope" as redundant with the receipt subject.

**D2 (mine, carried as scored clauses).** `member_sha256`/nested-digest chain (F1 = their e5) —
their seats already publish the whole-member and nested digests, which is exactly the shape my
demonstration asks for: with the current tool a wrong or absent `member_sha256` returns `ok=True`.
`rea_params_ok` (F4 = their e10): `max_depth == 1`, output bounds, unblob 26.6.4 with the resolved
binary digest, `run.json`'s sasquatch-v4be 4.5.1 / `fac88740…`. Child-PATH construction plus
"rerun's resolved `sasquatch-v4be` digest equals the receipt's recorded tool digest" (F5 = their
e11). `run.json` binding and drift-set additions (F3 = their e12), framed as cost, never as proof.

**D3 (their correction to my F9, adopted).** "First component is the chunk extract root" holds only
for `[0,len)` chunks; any carve yields
`<staged>_extract/<start>-<end>.squashfs_v4_be_extract/…` and the prototype's single-component strip
leaves the inner root in the compared path (fail-closed), and a two-chunk carrier yields two
null-path `depth-limited` gaps against a structural allowance of 1 — so `handler_ok` must become
"exactly one `squashfs_v4_be` chunk" and the root must be derived per chunk from `chunks[].range`.
All four round-41 carriers are offset-0 carves, so the prototype remains adequate for the score while
the predicate text and selftests must be fixed.

**D4 (residual no clause closes).** A receipt fabricated from the oracle on genuinely fresh bytes
still passes (the rerun agrees with it). The freeze text must say provenance is **not** proven —
`evidence_id_ok` is well-formedness. This keeps R40-CL2 honest without pretending it is repaired.

**D5 (the seats' measured facts — wave artifacts, not pins, and not this report's measurements).**
V3 (`artifacts/R41C1VendorV3/carriers-fragment.json`): carrier pin `c4f74f54…` is the carve
`[0,30233394)` of the member, member `87cc5d6b…` over 30,236,680 B (its `carrier_pin_note` says so
explicitly), image `770efb4e…`, `oracle_counts` 8 regular / 9 dirs / 85 symlinks / 1 char device
(= 104 superblock inodes). V4 (`artifacts/R41C1VendorV4/carriers-V4.json`, `provenance.json`,
`budget.json`): image `a5a3a763…` 36,392,960 B → member `./var/tmp/filesystem.image` `4cfc3016…`
33,361,928 B → nested `filesystem_core.squashfs` `4d5de25c…` 32,722,944 B → carrier `ce27ebca…` =
carve `[0,32720860)`; `budget.json` records the REA 6.5.0 entry budget (default
`max_output_files` 10000, `dist/domain/firmware/firmwareAnalysis.js:42-46`) and the 6349/615/7367
counts. These resolve my F2 (the V4 either/or and the "fits REA's entry budget" branch) — but they
were produced by the owning seats' pre-freeze passes, so (i) the predicate's
untouched-before-freeze sentence must be requalified as in §1 F2, and (ii) the freeze must re-derive
each digest from the committed `carriers.json`, not from a wave report: the peer's §(i) identity text
is a proposal the L1 must fill with committed bytes, and a wave report is not a pin (the same defect
class as F1).
