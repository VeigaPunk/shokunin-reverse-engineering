# Verify17BranchTip — round-17/verify.py jj-safe source pin (R1)

Scope: contract.md bullet `round-17/verify.py` (contract.md:83-86), implementing
JjAuditKaidoku.md R1 (line 242; cell line 187), plus L1 mid-flight revision:
HEAD probed by `git rev-parse --verify HEAD^{commit}` carrying the marker
`# head-rev-lint: compare-only`; every git probe failure maps to a named finding
(`branch_missing` / `head_not_branch_tip` / `branch_not_pushed` /
`status_failure`) and exit 2; header warns that a rerun overwrites the retained
r17 evidence and belongs only in a clone. Minimal diff: source-revision
resolution + pre-run refusal only. verify.py itself was NOT run (it runs the
whole r17 pass); the new logic was proven by a /tmp harness against mkdtemp
repos.

## Files changed

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/verify.py`
  (+59/−2). `_git_or_none` helper at verify.py:65-69; `resolve_source(branch=)`
  at verify.py:72-103 (HEAD probe with `# head-rev-lint: compare-only` marker
  at verify.py:83-84); refusal gate at verify.py:110-113, placed before the
  `base` rev-parse so it precedes every command of the pass;
  `source = res["source"]` at verify.py:115 (was `git rev-parse HEAD`);
  record gains `source_branch`, `head_equals_source` at verify.py:225;
  docstring change-note + rerun-overwrites warning at verify.py:10-17.
- Harness (not a lane file): `/tmp/verify17_harness.py`.

## What changed (observed)

- `source` is now `refs/heads/main^{commit}` (branch tip), never HEAD. Under jj
  colocation HEAD is the working-copy parent `@-`, which can be an unbookmarked,
  unpushed commit (JjAuditKaidoku.md:242 observed `HEAD=f87053c4…` vs
  `main=origin/main=4c63e873…` — that divergence is exactly what the gate now
  refuses).
- Before any command of the pass runs, it exits 2 with JSON
  `{"refused": true, "findings": [...]}` unless HEAD == `refs/heads/main`,
  `refs/heads/main` == `refs/remotes/origin/main`, and
  `git status --porcelain --untracked-files=no` is empty.
- Per-probe failure→finding mapping (L1 spec): branch-tip rev-parse fails ⇒
  `branch_missing`; HEAD rev-parse fails or mismatches ⇒ `head_not_branch_tip`;
  remote rev-parse fails or mismatches ⇒ `branch_not_pushed` (absent remote =
  failure); `git status` nonzero ⇒ `status_failure`, empty-vs-nonempty ⇒
  `worktree_dirty`. Findings accumulate, so a deleted `main` reports
  `["branch_missing","head_not_branch_tip","branch_not_pushed","worktree_dirty"]`
  (case e below) — every violated condition is named, refusal is still exit 2.
- The HEAD probe uses `rev-parse --verify HEAD^{commit}` deliberately (L1):
  it is a compare-only read of the ref, marked `# head-rev-lint: compare-only`
  on the line above so the round-18 lint can classify it as the one intentional
  HEAD site rather than an anonymous live site. `source` itself never goes
  through HEAD.
- [INFERENCE] `git status --porcelain --untracked-files=no` under jj colocation
  still detects tracked content edits (the audit found `git status` matched
  `jj diff --summary`, JjAuditKaidoku.md:188). Untracked files are ignored by
  design (contract); the existing `worktree_dirty_at_start` record still
  captures them.

## Diff

```diff
diff --git i/.ufo/waves/round-17/verify.py w/.ufo/waves/round-17/verify.py
index b6852f9..810f138 100755
--- i/.ufo/waves/round-17/verify.py
+++ w/.ufo/waves/round-17/verify.py
@@ -7,6 +7,15 @@ retains argv, cwd, env overrides, UTC start/end, exit, and stdout/stderr
 with tools/pins.py before and after the pass: equal maps show identical bytes
 at those two instants, not continuity between them (QUALITY #19).

+Round-18 change (jj colocation fix, JjAuditKaidoku.md R1): `source` is now
+refs/heads/main (the branch tip), never HEAD, and the pass refuses with
+exit 2 before running any command unless HEAD equals the branch tip, the
+tip equals refs/remotes/origin/main, and no tracked file is modified.
+The retained d0ab299 run (verification.json) used the pre-change bytes,
+where `source` was `git rev-parse HEAD`. Rerunning this script overwrites
+that retained round-17 evidence (verification.json + verify/); run it only
+in a throwaway clone.
+
 Usage: python3 -I -B verify.py BASELINE_REV   (writes verification.json + verify/)
 """
@@ -51,12 +60,57 @@ def git(*args):
     return subprocess.check_output(["git", "-C", LANE, *args], text=True).strip()


+def _git_or_none(*args):
+    try:
+        return git(*args)
+    except subprocess.CalledProcessError:
+        return None
+
+
+def resolve_source(branch="main"):
+    """jj-safe source revision + pre-run refusals (stdlib only; round-18 R1).
+
+    Pins `source` to refs/heads/<branch>, not HEAD: under jj colocation HEAD
+    is the working-copy parent (@-), which can be an unbookmarked, unpushed
+    commit. Returns {branch, source, head, remote, findings}; `findings` is
+    a list of named refusals and each git probe failure maps to one named
+    finding (branch tip -> branch_missing, HEAD -> head_not_branch_tip,
+    remote -> branch_not_pushed, status -> status_failure).
+    """
+    source = _git_or_none("rev-parse", "--verify", f"refs/heads/{branch}^{{commit}}")
+    # head-rev-lint: compare-only
+    head = _git_or_none("rev-parse", "--verify", "HEAD^{commit}")
+    remote = _git_or_none("rev-parse", "--verify", f"refs/remotes/origin/{branch}^{{commit}}")
+    try:
+        status_out = git("status", "--porcelain", "--untracked-files=no")
+        status_failed = False
+    except subprocess.CalledProcessError:
+        status_out, status_failed = "", True
+    findings = []
+    if source is None:
+        findings.append("branch_missing")
+    if head != source:
+        findings.append("head_not_branch_tip")
+    if remote != source:
+        findings.append("branch_not_pushed")
+    if status_failed:
+        findings.append("status_failure")
+    elif status_out.splitlines():
+        findings.append("worktree_dirty")
+    return {"branch": branch, "source": source, "head": head,
+            "remote": remote, "findings": findings}
+
+
 def main():
     if len(sys.argv) != 2:
         print(__doc__, file=sys.stderr)
         return 2
+    res = resolve_source()
+    if res["findings"]:
+        print(json.dumps({"refused": True, **res}, sort_keys=True, indent=2))
+        return 2
     base = git("rev-parse", "--verify", sys.argv[1] + "^{commit}")
-    source = git("rev-parse", "HEAD")
+    source = res["source"]
     dirty = git("status", "--porcelain")
@@ -168,6 +222,7 @@ def main():
         "baseline_revision": base, "source_revision": source,
+        "source_branch": res["branch"], "head_equals_source": res["head"] == res["source"],
@@ -180,7 +235,7 @@ def main():
-                      "source_revision": source}, indent=2))
+                      "source_revision": source, "source_branch": res["branch"]}, indent=2))
```

(Full diff: `/tmp/verify17.diff`, 96 lines; stat 1 file, +59/−2.)

## Harness proof

`/tmp/verify17_harness.py` imports the real verify.py, retargets `mod.LANE` at a
throwaway `mkdtemp` seed+clone pair, and exercises `resolve_source()` plus the
real `main()` refusal path (exit captured in-process; refusal returns before
any command runs, so nothing else executes):

```
PASS a_clean_head_main_origin: {"branch": "main", "findings": [], "head": "6d3ed53d0a303159a6b3fd285d35d124275463da", "remote": "6d3ed53d0a303159a6b3fd285d35d124275463da", "source": "6d3ed53d0a303159a6b3fd285d35d124275463da"}
PASS b_detached_off_branch: exit=2 findings=['head_not_branch_tip'] out='{\n  "branch": "main",\n  "findings": [\n    "head_not_branch_tip"\n  ],\n  "head": "a474f7051f920231056208cfac43dee66ec58319",\n  "refused": true,\n  "remote": "6d3ed53d0a303159a6b3fd285d35d124275463da",\n  "source": "6d3ed53d0a303159a6b3fd285d35d124275463da"\n}'
PASS c_unpushed_tip: exit=2 findings=['branch_not_pushed']
PASS d_tracked_dirty: exit=2 findings=['worktree_dirty']
PASS e_branch_missing: exit=2 out='{\n  "branch": "main",\n  "findings": [\n    "branch_missing",\n    "head_not_branch_tip",\n    "branch_not_pushed",\n    "worktree_dirty"\n  ],\n  "head": "ce83c482d254574462013b1a8c189f046b2bd8c0",\n  "refused": true,\n  "remote": "ce83c482d254574462013b1a8c189f046b2bd8c0",\n  "source": null\n}'
SELFTEST: CLEAN cases=5
harness_exit=0
```

- (a) HEAD == main == origin/main → `findings == []` (gate passes; the real
  pass would proceed — not run per assignment).
- (b) detached HEAD on an off-branch commit → `main()` exits 2, refusal JSON
  `head_not_branch_tip` — the required red case.
- (c) tip ahead of origin → `branch_not_pushed` exit 2.
- (d) tracked modification → `worktree_dirty` exit 2.
- (e) `refs/heads/main` deleted → every probe fails or mismatches, so all four
  violated conditions are named; `branch_missing` is present, exit 2, no
  traceback. `fatal: Needed a single revision` on stderr is git's own message
  during a failing probe — cosmetic; the exception is caught.
- `status_failure` is not naturally reproducible inside the fixture without
  breaking the repo outright (a corrupt `.git` would fail earlier probes too);
  its code path is the `CalledProcessError` arm at verify.py:89-90 → finding at
  verify.py:98-99.

## Commands run (exit codes)

| command | exit |
|---|---|
| `find /home/vgpnk -name 'JjAuditKaidoku.md' …` | 0 |
| `ls .ufo/waves/round-18{,/w1}` | 0 |
| `grep -n -i 'Verify17\|verify.py\|branch.tip' claims.json wave1-assignments.json` | 0 (hits pasted) |
| `grep -rn 'd0ab299' …` | 0 — d0ab299 confirmed as r17 source revision in verification.json/LOG.md |
| `python3 -I -B -c "import ast; ast.parse(…verify.py…)"` ×3 | 0 (`AST OK`) |
| `python3 -I -B /tmp/verify17_harness.py --selftest` (early runs) | 1 — two harness-side fixes (non-bare push refused → `receive.denyCurrentBranch=ignore`; case-e argv `main` unresolvable → `origin/main`) |
| `python3 -I -B /tmp/verify17_harness.py --selftest` (final, after L1 revision) | 0 — last line `SELFTEST: CLEAN cases=5` |
| `git -C LANE diff -- .ufo/waves/round-17/verify.py` ×3 | 0 (final diff pasted above) |
| `git -C LANE status --porcelain=v1` / `ls-files --error-unmatch` / `cat-file -e` | 0 — verify.py tracked, `M` |

--selftest evidence: `python3 -I -B /tmp/verify17_harness.py --selftest` →
exit 0, last line: `SELFTEST: CLEAN cases=5`

## Evidence retained

- Harness: `/tmp/verify17_harness.py`; full diff: `/tmp/verify17.diff`.
- Lane state at edit time: `HEAD == main == origin/main ==
  9011581d84527ba34c675f9cf912e54d2e72d470` (baseline B) — the gate passes on
  the real lane today; it only refuses under the jj hazard states R1 names.

## Risks / limits

- Gate placement: refusal runs before `base` rev-parse — `resolve_source`'s own
  four read-only git calls are the only commands run prior to refusal.
- The single `rev-parse HEAD^{commit}` site is intentional (L1 directive) and
  carries `# head-rev-lint: compare-only`; if the lint's classifier key for
  allowlisting differs, this comment is the hook to match.
- [INFERENCE] `worktree_dirty` under jj can under-report a staged-only state
  after an index reset — acceptable; content diffs do surface in
  `status --porcelain`.
- `status_failure` is unreachable in a healthy fixture repo; covered by code
  inspection, not a live red case.
- verify.py deliberately not executed; the L1's integrated re-run will exercise
  the ok path end-to-end (in a clone, per the new header warning).
- No tools installed; no peer conflicts (this seat owns verify.py per
  wave1-assignments `Verify17BranchTip`).
