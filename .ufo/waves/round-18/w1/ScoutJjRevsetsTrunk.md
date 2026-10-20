# ScoutJjRevsetsTrunk — jj docs for C2 (branch-tip pinning)

Seat: `KaidokuR18.ScoutJjRevsetsTrunk` (leaf scout, advisory). Round 18, exhaust: revsets/bookmarks
(`name@remote`, `trunk()`), `snapshot.auto-track`, `snapshot.max-new-file-size` 1 MiB default.
Read-only in LANE; all jj-write probes ran in `mktemp -d` sandboxes. No REA, no carrier execution.

## Verdict for L1 (one line per artifact)

| artifact | C2 value | disposition |
|---|---|---|
| `docs/git-compatibility.md` §Colocated workspaces | **grounds the defect**: jj updates `.git/HEAD`, so HEAD names the working-copy commit | **SOURCES row — deserved** |
| `docs/revsets.md` + `docs/bookmarks.md` (`trunk()`, `<name>@<remote>`) | **bounds the fix's truth claim**: `main@origin` is a *last-seen* position | **SOURCES row — deserved** |
| `docs/config.md` snapshot settings + `cli/src/config/misc.toml` defaults | sandbox-validity facts only (auto-track scope, 1 MiB, existing-file exemption) | **lead only** for C2; optional third row (draft §4.3) |

## 1. Provenance chain (observation)

All three embedded help topics are byte-identical to the raw docs at tag `v0.45.1`, and that tag's
commit is the hash printed by the installed binary. So a `docs/<page>.md:<line>` anchor for those three
pages indexes exactly the text this host's `jj` ships.

```console
$ jj --version
jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5            # exit 0
$ git ls-remote --tags https://github.com/jj-vcs/jj 'refs/tags/v0.45.1*'
7c41cdeb16b6b321c64e789a966b6adf723816a5	refs/tags/v0.45.1    # exit 0; lightweight tag, no ^{} line
$ curl -sSfL -o config.md    https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/config.md    # exit 0
$ curl -sSfL -o revsets.md   https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/revsets.md   # exit 0
$ curl -sSfL -o bookmarks.md https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/bookmarks.md # exit 0
$ jj help -k config  > config.help;  cmp -s config.md  config.help;  echo $?   # 0
$ jj help -k revsets > revsets.help; cmp -s revsets.md revsets.help; echo $?   # 0
$ jj help -k bookmarks > bm.help;    cmp -s bookmarks.md bm.help;    echo $?   # 0
```

(temp paths elided; all runs on 2026-10-20)

sha256 pairs (doc = help): `config` `ceefb706…c4c85e3`; `revsets` `0988ee4d…d67986ee9`;
`bookmarks` `d60653ac…dd02763ca`. `git-compatibility.md` is **not** a `jj help -k` topic (topics:
`bookmarks`, `config`, `filesets`, `glossary`, `revsets`, `templates`, `tutorial`), so F1 is tag-anchored
only — raw hash `0fb71f99…c766c641` — not help-verified; the tag is still the commit the binary reports.
Rendered page URLs (HTTP 200, `curl -o /dev/null -w '%{http_code}' -L`):
`https://docs.jj-vcs.dev/v0.45.1/{config,revsets,bookmarks,git-compatibility}/`; the `latest/` mirror also
returns 200 but is a moving target — cite the `v0.45.1` path.

## 2. Findings

### F1 — in a colocated workspace, `.git/HEAD` is jj's output, not a branch pointer (observation)

`docs/git-compatibility.md:100-117`, tag `v0.45.1`; section anchor on the rendered page:
`https://docs.jj-vcs.dev/v0.45.1/git-compatibility/#colocated-jujutsugit-workspaces` (verified:
`id="colocated-jujutsugit-workspaces"` present).

> `:111-117` — "It is allowed to mix `jj` and `git` commands in such a workspace in any order. However,
> it may be easier to keep track of what is going on if you mostly use read-only `git` commands and use
> `jj` to make changes to the repo. One reason for this (see below for more) is that `jj` commands will
> usually put the Git repo in a "detached HEAD" state, since in `jj` there is not concept of a
> "currently tracked branch". Before doing mutating Git commands, you may need to tell Git what the
> current branch should be with a `git switch` command."

> `:208` — "# Convince jj to update .git/HEAD to point to the working-copy commit's parent"
> (comment inside the manual non-colocated→colocated recipe, `:197-211`).

This is the mechanism C2 names: whatever HEAD points at is jj's bookkeeping — the working-copy commit's
parent after a commit (`:208`), i.e. `@-` — not the branch tip, and it drifts on every jj command. Equality
with `refs/heads/main` is incidental, as P1 shows.

### F2 — `trunk()` and the lane's own alias (observation + inference)

`docs/revsets.md:625-636`; rendered anchor is `#functions` (no `id="trunk"` was present in the rendered
HTML; `id="functions"` was).

> `:625-627` — "`trunk()`: Resolves to the head commit for the default bookmark of the default remote, or
> the remote named `upstream` or `origin`. This is set at the repository level upon initialization of a
> Jujutsu repository."
> `:629-633` (paraphrase) — fallback order is bookmarks `main`, `master`, `trunk` on `upstream`/`origin`;
> ambiguous → newest; none → `root()`.
> `:28` — "The `@` expression refers to the working copy commit in the current workspace."
> `:30` — "Use `<name>@<remote>` to refer to a remote-tracking tag / bookmark."

LANE already encodes the jj-side pin, in repo config *outside* the worktree
(`jj config path --repo` → `/home/vgpnk/.config/jj/repos/82edd62c643a3add383a/config.toml`, exit 0):

```console
$ jj config list --repo
revset-aliases."trunk()" = "main@origin"
snapshot.auto-track = "none()"
user.name = "kaidoku-shokunin"
user.email = "kaidoku@shokunin.local"                          # exit 0
```

So `trunk()` in this lane *is* `main@origin` — the same ref C2's `revpin` resolves. [inference] That
makes `trunk()` the idiomatic jj spelling of C2's pin, but it is **not** a substitute for reading
`refs/heads/main` in stdlib-only tools: the alias lives outside Git, so it does not survive a clone.

### F3 — `<name>@<remote>` is last-seen, not live (observation)

`docs/bookmarks.md:27-32`, `:66-70`; rendered anchor `#remotes-and-tracked-bookmarks` and
`#terminology-summary` (both verified present).

> `:27-29` — "You can refer to the remembered remote bookmark positions with `<bookmark name>@<remote
> name>`, such as `jj new main@origin`. `jj` does not provide a way to manually edit these recorded
> positions."
> `:66-70` — "A **remote bookmark** is a bookmark ref on the remote. `jj` can find out its actual state
> only when it's actively communicating with the remote. However, `jj` does store the last-seen position
> of the remote bookmark; this is the commit `jj show <bookmark name>@<remote name>` would show. This
> notion is completely analogous to Git's "remote-tracking branches"."

Calibration consequence for C2: `refs/remotes/origin/main` (what `revpin.require_pushed` compares) proves
"matches the last `fetch`", not "exists on the remote". The claim/tool wording should say *pushed as of
the last fetch*; a finding named `branch_not_pushed` overstates it unless the receipt records that
`origin/main` is last-seen state. This is the one place where the docs change what C2 may *claim*.

### F4 — `snapshot.auto-track`: doc prose, shipped default, and the lane override (observation)

`docs/config.md:2128-2142`, section anchors `#paths-to-automatically-track` and `#snapshot-settings`
(both `id=` verified on the rendered v0.45.1 page).

> `:2130-2131` — "All new files in the working copy that don't match the ignore patterns are tracked by
> default. You can set the `snapshot.auto-track` to set which paths get automatically tracked when
> they're added to the working copy."
> `:2136-2137` — "If you set `snapshot.auto-track` to a non-default value, untracked files can be tracked
> with `jj file track`."

Shipped default at the same tag, `cli/src/config/misc.toml:59-61`: `[snapshot]`,
`max-new-file-size = "1MiB"`, `auto-track = "all()"`. Confirmed empirically in a config-clean repo:
`jj config list --include-defaults | grep snapshot` → `max-new-file-size = "1MiB"`,
`auto-track = "all()"` (exit 0). LANE's `none()` is therefore a **repo-scoped override**, not a version
default.

**Trap for the round:** run inside LANE, `jj config list --include-defaults` prints
`snapshot.auto-track = "none()"` (exit 0) because `--include-defaults` means "list built-ins too", not
"show only defaults". Anyone recording that as "the default" would be wrong by the lane's own override.
Also, repo config is deliberately outside the worktree (`docs/config.md:16-18`: "For security reasons,
they are not located inside the repo."), so a clone — C2's sandbox — inherits **neither** `none()` nor
the `trunk()` alias.

### F5 — `snapshot.max-new-file-size` = 1 MiB, new files only, existing files exempt (observation)

`docs/config.md:2144-2162`, anchor `#maximum-size-for-new-files` (verified).

> `:2146-2147` — "By default, as an anti-footgun measure, `jj` will refuse to add new files to the
> snapshot that are larger than a certain size; the default is 1MiB."
> `:2158-2160` — suffixes `B`, `MiB`, `GB`, …; "if no suffix is provided, or the value is a raw integer
> literal, the value is interpreted as if it were specified in bytes."
> `:2162` — "Files that already exist in the working copy are not subject to this limit."

Matters twice for C2: LANE's tree at `refs/heads/main` carries **20** tracked files >1 MiB
(`git ls-tree -r -l refs/heads/main | awk '$4>1048576' | wc -l` → 20; largest 6,212,446 B), and existing
files are exempt (`:2162`, observed once at 2 MiB in P2a), so `jj git init --colocate` on the clone is
expected to be clean [inference for the 20-file case]. A *newly written* >1 MiB sandbox artifact is
refused, but **exit 0** (P2b) — so setup validity must not be inferred from the commit's exit code.

## 3. Probes (all in `mktemp -d`; jj writes never in LANE)

**P1 — the C2 red condition, reproduced.** Fresh git repo → `jj git init --colocate` → write file →
`jj commit -m off`:

```console
$ JJ="jj --config user.name=a --config user.email=a@b"   # arg shorthand for the runs below
$ jj git init --colocate                                 # exit 0, "Initialized repo in \".\""
$ printf 'x\n' > new.txt
$ $JJ status                                             # exit 0: "A new.txt"; @ 549e1c60; @- b0c9a502 main
$ $JJ commit -m off                                      # exit 0: @ 38ed9203; @- 701678b9 "off"
$ git rev-parse HEAD            → 701678b95c96e42ab9869f78c3044d241830effc
$ git rev-parse refs/heads/main → b0c9a5024345a281e6a58332dd1a5e66f05863e1
```

HEAD = the off-branch commit; `main` unmoved. `jj help commit` (installed, exit 0) states the mechanism
explicitly: "`jj commit` doesn't move bookmarks forward." Observation, not inference.

**P2 — 1 MiB limit.** Two separate sandboxes:

(a) *Existing file is exempt*: a repo with a committed 2 MiB file → `jj git init --colocate` exit 0;
`jj file list` lists `big-existing.bin` (tracked).

(b) *New file is refused, without an error exit*: empty-base repo, then a new 2 MiB file:

```console
$ head -c 2097152 /dev/zero | tr '\0' 'b' > big.bin
$ $JJ status                                              # exit 0
Warning: Refused to snapshot some files:
  big.bin: 2.0MiB (2097152 bytes); the maximum size allowed is 1.0MiB (1048576 bytes)
Hint: This is to prevent large files from being added by accident. To fix this:
  * Add the file(s) to `.gitignore`
  * Run `jj config set --repo snapshot.max-new-file-size 2097152`
  * Run `jj --config snapshot.max-new-file-size=2097152 status`
Untracked paths:
? big.bin
Working copy  (@) : pznrrllo cad9e180 (empty) (no description set)
Parent commit (@-): kstzklnp f4e978be master | (empty) base
$ $JJ commit -m off                                       # exit 0; HEAD 131ee7ae; tree of HEAD: 0 entries
```

`1.0MiB (1048576 bytes)` confirms MiB = 2^20 and the default exactly. Refusal is a warning, never a
non-zero exit, and leaves the file untracked, not staged.

**P3 — `trunk()` in a fresh clone (no lane repo config).** `git clone --no-local src dst` →
`jj git init --colocate` → `jj log -r 'trunk()' -T commit_id.short()` → `27af5dd08c1e` (exit 0),
identical to `-r 'main@origin'` (exit 0). [observation] The built-in fallback finds `main@origin` in the
clone even without LANE's alias; the alias would be redundant there.

## 4. SOURCES judgement (L1 assigns ids; C1 claims S033, so these suggest S034+)

### 4.1 Deserved row — colocated HEAD ground

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S034 | Jujutsu v0.45.1 git-compatibility documentation — https://docs.jj-vcs.dev/v0.45.1/git-compatibility/#colocated-jujutsugit-workspaces | docs | A | Official v0.45.1 statement that colocated Jujutsu/Git workspaces let jj rewrite `.git/HEAD`, so HEAD names the working-copy commit rather than a branch | Tag `v0.45.1` = commit `7c41cdeb16b6b321c64e789a966b6adf723816a5` (the hash in this host's `jj --version`; raw `docs/git-compatibility.md` sha256 `0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641`); raw `docs/git-compatibility.md:111-117` — "`jj` commands will usually put the Git repo in a \"detached HEAD\" state, since in `jj` there is not concept of a \"currently tracked branch\""; `:208` "Convince jj to update .git/HEAD to point to the working-copy commit's parent" | In a colocated lane HEAD is jj's working-copy output, so a revision pin must read `refs/heads/main` and may use HEAD only as an equality witness; `git rev-parse HEAD` alone is not a branch tip. | mined | 2026-10-20 | on-release | `.ufo/waves/round-18/contract.md` §C2, `.ufo/waves/round-18/w1/ScoutJjRevsetsTrunk.md` |

### 4.2 Deserved row — pin semantics and their limit

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S035 | Jujutsu v0.45.1 revsets and bookmarks reference — https://docs.jj-vcs.dev/v0.45.1/revsets/#functions and https://docs.jj-vcs.dev/v0.45.1/bookmarks/#remotes-and-tracked-bookmarks | docs | A | Official v0.45.1 meaning of `trunk()` and of `<bookmark>@<remote>` as a remembered remote position | Tag `v0.45.1` (`7c41cdeb…`); raw `docs/revsets.md:625-636` ("`trunk()`: Resolves to the head commit for the default bookmark of the default remote, or the remote named `upstream` or `origin` … set at the repository level upon initialization"); `:28-30` (`@` = working copy; `<name>@<remote>` = remote-tracking bookmark); raw `docs/bookmarks.md:27-32` and `:66-70` ("`jj` does store the last-seen position of the remote bookmark … completely analogous to Git's \"remote-tracking branches\"") | `main@origin` is last-seen state, not a live remote read, so a pushed check against it proves "matches the last fetch"; the lane already aliases `trunk()` to `main@origin`, which is the jj spelling of C2's pin but is not visible to a stdlib-only reader. | mined | 2026-10-20 | on-release | `.ufo/waves/round-18/contract.md` §C2, `.ufo/waves/round-18/w1/ScoutJjRevsetsTrunk.md` |

### 4.3 Lead only (row optional)

`docs/config.md` snapshot settings + `cli/src/config/misc.toml:59-61`. It does not ground the pin's
correctness — `jj commit` creates the off-branch commit whether or not the write is tracked (P2b) — so it
should stay a lead unless the executor cites the defaults in `jj-red-before.py`'s header. If L1 wants it
as a row, it is a third row on the same tag: anchors `docs/config.md:2130-2137`, `:2144-2162`; shipped
default `misc.toml:59-61`; teaches "auto-track defaults to `all()` at the lane's version and LANE
overrides it to `none()` per repo; new-file snapshot limit is 1 MiB with existing files exempt; refusal
is a warning with exit 0". The two defaults belong in the tool header regardless.

### 4.4 Leads (not rows)

- `jj help commit` text ("`jj commit` doesn't move bookmarks forward") — installed binary only, no
  versioned page; evidence is P1, not a source row.
- `docs/filesets.md` / `docs/working-copy.md#ignored-files` — referenced by the auto-track prose; only
  needed if a tool sets `snapshot.auto-track` (C2 does not).
- `cli/src/config/revsets.toml` — built-in alias list; useful only if the lane ever removes its
  `trunk()` override.
- `https://docs.jj-vcs.dev/latest/…` — returned 200 but is unversioned and was not text-compared; do not
  anchor rows to it.

## 5. Calibration notes for C2

1. **HEAD is not a tip here, and the doc says why** (F1). C2's baseline red is exactly P1:
   `git rev-parse HEAD` = off-branch commit, `refs/heads/main` = base. Both at exit 0, so the defect is
   silent — consistent with the claim's "3 live sites → 0".
2. **`require_pushed` is last-seen** (F3). Record `origin/main` as last-fetched evidence; do not let the
   receipt or the finding name claim live remote state. Suggested receipt field wording:
   `remote_last_seen`.
3. **Sandbox isolation** (F4/P3). `.jj` is not in the Git tree
   (`git ls-tree -d --name-only refs/heads/main | grep -x '.jj'` → exit 1) and repo config lives outside
   the worktree (`docs/config.md:16-18`), so a `git clone` carries neither; the sandbox gets
   `auto-track=all()` and built-in `trunk()` → `main@origin` (P3 observed). Do not port the lane's
   `none()` assumption into `jj-red-before.py`; conversely, the lane itself will *not* auto-track new
   report/tool files — integration must `jj file track`/`git add` them explicitly [inference from the
   `none()` override].
4. **1 MiB exemption covers the clone** (F5/P2a): [inference] LANE's 20 tracked files >1 MiB should
   initialize cleanly in the sandbox because `docs/config.md:2162` exempts existing files; P2a verified
   the rule at 2 MiB for a committed file. A *new* >1 MiB receipt is silently untracked with exit 0.
   Keep sandbox artifacts small, or the red/green receipt could omit its own evidence file without
   failing.
5. **`jj commit` always exits 0** here (empty tree included), so step (1) must assert
   `HEAD != refs/heads/main` after the commit, not rely on commit success/failure.
6. The lane's jj-idiomatic pin name is `trunk()` (= `main@origin`), but C2's tools must keep reading git
   refs (stdlib-only, outside Git config). The docs justify the *semantics*, not an implementation; do
   not switch the tools to calling `jj`.

## 6. Gaps

- `.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` named in the round-18 claims does **not** exist in
  LANE at `9011581` — absent from the filesystem (`ls .ufo/waves` → no `hyaku`) and from the Git tree
  (`git ls-tree -d --name-only refs/heads/main .ufo/waves/`). The three HEAD-keyed sites are therefore
  taken from `.ufo/waves/round-18/contract.md` §C2, not from the audit's §5; if the audit is meant to be
  authoritative for site identity, L1 must supply it.
- Rendered-site line numbers are not comparable to raw markdown; every anchor above states its artifact
  (`docs/<page>.md:<line>` at tag `v0.45.1`).
- Only the versioned `v0.45.1` pages were quoted. The `latest/` mirror returned HTTP 200 but was not
  text-compared; do not repoint an anchor to it without re-opening.

## 7. Tooling

No installs or upgrades (nothing needed; `curl`, `jj 0.45.1`, `git` already present). No REA calls, no
Ghidra, no carrier execution. LANE jj use was limited to non-repo-touching `--version` / `config` /
`help`; every probe that writes ran under `mktemp -d`.

Read-only lane check after all commands: `HEAD` = `refs/heads/main` = `refs/remotes/origin/main` =
`9011581d84527ba34c675f9cf912e54d2e72d470` (three `git rev-parse --verify` calls, exit 0 each);
`.git/HEAD` mtime `2026-10-20 12:06:56 -0300`. `git status --porcelain --untracked-files=no` showed 3
then 5 peer-owned modifications while I worked (`.ufo/gates/citation-drift/citation-drift-probe.py`,
`.ufo/waves/round-17/{tools/carrier-run.py,tools/compare.py,tools/log-extract.py,verify.py}`) — none
written by this seat. My only write is this file, untracked:
`?? .ufo/waves/round-18/w1/ScoutJjRevsetsTrunk.md`.
