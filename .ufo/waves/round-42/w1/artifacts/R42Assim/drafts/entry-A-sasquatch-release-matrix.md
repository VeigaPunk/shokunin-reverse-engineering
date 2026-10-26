# DRAFT (not landed) — admitted entry A, re-grounded

Source package file: `merge/kaidoku/knowledge/corpus/knowledge/sasquatch-prebuilt-package-inventory.md`
(staged S130; refused round 36 Decision 2 — `corpus/lessons/round-36.md:42`).
Proposed lane path: `corpus/knowledge/2026-10-26-r42-sasquatch-release-matrix.md`
Proposed lane rows: S130 (API), S131 (rendered page) — see `sources-rows.md`.

Every number below was produced by the commands in `../sources-reopened.md` §A on 2026-10-26;
receipts `../receipts/rel.json` (sha256 `57a19513…499db`) and `../receipts/sasq-releases.html`
(sha256 `71ebf160…b734a`).

---

source: S130 — https://api.github.com/repos/onekey-sec/sasquatch/releases — the release list as JSON: 8 releases with `tag_name`, `published_at`, per-release `assets[]` (name, size, `digest`) and `body` — fetched 2026-10-26T21:51:26Z, HTTP 200, 87700 B, sha256 `57a19513ca266c10a310504fc33fa16f15e04f92f0be6840c2eb4e6c56a499db`; not unblob behaviour, not any carrier, not licence permission to redistribute
source: S131 — https://github.com/onekey-sec/sasquatch/releases — rendered page "Releases · onekey-sec/sasquatch": an 8-tag release list in the page bytes — fetched 2026-10-26T21:52:15Z, HTTP 200, 349266 B, sha256 `71ebf1600a0a9764f62298976d0d2bd0e0700694e3e2ed5612386c7c370b734a`; the page carries **no** asset filename
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d),[len(r["assets"]) for r in d])'` → `8 [6, 6, 6, 6, 6, 6, 6, 2]` (ran 2026-10-26); a different list means a release was added, deleted or re-asseted
ground: the operator-facing packaging half of the frontier bullet `sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today` (`PROVINCE.md:156-157`, historically phrased AUR-only); discharges round 36's refusal `sasquatch-prebuilt-package-inventory` (`corpus/lessons/round-36.md:42`)

# The sasquatch release train publishes three-architecture Debian packages from v1.0.1 on — v1.0 is amd64-only, and no release body states a package/upstream version pair

**Claim (observed, S130).** onekey-sec/sasquatch publishes **8 releases**. Seven of the eight
carry **six** assets: `sasquatch_1.0_{amd64,arm64,armhf}.deb` and the matching
`sasquatch-dbgsym_1.0_*` packages. The eighth — the oldest, `sasquatch-v1.0` (published
2022-02-26T23:10:04Z) — carries **two**, both amd64: `sasquatch_1.0_amd64.deb` (185708 B) and
`sasquatch-dbgsym_1.0_amd64.deb` (321380 B). The architecture matrix therefore begins at
`sasquatch-v1.0.1` (2022-12-03T10:18:00Z: 185724 / 168184 / 162288 B for amd64 / arm64 / armhf),
not at v1.0.

| tag | published (UTC) | assets | amd64 | arm64 | armhf |
|---|---|---|---|---|---|
| `sasquatch-v4.5.1-6` | 2026-01-27T11:57:51Z | 6 | 187244 | 170080 | 164428 |
| `sasquatch-v4.5.1-5` | 2025-02-10T14:54:38Z | 6 | present | present | present |
| `sasquatch-v4.5.1-4` | 2023-06-06T19:02:28Z | 6 | present | present | present |
| `sasquatch-v4.5.1-3` | 2023-04-07T09:59:24Z | 6 | present | present | present |
| `sasquatch-v4.5.1-2` | 2023-03-09T17:43:19Z | 6 | present | present | present |
| `sasquatch-v4.5.1-1` | 2023-03-02T10:01:02Z | 6 | present | present | present |
| `sasquatch-v1.0.1` | 2022-12-03T10:18:00Z | 6 | 185724 | 168184 | 162288 |
| `sasquatch-v1.0` | 2022-02-26T23:10:04Z | **2** | 185708 | — | — |

Sizes in bytes, from `assets[].size`. The newest release's six assets are the only ones the API
publishes with a `digest` (sha256) field — `6 of 6` for `sasquatch-v4.5.1-6`, `0 of 6` for each of
the other seven releases, so the older packages can be size-pinned but not digest-pinned from this
endpoint.

**The version-pair sentence is not in any release body.** `sasquatch-v4.5.1-6`'s body is 645 bytes
and holds three change lines, a "New Contributors" list and a changelog URL; it names no
package/upstream version pair. What it does carry is the fix line
"unsquashfs: fix prototypes for C23 by @whispersofthedawn in …/pull/32" (S130, `body`).
`sasquatch-v1.0`'s body is empty (0 bytes).

**Where the asset facts actually come from.** The rendered releases page (S131) lists exactly the
eight tags and **zero** occurrences of any asset filename: an unauthenticated fetch of
`https://github.com/onekey-sec/sasquatch/releases` does not carry the asset list, so the asset
names, sizes and digests are facts of the REST endpoint (S130), not of the page. The staged entry
cited the page for the assets; that citation is corrected here.

**Why this matters for the lane.** The lane's Frontier bullet said `sasquatch (AUR)`, which read as
"AUR is the route". Three published architectures mean the packaging decision is which arch and
which tag, taken from an official release, not a hunt. It also separates two numbers the package
conflates: the packaged upstream version (`4.5.1`, in the tag) and the Debian package version
(`1.0`, in the filename) — a separation the tag/filename pair states, not the body.

**Not claimed.** Nothing here says any of these packages works with the installed unblob: the
binary's provenance and the pair's behaviour on this host are held separately
(`corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`,
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`; the installed amd64 member is
`~/.local/bin/sasquatch` sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`,
re-hashed 2026-10-26). The arm64 and armhf packages were not downloaded or run. Nothing here is a
licence statement about redistribution.

---
