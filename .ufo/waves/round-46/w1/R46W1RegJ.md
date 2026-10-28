# R46W1RegJ — three instrument-registry rows (tag `reg-j`)

Seat: registry rows for `tools/round-41/local-source-gate.py`, `tools/round-42/sqfs3-oracle.py`,
`tools/round-46/census.py`. Read-only on the lane tree. Deliverables in
`.ufo/waves/round-46/w1/R46W1RegJ/`: `rows.md` (three rows, paste verbatim), `receipt.md`
(command / exit / stdout sha256 / UTC for 28 runs), `receipts/` (raw stdout+stderr per run).

All three instruments are **byte-identical** at every rev of the ladder this seat walked
(`3182047…`, `50862e4a…`, `0425224…`, `49e6cac4…`): blob ids `17c4ad5a` (`census.py`), `99d9e478`
(`sqfs3-oracle.py`), `053aeabe` (`local-source-gate.py`). So every row below describes the same bytes
at the freeze and at HEAD.

`rows.md` sha256 `fa1e1b2a1adc29f0c4fd899ab17f0ae161d6e85e79ae5cfc5a25e15a349df1dd`.

## 0. State at the tip, and what landed

The lane tip moved three times while this seat ran (`87578656` → `1e32827b` → `49e6cac4`). Measured at
HEAD `49e6cac4f6604986b1a7e9cfcbd9d46704dff390`:

| counter | bytes | freeze | rev | exit | result |
|---|---|---|---|---|---|
| `registry.py` (C2) | at `0425224` | `0425224` | `49e6cac4` | 0 | `met_target true`, `registry_rows 38`, `thin []`, battery `7 / 7 / 0 / 1` |
| `attest.py` (C1) | at `0425224` | `0425224` | `49e6cac4` | 0 | `met_target true`, `failing []`, battery `9 / 9 / 0 / 1`, `v2_crash 0` |

My three rows landed **byte-identically** in `SKILL.md` at `781e19ae` (checked line by line against
`rows.md`: all three `PRESENT IDENTICAL`; lines 1707, 1720, 1733). The section at HEAD holds 38 rows
between one `<!-- instrument-registry v2 -->` / `<!-- /instrument-registry -->` pair. Nothing further is
needed from this seat for the rows themselves.

## 1. Delivered rows

`rows.md` holds exactly three lines in the 7-column house order
(`tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner`).
Checked on the file itself: 3 lines, 7 cells each, cell 1 exactly the backticked path, cell 3 binds
`0=`, `1=` and `2=` under the counter's own `\b([012])\s*[=:]` regex, zero backticks outside cell 1,
no literal `|` inside any cell. Pasted verbatim into a fixture `SKILL.md` between the v2 markers with the
exact house header and a three-path census, the frozen counter scores `exit 0 met_target true failing []`
(receipt `fxreg-structural`) — the rows were judged by the judging instrument before landing.

## 2. What each row claims, and the command that verified it

Exit meanings are read from the source and then exercised. Numbers are exit codes.

| row | claim verified | command | exit |
|---|---|---|---|
| `local-source-gate.py` | selftest exists and passes (cell 4) | `--selftest` | 0 (`selftest: 23/23 cases`) |
| `local-source-gate.py` | 2 = usage/parse error | `--root /nonexistent-xyz` | 2 |
| `local-source-gate.py` | 0 = every out-of-lane row resolved, on the lane's real table at the freeze | `--root <lane> --rev 3182047…` | 0 (`verdict PASS (rows: none)`) |
| `local-source-gate.py` | 1 = at least one row unresolved | `--root <fixture>` with one row naming an unmapped out-of-lane path | 1 (`[map-missing]`, `verdict FAIL (rows: S900)`) |
| `local-source-gate.py` | cell 5: the sidecar map is the pinned-value path | `git cat-file -e 3182047…:corpus/evidence/local-sources.json` | present, 12533 bytes |
| `sqfs3-oracle.py` | selftest exists and passes (cell 4) | `--selftest --work <fresh>` | 0 (`0 failure(s)`) |
| `sqfs3-oracle.py` | 2 = image unreadable | `--work <fresh> /nonexistent-xyz.img` | 2 (`is not a file`) |
| `sqfs3-oracle.py` | 3 exists and is reachable (outside the house map, see F6) | `--dev-allow-v4` on a v4 image with one file named `a<TAB>b.txt` | 3 (`reason=path_not_representable`) |
| `sqfs3-oracle.py` | cell 5: `oracle-run.json` records the input sha256, tool set and cross-check verdict | read `<out>/oracle-run.json` from the exit-3 run | keys present: `input.sha256`, `tools{unsquashfs,7z,backhand}`, `cross_check.verdict` |
| `census.py` | 0 = census computed; cell 5: re-derives the committed `census.json` | `--root <lane> --rev 3182047… --out <scratch>/census.json` | 0, bytes **identical** to `3182047…:tools/round-46/census.json` (38 paths) |
| `census.py` | 2 = argparse usage error | same without `--root` | 2 |
| `census.py` | cell 4 `none`: no selftest flag exists | same with `--selftest` | 2 (`unrecognized arguments: --selftest`) |
| `census.py` | 1 = unhandled exception, not a verdict | same, `--out /nonexistent-dir-xyz/out.json` | 1 (`FileNotFoundError` traceback) |

Two verification runs recorded a first-attempt failure and are kept as evidence, not hidden:
`--selftest --work` on an **already used** directory crashes (F4), and `--out` into a **missing parent
directory** crashes (F3). The rows describe the corrected invocations.

## 3. Findings

### F1 — the freeze ladder: every earlier freeze makes the counter refuse the tip (resolved by re-declaring; residual risk stated)

```
registry.py --freeze 31820472784284727546808acc31b3ea1e73919b --rev <HEAD> --no-battery
→ exit 2, reason "frozen_path_changed",
  frozen_path_changed ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]

registry.py --freeze 50862e4a041499dd2ce0da68d10301b765bb9997 --rev <HEAD> --no-battery
→ exit 2, reason "frozen_path_changed",
  frozen_path_changed ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/registry.py"]
```

`50862e4a` (13:51) superseded the stated freeze `3182047` (13:46); `0425224` (14:00, the F4 repair)
superseded `50862e4a`; the lesson landed at `49e6cac4` names the situation ("four freeze commits").
With `--freeze 0425224` both counters are clean at HEAD and green (§0), and with the post-repair bytes
against the *older* freeze the answer is still `exit 2` (`regD`, not a bug — it is the rule working).

Residual, for the record and not for a fix here: the admissible freeze is now the commit that repaired
the instrument, so the window `3182047..0425224` — exactly where the instrument was written, found
non-discriminating (F2) and repaired — is not defended by the instrument's own rule. That is a property of
"re-declare the freeze after each repair", not of any single counter. The claims file's derivation
("the commit that first contains this file and `tools/round-46/`") still resolves to `3182047`, so the
`@<freeze>` a reader re-derives from the claims file is not the `@<freeze>` the receipts were scored at.

### F2 — C2 clause 6 `battery.v1_green == 7` was unreachable before the F4 repair (closed; kept as the measurement that forced it)

Measured with the frozen `registry.py` at `50862e4a` on three artefacts, all of which passed every
structural clause (`exit 0`, `failing []`):

| artefact | `forgeries_total` | `v1_green` | `v2_green` | `genuine_green` | verdict |
|---|---|---|---|---|---|
| 3 rows (this seat's rows only) | 7 | 5 | 0 | 1 | exit 1, `battery v1_green 5 != 7` |
| 38 rows, house format, clean `SKILL.md` | 7 | 5 | 0 | 1 | exit 1, `battery v1_green 5 != 7` |
| 38 rows, house format, real `SKILL.md` at `87578656` | 7 | **0** | 0 | 1 | exit 1, `battery v1_green 0 != 7` |

Root cause in the pre-repair bytes: `score()` reads `strict_cell` / `strict_exit` / `presence` from the
**spec**, so `--profile v1` kept r46's exact-cell and exact-exit checks; `hard = profile == "v2"` gated only
the marker binding and the header. `substring-cell` and `prose-exit` therefore stayed red under `v1`, and the
ceiling was 5, not 7. On the real `SKILL.md` a second effect drove it to 0: under `v1`, `rows_anywhere`
scans the whole file (83 rows) and `by_path.setdefault` is first-wins, so the six pre-existing round-44/45
rows with prose verdict cells shadowed the new section's rows — `thin` named exactly
`tools/round-44/{c1-counter.py,c1-run.sh,c2-counter.py}`, `tools/round-45/{c1-counter.py,c2-counter.py,frozen-path-preflight.py}`.

`0425224` ("the v1 registry profile applies its own loose checks (strict cell/exit/presence are v2-only)")
repairs exactly this, and the battery is now `7 / 7 / 0 / 1` (`regC`). Related receipt mismatch, still
worth correcting in the record: the claims file cites `controls/ctl-c2-1-v1-profile.json`, which does not
exist; `controls/ctl-c2-1-v1-scope.json` is the **round-45** counter (`"counter": "round-45-c2"`,
`scope_size 6`, `battery null`) and never measured the seven r46 forgeries.

### F3 — `census.py` does not create the `--out` parent directory (open)

`--out /nonexistent-dir-xyz/out.json` → `FileNotFoundError` traceback, exit 1, no JSON (receipt
`r3-badout`). The tool's own docstring presents `--out tools/round-46/census.json` as the normal form,
which works only because the parent exists. The row binds this honestly as `1 = unhandled exception`, but a
caller naming a new evidence directory gets a traceback where exit 2 would be the contract. Bytes
unchanged at HEAD (`17c4ad5a`), so the finding stands.

### F4 — `sqfs3-oracle.py --selftest` is not idempotent on a reused `--work` (open)

Second run with the same `--work`: `FileExistsError: [Errno 17] File exists: 'apple.txt' → <work>/bh-tree/link`,
exit 1 with a traceback. Exit 1 is documented as "the inline selftest failed", so the code is not wrong,
but the failure is a crash in fixture setup rather than a test result. The row's command names a **fresh**
`--work`. Bytes unchanged at HEAD.

### F5 — the post-freeze `attest.py` raised `NameError` at every rev (closed by the F3 commit)

```
attest.py@50862e4a --root <lane> --freeze 50862e4a --rev 87578656
→ exit 2, {"reason": "unhandled NameError: name 'REF' is not defined"}
```

`REF` was referenced at `attest.py:322` and never defined (only `HARD_REF`/`LOOSE_REF` exist), so the line
scan fired before any clause was scored. Repaired in `0425224`; C1 now exits 0 with battery
`9 / 9 / 0 / 1` (`attestA`). Recorded so a C1 `exit 2` from that window is not misread as
`frozen_path_changed`.

### F6 — `sqfs3-oracle.py` exits 3, outside the house `0/1/2` map (reported here, not in the row)

Exit 3 = producers disagree, or a path cannot be represented in a TAB table (`EXIT_DISAGREE`); verified
reachable (receipt `r2-exit3`). By this seat's brief, `rows.md` binds only 0, 1, 2. If the L1 wants the
map complete, replace row 2's cell 3 with:

```
0=producers agree and both tables written; 1=the inline selftest failed (never a verdict on an image); 2=image unreadable or unsupported, or a required producer could not complete; 3=producers disagree or a path cannot be represented in a TAB table
```

The counter still accepts that text (`{0,1,2}` remain bound; a `3=` does not change the key set), but it
departs from the seat rule, so it is offered, not applied. Read as written, a caller that sees 3 will read
it as "not met" against a house map that reserves 1 for that.

## 4. Limits

- Exit 3 of `sqfs3-oracle.py` was exercised only through `path_not_representable` on a v4 image with
  `--dev-allow-v4` (a flag documented as development-only). A producer-disagreement exit 3 on a real v1–v3
  image was **not** run.
- The agreement path (exit 0 on a real image, tables written) was **not** exercised on a lane carrier; the
  row's `0` is source-read at the end of `oracle()` plus the selftest, not a carrier run.
- Row 1's `0` **was** exercised on the lane's real `SOURCES.md` at the freeze.
- The three rows cover 3 of the 38 census paths; coverage of the other 35 is not this seat's.
- `7z`, `unsquashfs`, `unsquashfs-backhand` were present and used; this seat did not pin their versions
  (the tool records them itself in `oracle-run.json`).
- No install was made and no tool was added.

## 5. Hygiene

Wrote only `.ufo/waves/round-46/w1/R46W1RegJ/` (`rows.md`, `receipt.md`, `receipts/`) and this file.
Fixture repos were created under `HYAKU_SCRATCH` with `git rev-parse --show-toplevel` asserted before each
first commit; no commit, stage, checkout or reset touched the lane. Scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegJ` removed after the receipts were copied; nothing was written
under `/tmp`.
