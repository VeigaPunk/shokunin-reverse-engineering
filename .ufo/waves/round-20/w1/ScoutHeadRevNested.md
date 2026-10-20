# ScoutHeadRevNested — the two nested HEAD reads and why HeadRevLintNested failed

Written 2026-10-20T17:52:12-03:00 (`date -Iseconds` at write time). Read-only seat: no lane file was edited;
scratch copies live under `/tmp/kr20-*` and `mktemp -d`. No tool was installed or upgraded this seat.

Observed base: `git -C /tmp/kr20-ScoutHeadRevNested rev-parse HEAD` -> `14f0260ad319ecc26994381b2415d5a999003375`
(`git clone -q --no-hardlinks LANE /tmp/kr20-ScoutHeadRevNested`, exit 0). Round-20 tip observed as
`d1d981d2cc041dda4656c5b01d2c8445d8d17124`.

Verdict up front: the inherited patch **applies cleanly**; it fails its own `--selftest` at one stale
fixture-count assert, and a second stale expectation appears immediately behind it. Both are fixture-bookkeeping
defects, not defects in the nested scanner, which does report the two real sites correctly.

---

## 1. The two nested compare-only HEAD reads (observation)

Both read the same revision to **validate** the branch tip; neither selects the source revision.

| # | Path:line (baseline blob) | Code |
|---|---|---|
| 1 | `.ufo/waves/round-17/verify.py:83` | `head = _git_or_none("rev-parse", "--verify", "HEAD^{commit}")` |
| 2 | `.ufo/waves/round-18/tools/revpin.py:113` | `head = _resolve(lane, "HEAD^{commit}")` |

**Compare-only status (observation, from code — not from a tool label):**

- verify.py: `source` is `refs/heads/<branch>` (`:81`); `head` is only compared at `:93`
  (`if head != source: ... "head_not_branch_tip"`) and returned alongside `source` at `:101-102`.
  The preceding line `:82` carries `# head-rev-lint: compare-only`.
- revpin.py: `source` is `refs/heads/<branch>` (`:103`); `head` becomes `head_equals_source` (`:119`) and can
  only raise `head_not_branch_tip` (`:123-124`). **There is no `head-rev-lint:` annotation in revpin.py**
  (observed: `git grep -n 'head-rev-lint:' <rev> -- verify.py revpin.py` prints only `verify.py:82`).

### Call chains from the entry point (observation, baseline line numbers)

**verify.py** — `if __name__ == "__main__": sys.exit(main())` (`:244-245`)
-> `main()` (`:105`) -> `res = resolve_source()` (`:109`) -> `resolve_source()` (`:71`)
-> call `_git_or_none(...)` (`:83`) -> `_git_or_none(*args)` (`:64`) -> `return git(*args)` (`:66`)
-> `git(*args)` (`:60`) -> argv literal `["git", "-C", LANE, *args]` (`:61`).

**revpin.py** — `if __name__ == "__main__": sys.exit(main())` (`:325`)
-> `main()` (`:291`) -> `result = resolve_source(...)` (`:312`) -> `resolve_source(...)` (`:98`)
-> call `_resolve(lane, "HEAD^{commit}")` (`:113`) -> `_resolve(root, rev)` (`:84`)
-> `_git(root, "rev-parse", "--verify", "--quiet", rev)` (`:86`)
-> `_git(root, *args)` (`:76`) -> argv literal `["git", "-C", root, *args]` (`:78-81`).

**Why the primary rule misses them (observation):** the primary class admits a call whose first argument is a
literal `["git", ...]` argv, or a call to a function *whose own body builds* one
(`.ufo/waves/round-18/tools/head-rev-lint.py:1-30`, docstring). `_git_or_none` and `_resolve` build no literal:
they forward `*args` / `rev` into a wrapper. That is one hop beyond the rule — exactly the nested class.

---

## 2. Why the inherited patch failed (observation)

Apply is **not** the failure:

```text
$ git -C /tmp/kr20-ScoutHeadRevNested apply --check -v .../round-19/w1/inherited/HeadRevLintNested.patch
Checking patch .ufo/waves/round-18/tools/head-rev-lint.py...
EXIT=0
$ git -C /tmp/kr20-ScoutHeadRevNested apply .../HeadRevLintNested.patch
APPLY_EXIT=0
```

The patched tree's selftest is red (verbatim):

```text
$ python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest
SELFTEST: FAILED 3
SELFTEST_EXIT=1
```

Traceback from a direct call of `selftest()` (verbatim):

```text
  File "/tmp/kr20-ScoutHeadRevNested/.ufo/waves/round-18/tools/head-rev-lint.py", line 1341, in selftest
    assert result["fixture_count"] == 2, result["fixture_count"]
AssertionError: 3
```

`SELFTEST: FAILED 3` is an `AssertionError` whose *message* is the bare integer `3`; the tool's reporting at
`:1376` prints only `exc`, so the one-line output hides which assert fired. That is why the failure read as
opaque.

**Root cause (observation):** the patch adds `FIXTURE_NESTED_PY`
(`HeadRevLintNested.patch:539`) to revision 1 (`:580`) but leaves the later fixture expectations stale. The
fixture repo at rev2 has three primary fixture sites, not two:

| rev2 site | context | reason |
|---|---|---|
| `ctx.py:5` | fixture | enclosing function `selftest()` |
| `fixtures/rebuild.sh:2` | fixture | path contains `/fixtures/` |
| `nested.py:30` | fixture | enclosing function `selftest()` |

`nested.py:30` is the direct `git("rev-parse", "HEAD")` in the new fixture buffer
(`head-rev-lint.py:1188-1220`, direct call at `:1217`). The rev2 cleanup at `:1334-1335` removes only
`live.py`, `edge.py`, `run.sh`, so `nested.py` survives. Observed counts by revision:

```text
REV c83918a7 exit 1 sites 21 live 15 fixture 5 annot 1 nested 2   # rev1 — every patched rev1 assert passed
REV cc812449 exit 0 sites  3 live  0 fixture 3 annot 0 nested 2   # rev2 — asserted 2, observed 3
```

**Second, latent failure (observation):** bumping `:1341` from `2` to `3` only moves the red one stage later —

```text
$ python3 -I -B $D/hrl.py --selftest
SELFTEST: FAILED 
SELFTEST_EXIT=1
```

(the empty message is `assert result["live_count"] == 0 and result["fixture_count"] == 0` at `:1350`, which has no
message). At rev3 `nested.py:30` still exists, so `fixture_count == 1`, and `sites == []` at `:1352` would fail
next. The rev3 cleanup `:1344-1345` also omits `nested.py`.

**Two observed repairs, both green:**

- **A (one line, recommended):** add `.ufo/waves/round-17/nested.py` to the rev2 rm at `:1334-1335`.
  `nested.py`'s nested assertions all run at rev1 (`:1295-1310`), so rev2/rev3 lose nothing.
  Observed: `SELFTEST: CLEAN cases=3`, exit 0.
- **B (two lines):** `:1341` `== 2` -> `== 3` **and** add `nested.py` to the rev3 rm at `:1344-1345`.
  Observed: `SELFTEST: CLEAN cases=3`, exit 0.

The unpatched baseline tool at the same base is green: `SELFTEST: CLEAN cases=3`, exit 0.

---

## 3. Does the patched scanner actually find the two sites? (observation)

Run read-only against the lane's Git objects, `--root LANE --rev <rev>`:

| Tool | rev | live_count | nested_count | nested_live_count | strict exit |
|---|---|---|---|---|---|
| unpatched (blob at 14f0260, run from mkdtemp) | 14f0260 | 0 | — (no key) | — | 0 |
| patched | 14f0260 | 0 | 2 | 2 | 0 |
| patched | d1d981d (R20 tip) | 0 | 2 | 2 | 0 |

Patched records at both revs (identical):

```text
NESTED .ufo/waves/round-17/verify.py 83 rev-parse-HEAD live _git_or_none ['_git_or_none', 'git']
NESTED .ufo/waves/round-18/tools/revpin.py 113 rev-parse-HEAD live _resolve ['_resolve', '_git']
```

Neither line appears in the unpatched `sites[]`; the unpatched output has no `nested` key at all
(`['annotated_count','excluded','files_scanned','fixture_count','limits','live_count','rev','routed_sites','sites']`).
The nested class does not move `live_count` or `--strict` (0 both before and after), as documented.

**Calibration caveat (observation):** both nested rows carry `context: "live"`, not `annotated`. The annotation
at `verify.py:82` sits on the *preceding* line, and the rule reads only the site line: `python_context` passes
`lines[line-1]` (`head-rev-lint.py:563-564`) into `annotation_for_line`, which regexes that single string
(`:345-347`). So the tool does **not** itself certify "compare-only" for either row; that label rests on the
code reading in section 1 (and on `verify.py:82`, which is inert under the current rule). A round-20 counter for
D6a must key on the nested *lines/`via`/`nested_count`*, not on `context == "annotated"`, or it will read the
patch as contradicting its own claim.

Related: `c1-census-v10.py` contains no `nested`, `head-rev-lint`, or `round-17` token (observed: grep prints
nothing), so the census neither declares nor blocks this class; D6a is carried by the lint tool alone.

---

## 4. Round-19 disposition of this patch (observation)

- The authoring seat never delivered: `.ufo/waves/round-19/evidence/wave-outcomes/w1-terminal.json:70-79` —
  `"name": "HeadRevLintNested"`, `"report_present": false`, `"stop_reason": "aborted"`,
  `"cause": "Request was aborted"`. `.ufo/waves/round-19/evidence/wave-outcomes/w1-causes.json:5` records the
  kill (L1 session exit on a provider 429). The patch is therefore an unverified orphan, not a rejected
  submission: no seat ever observed it green.
- Round-19 wave 2 had already caught the **first** defect: `.ufo/waves/round-19/w2/ToolAliasLintLimits.md:19`
  reports `SELFTEST: FAILED 3` at the candidate's line 1341 and the missing `nested.py` removal in the rev2
  cleanup (baseline anchors `head-rev-lint.py:856-868`, assert `:873`). This scout reproduces that exactly
  (`:873` in the mkdtemp baseline blob is the same assert the patched tree numbers `:1341`).
  **New here:** the rev3 stage is also stale, so the one-line count bump alone is not sufficient; repair A
  (rm at rev2) is the smaller green fix.

---

## Command log (each with its observed exit)

```text
git -C /tmp/kr20-ScoutHeadRevNested rev-parse HEAD                                   # exit 0 -> 14f0260a...
git -C /tmp/kr20-ScoutHeadRevNested apply --check -v <patch>                          # exit 0
git -C /tmp/kr20-ScoutHeadRevNested apply <patch>                                     # exit 0
python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --selftest                   # exit 1 -> SELFTEST: FAILED 3
python3 -I -B -c '<importlib; selftest() with traceback>'                             # exit 0 -> AssertionError: 3 at line 1341
python3 -I -B -c '<spy on evaluate; selftest()>'                                       # exit 0 -> rev1: 21/15/5/1/2; rev2: 3/0/3/0/2
python3 -I -B $D/hrl.py --selftest   (repair A: rm nested.py at rev2)                 # exit 0 -> SELFTEST: CLEAN cases=3
python3 -I -B $D/hrl.py --selftest   (repair B: count 3 + rm nested.py at rev3)        # exit 0 -> SELFTEST: CLEAN cases=3
python3 -I -B $D/head-rev-lint-base.py --selftest   (unpatched baseline)              # exit 0 -> SELFTEST: CLEAN cases=3
python3 -I -B $D/head-rev-lint-base.py --root LANE --rev 14f0260 --strict             # exit 0 -> live 0, fixture 15, annot 6, no nested key
python3 -I -B <patched> --root LANE --rev 14f0260 --strict                            # exit 0 -> live 0, nested 2, nested_live 2
python3 -I -B <patched> --root LANE --rev d1d981d --strict                            # exit 0 -> live 0, nested 2, nested_live 2
git --no-optional-locks grep -n 'head-rev-lint:' 14f0260 -- verify.py revpin.py       # exit 0 -> only verify.py:82
git -C LANE cat-file -e 14f0260:.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch  # exit 0 (tracked)
```

## Limits / unresolved

- The nested resolver is intra-file, `NESTED_DEPTH = 6`, `NESTED_TEMPLATES = 8` per function; a chain through
  another module or a same-named def is not resolved (the patch states this in `LIMITS`,
  `HeadRevLintNested.patch` docstring hunk). Not re-derived here.
- The patch's docstring still advertises `SELFTEST: FAILED ...` without `cases=`/`fails=` for the red path, and
  its failure path prints a bare exception message; the contract's `SELFTEST: FAILED ... cases=N fails=M` shape
  is not met on red. Only the green shape (`SELFTEST: CLEAN cases=3`) satisfies the contract.
- I did not run the patched tool inside the lane tip's working tree (read-only seat); all runs read Git objects
  via `--rev`, so no working-tree state was exercised.
