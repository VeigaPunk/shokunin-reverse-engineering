# ScoutProvince — round 48 province membership

Seat: ScoutProvince. Read-only. Axes named: coverage (is this a domain surface the province or the coverage map must record), depth (does the registry rebind deepen a province surface, or only SKILL craft), calibration (does the freeze's "no PROVINCE move" sentence match the tree).

**Answer.** The round's two surfaces do not fall inside the lane's declared province. They are this lane's craft table and this lane's record counter. No line in `PROVINCE.md` must change. Adding a Core, Frontier, or Adjacent row for them would declare a domain surface the freeze disclaims.

Counters `tools/round-48/meanings.py` and `tools/round-48/record2.py` were not run. Disk-guard was not run: no heavy pass. No tool was installed.

## What the province is

`PROVINCE.md` declares one domain, and three lists under it.

> **Domain:** reverse engineering of shipped artifacts with REA on this Linux host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages; evidence-first static analysis that keeps observation, inference and unknowns separate. (`PROVINCE.md:3-6`)

> The domain is a frontier, not a fence: it grows by evidence (LEARNING.md). (`PROVINCE.md:36`)

> ## Core (`PROVINCE.md:38`)
> ## Frontier (`PROVINCE.md:73`)
> ## Adjacent (`PROVINCE.md:97`)
> Ground the lane refuses or defers — reported to the orchestrator, never absorbed. (`PROVINCE.md:97-100`)

The growth rule the domain line cites, fleet `LEARNING.md` (one file under `/home/vgpnk/Projects/shokunin`; no lane-local copy):

> 3. **Understanding** — distill what was admitted: connect entries, state the principle behind them, fold durable understanding into `SKILL.md` (`LEARNING.md:16-18`)
> 4. **Expanding perspective** — work the province frontier … The province grows by evidence, not by declaration. (`LEARNING.md:22-24`)
> `PROVINCE.md` holds **Core** (surfaces owned now), **Frontier** (areas being explored; expected to grow) and **Adjacent** (sibling-owned; report, don't absorb). Moving frontier ground into core is ordinary growth, recorded in `LOG.md`. (`LEARNING.md:75-78`)
> Expansion is served by `coverage` and `adjacency`; quality by `depth` …; discernment by `calibration`. (`LEARNING.md:85-86`)

The coverage map is the knowledge index, not the instrument table: "A row is written when its file exists, never before." (`corpus/README.md:9`), under `## Coverage map` (`corpus/README.md:11`).

`SKILL.md` points the domain at that file and does not treat the craft section as a province list: "Owned surfaces (verified 2026-10-13, see PROVINCE.md)" (`SKILL.md:10-11`).

## The two surfaces, and where they live

Claims file `plans/round-48-claims.md` at the declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` (read in the worktree; blob check below).

> Coverage gets no claim: this round adds no domain surface (no knowledge entry, no PROVINCE move, no coverage-map row). (`plans/round-48-claims.md:16-17`)

| claim | axis | where it lives | province list it would have to enter |
|---|---|---|---|
| R48-C1 | depth | `SKILL.md` `## Queue-drain craft` block 25, and the marker-bound instrument-registry section, scored by `tools/round-48/meanings.py` | none. Understanding folds into `SKILL.md` (`LEARNING.md:16-18`). Depth is a quality axis, not expansion. |
| R48-C2 | calibration | `tools/round-48/record2.py` re-derives `SCORECARD.md` | none. Calibration is discernment (`LEARNING.md:86`). The counter's card is `SCORECARD.md`. |

The instrument registry is the SKILL section opened by `<!-- instrument-registry v2 -->` and closed by `<!-- /instrument-registry -->` (`SKILL.md:1705` and `SKILL.md:1750`), headed `### Round-46 instrument registry` (`SKILL.md:1694`). `meanings.py` binds those markers (`REG_OPEN` / `REG_CLOSE` at `tools/round-48/meanings.py:51-52`). Its citation allow-list is `corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-48/` (`meanings.py:48-50`). It does not name `PROVINCE.md`.

`census2.json` is a path set of `tools/round-4[1-8]/**.{py,sh}` named in claim files (`tools/round-48/census2.json:2`). The round-48 names in that set are `tools/round-48/meanings.py` and `tools/round-48/record2.py` (`census2.json:44-45`, `:139-140`). No province path is in the set.

`record2.py` sets `CARD = "SCORECARD.md"` (`tools/round-48/record2.py:42`). A search of that file for `PROVINCE` returns no match. Causal separability in the claims file: C1 never reads `SCORECARD.md`; C2 never reads the craft section (`plans/round-48-claims.md:112-114`). Neither clause names `PROVINCE.md` as an input.

Landing requirement (`plans/round-48-claims.md:122-131`) names `SKILL.md` block 25, instrument-registry rows, and `SCORECARD.md` `## Round 48` / `## Record corrections — round 48` / the Owned-axes head. It does not name `PROVINCE.md`. Frozen paths are only `plans/round-48-claims.md` and `tools/round-48/` (`plans/round-48-claims.md:118-121`).

Same class of waiver, previous round, already landed without a province row:

> No domain surface is touched: no knowledge entry, no coverage-map row, no `PROVINCE.md` row. (`plans/round-47-claims.md:208-210`)

Round 46 stated the same coverage waiver for the instrument registry (`plans/round-46-claims.md:15-16`, `:21`).

## Do not confuse the two registries

`PROVINCE.md` already has a registry. It is not this one.

> Cross-lane registry this lane maintains: the REA surface map — per-client registration state, provider availability, provider env keys, and the on-host artifact inventory — kept in `corpus/knowledge/`, refreshed by `rea doctor` each round. (`PROVINCE.md:64-67`)

That paragraph is the REA map. Round 48 does not refresh doctor output, pins, or the artifact inventory: `git diff --name-only` from base `61b87d742032e65fca9c38267d7d6ed7e555edad` to the freeze names nothing under `PROVINCE.md`, `corpus/README.md`, or `corpus/knowledge` (receipt `diff-domain`, empty stdout). The sentence does not become false, and it does not oblige a new province row for `meanings.py` or `record2.py`.

The other "registry" hits in `PROVINCE.md` are the installed dissector registry (`PROVINCE.md:292`, `:299`). They are packet-capture holdings, not the SKILL instrument table.

## Clause 7's knowledge citation is a pointer

R48-C1 requires the craft block to cite at least one existing `corpus/knowledge/` path (`plans/round-48-claims.md:56-59`; `MUST_KNOW` at `meanings.py:50`). The counter's own draft citation is `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` (`meanings.py:471`, `:588`, `:637`). That stem is already a coverage-map row:

> Instrument admission (shortcut replay) | `2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop` | held as a tool, not as capability (`corpus/README.md:88`)

and an index row at `corpus/README.md:208`. Citing it adds no file, no coverage-map row, and no province surface. A new knowledge file is not in the landing requirement. If a later landing added one, the coverage map would then need a row because a row is written when its file exists (`corpus/README.md:9`); a `PROVINCE.md` row would be required only if that entry moved Core or Frontier. The freeze does not do that.

## Lines that must stay

Last `##` heading at the freeze is still the round-44 stop. There is no round-45, 46, 47, or 48 heading.

> ## Round-44 measured, not promoted (R44-C1 honest stop) (`PROVINCE.md:424`)
> SquashFS v1/v2 remain Frontier pending a new pre-data freeze that aligns the predicate and instrument. (`PROVINCE.md:430`)

Round 48 does not measure those images. That note stays.

Adjacent source-repo reconstruction stays unowned (`PROVINCE.md:108-109`; `SKILL.md:754-760`). Grading the lane's own `SKILL.md` and `SCORECARD.md` is not that ground, and it is not a reason to edit the exclusion.

`git grep` at the freeze for `instrument registry`, `SCORECARD`, `meanings.py`, `record2.py`, and `round-48` in `PROVINCE.md` exits 1 with empty stdout (no match). Nothing in the file names these surfaces, so nothing in the file is stale when they land in `SKILL.md` and `SCORECARD.md`.

## Tree facts

`git rev-parse --show-toplevel` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

`PROVINCE.md` blob `7f3f6563cff9130e2e0cd6050630244fb0d5a0b8` at base `61b87d74`, at freeze `dc73587a`, and at `HEAD` `f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`. Worktree vs freeze for that path is empty. `HEAD` is not the freeze; the province file has not moved with it.

Last commit that touches `PROVINCE.md`: `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`, 2026-10-28 09:57:16 -0300, `round-44: record C1 honest stop on frozen provenance mismatch`. Rounds 45–48 have not edited it. Base is an ancestor of the freeze (`merge-base --is-ancestor`, exit 0).

## Receipts

Copied to `.ufo/waves/round-48/w1/ScoutProvince/receipts/`. Empty stdout sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` is sha256 of zero bytes. `grep-province` exit 1 is git's "no match", not a counter exit.

| name | exit | stdout sha256 | UTC |
|---|---|---|---|
| toplevel | 0 | `ea76b3c71d6e707c31fe1bd21e40913ffe9c780f48271b045c54c6a8d5b4b417` | 2026-10-28T18:51:00Z |
| head | 0 | `9edd4cab7f827966743e78d3f16a4ba8cc34bb7eb1a034c2affea8a4539f057b` | 2026-10-28T18:51:00Z |
| ancestor | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T18:51:00Z |
| blobs | 0 | `04b08d4566069a415e64294ed102fd6979fb457682eebff8c5290407a3a11650` | 2026-10-28T18:51:00Z |
| diff-province | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T18:51:00Z |
| diff-domain | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T18:51:00Z |
| log-province | 0 | `ef23cd55b6ba27082bf1c12517b87923d95742ae320879a42ac46da9bdb73822` | 2026-10-28T18:51:00Z |
| grep-province | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T18:51:00Z |
| headings | 0 | `6aeefaff5e865894a92149d9c7029836118c7449d9f4f618a87488ae3c8564e7` | 2026-10-28T18:51:00Z |
| worktree-vs-freeze | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T18:51:00Z |

Commands are in the matching `.meta` files. Stderr was empty on every receipt (stderr sha256 = empty).

## Not run

- `tools/round-48/meanings.py` and `tools/round-48/record2.py` (claim scores belong to other seats).
- `scripts/hyaku/disk-guard.sh status` (no heavy pass).
- Any mutation of the lane tree other than this report and the receipt copies.
