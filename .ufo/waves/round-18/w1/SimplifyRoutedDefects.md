# SimplifyRoutedDefects — YAGNI review of C1/C2 tool specs

Seat: `KaidokuR18.SimplifyRoutedDefects` (author-side advisory, leaf). Read-only: no
contract/tool edits; this report is the only file written. Baseline
`B = 9011581d84527ba34c675f9cf912e54d2e72d470` (`claims.json:4`). The lane is already
detached and jj-colocated: `git rev-parse refs/heads/main` = `HEAD` = `origin/main` =
`B`; `git symbolic-ref -q HEAD` exits 1; `.jj/` exists.

While this ran, siblings were writing `.ufo/waves/round-18/{controls.py,measure.py,verify.py,
tools/revpin.py,tools/routed-defects.py}` (untracked, mtimes 12:28-12:34). Worktree
anchors below are labelled `[O-worktree]` and may move; contract/B anchors are stable.

Axes: calibration (does the count mean what the claim says), operability (does a flag
have a caller), depth (does a new tool become a second authority).

## 1. Deletion candidates

**D1. `revpin.py` CLI and its two `--no-*` flags — drop; keep the module.**
`contract.md:51,57-59` specifies `revpin.py --root DIR [--branch main]
[--no-require-pushed] [--no-require-head]` plus CLI exit 0/2. No round command runs the
CLI; `W18/verify.py` loads the module and calls `resolve_source(LANE)` (`verify.py:38,90-97`),
and `jj-red-before` calls `resolve_source(sb)` (`contract.md:95-96`); the `revpin`
references in `measure.py:579,594` are selftest stub strings (`STUB_HEAD_OK`), not
production imports. The two flags are exercised only by
revpin's own selftest (`revpin.py:206` `--no-require-pushed`, `:235` `--no-require-head`);
the only code that passes those parameters is the CLI itself (`revpin.py:309-310`), and
module callers use the defaults. Dropping the CLI + both parameters removes the argparse/`main`
block (`revpin.py:286-310`) and two selftest-only cases. Nothing else breaks.

**D2. R17-PINMAP check (d), literal `map_sha256` — drop from C1.**
`contract.md:32`; implementation `[O-worktree] routed-defects.py:142-151` is
`elif "map_sha256" in src` — any occurrence satisfies it, including a comment
(`CriticC1.md:37,49` already shows the token flip). The routed defect permits *either*
retaining mid maps *or* the named correction; (a)-(c) close the correction branch.
Retention is C3's in-place change (`contract.md:128-131`) and its behavioral test is
receipt-validate's recomputed mid-map digest (`contract.md:129-131`). (d) therefore
duplicates C3's test and makes C1's closure depend on C3 landing. Keep (a)-(c); if the
L1 wants C1 to own retention, move the carrier-run change to C1 and remove it from C3
(one owner, not two). Baseline is red either way: committed `carrier-run.py` has 0
`map_sha256` (rc 1).

**D3. `jj-red-before` step (4) — drop.**
`contract.md:95-96` runs `git -C sb rev-parse HEAD` vs `revpin.resolve_source(sb)`. The
raise is already covered by revpin's own selftest (`contract.md:58-59`). Worse, the step
materialises a bare `rev-parse HEAD` inside `.ufo/waves/round-18/`, which head-rev-lint
scans (`contract.md:62-63`); its enclosing function is not `selftest`/`fixture`, so the
lint counts it live and the source revision can no longer print 0 (same point:
`CriticC2.md:99`). Keep steps (1)-(3), which are the only real-jj integration evidence.
If step (4) is kept, it needs an explicit allowlist entry with a reason — not a
fixture-shaped function name.

**D4. Custody `# repo-dirty:` — drop or justify.**
`contract.md:80-81`. No claim, measure, or lint reads it; C2's falsifiable pair is the
branch-tip/HEAD flag (`claims.json:20`). `repo-root`, `repo-branch`, `repo-branch-tip`,
`repo-HEAD-is-branch-tip` are load-bearing. Audit R3 did suggest a dirty flag
(`JjAuditKaidoku.md:246`), so keeping it is defensible as a diagnostic — but then state
whether it or the fixed verify.py's dirty check (`contract.md:83-85`; current
`verify.py:60` runs `status --porcelain` without `--untracked-files=no`) is
authoritative: both check tracked dirt with different commands. Saving is one line;
confidence medium.

**D5. Citation-drift `branch` output / `--branch` — optional.**
`contract.md:73-76`. The counting command never passes `--branch`; the lane has one
branch. `rev_resolved` is the load-bearing new field; `branch` is documentation. Keep
only if branch-rename operability is wanted (low value, low cost).

**Retained despite not being needed by the counting commands** — deleting these would
harm calibration:
- `--strict` on routed-defects/head-rev-lint: the claims' commands read JSON counts, but
  `W18/verify.py:174-186` already executes both with `--strict` and asserts baseline 1 /
  source 0. Remove the flag and those three harness runs together, or neither.
- `files_scanned`, `fixture_count`, `sites[].code`: the audit trail that makes the 3-vs-8
  question decidable (`CriticC2.md:149` asks for `files_scanned` and the scope prefixes;
  `fixture_count`/`code` are the same trail).
- `--selftest` red cases: required by the global tool contract (`contract.md:8-13`).

## 2. Duplicate authorities

**DUP1. `W18/controls.py` is a second copy of `W17/controls.py`.**
`[O-worktree]` 807 vs 518 lines. The deltas are real and documented
(`Controls18.md:16-40`, contract.md:142-145): SCORECARD append, byte-identical
knowledge except the one appendable r17 entry, SOURCES status/recheck/used-by,
SHA256SUMS restore, SKILL diff. But `Rev` (W17:87-122), `prefix_report`/`unchanged_report`
(:198-224), `quality_registry` (:268-290), `sources_registry` (:292-321) and the selftest
git fixture (:429-445) are duplicated. A blind copy is wrong in *both* directions:
- W17 `dir_prefix_report` (:226-240) allows any corpus/lessons|knowledge `.md` to be
  appended; W18 requires byte-identical except the one r17 entry. Copying is weaker.
- W17 `frozen_report` (:242-266, `FROZEN_PREFIXES` :56) freezes every `.ufo/waves/` blob,
  including `round-17/predictions/SHA256SUMS`; W18 requires the one-line restore.
  Copying is stricter than the intended change.
Since 23 selftest cases are already green (`Controls18.md`), do not rewrite this round.
Freeze it; next round import `Rev`/report helpers via `spec_from_file_location`
(precedent: W17 `verify.py:41-49` loads `pins.py`) and keep only the five deltas.
Note also `[O-worktree] W18/controls.py:57-65` carves all six in-place fixes out of
`frozen_report`: SHA256SUMS plus the five edited `.ufo/waves/round-17/` tool files.
The contract's no-harm bullet (`contract.md:142-145`) names only the SHA256SUMS restore;
the other five are BEFORE blobs under `FROZEN_PREFIXES` too and would be flagged by a
literal W17 copy. The carve-out is necessary — say so in the contract, and name the six
files, rather than leaving the wider set to the implementation.

**DUP2. `routed-defects.py` helper layer.**
`[O-worktree] routed-defects.py:45-105` re-implements `git show`/blob text/table cells/
section slicing; W17 `controls.Rev` (:87-122), `source_rows` (:157-172),
`admission_rows` (:174-196) are the existing authority (~60 duplicated lines). Keeping
this gate standalone is defensible (it reads six named paths, no tree scan). The real
risk is convention drift: `_cells` drops the leading/trailing empty cells, while
`source_rows` keeps them and indexes `USED_BY_COLUMN = 11` (`controls.py:65`). Both are
correct; write the convention in the docstring or reuse one helper next round.

**DUP3. `head-rev-lint.py` (not yet built) should not add a third blob reader.**
It needs `git ls-tree -r --name-only REV` + `git show REV:path`; `controls.Rev` has
both (:87-122) and `temporal-sweep.py:68-120` has `git_show`/`resolve`/`site_files`.
Import one (precedent above) or copy ~30 lines — but not both patterns. The AST/site
logic stays local.

**DUP4. `revpin` predicate is inlined four times — mostly justified.**
citation-drift (`contract.md:73-74`), custody-pair (:78-81), r17 verify (:83-85), and
revpin (:51-56). Inline is right for the two gates ("no import from W18", :74) and for
r17 verify (importing W18 would invert the wave dependency). Requirement: the same
three finding names in the same order in every copy (`branch_missing`,
`head_not_branch_tip`, `branch_not_pushed`); only revpin's copy is tested at module
level, and step (4) is the only sandbox test of it (D3).

**DUP5. `jj-red-before` steps (2)-(3) duplicate the probes' selftests — keep.**
Unit fixtures do not exercise a real jj-colocated clone; that is the claim's evidence
(`claims.json:20`). Only step (4) is redundant.

**DUP6. R17-REGISTRY parsing vs `invocation-audit.parse_registry` (:153-176) / W17
measure `REGISTRY_KIND` (:52).** Different fields (5th-cell write scope and 2nd-cell
kind vs command argv); local parse is fine. Keep `cells[1] = name`, `cells[2] = kind`.

## 3. Counting-command calibration (brief; peers hold the long form)

**[O]** At B the contract's own context rule gives **8 live**, not 3:
`citation-drift-probe.py:477` (default-HEAD), `custody-pair.py:326-327` (the HEAD
literal is :327), `controls.py:442` (`_commit`, called only from `selftest` at
:452/:454/:474), `verify.py:59`, `w2/audit-attack.py:91`, `:348-349`,
`w2/temporal-attack/fixtures/rebuild.sh:9,11`. Fixture by the stated rule: 6 call sites
(`measure.py:223`, `invocation-audit.py:424`, `temporal-sweep.py:260-261,288-289,
307-308,332`). This independently reproduces `CriticC2.md:48-75` and
`ConnSiblingOverlap.md:97-117`; my AST census over 37 tracked `*.py`/`*.sh` at B printed
`8 live / 6 fixture` (raw scan 17 hits before list-vs-call dedupe), exit 0.

**[O] Structural point beyond the three routed files.** The contract itself requires
`git rev-parse --verify HEAD^{commit}` in revpin (`contract.md:54`) and scans
`.ufo/waves/round-18/` (`:62-63`). `[O-worktree] resolve_source` (`revpin.py:93-120`)
is a live function, so the literal kind counts it; the planned guards in
verify/citation/custody (`contract.md:73-85`) do the same. `W18/verify.py:183-186`
already asserts
`head-rev-lint --strict` exit 0 at source. Therefore **live_count cannot reach 0 by
fixing the three routed files alone**; the count and the lint kind must be reconciled
before integration.

**Smallest single-count fix (YAGNI): restore the audit's allowlist.**
`JjAuditKaidoku.md:263` (recommendation 4) already asked for a lint "outside the
known-safe allowlist". The contract replaced that with a name-only fixture rule. Do:
1. `fixture` by path (`**/fixtures/**`, `**/w[0-9]+/**`) and by caller-fixpoint (seed
   functions whose name contains `selftest`/`fixture`; a function all of whose callers
   are fixture is fixture — this catches `_commit`, which a name-only rule cannot);
2. allowlist the guard/record HEAD reads the fixes introduce — revpin's head
   resolution, verify's refusal, citation's `--rev HEAD` guard, custody's
   `repo-HEAD` record, and (if kept) jj-red-before's baseline — each with path, exact
   code, and reason; emit `allowlisted: true` + reason per site;
3. `live_count` = sites neither fixture nor allowlisted; `--strict` gates on it.
Result: 3 at B -> 0 at source, one count, no second metric. Cost: two predicates + five
reviewed entries. The peer alternatives cost more surface: a permanent
`routed_live_count` that goes 3->0 while `live_count` goes 8->5
(`ConnSiblingOverlap.md:138`), or an `excluded:[...]`/`limits:[...]` schema for every
hit (`CriticC2.md:149`). Both are honest; the allowlist is smaller and is the routed
recommendation.

**Do not grow the detector.** It misses `@`, `HEAD~0`, `rev-list HEAD`, implicit-HEAD
commands, and string-built argv (`CriticC2.md:80-96`). State those as limits in the
docstring; jj-red-before steps (1)-(3) are the behavioral backstop. YAGNI says the
three routed spellings plus the named guards are the surface to hold.

**Anchor defect.** `claims.json:19` cites `.ufo/waves/hyaku/jj-w1/reports/
JjAuditKaidoku.md`; that path does not exist in the lane (`test -f` rc 1) and exists
only at `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md`
(rc 0). Cite the fleet-absolute path (or copy section 5 into W18), otherwise C2's
"sourced" cannot be opened from the lane.

## 4. Preserved contract (what the claims actually need)

- `routed-defects`: `--root`, `--rev`, `{rev, defects:[{id, open, checks:[{name, ok}]}],
  open_count}`, exit 0 / 2 (0 even when open; `--strict` 1 for the harness), six ids,
  selftest with 6-open, 6-closed and one broken check per defect. (d) dropped.
- `head-rev-lint`: `--root`, `--rev`, `sites[]` with `path,line,kind,context,code,
  allowlisted,reason`, `files_scanned`, `live_count` (fixture- and allowlist-excluded),
  exit 0 / 2, `--strict` for verify.py; fixture predicate per §3.
- `revpin`: module only, `resolve_source(lane, branch="main")` ->
  `{branch, source, head, head_equals_source, remote, pushed}`, three named findings,
  selftest three cases.
- `jj-red-before`: steps (1)-(3) with argv/exit/stdout/stderr and `all_held`, exit 0/1/2.
- In-place fixes as written; guards use `rev-parse --verify HEAD^{commit}` so the
  allowlist stays narrow; custody keeps `repo-root/branch/tip/head-is-tip`; compare
  already skips `#` lines (`custody-pair.py:491`), so the new metadata needs no code.

## 5. Evidence (commands and exits)

```
$ git -C LANE rev-parse --verify refs/heads/main^{commit}
9011581d84527ba34c675f9cf912e54d2e72d470            rc=0
$ git -C LANE rev-parse --verify refs/remotes/origin/main^{commit}
9011581d84527ba34c675f9cf912e54d2e72d470            rc=0
$ git -C LANE symbolic-ref -q HEAD                    (no output) rc=1   # detached
$ test -d .jj                                        rc=0               # colocated

$ python3 -I -B /tmp/astlint3.py                     rc=0
# read-only throwaway AST scan of `git ls-tree -r` + `git show` at B; no lane writes
files 37 sites 17
Counter({('rev-parse-HEAD','fixture'):9, ('rev-parse-HEAD','live'):5,
         ('shell','live(shell)'):2, ('default-HEAD','live'):1})
# per-call dedupe: 8 live, 6 fixture (temporal-sweep list+call counted twice above)
# live: citation:477, custody:326-327, controls:442, verify:59,
#       audit-attack:91, :348-349, rebuild.sh:9, :11

$ git -C LANE grep -n -E 'rev-parse[^|]*HEAD|default="HEAD"' refs/heads/main -- \
  .ufo/gates .ufo/rounds .ufo/waves/round-14 .ufo/waves/round-15 \
  .ufo/waves/round-16 .ufo/waves/round-17 .ufo/waves/round-18   rc=0
# 13 *.py/*.sh hits by file extension (the two md lines that happen to contain
# "measure.py:" are prose); this line-based form misses the multiline
# audit-attack.py:348-349 call, which the AST scan above adds.

Each row below was run as `git show refs/heads/main:<path> | grep -c -- '<token>'`;
the printed count and rc are shown:
carrier-run.py map_sha256                 -> 0 rc=1
SKILL.md 'Write scope:'                   -> 0 rc=1
SOURCES.md 'supersedes S032'              -> 0 rc=1
SHA256SUMS 'predictions/carriers.tsv'     -> 0 rc=1
QUALITY.md R17-PINMAP                     -> 0 rc=1
SCORECARD.md R17-PINMAP                   -> 0 rc=1
LOG.md R17-VALIDATE16                     -> 0 rc=1
SCORECARD.md R17-PRODUCER-REV             -> 0 rc=1
corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md R17-PINMAP -> 0 rc=1

$ git -C LANE cat-file -e refs/heads/main:.ufo/waves/round-18/evidence/validate16/summary.json
fatal: ... does not exist                             rc=128
$ test -f .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md        rc=1
$ test -f /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md  rc=0

$ grep -n '_commit(' .ufo/waves/round-17/controls.py  rc=0
452,454,474 (all inside selftest; def :429)
$ grep -n 'require_pushed=not\|require_head=not' .ufo/waves/round-18/tools/revpin.py rc=0
309-310; selftest CLI calls at :206, :235
$ grep -n -- '--strict' .ufo/waves/round-18/verify.py rc=0
179 (routed-defects source), 184 (head-rev-lint baseline), 186 (head-rev-lint source), 243
$ wc -l .ufo/waves/round-18/controls.py .ufo/waves/round-17/controls.py \
        .ufo/waves/round-18/measure.py .ufo/waves/round-18/tools/routed-defects.py \
        .ufo/waves/round-18/tools/revpin.py
807 / 518 / 914 / 621 / 321                          rc=0
$ grep -n 'map_sha256' .ufo/waves/round-18/tools/routed-defects.py rc=0
146,148,151 (the literal check); 414 is a selftest fixture string
```

Not run: any round tool `--selftest`, `routed-defects`/`head-rev-lint` at B/S, or
`measure.py` — siblings own those runs; this seat compared bytes only.

## 6. Tradeoffs / stop

- Nothing deleted: all D1-D5 are candidates for the L1's integration, with the anchors
  above. D1-D3 are high confidence; D4 is a one-line diagnostic whose removal trades
  the audit's R3 note for a smaller contract; D5 is cosmetic.
- The next deletion would harm an axis. Dropping `--strict` alone breaks
  `W18/verify.py:174-186`; dropping `files_scanned`/`fixture_count`/`code` removes the
  audit trail that decides whether 3 or 8 is true; dropping `repo-root`/`repo-branch`/
  `repo-tip` makes `repo-HEAD-is-branch-tip` uninterpretable. Stop here for this round.
- Rewriting `W18/controls.py` to import W17 is not cheap after 23 green selftest cases;
  record it as next-round debt, not a round-18 edit.
- Residual risk after the proposed changes: a verified HEAD read used as a *source*
  (not a guard) would pass the allowlist-based lint; jj-red-before remains the
  behavioral check, and the limits must say so.
- No tools installed or upgraded.
