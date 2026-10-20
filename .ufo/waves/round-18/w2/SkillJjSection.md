PARTIAL

# SkillJjSection — SKILL.md "Revision pins under jj — round 18" at REV (w2 falsify, advisory seat)

Target: `git show REV:SKILL.md` lines 567-593 (the section runs to EOF, `wc -l` = 593).
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`.
The lane was only read. Every experiment ran in `D=$(mktemp -d /dev/shm/skilljj-XXXXXX)` (`/dev/shm/skilljj-btHwak`), using `git clone --no-local` copies with `origin` removed (`git remote` prints nothing). D was removed after this report.
No installs. No REA, no Ghidra, no carrier executed. This verdict is a recommendation only.

## Verdict
Every citation resolves:
- S036 bytes and lines match.
- JjAuditKaidoku F2 is present and reproduces.
- The receipt shows 14/14, and re-running it on REV's bytes also gives 14/14.

The decision table, however, is not true of every lane tool it governs:
- Row 2's refusal only fires on the literal `HEAD`; aliases get past it, and custody-pair flags instead of refusing.
- Row 3's signal describes round-17 verify.py's equality test, but revpin and round-18 verify.py use an ancestry test.
- Row 3's citation rule brings back the retired `pushed <hash>` token.
- Row 588 has one overclaim about origin/main.

## Findings (severity order)

### M1 — `branch_not_pushed` has two semantics in the lane; SKILL.md:579 states only one [Medium, observed]
- SKILL.md:579 signal: "Tip differs from `refs/remotes/origin/main`" → refuse `branch_not_pushed`.
- `.ufo/waves/round-17/verify.py:94-95` at REV: `if remote != source: findings.append("branch_not_pushed")` (equality; matches contract.md:83-85).
- `.ufo/waves/round-18/tools/revpin.py:116` at REV: `"pushed": remote is not None and _is_ancestor(lane, source, remote)` (ancestry). The docstring at :32-35 rejects equality on purpose. revpin feeds round-18 verify.py:90-99 and is described at SKILL.md:588.
- Same sandbox state for both (HEAD = main = b2aad08, `origin/main` = 56610b3, a child of the tip, zero remotes):
  - round-17 `resolve_source()` (module loaded with `LANE` re-pointed to $SB, `main()` not called) → `{"findings": ["branch_not_pushed"], ...}`. r17verify:109-111 would therefore exit 2.
  - `python3 -I -B $SB/.ufo/waves/round-18/tools/revpin.py --root $SB` → exit 0, `"pushed": true`, `remote 56610b3… ≠ source b2aad08…`.
- The two agree only when the tip is ahead (`origin/main=main~1` → revpin exit 2 `branch_not_pushed`, observed), diverged, or the ref is absent. When the tip is behind origin, the table predicts a refusal that revpin does not make.

### M2 — Row 2's refusal fires only on the literal string `HEAD` [Medium, observed]
- SKILL.md:578: "HEAD is not the branch tip → Refuse with `head_not_branch_tip`, exit 2, before any gate runs".
- citation-drift-probe.py:314-316 at REV: "Any other explicit rev passes through unchanged"; :329 checks only `if rev == "HEAD":`.
- Sandbox setup: HEAD detached at off-branch 56610b3. SCORECARD.md:59 was rewritten with the edit tool to `OFF-BRANCH REWRITE by SkillJjSection sandbox …`; any edit that drops `[mcp_servers.rea]` reproduces this. Then a plain `git commit`. main = b2aad08.

  | `--rev` | exit | REV_RESOLVED | finding |
  |---|---|---|---|
  | (omitted) | 0 | b2aad08 | findings=0 |
  | `HEAD` | 2 | HEAD | head_not_branch_tip |
  | `@` | 0 | 56610b3 | citation_dead sc59 SCORECARD.md:59 (off-branch content) |
  | `HEAD~0` | 0 | 56610b3 | same |
  | `HEAD^{commit}` | 0 | 56610b3 | same |

- This is the silent wrong-tree read that the Limit cell at :578 says the check prevents.
- [INFERENCE] `@` is the likeliest slip. In jj, `@` means the working-copy commit; Git reads it as HEAD, which is jj's `@-`.
- head-rev-lint cannot see this: it scans code sites, not argv values (its own `limits`).

### M3 — Row 3's citation rule brings back the retired `pushed <hash>` token [Medium, observed]
- SKILL.md:579 says: "cite only the hash the helper printed as `landed`/`pushed`".
- The canonical lane contract, `scripts/hyaku/lane-addendum.md:135`, says: "Cite ONLY the helper's final `landed <hash>` line after successful remote verification."
  - Fleet commit `f4eac4e` (2026-10-20 13:09:50 -0300, in fleet HEAD) removed the old allowance "(an older helper prints `pushed <hash>`)".
  - That commit is earlier than REV (13:38:07).
- The lane helper prints only `rewritten` and `landed` (`jj-lane.sh:251,252,258`), and checks `landed` against `git ls-remote` (`:237-245`).
- The only current `pushed` printer is `fleet-commit.sh:64`: `echo "pushed $(git rev-parse --short HEAD) …"`. That is a short hash taken from bare HEAD with no remote check, which contradicts SKILL.md:573 "never bare HEAD".

### L1 — "tip pushed" (SKILL.md:588) overclaims what `pushed` means [Low, observed]
- The SKILL.md:579 Limit is right ("not live remote state"), but row 588 still says "0 tip resolved (HEAD equals tip, tip pushed)".
- Sandbox with `git remote` empty:
  - With no `origin/main` → revpin exit 2 `branch_not_pushed`, `remote: null`.
  - After `git update-ref refs/remotes/origin/main refs/heads/main`, still with no remote → exit 0, `"pushed": true`.
- The committed receipt follows the same pattern:
  - `git remote` prints "" (jj-red-before.json:212-221).
  - Then `update-ref` (:224-233).
  - Then D0 records `"pushed": true` (:70-73).
- "Last fetched position" is also imprecise. A push moves the ref too (JjAuditKaidoku.md:74: `origin/main` == pushed hash after `jj git push`), and any `update-ref` can set it.

### L2 — Row 2 doesn't fit custody-pair, and "never bare HEAD" (573) is literally false there [Low, observed]
- With an off-branch HEAD, the fixed custody-pair capture exits 0 and writes `repo-HEAD-is-branch-tip: no` with `repo_head` = the off-branch commit:
  - in the receipt (jj-red-before.json:573-583);
  - in my REV re-run (`fixed-custody-capture` exit 0).
- That flag-not-refuse behaviour is by design (contract.md:80-82; custody-pair.py:104-121).
- custody-pair.py:407 still writes bare HEAD: `# repo-HEAD:`, commented "retained @- pin, flagged below". The table never tells an operator to read `# repo-HEAD-is-branch-tip:` on custody receipts.
- Row 1's "record `head_equals_source: true`" is only the verify/revpin field. citation-drift emits `CITATION_DRIFT_REV_RESOLVED`, and custody-pair emits `repo-HEAD-is-branch-tip: yes`.

### L3 — The Evidence line (581-582) isn't bound to the bytes it vouches for; the substance still replicates [Low, observed]
- The receipt was produced while the lane tip was 9011581 (jj-red-before.json:176-178).
- Its "fixed" forms ran from the lane working tree: the step argv is `/home/vgpnk/…/kaidoku-shokunin/.ufo/gates/…`, and jj-red-before.py:1015-1019 defaults to "in the working tree".
- They were checked only by byte markers (jj-red-before.py:98-101). The receipt records no digest or revision of the fixed tools: zero occurrences of `b2aad08` or `eb6c266`.
- Mitigation, observed:
  - The receipt and the tools landed together in eb6c266, and `git diff --stat eb6c266 REV` over the four tools plus the receipt is empty.
  - Re-running at REV's bytes gives exit 0, 14/14 held.
- The receipt cannot support row 3:
  - No expectation in it exercises `branch_not_pushed`.
  - D0's `pushed` rests on a faked ref (jj-red-before.py:6-7,21).
  - Row 3 is supported only by revpin's selftest (revpin.py:188-209) and by M1/L1 here.

### L4 — The table leaves out states this lane will hit, and gives no recovery step [Low, observed + INFERENCE]
- **No `origin/main` ref.** Every contract-mandated sandbox clone (origin removed) hits this. revpin exits 2 `branch_not_pushed` with `remote: null` (observed); round-17 verify gives the same finding (None ≠ source). jj-red-before only works by faking the ref.
- **Findings the table never names:**
  - `branch_missing`.
  - round-17 verify's `worktree_dirty` and `status_failure` (r17verify:96-99).
  - round-18 verify.py only records dirtiness (verify.py:101,280); it does not refuse on it, which is another divergence between the two verify scripts.
- **No recovery after `head_not_branch_tip`.** [INFERENCE] The helper's `reanchor_wc` handles only an EMPTY `@` (jj-lane.sh:262-275). A non-empty off-branch commit needs a land-or-abandon step that the table doesn't name.

### I1 — Citation precision [Info]
- Row 1 ("detached at the tip … after a helper commit") rests on F1 (JjAuditKaidoku.md:47-56) and on F2's last paragraph (:74), but the section cites only F2.
- The cross-repo citation is a bare worktree path. The file is tracked at fleet `7d0c7605` and unchanged (sha256 `cac5daf6…`), so it is grounded today but not pinned to a revision.

## Claims that hold
- **S036.** The raw v0.45.1 `git-compatibility.md` hashes to sha256 `0fb71f99…c641`, matching SOURCES.md:42. Lines 114-116 read "`jj` commands will usually put the Git repo in a "detached HEAD" state". Line 208 says HEAD points "to the working-copy commit's parent".
- **jj 0.45.1, colocated.** `jj --version` → `0.45.1-7c41cdeb…`, and `$LANE/.jj/repo/store/git_target` = `../../../.git`.
- **Live lane is in row 1's state.** `git symbolic-ref -q HEAD` exits 1, and HEAD = `refs/heads/main` = `refs/remotes/origin/main` = b2aad08.
- **F2 reproduces.** With HEAD at 56610b3, `merge-base --is-ancestor HEAD main` exits 1 and `git show HEAD:SCORECARD.md` exits 0.
- **Row 2 holds for:**
  - round-18 verify.py:89-99 and r17verify:108-111 (both refuse before any command runs);
  - the revpin CLI (exit 2, observed);
  - a literal `--rev HEAD` (exit 2, observed).
- **Row 3 holds** when the tip is ahead of origin and when the ref is absent (both exit 2, observed).
- **head-rev-lint at REV** (sandbox clone): exit 0, `live_count` 0, `annotated_count` 6, `fixture_count` 15.
- **Registry row 589.** The re-run exits 0. Its own `/tmp/jj-red-before-qijw7m9*` sandbox is gone afterwards (`ls`: cannot access), and lane_tip before == after.

## Commands (exit codes observed)
```
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94
FLEET=/home/vgpnk/Projects/shokunin D=/dev/shm/skilljj-btHwak SB=$D/sb L=$D/lane-rev
git -C $LANE show $REV:SKILL.md | grep -n "Revision pins under jj"            # 0 -> 567
git -C $LANE show $REV:corpus/SOURCES.md | grep -n S036                      # 0 -> 42,50
curl -sSfL -o $D/gc.md https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md  # 0; sha256 0fb71f99…c641
jj --version                                                                  # 0 -> 0.45.1-7c41cdeb…
git -C $LANE symbolic-ref -q HEAD                                             # 1 (detached)
git -C $LANE rev-parse HEAD refs/heads/main refs/remotes/origin/main          # 0 -> b2aad08 x3
git -C $FLEET ls-files --error-unmatch .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md   # 0
git -C $FLEET diff --quiet HEAD -- .ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md        # 0
grep -n -E 'echo "(pushed|landed|rewritten)' $FLEET/scripts/hyaku/jj-lane.sh  # 0 -> 251,252,258
git -C $FLEET show f4eac4e -- scripts/hyaku/lane-addendum.md | grep -n -E '^[-+].*(pushed <hash>|landed <hash>)'  # 0
git -C $FLEET merge-base --is-ancestor f4eac4e HEAD                           # 0
git clone -q --no-local $LANE $SB && git -C $SB remote remove origin          # 0; `git -C $SB remote` prints nothing (same for $L)
sha256sum <tool> vs git show $REV:<tool> (probe, custody-pair, revpin, jj-red-before, r17 verify)  # equal x5
python3 -I -B $SB/.ufo/waves/round-18/tools/revpin.py --root $SB              # 2 branch_not_pushed, remote null
git -C $SB update-ref refs/remotes/origin/main refs/heads/main; <revpin>      # 0; pushed true, zero remotes
git -C $SB checkout -q --detach refs/heads/main; <edit SCORECARD.md:59>; git -C $SB -c user.name=sandbox -c user.email=sandbox@example.invalid commit -q -am off   # 0 -> 56610b3
git -C $SB merge-base --is-ancestor HEAD refs/heads/main                      # 1
python3 -I -B $SB/.ufo/gates/citation-drift/citation-drift-probe.py --root $SB [--rev X] --table $SB/.ufo/gates/citation-drift/pointer-table.json --expected $SB/.ufo/gates/citation-drift/expected.json   # M2 table
<revpin> at off-branch HEAD                                                   # 2 head_not_branch_tip
git -C $SB checkout -q --detach refs/heads/main && git -C $SB update-ref refs/remotes/origin/main 56610b3e8821613fb83affd4d5b20e43fdd2ea5c; <revpin>   # 0 pushed true
git -C $SB update-ref refs/remotes/origin/main refs/heads/main~1; <revpin>    # 2 branch_not_pushed
<restore 56610b3>; python3 -I -B -c "import importlib.util …spec_from_file_location('r17v','$SB/.ufo/waves/round-17/verify.py')…; m.LANE='$SB'; print(m.resolve_source())"   # 0 -> findings ["branch_not_pushed"]
python3 -I -B $L/.ufo/waves/round-18/tools/jj-red-before.py --root $L --cd-probe $L/.ufo/gates/citation-drift/citation-drift-probe.py --custody-pair $L/.ufo/gates/custody-pair/custody-pair.py --revpin $L/.ufo/waves/round-18/tools/revpin.py --jj /home/vgpnk/.local/bin/jj --out $D/receipt-at-rev.json   # 0; 14/14 held
python3 -I -B $L/.ufo/waves/round-18/tools/head-rev-lint.py --root $L --rev $REV --strict   # 0; live_count 0
git -C $L log --format=%H -- .ufo/waves/round-18/evidence/jj-red-before.json  # 0 -> eb6c266 only
git -C $L diff --stat eb6c266 $REV -- <4 tools + receipt>                     # 0; empty
```

## Residual risk and verification gaps
- [INFERENCE] Lane tools pin a revision for the Git objects they read, but they execute from the working tree. HEAD == tip proves nothing about the bytes of the tool that is running; L3 is an instance. verify.py snapshots digests at start and end (QUALITY #19) but never compares them with the blobs at `source`.
- Not exercised:
  - the helper's push-recovery and rebase path;
  - multi-workspace jj (writer worktrees, lane-addendum.md:100), where the root's HEAD can lag main and cause a false `head_not_branch_tip` [INFERENCE].
- I did not create `/tmp/jj-red-before-{receipt.json,stdout.json,stderr.txt}`, and I did not inspect them.
- Tools: nothing installed. I used the system git, curl and python3, plus the preinstalled jj 0.45.1. jj ran only inside jj-red-before's own `/tmp` clone of my origin-less clone.
