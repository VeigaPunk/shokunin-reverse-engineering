source: S136 — https://api.github.com/repos/onekey-sec/sasquatch/releases — the release list as machine JSON: 8 releases, each with `tag_name`, `published_at`, `body` and `assets[]` (name, size, `digest`); fetched 2026-10-27T08:18:38Z, HTTP 200, 107313 B, sha256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0`; not unblob behaviour, not any carrier, not licence permission to redistribute
source: S137 — https://github.com/onekey-sec/sasquatch/releases — rendered page "Releases · onekey-sec/sasquatch": 8 distinct release-tag links in the page bytes, zero asset filenames; fetched 2026-10-27T08:20:30Z, HTTP 200, 349255 B, sha256 `89e7377d92132bfa1bf1a004bf38a6f105dfe85ea99a753cccde49af29227a67`; a second fetch at 2026-10-27T09:05:48Z returned the same length (349255 B) with a different digest `56632d0f19d7e7e81776e9a48e04f7ce4b89d32f9c79670617e5f2c888cb1cea`, and round 42's retained fetch was 349266 B, sha256 `71ebf1600a0a9764f62298976d0d2bd0e0700694e3e2ed5612386c7c370b734a`
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | jq -c '[length, (map(.assets|length)), (map([.assets[]|select(.digest)]|length))]'` → `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]` (ran 2026-10-27T08:20:15Z, exit 0); a ninth release, a changed asset count, or a second release whose assets carry `digest` means the matrix moved
ground: the operator-facing packaging half of the Frontier bullet `- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback covers the carved-image path today.` (`PROVINCE.md:156-157`); discharges round 36's refusal of `sasquatch-prebuilt-package-inventory` (`corpus/lessons/round-36.md:42`), re-grounded on 2026-10-27 bytes under round 42's ADMIT verdict (`.ufo/waves/round-42/w1/R42Assim.md` `## 1`)

# The sasquatch release train publishes three-architecture Debian packages from v1.0.1 on — v1.0 is amd64-only, and no release body states a package/upstream version pair

**Claim (observed, S136).** onekey-sec/sasquatch publishes **8 releases**. Seven of the eight carry
**six** assets: `sasquatch_1.0_{amd64,arm64,armhf}.deb` and the matching `sasquatch-dbgsym_1.0_*`
packages. The eighth — the oldest, `sasquatch-v1.0` (published 2022-02-26T23:10:04Z) — carries
**two**, both amd64: `sasquatch_1.0_amd64.deb` (185708 B) and `sasquatch-dbgsym_1.0_amd64.deb`
(321380 B). The architecture matrix therefore begins one tag later, at `sasquatch-v1.0.1`
(2022-12-03T10:18:00Z: 185724 / 168184 / 162288 B for amd64 / arm64 / armhf), not at v1.0.

| tag | published (UTC) | assets | `sasquatch_1.0_amd64.deb` | `…_arm64.deb` | `…_armhf.deb` | `assets[].digest` |
|---|---|---|---|---|---|---|
| `sasquatch-v4.5.1-6` | 2026-01-27T11:57:51Z | 6 | 187244 | 170080 | 164428 | **6 of 6** |
| `sasquatch-v4.5.1-5` | 2025-02-10T14:54:38Z | 6 | 187040 | 170556 | 164376 | 0 of 6 |
| `sasquatch-v4.5.1-4` | 2023-06-06T19:02:28Z | 6 | 186968 | 169824 | 164524 | 0 of 6 |
| `sasquatch-v4.5.1-3` | 2023-04-07T09:59:24Z | 6 | 187024 | 169828 | 164452 | 0 of 6 |
| `sasquatch-v4.5.1-2` | 2023-03-09T17:43:19Z | 6 | 187076 | 169504 | 164724 | 0 of 6 |
| `sasquatch-v4.5.1-1` | 2023-03-02T10:01:02Z | 6 | 187016 | 169360 | 164716 | 0 of 6 |
| `sasquatch-v1.0.1` | 2022-12-03T10:18:00Z | 6 | 185724 | 168184 | 162288 | 0 of 6 |
| `sasquatch-v1.0` | 2022-02-26T23:10:04Z | **2** | 185708 | — (absent) | — (absent) | 0 of 2 |

Sizes in bytes, from `assets[].size`. The newest release's six `dbgsym` members are 323896 (amd64),
327784 (arm64) and 319048 (armhf); `sasquatch-v1.0`'s single `dbgsym` member is 321380.

**Per-asset pins.** Only `sasquatch-v4.5.1-6`'s assets carry a `digest` field; the six values the API
published at 2026-10-27T08:18:38Z are `sasquatch_1.0_amd64.deb` sha256
`efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` (also held by S107),
`sasquatch_1.0_arm64.deb` sha256 `28e57a4ff545da32a65c3e061ff8a51e5ebaa5d170985c49f0b3eef08923476e`,
`sasquatch_1.0_armhf.deb` sha256 `29c721598df93dcdf3c876b61d9941764f40af8f0ec4f0f8ac3d2fe75b8f1c22`,
`sasquatch-dbgsym_1.0_amd64.deb` sha256 `73d44ca506e3273784091f3092839e8e8c162a81bb7d5af757201b0b1d41c54e`,
`sasquatch-dbgsym_1.0_arm64.deb` sha256 `7891831a7cd7111d7d2380ef2df3dcb32295ea5093eff5ceec15e407e7be49c4`,
`sasquatch-dbgsym_1.0_armhf.deb` sha256 `9d82e6d4320957e2491603aa00f9c55fd816770a5f8926eaf7c454e98e74686a`. For the
seven older releases the endpoint publishes no digest. Their 38 assets are not downloaded or independently
hash-pinned here; the matrix records the API's size fields only, so those are point-in-time source observations,
not content digests or proof of package bytes.

**The two round-36 falsifications, re-checked on this round's bytes.**

1. *"each [release] carrying a Debian package per architecture"* — **false as a universal.**
   `sasquatch-v1.0` carries 2 assets, both amd64; its name set is
   `{sasquatch_1.0_amd64.deb, sasquatch-dbgsym_1.0_amd64.deb}` and no `arm64` or `armhf` string occurs
   in that release's `assets[]`. The per-release asset counts are `[6, 6, 6, 6, 6, 6, 6, 2]`.
2. *"The release body shows the packaged upstream version (4.5.1) against the package version (1.0)"* —
   **not in any body.** Five of the eight bodies are empty (`v4.5.1-4`, `v4.5.1-3`, `v4.5.1-2`,
   `v1.0.1`, `v1.0`); the three that are not are 645, 560 and 38 bytes. None
   contains a standalone `1.0` token, so no body pairs the package version with an upstream version.
   `sasquatch-v4.5.1-6`'s 645-byte body lists three change lines, a "New Contributors" list and a
   `Full Changelog` URL (`…compare/sasquatch-v4.5.1-5...sasquatch-v4.5.1-6`) and includes the line
   "unsquashfs: fix prototypes for C23 by @whispersofthedawn in …/pull/32". The one body that names an
   upstream version at all is `sasquatch-v4.5.1-1`'s, 38 bytes: "Rebased on top of squashfs-tools
   4.5.1" — the upstream base only, with no package version beside it.

**Where the asset facts come from.** The rendered releases page (S137) carries the eight tag links and
**zero** occurrences of any asset filename (`grep -c 'sasquatch_1.0_amd64.deb'` → 0; likewise for the
arm64, armhf and dbgsym names): an unauthenticated fetch of
`https://github.com/onekey-sec/sasquatch/releases` does not serve the asset list, so asset names,
sizes and digests are facts of the REST endpoint (S136), not of the page. The staged entry cited the
page for the assets; that citation is corrected here.

**Two numbers the package name conflates.** The tag states `4.5.1`, the filename states `1.0`. The
`v4.5.1-1` body identifies `4.5.1` as the squashfs-tools base it was rebased onto, and the installed
amd64 member self-reports `unsquashfs version 4.5.1 (2022/03/17)` (round-36 receipt
`corpus/evidence/round-36/c1/K1/after-run.json`; binary sha256
`ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, re-hashed 2026-10-26 and again
2026-10-27, unchanged). So `1.0` is
sasquatch's own Debian package version and `4.5.1` is the upstream handler base. [INFERENCE] for the
six older `v4.5.1-*` tags: only `v4.5.1-1`'s body states the base, so their common base is inferred
from the tag string, not from their own bodies.

**Why this matters for the lane.** The lane's Frontier bullet said `sasquatch (AUR)`, which read as
"AUR is the route". Three published architectures mean the packaging decision is *which arch and which
tag*, taken from an official release, not a hunt — and the arch is load-bearing: the lane runs the
amd64 package, and the arm64/armhf packages are published but never downloaded or run here. It also
separates the two version numbers the package name conflates (above), which is what the Frontier
bullet and the round-36 refusal read as one.

**Not claimed.** Nothing here says any of these packages works with the installed unblob: the binary's
provenance and the pair's behaviour on this host are held separately
(`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`,
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`). The arm64 and armhf packages were
not downloaded or run. Nothing here is a licence statement about redistribution.

**Limits — an API body is not a document.** The endpoint's bytes are not a pinnable document. This
capture, taken 10.5 h after round 42's, returns the same tags, the same `published_at` values and the
same `(name, size)` set for all 44 assets; reduced to one line **both** captures serialize to 87701 B
(round 42's receipt is that compact form, 87700 B without the trailing newline; this round's receipt is
the pretty HTTP body at 107313 B — a length difference that is serialization, not drift), and the only
field-level differences are **7 `download_count` counters** (`sasquatch_1.0_amd64.deb` on
`sasquatch-v4.5.1-6`: 23694 → 23773). The rendered page moves per request: two same-day fetches are
both 349255 B with different digests (`89e7377d…`, `56632d0f…`), and round 42's retained fetch is
349266 B, sha256 `71ebf160…`. What is pinned is therefore the **projection** in `recheck:` (release
count, per-release asset count, per-release digest count), not the response digest; a digest pin reds
on a download counter and a page pin reds on a per-request token. Beyond the projection, this entry
rests on nothing a later body edit could not change: if a maintainer edits `sasquatch-v4.5.1-1`'s body
to state a package version, the second falsification above flips without the tag or asset rows moving
— so the recheck filter is a *floor*, and the body sentence is re-read (not re-counted) when the
filter's third element first becomes non-zero.

**Overlap.** S107 already holds `sasquatch-v4.5.1-6`'s asset set, publish date and the amd64 package
digest; held entry `2026-10-26-unblob-sasquatch-dependency.md` holds the Debian-package *route*. What
is new here is the eight-release matrix, its start tag, the arch gap at `v1.0`, the digest-presence
pattern, the arm64/armhf digests and the body-version finding. No v3 or extractor-behaviour claim is
made.

**Re-grounded in-wave (2026-10-27).** The round's re-grounding seat re-fetched both sources
independently and re-derived every cell of the matrix above; its verdict is **ADMIT, flip unfired on
all three limbs** — still 8 releases (`?per_page=100&page=2` → HTTP 200 with **0 items**; the
repository's tags endpoint returns 19 tags, of which the 8 `sasquatch-v*` ones are exactly these
releases and the rest are `squashfs-tools-v4.x` tags), every release-level and asset-level field equal
to round 42's receipt except 7 `download_count` counters, and 0 of 8 bodies containing a standalone
`1.0` token (`.ufo/waves/round-43/w1/R43AssimGround.md` §1–§2; its API receipt is byte-identical to
this seat's, sha256 `cb42cd61…`). The staged entry's own `recheck:` — `grep -c 'sasquatch-v4.5.1-6'`
→ `12` — reproduces, and `~/.local/bin/sasquatch` re-hashes to `ad02d27a…c774754` on 2026-10-27,
unchanged.
