# CustodyPairBranchTip — round-18 report (custody-pair.py R3 fix)

Scope: in-place edit of `.ufo/gates/custody-pair/custody-pair.py` per contract
bullet `custody-pair.py` (contract.md:78-82), closing jj risk R3
(`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:167,246`).

## Files changed

- `.ufo/gates/custody-pair/custody-pair.py` — only file edited.

## Behavior (what changed)

- `capture` gains `--repo DIR` (`custody-pair.py:1436`), default
  `LANE_ROOT = TOOL_PATH.parents[3]` — the directory that owns `.ufo/`
  (`custody-pair.py:214`). `Path.cwd()` is never consulted; cwd is still
  printed as `# cwd:`.
- `repo_head(cwd)` deleted; replaced by `_git_at(repo, *argv)` +
  `repo_context(repo)` (`custody-pair.py:350-391`), all read-only
  (`rev-parse --git-dir`, `rev-parse HEAD`, `rev-parse --verify
  refs/heads/main^{commit}`, `status --porcelain --untracked-files=no`).
- Receipt header keeps `# repo-HEAD:` (self-pin `# tool: … sha256` untouched)
  and adds, in contract order (`custody-pair.py:407-412`):
  `# repo-root:`, `# repo-branch:`, `# repo-branch-tip:`,
  `# repo-HEAD-is-branch-tip: yes|no`, `# repo-dirty: yes|no`.
- L1 directive applied: every HEAD read used only for comparison with the
  branch tip, plus the retained `# repo-HEAD:` emit line, carries the
  comment `# head-rev-lint: compare-only` (custody-pair.py:381, 407,
  1350, 1353). Tip comes from `refs/heads/main^{commit}` only
  (custody-pair.py:382); `Path.cwd()` is never used for the repo pin.
- Compare semantics unchanged: `parse_receipt`/`verify` never read `#` header
  lines — they are metadata exactly as `# repo-HEAD:` always was.
- Fail-closed notes (OBSERVATION of my own choices): non-repo or missing
  branch → `repo-HEAD-is-branch-tip: no`; `repo-dirty:` prints `(none)` when
  `git status` cannot run (contract's `yes|no` holds whenever the value is
  knowable; `(none)` is the honest unknown, matching `(none)` for hashes).
- New selftest cases (custody-pair.py:1336-1387):
  - `repo-header-off-branch-tip-no` — RED case: mkdtemp fixture repo, two
    commits, `git checkout --detach HEAD~` → header must read
    `repo-HEAD-is-branch-tip: no`, `repo-HEAD` = off-branch commit,
    `repo-branch-tip` = tip, `repo-dirty: no`; then `checkout main` → `yes`.
  - `repo-arg-and-lane-root-default` — subprocess capture with `cwd="/"`,
    no `--repo` → `repo-root` = LANE_ROOT; explicit `--repo` → that repo.
- Docstring: ROUND-18 HARDENING paragraph (custody-pair.py:102-121);
  `RECEIPT_VERSION` stays 2 (custody-pair.py:209).

## Receipt-version: NO bump required

`# receipt-version: 2` stays. The additions are `#`-prefixed header comments:
`parse_receipt` splits on `PATH:` stanzas and regex-reads stanza keys only
(v2 path), or skips `#` lines entirely (v1 shapes); verify compares only
stanza `COMPARE_KEYS` (11 fields). Stanza shape, parse and compare are
byte-for-byte unchanged — new receipts self-describe as v2 and old v2
receipts remain fully comparable.

## Commands run (exact, with exit)

1. `python3 -c "import json; …claims.json…"` — exit 0 (read claims).
2. `python3 -I -B …/custody-pair.py selftest` — **exit 0**; last line:
   `CUSTODY_PAIR_SELFTEST: CLEAN cases=30 passed=30 failed=0 exit=0`
   (new cases `repo-header-off-branch-tip-no` and
   `repo-arg-and-lane-root-default` both PASS; USAGE/verify lines above it
   are case-expected output).
3. `python3 -I -B …/custody-pair.py capture --out /tmp/kr18-custody-test.txt`
   — **exit 0** (`CUSTODY_PAIR_CAPTURE: OK paths=5/5`); stderr carried the
   declared `WARN: /tmp is quota-exhausted…`.
4. `rm -f /tmp/kr18-custody-test.txt{,.sha256} && ls /tmp/kr18-custody-test.txt*`
   — rm exit 0; `ls` exit 2 (confirming deletion).
5. `grep -n … custody-pair.py` — exit 0 (line anchors only).
6. (post-L1-note) `python3 -c "import ast; ast.parse(…)"` — exit 0
   (`SYNTAX OK`); `python3 -I -B …/custody-pair.py selftest | tail -8` —
   **exit 0**, last line identical: `CUSTODY_PAIR_SELFTEST: CLEAN cases=30
   passed=30 failed=0 exit=0`.

## New header lines from the /tmp capture (since deleted)

```
# repo-HEAD: 9011581d84527ba34c675f9cf912e54d2e72d470
# repo-root: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# repo-branch: main
# repo-branch-tip: 9011581d84527ba34c675f9cf912e54d2e72d470
# repo-HEAD-is-branch-tip: yes
# repo-dirty: yes
```

OBSERVATION: the capture ran with `cwd=/home/vgpnk/Projects/shokunin` (the
monorepo parent) yet `repo-root`/`repo-branch-tip` pin the lane —
`# repo-HEAD:` now equals the lane branch tip because HEAD sits at it;
`repo-dirty: yes` is real (tracked ` M` on round-17 tools + this edit).

## Risks / blockers

- `.ufo/gates/custody-pair/README.md` is now stale (says 28 cases, no
  `--repo`); README edits were out of my assigned-file scope — flag for L1
  integration (README.md:229-248).
- `REPO_BRANCH` is the literal `main` per the lane VCS rule; a non-`main`
  `--repo` would read `repo-branch-tip: (none)` and `…-is-branch-tip: no`
  (fail-closed, correct).
- No tool installs; no git/jj writes in the lane; no blockers.
