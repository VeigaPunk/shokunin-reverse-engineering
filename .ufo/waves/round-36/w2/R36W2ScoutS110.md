# R36W2ScoutS110 — re-open S110 and check the knowledge entry

Seat: scout, leaf. Opened 2026-10-26T05:00:45Z. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ScoutS110`, removed before yield. No tools installed. Lane HEAD read-only: `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`.

## 1. S110 re-opened (all observed)

`curl -fsSL -o t.md https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` → exit 0.

| Item | Entry says | Observed | Verdict |
|---|---|---|---|
| lines | 235 | `wc -l` = 235 (7580 bytes, no CR) | agree |
| sha256 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` | identical | agree |
| tag commit | `1fcc7a0a584a70a96c31f5a276c20944d199a089` | `git ls-remote https://github.com/onekey-sec/unblob 'refs/tags/26.6.4*' HEAD` → `1fcc7a0a584a70a96c31f5a276c20944d199a089 refs/tags/26.6.4` (no `^{}` line, so a lightweight tag) | agree |
| "byte-identical to HEAD" | yes | `curl …/HEAD/README.md`, `cmp` → identical, same sha256. The remote HEAD is now `ec14d614428b6ac5447a0da1f1c02bd2e039dfd6`, not the tag commit. The README bytes are the same. | agree |
| line 49 quote | `For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):` | `sed -n 49p` is that string exactly; `cat -A` shows it ends in `:$` | agree |
| line 43 | "Then install the required external extractor tools. On Ubuntu/Debian:" | exact | agree |

Debian-package install (README lines 52-53), verbatim:
```
curl -L -o sasquatch_1.0.deb "https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_$(dpkg --print-architecture).deb"
sudo dpkg -i sasquatch_1.0.deb && rm sasquatch_1.0.deb
```
So the README does document a Debian-package install for sasquatch. The amd64 asset URL resolves: `curl -sSLI …/sasquatch_1.0_amd64.deb` → `302` then `200`.

Structure around line 49: the `## Installation` heading is at line 35 and `### pip (recommended for most users)` at line 37. No heading falls between line 37 and `### Docker` at line 62. Lines 43-54 (apt block, line 49 sentence, dpkg block) all sit under the pip subsection. Line 56 then says "Verify that all extractors are available".

## 2. Sentence-by-sentence check of `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (blob tag BA4C)

| Line | Sentence, abridged | Verdict |
|---|---|---|
| 1 | `source: S110 …tag 26.6.4 (commit 1fcc7a0a…), 235 lines, sha256 6544d60f…, byte-identical to HEAD on 2026-10-26; line 49 "…"` | **Agree.** Every field reproduced above. |
| 3 | `verified-at … both READMEs re-opened … access 2026-10-26T04:36:42Z` | **Agree** that the content matches. I re-fetched 24 minutes later and got the same S110 digest. I cannot verify the 04:36:42Z timestamp. S111 re-fetched: 30 lines, sha256 `f09961ee…1fef`, line 12 "Very beta.", line 17 compiler/liblzma/liblzo/zlib, line 26 "squashfs-tools v4.3". All three match the entry. |
| 4 | `recheck: 180d — curl … \| sha256sum → 6544d60f…3716` | **Agree.** The command works as written and returns that digest. |
| 8 | "staged S106 → S110, staged S107 → S111 … both sources re-opened on 2026-10-26, pinned by tag/commit and sha256" | **Agree** on the S110 pin. The renumbering is lane-internal and I did not check the staged package. |
| 10-12 | "unblob's own README makes SquashFS support conditional on an external extractor: 'For SquashFS support, also install [sasquatch]…' (S110, line 49), inside the block that line 43 opens with 'Then install the required external extractor tools. On Ubuntu/Debian:'" | **Agree** that the quote, line numbers and enclosing block are correct. **Qualification (calibration, see D1):** the condition holds for the pip install route only. |
| 13-14 | "The README links the onekey-sec sasquatch project and publishes the install as a prebuilt Debian package, so a packaged route exists beside a source build." | **Agree.** Line 49 links `github.com/onekey-sec/sasquatch`. Lines 52-53 are a `.deb` download plus `dpkg -i`. "Beside a source build" rests on S111 (devttys0 `build.sh`), not on S110. The S110 README gives no source-build path for sasquatch. |
| 37-38 | "S110 shows the producer-documented Debian-package route" (against the Frontier phrase "AUR-only") | **Agree.** Lines 49-53 are a producer-documented Debian-package route. The README names no AUR route for sasquatch (I grepped: `sasquatch` appears only on lines 49, 52 and 53). I did not read the `PROVINCE.md` Frontier text. |
| 40-41 | "Not claimed … that the onekey-sec package is a fork of devttys0 (neither README says so)" | **Agree for S110**: the unblob README does not mention devttys0. I also grepped a fresh clone of `onekey-sec/sasquatch` HEAD `b34aa5ef67068a2137ac04e2272915bd45388260` for `very beta|devttys0` (`grep -rIl -i`) and got no files. So neither onekey-sec text says "fork" or "devttys0". |

## 3. Disagreements and calibration findings

**D1 — title and framing overgeneralise (S110-cited; minor).**
- Title: "unblob's SquashFS support is a declared dependency on an external sasquatch extractor". Lines 10-12: "makes SquashFS support conditional on an external extractor".
- S110 itself says, under `### Docker` (line 64): "The Docker image bundles all extractors — no extra setup needed". Under `### Kali Linux` (lines 77-79) it gives only `sudo apt install unblob`. The external-tool step appears only under the pip route (lines 37-60). A route qualifier ("pip install route") would match the source. The Docker line is a direct counter-datum in the same document.
- Consequence 1 ("the missing-dependency path is unblob's design") is separately supported by REA gap output. S110 supports it for pip installs only.

**D2 — attribution slip in consequence 2 (not an S110 sentence, but it contradicts the entry's own "Not claimed").**
- Line 30: "Because the producer calls its own extractor 'Very beta'". "Very beta." is line 12 of the **devttys0** README (S111), which line 41 declines to link to the onekey-sec package.
- The producer here is unblob/onekey-sec. S110 says nothing about maturity, and no file in onekey-sec/sasquatch HEAD `b34aa5ef` contains "very beta" (grep, no hits).
- Either "producer" means devttys0, which the entry elsewhere says is not established to be the same project, or the sentence is wrong. Suggested wording: "Because the devttys0 sasquatch README (S111) calls it 'Very beta'…". The conclusion is labelled [INFERENCE]. The attribution is still unsupported as written.

**D3 — nit.** Line 14 says the README "publishes the install as a prebuilt Debian package". It fetches a release asset from onekey-sec's GitHub release `sasquatch-v4.5.1-6` and the file is named `sasquatch_1.0_<arch>.deb`. That is not distro-packaged. "Prebuilt .deb release asset" is more exact. This is wording only.

**Nothing found against:** line count, sha256, tag commit, line-49 quote, line-43 quote, byte-identity to HEAD, and the Debian-package install in the README. All reproduced exactly.

## 4. Not checked
- The 2026-10-26T04:36:42Z access time and the staged package `merge/kaidoku/...` text.
- `PROVINCE.md:149-150`, the K*/before.json gap fields, the `~/.local/bin/sasquatch` sha256 and `unblob --show-external-dependencies` output. None cite S110.
- Whether `sasquatch-v4.5.1-6` carries 4.5.1. I observed only the `unsquashfs version 4.5.1 (2022/03/17)` field in `corpus/evidence/round-36/c1/K1/after-run.json:10`.
