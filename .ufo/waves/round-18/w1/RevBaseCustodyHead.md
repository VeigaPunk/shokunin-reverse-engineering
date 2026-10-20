# RevBaseCustodyHead — R3 falsification at baseline `9011581d`

- Seat: advisory reviewer, round 18 wave 1. Task: falsify jj risk **R3** from
  `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:167,246` at
  `B = 9011581d84527ba34c675f9cf912e54d2e72d470`, against `LANE/.ufo/waves/round-18/contract.md:78-82`.
- Verdict: **citation exact; mechanism real and reproduced; not realized in the lane's current state.**
  R3's audit severity "High" is overstated for machine behaviour (no consumer reads the field, no gate
  changes verdict) and defensible only for evidence semantics; I calibrate it **Medium, High-conditional**.
  The contract's fix is the right minimal change, with four wording/coverage defects listed in §5.
- Labels: **[OBS]** = observed output I produced here; **[INF]** = inference. Every command below is pasted
  with its exit code. `LANE`, `SB`, `GATE`, `CAND` are shell variables from the actual runs; `git -C LANE` denotes
  the same invocation I ran as `cd LANE && git …`. Exit codes are pasted verbatim; the one evidence table in
  §4 abbreviates its command cells for width, but every exit code and header value in it is verbatim.

## 1. Citation check: are the cited lines still those?

**[OBS]** Baseline blob, numbered (`sed` used read-only only):

```
$ git -C LANE show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/gates/custody-pair/custody-pair.py | nl -ba | sed -n '315,365p'
   324  def repo_head(cwd: Path) -> str:
   325      try:
   326          out = subprocess.run(
   327              ["git", "rev-parse", "HEAD"],
   328              cwd=str(cwd), capture_output=True, text=True, timeout=10,
   329          )
   330          if out.returncode == 0:
   331              return out.stdout.strip()
   332      except Exception:
   333          pass
   334      return "(none)"
   ...
   349          "# repo-HEAD: %s" % repo_head(Path.cwd()),
EXIT=0
```

**[OBS]** The working-tree file was byte-identical to the baseline at the citation check and through the
evidence runs; a sibling seat began the in-place round-18 fix after them (`git status` at the final check:
` M .ufo/gates/custody-pair/custody-pair.py`). All `:NNN` anchors in this report are **baseline-blob**
coordinates, and §5.2 records the in-flight snapshot separately.

```
$ git -C LANE diff --stat 9011581d84527ba34c675f9cf912e54d2e72d470 -- .ufo/gates/custody-pair/custody-pair.py
(no output)
EXIT=0
$ grep -n 'repo_head\|repo-HEAD\|rev-parse' .ufo/gates/custody-pair/custody-pair.py
324:def repo_head(cwd: Path) -> str:
327:            ["git", "rev-parse", "HEAD"],
328:            cwd=str(cwd), capture_output=True, text=True, timeout=10,
349:        "# repo-HEAD: %s" % repo_head(Path.cwd()),
EXIT=0
```

So: `:324` definition, `:327` exact argv `["git","rev-parse","HEAD"]`, `:328` `cwd=str(cwd)`, `:349` the
`repo_head(Path.cwd())` call — **all four cited coordinates reproduce exactly**. The audit's internal anchors
also reproduce (`JjAuditKaidoku.md:167` is the custody-pair table row; `:246` is the R3 paragraph):

```
$ nl -ba .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md | sed -n '167p;246p'
   167  | `.ufo/gates/custody-pair/custody-pair.py:327` (used at L349 as `repo_head(Path.cwd())`) | `["git","rev-parse","HEAD"]`, `cwd=str(cwd)` | D | **High for a custody artifact.** ...
   246  **R3 — `custody-pair.py:327` records `repo-HEAD` as `@-`.** ...
EXIT=0
```

The file is unchanged between the audit baseline `da64646adcb19c1ede7537b799b8c7d283fe43da` and `B`
(`git diff --stat da64646 B -- <file>` → no output, EXIT=0), so the finding is not stale by drift.

## 2. Is R3 real under the lane's current state?

**[OBS]** Lane state, two independent reads:

```
$ scripts/hyaku/jj-lane.sh state LANE
state branch=main local=9011581d84527ba34c675f9cf912e54d2e72d470 remote=9011581d84527ba34c675f9cf912e54d2e72d470 ahead=0 behind=0 head=detached tracked=0 untracked=1
EXIT=0
$ git -C LANE rev-parse HEAD main origin/main
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
EXIT=0
$ cat LANE/.git/HEAD
9011581d84527ba34c675f9cf912e54d2e72d470          # detached, at the branch tip
```

`.jj` exists (colocation is live), and `.jj` was created at `2026-10-20 11:51:47 -0300`
(`stat -c '%n %y' .jj`). At this instant **HEAD is detached but equals `refs/heads/main` and
`refs/remotes/origin/main`**, so a capture *right now* records the correct commit. The hazard is the
divergence window, not the steady state.

**[OBS]** The only real custody receipt in the lane is pre-colocation and recorded an on-branch commit:

```
$ head -14 .ufo/waves/round-17/custody/custody-r17.v2.txt
# captured-utc: 2026-10-20T14:47:36Z
# cwd: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# repo-HEAD: d0ab2992149a38794e5ef2474ba5d4ef5ee1e905
EXIT=0
$ git -C LANE cat-file -t d0ab2992149a38794e5ef2474ba5d4ef5ee1e905     -> commit   EXIT=0
$ git -C LANE merge-base --is-ancestor d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 main          -> EXIT=0
$ git -C LANE merge-base --is-ancestor d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 origin/main   -> EXIT=0
$ git -C LANE rev-list --count d0ab2992149a38794e5ef2474ba5d4ef5ee1e905..main  -> 4          EXIT=0
$ git -C LANE rev-list --count main..d0ab2992149a38794e5ef2474ba5d4ef5ee1e905  -> 0          EXIT=0
```

Timeline (observed commit times, `git log --format='%h %ci %s' -5 main`): `d0ab299` at `11:47:24`,
`.jj` created `11:51:47`, receipt `captured-utc 14:47:36Z = 11:47:36 -03:00`. The receipt therefore
predates colocation by ~4 minutes, and its `repo-HEAD` is an ancestor of `main` (4 commits behind today).
**[INF]** It was almost certainly the branch tip at capture time (the round-17 helper sequence), but the
receipt alone cannot prove that — which is exactly the information the contract's fix adds.

**[OBS]** No gate or tool consumes `repo-HEAD`; only historical claim scripts render it:

```
$ grep -rn 'repo-HEAD' --include='*.py' --include='*.sh' .ufo | grep -v 'custody-pair/custody-pair.py'
… only .ufo/waves/arc3-loop1-*/claims/** historical probe copies and manifest-gen.sh
EXIT=0
```

## 3. Mechanism: reproduced in a throwaway sandbox (outside LANE)

**[OBS]** A jj-colocated repo with an unbookmarked commit (the audit's F2 shape, replicated):

```
$ git init -q -b main .; git commit -qm base; jj --config user.name=x --config user.email=x@y git init --colocate .
$ printf 'beta\n' > b.txt; jj --config user.name=x --config user.email=x@y commit -m off
Working copy  (@) now at: rkmpzrzz 198b1eb7 (empty) (no description set)
Parent commit (@-)      : pmxznswy 3cb4a055 off
JJCOMMIT_EXIT=0
$ git rev-parse HEAD                      -> 3cb4a0554ba0a4fea8147502c6c0d720624f840c   EXIT=0
$ git rev-parse refs/heads/main           -> ef6c701ad417f740a87e003b35e748f53d6121de   EXIT=0
$ git merge-base --is-ancestor HEAD main  -> (no output)                                 EXIT=1
$ git symbolic-ref -q HEAD                -> (no output)                                 EXIT=1
```

**[OBS]** The baseline gate, run with cwd inside that sandbox, silently records the off-branch commit
(exit 0 because the measured path exists — the repo identity never affects the exit map):

```
$ cd SB && python3 -I GATE capture --out SB/rec-baseline.txt --label r3 --paths SB/a.txt
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=r3 exit=0
CAPTURE_IN_REPO_EXIT=0
# repo-HEAD: 3cb4a0554ba0a4fea8147502c6c0d720624f840c      # != branch tip ef6c701a
```

**[OBS]** The `Path.cwd()` half also fires: outside any repo the field becomes `(none)`, again exit 0:

```
$ cd /dev/shm && python3 -I GATE capture --out SB/rec-outside.txt --label r3-outside --paths SB/a.txt
CAPTURE_OUTSIDE_EXIT=0
# cwd: /dev/shm
# repo-HEAD: (none)
```

**[OBS]** Under the live lane cwd the field is currently correct (`9011581…` = HEAD = main = origin/main),
again exit 0. This capture used `--paths` pointing at the sandbox file; the five operator credential paths
were only resolved by the write-guard, never opened.

```
$ cd LANE && python3 -I GATE capture --out /dev/shm/revbase-custody-head/rec-lane.txt --label r3-lane --paths /dev/shm/revbase-custody-head/sb/a.txt
CUSTODY_PAIR_CAPTURE: OK paths=1/1 label=r3-lane exit=0
CAPTURE_LANE_EXIT=0
# cwd: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# repo-HEAD: 9011581d84527ba34c675f9cf912e54d2e72d470
```

**Finding.** R3 is a **real mechanism**: two distinct silent mis-records, both exit 0. It is **not a current
lane failure**: `HEAD == main == origin/main` at both state reads, and the one real receipt is pre-colocation
and on-branch. The audit's "High" is right only in the conditional sense "if a receipt is cited as a landed
pin while HEAD is off-branch"; as a gate defect it is **Medium** (no consumer; no verdict change).

## 4. Minimal change that fixes it without changing explicit behaviour

custody-pair has **no `--rev` option** (parser at `:1316-1318`), so "explicit-rev behaviour" maps to: explicit
`--paths`/`--out`/`--label` capture results, the verify exit map, and receipt comparability. I built and ran a
candidate in a **sandbox copy only** (`/dev/shm/revbase-custody-head/gate/custody-pair.py`), never in LANE:

1. `DEFAULT_REPO = TOOL_PATH.parents[3]`, `DEFAULT_BRANCH = "main"` after `:188`.
2. `repo_meta(repo)` helper (below `:324`) reading one `git -C repo` process per field; `repo_head(repo)` kept
   as the legacy `# repo-HEAD:` value.
3. `render_receipt(sections, label, now, repo)` (`:337`) emits, after `# cwd:`: `# repo-root:`, `# repo-branch:`,
   `# repo-branch-tip:`, `# repo-HEAD:` (legacy value), `# repo-HEAD-is-branch-tip: yes|no`, `# repo-dirty:`.
4. `cmd_capture` (`:679`): `repo = Path(getattr(args, "repo", None) or DEFAULT_REPO).expanduser()` and pass it to
   `render_receipt` (`:683`).
5. Parser: `p_cap.add_argument("--repo", default=None, …)` after `:1317`.
6. `compare`: **no code change** — `parse_receipt` (`:438-459`) splits on `^PATH:` and never parses the header,
   so every `#`-prefixed field is metadata by construction.

Candidate evidence (all **[OBS]**):

| Probe | Command | Result |
|---|---|---|
| selftest, patched | `python3 -I CAND selftest` | `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` |
| selftest, unpatched control | same, baseline copy | `CLEAN cases=28 passed=28 failed=0 exit=0` |
| off-branch HEAD, **cwd outside repo**, default repo | `cd /dev/shm && python3 -I SB/.ufo/gates/custody-pair/custody-pair.py capture --out SB/rec-final.txt --paths SB/a.txt` | exit 0; `repo-branch-tip: ef6c701a…`, `repo-HEAD: 3cb4a055…`, `repo-HEAD-is-branch-tip: no` |
| explicit `--repo` from `cwd=/` | `cd / && python3 -I CAND capture --repo SB --out …` | exit 0; same tip/HEAD/`no` |
| shallow `--repo` canonicalized | `--repo LANE/.ufo/gates` | exit 0; `repo-root: /…/kaidoku-shokunin` (show-toplevel), `repo-branch-tip: 9011581…`, `repo-HEAD-is-branch-tip: yes`, `repo-dirty: yes` |
| live lane value | `--repo LANE` with sandbox `--paths` | exit 0; tip `9011581…`, HEAD `9011581…`, `yes`, `dirty: yes` (two sibling-edited tracked files at that instant) |
| old consumer reads new receipt | `python3 -I BASELINE verify rec-old2.txt rec-new2.txt` (unchanged `f.txt`) | `VERDICT: MATCH paths=1 MATCH=1 exit=0` |
| candidate consumer, same pair | `python3 -I CAND verify …` | `CUSTODY_PAIR_VERIFY: MATCH paths=1/1 drift=0 exit=0` |
| absent-path exit parity | `--paths missing.txt`, old vs new | `OLD_ABSENT_EXIT=13`, `NEW_ABSENT_EXIT=13` |
| dirty flag (tracked only) | tracked `M a.txt` then capture | `repo-dirty: yes`; `git status --porcelain --untracked-files=no` → ` M a.txt` |
| contract's red selftest case, **plain git, no jj** | fixture: `git init -b main`, commit, `git checkout --detach`, commit | `FIX_ANCESTOR_EXIT=1`; capture exit 0; `repo-HEAD-is-branch-tip: no` |

**Lint-clean HEAD read.** The first candidate read HEAD with `git -C repo rev-parse HEAD`, which reproduces the
very site the contract's `head-rev-lint` counts. I switched the candidate to
`git -C repo log -n 1 --format=%H` (identical value: `3cb4a055…`, EXIT=0; non-repo → exit 128 → `(none)`), the
same resolution the in-flight `verify.py` fix uses (see §5.1). After the switch the candidate contains no
`rev-parse HEAD` argv; the only textual match is the explanatory comment, which a line-regex lint could
false-positive on — keep the comment free of the literal pair or have the lint strip comments.

**Receipt version.** No bump is needed: the additions are `#` header fields, `parse_receipt` yields `v2` from the
`PATH:` stanza + `mtime_epoch` basis (`:458`), and existing receipts still compare (`MATCH` above). Bumping
`RECEIPT_VERSION` to 3 would falsely signal a stanza change; if instrument discrimination is wanted, add an
explicit `# instrument-version:` line instead.

## 5. Contract comparison (`contract.md:78-82`) and defects found

The contract bullet matches the audit's fix and is implementable as above, but four points need correction:

1. **"lane root two levels above the script" is wrong by two levels.** `TOOL_PATH` is
   `LANE/.ufo/gates/custody-pair/custody-pair.py`; `parents = [custody-pair, gates, .ufo, LANE]`:

   ```
   $ python3 -c "from pathlib import Path; p=Path('LANE/.ufo/gates/custody-pair/custody-pair.py').resolve(); print([str(p.parents[i]) for i in range(4)])"
   ['/…/kaidoku-shokunin/.ufo/gates/custody-pair', '/…/kaidoku-shokunin/.ufo/gates', '/…/kaidoku-shokunin/.ufo', '/…/kaidoku-shokunin']
   EXIT=0
   ```

   Literal `parent.parent` is `.ufo/gates`, i.e. the *two-level* reading is **not** the lane root; the lane root is
   `parents[3]`. This is survivable only because `git -C .ufo/gates rev-parse --show-toplevel` still returns LANE
   (EXIT=0): HEAD/tip stay correct via walk-up, but a `repo-root` printed as `str(repo)` would record
   `.ufo/gates`. **Recommendation: `DEFAULT_REPO = TOOL_PATH.parents[3]`, and always record `repo-root` from
   `git rev-parse --show-toplevel`** (the candidate canonicalizes a shallow `--repo` to LANE, table row 5).

2. **`--branch` is missing.** The contract names `# repo-branch:` but only adds `--repo`, so the branch must be
   a constant (`"main"`). On any other branch, `repo-branch-tip` is resolved against `main` and
   `repo-HEAD-is-branch-tip` reads `no` on a legitimate tip. **Recommendation:** a named `DEFAULT_BRANCH =
   "main"` plus an optional `--branch` defaulting to it (no effect on explicit paths/exits), or a one-line
   statement in the tool docstring that it is main-only.

3. **All nine direct `cmd_capture(argparse.Namespace(...))` selftest sites omit `repo`** — `:810, :996, :1011,
   :1036, :1081, :1118, :1151, :1201, :1218`. Reading `args.repo` unconditionally raises `AttributeError`
   before any assertion, so all 28 cases would fail. `getattr(args, "repo", None)` (candidate) keeps 28/28; the
   alternative is editing all nine sites. This is unstated in the contract and is the most likely silent
   breakage of the in-place fix.

4. **`repo-dirty: yes|no` (tracked modifications only) is blind to untracked wave output.** At my first
   state read: `state … tracked=0 untracked=1`, `git status --porcelain` → `?? .ufo/waves/round-18/`; a capture
   then would have said `repo-dirty: no` while the whole round-18 tree was uncommitted — precisely the F7
   hazard (an untracked `verify.py` can change a gate result). The contract mandates tracked-only, so the
   implementer should follow it, but the receipt should not be read as "worktree clean". **Recommendation:**
   either add `# repo-untracked: <count>` (cheap, additive) or state the limit in `SKILL.md:449`.

**Atomicity [INF].** The candidate issues four separate `git -C` processes (root, tip, head, dirty). A helper
commit landing mid-capture can make `repo-HEAD` and `repo-branch-tip` describe different instants, and
`head-is-branch-tip: yes` would then be a coincidence of two reads. Reading HEAD and the tip in one `git
rev-parse HEAD refs/heads/main^{commit}` process removes the skew but reintroduces the lint site; the honest
options are (a) accept and document non-atomicity, or (b) accept one live lint site for the pair read. Do not
silently claim atomicity.

### 5.1 Claims/lint contradiction (escalate to L1)

[INF] **C2's stated target "live HEAD-as-revision call sites 3 -> 0" (`claims.json:20`) cannot be met while each
fix keeps a literal `rev-parse HEAD`, under the contract's lint definition (`contract.md:63-66`).** The three
fixed tools still *must read HEAD*:

- custody keeps `# repo-HEAD:` (`contract.md:79`), i.e. a HEAD read;
- `verify.py` must "exit 2 unless HEAD equals the branch tip" (`contract.md:83-85`), i.e. a HEAD read;
- `citation-drift` must accept literal `--rev HEAD` "only when HEAD equals the branch tip"
  (`contract.md:75-76`), i.e. a HEAD read.

The lint's site kinds are syntactic (`rev-parse` + literal `HEAD`, `default="HEAD"`, `HEAD:`, upstream forms)
and define only `fixture|live` contexts, with no guarded/allowlist context. Therefore a correct fix leaves
**three live sites**, and reaching 0 requires relocating the read out of the lint's pattern. That is exactly
what the in-flight fix does: the working-tree `verify.py` (observed during this review, after the baseline-blob
read; concurrently edited by a sibling seat) reads HEAD as `git log -n 1 --format=%H` and its docstring says so
explicitly —
"`HEAD` is read via `git log -n 1 --format=%H` (defaults to HEAD) so no `rev-parse HEAD` revision site is
reintroduced" (working tree `:73-74`, call at `:78`; the baseline blob is
`git("rev-parse","HEAD")` at `:59`). My candidate adopts the same form for custody. The owner's in-flight
implementation chose the opposite: working-tree `:381` keeps `_git_at(repo, "rev-parse", "HEAD")` and its
module docstring says the site is retained ("still `git rev-parse HEAD` in the repo — under jj that is `@-`,
now flagged, not hidden"). That is a defensible semantic choice, but the lint as specified will count that
live site, so C2's `3 -> 0` cannot be satisfied by the delivered tree unless the lint or the claim changes.

Consequences to resolve before integration:
- The 0 is a **syntactic rev-parse-HEAD count**, not "HEAD is never read". Either add a `guarded` context to
  the lint (HEAD literal whose result is only compared to the branch tip) and count only unguarded sites, or
  restate C2 as "3 unguarded -> 0 unguarded; 3 comparison-only HEAD reads remain, named".
- The lint must detect helper-call shapes, because the baseline `verify.py:59` is itself a helper call
  (`git("rev-parse","HEAD")`, helper at `:50-51`). If it detects that shape, it also detects a custody helper
  call `_git(repo,"rev-parse","HEAD")`; my first candidate had exactly that shape, so it would have stayed at
  live_count 1. If instead the lint only matches literal argv list literals, a one-line helper refactor hides
  any HEAD site — the metric then measures nothing. State which shape is scanned.

### 5.2 In-flight owner implementation (snapshot; file is being edited concurrently)

**[OBS]** At the final check the working tree shows ` M .ufo/gates/custody-pair/custody-pair.py` (the contract's
in-place fix by another seat, not my edit; `git diff --stat` grew from 76 to 129 insertions across my reads, so
this is a moving target and anchors are current only as of the last read). Relevant working-tree anchors:

- `:209` `RECEIPT_VERSION = 2` retained with an explicit comment — matches the §4 verdict (no bump).
- `:214-215` `LANE_ROOT = TOOL_PATH.parents[3]`, `REPO_BRANCH = "main"` — the contract's "two levels" wording
  defect is resolved correctly in code for the default.
- `:350` `_git_at`, `:364` `repo_context`, `:381` `head = _git_at(repo, "rev-parse", "HEAD")` — the live lint
  site is retained **deliberately** (docstring `:365-370`: "still `git rev-parse HEAD` … now flagged, not
  hidden"). This is the semantic choice described in §5.1 and it keeps C2's syntactic `3 -> 0` out of reach.
- `:372` `"root": str(repo)` — not canonicalized (no `git rev-parse --show-toplevel`); correct for the default
  `parents[3]`, but `--repo <subdir>` would record the subdir as `repo-root`.
- `:377` `"dirty": "(none)"` — a non-repo or failed `status` renders `# repo-dirty: (none)`, outside the
  contract's `yes|no` enum (`contract.md:80`). Reconcile: allow `unknown` in the contract or map it explicitly.
- `:744-747` `Path(getattr(args, "repo", None) or LANE_ROOT)…` and the fourth argument to `render_receipt` —
  the nine direct `Namespace` selftest sites are safe (my §5 point 3 is already honoured here).
- `:1383-1386` `--repo` default `str(LANE_ROOT)`.
- Selftest: `case_repo_tip` at `:1340`, registered as `repo-header-off-branch-tip-no` at `:1373`, is a plain-git
  `git checkout --detach HEAD~` fixture (no jj) that asserts `repo-HEAD-is-branch-tip: no`, the off-branch
  `repo-HEAD`, `repo-branch-tip`, `repo-root`, `repo-dirty: no`, then the on-tip `yes`. `case_repo_cwd` at
  `:1377` runs the tool with `cwd="/"` and asserts the default still pins `LANE_ROOT` and an explicit
  `--repo` wins — exactly the two R3 halves. This implements the contract's red-case requirement in the shape
  I recommended (plain git, `mkdtemp`, no jj); the owner's own run is its evidence.
- I did **not** execute the in-flight file's selftest (it is another seat's artifact, mid-write). The owner's
  own recorded run is the evidence for it.

## 6. Sibling observation outside R3's direct scope

**[OBS]** `.jj/repo` contains `config-id`, `index`, `op_heads`, `op_store`, `store`, `submodule_store`,
`workspace_store` — **no `config.toml`**. The helper writes repo config on init
(`scripts/hyaku/jj-lane.sh:152`: `config set --repo snapshot.auto-track '"none()"`, plus user and
`trunk()` alias at `:153-155`). **[INF]** The lane's `snapshot.auto-track="none()"` assumption (audit F7, and the
premise of R2's untracked-invisibility clause and of `repo-dirty`'s tracked-only definition) is therefore not
verifiable from repo files; if the lane was colocated without those `config set` calls, a jj command can
snapshot the entire untracked `round-18/` tree into `@`. The L1 should resolve this before round-18 commits
(read-only check by the helper's owner; no seat should run `jj` in LANE to test it).

## 7. Residual risk and verification gaps

- I replicated the jj sequence; I did **not** run `jj-lane.sh commit` end-to-end. The helper's window is
  `jj commit` → `bookmark set` (`jj-lane.sh:229-234`); a failure between them leaves HEAD off-branch
  persistently, which is exactly the reproduced failure shape.
- No live custody capture was taken against the five operator paths; all captures used `--paths` overrides
  (a sandbox file). The guard resolves the five paths without opening them. The lane-cwd captures wrote only
  under `/dev/shm`.
- The lane is being edited concurrently by sibling seats: at my first state read `tracked=0`; later `git status --porcelain`
  showed `M .ufo/gates/citation-drift/citation-drift-probe.py`, `M .ufo/waves/round-17/tools/{carrier-run,
  compare,log-extract}.py`, `M .ufo/waves/round-17/verify.py`. Statements about those files are baseline-blob
  facts; the `verify.py` `log -n 1 --format=%H` observation is timestamped and may change. `custody-pair.py`
  itself was unmodified through the evidence runs (`git diff --stat B -- <file>` empty, EXIT=0); the final
  status check shows the owner's in-place edit underway (§5.2).
- jj version tested: 0.45.1 only. Sandbox kept for reproduction at `/dev/shm/revbase-custody-head/`
  (`sb/` = jj-colocated repo, `fixture-detached/` = plain-git red fixture, `gate/` = patched copy); disposable.
- No tool was installed or upgraded.

## 8. Compliance

- Wrote only this report in LANE. No `jj` and no git write in LANE or the fleet repo; all git was read-only
  (`show`, `cat-file`, `rev-parse`, `merge-base`, `rev-list`, `log`, `status`, `diff --stat`, `for-each-ref`).
  All mutations (git init, commits, jj colocate/commit, candidate edits) ran under `/dev/shm`.
- Did not run REA analyze/search/decompile, Ghidra, or any carrier binary. Did not open credential files: the
  gate's default custody paths were never captured, only resolved by its write-guard.
