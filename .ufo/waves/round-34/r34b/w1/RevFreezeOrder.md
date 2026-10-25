# RevFreezeOrder — freeze-order audit, R34-C2 pre-freeze shortcut-replay gate (round 34, run-6 re-dispatch, wave 1)

| Field | Value |
|---|---|
| Seat | `L1Kaidoku34-2.RevFreezeOrder` (reviewer, Godspeed, leaf — no subagent dispatch) |
| Lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (jj-colocated; read-only for this seat) |
| Scratch | `/fast/scratch/hyaku/kaidoku-r34b/w1/RevFreezeOrder/` (`base/` = `git archive ec3125ad`, `freeze/` = `git archive c79bbe7b`, `before-repro.json`, `after-repro.json`) |
| Freeze commit | `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, committer `2026-10-25T04:13:11-03:00` = **07:13:11Z**, parent `f432c8e3` |
| Local clock | `-0300`; all UTC values below = local + 3 h. Session clock: `date -u` → `2026-10-25T07:18:17Z` (first probe), `07:26:10Z` (last probe) |
| Audit window | Lane tip observed at `c79bbe7b` (07:18Z), moved to `b917ea64` (07:22:31Z) then `cd75b92e` (07:23:47Z) while this seat ran — see §7 |
| Tooling installed | **none** (no `uv`/`npx`/binary install; nothing needed) |

Scope: prove or refute (a) instruments+claims landed at `c79bbe7b`, (b) the before receipt is `finding=gate_absent` at the base revision, (c) the production receipt and the five control receipts are dated after the freeze commit, (d) no receipt predates the freeze — and name anything that cannot be ordered.

Evidence classes used: committed bytes (`git cat-file`, `git log --diff-filter=A`, `git ls-tree`), committer times, **loose-object birth times** (`.git/objects/**` `stat %w`), **filesystem birth/ctime/mtime** of every receipt (`stat -c '%w %y %z'`), the git reflog, the jj operation log (read-only: `jj --ignore-working-copy op log`), SHA-256 pin recomputation, and two independent counter runs in scratch.

---

## 1. Ordering table (all times UTC)

| UTC | Artifact | Evidence |
|---|---|---|
| 07:04:34.515 | `.ufo/waves/round-34/r34b/census-start.txt` born | `stat %w` |
| 07:07:01.173 | `mini-fix/build.py` born | `stat %w` |
| 07:08:35.905 | `mini-fix/spec.json` born | `stat %w` |
| 07:09:15.429 | `gate-config-mini.json`, `gate-config-naive.json` born | `stat %w` |
| 07:09:52.057 | `replay-gate.py` born | `stat %w` |
| 07:11:41.209 | `c2-shortcut-gate-counter.py` last write (born 07:09:28.739) | `stat %w/%y/%z` |
| 07:11:52 | `claims.json` `declared_at_utc` field | file content |
| 07:13:04.835 | `claims.json` born | `stat %w` |
| 07:13:11.224 | **commit object `bbf29491`** written (loose) | `.git/objects/bb/f29491…` `%w` |
| 07:13:11.341 | **commit object `2e16ab53`** written (loose) | `.git/objects/2e/16ab53…` `%w` |
| **07:13:11.435** | **commit object `c79bbe7b` (the freeze) written**; committer time `04:13:11-03:00` | `.git/objects/c7/9bbe7b…` `%w`; `git show --format=%cI`; reflog `HEAD@{2026-10-25 04:13:11 -0300}: export from jj` |
| 07:13:11.806 | jj `point bookmark main to commit c79bbe7b` | jj op log |
| 07:13:11.928 | jj `push bookmark main to git remote origin` | jj op log |
| 07:13:21.916 | `before/c2-at-base.txt` born (mtime/ctime .958) | `stat %w` |
| 07:13:21.964 | `after/c2-at-instruments.txt` born | `stat %w` |
| 07:13:24.882/.883 | `after/c2-at-instruments.json` born/written | `stat %w/%y` |
| 07:13:43.995–44.007 | `controls/gates/` + four mutant gate sources written | `stat %w/%y` |
| 07:13:46.840 | `controls/gate-always-clean.py.{json,txt}` | `stat` |
| 07:13:49.487 | `controls/gate-no-positive-check.py.{json,txt}` | `stat` |
| 07:13:52.344 | `controls/gate-vacuous-no-floor.py.{json,txt}` | `stat` |
| 07:13:52.449 | `controls/gate-junk-clean.py.{json,txt}` | `stat` |
| 07:13:52.481 | `controls/do-nothing.{json,txt}` | `stat` |
| 07:22:31 / .312 | landing commit `b917ea64` (committer time / loose-object birth) — first commit containing any receipt | `git log`, `stat` |
| 07:23:47 | stop commit `cd75b92e` (outside this audit's scope, see §7) | `git log` |

Derived: earliest receipt is **10.481 s after** the freeze object was written (`07:13:21.916 − 07:13:11.435`). The freeze was pushed to `origin` **10 ms** before the before-receipt file was created, and **9.988 s** before it.

---

## 2. (a) Instruments and claims landed at `c79bbe7b` — CONFIRMED

```
git -C <lane> show --stat --format='%H%ncI=%cI%naI=%aI%nPARENT=%P' c79bbe7b
```
→ exit 0; `PARENT=f432c8e3…`; `cI=aI=2026-10-25T04:13:11-03:00` (author time == committer time, i.e. no re-commit/amend ordering artifact visible); **27 files changed, 1345 insertions, 0 deletions** — `claims.json`, `replay-gate.py`, `c2-shortcut-gate-counter.py`, both gate configs, and the 22-file `mini-fix/` tree (build.py, expected.json, spec.json, mini-counter.py, naive-counter.py, 8 fixtures, 9 readers).

Per-path first-add test (`git log --diff-filter=A --format=%H -n1 -- <path>`) over the **26 pinned paths + `claims.json`**:

```
TOTAL=27 NOT_FIRST_ADDED_AT_FREEZE=0
```

Every pinned path first appears in `c79bbe7b`; none exists in `f432c8e3` or earlier. Instrument births (§1) are all ≤ 07:11:41.209Z, i.e. **before** the commit object at 07:13:11.435Z; `ctime == mtime == birth` on every instrument except the counter (born 07:09:28.739, single later write 07:11:41.209), so no instrument byte was rewritten after 07:11:41Z.

Pin integrity (`python3` — recompute SHA-256 of each pinned path in the worktree, and of the blob at `c79bbe7b:<path>`):

```
PINS_TOTAL=26 PINS_MISMATCH=0     (worktree == pin == blob@c79bbe7b, all three)
```

Rechecked after the lane moved to the stop tip: `pins=26 mismatch=0`. `git diff --stat c79bbe7b cd75b92e -- tools/round-34 .ufo/waves/round-34/r34b/claims.json` → **empty**: no post-freeze commit amended a frozen instrument or `claims.json` (`claims.json` sha256 `de3afbfb61d70fee177392b256719bb665ad07d999303999381442120facd828`, identical at `c79bbe7b`, `b917ea64`, `cd75b92e`, and worktree).

Fixture/reader shape at the freeze (`git ls-tree -r c79bbe7b -- …/mini-fix/{fixtures,readers}`): 8 fixtures, all `100644`, one of size 512 (`git cat-file -s`) — static bytes, never executable, never run. 9 readers, all `100755`, run as python by the counter only.

## 3. (b) Before receipt `finding=gate_absent` at the base revision — CONFIRMED, with a binding caveat

Committed bytes:
```
before/c2-at-base.txt:
GATE_COUNTER_UNEVALUABLE finding=gate_absent measured_revision=ec3125ad3d130d92f888a4128dfaa2982f36fff7 gate_path=tools/round-34/replay-gate.py
```
`claims.json` declares `"base_revision": "ec3125ad…"` and `"inherited_tip": "f432c8e3…"`; `ec3125ad` is the round-33 verifier spot-check commit, i.e. the last commit before round-34's first commit `8897a67f`, so "base" here means *round base*, not the freeze parent.

Independent re-derivation (no lane mutation; `git archive` only):
```
git -C <lane> archive ec3125ad | tar -x -C $SCRATCH/base      # base/tools/round-34/replay-gate.py: ABSENT
git -C <lane> archive c79bbe7b | tar -x -C $SCRATCH/freeze    # freeze/tools/round-34/replay-gate.py: PRESENT
/usr/bin/python3 -I -B $SCRATCH/counter-from-freeze.py --root $SCRATCH/base \
    --rev ec3125ad3d130d92f888a4128dfaa2982f36fff7 --json-out $SCRATCH/before-repro.json
```
→ 07:23:14Z, **exit 2**, stdout **byte-identical** to the committed line, JSON fields `finding=gate_absent`, `gate_present=false`, `met_target=false`, `exit=2`.

Gate presence at each candidate revision (`git cat-file -e <rev>:tools/round-34/replay-gate.py`):

| revision | gate |
|---|---|
| `ec3125ad` (declared base) | ABSENT |
| `f432c8e3` (freeze parent) | ABSENT |
| `c79bbe7b` (freeze) | PRESENT |

So `gate_absent` holds at both the declared base **and** the immediate pre-freeze parent. It is receipted only at `ec3125ad`.

Caveat, and this is a finding (§6 F2): the counter does **not** measure the revision it names. `c2-shortcut-gate-counter.py:73` does `"measured_revision": args.rev` (echo of argv) and `:74` does `"gate_present": (root / args.gate).is_file()` (a filesystem test on `--root`); the receipt records no `root`. The identical output is produced by any tree lacking that path and, as `controls/do-nothing` shows, by simply naming a nonexistent gate (`absent-gate.py`) at the freeze revision. The before receipt is therefore a *self-assertion*, and my §3 reproduction — not the receipt — is what establishes the base fact.

## 4. (c) Production receipt and five control receipts dated after the freeze — CONFIRMED

Six JSON/txt pairs (`after/c2-at-instruments`, `controls/do-nothing`, `controls/gate-{always-clean,junk-clean,no-positive-check,vacuous-no-floor}.py`). Every one has `birth ≥ 07:13:21.916Z`, i.e. **after** `07:13:11.435Z`; the latest is 07:13:52.481Z (+41 s). No receipt file has `ctime > mtime` beyond the redirect-truncate pattern (`txt` born when the process starts, rewritten when it finishes; `json` written at the end) — no receipt was edited after its run.

Cross-file consistency (`python3` over all 6 pairs): `RECEIPTS=6`, `all txt/json exit agree: True` (`OK`↔0, `MISS`↔1, `UNEVALUABLE`↔2), `all predicates identical: True`.

| receipt | exit | finding | gate_path |
|---|---|---|---|
| `after/c2-at-instruments` | 0 | `shortcut_gate_discriminates` | `tools/round-34/replay-gate.py` |
| `controls/do-nothing` | 2 | `gate_absent` | `tools/round-34/absent-gate.py` |
| `controls/gate-always-clean.py` | 1 | `shortcut_gate_miss` (`red_refused,selftest_clean`) | `…/controls/gates/gate-always-clean.py` |
| `controls/gate-junk-clean.py` | 1 | `shortcut_gate_miss` (`red_refused`) | `…/controls/gates/gate-junk-clean.py` |
| `controls/gate-no-positive-check.py` | 1 | `shortcut_gate_miss` (`mutants_killed,selftest_clean`) | `…/controls/gates/gate-no-positive-check.py` |
| `controls/gate-vacuous-no-floor.py` | 1 | `shortcut_gate_miss` (`selftest_clean`) | `…/controls/gates/gate-vacuous-no-floor.py` |

Independent reproduction of the production receipt at the freeze revision (scratch copy of `c79bbe7b`, bounded probe; the counter runs the gate selftest, one red and one green config, readers executed as python by the counter):
```
/usr/bin/python3 -I -B freeze/tools/round-34/c2-shortcut-gate-counter.py \
    --root $SCRATCH/freeze --rev c79bbe7b… --json-out $SCRATCH/after-repro.json
```
→ 07:23:36–37Z, **exit 0**, `real 0m2.702s`, line byte-identical to the committed `after/c2-at-instruments.txt`: `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`. All six clauses true; red `classes_over_target=["label-memorization"]`; green `shortcuts_below_target=7`; selftest 12 cases, 0 failures, 3/3 mutants killed. Identical on every field the committed receipt records.

Batch observation: the before receipt file was born 48 ms before the production receipt's stdout file (07:13:21.916 vs .964). The "before" measurement is not a temporally prior event to production — it is a measurement of a *different revision* issued in the same batch, both after the freeze. That is materially different from a pre-freeze run, and it is what the ordering actually shows.

## 5. (d) No receipt predates the freeze — CONFIRMED for claim receipts; one pre-freeze census exists

- All 6 claim receipts: earliest 07:13:21.916Z, +10.48 s after the freeze object.
- The 4 mutant gate sources in `controls/gates/`: 07:13:44.007Z, also after.
- VCS record: no commit before `c79bbe7b` contains any `r34b/{before,after,controls}` path (`git log --all --format='%h %cI %s' -- .ufo/waves/round-34/r34b` → `c79bbe7b`, `2e16ab53`, `bbf29491` only, and those three add `claims.json` alone); the receipts entered history at `b917ea64` (07:22:31Z), whose parent is the freeze.
- **Exception**: `r34b/census-start.txt`, born **07:04:34.515Z**, predates the freeze by **8 m 37 s**. It is a corpus/`SOURCES.md` duplicate-URL census (`kaidoku W04 S033…S102 duplicate url …`, `kaidoku ok …/corpus/SOURCES.md`), not a claim receipt: it names no instrument, no receipt, and no R34-C2 token. §6 F5.

## 6. Findings by severity

**F1 — Medium — the frozen `predicate_identity` assertion is false.** `claims.json` says: *"The same sentence is the gate config's `predicate` field, the C2 counter's PREDICATE constant and the receipt label."* The gate configs and `claims.json` carry one sentence (**237 chars**); the counter constant and therefore **all six receipts** carry a different one (**351 chars**):

- `claims.json` `claims[0].predicate` == `gate-config-mini.json.predicate` == `gate-config-naive.json.predicate` → `True` (programmatic compare). Begins `P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered structure-blind shortcut readers are scored under the counter's own predicate and none meets the target, while a registered structural reader does.`
- `c2-shortcut-gate-counter.py:23-32` `PREDICATE` == that sentence → `False`. Begins `P34-shortcut-replay: the committed replay gate refuses the shape-only counter whose label-keyed memorization meets its target, …`
- Therefore every receipt binds a predicate the frozen claim does not state, and the stated identity does not hold. `mini-fix/spec.json` carries no `predicate` field, so it is not a fourth site. The later commit `b917ea64` says *"predicate reconciliation"* in its subject, but `claims.json` and the counter are byte-unchanged through `cd75b92e` (§2), so no byte-level reconciliation landed; whatever reconciliation exists is report prose. This does not affect the gate's discriminating power (my §4 run passes all six clauses) nor any ordering claim.

**F2 — Medium — the before receipt is unbound to any tree.** `measured_revision` is an argv echo and `gate_present` is a `Path.is_file()` test on `--root`; no `root`, no `git rev-parse`, no tree/blob hash is recorded. A receipt saying `finding=gate_absent measured_revision=ec3125ad` is therefore unverifiable from its own bytes, and is indistinguishable in form from the `do-nothing` control (which passes a nonexistent gate path at the *freeze* revision). The base fact survives only because I re-derived it in scratch (§3) and because `git cat-file` shows the gate absent at `ec3125ad` and `f432c8e3`. Recommendation for the record: the before receipt should be restated as *"gate absent in the tree exported from `ec3125ad`; independently reproduced at 07:23:14Z, exit 2"*, or the counter given a `--root` field plus a rev/tree check.

**F3 — Low — the before receipt names the round base, not the freeze parent, and no receipt measures `f432c8e3`.** Both revisions lack the gate, so `gate_absent` is true at either; but the receipt that is supposed to evidence "no gate before the freeze" measures `ec3125ad` (round-33 spot-check), 6 commits before the freeze. `claims.json` makes this explicit (`base_revision` vs `inherited_tip`), so it is a naming/scope gap, not a false statement.

**F4 — Low — three commit objects exist inside the freeze second, and commit metadata cannot order them.** `git cat-file`:

| object | tree | change-id | message | files vs `f432c8e3` |
|---|---|---|---|---|
| `bbf29491` | `680a87cb` | **absent** (git-native, not a jj export) | empty | 5 (claims.json + gate + counter + 2 configs; **no `mini-fix/`**) |
| `2e16ab53` | `394b6aae` | `znxrzz…` | empty | 27 |
| `c79bbe7b` | `394b6aae` | `znxrzz…` | the freeze message | 27 |

All three carry committer time `1792912391 -0300` (1-second granularity → indistinguishable in metadata). Loose-object births order them: **07:13:11.224 → .341 → .435**, and the jj op log places `snapshot working copy` at 11.223 and `track paths` at 11.293 between the first two, `commit 2e16ab53` at 11.433, `point bookmark main → c79bbe7b` at 11.806, `push origin` at 11.928. `bbf29491`'s `claims.json` is byte-identical to the final one and pins the 22 `mini-fix/` files that its own tree does not contain. *[INFERENCE]* `bbf29491` is the pre-tracking snapshot taken before `mini-fix/` was added to git's tracked set; `2e16ab53` is the same tree committed with an empty message, superseded by `c79bbe7b` with the freeze message. Nothing in the receipts depends on those two objects, and no receipt exists at that instant, so this does not violate the ordering — but it is the one part of the freeze that committed metadata alone cannot order, and it must be cited as such rather than presented as a single atomic commit.

**F5 — Info — `census-start.txt` predates the freeze.** The literal statement "no receipt predates the freeze" is false unless qualified to *claim receipts*: the census at 07:04:34.5Z precedes the freeze by 8 m 37 s. Its content is a source-duplication census, not an instrument measurement, and it is consistent with the lane's order (census → build instruments 07:07–07:11 → write claims 07:13:04 → freeze 07:13:11 → receipts).

**F6 — Info — receipts carry no self-timestamp.** No receipt JSON has a `measured_at`/`run_at` field. Ordering rests entirely on filesystem birth/ctime (not settable by an unprivileged process without clock control), on `ctime == mtime` for every receipt (single write, no later edit), on the reflog, and on the first commit containing them (`b917ea64`, 07:22:31Z, object birth .312). These four independent sources agree to the millisecond, which is why the ordering is sound despite the missing in-band timestamp; but a receipt alone cannot date itself.

**F7 — Info — reader counting at the freeze (adjacent, not adjudicated).** The freeze message says "eight synthetic fixtures, seven shortcut classes". `mini-fix/readers/` holds **9** files; the two configs register **8** (7 shortcut classes + 1 structural positive control). `readers/label_keyed.py` is registered by neither config (`grep -n label_keyed` over `tools/round-34/*.py`, `*.json`, `mini-fix/*.py` → no hits), so it was unreachable for scoring at the freeze. This seat does not judge the consequence; it is named only because the later stop commit `cd75b92e` cites an unregistered shortcut class meeting the green target.

## 7. Lane movement during the audit (disclosure, not adjudicated)

| UTC | Tip | Subject |
|---|---|---|
| 07:18Z (audit start) | `c79bbe7b` | freeze |
| 07:22:31Z | `b917ea64` | *"retain before/production/control receipts, enforced pin container and predicate reconciliation after wave-1 record audits"* — 77 files, +6001; adds the 6 receipt pairs, `controls/gates/*`, `instruments.json`, `assimilation/*`, wave-1 prompts and `swarm-registry.json`; leaves `tools/round-34/**` and `claims.json` untouched |
| 07:23:47Z | `cd75b92e` (= `origin/main`) | *"stop R34-C2 on an unregistered content-multiset shortcut meeting the green target; bind the counterexample source and disclose five record defects"* |

My ordering conclusions are about the frozen state at `c79bbe7b` and hold unchanged at both later tips on the instrument/claims bytes (§2). `instruments.json` (added at `b917ea64`, post-freeze) declares `frozen_claims_sha256 = de3afbfb…`, which I recomputed as correct; its own note records that the frozen pin map sits under `claims[0].pins` and that `freeze-integrity.py` rejects that container as `instruments_missing` — a schema gap declared by the lane, not repaired in the frozen bytes, and **not re-run by me** (see §8).

## 8. Residual risk and verification gaps

- The four mutant gates' runtime behaviour and the gate's own selftest internals were not audited here (other seats' scope); I only checked that their receipts agree with their verdict lines and postdate the freeze. The `gate-junk-clean.py` mutant is an 11-line stub that fakes the selftest JSON — I read its first lines, did not run it.
- `tools/round-34/freeze-integrity.py` was **not** executed against `claims.json` (its `instruments_missing` verdict is taken from `instruments.json`'s note, not reproduced).
- The inherited R34-C1 production reader and its twelve carriers were not executed, scored, or opened as programs; no ELF, fixture or reader binary was run. Only the two counters above were executed, in scratch copies of `git archive` output.
- Whether the operator *typed* `--rev ec3125ad` while standing in a checkout of `ec3125ad` is not establishable from any committed byte (F2). My reproduction replaces that link; it does not prove the original run's provenance.
- The freeze-second internal order rests on loose-object birth times and the jj op log, not on git commit metadata (F4). A host clock rollback would be needed to forge it, but it is a weaker class than a signed timestamp; I found no contradiction between object births, reflog, op log and receipt births.
- `after/c2-at-instruments.json` and my `after-repro.json` agree on every recorded field but were not compared byte-for-byte; the committed file additionally records `target`/`predicate` from the same constants.

## Verdict

**CONFIRMED — freeze order holds.** (a) All 26 pinned instruments and `claims.json` first-add at `c79bbe7b` (27/27, pins 26/26 clean, no post-freeze amendment through `cd75b92e`); (b) `finding=gate_absent` at the declared base `ec3125ad` is true and independently reproduced (exit 2, 07:23:14Z) and also holds at the freeze parent `f432c8e3`; (c) the production receipt and all five control receipts postdate the freeze object by 10.5–41.1 s and the production receipt reproduces all six clauses at the freeze bytes (exit 0, 07:23:37Z); (d) no claim receipt predates the freeze — the sole earlier artifact is `census-start.txt` (07:04:34.5Z), which is a pre-freeze source census, not a claim receipt. Two defects are handed up: **F1** the frozen `predicate_identity` claim is false (receipts bind a 351-char predicate the 237-char claim/configs do not state), and **F2** `measured_revision` is an unverified argv echo with no recorded root, making the before receipt self-asserting until independently reproduced as done here.
