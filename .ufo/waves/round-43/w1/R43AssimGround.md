# R43AssimGround — assimilation re-grounding of the ONE admitted entry (`sasquatch-prebuilt-package-inventory`)

**Verdict: CONFIRMED — ADMIT.** The entry's flip does not fire: the API still shows **8 releases**
(no ninth; `?page=2` → 0 items, the tags endpoint carries no new `sasquatch-v*` release tag), the
**asset set is byte-identical to the round-42 receipt** (every release-level and asset-level field
equal except `download_count` on 7 assets), and **no release body states a package/upstream version
pair** (0 of 8 bodies contain a standalone `1.0` token). The id-collision guard is proven on an
indented fixture, the scratch mirror-lane census **exits 0**, and the two normalized rows are
delivered below. One **calibration defect** in the sibling scribe seat's draft is reported (§7): its
"the response grew by 19 613 B" limits sentence compares two different JSON serialisations, not two
different payloads.

Seat: `R43AssimGround` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `6b9e64fe7e0de202d9383baad5792fbfe039a743`. Axes: coverage, depth, calibration. Milestone:
round 43 wave 1 — pre-freeze build, recon, sources, attack of the draft.

Bounds: wrote only this report and `artifacts/R43AssimGround/`. No lane file was created, edited or
deleted; no VCS mutation; nothing written to `/home/vgpnk/Projects/shokuknow`; no REA, unblob or
sasquatch run on any image; no firmware image fetched, carved or copied. Scratch
`/fast/scratch/hyaku/kaidoku-r43/w1-R43AssimGround` removed at the end; every path cited below lives
in the artifacts dir. **No tool installed or upgraded** — `curl`, `jq`, `python3`, `git`, `tar` and
`sources-census.sh` were already present (`curl 8.23.0`, `git 2.56.0`, GNU Awk 5.4.1); no pacman
transaction; no PATH-directory write.

## Axes

| axis | what this seat moved |
|---|---|
| **coverage** | the round's one admitted entry is re-grounded on bytes fetched this round, with every asset the entry names (8 releases, 44 assets, all names/sizes/digests) located; the two registry rows it needs are normalized and census-green. |
| **depth** | the flip test is decided by a byte-level field-by-field comparison against the round-42 receipt, not by an eyeball: the whole payload is unchanged except 7 mutable `download_count` counters. That also exposes a **serialisation artifact** in the sibling draft's limits paragraph (§7). |
| **calibration** | the id-collision guard is proven on an **indented** `  \| S002 \|` fixture (the round-40 caveat, closed), the mirror census is shown **able to fail** on six distinct controls, and the id assignment is reconciled with the plan's reserved S135 instead of colliding with it. |

## 1. The re-opened source (my own fetch, not the sibling's receipt)

Both cited sources were fetched by this seat. Receipts: `artifacts/R43AssimGround/receipts/fetch-receipt.txt`,
`receipts/rel-r43-assimground.json` (107 313 B),
`receipts/sasq-releases-r43-assimground.html` (349 255 B).

| source | access time (UTC) | HTTP | bytes | sha256 |
|---|---|---|---|---|
| `https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100` | 2026-10-27T08:18:09Z | 200 | 107 313 | `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0` |
| same endpoint, second fetch | no separate clock reading (sequenced between the two readings below) | 200 | 107 313 | `d15543541ba46be0fc26a59441fccbcb8257238f31fe3fb530393f7989feda72` |
| `https://github.com/onekey-sec/sasquatch/releases` | 2026-10-27T08:19:46Z | 200 | 349 255 | `150c7584282394a4c68c5b93587ac5f9ffd167badb04349d522e584045f7d3d0` |
| same page, fetch 2 | no separate clock reading (the two extra page fetches ran back-to-back in one command, later in the session) | 200 | 349 255 | `3957c55163b34c97b937e19c8d043c5ee95d0e830ac452f7c3675d9970d8f9f0` |
| same page, fetch 3 | same command as fetch 2 | 200 | 349 251 | `e5f85ce0ded2678f56039ec7034c796cea0afe3cdf06142894383a49eebc7eda` |

Only two clock readings are exact (`date -u +%FT%TZ` was run immediately before the API fetch and
immediately before the page fetch); the other three fetches carry a byte/digest receipt without a
separately observed instant, and are marked as such rather than given an inferred timestamp.

My API receipt is **byte-identical** to the sibling scribe seat's retained
`artifacts/R43ScribeAssim/receipts/rel-r43.json` (`cmp` exit 0) — two independent fetches of the
same raw response. My page bytes differ from the sibling's retained page (both 349 255 B, different
sha256), which is the page's own instability, not a disagreement.

**Every asset/name the entry cites, located** (44 assets across 8 releases):

| tag | published (UTC) | assets | amd64 | arm64 | armhf | `assets[].digest` |
|---|---|---|---|---|---|---|
| `sasquatch-v4.5.1-6` | 2026-01-27T11:57:51Z | 6 | 187 244 | 170 080 | 164 428 | 6 of 6 |
| `sasquatch-v4.5.1-5` | 2025-02-10T14:54:38Z | 6 | 187 040 | 170 556 | 164 376 | 0 of 6 |
| `sasquatch-v4.5.1-4` | 2023-06-06T19:02:28Z | 6 | 186 968 | 169 824 | 164 524 | 0 of 6 |
| `sasquatch-v4.5.1-3` | 2023-04-07T09:59:24Z | 6 | 187 024 | 169 828 | 164 452 | 0 of 6 |
| `sasquatch-v4.5.1-2` | 2023-03-09T17:43:19Z | 6 | 187 076 | 169 504 | 164 724 | 0 of 6 |
| `sasquatch-v4.5.1-1` | 2023-03-02T10:01:02Z | 6 | 187 016 | 169 360 | 164 716 | 0 of 6 |
| `sasquatch-v1.0.1` | 2022-12-03T10:18:00Z | 6 | 185 724 | 168 184 | 162 288 | 0 of 6 |
| `sasquatch-v1.0` | 2022-02-26T23:10:04Z | **2** | 185 708 | absent | absent | 0 of 2 |

`dbgsym` members on `v4.5.1-6`: 323 896 / 327 784 / 319 048 B; `v1.0`'s single `dbgsym`: 321 380 B.
The six `v4.5.1-6` digests are `efbc92bd…` (amd64), `28e57a4f…` (arm64), `29c72159…` (armhf),
`73d44ca5…`, `7891831a…`, `9d82e6d4…` (dbgsym). Every size above was re-derived here and matches
the sibling draft's table cell for cell. `sasquatch_1.0_amd64.deb`'s digest `efbc92bd…` is the value
already held by lane row **S107** — the two rows agree, which is a second-order cross-check.

## 2. The flip test — decided on bytes, not on eyeball

The round-42 ADMIT verdict (`…/round-42/w1/R42Assim.md`, `## 1`) names one flip:
*"refetch shows a ninth release / changed assets / a body stating a version pair"*. Each limb,
measured against the retained round-42 receipt
`…/round-42/w1/artifacts/R42Assim/receipts/rel.json` (87 700 B, sha256 `57a19513…499db`):

**(a) A ninth release — NO.** The payload holds 8 releases. `?per_page=100&page=2` → HTTP 200 with
**0 items**. The tags endpoint (HTTP 200, 19 tags) contains the same 8 `sasquatch-v*` release tags
and no ninth; the remaining 11 are non-release tags (`v1.0`, `squashfs-tools-v4.6.1`,
`squashfs-tools-v4.5.1`, `squashfs-tools-v4.5`, …).

**(b) Changed assets — NO.** A field-by-field comparison of every release object and every one of
the 44 asset objects, round-42 vs today, found **exactly 7 differing fields, all of them
`download_count`**:

```
sasquatch-v4.5.1-6/sasquatch-dbgsym_1.0_amd64.deb   160 -> 161
sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb      23694 -> 23773
sasquatch-v4.5.1-6/sasquatch_1.0_arm64.deb       2404 -> 2411
sasquatch-v4.5.1-5/sasquatch_1.0_amd64.deb      34473 -> 34483
sasquatch-v4.5.1-5/sasquatch_1.0_arm64.deb       2334 -> 2337
sasquatch-v4.5.1-4/sasquatch_1.0_amd64.deb      51254 -> 51262
sasquatch-v4.5.1-4/sasquatch_1.0_arm64.deb       2748 -> 2749
```

With `download_count` removed from both sides, both payloads hash to
`8246d29baabeae5e99f6a295c08e2844e539ee2e61ce4880771d87bff42032ff`. Every tag, `published_at`,
body, asset name, asset size and asset digest is **unchanged**. The arch gap at `sasquatch-v1.0` is
unchanged: that release's `assets[]` is exactly
`{sasquatch-dbgsym_1.0_amd64.deb, sasquatch_1.0_amd64.deb}` and **no** asset name contains `arm`;
`arm64`/`armhf` appear on the other 7 tags only.

**(c) A body stating a version pair — NO.** Body lengths: 645, 560, 0, 0, 0, 38, 0, 0. **0 of 8**
bodies contain a standalone `1.0` token. The only body that names an upstream version at all is
`sasquatch-v4.5.1-1`'s 38 bytes: *"Rebased on top of squashfs-tools 4.5.1"* — the upstream base
alone, with no package version beside it. `v4.5.1-6`'s 645-byte body still carries the
`unsquashfs: fix prototypes for C23` line. The round-36 Decision-2 falsification therefore still
holds on this round's bytes.

**Verdict: the flip does not fire → ADMIT.** The two round-36 falsifications are corrected, not
reversed: the arch matrix starts at `sasquatch-v1.0.1`, and `sasquatch-v1.0` is amd64-only.

**Recheck command reproduced.** The staged entry's own command, verbatim:
`curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | grep -c 'sasquatch-v4.5.1-6'`
→ `12` (2026-10-27T08:48:41Z, exit 0) — the round-42 receipt value. The stable projection
`jq -c '[length, (map(.assets|length)), (map([.assets[]|select(.digest)]|length]))]'`
→ `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]`, identical at 08:19:46Z and 08:48:41Z, exit 0 both times.

**Provenance of the "Not claimed" sentence re-checked.** `sha256sum ~/.local/bin/sasquatch` →
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (re-hashed 2026-10-27) — equal
to the round-36 lane receipt `corpus/evidence/round-36/c1/K1/after-run.json` (whose
`unsquashfs version 4.5.1 (2022/03/17)` string I also re-read at the base commit) and to the
round-42 draft's stated value. The amd64/armhf packages were not downloaded and not run; nothing
here is a redistribution statement.

## 3. Id-collision check (before any append)

Full receipt: `artifacts/R43AssimGround/receipts/id-collision.txt`; id lists retained as
`receipts/reg-ids.txt`, `receipts/staged-ids.txt`.

| | value |
|---|---|
| registry at base `6b9e64fe` (0–3-space extractor) | **134** ids, `S001..S134`, contiguous |
| staged package `merge/kaidoku/SOURCES.append.md` | **132** ids, `S106..S237` |
| `comm -12` | **29 collisions**, `S106`..`S134` |
| first free lane id | `S135` — **reserved by this round** (see below) → this entry takes `S136`, `S137` |

The staged file's own `S130..S134` collide with the lane's round-42 rows as well; a verbatim append
would overwrite **29** live rows — the round-34 M34-12 failure mode.

**The guard, proven on an indented fixture** (this closes the round-40 caveat the round-42 artifact
`R42Assim/id-collision.txt` explicitly left open). Fixture (scratch, 4 lines):

```
| S002 | x |
  | S002 | y |
   | S777 | z |
| S003 | w |
```

| pattern | matches |
|---|---|
| narrow column-zero `^\| S[0-9]+ ` | **2** (lines 1, 4) |
| 0–3-space `^ {0,3}\| S[0-9]+ ` | **4** (lines 1, 2, 3, 4) |

The 0–3-space extractor sees the indented `  | S002 |` row and the 3-space `   | S777 |` row that
the column-zero pattern misses — on an indented fixture the narrow pattern under-counts the
registry by 2 ids. On today's two real inputs the two patterns agree numerically (base: 134 = 134;
staged: 0 indented rows), so the collision count above is not sensitive to the choice — but the
0–3-space extractor is the one that stays correct if either file ever gains an indented row, and it
is the one the seat spec binds. The sibling seat's `receipts/id-collision.txt` used the narrow
pattern and asserts it "is sufficient for this file"; that is true for today's bytes but does not
close the fixture proof, which this seat closes.

**S135 reconciliation (calibration).** The seat spec says to write the rows as `S135-ONWARD`
placeholders and let the L1 assign real ids. At the base the first free id *is* `S135`, but
`plans/round-43-claims.md` `## Frontier step` reserves **S135 for the unblob 26.6.4 LICENSE row**
(opened by the L1 at 2026-10-27T08:08Z; delivered by seat `R43SrcLicense` as
`artifacts/R43SrcLicense/row-S135-docs.md`). Taking S135 for an API row would collide with the
round's own planned row. The rows are therefore numbered **S136, S137** — the first two ids
continuing the registry after S135 — and the L1 still assigns the final ids at landing. The sibling
scribe seat independently reached the same two ids from the same base.

## 4. Mirror-lane census — exit 0, and shown able to fail

Full receipt: `artifacts/R43AssimGround/receipts/mirror-census.txt`; raw outputs under `receipts/`.

Mirror construction (scratch only): `git -C <lane> archive 6b9e64fe… corpus SKILL.md
tools/round-27/xpin-attribute.mjs | tar -x -C $S/mirror` (3 247 files, 66 MB; `SKILL.md` and
`tools/round-27/xpin-attribute.mjs` are copied because base rows S036 and S081 cite them as
used-by targets), **plus** the base `corpus/SOURCES.md` with my two normalized rows inserted inside
`## Registry` right after the S134 row, **plus** the admitted entry file at
`corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` (the file the rows' used-by names).

```
$ sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
EXIT = 0
E-lines (E01..E12) .... 0
W04 warnings ........... 13        (the base registry's own pre-existing warnings; the same 13
                                  as .ufo/waves/round-43/census-start.txt)
final line ............. file  ok  $S/mirror/corpus/SOURCES.md
```

Census mode on the same mirror → exit 0: `rows 136 | tier.A 128 | tier.B 7 | tier.C 1 |
tier.invalid 0 | status.mined 131 | status.rejected 5 | status.queued 0 | status.invalid 0 |
FLEET.missing 0`. The base registry alone is `rows 134`; the tallies move by exactly the two added
rows, so **no base row was swapped** (the M34-12 shape is excluded by the per-status/per-tier
tallies, not only by the row count).

Controls — the harness is shown able to fail:

| control | exit | finding |
|---|---|---|
| CTL-D baseline | 0 | 0 E-lines |
| CTL-A used-by target file removed | 1 | `E11 S136/S137 missing used-by corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` |
| CTL-B S136 row duplicated in place | 1 | `E03 S136 duplicate id` + `E04 duplicate url … within scope …` |
| CTL-C a literal pipe inserted in the S136 scope cell | 1 | `E01 S136 fields=12` |
| CTL-E S136 kind changed to `license` | 1 | `E05 S136 kind=license` |
| CTL-F S136 row appended after `## Registry` | 1 | `E12 S136 row outside Registry section` |
| CTL-H the 132 staged rows appended **verbatim** | 1 | **266 E-lines**: 44 × `E01` (fields=12 — 44 staged rows carry a literal escaped pipe inside a cell and split into 14 fields), 88 × `E09` (recheck cell is a sentence, not an ISO date / `Nd` / symbolic cadence), 2 × `E03` (S136, S137 duplicate id), 132 × `E11` (every staged used-by path absent from the mirror) |

CTL-H is the load-bearing one for the L1: **the staged file cannot be appended as-is at all** — it
is malformed against the fleet validator independently of the id collisions. The two normalized rows
below are the re-grounded replacement.

## 5. The normalized rows (fleet schema, `S135-ONWARD` placeholders → S136/S137)

Delivered verbatim as `artifacts/R43AssimGround/rows/normalized-rows.md`; also inlined here. Schema
checked: **NF = 13** on both rows (11 columns), **no literal and no escaped pipe** in any cell,
`recheck` = `180d` (the `Nd` form the validator accepts), `status` = `mined`, `used-by` = **exactly
the admitted entry** (one path, no second entry), `opened` = `2026-10-27`, tier `A`, kinds
`dataset` and `docs` (both in the census enum).

```
| S136 | onekey-sec/sasquatch releases API — https://api.github.com/repos/onekey-sec/sasquatch/releases | dataset | A | The release inventory as a machine-readable feed: 8 releases, each with tag_name, published_at, body and an assets array of name, size and optional digest; not unblob behaviour, not any carrier, not licence permission to redistribute | fetched 2026-10-27T08:18:09Z, HTTP 200, 107313 B, sha256 cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0; re-grounded projection [8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]] (2026-10-27T08:19:46Z, exit 0) and the same projection at 08:48:41Z; the projection is the pin, the response digest is not, because the response is byte-stable only after re-serialisation | Count published assets per release before stating an architecture matrix: the matrix starts at sasquatch-v1.0.1 and sasquatch-v1.0 is amd64-only | mined | 2026-10-27 | 180d | corpus/knowledge/2026-10-27-sasquatch-release-matrix.md |
| S137 | onekey-sec/sasquatch releases page — https://github.com/onekey-sec/sasquatch/releases | docs | A | The rendered page's tag links only (8 distinct tags); the page bytes carry no asset filename, so every asset fact belongs to S136 | fetched 2026-10-27T08:19:46Z, HTTP 200, 349255 B, sha256 150c7584282394a4c68c5b93587ac5f9ffd167badb04349d522e584045f7d3d0; a later fetch returned 349251 B, sha256 e5f85ce0ded2678f56039ec7034c796cea0afe3cdf06142894383a49eebc7eda; grep -c sasquatch_1.0_amd64.deb returned 0 | Do not cite a rendered release page for its assets; cite the endpoint that serves them | mined | 2026-10-27 | 180d | corpus/knowledge/2026-10-27-sasquatch-release-matrix.md |
```

Deltas against the sibling scribe seat's `drafts/sources-rows.md`, all deliberate:

- **S136 anchor** quotes *my* fetch (08:18:09Z, sha256 `cb42cd61…` — byte-identical to the sibling's
  retained receipt) and adds the projection at two instants plus the reason the digest is not the
  pin.
- **S137 anchor** quotes *my* page fetch and my later fetch (349 251 B, `e5f85ce0…`); the sibling's
  cited 349 250 B / `d68fabf7…` was not produced by this seat and is not repeated as if it were.
  The anchor now carries two observed page lengths (349 255 / 349 251) and the "no asset filename"
  probe.
- Both rows keep `used-by` = the single admitted entry. If the L1 lands the entry under a
  different filename, the two `used-by` cells and the entry's own path must move together — E11
  otherwise reds (CTL-A shows the check is live).

**Ordering constraint for the L1 (same shape as `R43SrcLicense` §5).** `used-by` is checked on disk
for every `mined` row. The entry file
`corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` **does not exist in the lane today**
(the base tree's `corpus/knowledge/` has no `2026-10-27-` file). The two rows and the entry must
land in the **same commit**, or the rows after the entry — otherwise the round's own census validate
reds on the rows the round just added.

## 6. Quarantine slice (frontier step, 5 rows) and `considerthese/`

**Quarantine slice re-derived**, from the read-only register
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(sha256 `5afe1810…bad833`), with the round-38 derivation command unchanged → **5 rows**
(`S150 payload-absent`; `S113`, `S117`, `S136`, `S147` "the cited source could not be fetched…"),
register lines 82 / 315 / 316 / 317 / 318. sha256 of the derived slice:
`7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` — **byte-identical to rounds
38, 39, 41 and 42**. Receipt: `receipts/quarantine-slice.txt`, slice retained as
`receipts/quarantine-slice.derived`.

Scope note, stated rather than glossed: those five ids are **staged-package** ids, and the slice
therefore touches no row this seat proposes. The per-row **hand-check of the five cited sources is
not this seat's** — it is the wave's separate quarantine hand-check item (`R43Quarantine`); this
seat delivers the derivation and the digest equality only and does not claim a verdict it did not
produce.

**`considerthese/`** — **absent from this lane.** `ls -d <lane>/considerthese` → no such directory,
and `git ls-tree -r 6b9e64fe… -- considerthese` at the base is empty. Swept at the fleet root, 17 of
the 21 `*-shokunin` lanes have one; **kaidoku has none**. The round's report line is therefore: *no
`considerthese/` directory exists in this lane* (the fleet root's other lanes' directories are
outside this lane and are not evidence about it).

## 7. Defect found in the sibling scribe seat's draft (for the L1)

**R43-AG1 (calibration, medium).** The sibling draft's `## Limits` paragraph says the capture
"returned the same tags … while a `download_count` moved from 160 to 161 **and byte length grew
from 87 700 to 107 313 B**", and the entry body repeats "this capture … returned … byte length grew
from 87700 to 107313 B". **The size difference is a serialisation artifact, not a content change.**
The round-42 receipt is 87 700 B with **zero newlines** — it is the `jq -c` (single-line) form of
the payload: `jq -c . <r42 receipt> | head -c -1` reproduces sha256 `57a19513…499db` exactly. Today's
87 700 B is the **same** figure for the same payload in the same single-line form
(`json.dumps(..., separators=(',',':'))` → 87 700 B, both sides); 107 313 B is the raw
pretty-printed HTTP body. So the payload did not grow by 19 613 B — it is byte-for-byte the same
length once serialised the same way, and the only content deltas are the 7 `download_count`
counters (§2b). The entry's *conclusion* (the endpoint's bytes are not a stable pin; pin the
projection) is correct and this seat's rows carry it; the *stated evidence* for it is
misattributed and should be corrected before landing, or a later reader will believe the upstream
payload changed when it did not.

**R43-AG2 (calibration, low).** The sibling's `S137` anchor cites a second page fetch
(349 250 B, sha256 `d68fabf7…`) that no retained receipt in `artifacts/R43ScribeAssim/receipts/`
carries. This seat independently obtained three page lengths (349 255 / 349 255 / 349 251 B) with
three distinct digests, so the phenomenon is real; the specific digest is simply uncorroborated by
any retained file. Either retain that fetch or cite one that is retained. My rows cite only digests
this seat fetched and retained.

**R43-AG3 (calibration, low).** The sibling's `receipts/id-collision.txt` states the column-zero
pattern "is sufficient for this file" and does not exercise the indented fixture. True for today's
bytes, but the round-40 caveat it inherits is only closed by the fixture proof in §3; the
0–3-space pattern is the one that binds.

## 8. Commands actually run (exact; exit 0 unless stated)

```
date -u +%FT%TZ                                                        # 2026-10-27T08:18:09Z …
curl -sS -w 'HTTP_STATUS=%{http_code}\n' -o rel.json \
  'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100'
                                                                       # HTTP 200; 107313 B;
                                                                       # sha256 cb42cd61…
curl -sS -o rel-accept.json -w 'HTTP=%{http_code}\n' -H 'Accept: application/vnd.github+json' …   # 200, 107313 B
curl -sS -o rel-b.json -w 'HTTP=%{http_code}\n' -H 'Accept: application/vnd.github.v3+json' …     # 200, 107313 B
curl -sS -o rel-p2.json -w 'HTTP=%{http_code}\n' '…/releases?per_page=100&page=2'   # 200, 0 items
curl -sS -o tags.json  -w 'HTTP=%{http_code}\n' '…/tags?per_page=100'              # 200, 19 tags
curl -sS -o sasq-releases.html -w 'HTTP_STATUS=%{http_code}\n' https://github.com/onekey-sec/sasquatch/releases
                                                                       # HTTP 200; 349255 B
grep -c 'sasquatch_1.0_amd64.deb' sasq-releases.html                  # 0
grep -c 'sasquatch_1.0_arm64.deb' sasq-releases.html                  # 0
curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | grep -c 'sasquatch-v4.5.1-6'
                                                                       # 12  (ran 2026-10-27T08:48:41Z)
curl -fsSL …/releases | jq -c '[length,(map(.assets|length)),(map([.assets[]|select(.digest)]|length))]'
                                                                       # [8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]
python3 (field-by-field diff of r42 receipt vs today, download_count isolated)  # 7 fields, all download_count
jq -c . <r42 receipt> | head -c -1 | sha256sum                       # 57a19513…499db (== r42 receipt)
sha256sum ~/.local/bin/sasquatch                                      # ad02d27a…c774754
strings -a ~/.local/bin/sasquatch | grep 'unsquashfs version'         # unsquashfs version 4.5.1 (2022/03/17)
git -C <lane> show 6b9e64fe…:corpus/SOURCES.md | grep -oE '^ {0,3}\| S[0-9]+ ' | grep -oE 'S[0-9]+' | sort -V > reg-ids
grep -oE '^ {0,3}\| S[0-9]+ ' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md | … > staged-ids
comm -12 <(sort reg-ids) <(sort staged-ids)                          # 29 ids, S106..S134
printf '| S002 | x |\n  | S002 | y |\n   | S777 | z |\n| S003 | w |\n' > fix.md
grep -cE '^\| S[0-9]+ ' fix.md                                        # 2   (narrow pattern)
grep -cE '^ {0,3}\| S[0-9]+ ' fix.md                                  # 4   (0-3-space pattern)
git -C <lane> archive 6b9e64fe… corpus SKILL.md tools/round-27/xpin-attribute.mjs | tar -x -C $S/mirror
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md
                                                                       # EXIT 0, 0 E-lines, 13 W04
… plus the six controls of §4 (each exit 1, receipts ctl-A..ctl-H.out)
awk -F'|' -v l='kaidoku' … absent-defect-register.md                   # 5 rows
sha256sum quarantine-slice.derived                                    # 7383a90e…28e6a (== rounds 38-42)
git -C <lane> ls-tree -r --name-only 6b9e64fe… -- considerthese        # empty
```

Only the two public read-only GETs (plus the pagination/tags probes) left this machine; no REA,
unblob, sasquatch or `unsquashfs` invocation of any kind; no firmware image fetched, carved,
extracted or copied.

## 9. Limits and markers

- **[INFERENCE]** The claim "`1.0` is sasquatch's own Debian package version and `4.5.1` is the
  upstream handler base" is the entry's reading of the tag/filename pair plus the installed binary's
  `unsquashfs version 4.5.1 (2022/03/17)`. The bytes support it for the installed amd64 member and
  for `v4.5.1-1`'s own body; for the six older `v4.5.1-*` tags the base is inferred from the tag
  string. The entry must keep that marker.
- The **arm64 and armhf packages were not downloaded and not run**; their digests are the API's
  published values, not independently recomputed here.
- The **seven older releases' assets carry no published digest**, so those packages are size-pinned
  only; a per-asset sha256 for them would cost 42 package downloads (7 releases × 6 assets, less
  `sasquatch-v1.0`'s two) and is not done.
- The mirror census is a **scratch harness**, not a run on the live tree: it proves field shape, id
  uniqueness, enum compliance, URL/scope uniqueness and used-by resolution for the proposed rows.
  The live tree's validate at landing is the L1's to run.
- The **page's bytes vary per fetch** (349 255 / 349 255 / 349 251 B here, 349 250 B in the sibling's
  cited fetch); only the tag count and the "no asset filename" fact are stable. Nothing in S137's
  anchor depends on the byte length.
- The round-42 receipt is the `jq -c` form, not the raw HTTP body; that is why the raw-body byte
  counts of the two rounds differ (87 700 vs 107 313) while the payloads are identical apart from
  `download_count` (§7 R43-AG1).
- The five quarantine-slice rows' **cited sources were not re-checked by this seat**; only the
  derivation and the digest equality are this seat's evidence.
- **No tool was installed or upgraded**; the operator's tooling directive was satisfied by using
  tools already present.
