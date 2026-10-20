# ScoutGitRevParseDocs — what a Git revision pin actually requires (round 18, w1)

Author-side scout report for C2 (jj-safe revision pins). Read-only on LANE; this file is the only write.
No subagent dispatch, no REA, no carrier execution, no `jj`.

**Verdict: a SOURCES row is warranted — one `docs` / tier A row covering both pages (propose `S035`).** Draft in §7.
The docs do not merely restate the lane's practice: they establish (a) why `HEAD` is not a branch identity,
(b) that a bare `<name>` is ambiguous and can resolve to a tag, and (c) the three preconditions `@{upstream}`
needs, of which this lane already fails one by construction.

## 1. Sources opened

| Source | Fetch / identity | Size |
|---|---|---|
| https://git-scm.com/docs/git-rev-parse | `curl -sSL`, 2026-10-20; sha256 `1e84fc200220b2cd356b78f2344766ee7cbaafa8bcef64679dbf47ec585f19da`; page header "git-rev-parse last updated in 2.56.0" (html:1330) | 122,459 bytes |
| https://git-scm.com/docs/gitrevisions | `curl -sSL`, 2026-10-20; sha256 `0dd9ee45f05b3dc5cddeae36bdd86c449ab72a314e27d99c5b1240e5dc684b68`; header "gitrevisions last updated in 2.56.0" | 74,654 bytes |

Local binary: `git --version` → `git version 2.56.0`, exit 0. That matches both pages' latest version, so the
observations below are on the documented version, not an older one.
Supplementary anchor: `man gitglossary` on the installed git 2.56.0 (`col -b` lines 133-137 "detached HEAD",
205-209 "HEAD"), used only to corroborate; it is not proposed as a registry source.

Anchor notation: `html:N` = line N of the fetched bytes whose sha256 is above (reproducible with the same
`curl`). Rendered-text line numbers from the reader are given in §4 only as convenience; the sha256 + `html:N`
pair is the real anchor. Section ids (`#Documentation/git-rev-parse.txt---verify`, etc.) are the pages' own.

## 2. Answers — what each form requires

All items marked **[OBS]** are commands run in this session (receipts §3); **[DOC]** is the source text;
**[INF]** is my inference.

### 2.1 `--verify`

**[DOC]** "Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1
that can be used to access the object database. If so, emit it to the standard output; otherwise, error out."
— git-rev-parse html:2720-2723 (rendered 332-335).

Requires:
- exactly **one** argument — two revisions is an error, observed `fatal: Needed a single revision`, exit 128 **[OBS]**;
- the argument must resolve to an object; failures are non-zero (doc says "otherwise, error out") **[DOC]**;
- `-q`/`--quiet` makes the failure silent and is "Only meaningful in `--verify` mode" (html:2743-2745) **[DOC]**;
  observed silent `exit 1`, versus `exit 128` with the message **[OBS]**.

Does **not** require: commit-ness, branch membership, or an attached HEAD. It emits the object id, not a ref
name, so it cannot by itself witness "this is the branch tip".
**[DOC]** adds the type guard itself: "you can add the `^{type}` peeling operator to the parameter"
(html:2726-2731) and recommends `--end-of-options` for untrusted names (html:2735-2736).

### 2.2 `<rev>^{commit}`

**[DOC]** "A suffix `^` followed by an object type name enclosed in brace pair means dereference the object at
`<rev>` recursively until an object of type `<type>` is found or the object cannot be dereferenced anymore (in
which case, barf). For example, if `<rev>` is a commit-ish, `<rev>^{commit}` describes the corresponding commit
object." — gitrevisions html:2388-2394 (rev-parse html:3270-3276, rendered 772-779). `<rev>^0` is a shorthand.

Requires: a resolvable `<rev>`, and a commit reachable by recursive dereference (so it peels annotated tags;
observed `t1` → tag object id, `t1^{commit}` → commit id, both exit 0) **[OBS]**. A non-commit target barfs:
`<blob>^{commit}` → `error: … expected commit type, but the object dereferences to blob type` + exit 128 **[OBS]**.

It does **not** prove branch attachment: on a detached HEAD, `HEAD^{commit}` exits 0 and returns the detached
commit **[OBS]**. So the C2 red/green cannot come from `^{commit}`; it comes from comparing the two OIDs. The
contract's `revpin` compares `HEAD^{commit}` with `refs/heads/<branch>^{commit}` — correct use, but the guard
is the comparison, not the peel.

### 2.3 `refs/heads/<name>` vs `HEAD`

**[DOC]** `<refname>` lookup takes the first match in this order (gitrevisions html:2191-2216; rev-parse
html:3073-3098, rendered 618-638):
1. `$GIT_DIR/<refname>` — "this is usually useful only for `HEAD`, `FETCH_HEAD`, …" (html:2202-2203)
2. `refs/<refname>`
3. `refs/tags/<refname>`
4. `refs/heads/<refname>`
5. `refs/remotes/<refname>`
6. `refs/remotes/<refname>/HEAD`

**[DOC]** `HEAD` "names the commit on which you based the changes in the working tree" (gitrevisions
html:2223-2225). Glossary: HEAD "is a reference to one of the heads in your repository, except when using a
detached HEAD, in which case it directly references an arbitrary commit" (`man gitglossary`, col lines 205-209).

Therefore **[INF]**:
- `refs/heads/main` is checkout-independent branch identity; `HEAD` is working-tree identity. They coincide
  only while HEAD is attached to that branch.
- Rule 1 proves `HEAD` is matched as a pseudo-ref *before* rule 4; it is not a synonym for the branch.
- A bare `<name>` is **not** equivalent to `refs/heads/<name>`: rule 3 (`refs/tags/`) precedes rule 4. Observed:
  with both `refs/tags/main` and `refs/heads/main` present, `git rev-parse --verify main` warned
  `refname 'main' is ambiguous.` and returned the **tag** object id, exit 0, while
  `refs/heads/main^{commit}` returned the branch tip **[OBS]**. The `refs/heads/` prefix is therefore
  load-bearing determinism, not style.
- `--symbolic-full-name` is a separate documented option, not a modifier of `--verify` (html:2783-2791);
  observed attached HEAD → `refs/heads/main`, detached HEAD → literal `HEAD`, exit 0 both **[OBS]**.

Lane state **[OBS]**: HEAD is detached (`git symbolic-ref -q HEAD` exit 1; `--symbolic-full-name HEAD` prints
`HEAD`) while `HEAD`, `refs/heads/main` and `refs/remotes/origin/main` all name `9011581d…`.
So the lane is currently green for *equality by accident of state*: the hazard is latent, and a red run needs
an off-branch HEAD (what `jj-red-before.py` constructs), not a different command.

### 2.4 `@{upstream}`

**[DOC]** "A branch B may be set up to build on top of a branch X (configured with `branch.<name>.merge`) at a
remote R (configured with `branch.<name>.remote`). B@{u} refers to the remote-tracking branch for the branch X
taken from remote R, typically found at `refs/remotes/R/X`." — gitrevisions html:2325-2328 (rev-parse
html:3207-3208). The suffix is case-insensitive (html:2361-2362).

Requires, in order **[OBS]**:
1. **For the implicit form `@{u}`: HEAD must point to a branch.** Detached → `fatal: HEAD does not point to a
   branch`, exit 128.
2. **`branch.<name>.remote` and `branch.<name>.merge` configured.** Attached with neither → `fatal: no upstream
   configured for branch 'main'`, exit 128.
3. **The remote-tracking ref must exist.** With config set but no `refs/remotes/origin/main` →
   `fatal: upstream branch 'refs/heads/main' not stored as a remote-tracking branch`, exit 128.

The **named form** `main@{u}` does not need attachment (HEAD may be detached) and still resolves, exit 0,
provided conditions 2 and 3 hold **[OBS]**. So the lane's ban on `@{u}`/`--abbrev-ref`/`--show-current` is
structural, not cosmetic: in this lane the bare `@{u}` form cannot run at all. But note the named form is also
not a push receipt — it only names a local remote-tracking ref, which is a cached observation of the remote.

Lane receipt refines this: `branch.main.remote` = `origin`, `branch.main.merge` = `refs/heads/main`, and
`refs/remotes/origin/main` = `9011581d…` all exist **[OBS]**. The lane's `@{u}` failure is therefore **only**
condition 1 (attachment), which is exactly the jj-colocated property.

## 3. Command receipts

### 3.1 LANE probes (read-only; `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`)

```
$ git -C $L rev-parse --verify HEAD                                   -> 9011581d84527ba34c675f9cf912e54d2e72d470  exit 0
$ git -C $L rev-parse --verify 'refs/heads/main^{commit}'             -> 9011581d84527ba34c675f9cf912e54d2e72d470  exit 0
$ git -C $L rev-parse --verify 'HEAD^{commit}'                        -> 9011581d84527ba34c675f9cf912e54d2e72d470  exit 0
$ git -C $L rev-parse --verify '@{upstream}'                          -> fatal: HEAD does not point to a branch     exit 128
$ git -C $L symbolic-ref -q HEAD                                      -> (no output)                               exit 1
$ git -C $L rev-parse --symbolic-full-name HEAD                       -> HEAD                                      exit 0
$ git -C $L show-ref --verify refs/heads/main                         -> 9011581d… refs/heads/main                 exit 0
$ git -C $L show-ref --verify refs/remotes/origin/main                -> 9011581d… refs/remotes/origin/main        exit 0
$ git -C $L config --get branch.main.remote                           -> origin                                    exit 0
$ git -C $L config --get branch.main.merge                            -> refs/heads/main                           exit 0
```

`symbolic-ref` is used here only as a diagnostic; it is **not** proposed for any lane tool (contract
`.ufo/waves/round-18/contract.md:17-19` bans it, and `--symbolic-full-name` already gives the same signal
without erroring).

### 3.2 Throwaway fixtures (`mktemp -d` under `/tmp`; removed with the sandbox dirs)

| Setup | Command | Observed | Exit |
|---|---|---|---|
| attached, upstream via `push -u` | `rev-parse --verify @{u}` | commit id | 0 |
| attached, upstream configured | `rev-parse --verify @{u}` | commit id | 0 |
| attached, upstream unset | `rev-parse --verify @{u}` | `fatal: no upstream configured for branch 'main'` | 128 |
| attached, config set, no tracking ref | `rev-parse --verify @{u}` | `fatal: upstream branch 'refs/heads/main' not stored as a remote-tracking branch` | 128 |
| detached | `rev-parse --verify 'refs/heads/main^{commit}'` | branch tip | 0 |
| detached | `rev-parse --verify 'HEAD^{commit}'` | detached commit | 0 |
| detached | `rev-parse --verify @{u}` / `@{upstream}` | `fatal: HEAD does not point to a branch` | 128 |
| detached, config + tracking ref present | `rev-parse --verify 'main@{u}'` | remote-tracking commit id | 0 |
| any | `rev-parse --verify HEAD refs/heads/main` | `fatal: Needed a single revision` | 128 |
| any | `rev-parse --verify 'refs/heads/nope^{commit}'` | `fatal: Needed a single revision` | 128 |
| any | `rev-parse -q --verify 'refs/heads/nope^{commit}'` | (silent) | 1 |
| any | `rev-parse -q --verify 'refs/remotes/origin/main^{commit}'` (no remote) | (silent) | 1 |
| annotated tag | `rev-parse --verify t1` / `'t1^{commit}'` | tag id / commit id | 0 / 0 |
| blob | `rev-parse --verify '<blob>^{commit}'` | `error: … expected commit type, but the object dereferences to blob type` then `fatal: Needed a single revision` | 128 |
| tag `main` + branch `main` | `rev-parse --verify main` | `warning: refname 'main' is ambiguous.` + **tag** id | 0 |
| same | `rev-parse --verify 'refs/heads/main^{commit}'` | branch id | 0 |
| unborn branch | `rev-parse --verify HEAD` / `refs/heads/main` | `fatal: Needed a single revision` | 128 |
| `refs/heads/x` ← tag object | `git update-ref refs/heads/pinned <tag-oid>` | `fatal: update_ref failed … trying to write non-commit object … to branch` | 128 |
| SHA-256 repo (`git init --object-format=sha256`) | `rev-parse --verify HEAD` | 64 hex chars (`wc -c` 65 with newline) | 0 |
| attached / detached | `rev-parse --symbolic-full-name HEAD` | `refs/heads/main` / `HEAD` | 0 |

## 4. Anchor index

| Construct | Page | `html:N` | Page id | Rendered lines |
|---|---|---|---|---|
| `--verify` definition | git-rev-parse | 2720-2723 | `#Documentation/git-rev-parse.txt---verify` (2718) | 330-335 |
| peel advice / untrusted name | git-rev-parse | 2726-2731, 2735-2736 | same | 337-347 |
| `-q` silent | git-rev-parse | 2743-2745 | same | 349-355 |
| `--symbolic-full-name` | git-rev-parse | 2783-2791 | `#Documentation/git-rev-parse.txt---symbolic-full-name` | 389-395 |
| `<refname>` rules | git-rev-parse | 3073-3098 | `#_specifying_revisions` (3034) | 618-638 |
| `HEAD` meaning | git-rev-parse | 3105-3107 | refname section | 640-642 |
| `@{upstream}` | git-rev-parse | 3205-3209 | `…-branchnameupstreamegmasterupstreamu` (3205) | 723-729 |
| `^{<type>}` | git-rev-parse | 3270-3276 | `#_specifying_revisions` | 772-779 |
| examples (`--verify HEAD`, `$REV^{commit}`) | git-rev-parse | 3750-3770 | `#_examples` | 1153-1166 |
| `<refname>` rules | gitrevisions | 2191-2216 | `#_specifying_revisions` (2152) | 243-263 |
| `HEAD` meaning | gitrevisions | 2223-2225 | `…-HEAD` (2223) | 265-267 |
| `@{upstream}` | gitrevisions | 2323-2328 | `…-branchnameupstreamegmasterupstreamu` (2323) | 348-351 |
| case-insensitive suffix | gitrevisions | 2373-2374 | upstream section | 378-379 |
| `^{<type>}` | gitrevisions | 2388-2394 | `#_specifying_revisions` | 397-404 |
| HEAD / detached HEAD | `man gitglossary` (git 2.56.0) | col `-b` 133-137, 205-209 | — | — |

## 5. Quotes (Gate-table rows, contiguous, ≤25 words each)

Word counts computed with `str.split()` on the rendered text.

| ID | URL / location | Contiguous quote |
|---|---|---|
| S035 | https://git-scm.com/docs/git-rev-parse, `--verify` (html:2720-2721) | Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1 |
| S035 | https://git-scm.com/docs/gitrevisions, `HEAD` (html:2225) | names the commit on which you based the changes in the working tree |
| S035 | https://git-scm.com/docs/gitrevisions, `<refname>` (html:2197-2198) | When ambiguous, a `<refname>` is disambiguated by taking the first match in the following rules |
| S035 | https://git-scm.com/docs/gitrevisions, `@{upstream}` (html:2325-2326) | A branch B may be set up to build on top of a branch X (configured with branch.<name>.merge) at a remote R |
| S035 | https://git-scm.com/docs/gitrevisions, `@{upstream}` (html:2327-2328) | B@{u} refers to the remote-tracking branch for the branch X taken from remote R |
| S035 | https://git-scm.com/docs/gitrevisions, `^{<type>}` (html:2388-2389) | dereference the object at <rev> recursively until an object of type <type> is found |

(18, 13, 15, 22, 14, 14 words. The `<refname>` rule list itself — rules 1-6 — is 40+ words and is cited by id,
not quoted.)

## 6. Calibration and operability notes for C2

1. **[OBS]** The docs say `--verify` emits "a raw 20-byte SHA-1" (html:2721) but git 2.56 in a
   `--object-format=sha256` repo emitted 64 hex chars. `revpin.py` must not hardcode 40 hex; better, compare
   the two resolved strings and never parse length.
2. **[OBS]** The stderr for a missing ref and for two arguments is identical (`fatal: Needed a single
   revision`). `revpin` cannot classify findings from stderr; it must classify from which call it made.
   Exit codes are 128 with a message, 1 with `-q` — neither is the contract's tool-level 2, which stays the
   tool's own code.
3. **[OBS]** Bare `<name>` can resolve to a tag. `refs/heads/<branch>` is the only deterministic spelling;
   appending `^{commit}` adds the type guard. The contract already specifies both
   (`.ufo/waves/round-18/contract.md:51-56`), and this note explains why the prefix must not be "simplified".
4. **[OBS]** `^{commit}` is not an attachment guard (detached `HEAD^{commit}` succeeds). The C2 detections are:
   equality of the two OIDs (`head_not_branch_tip`) and equality of the branch tip with
   `refs/remotes/origin/<branch>` (`branch_not_pushed`).
5. **[OBS]** `rev-parse --symbolic-full-name HEAD` prints `refs/heads/<branch>` attached and literal `HEAD`
   detached, exit 0 in both cases. If L1 wants the finding to distinguish "detached" from "off-branch" (the
   contract only needs `head_not_branch_tip`), this is a documented one-call discriminator that stays inside
   the allowed `rev-parse` command set; it is optional. **[INF]** it does not make the red case reachable —
   only an off-branch HEAD does.
6. **[DOC]+[INF]** The doc's own canonical `--verify` example is "Print the object name of the current
   commit: `$ git rev-parse --verify HEAD`" (html:3755-3757). The r17 tools used exactly that idiom. The defect
   was not misuse of `--verify`; it was reading "current commit" as "source revision". That distinction is the
   lesson-worthy part: **doc conformance is not fitness for a pin**.
7. **[OBS]** `git update-ref` itself refuses to point `refs/heads/*` at a non-commit, so `^{commit}` on the
   branch ref is defense-in-depth, not the load-bearing guard.

## 7. Row recommendation and draft

**Warranted: yes, one row.** Grounds:
- C2's `claims.json` falsifiable statement (`claims.json:17-20`) asserts that HEAD-keyed sites are unsafe in a
  colocated lane. The lane probes alone are green today because HEAD happens to equal the tip (§2.3); without
  the docs' lookup-order and HEAD definition, the claim rests on an observed coincidence and a sibling's jj
  page (`.ufo/waves/round-18/w1/DraftJjRow.md:41`, proposed `S034`) that says HEAD is detached but not what
  that means to a git revision.
- No git/git-scm row exists: `corpus/SOURCES.md` has 32 data rows `S001`-`S032` (`grep -c '^| S0'` = 32) and
  `grep -iE 'git-scm|rev-parse|detached|colocat|jj|gitrevisions' corpus/SOURCES.md` returned no row.
- The pages carry the operability facts the tools must encode: single-argument `--verify`, silent `-q` exit 1,
  SHA-256 output length, tag-over-branch ambiguity, and the three `@{upstream}` preconditions.

**One row, not two.** The pages are one vocabulary used together (command behavior + syntax), and precedent
combines URLs in one row (S029, `corpus/SOURCES.md:35`). Splitting would create two rows always cited together.

**Numbering.** `S033` is claimed by C1 (`claims.json:14`) and `S034` is proposed by the jj draft
(`.ufo/waves/round-18/w1/DraftJjRow.md:37-41`); this draft takes `S035` until L1 assigns. One subject, no
overlap with either: S034 is jj behavior, S035 is git semantics.

Draft (11 cells, no `|` inside any cell):

```
| S035 | Git revision grammar and verification semantics — https://git-scm.com/docs/git-rev-parse and https://git-scm.com/docs/gitrevisions | docs | A | The official semantics a revision pin rests on: `--verify` arity and failure modes, `^{commit}` peeling, `<refname>` lookup order, and what `@{upstream}` requires | Pages fetched 2026-10-20, git-rev-parse 122,459 bytes sha256 `1e84fc200220b2cd356b78f2344766ee7cbaafa8bcef64679dbf47ec585f19da` (last updated 2.56.0), gitrevisions 74,654 bytes sha256 `0dd9ee45f05b3dc5cddeae36bdd86c449ab72a314e27d99c5b1240e5dc684b68`; `--verify` html:2720-2745, `_specifying_revisions` html:3034-3108, `@{upstream}` html:3205-3209, `^{<type>}` html:3270-3276, examples html:3755-3770; gitrevisions html:2152-2226, `@{upstream}` html:2323-2328, `^{<type>}` html:2388-2394 | HEAD names the commit the working tree is based on and is looked up before refs/heads, so a detached-HEAD pin is not a branch-tip pin; a bare name can resolve to a tag, so the refs/heads prefix is required; `^{commit}` proves commit-ish but not attachment; `@{upstream}` needs an attached branch, branch.<name>.remote/merge and a stored remote-tracking ref, so it cannot serve a colocated lane. | queued | 2026-10-20 | on-release | — |
```

Notes for L1 (not part of the row):
- `status`/`used-by`: flip to `mined` + `corpus/lessons/round-18.md` only if the round-18 lesson actually cites
  S035; the registry's `used-by` column is the citation record (pattern: `corpus/SOURCES.md:36`). Do not label
  `mined` on the strength of this draft alone.
- `recheck: on-release` because both pages are versioned with git and the header names the version
  (html:1330); the digest is reproducible while the page serves 2.56.0.
- The row is a source, not a QUALITY criterion; the falsifiable artifact for C2 remains `head-rev-lint`
  `live_count` and the `jj-red-before` expectations, not this row.

## 8. Limits

- Behavior is observed on git 2.56.0 only. Error text is not an API and may differ on older git, so tools must
  key on input/exit status, not messages.
- `@{u}` staleness was not tested; the docs call it the "remote-tracking branch", which is a local cache of the
  remote state. The contract's pushed-ness test compares OIDs to `refs/remotes/origin/main`, which is the same
  kind of local observation; this report does not upgrade that to remote truth.
- No `jj` command was run. The jj-side detached state is the sibling's scope (S034 draft) plus this lane's own
  HEAD probe; I did not reproduce `jj new`/`jj commit` here.
- The glossary quote is hyphenated by the man renderer ("refer-/ence" across lines); anchored to the installed
  man page rather than reproduced as a Gate quote.
- No carrier, REA, or Ghidra invocation; nothing here exercises C3.

## 9. Tooling record

No installs or updates. Tools used: `git 2.56.0`, `curl`, `sha256sum`, `wc`, `man`/`col`, `python3` (stdlib,
word counts). Scratch data: `/tmp/docsnap.HU8y0b/` (both fetched pages), `/tmp/revparse-probe*.…` (git
fixtures). Nothing written inside LANE except this report; no git or jj write in LANE.
