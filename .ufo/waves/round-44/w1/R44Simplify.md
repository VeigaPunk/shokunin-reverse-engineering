# R44Simplify — YAGNI review of the round-44 surface

Seat R44Simplify. Base `c29360e3ba5381a5ab69e372d0d9577970f85018`.
Reviewed: `plans/round-44-claims.md` as it stands now (337 lines, md5
`fe309a6bd28d6c275dbbccb38da98844`) and every draft under
`.ufo/waves/round-44/w1/artifacts/`. `tools/round-44/` does not exist yet, so the "drafted tools"
are the pre-install artifacts named below; nothing here was verified against an installed tree.

The draft moved twice while this review ran (carriers 4 → 6; then C2 narrowed from six categories
to three named assertions). Findings are keyed to the current text. One early finding — the v2.1
oracle trees were orphan bytes with no carrier — is **closed by amendment 1** and is recorded as
verified rather than flagged.

## Axes

1. **Predicate necessity** — every frozen path, tool and counter arm must be consumed by a
   predicate clause or by a control at `REV`. A frozen path nothing reads can only produce a false
   `frozen_path_changed` (exit 2), never a correct score.
2. **Single authority** — one parser / pin table / loader per fact. Where copies disagree (they
   do: S2) the second copy is also a correctness hazard.
3. **Landing consequence** — every frozen rubric entry must be able to change between BASE and REV
   and be repairable by an honest text repair. An entry that is green at its own pin, or that no
   permitted repair can satisfy, is dead rubric weight that drives a wrong repair.

## Gate A — the 5th carrier question (asked by the seat spec)

**A bare `squashfs_v3_broadcom` fixture is scope creep and was correctly dropped.** Four measured
grounds:

- **Handler unit.** P44-C1 binds each carrier's handler family by exact equality to
  `squashfs_v1` / `squashfs_v2` (`plans/round-44-claims.md:124`). `squashfs_v3_broadcom` is a
  different handler name; a v3bc carrier cannot bind under this predicate at all.
- **No coverage movement.** `squashfs_v3` + `squashfs_v3_ddwrt` are already Core (`PROVINCE.md:414`);
  `squashfs_v3_broadcom` is named Frontier by PROVINCE and by the claim's own disclosed-limits line.
  Adding it would be a second, undeclared Frontier→Core move.
- **No oracle under this claim's rule.** `/usr/bin/unsquashfs -lls` on
  `corpus/evidence/round-42/c2/fixtures/v3bc-le--squashfs_v3_le.bin` →
  `FATAL ERROR: Can't find a valid SQUASHFS superblock`, rc=1. (7z 26.04 does list 2 members, so a
  second-reader oracle exists — but this claim's oracle binding is the unsquashfs census frozen in
  `carriers.json`, and mixing producers would need its own binding.)
- **Fixture identity is not an independent set.** Only `v3bc-le` is committed (no BE partner), and
  `tools/round-42/fixtures.json`'s `duplicate_bytes` rows name `v3bc-be` / `v3ddwrt-le` — files
  that are not in the committed fixture dir.

The frozen target is the six carriers in `carriers.json` (`carriers_matched == 6`,
`plans/round-44-claims.md:158`); a 7th id would move the target, the oracle, the control set and
the do-nothing baseline. **Drop confirmed.**

**The 4 → 6 amendment is a different case and should stay.** The two added carriers are
`squashfs_v2.1` LE/BE: same handler family, same oracle tool, same MIT fixture set, and their
oracle trees were already fetched. Verified, not assumed — for each of the six:

```
unsquashfs -d <scratch>/<id> -f <carrier>
diff -r <scratch>/<id> corpus/evidence/round-44/oracle/<fam>/<endian>/__output__/<...>.bin_extract
  → clean for v1.0_le, v1.0_be, v2.0_le, v2.0_be, v2.1_le, v2.1_be
```

All 22 committed oracle files map onto the six carriers, so **no orphan oracle path remains** —
the seat's "oracle path for a carrier not frozen" example is closed, not illustrated.

## Gate B — C2 spec: one contradiction to fix before the freeze

The narrowed C2 is a real, repairable calibration claim. I re-derived its three named mismatches at
base and they hold:

| asserted (Owned axes) | at base | verdict |
|---|---|---|
| coverage `133/133 knowledge files mapped` (leading figure) | 137 knowledge files | stale |
| depth `20/20 queue-drain rule blocks` (leading figure) | 21 rule blocks | stale |
| craft section `SKILL.md:81-449` | section is lines **81-543** (last non-blank), 21 blocks | stale range |

(The `81-543` figure in the claim text is correct — 544-546 are blank lines before the next
heading. The range still *resolves*, so a `line <= file length` check would pass it; the check must
assert the section's actual end.)

**The contradiction.** The rubric rule says "`pin_rev` is extracted from the same base line
(`at \`<hex>\``); a pinned entry is checked ONLY at its pin … a REV-state entry only when the line
carries no rev qualifier." All three asserted values live on lines that *do* carry `at \`e1c83313\``
tokens, and all three are **true at that pin** (133 files at `e1c83313`; 20 rule blocks at
`e1c83313`; `SKILL.md:81-449` resolves there). Under the stated rule all three are pinned → green →
`mismatches == 0` → **C2 would honest-stop on its own entries**, contradicting the surface
sentence that names them as the mismatches. Fix (one sentence): `pin_rev` is set only when the
*asserted substring* is revision-scoped in the text (inside the pinned parenthetical); the leading
Owned-axes figure is current-state and carries `pin_rev: null`. The parenthetical historical values
(`133/133`, `130/130`, `20/20`, `19/19`) stay pinned and are never rewritten — that half of the
amendment is already right.

**Do not promote the dev rubric.** `R44C2Counter/dev-rubric.json` (4 entries) is the arm that made
the earlier false positives, and three of its four checks still mis-scope:

- `dev-scorecard-map-count` reads the *first* `N/M knowledge files mapped` token and compares it to
  the REV file count — a pinned historical value compared to current state (the false positive this
  amendment fixes at claim level, still live in the dev file).
- `dev-readme-map-coverage` scans the whole README for `2026-…` stems and reports 11 **lesson**
  stems as `dangling`; command A scopes to the `## Coverage map` section and compares knowledge
  stems, where base is `mapped 137/137, missing [], dangling []`.
- `dev-shonen-path-line` resolves refs against the working tree (`pathlib.Path(path).exists()`)
  instead of `git show <REV>:<path>`, and ignores revision qualifiers.

If any of these shapes reaches `tools/round-44/c2-rubric.json`, CTL-C2-0's mismatch count is not
ground and a "repair" would falsify a correct statement.

## Deletion candidates, ranked (smallest deletable set)

Each names the exact edit. Line numbers are the current claims text.

**S1. Duplicate rubric parsers — `c2-counter.py` ↔ `c2-controls.py`.** `c2-counter.py:146-155`
declares ~45 alias keys (`ENTRY_LIST_KEYS` 5, `ID_KEYS` 5, `CHECK_KEYS` 5, `COMMAND_KEYS` 6,
`ASSERT_KEYS` 5, `COMPARE_KEYS` 3, `OBSERVED_KEYS` 6, `FILE_KEYS` 4, `FILES_KEYS` 3, `EDIT_KEYS` 3)
for a rubric the L1 writes once to a known schema (`{id, file, line_at_base, line_sha256, asserted,
check…}`, claims:212-214). `c2-controls.py` re-implements the same discovery independently (`pick`,
`rubric_entries`, `entry_candidates`, lines 227-303) rather than invoking the frozen counter and
reading its JSON. Fix: drop the aliases to the frozen schema; make the control call the counter.
This also strengthens CTL-C2-2 — a tolerant parser can accept a malformed rubric that must exit 2.

**S2. `c1-oracle.py`'s hardcoded `CARRIERS` fallback (4 entries) vs a 6-carrier `carriers.json`.**
`c1-oracle.py:110-155` lists `v1-le, v1-be, v2-le, v2-be`; the claim's table has six. Any
`--carriers`-less run silently builds a 4-carrier oracle — a second pin authority that is already
wrong. Fix: delete the fallback and require `--carriers`.

**S3. `gap-rule.json` (claims:306).** Amendment 5 replaced the rule with `gaps == []` and
`unpublished_entries == []` because all six carriers have **zero** non-regular members. Measured:
`unsquashfs -lls` on each carrier lists the root directory plus 3-4 regular files, nothing else. A
per-kind `allowed`/`required`/`removed` table can never be consulted. Fix: delete the file and the
per-kind arms; the boolean plus the frozen member census in `carriers.json` is the whole rule. (The
"shown able to fail" witness for this area is CTL-C1-5's mutated superbytes, not a gap table.)

**S4. The `prior-pins.json` arm (claims:306).** The arm refuses a carrier whose bytes a prior round
already scored. Measured: `prior-pins.json` holds 14 pins and **none** of the six carrier sha256s is
among them (the four v1/v2.0 bytes were round-42 C2 *held-out inputs*, never a C1 carrier). The
relabel risk it would cover is already covered by CTL-C1-4 (byte-identical envelope refusal +
`output_directory` provenance). The arm has no reachable failure mode at REV. Fix: drop the arm and
the file from the frozen set, or name the control that proves it can red.

**S5. Two audit-only counter freezes (claims:309-310).** `tools/round-42/c1-counter.py` and
`tools/round-43/c1-counter.py` are frozen "audit-only"; no counter reads either at REV, and the
port's bytes are frozen under `tools/round-44/`. Their only REV effect is an exit-2 false red if
someone touches a prior round's file. Fix: record `port_source_sha256` and
`freeze_walk_source_sha256` inside `carriers.json` (data → exit 1 when wrong) and drop both freeze
entries.

**S6. `tools/round-39/gen-squashfs.py` conditional freeze (claims:318).** "Only if CTL-C1-2's
fabricator calls it." It cannot: measured, it emits SquashFS **4.0** only (213-byte image; `file` →
"version 4.0"; superblock major reads 0 at offset 28). CTL-C1-2 fabricates a JSON envelope from the
oracle; no image is built. Fix: delete the conditional entry; a conditional freeze is unfalsifiable
by construction.

**S7. `tools/round-42/fixtures.json` freeze (claims:309).** Read by two **wave-1 seat checks**
(`R44ConnRouted/routed-checks.py`, `R44ScoutSkill/checks.sh`) and by no counter, control or rubric;
`c1-oracle.py` mentions it only in a comment. Its `duplicate_bytes` rows name files that are not
committed (Gate A). Fix: drop from frozen paths; the six pins live in `carriers.json`.

**S8. `tools/round-27/xpin-attribute.mjs` frozen twice (claims:308).** "audit-only if vendored"
while the vendored copy under `tools/round-44/` is frozen too — two copies of one instrument. Fix:
freeze only the vendored copy, binding its sha256 in `carriers.json`.

**S9. `c1-extra.py` (claims:307, "ported").** No predicate names it, no seat prompt asks for it, no
draft exists (`artifacts/R44C1*` contains oracle/run only). Round-42's `c1-extra.py` was a separate
extra-claims counter; round 44 has no second predicate. Fix: delete the name.

**S10. `SKILL.md` whole-file byte-freeze (claims:319) — redundant with the model used for the other
self-assessment surfaces.** SCORECARD/SHONEN/README are correctly BASE-pinned with cited lines bound
by `line_sha256`; that already detects registry-row drift and permits honest appends. Freezing all
of SKILL.md adds only an exit-2 surface (an unrelated SKILL edit reds both claims) and it also
blocks the very craft-range repair C2 now claims. Fix: move SKILL.md to the BASE-pinned list, or
state why it is the one self-assessment file that must be immutable.

**S11. Receipt-writer duplication.** The contract fixes one receipt shape (seat, command, exit code,
stdout sha256, wall time). This wave already has `R44Assim/receipt.py` (41 lines) and
`R44EntryDraft/receipt.py` (216 lines), plus per-tool `receipt()` functions inside the counter and
controls, against the lane precedent `tools/round-43/receipt-wrap.py` (127 lines). Fix: one frozen
receipt writer, seat name as a parameter.

**S12. `c1-run.py` duplicates the carrier schema.** `load_carriers` exists in both
`R44C1Run/c1-run.py:136` and `R44C1Oracle/c1-oracle.py:518`, each with its own pin handling: two
readers of one frozen file. Fix: one loader.

### Two freeze-time consistency fixes found on the way

- **`c1-run.sh` has no producer.** The claim's data procedure and frozen list name
  `tools/round-44/c1-run.sh` (claims:162, 307); the draft is `c1-run.py` (682 lines). Rename, or
  make the claim name the frozen file.
- **`corpus/SOURCES.md` is listed twice with opposite rules** — byte-frozen (claims:319) and
  "NOT frozen — BASE-pinned … for C2 only" (claims:324). A counter can implement only one. Keep
  byte-frozen (C1 lands S138/S139 in the freeze commit) and delete the second occurrence.

## Checked and kept — load-bearing, do not delete

- The six carrier `.bin`s, `corpus/evidence/round-44/oracle/**` (now 1:1 with carriers), and the
  oracle rows frozen in `carriers.json` — the only provenance for the publication binding.
- `corpus/evidence/round-42/c1/**` (CTL-C1-1 v3 receipts) and
  `corpus/evidence/round-42/c2/heldout/{H41,H43,H44,H45}` + `corpus/evidence/round-43/c1/heldout/H41`
  (CTL-C1-4 relabel inputs) — verified present; the four r42 entries are exactly the `legacy-*`
  envelopes, so the control has real inputs.
- `rea-pkg.json` and the vendored `xpin-attribute.mjs` — the evidence-id recompute clause;
  `c1-run`'s `extract-env.json` / `run.json` — CTL-C1-3 needs the captured child PATH.
- `c1-oracle.py` as a **pre-freeze builder** (1092 lines): its post-freeze role is audit only. If
  the L1 wants the smallest frozen set it can live outside `tools/round-44/` and be cited by
  receipt; recommended to keep, because it is the only way to rebuild the oracle rows. Tradeoff
  stated, not a deletion.

## Note on amendment 11 (`cmp -l`)

The hazard reproduces, but not under the condition the text states — and a wave-2 critic will
re-run it the obvious way:

```
/usr/bin/cmp -l a b >/dev/null      rc=1   (differing 4096-byte files)
/usr/bin/cmp -l a b                 rc=0   (same files, output to a pipe/tty/regular file)
plain /usr/bin/cmp a b              rc=1
/usr/bin/cmp -s a b                 rc=1
```

GNU diffutils 3.12, `pacman -Qkk diffutils` clean; threshold is 4096 B and the 0 appears only when
`cmp`'s stdout actually receives bytes (piping to `head` shows the same 0, inherited from the
writer's path). Recommendation: add the stdout condition to that sentence. The operative rule —
counters, controls and the rubric never use `cmp -l` — stays and is cheap; `cmp -s` and plain `cmp`
were correct in every case measured.

## Preserved contract

No claim, control, carrier, oracle row, rubric check or freeze path that a predicate or control
reads at `REV` is proposed for deletion. The set removes: unfalsifiable freeze entries (S5-S8,
S10), an unbuilt tool name (S9), a table the amendment replaced (S3), an arm with no reachable
failure mode (S4), and duplicate parsers/loaders/writers (S1, S2, S11, S12). Neither gate changes a
target: Gate A confirms the drop; Gate B fixes a rule contradiction that currently makes C2 stop on
its own entries, and keeps the dev arm out of the frozen rubric.

Nothing in this seat wrote to the lane tree outside this file. All probes ran under
`/fast/scratch/hyaku/kaidoku-r44/probe-R44Simplify/`; a detached `git worktree` at base
(`base-tree`) was used for BASE-side scoring and was not committed.
