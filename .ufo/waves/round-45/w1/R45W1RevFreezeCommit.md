# R45 wave 1 — freeze-commit scope audit

Seat `R45W1RevFreezeCommit` (reviewer). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, parent `149133d47aa7e90796f96047afe6d251a3e65b2c`,
HEAD at run time `faa875bc0eb839d15b83c4afa6078819e5a7b381`. Run window 2026-10-28T15:36Z–15:43Z.
Host tools: `Python 3.14.8`, `git 2.56.0`. **No installs** (no pacman/uv/npx/cargo). Read-only on the lane
tree; every write went to `.ufo/waves/round-45/w1/R45W1RevFreezeCommit/`.

**Verdict.** The freeze commit's *scope* is clean: exactly 10 paths, every one inside the three declared
prefixes, none outside, no renames/copies, no `SKILL.md`. The r44 bulk-sweep defect did not recur.
The asked-for preflight call reports **red (exit 1)** and that red is **correct behaviour on the wrong
base** — a definitional artefact of freezing, *not* a legitimate touch. Separately, the audit found one
**high-impact defect** in the frozen counters' freeze arm that is invisible to the call in question.

> Frozen bytes were not modified. Blob shas now equal the freeze blob shas for all five frozen paths:
> ```
> plans/round-45-claims.md                  f93df4c3bd4069a0cd576d9649f1157609b6a5d5
> tools/round-45/frozen-path-preflight.py   b42398273da0449c01f6f26cc630853d58ea55ec
> tools/round-45/c1-counter.py              4ce400b29d6eba3cb03e242db8ba8bdf9d4fcfdd
> tools/round-45/c2-counter.py              7d83de6258cb624b1ebb0e18c326cf9fb5fd1aee
> tools/round-45/registry-scope.json        4855e97e497e329737f00076bdf686bf71b0827d
> ```
> `git -C L diff --stat f762b727 -- plans/round-45-claims.md tools/round-45/` → empty.

---

## 1. The full path list — ten paths, all declared

`git -C L diff-tree --no-commit-id --name-status -r f762b727…` (exit 0):

| # | status | path | declared prefix | frozen? |
|---|---|---|---|---|
| 1 | A | `.ufo/waves/round-45/controls/c1-selftest.txt` | `controls/*` | no (declared) |
| 2 | A | `.ufo/waves/round-45/controls/c2-selftest.txt` | `controls/*` | no (declared) |
| 3 | A | `.ufo/waves/round-45/controls/ctl-c1-0-base.json` | `controls/*` | no (declared) |
| 4 | A | `.ufo/waves/round-45/controls/ctl-c2-0-base-unevaluable.json` | `controls/*` | no (declared) |
| 5 | A | `.ufo/waves/round-45/controls/preflight-selftest.txt` | `controls/*` | no (declared) |
| 6 | A | `plans/round-45-claims.md` | `plans/round-45-claims.md` | **yes** |
| 7 | A | `tools/round-45/c1-counter.py` | `tools/round-45/` | **yes** |
| 8 | A | `tools/round-45/c2-counter.py` | `tools/round-45/` | **yes** |
| 9 | M | `tools/round-45/frozen-path-preflight.py` | `tools/round-45/` | **yes** |
| 10 | A | `tools/round-45/registry-scope.json` | `tools/round-45/` | **yes** |

- **Paths outside** `plans/round-45-claims.md`, `tools/round-45/*`, `.ufo/waves/round-45/controls/*`:
  **none.** The filter `grep -Ev '^(plans/round-45-claims\.md|tools/round-45/|\.ufo/waves/round-45/controls/)'`
  printed `(none)`.
- Total: **10** (`wc -l`). Declared tallies: 1 + 4 + 5 = 10. Exact match.
- With `-M -C` (rename/copy detection): the list is byte-identical — no `R`/`C` rows, so no path was
  moved to launder a change.
- Churn: **1148 insertions / 55 deletions**. The only deletions are in `frozen-path-preflight.py`
  (263+/55−), i.e. an in-place rewrite of the v1 single-arm gate the claims file describes — not a scatter.
- No `SKILL.md`, no `corpus/`, no `LOG.md`, no `SCORECARD.md` in the commit. That is required: the claims
  file names those as graded surface/record, explicitly *not* frozen.

**Against the r44 defect:** 432 paths → 10 paths (43× smaller). Zero paths outside three declared
prefixes. The bulk-sweep shape did not recur.

**Wording note for the landing (the L1 should not conflate two counts).** Of the ten paths *five* are
frozen paths (claims file + four tools) and *five* are control receipts the claims file declares
**not** frozen. "The freeze commit touched ten paths" and "the freeze covers five paths" are both true
and are different statements; the counters encode the second (`FROZEN = [CLAIMS, "tools/round-45"]`,
`c1-counter.py:32`, `c2-counter.py:30`).

## 2. Author and committer identities and timestamps

`git -C L show --no-patch --format=fuller` and `git -C L cat-file -p`:

| field | value |
|---|---|
| author | `kaidoku-shokunin <kaidoku@shokunin.local>` |
| authored | epoch `1793200735`, `2026-10-28T12:18:55-03:00` |
| committer | `kaidoku-shokunin <kaidoku@shokunin.local>` |
| committed | epoch `1793201240`, `2026-10-28T12:27:20-03:00` |
| delta | **505 s** (author date 8 m 25 s before commit date) |
| parent | `149133d4…` — single parent, not a merge |
| tree | `2a3a24c0821d2543ff0474a411402651fce29d5f` |
| object | 353 bytes, unsigned (no `gpgsig`) |
| trailer | `change-id tpuwpsluyrmsyonlyvpoyotwwswpmmnq` (jj-managed) |

Reading: author and committer are the *same* identity, so there is no human-vs-agent mismatch to flag.
The 505 s gap plus the `change-id` trailer is the jj shape — the change was created at 12:18:55 and
finished/committed at 12:27:20. Committer time is monotonic against the parent (`11:54:42`), so the
freeze is not back-dated.

## 3. `git status --porcelain` at run time — **not empty**

Two samples:

```
15:36Z  ?? .ufo/waves/round-45/w1.ready.dispatched                       (1 line)
15:41:34Z                                                               (14 lines)
?? .ufo/waves/round-45/l1/preflight-c86ea508.json
?? .ufo/waves/round-45/l1/preflight-round45-frozen.json
?? .ufo/waves/round-45/w1.ready.dispatched
?? .ufo/waves/round-45/w1/R45W1C1CounterMutants/  … +11 more seat dirs
```
stdout sha256 of the 14-line snapshot: `0a61c34f8401bdad0000982bec2115e318498335d385af2d3380e68aff6a4d91`.

- **Tracked modifications: none.** `git status --porcelain --untracked-files=no` → empty.
- **Entries under a frozen path: none.** `git status --porcelain -z -- plans/round-45-claims.md tools/round-45/`
  → empty.
- Every entry is an **untracked wave-harness artefact** under `.ufo/waves/round-45/` (the dispatcher's
  `w1.ready.dispatched` marker and sibling seats' report dirs), created after the freeze.

Honest phrasing for the landing: *the worktree is not clean in the git sense and is clean in the frozen
sense.* Neither "clean worktree" nor "dirty worktree ⇒ freeze suspect" is supportable. Consequence for
the instrument: the preflight's dirty arm defaults its scope to the pathspec
(`dirty_pathspecs or pathspecs`, `frozen-path-preflight.py`), so `--check-dirty` on this tree reports
`dirty: []`, verdict `clean`, exit 0 (receipt A4/A5) — the harness noise is *deliberately* out of the
dirty arm's scope, which is the right call but must be stated when citing the arm.

## 4. What the frozen preflight reports for the asked-for call

Exact command, frozen interpreter extracted from the freeze (`sha256 633ebc05…23 0523b`, byte-identical
to the worktree copy), run with `TMPDIR` inside my scratch:

```
python3 -I -B $S/preflight-frozen.py --root L \
  --freeze 149133d4… --rev f762b727… \
  --pathspec tools/round-45/ --freeze-path tools/round-45 --require-pathspec
```

**exit 1**, stdout sha256 `1eb88defda6d28c4e93ce62f9f580eecbebbba80f6ec576e9755b0a5b8f72043`:

```json
{"blob_changed": ["tools/round-45", "tools/round-45/frozen-path-preflight.py"],
 "dirty": [], "restored": [],
 "freeze": "149133d47aa7e90796f96047afe6d251a3e65b2c",
 "rev": "f762b7273e3f6ca3c710bb37d5de92a4a4417aec",
 "touched": [{"status":"A","path":"tools/round-45/c1-counter.py","commit":"f762b727…"},
             {"status":"A","path":"tools/round-45/c2-counter.py","commit":"f762b727…"},
             {"status":"M","path":"tools/round-45/frozen-path-preflight.py","commit":"f762b727…"},
             {"status":"A","path":"tools/round-45/registry-scope.json","commit":"f762b727…"}],
 "verdict": "frozen_path_changed"}
```

`--require-pathspec` did **not** fire: the parent tree has `tools/round-45` as a tree
(`git ls-tree -r f762b727^ -- tools/round-45` → `tools/round-45/frozen-path-preflight.py` only), and
`covers(["tools/round-45/"], "tools/round-45")` is true. So the r44 defect arm ("directory freeze with
no pathspec") is exercised here and passes.

### Legitimate touch or artefact of freezing? — **Artefact of the base choice.**

1. `FREEZE..REV` is **half-open**. The freeze is *by definition* the commit that first contains the
   frozen bytes, so with `--freeze f762b727 --rev f762b727` the range is empty and the gate is clean:
   **exit 0**, sha256 `716adc69808df60f978ce11e1893219cc0f920e132ddf82a1a8b443fc7d19959` (A3) — the same
   verdict as the committed `controls/preflight-at-freeze.json` (`freeze == rev == f762b727`, `clean`).
2. With `--freeze <parent>` the range contains the very commit that creates/modifies those bytes, so
   **every** frozen path must appear. Widening the call to both declared frozen pathspecs reports
   **exactly the five frozen paths** (A2: `plans/round-45-claims.md` + the four tools). The result is
   forced; it carries no information about whether the freeze was later violated.
3. **Scoring consequence — the parent base is inadmissible forever.** Under it no landing could ever be
   admitted: the preflight would sit at exit 1 and both counters at exit 2 for all time (B3/B4). A scorer
   that substituted the claims file's published `Base 149133d4…` for `FREEZE` would therefore misread a
   perfectly clean landing as `frozen_path_changed`.
4. **It is nevertheless a real detection on real bytes** — and that is the useful half. The four tool
   paths are genuinely added/modified relative to the parent, and `frozen-path-preflight.py` is a genuine
   263+/55− rewrite of the v1 single-arm gate. So the log arm, the blob arm, and `--require-pathspec` all
   fire on real history, not only on selftest fixtures. That is positive evidence for the table's `arm`
   column.

**Is the parent-base trap live?** Mild. The claims file's header publishes `Base 149133d4…` prominently,
which is exactly the tempting wrong value; but its counting command uses the placeholder
`--freeze <FREEZE>` and it publishes the re-derivation, which I ran and which is exact:
`git -C L log --format=%H -1 -- plans/round-45-claims.md` → `f762b727…` (and no later commit touches that
file). So the derivation is unambiguous; the risk is a seat ignoring it, not an ambiguity in the text.
**Recommendation for the landing text:** state in the table's header row that `FREEZE = f762b727…` (the
freeze commit), that `Base 149133d4…` is the pre-freeze parent and is *never* a `--freeze` argument, and
that a parent-based call is expected to run red.

---

## 5. Findings by severity

### F1 — HIGH: both frozen counters' freeze arm is blind to a frozen path written by a merge commit's own resolution

`frozen_path_changed()` in both counters is
`git log --name-only --format= <freeze>..<rev> -- <FROZEN>` (`c1-counter.py:52-56`, `c2-counter.py:63-67`).
`git log --name-only` prints **no diff for a merge commit**, so an edit made by the merge itself — a
hand resolution — is invisible. The preflight does not share the hole: it passes
`-m --diff-merges=first-parent` *and* keeps a blob arm.

Reproducible probe, `fixtures/evil_merge_probe.sh`, transcript `receipts/F1_evil_merge_probe.txt`
(utc `2026-10-28T15:42:34Z`, sha256 `466b3cbc6ce85798c6a0ae62da65dcb3fd9a9fe7ea09276f3bbe8c2941cc2340`).
Fixture: freeze → side branch edits `a.txt`, trunk edits `b.txt`, merge, then the **merge commit itself**
writes `frozen/target.txt` (a path neither parent touched):

```
frozen/target.txt at freeze = 'v0'   blob=13ceda207b642cbbbdc409ae0bc8eefd1c2bd573
frozen/target.txt at HEAD   = 'EVIL' blob=b2f3ae2a7251310b2009633215d8413cd294f682
arm 1 preflight  -> verdict frozen_path_changed, touched [frozen/target.txt]  PREFLIGHT_EXIT=1   (correct)
arm 2 c1-counter -> []      (blind)
arm 2 c2-counter -> []      (blind)
log --name-only (counter form):            (nothing)
log -m --diff-merges=first-parent:         frozen/target.txt
```

Blast radius: with `frozen_path_changed == []` the counters proceed to score and can print `met_target`
on tampered frozen bytes. The claims file's rule — *"A score at REV is admissible only if no commit in
FREEZE..REV touches a frozen path … the counter's arm reads commit history"* — is therefore broader than
what the counters implement.

**Not hypothetical in this lane.** The lane's own history contains **2 merges** (454 commits,
`git rev-list --merges HEAD`), and *both* performed their own resolution edits that the counter form
cannot see:

```
7256d1da 2026-10-18  "merge origin/main: … union resolution keeps both sides"  first-parent: M LOG.md M README.md
a46b1e70 2026-10-17  "Merge pull request #2 from VeigaPunk/devin/wiki-link"    first-parent: M LOG.md M README.md
git log -1 --name-only 7256d1da  -> (empty)      # exactly the counter's form
```

Neither touched a frozen path, so no past round's freeze was actually compromised — but the merge workflow
(including a *union resolution*) is live in this repo, and the counters are the instruments that certify
admissibility.

Calibration: **impact high** (false admissibility certificate) × **current likelihood low** (0 merges in
`freeze..HEAD`; both real merges predate round 45 and touched no frozen path). Fix cannot land this round
— `c1-counter.py`/`c2-counter.py` are frozen, so editing them makes every counter exit 2 by its own rule.
**Hand-off:** (a) the C1 table must not claim the counter arm covers merge resolutions — its row should
say *path presence over linear history*; (b) carry a round-46 item adding `-m --diff-merges=first-parent`
(and ideally the tip-blob comparison the preflight already has) to `frozen_path_changed` in both counters.

### F2 — MEDIUM: the named preflight invocation under-covers the freeze by one path

`--pathspec tools/round-45/ --freeze-path tools/round-45` guards the directory only. The claims file
declares **two** frozen paths; `plans/round-45-claims.md` is outside that pathspec, so the gate cannot
see it. Same base, wider pathspecs:

| receipt | pathspecs | exit | `touched` count |
|---|---|---|---|
| A1 | `tools/round-45/` | 1 | **4** |
| A2 | `tools/round-45/` + `plans/round-45-claims.md` | 1 | **5** |

The missing one is `plans/round-45-claims.md` (A2 touched adds `A plans/round-45-claims.md`; blob_changed
adds it too). A receipt that cites A1 as "the freeze gate" certifies four of five frozen paths.
**Recommendation:** the table row that documents the gate's invocation must name both pathspecs (and both
`--freeze-path` values), or the gate is one path short of its own freeze.

### F3 — LOW: the same condition yields exit 1 in the gate and exit 2 in the counters

Identical range, identical condition (frozen path touched):

| instrument | exit | verdict/reason |
|---|---|---|
| preflight (A1/A2) | **1** | `verdict: frozen_path_changed` |
| c1-counter (B3) | **2** | `verdict: could_not_evaluate`, `reason: frozen_path_changed` |
| c2-counter (B4) | **2** | same |

Both are defensible under the contract (a gate's "violation" is 1; a scorer's "cannot score" is 2), and
both receipts carry `frozen_path_changed` in the reason. But the C1 table's `exit` column will teach one
code per trigger, and "frozen path touched" is *two* codes depending on the instrument. Recommendation:
split the trigger into two rows (gate vs counter) or annotate the cell.

### F4 — LOW: `blob_changed` names **tree** objects, not blobs, and duplicates the file rows

`blob_changed` here contains `"tools/round-45"` — the parent's tree oid for the directory, obtained by
`rev-parse <rev>:<dir>`. A tree oid changes whenever any descendant changes, so for a directory freeze the
entry is a redundant restatement of the per-file rows. It is not a false positive (a tree oid only moves
when content moves) and it is genuine defence-in-depth — it is the arm that still fires when the log arm
is fooled (F1) — so it should be **documented, not removed**. Recommendation: the table's `arm` column
should describe it as "frozen subtree oid", not "blob", or a reader will take `blob_changed: ["tools/round-45"]`
for a per-file claim.

### F5 — INFO: `cases >= 11` (clause 6) is the *preflight's* 11, not the c1 counter's 9

R45-C1 clause 6 requires the interpreter's `--selftest` to report `cases >= 11, failures == 0`. Measured:

| instrument | selftest | cases | failures | exit |
|---|---|---|---|---|
| `frozen-path-preflight.py` (frozen extract) | `PREFLIGHT_SELFTEST` | **11** | 0 | 0 |
| `c1-counter.py` | `C1_SELFTEST` | 9 | 0 | 0 |
| `c2-counter.py` | `C2_SELFTEST` | 7 | 0 | 0 |

Clause 6 is satisfied by the preflight, and its seven named red cases are all present
(`red-touched`, `red-restored`, `red-dirty`, `red-dirfreeze-no-pathspec`, `red-unknown-freeze`,
`red-nonancestor`, `red-bulk-sweep` = 7 red + 4 green = 11). The wiring is real: `c1-counter.py:106-112`
runs `--selftest` from the bytes at `--rev` and requires `cases >= 11 and failures == 0`. Flagged only
because a seat that reads "the interpreter" as *the c1 counter* sees 9 < 11 and would wrongly fail the
claim. Recommendation: the landing text should name `frozen-path-preflight.py` explicitly in the clause-6
evidence line.

---

## 6. Verified positives (independently reproduced, receipts below)

- **Scope is clean** — 10/10 declared, 0 outside, no `R`/`C` rows (§1).
- **Freeze is re-derivable exactly as the claims file says** — `git log --format=%H -1 -- plans/round-45-claims.md`
  → `f762b727…`.
- **Frozen bytes intact now** — 5 blob shas equal to the freeze, `git diff f762b727 -- …` empty.
- **Landing range admissible at HEAD** — `freeze..HEAD` clean under the single pathspec (A4) and under
  both pathspecs with `--check-dirty` (A5): exit 0, `touched/blob_changed/restored/dirty` all `[]`, and
  `git log f762b727..HEAD -- plans/round-45-claims.md tools/round-45/` is empty. The five post-freeze
  commits (`9ff920cd`, `e715263c`, `1f4b27f8`, `abfeda50`, `faa875bc`) touched zero frozen paths.
- **Do-nothing before-receipts are genuine** — re-running the frozen counters at `--freeze f762b727
  --rev f762b727` reproduces `controls/ctl-c1-0-do-nothing.json` and `controls/ctl-c2-0-do-nothing.json`
  **dict-identical** (exit 1 each; c1 `failing` has the same five entries, c2 `unregistered` the same six
  paths, `scope_size 6`, `registry_rows 39`). This is the strongest available control-integrity proof,
  since no hash pin exists (see §7).
- **All three selftests reproduce byte-identically** to the committed receipts
  (`controls/{preflight,c1,c2}-selftest.txt`).
- **Determinism** — every receipt's stdout sha256 matched across two independent runs (15:36Z batch and
  15:41Z batch), so the hashes in this report are stable identifiers.
- **The r44 sweep shape is caught on real history** — the L1's own `controls`-adjacent receipt
  `l1/preflight-c86ea508.json` shows `c86ea508` touching eight `tools/round-44/control-fixtures/…` files
  → `verdict: frozen_path_changed`; the same shape is red in the selftest (`red-bulk-sweep`).

## 7. Residual risk and verification gaps

1. **F1 is unarmed and cannot be armed this round** (frozen bytes). Until then, admissibility rests on the
   preflight, not on the counters, whenever the range can contain a merge.
2. **The control receipts are neither frozen nor hashed.** The freeze commit adds five of them and
   `9ff920cd` adds `ctl-c1-0-do-nothing.json` / `ctl-c2-0-do-nothing.json` *after* the freeze — as the
   claims file allows. Consequently no gate can detect a rewritten before-receipt; the only integrity
   proof is re-derivation, which I performed and which is clean. Recommendation: the landing must cite the
   reproduction command (not just the file) as the control's evidence, because the claims file cannot be
   amended to pin a hash.
3. **Not run / not tested (stated, not passed):** the c1/c2 counters against the real landing revisions
   (sibling seats own that); `git fsck`; any `SKILL.md` content check (C2 predicate); octopus (>2-parent)
   merges; a freeze whose frozen directory is *deleted* at `REV`; and any pre-`f762b727` round's freeze
   semantics.
4. **Cross-instrument path sets differ by construction** — the counters always check
   `[plans/round-45-claims.md, tools/round-45]`; the preflight checks only what it is given (F2). Numbers
   from the two are not interchangeable.

## 8. Receipts

`receipts.tsv` (utc · exit · stdout sha256 · tag), `commands.sh` (exact command lines), `receipts/`
(raw stdout + json per call), `fixtures/evil_merge_probe.sh` (F1 probe, re-runnable).

| tag | utc | exit | stdout sha256 |
|---|---|---|---|
| A1 parent→freeze, `tools/round-45/` | 15:41:59Z | 1 | `1eb88def…b8f72043` |
| A2 parent→freeze, both pathspecs | 15:41:59Z | 1 | `1a1c0f2a…c271fc2d` |
| A3 freeze→freeze (canonical) | 15:41:59Z | 0 | `716adc69…c7d19959` |
| A4 freeze→HEAD, `--check-dirty` | 15:41:59Z | 0 | `aa8c6163…8a2d15396` |
| A5 freeze→HEAD, both pathspecs, `--check-dirty` | 15:42:00Z | 0 | `4b5a685d…1c69c6b20c658` |
| B1 c1 do-nothing (freeze..freeze) | 15:42:00Z | 1 | `e2731609…f41fb4e1` |
| B2 c2 do-nothing (freeze..freeze) | 15:42:00Z | 1 | `d6e202aa…db9216dd0` |
| B3 c1 parent-base | 15:42:00Z | 2 | `116ee9e8…cb904c25` |
| B4 c2 parent-base | 15:42:00Z | 2 | `77d1aec0…7a28a0b968` |
| C1 preflight `--selftest` | 15:42:00Z | 0 | `9f03df65…389ec06c` |
| C2 c1 `--selftest` | 15:42:00Z | 0 | `296734f2…3754fdac6d` |
| C3 c2 `--selftest` | 15:42:01Z | 0 | `aea7e363…70b40b0f2d` |
| F1 evil-merge probe | 15:42:34Z | 0 (probe harness) | `466b3cbc…941cc2340` |

Scope/identity/status commands and their outputs are quoted inline in §1–§3; their exact lines are in
`commands.sh`. Scratch (`/fast/scratch/hyaku/kaidoku-r45/R45W1RevFreezeCommit`) was removed after these
receipts were copied here.

## 9. Statement of the answered questions

1. **Full path list:** ten paths, enumerated in §1 — exactly the declared set.
2. **Paths outside the three declared prefixes:** none.
3. **Author/committer:** same identity `kaidoku-shokunin <kaidoku@shokunin.local>`; authored
   `2026-10-28T12:18:55-03:00`, committed `2026-10-28T12:27:20-03:00` (Δ 505 s), unsigned, jj `change-id`.
4. **`status --porcelain` empty?** No — one untracked harness artefact at first sample, fourteen at the
   later sample; zero tracked modifications and zero entries under a frozen path.
5. **Preflight on `--freeze <parent> --rev f762b727 … --require-pathspec`:** **exit 1,
   `frozen_path_changed`**, 4 touched paths (5 with both declared pathspecs) — an **artefact of the
   parent base**, not a legitimate touch: the gate is clean (exit 0) with `FREEZE = f762b727`, which is
   the only admissible base; the red nevertheless proves the arms fire on real bytes.
