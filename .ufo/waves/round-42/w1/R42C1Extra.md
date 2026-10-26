# R42C1Extra — round-42 port of `tools/round-41/c1-extra.py`

**DONE** — `c1-extra.py` is ported, 41/41 offline self-tests pass, it scores a green landing and
five red variants on real lane documents in a sandbox clone, it integrates end to end with the
real `tools/round-42/sqfs3-oracle.py` on v3 fixtures, and it is the unmoved measurement (exit 2)
at both the base and wave-1 HEAD. One finding needs the freeze: a SquashFS **v3 LZMA** image
cannot get the two-producer oracle (unsquashfs 4.7.5 refuses it).

Artifacts: `.ufo/waves/round-42/w1/artifacts/R42C1Extra/` (`README.md` has rebuild commands).
Tool digest: `c1-extra.py` = `63d7cf91ce749e12ee8ae38ed36cdbd274c092f4d215b3f8d24f77a672975158`.

## 1. What the port changes (round-41 → round-42)

| # | round-41 (`c4a38ea2:tools/round-41/c1-extra.py`) | round-42 |
|---|---|---|
| 1 | `CARRIERS = '.ufo/waves/round-41/c1/carriers.json'` | `.ufo/waves/round-42/c1/carriers.json` |
| 2 | reader `tools/round-41/sqfs-list.py`, `--layout avm` | oracle `tools/round-42/sqfs3-oracle.py` (two producers, `unsquashfs` 4.7.5 + 7-Zip), no layout flag |
| 3 | `ENTRY`/`STEM` `2026-10-26-r41-avm-be-squashfs-core` | `2026-10-26-r42-squashfs-v3-core` |
| 4 | heading `## Round-41 additions to Core`, note `Round-41 frontier note` | `## Round-42 additions to Core`, `Round-42 frontier note` |
| 5 | carrier bytes: lane `path` at REV, else `<pin>.bin` in `--carrier-cache` | **pin-scan of the cache**: `<pin>.bin`, `<pin>.sqfs`, `<id>.bin`, `<id>.sqfs`, `<pin>`, then every regular file in the cache root; a lane `path` is RED (round-42 carriers are published images, never committed) |
| 6 | oracle CLI fixed | **CLI discovered once** on the first carrier from `IMG --out DIR`, `IMG DIR`, `--input IMG --out DIR`, `--image IMG --out DIR`; the accepted form and every attempt (form, exit, stderr head) land in the receipt |
| 7 | table compare = sorted raw text lines | parsed row sets with format validation: oracle `(rel, sha256, size)` (3 fields, 64-lowercase-hex, integer size), nonregular `(rel, kind, detail)` (2 or 3 fields, empty third ≡ absent); duplicate rows red; empty oracle table red; a **dropped non-empty detail is red**, an **empty-detail two-field row is green** |
| 8 | oracle path accepted anywhere | path must sit under `corpus/evidence/round-42/c1/` (the CTL-C1-1 relabelling shape is red) |
| 9 | note required the round-40 `measured, not promoted` record phrase | note must name the `squashfs_v3` family **and** what stays Frontier — v1, v2 **and** v4+Broadcom — plus a residual verb |
| 10 | receipt had no tool identity (closure D4) | `counter_sha256`, `counter_path`, `counter_bytes`, `counter_at_rev_sha256`, `counter_matches_rev`, `counter_pin_ok`; `met` also requires `counter_pin_ok` (false only when the frozen path exists at REV with different bytes) |
| 11 | any reader non-zero exit → carrier not ok | unchanged (red, **never** unevaluable); only a missing `carriers.json` / oracle tool at the freeze is unevaluable (exit 2) |
| 12 | `--selftest --tools DIR` requiring lane tools | `--selftest` needs nothing external (in-fixture stub oracle); new `--oracle-check --oracle FILE --dev-image FILE` runs the real tool end to end |

Scratch: `$HYAKU_SCRATCH/kaidoku-r42` (TMPDIR/`--work` honoured; `/tmp` not referenced).

## 2. Bindings as implemented (the text the freeze can quote)

- `oracle_rederived` — for every carrier in `carriers.json` **read at FREEZE**: it has no lane
  `path`, it has an http(s) `external.url` (or top-level `url`), its `oracle`/`nonregular` paths
  start with `corpus/evidence/round-42/c1/`, its bytes are the cache file whose sha256 equals the
  frozen pin, and the **oracle tool bytes at FREEZE** re-derive both tables equal (as parsed row
  sets) to the tables **at REV**.
- `sourced_new` — the entry at REV has a line starting `source` that cites an S-id whose
  `corpus/SOURCES.md` row is absent at `--base` and present at REV with the entry path or stem in
  its used-by cell. `S129` is the highest row at `c4a38ea2`; citing it (or any lower id) is red.
- `frontier_content` — one PROVINCE.md line at REV starts `Round-42 frontier note` and carries:
  the heading `## Round-42 additions to Core`, the stem, a supersede verb, `squashfs_v3` (word
  bounded, `squashfs_v30` does not count), `v1`, `v2`, `v4` with `Broadcom`, and a residual verb
  (`stay*/remain*/not claimed/outside`).

`met` = the three bindings **and** `counter_pin_ok`. Exit 0 met / 1 not met / 2 unevaluable.

## 3. Evidence

### E1 — offline self-test: 41 cases, 41 pass

```
$ python3 artifacts/R42C1Extra/c1-extra.py --selftest --work "$S"
SELFTEST cases=41 pass=41 fail=0            # exit 0
```

(`selftest/selftest.txt`.) Round-41 cases kept where they still apply (`green`, `base-has-nothing`,
`trimmed-oracle`, `edited-oracle-same-count`, `extra-nonregular-row`, `external-carrier-pin-mismatch`,
`external-carrier-missing-cache`, `old-sid-with-used-by`, `new-sid-no-used-by`,
`presence-only-frontier-note`, `round-41-note-names-r42-heading`, `note-miscases-heading`,
`green-after-restore`, `bad-rev-unevaluable`); dropped only the AVM-layout case (no layout reader in
the round-42 chain). New, and each red case names the binding it must fail:

- **asked for**: `base-sid-s129-with-used-by` (an id present at base is not new coverage),
  `note-names-v4-only` (a note naming `squashfs_v4` only is not a note about the v3 family);
- `note-omits-v1v2-residual`, `note-omits-v4-broadcom-residual`, `note-without-supersede-verb`,
  `note-names-squashfs_v30`, `sid-adjacent-digits-are-not-a-row` (`S1120`);
- oracle mechanics: `oracle-positional-cli-discovered` (green with a positional-only CLI),
  `oracle-absent-at-freeze` (unevaluable), `oracle-cannot-read-carrier` (exit 2), 
  `oracle-extractor-failure-exit3` (red, not unevaluable), `table-from-the-other-carrier`,
  `oracle-row-wrong-field-count`, `duplicate-oracle-row`, `nonregular-detail-dropped-is-red`,
  `empty-detail-two-field-row-parse-equal`;
- carrier shape: `carrier-committed-in-lane`, `carrier-without-external-url`,
  `oracle-outside-round-42-evidence`, `cache-entry-named-by-hand` (pin-scan, not filename);
- identity (D4): `counter_sha256-is-self-hash`, `counter_matches_rev-null-before-integration`,
  `counter-installed-at-rev-matches`, `counter_matches_rev-true-when-installed`,
  `counter-drift-at-rev-is-not-met`.

### E2 — the unmoved measurement (control)

```
$ c1-extra.py --root LANE --rev c4a38ea2 --freeze c4a38ea2 --base c4a38ea2     # exit 2
"unevaluable": "absent at freeze: .ufo/waves/round-42/c1/carriers.json, tools/round-42/sqfs3-oracle.py"
$ c1-extra.py --root LANE --rev fdabdfa4 --freeze fdabdfa4 --base c4a38ea2     # exit 2, same line
```

(`before-c4a38ea2….json`, `before-fdabdfa4….json`; both carry `counter_sha256 63d7cf91…`.)

### E3 — dry run on real lane documents (sandbox clone, 13/13)

`dryrun.py` clones the lane at HEAD into scratch (`rev-parse --show-toplevel` asserted), gives it a
synthetic landing (one external carrier with 1.4 KiB of synthetic bytes + a **stand-in** oracle,
the entry, a new `S130` row, the round-42 note) and scores eleven revisions plus two identity rows:
**13/13 `ok`, clone commits `ac860728` (freeze) / `c33bed00` (landing)**.

| tag | met | binding that fired |
|---|---|---|
| `green` | **true** | — (`sourced_new`: cited `S112`,`S130`; `at_base` `S112`; new-with-used-by `S130`) |
| `note-omits-v1v2` | false | `frontier_content` |
| `note-names-v4-only` | false | `frontier_content` |
| `green-after-note-restore` | true | — |
| `oracle-row-edited` (one sha256 flipped, row count kept) | false | `oracle_rederived` |
| `green-after-table-restore` | true | — |
| `oracle-path-relabelled` → `corpus/evidence/round-41/c1/D1/oracle.tsv` | false | `oracle_rederived` — *"oracle path … is outside corpus/evidence/round-42/c1/ (round-41 relabelling shape)"* |
| `entry-cites-S129` | false | `sourced_new` |
| `counter-installed-at-rev` | true | `counter_sha256 == counter_at_rev_sha256 == 63d7cf91…` |
| `counter-drifted-at-rev` | **false** | all three bindings true, `counter_pin_ok false`, `counter_matches_rev false` |
| `green-final` | true | — |

The green note sentence that scores `frontier_content` true on the real `PROVINCE.md` (proposed
wording for `R42C1EntryDraft`/L1; it names the family and both residual groups; the gate
reads it as **one physical line**, shown wrapped here):

```text
Round-42 frontier note, 2026-10-26: SquashFS v1-v3 chunks now extract through the `squashfs_v3`
handler family (`squashfs_v3`, `_ddwrt`, `_broadcom`, `_nonstandard`, `_adaptive`); the Frontier
text for v1-v3 is superseded for the handler family measured here, while v1/v2 images and v4
Broadcom bodies stay Frontier — see ## Round-42 additions to Core
(`2026-10-26-r42-squashfs-v3-core`).
```

### E4 — integration with the real oracle (`--oracle-check`)

The sibling tool landed mid-seat: `.ufo/waves/round-42/w1/artifacts/R42C1Oracle/sqfs3-oracle.py`
sha256 `f7beb56ee8b53ace15e86537f2df97a8597f6716154f20a8db0d89795e859390`. Its CLI is
`IMAGE --out DIR` (plus `--files/--nonregular/--json`), which my **first** discovered form hits
(`oracle_form: "img--out"`).

| fixture (MIT, unblob 26.6.4, 4 KiB) | sha256 | rows oracle/nonreg | oracle cross-check | `--oracle-check` |
|---|---|---|---|---|
| `squashfs_v3/little_endian/…/squashfs_v3_le.bin` | `0161351c…cd1f7` | 2 / 0 | agree | **ok** (green met, flipped row → `oracle_rederived` false, other two true) |
| `squashfs_v3/little_endian/…/squashfs_v3.le.4kpad.bin` | `5afb4387…6dda` | 4 / 0 | agree | ok |
| `squashfs_v3_broadcom/little_endian/…/squashfs_v3_le.bin` (`shsq`) | `6baad438…37d3` | 2 / 0 | agree, magic normalized | ok |
| `squashfs_v3_nonstandard/little_endian/…/squashfs_v3_le.bin` (`zlqs`) | `3bce6ae3…1acb` | 2 / 0 | agree, magic normalized | ok |
| `squashfs_v3_adaptive/__input__/squashfs_v3_le.lzma.bin` (`hsqs`, **LZMA**) | `2ac15e5c…3124` | — | **`producer_incomplete:unsquashfs`** | **FAILED** (no tables in any form) |

The refusal is the oracle's own, and correct: `unsquashfs` 4.7.5 exits 1 on that image
(`gzip uncompress failed with error code -3` / `FATAL ERROR: read_inode`), `7z` 26.04 lists its two
files, so the two-producer rule has no oracle there and my gate reports the carrier not met rather
than unevaluable. Recorded in `oracle-check/lzma-refusal-oracle-run.json`.

Note: the DD-WRT LE fixture is byte-identical to the standard v3 LE fixture (`0161351c…`, magic
`hsqs`), so it is not an independent data point; broadcom/nonstandard are the vendor-magic ones.

## 4. Freeze-relevant findings for the L1 and sibling seats

1. **The oracle CLI is settled**: `sqfs3-oracle.py IMAGE --out DIR` writes `oracle.tsv`,
   `nonregular.tsv`, `oracle-run.json`; my gate also accepts the positional form, so neither seat
   has to move. Exit 2 = unreadable/one producer incomplete, 3 = producers disagree; both become a
   red carrier, never unevaluable.
2. **v3 LZMA cannot be a C1 carrier.** `squashfs_v3_adaptive` LZMA images have no two-producer
   oracle (unsquashfs 4.7.5 fails, E4). If a candidate image is LZMA, either the draft's oracle
   clause must name a different second/third producer or the carrier must be dropped. [The four
   proposed carriers — DD-WRT `tqsh`, OpenWrt `squashfs-3.0`, vendor rootfs — are gzip or LZMA and
   must be probed before the freeze.]
3. **`carriers.json` keys my gate reads**: `carriers[].{id, sha256 (carve pin), external.url
   (or top-level url), oracle, nonregular}`; it ignores everything else (`external` container chain,
   `prior_pins`, `projection`). A lane `path` on a carrier is red by construction; cache file naming
   is irrelevant because bytes are resolved by pin (`cache-entry-named-by-hand` proves it).
4. **Frontier note token contract** (§2): the family token is `squashfs_v3` word-bounded, so
   `squashfs_v30` or a bare `v3` does not satisfy it; the residual clause must carry `v1`, `v2`,
   `v4`+`Broadcom` and a stay/remain verb in the same line. The sample in E3 passes as written.
5. **SOURCES**: base highest is `S129`; the entry's `source:` lines must cite at least one row > base
   whose used-by names the entry path **or** stem (`new-sid-used-by-stem` proves the stem route).
6. **D4 identity is enforced, not decorative**: a receipt whose bytes differ from `tools/round-42/
   c1-extra.py` at REV is not `met` (`counter-drift-at-rev`), and before integration the clause is
   vacuous (`counter_matches_rev null`). Install the artifact byte-for-byte.

## 5. Limits and inference

- The dry run's `oracle_rederived` green uses a **stand-in** oracle (the real one did not exist when
  the dry run was built); it proves the wiring, the carriers/evidence-path rules and the document
  bindings against **real lane bytes**, not the v3 oracle chain. The real chain is proven separately
  in E4 on five fixtures (all 4 KiB; no real distribution rootfs was available to this seat, and
  carriers are reserved to the `R42C1Img*` seats).
- [INFERENCE] A real 2–30 MB carrier's oracle run will be slower (two extractions per carrier) but
  the binding is per-carrier identical; the gate has no timeout and inherits the caller's.
- [INFERENCE] `nonregular.tsv` from the real oracle carries `dir` rows (v3 fixtures here have none),
  so the frozen tables will be larger than these fixtures'; comparison is row-set based either way.
- Not measured here: the counter's own clauses (superblock, carve, gaps, rerun projection,
  `compressed` compression coverage, `squashfs_v3_ddwrt`-style handler binding) — those belong to
  `tools/round-42/c1-counter.py` (`R42C1Counter`). This gate does not re-check freeze drift; the
  counter owns the frozen-path list.
- No tool was installed, upgraded or removed by this seat; no pacman/uv/npx transaction ran.

## 6. Risks / blockers

- **R1 (freeze)**: if the L1 installs a reformatted `c1-extra.py` (even a trailing newline), the
  score goes red on `counter_pin_ok`. Copy the artifact byte-for-byte
  (`63d7cf91ce749e12ee8ae38ed36cdbd274c092f4d215b3f8d24f77a672975158`).
- **R2 (carrier)**: any LZMA v3 carrier fails E4's rule; probe compression before the freeze.
- **R3 (note)**: the scribe's final note must keep the four residual tokens in one line; the draft's
  "Not claimed: v1/v2 images, v4 Broadcom" sentence is exactly the shape to reuse.
- **R4 (blocked item, none)**: no blocker stopped this seat; the only thing not run is a full real
  carrier score, which requires the freeze.

## 7. Files written

| path | sha256 / note |
|---|---|
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/c1-extra.py` | `63d7cf91ce749e12ee8ae38ed36cdbd274c092f4d215b3f8d24f77a672975158` |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/dryrun.py` | `b443b44d44af3d89715c7725ddbdb79a60c6500e01f089131e99a7f157e61ee7` |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/README.md` | rebuild commands |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/selftest/selftest.txt` | 41/41 |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/dryrun/` | 13 receipts + `dryrun-summary.json` |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/oracle-check/` | 5 `--oracle-check` JSONs + summary + the LZMA refusal record |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/fixtures/` | 5 MIT fixtures (4 KiB each) + `fixtures.json` |
| `.ufo/waves/round-42/w1/artifacts/R42C1Extra/before-*.json` | exit-2 receipts at base and HEAD |
| `.ufo/waves/round-42/w1/R42C1Extra.md` | this report |

Scratch (`/fast/scratch/hyaku/kaidoku-r42/R42C1Extra`, including the sandbox clone) is removed.
No file outside the two paths above (and my scratch) was written; no VCS state was mutated.
