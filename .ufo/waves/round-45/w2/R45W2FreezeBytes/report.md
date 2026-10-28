# R45W2FreezeBytes — adversarial falsification of the freeze-integrity record

Wave 2, round 45, seat `R45W2FreezeBytes`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

- Freeze **`f762b7273e3f6ca3c710bb37d5de92a4a4417aec`** (tip compared against: A3 **`f59565b782c18b0eb691bec12f52d2f80d9f5032`**).
- Measured revision (A1) **`1f4b27f82353d6544dc0c8048b3cfdadd8525d12`**; lane HEAD at work time **`a63d109faa050207d4c184471889049741c9ebbf`**.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W2FreezeBytes` (removed after the receipts below were taken). All fixtures asserted `git -C "$D" rev-parse --show-toplevel` == `$D` before their first commit.
- **Write discipline:** no write to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`, or any sibling lane. Every attack on an artefact ran against a **copy in `$S`**; every git invocation was read-only (`rev-parse`, `ls-tree`, `log`, `show`, `rev-list`, `merge-base`, `cat-file`). No commit/stage/stash ran in the lane.
- Process note for honesty: one intermediate arm-removal pass buffered output through a transient `/tmp/.x` and was discarded and **redone without any `/tmp` write**; only the redo is cited (it is the byte-identical-output measurement in §5). Nothing citable came from `/tmp`.

## 1. Verdicts

| # | attack | verdict | decisive receipt |
|---|---|---|---|
| V1 | blob hashes at `f762b727` vs `f59565b7` for every file under `tools/round-45/` and for `plans/round-45-claims.md` | **holds** | R1: all five blobs equal both sides |
| V2 | frozen subtree oid at both revisions | **holds** | R2: `8cb6fa80…` both sides |
| V3 | commit list for `f762b727..f59565b7 -- plans/round-45-claims.md tools/round-45` (expect empty) | **holds** | R3: `commits=0` |
| V4 | same pathspec from the freeze to lane HEAD (a later commit could have touched it) | **holds** | R4: `commits=0` |
| V5 | the record's own freeze derivation `git log --format=%H -1 -- plans/round-45-claims.md` | **holds**, and is robust because the file has exactly one touching commit | R5 |
| V6 | `red-frozen-touched` selftest case of `c2-counter.py` | **holds** (expect 2, got 2; 7/7) | R6 |
| V7 | `frozen-path-preflight.py --selftest` | **holds** (11 cases, 0 failures) | R7 |
| V8 | detector vs a committed append / commit-then-revert / mode-only chmod / delete / nested pathspec | **holds** (all detected) | R8 |
| V9 | detector vs a mutation landed **only in a merge commit's conflict resolution** | **FALSIFIED** | R9, R10 |
| V10 | A3's disclosure that the red cases are "arm-covering but not arm-isolating", naming `blob` and `restored` | **holds as written, incomplete**: a third arm (`touched`) is also non-isolating, and it is the only arm the counters use | R11 |
| V11 | the block's self-disclosed limit ("a table of structurally valid but empty rows would pass it") | **holds** — confirmed, not evasive | R12 |
| V12 | A3's `--dirty-pathspec` false-clean disclosure | **holds** — reproduces exactly | R13 |
| V13 | counters vs a worktree-only change / a new untracked file under the frozen directory | **holds (out of claim scope)** — not a falsification; see §8 | R8 |
| V14 | the round's two counters still read 0/`met_target` at the measured revision | **holds** — `frozen_path_changed []`, no measured value moves | R14 |
| V15 | C2's `scope_size == 6` as a proxy for "six instruments" — a scope file repeating **one** path six times | **FALSIFIED** (predicate weaker than its own prose; frozen file itself is clean) | R15 |

## 2. V1–V5: the freeze really is byte-frozen

```
plans/round-45-claims.md                f93df4c3bd4069a0cd576d9649f1157609b6a5d5  == f93df4c3… (both revs)
tools/round-45/c1-counter.py            4ce400b29d6eba3cb03e242db8ba8bdf9d4fcfdd  == (both revs)
tools/round-45/c2-counter.py            7d83de6258cb624b1ebb0e18c326cf9fb5fd1aee  == (both revs)
tools/round-45/frozen-path-preflight.py b42398273da0449c01f6f26cc630853d58ea55ec  == (both revs)
tools/round-45/registry-scope.json      4855e97e497e329737f00076bdf686bf71b0827d  == (both revs)
tree f762b727:tools/round-45 = f59565b7:tools/round-45 = 8cb6fa801ed16c54f3db14bb7c432a3d5385997e
```

`commits=0` for the pathspec over `f762b727..f59565b7` **and** over `f762b727..HEAD`. The same five
blobs are also unchanged at HEAD, so the file set is frozen not only against A3 but against every
commit that has landed since — including A2, the A2/A3 score commits and R45-CL17.

Freeze derivation is sound rather than merely lucky: `git rev-list --count HEAD -- plans/round-45-claims.md`
is **1**, so "the commit that first contains this file" and "the most recent commit touching it"
(what `git log -1` prints) coincide for the whole history. The derivation in `plans/round-45-claims.md:9-11`
cannot drift into naming a later commit while still passing.

## 3. V6–V8: the instruments' own red cases and the ordinary touch shapes

`c2-counter.py --selftest` → `C2_SELFTEST: cases=7 failures=0`, with
`{"expect": 2, "got": 2, "ok": true, "selftest": "red-frozen-touched"}` — the specific case the
assignment asked for. `frozen-path-preflight.py --selftest` → `cases=11 failures=0`.

Against a byte-identical copy of each counter's `frozen_path_changed` (imported from `$S`, not from
the lane), seven commit shapes:

| shape | detected |
|---|---|
| committed append | yes |
| append then revert (tip bytes == freeze bytes) | yes — the `restored` semantic holds, `raw` shows two commits |
| mode-only `chmod 644→755`, blob unchanged | yes |
| frozen file deleted | yes |
| nested file modified under the `tools/round-45` directory pathspec | yes |
| new nested file added under it | yes |
| **mutation only in a merge commit's resolution** | **NO** |

## 4. V9 (FALSIFIED): a merge-commit mutation is invisible to both counters

`frozen_path_changed` in both counters is exactly:

```python
log = git(root, "log", "--name-only", "--format=", f"{freeze}..{rev}", "--", *FROZEN)
```

`git log` prints no diff for a merge commit unless `-m`/`--cc`/`--diff-merges` is given. A merge
whose **conflict resolution** is the only place a frozen path changes is therefore missing from
`FREEZE..REV`, and the arm returns `[]`.

End-to-end against the unmodified `c2-counter.py` (`$S/e2e.py`), fixture whose SKILL.md/scope satisfy
every c2 clause, freeze added, then an evil merge appending one line to `plans/round-45-claims.md`:

```json
{"claims_blob_at_freeze": "7424a92c6d4bb8b9408c2ae9e1d7fb28c7089eb7",
 "claims_blob_at_rev":    "bf15fcd2e56340575b1d6ac433f7b93e0d85eb4b",
 "blob_differs": true,
 "post_merge_exit": 0, "post_merge_reason": null,
 "post_merge_met_target": true,
 "post_merge_frozen_path_changed": [], "post_merge_failing": [],
 "raw_name_only": [],
 "with_dash_m": ["plans/round-45-claims.md", "plans/round-45-claims.md"]}
```

The counter exits **0 `met_target: true` while the frozen blob differs**. That contradicts
`plans/round-45-claims.md:143-148` ("no commit in `FREEZE..REV` touches a frozen path … a touch makes
the counter exit 2 `frozen_path_changed`") and block 22's commit row. The counters have **no second
arm**: `grep` for `blob|ls-tree|diff --` finds only the `rev-parse --verify` guards, so nothing else
can catch it.

Calibration — this is a real shape in this repository, not a hypothetical: `git rev-list --merges --count HEAD`
= **2**, one of them `7256d1da merge origin/main: … union resolution keeps both sides`, i.e. a merge
commit whose content is decided by the resolution. Both predate the freeze and
`git rev-list --merges --count f762b727..HEAD` is **0**, so nothing in the scored range exercises the
hole — but the lane has already done exactly the thing the arm cannot see.

The standalone gate is *not* affected: the same fixture scores `verdict: frozen_path_changed`, exit 1,
`touched: [{"commit": "6ba826c9…", "status": "M", "path": "plans/round-45-claims.md"}]`, because it runs

```python
git log -m --diff-merges=first-parent --name-status --format=%x00%H …
```

and separately compares per-path blobs (`blob_changed: ["plans/round-45-claims.md"]`). So the defect is
narrow and named: **the counters reimplemented the arm more weakly than the interpreter the claim points at.**

**Fix** (one line, in each counter's `frozen_path_changed`, plus optionally the preflight's blob arm):

```python
log = git(root, "log", "-m", "--diff-merges=first-parent", "--name-only",
          "--format=", f"{freeze}..{rev}", "--", *FROZEN)
```

Verified sufficient above (`with_dash_m` non-empty on the same fixture). Belting-and-braces version,
which also survives a resolution that happens to match one parent: iterate `git ls-tree -r --name-only <base> -- <pathspec>`
and flag any path where `rev-parse <base>:<p>` != `rev-parse <tip>:<p>` — the preflight's `blob` arm.

**Routing constraint for L1:** the fix cannot land in place. `tools/round-45/` is frozen, so committing
the patch makes both counters exit 2 `frozen_path_changed` for every later rev, destroying this round's
claim. It is a round-46 carry-forward with its own freeze (new claims file), or an explicit re-freeze.
No measured value moves either way (§8).

## 5. V10: A3's arm-isolation disclosure is true but stops one arm short

Block 22 (`SKILL.md:571-574`) says the red cases are "arm-covering but not arm-isolating — deleting the
`restored` classification or the `blob` arm alone still reads 11/0 because `touched` absorbs the kill".
Deleting each arm from the verdict expression in a scratch copy:

| arm removed | rc | result | stdout sha | vs baseline |
|---|---|---|---|---|
| `blob` | 0 | `cases=11 failures=0` | `00c89f9dd2b61c3b` | **byte-identical** |
| `restored` | 0 | `cases=11 failures=0` | `00c89f9dd2b61c3b` | **byte-identical** |
| `touched` | 0 | `cases=11 failures=0` | `00c89f9dd2b61c3b` | **byte-identical** |
| `dirty` | 1 | `cases=11 failures=1` | `c1dcadec850e09c5` | differs |

The two named arms behave as disclosed. But `touched` is a **third** single-removal-invariant arm: its
removal does not change one byte of the selftest output. The disclosure therefore reads as "only these
two are absorbed", and that is not the case. The omission is material rather than pedantic because
`touched` is precisely the arm the two counters rely on exclusively (§4): the one arm with no red case
that only it can pass is the arm carrying the counters' whole freeze guarantee. Minimal pairs confirm
the redundancy structure rather than a dead arm: `{touched, dirty}` alone pass 11/11; dropping
`blob`+`touched` fails 2; dropping `touched`+`restored` fails 1; `dirty` alone fails 3; `blob` alone
fails 2. So `touched` is load-bearing and merely not *isolated* by any case.

Suggested correction to block 22: name three arms, or state the fact directly ("no single arm removal
except `dirty` changes the count") and add a case where the tip bytes still equal the freeze bytes and
the classification is the only signal.

## 6. V11–V12: the two self-disclosed limits are honest

- **Empty rows.** Copying the real `SKILL.md` into a fixture and replacing only block 22's ten table
  rows with `| garbage trigger N | garbage arm N | <0|1|2> | garbage receipt |` (marker, header, prose
  and citations untouched) still scores `c1_exit: 0`, `met_target: true`, `rule_blocks: 22`,
  `block22_rows: 10`, `block22_refs: 8`, `block22_unresolved_citations: []`. The claim's predicate is
  structural exactly as `SKILL.md:603-605` admits.
- **`--dirty-pathspec`.** With `plans/round-45-claims.md` genuinely dirty (` M`), the gate returns
  `verdict: frozen_path_changed`, `dirty: [" M plans/round-45-claims.md"]` without the flag and
  `verdict: clean`, `dirty: []` with `--dirty-pathspec tools/round-45` — the flag *replaces* the dirty
  scope, exactly as `SKILL.md:574-577` states, and the round's documented invocation never passes it.

## 7. V15 (FALSIFIED): six copies of one path certify as six instruments

C2's predicate 1 is `scope_size == 6`, and `scope_size` is `len(json["paths"])` — a list length, not a
count of distinct instruments. Fixture: one real instrument (`tools/round-45/c1-counter.py`), one
registry row, and a scope file whose `paths` array repeats that single path six times. Scored by the
unmodified `c2-counter.py`:

```
scope_size=6  registered=6  unregistered=[]  thin=[]  met_target=True   (rc=0)
```

So the calibration claim — "the registry names the instruments that carry the claims" — is satisfiable
with **one** instrument registered once, provided the scope file repeats it. This is the same failure
family as §4: the predicate is weaker than the prose it stands for. The claims' own kill rule
(`plans/round-45-claims.md:127-130`) says "Row counting cannot substitute for path equality", which
closes the *wrong-row* hole (`red-wrong-path-rows`) but leaves the *duplicate-path* hole open.

Calibration, stated plainly: **this does not impugn this round's measurement.** The frozen
`tools/round-45/registry-scope.json` lists six genuinely distinct paths (verified at both revisions,
§2), and the live run registers 6/6 with `unregistered []`. The reachable-but-unexercised weakness is
in the instrument's invariant, not in the data it scored.

**Fix:** `if len(set(scope)) != 6: reasons.append(...)`, plus a selftest case
`red-duplicate-scope` with `SCOPE_TEST` replaced by `[SCOPE_TEST[0]] * 6`. Same routing constraint as
§4: `tools/round-45/` is frozen, so this rides round 46's freeze.

## 8. V13–V14: what I am *not* calling false, and the round's numbers

The counter's `frozen_path_changed` misses an uncommitted worktree edit and a brand-new untracked file
under `tools/round-45/`. **This is not a falsification.** `plans/round-45-claims.md:145-146` scopes the
arm to commits in `FREEZE..REV`; the worktree is the preflight's `--check-dirty` arm by design, and
`SKILL.md:589` row 4 assigns it there. Calling it a defect would be exactly the over-calling this wave
should avoid. It is recorded here as a shape the *counters* cannot see, so the L1 does not read the
counter's exit 0 as a worktree guarantee.

Live, read-only, at the measured revision A1:

```
c1: exit 0  rule_blocks=22 block22_rows=10 block22_refs=7 unresolved=[] frozen_path_changed=[] met_target=true
    preflight_selftest={cases:11, failures:0, ok:true} block22_cites={S140:true, interpreter:true}
c2: exit 0  registered=6/6 unregistered=[] thin=[] frozen_path_changed=[] met_target=true
both at HEAD a63d109f: exit 0
```

So the round's measured values stand and the freeze-integrity premise under them is true **for this
history**: there is no merge in `f762b727..HEAD`, and no commit anywhere in that range touches a frozen
path. §4 is a defect in the *claim's universality*, not in this round's numbers.

## 9. Receipts (exact command, exit code, stdout sha256, UTC)

`S=/fast/scratch/hyaku/kaidoku-r45/R45W2FreezeBytes`; `TMPDIR=HYAKU_SCRATCH=$S`.

| id | command | rc | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `for p in plans/round-45-claims.md $(git ls-tree -r --name-only f762b727 -- tools/round-45); do echo "$p $(git rev-parse f762b727:$p) $(git rev-parse f59565b7:$p)"; done` (cwd lane) | 0 | `a6ca6045764963e0…` | 2026-10-28T16:03:00Z |
| R2 | `echo "f762b727 $(git rev-parse f762b727:tools/round-45)" && echo "f59565b7 $(git rev-parse f59565b7:tools/round-45)"` | 0 | `475e03326103608c…` | 2026-10-28T16:03:00Z |
| R3 | `git log --oneline f762b727..f59565b7 -- plans/round-45-claims.md tools/round-45; git rev-list --count f762b727..f59565b7 -- …` | 0 | `bfe36a7928a58a52…` (`commits=0`) | 2026-10-28T16:03:01Z |
| R4 | `git rev-list --count f762b727..a63d109f -- plans/round-45-claims.md tools/round-45` | 0 | `bfe36a7928a58a52…` (`commits=0`) | 2026-10-28T16:03:01Z |
| R5 | `git log --format=%H -1 -- plans/round-45-claims.md; git rev-list --count HEAD -- plans/round-45-claims.md` | 0 | `dd17eef9266f3027…` (`f762b727…`, `total-touching=1`) | 2026-10-28T16:03:01Z |
| R6 | `python3 -I -B c2-counter.py --selftest` (copy in `$S/bin`) | 0 | `aea7e363e5661efc…` (`red-frozen-touched` expect 2 got 2; `C2_SELFTEST: cases=7 failures=0`) | 2026-10-28T16:03:01Z |
| R7 | `python3 -I -B frozen-path-preflight.py --selftest` | 0 | `9f03df6538de49b7…` (`cases=11 failures=0`) | 2026-10-28T16:03:01Z |
| R8 | `python3 -I -B probe.py $S/fx3` (seven shapes, counters' own function imported from `$S/bin`) | 0 | `f1c4785749d4ae83…` | 2026-10-28T16:03:01Z |
| R9 | `python3 -I -B e2e.py $S/e2e-fx2` (evil merge scored by unmodified c2) | 0 | `c242eaee278e18bd…` (`post_merge_exit 0`, `met_target true`, blobs `7424a92c…` vs `bf15fcd2…`) | 2026-10-28T16:03:01Z |
| R10 | `frozen-path-preflight.py --root $S/e2e-fx2 --freeze 4772541a… --rev 6ba826c9… --pathspec plans/round-45-claims.md --pathspec tools/round-45` | **1** | `e67f5943aa20ff05…` (`touched[0].status=M`, `blob_changed=[claims]`) | 2026-10-28T16:05:29Z |
| R11 | arm-removal loop, `OUT=$(… --selftest); RC=$?` over `no-blob/no-restored/no-touched/no-dirty` | 0/0/0/**1** | `00c89f9dd2b61c3b…` ×3 vs baseline `00c89f9dd2b61c3b…`; `no-dirty` `c1dcadec850e09c5…` | 2026-10-28T16:03:23Z |
| R12 | `python3 -I -B emptyrows.py $S/emptyfx2` | 0 | `4362dd87c749f400…` (`c1_exit 0`, `met_target true`, `block22_rows 10`) | 2026-10-28T16:03:02Z |
| R13 | `frozen-path-preflight.py --root $S/dirty --freeze <root> --rev <root> --check-dirty --pathspec … --dirty-pathspec tools/round-45` | 0 | `22a451358960050f…` (`verdict clean` while claims dirty) | 2026-10-28T16:03:02Z |
| R14 | `c1-counter.py --root <lane> --freeze f762b727 --rev 1f4b27f8 --json-out $S/r-c1.json`; same for c2 | 0 / 0 | `e607db25889d94fe…` | 2026-10-28T16:03:02Z |
| R15 | `c2-counter.py --root $S/dupscope --freeze <root> --rev <root>` where `registry-scope.json` = `{"paths": [<one path>] * 6}` | 0 | `94f0b34de6a1bfad…` (`met_target True`, `scope_size 6`, `registered 6`) | 2026-10-28T16:04:43Z |

Git-side receipts R1–R5 were taken with `git -C <lane>`; all are plumbing reads, none mutates.

Hashing convention, stated so no reviewer reads a false mismatch: R1–R9 and R12–R14 hash
`subprocess`-captured stdout **including** the trailing newline; R10, R11 and R15 hash `$(...)`
command-substitution output, which strips it. The same preflight selftest therefore appears as
`9f03df6538de49b7…` with the newline (R7) and `00c89f9dd2b61c3b…` stripped (R11 baseline); both
digests are reproducible from `printf '%s\n'` and `printf '%s'` over the same output.

## 10. Risks and open items

1. **Carry-forward (must not be patched in place):** counters' `frozen_path_changed` is blind to
   merge-commit-only mutations. Fix = `-m --diff-merges=first-parent` and/or a per-path blob arm
   (§4). Round 46, new freeze. Patching now trips the very guard under test.
2. **Carry-forward:** C2's `scope_size` counts list entries, not distinct instruments, so a duplicated
   scope file passes (§7). Fix = distinctness check + `red-duplicate-scope` selftest case. Round 46.
3. **Disclosure correction (cheap, no code):** block 22 names two non-isolating arms; there are three
   (`blob`, `restored`, `touched`). `touched` is the counters' only arm — the omission points at the
   weakest link, so it is worth naming.
4. **Not run (stated as "not run", not as a pass):** whether a *rename* of a frozen path to a path
   outside the pathspec is reported under every `--find-renames` heuristic; whether a frozen path
   replaced by a *submodule gitlink* (`160000`) is reported as `T` by the preflight's status set, which
   does include `T` but has no case exercising it. Nothing else in the assignment was skipped.
5. **Calibration note:** V13's two false-cleans are deliberately *not* counted as falsifications; the
   claim scopes the arm to commits and block 22 assigns the worktree to `--check-dirty`.
