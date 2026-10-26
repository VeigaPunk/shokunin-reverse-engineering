# R36W2CriticEntryC1 — attack on `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`

Seat: critic, wave 2 (falsify the integrated landing). Axes: **coverage**, **calibration**.
Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, target
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` at the assigned tip
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (lane HEAD `6f2ba761`, `.ufo/waves/` only, entry bytes
unchanged — `git log --oneline --follow -- <entry>` = one commit `ffc81341`). Freeze
`790561d4e3aca732a434081aa9573ec2fa5fd7d0`, base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`.
Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2CriticEntryC1`, `TMPDIR` set, removed at exit.
Nothing frozen was changed; no VCS mutation; no subagents; only this report was written.

## Verdict

**The entry's measured data set reproduces; its prose does not.** Every number I re-derived from the
committed receipts, the carrier bytes and two fresh REA runs agrees with the entry (§1). The prose carries
**two false statements about the carriers and the receipt** (F1 `.DirIcon` target, F2 "depth 3"), **one
header that quotes a sub-field of a receipt whose verdict at that revision was red** (F3), **one
contradiction with the entry's own "not claimed" list** (F4), **one scope word the entry's own citation
falsifies** (F5), and eleven lower-ranked label / count / format defects (F6–F16).

No finding requires re-measuring the claim. Each is a prose correction inside the entry, and the correction
is stated with each finding. Severity: **S1** = a reader will act on a false statement about the carrier
bytes or the receipt; **S2** = a false, contradicted or selectively quoted measured statement in supporting prose (F3–F5);
**S3** = a miscount, a mis-described measurement, or a recheck/pin that cannot do what its reader will
assume (F6–F10, F12); **S4** = label, format or convention defect (F11, F13–F16).

## 1. What reproduced (so the findings stay scoped to the prose)

| entry figure | how I checked | result |
|---|---|---|
| carrier digests, oracle offsets | `sha256sum` of freshly downloaded K3/K4; `git show` K1/K2 fixtures | K3 `b644d034…f29fb` 11454968 B, K4 `8efcec73…e1c2` 11356680 B, K1 `938029…a589` 73728 B, K2 `ce5bf60e…084f` 208896 B — all equal `carriers.json`; offsets 0/0/944632/936456 equal `K*/oracle-run.json` |
| oracle rows, distinct digests | `wc -l` / `cut -f2 \| sort -u \| wc -l` on `K*/oracle.tsv` | 3/3, 4/4, 2130/2116, 2130/2116 — equal to the table |
| K1/K2 oracle = committed source trees | hashed `fixtures/k1-src`, `k2-src` (plus the `var/notice-link` symlink) against `K1,K2/oracle.tsv` | byte-for-byte equal, all 7 rows |
| fixture "kind" column | `/usr/bin/unsquashfs -s` on both fixtures | `SQUASHFS 4:0`, Compression xz / gzip, Block size 131072 / 4096 — matches "xz, 128 KiB" and "gzip, 4 KiB" |
| before gap record (all four) | `jq` on `K*/before.json` | one gap each, `missing-extractor-dependency`, handler `squashfs_v4_le`, deps `["sasquatch"]`, `input_path` literally `$input`, `root_file_range` `{0,73728}` / `{0,208896}` / `{944632,10510336}` / `{936456,10420224}`, continuation `4ca863d0…a07a` in all four, `coverage: partial`, one `ExtractorDependencyNotFoundReport` `severity ERROR` |
| before published files | same | K1/K2 `files: []`, `published_bytes 0`, 1 chunk with `extraction_failed: true`; K3/K4 2 files, `published_bytes` 11454968 / 11356680 (= whole carrier), 3 chunks |
| after table (all four) | `jq` on `K*/after.json` | files/gaps/published_bytes/coverage exactly as tabulated (3/0/70086/complete, 4/1/273971/partial, 2147/2/51122564/partial, 2147/2/51792724/partial) |
| 17 extras, composition, padding digest | path and digest diff of published set against `K*/oracle.tsv` (LC_ALL=C) | 17 extras, 0 missing, both carriers; 1 runtime carve + 8 nested carves (nvim + 7 parsers) + 8 one-byte `.padding`, padding sha256 `6e340b9c…a01d` |
| eight receipts: `max_depth 3`, `depth_limited_paths []` | `jq` over the 8 `{before,after}.json` | true for all eight |
| continuation instruction quoted in the entry | `jq .normalized_result.extraction_continuations` | both quoted sentences are byte-identical to `K*/after.json` / `K*/before.json` |
| sasquatch binaries | `stat`, `sha256sum`, `-version` on `~/.local/bin/{sasquatch,sasquatch-v4be}` | 382824 B `ad02d27a…4754`, 436232 B `fac88740…14c6`; **both** print `unsquashfs version 4.5.1 (2022/03/17)` |
| S108 handler claims | installed handler at `…/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` (sha256 `2d7b901b…599287`) | `EXECUTABLE`/`V4BE_EXECUTABLE`, `get_dependencies()` returns both, LE argv `-le -no-exit-code -f -d {outdir} {inpath}`, AVM test `header.bytes_used == header.mkfs_time` — all as the entry says |
| the entry's recheck line | ran it (§F9) | exit 0, `{"files":3,"gaps":0}` |
| K3 and K4 after receipts, independently | fresh `npx -y rea-agents@6.5.0 extract-firmware` on the re-downloaded carriers (rc 0 both) | K3: 2147 files, 17 extras, **2130/2130 oracle rows matched**, 2 gaps, `published_bytes` 51122564, `partial`; K4: 2147 / 17 / **2130/2130**, 2 gaps, 51792724, `partial` |

So: the coverage claim's data is sound and I could not falsify it.

## 2. Findings, severity-ranked

### F1 (S1) — the `.DirIcon` line states the *resolved* target as the payload's symlink, so the symlink statement is false about the carrier

Entry `:118`:

> K2's payload holds `var/notice-link -> ../usr/share/doc/NOTICE`; K3's and K4's payloads both hold
> `.DirIcon -> usr/share/icons/hicolor/128x128/apps/nvim.png` and `nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png`.

The payload does not hold that. Counterexample, from the exact carrier bytes the entry froze (fresh
download, digest equal to `carriers.json`), read with the same oracle tool the entry uses:

```
$ /usr/bin/unsquashfs -o 944632 -ll k3.appimage | grep '^l'
lrwxrwxrwx root/root   8 2026-10-09 12:35 squashfs-root/.DirIcon -> nvim.png
lrwxrwxrwx root/root  45 2026-10-09 12:35 squashfs-root/nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png
$ /usr/bin/unsquashfs -o 936456 -ll k4.appimage | grep '^l'      # identical two lines
```

`8` = `len("nvim.png")`, so the inode target is the literal `nvim.png`. What the entry copied is
`normalized_result.unpublished_entries[].link_target`, which REA reports *resolved* for the indirect link
(`K3/after.json`, `K4/after.json`, and my fresh envelopes reproduce the same resolved string). The entry
never says the envelope resolves.

This is not a new discovery: two wave-1 seats recorded it —
`.ufo/waves/round-36/w1/R36ExecIndependentC1.md:258` ("Fidelity nuance … the raw squashfs link is
`nvim.png`") and `w1/R36ExecReproK4.md:212` ("`unsquashfs -ll` shows `.DirIcon → nvim.png`") — and the
entry it cites for the second oracle states it too (`w1/R36ExecAppImageExtract.md:49`). The landing
repeats the misreading instead of absorbing the nuance.

Why S1: the section is *about* symlink fidelity, and the sentence is the one a reader will transcribe into
a rule ("REA's `link_target` is the payload's link text"). It is also the only place the entry quotes
payload content whose ground truth it did not itself measure.

**Smallest safe correction:** "K3/K4 hold `.DirIcon -> nvim.png` and `nvim.png -> usr/share/icons/hicolor/128x128/apps/nvim.png`; `unpublished_entries[].link_target` reports the *resolved* target for `.DirIcon` (`…/nvim.png`), not the immediate one [INFERENCE: unblob resolves the indirection] (`unsquashfs -ll` on the frozen bytes)."

### F2 (S1) — "depth 3, the configured maximum" is not in any receipt; the receipts say depth 2

Entry `:104-105`:

> 8 nested `carved.elf` from ELF carving inside the payload: `usr/bin/nvim` plus the seven
> `usr/lib/nvim/parser/*.so` (c, lua, markdown, markdown_inline, query, vim, vimdoc) — depth 3, the
> configured maximum.

Measured, from the committed receipts:

```
$ jq -r '[.normalized_result.files[].analysis_depth|select(.!=null)]|max' K3/after.json   -> 2
$ jq -r '.normalized_result.files[].analysis_depth' K3/after.json | sort | uniq -c
   2131 1
      8 2
      8 (null)
$ jq -r '.raw_result.report[] | (.task.depth // "null")' K3/after.json | sort | uniq -c
      1 0
   2249 1
     16 2
```

`parameters.max_depth` is 3 and `depth_limited_paths` is `[]` in all eight receipts (entry `:80-81`), so
nothing reached a limit. My fresh K3 run reproduces the same histogram and my fresh K4 run the same maximum (2). The wave-1 seat
already measured it: `w1/R36ExecReproK3.md:112` "8 × `…/carved.elf` (depth 2, whole-file chunks)".

Two defects in one clause: the field value is wrong (2, not 3), and "the configured maximum" invites the
reader to conclude the recursion was depth-bounded at the deepest published artifact — the opposite of
what `depth_limited_paths: []` records. It also sits twenty-four lines below the entry's own "empty in all of
them".

**Correction:** "… — `analysis_depth 2`, the receipt's maximum; `max_depth` 3 was not reached and no path was depth-limited (`depth_limited_paths: []`)."

### F3 (S2) — `verified-at` quotes `carriers_matched 4` from a receipt whose verdict at that revision was `met_target: false`, and never names the revision where it passed

Entry `:4`:

> verified-at: 2026-10-26; receipts committed at `3310d8fa…` against the predicate/carrier/oracle freeze `790561d4…`; the frozen counter reports `carriers_matched 4` at that revision

The only counter receipt at `3310d8fa` is `.ufo/waves/round-36/interim/c1-after-receipts-only.json`:

```json
{"revision":"3310d8fa27bfaa95ad858c4aaad6f6377f853982","freeze":"790561d4…",
 "carriers_matched":4,"met_target":false,
 "bindings":{"coverage_map_row":false,"entry_present":false,"entry_source_ids":[],
             "opened_source_rows":[],"province_core_row":false,"province_core_section":false,"sourced":false}}
```

The claim is actually green one commit later — `.ufo/waves/round-36/after/c1-at-ffc81341.json`
(`revision ffc81341…`, `met_target: true`, all bindings true) — and the entry never names `ffc81341`,
`01a44dbf`, or any receipt path. As written, a reader takes "verified-at … at that revision" as "the claim
passed at `3310d8fa`", which is false, and cannot find the receipt that shows it passed anywhere.

Criteria: #34 ("a receipt that expected a red result … is not a pass"), #21 (a comparator verdict is never
the compared object), #52 (a cited gate result must be backed by the committed receipt that shows it).

**Correction:** "… the frozen counter reports `carriers_matched 4` at `3310d8fa` with `met_target false` (bindings not yet landed; `.ufo/waves/round-36/interim/c1-after-receipts-only.json`) and `met_target true` at `ffc81341` (`.ufo/waves/round-36/after/c1-at-ffc81341.json`)." No committed counter receipt names `01a44dbf`, so the entry should cite the two revisions it has receipts for rather than a bare "that revision".

### F4 (S2) — "Carrier authenticity is separate and does hold" contradicts the entry's own not-claimed list

Entry `:170-171` says carrier authenticity "does hold"; entry `:190-191` says there is "no
security/authenticity claim about sasquatch or the neovim assets beyond digest equality". Both cannot
stand. Substantively, digest equality with a digest published by the same host that serves the asset is
transport/identity consistency: a compromised release satisfies both sides. The checked fact is "the
downloaded bytes equal the vendor-published digests (S109)" — which I reproduced — not authenticity.

**Correction:** replace "Carrier authenticity is separate and does hold:" with "Carrier identity is separate and does hold *to digest equality*:" and leave the `:190` bullet untouched.

### F5 (S2) — "Nothing was executed" is falsified by the entry's own citation later in the same section

Entry `:186-187`:

> **No behaviour of the extracted programs.** Nothing was executed; the 2130 members are hashed bytes.
> Running an AppImage runtime or its payload is a separate, code-executing act.

Entry `:166-168` cites `w1/R36ExecAppImageExtract.md`, whose §2 is a literal execution of K3's runtime:

```
$ ../nvim-linux-x86_64.appimage --appimage-extract        # exit 0
$ ./nvim-linux-x86_64.appimage --appimage-version
```

and §4 re-runs it under `strace`. A reader may quote "Nothing was executed" as a round-level no-execution
claim and be contradicted by the seat report the same entry relies on. (The narrow true statement — no
*published member* was executed — is what the bullet's first clause means.)

**Correction:** "No extracted member was executed; K3's AppImage runtime was executed by the wave-1 seat to obtain the second oracle (`w1/R36ExecAppImageExtract.md` §2)."

### F6 (S3) — the oracle-limits paragraph promotes K3's runtime to a "code-separate oracle" without the residual the cited report states

Entry `:166-168` calls the runtime oracle "code-separate" and reports 2130/2130, 0 digest and 0 size
mismatches — accurate — but omits the one limit the cited report names:
`w1/R36ExecAppImageExtract.md` §7, "Residual shared dependency: both implementations decompress the same
zstd blocks … A decoder defect common to both zstd versions could in principle make the two agree on
wrong bytes. Narrow, but it is the one axis where 'independent' is not absolute". The entry's own
K3-vs-sasquatch sentence keeps a comparable caveat ("one code family"); the K3-vs-runtime sentence drops it,
so a reader over-reads K3 as fully corroborated. Payloads are zstd (`compression 6`), so the shared axis is
live on these carriers.

**Correction:** append "… and both decode the same zstd blocks — a decoder defect common to the runtime's embedded libzstd and the host's would make them agree on wrong bytes (that report's §7)."

### F7 (S3) — "14 rows share their bytes with another row" miscounts; 16 rows do

Entry `:34-36`. Counted on `K3/oracle.tsv` (identical on K4):

```
$ cut -f2 K3/oracle.tsv | sort | uniq -c | awk '$1>1{print $1, $2}'
3  7e324306b8898c97f934dc4e7a74ad8c4f8a2d8638ac9307aaf378868a3de469
13 f0ef4411f89506425f962e70b4125724d6093bc7121caeab365e678dcc9e0e78
$ cut -f2 K3/oracle.tsv | sort | uniq -c | awk '$1>1{s+=$1} END{print s}'
16
```

Groups: 13 × `usr/share/nvim/runtime/ftplugin/*.lua` (110 B) and 3 × `…/ftplugin/*.vim` (383 B). 14 is the
*excess* over the 2116 distinct values, not the number of rows that share. Wave-1 already stated the
correct shape (`w1/R36CriticC1Shortcut.md` F10: "2 duplicate-sha groups (13 and 3 rows, all distinct
paths)"), and the conclusion ("all 2130 rows are counted individually") survives.

**Correction:** "2130 rows over 2116 distinct sha256 values — two duplicate groups (13 × 110-byte `ftplugin/*.lua`, 3 × 383-byte `ftplugin/*.vim`), i.e. 16 sharing rows / 14 beyond the distinct count — and the frozen predicate matches per oracle row …".

### F8 (S3) — the "engine `executable_sha256`" is the digest of a 327-byte uv console-script shim, not of the unblob engine

Entry `:18-19` gives `0ce7b624…1d09` as part of the "Measured configuration". That value is REA's
`normalized_result.engine.executable_sha256`, a faithful field echo — but the file it hashes is:

```
$ ls -l ~/.local/bin/unblob
lrwxrwxrwx … /home/vgpnk/.local/bin/unblob -> /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob
-rwxr-xr-x 327 … /home/vgpnk/.local/share/uv/tools/unblob/bin/unblob      # 9 lines: `from unblob.cli import main`
sha256sum … -> 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09      (both paths)
```

A reader who cites `0ce7b624…` as "the unblob 26.6.4 engine pin" pins a launcher that imports whatever
`unblob` is importable; the handler bytes the entry's S108 argument rests on are a different file
(`2d7b901b…599287`, present and equal at the installed path). `unblob --version` → `26.6.4`.

**Correction:** "unblob 26.6.4 (engine `executable_sha256 0ce7b624…` = the 327-byte uv console-script launcher, not the engine package; the handler file this entry cites is `2d7b901b…599287`)".

### F9 (S3) — the recheck works, but it is a one-carrier count smoke test with unstated prerequisites, no revision, and an evidence id that cannot match

I ran the documented line (only `S` moved into my scratch, `HYAKU_SCRATCH=$S`):

```
$ S=<scratch>/recheck; tools/round-36/c1-run.sh after corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh "$S"
real 1.764s   exit 0
$ jq -c '.normalized_result|{files:(.files|length),gaps:(.extraction_gaps|length)}' "$S/after.json"
{"files":3,"gaps":0}
```

So the stated output reproduces. Four things a reader can act on wrongly:

1. **No revision.** The lane's counter-based `recheck:` lines (`corpus/knowledge/2026-10-2{2,3}-r2{9,30,31}*.md`, `…-r34-elf-version-needs.md`) name `--rev <REV>` and recheck with the round counter; the two that do not run a counter (r33 source pins, r34b `on-release`) re-open a source, not a claim. This one runs HEAD's harness against HEAD's fixture, so a later edit to `tools/round-36/c1-run.sh` silently changes what the recheck means. QUALITY #18 requires the recheck to retain or name the measured revision.
2. **Hidden prerequisites.** `c1-run.sh:74` exits 2 when `sasquatch` is not on `PATH`; `c1-run.sh:79` defaults `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`. Both are true on this host and both are unstated in the header.
3. **Cannot reach the claim.** It checks `files`/`extraction_gaps` counts on K1 only: not the four carriers, not the member digests, not `before`, not the evidence ids, not the PROVINCE/SOURCES bindings. `{"files":3,"gaps":0}` is also what a wrong-member publication with the right count would print.
4. **The id differs, and rightly.** My run's envelope is `ev_7522aaff4b17fb4caa45485aa32360459fdc4b226b4d3d54a6b55e3032c3a068`; the stored K1 after id is `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860`. `parameters.path`/`output_directory` are inside the id domain, so a recheck at another path cannot reproduce the stored id. The entry says nothing, and a reader comparing ids will read the mismatch as a defect.

**Correction:** keep the harness line but label it a live smoke test with its two prerequisites and the id caveat, and add as *the* recheck: `python3 -I -B tools/round-36/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --freeze 790561d4… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (exit 0 iff `carriers_matched == 4` and every binding true).

### F10 (S3) — `root_file_range` is printed as an unnamed pair, and the K3 row reads as `{start, end}` while it is `{offset, length}`

Entry `:50` tabulates `K3 {944632, 10510336}`, `K4 {936456, 10420224}`. The receipt keys are
`{"offset": …, "length": …}` (`K*/before.json`), and the payload chunk the same entry names two sections
later is `944632-11454968.squashfs_v4_le` — 944632 + 10510336 = 11454968. A reader who takes the row as
`{start, end}` gets length 9,565,704 instead of 10,510,336 and contradicts the entry's own chunk filename.

**Correction:** print `{offset: 944632, length: 10510336}` (or `… end 11454968`) for all four rows.

### F11 (S4) — the section heading overclaims its own bullet: one of the 17 "second-level" extras is first-level and present in `before`

Entry `:97` heading "The 17 extras per AppImage are second-level recursion output" vs `:103` "This one is
*also* published in the `before` run; it is a member's peer, not recursion output." The runtime carve is
first-level recursion output (it exists before sasquatch is installed; `analysis_depth 1`), so the heading
is wrong for 1 of 17 and "not recursion output" is the wrong phrase for it. Counts are unaffected (both
carriers: 1 + 8 + 8).

**Correction:** heading "…: 16 second-level extras plus the first-level runtime carve"; bullet "… this one is the first-level ELF carve of the carrier's runtime, already published in the `before` run, not second-level output."

### F12 (S3) — the Receipts paragraph offers an id re-hash as the only support, and does not point at the provenance that exists

Entry `:213-215`: "The frozen counter re-derives each stored id under the rea-agents 6.5.0 rule and reports
`before_evidence_id_ok` and `after_evidence_id_ok` true for all four carriers." True (I re-read
`c1-at-ffc81341.json`), but per **QUALITY #78** an id recompute is not provenance — a fabricated envelope
re-hashed with the same rule passes (`M36-4`, wave-1 `R36CriticC1Shortcut.md` F1). The provenance the round
does hold — four independent seat reproductions, `w1/R36ExecReproK{1,2,3,4}.md` — is not cited by the entry,
and the entry names neither the receipt file nor a command for the id keys, so a reader can only re-hash.

**Correction:** add "provenance of these receipts is the four non-author reproductions `w1/R36ExecReproK{1,2,3,4}.md` (published `(relative_path, sha256)` set and gap kinds compared); the id recompute above is integrity, not provenance."

### F13 (S4) — "the published regular files lose executable permission bits" is stated from the tool's instruction, unmeasured; measured it is stronger (mode normalised to 0600)

Entry `:127-128` (the continuation sentence it derives from is quoted at `:123`). The sentence is a claim about produced artifacts, sourced from the continuation text, and
no receipt records modes. I measured it on a fresh K3 extraction:

```
published: usr/bin/nvim 0600, AppRun 0600, usr/lib/nvim/parser/c.so 0600, runtime carved.elf 0600
in image:  AppRun 0755, usr/bin/nvim 0755, usr/lib/nvim/parser/c.so 0644        (unsquashfs -ll)
```

So the claim holds, but "lose executable bits" understates it (read bits go too) and the entry does not say
it is tool-stated rather than measured.

**Correction:** "the published regular files are mode `0600` — every mode bit but owner read/write is dropped (measured on a fresh K3 extraction; image modes 0755/0644) — and the frozen oracle does not compare modes anyway ([INFERENCE from `extraction_continuations[].instruction]` for the producer's intent)."

### F14 (S4) — two unlabelled inferences (QUALITY #5)

1. Entry `:164-165` "(it is a patched squashfs-tools 4.5.1)". S107 does not say this and S108 is the handler;
   the only lane source that describes sasquatch as a patch set over `unsquashfs` is S111, which this entry
   does not cite. It is a reasonable inference from the `-version` line, but it is the load-bearing half of
   the "one code family" argument for K3/K4 and carries no label.
2. Entry `:146-147` "The missing-dependency gap and its continuation are therefore unblob's designed
   behaviour". The *gap kind* is unblob's; the continuation sentence ("REA installs nothing. …") is REA's own
   envelope wording, which the entry's own Sources table says S108 does **not** ground ("not REA's gap
   wording"). Two producer layers are merged into one attribution.

**Correction:** tag (1) `[INFERENCE]`, and split (2): "the gap kind is unblob's designed dependency behaviour (S108); the continuation sentence is REA's wording (observed in the receipt, not grounded by S108)."

### F15 (S4) — no carrier is named by absolute path (QUALITY #4)

The carrier table gives repo-relative fixture paths and sha256 for K1/K2, and sha256 only for K3/K4 (their
release URL appears in the `source: S109` line, not in the table; `carriers.json` has both). The REA receipts' `subject.local_path` points at
`/fast/scratch/hyaku/kaidoku-r36/L1/carriers/…`, which no longer exists. Identity is stable (digest), but a
reader cannot walk from the entry to the bytes by path alone.

**Correction:** give the two absolute fixture paths under the lane root and the two release URLs.

## 3. Scope-word audit (`every` / `all` / `each` / `nothing`)

| entry site | statement | verdict |
|---|---|---|
| `:40-41` "removes every PATH directory holding an executable named `sasquatch`" | harness filter | true, and worth one extra clause: it is directory-level, so `sasquatch-v4be` (same directory) is removed too (`w1/R36ExecReproK4.md` §7.4). Harmless for LE carriers; the archive stays clean |
| `:41` "In all four carriers unblob emits exactly one extraction gap" | before arm | true |
| `:51` "identical in all four" | continuation id | true |
| `:58` "`coverage` is `partial` in all four" | before arm | true |
| `:80-81` "`max_depth` is 3 in all eight … `depth_limited_paths` is empty in all of them" | eight receipts | true |
| `:110` "No oracle row is left unmatched" | after arm | true (my fresh runs: 2130/2130 twice) |
| `:110-111` "no extra is a member of the squashfs image" | extras | true (10 distinct extra digests, none in the oracle) |
| `:140-141` "every `K*/after-run.json` records …; every `K*/before-run.json` records `sasquatch: ""`" | run metadata | true |
| `:186` "Nothing was executed" | round scope | **false** — F5 |
| `:190-191` "no security/authenticity claim … beyond digest equality" | — | true, but contradicted at `:170` — F4 |
| `:214` "true for all four carriers" | id keys | true, but not provenance — F12 |

## 4. Where I found nothing

- No disagreement with any tabulated count, digest, offset, byte sum, gap field, continuation id, or
  instruction quote; no missing or extra oracle row in either after receipt; no divergence between the two
  fresh runs and the committed ones on any field the entry states, except F2's depth.
- The 7z, big-endian/AVM, vendor-mangled, other-verb and 6.7.0 disclaimers are correctly scoped and I found
  no carrier in the set that exercises them in the receipts.
- The `PROVINCE.md:156-157` and `corpus/README.md:44` quotes the entry reproduces for its "novelty" section are
  word-for-word present at the tip. Note (not a defect): the same landing added `corpus/README.md:89`, which
  annotates the Firmware row as history — the entry does not mention that annotation, but it does not
  contradict the entry's past-tense "the lane recorded" either.
- Source binding (S107/S108/S109 mined, opened 2026-10-26, used-by naming the entry) is true at `ffc81341`
  per `c1-at-ffc81341.json` `bindings.opened_source_rows`; I did not re-open the upstream pages this seat
  (wave-2 `R36W2ScoutS107/108/109` own that).
- I did not re-download the deb (relied on wave-2 `R36W2ScoutS107` and the installed-binary digests, which
  match S107's member digests). K2's after receipt was read, not re-run.

## 5. Tooling and hygiene

No tool installed or upgraded (no pacman, no `uv`, no release binary). Used as found: `npx -y
rea-agents@6.5.0` (the cached package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`, `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`),
`curl 8.x` (two 11 MB carrier downloads into scratch), `/usr/bin/unsquashfs` 4.7.5 (present; used for `-ll`
and `-s` only — the frozen oracle tables were not regenerated), `jq`, `python3 -I`, `sha256sum`, `stat`.
My own scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2CriticEntryC1` (carriers, two fresh REA output trees,
one harness recheck) was removed before yield; no `find`/`du` under `/fast/scratch`; nothing written outside
this report; no `git` write operation.
