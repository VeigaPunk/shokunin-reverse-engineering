# ScribeKnowledgeEntry — round 34, run-6 re-dispatch, wave 1

Seat: `L1Kaidoku34-2.ScribeKnowledgeEntry`. Draft only. No lane file other than this report was
written; no VCS command, no `pacman`, no network, no ELF carrier, fixture or reader executed as a
program. Tool installs: none (no gap hit; `python3` = `/usr/bin/python3` sufficed).

Claim context (not re-scored, not re-frozen here): R34-C2, `depth`, frozen instruments at
`c79bbe7b0959132b9873ff3431cf5eb313b58b33`. Inherited R34-C1 stays untouched; its production reader
and twelve carriers were not executed or scored by this seat.

---

## 1. Behavior observed

### 1.1 Frozen-instrument pins match the claims file (observed, not assumed)

Command (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`), 2026-10-25T07:19Z, exit 0:

```
sha256sum tools/round-34/mini-fix/fixtures/*.mrec tools/round-34/replay-gate.py \
          tools/round-34/c2-shortcut-gate-counter.py tools/round-34/gate-config-mini.json \
          tools/round-34/gate-config-naive.json
```

All 12 digests equal the `pins` map in `.ufo/waves/round-34/r34b/claims.json` exactly —
gate `8fa94b23…` , counter `41d5970…`, configs `4483f385…` / `72b12941…`, the eight fixtures
`alpha d1de0e6f…`, `beta a8547fcf…`, `delta 79ff7036…`, `epsilon 82f03f99…`, `eta 5bcabeb2…`,
`gamma ffb57ecd…`, `theta b1f87d7c…`, `zeta 19ff4074…`. Fixtures are `512` bytes, mode `644`
(`stat -c '%n %s %a'`, same session).

### 1.2 Gate self-test reproduced independently

```
python3 -I -B tools/round-34/replay-gate.py --selftest
```
2026-10-25T07:19:49Z, **exit 0** — `{"cases": 12, "failed": [], "failures": 0, "mutants": 3,
"mutants_killed": 3}` (transcript: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/gate-selftest.txt`).
Twelve cases = six verdict cases + two schema refusals + one absent-positive + three mutant kills.

### 1.3 Nine readers scored on both surfaces (my own runs)

```
python3 -I -B tools/round-34/mini-fix/{mini,naive}-counter.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --control-reader tools/round-34/mini-fix/readers/<class>.py
```
2026-10-25T07:20:22Z, receipts in `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/matrix/`:

| class | green (permuted) | red (pristine) |
|---|---|---|
| structural (positive) | **8/8, exit 0** | 8/8, exit 0 |
| all-false | 0/8, exit 1 | 0/8, exit 1 |
| size-keyed | 1/8, exit 1 | 1/8, exit 1 |
| fixed-slice | 0/8, exit 1 | 0/8, exit 1 |
| digest-keyed | 0/8, exit 1 | 0/8, exit 1 |
| string-scan | 0/8, exit 1 | 0/8, exit 1 |
| record-order-replay | 0/8, exit 1 | 0/8, exit 1 |
| label-memorization (`label_replay_full.py`) | 0/8, exit 1 | **8/8, exit 0** |
| `label_keyed.py` (present, **not registered**) | 0/8, exit 1 | 0/8, exit 1 |

### 1.4 The three gate verdicts, reproduced with my own receipts

```
python3 -I -B tools/round-34/replay-gate.py --root <LANE> --config <cfg> --json-out <receipt>
```
2026-10-25T07:22:10Z:

| config | exit | line |
|---|---|---|
| `tools/round-34/gate-config-mini.json` | 0 | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` |
| `tools/round-34/gate-config-naive.json` | 2 | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` |

These match the frozen production receipt `.ufo/waves/round-34/r34b/after/c2-at-instruments.json`
(`clauses` all true, `green.positive_matched=8`, `red.classes_over_target=["label-memorization"]`)
and the before receipt `.ufo/waves/round-34/r34b/before/c2-at-base.txt`
(`GATE_COUNTER_UNEVALUABLE finding=gate_absent … ec3125ad…`, exit 2). I am not asserting the
counter's six clauses; the Exec seats own the recount. My two lines only show the gate's own
verdict tokens are the ones the entry must document.

### 1.5 Five controls, receipts inspected

`.ufo/waves/round-34/r34b/controls/`; sources in `controls/gates/`:

| control | exit | `clauses_failed` |
|---|---|---|
| `do-nothing` (`--gate …/absent-gate.py`) | 2 | receipt has **no** `clauses` map; `gate_present=false`, `finding=gate_absent` |
| `gate-always-clean.py` (`if False:` replacing `if over:`) | 1 | `red_refused`, `selftest_clean` (`selftest_failures=2`) |
| `gate-vacuous-no-floor.py` (drops `< MIN_SHORTCUTS`) | 1 | `selftest_clean` (`selftest_failures=1`) |
| `gate-no-positive-check.py` (`if False:` replacing the positive check) | 1 | `mutants_killed`, `selftest_clean` (`mutants_killed=2`, `selftest_failures=2`) |
| `gate-junk-clean.py` (prints fixed CLEAN fields) | 1 | `red_refused` only (`selftest_failures=0`, `mutants_killed=3`) |

---

## 2. Gates run

| gate | command | exit | UTC |
|---|---|---|---|
| pin identity | `sha256sum` on the 12 pinned paths | 0 | 2026-10-25T07:19Z |
| gate self-test | `python3 -I -B tools/round-34/replay-gate.py --selftest` | 0 | 2026-10-25T07:19:49Z |
| green surface | `replay-gate.py --config gate-config-mini.json` | 0 | 2026-10-25T07:22:10Z |
| red surface | `replay-gate.py --config gate-config-naive.json` | 2 | 2026-10-25T07:22:10Z |
| superset-config probe (seat-local) | `replay-gate.py --config …/gate-config-mini-plus-unregistered.json` | 2 | 2026-10-25T07:22:10Z |

No build, lint or bulk suite was run. No ELF bytes were executed; readers ran only as Python under
the counters, exactly as the lane rule permits.

---

## 3. Touched surfaces

- Written: this report only,
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w1/ScribeKnowledgeEntry.md`.
- Written (scratch): `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/` —
  `gate-selftest.txt`, `gate-{green,red,plus}.{txt,json}`, `gate-config-mini-plus-unregistered.json`,
  `matrix/` (22 receipts + stderr), `attack/{topology_keyed.py,scalar_anchor.py,record-orders.json}`.
- Not written: `corpus/**`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, any lane tool,
  VCS state, any other seat's files.

---

## 4. Findings

**F1 — the CLEAN verdict is registry-relative; the green surface does not defeat topology
memorization (depth).** `mini-counter.permute()` (`tools/round-34/mini-fix/mini-counter.py:72-96`)
reorders only the name pool and rewrites each record's `name_off`. Record count, record order,
`flags`, `value`, `records_off` and `names_off` are all preserved. Two seat-built readers that
resolve no name and read no pool byte therefore stay at 8/8:

```
python3 -I -B tools/round-34/mini-fix/mini-counter.py --root <LANE> \
  --control-reader /fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/attack/{topology_keyed,scalar_anchor}.py
```
2026-10-25T07:21:58Z — both exit 0, `matched=8, met_target=true` on **both** surfaces
(`matrix/mini-topology_keyed.json`, `matrix/mini-scalar_anchor.json`,
`matrix/naive-topology_keyed.json`, `matrix/naive-scalar_anchor.json`). `topology_keyed` keys on the
`(flags,value)` sequence; `scalar_anchor` keys on `(count, first record's value)` and emits a fully
memorized record list. Both are exactly the family QUALITY 67 names — "memorizes topology/scalars".
Registering them in a copy of the green config makes the pinned gate refuse:

```
REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=7
  shortcuts_over_target=scalar-anchor,topology-keyed
```
(exit 2, `gate-plus.json` + `gate-plus.txt`, 2026-10-25T07:22:10Z). So the frozen `green_clean`
clause is true, but it asserts only "none of the seven *registered* classes meets the target".
This is a completeness limit, not a claim miss: no registered clause moved, and nothing was
re-scaled. The durable fix would be a green surface that also mutates the scalars the memorizer
echoes (fresh fixtures with a private oracle), or registering a topology class — neither is done
here.

**F2 — `selftest_clean` and `mutants_killed` are self-reported by the gate under test.**
`gate-junk-clean.py` prints a hardcoded `--selftest` summary and fixed CLEAN fields; the counter
scores it `selftest_failures=0, mutants_killed=3`, i.e. both clauses pass, and only `red_refused`
catches it (`.ufo/waves/round-34/r34b/controls/gate-junk-clean.py.json`). The self-test clause
therefore constrains the gate's behaviour only when the gate actually runs it.

**F3 — S106 does not support "sh_link selects the lookup string table".**
`corpus/knowledge/2026-10-23-r34-elf-version-needs.md` states "use section `sh_link` to select its
string table, not a guessed section name". The pinned binutils capture validates
`sh_link → SHT_STRTAB` only as a warning condition (`readelf.c:8547-8558`) and resolves `vn_file` /
`vna_name` through `filedata->dynamic_strings`, bound to the section *named* `.dynstr`
(`readelf.c:445-459`, `8321-8333`). Those are different claims; the earlier entry's wording needs a
measured correction, which is the L1's call, not mine to edit.

**F4 — most registered classes carry no falsification evidence.**
Five of seven classes score 0/8 on *both* surfaces; `size-keyed` scores 1/8 on both (its template is
exactly alpha's three records); only `label-memorization` moves between surfaces (0/8 → 8/8). The
four 0/8-on-red classes cannot show a counter is falsifiable — they only populate the floor. And
`readers/label_keyed.py` exists but is registered in neither config.

**F5 — S106 capture provenance gap (routed).**
`/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/` holds two real captures —
`readelf.c` 656 703 B `sha256 943be51242fb13f627577328a5d8f4105188e39771184eeeea2bd4708310235d`
and `readelf-2_47.c` 689 644 B `sha256 7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff` —
plus `readelf-binutils-2_44/2_45/2_46.c` and `t1`/`t2` which are 14-byte `404: Not Found` bodies
(`t2` is byte-identical to `readelf.c`), and `tags.json` (280 B) which is a GitHub API rate-limit
message rather than a tag list. No fetch log binds a URL or tag to either capture, so S106's `source`
cell must come from that seat's report; I did not infer it. The two captures' verneed blocks are the
same text (line numbers differ: 13343-13460 vs 14020-14123), so the entry's anchors hold for both.

---

## 5. Draft entry (for the L1 to land at `corpus/knowledge/2026-10-25-r34-pre-freeze-shortcut-replay-gate.md`)

```md
source: S106 — binutils `readelf.c` at the pinned release tag recorded in the SOURCES row (captures: /fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf.c, sha256 943be51242fb13f627577328a5d8f4105188e39771184eeeea2bd4708310235d, and …/readelf-2_47.c, sha256 7e81eedf19b2b93663bb3f598f74b54c107bd699f551667eb1b3d0e33eddeeff); local instruments under tools/round-34/ at c79bbe7b0959132b9873ff3431cf5eb313b58b33
verified-at: 2026-10-25; gate self-test, green/red verdicts and per-class scores re-observed by L1Kaidoku34-2.ScribeKnowledgeEntry (.ufo/waves/round-34/r34b/w1/ScribeKnowledgeEntry.md); production verdicts and the six C2 clauses remain bound to .ufo/waves/round-34/r34b/after/c2-at-instruments.json
recheck: python3 -I -B tools/round-34/replay-gate.py --root <LANE> --config tools/round-34/gate-config-mini.json (expect REPLAY_GATE_CLEAN, exit 0); … --config tools/round-34/gate-config-naive.json (expect REPLAY_GATE_REFUSED, exit 2); python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>; reopen S106 on a binutils release change

# Pre-freeze shortcut-replay gate: refuse a counter that shape can satisfy

## Question and novelty

How do you know that a finite ELF structural-decoding counter measures structure and not the shape
of its fixtures, *before* the counter is frozen? QUALITY 67 makes this a pre-freeze obligation for
the lane:

> "Before freezing a finite ELF structural-decoding counter, exercise a structure-blind replay keyed
> on invariant fixture identity (for example, size) that memorizes topology/scalars and reads only
> fixed name slices. Randomized names or opaque paths alone do not force record traversal."
> (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:77`)

The obligation exists because r34's earlier counter was accepted by a size-keyed fixed-name-slice
replay at 12/12 with no ELF structural decoding (`corpus/lessons/round-34.md:18`, M34-4;
`.ufo/waves/round-34/w1/CtlLabels-files/size-pristine.receipt.json`). This entry records the gate
built for the next counter and, more usefully, exactly how narrow its CLEAN verdict is.

## What "structural decoding" means for a version-needs reader (S106)

binutils `readelf` is the lane's legitimate-reader ground. Its GNU version-needs walk, in decode
order:

| Step | What the reader does | Anchor |
|---|---|---|
| Section gate | A section of type `SHT_GNU_verneed` is only well-formed when `sh_link` indexes an `SHT_STRTAB`; otherwise it warns and the association is not trusted | `readelf.c:8547-8558` (capture: `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf.c`) |
| Body fetch | The whole section is fetched once by `sh_offset`/`sh_size`, and `endbuf` bounds every later read | `readelf.c:13373-13379` |
| Entry walk | The entry count comes from the section header (`sh_info`); each `Verneed` is a fixed 16-byte record decoding `vn_version, vn_cnt, vn_file, vn_aux, vn_next` | `readelf.c:13381-13399` |
| Record-relative advance | The auxiliary array starts at `entry + vn_aux`; each `Vernaux` advances by its own `vna_next`; the next entry advances by `vn_next`. Offsets are relative to the record, never to file offset zero | `readelf.c:13412-13453`, `13459-13470` |
| Malformed records | A `vn_next`/`vna_next` smaller than the record, or an offset past `endbuf`, warns and terminates the loop instead of trusting the declared count | `readelf.c:13441-13450`, `13459-13466` |
| Name resolution | Names are *offsets into a string pool* (`vn_file`, `vna_name`), validated as `offset < pool_length` before use; the pool is `filedata->dynamic_strings`, bound to the `.dynstr` `SHT_STRTAB` | `readelf.c:445-459`, `8321-8333`, calls at `13403` and `13431` |

So "structural decoding", for this record family, is four properties together: the **record array**
declares count and order; every link is **relative to the record that holds it**; every name is a
**validated offset into a pool**; and every read is **bounded before use**. A reader that slices
fixed byte positions, replays a memorized record set, or scans printable runs has none of the four —
it can match bytes without ever associating a name with the record that declares it.

Two source boundaries worth keeping explicit. First, `readelf` only *validates* `sh_link` and then
looks names up in the section named `.dynstr`; a local reader that resolves names through the
verneed section's `sh_link` target is making a different, narrower choice, and S106 does not
authorise the sentence "sh_link selects the lookup table". Second, the walk above is printing
behaviour observed in source; it establishes field order and bound-checking discipline, not loader
acceptance, authenticity or symbol resolution.

## The gate, its three verdicts and the exact clause each depends on

Instrument: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-34/replay-gate.py`
(sha256 `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558`). It is generic: it runs
whatever counter argv a config names, substituting the reader path for the single `{reader}`
placeholder, and reads that counter's own `matched`/`target`/`met_target` fields.

| Verdict | Exit | Depends on |
|---|---|---|
| `REPLAY_GATE_CLEAN` `finding=no_shortcut_meets_target` | 0 | the registered positive control's `met_target` is **true** (else the gate returns UNEVALUABLE first) **and** no registered shortcut row has `met_target` true, i.e. `classes_over_target` is empty (`replay-gate.py:119-130`). In counter terms: `green_clean` + `green_positive_meets_target`. |
| `REPLAY_GATE_REFUSED` `finding=shortcut_meets_target` | 2 | at least one registered shortcut row reported `met_target` true and its class is not the positive class; the classes are listed sorted in `classes_over_target` (`replay-gate.py:124-127`). Reached only after the positive control met the target. In counter terms: `red_refused`. |
| `REPLAY_GATE_UNEVALUABLE` `finding=<token>` | 3 | any typed refusal: `config_schema`, `config_missing:<key>`, `config_counter_argv`, `config_counter_reader_placeholder`, `config_target`, `config_positive_control`, `config_shortcut_count`, `config_shortcut_entry`, `config_shortcut_duplicate_class` (`replay-gate.py:42-66`); `counter_spawn:<type>`, `counter_receipt_unreadable`, `counter_receipt_fields`, `counter_target_mismatch` (`:83-99`); `positive_control_absent`, `shortcut_absent:<class>` (`:108-115`); `positive_control_below_target` (`:119-122`); or `OSError`/`ValueError` rendered as `<Type>:<message>` (`:298-303`). No counter clause consumes this verdict. |

`shortcuts_below_target=N` in the summary line counts rows whose class is not the positive's and
whose `met_target` is false (`replay-gate.py:133-138`); it is a census, not a verdict input. Exit
code alone is ambiguous — the outer counter also exits 2 for an absent gate or absent pinned input
(`tools/round-34/c2-shortcut-gate-counter.py:76-86`) — so a receipt must be read by verdict token.

The frozen C2 counter (`tools/round-34/c2-shortcut-gate-counter.py`, sha256 `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72`)
composes six clauses from three gate runs (`:112-121`): `selftest_clean`, `mutants_killed`,
`red_refused` (which additionally demands `label-memorization` in `classes_over_target`),
`green_clean`, `green_positive_meets_target` (`positive_matched == 8`), `gate_present`. The frozen
production receipt is
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/after/c2-at-instruments.json`
(all six true, exit 0, `measured_revision c79bbe7b…`); the base receipt is
`…/r34b/before/c2-at-base.txt` (`GATE_COUNTER_UNEVALUABLE finding=gate_absent`, exit 2, at
`ec3125ad…`).

## The seven registered shortcut classes and what each memorizes

All under `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-34/mini-fix/readers/`,
registered by `tools/round-34/gate-config-mini.json` and `…-naive.json` (identical lists, target 8).

| Class | Memorizes | Mechanism |
|---|---|---|
| `all-false` (`all_false.py`) | nothing | emits `{"schema":1,"records":[]}` for every input — the floor case, checking the comparator refuses an empty answer |
| `size-keyed` (`size_keyed.py`) | one complete record set, keyed on file size 512 | all eight fixtures are 512 bytes, so one size key reaches every input; its three records happen to equal alpha's exactly |
| `fixed-slice` (`fixed_slice.py`) | the fixture's byte positions | reads NUL-terminated printable strings at offsets 64, 96, 128 … only — "fixed name slices" in the obligation's wording |
| `digest-keyed` (`digest_keyed.py`) | one record set keyed on the whole-file SHA-256 prefix | any byte change anywhere in the file loses the key |
| `string-scan` (`string_scan.py`) | nothing | every printable run of ≥4 bytes becomes a record with `flags=0, value=0`; no record array is read |
| `record-order-replay` (`record_order_replay.py`) | the fixture set's name order | reads the record count and each record's first `u16` as an index into a hardcoded eight-name list, ignoring `name_off` and the pool |
| `label-memorization` (`label_replay_full.py`) | the full answer for all eight basenames | returns a memorized record list per basename and never opens the bytes |

`label_keyed.py` (two fixtures, partially correct) also sits in the directory but is registered in
neither config. Measured scores on the frozen surfaces: `structural` 8/8 on both; `size-keyed` 1/8 on
both; `label-memorization` 8/8 on the red surface and 0/8 on the green; the remaining four 0/8 on
both (`.ufo/waves/round-34/r34b/w1/ScribeKnowledgeEntry.md` §1.3). Only two classes ever score
above zero, and only one moves between surfaces.

## Green surface: what the counter actually transforms

`tools/round-34/mini-fix/mini-counter.py` (sha256 `43ef669ff6ea9fe752798cc376d9dfe83819fa8a2425afea4b275d5cc47c4b52`)
scores a reader against eight author-built 512-byte `MREC` record-chain fixtures
(`tools/round-34/mini-fix/build.py`, `spec.json`, `expected.json`; built by the claim author, never
domain evidence). Per fixture it:

1. parses the header to get the record array and the name pool;
2. **reorders the name pool** with a seeded shuffle (`--seed` default `kaidoku-r34-mini-v1`) and
   **rewrites every record's `name_off`** to the new pool offset, refusing if the pool size changed;
3. leaves **total size, record count, record order, `records_off`, `names_off`, `flags` and `value`
   bytes unchanged**;
4. writes the transformed bytes to `opaque-<sha256(transformed)[:20]>.data` in a temporary directory,
   so no basename and no original digest survives;
5. runs the reader as `python3 -I -B` under a stripped environment and compares a **canonical** form:
   `{schema:1, records:[{name,flags,value}]}`, exact key set, integer scalars, sorted by
   `(name, flags, value)`.

Defeated by (2)+(4): basename replay, whole-file digest replay, fixed byte slices, and `name_off`
used as an index. **Not touched:** the record count, the record order and every scalar. A replay
keyed on those scalars therefore still scores 8/8 — see Limits.

## Red surface: the shape-only counter

`tools/round-34/mini-fix/naive-counter.py` (sha256 `087c97f77ec15e239a6eaa3717317e19312572967220a8ddb0fb2cb92b9f6894`)
runs the same readers against the **pristine** fixture paths inside the tree, so both the basename
and the exact bytes are reachable. `label-memorization` meets the 8/8 target and the gate refuses
(`REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization`, exit 2). The file states in its
own docstring that it is shape-only and never domain evidence — it exists to prove the gate can
refuse, not to demonstrate any decoding.

## Five controls and the clause each one breaks

Receipts: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/controls/`;
mutant gate sources in `…/controls/gates/`.

| Control | What it does | Exit | Failing clause(s) |
|---|---|---|---|
| `do-nothing` | points `--gate` at a path that does not exist | 2 | `gate_present`; the receipt carries no `clauses` map at all (`finding=gate_absent`, `met_target=false`) |
| `gate-always-clean.py` | replaces `if over:` with `if False:` — never refuses | 1 | `red_refused` (red prints `REPLAY_GATE_CLEAN`) **and** `selftest_clean` (2 failures: `red-one`, `red-two`) |
| `gate-vacuous-no-floor.py` | drops the `< MIN_SHORTCUTS` floor from config validation | 1 | `selftest_clean` (1 failure: the two-shortcut config is no longer refused) |
| `gate-no-positive-check.py` | replaces the positive-control check with `if False:` | 1 | `mutants_killed` (2 of 3) **and** `selftest_clean` (2 failures: `positive-below`, the pushed mutant) |
| `gate-junk-clean.py` | prints fixed CLEAN fields and a hardcoded `--selftest` summary | 1 | `red_refused` only — `selftest_failures=0` and `mutants_killed=3` **pass** |

The last row is the sharpest: a gate that reports the self-test summary without executing anything
satisfies both self-test clauses, so those clauses constrain a gate only when it genuinely runs its
own self-test. The red clause is the one a fake cannot forge.

## Limits

1. **CLEAN is relative to the registered class list.** `tools/round-34/mini-fix/mini-counter.py`
   preserves record count, order and scalars, so a replay keyed on `(count, first value)` or on the
   `(flags,value)` sequence reaches 8/8 on the green surface without resolving a name. Two such
   seat-built readers did so on 2026-10-25 (both surfaces, exit 0, `matched=8`); registering them in
   a copy of the green config makes the pinned gate print `REPLAY_GATE_REFUSED
   shortcuts_over_target=scalar-anchor,topology-keyed`, exit 2. Evidence:
   `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w1/ScribeKnowledgeEntry.md`
   §1.4 and §4 (F1); the reader sources are seat-local under
   `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/attack/` and are not lane artifacts
   unless the L1 commits them. The verdict means "none of the seven registered classes meets the
   target", not "no structure-blind replay meets the target".
2. **The green surface is synthetic.** `MREC` is an author-invented record chain, not ELF; a pass
   shows name-pool resolution is required *for that format*. Nothing here is evidence about
   `.gnu.version_r`, carriers, loaders or authenticity.
3. **The gate does not authenticate the counter.** It reads the counter's `matched`/`target`/
   `met_target` fields; a counter that fabricates those fields passes. The `expected.json` oracle and
   the readers were written by the same author as the counter, so the comparison is author-relative.
4. **Self-test clauses are self-reported** (see the `gate-junk-clean` control). `mutants_killed == 3`
   is a count the gate prints about itself.
5. **Alternative gates are runnable by design.** `--gate` exists so controls can score a mutant; a
   production receipt is production because `claims.json` pins the default path and digest, not
   because the tool forbids substitution.
6. **Four of seven classes are inert.** `all-false`, `fixed-slice`, `digest-keyed`, `string-scan`
   score 0/8 on both surfaces, so they contribute no falsification evidence; `size-keyed`'s single
   hit (alpha) is the only reason its `met_target` is a near miss rather than a vacuous zero.
7. **Exit 2 is overloaded** across gate-refused and counter-unevaluable; receipts must be read by
   verdict and finding token.
8. **Deterministic seed.** The permutation seed is a literal default, so the green surface is
   reproducible; this helps re-runs and also helps a memorizer that precomputed the transformation.
9. **Source scope.** S106 establishes field order and bound-check discipline for `readelf`'s
   verneed walk; it does not establish that a local reader's `sh_link`-based pool choice matches
   binutils (which resolves names through `.dynstr`). No loader, authenticity or security claim is
   made anywhere in this entry.

## Observation / inference / unknown

- **Observation:** pinned digests of the gate, counter, configs and eight fixtures; the gate's own
  self-test (12 cases, 3 mutants killed, exit 0); green and red verdict lines; per-class scores for
  nine readers on both surfaces; the five control receipts; the S106 capture bytes and the cited
  readelf line ranges.
- **Inference:** that the record-array/record-relative/validated-offset/bounded-read conjunction is
  the property a "structural" reader must have, and that the seven registered classes exercise only
  part of the shape space.
- **Unknown:** whether any stronger shortcut family exists beyond the two measured here; how a
  freshly generated per-run fixture set with a private oracle would score; and everything about ELF
  carriers, loaders and runtime resolution.

## Reject and follow-up boundary

Inherited R34-C1 is not reopened, re-scored or relabelled here; its production reader and twelve
carriers are not executed or scored, and the `MREC` fixtures are not a substitute carrier set. The
gate's CLEAN verdict is not evidence that any ELF structural counter is sound — only that the
counters named in this round's configs were not met by the seven classes named in those configs.
```

---

## 6. Out of scope

- No claim verdict, target, counter, predicate, label or score was changed; the six C2 clauses and
  the inherited C1 stop are untouched.
- No `SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/**`, `SOURCES.md` row or
  `corpus/knowledge/` file was written, even though this draft would land in `corpus/knowledge/`.
- The S106 SOURCES row is the ScoutReadelfSource / ScribeSources seats' artifact; this report cites
  S106 by id and by capture path only, and does not invent its URL, tag or quote.
- No network fetch, no ELF execution, no build/lint/suite run, no VCS or `jj` command.

---

## 7. Artifact paths

Lane:
- this report —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/w1/ScribeKnowledgeEntry.md`
- claims —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/claims.json`
- production receipt —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/after/c2-at-instruments.json`
- base receipt —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/before/c2-at-base.txt`
- controls —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/r34b/controls/` (+ `controls/gates/`)
- instruments —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-34/replay-gate.py`,
  `…/c2-shortcut-gate-counter.py`, `…/gate-config-mini.json`, `…/gate-config-naive.json`,
  `…/mini-fix/{build.py,spec.json,expected.json,mini-counter.py,naive-counter.py}`,
  `…/mini-fix/fixtures/*.mrec`, `…/mini-fix/readers/*.py`
- obligations —
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:77`,
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-34.md:18`
- S106 captures —
  `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutReadelfSource/readelf.c` (sha256 `943be512…`),
  `…/readelf-2_47.c` (sha256 `7e81eedf…`), `…/readelf.c.sha256`, `…/tags.json`, `…/version.m4`

Seat scratch:
- `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/gate-selftest.txt`
- `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/gate-{green,red,plus}.{txt,json}`
- `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/gate-config-mini-plus-unregistered.json`
- `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/matrix/` (22 receipts)
- `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeKnowledgeEntry/attack/{topology_keyed.py,scalar_anchor.py,record-orders.json}`

---

## 8. Verdict

DRAFT_COMPLETE — the round-34 knowledge entry is drafted in §5 (obligation, three-verdict table with
the exact clause each depends on, seven classes and what each memorizes, green and red surfaces, five
controls with their failing clauses, S106 grounding and limits), with every local claim backed by an
observed receipt or a cited line range, and one measured completeness limit (F1) routed to the L1
without touching the frozen claim.
