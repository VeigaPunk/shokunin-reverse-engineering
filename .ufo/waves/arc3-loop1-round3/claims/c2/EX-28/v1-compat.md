# EX-28 — v1 back-compat on the revised custody-pair tool (chain c2, executor)

Wave `arc3-loop1-round3` · 2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Task: **sums-form → MATCH-V1-PARTIAL exit 0; round-1 stanza → exit 12 + SHA256-CONTRACT 5/5**
over the tool revised in this round by EX-21 (`.ufo/gates/custody-pair/custody-pair.py`).
All evidence files sit next to this file (`ev2/`, `ev3/`, `ev/`, inputs at the top level).
Scratch: `/dev/shm/ex28-r3` (never `/tmp`). No custody path was written by this seat.

## 0. Frozen inputs (identity re-derived for this artifact)

| input | path | sha256 |
|---|---|---|
| R1 — round-1 canonical v1 receipt (CU-1) | `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt` | `b8ed19365c103a4ab355678f0fffe0db4e0011a18b441e79f38d9e80de3d0776` |
| R2 — round-2 authoritative v2 pre-pair receipt (EX-32) | `.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt` | `fa9706c6f036e882ee1fe9e8589c4aa9fa7e60de65c6eaf4e2c8ac0949eba1c9` (sidecar in tree) |
| R3 — round-3 c2 pre-pair v2 receipt | `.ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt` | `d31ece6f0d5519a476d9067a40a566ec9d2c38f2e55068435655ae039e46b0a0` (sidecar in tree) |
| sums-form under test | `v1-sums-round1.txt` (the `## compact sha256 list` block of R1, 5 rows, re-extracted) | `7b68040bb548bdf43604ca6c3e677906b09277d8e4200c4d35279d5aecbaaf6b` |
| live-pinned sums form | `v1-sums-live.txt` (5 rows, live sha of 13:06Z) | `6f502174192d488fe8f8dd2812d7104ef4a831b2aef96cd2502a9936c46181b2` |

All digests in this table were re-derived at hand-off; the full file inventory is in `MANIFEST.sha256` (see §9).

## 1. Tool revision timeline (the target moved under this seat)

| revision sha256 | bytes | lines | mtime (local -03) | note |
|---|---|---|---|---|
| `112d01dc…` | 39157 | 889 | 2026-10-19 09:05:19 | round-2 revision (VZ-3 verdict revision) |
| `68e30768…`, `d164d49f…`, `460a01f0…` | 39187–42234 | 918–946 | 10:08:4x–10:09:1x | EX-21 mid-flight edits |
| `b9bd55e9… …57dffff1…` | — | — | 10:09:24–10:11:16 | 8 further edits, see `gate-revision-timeline.txt` |
| **`03bd6242470ac8d27ea832af6bcb71049ccfad92f2ba8c878b30f51b5211bd83`** | **51868** | **1109** | **10:11:16.364** | **measured revision** — stable 10:11:16→13:12:25Z (11 poll checks) |
| `73c15b84…` → `89bfebec4396e2e62a4409aee6587ffac5366b9988ee97463d20ff75e881a1e0` | 51907 / 51937 | — | 10:12:40 / 10:12:44 | post-measurement edits; spot-check in §7 |

Poll log (sha + mtime per check, 20 s cadence): `gate-revision-timeline.txt`.
Snapshots of each measured revision are preserved by sha under `/dev/shm/ex28-r3/snap/<sha>/custody-pair.py`
and their digests recorded in `gate-snapshots.sha256`. Every transcript header names its revision.

## 2. Frozen claim 1 — sums-form ⇒ MATCH-V1-PARTIAL, exit 0 — **HOLDS**

Input A = `v1-sums-round1.txt` (5 rows, round-1 pins), B = the candidate.

| comparison | A | B | result | exit |
|---|---|---|---|---|
| frozen/frozen (pre-drift) | sums-v1 | R2 (v2) | `MATCH-V1-PARTIAL  compared=1/11` ×5, `SHA256-CONTRACT: 5/5`, `VERDICT: MATCH-V1-PARTIAL paths=5` | **0** |
| live-pinned/live | `v1-sums-live.txt` | live | `MATCH-V1-PARTIAL` ×5, `SHA256-CONTRACT: 5/5` | **0** |
| round-1 pins/live (post-drift, §3) | sums-v1 | live | 4× `MATCH-V1-PARTIAL` + 1× `CONTENT-DRIFT moved=sha256`, `SHA256-CONTRACT: 4/5` | 10 |

Transcripts: `ev2/core-sums-frozen.txt`, `ev2/core-sums-livelive.txt`, `ev2/core-sums-live.txt`.
The exit-0 clause is a property of *agreeing* sha pins; the exit-10 row is the live content drift of §3, not a v1 regression.

## 3. Frozen claim 2 — round-1 stanza ⇒ exit 12 + SHA256-CONTRACT 5/5 — **HOLDS (against a pre-drift candidate)**

`ev2/core-stanza-frozen.txt` (A = R1, B = R2):

```
PATH /home/vgpnk/.config/devin/mcp_config.json: METADATA-DRIFT  compared=5/11
    LABEL-DEFECT: MTIME_UTC says '2026-10-14 17:53:20' = localtime(epoch 1792011200); gmtime(epoch) is '2026-10-14 20:53:20'
... (5× LABEL-DEFECT, one per path; kimi stanza: '2026-10-18 23:20:43' vs 2026-10-19 02:20:43)
SHA256-CONTRACT: 5/5 paths agree on sha256 (v1/v2 receipts compare on this field)
VERDICT: METADATA-DRIFT  paths=5  METADATA-DRIFT=5  exit=12
```

Both frozen numbers reproduce **exactly** at revision `03bd6242` and at `112d01dc` (round-2 revision) —
the header line there reads `CUSTODY-PAIR VERIFY (v2 instrument)` and the class map is unchanged.

### 3a. The live-mode delta — a real custody event between the rounds

`~/.kimi-code/config.toml` was rewritten **between round-2's last capture and round-3's dispatch**:

| field | round-2 pins (R2, 12:04:06Z) | live (13:06Z→) |
|---|---|---|
| sha256 | `8cbacd48ab85ea86e122bae102d8ee63e2fd3181aa551603b3923b912573c38d` | `bc66d543018eddb1b74c6057f6873e014f25d0a4fc1bc13c0ff6d3a63c86ddc3` |
| inode | 34530637 | 37793921 |
| mode | 600 | 644 |
| mtime/ctime | 1792376443 = 2026-10-19T02:20:43Z | 1792414665 = **2026-10-19T12:57:45Z** |

Angle cache is the only path that moved (other 4 paths byte-identical since round 1). Consequences:

* `verify R1 --live` → `CONTENT-DRIFT` on the kimi path + 4× `METADATA-DRIFT/LABEL-DEFECT`, **exit 10, SHA256-CONTRACT 4/5** (`ev2/core-stanza-live.txt`)
* `verify R1 R3` → same shape, exit 10, 4/5 (`ev2/core-r1-vs-r3receipt.txt`)
* `verify R3 --live` → `MATCH 5/5 exit 0` (`ev2/core-r3receipt-live.txt`) — custody is stable *after* the event, so round-3's live pre/post pair is capturable from the R3 baseline
* Writer attribution (read-only evidence): the rewrite left **no** `.bak` sidecar (the kimi CLI writer emitted `config.toml.YYYYMMDD-HHMMSS.bak` for every one of its 7 October rewrites — round-1 `adjacent-hashes-pre.txt`) and **no** `~/.kimi-code/file-history/` entry (that dir holds only `wd_*` entries) → the write came from the CLI process config-save path, not from an agent edit tool. Exact writer not established; the event predates round-3's dispatch (wave dir created 13:03Z).

**Round-crossing lesson for the C2 claim**: "the round's live pre/post pair verifies MATCH 5/5" must be captured **from the R3 baseline onward** — any comparison against round-1/round-2 pins now reads exit 10 by design.

## 4. Revised-tool matrix at `03bd6242` (24 runs, all transcripts in `ev2/`)

| # | run | exit | class |
|---|---|---|---|
| 1 | `verify v1-sums-round1.txt R2` | **0** | MATCH-V1-PARTIAL 5/5 |
| 2 | `verify R1 R2` | **12** | METADATA-DRIFT (5× LABEL-DEFECT), SHA256-CONTRACT 5/5 |
| 3 | `verify v1-sums-round1.txt --live` | 10 | CONTENT-DRIFT(kimi) + 4× V1-PARTIAL, 4/5 |
| 4 | `verify R1 --live` | 10 | CONTENT-DRIFT(kimi) + 4× METADATA-DRIFT |
| 5 | `verify v1-sums-live.txt --live` | **0** | MATCH-V1-PARTIAL 5/5 |
| 6 | `verify R1 R3` | 10 | CONTENT-DRIFT + 4× METADATA-DRIFT |
| 7 | `verify R3 --live` | **0** | MATCH 5/5 |
| 8–16 | attack battery (see §5) | various | see §5 |
| 17 | `selftest --scratch <dir>` | **0** | `CLEAN cases=21 passed=21 failed=0` (v1 cases 11–13 PASS) |
| 18 | `selftest --scratch <missing dir>` | **2** | `USAGE: scratch base is not a directory: …` (D6 closed) |
| 19 | `verify sums-1of5.txt --live --require-paths 5` | **2** | `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: …` (D3 closed) |
| 20 | `verify --help` | 0 | `--require-paths N` wired |

## 5. Attacks attempted, with verdicts

| attack | fixture | measured | verdict |
|---|---|---|---|
| A1 — 1-of-5 reference as a silent pass (D3 surface, no flag) | `sums-1of5.txt` | `MATCH-V1-PARTIAL 1/1`, exit 0 | **hole is opt-in-only**: unchanged without the flag; **closed by `--require-paths`** (A1r → exit 2 + coverage line). Residual: the gate is opt-in, so any consumer that does not pass the flag still reads a 1-of-5 receipt as 0 |
| A1r — 1-of-5 + `--require-paths 5` | same | `REFERENCE-COVERAGE: 1/5`, exit 2 | **fail-closed** |
| A2 — reference with zero parseable rows | `sums-empty.txt` | `USAGE: unparsable receipt …`, exit 2 | correct, unchanged |
| A3 — v1 stanza carrying `EXISTS: no` for a nonexistent path | `stanza-exists-no.txt` | `MATCH  compared=0/11`, `SHA256-CONTRACT: 0/0`, exit 0 | synthetic both-absent MATCH is *not* the round-2 D2 defect (no EACCES involved); the real EACCES path is now `UNEVALUABLE` exit 14 (selftest cases 16–17) |
| A4 — one stanza's `SHA256:` line stripped | `stanza-no-kimi-sha-live.txt` | kimi path `METADATA-DRIFT moved=mode` (content drift masked, mode caught it), `SHA256-CONTRACT: 4/4`, exit 12 | **residual** — see §8/1 |
| A4b — v1 stanza that omits `SHA256:` entirely, content then swapped same-size/same-mode | `fix/v1-stanza-no-sha.txt` | before exit 0; after content swap **exit 0**, `MATCH-V1-PARTIAL`, `SHA256-CONTRACT: 0/0` | **silent content-blindness on the v1 surface** when the field is absent — see §8/1 |
| A5 — `sha256sum --binary` marker `*/path` | `sums-binary-marker.txt` | path key `*/home/…` → `ABSENT`, exit 13 | **fail-closed but misclassified** (GNU `-b` form is not path-normalized) |
| A6 — `./` / `~` path spellings | `sums-dotpath.txt`, `sums-tilde.txt` | `ABSENT` + `EXTRA-PATH`, exit 13 | **fail-closed but misclassified** (exact-string path identity; pathlib normalizes only the live side) |
| A7 — uppercase hex digest | `sums-upper.txt` | `MATCH-V1-PARTIAL`, exit 0 | accepted (case-insensitive), correct |
| A8 — single-space / tab separator, CRLF, no final newline | `sums-1space/tab/crlf/nonl` | `MATCH-V1-PARTIAL`, exit 0 each | robust |
| A9 — duplicate rows, tampered sha first then correct | `sums-dup-rev.txt` | `MATCH-V1-PARTIAL 1/1`, exit 0 | **ambiguity silently resolved (last row wins)**; with the tampered row last it reads exit 10 (`sums-dup.txt`) |
| A10 — pipe-v1 round-1 metadata file (bonus shape) | `config-pre-pair-metadata.txt` vs R2 | `METADATA-DRIFT` 5×, `SHA256-CONTRACT: 5/5`, exit 12 | third v1 shape also cross-round-verifiable |

## 6. What is *not* claimed

* These measurements are at revision `03bd6242` (spot-checked at `89bfebec` and `7cd19c3c`); the gate file
  was rewritten ≥14 times during this seat. Rule #14: **re-derive at landing** with §9.
* No statement about D1 (capture TOCTOU), D4/D5, or the hardlink arm — other c2 seats own those.
* The exit-10 rows are *correct* tool behaviour over a changed live filesystem, not tool defects.

## 7. Spot-checks after the measured revision (the target kept moving)

`89bfebec…` (13:12:44Z, 51,937 B) — `ev3/`: sums-frozen **0**, stanza-frozen **12** (+`SHA256-CONTRACT 5/5`),
sums-live/live **0**, stanza-live 10, 1-of-5+`--require-paths` **2** with the coverage line → v1 surface unchanged.
**But** `selftest` read `DIRTY cases=21 passed=20 failed=1 exit=3`:
`case require-paths-blocks-partial-reference FAIL (TypeError: _run_verify() got an unexpected keyword argument 'require_paths')`
(`ev3/selftest.txt`) — the same edit had not updated the helper signature. It PASSED at `03bd6242`
(`ev2/selftest.txt`, case 17). Flagged to the implementer in the seat report as a mid-flight regression.

`7cd19c3c…` (13:13:20Z, 54,279 B) — re-run end-to-end with `rerun-v1-compat.sh` (scratch
`/dev/shm/ex28-rerun-test`): the full battery reproduces the §4/§5 rows exactly (frozen pair **0 / 12**,
R1-vs-R3 **10**, R3-vs-live **0**, R1-vs-live **10**, 1-of-5+`--require-paths` **2** + `REFERENCE-COVERAGE: 1/5`,
D6 probe **2**, all thirteen attack fixtures unchanged), and `selftest` now reads
`CLEAN cases=22 passed=22 failed=0 exit=0` → the transient DIRTY at `89bfebec` is gone, and the round's
"selftest 15 → ≥17 at exit 0" clause holds at `7cd19c3c`. (Note for the recipe: `rerun-v1-compat.sh`'s
`--require-paths wired` line at `7cd19c3c` was a false negative of this seat's own regex — the flag is wired:
`verify --help` lists `--require-paths N`, and the run above prints the coverage line. The script's check has
been fixed.)

## 8. Proposed changes (patch text: `proposed-contract-denominator.patch.md`)

1. **Contract denominator on the v1 surface.** `SHA256-CONTRACT: n/m` counts *pairs present on both sides*,
   so a v1 reference that omits a `SHA256:` field shrinks the denominator (4/4, 0/0) and can read like full
   agreement while content was never compared (A4b: swap invisible, exit 0). Proposal: print the contract
   against the reference's stanza count as well — `SHA256-CONTRACT: 4/5 paths agree on sha256 (1 reference
   stanza omits SHA256)` — and emit an `OMITTED-SHA256: <path>` finding (class METADATA-DRIFT) so a v1
   receipt cannot silently reduce its own field set. Companion flag: `--require-sha N`.
2. **Ambiguous duplicates (A9).** `parse_receipt` keeps the last row per path (dict overwrite). Proposal:
   a `DUPLICATE-PATH: <path>` note + worst-case merge (or exit 2 USAGE) instead of silent last-wins.
3. **Path-string forms (A5/A6).** `*/path`, `./path`, `~/path` fail *closed* but as `ABSENT`, which reads as a
   custody event. Proposal: normalize (expanduser/strip the binary marker) at parse time, or emit
   `PATH-FORM: <raw>` as a note on the ABSENT row so the class is not mistaken for a disappearance.

## 9. Re-derivation recipe (rule #14)

```bash
cd /dev/shm && rm -rf ex28-rerun && mkdir ex28-rerun && cd ex28-rerun
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/EX-28
bash "$D/rerun-v1-compat.sh" /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py
```

`rerun-v1-compat.sh` pins the tool by sha into a scratch snapshot, replays the frozen pair and the attack
battery, runs `selftest`, and prints a revision-labelled summary. Identities of this artifact’s files are in
`MANIFEST.sha256`; the artifact digest is in `v1-compat.md.sha256`, re-derived after the last write.