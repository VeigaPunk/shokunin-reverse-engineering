# A2NoveltyFull — C1 novelty premise vs all tracked history through 283aad7f

Evidence commands 2026-10-23T06:46:00Z–06:49:31Z. Report file observed on disk 2026-10-23T06:51:09Z, sha256 7f6ea113e798268b10961b477642aa391f1c966fb549875496d166e418f88440 (hash is of the file before this timestamp line was corrected).
Seat A2NoveltyFull. No REA. No tools installed or updated. No counter, predicate, or target edited.
Axes used: history span (every ancestor, not one tree), spelling span (ARM64X / ARM64EC / CHPE / hybrid PE, plus filename and false-positive cuts), run-versus-mention (a recorded live hybrid run versus a reserve sentence).

## Verdict

The frozen C1 novelty premise holds through base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.

Exercised:

- `PROVINCE.md` at that commit names `ARM64X` once, line 83, under `## Frontier` at line 73. Not under Core.
- No tracked path, at the base or in any of the 279 ancestor commits, records a run of a file the lane observed to be an ARM64X hybrid (CHPE metadata, a second architecture, or machine `0xA641`).
- Knowledge filenames never contain `arm64x`, `arm64ec`, `chpe`, or `hybrid`.

The frozen 17-line pathspec sweep is reproducible and incomplete. It misses `.ufo`, including a round-27 live clang / lld / `llvm-readobj` attempt. That same record says the product is not a genuine hybrid and that the seat did no REA run. That attempt does not falsify the premise under the reading above. It does falsify any reading that the lane never executed an ARM64X-targeted link.

Inference, marked where used: a COFF machine of `0xAA64` alone does not separate plain ARM64 from ARM64X. The round-27 load-config scan is the record that does.

## Bound

- Lane sandbox clone: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2NoveltyFull/lane.git-clone` (`git clone --shared --no-checkout` of the lane). Clone HEAD `f382e3b7978e6091a19ca93277c15a75c0016b43`. Every search below is pinned to `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`, not that HEAD.
- Git commands: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C` that clone. Read-only. Lane git/jj not written by this seat.
- Ancestors: `git rev-list 283aad7f` → 279 commits (exit 0). `jj -R /home/vgpnk/Projects/shokunin/kaidoku-shokunin log -r ::283aad7f` → 280 lines (exit 0); the extra id is jj's virtual root `0000000000000000000000000000000000000000`, not another change.
- Tracked tree at base: `git ls-tree -r --name-only` → 21698 paths (exit 0), including the `.ufo` tree. Working-tree files newer than the base were not searched.
- `df -h /fast` before any scratch write: 245G avail. No rebuild.

## Commands and exits

Frozen pathspec, re-run, not trusted as the bound. 2026-10-23T06:48Z.

```
git grep -n -i -E 'arm64x|arm64ec|chpe' 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525 -- corpus PROVINCE.md SKILL.md SCORECARD.md LOG.md
```

Exit 0. 17 lines. Same count the freeze receipt claims. `git ls-tree -r --name-only 283aad7f | grep -c -i -E 'arm64x|arm64ec|chpe'` → `0`.

Full text tree at the base. 2026-10-23T06:46:00Z.

```
git grep -n -I -i -E 'arm64x|arm64ec|chpe|hybrid[[:space:]_-]*pe|arm64[[:space:]_-]*ec|arm64[[:space:]_-]*x' 283aad7fe56d82f4ed4f8e43f099c2e1ceed5525
```

Exit 0. 112 lines. By top directory: `.ufo` 95, `corpus` 9, `SCORECARD.md` 5, `LOG.md` 2, `PROVINCE.md` 1. `README.md` (repo root) and `SKILL.md` contribute 0. `corpus/README.md` is inside the 9.

Filename spellings, base tree and every ancestor path via `git diff-tree --name-only -r -m` over all 279 commits (root additions still present are in the base `ls-tree`; deletions show up on the deleting commit).

```
grep -i -E 'arm64x|arm64ec|chpe|hybrid'
```

Base name hits: 0. Historical path hits: 0.

Pickaxe, all ancestors. Exit 0. 20 commits. `git log -m -i -G` with the same regex adds one merge, `7256d1da5d77bcb78d595add182cfa7fc5304439` (2026-10-18), whose matching hunks repeat the E6 census sentence and the README reserve line already in the tree. No commit after round-27 wave-2 (`29a76a637ad445f836b9b30382c0a6ee92a069a8`, 2026-10-22 12:54:46 -0300) adds or removes a matching line. Rounds 28–31 are inside the 279 and did not touch these spellings.

`PROVINCE.md` itself changes the spelling in exactly two commits: introduced `8f89dbda8b2e580c4b5c14aa1bba43a0dc2a54c4` (2026-10-13), reworded `40de38343398eee72aeebad7429f3bb99ab0a8dd` (2026-10-19). Both hunks sit under the Frontier preamble ("Claimed in MINT.md, not yet held" / "pruned from this section"). Never a Core row.

Tree-wide `git grep -n -I -i -E '0xa641|CHPEMetadata|coff-load-config' 283aad7f`: exit 0, 3 lines, all in `.ufo/waves/round-27/w2/CriticPlanned.md`.

## False positives cut from the 112

Exercised match text, not the acronym or the hybrid-PE name:

- `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch:92982` match `CHPE` inside `nGCHPEqx2W9`.
- Same file `:107900` match `CHpe` inside `RNfSRCHpeyF3rSpI73`.
- `.ufo/waves/arc2-loop1-round3/E9.md:120` match `ARM64-x` inside "an ARM64-x86-64-language match".

109 lines remain. They are reserve / planned-not-run / source-citation sentences, copies of those sentences in wave patches and scratch trees, the E6 absence census, or the round-27 CriticPlanned checks. No remaining line is an REA inspect or analyze of an ARM64X hybrid.

## Premise quotes (re-opened with git show at 283aad7f; ≤25 words)

`PROVINCE.md:73` heading `## Frontier`. `PROVINCE.md:83`: "Reserve: ARM64X hybrids (the 91MB Godot ARM64 template is held, arc2-r7)."

First landing, `8f89dbda` `PROVINCE.md` hunk, still that Frontier list: "Reserve: 91MB Godot ARM64 template, ARM64X hybrids." The 2026-10-19 edit only moves the Godot clause into the parenthetical and adds "is held, arc2-r7".

`LOG.md:1721-1722`: "no ARM64X carrier, analysis run, new knowledge entry, or numeric score change." `LOG.md:1744-1745`: "no live REA provider/session was probed; no ARM64X capability was attempted."

`corpus/lessons/round-13.md:4`: "no ARM64X capability, target execution, or domain-knowledge admission". `:57`: "No ARM64X sample was sought or required; no target binary or artifact was executed".

`SCORECARD.md:2108-2109`: "Primary: ARM64X hybrid PE analysis via Ghidra on one real host carrier". `:2129-2130`: "or an ARM64X capability. The prior planned ARM64X run is not pursued under this steer." `:2160-2161`: "ARM64X stays a frontier candidate requiring a real carrier and explicit steer". `:3128`: "The PE-subtype example is not runnable here (no ARM64X carrier on this host)."

`corpus/README.md:218`: "PE reserve: ARM64X hybrids; signal-desktop 38.5MB asar held r4-05". Repo-root `README.md`: no match.

`corpus/SOURCES.md:25` names S019, "ARM64EC and WoW64 CHPE Metadata Parsing", as a mined doc. `:117`: "no ARM64X carrier was required, no target was run, and it does not claim Ghidra/REA ARM64X support."

`corpus/knowledge/2026-10-13-r3-pe-arm64.md:42`: "larger ARM64 binary with jump tables / ARM64X hybrid PE, or exception-heavy". `:45` heading: "Candidate 2 — Godot `windows_release_arm64.exe` (not run)". `:71`: "ARM64X hybrid binaries, jump-table density, .pdata unwind edge cases". Those lines name a next frontier. The run log in the same file is `cli-arm64.exe`.

## Live runs that are not hybrid runs

Round-3 ARM64, not ARM64X. `corpus/knowledge/2026-10-13-r3-pe-arm64.md:59`: "timeout 900 npx -y rea-agents@6.4.0 analyze cli-arm64.exe --format json". `:20` records machine "IMAGE_FILE_MACHINE_ARM64 (0xAA64)". Filename `2026-10-13-r3-pe-arm64.md` has no `x` suffix.

Godot scale wall, plain ARM64. `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md:18`: "PE32+ executable for MS Windows 6.00 (GUI), ARM64, 8 sections". `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:3` titles a 91.6MB Godot ARM64 hold. `git grep` of `arm64x|arm64ec|chpe|hybrid` on those two files at the base: no lines (the combined grep that also included the r3 file returned only the two r3 lines above). Exit 0.

arc2 round-3 census, absence, file-headers only. `.ufo/waves/arc2-loop1-round3/E6.md:276-278`: "Method: `llvm-readobj --file-headers` per file". `:273` count "37 IMAGE_FILE_MACHINE_ARM64 (0xAA64)". `:280`: "No ARM64X hybrid PE was found". `:281-282`: "none of the 37 ARM64 files carries one — all are plain `0xAA64`". `:393`: "No ARM64X hybrid present." The file does not record `--coff-load-config` or `CHPEMetadataPointer`. Inference: that census did not print a CHPE directory; machine `0xAA64` is also what a real ARM64X image reports. The frozen sweep's prose already cites `:280`. This seat does not treat E6 alone as proof that no hybrid bytes existed on the host.

## Round-27 live ARM64X-targeted commands (not an REA hybrid run)

`.ufo/waves/round-27/w2/CriticPlanned.md`, present at the base, outside the frozen pathspec, not mentioned in `claims.json` `novelty_sweep`.

`:3`: "Read-only on the lane; no REA run; no install."

`:21` check 7, host scan, command text `timeout 600 python3 -I -B pe-scan.py /home /usr /opt /fast`, started 2026-10-22T15:36:39Z, finished 15:40:08Z, exit 0. Excerpt recorded there: `pe_files 633`, `0xaa64 38` (37 host files plus that seat's `hyb.dll`), no `0xa641` line. Then `llvm-readobj --coff-load-config` on each of the 37 at 15:41:00Z, exit 0: "35 print `CHPEMetadataPointer: 0x0`, 0 nonzero". Quote from the same line: "no ARM64X hybrid exists on this host".

`:22` check 8, synthetic build at 2026-10-22T15:37:49Z and 15:37:59Z in `arm64x/`: `clang --target=aarch64-pc-windows-msvc` and `--target=arm64ec-pc-windows-msvc` (exit 0), `lld-link -machine:arm64x -dll -nodefaultlib`. With stubs, link exit 0, warning recorded as "`__chpe_metadata` is missing for ARM64X target". `llvm-readobj --coff-load-config` "shows only `Machine: IMAGE_FILE_MACHINE_ARM64 (0xAA64)`, no CHPE metadata." Quote: "LLD 23.1.3 alone does not give a genuine hybrid".

`:23` check 9: `unzip -l` of Ghidra 12.1.4 jars, exit 0, finds `ImageArm64X.class`. Quote: "the gap is the carrier, not Ghidra." Not a carrier analysis.

`:41`: "`arm64x/hyb.dll` f7b12b54774fd043cee886b84d17829e9e30f1c2bf5b3ba27db1eb96f845e931 (not a genuine hybrid; see check 8)". That filename is not in any ancestor tree (path hits 0). The bytes are not a committed blob under another name that this spelling search can see; only the hash line is tracked.

This is a previous live toolchain run aimed at ARM64X. It is not a recorded run of an ARM64X hybrid file, and not an REA inspect. The premise's "no lane run of an ARM64X file" matches the seat's own observation. A wider gloss ("the lane never ran ARM64X-targeted commands") is false, and the frozen sweep did not show this seat.

## Knowledge filenames

Historical `corpus/knowledge/` paths matching `arm64|pe-|hybrid|chpe|coff` are only:

- `corpus/knowledge/2026-10-13-pe-surface.md`
- `corpus/knowledge/2026-10-13-r2-pe-e2e-proof.md`
- `corpus/knowledge/2026-10-13-r3-pe-arm64.md`
- `corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md`
- `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md`
- `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`

None of those names contain `arm64x`, `arm64ec`, `chpe`, or `hybrid`. No other knowledge filename in the 279 commits does either (the broader `arm64x|arm64ec|chpe|hybrid` path filter was 0).

## What the 17-line sweep got right, and what it left out

Right, re-checked: those 17 lines are frontier, reserve, planned-not-run, or the S019 source row. Filename count 0. `PROVINCE.md` one Frontier line. E6 `:280` is cited in the freeze prose even though E6 is outside the pathspec.

Left out of the pathspec, found here: 95 `.ufo` lines. Almost all repeat the reserve sentence inside patches, scratch `PROVINCE.md` copies, citation-drift fixtures, and the interactive-session transcript (the `__advisor.jsonl:29` match is the same "PE reserve: ARM64X hybrids" quote, not a run). The one substantive omission is CriticPlanned checks 7–9. `.ufo/waves/arc3-loop1-round12/integration/records-draft.md:117` is a plan sentence ("Primary candidate: ARM64X hybrid-PE analysis via Ghidra"), consistent with SCORECARD `:2108`, not a run. Round-4 wave notes say the reserve was untested ("only ARM64X hybrids remain unexercised"; "no corpus entry runs one"). Those notes agree with the premise; they are not an independent run.

## Evidence hashes (scratch outputs)

| file | sha256 |
| --- | --- |
| grep-base-text.txt (112-line full grep) | `af1564d86efbc0e894dbe51c0a4775198e24cc107ac275c172bc212ed949e8ec` |
| frozen-repro.txt (17 lines) | `50af1245f34ee91caba406de7f7a06434d6eae2cf82d5ca4ede99ab39eaa8d16` |
| pickaxe-commits.txt | `ff1d26b95f3f018cac2ec98efd4ef9bb680c8ffa662860fd8f07c9b3b6002f5d` |
| all-names-base.txt | `9f31844ec665661d5e6916e5d7af00d932555fd5c305d06b94be6181ac6af84d` |
| rev-list.txt | `903d764ddfd96afbb0e718690dc9e4dacabe21695e8aa58852cfbbabf2a34c6a` |
| jj-ancestors.txt | `f57d715b0466716d4a5f29f8779eeb1ca77866c9edc42b5eedf70fd54a15a91b` |

Sandbox revision searched: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`. Clone HEAD left at `f382e3b7978e6091a19ca93277c15a75c0016b43` because `--no-checkout` clone points at the lane tip; no search used that tip as the tree.

## Not claimed

Host disks outside the git tree were not re-scanned. Round-27 scratch files under `/fast/scratch/hyaku/kaidoku-r27/` were not re-opened; only the committed CriticPlanned record was read. No carrier binary was executed. No process was left running.
