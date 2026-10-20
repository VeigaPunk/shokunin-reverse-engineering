# DraftS033Row — round 18 (author-side draft, not integrated)

Seat: `KaidokuR18.DraftS033Row`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on lane files; this report is the only write.

## Draft

### SOURCES.md registry row (11 cells, append after S032 at `corpus/SOURCES.md:38`)

```
| S033 | Ghidra pull request #9348, swiss-map Go 1.24/1.25 recovery, head a214355 — https://github.com/NationalSecurityAgency/ghidra/pull/9348 | community | B | Same subject as S032: the open, unmerged PR's identity and its proposed `internal/abi.SwissMapType` resolution, as the author's claim only | PR title `Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries`, state OPEN, head commit `a214355498e84aa86280be0c31c955aaf94f2d12` (`gh pr view 9348 -R NationalSecurityAgency/ghidra --json headRefOid,state,title`, read 2026-10-20); accessed 2026-10-20; page sha256 `8a94af638bc8941e705313d9382ca52c792c7f0e6b324cb8fc26fc08ce9a4f09` fetch-time only (`curl -sSL` of the same URL gave `dab89ce7d80778da1ecefc2120f4cb779cb411c414f21b4ddc4673d533eaeddb` in the same session) | supersedes S032 — S032 keyed the page on a sha256 that does not reproduce, so this row names the PR by title, OPEN state and head commit `a214355`, the revision whose commit messages carry the mechanism claim; the claim stays tier B | mined | 2026-10-20 | 90d | corpus/lessons/round-18.md |
```

Notes for L1 integration (not part of the row):
- `status` is `mined` only if `corpus/lessons/round-18.md` cites S033 (the rule at `CORPUS.md:103`). If the lesson does not cite it, set `status` `queued` and `used-by` `—`.
- S032 keeps its row. Per `CORPUS.md:116-118`, its `status`, `recheck` and `used-by` may change in place only; this draft proposes no S032 change except an optional `used-by` append if the round-18 lesson cites S032.
- The round-18 lesson should log S033 as a new row in its registry-transitions list (as `corpus/lessons/round-17.md:74` did for S024–S032).

### Lesson `## Gate` rows (table format of `corpus/lessons/round-17.md:46`; access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S033 | https://github.com/NationalSecurityAgency/ghidra/pull/9348, `<title>` (fetched HTML line 286) | Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries |
| S033 | https://github.com/NationalSecurityAgency/ghidra/pull/9348, force-push timeline event (fetched HTML lines 2837-2850) | force-pushed the fix/golang-stripped-type-markup-master branch from 5fe0753 to a214355 |

## Findings

Observed (commands run 2026-10-20; `date -u +%Y-%m-%d` gave `2026-10-20`):

1. PR identity and state. `gh pr view 9348 -R NationalSecurityAgency/ghidra --json title,state,isDraft,headRefOid,headRefName,baseRefName,updatedAt,mergeStateStatus,reviewDecision,labels,number` returned `state: OPEN`, `isDraft: false`, `headRefOid: a214355498e84aa86280be0c31c955aaf94f2d12`, `headRefName: fix/golang-stripped-type-markup-master`, `baseRefName: master`, `updatedAt: 2026-08-31T11:56:44Z`, `mergeStateStatus: BLOCKED`. The title matches S032's anchor text.
2. Head commit history. The `commits` query lists three commits, all committed `2026-08-31T11:56:03Z`: `1aa79ff…` (don't let one bad type abort all type markup), `a94872c…` (reject out-of-bounds rtti name offsets), `a214355…` (resolve stripped 1.24/1.25 maps as SwissMapType).
3. Force-push. `/tmp/pr9348.html:2837-2850` shows the timeline text "force-pushed the fix/golang-stripped-type-markup-master branch from 5fe0753 to a214355" (event dated 2026-08-31 per the page's own timeline). So the head moved once, and S032's unanchored revision cannot be told apart from the current head without the commit hash.
4. Digest instability. `sha256sum /tmp/pr9348.html` = `8a94af63…`; `sha256sum /tmp/pr9348.b.html` (second `curl -sSL` of the same URL) = `dab89ce7…`. These differ within one session. The fetched HTML embeds per-request channel tokens and nonces (`/tmp/pr9348.html:776`, `aliveChannel`). Combined with the routed defect, S032's `436c0f63…` and the r17 fetches `028dbb7d…`, `f3841de0…` (`corpus/lessons/round-17-verifier-spotcheck.md:147`), no digest of this page is reproducible. The digest is therefore a fetch-time label, not an identity.
5. Mechanism text. The head commit `a214355`'s message says `GoMapType's structureName candidate list was missing internal/abi.SwissMapType` (reader text of the PR page, commit `a214355` body, `artifact://38823`; its title link is at `/tmp/pr9348.html:2735`). S033 records this as the author's claim, tier B, unverified by this seat: I did not open the diff, build, or run any carrier.

Format and rule checks:
- 11 cells, no `|` inside any cell (`CORPUS.md:86-89`).
- `teaches` opens `supersedes S032 —` (`CORPUS.md:116-118`; contract criterion `.ufo/waves/round-18/contract.md:44-45`).
- `anchor` contains `fetch-time` (contract `:45`) and gives title, state, head commit and access date (`CORPUS.md:99-100`, S032 precedent at `corpus/SOURCES.md:38`).
- `kind` `community`, `tier` B: community is never A (`CORPUS.md:93-97`).
- Gate rows carry URL, access date and quotes ≤25 words: title quote is 9 words, force-push quote is 8 words (`CORPUS.md:112-115`).

Limits and inference:
- The `OPEN` state and `a214355` head are as of the read time. `recheck` 90d is a judgement matching S032; `on-release` does not apply, there is no release.
- `opened` 2026-10-20 is the date this seat opened the source.
- Whether `corpus/lessons/round-18.md` will cite S033 is the L1's decision; the `mined` status depends on it (see Draft notes).

## Tooling record
- No installs or updates. Used existing `gh` 2.102.0 at `/home/vgpnk/.local/bin/gh`, `curl`, `jq`, `sha256sum`.
- Scratch fetches left at `/tmp/pr9348.html` and `/tmp/pr9348.b.html` (outside the lane; cited above).

## Out of scope (not done)
- No REA, Ghidra, carrier execution, or lane file edits. No `jj` or git writes. No subagent dispatch (leaf).
- Did not verify the PR's mechanism claim against the diff or the Go source.
