# ScribeRegistryRows — routed defect 3: SKILL.md gate registry rows (rounds 27–28)

Scope: draft one registry block, in the round-22/23/24 measurement-registry shape, covering the
two round-27 counters and the two round-28 counters. Deliverable is the draft text plus the line
it belongs after; the L1 integrates.

## Placement

The block belongs after SKILL.md line 946 — the last line of the file at the observed tip
(`cae73c4966763103a7d67deca7a7f67322715a59`; the same tail held at the earlier observed tip
`9db24c9e10287d44d9f780d782ab608f3c84ff5a`). That line is the final bullet of
`### Round-27 falsify-wave corrections to the section above (appended)`. SKILL.md is append-only
by round; rounds 26–28 have no registry, so appending at the file tail keeps chronological order.
The block uses a `###` heading so it nests under the last `##` section (round 27), matching the
`### Round-N measurement registry` convention at SKILL.md:679, :731, :770 (round 25's row is a
bare table at :804-806 inside its own `##` section).

Confirmed absent: `grep -n 'c1-rename-identity\|c2-xpin-check\|c1-heldout-naming\|c2-filtered-flag'
SKILL.md` prints only this line's absence — no existing rows for these four tools.

## Draft block

```markdown
### Round-27/28 measurement registry

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round27-C1 | gate / kaidoku | `python3 -I -B tools/round-27/c1-rename-identity.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 rows_complete=16/16 and entry_ok=1, 1 otherwise (each incomplete pair prints INCOMPLETE with reasons), 2 input error. Reads Git objects at --rev only; per row, base/repeat/renamed envelopes re-derive the verdict (unstable if base != repeat, content-keyed if renamed == base, else rename-sensitive) | `python3 -I -B tools/round-27/c1-rename-identity.py --selftest` (no --root/--rev): builds a green fixture plus 21 red mutations as private scratch repos, 22 cases; 0 all pass, 1 any failure. Green at tip (selftest cases=22 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-27/before/c1-selftest.txt` | Counter sha256 e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7 (`.ufo/waves/round-27/claims.json` instruments; unchanged since freeze commit a4f674b3). Frozen carriers jq e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806, tinyxxd 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65; package pin 6.5.0 + package.json sha256 a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Loads `tools/round-26/recompute-ids.py` at REV unpinned (INSTRUMENT_UNPINNED, routed defect 4). Refuses runs started or files first committed before the counter commit. Git reads only; selftest writes removed scratch clones |
| round27-C2 | gate / kaidoku | `python3 -I -B tools/round-27/c2-xpin-check.py --root <LANE> --rev <REV> [--base <BASE>] [--tool-cmd <CMD>]`; 0 r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1, 1 otherwise, 2 input error (including changed or missing installed package files it verifies). Runs the tool under node on the 24 round-26 envelopes plus 3 generated red envelopes; recomputes both pins independently (6.5.0 rule via `tools/round-26/recompute-ids.py`, 6.7.0 rule from the installed package) | `python3 -I -B tools/round-27/c2-xpin-check.py --selftest`: 4 stub-mode cases + tool-absent-at-base + capability/source rows fixture, 6 cases; 0 all pass, 1 any failure. **Red at tip**: `correct-stub` expects exit 1 but measure now returns 0 once the capability and source rows exist (selftest cases=6 failures=1, exit 1, 2026-10-22T18:28Z; routed defect 2 — re-anchor pending, seat ExecR27SelftestFix). Freeze receipt `.ufo/waves/round-27/before/c2-selftest.txt` was green (6 cases, 0 failures) | Counter sha256 d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3 (`.ufo/waves/round-27/claims.json` instruments). FROZEN_FILES pin installed package bytes: 6.5.0 package.json a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c, 6.5.0 dist/domain/evidence.js f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff, 6.7.0 package.json 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570, 6.7.0 dist/domain/evidence.js a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb. Git reads only; tool runs in a private scratch dir, no lane writes |
| round28-C1 | gate / kaidoku | `python3 -I -B tools/round-28/c1-heldout-naming.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 runs_ok=61/61 rows_complete=187/187 tally_equal=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 a pinned input absent or differing. Reads Git objects at --rev only, never network or REA. Also `--emit-tally` (recompute the tally from the working tree; L1 use, not a verdict). Byte-identical lookup bodies across selectors are legitimate: responses are keyed by manifest entry, not by bytes | `python3 -I -B tools/round-28/c1-heldout-naming.py --selftest`: 19 listed cases + planted-wrong-name check + pin refusal, 21 cases in private temp repos; 0 all pass, 1 any failure. Green at tip (selftest cases=21 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-28/before/c1-selftest.txt` | Counter sha256 29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c (`.ufo/waves/round-28/claims.json` instruments). Every input it loads is pinned in PINS and `loaded_by_counter`: resolver `tools/round-25/a2/resolve-selectors.py` 4be915668ea20a643d04c9b8ae3c83bc9f5fd1b4d8821e06cabdccce36b3c23d, `corpus/evidence/round-28/c1/carriers.tsv` 4392b5c377cc2e343d385ba3b93206a0bb67df972bdc3814780819f1d4c5e71f, `heldout.tsv` 423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef; package pin 6.5.0 + a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c. Refuses runs/lookups from before the counter commit. Git reads only; selftest writes private temp dirs |
| round28-C2 | gate / kaidoku | `python3 -I -B tools/round-28/c2-filtered-flag.py --root <LANE> --rev <REV> [--base <BASE>]`; 0 responses_complete=230/230 entries>=1 mismatches=0 predicted_true>=1 entry_ok=1, 1 otherwise (FAIL reasons listed), 2 pin failure. Reads Git objects at --rev only; a non-boolean `filtered` counts as a mismatch and both branches must be exercised | `python3 -I -B tools/round-28/c2-filtered-flag.py --selftest`: 16 listed cases + pin refusal, 17 cases in private temp repos; 0 all pass, 1 any failure. Green at tip (selftest cases=17 failures=0, exit 0, 2026-10-22T18:28Z); freeze receipt `.ufo/waves/round-28/before/c2-selftest.txt` | Counter sha256 4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef (`.ufo/waves/round-28/claims-c2.json` instruments). Pinned inputs: `corpus/evidence/round-28/c2/selectors.tsv` ad1b50982922ed69f6953b490716746adb5d5587c4395d29489b1db7fab464ae, `canonical-signatures.json` 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2 (`loaded_by_counter`). Refuses responses fetched or files first committed before the counter commit. Git reads only; selftest writes private temp dirs |
```

## Evidence

- `sha256sum` on the four tools at tip (worktree) matched the frozen pins exactly:
  c1-rename-identity e0a07995…, c2-xpin-check d8de667f… (round-27 `claims.json` instruments);
  c1-heldout-naming 29c2b571…, c2-filtered-flag 4fdf7db8… (round-28 `claims.json` / `claims-c2.json`
  instruments). `git log` per tool shows one commit each (a4f674b3, a4f674b3, 87d3dfb6, 86fa8526)
  — all four byte-identical to their freeze, no supersessions.
- Selftest runs, `python3 -I -B <tool> --selftest`, TMPDIR in my seat scratch, 2026-10-22T18:28Z:
  r27-C1 exit 0 `selftest cases=22 failures=0`; r27-C2 exit 1 `selftest cases=6 failures=1`
  (`FAIL correct-stub: exit 0, expects 'r26_rows_ok=24/24 red_ok=3/3'` — measure returns 0 because
  capability_row=1 source_row=1 at HEAD); r28-C1 exit 0 `cases=21 failures=0`; r28-C2 exit 0
  `cases=17 failures=0`. Case counts agree with the freezes (21 and 17 named in claims files).
- Case-count derivations read from source: r27-C1 `len(cases)`=22; r27-C2 `len(cases)+2`=6;
  r28-C1 `len(cases)+2`=21; r28-C2 `len(cases)+1`=17.
- Verdict maps read from each tool's main/run function: r27 counters return 0/1, exit 2 on
  InputError (and argparse usage error); r28 counters return 0/1, exit 2 on PinError.
- Freeze receipts `.ufo/waves/round-{27,28}/before/c{1,2}-selftest.txt` each end `failures=0`, exit 0.

## Observations / limits

- Observation: the r27-C2 selftest is red at the tip (routed defect 2 still open; sibling
  ExecR27SelftestFix owns the re-anchor). The row states this so the registry is not stale
  if the fix lands; L1 may update that cell after the fix.
- Observation: the lane tip advanced during this seat's work (9db24c9e -> cae73c49); the SKILL.md
  tail (line 946) and all four tool bytes were unchanged across both tips.
- Out of scope: no lane edit performed; no installs; `tools/round-28/collect-*.py` and
  `select-heldout.py` are producers, not counters, so they are not registry rows (they are named
  in `producers_not_counters` if the L1 wants them).
- Unknown: whether the L1 prefers two separate `### Round-27`/`### Round-28` tables; the block is
  one table per the assignment's "one registry block".

Report: .ufo/waves/round-28/a2w/ScribeRegistryRows.md
