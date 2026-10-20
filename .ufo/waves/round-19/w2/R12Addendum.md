# R12 addendum review — round 19 wave 2

**Reviewed revision:** `refs/heads/main` = `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (observed by `git rev-parse`, exit 0). The entry reviewed is `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`. Axes: **calibration** (source scope and consistency), **freshness** (live custody/identity rechecks), **depth** (prefix property and independent probes). Read-only review; no production edits, installs, REA/Ghidra, or carrier execution. The only write is this report.

## Findings, by severity

### Major — committed source-gap paragraph is stale and self-contradictory (calibration)

**Observation.** At committed main, entry `:47` says “Not grounded by any row” for the REA package-source claims and `rea-agents@6.7.0`, then asserts `grep -n -i -E 'rea-agents|npm' corpus/SOURCES.md` has “no match.” But committed `corpus/SOURCES.md:43` is S037, explicitly naming `rea-agents`, `npm`, and the registry URL; its `used-by` includes this very knowledge entry. The same entry’s committed closing line `:71` says the package identity “is now also registered as S037.” The no-match statement is false at the revision containing it, and the “not grounded” phrase contradicts the later S037 statement unless narrowly limited to local package-source hashes / Evidence-ID semantics.

Commands / evidence:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show refs/heads/main:corpus/SOURCES.md | grep -inE 'rea-agents|npm'
# exit=0; S037 match at SOURCES.md:43 (and the round-19 search-log match at :71)

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show refs/heads/main:corpus/SOURCES.md | grep -n 'arc3-r12-go-evidence-id-domain'
# exit=0; S037 row at :43 lists the entry as used-by

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show refs/heads/main:corpus/SOURCES.md | grep -n 'S039'
# exit=1; no S039 row in committed main
```

**Inference.** The w1 “no row” observation was true before S037 was opened, but it was integrated unchanged alongside S037. This repeats the stale-status-clause defect class noted in `corpus/lessons/round-12.md:16` (row 5). It is actionable because the committed entry now presents a false scope statement, even though its closing sentence partly corrects it.

**Pending correction observed, not committed.** `git ls-files -m` listed both the entry and `corpus/SOURCES.md`; `git diff refs/heads/main -- corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` showed a 2-insertion/2-deletion replacement in the addendum region. The worktree replacement says “Grounding limits and in-round source-index correction,” indexes the REA package-source and measured-envelope claims by S039, and states S037 covers published package identity only, not the Evidence-ID projection. The worktree `corpus/SOURCES.md` contains S039, absent from main. Land the corrected entry and S039 row together; committing only the entry would leave a dangling S039 citation. The edit remains within the appended region: the original entry bytes still prefix the worktree file (depth check below).

### Answer — S037’s scope is published identity/integrity/provenance, not analyzer behavior (calibration)

**Observation.** Committed `corpus/SOURCES.md:43` scopes S037 to “Publish identity and integrity of rea-agents@6.7.0 as served by the npm registry, with its SLSA provenance source commit; not the package's runtime behaviour.” Its anchors are registry `dist.integrity`, `dist.shasum`, attestations, packument publication time/latest tag, and the SLSA source commit. Committed `LOG.md:2232` independently says “S037 supports publication identity only”; the claims amendment also scopes it to the published version identity.

**Conclusion.** Yes, with that precision: S037 supports the published package’s identity/integrity and provenance claim. It does **not** establish the local npx cache’s individual file hashes, the `inspect_go_binary` Evidence-ID projection, or runtime behavior. The live package-file hashes below are local observations against the retained `package-source-hashes.txt`; they are not registry evidence. The committed closing sentence at entry `:71` is safe only if “package identity” means *published* package identity. The pending worktree wording is clearer.

## Verified facts and depth checks

### Append-only property — holds

**Observation.** Extracted the baseline and main versions of the entry into `/tmp/kr19-r12a/base.md` and `main.md`; their sizes are 8,350 and 14,533 bytes. The worktree copy is 14,697 bytes.

```text
cmp --bytes=8350 /tmp/kr19-r12a/base.md /tmp/kr19-r12a/main.md
# exit=0: all baseline bytes match the start of main
cmp --bytes=8350 /tmp/kr19-r12a/base.md /tmp/kr19-r12a/wt.md
# exit=0: all baseline bytes match the start of the pending worktree version
cmp /tmp/kr19-r12a/main.md /tmp/kr19-r12a/wt.md
# exit=1: versions differ at char 9485, line 44 (the pending addendum correction)
```

Thus the original entry remains a byte prefix at both committed main and the observed pending edit. The pending replacement is in the appended addendum, not the pre-existing entry body.

### Custody legs and addendum line anchors — confirmed

**Observation.** `find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round12 -ipath '*pre*pair*' | wc -l` returned `0` (exit 0). Both `receipts/config-post-only.txt:6` and `config-post-only-2.txt:6` label the captures unpaired. The first receipt records capture time `:4`, cwd/repo-HEAD `:8-9`, and config paths/hashes/stat values; the second has the same cwd/repo-HEAD at `:8-9`.

The addendum’s cited receipt facts match the files: latest ctime in the first receipt is Kimi at `:64` (`2026-10-19T19:09:51Z`); other ctimes are earlier at `:28`, `:46`, `:82`, `:100`. The first receipt `.bashrc` hash at `:75` is `7d2ca28a…`; the second receipt `:75` is `0cd3d560…`, with mtime/ctime at `:78/:82` of `2026-10-19T21:46:35Z`. These facts align with `corpus/lessons/round-12.md:14,35`. The cited cwd is the `.tower/worktrees/kaika/kaidoku-shokunin` path, not the lane path.

Live command:

```text
eval 'grep "^PATH:" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round12/receipts/config-post-only-2.txt; echo "---live---"; for p in $(grep "^PATH:" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round12/receipts/config-post-only-2.txt | sed "s/^PATH: //"); do sha256sum "$p" 2>&1; stat -c "mtime=%y" "$p" 2>&1; done; echo "exit=$?"'
# exit=0
```

Observed live: Devin `9159ca91…` and OMP `26607852…` differ from the second receipt (`16f496e6…` at `:21`; `38d2a1d0…` at `:39`); both mtimes are `2026-10-20 13:35:56 -0300`. Kimi (`14ef6259…`), profile (`6c6be761…`), and `.bashrc` (`0cd3d560…`) still match that receipt. Live `sha256sum /home/vgpnk/.bashrc` plus `stat` returned the same hash and `2026-10-19 18:46:35 -0300` mtime/ctime (exit 0). These corroborate addendum items 1–6 and `corpus/lessons/round-18.md:88-89`; no zero-drift/pre-pair claim is made.

CR-4 mtimes were independently checked:

```text
stat -c '%n mtime=%y' <CR-4 base-1.json> <CR-4 copy-a.json> <CR-4 copy-b.json>
# exit=0; 2026-10-19 16:45:36.184, 16:45:37.099, 16:45:37.556 -0300
```

This matches addendum item 2 and precedes the receipt capture at `2026-10-19T21:38:54Z`. **Inference, already labeled in the addendum:** mtimes are last-write times, not proof of call time.

### Docker identity drift — confirmed; historical identity recoverable

**Observation.** Live commands:

```text
sha256sum /usr/bin/docker && stat -c 'size=%s mtime=%y' /usr/bin/docker && pacman -Qo /usr/bin/docker
# exit=0; SHA-256 566a4e83c1f148720e9628fbee98afcbe00867f0bfec819786f900c40f90d41a;
# size 30487344; owner docker 1:29.9.1-1

grep -n 'upgraded docker' /var/log/pacman.log
# exit=0; line 2668: [2026-10-20T09:16:36-0300] upgraded docker (1:29.7.2-1 -> 1:29.9.1-1)

ls -d /var/tmp/kaidoku-cr4-r12 /var/tmp/kaidoku-r12-c1
# exit=2; neither retained-copy directory exists
```

This confirms entry `:7`’s old-hash precondition is stale on the live host, and item 8’s retained copies are absent.

**New depth result (read-only; no execution).** The cached 29.7.2 package exists. Extracting its `usr/bin/docker` gives exactly the recorded old identity:

```text
bsdtar -xOf '/var/cache/pacman/pkg/docker-1:29.7.2-1-x86_64.pkg.tar.zst' usr/bin/docker | sha256sum
# exit=0; 70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9
```

That equals `identity.txt:1` and the entry’s recorded hash. The addendum ends item 7 with “its extracted binary has not been verified”; this review closes that gap. **Inference:** the old subject bytes are recoverable offline from the package cache, so the old-hash precondition can be restored using those bytes; no claim is made that the current `/usr/bin/docker` is the old binary.

### Package custody and retained result checks — confirmed

```text
sha256sum <npx-cache>/node_modules/rea-agents/package.json <...>/dist/domain/evidence.js <...>/dist/domain/canonicalDigest.js <...>/dist/application/go/GoBinaryService.js <...>/dist/go/GoBinaryProvider.js
# exit=0; 3f6c47fb…; a3fb9f02…; f46d6bd4…; 5494185f…; bdea4f88…
grep -m1 '"version"' <npx-cache>/node_modules/rea-agents/package.json
# exit=0; "version": "6.7.0"
```

All five hashes match `.ufo/waves/arc3-loop1-round12/claims/c1/CR-4/evidence/package-source-hashes.txt:2-6`. Entry anchors `:11,13,15,19-25,30` were checked against the cited package/source and retained records. `identity.txt:1-6` and `recompute-results.txt` / `integration/c1/live-recompute.txt` match the entry’s subject hashes and stored/copy IDs (`:19-25`). `integration/c1/reconcile-all-go-ids.txt` ends with `records=27 matched=27 …` and `exit=0`; `base-1.json` contains `go1.26.5-X:nodwarf5` and `github.com/docker/cli/cmd/docker`, as cited at entry `:24-25`. SOURCES anchors S024 `:30`, S025 `:31`, S026 `:32`, S031 `:37`, lesson anchors `round-18.md:88-89`, `round-12.md:14,35`, and `round-12-verifier-spotcheck.md:17` all matched the addendum’s descriptions.

## Minor notes

- Entry item 6 abbreviates the OMP hash as `266078…` (six hex digits); live value begins `26607852…` and matches the claim. Cosmetic, not a false hash.
- Live `/usr/bin/docker` mtime is `2026-10-15 10:58:57 -0300`, before the logged upgrade. The addendum does not use mtime to date the package; pacman’s preserved file mtime must not be treated as install time.
- The worktree is broadly modified (including the entry and SOURCES); findings above distinguish committed main from pending integration. The worktree correction also adds S039, which is absent from committed main. Review/measure the final landed artifact, not an uncommitted mixed state.

## Residual risk and verification gaps

- **Committed main still has the stale :47 claim.** The observed worktree correction is not committed; if closure is at `279e8b1`, the contradiction ships. If it lands, recheck the final integrated entry and ensure the S039 row lands with its citation.
- I read the committed S037 registry row for scope but did not independently refetch npm metadata or verify its attestation/digest; that is outside this addendum review’s source-scope question.
- Custody receipts are post-only. The addendum correctly treats mtimes as non-call-time evidence and does not claim a same-round pre-pair or continuous custody.
- No tools were installed or updated; none was needed. No builds, tests, or broad suite were run.