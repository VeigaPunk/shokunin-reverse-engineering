PARTIAL

# LintBlindSpots: testing head-rev-lint's "0 live" at REV b2aad08

- **Seat:** `KaidokuR18.LintBlindSpots`. Reviewer role, advisory on the author side. Its verdict is a recommendation, not an admission.
- **REV:** `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Every `path:line` below is a line number in `git show REV:path`.
- **Lane access:** read-only git only. No jj, no REA or Ghidra, no carrier run, and no lane file edited.
- **Scratch space:** `mktemp -d /tmp/lbs-*`, plus one `tempfile.mkdtemp` made by the census. Fixture repos were made there with `git init`, never cloned, so they have no remotes. All scratch was removed (`rm exit=0`).
- **Installs:** none.

## Verdict

**The number 0 holds.** The lint at REV reports `live 0 / fixture 15 / annotated 6 / files_scanned 39` and exits 0 (R0). I ran a separate census over the same 49 files (R5) and read every hit. No missed site is a live HEAD-as-revision pin that goes unflagged. *(observation)*

**The lint does not show that 0 is true.** Three gaps:

1. **Two hidden HEAD reads in C2-fixed code.** The lint cannot see `round-17/verify.py:82` or `round-18/tools/revpin.py:108`. I copied both files into a fixture and rewrote each of the two calls as a direct call to the helper that builds the git argv, keeping the same HEAD argument on the same line. The same lint then reported **live 2** (R2).
   - `round-17/verify.py` is a routed file. It reads 0 because the HEAD read sits behind a second wrapper, not because of its annotation.
   - That `compare-only` annotation is on the comment line :81. The lint only checks the site line itself, so the annotation would have no effect.
2. **HEAD aliases get past the fixed gate.** The fixed citation-drift probe still evaluates HEAD for `--rev @`, `HEAD~0`, `HEAD^{commit}` and `HEAD@{0}` (R4). This pin happens at runtime and can be reached; no static count can see it.
3. **The named forms are missed.** Of the forms this assignment names, the lint misses `git log -1`, `git show -s`, `git describe`, `HEAD~0:path`, `@:path`, `@~0`, every runtime-built default, and quoted or backtick `HEAD` in shell. In total it missed 38 of 49 probe forms (R3).
   - None of these forms appears at REV (R5, R6), so they do not break the 0 today.
   - A strict exit 0 is still no evidence that they are absent.

## Findings by severity

### F1 (medium, calibration): two compare-only HEAD reads are hidden, and the lint's own rules count both as live once visible

**What I observed:**
- **`.ufo/waves/round-17/verify.py:82`** reads `head = _git_or_none("rev-parse", "--verify", "HEAD^{commit}")`.
  - `_git_or_none` (:63-67) calls `git` (:59-60), which builds the argv.
  - The lint treats a function as a wrapper only if its own body has a call whose first argument is a `["git", …]` literal, or assigns one (head-rev-lint.py:452-468). It classifies calls only to those wrappers (:421). So this call is never a site.
  - The annotation is on :81, a comment-only line. `python_context` only reads the site line itself (head-rev-lint.py:524-525).
- **`.ufo/waves/round-18/tools/revpin.py:108`** reads `head = _resolve(lane, "HEAD^{commit}")`.
  - `_resolve` (:79-84) holds the `rev-parse` subcommand itself and calls `_git` (:71-76).
  - This site has no annotation.
- **R0:** neither line appears in the REV lint output.
- **R2 (REV file contents in a `git init` fixture):**

  | step | lint result |
  |---|---|
  | control, files unchanged | `live 0`, only revpin.py:218 as fixture |
  | rewrite both calls as direct `git` calls (line numbers unchanged) | `live 2`: verify.py:82 live, revpin.py:108 live |
  | add the annotation text to the end of line :82 | `live 1`: verify.py:82 annotated, revpin.py:108 still live |

**Is it a live pin?** No.
- Both sites compare HEAD with the branch tip: verify.py:92 `if head != source`, and revpin.py:114 `head_equals_source`.
- Both only record the value afterwards:
  - round-17/verify.py:225 stores a boolean.
  - round-18/verify.py:278 stores `"head_revision": pin.get("head")`.
- Neither value is ever used as the revision being evaluated.

**Impact [INFERENCE]:**
- C2's "after 0" holds at these two sites only because the lint cannot see them.
- If the lint learned to follow wrappers, the claim's strict check would exit 1. That changes only if the verify.py:81 annotation moves onto :82 and revpin.py:108 gets its own annotation.
- The reverse case matters more: a real live pin written through the lane's usual helper pattern (`_git_or_none`, `_resolve`, `sha_of`) would pass `--strict` without a sound.

**Fix sketch:**
- Follow wrappers transitively, so a call that forwards `*args` to a known wrapper counts as a wrapper.
- Carry subcommand literals from the wrapper body: `_resolve` and `sha_of` imply `rev-parse`.
- Either accept an annotation on the comment-only line directly above a site, or move verify.py:81 onto :82.

### F2 (medium, operability): HEAD aliases get past the C2 refusal in citation-drift-probe

**What I observed:**
- `resolve_rev` refuses only the exact string, at :329 `if rev == "HEAD":`.
- Any other spelling counts as an explicit revision and is evaluated as given (:339-342).
- R4 used the REV probe's own fixture, `build_fixture("detached_head")`: main is clean, and HEAD is an unbookmarked off-branch commit that deletes TARGET.md. All runs used `--strict`.

| `--rev` | exit | `CITATION_DRIFT_REV_RESOLVED` | findings |
|---|---|---|---|
| (omitted) | 0 | main tip `c9fd130a2c54` | none |
| `HEAD` | 2 | `HEAD` | `head_not_branch_tip` |
| `@` | 1 | off-branch `50feb8af6d57` | `citation_file_absent` |
| `HEAD~0` | 1 | off-branch `50feb8af6d57` | `citation_file_absent` |
| `HEAD^{commit}` | 1 | off-branch `50feb8af6d57` | `citation_file_absent` |
| `HEAD@{0}` | 1 | off-branch `50feb8af6d57` | `citation_file_absent` |

- This is jj-audit R2(a): the probe judges a tree that is not on main. Here that shows up as a `citation_file_absent` false red.
- The lint itself treats `@`, `HEAD~N` and `HEAD^{…}` as HEAD (`HEAD_LIT_RE`, head-rev-lint.py:89). The gate it measures only guards the literal `HEAD`.

**Is it a live pin?** Not in registered use. The gap is reachable but dormant.
- SKILL.md:448 passes `--rev <REV>`.
- The retained receipt `.ufo/waves/round-18/evidence/jj-red-before.json` only exercised `--rev HEAD` and `--rev refs/heads/main` (R9; also jj-red-before.py:389-390 and :576-577).
- So the 14/14 receipt never tests aliases.
- [INFERENCE] In a jj lane, `@` means the working copy, but git resolves it to HEAD, which is jj's `@-`. An operator who types a jj-style `--rev @` lands on exactly the off-branch commit.

**Fix sketch:**
- Refuse when `git_commit(root, rev + "^{commit}")` equals `head_commit(root)` and that commit is not the branch tip, whatever the spelling.
- Add `@` and `HEAD~0` cases to jj-red-before.

### F3 (low, calibration): annotation labels that misstate their site

The lint trusts annotations as written (LIMITS, head-rev-lint.py:142-143). Neither case below is a live pin in the lane.

- **custody-pair.py:381** is annotated `compare-only`.
  - The same value is also written into the receipt as `# repo-HEAD:` (:385, :407). The comment on :407 itself says "retained @- pin, flagged below".
  - The lint defines `compare-only` as "HEAD read solely to compare with the branch tip" (head-rev-lint.py:37-38).
  - The value is flagged by `repo-HEAD-is-branch-tip` (:388, :411), which meets C2's "refuse or flag". So this is a wrong label, not an unflagged live pin.
- **jj-red-before.py:254-255** is annotated `red-before`.
  - In fact it is a fallback that uses HEAD in place of the branch tip: `tip = sha_of(…origin/main) or sha_of(sb, "HEAD")`.
  - That `tip` is then written into `refs/remotes/origin/main`, and possibly into `refs/heads/main` (:264-271). That is not a baseline reproduction.
  - It runs in the sandbox only. [INFERENCE] It cannot be reached while the lane has `refs/heads/main`, because `git clone --no-local` then creates `origin/main`.

### F4 (info): named forms the lint misses, none present at REV

R3 put each form in its own uncalled top-level function, so the lint's context is `live`, and ran the REV copy of the lint over them. It missed 38 of 49.

| named form | Python | shell | at REV (R5/R6) |
|---|---|---|---|
| `git log -1` (implicit HEAD) | MISSED | MISSED | absent |
| `git show -s`, `git describe` (implicit HEAD) | MISSED | MISSED | absent |
| `show HEAD`, `show HEAD:path` | caught (`other-HEAD`, `HEAD-colon`) | `"HEAD:path"` quoted: MISSED | absent in live code |
| `@` (`rev-parse @`) | caught | caught | absent |
| `@:path`, `@~0` | MISSED | not tested | absent |
| `HEAD~0` (`rev-parse HEAD~0`) | caught | caught | absent |
| `HEAD~0:path` | MISSED | MISSED | absent |
| runtime defaults: local var, env fallback, positional argparse, `--commitish`, `default="@"`, `default="HEAD~0"`, `set_defaults(rev="HEAD")` | all MISSED | `"${REV:-HEAD}"` quoted: MISSED. Bare `${REV:-HEAD}` and `REV=HEAD` then `"$REV"`: caught | in code, only `citation-drift-probe.py:563` (selftest); inside fixture strings, jj-red-before.py:733 (row 10) |
| shell `"HEAD"`, `'HEAD'`, backticks, `"$GIT"`, line continuation | n/a | all MISSED | absent |
| wrapper of a wrapper; wrapper that holds the subcommand | MISSED | n/a | **present**: verify.py:82, revpin.py:108, jj-red-before.py:255/284/318 |
| annotation on the line above the site | counted live | n/a | **present**: verify.py:81-82 (the lint never sees this site) |

**Other misses:**
- `HEAD^^`, `HEAD@{0}` and `main..HEAD`.
- `git show -m HEAD`: `VALUE_FLAGS` contains `-m` (:103-104), and it is treated as taking a value even after the subcommand.
- `diff-tree HEAD`.
- `"HEAD:" + path`.
- `["git",…] + ["rev-parse","HEAD"]`: the right-hand list is dropped at :264.
- An argv bound to a name, a `shell=True` string, and `"…".split()`.
- A generic runner that takes the argv as its 2nd positional argument.

**Do the documented limits cover this?** Only partly.
- LIMITS (:129-144) and SKILL.md:587 ("Syntactic: dynamic revision flow is a listed blind spot") cover:
  - dynamic argv and defaults,
  - cross-module wrappers,
  - complex shell quoting,
  - trusted annotations.
- They do not mention these misses, which are all static literals:
  - implicit-HEAD subcommands,
  - `HEAD~N:` and `@:` paths,
  - `@~N`, `HEAD^^`, `HEAD@{N}` and ranges,
  - `VALUE_FLAGS` applied after the subcommand,
  - the dropped right-hand list in a `+` concatenation,
  - wrappers of wrappers within one file,
  - an argv passed as a later positional argument,
  - plain `"HEAD"` quoting or backticks in shell.

## Every miss at REV in the scanned scope

These are the R5 census rows marked MISSED that use HEAD as a revision, after reading each one.

| # | REV anchor | form | why the lint misses it | live pin? |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-17/verify.py:82` | `_git_or_none("rev-parse","--verify","HEAD^{commit}")` | wrapper of a wrapper | **No**: compare-only (F1). Would count live if visible (R2) |
| 2 | `.ufo/waves/round-18/tools/revpin.py:108` | `_resolve(lane, "HEAD^{commit}")` | wrapper holds the subcommand | **No**: compare plus record (F1). No annotation |
| 3 | `.ufo/waves/round-18/tools/jj-red-before.py:255` | `sha_of(sb, "HEAD", …)`, fallback for the tip | `sha_of` (:157-162) is a wrapper of a wrapper | **No**: sandbox only. Wrong label (F3) |
| 4 | `jj-red-before.py:284` | `head_d0 = sha_of(sb, "HEAD", …)` | same | **No**: sandbox compare, annotated on the same line |
| 5 | `jj-red-before.py:318` | `head_sha = sha_of(sb, "HEAD", …)` | same | **No**: sandbox |
| 6 | `jj-red-before.py:390`, `:577` | `"--rev", "HEAD"` passed to the probe CLI | not a git argv | **No**: sandbox red/green test, annotated |
| 7 | `.ufo/gates/citation-drift/citation-drift-probe.py:553` | `argv += ["--rev", "HEAD"]` | not a git argv; annotation sits on :552 | **No**: inside `selftest()` |
| 8 | `citation-drift-probe.py:563` | `rev = "HEAD"`, then `run_check`, then `git show HEAD:…` | value built at runtime | **No**: selftest fixtures |
| 9 | `citation-drift-probe.py:329`, `:339-342` | `--rev` aliases passed through unchanged | runtime input | **Reachable but not in registered use** (F2) |
| 10 | `jj-red-before.py:729-866` (e.g. :733 `default="HEAD"`, :786 `rev-parse HEAD`, :763/:813 `sha("HEAD")`, :859 `_sha(lane, "HEAD")`; R10) | code inside string literals | strings are not parsed | **No**: selftest fixture lane |
| 11 | `custody-pair.py:383`; `round-17/verify.py:85`, `:114`; `round-18/verify.py:101` | `git status --porcelain` (compares against HEAD implicitly) | not a site kind | **No**: dirty-tree checks, not revision pins |

**Not misses:**
- The 4 seat-dir sites listed under `excluded`: audit-attack.py:91 and :349, rebuild.sh:9 and :11.
- Shell `git` lines with no HEAD: rebuild.sh:5 (`git init`/`git config`; seat-dir fixture) and run-carriers.sh:246 (`refs/heads/main^{commit}`).
- `@` used as a citation key (citation-drift-probe.py:139, :151) and as a model alias (verify-recovery.py:36).
- The string comparison `resolved == "HEAD"` at jj-red-before.py:518. The comparison at citation-drift-probe.py:329 is not a pin by itself either; it is listed in row 9 only as the anchor of F2's exact-string guard.
- Prompt text in gen-wave1.py: :72, :192, :194, :262, :321, :322.
- The lint's own LIMITS text (head-rev-lint.py:130), selftest fixture strings (:687-776, :858-859) and matcher constants (:236-237, :335, :432).

**Absence checks for the named forms** (R5, R6):
- No git argv or wrapper call at REV uses `log`, `describe`, `shortlog`, `whatchanged`, `reflog`, `diff-tree` or `worktree`.
- No code uses `HEAD~0`, `@~`, `HEAD^^`, `HEAD@{`, `shell=True`, `os.system` or `os.popen`.
- The only `git` lines in shell are rebuild.sh:5, :9 and :11 (seat dir, fixture) and run-carriers.sh:246 (`refs/heads/main^{commit}`).
- build.sh:24 builds with `-buildvcs=false`, so no VCS HEAD stamp is read.

**Fixture contexts:** I checked the callers of each of the 15 fixture sites' enclosing functions with an in-process AST walk. That check is not a pasted command. Every enclosing function is a selftest body or a fixture builder reached only from selftest. This is an observation, not a finding.

## Residual risk and verification gaps

- **Census coverage.** The census finds HEAD/`@` revision literals (including suffixes, `:path` and ranges), implicit-HEAD subcommands in literal argvs or known wrapper names, and every shell `git` line. A revision assembled without such a literal, for example read from a file, would escape both the lint and the census.
- **Unguarded revision inputs.** These accept `HEAD` and its aliases as given:
  - routed-defects, head-rev-lint, measure, controls, temporal-sweep and invocation-audit;
  - both verify.py `BASELINE_REV` arguments.
  
  Only citation-drift guards its input, and only against the literal `HEAD` (F2). The registered argvs use `<REV>` placeholders, so exposure depends on what an operator substitutes.
- **Outside the scanned scope.** There are 222 matching lines in `*.py`/`*.sh` at REV, mostly in `.ufo/waves/arc3-*` claim harnesses (R8). I did not audit them. Every script registered in SKILL.md at REV is inside the scanned directories (R7).
- **R2 mutants are not runnable equivalents.** `git` raises where `_git_or_none` returns None, and `_git` returns a CompletedProcess. That does not matter for a static lint.
- **No jj here.** The off-branch state in R4 is plain git, using the probe's own fixture, which is the same shape jj-red-before uses.
- **Concurrent edits by another seat.** Near the end of my run, `git diff --stat` (exit 0) showed uncommitted changes to 4 tracked files: custody-pair.py, round-17/verify.py, routed-defects.py and round-18/verify.py. HEAD was still REV.
  - I did not make these changes.
  - All anchors above are REV blob lines. Working-tree line numbers can differ: in the working tree, round-17/verify.py shifts by +1 after its docstring.
  - `git diff -U1` on custody-pair.py and round-17/verify.py shows the edits do not touch the F1/F3 HEAD reads. They change `LANE`/`LANE_ROOT` derivation and add `--no-optional-locks` to `_git_at`.
  - I did not read the diffs of the other two files.

## Commands and exit codes (as run)

### R0. REV lint, filtered to the affected files

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && T=$(mktemp -d /tmp/lbs-r0.XXXXXX) && git show $REV:.ufo/waves/round-18/tools/head-rev-lint.py > $T/hrl.py && python3 -I -B $T/hrl.py --root . --rev $REV > $T/out.json; echo "lint exit=$?"; python3 -I -B -c '
import json,sys
d=json.load(open(sys.argv[1]))
print("live",d["live_count"],"fixture",d["fixture_count"],"annotated",d["annotated_count"],"files_scanned",d["files_scanned"])
for s in d["sites"]:
    if s["path"].endswith(("round-17/verify.py","tools/revpin.py","tools/jj-red-before.py","citation-drift-probe.py")):
        print(" ", s["path"]+":"+str(s["line"]), s["kind"], s["context"])
' $T/out.json; echo "filter exit=$?"; echo "T=$T"
```

```
lint exit=0
live 0 fixture 15 annotated 6 files_scanned 39
  .ufo/gates/citation-drift/citation-drift-probe.py:304 other-HEAD annotated
  .ufo/gates/citation-drift/citation-drift-probe.py:452 other-HEAD fixture
  .ufo/waves/round-18/tools/jj-red-before.py:377 rev-parse-HEAD annotated
  .ufo/waves/round-18/tools/jj-red-before.py:659 rev-parse-HEAD annotated
  .ufo/waves/round-18/tools/revpin.py:218 other-HEAD fixture
filter exit=0
```

(An earlier run of the working-tree copy, `.ufo/waves/round-18/tools/head-rev-lint.py --root . --rev REV`, also exited 0 with `live 0 fixture 15 annotated 6 scanned 39 excluded 10`.)

### R1. Anchor lines

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && show(){ git show "$REV:$1" | awk -v r="$2" -v f="$1" 'BEGIN{n=split(r,a,",");for(i=1;i<=n;i++){split(a[i],b,"-");lo[i]=b[1];hi[i]=(b[2]?b[2]:b[1])}} {for(i=1;i<=n;i++) if(NR>=lo[i]&&NR<=hi[i]) {print f":"NR": "$0; break}}'; echo "  [git show exit=${PIPESTATUS[0]}]"; }; show .ufo/waves/round-17/verify.py 59-60,63-65,81-82,92; show .ufo/waves/round-18/tools/revpin.py 71-74,79-81,108,114; show .ufo/waves/round-18/tools/jj-red-before.py 157-159,254-255,284,318,389-390,576-577; show .ufo/gates/citation-drift/citation-drift-probe.py 329,339-342,551-553,562-566; show .ufo/gates/custody-pair/custody-pair.py 381,388,407
```

All 5 `git show` calls exited 0. The printed lines match the code quoted in F1-F3 and the table.

Further anchors come from `git show REV:<path>` piped into `awk 'NR>=a && NR<=b'` or `grep -n -E <pattern>`; every pipeline exited 0:
- head-rev-lint.py :37-38, :89, :103-104, :129-144, :241-265, :421, :432, :452-468, :524-525
- round-18/verify.py:278 and round-17/verify.py:225
- custody-pair.py:384-386 and :411
- build.sh:24

### R2. Inlining the wrappers makes the hidden sites count live

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && T=$(mktemp -d /tmp/lbs-r2.XXXXXX) && F=$T/f && G="git -C $F -c user.name=x -c user.email=x@invalid -c commit.gpgsign=false" && git show $REV:.ufo/waves/round-18/tools/head-rev-lint.py > $T/hrl.py && git init -q -b main $F && mkdir -p $F/.ufo/waves/round-17 $F/.ufo/waves/round-18/tools && git show $REV:.ufo/waves/round-17/verify.py > $F/.ufo/waves/round-17/verify.py && git show $REV:.ufo/waves/round-18/tools/revpin.py > $F/.ufo/waves/round-18/tools/revpin.py && $G add -A && $G commit -qm control && echo "setup exit=$?"
SUM='import json,sys; d=json.load(sys.stdin); print("live",d["live_count"],"annotated",d["annotated_count"],[(s["path"].rsplit("/",1)[1],s["line"],s["kind"],s["context"]) for s in d["sites"]])'
python3 -I -B $T/hrl.py --root $F --rev main | python3 -I -B -c "$SUM"; echo "control lint|sum exit=${PIPESTATUS[0]}|${PIPESTATUS[1]}"
python3 -I -B - $F <<'EOF'
import sys
f = sys.argv[1]
for rel, old, new in [
    (".ufo/waves/round-17/verify.py",
     'head = _git_or_none("rev-parse", "--verify", "HEAD^{commit}")',
     'head = git("rev-parse", "--verify", "HEAD^{commit}")'),
    (".ufo/waves/round-18/tools/revpin.py",
     'head = _resolve(lane, "HEAD^{commit}")',
     'head = _git(lane, "rev-parse", "--verify", "--quiet", "HEAD^{commit}")')]:
    p = f + "/" + rel
    s = open(p).read()
    assert s.count(old) == 1, rel
    open(p, "w").write(s.replace(old, new))
print("inlined 2 calls (wrapper depth 2 -> 1), line numbers unchanged")
EOF
echo "mutate exit=$?"; $G commit -qam inline; python3 -I -B $T/hrl.py --root $F --rev main | python3 -I -B -c "$SUM"; echo "mutant lint|sum exit=${PIPESTATUS[0]}|${PIPESTATUS[1]}"
python3 -I -B - $F <<'EOF'
import sys
p = sys.argv[1] + "/.ufo/waves/round-17/verify.py"
s = open(p).read()
old = 'head = git("rev-parse", "--verify", "HEAD^{commit}")'
assert s.count(old) == 1
open(p, "w").write(s.replace(old, old + "  # head-rev-lint: compare-only"))
print("moved the :81 annotation text onto the :82 site line")
EOF
echo "annotate exit=$?"; $G commit -qam annotate-same-line; python3 -I -B $T/hrl.py --root $F --rev main | python3 -I -B -c "$SUM"; echo "annotated lint|sum exit=${PIPESTATUS[0]}|${PIPESTATUS[1]}"; echo "T=$T"
```

The script prints "moved", but it actually appended the annotation text to line :82; the :81 comment stays in place.

```
setup exit=0
live 0 annotated 0 [('revpin.py', 218, 'other-HEAD', 'fixture')]
control lint|sum exit=0|0
inlined 2 calls (wrapper depth 2 -> 1), line numbers unchanged
mutate exit=0
live 2 annotated 0 [('verify.py', 82, 'rev-parse-HEAD', 'live'), ('revpin.py', 108, 'rev-parse-HEAD', 'live'), ('revpin.py', 218, 'other-HEAD', 'fixture')]
mutant lint|sum exit=0|0
moved the :81 annotation text onto the :82 site line
annotate exit=0
live 1 annotated 1 [('verify.py', 82, 'rev-parse-HEAD', 'annotated'), ('revpin.py', 108, 'rev-parse-HEAD', 'live'), ('revpin.py', 218, 'other-HEAD', 'fixture')]
annotated lint|sum exit=0|0
```

### R3. Matrix of HEAD forms

The script is in the appendix. Harness exit 0; the inner lint exit 0.

```
lint exit=0
live_count=11 annotated=0 fixture=0
probe_forms.py L23  git log -1 (implicit HEAD)                       MISSED
probe_forms.py L26  git show -s (implicit HEAD)                      MISSED
probe_forms.py L29  git describe (implicit HEAD)                     MISSED
probe_forms.py L32  show HEAD                                        [('other-HEAD', 'live')]
probe_forms.py L35  show HEAD:path                                   [('HEAD-colon', 'live')]
probe_forms.py L38  rev-parse @                                      [('rev-parse-HEAD', 'live')]
probe_forms.py L41  rev-parse HEAD~0                                 [('rev-parse-HEAD', 'live')]
probe_forms.py L44  show HEAD~0:path                                 MISSED
probe_forms.py L47  show @:path                                      MISSED
probe_forms.py L50  rev-parse @~0                                    MISSED
probe_forms.py L53  rev-parse HEAD^^                                 MISSED
probe_forms.py L56  rev-parse HEAD@{0}                               MISSED
probe_forms.py L59  log main..HEAD                                   MISSED
probe_forms.py L62  show -m HEAD (-m eaten as value flag)            MISSED
probe_forms.py L65  diff-tree HEAD (subcommand not listed)           MISSED
probe_forms.py L68  "HEAD:" + path                                   MISSED
probe_forms.py L71  ["git",...] + ["rev-parse","HEAD"]               MISSED
probe_forms.py L74-75 argv bound to a name                             MISSED
probe_forms.py L78  shell=True string                                MISSED
probe_forms.py L81  str.split() argv                                 MISSED
probe_forms.py L84-85 runtime default: local var                       MISSED
probe_forms.py L88-89 runtime default: env fallback                    MISSED
probe_forms.py L92  argparse positional default                      MISSED
probe_forms.py L95  argparse default on --commitish                  MISSED
probe_forms.py L98  argparse --rev default "@"                       MISSED
probe_forms.py L101 argparse --rev default "HEAD~0"                  MISSED
probe_forms.py L104 argparse set_defaults(rev=HEAD)                  MISSED
probe_forms.py L107 2-level wrapper (verify.py:82 shape)             MISSED
probe_forms.py L110 wrapper owns subcommand (revpin.py:108 shape)    MISSED
probe_forms.py L113-114 annotation on line above (verify.py:81 shape)    [('rev-parse-HEAD', 'live')]
probe_forms.py L117 generic runner, argv 2nd positional              MISSED
probe_forms.py L120 control: rev-parse HEAD                          [('rev-parse-HEAD', 'live')]
probe_forms.sh L2   control: $(git rev-parse HEAD)                   [('rev-parse-HEAD', 'live')]
probe_forms.sh L3   backticks                                        MISSED
probe_forms.sh L4   double-quoted "HEAD"                             MISSED
probe_forms.sh L5   single-quoted 'HEAD'                             MISSED
probe_forms.sh L6   quoted "HEAD:path"                               MISSED
probe_forms.sh L7   quoted "${REV:-HEAD}"                            MISSED
probe_forms.sh L8   control: bare ${REV:-HEAD}                       [('rev-parse-HEAD', 'live')]
probe_forms.sh L9   git log -1 (implicit HEAD)                       MISSED
probe_forms.sh L10  git show -s (implicit HEAD)                      MISSED
probe_forms.sh L11  rev-parse @                                      [('rev-parse-HEAD', 'live')]
probe_forms.sh L12  rev-parse HEAD~0                                 [('rev-parse-HEAD', 'live')]
probe_forms.sh L13  show HEAD~0:path                                 MISSED
probe_forms.sh L14  "$GIT" binary variable                           MISSED
probe_forms.sh L15-16 line continuation                                MISSED
probe_forms.sh L17  git describe (implicit HEAD)                     MISSED
probe_forms.sh L18  log main..HEAD                                   MISSED
probe_forms.sh L19-20 control: REV=HEAD then "$REV"                    [('rev-parse-HEAD', 'live')]
forms=49 missed=38
harness exit=0
```

### R4. HEAD aliases get past the citation-drift refusal

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && T=$(mktemp -d /tmp/lbs-r4b.XXXXXX) && git show $REV:.ufo/gates/citation-drift/citation-drift-probe.py > $T/cdp.py && python3 -I -B - "$T" <<'EOF'
import hashlib, importlib.util, json, os, subprocess, sys
T = sys.argv[1]; probe = os.path.join(T, "cdp.py")
spec = importlib.util.spec_from_file_location("cdp", probe); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root = m.build_fixture("detached_head")  # REV fixture: main clean; HEAD = unbookmarked off-branch commit that deletes TARGET.md
table = os.path.join(T, "table.json"); json.dump(m.fixture_table("clean"), open(table, "w"))
exp = os.path.join(T, "expected.json")
json.dump({"snapshots": {}, "pointer_table": {"sha256": hashlib.sha256(open(table, "rb").read()).hexdigest()}}, open(exp, "w"))
sha = lambda r: subprocess.run(["git", "-C", root, "rev-parse", "--verify", r], capture_output=True, text=True).stdout.strip()[:12]
print("main=%s HEAD=%s" % (sha("refs/heads/main"), sha("HEAD")))
for rev in [None, "HEAD", "@", "HEAD~0", "HEAD^{commit}", "HEAD@{0}"]:
    argv = [sys.executable, "-I", "-B", probe, "--root", root, "--table", table, "--expected", exp, "--strict"] + (["--rev", rev] if rev else [])
    p = subprocess.run(argv, capture_output=True, text=True)
    out = {l.split(":", 1)[0]: l.split(":", 1)[1].strip() for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT_")}
    ids = sorted({l.split(":", 1)[1].strip().split(" ", 1)[0] for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT:")})
    print("--rev %-14s exit=%d resolved=%-12s findings=%s" % (rev or "(omitted)", p.returncode, out.get("CITATION_DRIFT_REV_RESOLVED", "?")[:12], ids))
subprocess.run(["rm", "-rf", root])
EOF
echo "harness exit=$?"; rm -rf "$T" /tmp/lbs-r4.PT0zi8; echo "cleanup exit=$?"
```

```
main=c9fd130a2c54 HEAD=50feb8af6d57
--rev (omitted)      exit=0 resolved=c9fd130a2c54 findings=[]
--rev HEAD           exit=2 resolved=HEAD         findings=['head_not_branch_tip']
--rev @              exit=1 resolved=50feb8af6d57 findings=['citation_file_absent']
--rev HEAD~0         exit=1 resolved=50feb8af6d57 findings=['citation_file_absent']
--rev HEAD^{commit}  exit=1 resolved=50feb8af6d57 findings=['citation_file_absent']
--rev HEAD@{0}       exit=1 resolved=50feb8af6d57 findings=['citation_file_absent']
harness exit=0
cleanup exit=0
```

An earlier identical run, which did not print the resolved revision, gave the same exits: 0, 2, 1, 1, 1, 1.

### R5. Independent census of the scanned scope

The script is in the appendix. Census exit 0. It reports `files=49 lint_live=0 lint_sites=25`. Each row it marks MISSED is either one of table rows 1-11 or one of the "not misses" listed under that table.

The census's string pattern only matches a `git … HEAD` that sits on a single line. So for row 10 it flagged only :778. The other row-10 lines come from R10.

### R6. Grep REV scope for the named forms (exit 0)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; git grep -n -E '"log"|\bgit +log\b|"describe"|\bgit +describe\b|"diff-tree"|"shortlog"|shell=True|os\.system|os\.popen|HEAD~0|"@"|@~|HEAD\^\^|HEAD@\{' $REV -- ':(glob).ufo/{gates,rounds}/**/*.py' ':(glob).ufo/{gates,rounds}/**/*.sh' ':(glob).ufo/waves/round-1[4-8]/**/*.py' ':(glob).ufo/waves/round-1[4-8]/**/*.sh' | sed "s/^$REV://" | cut -c1-150; echo "git grep exit=${PIPESTATUS[0]}"
```

Every hit is non-code or non-git:
- prompt text in gen-wave1.py:194 and :322;
- the lint's own `REV_COMMANDS` (head-rev-lint.py:97-100) and its fixture string (:710-711);
- `("LOG.md", "log")` labels in routed-defects.py:430, 473, 479, 515.

### R7. Scripts registered in SKILL.md at REV (exit 0)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; git show $REV:SKILL.md | grep -n -o -E '(python3|bash|sh)[^`|]*\.ufo/[^ `|]*\.(py|sh)' | sed -E 's/^([0-9]+):.*(\.ufo\/[^ ]*\.(py|sh)).*/\1 \2/' | sort -k2 -u | awk '{print $2" (SKILL.md:"$1")"}'; echo "exit=${PIPESTATUS[1]}"
```

It lists 28 scripts, all under `.ufo/gates/`, `.ufo/rounds/` or `.ufo/waves/round-1[4-8]/`.

### R8. Matches outside the scanned scope (exit 0, 222 lines)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git grep -n -E 'rev-parse["'"'"', ]+(HEAD|@)|"HEAD"|git log -1|"log", "-1"' b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- '*.py' '*.sh' ':!.ufo/gates' ':!.ufo/rounds' ':!.ufo/waves/round-14' ':!.ufo/waves/round-15' ':!.ufo/waves/round-16' ':!.ufo/waves/round-17' ':!.ufo/waves/round-18' | wc -l; echo "exit=${PIPESTATUS[0]}"
```

### R9. `--rev` values in the retained jj-red-before receipt (exit 0)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; git show $REV:.ufo/waves/round-18/evidence/jj-red-before.json | python3 -I -B -c '
import json,sys
d=json.load(sys.stdin)
print(sorted(d.keys()))
exps=d.get("expectations") or d.get("expects") or []
print("expectations:",len(exps), "held:", sum(1 for e in exps if e.get("held") or e.get("ok")))
revs=set()
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v)
    elif isinstance(o,list):
        for i,x in enumerate(o):
            if x=="--rev" and i+1<len(o): revs.add(o[i+1])
            walk(x)
walk(d)
print("--rev values used:", sorted(revs))
'; echo "exit=${PIPESTATUS[1]}"
```

```
['all_held', 'baseline_extracts', 'baseline_rev', 'branch', 'expectations', 'lane', 'lane_tip', 'not_runnable', 'setup', 'steps', 'tool']
expectations: 14 held: 14
--rev values used: ['HEAD', 'refs/heads/main']
exit=0
```

### R10. HEAD forms inside jj-red-before's embedded fixture scripts (exit 0|0)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/jj-red-before.py | grep -n -E '^FIXTURE_[A-Z_]+ *=|"HEAD"' | awk -F: '$1>=700 && $1<=870'; echo "exit=${PIPESTATUS[0]}|${PIPESTATUS[1]}"
```

Lines printed: 729 `FIXTURE_CD_BASELINE`, 733 `ap.add_argument("--rev", default="HEAD")`, 750 `FIXTURE_CD_FIXED`, 763 `sha("HEAD")`, 764 `a.rev == "HEAD"`, 775 `FIXTURE_CD_REGRESSED`, 778 `FIXTURE_CP_BASELINE`, 786 `["git", "rev-parse", "HEAD"]`, 798 `FIXTURE_CP_FIXED`, 813 `sha("HEAD")`, 835 `FIXTURE_CP_REGRESSED`, 838 `FIXTURE_REVPIN`, 859 `_sha(lane, "HEAD")`. Every HEAD line is annotated `red-before (selftest fixture)`.

### Cleanup (exit 0)

```bash
rm -rf /tmp/lbs-census.sUNgKl /tmp/lbs-r0.g6Z8Vp /tmp/lbs-r2.K0brqO /tmp/lbs-r3.fbnzhx /tmp/scope /tmp/hrl-rev.json /tmp/hrl-rev.err /tmp/tmpv41yj4p6; echo "rm exit=$?"
```

`/tmp/scope` held REV contents read with `git show` for local AST walks. `/tmp/tmpv41yj4p6` was the census's lint copy, which matched the REV blob byte for byte.

## Appendix: scripts as run

### R3 harness

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && T=$(mktemp -d /tmp/lbs-r3.XXXXXX) && git show $REV:.ufo/waves/round-18/tools/head-rev-lint.py > $T/hrl.py && python3 -I -B - "$T" <<'EOF'
import json, os, subprocess, sys
T = sys.argv[1]; F = os.path.join(T, "f"); W = os.path.join(F, ".ufo/waves/round-18")
os.makedirs(W)
PY = [  # (label, lines) -- each form in its own uncalled top-level function => lint context "live"
 ("git log -1 (implicit HEAD)", ['subprocess.run(["git", "log", "-1", "--format=%H"])']),
 ("git show -s (implicit HEAD)", ['subprocess.run(["git", "show", "-s", "--format=%H"])']),
 ("git describe (implicit HEAD)", ['subprocess.run(["git", "describe", "--always"])']),
 ("show HEAD", ['subprocess.run(["git", "show", "HEAD"])']),
 ("show HEAD:path", ['subprocess.run(["git", "show", "HEAD:LOG.md"])']),
 ("rev-parse @", ['subprocess.run(["git", "rev-parse", "@"])']),
 ("rev-parse HEAD~0", ['subprocess.run(["git", "rev-parse", "HEAD~0"])']),
 ("show HEAD~0:path", ['subprocess.run(["git", "show", "HEAD~0:LOG.md"])']),
 ("show @:path", ['subprocess.run(["git", "show", "@:LOG.md"])']),
 ("rev-parse @~0", ['subprocess.run(["git", "rev-parse", "@~0"])']),
 ("rev-parse HEAD^^", ['subprocess.run(["git", "rev-parse", "HEAD^^"])']),
 ("rev-parse HEAD@{0}", ['subprocess.run(["git", "rev-parse", "HEAD@{0}"])']),
 ("log main..HEAD", ['subprocess.run(["git", "log", "main..HEAD"])']),
 ("show -m HEAD (-m eaten as value flag)", ['subprocess.run(["git", "show", "-m", "HEAD"])']),
 ("diff-tree HEAD (subcommand not listed)", ['subprocess.run(["git", "diff-tree", "-r", "HEAD"])']),
 ('"HEAD:" + path', ['subprocess.run(["git", "show", "HEAD:" + str(1)])']),
 ('["git",...] + ["rev-parse","HEAD"]', ['subprocess.run(["git", "-C", "."] + ["rev-parse", "HEAD"])']),
 ("argv bound to a name", ['cmd = ["git", "rev-parse", "HEAD"]', 'subprocess.run(cmd)']),
 ("shell=True string", ['subprocess.run("git rev-parse HEAD", shell=True)']),
 ("str.split() argv", ['subprocess.run("git rev-parse HEAD".split())']),
 ("runtime default: local var", ['rev = "HEAD"', 'subprocess.run(["git", "rev-parse", rev])']),
 ("runtime default: env fallback", ['rev = os.environ.get("LANE_REV", "HEAD")', 'subprocess.run(["git", "show", rev + ":LOG.md"])']),
 ("argparse positional default", ['argparse.ArgumentParser().add_argument("revision", nargs="?", default="HEAD")']),
 ("argparse default on --commitish", ['argparse.ArgumentParser().add_argument("--commitish", default="HEAD")']),
 ('argparse --rev default "@"', ['argparse.ArgumentParser().add_argument("--rev", default="@")']),
 ('argparse --rev default "HEAD~0"', ['argparse.ArgumentParser().add_argument("--rev", default="HEAD~0")']),
 ("argparse set_defaults(rev=HEAD)", ['argparse.ArgumentParser().set_defaults(rev="HEAD")']),
 ("2-level wrapper (verify.py:82 shape)", ['h2("rev-parse", "--verify", "HEAD^{commit}")']),
 ("wrapper owns subcommand (revpin.py:108 shape)", ['resolve("HEAD^{commit}")']),
 ("annotation on line above (verify.py:81 shape)", ['# head-rev-lint: compare-only', 'subprocess.run(["git", "rev-parse", "HEAD"])']),
 ("generic runner, argv 2nd positional", ['runlog("label", ["git", "rev-parse", "HEAD"])']),
 ("control: rev-parse HEAD", ['subprocess.run(["git", "rev-parse", "HEAD"])']),
]
src = ["import argparse", "import os", "import subprocess", "", "",
       "def g1(*a):", '    return subprocess.run(["git", *a])', "", "",
       "def h2(*a):", "    return g1(*a)", "", "",
       "def resolve(r):", '    return g1("rev-parse", "--verify", r)', "", "",
       "def runlog(label, argv):", "    return subprocess.run(argv)", ""]
spans = []
for i, (label, lines) in enumerate(PY):
    src += ["", "def form_%02d():" % i]
    lo = len(src) + 1
    src += ["    " + l for l in lines]
    spans.append(("probe_forms.py", label, lo, len(src)))
open(os.path.join(W, "probe_forms.py"), "w").write("\n".join(src) + "\n")
SH = [
 ("control: $(git rev-parse HEAD)", ['R=$(git rev-parse HEAD)']),
 ("backticks", ['R=`git rev-parse HEAD`']),
 ('double-quoted "HEAD"', ['git rev-parse "HEAD"']),
 ("single-quoted 'HEAD'", ["git rev-parse 'HEAD'"]),
 ('quoted "HEAD:path"', ['git show "HEAD:LOG.md"']),
 ('quoted "${REV:-HEAD}"', ['git rev-parse "${REV:-HEAD}"']),
 ("control: bare ${REV:-HEAD}", ['git rev-parse ${REV:-HEAD}']),
 ("git log -1 (implicit HEAD)", ['git log -1 --format=%H']),
 ("git show -s (implicit HEAD)", ['git show -s --format=%H']),
 ("rev-parse @", ['git rev-parse @']),
 ("rev-parse HEAD~0", ['git rev-parse HEAD~0']),
 ("show HEAD~0:path", ['git show HEAD~0:LOG.md']),
 ('"$GIT" binary variable', ['"$GIT" rev-parse HEAD']),
 ("line continuation", ['git \\', '  rev-parse HEAD']),
 ("git describe (implicit HEAD)", ['git describe --always']),
 ("log main..HEAD", ['git log main..HEAD']),
 ("control: REV=HEAD then \"$REV\"", ['REV=HEAD', 'git rev-parse "$REV"']),
]
sh = ["#!/bin/sh"]
for label, lines in SH:
    lo = len(sh) + 1; sh += lines; spans.append(("probe_forms.sh", label, lo, len(sh)))
open(os.path.join(W, "probe_forms.sh"), "w").write("\n".join(sh) + "\n")
G = ["git", "-C", F, "-c", "user.name=x", "-c", "user.email=x@invalid", "-c", "commit.gpgsign=false"]
subprocess.run(["git", "init", "-q", "-b", "main", F], check=True)
subprocess.run(G + ["add", "-A"], check=True); subprocess.run(G + ["commit", "-qm", "forms"], check=True)
p = subprocess.run([sys.executable, "-I", "-B", os.path.join(T, "hrl.py"), "--root", F, "--rev", "main"], capture_output=True, text=True)
print("lint exit=%d" % p.returncode)
d = json.loads(p.stdout)
print("live_count=%d annotated=%d fixture=%d" % (d["live_count"], d["annotated_count"], d["fixture_count"]))
missed = 0
for fname, label, lo, hi in spans:
    hits = [(s["kind"], s["context"]) for s in d["sites"] if s["path"].endswith(fname) and lo <= s["line"] <= hi]
    missed += not hits
    print("%-14s L%-3s %-48s %s" % (fname, lo if lo == hi else "%d-%d" % (lo, hi), label, hits or "MISSED"))
print("forms=%d missed=%d" % (len(spans), missed))
EOF
echo "harness exit=$?"; echo "T=$T"
```

### R5 census

`census.py` sha256 `185e2af8ecddf7ddf68d91b00e5d4287c627fd69262189a6f02b0eb26123e4ab`, 34 lines. Run as `python3 -I -B $T/census.py . b2aad08ceeee8dd125ce0d316056d8bd766c7f94; echo "census exit=$?"`, which printed `census exit=0`.

```python
# usage: python3 -I -B census.py LANE REV  (read-only: git ls-tree/show/rev-parse; runs REV's head-rev-lint from a blob copy)
import ast, json, os, re, subprocess, sys, tempfile
LANE, REV = sys.argv[1], sys.argv[2]
git = lambda *a: subprocess.run(["git", "-C", LANE, *a], capture_output=True, check=True).stdout
DIRS = [".ufo/gates", ".ufo/rounds"] + [".ufo/waves/round-%d" % n for n in range(14, 19)]
files = [f for f in git("ls-tree", "-r", "--name-only", REV, "--", *DIRS).decode().splitlines() if f.endswith((".py", ".sh"))]
lint_py = os.path.join(tempfile.mkdtemp(), "hrl.py"); open(lint_py, "wb").write(git("show", REV + ":.ufo/waves/round-18/tools/head-rev-lint.py"))
out = json.loads(subprocess.run([sys.executable, "-I", "-B", lint_py, "--root", LANE, "--rev", REV], capture_output=True, check=True).stdout)
seen = {(s["path"], s["line"]) for s in out["sites"]} | {(e["path"], s["line"]) for e in out["excluded"] for s in e["sites"]}
REVTOK = re.compile(r"^(?:HEAD|@)(?:[~^][0-9]*|\^\{[^}]*\}|@\{[^}]*\})*(?::.*)?$|\.\.\.?(?:HEAD|@)\b|\b(?:HEAD|@)\.\.")
IMPLICIT = {"log", "describe", "shortlog", "whatchanged", "reflog", "diff-tree", "worktree", "status"}
rows = []
for f in files:
    src = git("show", "%s:%s" % (REV, f)).decode()
    if f.endswith(".sh"):
        for i, l in enumerate(src.splitlines(), 1):
            if re.search(r"\bgit\b", l) and not l.strip().startswith("#"):
                rows.append((f, i, "sh-git-line", (f, i) in seen, l.strip()[:70]))
        continue
    tree = ast.parse(src); docs = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body and isinstance(n.body[0], ast.Expr)}
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs and (REVTOK.search(n.value) or re.search(r"\bgit\b[^\n]*\b(HEAD|log|describe)\b", n.value)):
            rows.append((f, n.lineno, "head-token %r" % n.value[:40], (f, n.lineno) in seen, src.splitlines()[n.lineno - 1].strip()[:70]))
        if isinstance(n, (ast.List, ast.Tuple)) and n.elts and isinstance(n.elts[0], ast.Constant) and n.elts[0].value == "git":
            sub = [e.value for e in n.elts[1:] if isinstance(e, ast.Constant) and isinstance(e.value, str) and not e.value.startswith("-")]
            if sub and sub[0] in IMPLICIT:
                rows.append((f, n.lineno, "implicit-HEAD subcommand %s" % sub[0], (f, n.lineno) in seen, src.splitlines()[n.lineno - 1].strip()[:70]))
        if isinstance(n, ast.Call) and getattr(n.func, "attr", getattr(n.func, "id", "")) in IMPLICIT | {"_git_at", "git", "_git", "run"}:
            sub = [a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str) and not a.value.startswith("-")]
            if sub and sub[0] in IMPLICIT:
                rows.append((f, n.lineno, "implicit-HEAD subcommand %s (wrapper)" % sub[0], (f, n.lineno) in seen, src.splitlines()[n.lineno - 1].strip()[:70]))
print("files=%d lint_live=%d lint_sites=%d" % (len(files), out["live_count"], len(seen)))
for f, l, what, s, code in sorted(set(rows)):
    print("%s:%d  lint=%s  %s  | %s" % (f, l, "seen" if s else "MISSED", what, code))
```

**Census caveats:**
- Hits are keyed by the constant's line, so a token that sits on the line after its call's opening shows as `seen` only if the lint reported that same line. It did for all multi-line calls at REV (e.g. citation-drift-probe.py:304, temporal-sweep.py:343).
- Shell lines are not tokenized; the census lists every `git` line for reading.
