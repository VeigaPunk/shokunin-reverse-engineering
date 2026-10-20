# DraftJjRow — jj git-compatibility SOURCES row and Gate quote (round 18, w1)

Author-side draft only. No lane file was edited. L1 integrates.

## Source capture

- URL requested: https://jj-vcs.github.io/jj/latest/git-compatibility/
- `curl -sI` on that URL returned `HTTP/2 301`, `location: http://docs.jj-vcs.dev/latest/git-compatibility/`. The reader tool also reported the canonical `https://docs.jj-vcs.dev/latest/git-compatibility/`.
- Saved bytes: `/tmp/kaidoku-r18-jj.JnOZDv/git-compatibility.html`, 2415 lines, `sha256 db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` (command: `curl -sSfL -o … ; sha256sum`). Cited below as `html:N`.
- Page has no version stamp. Its `<title>` is "Git compatibility - Jujutsu docs" (html head). So the page cannot be tied to jj 0.45.1 from the page itself.
- Local binary: `jj --version` → `jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5` (command source).

## Observed sandbox check (throwaway repo, not LANE)

Commands run in `mktemp -d` under `/tmp/kaidoku-r18-jjsbx.*` (removed afterwards), identity via env, jj 0.45.1:

```
git init -q -b main repo && cd repo && git commit -q --allow-empty -m init
git symbolic-ref -q HEAD            -> refs/heads/main
jj git init                         -> "Initialized repo in ."
jj git colocation status            -> "Workspace is currently colocated with Git."
ls -a                               -> . .. .git .jj
jj new -m off                       -> working copy now at kztkupou (empty) off; parent lwtpqunr
git symbolic-ref -q HEAD            -> (empty: detached)
git rev-parse HEAD                  -> 22b62a4dc08e39898107bd3ba0aceb9202af7ebc
git rev-parse refs/heads/main       -> acbfd85b466d64b22d23ae93ed57d321125d85b1
jj git export                       -> "No export needed in colocated workspaces."
git symbolic-ref -q HEAD            -> (empty: still detached)
```

This is one observation on jj 0.45.1 only. It supports the doc's detached-HEAD statement for this version.

## Draft

### SOURCES row (proposed id S034)

Note: `claims.json:14` assigns `S033` to C1, so this row takes `S034` unless L1 renumbers.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S034 | jj Git compatibility documentation — https://jj-vcs.github.io/jj/latest/git-compatibility/ (301 to http://docs.jj-vcs.dev/latest/git-compatibility/) | docs | A | How a colocated jj workspace shares its Git repo and HEAD: colocation default, detached HEAD after jj commands, and the branch mapping the page leaves undocumented | fetched 2026-10-20, sha256 `db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254` (2415-line HTML); `#colocated-jujutsugit-workspaces` html:2223-2237; `#branches` html:2329-2330 | Colocation is the default for `jj git init` and `jj git clone` (html:2224-2225). jj commands usually leave Git HEAD detached, so mutating git commands may need `git switch` first (html:2235-2237). The Branches section is only "TODO: Describe how branches are mapped" (html:2330), so branch-pin rules rest on observed behaviour, not on this page. | mined | 2026-10-20 | on-release | corpus/lessons/round-18.md (C2; planned, not yet written) |

Sentence sources for the teaches cell:
- "Colocation is the default…" — html:2224-2225: "A colocated Jujutsu workspace is a hybrid Jujutsu/Git workspace. This is the default for Git-backed workspace created with `jj git init` or `jj git clone`."
- "jj commands usually leave Git HEAD detached…" — html:2235-2237: "…jj commands will usually put the Git repo in a "detached HEAD" state … Before doing mutating Git commands, you may need to tell Git what the current branch should be with a `git switch` command."
- "The Branches section is only TODO" — html:2330: "TODO: Describe how branches are mapped".
- Sandbox observation (command block above) confirms the detached HEAD for jj 0.45.1 after `jj new`.

### Gate quote line

Format follows the round-17 `### Opened sources and located quotes` table in `corpus/lessons/round-17.md` (lines 44-48).

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S034 | https://jj-vcs.github.io/jj/latest/git-compatibility/ (fetched 2026-10-20), html:2235-2236 | `jj commands will usually put the Git repo in a "detached HEAD" state, since in jj there is not concept of a "currently tracked branch".` |

Quote facts:
- 25 words by `str.split()`. The limit is ≤25, so it fits exactly.
- The source text reads "there is not concept" (typo kept, verbatim).
- The HTML wraps the sentence across lines 2235-2236 and wraps `jj` in `<code>`. The quote is the rendered text.

Optional second quote if L1 wants the mutating-command clause (22 words, html:2236-2237): `Before doing mutating Git commands, you may need to tell Git what the current branch should be with a git switch command.`

## Limits and calibration

- The doc is `latest` with no version stamp (html head). It is not pinned to jj 0.45.1 from the page itself.
- Only the sandbox check ties the detached-HEAD statement to the local binary, and only for `jj new` on 0.45.1. `jj git import`/`export` on the lane was not tested. The lane is jj 0.45.1 (per `contract.md:17`).
- The page's `#branches` section is a TODO (html:2330). Mapping of jj bookmarks to Git branches is not documented on this page. Anything C2 says about bookmark-to-branch behaviour is observed, not sourced.
- The page describes the non-colocated case: "no branches at all (not even a main branch)" (html:2246). That is outside the lane's colocated case.
- Id collision: `S033` is claimed by C1 (`claims.json:14`), so `S034` is proposed here.

## Tooling record

- Installed or updated: nothing. Used `curl`, `sha256sum`, `python3` stdlib (HTML-to-text extraction), `git`, and the pre-installed `jj 0.45.1`.
- Temp files outside LANE: `/tmp/kaidoku-r18-jj.JnOZDv/` (fetched HTML and extracted text, kept for L1 re-check). Sandbox `/tmp/kaidoku-r18-jjsbx.*` removed.
- No `jj` or git write in LANE. Only read-only file reads in LANE: `contract.md`, `claims.json`, `wave1-spec.json`, `corpus/SOURCES.md`, `corpus/lessons/round-17.md`.
