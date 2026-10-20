# R12Disclosure — round 19, w1 (seat KaidokuR19.R12Disclosure)

Scope: draft the append-only correction/disclosure addendum for
`corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`, answering
`corpus/lessons/round-18.md:88` (no `S###` row; no custody-leg disclosure). Read-only seat: this report is the only file written. No REA, Ghidra, or carrier execution. No tool installs or updates (none needed).

Observed base: lane `refs/heads/main` = `85589ac`. `git diff --quiet 8a8da7e… --` on the entry, `corpus/SOURCES.md`, and `corpus/lessons/round-18.md` → exit 0 (unchanged since round-19 baseline `8a8da7e`).

## Findings

### 1. Source rows (answers the `S###` half of round-18.md:88)

- **Grounded by existing rows:**
  - S024 (`corpus/SOURCES.md:30`): the buildinfo reader returns the version raw, including any `X:` token; absence of the magic means no record. Grounds the entry's `go1.26.5-X:nodwarf5` as reader output (entry:24) and the "observed artifact record" limit (entry:30).
  - S026 (`corpus/SOURCES.md:32`): the linker writes `X:<exp>` after a dash when the version has no `-`. Grounds the `-X:nodwarf5` form. Caveat: anchored to the go1.27.3 tree; the go1.26.5 linker was not opened (INFERENCE that it matches).
  - S031 (`corpus/SOURCES.md:37`): `GOEXPERIMENT=nodwarf5` disables DWARF 5 at build time. Grounds the token's meaning.
- **Not grounded by any row (gaps):**
  - Go 1.26.5 as a release: S025 (`corpus/SOURCES.md:31`) anchors `#go1.27.0`, `#go1.27.3`, `#go1.26.0` only.
  - REA package-source claims (entry:11,13,15,19-25) and the rea-agents@6.7.0 identity: `grep -n -i -E 'rea-agents|npm' corpus/SOURCES.md` → no output, exit 1. The 36 rows are S001–S036 (`corpus/SOURCES.md:7-42`).
  - S001–S003, S023 do not bear on `inspect_go_binary`; not cited.
- Registry-owner decision: whether to open a rea-agents package row (next free id S037). Not minted by this seat.

### 2. Custody legs (answers the custody half of round-18.md:88 and round-12-verifier-spotcheck.md:17)

- No pre-pair exists in the r12 tree: `find .ufo/waves/arc3-loop1-round12 -ipath '*pre*pair*'` → no output.
- Only two post-only receipts exist, both labelled unpaired (`.ufo/waves/arc3-loop1-round12/receipts/config-post-only.txt:6`; `config-post-only-2.txt:6`).
- CR-4 envelopes (`claims/c1/CR-4/evidence/base-1.json`, `copy-a.json`, `copy-b.json`) have mtimes 2026-10-19 16:45:36–16:45:37 -0300 (`stat`). First post-only capture is `2026-10-19T21:38:54Z` (`config-post-only.txt:4`). mtimes reflect last write, so call time is INFERENCE.
- One-sided ctime bound only: kimi ctime `2026-10-19T19:09:51Z` is the latest (`config-post-only.txt:64`); other paths' ctimes are older (`:28,46,82,100`). No earlier capture brackets the CR-4 leg.
- `.bashrc` changed between captures: sha `7d2ca28a…` (`config-post-only.txt:75`) → `0cd3d560…` (`config-post-only-2.txt:75`); mtime/ctime `2026-10-19T21:46:35Z` (`config-post-only-2.txt:78,82`). `round-12.md:35` records `CONTENT-DRIFT paths=4/5 drift=1` (`.bashrc` only). Cause: INFERENCE (operator-side).
- Both receipts captured from `cwd …/.tower/worktrees/kaika/kaidoku-shokunin`, `repo-HEAD de77d754…` (`config-post-only.txt:8-9`; `config-post-only-2.txt:8-9`), not the lane path.
- Current state: `sha256sum` of devin/omp configs → `9159ca91…`, `266078…` (receipts: `16f496e6…` at `config-post-only-2.txt:21`, `38d2a1d0…` at `:39`). `stat` mtimes `2026-10-20 13:35:56 -0300` for both. `round-18.md:89` records this as outside the lane. kimi `14ef6259…`, profile `6c6be761…`, post-only-2 `.bashrc` `0cd3d560…` match the last receipt.

### 3. Freshness of the entry's recheck line (entry:7)

- Precondition fails: `sha256sum /usr/bin/docker` → `566a4e83c1f148720e9628fbee98afcbe00867f0bfec819786f900c40f90d41a`; `stat` size `30487344`. Entry and `claims/c1/CR-4/evidence/identity.txt:1-6` record `70f68a77…`, `29327600` bytes.
- `/var/log/pacman.log`: `[2026-10-20T09:16:36-0300] [ALPM] upgraded docker (1:29.7.2-1 -> 1:29.9.1-1)`. `pacman -Qo /usr/bin/docker` → owned by `docker 1:29.9.1-1`. Read-only queries; pacman was not modified.
- The 29.7.2 package file is in `/var/cache/pacman/pkg/docker-1:29.7.2-1-x86_64.pkg.tar.zst`. Its extracted binary was not verified.
- Retained copies are absent: `identity.txt:2-3` names `/var/tmp/kaidoku-cr4-r12/…`; `ls` → No such file. Entry:22 names `/var/tmp/kaidoku-r12-c1/…`; also absent.
- Package custody intact: `package.json` and the four dist files hash to `package-source-hashes.txt:2-6` values (sha256sum, 2026-10-20; all match). npx cache `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` present, version `6.7.0`.

### 4. Checked and unchanged

- Entry copy IDs match on-disk files: `integration/c1/live-recompute.txt` (`ev_1633edb3…`, `ev_d38b041a…`); `claims/c1/CR-4/evidence/recompute-results.txt` (`ev_01c99c5d…`, `ev_4a5922f1…`). Entry:21-22 match.
- `integration/c1/reconcile-all-go-ids.txt` last lines: `records=27 matched=27 bundles=CR-1,CR-4,EX-2,EX-4,EX-5,EX-6,EX-8`, `exit=0`. Entry:25 matches.
- Entry:24 `go1.26.5-X:nodwarf5` and `github.com/docker/cli/cmd/docker` appear in `claims/c1/CR-4/evidence/base-1.json` (grep match).
- Entry has zero `S0xx` tokens and zero `custody` tokens: `grep -c` → 0 and 0 (round-18.md:88 holds).
- Package anchors: `dist/domain/evidence.js:159` `semanticProjection`, `:183` `computeEvidenceId`; `dist/domain/canonicalDigest.js:8` `digestCanonicalValue`, `:63` sorted keys; `dist/application/go/GoBinaryService.js:54-66` (`createEvidence`, `path`, `artifact-path`); `dist/go/GoBinaryProvider.js:122` doc, `:140` `inspect`.

### 5. Commands and exits (this seat)

- `git -C . cat-file -t 8a8da7e…` → commit, 0; `git diff --quiet 8a8da7e… -- <3 files>` → 0; `git rev-parse --short refs/heads/main` → `85589ac`.
- `sha256sum` (5 config paths, 5 package files, `/usr/bin/docker`) → 0.
- `stat -c …` (docker, configs, CR-4 envelopes, receipts) → 0.
- `pacman -Qo /usr/bin/docker`, `pacman -Qi docker` → 0; `grep -i docker /var/log/pacman.log` → 0.
- `ls /var/cache/pacman/pkg | grep …` → 0; `ls /var/tmp/kaidoku-*` → 2 (absent).
- `find .ufo/waves/arc3-loop1-round12 -ipath '*pre*pair*'` → no output (0).
- `grep -c 'S0[0-9]{2}'` and `grep -c -i custody` on the entry → counts 0 with exit 1 (zero-match).
- Python JSON read of `base-1.json` meta → `{"command":"inspect-go-binary","duration":"32ms"}`.
- No REA, Ghidra, or carrier run. No lane file written.

### 6. Out-of-scope / for the L1

- Entry body is not edited by this draft; the addendum is append-only.
- The draft recommends no rows be minted; the registry decision is the L1's.
- The 2026-10-20 docker upgrade and the devin/omp rewrite are fleet/operator-side (`round-18.md:89`); reported, not acted on.
- Open question for the L1: the custody-leg bound in the draft is one-sided and rests on ctimes, not a pre-pair.

## Draft

## Addendum (2026-10-20, round 19) — append-only; the entry above is unchanged

Answers `corpus/lessons/round-18.md:88` (no `S###` row; no custody-leg disclosure) and `corpus/lessons/round-12-verifier-spotcheck.md:17` (debt: "give the C1 entry an `S###` source row; disclose the unpaired custody legs in the entry"). Checks use on-disk artifacts only; no REA call was re-run.

### Source rows

Grounded by existing rows (`corpus/SOURCES.md`):

- **S024** (`corpus/SOURCES.md:30`): Go's buildinfo reader returns the version raw, including any `X:` token; absence of the magic means no record. Grounds the reported Go version `go1.26.5-X:nodwarf5` (entry line 24) as reader output, and the "observed artifact record" limit (entry line 30).
- **S026** (`corpus/SOURCES.md:32`): the linker writes `X:<exp>` after a dash when the version has no `-`. Grounds the form `-X:nodwarf5`. Scope: S026 is anchored to the go1.27.3 tree; the go1.26.5 linker was not opened, so that it matches is INFERENCE.
- **S031** (`corpus/SOURCES.md:37`): `GOEXPERIMENT=nodwarf5` disables DWARF 5 generation at build time. Grounds the meaning of the token.

Not grounded by any row:

- Go 1.26.5 as a released toolchain: S025 (`corpus/SOURCES.md:31`) anchors `#go1.27.0`, `#go1.27.3` and `#go1.26.0` only.
- The REA package-source claims (entry lines 11, 13, 15, 19–25) and the identity of rea-agents@6.7.0. No row names rea-agents or npm (`grep -n -i -E 'rea-agents|npm' corpus/SOURCES.md` → no match). Package identities are the hashes in `claims/c1/CR-4/evidence/package-source-hashes.txt:2-6`.
- Ghidra rows S003 and S023 and REA-skill rows S001–S002 do not bear on `inspect_go_binary` and are not cited for this entry.

### Custody legs

1. **No pre-pair for the live CLI legs.** No pre-pair receipt exists under `.ufo/waves/arc3-loop1-round12/` (`find … -ipath '*pre*pair*'` returns nothing). The only receipts are two post-only captures, each labelled unpaired (`.ufo/waves/arc3-loop1-round12/receipts/config-post-only.txt:6`; `receipts/config-post-only-2.txt:6`). The SOP says a zero-drift claim without its own same-round pre-pair is void (`SKILL.md:207-208`; section at `SKILL.md:319`). This matches the gap recorded at `corpus/lessons/round-12.md:14`.
2. **CR-4 envelopes precede the first post-only capture.** `claims/c1/CR-4/evidence/base-1.json`, `copy-a.json` and `copy-b.json` have mtimes 2026-10-19 16:45:36–16:45:37 −0300 (`stat`). The first post-only capture is `captured-utc: 2026-10-19T21:38:54Z` (`receipts/config-post-only.txt:4`). mtimes record last write, not call time; that the envelopes were written during the live call is INFERENCE.
3. **One-sided ctime bound, not a pair.** The latest ctime in the first post-only capture is kimi's, `CTIME_UTC_RENDER: 2026-10-19T19:09:51Z` (`receipts/config-post-only.txt:64`). The other four paths' ctimes are older (`:28`, `:46`, `:82`, `:100`). No earlier capture brackets the CR-4 leg.
4. **Operator-side edit between captures.** `.bashrc` sha changed from `7d2ca28a…` (`receipts/config-post-only.txt:75`) to `0cd3d560…` (`receipts/config-post-only-2.txt:75`). Its mtime and ctime are `2026-10-19T21:46:35Z` (`config-post-only-2.txt:78,82`). `corpus/lessons/round-12.md:35` records `CONTENT-DRIFT paths=4/5 drift=1` (`.bashrc` only). The cause, an operator edit, is INFERENCE; the lane does not write `.bashrc`.
5. **Capture location.** Both receipts were captured with `cwd: /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/kaidoku-shokunin` and `repo-HEAD: de77d754523afb673b4421d363fe89311644af4f` (`receipts/config-post-only.txt:8-9`; `config-post-only-2.txt:8-9`). They were not taken from the lane path.
6. **Current configs are outside the last receipt.** The devin and omp config hashes now differ from both receipts (`sha256sum`: `9159ca91…` and `266078…`; receipts `config-post-only-2.txt:21` `16f496e6…` and `:39` `38d2a1d0…`). Their mtimes are `2026-10-20 13:35:56 −0300` (`stat`). `corpus/lessons/round-18.md:89` records this rewrite as outside the lane. The kimi, profile and `.bashrc` hashes still match the last receipt. No custody statement in this entry extends to the current configs.

### Subject identity drift

7. **`/usr/bin/docker` no longer matches the recorded identity.** The entry records SHA-256 `70f68a77…` and 29,327,600 bytes (`claims/c1/CR-4/evidence/identity.txt:1-6`). On 2026-10-20, `sha256sum /usr/bin/docker` gives `566a4e83c1f148720e9628fbee98afcbe00867f0bfec819786f900c40f90d41a`, and `stat` gives 30,487,344 bytes. `/var/log/pacman.log` records `[2026-10-20T09:16:36-0300] [ALPM] upgraded docker (1:29.7.2-1 -> 1:29.9.1-1)`. `pacman -Qo /usr/bin/docker` names `docker 1:29.9.1-1` as owner. The recheck precondition at entry line 7 ("while `/usr/bin/docker` keeps SHA-256 `70f68a77…`") therefore does not hold on this host. The 29.7.2 package file remains in `/var/cache/pacman/pkg/docker-1:29.7.2-1-x86_64.pkg.tar.zst`; its extracted binary has not been verified.
8. **Retained copies are absent.** `identity.txt:2-3` names `/var/tmp/kaidoku-cr4-r12/copy-a/docker` and `copy-b/docker-copy`. Entry line 22 names `/var/tmp/kaidoku-r12-c1/`. Neither path exists (`ls` → no such file). Re-running the recheck needs fresh copies of a binary whose hash has changed (item 7).
9. **Package custody intact on this host.** The rea-agents 6.7.0 npx cache `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents` is present. `package.json` and the four dist files hash to the values in `package-source-hashes.txt:2-6` (`sha256sum`, 2026-10-20).

### Checked and unchanged

- The copy IDs at entry lines 21–22 match the on-disk files `integration/c1/live-recompute.txt` and `claims/c1/CR-4/evidence/recompute-results.txt`.
- `integration/c1/reconcile-all-go-ids.txt` reports `records=27 matched=27`, `exit=0` (entry line 25).
- The Go string `go1.26.5-X:nodwarf5` and module `github.com/docker/cli/cmd/docker` appear in `claims/c1/CR-4/evidence/base-1.json`.
