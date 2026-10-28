# R46W1RegL — three instrument-registry rows, verified from source, plus a predicate attack on R46-C2

Seat `R46W1RegL`, round 46 wave 1, lane `kaidoku`. Freeze read: `3182047` (as instructed);
the lane has since re-frozen twice more (see §5). Lane tree untouched; read-only git only.

## 1. Deliverable

`.ufo/waves/round-46/w1/R46W1RegL/rows.md` — three rows, exact 7-cell house format, cell 0
exactly the backticked path, verdict maps binding `0=`, `1=`, `2=`. Re-read from disk and
checked cell-by-cell (7 cells, backticked cell 0, `{0,1,2}` on cell 3, no stray pipes).

```
| `tools/round-41/sqfs-list.py` | probe - independent SquashFS 4.0 oracle reader (LE, standard BE, AVM layout) emitting a regular-file TSV of relpath, sha256 and size, a non-regular TSV, one-file extract and an inspect JSON summary | 0=enumerated every entry, or extracted the named file, or every self-test case passed; 1=a self-test case failed; 2=could-not-evaluate: unreadable image, bad magic, unsupported compression, truncated image, or a usage error | python3 -I -B tools/round-41/sqfs-list.py --selftest | none | the --files and --nonregular TSV paths, the --out extract path, and self-test temp images | kaidoku |
| `tools/round-43/c1-counter.py` | gate - R43-C1 depth counter: runs the frozen v4 triage interpreter and the frozen independent evaluator over the seeded held-out envelope set and requires every label and action pair to agree plus every declared binding true | 0=met_target true, every held-out pair matched and every binding true; 1=not met: at least one pair miss or one binding false, the receipt still written; 2=could-not-evaluate: frozen_path_changed, freeze not an ancestor of rev, unknown revision, absent or unparsable manifest, or a frozen tool failing to run | python3 -I -B tools/round-43/c1-counter.py --selftest | tools/round-42/sqfs-triage-v4.py and tools/round-42/indep-eval-v4.py pinned at anchor d1681696, with corpus/evidence/round-43/c1/heldout/ | the --json-out receipt and a private scratch dir under HYAKU_SCRATCH removed at exit | kaidoku |
| `tools/round-46/registry.py` | gate - R46-C2 calibration counter: scores the marker-bound SKILL instrument-registry section against tools/round-46/census.json, requiring exact cell-0 path equality, the house header, a bound verdict map per row and presence at the measured revision, and rejects all seven forgery classes | 0=met: no unregistered, thin or absent-at-rev path and the battery reports seven forgeries green under v1 and none under v2; 1=not met: an unregistered, thin or absent-at-rev path, or a battery count off target; 2=could-not-evaluate: missing or doubled markers, absent census, absent SKILL.md at rev, frozen_path_changed, or no scratch root | python3 -I -B tools/round-46/registry.py --selftest --root . --freeze 0 --rev 0 | tools/round-46/census.json | the --json-out receipt and a private scratch dir under HYAKU_SCRATCH for the forgery battery | kaidoku |
```

Formatting note for the paste: the seat spec forbids backticks outside cell 1, so cells 2–6
are plain. The landed section wraps path tokens in backticks; wrapping cell 5's two paths and
cell 4's command changes nothing the counter reads (`strict_cell` looks at cell 0 only,
`strict_exit` at cell 2).

**These rows pass the real parser, not just a regex of mine.** One-commit fixture
(`git -C $D rev-parse --show-toplevel` asserted equal to `$D` before the first commit),
`SKILL.md` = house header + my three rows between the two `instrument-registry v2` markers,
census = my three paths, the three tool paths present:

| instrument | exit | receipt |
|---|---|---|
| `registry.py@3182047 --profile v2 --no-battery` | 0 | `registered` 3, `unregistered` [], `thin` [], `absent_at_rev` [], `failing` [], `met_target` true |
| `registry.py@F4 (0425224) --profile v2 --no-battery` | 0 | same verdict; F4 is the instrument revision the L1 scored with |
| negative: one verdict cell → `0 rows, 1 column, 2 bytes` | 1 | `thin=['tools/round-43/c1-counter.py']`, `failing=['thin verdict-map cells: 1']` |

The negative control matters: without it, "my rows pass" would only prove the parser runs.

## 2. Where each exit meaning comes from (source at the freeze, never guessed)

`tools/round-41/sqfs-list.py` — the only producer of `1` is `1516`
`return 0 if bad == 0 else 1` at the end of `run_selftest`; `main` returns `0` on a written
enumeration or extraction, and both other failure surfaces are `2` (`ap.error` at `1547` and
`1565`, `SqfsError` at `1551`/`1573`). Executed: `--selftest` → 16/16, exit 0; the frozen
command verbatim (`python3 -B tools/round-41/sqfs-list.py --selftest`) → 16/16, exit 0;
no args → 2; `/nonexistent.sqfs` → 2; a copy with `228: b'hsqs'` → `b'Hsqs'` → `13/16
passed`, exit 1. Exit 1 is a **self-test-only** branch; the row says so.

`tools/round-43/c1-counter.py` — its own docstring `100–102` states the map: `0` target met,
`1` not met "(a pair miss or a binding false)", `2` unevaluable (`frozen_path_changed` first).
Code: `2545` `met = bool(matched == N and bindings_ok)`, `2555`
`res['exit_code'] = 0 if met else 1`, the `2` path at `2596–2626`, usage `2` at `2588`.
The key that names false bindings is `bindings_false` (`2548`, printed `2622`) — there is no
`failing` key anywhere in the file. Executed: `--selftest` → `SELFTEST cases=91 pass=91
fail=0`, exit 0; no args → 2 with `usage: --root --rev --freeze required (or --selftest)`.

`tools/round-46/registry.py` — docstring: "Exit codes: 0 met; 1 not met; 2 could-not-evaluate."
`score()` returns `(0 if not failing else 1)` (`218`); `2` comes from `freeze_state` (`2`
`frozen_path_changed`, unknown revision, non-ancestor freeze), `load_scope` (absent/unreadable
census), `gate.scratch`, and `395` "SKILL.md absent at rev". Executed: `--selftest` **bare** →
**2** (`--root/--freeze/--rev` are `required=True`, so argparse rejects before `426` runs);
`--selftest --root . --freeze 0 --rev 0` → `REGISTRY_SELFTEST: cases=12 failures=0`, exit 0.

No CLI here takes an exit code outside `{0,1,2}`. (`c1-counter.py` embeds fixture scripts that
`sys.exit(3)` at `2969` and `sys.exit(9)` at `3026`; those are strings written into one-commit
fixtures, not this tool's exit surface.)

## 3. The C2 predicate accepts rows that carry no information (measured)

`registry.py:46` is `EXITMAP = re.compile(r"\b([012])\s*[=:]")`, and `196–202` requires only
`set(EXITMAP.findall(cell)) == {"0","1","2"}`. The digits are bound; the **meanings are not
read at all**, and no cell except cell 0 is required to be non-empty. Against the frozen F4
instrument, with the battery on:

- the `c1-counter.py` row's verdict map replaced by `0=banana; 1=banana; 2=banana` →
  `met_target` true, `thin` [], exit 0;
- all three rows rewritten `| \`path\` |  | 0=banana; 1=nope; 2=whatever |  |  |  | kaidoku |`
  (purpose, self-test, pinned path and write scope **all empty**) → `registered` 3,
  `unregistered` [], `thin` [], `failing` [], `met_target` true, exit 0;
- same artefact with the seven-forgery battery: `forgeries_total` 7, `v1_green` 7,
  `v2_green` 0, `genuine_green` 1, exit 0.

So an instrument registry consisting of three rows that state nothing satisfies R46-C2 in
full, battery included. This is not a violation of the claim — clause 4 says "enumerates `0=`,
`1=`, `2=`", and the kill rule is about `0 of 1, 2` — it is the **same defect class the round
was built to close** (`R45-CL14 d`, "accepted any cell containing 0, 1 and 2"), narrowed from
"contains the digits" to "contains the digits followed by `=`" and left otherwise open. The
round-45 artefact scored green on a six-fenced-row forgery; the round-46 artefact scores green
on rows whose every field is blank. **The claim is met as written; the measure is still
non-discriminating on content.** Proposed routing (not implemented, per seat scope): require
each of cells 1 and 3–6 to be non-empty and require the verdict map to carry a fixed token per
code (e.g. `0=met`, `1=not met`, `2=could-not-evaluate`, or a declared synonym table), and add
one battery mutation "vacuous row".

## 4. The three rows are already landed — here is what the landed versions get wrong

Commit `781e19ae` landed a 38-row section and `1e32827b` records "C2 38 of 38 registered" at
F4; all three of my paths are in it (`SKILL.md:1709`, `:1722`, `:1735`). The landed rows pass
the predicate; they were not audited against the source. Mine were. Deltas:

- **`SKILL.md:1722` (`c1-counter.py`), cell 3 — two real errors.** "1=not met, at least one
  binding false and named in `failing`": (a) exit 1 is also produced by a **pair miss with
  every binding true** (`2545`, and the instrument's own docstring `101` says "a pair miss or
  a binding false"); (b) there is no `failing` key — the field is `bindings_false` (`2548`,
  `2622`). A reader following that row would look for a key the tool never writes.
- **`SKILL.md:1722`, cell 3 — the `2` examples omit `frozen_path_changed`**, which is the one
  reason this lane actually hits (it fired on my first real-lane probe, §5).
- **`SKILL.md:1722`, cell 5 — pinned set incomplete**: `tools/round-42/indep-eval-v4.py`
  (`149`) is the evaluator the entire claim is measured against and is absent; so is the
  held-out evidence root. "at the round-43 freeze" is also imprecise — the anchor is
  `d1681696`, the round-42 freeze (`160`).
- **`SKILL.md:1735` (`registry.py`), cell 6** — "writes only `--json-out`" omits the battery's
  scratch tree (`gate.scratch` under `HYAKU_SCRATCH`). Cell 3 omits "absent SKILL.md at rev"
  (`395`); cell 3's `1`/`2` split is otherwise correct, including markers under `1`.
- **`SKILL.md:1709` (`sqfs-list.py`)** is accurate. Its `0=` omits the self-test-green case
  (`1516`) and its write scope omits the selftest's temp images; both omissions, not errors.

Recommendation: replace row `1722` outright; refreshing `1709`/`1735` is optional accuracy.

## 5. Freeze chain: the declared freeze cannot score (already recorded as `M46-3`)

`plans/round-46-claims.md` defines the freeze as "the commit that first contains this file and
`tools/round-46/`" — that is `3182047`. Three later commits touch the frozen directory:
`50862e4a` (`attest.py`, `gate.py`, `registry.py`), `65678df0` (`attest.py`), `04252247`
(`registry.py`, F4). Measured:

```
registry.py@3182047 --root <lane> --freeze 3182047 --rev 8757865679e6 --profile v2 --no-battery
→ exit 2, reason=frozen_path_changed,
  touched=[attest.py, gate.py, registry.py], restored=<same three>, blob_changed=[tools/round-46/]
```

The claims file itself is unchanged (`git diff --stat 3182047 HEAD -- plans/round-46-claims.md`
empty), and the directory is clean at F4 (`git diff --stat 04252247 HEAD -- tools/round-46/
plans/round-46-claims.md` empty). So the scoreable freeze is `04252247`, not `3182047` — which
is what the L1's own receipts use (`l1/scores/c2-at-F4.json`, `c1-at-F4.json`, both
`freeze=rev=0425224`, both met). This is `corpus/lessons/round-46.md:19` (`M46-3`);
I am confirming it from the counters, not claiming it as new.

## 6. Two claims-file values that the instrument contradicts

`plans/round-46-claims.md:194` — "`registry.py --selftest` prints `cases=11 failures=0`".
At the freeze: the bare invocation **exits 2** (argparse requires `--root/--freeze/--rev`) and
the runnable form prints **`cases=12 failures=0`**. The source has twelve `case(` calls
(`462–524`), in both `3182047` and F4. `attest.py`'s `cases=15` at `:192` does match its source.
Neither value is a predicate clause, so no score moves; the "Satisfiability preflight" paragraph
is simply not true as written, and a reader who pastes `registry.py --selftest` gets a usage
error. The landed row already avoids this by passing the required args — worth keeping.

## 7. Risks

- **Content-free registries score green** (§3). Until clause 4 binds meanings, "38 of 38
  registered" is a statement about row count and spelling, not about the instrument set.
- **Row accuracy is unmeasured.** One landed row names a receipt key that does not exist; the
  counter cannot see that, so nothing in the pipeline will catch the next one.
- **`SKILL.md` is unfrozen**, so replacing rows means a new commit and a re-score; expect C2 to
  stay met (structure unchanged) — the batch is safe, and §3's vacuous rows stay green under
  it, so the re-score does not prove the fix.
- I did not run the battery against the **real lane** (only against my fixture): it would
  mutate copies of the landed section, and the landed receipts already carry
  `forgeries_total` 7 / `v1_green` 7 / `v2_green` 0 / `genuine_green` 1
  (`l1/scores/c2-at-F4.json`). The C1 side is not mine and was not run.

## 8. What was not run

- `c1-counter.py` exit 1 — needs a complete round-43 measurement tree; read from source
  (`2545`, `2555`) and the instrument's docstring (`101`) instead.
- `attest.py --selftest` — out of seat.
- Full-battery runs against the real lane — out of seat (see §7).

Receipts: `.ufo/waves/round-46/w1/R46W1RegL/receipt.md` (command, exit code, stdout sha256,
UTC for every run). No installs, no PATH changes, no commits.
