# C2Mutation — mutation test of the R25-C2 coverage instrument

Target: `tools/round-25/a2/c2-coverage.py` (sha256 `7a7e6d6529033c5dfac6da252507ac597b30f0a3d4740522d17f87f4ee6b2c70`).
Base commit: `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (C2 landing commit).
Method: sandbox clone `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2Mutation/clone`; one defect per commit;
real instrument run on each commit; clone reset to base after every mutant.
Detector: `python3 -I -B tools/round-25/a2/c2-coverage.py --root <clone> --rev <mutant rev>`; exit 0 + `entry_sourced:1` = pass.
Baseline at base rev (2026-10-22T10:50:01Z): `knowledge_md 108`, `cited_rows [S021,S075,S076,S077]`,
`qualifying_rows [S075,S076,S077]`, `entry_sourced 1`, exit 0. Same output from the lane at the same rev.

## Mutant table

`md` = `knowledge_md`. "Kill" = instrument reports the entry unsourced (exit 1). All rows ran 2026-10-22T10:53:02Z.

| id | mutation | md | qualifying_rows | exit | verdict |
|---|---|---|---|---|---|
| M1 | S075-S077 `status` mined→opened | 108 | [] | 1 | killed |
| M2 | S075-S077 `opened` 2026-10-22→2026-10-21 | 108 | [] | 1 | killed |
| M3 | `used-by` of all three rows drops the entry path | 108 | [] | 1 | killed |
| M4 | entry `source:` line keeps only S021 (no S07x) | 108 | [] | 1 | killed |
| M5 | entry renamed to `…-resolution-v2.md` | 108 | [] (`entry_present:false`) | 1 | killed |
| M6 | S075 row truncated to too few cells | 108 | [S076,S077] | 0 | **survived** |
| M7 | all three rows truncated to too few cells | 108 | [] | 1 | killed |
| M8 | S077 URL → `https://example.invalid/never-fetched/interpretation.md` | 108 | [S075,S076,S077] | 0 | **survived (false accept)** |
| M9 | `used-by` → `…-resolution.md-old` (lookalike, no such file) | 108 | [S075,S076,S077] | 0 | **survived (false accept)** |
| M10 | entry cites only a fabricated never-opened row S078 | 108 | [S078] | 0 | **survived (false accept)** |
| M11 | same fabricated S078 but `status`=planned | 108 | [] | 1 | killed |
| M12 | `opened` cell → `2026-10-22 (never)` | 108 | [] | 1 | killed |
| M13 | one extra column inserted before `status` (14 cells) | 108 | [] | 1 | killed |
| M14 | `used-by` prefixed `./` | 108 | [S075,S076,S077] | 0 | **survived (false accept)** |
| M15 | entry body emptied, only the `source:` line kept | 108 | [S075,S076,S077] | 0 | **survived** |
| M16 | S075 `teaches` cell blanked | 108 | [S075,S076,S077] | 0 | **survived** |
| M17 | S075-S077 moved to `corpus/SOURCES-other.md` | 108 | [] | 1 | killed |
| M18 | unrelated knowledge `.md` added (108→109) | 109 | [S075,S076,S077] | 0 | **survived (count not gated)** |
| M19 | `corpus/knowledge/.gitkeep` deleted | 108 | [S075,S076,S077] | 0 | survived (no `.md` lost) |
| M20 | only S075 `used-by` drops the entry | 108 | [S076,S077] | 0 | survived (one row suffices) |
| M21 | entry `source:` line cites only S076 | 108 | [S076] | 0 | survived (one row suffices) |
| M22 | a real knowledge `.md` deleted (108→107) | 107 | [S075,S076,S077] | 0 | **survived (count not gated)** |
| M23 | duplicate S076 row appended with `status`=opened | 108 | [S075,S077] | 0 | survived (last row wins) |
| M24 | S021 `opened` forged to 2026-10-22, `used-by` extended (entry still cites S075-S077) | 108 | [S021,S075,S076,S077] | 0 | survived |
| M25 | entry cites only S021, S021 opened 2026-10-19 | 108 | [] | 1 | killed |
| M26 | entry cites only S021; S021 `opened` forged to 2026-10-22 | 108 | [S021] | 0 | **survived (false accept)** |
| M27 | entry `source:` line capitalised `Source:` | 108 | [] | 1 | killed |
| M28 | a first `source:` line with no S-ids precedes the real one | 108 | [] | 1 | killed |

Six required mutants: M1, M2, M3, M4, M5 killed; the "row with too few cells" case is M6/M7 — killed only when
every row is malformed (M7); one malformed row is silently ignored (M6).

## Does the instrument check that the source was actually opened?

**No. [observation]** The instrument never opens anything. It parses the `corpus/SOURCES.md` blob and tests three
literal cell strings: `cells[8] == "mined"`, `cells[9] == "2026-10-22"` (hard-coded `OPENED` constant), and
`ENTRY in cells[11]` (substring, not path-list membership). It never fetches the URL, never checks an anchor quote,
never looks for a saved evidence artifact, and never cross-checks the `opened` cell against the row's own `anchor`
cell. Three independent mutants prove this (M8, M10, M26).

## False accepts (instrument says sourced, truth is not sourced)

1. **M10 — a row citing the entry but never opened.** A fabricated row was appended:
   `| S078 | Never fetched placeholder — https://example.invalid/never-fetched | docs | A | A source that was never
   opened | no anchor | nothing | mined | 2026-10-22 | 180d | corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md |`,
   and the entry's `source:` line was changed to cite only S078. Output:
   `"cited_rows": ["S078"], "qualifying_rows": ["S078"], "entry_sourced": 1`, exit 0. Nothing about S078 was ever
   fetched or saved; the instrument passes it because the row *says* mined/2026-10-22.
2. **M8 — a never-fetched URL inside a real row.** S075-S077 stay as they are except S077's source URL becomes
   `https://example.invalid/never-fetched/interpretation.md`; `qualifying_rows` still `[S075,S076,S077]`, exit 0.
3. **M26 — a prior-round source re-dated.** S021 was genuinely fetched 2026-10-19 (its `anchor` cell still reads
   "Current `latest` page fetched 2026-10-19; `Function Selector`" in the mutated commit, and the entry body still
   cites it as opened 2026-10-19). Forging only its `opened` cell to `2026-10-22` and extending its `used-by` makes
   the entry "sourced" via a source that was never opened this round: `qualifying_rows ["S021"]`, exit 0.
   M25 shows the same row unmodified is correctly rejected — the instrument's opinion is driven purely by the cell.

Other survivals are coverage findings, not false statements about opening:
- M6/M23 — one malformed or shadowing row among three is silently ignored; the row is not parsed at all
  (`len(cells) >= 13` gate) or is overwritten by a later duplicate id (last row wins). Exit stays 0.
- M9/M14 — `used-by` is matched as a substring, so a lookalike path (`…-resolution.md-old`) or a `./`-prefixed path
  satisfies it even though no such file is named.
- M15/M16 — the entry's content is never inspected: an entry consisting only of its `source:` line passes, and a
  blanked `teaches` cell passes.
- M18/M22 — `knowledge_md` is printed but never asserted, so the "108" half of the claim cannot fail this
  instrument: 109 and 107 both exit 0. The count must be checked by the caller (or by a gate), not by this tool.
- M20/M21 — one qualifying row is enough, so the entry need not be sourced by the rows it actually relies on.

Brittle-by-design points worth disclosing (all fail closed): M13 (an extra column shifts the status/opened/used-by
indices, so the row stops qualifying), M12 (strict string equality on the date), M27/M28 (the first line starting
with `source:` wins; a decal `source:` line or a capital `Source:` yields no citations). The parser is also
position-based: it assumes exactly the current column order of `corpus/SOURCES.md`.

## Restoration and bounds

- Clone reset to `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`, `git status --porcelain` empty.
- Pristine bytes after the run: `corpus/SOURCES.md` sha256 `4ebc0a1800b391a654c90ee16c3370dd4825f9f31007d7d1e9e668cf25556895`,
  entry sha256 `3a888b155834e0a0633c75bb69d2c0077654c7053ea566e6a43b9279231fb624` — identical to
  `git show 08c7a72:…` for both. Each mutant's before/after hashes are in `final_table.json`.
- Lane read-only: no lane file was edited, no git write, no `jj`. The lane working tree shows
  `M corpus/SOURCES.md`, `M corpus/knowledge/…-resolution.md`, `M SCORECARD.md`, `M corpus/lessons/round-25.md`
  — those are other agents' uncommitted edits, present before and after my run; I did not touch them. My mutants
  were applied in the clone only, so they target the frozen commit, not the moved lane working tree.
- No packages installed. No network calls. No REA runs (not needed for this target).

## Artifacts (scratch dir, sha256)

`final_table.json` `c236efacfddeb4c78f3ad5a5ac16ca5031f5708e3c30ef9b1046169ee9ad92ba` — all 28 mutants with revs, UTC and
before/after hashes. Harnesses: `harness.py` `3cb43ccb27ae56e2…` , `harness2.py` `905af2dc72052fcbb…`,
`harness3.py` `7f9e1309993a394c…`, `harness4.py` `16e6e9cbc4b898f0…`, `harness5.py` `390a6893d433bd59f…`,
`harness6.py` `d93abb3ced8bcf76…`, `harness7.py` `4f93a736966fe4c9…` (M29 no-op aborted that batch; superseded by
`harness7b.py` `142e3edadb8e41ff…`), `replay.py` `62c400bce7cfcddb…`.
Raw per-batch results: `results.json` `3f221245903ad154…`, `results2.json` `1fcdaa61ff089857…`,
`results3.json` `11f5f61d84dcd898…`, `results4.json` `8ab2b4cdbcf52ee6…`, `results5.json` `e61e777a1ad3c7a4…`,
`results6.json` `8a37a17ed9cb71ae…`, `results7.json` `5a77f8de89559f23…`. Full digests in the seat directory.

## Verdict on the frozen claim

The instrument does detect each of the six named defects it was built to detect except the malformed-row case
(M6). It does **not** establish that the entry's sources were opened; three mutants (M8, M10, M26) make it report
`entry_sourced: 1` for sources that were never opened. R25-C2's "opened 2026-10-22" half of the claim is therefore
self-reported by `corpus/SOURCES.md` cells, not verified by the instrument. [inference] The lane's separate
per-source envelopes and saved lookups are the evidence for actual opening; this counter cannot be, and should not
be cited as, that evidence.
