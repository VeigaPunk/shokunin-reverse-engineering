# Round 29 freeze-gate behavior

## Scope and verdicts

Compared the frozen R24 gate with `tools/round-29/freeze-gate.py` at measured commit `18be864a528873b2b70d8c94e31f880290249e90`; all execution was against a scratch clone at that commit. The full gate JSON outputs, exit-code files, and freeze lists are retained under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/`.

- **[OBSERVATION] “Audits every `claims*.json`”: holds for the new gate's path pattern.** At the measured tip, the new gate audits all 16 files the old gate audits plus three additional matching files. The fixture also shows the new gate auditing `claims-x.json` while the old gate omits it. **[INFERENCE / boundary]** This means every file matching the new gate's regex under `.ufo/waves/round-N/` (the `claims` prefix, permitted suffix characters, and `.json` suffix), not every arbitrary claims-named file anywhere in the repository.
- **[OBSERVATION] Pin-key change: holds.** For an instrument whose matching SHA is recorded only under `producers_not_counters`, the new gate returns `CLEAN`, while the old gate reports `INSTRUMENT_UNPINNED`. The fixture separately demonstrates the new gate reporting an unpinned instrument named by the extra claims file.
- **[OBSERVATION] Both measured-tip runs exited 0 and matched their respective disclosure ledgers exactly** (16/16 and 19/19). Findings remain in the gate output; exit 0 here means no required-clean or disclosure mismatch was requested/found.

## Measured-tip gate outputs

At `2026-10-22T20:22:21Z`, these were run in the scratch clone:

```text
python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/clone/.ufo/waves/round-24/tools/freeze-gate.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/clone --rev 18be864a528873b2b70d8c94e31f880290249e90 --disclosures corpus/claim-freezes.tsv
python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/clone/tools/round-29/freeze-gate.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/clone --rev 18be864a528873b2b70d8c94e31f880290249e90 --disclosures corpus/claim-freezes-v2.tsv
```

Exact `jq -c '{claim,rev,audited,clean,flagged,summary,disclosures}'` output excerpts (full unprojected JSON is in the named artifacts):

```json
{"claim":"R24-C2","rev":"18be864a528873b2b70d8c94e31f880290249e90","audited":16,"clean":1,"flagged":["round-14","round-15","round-16","round-17","round-18","round-19","round-20","round-21","round-22","round-23","round-25","round-26","round-27","round-28","round-29"],"summary":{"INSTRUMENT_ABSENT":12,"INSTRUMENT_NONE":3,"INSTRUMENT_PIN_MISMATCH":0,"INSTRUMENT_REVISED":15,"INSTRUMENT_UNPINNED":10,"INSTRUMENT_UNRESOLVED":9},"disclosures":{"exact":16,"mismatched":[],"missing":[],"of":16,"path":"corpus/claim-freezes.tsv","present":true,"stray":[]}}
{"claim":"R29-freeze-gate","rev":"18be864a528873b2b70d8c94e31f880290249e90","audited":19,"clean":2,"flagged":["round-14","round-14/claims-review.json","round-15","round-15/claims-review.json","round-16","round-17","round-18","round-19","round-20","round-21","round-22","round-23","round-25","round-26","round-27","round-28","round-29"],"summary":{"INSTRUMENT_ABSENT":12,"INSTRUMENT_NONE":5,"INSTRUMENT_PIN_MISMATCH":0,"INSTRUMENT_REVISED":15,"INSTRUMENT_UNPINNED":6,"INSTRUMENT_UNRESOLVED":9},"disclosures":{"exact":19,"mismatched":[],"missing":[],"of":19,"path":"corpus/claim-freezes-v2.tsv","present":true,"stray":[]}}
```

**Exit codes:** old `0` (`old-tip.exit`); new `0` (`new-tip.exit`). The JSON contains the exact disclosure results and no missing, mismatched, or stray rows.

## Freeze-list comparison

**[OBSERVATION]** At `2026-10-22T20:23:31Z`, compared `jq -r '.freezes[].claims_file'` from the two saved tip outputs, sorted under `LC_ALL=C`, then used `comm -23` and `comm -13`. Exact output:

```text
old_count=16
new_count=19
old_only:
new_only:
.ufo/waves/round-14/claims-review.json
.ufo/waves/round-15/claims-review.json
.ufo/waves/round-28/claims-c2.json
exit=0
```

Thus the lists have 16 shared entries, no old-only entries, and the three listed new-only entries. The sorted complete lists are retained as `old-freeze-list.txt` and `new-freeze-list.txt`.

## Fixture evidence

Created and committed a small fixture repository at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/fixture`, HEAD `c6a5f9357a6cfb210c4c042bd5ffbfeed97126bb`. `claims.json` names `tools/producer.py` and records its SHA under `producers_not_counters`; `claims-x.json` names `tools/unpinned.py` without a SHA.

At `2026-10-22T20:22:11Z`, the old gate was run with `--root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/fixture --rev c6a5f9357a6cfb210c4c042bd5ffbfeed97126bb`:

```json
{"claim":"R24-C2","rev":"c6a5f9357a6cfb210c4c042bd5ffbfeed97126bb","audited":1,"clean":0,"flagged":["round-99"],"summary":{"INSTRUMENT_ABSENT":0,"INSTRUMENT_NONE":0,"INSTRUMENT_PIN_MISMATCH":0,"INSTRUMENT_REVISED":0,"INSTRUMENT_UNPINNED":1,"INSTRUMENT_UNRESOLVED":0},"freezes":[{"claims_file":".ufo/waves/round-99/claims.json","verdict":"FLAGGED","instruments":["tools/producer.py"],"findings":[{"finding":"INSTRUMENT_UNPINNED","path":"tools/producer.py"}]}]}
exit=0
```

At `2026-10-22T20:22:07Z`, the new gate was run with the same root and revision:

```json
{"claim":"R29-freeze-gate","rev":"c6a5f9357a6cfb210c4c042bd5ffbfeed97126bb","audited":2,"clean":1,"flagged":["round-99/claims-x.json"],"summary":{"INSTRUMENT_ABSENT":0,"INSTRUMENT_NONE":0,"INSTRUMENT_PIN_MISMATCH":0,"INSTRUMENT_REVISED":0,"INSTRUMENT_UNPINNED":1,"INSTRUMENT_UNRESOLVED":0},"freezes":[{"claims_file":".ufo/waves/round-99/claims.json","verdict":"CLEAN","instruments":["tools/producer.py"],"findings":[]},{"claims_file":".ufo/waves/round-99/claims-x.json","verdict":"FLAGGED","instruments":["tools/unpinned.py"],"findings":[{"finding":"INSTRUMENT_UNPINNED","path":"tools/unpinned.py"}]}]}
exit=0
```

**[OBSERVATION]** This distinguishes both changes: the new gate sees and flags the extra unpinned claims file; the old gate audits only `claims.json` and does not report `claims-x.json`. For `tools/producer.py`, the exact SHA is `f2615fd47ab6cf6a472cab18a73ba01d9cbee56c0215db2114a4329e00d22ca0`; new-gate `CLEAN` versus old-gate `INSTRUMENT_UNPINNED` demonstrates the producer-pin change.

Fixture tracked-file list and SHA-256, produced by `git ls-files -z | xargs -0 sha256sum` at `2026-10-22T20:23:37Z`:

```text
afeab94e21c514546492e9fc83aa60f015de5c965b204af70cd96cd09b0f2fd4  .ufo/waves/round-99/claims-x.json
fb0226ba530095aeeb1558a1179f405f5fd20ac8c4af5ee9a927d470fcd62bfe  .ufo/waves/round-99/claims.json
f2615fd47ab6cf6a472cab18a73ba01d9cbee56c0215db2114a4329e00d22ca0  tools/producer.py
b2ab78c99344a1b40a312b532821d55d6511b127fbbff76dc8dcfbbc7f1d27a5  tools/unpinned.py
```

## Retained artifacts and hashes

The following hashes were produced by `sha256sum` at `2026-10-22T20:23:37Z`. Paths are relative to `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecGateV2/`:

```text
e79e1c4e3ffb37f9173f575d0e33de3f0652e84c4c1c1c41a468d3ce172fda03  old-tip.json
217131d553651d2cc36316c57b857b8d78cdb9b40de01658440e904a568b800c  new-tip.json
f131949a71c0e95d2a75eb5b2f1c75e94c93be62ca5eda13380269cc5dffe048  old-fixture.json
d57114661b9bfa1a8dc6b2bd37fe1795d0e0f7bbac58953dca85f21e47493fe8  new-fixture.json
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  old-tip.exit
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  new-tip.exit
281f111c4ab9cf6166c842d1e8007c2362b18ae633e905cf305c7318c35fa08f  old-freeze-list.txt
92cc62c1f629c58a604746dbeb1ff6b0d7b46b933259ab9a737778209794ee6f  new-freeze-list.txt
8a71fe84b94310b1b600793b4af011e586359304a6302ee33662d6522290b329  clone/.ufo/waves/round-24/tools/freeze-gate.py
25b54339ce5f966309ce159fd2767579521d05eb239916d7dee0269f88b93eb2  clone/tools/round-29/freeze-gate.py
5b5affb854997943bed2a626cf1a1f4f6d77c25c6b22a4753fb7fe01a5f50129  clone/corpus/claim-freezes.tsv
c08e84e281f56b7fd33a5e6cd21e08b95b6092c6da4d5144bed76cc0a85d7532  clone/corpus/claim-freezes-v2.tsv
```

No tools were installed or updated. No blockers. **Risk/boundary [INFERENCE]:** callers should not interpret “every `claims*.json`” more broadly than the gate's `.ufo/waves/round-N/` matcher and filename regex; the gate evaluates the selected committed revision, not uncommitted files.
