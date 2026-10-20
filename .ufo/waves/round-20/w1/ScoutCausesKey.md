# ScoutCausesKey — round-20 W1 scout (read-only)

Written 2026-10-20T17:49:14-03:00 (clock at write time). Observed lane tip
`refs/heads/main` = `d1d981d2cc041dda4656c5b01d2c8445d8d17124`; the tool blob at that tip is
sha256 `b9992325e01ec6e7a900d51526246393409b8754c442fe6c346bf3d9f4c1fdf6`
(`git --no-optional-locks show main:.ufo/waves/round-19/tools/wave-outcomes.py | sha256sum` → exit 0),
identical to the working tree (`sha256sum .ufo/waves/round-19/tools/wave-outcomes.py` → exit 0).
No installs, no REA/Go execution, no lane writes beyond this report. All fixtures were built under
`tempfile.mkdtemp()` in `/tmp` (`/tmp/kr20-scout-*`), never in the lane or a git worktree.

Read-only note: `[OBS]` = observed in this run; `[INF]` = inference.

## Axes

- **Calibration.** Shape selection is by key presence alone (`:237`), not by type, `wave`, or seat set —
  contradicting the docstring's wrapped example, which shows `wave` (`:26`). Any fix must say which
  observables actually decide the shape, and keep the existing selftest `wrapped-causes` (no `wave`)
  green unless the contract changes.
- **Coverage.** Only three committed causes inputs exist (flat 42, empty 0, flat 4); round-18 has no
  committed `evidence/wave-outcomes` directory. None of them exercises the collision.
- **Depth.** The collision is not only a refusal: an object-valued `causes` seat can silently
  reassign its cause text to a different seat, flipping exit 1 → 0. The string-value case the round-19
  review found is the mild variant.

## 1. Wrapped vs flat detection — observed trace

Anchors in `.ufo/waves/round-19/tools/wave-outcomes.py` (line numbers verified by `grep -n`, exit 0):

- Accepted shapes documented: flat map `:25`, wrapped map `:26` (shown with `wave`), list of rows
  `:27-29`; metadata names ignored in the flat shape `:30-32`.
- `load_causes` (`:232`) reads JSON (`:234`), then:

```python
raw = doc                                            # :236
if isinstance(doc, dict) and "causes" in doc:        # :237  shape chosen by key presence ALONE
    wave = doc.get("wave") if isinstance(...)        # :238  wave optional, any missing -> None
    raw = doc["causes"]                              # :239
    if not isinstance(raw, dict): raise causes_invalid  # :240-243 (type checked AFTER shape)
elif isinstance(doc, dict) and "seats" in doc:       # :244  second wrapper key, same pattern
    ...
resolved/ignored; if isinstance(raw, dict):          # :253  flat-map loop
    ... if key in META_KEYS and key not in seats: ignored   # :259-261
elif isinstance(raw, list): ...                      # :266  list-of-rows loop
else: raise causes_invalid                           # :285-288
```

Observed consequences:

1. **Wrapper needs no `wave`.** `{"causes": {"A": "boom"}}` against seat `A` → exit 0 (probe
   `wrapper_no_wave`). The selftest encodes this too: case `wrapped-causes` (`:703-712`) uses
   `{"causes": {"Bravo": "exited 1"}}` and expects exit 0.
2. **`causes` wins over `seats`.** Both keys present → the `:237` branch runs (`probe
   both_keys_causes_wins` → exit 0; `wave` null).
3. **Seat precedence exists only for `META_KEYS`.** `:259` ignores a metadata key unless it is also a
   registered seat; `source` as a seat resolves (`selftest meta-key-seat` `:726-736`), and `wave` as a
   seat resolves (probe `seat_named_wave` → exit 0, cause recorded). `causes`/`seats` never reach
   this guard because `:237`/`:244` consume them first.
4. **Empty object is a valid empty flat map.** `w2-causes.json` is `{}` (3 bytes) and is accepted with
   `recorded=0` (probe `empty_flat` → exit 0).
5. **No collision case in the selftest.** `grep -n 'seat_named'` over the file → exit 1 (no match);
   `--selftest` → `SELFTEST: CLEAN cases=33` (exit 0). D6e therefore needs a new case.

## 2. Collision input (constructed) and observed exits

Fixture shape (written only under `/tmp`), run as
`python3 -I -B <tool> --registration reg.json --report-dir reports --causes causes.json --out out.json`:

```
reg.json      {"schema":"ufo-swarm-registry-v1","members":{"causes":{"role":"executor","agentId":"K20.causes"},
               "A":{"role":"executor","agentId":"K20.A"}}}
reports/      one non-empty <name>.md per seat that "reported"
causes.json   as tabulated
```

| probe | registration seats / reports | causes JSON | result |
|---|---|---|---|
| `control_flat_named` | `CauseSeat` / same | `{"CauseSeat":"boom"}` | exit 0, recorded=1 |
| `collide_string` | `causes` / same | `{"causes":"boom"}` | **exit 2** `causes_invalid: 'causes' is str, expected an object keyed by seat` |
| `collide_object` | `causes` / same | `{"causes":{"cause":"boom"}}` | **exit 2** `causes_unknown_seat: 'cause' is neither a seat nor an agentId ... (1 seats)` |
| `collide_object_mixed` | `causes`,`Other` / same | `{"causes":{"cause":"boom"},"Other":"x"}` | **exit 2** `causes_unknown_seat` |
| `wrapped_ok` | `CauseSeat` / same | `{"wave":"w1","causes":{"CauseSeat":"boom"}}` | exit 0, recorded=1 |
| `wrapped_nested_causes_seat` | `causes` / same | `{"wave":"w2","causes":{"causes":"boom"}}` | exit 0, `seats[0].cause="boom"`, recorded=1 |
| `misattr` | `causes`,`A`; only `A` reports | `{"causes":{"A":"boom-intended-for-causes-seat"}}` | **exit 1**; cause lands on `A`, `causes` uncaused |
| `flip` | `causes`,`A`; only `causes` reports | `{"causes":{"A":"boom-intended-for-causes-seat"}}` | **exit 0**; `rows`: `A{report_present:false, cause:"boom..."}`, `causes{report_present:true, cause:null}`; `uncaused=[]` |
| `seat_named_wave` | `wave` / same | `{"wave":"boom"}` | exit 0, recorded=1 |
| `collide_seats_string` | `seats` / same | `{"seats":"boom"}` | **exit 2** `causes_invalid: 'seats' is str, expected a list of rows` |
| `flat_seats_seat_list_value` | `seats`,`A` / same | `{"seats":["boom"],"A":"x"}` | **exit 2** `cause_value_invalid: ... seats[0] is str, expected an object row` |
| `list_shape_causes_seat` | `causes` / same | `{"seats":[{"name":"causes","cause":"boom"}]}` | exit 0 (the workaround round-19 used) |

**Depth finding ([OBS]).** `flip` is the important collision: the flat map assigns a cause to seat
`causes` whose value is the object `{"A": "..."}`; the tool reads it as the wrapper, attributes the
text to seat `A`, and returns **exit 0** with a dead `A` marked caused. A correct flat reading (cause
on reporting seat `causes`, nothing on `A`) yields **exit 1**. So the collision can turn a red
record into green, not merely refuse — worse than the round-19 P3 note
(`.ufo/waves/round-19/w2/ToolWaveOutcomes.md:11-13`, which exercised only the string value and the
list-shape workaround at `:66-72`).

**Residuals of the heuristics suggested in `W20/gen-wave1.py:152` ([OBS]; [INF] on admissibility):**

- "wrapper only when the `causes` value is an object **and** a `wave` key is present" still collides
  for flat `{"causes":{"cause":"boom"},"wave":"w2"}` with seats `causes`,`wave` → exit 2
  (`flat_causes_obj_plus_wave_seat`).
- "... or a schema tag" still collides for flat
  `{"causes":{"cause":"boom"},"schema":"...","A":"x"}` → exit 2 (`flat_causes_obj_plus_schema`);
  `schema` is an ignorable flat-map metadata name per `:30-32`, so it cannot be a reliable wrapper
  marker.
- "registered seat name wins" is not directly usable either: it would break the legal wrapped form
  `{"causes":{"causes":"boom"}}` (`wrapped_nested_causes_seat`, exit 0 recorded=1 — parsing it flat
  would drop the cause silently) and would need selftest `c22` (`:703-712`) to change.
  `[INF]` A sound discriminator has to consult the *value's* keys (seat-resolvable vs `CAUSE_KEYS`
  `:71`) or require an explicit schema/`wave` marker; the writer should state which and test both
  wrapper-without-`wave` and nested-`causes`-seat.

Other object-valued collision forms ([OBS]): `{"causes":{"reason":"boom"}}` → exit 2
`causes_unknown_seat: 'reason' ...`; `{"causes":{"cause":"boom"},"note":"x","A":"y"}` → exit 2
(`note` is ignored metadata but the wrapper path is already chosen). With a `seats` seat the list
branch is entered and a non-object row refuses (`cause_value_invalid`, above).

## 3. Committed causes / wave-outcomes files and shapes

`git --no-optional-locks ls-files | grep -i 'wave-outcome\|causes'` → exit 0; it lists the ten
files below plus `.ufo/waves/round-17/wave-outcomes.json` and the tool/selftest transcripts.
`ls .ufo/waves/round-18/evidence/wave-outcomes` → exit 2 (no such directory), and
`git ls-files '.ufo/waves/round-18/*' | grep -i 'cause\|outcome'` → exit 1 (no match). So the only
committed round-18 causes input is the **copy** retained under round-19 evidence.

`.ufo/waves/round-19/evidence/wave-outcomes/` (sha256 over bytes, observed exit 0):

| file | bytes | sha256 | shape |
|---|---|---|---|
| `w1-causes.json` | 15279 | `5cb48b1973ce50336b9dd62cd55c2b6bb229a40512a8578d69d3f3c2e924c390` | **flat map**, 42 keys, every value a `str`; no metadata-name keys; 90-seat registration |
| `w2-causes.json` | 3 | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` | **empty flat map** `{}` (`recorded=0`) |
| `r18-w2-causes.json` | 418 | `235c5fb6d9760e4025c963ebc7ed25f9bdffe3246563b62a2ca6d9ab5f76afd2` | **flat map**, 4 keys (`GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY`), values `str`; 98-seat registration |
| `r18-w2-outcomes.json` | 13346 | `edca369d33f7562af00b8135d7e9555320d69bccc5dda3184788d6e4b4b0a3ad` | tool record `ufo-wave-outcomes-v1`, 20 keys, `wave:null`, `causes_recorded:4`, rows under `seats` |
| `r18-w2-green.stdout` | 476 | `ef0e1d7df454e5e716e6e9a04e97ed16d4342bb1045792ee9181f26088995102` | text: 98/94/4, 4 causes, uncaused 0 |
| `r18-w2-green.exit` | 13 | `407f92e3cc067780137c1d4ffe0d7f0cbd75d336db64d72228387a96f42e4be5` | `green exit=0` |
| `r18-w2-red.stdout` | 611 | `25cf86bec5fefc5d308b1f5dc0b045107393b0194a4a81e6d1edd248cfe7383e` | text: 98/94/4, 0 causes, uncaused 4 |
| `r18-w2-red.exit` | 11 | `4bb5e1bed8a62f81d20924283e9f2b8afe3c8599fdda527cddff89204b09f8ee` | `red exit=1` |
| `w1-terminal.json` | 46121 | `ec18ab75addeb4a5435a32e3be1f6fd7fafa4a96bd6598b5926a94427f23403e` | `{cutoff, seats}` terminal record — **not** a causes file |
| `w2-terminal.json` | 33435 | `eb9d590795fc6576434bc121a198d0f1af26cc468f1492aef688f3928db2fbff` | `{cutoff, seats}` — **not** a causes file |

[INF] Because none of the three committed inputs contains a top-level `causes` key or a `causes`
seat, the collision does not change the round-19 retained outputs; the contract's
"Current round inputs contain none of those attacks" (`corpus/lessons/round-19.md:183-185`) holds for
these blobs.

## 4. Re-run targets for the D6e executor (canonical argv already in the lane)

- r18-w2 red/green: `.ufo/waves/round-19/w2/LessonMistakes.md:43-49`
  (`--registration .ufo/waves/round-18/wave2-registration.json --report-dir .ufo/waves/round-18/w2`,
  empty causes exit 1 / `r18-w2-causes.json` exit 0; registration sha `4e43ca53…` per
  `.ufo/waves/round-19/w2/Quality22.md:23`).
- W1 recount: `.ufo/waves/round-19/w2/LessonMistakes.md:52` → 90 seats / 48 reports / 42 causes,
  exit 0.
- Selftest baseline: `python3 -I -B .ufo/waves/round-19/tools/wave-outcomes.py --selftest` →
  `SELFTEST: CLEAN cases=33`, exit 0; new case must add `seat_named_causes` without regressing
  `wrapped-causes`, `flat-meta`, `meta-key-seat`, `list-causes`.

## 5. Remaining unknowns

- Which discriminator the L1 will accept is not fixed by the contract beyond "a seat literally named
  `causes` never collides" (`W20/contract.md:68-69`); the three candidate rules above each leave a
  named residual or need an existing selftest changed. [INF]
- I did not re-run the three committed inputs through the tool in this scout (only shape/hash
  inspection), so I claim no observed stdout for those; the retained transcripts are cited as data.
