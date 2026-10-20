# CriticC2 — attack on C2 ("3 live HEAD sites → 0" + jj-red-before)

Seat: KaidokuR18.CriticC2 (author-side advisory critic; not an outside reviewer, not a judge). Date 2026-10-20.
Scope: `claims.json` C2 and `contract.md:49-98`. The C2 tools (`W18/tools/head-rev-lint.py`, `revpin.py`,
`jj-red-before.py`) did **not exist** when this review ran (glob of `.ufo/waves/round-18/**` showed no `tools/`).
So this review attacks the **contract rules** and the **claimed numbers**. It does not attack delivered bytes.
Where this report says "prototype", it means my own literal reading of `contract.md:62-70`, run in-memory over Git objects.
The prototype is not the seat's tool.
LANE was read-only for this review. The only writes were this report and a throwaway mkdtemp sandbox under `/tmp`, which I removed afterwards.

Axes: calibration (do the numbers mean what they say?), operability (does the lane really get safer under jj?),
and depth (does the evidence reach the shipped bytes?).

## Verdict (summary)

| # | Counterexample | Kind | Axes |
|---|---|---|---|
| A1 | The stated lint rules give **8** live sites at B (or **6** if git argv only means list literals), not **3**. Getting exactly 3 needs exclusions that the contract never states. | fixable defect (calibration) | calibration |
| A2 | A list-literal-only lint misses `verify.py:59`, the audit's highest-risk site, because it is a wrapper call `git("rev-parse","HEAD")`. | fixable defect | calibration, depth |
| A3 | The four site kinds are a denylist of spellings. 18 of 20 HEAD-pinning forms I tested escape it, including `HEAD^{commit}`, which the fixes themselves must use. So the "0" partly measures spelling. | tradeoff → must be **declared in output** | calibration |
| A4 | At the delivered revision, `jj-red-before.py` has to contain `git -C sb rev-parse HEAD` in a live-named function. The rules then count it, unless the author dodges by naming or argv-building. | fixable defect (duplicate authority via naming) | calibration |
| A5 | The sandbox in the contract never reaches the lane's real steady state, which is HEAD detached **at** the tip. It only tests off-branch. A fix that refuses every detached HEAD would still pass. | fixable defect | operability |
| A6 | The baseline citation-drift "red" cannot be observed. With default paths it fails for the wrong reason (exit 2, `pointer_table_unreadable`). With the real table, HEAD-off and main give byte-identical findings. Only the literal string `HEAD` differs. | fixable defect | calibration, depth |
| A7 | The shipped `verify.py` bytes are never run in jj state. The sandbox exercises `revpin.py`, and Verify17BranchTip exercises a `/tmp` extract. Those are two different code bodies from the one counted as fixed. | fixable defect (false provenance) | depth, operability |
| A8 | Editing `round-17/verify.py` changes a **pinned producer identity**: r17 `verification.json` pins it at `2896f53a…`. The forward operability gain is close to zero, because r17 verification is a one-shot that already ran. | tradeoff for the judge | operability (harm side) |

## Evidence

### E1 — repo state (observation)

```
$ cd LANE && git rev-parse HEAD refs/heads/main            # exit 0
9011581d84527ba34c675f9cf912e54d2e72d470
9011581d84527ba34c675f9cf912e54d2e72d470
$ cat .git/HEAD                                            # exit 0
9011581d84527ba34c675f9cf912e54d2e72d470                  # raw sha => HEAD is DETACHED at the tip
$ git for-each-ref                                         # exit 0 (excerpt)
9011581… refs/heads/main   9011581… refs/remotes/origin/main   + 16 refs/jj/keep/*
```
So the live lane is in the state JjTrialKaidoku.md:40 reports after a helper commit (`head=detached`, ahead=0).
HEAD equals the tip, and nothing points HEAD at the branch.

### E2 — what the stated rules count at B (A1, A2)

In-scope tracked files at B: 37 `*.py`/`*.sh` (`git ls-tree -r --name-only 9011581 -- .ufo/gates .ufo/rounds .ufo/waves/round-1{4..8}`, exit 0).
Raw HEAD sweep: `git grep -n -E 'HEAD|@\{u\}|abbrev-ref|show-current|symbolic-ref' 9011581 -- <scope>` (exit 0).

My prototype applies `contract.md:62-70` literally: AST; enclosing function name contains `selftest`/`fixture` ⇒ fixture; shell files are always live. Its output at B:

| site (B) | kind | enclosing fn | context by rule | real nature |
|---|---|---|---|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py:477` | default-HEAD | `main` | live | **true live** (audit R2) |
| `.ufo/gates/custody-pair/custody-pair.py:326-327` | rev-parse-HEAD (list literal) | `repo_head` | live | **true live** (audit R3) |
| `.ufo/waves/round-17/verify.py:59` | rev-parse-HEAD (**wrapper** `git(...)`) | `main` | live | **true live** (audit R1) |
| `.ufo/waves/round-17/controls.py:442` | rev-parse-HEAD (wrapper) | `_commit` | **live** | fixture helper (mkdtemp repo, `:449`) → false positive |
| `.ufo/waves/round-17/w2/audit-attack.py:91` | rev-parse-HEAD | `build_repo` | **live** | fixture repo → false positive |
| `.ufo/waves/round-17/w2/audit-attack.py:348` | rev-parse-HEAD | `main` | **live** | fixture repo → false positive |
| `.ufo/waves/round-17/w2/temporal-attack/fixtures/rebuild.sh:9` | shell `$(git rev-parse HEAD)` | — | **live** (shell rule) | `/tmp` fixture (`:4`) → false positive |
| `…/rebuild.sh:11` | same | — | **live** | false positive |
| `round-17/measure.py:223` | rev-parse-HEAD | `_git_fixture` | fixture | correct |
| `round-17/tools/invocation-audit.py:424` | rev-parse-HEAD | `selftest` | fixture | correct |
| `round-17/tools/temporal-sweep.py:260,288,307,332` | rev-parse-HEAD | `selftest` | fixture | correct |

- **Observation.** With wrapper detection the rules give live = 8. If "git argv" means list literals only, live = 6, and `verify.py:59` and `controls.py:442` drop out.
- **Observation.** `custody-pair.py:349` (`"# repo-HEAD: %s"`) contains the substring `HEAD:`. A substring `HEAD-colon` matcher would flag it, and the contract keeps that header line (`contract.md:79`), so such a matcher can never reach 0.
- **Why the extra sites exist (observation).** The w2 attack scripts were untracked when the audit ran: `git ls-tree -r --name-only da64646 -- .ufo/waves/round-17/w2 | grep -cE '\.(py|sh)$'` printed `0` (exit 1). They were added later, in `95e34db`/`d0ab299` (`git log --diff-filter=A …`, exit 0).
- **Inference.** The "3" comes from JjAuditKaidoku.md (audited at `da64646`, scope listed at :13-18). It was not measured at B with the stated rules.
- **Inference.** The executor prompt anchors the tool to that number: "Ground truth for the baseline … the three HEAD-keyed live sites are …" (`wave1-spec.json:20`). It also asks the seat to explain each extra hit as "true positive or lint bug". That invites tuning the lint until it outputs 3.

### E3 — the denylist misses HEAD pins (A3, A4)

I ran the same prototype over 20 one-function snippets (in-memory; nothing written). Only these were caught:
- `f"HEAD:{p}"` (HEAD-colon)
- the jj-red-before baseline expression `["git","-C",sb,"rev-parse","HEAD"]` in `run_steps`, which counts as **live**
- a misnamed fixture helper `_commit`, which counts as **live**

Not caught (each one pins HEAD):
- `rev-parse @`
- `rev-parse --verify HEAD^{commit}`
- `HEAD~0`
- `log -1 --format=%H` (implicit HEAD)
- `rev-list -1 HEAD`
- `show HEAD -- f`
- `ls-tree -r HEAD`
- `DEFAULT_REV="HEAD"; default=DEFAULT_REV`
- `os.environ.get("REV","HEAD")` → f-string
- `def check(root, rev="HEAD")`
- `"%s:%s" % ("HEAD", p)`
- `subprocess.check_output("git rev-parse HEAD", shell=True)`
- `"git rev-parse HEAD".split()`
- `add_argument("--commit", default="HEAD")`
- `rev = "HEAD"; git("rev-parse", rev)`

Shell: `${REV:-HEAD}`, `git rev-parse @` and `git log -1` are also not matched.

- **Observation (fair to the claim).** At B, none of these blind-spot forms occurs in a live in-scope site. The only non-matching HEAD forms are fixture forms: `temporal-sweep.py:343` (`rev-list … HEAD`, in `selftest`) and `citation-drift-probe.py:451` (variable indirection, in `selftest`). Command: `git grep -n -E "\"@\"|'@'|\"log\"|'log'|git log|rev-list|describe|\"--format=%H\"" 9011581 -- <scope>`, exit 0. So **the baseline 3 is not under-counted. The risk is in the "after" count.**
- **Observation.** `contract.md:54` requires `git rev-parse --verify HEAD^{commit}`. The contract also tells each fixed site to inline that call (`:73-85`), so the read appears in all four fixed bodies.
- **Inference.** The delivered revision reaches 0 only if the lint does **not** treat `HEAD^{commit}` as HEAD. The same rule also lets `source = git("rev-parse","--verify","HEAD^{commit}")` through. That is the exact R1 regression, written one character differently.
- **Inference.** `jj-red-before.py` (`contract.md:95`) must run `git -C sb rev-parse HEAD` and lives in scope (`.ufo/waves/round-18/`). Verify18Harness expects `--strict` at source to exit 0 (`wave1-spec.json:95`). So either the lint reports live ≥ 1 at S, or the author hides the call with a function name containing `fixture` or a runtime-built argv. Either way, suppression would be decided by naming, which is a second authority nobody reviews.

Out of scope, and silent in the output: 142 tracked files under `.ufo/waves/arc3-loop1-*` match `rev-parse.{0,20}HEAD|"HEAD"`. That includes ≥ 19 copies of `citation-drift-probe.py` with `default="HEAD"`, for example `…/arc3-loop1-round1/claims/c2/RV-6/after/citation-drift-probe.py:477`. Commands: `git grep -l … | uniq -c` and `git grep -n 'default="HEAD"' …`, both exit 0. Excluding them is defensible (they are historical wave outputs; audit §6 :256), but "0" is only meaningful together with that scope.

### E4 — sandbox fidelity, run once in my own mkdtemp sandbox (A5, A6)

`bash /tmp/criticc2-probe.sh` exited 0; the script was deleted afterwards. It did:
- `git clone --no-local LANE sb`
- `jj --config user.name=… git init --colocate`
- a helper-style `jj commit` + `jj --ignore-working-copy bookmark set main -r @-`
- a `jj commit -m off` that leaves main unmoved
- the B citation-drift probe, run from a `/tmp` copy

Output (verbatim excerpts):
```
[after-clone]   HEAD=9011581d8452 main=9011581d8452 origin/main=9011581d8452 symref=refs/heads/main rc=0
[after-jj-init] HEAD=9011581d8452 main=9011581d8452 ...                     symref=refs/heads/main rc=0
[after-helper-style-commit] HEAD=af455e48ea02 main=af455e48ea02 origin/main=9011581d8452 symref=rc=1 is-ancestor-of-main=0
[after-off-commit]          HEAD=d1ede51d92c7 main=af455e48ea02 ...                      symref=rc=1 is-ancestor-of-main=1
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT: pointer_table_unreadable entry=expected.json [Errno 2] No such file or directory: '/tmp/criticc2-…/expected.json'
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2          # baseline probe, default paths
baseline-probe HEAD(off) exit=0  /  baseline-probe main exit=0        # with LANE's real --table/--expected
findings identical HEAD(off) vs main: diff exit=0
bp-head.txt:CITATION_DRIFT_VERDICT: reported findings=0 exit=0
bp-main.txt:CITATION_DRIFT_VERDICT: reported findings=0 exit=0
cleanup exit=0
```

What this shows:
- **Observation.** A clone of the detached lane (E1) starts **attached** to `refs/heads/main`, and `jj git init` keeps it attached. The contract's sequence (`contract.md:89-91`) then goes straight to the off-branch commit. It never produces the live state from E1 and JjTrialKaidoku.md:40 (detached at the tip).
- Detached-at-tip is the state where a fixed form must stay **quiet** (exit 0, `head_equals_source: true`). That is the false-refusal regression check, and no expectation in `contract.md:92-97` covers it.
- **Observation.** The baseline probe resolves its defaults relative to its own file (`citation-drift-probe.py:60-62`). Copied to a temp file, it fails at `run_check` → `pointer_table_unreadable` (`:289-293`) **before** reading any tree.
- With the real paths, the off commit only adds a file that nothing cites. So findings are identical, and the probe prints only the literal string `CITATION_DRIFT_REVISION: HEAD` (`:325`), not a sha.
- Step (1)'s "red if it evaluates the off-branch commit" therefore has no behavioral signal. It holds by spelling, or by an unrelated exit 2.
- **Inference.** JjTrialKaidoku.md:44-45 describes a third state: rejected push → fetch + rebase, after which committed ≠ pushed. It is not modeled at all. The trial does not report where HEAD ends up after that recovery, so whether fixed forms refuse there is unknown.
- **Observation.** The sandbox does not carry the lane's jj repo config (`auto-track="none()"`, identity, `trunk()` alias; JjTrialKaidoku.md:21). That config lives in `.jj/` and is not cloned. With the default `all()`, the planted file is auto-tracked, so the off commit is non-empty. Under `none()` it would be empty, but still off-branch. This is minor, but it should be stated.

### E5 — verify.py: bytes never run, identity changed (A7, A8)

- **Observation.** `verify.py` hard-codes `LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"` (`round-17/verify.py:21`) and calls `git -C LANE` (`:51`). So jj-red-before cannot point it at `sb`.
- The contract tells all four fixed sites to **inline** their own copy of the logic (`contract.md:74,83-85`). jj-red-before step (4) tests `revpin.resolve_source` (`:95-96`). Verify17BranchTip tests "a tiny /tmp harness" extracted from the logic (`wave1-spec.json:40`).
- Neither of those is the shipped `verify.py`. So "site 1 fixed" would be supported only by the lint no longer seeing `rev-parse HEAD` there.
- **Observation.** `git show 9011581:.ufo/waves/round-17/verify.py | sha256sum` gives `2896f53a…1903`. That digest equals the pinned entry in r17 `verification.json` `pins_pre.entries[".../round-17/verify.py"].sha256` (`2896f53a…1903`, size 10047). Both commands exited 0.
- An in-place edit makes the working-tree producer differ from its retained pin. The contract acknowledges this only with a header comment (`contract.md:86`).
- **Inference.** r18 ships its own `W18/verify.py` pinned by revpin (`contract.md:146`). Nothing re-runs the r17 pass. So the r17 edit mostly changes the count, not lane behavior.
- **Observation (no harm found).** custody-pair `compare` already skips `#` lines (`custody-pair.py:465`). The new `# repo-*` headers therefore cannot break comparison with the r17 `custody-r17.v2.txt`.

## Smallest safe corrections

1. **Make the count reproducible from stated rules (A1, A2).** The lint should emit every hit in every context, plus `files_scanned` and the scope prefixes. Any exclusion (`w2/`, `fixtures/`, a named helper) goes into an explicit `excluded:[{path, line, reason}]` list in the output. No silent filtering, and no matching on function names alone. Detect wrapper calls (a `Call` whose string args include `rev-parse` and `HEAD`). Report the line of the `HEAD` literal so it matches the audit anchor (`custody-pair.py:327`, not `:326`).
   The claim should then read "live at B = N (list), of which 3 are jj-relevant and the rest are dispositioned fixture/excluded with reasons". It should not say "3 at B" unless the tool prints exactly 3 with no hidden filter.
2. **Declare the blind spots (A3).** Add `limits:[…]` to the lint output, naming at least `HEAD^{…}`/`~N`/`@`, implicit-HEAD commands (`log -1`, `show`, `ls-tree HEAD`), non-literal defaults, string commands, and shell `${X:-HEAD}`. Either extend `rev-parse-HEAD` to any `HEAD[\^~]…`/`@` token **outside** the inlined compare-only call, or keep the narrow rule and state that "0" means "0 denylisted spellings". Add E3 snippets as selftest red cases or as declared-limit cases.
3. **Allowlist by reviewable entry, not by naming (A4).** jj-red-before's intentional baseline expression goes into a checked allowlist (path + exact code + reason), and the output reports `allowlisted_count`.
4. **Sandbox states (A5, A6).** Add these expectations:
   - (a) After a helper-style commit + bookmark move (detached at tip): baseline and fixed forms agree, fixed forms exit 0 with `head_equals_source:true`. This is the no-false-refusal check.
   - (b) The off commit **modifies a line cited by `pointer-table.json`**, and the baseline probe runs with LANE's real `--table/--expected`. Baseline findings should then differ from those at `main`, making the red behavioral.
   - (c) Run baseline custody-pair with `cwd=sb`, so `Path.cwd()` (`custody-pair.py:349`) records the off commit.
   - (d) Optionally, a rebase-recovery state, or state explicitly that it is unmodeled.
5. **Exercise shipped bytes (A7).** Copy the delivered `verify.py` into the sandbox and replace only the `LANE` constant with `sb`. In the off-branch state it should exit 2 before creating `verify/` output; record the argv/exit/stdout and the copy's diff (one line).
6. **Name the identity change (A8).** Record in LOG/knowledge that `round-17/verify.py` changed from pinned `2896f53a…` to `<new sha>`, and that the r17 producer is `git show d0ab299:…/verify.py`. Alternatively, leave r17 `verify.py` byte-identical with a reasoned `excluded` entry (historical one-shot, superseded by W18/verify.py). The judge should weigh this tradeoff.

## What a non-author would need to see to agree operability improved

- One lint, pinned by sha256, run from S against **both** B and S. The same bytes must be used at both revisions. Note: measure.py loads the lint only "when present at REV" (`wave1-spec.json:85`), so `measure.py B` reports could-not-evaluate, not 3.
- Full site lists from both runs, with explicit exclusions and limits.
- A reconciliation table: JjAuditKaidoku.md §3.1's 32 live rows (:164-195) → lint rows.
- **Mutation proof at S.** In a mkdtemp clone of S, restore each of the three fixed files to its B bytes, one at a time (`git show B:path > path`, three runs). Expect the lint to give live = 1 each time, and the matching jj-red-before step to go red. This shows the 0 is caused by the fixes and not by lint drift.
- A jj-red-before receipt containing the four states in correction 4, with behavioral (not spelling) discrimination for every red.
- The shipped `verify.py` copy run as in correction 5.
- A live-lane read-only run of each fixed form in the current detached-at-tip state, showing exit 0 and no false refusal. For example, `revpin.py --root LANE` → `head_equals_source: true`.

## Commands run (all exits shown inline above)

- `cat claims.json; ls …` (exit 0; `round-18/tools` absent).
- Repo state: `git rev-parse` (exit 0), `cat .git/HEAD` (exit 0), `git for-each-ref` (exit 0).
- B sweep: `git ls-tree`, `git grep` (exit 0).
- In-context reads of each site via `git show 9011581:<path> | awk` (exit 0).
- Python prototype over Git objects (in-memory, no writes).
- w2 history: `git ls-tree da64646 … | grep -c` (printed 0, exit 1); `git log --diff-filter=A` (exit 0).
- verification.json pin vs blob sha (exit 0).
- Out-of-scope `git grep` counts (exit 0).
- `jj --version` → `jj 0.45.1-7c41cdeb…` (exit 0; run with cwd=LANE, no repo access).
- Temp safety: `echo $TMPDIR` → unset; `findmnt /tmp` → xfs (exit 0).
- Sandbox script (exit 0, sandbox removed).

No jj or git write ran in LANE. Installs: none.
