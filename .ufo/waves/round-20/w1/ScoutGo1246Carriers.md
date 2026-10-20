# ScoutGo1246Carriers — C3 carrier recon (round 20)

Seat: KaidokuR20.ScoutGo1246Carriers-2 (read-only leaf; no subagents; no Go binary executed; no REA/Ghidra run; no `jj`/git writes).
Ticket axes: **coverage** (all 20 carriers, not a nine-file sample), **depth** (buildinfo layout + two misread traps),
**calibration** (correcting what "never analyzed" can be proven from committed bytes).
Written 2026-10-20T17:51:15-03:00 / 2026-10-20T20:51:15+00:00 (clock at first write, from `stat -c '%y'`);
correction pass at 17:52:28 -03:00 (file mtime observed before this final edit). No later or estimated instants are asserted.
Lane baseline unchanged: `14f0260ad319ecc26994381b2415d5a999003375` (contract.md:2); read-only git not exercised.

Scope is exactly the C3 carrier set as the contract defines it — `bin/*` and `pkg/tool/linux_amd64/*` under
`/home/vgpnk/.local/opt/go-1.24.6` (`.ufo/waves/round-20/contract.md:89-92`). No Go toolchain binary was executed;
every command below reads bytes only.

## 1. Carrier set (OBSERVATION)

`ls -la .../bin .../pkg/tool/linux_amd64` → **EXIT=0**: 2 files in `bin/` (`go`, `gofmt`), 18 in
`pkg/tool/linux_amd64/`, all mode `0644` (exec bits cleared, matching
`.ufo/waves/round-20/evidence/carrier-guard/manual-arm.json:3` `taken_at_utc` and its 20 `mode_after: "0o644"`).

Whole-install ELF scan (python, `os.walk` on 14175 regular files, first 4 bytes `\x7fELF`) → **EXIT=0**:
`carriers=20 extra_elf=53`, total carrier bytes **121797646**. The 53 extras are Go **objects/test data**, not
toolchain executables, and **none has any exec bit**: `syso` 2 (`src/crypto/internal/boring/syso`), `testdata`
39 (`src/debug/elf` 25, `src/debug/dwarf` 14), `src/runtime/pprof` 4, `src/runtime/race*` 8; suffixes
`.obj` 20, `.elf`/`.elf4`/`.elf5` 14, `.syso` 10, `.so_` 1, extensionless 8. So the 20-file carrier set is complete
for executable toolchain binaries (supports the frozen-count claim in `claims.json` C3 `before_after`: N ≥ 8).

## 2. Per-carrier size / sha256 / buildinfo / version (OBSERVATION)

Hash + magic scan (python `-I -B`, whole-file `data.find(b"\xff Go buildinf:")`, then every occurrence validated:
16-byte alignment, `ptr_size ∈ {4,8}`, `flags & ~0x3 == 0`, inline uvarint lengths) → **EXIT=0**;
`ALL_HAVE_BUILDINF=True`. Cross-checked with the lane's own decoder
`.ufo/waves/round-17/tools/buildinfo-probe.py` (`MAGIC` at `:30`, `ALIGN` `:32`, `HEADER_SIZE` `:33`,
`PTR_SIZE_OFFSET` `:38`, `FLAGS_OFFSET` `:39`, `FLAGS_VERSION_INL` `:48`) for all 20 → **EXIT=0**; the decoder and the
independent scan agree on version, header offset and magic count for 20/20.

All 20: `\xff Go buildinf:` present, **inline** form (`flags=0x2`), `ptr_size=8`, little-endian, version string
**`go1.24.6`** (8 chars).

| carrier (under `/home/vgpnk/.local/opt/go-1.24.6/`) | size | sha256 | buildinf | version | header off | header vaddr |
|---|---:|---|---|---|---:|---|
| `bin/go` | 14323704 | `d8a308e5fd7fc2752212b49f5cd9cac32fafdc78ccc47f4937cd05cbca68b404` | yes (2 sites) | `go1.24.6` | 12787712 | 0x1032000 |
| `bin/gofmt` | 2926077 | `349a5616eaeb79acc05ebb77a67ae1ee617d4b09d6a817b8e338155374045863` | yes (1) | `go1.24.6` | 2633728 | 0x683000 |
| `pkg/tool/linux_amd64/addr2line` | 2618738 | `58442b897ab89678d67d16c595009e4ab4a2daf47b3b8fd34bd55793ad428c85` | yes (1) | `go1.24.6` | 2351104 | 0x63e000 |
| `pkg/tool/linux_amd64/asm` | 4650770 | `6785f36b7e11b0e52185dc516ff3d8f531b4c7ca9926752b21bbe5535b43ba68` | yes (1) | `go1.24.6` | 4026368 | 0x7d7000 |
| `pkg/tool/linux_amd64/buildid` | 2562362 | `19ccf840f12919deee1b622cea5025415f5304d05fd661bef70865fe211d6481` | yes (1) | `go1.24.6` | 2314240 | 0x635000 |
| `pkg/tool/linux_amd64/cgo` | 4340893 | `408905569997442712eb1dbea1ba80370d0ee60f624dfd127363ec54cbd4e54f` | yes (1) | `go1.24.6` | 3903488 | 0x7b9000 |
| `pkg/tool/linux_amd64/compile` | 20979839 | `09dfabe6f644ac7a82e50725e902093cc6dabf3f61d0aff0c6a7c105ea59e367` | yes (1) | `go1.24.6` | 18419712 | 0x1591000 |
| `pkg/tool/linux_amd64/covdata` | 2998893 | `5759d45359caad341f1c3e49b58581c0300f4d1ece86be198e157dcb4d36645c` | yes (1) | `go1.24.6` | 2658304 | 0x689000 |
| `pkg/tool/linux_amd64/cover` | 4953216 | `0d654eaee35306031d005f8fd7c9c497ef45b5ea46d05880ffd13ae0c0f86c61` | yes (1) | `go1.24.6` | 4407296 | 0x834000 |
| `pkg/tool/linux_amd64/doc` | 3453020 | `df470db854e19e7c932e7d26dfcb63afbd65d8750be094838023060e78cc65cb` | yes (1) | `go1.24.6` | 3080192 | 0x6f0000 |
| `pkg/tool/linux_amd64/fix` | 2958934 | `816e6374ffd07b6ff3fc6633d9ef6cffa8d9f04bc286f8c6154e5be1d872b948` | yes (1) | `go1.24.6` | 2662400 | 0x68a000 |
| `pkg/tool/linux_amd64/link` | 6230794 | `cba420d80ab95282d66e67a08cbe7e15670861cfe71959a44f855c05ee808d2e` | yes (2 sites) | `go1.24.6` | 5636096 | 0x960000 |
| `pkg/tool/linux_amd64/nm` | 2603850 | `3b714bc40358ca70e07c71345a3d4f71ac5b44c2c6ddda77252eb93acfd3cc4b` | yes (1) | `go1.24.6` | 2334720 | 0x63a000 |
| `pkg/tool/linux_amd64/objdump` | 4617408 | `225e767ca425d62969be0abcbd38f12b8e2a3ce3421ac23b5936e990bc9bfd57` | yes (1) | `go1.24.6` | 3706880 | 0x789000 |
| `pkg/tool/linux_amd64/pack` | 2092793 | `5d7a41e83cc2cd58f675044b692456a137a959f92fc3614081348537fda1446a` | yes (1) | `go1.24.6` | 1875968 | 0x5ca000 |
| `pkg/tool/linux_amd64/pprof` | 13958879 | `8218e4e3531ac53f681bbea2de258afc438c61965a01d6083e4d665c704ce8aa` | yes (1) | `go1.24.6` | 11976704 | 0xf6c000 |
| `pkg/tool/linux_amd64/preprofile` | 2203930 | `789192d566a4128506fda395ea3e2ff9a7e44f5221665fab5e9e65936d07b1e7` | yes (1) | `go1.24.6` | 1982464 | 0x5e4000 |
| `pkg/tool/linux_amd64/test2json` | 2393560 | `9ab01024a93aebab7ef88867cfa20772c778ae4193e2c7d30cf0ef93205d94cd` | yes (1) | `go1.24.6` | 2146304 | 0x60c000 |
| `pkg/tool/linux_amd64/trace` | 13451782 | `d65fb56e8e320af369a662f1a15d5a6c82abb06610d4e584576dcbdd33658186` | yes (1) | `go1.24.6` | 12169216 | 0xf9b000 |
| `pkg/tool/linux_amd64/vet` | 7478204 | `a9fb46ae5365ad80cdaf31ea1d2e66d1be093ca00837fd30a4c5e1efacbc2944` | yes (1) | `go1.24.6` | 6815744 | 0xa8000 |

Magic sites: **22 across 20 files** (18 files × 1; `bin/go` and `link` × 2). All 20 rows above agree **exactly**
(sha256, size, mode) with the carrier-guard manifest: python diff of my rows against
`.ufo/waves/round-20/evidence/carrier-guard/manual-arm.json` → **EXIT=0**, `arm_count=20 mine=20
disagreements=[] extra_paths=[]`. Anchor for `link`'s hash: `manual-arm.json:95`.

### Buildinfo layout (OBSERVATION, `xxd -s 2633728 -l 64 bin/gofmt` → EXIT=0)

```
00283000: ff20 476f 2062 7569 6c64 696e 663a 0802  . Go buildinf:..
00283010: 0000 ... (16 bytes zero pad)
00283020: 0867 6f31 2e32 342e 36d9 0130 77af 0c92  .go1.24.6..0w...
00283030: 7408 0241 e1c1 07e6 d618 e670 6174 6809  t..A.......path.
```
14-byte magic, `ptr=0x08`, `flags=0x02` (inline), 16-byte pad to 32, then uvarint `0x08` + `go1.24.6`, then
uvarint `0xd9 0x01` = 217 + module info beginning with the `INFO_START` sentinel `3077af0c…`. Section profile
(`readelf -S -W`, all 20) → **EXIT=0**, one distinct profile `0/1/1`: **0 `.debug_*` sections**, 1 `.go.buildinfo`,
1 `.go.fipsinfo`. The absence of DWARF is consistent with the round-18 census build setting
`"-gcflags": "cmd/...=-dwarf=false"` (e.g. `.ufo/waves/round-18/evidence/real-carrier-census.json:478`, the
`bin/go` entry, whose `dep_count: 0` at `:486` identifies the same object) — relevant to any forecast of Ghidra's
first failure, since only pclntab/typelink are available.

### Two misread traps (OBSERVATION; calibration for C3's first-failure hypotheses)

1. **Decoy magic sites.** A naive whole-file first-hit returns an invalid header for `link`: first occurrence at
   3382936 has `ptr=114, flags=117` (not a header) inside `.rodata` (file `[0x2bd000,0x3cf241)`), while the true
   header is at 5636096 in `.go.buildinfo` (section `[0x560000,0x560110)`). `bin/go` likewise has a decoy at
   12790752 in `.noptrdata` (file `[0xc321a0,0xc7b2c1)`), 3040 bytes past its true header at 12787712. Both decoys
   are adjacent to ordinary string data, i.e. copies of the constant rather than headers: `link`'s decoy reads
   `…buildinf:runtime.egcbssmain..inittask…`; `go`'s reads `…buildinf:\0\0]]]]><![CDATA[>…`. The lane decoder handles this correctly — on `link` it reports
   `header_offset: 5636096`, `magic_file_offsets: [3382936, 5636096]`, `search_space: ".go.buildinfo section"`
   (`python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py <link>` → **EXIT=0**) — but any first-hit scanner,
   including a Ghidra-side one, would mis-locate `link`'s blob.
2. **`strings -a | grep -m1 go1.24` is not a version test.** On `bin/go` the first `go1.2x` match in file order is a
   regex constant containing `go1.24` (`strings -a … | grep -n 'go1\.2[0-9]'` → line 132471), long before the real
   `go1.24.6` strings at lines 136212 and 156190. Only the buildinfo blob (or a `go1\.24\.6`-exact grep) is
   authoritative; `-m1` on the loose pattern silently yields `go1.24`.

## 3. Install vs official archive (OBSERVATION)

- `curl -fsSL 'https://go.dev/dl/?mode=json&include=all' -o /tmp/kr20-go-dl.json` → **CURL_EXIT=0**; parsed entry:
  `filename=go1.24.6.linux-amd64.tar.gz`, `sha256=bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712`,
  `size=78583176` — equals the round-19 record at `corpus/lessons/round-19.md:71-73` (and the sibling provenance
  seat's line-anchored quote in `.ufo/waves/round-20/w1/SourceGo1246.md`).
- Fresh download `https://dl.google.com/go/go1.24.6.linux-amd64.tar.gz` → **CURL_EXIT=0**, 78583176 bytes,
  `sha256sum` → **EXIT=0**: `bbca37cc…8712` (byte-identical to the JSON).
- `tar -xzf` of the 20 members into a `mktemp -d` staging dir → **TAR_EXIT=0**; sha256 comparison (python `-I -B`)
  → **EXIT=0**: `matched=20/20 diff=[]` — i.e. all twenty installed files, not merely nine, hash identically to
  their archive members.
- Archive-vs-filesystem metadata (same python run, **EXIT=0**): every member is `tar_mode=0755` vs `fs_mode=0644`
  (the cleared exec bit), `mode_mtime_size_disagreements=[]`; installed mtime equals the tar member mtime
  **1754075906 = 2025-08-01T19:18:26+00:00** for 20/20. Ownership differs as expected for a user-space extract
  (`tar 0:0` → `fs 1000:1000`). This is an extraction, not a rebuild: content, mode, and mtime all derive from the
  official archive.

## 4. Prior exposure to REA/Ghidra (OBSERVATION, with one correction to the ticket's framing)

The ticket asks to prove "none was ever analyzed by REA/Ghidra". The provable statement is narrower and I state it
exactly:

- **All 20 carriers were already inspected by REA `inspect-go-binary` in round 18.** Every one of the 20
  go-1.24.6 entries in `.ufo/waves/round-18/evidence/real-carrier-census.json` carries `rea_evidence_id` and
  `rea_inspect_exit: 0` (e.g. `bin/go`: `go_version` `:493`, `path` `:499`, `rea_evidence_id` `ev_75e9de40…`
  `:500`, `rea_inspect_exit` `:501`, `sha256` `:502`; `link`: `path` `:852`, `rea_evidence_id` `ev_11daed0e…`
  `:853`, `sha256` `:855` — and a duplicate `link` record in `ranked_candidates` at `:1516-1519`, so path-grep
  counts over this file are not entry counts; all 20 keys include `rea_evidence_id`/`rea_inspect_exit`). The census method field names the channel: `real-carrier-census` via
  `carrier-census.py` "(REA inspect-go-binary 6.5.0 + pacman -Qo)" — documented as the census command in
  `.ufo/waves/round-17/contract.md:35,64,112` and restated in `.ufo/waves/round-18/w1/RealCarrierCensus.md:23`.
  So the bytes have been read by a REA command and the build metadata (version, build settings, module path) is
  already on record. "Never touched by REA" would be false.
- **No REA `analyze`/`search`/`decompile` and no Ghidra `analyzeHeadless` has ever targeted any of the 20.**
  Two independent scans:
  - by path: python walk of 11710 `.json/.jsonl/.txt/.md/.log/.stdout/.stderr` files under `.ufo/waves` for files
    containing a go-1.24.6 value together with an analysis verb → **EXIT=0**, **6 files at scan time**, all
    assignment/prohibition text (`round-20/contract.md:91`, `round-20/gen-wave1.py:650`, `round-18`+`round-20`
    `wave1-spec.json` / `wave1-dispatch.json` prompt bodies, `round-18/wave1-result.txt` spawn summary). Re-run a
    few minutes later (after sibling reports landed) → 8 files: the two additions are this report and
    `w1/ScoutGo1273Exposure.md`; still **zero receipts**. No same-line pairing of a go-1.24.6 path with `analyze*`
    exists outside prohibition/assignment text (line-level re-scan → empty).
  - by content hash: `grep -rl <sha256>` over `.ufo/waves/` for **all 20** carrier hashes (not a nine-file sample)
    → **EXIT=0**. At first scan each hash hit exactly **2** files: the round-18 census and `manual-arm.json` —
    neither an analysis receipt. Re-run after sibling artifacts landed: those 2 plus non-receipt references only —
    this report (all 20) and `w1/GenPredictionsR20.md` + `w1/patches/GenPredictionsR20-2.patch` (for the 10 carriers
    in that frozen sample); measured histogram **5 files × 10 hashes, 3 files × 10 hashes**, zero receipts.
    (The archive digest `bbca37cc…` is a different value, appearing in 11 unrelated provenance/prompt files; it is
    not a carrier content hash.)
- **Every round-18 analysis receipt targets something else.** All 15 `runs/*/receipt.json` targets are either real
  applications (`/usr/bin/aether`, `/home/vgpnk/.local/bin/notesmd-cli`, `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge`)
  or synthetics under `/home/vgpnk/.local/share/kaidoku-r18/carriers/` — e.g. `runs/s1246-swiss-methods/receipt.json`,
  `runs/calib-aether/receipt.json`, `runs/real-kimi-webbridge/receipt.json`. That matches the ticket's premise:
  go1.24.6 (and 1.25.0) was used only to **build** the round-18 synthetics.
- No `.log` anywhere under `.ufo/` mentions `go-1.24.6` (`grep -rl` → **RC=0**, no paths), and `.ufo/state` has no
  mention (**RC2=0**). `analyzeHeadless` is mentioned in 137 committed files — none of them a go-1.24.6 target.
- **Independent sibling corroboration (read-only artifacts, not my runs).** `w1/CriticC3.md:66-67` runs the same
  hash-set grep and reports "only `.ufo/waves/round-18/evidence/real-carrier-census.json`", with the same off-lane
  caveat at `:73` — two independent scans, same conclusion. `w1/GenPredictionsR20.md:13-22` freezes a **10-carrier**
  sample from this set (`go, gofmt, asm, cgo, compile, cover, preprofile, vet, pprof, trace`) as
  `held-out-toolchain`; the other **10** carriers I hashed (`addr2line, buildid, covdata, doc, fix, link, nm,
  objdump, pack, test2json`) are verified but outside that frozen sample — coverage headroom if N must widen.
  That seat also records (`:7`) that its prediction blobs could not be generated because the v2 emulator had not
  landed, so at the time of writing C3's N rests on a manifest, not on a frozen forecast.

Consequence for C3: the 20 carriers are **held out from analysis** (no frozen-read prediction has ever been
scored against them), but they are **not held out from REA metadata inspection**. If the round-20 claim is scored
as "held-out = never analyzed", it holds; if read as "never processed by REA at all", it must be reworded.

## 5. Residual unknowns / limits (INFERENCE unless stated)

- Everything above is scoped to **committed lane evidence** (`.ufo/waves`, `.ufo/state`) plus the live filesystem.
  I did not inspect REA/Ghidra caches or project stores outside the lane; nothing required it, and no receipt
  exists in the lane, so analysis can only be shown absent *in the lane*, not system-wide. (INFERENCE, from
  absence of receipts.)
- The 53 non-carrier ELFs are objects/`.obj`/test data (none executable); they were counted, not hashed. If the
  round wants a complete "every ELF under the install" census, that is a separate claim. (OBSERVATION + scope note.)
- The second magic in `go`/`link` is a constant copy in `.noptrdata`/`.rodata`; I did not disassemble to identify
  the referencing function (would require analysis of the carrier within this seat's prohibition, and is not needed
  to establish the misread).
- Archive match is content-level (sha256) plus member mode/mtime; I did not verify the archive's GPG/signature
  chain beyond the TLS-fetched go.dev JSON publishing that digest (the same channel the round-19 record used).

## 6. Commands run (each with observed exit)

| # | command (abridged) | exit |
|---|---|---|
| 1 | `ls -la .../go-1.24.6/bin .../pkg/tool/linux_amd64` | 0 |
| 2 | python whole-file sha256 + `\xff Go buildinf:` scan, 20 files | 0 (`count=20`, `ALL_HAVE_BUILDINF=True`) |
| 3 | python validated-header reparse (align/ptr/flags/uvarint) | 0 (20/20 `go1.24.6`) |
| 4 | `curl -fsSL 'https://go.dev/dl/?mode=json&include=all' -o /tmp/kr20-go-dl.json` | 0 |
| 5 | `curl -fsSL https://dl.google.com/go/go1.24.6.linux-amd64.tar.gz -o …` | 0 |
| 6 | `sha256sum …/go1.24.6.linux-amd64.tar.gz` | 0 (`bbca37cc…8712`) |
| 7 | `tar -xzf` 20 members + python sha256 compare | 0 (`matched=20/20 diff=[]`) |
| 8 | `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py <each of 20>` | 0 per file |
| 9 | `readelf -S -W` profile loop (`.debug_*`, `.go.buildinfo`, `.go.fipsinfo`) | 0 (20× `0/1/1`) |
| 10 | `xxd` header/decoys; `strings -a \| grep -n 'go1\.2[0-9]'` | 0 |
| 11 | python install-tree ELF walk + exec-bit check | 0 (`carriers=20 extra_elf=53`) |
| 12 | python compare vs `manual-arm.json` | 0 (0 disagreements) |
| 13 | python/text scan `.ufo/waves` for path/hash × analysis verb | 0 (6 assignment-text hits; 0 receipts) |

Scratch (download, extracted tree, JSON rows) lived only under `mktemp -d /tmp/kr20-c3-*` and was removed after
this report was written. **Installs: none** — no tool was installed or upgraded for this seat (no pacman transaction
was attempted; the host-wide pause was respected).

Report: .ufo/waves/round-20/w1/ScoutGo1246Carriers.md
