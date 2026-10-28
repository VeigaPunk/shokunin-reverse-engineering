# R46W1ExecGap — the round-45 discrimination gap, measured live on committed bytes

Seat `R46W1ExecGap` (executor), round 46 wave 1. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze per the frozen claims file and the
seat prompt: `31820472784284727546808acc31b3ea1e73919b`. Lane HEAD moved during the seat
(concurrent wave-1 commits); every receipt below pins the revision it ran at. Toolchain:
`/usr/bin/python3` 3.14.8, git 2.56.0. No installs, no upgrades, no lane writes, no git
mutation.

## Verdict in one paragraph

**The gap is real and reproducible from committed text.** The round-45 cheapest-green C1
forgery — 21 plain bullets, a garbage four-column table, four one-line citations — scores
`met_target: true` **exit 0** under the frozen round-45 counter
(`tools/round-45/c1-counter.py` @ the freeze, sha256 `2cfc5a48…`) **and** under
`tools/round-46/attest.py --spec r45 --profile v1` (exit 0, byte-identical stdout at the
freeze bytes and at HEAD bytes). It does so **with the real
`tools/round-45/frozen-path-preflight.py`** (`cases=11 failures=0`), not only with the
4-line stub — so the acceptance is the artefact's shape, not the interpreter's identity.
The round-46 v2 code path rejects the same fixture (exit 1), which is the hole C1 closes.
Separately, the seat surfaced a **live freeze-identity defect**: the freeze the frozen file
defines is not the freeze the landing was scored against, and the frozen `tools/round-46/`
directory has been edited after *both* candidate freezes — every lane score against either
freeze now exits 2 `frozen_path_changed` (details §7; I did not "fix" anything).

## 1. The forgery under measurement

| item | value |
|---|---|
| round-45 seat that recorded it | `R45W1CritC1`, label `fx-a6-cheapest-green` |
| round-45 receipt | `.ufo/waves/round-45/w1/R45W1CritC1/receipts.json`, exit **0**, stdout sha256 `34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3`, UTC `2026-10-28T15:42:01Z` |
| surviving reconstruction | `.ufo/waves/round-45/w2/R45W2Lesson/fx-a6-SKILL.md`, sha256 `cc523958abcc3d484e89da26a7c2137461d8fbb4c440aee9ec4ad8c22632516a` |
| line count | **40** (`wc -l`), not the 44 the claims file and R45-CL13 quote — the critic's scratch is gone and the reconstruction is the only persistent copy; record discrepancy, not a verdict |
| its content | 21 `- **N. Plain rule N.**` bullets + block `22.` with `<!-- freeze-integrity-table v1 -->` carrying 8 `\| lorem i \| ipsum \| i%3 \| dolor \|` rows + four `:1` citations + a citation of the interpreter path |

The label was found by `grep -n "cheapest\|a6"` over `R45W1CritC1/report.md` (line 41 and
line 139 of the receipt table) and cross-checked against `receipts.json` entry
`fx-a6-cheapest-green` (exit 0).

## 2. Fixtures

Two one-commit private repos, `git init -q` inside
`S=/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap`, toplevel asserted equal to the fixture path
before the first commit. Contents per fixture:

- `SKILL.md` — the reconstruction bytes above (byte-identical, sha `cc523958…`);
- `plans/round-45-claims.md` — the lane's round-45 claims file at HEAD (its
  `## Frozen paths (exact)` section names `plans/round-45-claims.md` and `tools/round-45/`);
- `tools/round-45/frozen-path-preflight.py` — **real** bytes (sha `633ebc05…`) in `fx-a6-real`,
  the 4-line stub (sha `815c2fe9…`) in `fx-a6-stub` (the critic's exact variant);
- `tools/round-45/c1-counter.py` — at the freeze, sha `2cfc5a48…` (the fixture's frozen dir is
  internally consistent; freeze == rev, so the frozen-path arm is clean by construction and
  the measurement isolates discrimination, not freeze hygiene);
- the four cited files, real bytes: `corpus/lessons/round-44.md`,
  `corpus/lessons/round-44-verifier-spotcheck.md`,
  `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`, `plans/round-45-claims.md`.

`fx-a6-real` rev `85a03abf1990e68977e32eba4dee159b5bee6ae5`;
`fx-a6-stub` rev `53c7cc2dbdb86c64777908ce2ab3c8ab15d744cc`.

## 3. Receipt A — the FROZEN round-45 counter accepts the forgery

```
/usr/bin/python3 -I -B $S/bin/c1-counter.py --root $S/fx-a6-real \
  --freeze 85a03abf… --rev 85a03abf…
```

| field | value |
|---|---|
| exit | **0** |
| `met_target` | **true** |
| stdout sha256 | `2190dce38491eaaa83866e3494a6526550d7d428e2900c3cdb0dc8b6c12b231e` |
| UTC | `2026-10-28T17:00:23Z` |
| counter's own clause values | `rule_blocks 22`, `block22_present 1`, `block22_rows 8`, `block22_refs 4`, `block22_unresolved_citations []`, `block22_header_ok true`, `block22_cites {S140: true, interpreter: true}`, `preflight_selftest {cases: 11, failures: 0, ok: true}`, `frozen_path_changed []` |

Stub variant (`fx-a6-stub`, the critic's exact artefact): exit **0**, stdout sha256
`08b01417a3a50aef3f8fcf98d0f38df8f0933f20a559fc99f4f2e53625537c47`, UTC
`2026-10-28T17:00:24Z`, `preflight_selftest {cases: 11, failures: 0, ok: true}` parsed from a
4-line print.

The stdout sha differs from the critic's `34336cf7…` because the fixture commit, its file set
and the freeze OID differ; the **verdict and every clause value match**.

## 4. Receipt B — the round-46 v1 profile accepts the same forgery

```
/usr/bin/python3 -I -B $S/bin/r46-freeze/attest.py --root $S/fx-a6-real \
  --freeze 85a03abf… --rev 85a03abf… --spec r45 --profile v1 --no-battery
/usr/bin/python3 -I -B $S/bin/r46-head/attest.py   --root $S/fx-a6-real \
  --freeze 85a03abf… --rev 85a03abf… --spec r45 --profile v1 --no-battery
```

| instrument bytes | exit | stdout sha256 | UTC |
|---|---|---|---|
| freeze `attest.py` (`dd1e7df1…`, `gate.py` `64626cca…`) | **0** | `1828bf2205319256d6b92b0a8458e41706ec91831a5c41aeee5101f7ca9ac23f` | `2026-10-28T17:00:23Z` |
| HEAD `attest.py` (`e6c44d2d…`, `gate.py` `847aa33b…`) | **0** | `1828bf2205319256d6b92b0a8458e41706ec91831a5c41aeee5101f7ca9ac23f` | `2026-10-28T17:00:23Z` |

Identical stdout under both byte sets: the F3 v1-port fixes (row floor, header/selector
clauses) change nothing on this artefact — the port is faithful in the direction that matters
for the control. Receipt clause values: `rule_blocks 22`, `marker_occurrences 1`,
`block_present 1`, `header_ok true` (substring containment), `rows 8` (== `v1_min_rows`),
`refs 4` (== `refs_min`), `unresolved_citations []`, `cites {S140: true, interpreter-path:
true}`, `met_target true`, `frozen_path_changed []`.

Stub variant: exit **0**, sha256 `fc8a25b124297f88bf9086405fef789c64e93cd69b3e6f973ebeb644398d4184`,
UTC `2026-10-28T17:00:24Z`.

**Answer to the seat's question: yes.** A forgery round 45 accepted is still accepted by the
round-46 v1 profile, on the frozen v1 clause set and on today's bytes. `ctl-c1-1-v1-profile`'s
premise is confirmed on this artefact, not merely asserted.

`--no-battery` is the correct switch for this comparison: the round-45 clause set has no
battery arm, and `score(…, battery=…)` imposes the r46 constants (`forgeries_total == 9`,
`v1_green == 9`, …) regardless of `--profile`, so with the battery on the v1 run exits **1**
(stdout sha `8bec2894…`) for a reason that is not part of the round-45 predicate.

## 5. Control — the v2 code path rejects it (exit 1)

```
/usr/bin/python3 -I -B $S/bin/r46-head/attest.py --root $S/fx-a6-real \
  --freeze 85a03abf… --rev 85a03abf… --spec r45 --profile v2 --no-battery
```

| field | value |
|---|---|
| exit | **1** |
| `failing` | `["unresolved or unvalidated citations: 1"]` |
| the offending ref | `tools/round-45/frozen-path-preflight.py: outside the validated path set` |
| stdout sha256 | `27c7515423ab83e1f11418c7abd63ad6cb433f66d9afc49f8de789c2d9e7c58a` |
| UTC | `2026-10-28T17:00:24Z` |

Honest calibration of that verdict: under `--spec r45` the v2 rejection of this artefact is
carried **only** by the citation allowlist (`tools/…` is outside the r45 `allow` tuple). The
garbage rows themselves stay invisible to `--spec r45` at any profile, because `routed` and
`vocab` are r46-only. The claim's discrimination against garbage rows lives in the **r46 v2**
surface (block 23: thirteen routed `R45-CL<n>` ids in cell 0 plus the arm vocabulary), not in
the r45 spec replayed at v2. Anyone reading "v2 rejects the a6 forgery" as "v2 rejects garbage
rows" would be reading one clause as another.

## 6. What the v1 acceptance is made of (so the landing can cite the mechanism)

Every closed v1 hole that produces the exit 0, with the a6 value that satisfies it:

| R45-CL13 sub-defect | a6 value that passes | where it is caught now |
|---|---|---|
| (a) no interpreter pin | no pin required; selftest banner parsed from any file | block 23 clause 6 (`sha256:` pin vs bytes at `--rev`) |
| (b) citations with no line selector / off-topic | four `:1` refs to real files, none about freeze integrity | clause 5 (line selector mandatory, allowlist validated) |
| (c) header by substring | `\| trigger \| arm \| exit \| receipt \|` matches by `in` | clause 2 (exact header equality) |
| (d) marker counted per block | one marker suffices | clause 1 (`marker_occurrences == 1`) |
| (e) block count inflated/`>=` | 22 exact bullets, no semantic index | clause 1–4 (`23.` title, routed ids, vocabulary) |
| (f) crash → exit 1, empty stdout | not exercised by this fixture | `Malformed` → exit 2 with reason (selftest case) |
| rows are shape only | 8 garbage rows == floor | clause 3–4 (13 rows, routed id + arm token per row) |

## 7. Finding (not fixed): the freeze the file defines is not the freeze that was scored

The frozen file's own text: "**Freeze** = the commit that first contains this file and
`tools/round-46/`… `git log --format=%H -1 -- plans/round-46-claims.md` re-derives it.
Nothing in this file or in `tools/round-46/` changes after the freeze."

Measured (`freeze-probes.json`, `lane-admissibility.json`):

| command (`git -C <lane>`) | value |
|---|---|
| `log --format=%H -1 -- plans/round-46-claims.md` | `31820472784284727546808acc31b3ea1e73919b` |
| `log --format=%H -1 -- tools/round-46/` | `0425224756791b414454df28a9abf93dcdf154ce` at probe time; `65678df0…` before F4 |
| `diff --stat 3182047..HEAD -- plans/round-46-claims.md tools/round-46/` | `attest.py 59 ±`, `gate.py 3 ±`, `registry.py 12 ±`, 45 insertions / 29 deletions |
| frozen-byte sha256 `attest.py` @freeze → @HEAD | `dd1e7df1…` → `e6c44d2d…` |
| frozen-byte sha256 `gate.py` @freeze → @HEAD | `64626cca…` → `847aa33b…` |
| frozen-byte sha256 `registry.py` @freeze → @HEAD | `307506d5…` → `5e16e4af…` (via `db5adc02…`) |
| `log -m --diff-merges=first-parent --name-status 3182047..HEAD -- <frozen>` | touches at `50862e4a` (attest+gate+registry), `65678df0` (attest), `0425224` (registry) |

Consequences, each measured:

1. `attest.py --freeze 3182047… --rev <head> --no-battery` → **exit 2**
   `frozen_path_changed` = `[tools/round-46/, tools/round-46/attest.py, gate.py, registry.py]`,
   `restored` = the same three files. Identical stdout sha `4800c402…` whether the instrument
   is the freeze bytes or the HEAD bytes (UTC `2026-10-28T17:01:59Z`, rev `1e32827b…`).
   So under the file's own freeze the lane's claim is **inadmissible** — as the file says it
   must be.
2. The landing was scored against a freeze that exists only in a commit message:
   `50862e4a` — "…declared as the authoritative freeze because the first freeze commit did not
   carry the final bytes". The frozen file contains no such declaration, so the freeze cannot
   be re-derived from the rule; it is declared by the same actor who then edits the frozen
   directory (three times: `50862e4a`, `65678df0`, `0425224`).
3. Even at that declared freeze, the landing is now inadmissible: `0425224` (F4) rewrote
   `tools/round-46/registry.py`, so
   `attest.py|registry.py --freeze 65678df0… --rev 0425224… --no-battery` → **exit 2**
   `frozen_path_changed = [tools/round-46/, tools/round-46/registry.py]` (C1 sha
   `1f75bcb0…`, C2 sha `4cbd87d5…`, UTC `2026-10-28T17:02:47Z`). The same at HEAD
   (`attest` `7c7a664c…`, `registry` `2dcaf5dc…`). Yet commit `1e32827b` reports "both claims
   met at 0425224".
   For the record, the earlier probe at rev `781e19ae` (before F4) with that freeze exited
   **0** (`9494851b…`, UTC `2026-10-28T17:00:25Z`) — the window in which the landing was
   admissible closed when `registry.py` was edited.
4. Receipt-label defect in the frozen core: `restored` names paths whose *bytes differ*
   between freeze and rev. For the directory entry `tools/round-46/`, `blob_changed` carries
   only the directory, so every touched file beneath it lands in `restored`:
   `registry.py` is reported `restored` while its sha goes `db5adc02…` → `5e16e4af…`. The
   verdict (exit 2) is right; the label is wrong (`R45-CL24`-class record drift).

I did not change the frozen bytes, re-declare a freeze, or re-score the claims. This is the
L1's reconciliation: the frozen text is the rule, and by it the current rev is not admissible.

## 8. Limits and non-claims

- Not run: `--selftest` of either round-46 instrument (other seats own it); the lane's C1/C2
  target scores beyond the freeze-admissibility probe; registry/census semantics.
- The `fx-a6-*` fixtures are reconstructed from the committed reconstruction, not the critic's
  destroyed scratch; the 44-line count in the record is not reproducible from surviving bytes
  (40 lines).
- `--spec r45 --profile v1` was scored with `--no-battery` for the comparison, on purpose (§4).
- Scratch `S` was removed after the receipts below were copied into this directory.

## 9. Reproduce

```sh
S=/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap; mkdir -p "$S"
export TMPDIR="$S" HYAKU_SCRATCH="$S"
python3 -I -B driver.py     # fixtures + receipts.json (round-45 counter, v1/v2, lane probes)
python3 -I -B probe2.py     # full battery stdout -> battery-full.json
python3 -I -B probe3.py     # freeze identity -> freeze-probes.json
python3 -I -B probe4.py     # lane admissibility -> lane-admissibility.json
```

Receipts in this directory: `receipts.json`, `battery-full.json`, `freeze-probes.json`,
`lane-admissibility.json`, plus `driver.py`, `probe2.py`, `probe3.py`, `probe4.py`.
