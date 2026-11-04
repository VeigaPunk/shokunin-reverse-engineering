# SentinelScope — round-68 scope / secret / provenance audit (receipts)

Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (separate git repo from the fleet root).
Range audited: `fcbe200f6739c38939e0dabf3f251de2cc6bd727..1eaf596e5f241762349fbd102c9e09ec1df18e3f`
(2 commits) plus the post-freeze commit `6ffa9ce1119ec01c953494d8f5b28e419efad646` and the uncommitted
`w1/` tree, snapshot at `2026-11-03T22:45-03:00`. Read-only; no scratch dir created or used; no tool
installed; no subagent; no git/jj mutation.

One line per check: verdict, name, and the command behind it.

1. **Scope containment — PASS.** `git -C <lane> diff --name-status fcbe200f..1eaf596e` → 15 paths, every
   one lane-relative: `plans/round-68-claims.md`, `tools/round-68/{registry-conformance,packed-elf,controls}.py`,
   `.ufo/waves/round-68/claims.json`, `.ufo/waves/round-68/l1/census-start.txt`,
   `.ufo/waves/round-68/l1/pre/{c1-at-base.json,c1-at-base.stdout,c2-dryrun-at-base.json,c2-dryrun.err,c2-skiprun.json,controls-at-base.json,controls-at-base.stdout}`,
   `LOG.md`, `SCORECARD.md`. Post-freeze `6ffa9ce1` adds only
   `.ufo/waves/round-68/{gen-w1.py,r68-w1-dispatch.json,r68-w1-spec.json,r68-w1.ready}` (4 paths, all
   under round-68). No path outside the lane, no path in another round's `tools/`, no `corpus/`, no
   jj/git index file.
1a. **Ledgers are in scope by rule — PASS.** `AGENTS.md:4` — "Every change appends a LOG.md entry with the
   evidence that motivated it"; SCORECARD.md is modified by the round record in r65/r66/r67
   (`git log --format=%h --diff-filter=M -- LOG.md SCORECARD.md` → `7a3c21d4`, `5de8a1de`, `2dc9789f`, …).
   Append-only preserved: `git diff --numstat fcbe200f..1eaf596e -- LOG.md SCORECARD.md` → `9 0 LOG.md`,
   `24 0 SCORECARD.md` (0 deletions; no filed byte rewritten).
1b. **No symlink / gitlink / submodule added — PASS.** `git diff --raw fcbe200f..1eaf596e` → modes
   `100644` ×12, `100755` ×3 (the three instruments only). No `120000`/`160000` entry in the range.
1c. **Worktree index untouched by seats — PASS.** `git -C <lane> diff --cached --name-only` → empty;
   `git -C <lane> status --porcelain` → `?? .ufo/waves/round-68/w1/` plus two dispatch artifacts, i.e.
   the wave tree is untracked, nothing staged.

2. **No credential material in the round's committed bytes — PASS.** `git diff fcbe200f..HEAD` piped through
   13 shapes (PRIVATE KEY block, `sk-`, `gh[pousr]_`, `github_pat_`, `AKIA`, `xox[abprs]-`, `AIza`,
   `password=`, `passwd=`, `cookie=`, `Authorization:`, `Bearer <20+>`, `api_key=`, `secret=`, `token=`)
   → 0 lines (`grep -c` → `0`, exit 1). Embedded-URL userinfo `://[^/[:space:]]+@` → 0. Env-dump shapes
   (`^(OPENAI|ANTHROPIC|AWS|GITHUB|GH|HF|NPM|SSH)_[A-Z_]+=`) → 0. Binary-carrier check:
   `git show HEAD:<path> | file -` over all 19 added paths → JSON text / ASCII+UTF-8 text / Python script
   only, no compiled or opaque blob.
2a. **Outside-lane paths are pre-public — PASS (note).** The range names
   `/home/vgpnk/.agents/skills/godspeed/directive.md`, `/home/vgpnk/.omp/agent/RULES.md`,
   `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, and (in the c2 receipts)
   `/run/user/1000/fnm_multishells/1981588_1793727763382/bin/node`. Each already appears in committed
   bytes at the base: `git log --all -S'/home/vgpnk/.agents/skills/godspeed'` → hits in rounds 65–67;
   `git log --all -S'/home/vgpnk/.omp/agent/RULES.md'` → same; `git grep -c 'fnm_multishells'
   fcbe200f` → 5 files; the npx path appears in `.ufo/waves/arc2-loop1-round1/*`. No new class of private
   path is introduced. Note (observation): `/run/user/1000/...` reveals the host uid, not a credential.

3. **Pins match the blobs at the freeze — PASS.** `git show 1eaf596e:<p> | sha256sum` →
   `tools/round-68/registry-conformance.py` = `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315`,
   `packed-elf.py` = `48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e`,
   `controls.py` = `0657ee080ba92459cfc2916715dce8c0f1c49930e03c8c3d36ac60dbd5618fb4`; identical to
   `claims.json.instruments`, to the working tree (`sha256sum tools/round-68/*.py`), and to `HEAD`.
   No post-freeze edit: `git log --format=%h main -- tools/round-68` → `6020eb60` only; that commit is an
   ancestor of the freeze (`git merge-base --is-ancestor 6020eb60 1eaf596e` → 0).
3a. **Freeze identity and immutability — PASS.** `git log --diff-filter=A --format=%H --
   .ufo/waves/round-68/claims.json` → `1eaf596e5f24…`; the claims blob at the freeze equals the working
   tree (`ea65bf6959c62fd45972adfc35294a4b91709af86cce0b02c14283e90d9030af` both sides). `git log --
   .ufo/waves/round-68/claims.json` → one commit, so no amendment series.
3b. **Frozen instruments behave at their declared case counts — PASS (my run).**
   `python3 -I -B tools/round-68/registry-conformance.py --selftest` → `cases 11, failed [], ok true`;
   `python3 -I -B tools/round-68/packed-elf.py --selftest` → `cases 13, failed [], ok true`.

4. **No compiled cache or scratch artifact committed — PASS.** `git diff --name-only fcbe200f..HEAD |
   grep -E '__pycache__|\.pyc$|\.pyo$'` → none; `find .ufo/waves/round-68 tools/round-68 -name
   __pycache__ -o -name '*.pyc' -o -name '*.pyo'` → none; the untracked `w1/` snapshot (12 files, 72K)
   holds only `.md/.json/.diff/.py` text, no `__pycache__`, no symlink.

5. **Pre-receipt provenance — FINDING (three named defects; see report §Findings P1–P3).** The path and
   revision *existence* sub-checks pass, the instrument-binding sub-checks do not:
   - `grep -o '"rev": *[^,}]*' .ufo/waves/round-68/l1/pre/*.json` → `"rev": "main"` ×3, `"instrument.rev":
     null` ×3. Named revisions exist: `git cat-file -t fcbe200f…` → `commit`, `git rev-parse main` →
     `6ffa9ce1…`. **FINDING P2**: every measured revision is the movable ref `main`, not the frozen base
     sha, and A9's `instrument.rev` is null in 3/3 receipts.
   - Instrument digests in the receipts: `c1-at-base.json` `a300d831…` = frozen ✓; `c2-dryrun-at-base.json`
     `7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c` ≠ frozen `48ef4c68…`;
     `c2-skiprun.json` `ff11d8ec27cbce94b4790041ed4e0dc4dfffa241cb243ece24e08491c415a302` ≠ frozen.
     `git rev-list --all -- tools/round-68/packed-elf.py` (4 refs, incl. `hyaku/*` branches) → every blob
     is `48ef4c68…`; `find /fast/scratch/hyaku/kaidoku-r68 <lane>/.ufo -name '*.py' | xargs sha256sum`
     → no file with either hash; `find / -maxdepth 6 -name 'packed-elf*.py'` → the committed file only.
     **FINDING P1**: the c2 before-arm and the six control arms were produced by instrument builds that
     never entered git and no longer exist on disk; `controls-at-base.json` records no instrument digest
     at all (keys `arms/base/control_arms/green/ok/schema`) though `controls.py:38` shells out to
     `tools/round-68/packed-elf.py`.
   - npx lock: `grep -o '"lock_sha256": *[^,}]*' .ufo/waves/round-68/l1/pre/*.json` → `null` ×2 with
     `"lock_recorded_not_pinned": true` ×2. **FINDING P3**: the flag asserts a recording the receipt does
     not carry (A6 requires `lock_sha256` recorded); round-67's `claims.json:59` shows the host resolves
     lock `815c18f1`, so a value exists to record.
   - **PASS (note)**: the only absolute scratch paths under `l1/pre/` are
     `/fast/scratch/hyaku/kaidoku-r68/PackedDry/packed-98xah8q6/{jq,xxd}/…` inside `c2-dryrun-at-base.json`.
     The class is already public (base-committed r67 receipts carry `/fast/scratch/hyaku/kaidoku-r67/…`,
     e.g. `.ufo/waves/round-67/l1/scores/c1-at-landing.json:123`), the leaf is an ephemeral work-dir
     suffix, and the tree is now empty (`ls -A /fast/scratch/hyaku/kaidoku-r68/PackedDry` → empty). No
     foreign-lane path in `l1/pre/`: `grep -rohE '/home/vgpnk/Projects/shokunin/[A-Za-z0-9_.-]+'` → no
     match; `grep -rohE '/home/[A-Za-z0-9_./-]+'` → `/home/vgpnk/.npm` ×8 only.
   - **PASS (observation, receipt truthfulness)**: `c1-at-base.json` is true at the base tree — both
     `unregistered` paths exist at `fcbe200f` (`git cat-file -e`), all 12 `named_but_absent` paths are
     absent there, and `scope_size 69 / registry_rows 73 / legacy_unregistered 26 / named_but_absent 12`
     match frozen atom A1 exactly.

6. **Fleet root untouched by this lane's seats — PASS (with an attribution note).**
   `git -C /home/vgpnk/Projects/shokunin status --porcelain` →
   ` M .scratch/goal-20261103-hyaku-run15.md`, ` M .scratch/run15-state.json`, `?? .scratch/run13-state.json`,
   `?? .scratch/run15-kernel.py`, `?? after`. None is a fleet tracked document: fleet
   `LOG.md`, `SCORECARD.md`, `MANIFEST.json` are clean. Structural bound: the fleet repo does not track the
   lane (`git -C <fleet> ls-files --error-unmatch kaidoku-shokunin` → pathspec error), so a lane commit
   cannot write fleet bytes. Mtimes: `after` 20:05:14 (24 B, `== SCORECARD diff base-`), `goal-…-run15.md`
   16:26:59, `run13-state.json` 2026-10-30, `run15-kernel.py` 19:24:49 — all before the round's first
   commit (author 22:28:11). `.scratch/run15-state.json` 22:41:24 falls between the freeze (22:41:05) and
   the wave commit (22:42:34) and its content is hyaku run-15 orchestrator state (`"run": 15`, lanes
   `revenger/tsukuroi/kama/tameshi/mado/kaidoku`, `"target": 100`). **Inference** (not provable from lane
   bytes): written by the fleet orchestrator that spawned this wave, not by a kaidoku seat; no kaidoku
   byte records a fleet-root write. Reported, not cleaned.

Snapshot note (observation): the untracked `w1/` tree at 22:45 held 12 files / 72K —
`swarm-registry.json` (L1), `ExecRegistry/{census_own.py,regime_audit.py}`, `ExecControls/controls-rerun.json`,
`MutRegistry/{mutants.json,M1..M6,S1}.diff` — all inside `w1/`; two seat scripts carry mode `+x`; no secret
shape, no symlink, no `.pyc`. Live seats were still writing at snapshot time, so this is a point-in-time
view, not the settled wave tree.
