# R43W2C2Host — host-source and upstream-fallback attack

## Verdict

**No falsifier found on the assigned host-source surfaces.** The committed map distinguishes unavailable paths from live paths, and the fallback receipts identify the row-pinned upstream sources. The C2 score receipt itself is an honest stop, not a green: its `sources_numstat_three_additions` check is false and `exit_code` is 1, despite gate exit 0 and 136/136 content checks. I do not infer C2 success from the summary fields.

**Measured revisions:** lane tip read at `5856614ac4bf7f2363bbcd1956644474a82108e5`; committed C2 receipt evaluates `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`, with frozen plan revision `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. The SOURCES/map worktree SHA-256 values match the C2 receipt's values at `09ab56b8…`; committed artifacts/copies read at the lane tip have the hashes below. The lane had unrelated user changes (`SCORECARD.md`, `SHONEN.md`, `.ufo/waves/round-43/w2.ready`, `.ufo/waves/round-43/w2.ready.partial`, and the wave directory); none were changed.

## Findings by row

- **S035 — absent-host classification and Go-tag member identity: supported.** Both live Go `src/internal/abi` directories are absent on this host. The map marks both source paths absent in its note; its copies are not described as live-equal. The fallback receipt `R43RevLocalsrc/receipts/go-upstream-sha256.tsv` records the files from `go1.24.6/` and `go1.25.0/`; the verifier receipt names upstream identity against `golang/go@go1.24.6` and `@go1.25.0`, 28 members each. I independently read the two committed archives: each has 28 files, and each contains the three row-pinned members with identical hashes across tags: `map_swiss.go` `0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383`; `map_noswiss.go` `03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291`; `map_select_swiss.go` `c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718`. This supports matching row pins and cross-version identity; it does not establish live-host identity.
- **S081 — absent-host classification and npm pin: supported.** `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` is absent. The map explicitly calls this a “Pipe-absent resolution” and says the committed subset derives from the row-pinned `rea-agents-6.7.0.tgz`, not a live installation. The tarball receipt records SHA-256 `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`; the score's verifier stdout records this pin and the three member pins. Independently read the committed 3-file archive: the `dist/domain/evidence.js`, `dist/domain/canonicalDigest.js`, and `package.json` member SHA-256 values equal the full row pins (`a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`, `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`, `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`). No claim of live equality is made in the map or verifier evidence.
- **S048 — installed path is present now; tarball pin and member identity supported.** The 6.5.0 `dist` path currently exists, so I do not classify it absent. Its committed map note says the package-wide installed tree is larger than the copy bound and specifies 28 cited members, including the one package-relative `bridge/ghidra/ReaGhidraBridge.java`. I compared all 28 committed archive members read-only against the current installed package paths: 28/28 match. The C2 verifier receipt records all applicable member pins and `host-identity … 28 members`; the landing receipt says the tarball substrate was also checked. The current host comparison supports present-day equality only, not permanence. The receipt specifies pinned npm tarball SHA-256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` (also cited through S090/S092); the L1 C2 upstream scratch tarballs are now absent, so I did not freshly recompute the 6.5.0 tarball digest from its source bytes.
- **S082 — present-host records, no absent-object equality claim.** `/var/lib/pacman/local/tinyxxd-1.3.17-1/{desc,mtree}` and `/var/lib/pacman/sync/extra.db` are present. Map and verifier receipt classify these as present/live-host records; the C2 audit reports separate identities: local `desc`/`mtree`, and the repo database's `tinyxxd-1.3.17-1/desc` member. The receipt reproduces both package pins (`/usr/bin/tinyxxd` mtree digest `7b1e5d0c970afe68…`; sync `%SHA256SUM%` `3f84d7de243de139…`). It does not conflate the different installed and repository `desc` records or claim identity for an absent object.

## Stop evidence / calibration

Read `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json`: `checks_ok:false`, `sources_numstat_three_additions:false`, `exit_code:1`; gate exit 0, `rows_failed:[]`, `rows_checked:19`, `rows_total:137`, copy audit 136 checks/0 failures. Its `sources_numstat` is `4\t0\tcorpus/SOURCES.md`, while the frozen P43-C2 claim expected three additions. This defeats any interpretation that the C2 receipt is an overall green. The S035/S081/S048/S082 evidence does not repair or explain that clause, and no score rerun was attempted.

## Commands and read-only reproductions

All commands below ran against committed lane bytes/current host objects; no installation, VCS mutation, extractor, or firmware input was used.

1. Read frozen plan with `read` before inspecting lane tip; inspected `git log`, `git rev-parse HEAD`, and `git status --short`. Exit 0. Full measured lane tip: `5856614ac4bf7f2363bbcd1956644474a82108e5`.
2. Read S035/S048/S081/S082 row lines, committed `local-sources.json` entries, C2 score receipt, upstream fallback receipts, landing report and reverify table using `read`/`glob`. These are evidence reads, not tests.
3. `for p in <the seven host paths listed above>; do test -e "$p" ...; done` — exit 0. Results: Go 1.24.6 and 1.25.0 directories absent; S081 npx path absent; S048 dist present; S082 three records present.
4. `sha256sum` on all seven committed copy files — exit 0; results match map:
   - S035 archives: `8530a509c4d28765b68292bb5c3fda670fb53e8a8700dce90b0a567bf21a11d1` and `069d0c887b475efa4a4d98acc7803e2f56cdfd4812244457803d2c2a00fc0df3`.
   - S048 archive: `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`.
   - S081 archive: `11c07d925277ee136d430fe1e329151d39b63192ee866c2e54e64430dc89f42d`.
   - S082 files/record-member archive: `a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456`, `a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58`, `4c1d650f1528d17c0c9fd3000f5df257923e799e24dddd38c75edbe22e68bb31`.
5. Read-only Python `tarfile`/SHA-256 member check against those committed archives: exit 0. S035: both 28-file archives; all three pin hashes match across versions. S048: 28 files, 28 current-host member matches, zero mismatches. S081: 3 files, all three full member hashes match the cited row pins. No extraction to disk.
6. Checked `/fast/scratch/hyaku/kaidoku-r43/l1-c2-inputs/{tgz/rea6.5.0.tgz,tgz/rea6.7.0.tgz,go1.25.0.src.tar.gz,go1.24.6.src.tar.gz}`: all absent. This limits fresh re-download/re-derivation; I rely on committed upstream fallback receipts for those sources.
7. Disk check: `df -h /fast/scratch /home/vgpnk` reported 584G and 590G available respectively; no disk-guard status file was found at the three checked conventional paths. No heavy probe ran.

## Evidence paths and hashes read

SHA-256 unless labelled otherwise:

- `corpus/SOURCES.md` — `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`.
- `corpus/evidence/local-sources.json` — `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`.
- `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` — `126b529eb5c3b0d61eaceb5f2e026eb3de9b0a9c2256239eabd86a23eaad9f4e`.
- `.ufo/waves/round-43/w1/artifacts/R43RevLocalsrc/receipts/go-upstream-sha256.tsv` — `52e2c1156e5f34e8327e9b9439dec764dc0dd00a01a6367636b0ec56fa2c7ef7`.
- `.ufo/waves/round-43/w1/artifacts/R43RevLocalsrc/receipts/tarball-sha256.txt` — `26c2f9f74b46bac2ff62599638ab88686fb55cddd958ab77b37ac57d097ec472`.
- `.ufo/waves/round-43/w1/artifacts/R43C2Land/receipts/reverify.tsv` — `011378f982269717c1e3a400b9ed9c85233875a9cbcedffa4f2da74fd86f5286`.
- `.ufo/waves/round-43/w1/R43C2Land.md` — `8fbf3188d02963cc5aa0ecd86bd9853f29e36b39d7c2068e3fa0b32826aa60ae`.
- Seven committed S035/S048/S081/S082 copy paths: hashes stated in the section above.

**Limitations / inference:** receipts establish what their committed verifier measured at their recorded revision; I did not recreate the upstream Go or npm source archives because those scratch inputs are absent. Current S048 equality is independently measured, but is not evidence that the installation will persist. The checks establish source-byte/member identity, not the substantive claims those sources make.