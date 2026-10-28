# C1Digest — R47-C1 clause 6 (`mutations_sha256`) at the frozen counter

Seat `C1Digest`, wave 1, round 47, lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the lane: every lane byte was read through `git show`; every write is under
`.ufo/waves/round-47/w1/C1Digest/` or the (now removed) scratch root
`/fast/scratch/hyaku/kaidoku-r47/C1Digest`. No commit, push, stage or checkout was run in the
lane. No package was installed. No subagent was dispatched.

Two revisions matter and they are not the same:

- the **brief's freeze** `5017e1f7299c3a812e87e7950148f54313dd279e` — where the block does not
  exist yet, so clause 6 is unreachable there (`block_present 0`);
- the **measured revision** `REV = 2e4ae43463aabdae707f8c8a4daa41441ad67a71` (round-47 A3) —
  where block 24 is landed and every clause, clause 6 included, is scored.

`tools/round-47/exact.py` is byte-identical at the freeze, at A1, at A2 and at `REV`:
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`. The amendments touched
`plans/round-47-claims.md` and `tools/round-47/record.py` only.

## 1. Verdict on clause 6

**Met by the landed block, and falsifiable in the ways the clause promises.** The pin at `REV` is
`mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112`, which I
re-derived twice from the frozen source (`ast` walk and `re` over the `MUTATIONS` literal), and it
equals the module's own `MUT_DIGEST`. All four mutation names appear in the block. Every digest
that is *not* `sha256("\n".join(names-in-list-order))` fails the clause, one isolated failing
entry each: three names (`K1`), sorted names (`K2`), trailing newline (`K3`). Removing the names
fails with the named list (`K4`), and `K1+K4` yields exactly those two entries (`K5`), so the two
halves of the clause are separable and jointly necessary.

Values, re-derived (details and commands in `rows.md` §2):

| value | digest |
|---|---|
| `mutations_sha256` (canonical, list order, no terminator) | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` |
| `interpreter_sha256` (`git show REV:tools/round-47/exact.py \| sha256sum`) | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| first three names — the stale pin `_m_stale_digest` plants | `b7d3e477e2f6bf3d7967a55c17dfe2d5d314c968b61e88ac4ea75e41251ac61a` |
| sorted names | `bd0aaf6e051a8ee7f58492fa8ee49ca062fb8ad3335becfe6f84ceee01425fc6` |
| trailing newline | `39af8d103e715b3ba9d853e99d749a68d3e03c47b2cb0135d6e9fef6850de1c6` |

## 2. Runs — command, exit, stdout sha256, UTC

Lane-root runs write nothing and are re-runnable as printed (`R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
`C=tools/round-47/exact.py`, all invoked from `R` with `HYAKU_SCRATCH` set):

| # | freeze | rev | exit | stdout sha256 | UTC | reading |
|---|---|---|---|---|---|---|
| e1 | `5017e1f` | `5017e1f` | 1 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` | 2026-10-28T17:54:14Z | `block_present 0`, `rule_blocks 23`, `marker_occurrences 0`; failing `["marker_occurrences 0 != 1","marker_block_count 0 != 1"]` — the brief's expectation reproduced |
| e2 | `9018c53` (A1) | `e856beb` (landing) | 1 | `219d030bf624691f4c898685492907084fff192dd0f66129d2ce42dc137196e6` | 2026-10-28T17:54:14Z | the pre-A2 rows: one failing entry, `arm cells not exact vocabulary tokens`; **both clause-6 pins already true**, battery skipped |
| e3 | `2e4ae43` | `2e4ae43` | 0 | `43cc50b19a3aea0e7e9d48f7a2e62c9ec4851948922b4b5e184630708a8481d4` | 2026-10-28T17:54:15Z | landed block: `failing []`, battery `forgeries 4 / v2 4 / v3 0 / genuine 1 / crash 0`, `refs 8` |
| e4 | `2e4ae43` | `2e4ae43` | 0 | `43cc50b19a3aea0e7e9d48f7a2e62c9ec4851948922b4b5e184630708a8481d4` | 2026-10-28T17:55:07Z | byte-identical re-run (independent invocation) |
| e5 | `62e33f7` (A2) | `2e4ae43` | 2 | `b976b39631a66635c01ee62dde7d23c8575e5628a04a78bfa5938159254ef6b7` | 2026-10-28T17:55:22Z | `reason frozen_path_changed`, `touched ["tools/round-47/record.py"]` — see finding F1 |
| P1 | `2e4ae43` | `fc2a529` (fixture) | 0 | `55cfe61f89f44175e43b2e9eb12c3e385a18d8ce6c1f2774fe4172575a02e265` | 2026-10-28T17:54:57Z | the candidate block (bare tokens + `Arms:` paragraph) green with battery |

Fixture runs live in `receipts/raw/` (`index.txt` holds the same five fields per line). The
fixture clone was `/fast/scratch/hyaku/kaidoku-r47/C1Digest/clone2`, a `git clone --no-hardlinks`
of the lane checked out at `REV`; the clone is removed, the variant block bytes are archived in
`receipts/variant-blocks/`, so each run is rebuildable by pasting a variant into `SKILL.md` and
committing it in a clone.

| # | block change | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| K1 | pin := digest over three names | 1 | `02463c813923f3fedb8eefb6615ef8152c278a21a614fea09762eb99a85ea134` | 17:54:56Z |
| K2 | pin := digest over sorted names | 1 | `33ebefa2af3b2981c3dc589e569083e005b02a3b52c1dd3b03b0e2ab1db53b74` | 17:54:56Z |
| K3 | pin := digest with trailing newline | 1 | `edd6c54860dae104340d20344554ba633521a9c95e1ec2aeca8d6dca65053885` | 17:54:57Z |
| K4 | the four names removed | 1 | `88159ec9eacb61b881f5ac54bdbd4c588a05fef5f09ae0e60d9d1a1ee7120745` | 17:54:57Z |
| K5 | K1 + K4 | 1 | `5f9c5e644dbd5a94df47c1d8e705ed5f9641fa27d7435206cb7748ed149165b1` | 17:54:57Z |
| K6 | a second, stale pin added | **0** | `090c6769d76b483153cca64d4116fb8b34a09cdf74f188c9f7f26afcf4f2d0ce` | 17:54:57Z |
| K7 | names kept, binding denied in prose | **0** | `9b1b5a5c3f7b3846dab5ac8c1fdf82883d9ff7bf18b43ae8f48aa48ab260712e` | 17:54:57Z |
| K8 | claims citation moved to lines that address another paragraph | **0** | `201899c870408c8f0a76391cb0ff8b6d1ad6c683f3209908f6e98856118530ff` | 17:55:39Z |
| K9 | the round-46 gate cited by path | 1 | `05cbf28a7ceafc182dbf879867529efcab559f614f4218515638eff2fbd8aefb` | 17:56:46Z |

Driver transcripts (their stdout sha256): `drive.out` `fd77008e5fdbea61e31dc4a90d85c71db1d2212151fd58f62caee43d802e14d6`,
`drive2.out` `5062068c1082e1cc856999c6fed8c7cf6401e0af1d5c90f208c3d77922438944`,
`drive3.out` `234947636552fd72d5398cf0e10fd95113f338fe112676887bfb94de2ac2bfba`.
The first freeze run also wrote `receipt.json` in this directory (`--json-out`); `e1` supersedes
it and is the one with a timestamp.

## 3. Findings

**F1 (HIGH — landing hazard, measured).** The freeze is now a three-commit series and each
amendment touches a frozen path, so **only a freeze equal to the last frozen-path commit
evaluates**. `--freeze 5017e1f`, `--freeze 9018c53` (A1) and `--freeze 62e33f7` (A2) all exit 2
`frozen_path_changed` at `rev 2e4ae43` (`e5`, and `R0`-`R2` in `receipts/runs2.json` from a clean
clone); `--freeze 2e4ae43` exits 0 (`e3`/`e4`). The L1's own `c1-at-A2.json` receipt
(freeze `62e33f7`, rev `62e33f7`) is therefore no longer a landing receipt for any rev at or
after A3. Any further commit touching `plans/round-47-claims.md` or `tools/round-47/` resets the
freeze again. The claims text ("a change makes both counters exit 2 `frozen_path_changed`") is
honored by `gate.py:192-194`; what is missing is a line in the claims saying *which* of the
series is the freeze as of the last amendment, and the report citing that commit.

**F2 (MEDIUM — the clause-6 subject moved).** Clause 6 sat at `plans/round-47-claims.md:78-79`
at the freeze (190 lines) and at `:99-100` at `REV` (211 lines): A1-A3 insert prose above it.
A citation that names the clause positionally will silently stop addressing it. `K8` proves the
counter does not notice: `plans/round-47-claims.md:45-113` replaced by `:45-50` (same label,
different content) still scores exit 0.

**F3 (MEDIUM — the name half is a substring test).** `exact.py:252-255` asks `n in block`.
`K7` keeps all four names and adds "the battery scores only `flag-order-drift` … the other three
are named here as unscored": exit 0. This is R46-CL3's defect class (`appears in *some* row`)
re-entering through the names half of clause 6.

**F4 (LOW-MEDIUM — first pin wins).** `MUT_PIN.search(block)` (`exact.py:247`) reads the first
`mutations_sha256:` in the block. `K6` leaves the correct pin in place and adds a stale
`b7d3e477…` under the table: exit 0. The same holds for `interpreter_sha256` (`SELF_PIN`).

**F5 (MEDIUM — the pin covers names, not mutators).** `MUT_DIGEST` is built from the names only
(`exact.py:96`). Replacing one entry with a no-op mutator leaves the digest unchanged and the
battery still reports `forgeries_total 4, v2_green 4, v3_green 0, crash 0` while the fixture
entry reads `mutation was a no-op` and `v2_green` is incremented anyway (`exact.py:351-357`):
clause 9 passes with a dead forgery (`receipts/noop-mutator.json`). What stops this is not
clause 6 but the `interpreter_sha256` pin plus the freeze and dirty arms
(`gate.py:187-194`).

**F6 (INFO — clause 5 and clause 6 pull in opposite directions).** Arm cells must be the bare
token, so the explanation of what the arm computes has nowhere to live in the cell. The landing
commit `e856beb` satisfied clause 6 and failed clause 5 on all four cells (`e2`); A2 fixed it by
deleting the explanations. The explanation can be restored outside the cells — the v2-hole cell
or an `Arms:` paragraph — and that form is measured green (`P1`, `rows.md` §4).

**F7 (INFO — the block cannot cite its clause-7 subject).** `ALLOW` (`exact.py:36`) is
`corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-47/`. Citing
`tools/round-46/gate.py:99` fails clause 8: `K9` exits 1 with
`unresolved or unvalidated citations: 1` / `tools/round-46/gate.py: outside the validated path
set`. A row's v2-hole cell must therefore describe the flag pair without writing the path.

**F8 (INFO — record note, not this claim).** `corpus/SOURCES.md` S143 (`Python re` docs) was
added by the landing and its `used-by` cell names `corpus/lessons/round-47.md`, which does not
exist at `REV` (`git show REV:corpus/lessons/round-47.md` → absent). If that lesson is not
written before the round closes, the source row points at nothing; C2's `path` class reads only
`SCORECARD.md`, so no counter would catch it.

## 4. Risks

- Every figure above is tied to `REV = 2e4ae43`. The lane advanced twice while this seat ran
  (worktree draft → `e856beb` → A1/A2/A3); a later commit that touches a frozen path moves the
  usable freeze again (F1).
- The fixture commits (`fc2a529`, `5a30d61`…`318bbb3d`) existed only in the removed scratch
  clone and are not citable revisions. The archived variant blocks plus the commands in
  `receipts/raw/index.txt` reproduce each measurement in one clone.
- `K6`-`K9` and `N1` are holes in clauses 6/8/9 of the frozen counter. I did not edit the frozen
  bytes and do not propose a fix here; they are stated with receipts so the L1 can decide whether
  a v4 arm belongs in round 48's routed defects.

## 5. What the L1 can paste

`rows.md` carries the paste-ready pieces: the pin sentence (correct as landed), the
`R46-CL4 → digest` row that clause 6 governs, the other three rows in bare-token form, the
optional `Arms:` paragraph, and the line-selector table with the file lengths it was validated
against.
