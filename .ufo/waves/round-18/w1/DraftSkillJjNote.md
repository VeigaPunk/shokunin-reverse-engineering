# DraftSkillJjNote — round 18 wave 1 (SKILL.md draft, read-only)

- Seat: KaidokuR18.DraftSkillJjNote (leaf, advisory author-side draft; L1 integrates).
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, branch `main`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470` (contract.md:4).
- Lane files written: none. Only this report. No subagent dispatched. No REA, Ghidra, or carrier execution. No jj run anywhere.
- Installs: none. The host pacman pause and the operator tooling directive were not exercised; no tool was needed.

## Method and observations

Sources read in full: `JjAuditKaidoku.md` (F1–F7, §5 R1–R3, §7), `JjTrialKaidoku.md` (Steps 1–5, hazards 1–7), `contract.md` (VCS rule, C2), `claims.json` (C2 entry), `RULES.md`.

Command-sourced observations (read-only git in the lane, this seat):

```
$ git -C <lane> symbolic-ref -q HEAD            -> refs/heads/main (attached)
$ git rev-parse HEAD main origin/main           -> 9011581d84527ba34c675f9cf912e54d2e72d470 (all three)
$ git merge-base --is-ancestor HEAD main        -> exit 0
$ git status --porcelain --untracked-files=no | wc -l -> 0
$ ls -d .jj                                     -> .jj (exit 0)
$ glob .ufo/waves/round-18/**/*.py              -> gen-wave1.py only
```

The observed state at draft time is attached HEAD equal to the branch tip, with ancestry exit 0 and zero tracked modifications.

- `.jj` now exists in the live lane; the audit observed none at its time (JjAuditKaidoku.md:5). The audit's F1 says HEAD is attached immediately after colocation (JjAuditKaidoku.md:42-45), which matches the attached state observed here.
- The round-18 tools named in the contract (`revpin.py`, `head-rev-lint.py`, `jj-red-before.py`) are not yet present in the lane (glob above; contract.md:49-98 names them as to-be-built).

## Draft

### Revision pins under jj (round 18)

The lane `kaidoku-shokunin` is jj-colocated (jj 0.45.1). Git HEAD is not a reliable branch pointer: it is attached to `main` right after colocation and detached after a jj mutation (JjAuditKaidoku.md:42-45, JjTrialKaidoku.md:79). A HEAD-keyed read still returns data when HEAD is off-branch, so a successful read is not evidence that the tree landed (JjAuditKaidoku.md:69-71). Pin the branch tip, not HEAD (contract.md:17-21).

| Signal (read-only command) | Decision | Limit |
|---|---|---|
| `git symbolic-ref -q HEAD` → `refs/heads/main`, and `git rev-parse HEAD` equals `git rev-parse refs/heads/main` (JjAuditKaidoku.md:42-45) | Use the branch tip as the revision; HEAD may be used only because it equals the tip. | Holds only until the next jj mutation, which detaches HEAD (JjTrialKaidoku.md:40, :79). Re-check on every run. |
| HEAD ≠ branch tip: `symbolic-ref` exits 1, or `git merge-base --is-ancestor HEAD refs/heads/main` exits 1 (JjAuditKaidoku.md:65-69: HEAD `f87053c4…`, main `4c63e873…`) | Refuse with exit 2 and finding `head_not_branch_tip`; a literal `--rev HEAD` is accepted only when it equals the tip (contract.md:73-76, :93-94). | `git show HEAD:<path>` still succeeds off-branch (JjAuditKaidoku.md:71), so the failure is silent unless the ancestry check runs. |
| Tip ahead of remote: `refs/heads/main` ≠ `refs/remotes/origin/main` (contract.md:55-56, `branch_not_pushed`) | Refuse any record that claims the tree landed; cite only the `pushed` hash. | Rebase after a rejected push changes the hash: `committed f84fbda9` vs `pushed d898a7e8`; the `committed` hash is not on the remote (JjTrialKaidoku.md:44, :80). |

**`--rev HEAD` refusal.** `citation-drift-probe.py:477` defaults `--rev` to `HEAD`, and `git_show` reads `{rev}:{path}` at `citation-drift-probe.py:102`. Round 18 makes the default the branch tip, accepts literal `HEAD` only when it equals the tip, and otherwise exits 2 with `head_not_branch_tip` (contract.md:73-76). The audit classes the default as medium risk (JjAuditKaidoku.md:164) and as a false-red risk under `auto-track="none()"` (JjAuditKaidoku.md:244); that false-red chain is audit reasoning, not an executed result (JjAuditKaidoku.md:269).

**Custody repo branch tip.** `custody-pair.py:349` writes `# repo-HEAD:` from `repo_head(Path.cwd())`, which runs `git rev-parse HEAD` (`custody-pair.py:327`). Under jj that is `@-`, and it depends on the caller's directory (JjAuditKaidoku.md:167, :246). Round 18 adds `--repo DIR` (default: the lane root, never `Path.cwd()`) and the fields `# repo-root:`, `# repo-branch:`, `# repo-branch-tip:`, `# repo-HEAD-is-branch-tip: yes|no`, `# repo-dirty: yes|no` (tracked modifications only), and keeps `# repo-HEAD:` (contract.md:78-82). Read `repo-HEAD-is-branch-tip` before trusting `repo-HEAD`.

**Limits for all rows.**
- The round-17 `verify.py:59` (`git rev-parse HEAD`) is the highest-risk site (JjAuditKaidoku.md:187, :242). `verify.py` is untracked at HEAD (JjAuditKaidoku.md:144-146), so the round-18 change takes effect only once it is committed.
- Rev-pinned gates are insensitive to detach: `controls.py`, `temporal-sweep.py`, and `invocation-audit.py` exited 0 on a detached colocated lane and matched a plain clone (JjTrialKaidoku.md:53-56). The exposure is HEAD-keyed defaults, not every git call.
- jj revset syntax is not git syntax: `git rev-parse main@origin` fails (JjAuditKaidoku.md:109). Use `refs/remotes/origin/main` in git commands.
- Git staging is not durable across jj calls: a `git add` survives `jj status` but is reset by the next `jj commit` (JjTrialKaidoku.md:78; JjAuditKaidoku.md:76-91). Do not `git add` or `git commit` inside the lane.
- The audit covered jj 0.45.1 only and ran in a sandbox, not in the live lane (JjAuditKaidoku.md:272, :273).

## Findings for L1

- Calibration: the three rows above are the only signals the audit and trial both observed; no row is generalized beyond jj 0.45.1.
- Operability: the reproducible check is `git -C <lane> symbolic-ref -q HEAD; git rev-parse HEAD refs/heads/main refs/remotes/origin/main; git merge-base --is-ancestor HEAD refs/heads/main`.
- Depth: the trial's rev-pinned gate results (JjTrialKaidoku.md:53-56) and the audit's HEAD-keyed site list (JjAuditKaidoku.md:242-246) separate the risk from the non-risk.
- Placement suggestion (L1 decision): append as a `###` under a new round-18 `##` section after `## Retained Go carrier diagnostics — round 17` (SKILL.md:509), or under `## Config custody for live-probe rounds (SOP)` (SKILL.md:319) if L1 prefers custody placement.
- Open: the three round-18 tools are not built; the draft names them only as contract items (contract.md:49-98). The draft should be re-checked against them once they land.
