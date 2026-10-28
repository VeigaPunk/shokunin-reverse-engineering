# ScoutShonen — SHONEN boxes at the round-48 freeze

Axes: coverage (all four boxes and the non-moving three), depth (the pointer grammar a `[~]` line must carry), calibration (the update line names only the box this round moves, and does not record a score).

Anchored at assignment freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` (`plans/round-48-claims.md` + `tools/round-48/`). Base `61b87d742032e65fca9c38267d7d6ed7e555edad`. `SHONEN.md` last changed at `8de80f1daec68260eb256eb68375e2c33af759a9` (2026-10-27 09:08:39 -0300, round 43). No install.

HEAD moved while this seat read (`f3a7afc42c1da2457ab0ffd1883c5bdb822f2962`, then `0d76deedd7ce9dd17c510494c33b7b00c3282554`, then `663f30ee751694fb0970e7de68fe88356e680822`). Facts below are pinned to the freeze unless a HEAD is named. `verdict-meaning-table` is absent from `SKILL.md` at the freeze and at `663f30ee` (both greps exit 1, empty stdout sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). `SHONEN.md` and `PROVINCE.md` diff empty against the freeze at `0d76deed`. That diff was not re-run at `663f30ee`.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — marker `[~]` at `SHONEN.md:5`. Round 48 moves this box. Update line is below. No `[x]`: no named non-author verifier.
- [~] At least one end-to-end domain task executed and logged in LOG.md — marker `[~]` at `SHONEN.md:8`. Unchanged this round.
- [~] Instructions executable by an agent without oral context — marker `[~]` at `SHONEN.md:11`. Unchanged this round.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — marker `[~]` at `SHONEN.md:14`. Unchanged this round.

Four boxes, four `[~]`, zero `[ ]`, zero `[x]`. Seed sentences are byte-identical to `PROTOCOL.md` lines 445–448 (`<name>` = `kaidoku-shokunin`).

## Pointer style a `[~]` line must carry

From `PROTOCOL.md` (promotion gates, evidence standard, file contract, marks):

- The mark is `[~]`, which means asserted by the lane. `[x]` is legal only as `[x] <named non-author verifier>`. A bare `[x]` counts as `[~]`. This round has no such verifier, so the mark stays `[~]`.
- The box line is `- [~] <seed sentence>`. The evidence is one indented line on that box: a resolvable pointer, not a naked assertion, not a fifth box.
- A pointer is a repo path, a command and its output, a commit cited by hash, or an external document. It has to resolve at closure. `/tmp` and `local://` do not count. A number carries its counting command. A quote carries file and line.

From the lane resolver still registered for this grammar, `tools/round-38/c2-counter.py:27-29` and `:100-110` (same `TOKEN`/`PTR` as `tools/round-36/c2-counter.py:24-25`):

- A mechanical pointer is a backtick token with no whitespace: `` `path` ``, `` `path:N` ``, or `` `path:N-M` ``.
- `PTR` is `^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$`.
- The path must match `LANE`: `corpus/`, `tools/`, `.ufo/`, `plans/`, `evidence/`, `scripts/`, `considerthese/`, or a root file `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`.
- A line range must satisfy `1 <= start <= end <=` the file's line count at the cited revision.
- Continuation lines that start with two spaces stay on the same box (`:88-96`). The live file uses that for its `asserted:` paragraph and its `Round 43:` sentence. A backtick that contains a space (a marker, a shell command) is not a pointer.

## Which box moves

`plans/round-48-claims.md:21` at the freeze names R48-C1 depth as craft rule block 25 in `SKILL.md` `## Queue-drain craft`. That is box 1.

`plans/round-48-claims.md:16-17` at the freeze: "Coverage gets no claim: this round adds no domain surface (no knowledge entry, no PROVINCE move, no coverage-map row)." That leaves box 2 (no LOG end-to-end task) and box 4 (no `PROVINCE.md` edit) unmoved. R48-C2 writes `SCORECARD.md`, which is not a SHONEN box. Box 3 stays: `tools/round-48/meanings.py` is the block-25 counter, the same class as blocks 22–24, and `SHONEN.md` has not taken a sentence for those blocks (last edit `8de80f1d`, round 43).

At the freeze, recipe A's craft split (`SCORECARD.md:121`, `'rule_blocks': len(rules)`) gives `rule_blocks` 24, last title starts `24. `, `HAS25 False`, `SKILL.md` 1750 lines. Receipt `blocks.out` (stdout sha256 `3fff0bf17eb5c5529e11a5b11a4d6902f2adf1a8702fd8822d124fd3bb77efe0`, exit 0, 2026-10-28T18:51:50Z). The counter `tools/round-48/meanings.py` was not run.

## Round 48 update line (box 1 only)

Append this single indented sentence under the box-1 `[~]`. Do not flip the mark. Do not add a sentence to boxes 2–4. The exit and the receipt path stay unfilled until a landing revision is re-measured.

```
  Round 48: depth surface only — craft rule block 25 is named at `plans/round-48-claims.md:21` and is absent from `SKILL.md` at dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 (recipe A split at `SCORECARD.md:121` gives rule_blocks 24; marker search exit 1). When it lands, the block's marker is `<!-- verdict-meaning-table v1 -->`, header `trigger | v1 hole | v2 arm | exit`, arm `meaning` for R46-CL7 and `floor` for R47-CL10, interpreter `tools/round-48/meanings.py`. Do not write a met claim, a 25-block count, or `[x]` in this sentence; fill exit and receipt only from a re-run of that interpreter at the landing revision. Boxes 2–4 get no Round 48 line (`plans/round-48-claims.md:16-17`).
```

Pointers in that sentence that the round-38 resolver will check, all present at the freeze: `plans/round-48-claims.md:21` (line 21 is the R48-C1 row; file is 154 lines), `SKILL.md`, `SCORECARD.md:121`, `tools/round-48/meanings.py` (`git cat-file -e` exit 0), `plans/round-48-claims.md:16-17`. The freeze hash is unbackticked so it is not parsed as a path. The marker and the header contain spaces, so they are prose, not pointers.

## Receipts

Seat dir `.ufo/waves/round-48/w1/ScoutShonen/`. Each `*.meta` has `utc`, `exit`, `stdout_sha256`, `cmd`.

| receipt | exit | stdout sha256 | what |
|---|---|---|---|
| `head` | 0 | `9edd4cab7f827966743e78d3f16a4ba8cc34bb7eb1a034c2affea8a4539f057b` | first `rev-parse HEAD` → `f3a7afc4…` |
| `freeze` | 0 | `b1500dada38bd3f73a4643517feebb0fb14f74741f260d06ff614e5d6c729047` | freeze verifies |
| `shonen-log` | 0 | `88368a120c4a04345d68021bab6b89faa1ae4b455da162b811751cc506c6c5e5` | last five `SHONEN.md` commits |
| `shonen-marks` | 0 | `5261188fe2400cb4f4e2a4b25f03047250e6a2b58963d3e6bf87f758134d1f86` | four `[~]` lines |
| `marker-freeze` | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | marker absent at freeze |
| `marker-head` | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | marker absent at `f3a7afc4` |
| `marker-head-now` | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | marker absent at `663f30ee` |
| `shonen-same` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | empty diff, freeze..`f3a7afc4`, `SHONEN.md` `PROVINCE.md` `LOG.md` |
| `blocks` | 0 | `3fff0bf17eb5c5529e11a5b11a4d6902f2adf1a8702fd8822d124fd3bb77efe0` | rule_blocks 24, HAS25 false |
| `claims-lines` | 0 | `1852161993562e34002222eb9c73031f840e5addcafad7d8ff240ac56b6d6444` | freeze lines 15–21; A2 absent at freeze, present at `f3a7afc4` |
| `claims-log` | 0 | `3f6e8d506c0d846038e80c6cc23de9de674715131c6b0a8250100ac083218696` | `ac02a79` A2, `f3a7afc4` A3, `0f06251` A4, each subject says declared freeze |
| `pin` | 0 | `0f7c7d918f6b20c221dacbab51e846aa2d4d745658ae737d18e0e955f3a4a7f0` | lines 16–17 and 21; paths exist; SHONEN/PROVINCE diff empty at `0d76deed` |
| `a2` | 0 | `2faeb0bd2a9f028f63bf318da3cd19b981692092e7f06980a712cc299aa885d9` | A2 heading at `HEAD:plans/round-48-claims.md:147` during that read |
| `scorecard-recipe` | 0 | `81dd5e25dd8ad117d6c9e46f0ada897da38c709f42a1b2a5fe2bcdbabd14f0a1` | `SCORECARD.md:86` and `:121` at the freeze |
| `status` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | porcelain empty for the five paths at that instant |

`claims-slice.meta` records `git show -s --format=%H` on the freeze blob. stdout is the 154-line freeze file, not a hash. Use `claims-lines` and `pin` for the line pins.

Scratch `/fast/scratch/hyaku/kaidoku-r48/ScoutShonen` removed after these receipts were in the seat dir. `meanings.py` and `record2.py`: not run.
