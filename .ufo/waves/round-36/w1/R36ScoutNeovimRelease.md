# R36ScoutNeovimRelease — neovim v0.12.6 carrier provenance (K3/K4) and SOURCES row S109 draft

Date of observation: 2026-10-26 (fetches at 04:27Z UTC and a few minutes later). Advisory only; no lane file edited.

## Verdict
**Confirmed.** GitHub's published `digest` for both AppImages equals the sha256 frozen in `corpus/evidence/round-36/c1/carriers.json`, and an independent download hashes to the same value with the same size as the API reports.

| carrier | asset | API `digest` (sha256) | frozen carriers.json sha256 | downloaded sha256 (`sha256sum`) | API size = downloaded size |
|---|---|---|---|---|---|
| K3 | nvim-linux-x86_64.appimage | b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb | same (carriers.json:7) | same | 11454968 = 11454968 |
| K4 | nvim-linux-arm64.appimage | 8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2 | same (carriers.json:8) | same | 11356680 = 11356680 |

Commands (exit 0 each): `curl -sS https://api.github.com/repos/neovim/neovim/releases/tags/v0.12.6 | jq '.assets[]|select(.name|test("appimage"))|{name,digest,size}'`; `curl -sSL -o <f> https://github.com/neovim/neovim/releases/download/v0.12.6/<asset>` then `sha256sum`. API JSON (487 lines) sha256 `4ff9bb7bee2afbef0ed45c4062d3ab9e66da597a07319ccfe55623986912090c`, identical across two fetches; API `digest` lines 69 (arm64), 177 (x86_64) in that JSON. Release `tag_name` v0.12.6, `published_at` 2026-10-09T15:43:25Z, asset `updated_at` 2026-10-09T15:43:22Z (x86_64) / :23Z (arm64).

## Release page facts (observed)
- https://github.com/neovim/neovim/releases/tag/v0.12.6: "Nvim 0.12.6", released by github-actions 09 Oct 15:43, tag signed (verified, justinmk), commit `779c36969e31080503be2dfccbcc3f999e289606` (page shows `779c369`).
- **The release page as served to this fetch does not show the digests**: the Assets list is lazy-loaded ("Assets 14 / Loading"). The digest evidence is the API only; the page supports file names and install steps. [INFERENCE] a logged-in browser may render the per-asset digest; not observed here.
- Served HTML sha256 is not stable across fetches (`abf72ff6…`, `7baa3c22…` for two plain curls; the page embeds per-request nonces), so the page hash is NOT cited in the row; the API JSON hash is.
- Located quote (3 words, release page install step, served HTML line 759; arm64 twin at line 779): `Download nvim-linux-x86_64.appimage` (HTML: `<li>Download <strong>nvim-linux-x86_64.appimage</strong></li>`). Served HTML had 207,659 bytes in the capture that contained those line numbers (sha256 `7baa3c22fb23dd77c0da65cdfba42478fd28a42c007b10396eff1b859c7adbac`); line numbers are of that capture and may shift.
- The page's AppImage step also states the extract route: `./nvim-linux-x86_64.appimage --appimage-extract` then `./squashfs-root/usr/bin/nvim` (page line 763-764), consistent with the K3/K4 kind "type 2 AppImage with squashfs payload".

## Draft SOURCES.md row S109 (11 cells; single line; no pipe inside a cell)
Place it directly after the S106 row inside `## Registry` (S107/S108 are drafted by R36ScribeSources).

```markdown
| S109 | Neovim v0.12.6 release record — https://github.com/neovim/neovim/releases/tag/v0.12.6 (API https://api.github.com/repos/neovim/neovim/releases/tags/v0.12.6; assets https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-x86_64.appimage and https://github.com/neovim/neovim/releases/download/v0.12.6/nvim-linux-arm64.appimage) | dataset | A | Byte provenance of R36-C1 carriers K3 and K4 only (the two shipped AppImage files and their GitHub-published sha256 digests); not the AppImage payload contents, not sasquatch or REA behaviour | Tag v0.12.6 (commit 779c36969e31080503be2dfccbcc3f999e289606), release published 2026-10-09T15:43:25Z; API assets[] `digest` fields, served JSON SHA-256 4ff9bb7bee2afbef0ed45c4062d3ab9e66da597a07319ccfe55623986912090c (487 lines); release page install steps (served HTML line 759 x86_64, line 779 arm64) | Fix K3 and K4 to publisher-stated sha256 values `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` (x86_64, 11454968 bytes) and `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` (arm64, 11356680 bytes); located quote `Download nvim-linux-x86_64.appimage` | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Design choices: kind `dataset` (same as S094 Chinook release assets); tier A scoped to byte provenance of K3/K4 only; `mined` because used-by is the round-36 entry; recheck `on-release` (digest is a property of an immutable-tagged asset; recheck on a new v0.12.x only if carriers are re-fetched). The teaches cell is one learner benefit (fix carrier bytes to publisher-stated digests).

## Census check of the row (scratch mirror only)
Mirror = copy of lane `corpus/` with the row inserted after S106 and an empty placeholder for the entry path. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26` → exit 1 only because of two E11 findings on pre-existing rows S036 (`SKILL.md`) and S081 (`tools/round-27/xpin-attribute.mjs`), which are outside the mirrored `corpus/` tree (mirror artefacts). **No finding of any code (E01–E12, W01–W04) names S109.** The unmodified lane file validates `ok`, exit 0 (same command).
- Caveat: in the real lane, E11 will fire for S109 until `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` exists on disk (it did not at observation; checked by the mirror needing a placeholder). Land row and entry together.
- Id note: the lane registry's last row is S106; the round-36 staged-ids list (`.ufo/waves/round-36/assimilation/staged-ids`) starts S106 and includes S107–S109, so S109 is unused in the registry (grep of `corpus/SOURCES.md`: no S107–S109 rows).

## Limits / unresolved
- Release page digest display not observed (see above). The API `digest` field is GitHub's asset digest; it is not a publisher-signed checksum. Neovim also publishes `shasum.txt` in the release assets [INFERENCE from 14 assets; not opened]; not used.
- ELF-end/squashfs offset and payload contents of K3/K4 not examined (out of seat scope).

## Tools
None installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScoutNeovimRelease` (two ~11 MB downloads, page and API captures, mirror) removed at end of run; nothing under it is evidence.
