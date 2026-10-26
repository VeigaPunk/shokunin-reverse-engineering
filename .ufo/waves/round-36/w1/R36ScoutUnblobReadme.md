# R36ScoutUnblobReadme — re-open of unblob + sasquatch READMEs against `unblob-sasquatch-dependency.md`

Observation cutoff: 2026-10-26T04:27:35Z (first fetch). Advisory only; no lane/VCS writes, no tool installs (RULES.md read; nothing installed or updated). Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScoutUnblobReadme` removed at the end.

Entry under test: `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/unblob-sasquatch-dependency.md` (sha256 `032c97a822b89c4606bb6988ec32e2eeec1963277f4eae100a60b0085923ca78`, read-only).

## Sources re-opened today

| id | URL | http | bytes | lines | sha256 |
|---|---|---|---|---|---|
| U-main | `https://raw.githubusercontent.com/onekey-sec/unblob/HEAD/README.md` | 200 | 7580 | 235 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` |
| U-tag | `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | 200 | 7580 | 235 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` |
| D-master | `https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` | 200 | 1050 | 30 | `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` |

- The pin worked: tag `26.6.4` resolves (GitHub API `git/ref/tags/26.6.4`, type commit) to `1fcc7a0a584a70a96c31f5a276c20944d199a089` (commit date 2026-06-04T07:39:13Z; release `26.6.4` published 2026-06-04T08:52:43Z). The tag README is byte-identical to HEAD's. Default-branch HEAD today is `ec14d614428b6ac5447a0da1f1c02bd2e039dfd6`, so HEAD has moved past the tag but README.md has not changed; the last commit touching README.md (per `commits?path=README.md`) is 2026-03-04 or earlier.
- The entry's source line names "HEAD as fetched 2026-10-23" with no commit or hash. It was not reproducible by identity, only by luck. I could not see what HEAD was on 2026-10-23; today's bytes equal the 26.6.4 bytes. [INFERENCE] the 2026-10-23 fetch got the same bytes, because README.md was not touched after 2026-03-04.
- Recheck command in the entry (`curl -fsSL …/HEAD/README.md | grep -c 'sasquatch'` -> 3): re-run today, prints `3`. Matching lines are U-tag lines 49, 52, 53 (confirmed by `grep -n`). Note: it counts lines, and the README is not minified, so QUALITY #13 is satisfied.

## Located quotes (each ≤25 words, contiguous, raw bytes)

Unblob README (U-tag, `## Installation` line 35 → `### pip (recommended for most users)` line 37):
- U-tag:49 — "For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):" (11 words + link)
- U-tag:52 — `curl -L -o sasquatch_1.0.deb "https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_$(dpkg --print-architecture).deb"`
- U-tag:53 — `sudo dpkg -i sasquatch_1.0.deb && rm sasquatch_1.0.deb`
- U-tag:43 — "Then install the required external extractor tools. On Ubuntu/Debian:" (so the whole block, sasquatch deb included, is scoped to Ubuntu/Debian)
- U-tag:56,59 — "Verify that all extractors are available:" followed by `unblob --show-external-dependencies`

sasquatch README (D-master; setext headings, no `# sasquatch` heading):
- D-master:12 (under `About`, line 1) — "Very beta."
- D-master:4 — "a set of patches to the standard unsquashfs utility (part of squashfs-tools)"
- D-master:6 — "If the vendor has done something simple like just muck a bit with the header fields, `sasquatch` should sort it out."
- D-master:8 — "will attempt to automatically resolve such customizations via a brute-force method."
- D-master:17 (under `Prerequisites`, line 14) — "You need a C/C++ compiler, plus the liblzma, liblzo and zlib development libraries:" ; apt line 20: `sudo apt-get install build-essential liblzma-dev liblzo2-dev zlib1g-dev`
- D-master:26 (under `Installation`, line 23) — "The included `build.sh` script will download squashfs-tools v4.3, patch the source, then build and install `sasquatch`:"

## Per-sentence verdicts

| # | entry sentence / claim | verdict | evidence |
|---|---|---|---|
| 0a | Source line S106 cites § "Installation", `main`, HEAD | **supported, locator imprecise** | the text is in `## Installation` → `### pip` subsection (U-tag:35-53). "HEAD as fetched" is a floating pin; pin the `26.6.4` tag (`1fcc7a0a…`) + README sha256 above. |
| 0b | Source line S107 cites § "sasquatch" and § "Prerequisites" | **wrong locator** | D-master has no heading "sasquatch"; headings are `About` (L1), `Prerequisites` (L14), `Installation` (L23). "Very beta" and the patch description are under `About`. |
| 1 | "open `sasquatch` item is a producer-declared dependency, not a tool still to be discovered" | **supported** (U-tag:49), framing is lane-side interpretation | the README names it as a needed install. |
| 2 | "unblob's own README makes SquashFS support conditional on installing sasquatch" | **supported** | U-tag:49 "For SquashFS support, also install sasquatch". "Conditional" is a mild gloss: the README says install it for SquashFS support; it does not say SquashFS is unsupported without it. The installed handler does hard-require the executable: `unblob/handlers/filesystem/squashfs.py:25-26` `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"` (uv install, unblob 26.6.4) [observation, host]. |
| 3 | "publishes the install as a prebuilt Debian package from `onekey-sec/sasquatch` (`sasquatch-v4.5.1-6`), alongside the `curl`/`dpkg -i` commands" | **supported, still current** | U-tag:52-53. Release `sasquatch-v4.5.1-6` exists, published 2026-01-27T11:57:51Z, and is the latest release today (`releases/latest`). Assets include `sasquatch_1.0_{amd64,arm64,armhf}.deb`. The `.deb` version is `1.0` in the file name; "version 4.5.1" is the squashfs-tools base shown in the tag, and `sasquatch -version` on this host prints `unsquashfs version 4.5.1 (2022/03/17)`. The entry never states the deb is "1.0"; adding that is advisable. |
| 4 | "So the lane's 'AUR only' framing describes one packaging route, not the only route." | **supported as inference; scope gap** | the lane's "(AUR)" wording is lane-side (ground F1); not checked here. The README route is Ubuntu/Debian-only and uses `dpkg --print-architecture` + `dpkg -i`; this host has `ar` but no `dpkg` (`command -v dpkg` empty), so on this Arch host the README commands do not run verbatim. Not stated in the entry. |
| 5 | sasquatch "is a patch set over the standard `unsquashfs` (squashfs-tools)" | **supported** | D-master:4. |
| 6 | "header-field mutations are handled directly" | **supported, slightly strong** | D-master:6 says "should sort it out"; "handled directly" drops the hedge. |
| 7 | "changed LZMA compression options or their storage in compressed blocks are resolved by a brute-force method" | **supported, hedge lost** | D-master:8 "will attempt to automatically resolve … via a brute-force method" — an attempt, not a guarantee. |
| 8 | "self-described as 'Very beta'" | **supported** (quote located, D-master:12) | exact; 2 words. |
| 9 | "prerequisites are a C/C++ compiler plus `liblzma-dev`, `liblzo2-dev`, `zlib1g-dev` headers" | **supported** | D-master:17 and :20 (the `-dev` names come from the apt line; the prose says liblzma/liblzo/zlib development libraries; the apt line also installs `build-essential`). Debian package names only. |
| 10 | "`build.sh` downloads squashfs-tools v4.3, patches it, and builds" | **supported, incomplete** | D-master:26 also says it installs. Note this describes devttys0 upstream (4.3 base), which is a different build from the `.deb` (4.5.1 base); the entry says so in the caveat. |
| 11 | (a) "`sasquatch` absence on this host is a packaging/build decision, not a discovery gap" | **stale** as a host fact | on 2026-10-26 `unblob --show-external-dependencies` prints `sasquatch ✓` and `sasquatch-v4be ✓` (`~/.local/bin/sasquatch` 382824 B, `sasquatch-v4be` 436232 B, both mtime Oct 26 01:22, installed by L1). The entry's inference is not refuted but the premise "absent" no longer holds. Host-state sentence is not from either README anyway. |
| 12 | (b) "prebuilt `.deb` is a second, non-AUR path for the operator" | **supported as inference** | U-tag:52-53; see #4 on dpkg absence on this host. |
| 13 | (c) "'sasquatch is very beta' is the producer's own self-assessment, so a failed SquashFS extraction cannot be read as 'the image has no SquashFS'" | **first half supported; second half inference** | "Very beta." is D-master:12. The conclusion about failed extractions is the author's reasoning, not in either README; it should be labelled inference (QUALITY #5). Note the "Very beta" quote is for the devttys0 README; the onekey `.deb` README says nothing equivalent (see #14). |
| 14 | Caveat: ".deb is built from onekey-sec's fork (tag `sasquatch-v4.5.1-6`)" | **tag supported, "fork" unsupported by cited sources** | tag/release exist. Neither cited README says "fork". GitHub API for `onekey-sec/sasquatch`: `"fork": false`, `default_branch: main`, `pushed_at 2026-04-13T11:44:49Z`, `archived: false`, description null. The repo's own README (`…/onekey-sec/sasquatch/main/README`, no `.md`) opens with an unrelated "NEWS … release was meant to be today (10th March)" text, so it does not name devttys0 and carries no "Very beta". The fork relationship is not established by any retained source in the entry. |
| 15 | Caveat: "lane's own REA wrapper pins Unblob 26.6.x" | **supported by lane records, not by the READMEs** | `corpus/knowledge/2026-10-13-r2-firmware-probe.md:36` ("accepted releases are Unblob 26.6.x (verified with 26.6.4)") and `…r4u-01-firmware-deep.md:7` (unblob 26.6.4). Entry should cite those paths. |
| 16 | "operator must confirm the package satisfies the *pinned* unblob's expected sasquatch" | **reasonable, now partly answerable** | unblob 26.6.4 expects two executables, `sasquatch` and `sasquatch-v4be` (`squashfs.py:25-26`); the README's own check is `unblob --show-external-dependencies`, which the entry omits and which reports both ✓ here. The README does not state which sasquatch version the pin expects. |
| 17 | "Upstream `devttys0/sasquatch` and the onekey fork are different builds of the same idea; this row cites both" | **partly wrong** | the row cites the unblob README (which links onekey-sec) and the devttys0 README; it never cites an onekey-sec/sasquatch README, and that README does not describe the idea at all (see #14). Also the devttys0 README is stale: last push 2023-05-23 (`pushed_at`), `archived: false`. The "different builds" claim is supported only by base version (4.3 per D-master:26 vs 4.5.1 per host `sasquatch -version`). |
| 18 | `ground: F1 — "sasquatch (AUR) — unblob squashfs recursion; 7z fallback covers today"` | **not testable from the READMEs** | lane-side ground; nothing in either README bears on the 7z fallback. |

## Other findings

1. Source-ID collision: lane `corpus/SOURCES.md` at HEAD `d2e46ef5…` already uses `S106` for the GNU binutils readelf row (and no S107). The entry labels unblob README as `S106` and sasquatch README as `S107`. If admitted into the lane, the labels collide; renumber at admission (or state they are merge-local ids).
2. The unblob README sentence on the deb is under "On Ubuntu/Debian" (U-tag:43) — the entry's "publishes the install as a prebuilt Debian package" is accurate, but the entry should say Debian/Ubuntu-scoped.
3. QUALITY #4 (artifact identity) and #8 (version pins): the entry pins no commit/hash for either README and does not pin unblob 26.6.4 or the sasquatch `.deb` file sha256; today's values above fill this. #7 (not examined): the entry does not say that the `.deb` contents/behaviour were not examined and that the sasquatch binary was not exercised on a SquashFS carrier; this seat did not do so either. Only `sasquatch -version` and `unblob --show-external-dependencies` were run.
4. Mild overstatement scattered: hedges dropped ("should sort it out", "will attempt") in sentences 6-7; restore them.

## Recommendation under `corpus/QUALITY.md`

**Refuse as written; admit after a small fix.** Every README-grounded factual sentence on install routes (#2, #3, #5, #8, #9, #10) is supported and still current today (`26.6.4` tag README ≡ HEAD README; release `sasquatch-v4.5.1-6` still the latest), so the entry is not wrong in substance. It fails the bar on locators and identity, not on facts:
- #1/#42: S107 cites a non-existent § "sasquatch" (fix: `About`, line 12; `Prerequisites` L14-20; `Installation` L23-26) and supplies no located quotes.
- #4/#8: no commit/hash pin (add `26.6.4` = `1fcc7a0a584a70a96c31f5a276c20944d199a089`, README sha256 `6544d60f…3716`; D-master sha256 `f09961ee…fef`; `.deb` name `sasquatch_1.0_<arch>.deb`).
- #5: the "very beta ⇒ failed extraction ≠ no SquashFS" step and the "(a)" host-state step must be labelled inference; "(a)" is now stale (host has both executables).
- Unsupported: "onekey-sec's fork" (API `fork:false`; neither README says so); "different builds of the same idea" is supported only via base versions 4.3 vs 4.5.1.
- Add: the README's verify command `unblob --show-external-dependencies`, the `sasquatch-v4be` second executable, the Debian-only scope, and that `dpkg` is absent on this host.
- S106/S107 renumber on admission.

Re-checks used (all read-only): `curl -sS -o … https://raw.githubusercontent.com/…`, `sha256sum`, `grep -n -i -E 'sasquatch|squashfs|deb|dpkg|curl|apt'`, GitHub REST `git/ref/tags/26.6.4`, `commits/HEAD`, `commits?path=README.md`, `releases/tags/…`, `releases/latest`, repo metadata for `onekey-sec/sasquatch` and `devttys0/sasquatch`, `unblob --version` → `26.6.4`, `unblob --show-external-dependencies | grep -i sasq`, `sasquatch -version`.

Limits: the 2026-10-23 bytes the entry author saw were not retained anywhere I could open; the README HEAD bytes today equal the 26.6.4 tag bytes only. Unauthenticated GitHub API; some curl calls ended with `curl: (23)` after `head` closed the pipe (truncated display only, no data loss in the cited values). Did not extract or run the `.deb`, did not exercise sasquatch on a carrier, did not examine `unblob.org/installation`.
