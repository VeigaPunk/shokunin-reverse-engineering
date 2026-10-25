# R35ReviewerC1 — C1 false accepts/rejects (round 35, wave one)

Item: review C1 false accepts/rejects. Scope: `tools/round-35/c1-coverage-counter.py` (frozen pin
`e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220`) against the frozen predicate
P35-c1 and the plan after-state in `plans/round-35-claims.md`. Advisory only; no production file,
counter, claim, or VCS state was modified. Experiments ran in /tmp synthetic repos only.

## Instrument integrity (verified before findings)

- Worktree counter sha256 `e28792c7…` == blob at tip `3ecf4298` == blob at canonicalize commit
  `2323d197`; `git show a85ca674…:tools/round-35/c1-coverage-counter.py | sha256sum` =
  `018e96d0…` (pre-final bytes). Pin is consistent at tip.
- Canonical claims file: worktree `1b985540…` == blob at `2323d197` (frozen object read, not a
  dirty variant). Counter PREDICATE constant == C1 `predicate` field byte-for-byte
  (`predicate_field_equal: True`).
- Counter reads only `git show`/`git ls-tree` at `--rev` (immutable objects); no worktree, REA,
  or network reads in the check path. `--selftest` → `ok, green=0 red=1`.
- Base do-nothing control: `python3 -I -B tools/round-35/c1-coverage-counter.py --root . --freeze
  2323d197 --rev aa04633a…` → exit 1, eight named failures (entry_missing ×2,
  registry_row_missing ×2, province_missing ×2, readme_missing ×2). Canonical claims file is
  absent at base (exit 128 on `git show base:…`), so `--freeze` must be `2323d197` or later.
- S125/S129 occur 0 times in `corpus/SOURCES.md` at tip → claim data not yet landed, no score yet.

## Findings by severity

### F1 [HIGH — false accept] "opens with the provenance trio" is not enforced
`check()` (tools/round-35/c1-coverage-counter.py:104-116) tests `re.search(r"(?m)^source\s*:",
body)` and siblings — the trio may sit anywhere at line start, not at the file open. The frozen
predicate itself says "each entry exists, opens with the provenance trio and cites its new
SOURCES row". Repro (V2, exit 0 `C1_CLEAN`): entry body =
`"We studied the jsc2js mapper contract extensively.\n\n" + trio`. The red selftest only deletes
the trio entirely, and the plan's junk control ("lacks the trio or cites the wrong row") also
only covers absence — so no frozen control catches mid-file placement. Implementation is weaker
than the predicate it certifies.

### F2 [MEDIUM — false accept] duplicate SOURCES rows: last match wins
`rows[m.group(1)] = cells` (:122) lets a later duplicate mask an earlier failing row. Repro (V5,
exit 0): failing S125 row (`status=todo`, `opened=2026-10-01`, foreign used-by) followed by a
fully passing S125 duplicate → `C1_CLEAN`. No duplicate-id detection.

### F3 [MEDIUM — receipt defect] `checks` map in `--json-out` receipts is always all-True
Receipt is built as `{f"c1_{i}": (f not in fails) …}` over bare category names
("entry_exist", "trio", …) while `fails` holds prefixed strings ("entry_missing:…") — membership
never matches. Demonstrated: genuinely failing run (exit 1, `pass=false`, `failing` len 8)
still emits `checks: {c1_0…c1_5: true}` for all six. Kill rule and exit code carry the real
signal, but any consumer parsing `checks` sees full green. The selftest cannot catch this (it
asserts return codes only). Live defect at the pinned hash.

### F4 [LOW-MEDIUM — false accept vs plan after-state] no section scoping on PROVINCE/README
Plan after-state requires a "Round-35 Core-addition table row" and the README "coverage map";
counter checks bare substring presence anywhere (stems in PROVINCE.md, filenames in
corpus/README.md). Repros (both exit 0): V3 — stems appear only under a `## Frontier` bullet, no
Round-35 table; V4 — filenames appear only in a `## Changelog` line, no coverage-map table. The
frozen predicate's operational wording ("PROVINCE.md and the README coverage map hold both entry
filenames") is weaker than the plan prose; the counter implements the weaker reading. The
assimilation-duty surface (PROVINCE Frontier bullet "`.jsc` → source mapping") is likewise never
checked — an entry pass does not require the frontier bullet to exist at all.

### F5 [LOW — false accept by construction] zero-content entries pass
Entries consisting of only the three trio lines pass every check (V6, exit 0); the selftest's own
green fixture is exactly such a trio-only entry. Within the frozen scope (the declared junk
control is trio-absence/wrong-row only), so recorded as residual, not a bug against the freeze.

### F6 [LOW — process, disclosed] pinned counter bytes first appear in the freeze commit itself
The plan requires instruments "committed before `claims.json`". `instrument_supersessions` names
`a85ca674` as finalizing the counter, but that blob is `018e96d0…`; the final bytes (`e28792c7…`,
the `--freeze`-path fix) first appear in `2323d197` — the same commit that adds
`claims-canonical.json`. Honestly disclosed in `.ufo/waves/round-35/freeze-status.md`
(INSTRUMENT_REVISED debt; "C1/C2 were not scored before the final freeze"; no re-freeze). No
score has used non-pinned bytes; claim gate unaffected. Recorded for the honesty ledger, not as
a hidden defect.

### F7 [LOW — failure-class mislabel] unusable `--rev` reports as claim failure, not unevaluable
`--rev doesnotexist` with a valid `--freeze` → exit 1 with entry/row/province/readme "missing"
failures (V8b); `ls_tree`/`show` errors are indistinguishable from absent data. Exit 2 is
reserved for claims-file problems. A scorer typo would masquerade as a hard kill; harmless if
the rev is pinned by hash.

### F8 [NOTE] predicate gate is substring containment
`PREDICATE not in json.dumps(claims_obj)` accepts a claims file whose predicate field merely
contains the constant. The actual canonical field is byte-equal, so no live mismatch; noted as a
weaker-than-byte-identity gate shape.

## False-reject probes (no live defect)

- V7: used-by written stem-only (`2026-10-25-r35-jsc2js-mapper-contract`) → exit 1
  `registry_usedby_missing`. Convention-coupled, but the registry convention (S001… at
  `corpus/SOURCES.md`) is full repo-relative paths, matching the counter; low risk.
- `ROW_RE` requires exactly 11 pipe-delimited cells; an escaped `\|` inside a cell would shift
  columns and likely produce a false reject. Existing rows' URLs contain no pipes; low risk.

## Verified-good

Selftest green/red ok; base do-nothing exits 1 with named failures; predicate byte-match;
instrument pin matches tip and worktree; immutable-object-only reads; `opened` and `status`
cells checked exactly; per-entry row↔entry cross-wiring fails (S125 used-by must name the
mapper-contract path and vice versa).

## Residual risk and verification gaps

- F1/F4 mean the frozen counter certifies a weaker state than the predicate/plan sentence; if
  data lands with mid-file trios or misplaced mentions, the counter would pass a state the
  claims text does not describe. Per kill discipline this cannot be repaired by re-freeze; the
  residual belongs to the scorer's honesty, not the instrument.
- No data revision exists yet (S125/S129 absent at tip), so no green-at-data behavior was
  observed; everything above is synthetic-repo evidence plus base-rev control runs.
- `lsp` device not mounted in this seat; static claims rest on full-file reads of the 197-line
  counter plus execution repros (stronger than grep-only evidence).
- Escaped-pipe SOURCES cells and non-`2026-10-25`-prefixed `opened` variants were analyzed, not
  executed.

Key commands (cwd = lane root):
- `python3 -I -B tools/round-35/c1-coverage-counter.py --selftest` → `C1_SELFTEST: ok / green=0 red=1`
- `python3 -I -B tools/round-35/c1-coverage-counter.py --root . --freeze 2323d197 --rev aa04633a686d49756763b1feed4be6830d5bb479` → exit 1 (do-nothing control red)
- `git show 2323d197:.ufo/waves/round-35/claims-canonical.json | sha256sum` → `1b985540…` == worktree
- V2/V3/V4/V5/V6 synthetic repos → exit 0 `C1_CLEAN` (false accepts); V7/V8b → exit 1 (documented)
