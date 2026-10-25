# AStaticBlindness — R34-C2 wave 2: static audit of the decisive control readers

Seat: `L1Kaidoku34-2.AStaticBlindness`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scope (assignment): read `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py` and
`pathkey.py` line by line and confirm or refute that neither reads the ELF/MREC header, a record
entry, or a `name_off` field; report each read offset/function with a line pointer; name any hidden
structure use. Secondary (round context): attack the stop record, its decisive evidence, the five
disclosed defects and the proposed repairs. No claim reopened, no instrument edited, no score
awarded, no lane file other than this report and my scratch written.

Runtime: `/usr/bin/python3` = Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1 20260810].
Tooling ledger: **nothing installed or upgraded**; no `pacman`/`uv`/`npx`/network. All work on a
copy in `/fast/scratch/hyaku/kaidoku-r34b/w2/AStaticBlindness/`; no VCS mutation; no ELF carrier,
fixture or R34-C1 reader executed.

Audited artifacts (read-only, byte-identical to the frozen pins — 26/26 pins in
`.ufo/waves/round-34/r34b/instruments.json` verified against the worktree, 0 mismatches,
2026-10-25T07:33:35Z):

| file | lines | sha256 | pin |
|---|---|---|---|
| `w1/CtlMultiset-files/nameset.py` | 59 | `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` | claim-stop `source_sha256` = match |
| `w1/CtlMultiset-files/pathkey.py` | 60 | `28acfe5a79b29977c89de26accc55233d54c08daededf2452893e91043d481a9` | same as producer scratch `r_pathkey.py` |
| `tools/round-34/mini-fix/mini-counter.py` | 157 | `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52` | pin = match |
| `tools/round-34/mini-fix/expected.json` | — | `5ebb5349fd21eb3e885c775cb0068ece04188b9a9a7fdc414c1c83a2d8828483` | pin = match |

Also verified: lane copies of `nameset.py`, `pathkey.py`, `mini-counter-fresh.py` are sha256-identical
to the producer scratch originals in `/fast/scratch/hyaku/kaidoku-r34b/w1/ExecRedReproduce/`
(`2e8feaea…`, `28acfe5a…`, `5181330d…`), i.e. the L1 copied the producer's bytes without drift.

---

## 0. Axes named

1. **A1 semantic structure-blindness** — does any executed line decode a header field, a record
   entry, or `name_off`?
2. **A2 byte-level contact** — which byte ranges are actually touched, by which call, at which line?
3. **A3 key invariance** — is the shortcut's key constant across the counter's only transform?
4. **A4 falsification-chain integrity** — artifact identity, exact argv, receipts, seed claims.
5. **A5 repair adequacy** — do the stop's routed repairs (F1–F5) touch the mechanism the stop says
   falsified the measure?

---

## 1. Byte-access ledger (assignment answer, part 1)

### 1.1 `nameset.py` — every access

| # | line | call | bytes touched | offset arithmetic | decodes a field? |
|---|---|---|---|---|---|
| N1 | 46–47 | `len(sys.argv) != 2` | argv only | none | no |
| N2 | 22 | `re.compile(rb"[A-Za-z0-9_.+-]+\.so(?:\.[0-9]+)+")` | none (compiled once) | none | no |
| N3 | 48 | `Path(sys.argv[1]).read_bytes()` | **whole file, 0…EOF (512 B)**, including header `[0,16)`, record array `[16,names_off)`, name pool `[names_off,512)` | no seek, no offset, no length | no |
| N4 | 49 | `TOKEN.findall(data)` | scans every offset `0…511` of the same buffer | regex, no structural reference | no |
| N5 | 49 | `token.decode("ascii")` + `sorted({…})` | matched spans only | none | no |
| N6 | 50–53 | `key = "|".join(names)`; `TABLE[key]` | none (in-memory dict) | none | no |
| N7 | 54 | `print(json.dumps(...))` | stdout | none | no |

There is no `struct`, `unpack_from`, `int.from_bytes`, `seek`, `read(n)`, slice of `data` at a
computed offset, `MAGIC`, `MREC`, `version`, `count`, `records_off`, `names_off`, or `name_off` in
the file (grep census: the only occurrences of `name_off`/`names_off` in the source are the
docstring lines 10 and 14). `data` is referenced exactly twice: line 48 (bind) and line 49 (scan).

### 1.2 `pathkey.py` — every access

| # | line | call | bytes touched | offset arithmetic | decodes a field? |
|---|---|---|---|---|---|
| P1 | 45–46 | `len(sys.argv) != 2` | argv only | none | no |
| P2 | 47 | `path = Path(sys.argv[1])` | path string | none | no |
| P3 | 48 | `path.read_bytes()` | **whole file, 0…EOF (512 B)** | no seek/offset | no |
| P4 | 49 | `key = path.stem` | the *file name* supplied by the counter | none | no |
| P5 | 51 | `hashlib.sha256(data).hexdigest()` | whole buffer 0…511 as opaque bytes | none | no |
| P6 | 50–54 | `TABLE[key]` / `DIGESTS.get(...)` | none | none | no |
| P7 | 55 | `print(json.dumps(...))` | stdout | none | no |

No `struct`/`unpack`/offset/`name_off` anywhere; `data` is used only as the hash input (line 51).

### 1.3 Static table census (semantic content of both answer tables)

`TABLE`/`DIGESTS` were recovered with `ast.literal_eval` (parsed, **not imported or executed**):

- `nameset.TABLE`: 8 keys, each a `|`-joined **sorted SONAME set**; every value is record-identical
  (order-insensitive) to `tools/round-34/mini-fix/expected.json` for the matching fixture —
  `nameset_table_equals_expected = {alpha:true, beta:true, delta:true, epsilon:true, eta:true,
  gamma:true, theta:true, zeta:true}` (probe2 output, 07:31:48Z).
- `pathkey.TABLE`: 8 filename stems (`alpha`…`theta`) → expected records; `pathkey.DIGESTS`: the
  eight fixture sha256 values → the same stems; mapping verified 8/8 against the fixture files.
- Neither table contains a per-file `(name_off, flags, value)` triple; neither table is derived at
  runtime from the input bytes. The name→(flags,value) association is **wholly external** to the
  file, which is exactly what the stop asserts.

---

## 2. Verdict on the assigned question

**CONFIRM (operative reading) and REFUTE (literal reading).**

- **Confirmed:** neither reader *decodes* an MREC header field, a record entry, or a `name_off`
  value; neither iterates a record array; neither performs any offset arithmetic against the
  header. For `pathkey.py` the input content is used only as an opaque digest. The stop's operative
  statement — "the shortcut … walks no record array and reads no `name_off`; the association comes
  from the table, not from the bytes" — is true of both files as written.
- **Refuted as written:** the sentence "it **reads no header**" (nameset.py:9) and "never reads a
  header" (pathkey.py:5) are false at the byte-access level. Both call `read_bytes()` on the whole
  512-byte file (N3, P3), so header and record-entry bytes are in the buffer; `nameset` then applies
  a regex to **every** offset of that buffer (N4) and `pathkey` hashes **every** byte (P5). Neither
  is isolated from structure bytes; they merely never interpret them.

Corrected wording (draft only; the stop is not mine to edit): *"decodes no header field, no record
entry and no `name_off`; it scans the file's token classes and looks the answer up in a table that
bears the published expected records."*

No ELF parsing exists in either file: no `\x7fELF`, `e_shoff`, `e_phoff`, `.dynamic`, `DT_NEEDED`
or dynstr logic (grep census, 07:32:45Z, only docstring hits). The C2 surface is MREC-only; the
"ELF" half of the assignment question is vacuous for these two artifacts.

---

## 3. Hidden structure use (named, with evidence)

1. **Whole-file read as a structure-bearing buffer (both readers).** N3/P3 read the header and
   record array; nothing in either program constrains the read to the pool region. Consequence: the
   claim "structure-blind by construction" is not construction-level; it is content-level.
2. **`nameset`'s token scan can absorb record-region bytes.** Synthetic counterexample (static; a
   byte blob, no reader executed): a 512-byte MREC with `names_off=24` and one 8-byte record entry
   whose bytes spell `ab.so.1\0` yields regex matches `[(16,23,"ab.so.1"), (24,33,"libc.so.6")]`
   and key `"ab.so.1|libc.so.6"`, i.e. `key_equals_pool_only = false` (probe2.json,
   `synthetic_entry_token`, 07:31:48Z). Direction of the failure is refusal (key absent from
   `TABLE` → exit 3), not a false pass; but the reader's blindness is contingent on the header and
   record bytes carrying no token-shaped ASCII run.
3. **Pool-layout assumption without header use.** `nameset` relies on the pool being NUL-terminated
   ASCII somewhere in the file, which it discovers by scanning, not by `names_off`. It uses a
   *property* of the layout (SONAME strings exist as literal byte runs) but never the layout
   *pointer*. This is the precise sense in which it is "structure-adjacent but not structural".
4. **Answer tables are the published expected output.** All 8 `nameset` keys and all 8 `pathkey`
   keys/digests reproduce `expected.json` exactly (§1.3). The class therefore demonstrates
   *memorization of the published answer under a transform-invariant key*, not a compact invariant
   that generalises: on any unseen fixture both readers return exit 3 (verified 0/8 on the fresh
   generator, §5.3). The stop's phrase "content-multiset memorization" is accurate; a stronger
   phrase would be "published-answer replay keyed on the SONAME set".
5. **`pathkey` uses the input *name*, not content, as its primary key (P4).** Under the green
   counter this branch is dead — the counter passes `opaque-<sha256(transformed)[:20]>.data`
   (mini-counter.py:114) — which is why `pathkey` scores 0/8 on green and 8/8 on naive
   (measured, §5.2). No hidden structural use; the filename is simply a second, counter-supplied
   identity channel.

No other structure use exists: neither file imports `struct`, opens the file twice, seeks, stats
the file, or reads `os.environ`.

6. **Hidden non-use: record count is not in the key.** `nameset` builds a *set*
   (nameset.py:49, `sorted({…})`), so a fixture with two records sharing one SONAME would produce
   the same key as a one-record fixture with that name, and the replayed record list would be wrong
   for one of them. The frozen eight and the fresh generator both forbid duplicate names, so this is
   unexercised; it bounds the class (it is a memoriser of eight distinct name sets) without affecting
   the 8/8 result.

---

## 4. Key invariance measured (A3)

`permute()` (mini-counter.py:57–82) was re-implemented verbatim and applied to all eight fixtures
under the three seeds in the stop (`kaidoku-r34-mini-v1`, `alt-1`, `alt-2`). Per fixture and seed:
`size_eq=true`, `bytes_identical=false`, `decoded_eq=true`, `decoded_eq_expected=true`,
`key_eq(nameset key)=true`, `spans_outside_pool=[]` (probe2.json, 07:31:48Z, exit 0). So the
invariance the stop relies on is measured fact, not inference: the pool permutation changes every
byte layout the reader ignores and preserves exactly the set it keys on.

<details><summary>Probe commands</summary>

```
cd /fast/scratch/hyaku/kaidoku-r34b/w2/AStaticBlindness
/usr/bin/python3 -I -B probe.py   > probe.json   2> probe.err   # exit 0 @ 07:30:04Z
/usr/bin/python3 -I -B probe2.py  > probe2.json  2> probe2.err  # exit 0 @ 07:31:48Z
```
</details>

---

## 5. Reproduction of the decisive evidence (A4)

### 5.1 Exact argv from `claim-stop.json`, on the lane root (read-only; the counter writes only to
`tempfile`):

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
/usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . \
  --control-reader .ufo/waves/round-34/r34b/w1/CtlMultiset-files/nameset.py --seed <S>
```

| seed | UTC | exit | receipt | sha256 |
|---|---|---|---|---|
| `kaidoku-r34-mini-v1` | 07:30:24Z | **0** | `matched=8 target=8 met_target=true finding=records_match`, all 8 rows `ok:true, exit:0` | `c1e25a4f718e6ad0…` |
| `alt-1` | 07:30:24Z | **0** | same, 8/8 | `7c2c688aa790b245…` |
| `alt-2` | 07:30:24Z | **0** | same, 8/8 | `1923efeebad80f48…` |

Identical results on a scratch clone at 07:29:21Z (before the lane-root run). The stop's
`observed` block (exit 0, matched 8, three seeds) is **reproduced exactly**.

### 5.2 `pathkey.py` under both counters

| counter | root | UTC | exit | result |
|---|---|---|---|---|
| green `mini-counter.py` (default seed) | lane | 07:30:24Z | **1** | `matched=0 met_target=false`, every row `exit:3` |
| naive `naive-counter.py` | scratch clone (pinned bytes) | 07:29:33Z | **0** | `matched=8 met_target=true records_match` |

(The naive row was run on the scratch clone because the naive counter needs no lane-specific input;
its `mini-fix` tree is part of the 26-pin set verified above. The green row was run on the lane root
with the exact argv of `claim-stop.json`, writing only to `tempfile`.)

So the 8/8 attributed to path/digest replay in the stop's prose belongs to the **naive** counter;
under the green counter the permutation defeats it. The stop does not claim otherwise (its prose
says "payload-keyed (8/8, names zeroed)", a different artifact from `LabratSeedSensitivity`), but
the record should name the counter per class.

### 5.3 The stop's own proposed repair direction, measured

`mini-counter-fresh.py` (w1 prototype, sha256 `5181330d…`) on the scratch clone, one random seed
per run:

| reader | UTC | exit | matched/8 | seed |
|---|---|---|---|---|
| `readers/structural.py` | 07:32:16Z | 0 | **8** | `8ee165029f33263c…` |
| `nameset.py` | 07:32:16Z | 1 | **0** | `197274955499663d…` |
| `pathkey.py` | 07:32:16Z | 1 | **0** | `edded71f3b9ff423…` |

Per-run unpublished content defeats both memorisers while the structural control still meets target
— the producer's claim is confirmed on my own runs. Caveat: this prototype is **not** a pinned
instrument (absent from `instruments.json`), has no `--selftest` and no mutant set, so it cannot
inherit the frozen predicate without landing + pinning + a selftest.

---

## 6. Stop-record attack

### 6.1 What stands (checked, not assumed)

- Frozen instrument bytes: 26/26 pins verify against the worktree (07:33:35Z).
- `decisive_counterexample.source_sha256` = observed sha256 of `nameset.py`.
- Producer artifact identity: lane copies are byte-identical to the producer's scratch originals
  (three sha256 matches).
- The gate quantifies **only over the config-registered classes**: `replay-gate.py:112–127` iterates
  `config["shortcuts"]`; `over` is the set of registered rows at target. Reproduced on the clone:
  `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7
  shortcuts_over_target=-`, exit 0 (07:32:24Z), and `--selftest` 12 cases / 0 failures / 3 mutants
  killed, exit 0. An eighth, unregistered class therefore cannot move the verdict — the stop's
  statement "satisfied only because this class is unregistered" is exact.
- The frozen receipt `after/c2-at-instruments.json` carries the same green line, six clauses true,
  predicate sentence B, revision `c79bbe7b…`.
- Predicate hashes, recomputed by me: A (claims/config) `7c6c17f0…` ✔, B (c2 counter/receipts)
  `8340aea5…` ✔, C (`mini-counter.py:23`) `09988625…` ✔.

**The stop's substantive conclusion survives this audit:** a structure-blind, record-walking-free
reader meets the green counter's target at 8/8 on three seeds (exit 0), the counter's own predicate
sentence C ("only record-array traversal associates a name with its record") is false as written,
and the six frozen clauses are untouched. I find no defect that overturns the stop.

### 6.2 Record precision defects (low severity; wording, not conclusion)

- **D1 — "reads no header / no record entry" is literally false** for both readers (§2). The
  rationale sentence should say "decodes no header field / record entry / `name_off`". Evidence
  pointers: nameset.py:48,49; pathkey.py:48,51; synthetic record-region token demo §3.2.
- **D2 — F2's summary omits site C.** `claim-stop.json` describes F2 as "claims/config sentence A
  vs counter/receipt sentence B". `predicate-reconciliation.json` records **three** sites: A
  (claims + both configs), B (`c2-shortcut-gate-counter.py:23` + receipts), C
  (`mini-counter.py:23` + the naive label). The sentence the decisive counterexample is scored
  under is **C**, not B. All three hashes verify. The reconciliation file is correct; the stop's
  one-line summary is incomplete.

### 6.3 Repair adequacy (A5) — the routed repairs do not touch the decisive mechanism

- **F3's route ("assert class count == pinned count before CLEAN") cannot detect the stop's own
  counterexample.** At the falsified freeze the registered count *equals* the pinned count (7 = 7),
  so the assertion passes and the verdict is CLEAN. Count equality guards against silent *removal*
  (`replay-gate.py:58` floor, the `vacuous-no-shortcut-floor` mutant) — not against *omission at
  freeze time*, which is precisely the failure the stop reports. Evidence: `replay-gate.py:58,
  112–127`; `claim-stop.json` F3 and `kill_rule_applied`.
- **F4's route is correctly aimed but narrow.** Confirmed statically: selftest case `red-two`
  (`replay-gate.py:159`) has s1 and s2 at target, so a mutant that ignores the **last** shortcut row
  still sees s1,s2 and still returns REFUSED — the case cannot kill it; a row-count assertion (and a
  red-last case) is the right repair. This corroborates `MutGateBranches.md` F4 without rerunning it.
- **Missing route for the decisive defect.** The stop routes repairs for F1–F5 but routes none for
  the class-space gap its counterexample demonstrates. The only two mechanisms that address it are
  (a) making the expected association unpublished per run (fresh generator) or (b) non-layout
  transforms (record reorder + payload re-encoding), and neither is routed in `claim-stop.json`;
  the producer's `mini-counter-fresh.py` is not referenced there. Severity: medium — route gap,
  not a false statement.

### 6.4 Defects found in the frozen counter itself (context, not repair)

1. **`permute()` misparses the pool.** It slices `pool = data[names_off:]` (line 60) and splits on
   NUL to the **end of file**, so the trailing zero padding becomes hundreds of empty "strings":
   measured slot counts `alpha 445, beta 474, delta 452, epsilon 468, eta 436, gamma 392, theta 378,
   zeta 410` versus 1–6 real names. Consequence: the shuffle is over ~380–475 empty slots, and the
   real names move with probability ≈ 1 − 1/slots per name. Decoded output is still preserved
   (measured `decoded_eq=true` for all 8 × 3 seeds), so no current false result — but the transform
   is not "name-pool reordered" in the sense the docstring claims.
2. **The `permute_size` guard (`mini-counter.py:76–77`) is vacuous**: the rebuild is a reordering of
   NUL-terminated segments, so `len(new_pool) == len(pool)` always. It cannot fire.
3. **`permute()` hardcodes the record base at 16 (`mini-counter.py:80`) while `decode_fixture()`
   reads `records_off` from the header (line 43).** Any fixture with `records_off != 16` would be
   silently corrupted by the transform. Unreachable with the frozen fixtures and the fresh
   generator (both use 16), but it is a latent inconsistency between decode and transform.
4. **The counter does not check that `permute` preserves the decoded records** (no
   `decode(transformed) == expected` assertion in `score`, lines 100–132); it only compares reader
   output to `expected`. A transform bug would be scored as a reader failure. I verified preservation
   independently (§4); the instrument does not.
5. **The answer key and the reader share a filesystem.** `subprocess.run` (line 116) passes no
   `cwd=`, so the reader inherits the counter's cwd, and `expected.json` is resolved at
   `<root>/tools/round-34/mini-fix/expected.json` (line 102) with `--root .` in the receipt — i.e.
   readable by the reader at run time. `-I -B` and the scrubbed env do not isolate the filesystem.
   This does not create a new class (a reader still needs the transform-invariant key that `nameset`
   demonstrates) but it removes any doubt that the surface can distinguish decoding from reading the
   key. This strengthens the stop's finding and is not disclosed among F1–F5.

### 6.5 F1 and F5 corroborated (static / read-only)

- F1: `freeze-integrity.py:92–98` requires a top-level non-empty `instruments` object;
  `.ufo/waves/round-34/r34b/claims.json` carries pins under `claims[0].pins` and has **no**
  top-level `instruments`; `.ufo/waves/round-34/r34b/instruments.json` supplies a 26-entry top-level
  map (`frozen_claims_sha256` = `de3afbfb…`, and `sha256(claims.json)` = `de3afbfb…`, verified).
  I did **not** run `freeze-integrity.py` (assignment forbids running frozen instruments beyond
  readers-via-counter; the schema defect is statically evident).
- F5: `git cat-file -t b917ea64ebbeab49b8258d71ffb34e700715ffe6` → `commit`; `cd75b92e` → `commit`
  (read-only, 07:32:52Z).

---

## 7. Residual risk and verification gaps

- **Authorship independence is unverifiable from bytes.** I confirmed artifact identity (lane copies
  = producer scratch, sha256), not who authored them. The stop's `producer_seat` claim rests on the
  seat record, not on evidence I can check.
- **Seed coverage.** Three seeds plus one random seed on the fresh generator. No sweep; the
  invariance argument is structural (measured on 3 seeds, argued for all).
- **Fresh-generator soundness not proven.** `mini-counter-fresh.py` has no selftest, no mutants, is
  not pinned, and its hit probability against blind guessing was not measured by me.
- **Counter transformation under non-16 `records_off`** is unsound statically (§6.4.3); not
  exercised, because creating or running a mutated fixture was out of scope.
- **Not run (unrun checks must not be read as passed):** `freeze-integrity.py`,
  `c2-shortcut-gate-counter.py`, `mini-fix/build.py`, any ELF carrier, any R34-C1 reader, and the
  twelve pinned shortcut readers other than `structural.py` (which I ran only as the fresh counter's
  positive control and the gate selftest's positive control).
- Scratch receipts (sha256): `probe2.json 35b8ac9b…`, `gate-mini.out 371c15e7…`,
  `fresh2-structural.json e53352a1…`, `fresh2-nameset.json c080be2b…`,
  `fresh2-pathkey.json 53fcd9e8…`, `naive-nameset.json` = `naive-pathkey.json 42ab0733…`.
  Scratch is `/fast/scratch` and may be reclaimed; every command and exit above stands alone.

---

## VERDICT

`STATIC_AUDIT(nameset.py, pathkey.py): CONFIRM no header-field / record-entry / name_off decode, no
record-array walk (read sites N3/N4/N5 and P3/P4/P5 only); REFUTE the literal "reads no header" —
both read whole-file bytes and nameset scans every offset, and its key can absorb record-region
tokens (synthetic match at [16,23)). DECISIVE EVIDENCE REPRODUCED — nameset matched=8/target=8,
exit 0, seeds kaidoku-r34-mini-v1/alt-1/alt-2 (07:30:24Z); pathkey 0/8 green vs 8/8 naive.
STOP CONCLUSION HOLDS; defects are record-level: D1 wording, D2 F2 omits predicate site C, F3's
class-count repair cannot detect the unregistered class that produced the stop, and the frozen
counter's permute has a misparsed pool, a vacuous size guard, a hardcoded record base and no
decode-preservation check. No claim reopened, no instrument edited, no score awarded.`
