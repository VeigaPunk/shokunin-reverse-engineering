# MutR25Coverage — the round-25 coverage false accept, and what the frozen R26-C1 `entry_ok` rule catches

Seat `KaidokuR26.MutR25Coverage` (mutation-tester, leaf). Lane base `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`. Work 2026-10-22T12:16:05Z–12:41Z. Lane read-only throughout; no lane file, git index or `jj` state touched except this report.

## Target and question

Routed defect 3 (`corpus/lessons/round-25-verifier-spotcheck.md`, "Routed defects", item 3) says the round-25 C2 instrument has a disclosed false accept — "C2 reads the `opened` cell only" — and must not be reused as a frozen counter until that path is fixed with a red-before fixture. The frozen R26-C1 `entry_ok` rule (`.ufo/waves/round-26/claims.json`, `claims[0].rules.entry_ok`) reads: "1 if `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md` exists, its `source:` line names `corpus/evidence/round-26/c1/table.tsv` and at least one `S###` whose `SOURCES.md` row has `opened` 2026-10-22 and whose id appears in the `## Gate` section of `corpus/lessons/round-26.md`; else 0." Question: does the R26 rule close the round-25 false accept, and what does it still let through?

## Method

Sandbox clone `<seat>/clone`; 19 mutants, one defect per commit, two branches (`mut/r25`, `mut/r26`) rooted at the lane base, all 19 trees distinct (19 distinct patch sha256). Detector 1 is the frozen round-25 instrument with unmodified lane bytes: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-25/a2/c2-coverage.py --root <clone> --rev <rev>` (lane sha256 `7a7e6d6529033c5dfac6da252507ac597b30f0a3d4740522d17f87f4ee6b2c70`, identical before and after every run). Detector 2 is a seat probe, `<seat>/tools/entry_ok_probe.py`, implementing the frozen text above; it is **not** the lane counter (`tools/round-26/c1-id-identity.py`, owned by seat `KaidokuR26.CounterC1`) and exists so the frozen text can be scored before that counter lands. The same bounded detector ran on pristine, mutated and restored bytes: the clone working-tree digest was hashed before and after every run and the instrument sha256 re-checked; across all 19 runs the digest was unchanged, the instrument bytes were unchanged, `git status --porcelain` in the clone was empty and the clone HEAD was back at the base rev.

## Mutant table — family N: the frozen R26-C1 `entry_ok` rule

`prim` = primary reading (S ids from the first `source:` line; Gate = the `## Gate` section, heading to the next `## ` heading). `alt_ids` = any `source:` line. `alt_file` = Gate read as the whole lesson file. `alt_entry` = S ids from anywhere in the entry. All runs 2026-10-22T12:40:30Z, probe exit 0 throughout.

| id | mutation | prim | alt_ids | alt_file | alt_entry | verdict |
|---|---|---|---|---|---|---|
| N0 | well-formed: entry names the table, S090 mined + opened 2026-10-22, Gate row with URL and quote | 1 | 1 | 1 | 1 | baseline (green) |
| N-M1 | S090 row opened 2026-10-22, no lesson Gate section names S090 | 0 | 0 | 0 | 0 | **caught** |
| N-M2 | Gate names S090 but the Gate row carries no URL and no quote | 1 | 1 | 1 | 1 | **survived** |
| N-M3 | entry `source:` line names S090 but not `corpus/evidence/round-26/c1/table.tsv` | 0 | 0 | 0 | 0 | **caught** |
| N-M4 | S092 row `status` = `rejected`, opened 2026-10-22, Gate names it | 1 | 1 | 1 | 1 | **survived** |
| N-M5 | S090 named in the lesson only outside the `## Gate` section | 0 | 0 | 1 | 0 | caught (primary) |
| N-M6 | entry names a table path that is not the frozen table path | 0 | 0 | 0 | 0 | **caught** |
| N-M7 | `source:` line names the frozen table path, but the table file is absent from the tree | 1 | 1 | 1 | 1 | **survived** |
| N-M8 | the Gate-qualifying id sits only on the second `source:` line | 0 | 1 | 0 | 1 | caught (primary) |
| N-M9 | the qualifying SOURCES row `used-by` does not name the entry | 1 | 1 | 1 | 1 | **survived** |
| N-M10 | S090 source URL was never fetched, but its `opened` cell says 2026-10-22 | 1 | 1 | 1 | 1 | **survived** |
| N-M11 | S093 `opened` cell forged to 2026-10-22 while its own `anchor` cell says fetched 2026-10-19 | 1 | 1 | 1 | 1 | **survived** |
| N-M12 | the Gate-qualifying id appears only in the entry body, not on its `source:` line | 0 | 0 | 0 | 1 | caught (primary) |

The three mutants named in the assignment are **N-M1** (a SOURCES row with `opened` 2026-10-22 that no lesson Gate mentions), **N-M2** (a Gate that names the id without URL or quote) and **N-M3** (an entry whose `source:` line names the row but not the table).

## Mutant table — family R: the frozen round-25 instrument

The r25 entry `source:` line is rewritten to cite a single synthetic `S099` row so the instrument's verdict rests on that row alone. Runs 2026-10-22T12:40:30Z. `entry_sourced` 1 = the instrument accepts.

| id | mutation | exit | entry_sourced | qualifying_rows | verdict |
|---|---|---|---|---|---|
| R0 | pristine lane base | 0 | 1 | S075, S076, S077, S078 | baseline (green) |
| R-M1 | S099 opened 2026-10-22, absent from every lesson Gate section | 0 | 1 | S099 | **survived (false accept)** |
| R-M2 | as R-M1 plus a Gate row naming S099 with no URL and no quote | 0 | 1 | S099 | **survived (false accept)** |
| R-M3 | as R-M1 but the entry `source:` line names the row and no table | 0 | 1 | S099 | **survived (false accept)** |
| R-M4 | S099 status cell is `opened`, not `mined` | 1 | 0 | — | killed |
| R-M5 | S099 `used-by` names a lookalike path that does not exist | 0 | 1 | S099 | **survived (false accept)** |

The round-25 instrument never reads `corpus/lessons/round-25.md` at all, so a Gate that names the row with no URL and no quote (R-M2) changes nothing for it — it has no Gate check to fail.

## Answer: which mutants the frozen R26-C1 `entry_ok` rule catches

**Catches two of the three assigned mutants: N-M1** (row not named by any Gate, so `entry_ok` 0) **and N-M3** (`source:` line does not name the table, so `entry_ok` 0). Also N-M5, N-M6, N-M8 and N-M12 under the primary reading. **Misses one: N-M2** — the rule asks only that the id "appears in the `## Gate` section", and a Gate row naming S090 with no URL and no quote satisfies that literally, so `entry_ok` is 1. The round-25 false accept is therefore only partly closed: the R26 rule adds a Gate-membership requirement the round-25 instrument lacked, but does not require the Gate row to carry a URL or a quote, and does not require the SOURCES row to be `mined`. Three points of the frozen text are ambiguous and the mutants separate the readings: N-M5 — "appears in the `## Gate` section" reads section-scoped (prim 0) or whole-file (alt_file 1); N-M8 — "its `source:` line" reads first `source:` line only (prim 0) or any `source:` line (alt_ids 1); N-M12 — "at least one S###" reads from the `source:` line (prim 0) or anywhere in the entry (alt_entry 1).

## Residual false accepts of `entry_ok` (survivors under every reading)

1. **N-M2 — a Gate row with no URL and no quote.** The rule counts the id as Gate-named on the strength of the bare id; a Gate saying only "S090" supports nothing about the source being opened.
2. **N-M4 — a row whose `status` is `rejected` still qualifies.** The rule checks `opened` and Gate membership only. The round-25 instrument did check `status == "mined"`, so this check was dropped, not carried forward.
3. **N-M7 — the table file need not exist.** The rule asks that the `source:` line *names* the table path, not that the file is in the tree.
4. **N-M9 — the SOURCES row need not be used by the entry.** The rule never reads `used-by`.
5. **N-M10 and N-M11 — the `opened` cell is self-reported.** This is the round-25 defect carried forward verbatim: the rule reads the `opened` cell and nothing else about the source, so a never-fetched URL (N-M10) or a forged `opened` date contradicted by the row's own `anchor` cell (N-M11) both yield `entry_ok` 1.

Supplementary observation, not a mutation result: the round-26 landing present in the lane working tree at 12:35:02Z (uncommitted entry, lesson, S079 and S080 rows, `corpus/evidence/round-26/c1/`) scores 1 under all four readings, so the residuals above are latent rather than currently false.

## Fixtures delivered to seat KaidokuR26.CounterC1

Path `/fast/scratch/hyaku/kaidoku-r26/seats/MutR25Coverage/fixtures/`. Verified: all 19 revs resolve against a lane clone plus the bundle, and the probe exits 0 on N0. Usage:

```sh
git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/c1-fixtures
git -C /tmp/c1-fixtures fetch /fast/scratch/hyaku/kaidoku-r26/seats/MutR25Coverage/fixtures/mutants.bundle \
    'refs/heads/mut/r25:refs/heads/mut/r25' 'refs/heads/mut/r26:refs/heads/mut/r26'
python3 -I -B tools/round-26/c1-id-identity.py --root /tmp/c1-fixtures --rev <rev from fixtures/revs.json>
```

| artifact | sha256 |
|---|---|
| `fixtures/mutants.bundle` (thin bundle, base is a prerequisite) | `73a9a8c14b91dd418c0ff53313f368b045999423b71ac2fcdf831f1f028320bf` |
| `fixtures/revs.json` (base plus every mutant rev) | `766ba2f654f8b12fe9bef0667317a0e35fa663306c4292fa8cd0db28a265b431` |
| `fixtures/README.md` | `6a135d7dd173961ab39ad71c44149583374534ea28b9281df4954ea7b0c393ea` |
| `fixtures/patches/*.patch` (19 files, all sha256 distinct) | per-mutant hashes in `out/final_table.json` |
| `tools/entry_ok_probe.py` (seat probe) | `68f45e58fd022051009a05242857dec606f907f2752d03532e3f95b13df5f42d` |
| `tools/build_fixtures.py` | `fc6ccaacd906ed93fb6e316ee602a5d0fec01bdc3ea4a287ee970011c9074a7e` |
| `tools/run_detectors.py` | `076bde72a0db8c4feeec9cf0da13203e99ee62622a09dbf6f90aa0e205724771` |
| `tools/package_fixtures.py` | `c4c6d366103cfc9908ad5026358dc84b6a279a5dc01652c67ebdecebf1daf8fa` |
| `out/final_table.json` (full table, file hashes, tree digests) | `f30671101d40afff68bdb69591a4bf7ab8d277c005902d22db940676f0a2426b` |
| `out/detector_runs.json` (raw detector stdout and exit codes) | `08e977bff738b213276b4ca43f19add9a7c03e9565b263126c54a50d79f65671` |
| `out/bundle_verify.json` | `3ecd583bcfa7176b2d5d1728bf94f3b9b8cccef9c779bb8ae0e06b4522f82c07` |

Revs, all in `fixtures/revs.json`: N0 `95e34241f9bc52ba438c12fd432fc47073b5e717`; N-M1 `aafb8a37f01b5ee799d163e931eb7a2c41f730e9`; N-M2 `8a1a1bfe545de3e5ae6708130e239e1d55289b23`; N-M3 `6780840dea72d8d59ac1f4c73ca3e86ecb722313`; N-M4 `37e129a5f972c928fbb8503dc5bdd58e21b83ef2`; N-M5 `e40cfdbc3f3fa6f7d27a4cdac30311bed71f6ee5`; N-M6 `e777c3b84c4b35b6f7c2d24c2462f87aeaa2b23e`; N-M7 `a819b1c8a1fc47bc2993a74223f6d0a72d867d3e`; N-M8 `7e89ebbaed30939e0d19be35d77dc1e84b535be8`; N-M9 `7887bc6936700a36c093e0fb6a6a26fd50fc37c9`; N-M10 `5a5fda0df10f24fd39409eb909e76ac15676ec51`; N-M11 `0cb7be400acdefded86d893f5a375811f725bd4d`; N-M12 `0558e917ee0d802834e5848b7a2e75b34b7cfb59`; R0 `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`; R-M1 `e4ea54834bfcaf47816bea9746878024ab20cc68`; R-M2 `dbc38bbe8860c26a20a51c3bc810e8215e128dbd`; R-M3 `acdc20d1d22879a8937e794b8ed5ebf29d1740a5`; R-M4 `eed8015baf0d6e9d6aee98cb7fff23c5ed30402f`; R-M5 `f77e10c4ef6d1c59a781bad8fdd5cb42a3599bea`.

## Sources opened this round

`https://registry.npmjs.org/rea-agents/6.5.0` — plain HTTP fetch, 2026-10-22, bytes sha256 `52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde`, saved at `out/rea-agents-6.5.0.json`. Located quote (`dist.integrity`): "sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRvYPnV5Yodr+1RqewCQla68WulXlVnveD+A==". Used only to confirm the 6.5.0 registry record exists; it carries no claim in this report.

## Bounds and side effects

No lane file was written except this report; no git write, no `jj` command, no lane index change. The lane working tree shows `M corpus/README.md`, `M corpus/SOURCES.md` and untracked `corpus/evidence/round-26/c1/`, `corpus/lessons/round-26.md` and `corpus/knowledge/2026-10-22-r26-…md` — those are other seats' edits, present before and after my run. All mutation happened in `<seat>/clone`, which was reset to the base rev after every mutant, with a byte-identical tree digest before and after each detector run. REA was not invoked: this target needs no REA call. Tools installed or updated: none. Synthetic S-ids S090 to S093 (family N) and S099 (family R) exist only in the sandbox clone and the fixture bundle and must never enter the lane.

## Verdict

The frozen R26-C1 `entry_ok` rule catches two of the three assigned mutants (N-M1, N-M3) and misses one (N-M2, a Gate row with no URL and no quote). Five residual false accepts remain, of which N-M10 and N-M11 are the round-25 defect itself carried forward: the rule reads the `opened` cell and nothing else about the source. The rule is stricter than the round-25 instrument, adding Gate membership and a table name, but it drops the `status == "mined"` check the round-25 instrument had and never checks that the Gate row carries a URL and a quote.
