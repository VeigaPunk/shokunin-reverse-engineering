# R45W1SrcCensus — SOURCES census + append-only guard at the freeze

Seat: `R45W1SrcCensus` (leaf). Round 45 wave 1, lane `kaidoku`.
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Base `149133d47aa7e90796f96047afe6d251a3e65b2c`, freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`,
HEAD at measurement `faa875bc0eb839d15b83c4afa6078819e5a7b381`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W1SrcCensus` (`TMPDIR=$S`), removed after copy.
Raw ledger with per-receipt stdout sha256 and UTC stamps: `receipts.log` (this directory).
No lane path, frozen path, registry, lesson, LOG, SCORECARD or git index was written. No git mutating
command was run; the only commits created are inside `$S` fixtures whose toplevel was verified equal to `$D`.

## Invocation form (documented, not the prompt's)

The prompt gave `--base … --head …`. `tools/round-38/registry-immutable.sh` has no option parser:
its documented form is positional, `registry-immutable.sh LANE BASE REV` (header line 2, and
`lane=$1 base=$2 rev=$3` at line ~118). `--base` would be consumed as the lane and the script would
die on an unknown lane. **All guard receipts below use the documented positional form**, with the
prompt's argument values in that order.

## The three assigned receipts

### 1. SOURCES census validate

```
cmd:  bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
exit: 0
utc:  2026-10-28T15:40:59Z
stdout_sha256: 9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19
stdout_bytes:  1518      stderr_bytes: 0
W04 lines:     14        E-code lines: 0
```

stdout (all of it; the last line is the lane verdict):

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S123 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S138 duplicate url github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

Interpretation, grounded in the script's W04 arm (`scripts/sources-census.sh:644`): a line is printed
for each row that is the **first to pair an already-seen URL with a new scope**
(`u in url_seen && !(scope_key in url_scopes)`). 14 lines = 14 such rows over **10 distinct URLs**
(rea-agents tarball ×5; the remaining nine URLs once each). W codes never set the exit code
(`:795-806`: only `missing`/`findings` do), so exit 0 with 14 W04 is the instrument's clean-lane
answer, not a swallowed error. The validated bytes are the worktree file, sha256
`70be416d0294871d969b587bd4eb2f4980bc46f1d8faa9636ecf0176edbc401a`, equal to `HEAD:corpus/SOURCES.md`
(no uncommitted drift: `git status --porcelain` shows only `.ufo/waves/round-45/w1.ready.dispatched`).

### 2. Append-only guard, base → freeze

```
cmd:  bash tools/round-38/registry-immutable.sh . 149133d47aa7e90796f96047afe6d251a3e65b2c f762b7273e3f6ca3c710bb37d5de92a4a4417aec
exit: 0
utc:  2026-10-28T15:40:59Z
stdout_sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855   (sha256 of the empty string)
stdout_bytes:  0        stderr_bytes: 0
```

**No row changed outside status/recheck/used-by.** The guard prints one line per offending row and
exits 1; empty stdout + exit 0 is the clean result.

**This interval is vacuous, and that matters.** `corpus/SOURCES.md` is byte-identical at base and at
freeze — same blob sha256 `90a10fddc549777e841182986f4841d4736721ac05955d85bbf1d11641255dfd`,
same 139 rows:

| rev | rows | SOURCES.md sha256 |
|---|---|---|
| `149133d4` (base) | 139 | `90a10fddc549777e841182986f4841d4736721ac05955d85bbf1d11641255dfd` |
| `f762b727` (freeze) | 139 | `90a10fddc549777e841182986f4841d4736721ac05955d85bbf1d11641255dfd` |
| `faa875bc` (HEAD) | 141 | `70be416d0294871d969b587bd4eb2f4980bc46f1d8faa9636ecf0176edbc401a` |

So exit 0 here is true but carries no discriminating weight: there was nothing to differ. The guard
is not vacuous in general — the interval that exercises it is freeze → HEAD, where the registry grew
by two rows (R6 below), and the selftest (R5) proves the red arms fire.

### 3. Registry row count

```
cmd:  grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
exit: 0
utc:  2026-10-28T15:40:59Z
stdout: 141            stdout_sha256: 85a0e6eb5530a682fa88345a5e7a144248f49e5b71b3eb587a9db5cd2957495a
```

(Prompt wrote the pattern with doubled braces, i.e. Python-format-escaped; the effective ERE is the
one above.) `141` rows at HEAD, of which 139 predate the freeze.

## Supplementary receipts (same run, same tooling)

### R4 — census mode, three-way count agreement

```
cmd:  bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
exit: 0   utc: 2026-10-28T15:40:59Z   stdout_sha256: 01eb62a20aebb739a171fe8547f4f25ecb3423174b2861251bcba45c07e7964d
kaidoku	rows	141
kaidoku	tier.A	133   tier.B 7   tier.C 1        (133+7+1 = 141)
kaidoku	status.mined	136   status.rejected 5   (136+5 = 141; queued 0)
FLEET	rows	141   missing 0   tier.invalid 0   status.invalid 0
```

Three independent implementations agree on 141: the prompt's `grep`, the guard's stricter row regex
`^ {0,3}\| *S[0-9]{3,} *\|` (also 141 on the same bytes), and the census `rows` metric.

### R5 — guard selftest: the exit codes are semantic, not decorative

```
cmd:  bash tools/round-38/registry-immutable.sh --selftest
exit: 0   utc: 2026-10-28T15:40:59Z   stdout_sha256: e08d3d03b35982b244ea342273b747079fc23b1cab3a8fb5a23b8f25795ea2d1
case append-only:   expect exit=0 got 0 PASS
case in-place-cell: expect exit=1 got 1 PASS      (prints "S002 changed columns: 6")
case row-deletion:  expect exit=1 got 1 PASS
case row-reorder:   expect exit=1 got 1 PASS
case allowed-cells: expect exit=0 got 0 PASS
SELFTEST cases=5 pass=5 fail=0
```

The guard's 1 is a *detection*, demonstrated on a throwaway fixture under `$S` (toplevel verified
equal to `$D`). Fixture scaffolding was removed with `$S`.

### R6 — the intervals that carry information

```
cmd:  bash tools/round-38/registry-immutable.sh . 149133d4 HEAD      exit 0   stdout empty (sha e3b0c442…)
cmd:  bash tools/round-38/registry-immutable.sh . f762b72 HEAD       exit 0   stdout empty (sha e3b0c442…)
ids present at HEAD and absent at freeze: S140, S141
commits adding them: e715263c 2026-10-28T12:33:03-0300 "round-45: land SKILL rule block 22 … S140/S141; the lesson"
```

Two legal appends, zero in-place edits, zero deletions, zero reorder — across the whole base → HEAD
span. That is the receipt with discriminating power for corpus rule 2 this round.

### R7 — `validate --file` is not a freeze-revision census (usage hazard)

```
cmd:  bash scripts/sources-census.sh validate --file $S/SOURCES.at-freeze.md        exit 1  W04 14  E11 231
cmd:  bash scripts/sources-census.sh validate --file $S/S.head.md  (bytes == HEAD:corpus/SOURCES.md)
                                                                                  exit 1  W04 14  E11 233
```

Same bytes that R1 validated cleanly (`E=0`, exit 0) produce 231/233 `E11 missing used-by` lines and
exit 1 in `--file` mode. Cause, from the source (`scripts/sources-census.sh:497-501`): `--file` sets
`dir = realpath(dirname(file))/..`, and the used-by check tests `[ -e "$dir/$path" ]` (`:566-568`).
Unless the snapshot sits at `<lane>/corpus/SOURCES.md` inside a lane whose used-by targets exist,
every used-by path resolves against the wrong root. **Do not read `--file` E11 counts as lane
findings**, and do not use `--file` to produce a claim's before/after census.

### R8 — the census's section-boundary rule fires (E12)

`S141`'s row relocated verbatim into `## Leads (unopened)` on an otherwise identical copy:

```
cmd:  bash scripts/sources-census.sh validate --file $S/S.leads.md
exit: 1   stdout_sha256: 844d2539996aee873fa9c41ebe93b32cca82ce3c83ca23d0fd1da5b57e6d2283
file	E12	S141 row outside Registry section        (exactly 1 E12 line; grep sha 2bde4845…)
```

### R9 — the guard alone has a section-boundary hole; the census closes it

Fixture (`$S/fx-leads`, own repo, toplevel verified): base = three registry rows; rev = same three
plus one row appended **under `## Leads`**.

```
cmd:  bash tools/round-38/registry-immutable.sh $D $C0 $C1
exit: 0   stdout empty          <-- guard sees no violation
cmd:  bash scripts/sources-census.sh validate --file $S/p2.tip.md
exit: 1   file	E12	S900 row outside Registry section
```

The guard's `rows()` (`registry-immutable.sh:~130`) greps the whole file with no `## Registry`
section filter, so a row-shaped line outside the registry is simply "a row at both revs" or "an
append". Consequence for scoring: **the guard is a cell-stability checker, not a registry-membership
checker.** A row that leaves `## Registry` (still present in the file, e.g. relocated into `##
Search log`) reads as unchanged to the guard and is caught only by census E12. Any wave-2 claim that
rests on "no registry row changed" must run both.

### R10 — the round-45 freeze bytes are intact

```
git diff --stat f762b727..HEAD -- plans/round-45-claims.md tools/round-45/     -> empty
git diff --stat f762b727     -- plans/round-45-claims.md tools/round-45/      -> empty (worktree)
git log --format='%h %s' f762b727..HEAD -- plans/round-45-claims.md tools/round-45/   -> 0 commits
```

Five commits landed after the freeze (`9ff920cd`, `e715263c`, `1f4b27f8` amendment A1, `abfeda50`,
`faa875bc`) and none touches a frozen path. `git log --format=%H -1 -- plans/round-45-claims.md`
re-derives `f762b727…` as the claims file's freeze, matching the prompt.

Caveat for the worktree arm: the frozen **directory** contains git-ignored artefacts —

```
git status --porcelain --ignored --untracked-files=all -- tools/round-45/
!! tools/round-45/__pycache__/c1-counter.cpython-314.pyc
!! tools/round-45/__pycache__/c2-counter.cpython-314.pyc
```

A `--pathspec tools/round-45/` gate that enumerates the filesystem rather than git objects would see
two extra files inside a frozen directory. The freeze itself is a commit-tree pathspec, so this is
not a freeze violation; it is a trap for the dirty/worktree arm and is reported, not fixed.

### R11 — duplicate detection is backtick-sensitive (instrument accuracy)

The W04 URL for the go.dev rows prints as `go.dev/dl/?mode=json&include=all``, — with the Markdown
closing backtick glued on. `url_of()` (`:600-607`) takes the `[^[:space:]|]+` token and strips only a
fragment and a trailing slash. Probe: two rows with the *same* URL, one backticked and one bare:

```
cmd:  bash scripts/sources-census.sh validate --file $D/corpus/SOURCES.md
exit: 1   E04=0   W04=0        (only the 2 expected E11 lines)
```

So a duplicate whose only difference is cell formatting is invisible to both W04 and E04. Live impact
today is nil — `S038` and `S047` are both backticked, so they normalize identically and S047 is
flagged — but a future row writing the URL bare would silence its own duplicate warning.

### R12 — provenance of the guard itself

```
git log -- tools/round-38/registry-immutable.sh
7a1ac7fe 2026-10-26  round-38 (attempt 2): … registry-immutable check …
52b0eb29 2026-10-26  round-39: … r38 gate selftests …          (+100 / -2 on this file)
```

The deletion arm, the reorder arm and `--selftest` all arrive at `52b0eb29`, i.e. the round-38
instrument was extended in place during round 39. The note added by that commit still says, inside
this very file, "It is NOT the assigned deliverable; `tools/round-38/registry-immutable.sh` is
unchanged by this seat" — a header that contradicts the file it is written in. The guard I cite is
therefore **not** the round-38 delivered bytes; the `tools/round-38/` label overstates its age. The
check logic I exercised (cell comparison, exit codes) is the extended version and behaves as the
selftest describes; `tools/round-39/` holds no copy of the file.

### R13 — R45-C2 scope preconditions (bounded, not a C2 score)

All six paths enumerated by `tools/round-45/registry-scope.json` exist at **both** HEAD and the
freeze (`git cat-file -e`): `tools/round-44/{c1-counter.py,c1-run.sh,c2-counter.py}`,
`tools/round-45/{frozen-path-preflight.py,c1-counter.py,c2-counter.py}`. The scope file's six paths
equal the set named by the two claim files, so `scope_size == 6` is falsifiable rather than assumed.
Scoring C1/C2 belongs to other seats.

### R15 — the guard has no could-not-evaluate arm; three failure modes, two of them fabricated findings

The guard's contract says 0 clean / 1 row changed. Probes (all read-only, no lane mutation):

```
# rev unreadable
bash tools/round-38/registry-immutable.sh . 149133d4 deadbeef…(nonexistent)     exit 1, 139 lines, all "row deleted (append-only)"
# base unreadable, rev = freeze (139 rows)
bash tools/round-38/registry-immutable.sh . deadbeef…(nonexistent) f762b72      exit 1, 139 lines, all "row deleted (append-only)"
# base unreadable, rev = HEAD (141 rows)
bash tools/round-38/registry-immutable.sh . deadbeef…(nonexistent) HEAD          exit 1, 141 lines, all "row deleted (append-only)"
# lane path nonexistent
bash tools/round-38/registry-immutable.sh /nonexistent-lane 149133d4 HEAD       exit 0, empty stdout, git fatal on stderr
# lane path is a directory but not a repository
bash tools/round-38/registry-immutable.sh $S/notarepo 149133d4 HEAD             exit 0, git fatal on stderr
```

Three distinct defects, none of them exit 2:

1. **Silent pass on an unresolvable lane.** A nonexistent path or a non-repo directory yields
   `rows()` = empty for both sides, awk finishes with `hit=0`, and the guard exits **0**. A caller
   cannot distinguish "registry is append-only" from "I never read the registry". This is the same
   class as the round-44 defect the round is trying to kill.
2. **Fabricated violations on an unresolvable rev.** Exit 1 with one `S<n> row deleted (append-only)`
   line per base row. 139 false findings for a typo'd sha.
3. **Fabricated violations on an unresolvable base, with a mechanism.** The output count equals the
   number of **rev** rows, not base rows (139 for `f762b72`, 141 for `HEAD`). [INFERENCE from the
   awk at `registry-immutable.sh:~130` plus the observed counts] when the first input is empty the
   `NR==FNR` test stays true for the whole second file, so the rev rows load into the *base* map and
   the END block reports every one of them deleted.

Operational consequence for this round: the guard's exit 0 is admissible only if the lane, both revs
and a non-empty base row set are known good. The assigned receipt (2) is admissible because
`149133d4` and `f762b727` resolve in this repo and the row set is 139, not 0 — and because of R16.

### R16 — positive control: the guard reads this lane's real rows

Reverse interval on the real lane (`HEAD` as base, freeze as rev) — the two post-freeze rows must
surface as deletions if the arm is live on the actual file:

```
bash tools/round-38/registry-immutable.sh . HEAD f762b7273e3f6ca3c710bb37d5de92a4a4417aec
exit 1
S140 row deleted (append-only)
S141 row deleted (append-only)
```

Exactly two lines, exactly the two ids that the freeze → HEAD interval added. This makes receipt (2)
non-vacuous as a *reading of this lane* (the guard sees all 139/141 rows), even though the interval
itself carries no delta, and it independently confirms S140/S141 are the only rows added after the
freeze.

## What the three receipts do NOT establish

- The guard receipt (2) does not establish that the registry is append-only *in general* — the
  interval had zero delta. R6/R5 carry that weight.
- The census receipt (1) is an observation of HEAD's registry, not a claim that W04 count 14 is
  correct-by-design; 14 is the instrument's answer over 10 URLs.
- Neither instrument looks at `## Search log` or `## Leads` content, and the guard looks at no
  section at all (R9).
- The guard's exit 0 does not by itself prove it ran: an unresolvable lane path also yields exit 0
  with empty stdout (R15, mode 1). Pair every guard receipt with a positive control (R16) or with the
  explicit rev/row-count check (R11).
