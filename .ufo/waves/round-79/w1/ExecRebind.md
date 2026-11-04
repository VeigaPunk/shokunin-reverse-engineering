# ExecRebind — independent re-derivation of R79-C2 (freshness)

Seat: ExecRebind (leaf). Scope: re-derive the frozen R79-C2 claim with an own script, never
importing `tools/round-79/pointer-bind.py`. Lane edits: none. Writes confined to this evidence dir.

## Verdict

**R79-C2 holds under independent re-derivation.** Base `29d2ca30` binds 3/5 with exactly two
mismatches (`omp-pin`, `kimi-pin`); freeze `ed68cd0a` binds 5/5 with zero mismatches and zero
unparsed; the path-only rule still reports 0 mismatches on the stale record; my line-bound binder
fails when one pointer is rewritten in a scratch copy.

| | base `29d2ca30` | freeze `ed68cd0a` |
|---|---|---|
| exit | 1 | 0 |
| checks_total | 5 | 5 |
| matched | 3 | 5 |
| mismatches | 2 | 0 |
| unparsed | 0 | 0 |
| mismatch_ids | `omp-pin`, `kimi-pin` | — |

Claim sentence checked verbatim: base `mismatches 2` **naming** `omp-pin` (record `:8`, pin at
`:12`) and `kimi-pin` (record `:4126`, pin at `:4722`) — both the naming and the stated live lines
are reproduced; freeze `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`.

## Independence of the re-derivation

`rebind.py` here was written from the claim text and the record's own sentence shapes:

- record read as `git show <rev>:PROVINCE.md`;
- three pins: client-scoped, bounded, non-greedy adjacency
  `<Client> … `rea-agents@<v>` (`<path>:<line>`)` — this deliberately refuses the lead-in sentence
  ("and Kimi all pin `rea-agents@6.7.0` …") that has no pointer;
- Ghidra: the `application.version=<v>` value and the `…/Ghidra/application.properties:<n>`
  pointer taken from the same blank-line paragraph;
- `.bashrc`: the `.bashrc:<start>-<end>` cell in the paragraph that declares both
  `GHIDRA_INSTALL_DIR=` and `JAVA_HOME=` (so the later `:63-69` REA-key block, `:66`, `:61`,
  `:29` and `:63` citations are not candidates);
- binding: expand `~`, read the live file, require **every** declared token on a line inside the
  declared 1-based inclusive range; digest only the pointed lines.

No import, no copy of the instrument's regex table. The extraction differs in mechanism (paragraph
scope vs. first-match-in-document) yet selects the identical five cells at both revisions — a
convergence check, not a dependency.

## Per-check detail

### base `29d2ca30` (record sha256 `cf2c5fe4…a71ec`)

| id | pointer | token(s) | matched | reason |
|---|---|---|---|---|
| devin-pin | `/home/vgpnk/.config/devin/mcp_config.json:7` | `rea-agents@6.7.0` | true | — |
| omp-pin | `/home/vgpnk/.omp/agent/mcp.json:8` | `rea-agents@6.7.0` | **false** | token not on line 8 |
| kimi-pin | `~/.kimi-code/config.toml:4126` | `rea-agents@6.7.0` | **false** | token not on line 4126 |
| ghidra-version | `…/ghidra_12.1.4_PUBLIC/Ghidra/application.properties:17` | `application.version=12.1.4` | true | — |
| bashrc-exports | `/home/vgpnk/.bashrc:28-29` | `GHIDRA_INSTALL_DIR=`, `JAVA_HOME=` | true | — |

### freeze `ed68cd0a` (record sha256 `99d29a00…52ca0`)

Same five cells with `omp-pin` at `:12` and `kimi-pin` at `:4722`; all five matched, all reasons
empty.

## Live pin lines (the fact the claim rests on)

`grep -n -o 'rea-agents@6.7.0' <file> | cut -d: -f1` — line numbers only, no config bytes retained:

| client | file | live line(s) | record line (base) | record line (freeze) | agrees (base / freeze) |
|---|---|---|---|---|---|
| Devin | `/home/vgpnk/.config/devin/mcp_config.json` | 7 | 7 | 7 | yes / yes |
| OMP | `/home/vgpnk/.omp/agent/mcp.json` | 12 | 8 | 12 | **no** / yes |
| Kimi | `/home/vgpnk/.kimi-code/config.toml` | 4722 | 4126 | 4722 | **no** / yes |

Each config contains the pin on exactly one line; exactly the lines the freeze record names.

## Negative control (a control that can fail)

Scratch copy of the freeze record with the single string
`` `/home/vgpnk/.omp/agent/mcp.json:12` `` rewritten to `:1` (asserted exactly one occurrence):

```
exit 1, matched 4, mismatches 1 -> omp-pin: token 'rea-agents@6.7.0' is not on line 1
```

Positive counterpart through the same `--record-file` path: the unmodified freeze copy is 5/5,
exit 0 — so the red result is the rewrite, not the control plumbing.

## Control that cannot fail (why the claim target is the line-bound rule)

`--control path-only` at base `29d2ca30`: 5/5 matched, 0 mismatches, including both stale
pointers. Path existence alone is blind to a moved line; this is the round-78 defect the claim
retires.

## Digest convergence

My pointed-line sha256 values equal the frozen instrument receipts' values at both revisions
(independent parser and binder):

| id | base | freeze |
|---|---|---|
| devin-pin | `d62ab8da…` | `d62ab8da…` |
| omp-pin | `6c97fd49…` | `d62ab8da…` |
| kimi-pin | `c00d8456…` | `eb1c7da7…` |
| ghidra-version | `e655d6c5…` | `e655d6c5…` |
| bashrc-exports | `db162b4c…` | `db162b4c…` |

Devin `:7` and OMP `:12` share a digest because the pointed lines are byte-identical — an
independent structural cross-check on the two REA-pin cells.

## Instrument and record identity

Measured at this seat's run time (10:07 local):

- `tools/round-79/pointer-bind.py` sha256 `91d23dad…80a90` = the `instruments` pin in
  `.ufo/waves/round-79/claims.json`.
- `tools/round-78/attack-gate.py` sha256 `4e4baf00…2d2bf` = the `loaded_by_counter` pin.
- `PROVINCE.md` sha256 at base `cf2c5fe4…a71ec` and at freeze `99d29a00…52ca0` = the
  `record.sha256` values in the frozen base/landing receipts.

Qualification (reported by `ScoutRouted-2` after this seat's measurement): the worktree now carries
**uncommitted** edits to both round-79 instruments (`gate-mutation.py` `682f1e78…` → `75fbf1a7…`,
`pointer-bind.py` `91d23dad…` → `3f07bd2a…`; `attack-gate.py` still `4e4baf00…`). The identity
lines above are therefore true of the bytes present when read, not of the current worktree. This
does not touch the verdict: `rebind.py` never reads either instrument and reads `PROVINCE.md` from
committed bytes via `git show`, so its measurements are independent of worktree instrument state.
Consequence for the landing: the pin is already broken in the worktree, so a supersession entry is
required whether or not L1 commits the current diff.

## Cross-seat observation: the frozen predicate's printed argv cannot execute

Routed by `ScoutRouted-2` (read-only recon; reported, not re-run here because peer observations are
ground truth for this seat): the command printed in the R79-C2 predicate and in
`claims.json.counting_command` — `pointer-bind.py --root . --rev <rev> --json-out <receipt>` with
**no** `--battery` — exits 2 with a usage line and writes no receipt, at both `29d2ca30` and
`ed68cd0a`. Adding `--battery` yields the claimed exits and counts (freeze 0 / 5-5-0-0, base
1 / 5-3-2 with `omp-pin` `:8`, `kimi-pin` `:4126`).

Consequences for this seat's verdict:

- The **numbers** are right and are independently reproduced by `rebind.py`, which has no
  `--battery` switch at all — so this re-derivation is not an instance of the printed command and
  is unaffected by the defect.
- The **printed predicate text** is not executable as written: `PREDICATE` inside
  `tools/round-79/pointer-bind.py`, `claims.json.predicate` and `claims.json.counting_command`
  all carry the same missing flag. Repairing it is an L1 lane edit and would change the
  instrument sha256 (`91d23dad…`), so it needs a supersession entry or the freeze pin stops
  resolving (`INSTRUMENT_PIN_MISMATCH`). Not this seat's edit; recorded here so the landing can
  carry it.

## Risks / limits

1. Both my binder and the instrument read the **live** files, so both are subject to later host
   drift: the freeze result is true as of the run timestamp in `receipt.json`, not a proof about
   future file state.
2. My `.bashrc` cell is paragraph-scoped: if a second paragraph before the Ghidra paragraph were
   to declare both export names with a different `.bashrc` range, extraction would shift. At both
   frozen revisions the extracted cell is `:28-29`, identical to the instrument's.
3. The `.bashrc:63-69` REA-key block is **not** one of the five cells in either implementation;
   the five are the three REA pins, the Ghidra properties line, and the `:28-29` export range.
4. `--record-file` exists only to drive the controls; all claim measurements use `--rev` against
   committed bytes.
5. The frozen predicate/counting-command text omits `--battery` (see the cross-seat observation
   above): the numbers verify, the printed argv does not. Until the L1 repairs the three strings
   and lands a supersession entry, a stranger running the claim verbatim gets exit 2, not a
   receipt.
