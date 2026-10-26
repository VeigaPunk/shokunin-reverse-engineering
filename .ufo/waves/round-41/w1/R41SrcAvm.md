# R41SrcAvm — AVM V3/V4 vendor identity: directory opening and SOURCES rows S127/S128

**DONE** — both AVM download directories opened live on 2026-10-26 (HTTP 200, double-fetched, digests
stable), and the two missing identity rows are drafted paste-ready as `S127` (5490 / draft V3) and `S128`
(5491 / draft V4), 11 columns, mined, `2026-10-26`, `180d`, used-by
`corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`; row lint and its six-mutation selftest pass.

Seat `R41SrcAvm`, leaf, base `49096c7e6f226af0c750c4b003be58883cb6049f`. Nothing committed, no VCS
mutation, no vendor bytes in the lane, no extractor run on any reserved carrier.

## 1. Deliverable

| what | where |
|---|---|
| paste-ready rows (2 lines, 11 columns, 12 pipes each) | `.ufo/waves/round-41/w1/artifacts/R41SrcAvm/sources-rows.txt` |
| same rows + paste instruction, calibration and non-claims | `…/artifacts/R41SrcAvm/sources-rows-draft.md` |
| row lint (round-35 `ROW_RE` semantics, `--selftest`) | `…/artifacts/R41SrcAvm/check-rows.py` |
| every HTTP fact quoted in the rows | `…/artifacts/R41SrcAvm/avm-http-probe.tsv` |
| every quoted vendor line, with line numbers | `…/artifacts/R41SrcAvm/quote-excerpts.txt` (generator `excerpt.py`) |
| vendor row vs base round-40 record vs round-41 peer artifacts | `…/artifacts/R41SrcAvm/identity-crosscheck.tsv` |
| raw listing captures (574/574/420/420 B, vendor index pages only) | `…/artifacts/R41SrcAvm/avm-{5490,5491}-listing.html`, `avm-{5490,5491}-other-listing.html` |
| artifact digests | `…/artifacts/R41SrcAvm/SHA256SUMS` |

Lint result (exit 0):

```
base 49096c7e6f226af0c750c4b003be58883cb6049f: 126 registry rows, max id S126
row S127: 11 cells, 2111 chars, pipes 12
row S128: 11 cells, 2086 chars, pipes 12
PASS: ids ['S127', 'S128'] parse as 11 columns, novel against the base, mined, 2026-10-26, 180d, used-by corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md
```

`--selftest` (exit 0) re-parses a green copy and then rejects six mutants, so the lint is not vacuous:
pipe injected into a cell, id changed to the base's `S126`, located quote grown to 26 words, status flipped
to `rejected`, used-by repointed, recheck written as `on-release`.

## 2. Observed facts (opened 2026-10-26; every info file and both `fritz.os` listings fetched twice)

| field | 5490 (V3) | 5491 (V4) |
|---|---|---|
| directory listing | `https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/` GET 200, 574 B, sha256 `88c8d6485e1400cc77d8881bec189d065a045f5fe8ee285528eafaab8c4a19f4`, server Date 2026-10-26T20:21:37Z | `…-5491/…` GET 200, 574 B, sha256 `badbb744ff9d916fb52b4e89d6bd613009fc1b5891f115fa93b74c73583af6f7`, Date 2026-10-26T20:21:38Z |
| listing entries | `FRITZ.Box_5490-07.31.image` 04-Sep-2023 08:17 33269760; `info_de.txt` 18-Nov-2024 14:01 56125; `info_en.txt` 18-Nov-2024 14:01 50653 | `FRITZ.Box_5491-07.31.image` 04-Sep-2023 09:53 36392960; `info_de.txt` 47098; `info_en.txt` 53166 |
| `other/` parent | 200, 420 B: `fritz.os/`, `recover/` only | 200, 420 B: `fritz.os/`, `recover/` only |
| `info_en.txt` | 200, 50653 B, sha256 `e3100cdaeae9d72c8f8637119e492677ef074c468394e6d52a21fe73b7360d18`, Last-Modified 2024-11-18 14:01:57 GMT, ETag `"673b48d5-c5dd"`, fetched 2026-10-26T20:21:50–51Z | 200, 53166 B, sha256 `ec2528eb91f16d35c9245c8f7c276a57edd7fb58344a649fa1add451051970b4`, Last-Modified 2024-11-18 14:01:04 GMT, ETag `"673b48a0-cfae"`, fetched 20:21:52–53Z |
| `info_de.txt` | 200, 56125 B, sha256 `519e5038d4e28935f6c356333d0d48062e770125b11f2092600486b6b174a5c9` | 200, 47098 B, sha256 `dc663791cbb0499e69d0be097a844ed105772c2c7ad8e33d6e9b8397292c745e` |
| image **HEAD only** | 200, Content-Length 33269760, ETag `"64f592ae-1fba800"`, Last-Modified 2023-09-04 08:17:50 GMT | 200, Content-Length 36392960, ETag `"64f5a91e-22b5000"`, Last-Modified 2023-09-04 09:53:34 GMT |
| identity block, `info_en.txt` L8/L10/L12/L14 | `Product: FRITZ!Box 5490` / `Version: FRITZ!OS 7.31` / `Release date: 09/04/2023` | `Product: FRITZ!Box 5491` / `Version: FRITZ!OS 7.31` / same date |
| identity block, `info_de.txt` L8/L10/L14 | `Produkt: FRITZ!Box 5490` / `Version: FRITZ!OS 7.31` / `Release-Datum: 04.09.2023` | `Produkt: FRITZ!Box 5491` / `Version: FRITZ!OS 7.31` / `04.09.2023` |
| tail signature | `info_en.txt` L672 `DHA 2023/09/04`; `info_de.txt` L741 `DHA 2023/09/04` | `info_en.txt` L695 `HKR 2021/11/17`; `info_de.txt` L584 `HKR 2021/11/17.` |

Stability: `curl -H "If-None-Match: <etag>"` and `-H "If-Modified-Since: <last-modified>"` both returned
**304** for both `info_en.txt` files at 2026-10-26T20:22:28Z (5490) and 20:22:31Z (5491); the consolidated
probe re-fetched every info file a second time at 20:23:34–20:23:46Z and the sha256 pairs are identical.
Both `fritz.os` listings are byte-identical across the two fetches (same digests as above).

## 3. Exact commands (scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41SrcAvm`, `cd "$S"`)

```
curl -sS -D 5490-listing.headers -o 5490-listing.html -w 'http_code=%{http_code} size=%{size_download}\n' \
  https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/            # 200 574   (5491 same: 200 574)
curl -sS -D "$m-info_en.txt.headers" -o "$m-info_en.txt" -w 'http_code=%{http_code} size=%{size_download}\n' \
  "https://download.avm.de/fritzbox/fritzbox-$m/other/fritz.os/info_en.txt" # 200 50653 / 200 53166
curl -sS -o /dev/null -w 'http_code=%{http_code}\n' -H "If-None-Match: $etag" <info_en url>   # 304 304
curl -sS -I -w 'http_code=%{http_code}\n' <…/FRITZ.Box_$m-07.31.image>       # 200, metadata only, body not fetched
python3 excerpt.py <file> <lines…>        # quote-excerpts.txt
python3 check-rows.py --selftest          # exit 0
python3 check-rows.py                     # exit 0
```

Reads (no writes): `git -C <lane> show 49096c7…:corpus/SOURCES.md` (header, S124–S126, `## Paths`,
`## Search log`), `git grep -n -I -E 'fritzbox-5490|fritzbox-5491|Box_5490|Box_5491' 49096c7… -- .`,
`tools/round-35/c1-coverage-counter.py` (row regex), and the peer artifacts named in F7/F9.

## 4. Findings

**F1 — the identity chain closes four ways for both models** (listing, image HEAD, `info_en.txt`, `info_de.txt`;
5490 adds a fifth, its matching tail signature — 5491's tail diverges, F4). Listing size and mtime equal HTTP
`Content-Length` and `Last-Modified`; the ETag's two hex halves decode to exactly those values (the
`mtime-size` server convention is [INFERENCE]; the arithmetic is checked)
(`64f592ae`→2023-09-04T08:17:50Z with `1fba800`→33269760; `64f5a91e`→09:53:34Z with `22b5000`→36392960);
`info_en.txt` L8/L10/L14 agrees on product and version; `info_de.txt` L14 gives the same date in the other
format; the tail signature of 5490's file agrees. Both images therefore can be cited as
`FRITZ!Box 54xx, FRITZ!OS 07.31`, released 2023-09-04, from published bytes only.

**F2 — the release date is month/day in `info_en.txt`, and it is a real misread trap.** En `09/04/2023`
is 4 September, not 9 April: `info_de.txt` L14 `04.09.2023`, the image `Last-Modified` 2023-09-04 and 5490's
tail signature `DHA 2023/09/04` all settle it. Any freeze text that renders the en line as "9 April" is wrong
by five months; the rows state the ISO date in `teaches`.

**F3 — both info files are single-byte, CRLF, not UTF-8, and the licence line has no en dash.**
All high bytes in the four files are in 0xa0–0xff (`5490 en`: 0xa0×4, 0xa9, 0xe4, 0xe9, 0xfa; `5490 de`: 778
accented bytes, `5491 de`: 655) — no cp1252-only byte is present, so ISO-8859-1 decodes them. A strict UTF-8 read fails at
`5490 en` offset 17974 (line 233, `Telegärtner`) and at `5490 de` offset 44 (line 1). Line endings are CRLF
throughout (671/740/694/583 CRLF pairs). The copyright line is literally `© AVM GmbH 2004?2021. All rights
reserved.` in the en files (0x3f question mark, no dash) while the de files read `© AVM GmbH 2004 - 2021`;
the round-41 V3 artifact renders it `2004-2021`. Quote the vendor byte, not the reconstruction.

**F4 — 5491's trailing signature contradicts its own release date; 5490's does not.** `5491 info_en.txt` L695
`HKR 2021/11/17` and `5491 info_de.txt` L584 `HKR 2021/11/17.` are two years before the 2023-09-04 release
claimed at L14 and proven by `Last-Modified`. The file is internally non-uniform (a 2021 notes base with
2023 body text appended), so V4 must be dated from L14 + `Last-Modified`, never from the tail. Rows for the
two models deliberately differ in `teaches` for this reason.

**F5 — neither info file carries a Build number.** Case-insensitive `build` over both `info_en.txt` files:
zero hits. So `Build=` for V3/V4 can only come from inside the image (`var/content`, `var/version`); the
round-41 V3 peer already records `Version=07.31; Build=107857` and `FIRMWAREVERSION=151.07.31,,107857,`.
The rows scope this out explicitly rather than implying published build identity.

**F6 — the filename↔version binding is the directory listing's job, not `info_en.txt`'s.** `info_en.txt` L1
names only the template `FRITZ.Box_5490-xx.xx.image`; `5490 info_de.txt` L1 drops even the extension
(`FRITZ.Box_5490-xx.xx`) while `5491 info_de.txt` L1 keeps `.image`. The `fritz.os` directory holds exactly
one image per model, and `other/` holds only `fritz.os/` and `recover/`, so the single published `fritz.os`
image for each model is the `07.31` file named in the listing.

**F7 — the V3/V4 *bytes* are not new to the lane; the *extractor* is.** Base-committed
`.ufo/waves/round-40/w1/artifacts/R40C1VendorScout/candidates.tsv` lines 16–17 already carry both images
(5490: 33269760 B, sha256 `770efb4e368a…45ab7`, member `./var/tmp/filesystem.image` 30236680 B sha256
`87cc5d6b…a0f8`, inodes 104, `mkfs_time = bytes_used = 30233394`, marker YES; 5491: 36392960 B sha256
`a5a3a763…35f661`, member 33361928 B sha256 `4cfc3016…d92f6c`, inodes 104, `mkfs_time = bytes_used =
33358398`, marker YES), and `R40C1VendorScout.md` §Method states the only
external programs used were `curl`, `tar`, `sha256sum` and `python3`, with the one `sasquatch-v4be` listing
run reported on the 3490 wrapper, not on 5490/5491. The draft's phrasing "none of which any REA or unblob
run touched" therefore survives, but "bytes never fetched / never parsed before the freeze" would be false
and any freeze sentence must keep the REA/unblob qualifier. Sizes in the vendor listing equal the round-40
`bytes` column exactly, which is the cross-check that the 2026-10-26 download URL is the same object.

**F8 — round-40's w1 prose and the frozen carrier table disagree about V2.** `R40C1VendorScout.md:39`
picks `V2 = FRITZ.Box_7430-07.31.image`, while the frozen `.ufo/waves/round-40/c1/carriers.json:28` records
V2 as `FRITZ.Box_6820v1_LTE-07.30.image`. A round-41 seat that rebuilds development V1/V2 from the w1
report instead of the frozen table will fetch the wrong image. (Neither is a round-41 carrier; both are
development inputs.) Same file line 1 says "V2 = FRITZ.Box 7430", so the prose repeats the stale pick.

**F9 — V4's fetch chain is not yet recorded where the freeze will look.** `.ufo/waves/round-41/w1/artifacts/`
held `R41C1VendorV3/{fetch-5490.json, provenance.json}` (image sha256 `770efb4e…`, member sha256
`87cc5d6b…`, carrier slice sha256 `c4f74f54…`, all equal to the base record) but `R41C1VendorV4/` held only
`chain-walk.json`, `chain-walk.py`, `nonregular.tsv`, `oracle-check.tsv`, `oracle-run.json`, `oracle.tsv`,
`r41-oracle-run.sh` — no image/member/carrier sha256 or `info_en.txt` digest. Under the draft predicate the
vendor carriers need "fetch chain checks image sha256 → member sha256 (R40-CL6) → carrier sha256", so V4
needs that artifact before the freeze, or the claim has to name where it lives. I could not message the V4
seat (`R41C1VendorV4` is no longer on the roster); my identity numbers for 5491 (§2) are available for its
chain to cite or refute.

**F10 — licence bounds the rows, and they are written to that bound.** `info_en.txt` L665–670 (5491:
L688–693) restrict redistribution, grant backup-copy use only, and forbid "processed, disassembled, reverse
engineered … 'opened'" copies; 5490 L672 / 5491 L695 are the vendor's own release signatures. Hence: no
vendor bytes in the lane, `HEAD` only on the images, identity-only scope in both rows, and only the vendor's
own 574 B index pages retained as captures (no firmware content).

## 5. What the sources rows do and do not buy the freeze

- They give the C1 predicate a citable tier-A identity for V3/V4 that does not require holding vendor bytes:
  product, version, date, the single published image name, its size and mtime, with stable digests.
- They do **not** establish any SquashFS fact: endianness, superblock fields, the `mkfs_time == bytes_used`
  marker, inode counts, the member name, `filesystem_core.squashfs`, or the oracle. All of that stays with
  the V3/V4 seats' receipts (the base `candidates.tsv` numbers agree with the probe, but naming them in a
  SOURCES row would be exactly the "source docs are not held capability" mistake this lane scores against).
- Used-by is the entry the draft predicate requires. `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`
  does not exist at base or in the worktree at the time of writing (`test -f` → no), and the entry seat owns
  it. If the entry is renamed, both rows' used-by must be updated in the same landing commit — a c1 counter
  that checks "exists at REV and one row in `SOURCES.md` cites it as used-by" (round-35 style) will fail on a
  typo, and the L1, not me, owns that edit.
- `recheck 180d` is a deliberate deviation from S125's `on-release`, because this item allows only an ISO date
  or `NNd` and this is a static archive (fritz.os body unchanged since 2023-09-04, listing last touched
  2024-11-18, both proven by 304s). A vendor re-release moves the ETag recorded in the anchor.

## 6. Gates, limits, bounds

- **Not done, on purpose:** no `.image` body fetched (HEAD only), no REA, no unblob, no sasquatch, no
  extractor, no carve, nothing read from any reserved carrier beyond the vendor's own index pages and info
  files; no writes to `corpus/`, `tools/`, `plans/`, `PROVENANCE`, `SKILL.md`, `LOG.md`, or anywhere outside
  `.ufo/waves/round-41/w1/R41SrcAvm.md` and `.ufo/waves/round-41/w1/artifacts/R41SrcAvm/`.
- **VCS:** no mutation. Only `git show`, `git grep`, `git log`, `git status --porcelain`, `git diff --stat`
  (read-only). The worktree `corpus/SOURCES.md` equals base (empty diff), so my rows collide with nobody and
  `S127`/`S128` are the next free ids after `S126` (base has 126 registry rows).
- **Tooling:** nothing installed, nothing upgraded, nothing written into any PATH directory. `curl`,
  `python3`, `sha256sum`, `git`, `column` only.
- **Scratch:** `S=/fast/scratch/hyaku/kaidoku-r41/R41SrcAvm` used for all fetches and for lint runs; it is
  removed before yield, so every fetch is reproduced by the commands in §3 and pinned by the digests in §2.
- **Inference markers:** the claim that the 5490/5491 `fritz.os` directories publish no other version is
  bounded to what those two listings show this round (no web-wide negative). Reading `5491 L695` as a stale
  notes signature rather than a second release date is [INFERENCE] from the mismatch with L14 and
  `Last-Modified`; the located bytes are as quoted.
- **Peer claims I did not re-derive:** V3 `Build=107857`, `var/content`, the carrier slice `c4f74f54…`, and
  V4's `chain-walk.json`/`oracle-run.json` contents are quoted as their readers' artifacts, not as my
  observations; the image/member sha256 I did cross-check (F7, F9) are committed at base.

## 7. Handoff for the L1 (freeze)

1. Paste `sources-rows.txt` after `S126`; run `check-rows.py` after pasting (it re-reads the base itself and
   will catch an id clash with a sibling's landing).
2. Land the entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` with `source: S127 … / S128 …`
   so both used-by cells resolve, or rename used-by in the same commit.
3. Carry F7 (REA/unblob qualifier) and F8 (V2 prose vs frozen table) into the freeze text; act on F9 (V4
   fetch chain artifact) before any V4 receipt is scored.
4. Optional lane-convention bullet for `## Search log` (my seat may not write it):

   > 2026-10-26 round 41 — Question: what do AVM's own pages publish for the V3 (FRITZ!Box 5490) and V4
   > (FRITZ!Box 5491) carrier images, and is their identity citable without holding vendor bytes? Where:
   > the two `download.avm.de/fritzbox/fritzbox-549{0,1}/other/fritz.os/` listings, their `info_en.txt` /
   > `info_de.txt`, and `HEAD` on both `.image` files (`curl` only; no body fetched, no extractor run).
   > Identified 2 source families, screened 4 files + 2 listings, included 2 rows (S127, S128), excluded 0.
   > Capture digests, ETags, 304 results and the Latin-1/CRLF finding are in
   > `.ufo/waves/round-41/w1/artifacts/R41SrcAvm/`. Stop: product/version/date and the single-image binding
   > are grounded; layout, superblock and build identity belong to the carrier seats.
