# R36W2ScoutS111 — S111 re-open, sentence check, tier check

Seat: scout, leaf, read-only. Judged on coverage, calibration. Lane tip read: `6f2ba761` (git rev-parse HEAD at read time; entry last touched by `ffc81341`).
Tools installed: none. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ScoutS111` (removed at the end; nothing cited from it survives except as quoted below).

## 1. S111 re-opened (observed)

Command: `curl -fsSL -D hdr.txt -o r.md https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` → exit 0, HTTP/2 200, `date: Mon, 26 Oct 2026 05:00:48 GMT`, etag `"ffa9202a…36fd"` (varnish, `x-cache: HIT`).

| fact | row/entry says | observed | verdict |
|---|---|---|---|
| line count | 30 | `wc -l` 30 (`cat -A` shows 30 numbered lines, last is the closing fence) | agree |
| bytes | (not stated) | 1050 | — |
| sha256 | `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` | `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` | agree (full 64 hex) |
| line 12 | "Very beta." | `12: Very beta.` | agree, exact |
| line 17 | build prerequisites | `17: You need a C/C++ compiler, plus the liblzma, liblzo and zlib development libraries:` | agree, exact |
| line 26 | build.sh downloads squashfs-tools v4.3 | `26: The included \`build.sh\` script will download squashfs-tools v4.3, patch the source, then build and install \`sasquatch\`:` | agree, exact |

Also read: line 4 "a set of patches to the standard unsquashfs utility … hacked-up vendor-specific SquashFS implementations"; line 6 "muck a bit with the header fields"; line 8 "changes to the underlying LZMA compression options … brute-force method".

Extra provenance I opened (git, bare blobless clone of `https://github.com/devttys0/sasquatch.git`; GitHub REST API returned HTTP 403 to every call here, so no API facts are used):
- `git ls-remote … HEAD` and `refs/heads/master` = `bd864a1b037bf57ca7d64a292a60ba0d6459611f`; `git log -1 master` = 2021-03-24T20:21:17-04:00 "Merge pull request #38 from eacmen/patch-1".
- `git show master:README.md | sha256sum` = `f09961ee…1fef` (same bytes as the raw URL).
- `git blame -L12,12 master -- README.md` → `992e6004 (devttys0 2014-08-16 21:47:38 -0400 12) Very beta.` — the "Very beta." line is from **2014-08-16**.
- `git log -- README.md` newest = `1afaf5f9` 2015-12-29 "Removed squashfs-tools source code, updated README". The README bytes have not changed since 2015-12-29; the branch tip moved last on 2021-03-24 (via a `build.sh` edit, `82fb587a`).
- `master:build.sh` (fetched raw, exit 0): header comment "Script to download squashfs-tools v4.3, apply the patches…", `wget …/squashfs4.3/squashfs4.3.tar.gz`, `patch -p0 < ../patches/patch0.txt`. So README line 26 is borne out by the script it describes.

## 2. Sentence-by-sentence on `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`

Sentences that cite S111 (directly or by the contrast with it), with my verdict.

1. **Line 2 (source line).** "S111 — … branch master, 30 lines, sha256 f09961ee…1fef; line 12 "Very beta."; line 17 build prerequisites; line 26 build.sh downloads squashfs-tools v4.3". **Agree** on every number and quote (§1). **Disagree on pinning:** S111 is pinned by *branch name + sha256 only*. No commit is named, although `master` = `bd864a1b…` was one `git ls-remote` away. Line 8 of the same entry says the three corrections include "pins by document instead of a floating `HEAD`" and "both sources re-opened … pinned by tag/commit and sha256". That is true of S110 (tag 26.6.4 = commit `1fcc7a0a…`) and false of S111 (floating `master`). The sha256 does pin the bytes, so the defect is cosmetic for byte identity, but the "pinned by tag/commit" sentence over-generalises. Also: the line-4 `recheck:` command covers S110 only; the S111 row says `recheck 180d` with no command in the entry.
2. **Line 3 (verified-at).** "both READMEs re-opened by the lane this round; access 2026-10-26T04:36:42Z, wave-1 seat … §2.3". **Agree.** `R36ScribeAssimilationGate.md` §2.3 holds the S111 row `| …devttys0/sasquatch/master/README.md | 200 | 1050 | 30 | f09961ee… |` with the 04:36:42Z→04:36:44Z window. My independent re-open at 05:00:48Z reproduced 1050 bytes / 30 lines / the same sha256.
3. **Line 8 (renumbering "staged S107 → S111").** **Agree.** Gate seat line 157 and `corpus/lessons/round-36.md:39` say the same, and `SOURCES.md:117` carries "(staged as package S107, renumbered by document)". (The gate seat's own plan text at lines 144–157 used a different draft numbering, S107/S108; the landed numbering is S110/S111 and consistent across lesson, SOURCES and entry.)
4. **Lines 16–17.** "A patch set over the standard `unsquashfs` that targets vendor-modified SquashFS (header mutations, changed LZMA options), self-described as "Very beta." (line 12)." **Agree on content** (lines 4, 6, 8 of the README; "targets" is slightly stronger than the README's "attempts"). **Two calibration notes, not errors:** (a) line 12 is a bare "Very beta." with no subject; it sits right after line 10's "Additional advanced command line options…", so reading it as a label for the whole project is the natural reading but still a reading; (b) it is a 2014-08-16 line (blame above) in a repo whose README has been frozen since 2015-12-29. The entry gives the label without its age.
5. **Lines 18–19.** "Its source build needs a C/C++ compiler plus the liblzma, liblzo and zlib development libraries (line 17), and `build.sh` downloads squashfs-tools **v4.3**, patches it and builds (line 26)." **Agree**, line 17 and 26 quotes exact; `build.sh` confirms the 4.3 download and patch (§1). The README's "build and install" is shortened to "builds"; harmless.
6. **Lines 20–22.** "The packaged onekey-sec binary the lane installed reports `unsquashfs version 4.5.1 (2022/03/17)` (`…/K1/after-run.json`), so the two routes are built on different squashfs-tools bases; this entry does not claim they behave identically." **Agree.** `corpus/evidence/round-36/c1/K1/after-run.json:10` is `"sasquatch_version": "unsquashfs version 4.5.1 (2022/03/17)"` with `sasquatch_sha256` `ad02d27a…4754` (line 9) matching the entry's host-state sentence. The "different bases" step is an inference from README 4.3 vs observed 4.5.1; it is correct (4.3 ≠ 4.5.1) but it is not labelled `[INFERENCE]` like consequence 2 is, and the 4.3 side rests on the README + `build.sh` text, not on a build the lane ran. Minor labelling gap. Side fact: the onekey-sec repo itself carries both a `4.3-sasquatch` and a `4.5-sasquatch`/`sasquatch-4.5.1` branch (`git ls-remote https://github.com/onekey-sec/sasquatch.git`), so "the two routes" differ by which tarball was packaged, not by a fixed property of the projects.
7. **Lines 30–31.** "[INFERENCE] Because the producer calls its own extractor "Very beta", a failed or partial SquashFS extraction is not evidence that an image holds no SquashFS; read the chunk records and gaps first." **Disagree with the premise; the conclusion survives.** Three problems:
   - "the producer" is ambiguous: the entry's heading "**Claim (producer contract)**" uses *producer* for unblob (S110). "Very beta." is devttys0's 2014 line, not unblob's or onekey-sec's.
   - The packaged binary the lane actually runs is **not** the devttys0 build. The entry's own line 22 ("does not claim they behave identically"), its "Not claimed" paragraph ("the devttys0 build's behaviour"), and the S111 row's scope ("not the onekey-sec packaged binary") all say so. Consequence 2 nevertheless carries a devttys0 2014 label over to the package whose repository `main` last moved 2026-04-13 ("feat: add support for v2 LZMA variant", `b34aa5ef…`). That is the transfer the entry elsewhere refuses.
   - The conclusion does not need the label: README line 8 already says the vendor-LZMA case is resolved "via a brute-force method" that "will attempt", i.e. a miss is possible by the README's own text, and the entry's own Not-claimed paragraph (vendor-mangled images) says the same. [INFERENCE] a safer premise is S111 lines 6–8 ("attempt to automatically resolve").
   The SOURCES `teaches` cell for S111 ("Read a partial SquashFS extraction against the producer's own beta label…") repeats the same premise.
8. **Lines 40–41 (Not claimed).** "… that the onekey-sec package is a fork of devttys0 (neither README says so)." **Agree.** README (S111) names no downstream; S110 only links onekey-sec/sasquatch. I could not confirm the wave-1 `"fork": false` API reading (my API calls: HTTP 403, same rate limit the gate seat hit). Independent git evidence that is consistent with the non-claim: after `git fetch https://github.com/devttys0/sasquatch.git master:refs/heads/dev` into a bare clone of onekey-sec/sasquatch, `git merge-base main dev` exited **1** (no common ancestor); `git grep -i 'devttys0\|sasquatch' main -- README README-4.5.1 INSTALL ACKNOWLEDGEMENTS CHANGES` returned nothing; onekey-sec has no `README.md` (its `README` is the squashfs-tools text). [INFERENCE] that does not prove the code is unrelated (a rebase or vendored patch would also show this); it only means a "fork" claim has no support in either repo's own text/history. The Not-claimed sentence stays right as written.

Summary: sentences 1 (pin wording), 4 (undated label), 6 (unlabelled inference) and 7 (premise) carry the disagreements; everything numeric and every quote agrees.

## 3. Tier B

Rules read: `/home/vgpnk/Projects/shokunin/CORPUS.md:93-97` (QUALITY.md:99 points to SOURCES.md for tier definitions, but `kaidoku-shokunin/corpus/SOURCES.md` holds none; the definitions live in fleet `CORPUS.md`, and `kaidoku-shokunin/corpus/CORPUS.md` does not exist — the task's "CORPUS.md" resolves to the fleet file). Text: "`tier` — scoped to `scope`, never global. **A**: primary or authoritative for that scope (spec, official docs, source code, original paper, **maintainer statement**, …). **B**: strong secondary (expert write-up with reproducible detail, survey, textbook). **C**: lead only."

Finding: **B is the wrong tier by the rule text; A fits.**
- The S111 scope cell is "sasquatch's self-description … and source-build prerequisites only". The devttys0 README is the project author's own statement about his own project, i.e. the primary/maintainer source for exactly that scope. It is not a write-up *about* sasquatch by a third party, which is what B names.
- Lane precedent: the other README-as-source rows are tier A — S005 GoReSym README (`code`, A), S017 View8 README (`code`, A), S110 unblob README (`docs`, A, same entry). S111 is the only README row of its kind at B (the other `docs`+B rows are S027 an issue discussion and S044 a handbook, both genuinely secondary).
- Nothing in `corpus/lessons/round-36.md` (Gate lines 28–39) records a reason for B; the lesson's S111 bullet gives URL, access, sha256 and the line-12 quote only. The staged package row's tier was carried over; `R36ScribeAssimilationGate.md` does not discuss it.
- Counter-argument I considered: B could be defended if the row's job were to describe the onekey-sec packaged binary the lane runs (then devttys0's README is a secondary source for it). But the row's own scope and the entry's Not-claimed paragraph exclude that use, and tier is "scoped to `scope`".
- Counter-argument 2: staleness (README bytes frozen since 2015-12-29, "Very beta." from 2014). The rules treat staleness through `recheck`/scope, not tier ("Tier is curation, not truth"). The row's `recheck 180d` is already there.
- Direction/risk: B understates, it is not tier inflation (`sources-census.sh` E10 fires only for community kind at A). Both A and B can serve as support; only C is lead-only. So no admission decision changes. Because CORPUS.md rule 2 makes tier immutable in place, a fix is a superseding row (`teaches` opening `supersedes S111 —`); I recommend none is needed beyond recording the reason, but a future reader auditing tier consistency will find S111 the lone outlier among README rows.

Verdict on the tier question: **disagree with B** (A per CORPUS.md:93-94 and the S005/S017/S110 precedent); severity low, understatement.

## 4. Nothing found / not examined

- No disagreement with S111's line count, sha256, or the three quoted lines.
- No evidence that onekey-sec/sasquatch is or is not a fork (API 403; history/grep only; see 8).
- Not examined: S110 sentences and the C1 evidence chain (other seats); the packaged binary's behaviour; whether `~/.local/bin/sasquatch` is built from the 4.5.1 tree beyond its self-reported version string.
- Commands that failed: `curl https://api.github.com/repos/devttys0/sasquatch*` and `…/onekey-sec/sasquatch` → exit 22 (HTTP 403); `curl …/onekey-sec/sasquatch/master/README.md` → exit 22 (404; the default branch is `main` and has no `README.md`).
