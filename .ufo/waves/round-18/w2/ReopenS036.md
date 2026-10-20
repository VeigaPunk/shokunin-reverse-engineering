# ReopenS036 — SOURCES row S036 re-open (round 18, wave 2)

HOLDS

Seat: KaidokuR18.ReopenS036. REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`. Read-only; this report is the only file written. All commands run 2026-10-20. Working tree is byte-identical to REV for the three cited files, so working-tree line numbers equal REV line numbers.

## Verdict

HOLDS — anchor (URL, tag, sha256, lines 114-116, line 208), tier, scope, teaches, and the round-18.md Gate quote all verify at REV. Two provenance nuances recorded below; neither breaks the row.

## Row under test

OBSERVATION — `corpus/SOURCES.md:42` at REV (`git show REV:corpus/SOURCES.md`), columns `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by` (header at `corpus/SOURCES.md:5`):

- source: `jj 0.45.1 Git compatibility — https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md (rendered https://docs.jj-vcs.dev/v0.45.1/git-compatibility/)`
- kind `docs`, tier `A`
- scope: `What Git HEAD names in a colocated jj workspace, for the installed jj 0.45.1`
- anchor: `Tag v0.45.1, docs/git-compatibility.md sha256 0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641 fetched 2026-10-20; lines 114-116 (#colocated-jujutsugit-workspaces) and 208`
- teaches: `jj usually leaves the Git repo in a detached-HEAD state with no current branch, so a lane tool must pin refs/heads/<branch> and compare HEAD against it rather than read HEAD as the branch tip.`
- status `mined`, opened `2026-10-20`, recheck `on-release`, used-by `corpus/lessons/round-18.md, SKILL.md`

## Checks (command → exit code → result)

### 1. Anchor: digest reproduces

```
$ curl -sSL -o /tmp/s036-git-compat.md -w "http=%{http_code}\n" "https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md" && sha256sum /tmp/s036-git-compat.md
http=200
0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641  /tmp/s036-git-compat.md
exit=0
$ curl -sSL "https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md" | sha256sum
0fb71f992b0ed05d547e597d3f5f1cd33ed9e5d56a4e4e4cb851ba30c766c641  -
exit=0
$ python3 -I -B -c "row_sha='0fb71f99...c641'; import hashlib; actual=hashlib.sha256(open('/tmp/s036-git-compat.md','rb').read()).hexdigest(); print('row==actual:', row_sha==actual)"
row==actual: True
exit=0
```

OBSERVATION: digest matches the row byte-for-byte and is stable across two fetches. No s036 fetch-receipt file exists in `.ufo/waves/round-18/evidence/` (glob listed `jj-red-before.json`, `s032-digests.json`, …) — the digest is fetch-time only, consistent with the R17-S032-DIGEST lesson (`corpus/lessons/round-18.md:52`, "page digests are fetch-time only"); my refetch reproduces it today.

### 2. Anchor: lines 114-116 and 208

```
$ sed -n '105,125p' /tmp/s036-git-compat.md ; sed -n '200,215p' /tmp/s036-git-compat.md
exit=0
```

OBSERVATION (fetched bytes, sha256 as above):
- Line 114: `for this (see below for more) is that `jj` commands will usually put the Git`
- Line 115: `repo in a "detached HEAD" state, since in `jj` there is not concept of a`
- Line 116: `"currently tracked branch". Before doing mutating Git commands, you may need to`
- Line 208: `# Convince jj to update .git/HEAD to point to the working-copy commit's parent` (inside the "To convert to a non-colocated workspace" recipe that starts at line 191; commands `jj new && jj undo` at line 209).

NUANCE (observation): line 208 sits in the non-colocated-conversion recipe, not the colocated section named in the parenthetical; the anchor field does not say so. It still directly evidences that under jj `.git/HEAD` points at the working-copy commit's parent, i.e. not at a branch ref.

### 3. Anchor id nuance

```
$ grep -n "^#" /tmp/s036-git-compat.md
100:## <a name="colocated-jujutsugit-repos"></a>Colocated Jujutsu/Git workspaces
exit=0
$ curl -sSL -o /tmp/s036-rendered.html -w "http=%{http_code}\n" "https://docs.jj-vcs.dev/v0.45.1/git-compatibility/" && grep -o 'id="colocated-jujutsugit-[a-z]*"\|name="colocated-jujutsugit-[a-z]*"' /tmp/s036-rendered.html | sort -u
http=200
id="colocated-jujutsugit-workspaces"
name="colocated-jujutsugit-repos"
exit=0
```

OBSERVATION: the row's parenthetical `#colocated-jujutsugit-workspaces` is the rendered-page (mkdocs) heading id — present on the rendered v0.45.1 page. The raw markdown's explicit anchor at line 100 is `colocated-jujutsugit-repos`; the raw file's own internal link (line 77) uses the `-workspaces` id. Both artifacts are cited in the row's source cell, so the id is real; it is just not the raw file's `<a name>`. INFERENCE: no defect, a provenance nuance worth one clause if the row is ever revised.

### 4. Tier

OBSERVATION: row tier `A`; Gate registry delta `corpus/lessons/round-18.md:43` says "New rows S033–S036 (3 tier A, 1 tier B community)" — consistent: `corpus/SOURCES.md:39` S033 = community/B, `:40` S034 = docs/A, `:41` S035 = code/A, `:42` S036 = docs/A. INFERENCE: tier A matches the registry's de-facto convention (official first-party docs for the installed tool, cf. S006 Ghidra installed docs = A, S034 go.dev = A); no written tier rubric was found in SOURCES.md by my greps (`grep -n -i tier` outside rows returned only the header and census lines), so the A assignment is convention-consistent, not rubric-cited.

### 5. Scope

```
$ jj --version
jj 0.45.1-7c41cdeb16b6b321c64e789a966b6adf723816a5
exit=0
```

OBSERVATION: installed jj is 0.45.1, matching the doc tag; the doc's section "Colocated Jujutsu/Git workspaces" (line 100, next heading line 173) is exactly the Git-HEAD-in-colocated-workspace subject. Scope sentence is accurate and correctly bounded to the installed version.

### 6. Teaches

OBSERVATION: first half ("jj usually leaves the Git repo in a detached-HEAD state with no current branch") is directly supported by lines 114-116 ("will usually put the Git repo in a 'detached HEAD' state, since in `jj` there is not concept of a 'currently tracked branch'") and corroborated by line 208. INFERENCE: the second half ("must pin `refs/heads/<branch>` and compare HEAD against it") is the lane's application, not doc text — the doc's own remedy is `git switch` before mutating Git commands (line 117), a different problem. The pin remedy is grounded in git semantics (detached HEAD names a commit, not a branch) plus the audit evidence that motivated C2 (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:242-246`: under jj `HEAD=@-` can diverge from `main` while `git show HEAD:<path>` still succeeds) and is operationalized at `SKILL.md:573` ("Lane tools therefore pin `refs/heads/main`, never bare `HEAD`") and `SKILL.md:570` (cites `S036, git-compatibility.md:114-116`). This matches the registry's teaches convention (cf. S034's teaches, also an application sentence). Acceptable.

### 7. Gate quote, verbatim ≤25 words

```
$ python3 -I -B -c "
lines = open('/tmp/s036-git-compat.md', encoding='utf-8').read().split('\n')
seg = ' '.join(lines[113:116])
quote = '\`jj\` commands will usually put the Git repo in a \"detached HEAD\" state, since in \`jj\` there is not concept of a \"currently tracked branch\".'
print('verbatim-in-114-116:', quote in seg); print('words:', len(quote.split()))"
verbatim-in-114-116: True
words: 25
exit=0
```

OBSERVATION: `corpus/lessons/round-18.md:38` quote is verbatim inside lines 114-116 (spanning mid-114 to mid-116; the "lines 114-116" range is the containing lines, same convention as S034's "raw lines 571-573"), exactly 25 words, and preserves the doc's own grammar ("there is not concept").

### 8. Cross-references at REV

```
$ git show REV:corpus/lessons/round-18.md | grep -n "S036"
24:| SOURCES S033 (supersedes S032), S034, S035, S036 | admit (mined) | Opened 2026-10-20; quotes below |
26:| jj `latest` docs as the S036 anchor | reject | Unversioned (0.46 content); the v0.45.1 tag file is the anchor |
38:| S036 | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md, lines 114-116 | `jj` commands will usually put ... |
43:- New rows S033–S036 (3 tier A, 1 tier B community). Rows 32 → 36.
exit=0
$ git show REV:corpus/SOURCES.md | grep -c '^| S0' ; git show 9011581d...:corpus/SOURCES.md | grep -c '^| S0'
36
32
exit=0
$ git diff --stat REV -- corpus/SOURCES.md corpus/lessons/round-18.md SKILL.md
(no output) diff-exit=0
```

OBSERVATION: rows 32 → 36 confirmed (baseline max id S032); the `latest`-docs reject is grounded — main's `docs/git-compatibility.md` differs from v0.45.1 (`diff -q` exit 1, main sha256 `135a99ea40d2e626d0bc282283459650ba864df728449ac9225965578bc4e4bc`) and jj main `Cargo.toml:16` reads `version = "0.46.0"`, supporting the "(0.46 content)" parenthetical. `.ufo/waves/round-18/claims.json` amendment "C2 S036 (jj 0.45.1 git-compatibility)" matches the row. used-by verified: `corpus/lessons/round-18.md:38,50` and `SKILL.md:570,573,577`.

## Findings summary

| # | Finding | Class | Severity |
|---|---|---|---|
| 1 | Anchor id `#colocated-jujutsugit-workspaces` is the rendered-page id; raw markdown's explicit name is `colocated-jujutsugit-repos` (line 100) | observation | cosmetic |
| 2 | Line 208 is in the non-colocated-conversion recipe (section from line 191), not the colocated section; anchor field doesn't localize it | observation | cosmetic |
| 3 | Teaches' "must pin `refs/heads/<branch>`" half is lane application/inference, not doc text (doc remedy is `git switch`, line 117) | inference | none — matches teaches convention and is grounded by SKILL.md:573 + JjAuditKaidoku.md:242-246 |
| 4 | No fetch-receipt file for the S036 digest in `.ufo/waves/round-18/evidence/`; digest is fetch-time only (reproduced twice today) | observation | none — consistent with R17-S032-DIGEST lesson |

Verdict stands: HOLDS. No disagreement with the admit decision at `corpus/lessons/round-18.md:24` or the row as written; findings 1-2 are optional one-clause refinements, not corrections.
