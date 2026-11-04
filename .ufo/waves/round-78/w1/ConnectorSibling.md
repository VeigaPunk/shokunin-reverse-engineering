# ConnectorSibling — how sibling lanes bind a receipt to its instrument, and what r78's `receipt_auth` misses

Round 78, wave 1. Connector seat: read-only across sibling lanes, nothing absorbed, one bounded
proposal. Everything below is measured against committed bytes or against the lane's own module
loaded by path; no lane file was edited, no git write was issued.

- Lane under study: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
  `6205ec8c575fb070243c0c40e34a2b0daacde46a`, declaration `3e6b1efc…`, freeze `ffcb47d1…`.
- Rule under study: `auth_findings()` in `tools/round-78/attack-gate.py:492-512` (rule id
  `receipt_auth`), reachable from `scan_record()` (`:441-486`) and from the battery's
  `FIXTURE_RULES["receipt_auth"]` (`:612-616`).

## Search record (what was actually read)

The seat's four named paths are not all present: `kagi-shokunin/tools/` and
`kumitate-shokunin/tools/` **do not exist**. `kumitate-shokunin` keeps its instruments in
`scripts/` (36 files); `kagi-shokunin` keeps its checks inside `.ufo/waves/round-2x/` and carries
no durable `tools/` tree (grep for `sha256` over `kagi-shokunin/` hits 2017 wave-scoped files,
none of them a receipt↔instrument binder). Read-only greps for `instrument`, `sha256`, `rev` over
`mado-shokunin/tools/`, `kagi-shokunin/`, `kumitate-shokunin/scripts/`, `tameshi-shokunin/tools/`.
Four concrete precedents follow, all from `mado`, `tameshi` and `kumitate/scripts`.

## Precedents

### P1 — kumitate `counter-pins`: a pin must bind bytes, not a name

`kumitate-shokunin/scripts/counter-pins.mjs:34-35`

```
 *   - the resolved path must exist and be a REGULAR FILE — a symlinked pin is
 *     DRIFT (the pin must bind bytes, not a name).
```

Enforced against the filesystem (`lstatSync`/`realpathSync`), with a red-before selftest case
that swaps a pinned path for a symlink and expects `first=ps:not-a-regular-file`
(`counter-pins.mjs:255-263`). Same gate, `:32-33`, refuses an escaping path (`..` or absolute)
as DRIFT `path-escape`: "a pin must bind bytes beneath its base, never wherever a registry author
points" (`:297` selftest case).

### P2 — kumitate `counter-pins`: an empty binding set is a defect, never a pass

`kumitate-shokunin/scripts/counter-pins.mjs:39-41`

```
 *   - an EMPTY pins[] array is DRIFT `pins-empty`, not CLEAN: a registry that binds
 *     nothing is precisely the state this gate exists to catch.
```

`return { verdict: 'DRIFT', pins: 0, bad: ['pins-empty:registry binds nothing'], exit: 1 }`
(`:118`); selftest case 8 asserts that exact line (`:267-272`).

### P3 — tameshi `receipt-bytes-bind`: the same re-derivation shape, with separable reasons

`tameshi-shokunin/tools/receipt-bytes-bind.py:35`

```
  bound      sha256(`git cat-file blob <measured_rev>:<tool>`) == tool_sha256
```

Three arms — `bound`, `corrected`, `unbound` — and the correction arm is failure-closed even when
the primary rev matches: "A `measured_bytes_rev` that does not carry the recorded sha makes the
receipt unbound even when `measured_rev` happens to match: a false correction line is never a
pass" (`:43-45`). `measure_receipt()` (`:247-270`) returns *distinct* reasons `rev-unresolvable`,
`tool-absent`, `bytes-rev-absent`, `bytes-rev-unresolvable`, `bytes-rev-mismatch`.

### P4 — mado `receipt-citecheck`: a directory is not a resolvable file

`mado-shokunin/tools/mado-receipt-citecheck.py:51-53`

```
# extension-like suffix. A bare-directory token (.ufo/waves/round-63) is not a
# resolvable citation — `git ls-tree -r --name-only` lists blobs, and naming a
# directory is not naming a committed file.
```

Citations are extracted under a closed grammar and resolved against one
`git ls-tree -r --name-only <rev>` name set (`:16-18`, `:36-38`); the tool reports
`resolved=<r> missing=<m>` and never silently drops a citation.

## Difference — what r78's `receipt_auth` requires, and what the siblings require instead

`auth_findings()` requires exactly four things of a receipt that an in-scope record cell cites:

1. `rev` is 40 lowercase hex (`is_hex`, `attack-gate.py:129-131`) — **format only**;
2. `instrument` is a dict with `path: str` and `sha256` 64 lowercase hex;
3. `git show <rev>:<path>` succeeds;
4. `sha256(that stdout)` equals `instrument.sha256`.

Plus, upstream in `scan_record()` (`:462-472`), the receipt's own path must resolve at the
**measured** rev, else `receipt_auth` finds "absent at the measured revision". The trigger is the
record: only a SCORECARD capability row with `First-working round >= 78` (`:396-405`) or a
PROVINCE `- **Core — ` bullet naming `tools/round-78/` or `.ufo/waves/round-78/` (`:406-410`)
puts a cell in scope. That trigger is narrower than kumitate's explicit registry or tameshi's
receipt directory, and it is measured vacuous before filing: `in_scope_cells = 0` at
`6205ec8c`, at `3e6b1efc` and at `ffcb47d1` (`probe2-out.json`), because the round-78 rows land
in the filing record.

| property | kaidoku r78 `receipt_auth` | tameshi `receipt-bytes-bind` | kumitate `counter-pins` | mado `citecheck` |
|---|---|---|---|---|
| rev format | 40-hex lowercase, required | 7–40 hex (`REV_RE`), optional correction rev | **no rev at all** | `--rev` passed to `git ls-tree` unvalidated, default `HEAD` (`:215`, `:101`) |
| rev resolvability | implicit only, and conflated with absence | distinct `rev-unresolvable` | n/a | a bad rev is exit 2 `ERROR (stage=git)` (`:98-107`) |
| digest | sha256 of `git show rev:path` | sha256 of `git cat-file blob rev:tool` | sha256 of the resolved regular file | none |
| object type | **none** | none | regular file only; symlink = DRIFT | file-suffix required; directory token refused |
| path containment | none (git `rev:path` clips leading `/`) | none | escape (`..`/absolute) = DRIFT | repo-top allowlist `.ufo/ corpus/ tools/ quality/ plans/` |
| empty binding set | **no term** | n/a | DRIFT `pins-empty` | `citations=0` still prints a verdict |
| binding unit | a record-cited receipt | every receipt file in a directory | a declared registry | a cited path in named artifacts |

Two differences carry the weight. First, kumitate is the only sibling that refuses an object by
**what kind of thing it is** (regular file, inside the base); the other three bind a digest to a
name and never look at the mode. Second, tameshi is the only sibling that keeps "the rev does not
resolve" apart from "the tool is not there"; kaidoku merges them, and the merged reason is
misleading in the case that matters (below).

## Gap — the pinned object need not be an instrument at all

`git show <rev>:<path>` is not a file reader. For a mode-`120000` symlink it prints the link
target text; for a mode-`040000` tree it prints a pseudo-header and the entry names. `auth_findings`
hashes whatever comes back and compares it to the receipt's own declared digest — so a receipt
can authenticate a pin that is not instrument bytes, and the forger never needs access to the
instrument.

Measured with the lane's own `auth_findings()`, loaded by path, against a throwaway git repo under
seat scratch (`probe.py`, `probe3.py`; raw output `probe1-out.json`, `probe3-out.json`):

| pin | `git show` bytes | `auth_findings` |
|---|---|---|
| `tools/instrument.py` (real file, own rev) | the instrument source | `[]` — accepted (correct) |
| `tools/link.py` (**symlink**, mode `120000`) | `instrument.py` (13 bytes of link text) | `[]` — **accepted** |
| `tools/pkg` (**directory**, mode `040000`) | `tree 82432e28…:tools/pkg\n\ndata.txt\n` | `[]` — **accepted** |
| `tools/pkg/data.txt` (any data blob) | `data\n` | `[]` — **accepted** |
| wrong sha | — | `instrument sha256 is not the blob at its own rev` |
| absent path | — | `instrument … absent at <rev>` |
| non-40-hex rev (`deadbeef`) | — | `no 40-hex rev` |

`ls-tree` confirms the modes (`probe3-out.json`): `120000 blob … tools/link.py`,
`040000 tree … tools/pkg`, `100644 blob … tools/instrument.py`. The lane's own `git_ls` helper
(`attack-gate.py:147-148`) already shells `git ls-tree` and throws the mode away with
`--name-only`; the check is one output field away.

**The attack.** A receipt names `instrument.path = "tools/round-77"` (a directory) — or any
tracked data blob — and declares the sha256 of the short string git prints for it. No tracked file
changes, no instrument bytes are touched, and the rule's own sentence ("an `instrument.sha256` that
re-derives from the blob at that rev") holds: the digest does re-derive. What fails is the
property the sentence exists to establish — that this receipt was produced by that instrument.
This is the class kumitate refuses as "the pin must bind bytes, not a name" (P1) and the class
mado refuses as "naming a directory is not naming a committed file" (P4).

**Why the round's own battery does not catch it.** The `receipt_auth` fixture (`a1-forged-receipt`)
pins nothing — its receipt carries no `rev` and no `instrument` block — so the class is outside
a1. The five fixtures that do pin (`a2`–`a6`) pin `tools/round-78/fixture-instrument.py`, a regular
blob — at the freeze rev every blob under `.ufo/waves/round-78/attacks/` is regular
(`git ls-tree -r ffcb47d1 -- .ufo/waves/round-78/attacks/ | cut -d' ' -f1 | sort | uniq -c` →
46 × `100644`, 1 × `100755`, no `120000`/`040000`). The selftest carries two `receipt_auth`
cases (`attack-gate.py:830-835`) and they cover two
of the rule's four refusal arms: no `rev`, and no instrument block. Nothing in the battery or the
selftest can distinguish a pinned instrument from a pinned directory.

**Not claimed.** No committed receipt in this lane is measured as forged; `a1`–`a6` are fixtures,
and the genuine record was not read at a filing rev because none exists yet. This is a strength
gap in the rule's refusal set, not an accusation about the record, and not a violation of the
frozen kill rule — `claims.json:12` kills "a receipt admitted **without re-deriving** its own
instrument pin", and this receipt does re-derive. That is precisely the contradiction: the
predicate's letter is met while its purpose is not.

## Affected axes

- **calibration (R78-C1, the lane's tied-lowest axis)**: improves — one more attack class becomes
  refusable, and the rule's refusal set gains an object-type arm the battery does not test today.
- **freshness (R78-C2)**: untouched — no read of `PROVINCE.md` surface values, no interaction with
  `surface-recheck.py`.
- **coverage / depth**: no change to counts; if the proposal is adopted as an eleventh fixture the
  predicate's `fixtures_total 10` would move, so the bounded proposal keeps the rule's arm and
  selftest pair only, leaving the ten-fixture set intact.

## Proposed move (one, bounded)

In `auth_findings()`, before the digest comparison, resolve the pinned object's mode —
`git ls-tree <rev> -- <path>` (drop `--name-only` in a dedicated helper; `git_ls` at `:147-148`
cannot serve as-is) — and refuse anything that is not a regular blob
(`100644`/`100755`) with a distinct reason `pin-not-a-regular-blob`, alongside an optional split of
`rev-unresolvable` from `instrument-absent` (measured above: a 40-hex all-zero rev currently reads
"instrument tools/instrument.py absent at 000…", which names the wrong object). Add the selftest
pair: green = real file at its own rev; red = symlink pin and tree pin. Two reds, one green, no new
fixture id, so `fixtures_total 10` / `base_accepted 10` / `refused 10` stand.

## Risks

1. **The genuine arm can be vacuous and still read clean.** `ok` (`attack-gate.py:727-731`) is
   `fixtures_total == 10 and base_accepted == 10 and refused == 10 and not
   genuine.mismatch_count and not genuine.defects and not validate.defects` — there is no
   `in_scope_cells > 0` or `groups > 0` term, and `genuine.record` reports those counts without
   any rule acting on them. Measured: at base, declaration and freeze the record has
   `in_scope_cells 0, groups 0, bound_clauses 0, receipt_auth findings 0`, i.e. the "genuine
   control is the real record judged by every rule" sentence was, at every rev this round has
   committed so far, judged over nothing. This is kumitate's `pins-empty` shape (P2): a control
   that binds nothing is the state that gate exists to catch. It is not a predicate violation —
   the predicate's clauses are all satisfied — and it is not measured at a filing rev, which does
   not exist yet; I did not create one. It is the second-order risk that the same object-type
   fix does not touch.
2. **Over-tightening the other way.** Requiring the pin to live under `tools/` would be stricter
   than every sibling (kumitate binds lane-relative; mado's tops include `corpus/ quality/ plans/`)
   and would refuse legitimate instruments elsewhere. The proposal deliberately stops at object
   type.
3. **Review-surface effect.** A directory pin renders in prose as a path plus a 64-hex digest,
   which reads like a pin to a human reviewer; the fix's refusal reason must therefore be visible
   in the battery's `reasons[]`, not only in a code path.
4. **Conflation.** Merging `rev-unresolvable` and `instrument-absent` means a bad rev is reported
   as a missing file; if the object-type arm lands while this stays, a refusal against an
   unresolvable rev will still misname the object. Low blast radius, but it makes the new refusal
   harder to diagnose when it fires for the wrong reason.

## Verification

Re-run (scratch deleted afterwards; fixture repo is created under `--scratch` and asserted with
`git -C "$D" rev-parse --show-toplevel` before any commit, per seat bounds):

```
S=/fast/scratch/hyaku/kaidoku-r78/ConnectorSibling
TMPDIR=$S python3 -I -B probe.py  --scratch "$S" --gate <lane>/tools/round-78/attack-gate.py
TMPDIR=$S python3 -I -B probe3.py --scratch "$S" --gate <lane>/tools/round-78/attack-gate.py
TMPDIR=$S python3 -I -B probe2.py --lane <lane> --rev 6205ec8c575fb070243c0c40e34a2b0daacde46a \
        --scratch "$S" --gate <lane>/tools/round-78/attack-gate.py
```

The first two reproduce the accepted/refused table above; the third reproduces
`in_scope_cells 0` at the base rev and the vacuity fixture (`probe2-out.json`: an in-scope record
with no receipt citation scans to `groups 0`, `findings []`).

If the proposal lands: `python3 -I -B tools/round-78/attack-gate.py --selftest` must stay
`failures=0` with the two new reds, and `--battery` must still print `fixtures_total 10`,
`base_accepted 10`, `refused 10`, `genuine.defects []` — no committed fixture and no fixture
receipt pins a non-regular blob (a2–a6 pin `tools/round-78/fixture-instrument.py`, a `100644`
blob; a1 pins nothing), so the arm cannot touch the base arm.

## Files written

- `.ufo/waves/round-78/w1/ConnectorSibling.md` (this report)
- `.ufo/waves/round-78/w1/ConnectorSibling/probe.py`, `probe2.py`, `probe3.py`
- `.ufo/waves/round-78/w1/ConnectorSibling/probe1-out.json`, `probe2-out.json`, `probe3-out.json`
- `.ufo/waves/round-78/w1/ConnectorSibling/report.json`
