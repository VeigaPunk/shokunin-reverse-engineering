# ExecC3 — independent R71-C3 rederivation

Axes: operability; independent reproducibility; scope safety.

## Scope and method

Read the round-70 verifier spot-check first, including its seven routed items; only R71-C3 is adjudicated here. Read `plans/round-71-claims.md:115-151` and `claims[2]`. Base: `82c8e620c9222fb218aa0260570a3765da2afb44`; operative freeze: `b827a8b5d54f2885ec9be7786389f356c59226ce`.

`rederive.py` is my own parser and retained reproduction driver: regex split on pipes not immediately preceded by backslash, replace `\|` with `|`, trim cells, and drop the header/delimiter inside the unique registry markers. No import or invocation of the census parser contributes to the independent result. This immediate-backslash rule matches the frozen instrument; general even/odd runs of backslashes were not an acceptance target or independently tested. Paths are checked against a read-only recursive `git ls-tree` inventory at the base. Every row's absolute source line, cell count, tool path, existence, pinned/write/owner reconstruction and original line are retained in `independent-base.json` (88 entries).

The frozen census was extracted with `git show` and executed from scratch, rather than trusting moving worktree bytes. SHA256 `a7746d2ade8946c112ed097268df7ba905f0632a0af8b9e3375dc6ea7c42d528` matches the operative freeze container's instrument pin. The legacy census was extracted at the base; SHA256 `a7538e5f5174b5f69cc7537fc1bcdf97cc2f062747123d0eb6f57e60e9acc7c0` also matches the frozen container's dependency pin. Exact argv, cwd and exit codes are in `commands.json`; deleted scratch argv paths are run provenance, not retained evidence.

## Independent base result

88 rows, 88 unique paths, all 88 paths present at the base; 78 seven-cell rows, four eight-cell rows, six six-cell rows. No other shape occurs. Base SKILL.md SHA256: `b6bc5e4c645420594653894cef29141c34cee258ea9ab0550106695485419610`.

Four eight-cell rows at base SKILL.md lines 1862–1865: `tools/round-69/{packed-elf,mutation-check,contract-probe,controls}.py`. Each has owner `kaidoku`. Exact reconstructed cells (the `|` below is part of the pinned string, not a new column):

- **packed-elf.py** pinned = “`.ufo/waves/round-69/l1/pre/` (base arms), `.ufo/waves/round-69/w1/` (wave evidence); scratch under $HYAKU_SCRATCH|UPX_SHA256_PIN, UPX_VERSION_PIN, the CARRIERS table (sha256, floors, stub ceilings) and REA_PKGJSON_SHA256 in the source, all enforced”; write = “--json-out receipt and --work scratch; every copy is rebuilt inside --work and deleted”.
- **mutation-check.py** pinned = “`.ufo/waves/round-69/l1/pre/c1-at-base.json` (5 survivors) and the landing receipt (0)|the PATCH_SETS table (each patch site and its expected arm-false case) in the source”; write = “--json-out receipt only; every mutant lives in scratch”.
- **contract-probe.py** pinned = “`.ufo/waves/round-69/l1/pre/c2-at-base.json` (0 of 6) and the landing probe receipt (6 of 6)|UPX path, PACKING_MODE and the six arm ids in the source; the instrument under test is named by --rev and --tool”; write = “--json-out receipt only; fixtures live in scratch”.
- **controls.py** pinned = “`.ufo/waves/round-69/l1/pre/controls-at-base.json`|the four tool paths in TOOLS and BASE_RECEIPT in the source”; write = “--json-out receipt only; synthetic receipts and scratch fixtures”.

The six six-cell rows at base lines 1867–1872 are `tools/round-70/{packed-elf,mutation-check,contract-probe,seam-probe,forged-receipts,controls}.py`. In every case the pinned slice `[4:-2]` is empty: `pinned=""`, defect exactly `['pinned-empty']`. The positional rule consumes the intended pinned text as write and the final authored text as owner; the full displaced values are retained per row in `independent-base.json`. Thus accepting these as merely another multicell variant would hide a real omitted-column defect.

## Scratch-only repair simulation

Copied base SKILL.md into the exclusive scratch root and appended ` kaidoku |` after the existing trailing pipe of only those six round-70 rows. `six-row-repair.json` retains exact old/new lines. The original and repaired registries were re-parsed with my parser against the same base inventory:

- 88 rows; 88 unique existing paths; zero nonconformant rows; zero duplicate paths.
- Shapes after repair: 84 seven-cell rows and the same four eight-cell rows.
- Exactly six original lines changed. No round-69 row changed, including the additional seven-cell provenance-check row.
- `diff -u round69-base.lines round69-repaired.lines` exited 0 with empty stdout/stderr. Both files retain all five round-69 lines, proving the four eight-cell rows stayed byte-identical too.

This is a simulation, not a landed repair or an after-receipt at the record commit. `independent-repaired.json` retains the complete repaired parse, and `summary.json` records counts and line identity.

## Frozen and legacy executions

| command target | exit | observed result | retained evidence |
|---|---:|---|---|
| frozen census, base, `--generate` | 1 | 88 rows/88 paths; four multicell rows; six `pinned-empty`; duplicates empty; ok false | `census-base.json`, matching stdout/stderr |
| frozen census, freeze, `--generate` | 1 | 88 rows/88 paths; same four multicell rows and six `pinned-empty`; duplicates empty; ok false | `census-freeze.json`, matching stdout/stderr |
| frozen census `--selftest` | 0 | 14 cases, all true; failures empty | `census-selftest.stdout`, `.stderr` |
| base round-51 census3, base, `--check` | 2 | `{"error": "registry row must have seven cells", "exit": 2}` | `legacy-base.stderr`, `.stdout` |

The selftest includes absent-path, duplicate, marker, six-cell, and short-row rejection cases. Its case named `five-cell-nonconformant` actually constructs four cells in the frozen source (`registry-census.py:234`); it still exercises the `<6` defect but the name is imprecise. This does not change the observed 14/14 result.

## Interpretation, risks, and boundaries

**R71-C3 is not met at the freeze.** The frozen parser can evaluate the registry and name all six defects rather than exiting unevaluable, but the zero-nonconformant after predicate is false. The assigned record-stage repair is after this wave; its future landing is not observed here. The parent must measure the frozen census against the eventual record/landing revision and inspect the six-row repair disclosure before claiming met. The independent scratch result demonstrates the specified repair suffices for the base registry only.

No production implementation or registry was modified. Only this seat's findings and scratch files were written; read-only git commands only; no credentials read, no installs, no services, no commits, no pushes, no child agents. Python `/usr/bin/python3` was 3.14.8. Scratch was removed by the driver's `finally: shutil.rmtree`; receipts remain here. LSP is unavailable in this seat's exposed tool inventory; no production symbol refactor was attempted. The first scratch simulation accidentally removed the old trailing delimiter and failed its zero-defect assertion; the driver was corrected to preserve that delimiter before the reported completed execution. No frozen-instrument failure was attributed to this driver error.

Self-evaluation: accuracy 4/5 (record-stage outcome intentionally unobserved); completeness 5/5 (all six assigned steps have retained evidence); clarity 4/5 (exact cell strings are lengthy); actionability 5/5 (parent's required after measurement is explicit); conciseness 4/5 (full row JSON is retained separately). Mean 4.4/5. Improvements: retain a record-stage after receipt when that revision exists; keep row details in JSON for integration. Assessment is bounded to this seat's assignment.

VERDICT: not-met at freeze — six round-70 pinned-empty defects remain; independent six-row owner repair yields 0/88 nonconformant, frozen selftest 14/14, legacy base exit 2.
