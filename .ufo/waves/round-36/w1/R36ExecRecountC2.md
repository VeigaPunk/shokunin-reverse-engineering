# R36ExecRecountC2 — C2 selftest, frozen base recount, independent recompute

Seat: `R36ExecRecountC2` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured revision = base = `cab59f221fe19726b5692bfa4d9a9679e96b8a73` (== freeze base in
`plans/round-36-claims.md`). All reads are `git -C <lane>` object reads; no worktree file was
modified or used as measurement input.

Scratch: `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecRecountC2`, `TMPDIR=$S`; removed before this
report was finalized. Everything cited below is reproduced verbatim in this file.

## Instrument identity (read-only)

| Object | Command | Result |
|---|---|---|
| `tools/round-36/c2-counter.py` worktree | `sha256sum tools/round-36/c2-counter.py` | `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` |
| same at freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0` | `git show 790561d4:tools/round-36/c2-counter.py \| sha256sum` | `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` (identical) |
| same at base `cab59f22` | `git cat-file -e cab59f22:tools/round-36/c2-counter.py` | absent (exit 128) — instrument postdates the base, as expected; the counter run below executes the freeze-identical blob against **base git objects** |
| `plans/round-36-claims.md` | `sha256sum` vs `git show 790561d4:plans/round-36-claims.md \| sha256sum` | both `2c9cbde76cc0af8fd2b3cbd99cda7e149a17a2daea0b093669778622fa61d6c0` |
| lane HEAD at run time | `git rev-parse HEAD` | `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (not used for measurement) |

`git status --porcelain -- SCORECARD.md SHONEN.md tools/round-36/c2-counter.py plans/round-36-claims.md`
printed nothing (exit 0).

## 1. Frozen C2 counter selftest

```
S=/fast/scratch/hyaku/kaidoku-r36/R36ExecRecountC2; mkdir -p "$S"; export TMPDIR="$S"
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-36/c2-counter.py --selftest
```

Exit **0**. Stdout verbatim:

```json
{"selftest": "c2-counter", "cases": 13, "green_ok": 1, "red_ok": 12, "failures": []}
```

13 cases = 1 green + 12 red, matching the claims file's "13 cases (1 green; red: …)" enumeration.
The selftest is a mechanism check of the counter on synthetic fixtures; it says nothing about the
real surface (that is what §2–§3 measure).

## 2. Frozen counter at the base

```
python3 -I -B tools/round-36/c2-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev cab59f221fe19726b5692bfa4d9a9679e96b8a73 \
  --base cab59f221fe19726b5692bfa4d9a9679e96b8a73 \
  --json-out "$S/c2-base.json"
```

Exit **1** (target not met). Stdout verbatim:

```json
{"assertion_mismatches": [{"check": "O1 coverage mapped/files", "observed": [122, 122], "stated": [116, 116]}], "guards_ok": false, "met_target": false, "mismatches": 3, "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73", "unresolved": [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B/"], ["shonen:No cross-domain bleed (PROVINCE.md still accurate)", "ScoutSkillPlacement.md"]]}
```

Receipt fields that matter (`c2-base.json`):

- `mismatches: 3`, `assertions: 7`, `met_target: false`, `guards_ok: false`.
- `pointers: 34`; `unresolved`: exactly the two rows above.
- `assertion_mismatches`: only `O1 coverage mapped/files`, stated `[116, 116]`, observed `[122, 122]`.
- `guards`: `base_pointers: 34`, `missing_units: []`, `pointers_not_fewer: true`,
  `base_unresolved: [["cap:…REA 6.5.0","receipts-B"], ["shonen:No cross-domain bleed…","ScoutSkillPlacement.md"]]`,
  `unrepaired`: the same two entries (so `guards_ok` is false for the base-vs-base run; expected —
  base == rev means nothing is repaired).
- `observed.command_a: {"mapped": 122, "knowledge_files": 122, "resolved_rules": 17, "rule_blocks": 17}`;
  `observed.command_b: [9, 9]`; `observed.craft_range: [81, 314]`; `observed.adjacent_range: [97, 118]`.
  These other six assertions show no mismatch at the base.

Determinism: the same command was run twice to the same `--json-out`; stdout and receipt were
byte-identical, receipt sha256 `9cc4840a73daba0f23e417648616b9a6519c54a19f31f16540867e1bd8061767`.

## 3. Independent recompute (no counter code)

Written fresh in scratch (`recount_c2.py`); `tools/round-36/c2-counter.py` was **not** imported,
executed, or textually copied. Method:

1. Read `SCORECARD.md` and `SHONEN.md` at the base with `git show <rev>:<path>`.
2. Units: table rows of `## Owned axes` (header `Axis`) and of the `## Capabilities` table (header
   `Capability`, stop at the first non-table line); SHONEN boxes are `- [x| |~]` lines plus their
   two-space-indented continuation lines.
3. Pointer tokens: every backticked token in those units that parses as `<path>[:<N>[-<M>]]`, is not
   absolute (`/`, `~`), and whose path contains `/` or ends in `.md`. Resolution = `git cat-file -e
   <rev>:<path>` on the path with trailing `/` stripped; with a line range, the blob's
   `splitlines()` count must satisfy `1 <= lo <= hi <= count`.
4. Coverage half of command A, per `SCORECARD.md` `## Measurement recipes` A: knowledge-file stems from
   `git ls-tree -r --name-only <rev> -- corpus/knowledge` (`.md` only); mapped tokens =
   `2026-10-\d{2}-[a-z0-9-]+` in the `## Coverage map` section of `corpus/README.md`; observed =
   `(len(files & mapped), len(files))`; stated = first `(\d+)/(\d+) knowledge files mapped` in the
   `owned:coverage` row.

Core of the script (scaffolding `run/blob/exists` implemented with `subprocess.run(['git','-C',root,…])`):

```python
def section_rows(text, heading, header_cell, table_only):
    lines = text.splitlines(); i = lines.index(heading) + 1
    rows, seen_table = [], False
    for line in lines[i:]:
        if line.startswith('## '): break
        if line.startswith('|'):
            seen_table = True
            first = line.strip().strip('|').split('|')[0].strip()
            if set(first) <= set('-: ') or first == header_cell: continue
            rows.append(line)
        elif seen_table and table_only: break
    return rows

def shonen_boxes(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r'^- \[[ x~]\] (.*)$', line)
        if m: cur = m.group(1).strip(); out[cur] = line
        elif cur is not None and line.startswith('  '): out[cur] += '\n' + line
        else: cur = None
    return out

def scan(text):
    for tok in re.findall(r'`([^`\s]+)`', text):
        if tok.startswith('/') or tok.startswith('~'): continue
        m = re.fullmatch(r'([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?', tok)
        if not m: continue
        path = m.group(1)
        if '/' not in path and not path.endswith('.md'): continue
        yield tok, path, m.group(2), m.group(3)

def resolves(path, first, last):
    p = path.rstrip('/')
    if not p or not exists(p): return False
    if first is None: return True
    n = len((blob(p) or '').splitlines())
    a = int(first); b = int(last) if last is not None else a
    return 1 <= a <= b <= n

# coverage half of command A
paths = run('ls-tree','-r','--name-only',rev,'--','corpus/knowledge').stdout.splitlines()
files = {PurePosixPath(p).stem for p in paths if p.endswith('.md')}
cov = blob('corpus/README.md').split('## Coverage map\n',1)[1].split('\n## ',1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', cov))
m = re.search(r'(\d+)/(\d+) knowledge files mapped', units['owned:coverage'])
stated = [int(m.group(1)), int(m.group(2))] if m else None
observed = [len(files & mapped), len(files)]
```

Output (`python3 -I -B recount_c2.py <lane> cab59f22…`, exit 0), abridged to the decision fields:

```json
{"rev": "cab59f221fe19726b5692bfa4d9a9679e96b8a73", "units": 15, "pointers": 34,
 "per_unit": {"owned:coverage": 2, "owned:depth": 2, "owned:calibration": 2,
              "cap:pre-registered two-lane live battery on REA 6.5.0": 3,
              "cap:version-symmetry battery on REA 6.4.0": 2,
              "cap:config custody pre/post-pair for live-probe rounds": 2,
              "cap:contained user-service analyze of oversized PEs (analyzer-disable recipe)": 2,
              "cap:cross-pin evidence-ID attribution for saved REA envelopes": 4,
              "cap:curated source registry for existing REA frontier": 2,
              "cap:local raw-quote/heading regression audit": 1,
              "cap:retained REA Ghidra-session log capture": 2,
              "shonen:SKILL.md contains real decision tables, error patterns, checklists, cited sources": 2,
              "shonen:At least one end-to-end domain task executed and logged in LOG.md": 2,
              "shonen:Instructions executable by an agent without oral context": 1,
              "shonen:No cross-domain bleed (PROVINCE.md still accurate)": 5},
 "unresolved": [["cap:pre-registered two-lane live battery on REA 6.5.0", "receipts-B/"],
                ["shonen:No cross-domain bleed (PROVINCE.md still accurate)", "ScoutSkillPlacement.md"]],
 "coverage_stated": [116, 116], "coverage_observed": [122, 122], "coverage_mismatch": true,
 "missing_from_map": [], "dangling_in_map": []}
```

The full per-pointer list produced 34 entries, of which exactly the two above failed; all 32 others
resolved, including `SKILL.md:81-314` (range inside the file), `PROVINCE.md:97-118`, `PROVINCE.md:8-14`,
`PROVINCE.md:24`, `receipts/`-style directory pointers that do exist, and paths inside `.ufo/waves/`.

Independent corroboration of the two failures:

- `git cat-file -e cab59f22:receipts-B` → `fatal: path 'receipts-B' does not exist`, exit **128**.
  The directory exists only nested: `git ls-tree -r --name-only cab59f22 | grep receipts-B/` →
  `.ufo/waves/luna-round-6/receipts-B/…` (so the bare pointer is unresolved, not a missing document).
- `git cat-file -e cab59f22:ScoutSkillPlacement.md` → `fatal: path … does not exist`, exit **128**;
  the file exists only at `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`.
- Coverage: `git ls-tree -r --name-only cab59f22 -- corpus/knowledge | grep -c '\.md$'` → **122**;
  distinct `2026-10-\d{2}-[a-z0-9-]+` tokens in the `## Coverage map` section → **122**; set difference
  empty both ways (`missing_from_map: []`, `dangling_in_map: []`).

### 3a. Command A run verbatim from the card

The `## Measurement recipes` A body (SCORECARD.md lines 94–122 at the base) was extracted with
`git show cab59f22:SCORECARD.md | sed -n '94,122p'` and run as `python3 - cab59f22… < recipe`:

```json
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 122, "mapped": 122, "missing": [], "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73",
 "rule_blocks": 17}
```

Exit 0. `mapped=122`, `knowledge_files=122` against the row's stated `116/116`.

### 3b. Second, looser extraction variant

To test the token grammar's influence, the same surfaces were re-scanned with a different filter:
parse the optional `:N[-M]` suffix first, then keep any token whose *path* contains `/` or ends in
`.md`, with **no** character whitelist on the path. Result: 15 units, **34** pointers, and again exactly
`receipts-B/` (capability row) and `ScoutSkillPlacement.md` (SHONEN box 4) unresolved.

## 4. Agreement

| Quantity | Frozen counter | Independent recompute | Agreement |
|---|---|---|---|
| units | 15 | 15 | yes |
| total pointers | 34 | 34 (34 under the looser variant too) | yes |
| unresolved pointers | `receipts-B/`, `ScoutSkillPlacement.md` (2) | identical 2, same units | yes |
| O1 stated coverage | 116/116 | 116/116 | yes |
| O1 observed coverage | 122/122 | 122/122 | yes |
| mismatch total at base | 3 (2 pointers + 1 count) | 3 (2 pointers + 1 count) | yes |
| receipt determinism | identical stdout/receipt on rerun | n/a | yes |

**No disagreement found.** The base exhibits exactly the three mismatches the frozen predicate claims
(2 unresolved backticked pointers + the stale `116/116 knowledge files mapped`), and the counter's
`unresolved` / `base_unresolved` / `guards` fields are consistent with the independent scan.

## 5. Limits (recorded, not repaired)

- The selftest is a mechanism check (1 green / 12 red synthetic cases). It does not validate the
  counter against the real surface; §2–§3 do, and only for the three named base mismatches.
- I independently recomputed only the coverage half of command A and the pointer-resolution class, as
  assigned. `O2 depth resolved/rules`, `O3 calibration aligned/total`, `O4 SHONEN rule count`,
  `R1`–`R3` range checks and command B were **not** independently re-derived; the counter reports them
  clean at the base (`17/17`, `9/9`, ranges `81-314` / `97-118`).
- The pointer grammar (backticked token, optional single range `:N` or `:N-M`, path-or-`.md` rule) is a
  re-derivation of the predicate's "backticked repo pointer" wording. The looser variant in §3b, which
  removes the character whitelist, returns the same 34/34 and the same two failures, so the result is
  insensitive to that choice on this surface.
- The counter blob is absent at the base commit; "frozen counter" here means the freeze-commit-identical
  blob (sha256 `f079aff1…`) executed with `--rev cab59f22`. Identity is recorded above.
- No defect in the frozen counter or predicate was found in this seat's scope. Nothing was changed;
  no repair attempted.
- `receipts-B` is unresolved because the row's pointer lacks its `.ufo/waves/luna-round-6/` prefix, and
  `ScoutSkillPlacement.md` lacks `.ufo/waves/round-30/w1/`; both target documents do exist elsewhere in
  the tree at the base. This is the claim's stated base state, not a new finding.

## 6. Bounds compliance

- Wrote only this report file; no other lane write, no fleet/sibling/`shokuknow` write.
- No VCS mutation: only `git show`, `cat-file`, `ls-tree`, `rev-parse`, `status`. No `git add/commit/
  checkout/reset/stash/pull/push`, no jj.
- Scratch confined to `$S` with `TMPDIR=$S`; removed on completion. No `/tmp` files created.
- No subagents, no background jobs, no `agent://all` messages, no REA invocation, no pacman/pip/npx
  installs (nothing was installed or upgraded).
