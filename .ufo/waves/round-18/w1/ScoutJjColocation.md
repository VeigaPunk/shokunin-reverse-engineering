# ScoutJjColocation — jj colocated repos: what Git HEAD names

- Seat: `KaidokuR18.ScoutJjColocation` (leaf, advisory; L1 `KaidokuR18` integrates).
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470` (`contract.md:4`).
- Written: this report only. No REA, no Ghidra, no carrier execution, no subagent, no `jj` in LANE (only `jj --version`/`help` outside any repo cwd and `jj` inside `mkdtemp` sandboxes, removed). Installs: none (nothing needed; the host pacman pause was not exercised).

## Answer

1. **Observation — detached:** the 0.45.1 page states that `jj` commands "will usually put the Git repo in a `"detached HEAD"` state" and the supported-features table answers **Detached HEAD: Yes** (`docs/git-compatibility.md:114-116`, `:44-45` at tag `v0.45.1`).
2. **Observation — parent:** the only statement that HEAD names the working-copy *parent* is a comment in the manual colocation recipe — `# Convince jj to update .git/HEAD to point to the working-copy commit's parent` (`docs/git-compatibility.md:208`, tag `v0.45.1`). It is recipe commentary, not expository prose; the prose says only "detached".
3. **Observation — version:** `v0.45.0` and `v0.45.1` serve the same doc bytes (markdown sha256 `0fb71f99…`, both HTTP 200); `/latest/` is a different document (0.46.0 content: new `### In the same working copy (colocated)` section) and must not be cited for the host's 0.45.1. The same detached-HEAD sentence survives unchanged at `v0.46.0` `:145-147`.

## Documents (all fetched 2026-10-20, observation)

| artifact | URL | HTTP | bytes | sha256 |
|---|---|---|---|---|
| 0.45.1 rendered page | https://docs.jj-vcs.dev/v0.45.1/git-compatibility/ | 200 | 58508 | `5362168d6cd398ea2f6a2d9ed6cad2807f356ee2e8800b277767c2f0987c0367` |
| 0.45.0 rendered page | https://jj-vcs.github.io/jj/v0.45.0/git-compatibility/ | 200 | 58508 | same as above (`cmp` IDENTICAL) |
| latest rendered page | https://docs.jj-vcs.dev/latest/git-compatibility/ | 200 | 61334 | `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` |
| 0.45.1 markdown | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md | 200 | 12284 | `0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641` |
| 0.45.0 markdown | …/v0.45.0/docs/git-compatibility.md | 200 | 12284 | identical (`diff` → IDENTICAL_MD) |
| 0.46.0 markdown | …/v0.46.0/docs/git-compatibility.md | 200 | 13185 | `135a99ea40d2e626d0bc282283459650ba864df728449ac9225965578bc4e4bc` |
| main markdown | …/main/docs/git-compatibility.md | 200 | 13185 | identical to `v0.46.0` at fetch time (`diff` → TAG_EQ_MAIN) |

Both hosts serve identical bytes for both versions (`docs.jj-vcs.dev` and `jj-vcs.github.io` hashes compared, all matching) — the URLs are interchangeable, and `docs.jj-vcs.dev` is the one the binary's help cites.

Local jj docs: none installed — `find /home/vgpnk/.local /usr/share/doc -maxdepth 6 -name 'git-compatibility.md'` printed nothing (observation). The binary carries no colocation help topic: `jj help -k git-compatibility` → exit 2, `error: invalid value … [possible values: bookmarks, config, filesets, glossary, revsets, templates, tutorial]`; `jj git colocation --help` exit 0 has no HEAD sentence; `jj git init --help` (exit 0) links the page as `https://docs.jj-vcs.dev/latest/git-compatibility/#colocated-jujutsugit-repos` (observation).

## Quotes (exact, word counts verified)

**Q1 — detached HEAD, prose** (`v0.45.1` `docs/git-compatibility.md:114-116`, anchor `#colocated-jujutsugit-workspaces`), 25 words (at the ≤25 limit), `sic` — the doc omits "a" before "concept":

> `jj` commands will usually put the Git repo in a "detached HEAD" state, since in `jj` there is not concept of a "currently tracked branch".

**Q2 — working-copy parent** (`v0.45.1` `docs/git-compatibility.md:208`, anchor `#converting-a-workspace-into-a-colocated-workspace`), 9 words:

> update .git/HEAD to point to the working-copy commit's parent

**Q3 — supported features** (`v0.45.1` `docs/git-compatibility.md:44-45`):

> **Detached HEAD: Yes.** Jujutsu supports anonymous branches, so this is a natural state.

## Anchors (observation)

The rendered 0.45.1 page carries a heading `id="colocated-jujutsugit-workspaces"` **and** the source's explicit legacy `<a name="colocated-jujutsugit-repos">` (`git-compatibility.md:100`), each occurring once; the binary's help link uses the legacy name, so both resolve. The conversion section heading id is `converting-a-workspace-into-a-colocated-workspace` (`:173`). In 0.46.0 these are `:131` and `:204`.

## Behavior check — throwaway colocated repo, jj 0.45.1 (observation)

Sandbox under `mkdtemp`, removed after (`cleanup_exit=0`); identity passed via `--config`, never in LANE.

| state | `git rev-parse HEAD` | `jj log -r @` | `jj log -r @-` | `git symbolic-ref -q HEAD` |
|---|---|---|---|---|
| after `jj commit -m one` | `5267e1e2…` | `87525163…` | `5267e1e2…` | exit 1 (detached) |
| after appending a file + `jj st` | `5267e1e2…` | `c23d8cdd…` | `5267e1e2…` | — |
| after `jj bookmark create main -r @` | `5267e1e2…` | `c23d8cdd…` (== `refs/heads/main`) | `5267e1e2…` | — |
| after `jj new` | `c23d8cdd…` | `14367816…` | `c23d8cdd…` (== main) | — |

`head_eq_main=no` in the bookmark-at-`@` row: HEAD named the parent while the bookmark named `@` — exactly the C2 divergence shape. In the first probe, `refs/heads/main` did not exist at all after `jj commit`, and HEAD still equalled `@-`.

## Corroboration with narrower scope (observation)

`CHANGELOG.md` at `v0.45.1:96-97`, section `## [0.45.0] - 2026-09-02` → Fixed bugs: "In colocated workspaces, `jj workspace update-stale` now correctly resets the Git HEAD to the parent of the fresh working-copy commit." It uses the same parent wording but is scoped to one command, so it corroborates Q2 rather than replacing it; citing it would need its own row (different file), not an overload of the docs row.

## Lane calibration notes

- Current lane state (observation): `.git/HEAD` contains the bare 40-hex `9011581d84…` (not `ref: refs/heads/main`); `git symbolic-ref -q HEAD` exit 1; `HEAD` = `refs/heads/main` = `refs/remotes/origin/main` = `9011581d84…`. **Detached but coincident with the pushed tip** — so a HEAD-vs-tip red test cannot be demonstrated from the lane as it stands; C2's `jj-red-before.py` needs the synthetic off-branch commit it already specifies.
- The contract's cited audit path is not lane-relative: `git cat-file -e 9011581:.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` → exit 128; the file lives in the fleet repo at `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` (its §5 risk R1–R3 is the C2 source).
- Discrepancy to reconcile: `.ufo/waves/round-18/w1/DraftSkillJjNote.md:15` records `symbolic-ref -q HEAD -> refs/heads/main (attached)` and `:23` asserts an attached HEAD; at my observation the same query exits 1 and `.git/HEAD` is a raw sha. Both can be true at different times (the audit's F1 saw attached right after colocation); the draft's present-tense row should not be integrated unqualified.

## Draft SOURCES row (docs-kind; scope: "jj colocated repos: what Git HEAD names")

Copy-paste, single line, 11 cells (no cell contains `|`):

| S034 | jj 0.45.1 Git compatibility — https://docs.jj-vcs.dev/v0.45.1/git-compatibility/ | docs | A | jj colocated repos: what Git HEAD names | Tag `v0.45.1`, `docs/git-compatibility.md` sha256 `0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641` fetched 2026-10-20; lines 114-116 and 208; anchors `#colocated-jujutsugit-workspaces` and `#converting-a-workspace-into-a-colocated-workspace` | Official docs say `jj` commands usually put the Git repo in a "detached HEAD" state with no tracked branch, and the conversion recipe makes `.git/HEAD` name the working-copy commit's parent; so `git rev-parse HEAD` is a working-copy-relative commit, not a branch tip. | mined | 2026-10-20 | on-release | corpus/lessons/round-18.md, .ufo/waves/round-18/claims.json (C2) |

Integration notes (L1):
- The row is one long line (line 74 here); if your viewer truncates it, extract it with `sed -n '74p' <this report>` before pasting.
- **ID is a proposal.** `S033` is reserved by C1 (`contract.md:33`); C3 opens two more rows this round. Allocate the first free slot at integration and keep the cell text otherwise unchanged. Next-free probe: `grep -o '^| S[0-9][0-9][0-9]' corpus/SOURCES.md | sort -u | tail -1` (last row is `S032` now, `corpus/SOURCES.md:38`; a well-formed row has 11 cells).
- `used-by` assumes the C2 lesson lands in `corpus/lessons/round-18.md`; replace with the actual citing file(s). `claims.json` C2 `sourced` currently reads "jj documentation row opened this round (colocated workspaces / HEAD)" — substitute the allocated ID when the row lands.
- This row deliberately does **not** satisfy `R17-S032-DIGEST` (that check wants a teaches cell starting `supersedes S032 —`, C1's S033) and leaves rows S001–S032 untouched for `W18/controls.py`.
- Quote fidelity: cite `:208` for "parent" and `:114-116` for "detached"; a row that puts the parent wording on `:114-116` would be a misquote.

## Limits

- [INFERENCE] `/latest/` is built from main, and main equals tag `v0.46.0` at fetch time, so the two cannot be distinguished from these bytes; the version is bounded to "at least 0.46.0, not 0.45.1".
- [INFERENCE] The general rule "HEAD names `@-` after any jj command" is inferred from Q1+Q2 plus four observed states; merge/conflicted working copies (`@` with multiple parents) were not exercised and the page is silent on which parent HEAD names there.
- The jj 0.45.1 changelog's parent wording is scoped to `jj workspace update-stale`; it is not a general statement and is not in the drafted row.
- Host safety: no installs, no pacman, no host service touched; jj ran only in `mkdtemp` dirs, all removed.

## Command transcript (excerpt; every line's exit code recorded)

```
$ /home/vgpnk/.local/bin/jj --version
jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5          exit 0

$ curl -sS -o jj-v0.45.1.html -w 'HTTP=%{http_code}\n' https://jj-vcs.github.io/jj/v0.45.1/git-compatibility/
HTTP=200                                                       exit 0 (curl_exit=0)

$ sha256sum jj-v0.45.0.html jj-v0.45.1.html
5362168d…c0367  jj-v0.45.0.html
5362168d…c0367  jj-v0.45.1.html   ; cmp -> IDENTICAL

$ curl -sSL -o /dev/null -w '%{http_code}' https://docs.jj-vcs.dev/latest/git-compatibility/
200                                                            exit 0 (curl_exit=0, 61334 bytes)

$ diff gitcompat-v0.45.0.md gitcompat-v0.45.1.md
(no output)                                                    exit 0, IDENTICAL_MD
$ diff -q gitcompat-v0.46.0.md gitcompat-main.md
(no output)                                                    exit 0, TAG_EQ_MAIN

$ /home/vgpnk/.local/bin/jj help -k git-compatibility
error: invalid value 'git-compatibility' for '--keyword <KEYWORD>'   exit 2
$ /home/vgpnk/.local/bin/jj git colocation --help >/dev/null   exit 0
$ /home/vgpnk/.local/bin/jj help >/dev/null                    exit 0

# throwaway colocated sandbox (mkdtemp), jj 0.45.1
$ jj git init --colocate --config user.name=… --config user.email=…   exit 0
$ jj commit -m one --config …                                         exit 0
$ git symbolic-ref -q HEAD                                            exit 1 (no output)
$ git rev-parse HEAD         -> 5267e1e2…
$ jj log -r @  --no-graph -T commit_id -> 87525163…
$ jj log -r @- --no-graph -T commit_id -> 5267e1e2…   (HEAD == @-)
$ jj bookmark create main -r @ -> exit 0; git rev-parse refs/heads/main -> c23d8cdd…; head_eq_main=no
$ rm -rf "$d"                                                         exit 0

# LANE (read-only)
$ git rev-parse HEAD                 -> 9011581d84…                   exit 0
$ git symbolic-ref -q HEAD           -> (empty)                       exit 1
$ git rev-parse refs/heads/main      -> 9011581d84…                   exit 0
$ git rev-parse refs/remotes/origin/main -> 9011581d84…               exit 0
$ cat .git/HEAD                      -> 9011581d84… (raw sha)          exit 0
$ git cat-file -e 9011581d84…:.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md  exit 128
```
