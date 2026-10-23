# CtlHashReplay — SHA256-of-input keyed lookup control (round 34, wave 1)

Seat: `CtlHashReplay` (executor, leaf) · Axis: **depth** · Milestone: fresh pre-data skip-work controls, source reopens, independent expected audits, bounded repair falsification.

**Result: the control does NOT satisfy P34-version-needs at freeze.** Measured `matched = 1` of `target = 12`, `met_target = false`, `finding = version_needs_mismatch`, counter exit **1**, on three independent runs. This is a **miss to report, not a target rescale**: the frozen predicate, target, and counter were read from the frozen claims blob and were not amended, retargeted, or repaired after seeing the result.

## 1. What was built

The cheapest possible skip-work reader, generated deterministically from the frozen manifest.

| Item | Value |
|---|---|
| Control reader source | `controls/round-34/ctl-hash-replay.py` |
| sha256 of reader | `ad53c934be5260f032e220a7f795a12586dfbb5010f341a45641699322084512` |
| size | 46307 bytes |
| generator | `controls/round-34/gen_ctl_hash_replay.py` (sha256 `ad1a83e79824ffc130105498dbd312bccada93db4f41cbc64a1fcc998c8e96cc`) |
| table size | 12 keys (one per frozen carrier) |
| table key | the frozen manifest `sha256` of each original carrier |
| table value | the frozen `expected` record for that carrier, verbatim |
| lookup | `TABLE[sha256(input_bytes)]` |
| miss behaviour | prints `{"schema": 1, "needed": []}` |
| parse behaviour | **none** — no ELF byte is interpreted |

The reader is a literal digest lookup. It reads the input file solely to hash it; it never inspects a magic number, section header, program header, dynamic table, `.gnu.version_r`, string table, or any other ELF structure. The generated table is derived from `.ufo/waves/round-34/expected.json` at freeze `54a87a51a865ab931fd355e767303337b05cccf4` (manifest sha256 `f22e7e3b8f70c7a5dda784919f6df53a1feaf11cca0e4bba767509d51717974d`, verified equal to `claims.manifest_sha256` by the generator).

The generator is the only thing that reads the manifest; the scored reader is a self-contained static table.

## 2. How it was scored

Frozen `--control-reader` scoring at the freeze revision, in the seat sandbox only. The production reader `tools/round-34/elf-version-needs.py` was **never executed** (enforced mechanically by a deny list in `run_receipts.py`; the production reader is not on any probe argv, and every scored argv is recorded verbatim below). No binary fixture was authored, manufactured, or written; the counter's own schedule-1 candidates are generated in-process by the frozen counter into its own temporary directory.

Exact argv (identical for runs 1–3):

```
python3 -I -B tools/round-34/version-needs-counter.py \
  --root /fast/scratch/hyaku/kaidoku-r34/w1/CtlHashReplay \
  --rev 54a87a51a865ab931fd355e767303337b05cccf4 \
  --freeze 54a87a51a865ab931fd355e767303337b05cccf4 \
  --control-reader controls/round-34/ctl-hash-replay.py
```

`--rev` and `--freeze` are both the freeze revision, per the wave instruction. The counter's own frozen blob was used (`sha256 d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`, equal to `claims.instruments["tools/round-34/version-needs-counter.py"]`), so `running_counter_pin` and every `instrument_pin` passed.

### Measured results (three runs)

| Probe | UTC start | exit | matched | target | met_target | finding | documents_ok |
|---|---|---|---|---|---|---|---|
| ctl-hash-replay-run1 | 2026-10-23T10:56:26Z | 1 | 1 | 12 | false | version_needs_mismatch | true |
| ctl-hash-replay-run2 | 2026-10-23T10:56:27Z | 1 | 1 | 12 | false | version_needs_mismatch | true |
| ctl-hash-replay-run3 | 2026-10-23T10:56:27Z | 1 | 1 | 12 | false | version_needs_mismatch | true |

All seven document bindings were green at the measured revision (`corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `.ufo/waves/round-34/approved-skill-section.txt`, the `SKILL.md` section, `corpus/SOURCES.md#S103`, `corpus/SOURCES.md#S104`, and both frozen source captures). The failure is entirely in the reader, not in the document bindings.

### Per-schedule breakdown (the decisive axis)

| schedule | carriers matched | carriers missed |
|---|---|---|
| 0 — original bytes | **12 / 12** | 0 |
| 1 — randomized same-length string-table naming | **1 / 12** (e12 only) | 11 |

Row-level result: only `e12` has `matched = true`; `e01`–`e11` each match on schedule 0 and miss on schedule 1.

- **Original schedule may match — confirmed.** Every one of the twelve original carriers was hashed to a table key present in the map and returned the exact frozen expected record. The map is therefore not merely a lucky partial hit: it reproduces all twelve records exactly, including e11's 61 needed records / 77 auxiliary records and e08's 25 needed records.
- **Randomized string-table schedule defeats the hash map — confirmed.** The counter's schedule-1 candidate is the original bytes with the linked string table substituted under an unpredictable Sattolo permutation, so the file's sha256 changes and the digest no longer keys the table. The reader then emits the empty record, which mismatches the eleven nonempty carriers' frozen expectations. The permutation differs across runs: the schedule-1 input digests for all eleven nonempty carriers differ between run1/run2/run3, while the schedule-0 input digests are byte-identical across all three runs. The challenge is unpredictable, and the map is defeated by it.

`e12` is the documented exception: it has no `.gnu.version_r` / no version requirements and no `string_table` entry in the frozen manifest, so the counter replays its original bytes on schedule 1 as well. Its schedule-0 and schedule-1 input digests are equal (`1dc03d8fdacc17b802b28a01407ba0a814ee8fbf9d83522065773e09fd964aa1` both times). Its expected record is empty, so the reader's miss branch coincidentally produces the correct empty record. **e12's single match is an artifact of the empty-record case, not evidence of parsing.**

## 3. Depth probes (all exercised, all retained)

### 3.1 Table fidelity against the frozen manifest — PASS

`controls/round-34/check_table_fidelity.py`, exit 0, `passed = true`:

- `table_size = 12`, `manifest_carriers = 12`, `table_keys_equal_manifest_digests = true`
- `every_carrier_present = true` — every frozen carrier's blob digest, re-read from the freeze revision, is a table key
- `every_table_value_equals_frozen_expected = true` — every table value equals the frozen `expected` record exactly (dict equality, not a projection)
- `every_probe_digest_misses = true` — a single-byte in-memory perturbation of each carrier's string table (offset inside the linked string table for e01–e11; byte 0 for e12, which has none) yields a digest absent from the map, and the lookup falls through to the empty record. The perturbation is held in memory and never written to disk; no ELF is authored.
- `elf_interpretation_tokens_in_source = []` — regex scan for `\be_ident\b`, `\bstruct\b`, `\bEI_NIDENT\b`, `\bSHT_\w+`, `\bDT_\w+`, `\belf\.h\b`, `\bmagic\b`, `\bunpack\b`, `\bELFMAG\b`, `\bPT_LOAD\b`, `\bVerneed\b`, `\bVernaux\b`, `\bdynstr\b` over the reader source: zero hits.

### 3.2 Reader file-access audit — PASS

`controls/round-34/audit_reader_access.py` runs the reader under `sys.addaudithook` and records every file opened, so "reads input solely to hash it" is backed by an observed file list, not by source reading. Distinct paths opened for `e01` and for `e12`: the reader source itself, the input carrier, and CPython stdlib (`hashlib.py`, `pkgutil.py`, `weakref.py`, `_weakrefset.py` + their `.pyc`). **No other file is touched** — the reader reads no manifest, no expected JSON, no table file at runtime; the table is compiled into the source. Exit 0 for both.

### 3.3 Counter selftest — PASS

`python3 -I -B tools/round-34/version-needs-counter.py --selftest`, exit 0, `passed 11 / total 11` (`green-empty`, `red-junk`, `red-all-false`, `red-duplicate-json`, `red-exit`, `red-documents`, `red-boolean-schema`, `red-pin`, `red-manifest-count`, `green-translated`, `red-replay`). The counter's own text-only outer-CLI machinery is intact at this revision; note the built-in `red-replay` case, which the frozen counter already rejects for the same class of reason as this seat's control.

### 3.4 Degenerate baseline for attribution — measured, and a genuine finding

`controls/round-34/ctl-degenerate-empty.py` (always prints the empty record) was scored with the identical frozen `--control-reader` command, exit 1: `matched = 1`, `finding = version_needs_mismatch`, with schedule-0 matched count **1** and schedule-1 matched count **1** (only `e12`).

**This is the reportable depth finding:** the aggregate `matched` count of the hash-replay control (1) is *identical* to the aggregate count of a reader that does nothing but print `{"schema": 1, "needed": []}`. The aggregate alone cannot distinguish "hashes the input and replays the frozen record" from "does not read the input at all". The discrimination lives entirely in the per-schedule, per-row detail (12/12 vs 1/12 on schedule 0), which the counter does emit. Any future adjudication that reads only the scalar `matched` field of a `--control-reader` score cannot tell a replay attack from a no-op reader; the per-row `attempts` array must be read. This is a counter-reporting observation, not a counter defect — the counter's predicate outcome is correct in both cases and the counter itself never surfaces the distinction as a scalar.

### 3.5 Optional frozen author schedule — all miss — PASS

`controls/round-34/check_author_schedule_miss.py`, exit 0, `all_miss = true` over 11 mutants. The optional fixed author schedule (`.ufo/waves/round-34/prep/R34Expected-files/challenge/`, `m01.bin`–`m11.bin`) is **not** the production counter's schedule, so this is supplementary. Each of the eleven mutants hashes to a digest absent from the map (e.g. `m01.bin` → `1544363e728a10bb…`, `m11.bin` → `cad85ea1a123b0dd…`), and no mutant digest equals any original carrier digest. The map is defeated by the optional fixed schedule too, not only by the unpredictable production schedule. e12 is correctly excluded from that schedule, matching `claims.empty_control`.

## 4. Evidence retained

Archived under `.ufo/waves/round-34/w1/CtlHashReplay-files/` (lane write scope; sandbox copies are byte-identical, verified by sha256 on all seven sources):

```
CtlHashReplay-files/
  ctl-hash-replay.py            ad53c934be5260f032e220a7f795a12586dfbb5010f341a45641699322084512  46307
  gen_ctl_hash_replay.py        ad1a83e79824ffc130105498dbd312bccada93db4f41cbc64a1fcc998c8e96cc   4105
  check_table_fidelity.py       4af68f8c87eb72da9c1951818c01167f3eb2d88f08910fbf765ab5c4bdf19531   5160
  check_author_schedule_miss.py 3f7645089bd603297c17a8aba9591b10f5fe193db8585a4f05ca57f520739ccb   2287
  audit_reader_access.py        3f0cdb71db891eded01ebd719094178af4b82a05872a01c6165dd523a1d706b2   1327
  run_receipts.py               6acad5e0d8400349afd0affde3743fe07c7033c2ae869307f1365af302ee9a20   5831
  ctl-degenerate-empty.py       85ab1b7e88e52638fca6da954088a3c7da8afd1cf0be8c7153d6d9a7a197dca6    615
  receipts/
    receipts.json               f7331dd593128fa4…  (29060)  exact argv / UTC start / UTC end / exit /
                                                   stdout sha256 / stderr sha256 per probe, plus the
                                                   artifact digest table
    ctl-hash-replay-run{1,2,3}.stdout   43976 bytes each  full counter JSON, per-row per-schedule detail
    ctl-hash-replay-run{1,2,3}.stderr   0 bytes
    degenerate-empty-baseline.stdout    14512
    table-fidelity.stdout               7729
    author-schedule-miss.stdout         3482
    counter-selftest.stdout             1206
    reader-access-audit-e{01,12}.stdout / .stderr
```

Every stderr file is empty (0 bytes) — the control and every probe ran without diagnostics.

**Sandbox / VCS.** All work is in the seat sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/CtlHashReplay` on branch `seat-r34-CtlHashReplay`, base `54a87a51a865ab931fd355e767303337b05cccf4`, committed as `f2ee1007` (control sources) and `8018967a` (extended receipt harness). `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` were unset for every Git call; nothing was pushed; no Git or jj write touched the lane or any shared production file. The sandbox's sparse-checkout list was extended with `controls/` so the control sources could be committed — a sandbox-local sparse-checkout setting only, with no effect on the lane.

## 5. Scope compliance

- Production reader `tools/round-34/elf-version-needs.py`: **not executed**. Denied by an argv deny list inside `run_receipts.py` before each probe runs; absent from every recorded argv.
- No REA run, no held-item reconstruction, no loader execution, no target binary execution.
- `U064N008Hf47eb933` and `R33FixtureBuilder` and derivatives: untouched, not read, not used.
- No binary fixture authored. The only bytes written by this seat are Python source and JSON/text receipts. The byte perturbations in §3.1 exist only in process memory.
- Expected-author optional fixed schedule was used only as a **read-only** supplementary probe (§3.5), never as a production data producer; the production counter's own unpredictable schedule was the only thing that scored the control.
- The frozen predicate string is quoted verbatim from `claims.json` and the counter's own constant; it was not rewritten, narrowed, or repaired.
- No shared production file was edited. The only lane writes are this report and the `CtlHashReplay-files/` archival directory.
- No builds, linters, or formatters run; the only executed code is this seat's own bounded probes, each under `timeout`, sequentially, with no background jobs and no leftover processes (verified by `pgrep` after the last probe: no matches).

## 6. Risks, blockers, and open items

- **No blocker.** The assignment was fully executable as specified.
- **Counter-reporting risk (advisory to L1, not a change request):** as established in §3.4, the scalar `matched` in a `--control-reader` score is not sufficient to distinguish a hash-replay skip-work reader from a do-nothing reader — both score 1/12 here. The per-row `attempts` breakdown is the only signal that separates them. If the wave's admission rule reads only the scalar, a replay control could be misread as equivalent to a trivial one; if it reads the per-schedule detail, the replay control is correctly identified as matching the original schedule on all twelve and failing the randomized schedule on eleven.
- **The hash map is defeated, not merely incomplete.** A reader that wanted to defeat the counter must actually parse the ELF; the digest lookup cannot, because the counter's schedule-1 candidate is a byte-different file whose digest is not a key. This is the intended shape of the result: the frozen counter rejects a pure-replay reader.
- **Tool installs:** none. No `pacman`, `uv tool`, `cargo`, or `npm -g` install was performed; nothing was needed beyond the host's stock `python3` (3.14) and `git`.
- **Residual risk in §3.1:** the byte-perturbation probe uses a single perturbation offset per carrier. It establishes hash sensitivity, not a proof of no alternate keying; the §3.2 file-access audit and §3.1 token scan are the structural evidence that no ELF parsing occurs.

## 7. Files written

Lane (this seat's exclusive write scope only):

- `.ufo/waves/round-34/w1/CtlHashReplay.md` — this report (the report does not state its own digest; measure it from the working tree)
- `.ufo/waves/round-34/w1/CtlHashReplay-files/` — 7 source files + `receipts/` with 19 receipt files (see §4 for digests)

Sandbox `/fast/scratch/hyaku/kaidoku-r34/w1/CtlHashReplay`, branch `seat-r34-CtlHashReplay`, commits `f2ee1007` and `8018967a`:

- `controls/round-34/ctl-hash-replay.py` — the scored control reader
- `controls/round-34/gen_ctl_hash_replay.py` — deterministic generator (manifest → table → reader source)
- `controls/round-34/check_table_fidelity.py` — §3.1 fidelity + no-ELF-token probe
- `controls/round-34/check_author_schedule_miss.py` — §3.5 optional-schedule probe
- `controls/round-34/audit_reader_access.py` — §3.2 syscall-level file-access audit
- `controls/round-34/run_receipts.py` — §4 receipt harness (enforces the production-reader deny list)
- `controls/round-34/ctl-degenerate-empty.py` — §3.4 attribution baseline
- `controls/round-34/receipts/` — 19 receipt files including `receipts.json`

No other file was created, modified, or deleted anywhere.

## 8. One-line verdict

`CtlHashReplay`: the cheapest SHA256-of-input keyed lookup control, built over all twelve frozen original expected records, scored at the freeze revision with `--control-reader` on three runs, **matched 1 / target 12, met_target false, finding version_needs_mismatch** — it replays every original schedule exactly (12/12) and is defeated by the randomized string-table schedule on all eleven nonempty carriers (1/12), which is the expected and correct behaviour of the frozen counter against a pure-replay skip-work reader. Exact source and receipts are archived under `.ufo/waves/round-34/w1/CtlHashReplay-files/`.
