# C1S139Reopen — S139 squashfs-tools 4.7.5 re-open

**Verdict: re-open holds.** The `4.7.5` release identity and `/usr/bin/unsquashfs` match the S139 row and the `carriers.json` pin. The rendered releases-page digest moved (the row already treats that digest as mutable). One draft defect: `oracle_tool_ok` returns true when the top-level `oracle` key is absent.

Axes: coverage (page, tag page, releases feed, annotated tag), depth (located quote, version stdout, binary digest), calibration (those bytes against the row and the pin).

Access date: `2026-10-28T21:07:48Z` (response `Date: Wed, 28 Oct 2026 21:07:49 GMT`). No tools installed. Full `c1-counter.py` score and `c1-run.sh --data-run`: not run. Registry not edited.

## Gate text for `corpus/lessons/round-49.md` `## Gate`

Paste this row and the paragraph under it. `opened` stays `2026-10-28`.

| row | URL | accessed | located quote (≤25 words) |
|---|---|---|---|
| S139 | https://github.com/plougher/squashfs-tools/releases (tag https://github.com/plougher/squashfs-tools/releases/tag/4.7.5; feed https://api.github.com/repos/plougher/squashfs-tools/releases) | 2026-10-28T21:07:48Z, HTTP 200, 361752 B, sha256 `f60447fa2044281e223b51b500bcd33abf6d1061890e77da26730d1482fa8121` | section `#release-4.7.5` `<h3>`: "4.7.5 (01 MAR 2026): Bug fix release (mostly)" |

S139 stays admitted (docs, tier A, `mined`). The quote is 8 words and is the `<h3>` inside `<section id="release-4.7.5">` (this fetch: releases page line 939, tag page line 653). The same words are the first line of the release `body` after the `### ` marker. Release identity, re-measured equal to the row: `tag_name` `4.7.5`, `name` "Squashfs tools 4.7.5", `published_at` `2026-03-01T23:05:47Z`; annotated tag `1fdc2fe01d681438a04e2a137a9f51d829ba3358` (message `squashfs-tools-4.7.5`), peeled commit `708c59ae80853b0845017c33b42e56061cc546cd`; the releases feed lists 9 tags. `/usr/bin/unsquashfs -version` exits 1; first stdout line `unsquashfs version 4.7.5 (2026/03/01)`; binary sha256 `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c` (size 166976), equal to `carriers.json` `oracle.tool_sha256`. At landing, append `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` to `used-by`.

## Findings

| check | command | utc | exit | sha256 / HTTP | result |
|---|---|---|---|---|---|
| Releases page | `curl -sSL -D raw/page.headers -o raw/page.body -w 'http_code=%{http_code}\nsize_download=%{size_download}\nurl_effective=%{url_effective}\nnum_redirects=%{num_redirects}\n' "https://github.com/plougher/squashfs-tools/releases"` | 2026-10-28T21:07:48Z–21:07:49Z | curl 0 | HTTP 200, 0 redirects, 361752 B, body `f60447fa2044281e223b51b500bcd33abf6d1061890e77da26730d1482fa8121` | 9 tag links, `4.7.5` present. Quote in raw HTML and after tag strip |
| Tag page | `curl -sSL` same `-w` form, URL `https://github.com/plougher/squashfs-tools/releases/tag/4.7.5` | 2026-10-28T21:07:49Z–21:07:50Z | curl 0 | HTTP 200, 159470 B, `75e940e4259143ff39e1fc34cd60b8dd449ebbebf1aac2eb4c347fb5d89de4c5` | same `<h3>` at line 653 |
| Releases feed | `curl -sS -A kaidoku-r49-C1S139Reopen -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28'` URL `https://api.github.com/repos/plougher/squashfs-tools/releases` | 2026-10-28T21:07:50Z | curl 0 | HTTP 200, 48840 B, `191e6326363e87ae9298ba9882e546d948789295ffd6005af6811aa94ce26a60` | 9 objects. Newest: `tag_name` `4.7.5`, `name` "Squashfs tools 4.7.5", `published_at` `2026-03-01T23:05:47Z` |
| Release by tag | same API headers, URL `.../releases/tags/4.7.5` | 2026-10-28T21:07:51Z | curl 0 | HTTP 200, 5285 B, `4d97a6f3eb482c8112356dbc785157b612c3cf5afb802857528deefa4a6809ae` | `body` line 1 is `### 4.7.5 (01 MAR 2026): Bug fix release (mostly)` |
| Annotated tag ref | same API headers, URL `.../git/refs/tags/4.7.5` | 2026-10-28T21:07:50Z | curl 0 | HTTP 200, 343 B, `896eaf567e790d1be558da2110a260a9419f5cc236a48f572d211f528fbe0da5` | object `1fdc2fe01d681438a04e2a137a9f51d829ba3358`, type `tag` |
| Tag object | same API headers, URL `.../git/tags/1fdc2fe01d681438a04e2a137a9f51d829ba3358` | 2026-10-28T21:07:50Z–21:07:51Z | curl 0 | HTTP 200, 688 B, `0320bf1c914d613a4ab1642529ff5b9fda248dbf3204359d67c5ad6d6eef6a5c` | `tag` `4.7.5`, message `squashfs-tools-4.7.5\n` (1 word), object `708c59ae80853b0845017c33b42e56061cc546cd` type `commit`, tagger date `2026-03-01T22:57:20Z` |
| Git tag list | same API headers, URL `.../tags?per_page=100` | 2026-10-28T21:09:03Z | curl 0 | HTTP 200, 7787 B, `d90120ead0373c8376ce1b7d97f04caced5a26d4891f9bee02113aa28a3285a1` | 18 git tags. The `4.7.5` entry's commit sha is the peeled commit `708c59ae…`. The row's "9 distinct release tags" is the releases feed |
| `unsquashfs -version` | `/usr/bin/unsquashfs -version` (stdout and stderr split) | 2026-10-28T21:09:03Z | **1** | stdout 560 B `6154c39eee941fa66ea0ee7942802a2607d6ee2e749051c956569d7e9f6d333a`; stderr 0 B `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | first line `unsquashfs version 4.7.5 (2026/03/01)`. Exit 1 is the tool's version convention |
| `unsquashfs --version` | `/usr/bin/unsquashfs --version` | 2026-10-28T21:09:03Z | **1** | stdout sha256 identical to `-version` (`6154c39e…`); stderr empty | the row's `--version` and the carriers `-version` argv print the same bytes |
| Binary pin | `sha256sum /usr/bin/unsquashfs`; `stat -c 'size=%s …' /usr/bin/unsquashfs` | 2026-10-28T21:09:03Z | sha256sum 0 | `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c` | size 166976, mode 755, 1 link, realpath `/usr/bin/unsquashfs`. Equals `carriers.json` `oracle.tool_sha256`, `toolchain.unsquashfs.sha256`, and `version_argv_stdout_sha256` `6154c39e…` |
| Package | `pacman -Qo /usr/bin/unsquashfs`; `pacman -Qi squashfs-tools` | 2026-10-28T21:09:03Z–21:09:04Z | 0, 0 | — | `/usr/bin/unsquashfs is owned by squashfs-tools 4.7.5-1`. Packager Christian Hesse; build `2026-03-02`; URL `https://github.com/plougher/squashfs-tools` |
| `oracle_tool_ok` | `python3` import of draft `c1-counter.py` `oracle_tool_ok` on six specs (stdout `raw/oracle-tool-ok.stdout`) | 2026-10-28T21:10:35Z–21:10:36Z | 0 | stdout `6c7c0905098f79e85f5f8860634788cbe7adb16d2f72881c061c76cbbdf67083`; stderr empty | see defect D1 |

Receipts: `.ufo/waves/round-49/w1/C1S139Reopen/` (`SHA256SUMS`). Response headers there are redacted (`set-cookie` dropped).

### What still matches the row

`corpus/SOURCES.md` S139 evidence, re-measured this fetch:

- `tag_name` `4.7.5`, `name` "Squashfs tools 4.7.5", `published_at` `2026-03-01T23:05:47Z`
- annotated tag `1fdc2fe01d681438a04e2a137a9f51d829ba3358`, peeled commit `708c59ae80853b0845017c33b42e56061cc546cd`
- 9 names on the releases feed and 9 `releases/tag/` links on the rendered page: `4.5.1`, `4.6`, `4.6.1`, `4.7`, `4.7.1`, `4.7.2`, `4.7.3`, `4.7.4`, `4.7.5`
- `/usr/bin/unsquashfs --version` prints `unsquashfs version 4.7.5 (2026/03/01)` and exits 1

`carriers.json` `oracle.tool_sha256` / `toolchain.unsquashfs` (`sha256`, `size` 166976, `version_line`, `version_argv` `["/usr/bin/unsquashfs","-version"]`, `version_argv_exit` 1, `version_argv_stdout_sha256`) match this host. The S139 evidence cell records the page digest and the version line. The binary digest is the carriers pin.

The entry draft `w1/artifacts/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` source line for S139 (version line, binary sha256, Arch `squashfs-tools 4.7.5-1`, page HTTP 200, tag present) matches this measurement.

`c1-counter.py` `OPENED` is `2026-10-28`. This re-open is the same calendar day. The `opened` cell stays `2026-10-28`. Current `used-by` is `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`. The r49 entry append is a landing edit; the counter's `sourced` binding reads it.

### Page digest moved (record it in the Gate; leave the row's morning snapshot)

| fetch | bytes | sha256 |
|---|---|---|
| Row and round-44 receipt `w1/R44SrcOracle/receipts/s139-releases-page.stdout.txt`, started `2026-10-28T11:13:04Z` (read from that receipt; this seat did not re-fetch it) | 398943 | `d08749f4b9cdcf2a01cd1d4e472b77e0372a9107aa720bf683f8383b644dbd93` |
| This seat, `2026-10-28T21:07:48Z` | 361752 | `f60447fa2044281e223b51b500bcd33abf6d1061890e77da26730d1482fa8121` |

Both are HTTP 200 of `https://github.com/plougher/squashfs-tools/releases`. The row's rationale says the mutable page digest is the fetch record and the recheck pin is the tag identity. That sentence is what this pair shows. The counter does not read the page digest. Replacing the evidence cell with today's digest would describe this fetch and would no longer describe the 11:13:04Z receipt.

The git tags API returned 18 tags, including names the releases feed does not list (`squashfs-tools-4.6`, `CVE-2021-41072`, `4.4`, `3.2`, `3.1`, and others). The row's "9 distinct release tags" is the releases feed. Leave the 9.

The release asset `squashfs-tools-4.7.5.tar.gz` (API `size` 412571, `digest` `sha256:547b7b7f4d2e44bf91b6fc554664850c69563701deab9fd9cd7e21f694c88ea6`) is a different object from `/usr/bin/unsquashfs`. The tarball was not downloaded. The binary pin stays `461e1fd9…`.

### D1 — `oracle_tool_ok` is true when the top-level `oracle` key is missing

`c1-counter.py` docstring (the predicate), lines 176–177: "the frozen oracle tool path resolves and, when the table pins them, its sha256/version match". `BINDINGS` includes `oracle_tool_ok` (line 337). The function (lines 2222–2226) returns `(True, {reason: no oracle block frozen (advisory)})` when `spec.get('oracle')` is missing or `None`.

Executed import of the draft file, exit 0, stdout sha256 `6c7c0905098f79e85f5f8860634788cbe7adb16d2f72881c061c76cbbdf67083`:

| spec | ok |
|---|---|
| draft `carriers.json` (block present) | True; live sha256 equals `461e1fd9…`; version line `unsquashfs version 4.7.5 (2026/03/01)` |
| `{}` | True, advisory |
| `{"oracle": None}` | True, advisory |
| `{"oracle": {}}` | False, `oracle.tool is not a path` |
| `tool_sha256` set to 64 zeros | False |
| `version` set to `9.9.9` | False |

With the draft block present, a wrong sha256 and a wrong version each turn the binding false, and this host's binary turns it true. Omitting the key turns it true without resolving `/usr/bin/unsquashfs`. Per-carrier member rows are a different check (`carrier %r has no oracle member rows`, line 754). A full counter score of a carriers file with the key removed: not run.

Fold before the freeze: a missing `oracle` object should fail `oracle_tool_ok` (the path did not resolve). The draft `carriers.json` already carries the block; keep it in the freeze.
