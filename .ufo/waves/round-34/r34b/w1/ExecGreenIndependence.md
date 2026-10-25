# ExecGreenIndependence — independent expected-record audit (R34-C2 green surface)

Seat: leaf executor, round 34 run-6 re-dispatch, wave 1. Read-only on the lane; every write
below is under `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecGreenIndependence/` or this report.
No network used. No tool installed or upgraded (nothing needed; `python3` = `/usr/bin/python3`
was sufficient), so there is no tool/version/channel line to record.

## 1. Question and answer

Assignment: write an own MREC decoder from the format comment in
`tools/round-34/mini-fix/build.py` only (not from `mini-counter.py`), decode all eight
fixtures, diff against `expected.json`, and decide whether any expected record could only
have been produced by the author's own code path.

Answer in one line: **8/8 fixtures and 25/25 records match; zero content mismatches; and no
expected record requires author code — an independently written decoder regenerated
`expected.json` byte-for-byte (sha256 `5ebb5349fd21eb3e885c775cb0068ece04188b9a9a7fdc414c1c83a2d8828483`,
equal to the C2 pin) from the eight fixture files alone.**

## 2. Independence protocol actually followed

1. Read `build.py` (format comment + `expected()` sort rule) and `expected.json`.
2. Wrote `/fast/scratch/.../own_mrec_decoder.py` from the format comment; asserts only
   invariants stated there (`records_off` == header size 16, `names_off` == 16 + 8*count,
   NUL-terminated printable ASCII names).
3. Ran it and wrote the independence probes **before** opening `mini-counter.py`. The first
   probe version had a scratch bug (`count` unpacked as the name pool, so a synthetic ULE
   probe reported a bogus `raised`); it was caught, the probe was rewritten, and the v1
   probes file is retained as `independence-probes.json` with v3 as the authoritative run.
4. Read `mini-counter.py`, the green config and all nine readers only afterwards, to test the
   author-path claim against the counter's comparison semantics. Nothing in the decoder or
   probes was changed to accommodate the counter.

Scratch evidence (all retained):

- `own_mrec_decoder.py` — decoder; `own-decoded.json` (file-order decode), `own-decode-report.json`
  (header/poison invariants per fixture).
- `lane-decoded.json` — same decoder run directly on the lane fixtures dir.
- `expected-regenerated-by-own-decoder.json` — canonicalized regeneration of `expected.json`.
- `independence-probes.py`, `independence-probes-v3.json` (+ v1/v2 and stderr).
- `fixtures-copy/` — byte-identical copies used for the mutation probes (lane never written).

## 3. Format as decoded (from the build.py comment only)

Little endian: `"MREC"` | u16 version | u16 count | u32 records_off | u32 names_off |
count x (u16 name_off, u16 flags, u32 value) | NUL-terminated ASCII name pool; fixed 512 bytes.
Header offsets 0/4/6/8/12. Record `i` at `records_off + 8*i`; name is the pool slice from
`names_off + name_off` to the next NUL.

All eight fixtures satisfy the self-consistency invariants the comment implies, with no
exceptions: size 512, magic OK, version 1, `records_off` 16, `names_off` 16+8*count,
every `name_off` a genuine string start (0 mid-string offsets), no duplicate names, all bytes
after the pool zero, mode 0644.

## 4. Diff against `expected.json`

Unordered (name, flags, value) multiset, i.e. what the counter's `canonical()` compares:

| fixture | records | expected | own | match |
|---|---|---|---|---|
| alpha.mrec | 3 | 3 | 3 | yes |
| beta.mrec | 1 | 1 | 1 | yes |
| delta.mrec | 2 | 2 | 2 | yes |
| epsilon.mrec | 1 | 1 | 1 | yes |
| eta.mrec | 3 | 3 | 3 | yes |
| gamma.mrec | 5 | 5 | 5 | yes |
| theta.mrec | 6 | 6 | 6 | yes |
| zeta.mrec | 4 | 4 | 4 | yes |
| **total** | **25** | **25** | **25** | **8/8 fixtures, 25/25 records** |

Strict in-file record order versus `expected.json` (which is sorted by
`(name, flags, value)`) matches on 3/8 fixtures (alpha, beta, epsilon). The other 5/8 are
order permutations only — the same records in a different sequence. Every one of those 20
order-mismatched records, with its on-disk bytes (`<HHI`: name_off, flags, value):

| fixture | file idx | off | hex bytes | name | flags | value | expected idx |
|---|---|---|---|---|---|---|---|
| delta | 0 | 16 | `00000000010d0303` | libstdc++.so.6 | 0 | 50531585 | 1 |
| delta | 1 | 24 | `0f000000030b0000` | libatomic.so.1 | 0 | 2819 | 0 |
| eta | 0 | 16 | `0000010008030003` | libssl.so.3 | 1 | 50332424 | 2 |
| eta | 1 | 24 | `0c000000010d0303` | libcurl.so.4 | 0 | 50531585 | 1 |
| eta | 2 | 32 | `19000000030b0000` | libcares.so.2 | 0 | 2819 | 0 |
| gamma | 0 | 16 | `00000200600b0000` | libgcc_s.so.1 | 2 | 2912 | 1 |
| gamma | 1 | 24 | `0e00000000000000` | libpthread.so.0 | 0 | 0 | 2 |
| gamma | 2 | 32 | `1e000100600b0000` | libdl.so.2 | 1 | 2912 | 0 |
| gamma | 3 | 40 | `29000000600b0000` | libutil.so.1 | 0 | 2912 | 4 |
| gamma | 4 | 48 | `36000000600b0000` | libresolv.so.2 | 0 | 2912 | 3 |
| theta | 0 | 16 | `00000000030b0000` | libffi.so.8 | 0 | 2819 | 0 |
| theta | 1 | 24 | `0c000000030b0000` | libgmp.so.10 | 0 | 2819 | 1 |
| theta | 2 | 32 | `19000000030b0000` | libmpfr.so.6 | 0 | 2819 | 4 |
| theta | 3 | 40 | `26000000030b0000` | libmpc.so.3 | 0 | 2819 | 3 |
| theta | 4 | 48 | `32000000030b0000` | libisl.so.23 | 0 | 2819 | 2 |
| theta | 5 | 56 | `3f000000600b0000` | libzstd.so.1 | 0 | 2912 | 5 |
| zeta | 0 | 16 | `00000300600b0000` | libGL.so.1 | 3 | 2912 | 0 |
| zeta | 1 | 24 | `0b000000600b0000` | libX11.so.6 | 0 | 2912 | 1 |
| zeta | 2 | 32 | `17000000600b0000` | libxcb.so.1 | 0 | 2912 | 3 |
| zeta | 3 | 40 | `23000000600b0000` | libwayland-client.so.0 | 0 | 2912 | 2 |

No record differs in name, flags or value. No expected record is absent from its fixture and
no fixture record is absent from `expected.json` (25 = 25, all unique names across the set).

## 5. Could any expected record come only from the author's code path?

No, on the content. Evidence, strongest first:

1. **Byte-identical regeneration.** A decoder written from the format comment alone, reading
   only `fixtures/*.mrec`, produced a canonical records file that is byte-for-byte the lane's
   `expected.json`: `regen_sha256 == lane_sha256 ==
   5ebb5349fd21eb3e885c775cb0068ece04188b9a9a7fdc414c1c83a2d8828483`, `byte_identical True`
   (07:19:33Z). Parsed-JSON equality also holds: `parsed_equal_own_vs_lane_expected True`.
2. **Field-level necessity.** Every triple requires the record array: the name pool alone
   yields the eight name sets but no flags and no values (`P4_pool_only_flags_values_absent`);
   the six distinct values (`0, 2819, 2912, 50332424, 50531585, 100729359`) and four distinct
   flag words (`0..3`) are associated with names only through `(name_off, flags, value)`
   records. Conversely, names are recoverable from the pool, but the association is not — that
   is exactly the property the green predicate claims to test.
3. **No hidden author-side constants.** Single-byte mutation of `name_off`, `flags` or `value`
   on each fixture changes the decode (`P3_single_byte_mutations_change_decode`: all true,
   8/8 fixtures), so the decoder is not emitting memorised output and no field is decorative.
4. **Layout-independence.** Reversing the name pool (rewriting every `name_off`) leaves the
   canonical records identical on 8/8 fixtures (`P1_pool_reversed_identical` true; bytes differ
   on 6/8, n/a on the two single-name fixtures). Reversing the record array likewise leaves the
   canonical multiset identical on 8/8 (`P2_record_array_reversed_identical` true; bytes differ
   on 6/8, n/a on the two single-record fixtures beta and epsilon).

What *is* author-chosen, and must not be over-claimed as evidence:

- **Ordering.** `expected.json`'s sequence is `build.py::expected()`'s sort by
  `(name, flags, value)`; it is not a property of the fixture bytes (section 4). This is
  harmless for the gate because `mini-counter.py::canonical()` applies the same sort, so green
  scoring is order-insensitive. It does mean record ordering carries **no** discriminating
  information, and that the "permuted copies" property rests on pool permutation, not record
  order.
- **Envelope/formatting.** `schema: 1`, `indent=1`, `sort_keys=True`, trailing newline are
  serialization conventions, not record content.
- **Self-consistency by construction.** Fixtures and `expected.json` are both emitted by
  `build.py` from one `SPEC`, and `spec.json` carries the same triples
  (`spec_json_reproduces_expected True`). Agreement between expected and fixture is therefore
  tautological; the only independence evidence is the byte-level decode above (which is what
  was performed). Note also that fixtures + expected + spec are three copies of one author
  input, so a reader that could reach `spec.json`/`expected.json` would not have to decode
  anything.

## 6. Residual risk flagged to the L1 (unprobed, stated as such)

`mini-counter.py::score()` runs each reader as `sys.executable -I -B <reader> <opaque temp
path>` with `cwd` inherited (no `cwd=` argument) and env limited to `PATH`/`HOME`. The temp
input path is opaque and renamed, which is what defeats the registered label/digest/size
shortcut families. However a reader that resolved `tools/round-34/mini-fix/expected.json` (or
`spec.json`) relative to an inherited cwd would not need to decode the file at all; no
registered shortcut class does this, so the red clause would not kill it. I did **not** build
or run such a reader — this is a residual green-surface hazard, not a measured result, and it
is outside this seat's assigned audit. Mitigation is cheap if the L1 wants it (pass `cwd=` the
temp work dir, or run readers with an empty cwd); I did not make that change.

## 7. Pin integrity (read-only checks)

All computed sha256 values equal the C2 pins in `claims.json`:
`build.py c67180515bcb…`, `expected.json 5ebb5349fd21…`, `spec.json 3cb59080167d…`,
`mini-counter.py 43ef669ff6ea…`, `naive-counter.py 087c97f77ec1…`,
`replay-gate.py 8fa94b2332a6…`, and every `fixtures/*.mrec` (alpha `d1de0e6f…` … zeta
`19ff4074…`). All eight fixtures are 512 bytes, mode 0644.

## 8. Commands, exit codes, UTC (2026-10-25 all runs; `/usr/bin/python3`)

| UTC | command (cwd `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecGreenIndependence`) | exit |
|---|---|---|
| 07:18:46Z | `sha256sum fixtures-copy/*.mrec expected-lane.json` + lane pins (`build.py`, `expected.json`, `spec.json`, `mini-counter.py`, `naive-counter.py`, `replay-gate.py`) | 0 |
| 07:18:50Z | `python3 own_mrec_decoder.py fixtures-copy > own-decoded.json` | 0 |
| 07:19:22Z | `python3 independence_probes.py fixtures-copy > independence-probes.json` (v1, buggy ordering probe; superseded) | 0 |
| 07:19:33Z | regeneration + `byte_identical` comparison against lane `expected.json` | 0 |
| 07:19:48Z | spec/expected cross-check, uniqueness, counts, sizes, modes | 0 |
| 07:20:17Z | `python3 independence_probes.py fixtures-copy > independence-probes-v2.json` | 0 |
| 07:20:28Z | order-mismatch byte table (20 records, section 4) | 0 |
| 07:21:26Z | `python3 independence_probes.py fixtures-copy > independence-probes-v3.json` (authoritative probes) | 0 |
| 07:21:39Z | `python3 own_mrec_decoder.py <lane>/fixtures > lane-decoded.json`; canonical equality per fixture: all True | 0 |

No ELF carrier, fixture or reader was executed as a program of interest. No lane file was
written, staged or mutated; no counter was run against the lane.

## 9. Verdict

**PASS (independent expected-record audit).** The eight synthetic MREC fixtures decode to
exactly the 25 records in `expected.json` under an independently written decoder — 8/8
fixtures and 25/25 records, zero name/flags/value mismatches — and an independent
regeneration of `expected.json` from fixture bytes is byte-identical to the pinned file
(`5ebb5349…`). The only non-byte-derived properties are the canonical sort order and JSON
serialization, both matched by the counter's `canonical()`; no expected record is reachable
only through the author's code path. Residual unprobed risk: readers inherit the counter's
cwd, so `expected.json`/`spec.json` are reachable by path even though fixtures are renamed.
