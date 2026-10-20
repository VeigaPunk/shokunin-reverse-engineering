# CriticC1 — falsifying C1's eleven closures before they land

Axes: calibration (each item), coverage (all 11 + the counter itself), depth (weakest
substance check per item). Target file: `.ufo/waves/round-20/claims.json:14-18`;
counter spec: `.ufo/waves/round-20/gen-wave1.py:61-82`; interfaces: `contract.md:38-82`.

## Commands run (all exits observed, this seat)

- `git rev-parse HEAD` → `d1d981d2…`, committer `2026-10-20T17:43:06-03:00` (exit 0).
  [O] lane HEAD is past baseline `14f0260…`; the measured REV is still open.
- `ls .ufo/waves/round-20/tools/` → exit 2, does not exist. [O] every C1 correction is
  undelivered; this report attacks the *spec'd* closure tests, which is the right moment.
- `git status --porcelain` → `?? …/round-19/verify/scratch-custody/custody-pair-selftest-k_zd4w5n/{repo-fixture,repo-sub-fixture}/` (exit 0). [O] D1 residue is live now.
- `python3 -I -B .ufo/gates/c1-census-v10.py --root .` → exit 1, `VERDICT: FAIL
  (…undeclared=2)`: SCORECARD.md 2380-2382, SKILL.md 511-519. [O] (Note: piping through
  `| tail` masked exit as 0 on a first run — pipeline artifact, not the tool.)
- `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev main` →
  `live_count=0`; sites list contains **no** verify.py:83 or revpin.py:113 entry
  (revpin.py:223 shows as `other-HEAD fixture`). [O] both routed reads are *invisible*,
  not just unclassified — each sits behind a two-level wrapper (`_git_or_none`→`git`
  at verify.py:64-66,83; `_resolve`→`_git` at revpin.py:85-86,113).
- `stat -c %a /home/vgpnk/.local/opt/go-1.24.6/{bin/*,pkg/tool/linux_amd64/*}` → all 644
  (20 files). [O] arm state is real; `manual-arm.json` modes/digests plausible.

## Meta-attacks on the counter itself (apply to all 11)

- **M1 — "named" is a token guard.** `gen-wave1.py:63-64`: named = a `- R19-<ITEM>:`
  line in SCORECARD.md *and* lessons/round-20.md. Both are author-written prose; a
  substance check that only re-runs the fix's own selftest (D3, D6b, D6f) inherits the
  tool's honesty: a carrier-guard.py that prints `SELFTEST: CLEAN … exec_refused`
  without executing anything passes D3 substance. Defeat: for selftest-gated items the
  counter must *independently re-derive* one observable (e.g. stat the armed carriers —
  cheap: all 644 today), not only trust printed case names.
- **M2 — `--live` omitted from the counting command.** `claims.json:17` runs
  `routed-r19.py --root <LANE> --rev <REV> --strict` — no `--live` — yet the only check
  that sees the D1 worktree residue is under `--live` (`gen-wave1.py:67-68`; residue is
  untracked, so REV git objects are blind to it). C1 can read 11→0 while the residue
  dirs still sit in the tree. **Strongest single hole in the whole claim.**
  Defeat: counting command needs `--live`, or a separate `git status --porcelain`
  assertion on the delivered worktree.
- **M3 — counter vs. census split.** The census leg runs `--root <LANE>` on the
  working tree while routed-r19 reads REV objects; a dirty-but-committed-clean or
  clean-but-uncommitted delivery each defeat one leg in isolation. Defeat: same run
  must verify `git diff REV` is empty except declared files.

## Per-item strongest attack + defeating evidence

**D1 (custody-pair residue).** Attack: refuse `--scratch` inside a worktree and add a
`try/finally` cleanup — spec satisfied — but (a) never delete the existing
`scratch-custody` residue (untracked → invisible at REV) and (b) detect worktrees by
`os.path.isdir(p/".git")`, which misses *linked* worktrees and submodules where `.git`
is a **file**, and un-resolved symlinked scratch paths. Defeat: `git status
--porcelain` at delivery shows zero `custody-pair-selftest-*` anywhere; fixture using a
`git worktree add` scratch (`.git` file, not dir) still exits 2; scratch passed through
a symlink into a repo refused via `realpath`.

**D2 (future-dated timestamps).** Attack: regex misses bare `YYYY-MM-DD` and
`YYYY-MM-DD HH:MM` without a zone — the whole future class ships past the lint.
Contract (`contract.md:42-45`) licenses this literally (only zoned forms), so the lane
"closes" D2 while the defect generalization survives. Second attack: `--path` scoped to
`.ufo/waves/` leaves `corpus/`, SCORECARD.md, claims.json files outside evidence dirs
unchecked — the original defect was claims.json:36 *in a wave dir*, so a
wave-dir-scoped tool is tuned to the instance, not the class. Third: `git blame -C/-M`
default-off is fine, but a line rewritten later re-dates blame — a timestamp planted
inside a later legit edit passes. Defeat: fixture with a bare-date future timestamp and
an unzoned `HH:MM` timestamp must flag; run `--path` over corpus/ + wave files at REV;
an `--allow`-style exemption list must be enumerable in output (spec allows it:
`gen-wave1.py:97-98` — every exempted line is a hidden defect).

**D3 (carrier execution).** Attack: the record is trusted, not recomputed —
`check-<UTC>.json exit 0` is a self-report; a forged check record (or a check taken
*before* a later execution) reads green. Exec-bit arm is also copy-blind: `cp go /tmp/x;
chmod +x /tmp/x` executes the same bytes and check stays green — declared limit
(`contract.md:51-52` names only loader-mapped/root, not copies). And if
`predictions/carriers.tsv` is absent at REV, the equality clause vacuates
(`gen-wave1.py:71`: "if that file exists"). Defeat: counter stats each armed carrier
path at run time (all 644 today — recomputation, not record trust); check record's
`taken_at_utc` must postdate the arm and bound the run window; execution during armed
window must appear as `content_changed`/`mode_restored`/ctime-class finding or a named
admission.

**D4 (census re-key).** Attack: declare SCORECARD 2380-2382 / SKILL 511-519 **DATED** —
they read `historical (dated scope)` per `c1-census-v10.py:567-573`, and every stale or
false pin inside them is sheltered forever (the instrument's own docstring calls
DATED-shelter fail-open, `:26-33`). Contract says "true class", which is unverifiable —
a wrong-but-plausible class is the re-key-that-hides. Defeat: the two blocks assert
*live* facts (6.7.0 pins, current carrier diagnostics); a CURRENT row is the true
class. Evidence defeating a DATED re-key: `git show REV:SCORECARD.md | sed -n
2380,2382p` contains live-version claims; planted-stale fixture inside the new row must
still flag STALE (DATED would swallow it).

**D5 (final census).** Attack: record `final-census.json` against rev T, then amend the
SCORECARD append into the *same* commit so the tree-diff clause
(`gen-wave1.py:73-74` — "differs only in that record and its stdout file") still holds
while the census ran over pre-append content. Second: stdout produced by a census run
over a *dirty* worktree is committed as if clean-tree. Defeat: re-run census at
delivered tip, sha256-compare against `stdout_sha256` AND verify the recorded `rev`'s
tree equals the tip tree minus the two record files; the committed stdout must equal a
run against `git archive` of that rev (kills the dirty-worktree substitution).

**D6a (nested HEAD reads).** Attack: classify verify.py:83 / revpin.py:113 by a
path-allowlist (`nested` only for these two files) or by slapping
`# head-rev-lint: compare-only` annotations — annotations are trusted comments
(`head-rev-lint.py:142-143`), so a live non-compare read annotated `compare-only` stays
hidden; worse, a path-keyed `nested` class leaves every *new* two-level wrapper
invisible. Defeat: JSON at REV shows both sites with `context: nested` (not
`annotated`/`fixture`/absent); a fixture tool whose *nested* HEAD read is used as the
pin (not comparison) must still count `live` — nested ≠ excused. Note contract text
"(round-17 `verify.py`, `revpin.py`)" (`contract.md:56-57`) is loose — revpin.py lives
in round-18; a fixer exploiting the grouping to skip revpin.py is defeated by requiring
both explicit paths.

**D6b (revexec sandbox).** Attack: selftest-string trust (M1) plus namespace holes —
`unshare -n` blocks IP but not abstract UNIX sockets (`@dbus`, `@/tmp/.X11-unix/X0`,
inherited socket FDs), so `net_refused` passes while extracted code still talks to host
services. Also `runs_ok` green + no `--extra` coverage means a second extracted file
can write outside unwatched. Defeat: selftest fixture that opens an abstract-namespace
unix socket and one that writes via a pre-opened inherited FD must both refuse;
`write_outside_refused` exercised on an `--extra` file too.

**D6c (slug escape).** Attack: validate only `os.path.basename`-adjacent forms — slug
`sub/../x` fails regex (has `/`) but `..`-embedded slugs passing regex are impossible,
so the real remaining hole is **order**: `_snapshot` (`citation-drift-probe.py:168-185`)
currently opens the file *before* any check; a fix that validates after `isfile/read`
still touches the escaped path (pre-check TOCTOU/read). Also validation added only on
the `@slug` path while `entry["rev"]`-driven snapshot reads (`:249-253`) or `quoted`
entries (`:440`) bypass it. Defeat: fixtures `../x`, `a/b`, absolute `/etc/passwd`,
slug containing NUL/`..` alone (`.`, `..`, `a..b` legal? — `a..b` passes regex and
contains `..` substring: must be refused per contract "contain no `..`"), and a
symlink *inside* snapshot-dir pointing out — all exit 2 `slug_unsafe`, no read first.

**D6d (argv decoy).** Attack — the strongest in the set: fix only the list-shaped
`steps` path (`receipt-validate.py:614-621`) while the **object-shaped** `steps` dict
still authenticates by key alone (`:611-613` — `steps["analyze"]` is trusted without
any argv check). A receipt `{steps: {"analyze": {argv: ["npx","-y",
"rea-agents@6.5.0","search","analyze"], pin_checks:[…]}}}` satisfies the selftest
shape that stays green while the decoy authenticates. Second: keep the `name`/`step`
fallback (`:145-161` `return bool(declared)`) — `argv`-less identity still
authenticates, violating "authenticated *only when* argv has the token"
(`contract.md:65-67`). Third: `rea` basename path (`:157`) authenticates non-npx forms.
Defeat: object-shape step carrying a decoy argv must also read
`analyze_step_unauthenticated`; a `name:"analyze"` step with non-qualifying argv must
not count; positive control `["npx","-y","rea-agents@X.Y.Z","analyze",…]` still green.

**D6e (`causes` key collision).** Attack: disambiguate wrapper-vs-flat by
`doc["causes"]` being a dict — then a flat-map doc whose `causes`-named seat carries an
object value `{cause, source}` (`wave-outcomes.py:25` legal value form) still falls
into the wrapped branch and resolves its *inner* keys as seats → `causes_unknown_seat`
or silent meta-ignore. Same class hits seat `seats` (`:244`) and `wave` (`:238,259`
reads `doc["wave"]` as wave-meta even when `wave` is a *seat* in the flat map).
Defeat: fixture flat map `{"causes": {"cause":"x","source":"y"}, "Alpha":"z"}` with
seat `causes` must attribute the cause to seat `causes`; seat `wave` in flat form must
not set `doc.wave`; wrapped form `{"causes": {"causes": "x"}}` still green.

**D6f (jj selftest gaps).** Attack: add `jj_`-prefixed cases that pass on the BASELINE
blob too — `gen-wave1.py:80` requires ">=2 more `jj_` case ids than at B", a pure
count; `jj_duplicate_of_env_scrub` and `jj_second_alias` inflate the count with zero
new coverage. Real gaps to keep hidden under token cases: scrubbed-env coverage —
`_dirty_key` (`jj-red-before.py:123-125`) strips only `GIT_*`/`JJ_*`/`TMPDIR`;
`GIT_CONFIG_COUNT`-style vars, `LD_*`, `PYTHONPATH`, and PATH/`BASH_ENV` redirection
reach every child (ReviewJjRedBefore:54 E retains PATH/HOME). Defeat: each new `jj_`
case must fail on `git show B:…/jj-red-before.py` (red-before, not only green-after);
a `jj_child_env_observed` fixture whose child prints its env asserts absence of planted
`GIT_CONFIG_COUNT`/`LD_PRELOAD`/`GIT_DIR`.

**QUALITY rows (11th item).** Attack: append a row 23 that is vacuous
("verify before claiming") — count satisfied, byte-identity satisfied, no admissible
rule added. Or: satisfy "rows 1-22 byte-identical" by never touching them while row 23
re-states an existing rule (duplicate authority — a frontier regression). Defeat:
`git diff REV~1..REV -- corpus/QUALITY.md` shows only appended lines; the new row must
cite a mined mistake with a falsifiable recheck command per the table's own shape.

## Smallest safe corrections

1. Add `--live` to the C1 counting command (kills M2/D1-invisible-residue).
2. For every selftest-gated item, counter re-derives one observable outside the tool
   (D3 stat; D6a JSON site contexts; D6f red-on-baseline fixture).
3. D4: require CURRENT class (or a positive "row asserts no live claim" re-derivation
   by re-running census on a planted-stale fixture of the two blocks).
4. D6d: extend the substance fixture to the object-shaped `steps` form and the
   argv-absent `name` form, not only the list shape.
5. D2/D6e/D6f: substance fixtures must enumerate the *adjacent* shapes (unzoned stamps,
   flat-map `causes`/`wave`/`seats` seats, baseline-red `jj_` cases) — a fix tuned to
   the named instance is a re-key that hides.

Report complete; no lane writes besides this file. No installs.
