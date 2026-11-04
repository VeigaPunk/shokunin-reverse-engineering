# ExecRegistry — R68-C1 independent census re-derivation (round 68, w1)

Seat: ExecRegistry (leaf; no dispatch, no lane edits, no git/jj mutation).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Base: `fcbe200f6739c38939e0dabf3f251de2cc6bd727`. Freeze: `1eaf596e5f241762349fbd102c9e09ec1df18e3f`.
Measured tip: `6ffa9ce1119ec01c953494d8f5b28e419efad646` (`main` at 22:41–22:52).
Frozen instrument: `tools/round-68/registry-conformance.py`, sha256
`a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315` — byte-identical to the pin in
`.ufo/waves/round-68/claims.json` (verified with `sha256sum`, observation). The other two pins
(`packed-elf.py` `48ef4c68…`, `controls.py` `0657ee08…`) also match (observation).

All numbers below are **git-object** measurements at named revisions, produced by my own extractor
(`census_own.py`), not by the frozen instrument. The instrument is used only for (a) a static code
audit and (b) two in-memory pure-function probes plus one forward reading of the L1's uncommitted
`SKILL.md`; those are labelled where they appear.

## 1. Verdict of this seat

**Observation.** At the base revision my independent census reproduces the frozen receipt
`l1/pre/c1-at-base.json` exactly, field for field: `scope_size 69`, `registry_rows 73`,
`mismatches 2`, and the two mismatches are exactly `tools/round-67/avm-le-counter.py` and
`tools/round-67/mutation-battery.py`. At the freeze and at the current tip the strict pre-repair
reading is `scope_size 71`, `registry_rows 73`, `mismatches 4` (the same two round-67 paths plus
`tools/round-68/packed-elf.py` and `tools/round-68/registry-conformance.py`), because `plans/round-68-claims.md`
adds two own-round instruments and `SKILL.md` carries no round-67/round-68 rows yet. Adding exactly
the four rows atom A5 names yields `scope_size 71`, `registry_rows 77`, `mismatches 0`, `ok true` —
the predicate's target. **The arithmetic closes with exactly four added rows; five would fail the
pinned `registry_rows 77`.**

**Observation (not mine, uncommitted).** While this seat ran, the L1's landing appeared in the
working tree: `SKILL.md` is `M` with `+4` rows (`git diff --stat SKILL.md` = `1 file changed,
4 insertions(+)`), table lines 79 = header + separator + **77 rows**, and the four new rows are at
lines 1858–1861 (`tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`,
`tools/round-68/registry-conformance.py`, `tools/round-68/packed-elf.py`). Fed to the frozen
instrument's own pure `census()` together with the committed plans/tools at `6ffa9ce`, that
working-tree text reads `scope_size 71, registry_rows 77, registry_paths 77, unregistered [],
duplicate_rows [], row_absent [], thin [], mismatches 0, ok true` (observation on uncommitted
bytes). This is **not** the after-arm and is not a committed measurement; the census reads
`--rev` (git) only, so the repair must be committed before the after-run.

## 2. Method — my own extractor

`census_own.py` (sha256 `e23d587f…`, in this seat dir) reads git objects directly
(`git -C <lane> ls-tree -r --name-only <rev> -- plans tools`, `git show <rev>:<path>`) and
implements the regime from the declaration and atom A4 with its **own** grammar:

* plan scope: literal `tools/round-<N>/<path>.{py,sh,mjs}` mentions (word boundary after the
  extension), kept only when the captured round equals the plan's own round and the path exists at
  the revision;
* registry: lines inside exactly one `<!-- instrument-registry v2 -->` / `<!-- /instrument-registry -->`
  pair whose first cell is backticked;
* thin: a row's verdict cell that does not show each of 0/1/2 in verdict position (cell start, or
  after `;`/`|`/whitespace, followed by `=`/`:` or a word); a loose grammar (any code mention) is
  reported alongside so divergence is visible.

Exact commands (absolute paths; receipts in this seat dir):

```
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-68/w1/ExecRegistry/census_own.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <rev> --json-out <scratch>/own-<name>.json
#   <rev> = fcbe200f6739c38939e0dabf3f251de2cc6bd727 -> own-base.json
#   <rev> = 1eaf596e5f241762349fbd102c9e09ec1df18e3f -> own-freeze.json
#   <rev> = 6ffa9ce1119ec01c953494d8f5b28e419efad646 -> own-tip.json
#   <rev> = 6ffa9ce… --simulate-repair               -> own-tip-sim.json
python3 -I -B .../regime_audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev main   # audit-tip.json
```

Grammar cross-check (observation): for all 34 plan files at tip, the set of own-round paths found
by my literal grammar equals the set found by an independent re-implementation of the instrument's
`TOOL_RE` filter, with one difference: the instrument's regex also matches the hyphen-suffixed
directory `tools/round-50-c3/sqfs-triage-v5.py` (cited by plans 51/52/53) and then excludes it as
foreign; my grammar never matches it. No scope-set difference results.

## 3. One table per revision

### 3.1 Base `fcbe200` (predicate's before-arm)

| metric | value |
|---|---|
| scope_size | 69 |
| registry_rows (= distinct paths) | 73 (73) |
| unregistered | 2: `tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py` |
| duplicate_rows | [] |
| row_absent | [] |
| thin (strict = loose) | [] |
| legacy_unregistered (N<41) | 26 (`tools/round-35…40`, list identical to the receipt) |
| named_but_absent | 12 (6× `tools/round-51/*`, 6× `tools/round-52/*`) |
| mismatches | 2 |
| ok | false |

Per-round scope: 41:12, 42:10, 43:4, 44:3, 45:3, 46:4, 47:2, 48:2, 49:3, 50:6, 51:1, 52:0, 53:3,
55:2, 56:1, 57:1, 59:1, 60:1, 61:1, 62:1, 63:1, 64:1, 65:2, 66:2, 67:2 (sum 69).

Reconciliation against `.ufo/waves/round-68/l1/pre/c1-at-base.json`: **all 11 comparable fields
equal** (`scope_size`, `registry_rows`, `registry_paths`, `unregistered`, `duplicate_rows`,
`row_absent`, `thin`, `legacy_unregistered`, `named_but_absent`, `mismatches`, `ok`).

### 3.2 Freeze `1eaf596` and tip `6ffa9ce` — strict pre-repair (identical at both)

| metric | value |
|---|---|
| scope_size | 71 |
| registry_rows (= distinct paths) | 73 (73) |
| unregistered | 4: the two round-67 paths **plus** `tools/round-68/packed-elf.py`, `tools/round-68/registry-conformance.py` |
| duplicate_rows / row_absent / thin | [] / [] / [] |
| legacy_unregistered | 26 (unchanged) |
| named_but_absent | 12 (unchanged) |
| mismatches | 4 |
| ok | false |

`SKILL.md` is byte-identical from base to tip (`git diff --stat fcbe200 6ffa9ce -- SKILL.md` empty);
the +2 scope paths come only from `plans/round-68-claims.md` (own-round mentions at lines 34 and 67;
its round-67 mentions at lines 17/23/24 are foreign and excluded). `tools/round-68/controls.py` is
**not** in scope: `claims.json` lists it, but the census reads plans, and plan-68 never names it.

### 3.3 Tip `6ffa9ce` + exactly the four A5 rows (simulation)

| metric | value |
|---|---|
| scope_size | 71 |
| registry_rows (= distinct paths) | 77 (77) |
| unregistered | [] |
| duplicate_rows / row_absent / thin | [] / [] / [] |
| legacy_unregistered / named_but_absent | 26 / 12 |
| mismatches | 0 |
| ok | true |

This equals the predicate target (`mismatches 0`, `scope_size 71`, `registry_rows 77`) **provided**
the four rows are well formed: 7 cells each, no unescaped `|`, verdict cell naming 0, 1 and 2.
The L1's uncommitted working-tree rows satisfy all three conditions (observation above).

## 4. Regime audit — declaration vs code

Agreements (observation, by reading `plan_scope`/`census`/`registry_rows`):

* `REGIME_START = 41` matches the plan and A4; legacy rounds are separated, not counted.
* Own-round filter is a real filter: a path starting `tools/round-M/` with M ≠ plan round never
  enters `regime`/`named`; `scope` excludes paths absent at the revision; `named_but_absent` is
  excluded from `scope` and from `mismatches`.
* `mismatches = |unregistered| + |duplicate_rows| + |row_absent| + |thin|`, each set sorted and
  named, never a bare count; exit 0/1/2 as declared; markers must be exactly one each.

Disagreements and undocumented behaviours (each observed; none changes either pinned number at
either revision):

1. **Thin grammar under-documented.** The docstring says the code may sit "at the start of the cell
   or after `;`". `VERDICT_RE` also accepts after `|` and after any whitespace. Probe: a cell
   `0=met 1=not met 2=unevaluable` is **not** thin under the code. The `|` branch is unreachable
   through `registry_rows`, because cells are split on `|` before the verdict cell is extracted —
   a literal `|` inside a verdict cell would shift the cell, not be parsed as a separator.
2. **`named_but_absent` is own-round only.** Docstring: "a plan names a tool that does not exist at
   --rev". Code: only own-round names enter `named`, so a foreign-round citation to a missing tool
   is silently invisible. Probe (in-memory): plan-68 citing `tools/round-67/ghost.py` yields
   `named_but_absent []`. No such citation exists at either revision (all 37 foreign-cited paths
   exist at tip), so the base receipt is unaffected — but the docstring's blanket claim is false in
   general, and A4's unqualified "named_but_absent is reported" inherits the ambiguity.
3. **`plan_scope` docstring mislabels its third return.** Docstring: `(regime, legacy,
   named_but_absent)`; code returns `(regime, legacy, named)` where `named` includes existing paths.
   Probe: `plan_scope({"plans/round-67-claims.md": "tools/round-67/a.py"})` returns the path in both
   the first and third elements. Behaviour of `census` is correct; the docstring is not.
4. **`ok` has an extra condition** — `len(scope) > 0` — not stated in the docstring or A4. It only
   makes the empty-scope case fail closed; the predicate pins scope 71 anyway.
5. **`thin` inspects only the first row** for a duplicated path (`r[0]["verdict"]`). A thin second
   row is not listed in `thin`, but the duplicate is already a mismatch, so scoring is unaffected.
6. **"Exists as a blob" is `git ls-tree -r --name-only -- tools`**: any entry (including a symlink
   mode 120000) counts. No symlink exists in the current `tools` tree (observation via ls-tree
   output inspection).
7. **Scope is a literal-path reading of "names".** The regime prose says a plan "names" a
   `tools/round-N/<name>.(py|sh|mjs)` path; the code accepts only literal full-path mentions.
   Plans that freeze instruments through **brace expansion** or bare filenames are therefore not in
   scope. This is the one place where the declaration and the code can honestly be read as
   disagreeing, and it is load-bearing for inventory completeness (see §6), not for the numbers.

Foreign-round exclusion audit: verified in code (`tool.startswith("tools/round-{plan_round}/")`),
in data (plan-68's two round-67 citations are excluded from round-68's scope yet remain in scope
through plan-67's own citations at `plans/round-67-claims.md:47` and `:98`), and by sensitivity
(§5). It is genuinely excluded.

## 5. Sensitivity of the pinned numbers to the regime clauses

| clause dropped | base (scope, mismatches) | tip post-repair (scope, mismatches) |
|---|---|---|
| none (declared regime) | 69, 2 | 71, 0 |
| foreign citations counted as scope | 71, 2 | 73, 0 |
| legacy rounds (N<41) counted | 95, 28 | 97, 26 |
| both | 100, 31 | 102, 29 |

* Foreign exclusion is load-bearing for the pinned **scope_size 71** (73 without it) but not for the
  mismatch count at either revision. The two extra paths are `tools/round-41/local-source-gate.py`
  and `tools/round-42/prefile-gate.py`, both registered.
* Legacy exclusion is load-bearing for the **before-arm 2**: without it the base would report 28
  mismatches (the 26 legacy rows plus the two round-67 paths), contradicting the predicate.
* Thin-vs-loose grammar is not load-bearing today: `thin` is empty at both revisions under both
  readings.

## 6. Inventory completeness the census cannot see (scope audit)

**Observation.** 87 tools-shaped blobs exist at tip under rounds ≥ 41; the census's scope is 71 of
them (73 if foreign citations counted). Eleven modern instruments exist, are named by the scope
grammar nowhere, and have **no registry row** — repairing the four rows leaves all eleven invisible:

| path | why invisible |
|---|---|
| `tools/round-42/c1-extra.py` | plan-42 names it only inside the brace list `tools/round-42/{…,c1-extra.py,…}` (line 183) and by bare name (line 209) |
| `tools/round-43/build-copies-r43.py` | only inside `tools/round-43/{…}` (line 263) |
| `tools/round-43/c2-controls-r43.py` | only inside `tools/round-43/{…}` (line 263) |
| `tools/round-43/receipt-wrap.py` | only inside `tools/round-43/{…}` (line 263) |
| `tools/round-44/c1-controls.py`, `c1-oracle.py`, `c1-run.py`, `c2-controls.py` | no plan mentions them |
| `tools/round-48/census2.py` | plan-48 pins `tools/round-48/census2.json`, not the `.py` |
| `tools/round-67/c1-run.sh` | plan-67 never mentions it |
| `tools/round-68/controls.py` | plan-68 never mentions it (`claims.json` lists it; the census reads plans) |

Round-44 also carries `tools/round-44/c1-run.sh` (in scope, registered) beside the unregistered
`c1-run.py`, so the blind set is not a directory artifact.

Reverse direction, also unchecked except for existence: **6 registry rows whose path no plan
names** — `tools/round-41/local-source-gate.py`, `tools/round-42/prefile-gate.py`,
`tools/round-49/c1-controls.py`, `tools/round-49/c1-oracle.py`, `tools/round-49/c1-run.py`, and
`tools/round-50-c3/sqfs-triage-v5.py`. The last is not even round-shaped
(`tools/round-50-c3/`), yet it counts toward `registry_rows` (it is the one row my non-round-path
check finds); the row-side checks (duplicate/thin/absent) apply to it, the scope-side cannot.
In total 95 tools-shaped blobs at tip are named by no own plan and carry no row: the eleven modern
ones above plus 84 legacy ones (rounds 25–40). The legacy portion is expected and declared; the
modern eleven are this table.

**Inference.** The claim's type line ("the registry-conformance census over the lane's own
instrument inventory") is broader than what is measured: the census measures *plan-path-named
instruments ↔ registry rows*, with existence checks on rows, not inventory completeness. The frozen
predicate scores 0/71/77 either way; this is reported, not narrowed.

## 7. Notes and risks for the L1's landing

1. **Exactly four rows.** `registry_rows 77` allows no fifth row. In particular do **not** add rows
   for `tools/round-68/controls.py` or `tools/round-67/c1-run.sh` in this landing (77 → 78); they
   are invisible to scope and would break the pinned count.
2. **Row shape.** Each new row must keep 7 cells; an unescaped `|` inside a verdict cell shifts
   `cells[2]` and can produce `thin`. Verdict cells must name each of 0, 1 and 2 in the grammar of
   §4.1. The four working-tree rows satisfy this as of this report.
3. **Commit before measuring.** The instrument reads `git show <rev>:SKILL.md` and
   `git ls-tree <rev> -- tools|plans`; uncommitted rows do not exist for it.
4. **The base receipt names a moving ref.** `l1/pre/c1-at-base.json` records `"rev": "main"`, which
   now resolves to `6ffa9ce`; reproducing the before-arm requires `--rev
   fcbe200f6739c38939e0dabf3f251de2cc6bd727` (my run does, matching all fields). Its
   `"instrument": {"rev": null}` is honest (the instrument did not exist at base), but per A9 the
   measured-revision receipt must carry the sha as `--rev`; at the freeze/tip the instrument-bearing
   revision is `6020eb6064c9196764d9921ec070e34bc9308fb9`.
5. **Untracked stray in the instrument dir.** `tools/round-68/registry-conformance.receipt.json` is
   untracked (not authored by me; it reads `scope_size 1, registry_rows 2, duplicate
   tools/round-67/reg.py`, i.e. a fixture run). Git-object reads ignore it, but it sits inside a
   tracked instrument directory; the L1 decides.
6. **Concurrent working tree.** At read time the tree also showed `M tools/round-29/prefile-check.sh`
   and `M SKILL.md` (+4 rows), not authored by this seat; my measurements use git objects at
   `6ffa9ce` only.

## 8. Evidence (this seat dir, sha256)

| file | sha256 | content |
|---|---|---|
| `census_own.py` | `e23d587f23403356c3abc9a2645195e440ffa293873db9390fa1478dc1c55b9b` | independent census extractor |
| `regime_audit.py` | `d4fa150d18935b6441ca6767708871b6059b697547935540d71302987560aaf3` | inventory/regime audit |
| `own-base.json` | `a17470960ecb7ee2fee889521c6e026d2398dd1363fe9decce5e65ee65c3c82a` | base `fcbe200` |
| `own-freeze.json` | `e7d0d0e3687dd5df6b94adb22d0e3dcb1dd6c91cd705a893001ed52bf078238a` | freeze `1eaf596` |
| `own-tip.json` | `8e11e166d25e9ccffba6211e4fef69e28b749128c57d999a341cd9872c686d59` | tip `6ffa9ce`, pre-repair |
| `own-tip-sim.json` | `ecbe6eb88b213d654e51bfe9215d5e5314b487c1f844bf631ed458a37a1ac605` | tip + 4 A5 rows (simulation) |
| `audit-tip.json` | `20ad50a4b749567801e6a420f3d652582dfe7f2eeffde59809458d8866dfe179` | scope/inventory audit at tip |

Tooling: nothing installed or upgraded (no pacman transaction attempted); all work used the
preinstalled `python3`, `git`, `sha256sum`.

## 9. Limits (unknowns, not silently passed)

* I did not run the frozen instrument's CLI census at any revision, nor its `--selftest`; the
  parent owns gate execution. Instrument behaviour evidence is static reading plus in-memory
  pure-function probes (no files written, no bytecode cache).
* I did not re-derive R68-C2 (outside this seat), the six control arms, or any file beyond the
  census's own inputs (`SKILL.md`, `plans/round-N-claims.md`, `tools/**` blobs).
* Classifications: every "matches/differs" statement above is an observation from a command whose
  output is retained in the receipts; the reading of the claim's breadth (§6) is inference; the
  base receipt's original `main` target is unknown beyond its matching numbers.
