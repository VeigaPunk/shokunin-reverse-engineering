# EX-14 projection — C1 coverage, arc3-loop1-round3

Seat EX-14 · chain c1 · role executor · wave `arc3-loop1-round3` · 2026-10-19.
Task: command A **before** at HEAD (verbatim) + **after-projection** — apply the
drafted knowledge-entry + map-token patches to a `/var/tmp` scratch tree, run
command A, expect `83/83`, `14/14`, `missing []`, `dangling []`.

**VERDICT: PASS** on all three projected revisions of the entry draft (the draft
text kept being refined mid-wave; each refinement was re-projected). Command A:
`82/82 → 83/83`, `rules 14 → 14 (14/14)`, `missing []`, `dangling []` both sides;
prior-82 knowledge files byte-identical; `corpus/README.md` 190 → 190 lines with
only line 38 changed; token set 82 → 83 with the one new token == the entry stem;
citation-drift probe findings = 0 at base and at every projected commit.

## 1. Inputs — the exact drafted bytes used

All hashes re-derived by this seat (sha256sum / git), not transcribed.

| input | source | identity |
|---|---|---|
| entry literal, revision A | `claims/c1/records-drafts/knowledge-entry-draft.md` marker block at wrapper sha `b9ca0310…` (the revision SC-2's own `SC-2/README-identities.txt` quotes as final) | 16,466 B, sha256 `fcbcb69125af1c5f7b9a1e701eb9734d5e9bde8865e4f2c01a5ab17eca75652f` → `inputs/entry-literal-rev2.md` |
| entry literal, revision B | same file after a further append (live at 13:14Z, wrapper sha `cdbb5d0b…`); + one Observation (round carrier roster / VZ-1 matrix), 36 → 37 lines | 17,196 B, sha256 `18e910b90934c93f916602f615c01e68cd647c4ad3e7148ddef9ebcc07641ddc` → `inputs/entry-literal-rev4.md` |
| entry literal, revision C | same file after a later refinement of the id-domain observation line (live at 13:16Z, wrapper sha `9b0cb5b8…`) | 17,563 B, sha256 `189ac2a2cd564eca4c285a56e4ae649264c21733dc22dcfbfe380036834ddaf2` → `inputs/entry-literal-revC.md` |
| map-token new line (PRIMARY) | `claims/c1/records-drafts/map-token-patch.md` (sha256 `333ca590…`, stable since 13:08Z), code block after "New line — PRIMARY", byte-extracted | 337-char line + `\n`, sha256 `25011b3eb713c1fd02bea9d27d6eb296d626c90d69f022baa29812ad4810f635` → `inputs/new-line-primary.txt` |

Patch shape used: new file `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`
(stem `2026-10-19-arc3-r3-evm-optimizer-shapes`) + one-physical-line substitution
of `corpus/README.md:38` (old line sha256 `bfaf5540…`, README before 190 lines
sha256 `6ac43e838bca7d08cc7ac3c24cff60042cb174d92b08363db0798fa844163577`).

**PRIMARY variant chosen over HONEST-STOP** on evidence, not preference: the
optimizer-enabled legs recovered K/K — EX-10 `VaultB` opt200 13/13 (@6.4.0
`ev_d409bd50…`, @6.7.0 `ev_ae5aaee0…`), EX-07 `Rv2TokenOpt` 5/5 on all six
hex/raw legs across 6.4.0/6.5.0/6.7.0, EX-04 carrierB opt200 11/11, EX-05
`CarrierB` opt200 8/8 — read first-hand from the envelopes in the wave tree.

## 2. Method (no lane writes, no lane git commands)

- Scratch clone: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /var/tmp/ex14-scratch`
  → HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`, clean.
- Runner `inputs/project.py`: reset clone to base → write the entry file → exact
  single-line README substitution (asserts old line) → commit **in the scratch
  clone only** → run command A (SCORECARD.md recipe A, verbatim `git show REV:path`
  form) at base and at the scratch commit.
- Lane repo: read-only for this seat. `git rev-parse HEAD` = `c07af80f…` before
  and after; the only untracked/modified paths are other seats' work
  (`.ufo/gates/*` from C2/C3, the round-3 wave tree). No `/tmp` used anywhere
  (scratch under `/var/tmp/ex14` and `/var/tmp/ex14-scratch`).

## 3. Command A before — verbatim (lane HEAD `c07af80f…`)

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 82, "mapped": 82, "missing": [], "revision": "c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311", "rule_blocks": 14}
```

Reproduced byte-identically inside the scratch clone at base (same JSON — see
`evidence/projection-rev4.json` → `command_a_before`). Also corroborated by
independent seats: RV-4 `claims/c1/RV-4/command-A-before.txt`, SC-2, SC-1,
VZ-1, EX-12 — five other seats' captures read 82/82, 14/14.

## 4. Command A after — projected (scratch commits)

Revision A of the entry text — scratch commit `24cf6fd91e6a9688c15fb2218d8347adfdf79044`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "24cf6fd91e6a9688c15fb2218d8347adfdf79044", "rule_blocks": 14}
```

Revision B (current live literal) — scratch commit `a3e4b857e311eba6415b98a117b2dde606f69af9`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "a3e4b857e311eba6415b98a117b2dde606f69af9", "rule_blocks": 14}
```

Revision C (the live literal at 13:16Z) — scratch commit `9799641ea9a92557e2fa146095a9d9ee865a190a`:

```json
{"citation_resolved_rules": 14, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 83, "mapped": 83, "missing": [], "revision": "9799641ea9a92557e2fa146095a9d9ee865a190a", "rule_blocks": 14}
```

Raw audit records: `evidence/projection-rev2.json`, `evidence/projection-rev4.json`,
`evidence/projection-revC.json`, `evidence/projection-rev2-rerun.json`
(re-run stability: every field identical across runs except the scratch commit
id, which embeds commit time).

### Identity / derivation checks (all re-derived, per rule #14 discipline)

- `changed_line_numbers = [38]`; `line_neutral = true` (190 → 190). Whole-file
  README after: sha256 `016b632e46e5852ab966f7d99776676f125ffbf2418a897a4f8af9e31a642281`
  — independently matches SC-2's rehearsal after-state and RV-4's PRIMARY
  after-state measurement (cross-seat convergence, three parties).
- `prior82_byte_identical = true` at git level: `git diff --name-status base → projected`
  = exactly `M corpus/README.md` + `A corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md`.
- Token set: unique 82 → 83; occurrences 84 → 85; added == {stem}; removed [].
- Scratch-commit blobs (replay anchors): `corpus/README.md` =
  `ee6c2f62d2525a41a857337375f37c11a7cae2f6` (both revisions); entry blob =
  `5098f338e6684c43f20027280ee036cb5e41140f` (rev A) /
  `8d7b866f2f5463540a253595935b2bed98cde1a6` (rev B).
- Entry file bytes in the scratch tree re-hash to the input literal exactly
  (`fcbcb691…` / `18e910b9…`).
- Replayable patches: `inputs/base-to-projected-rev2.patch`,
  `inputs/base-to-projected-rev4.patch` (base → projected, 2 files, +37/−1).

## 5. Attacks + side checks, with verdicts

`inputs/attacks.py`, raw transcript `evidence/attacks.json`; all four
pre-registered outcomes reproduced exactly:

| attack | state built | command A | verdict |
|---|---|---|---|
| A1 token-only | README token, no entry file | `files 82, mapped 82, missing [], dangling ["2026-10-19-arc3-r3-evm-optimizer-shapes"]` | loud — pairing is load-bearing |
| A2 entry-only | entry file, no token | `files 83, mapped 82, missing [stem], dangling []` | loud |
| A3 stem mismatch | entry at stem, token truncated one char | `missing [stem]` + `dangling [wrong stem]` | loud, both directions |
| A4 row insert | new map row instead of same-line edit | `83/83` — **count is blind**; README 191 lines (line-neutrality broken) | the form the line-neutral clause prevents; r1's probe measurement additionally showed row inserts redden 5 pinned citations (not re-run here) |

Side-harm check (not part of the C1 claim): the citation-drift probe run against
the scratch clone with EX-41's current 57-entry table + digest-pinned
`expected.json` — **findings = 0** at base `c07af80f…` and all three projected
commits (revs A/B/C; transcript `evidence/probe-sidecheck.txt`). The table's
`readme38-arc3r1-token` anchor (r1 token survival in the map row) holds under the
projected line by construction: the new line retains `2026-10-19-arc3-r1-evm-real-solc`.

## 6. Catches / debt handed to the parent

1. **SC-2's identity note is stale vs its own draft file**: `SC-2/README-identities.txt`
   quotes the draft at `b9ca0310…` (literal `fcbcb691…`), but the live
   `records-drafts/knowledge-entry-draft.md` moved twice afterwards —
   `cdbb5d0b…` (literal `18e910b9…`, VZ-1 roster observation appended) then
   `9b0cb5b8…` (literal `189ac2a2…`, id-domain line refined). All three literal
   revisions were projected here with identical command A results, so the
   staleness cannot silently invalidate this projection; the identity note must
   still be re-derived at landing (rule #14).
2. **Stray token in the entry text**: `` `⟨pure-leg delta⟩` `` sits mid-sentence in
   the EX-04 carrierB observation of both revisions — looks like a leftover
   annotation marker, not prose. Cosmetic; does not affect command A; parent may
   ask SC-2 to clean it.
3. **Invariance statement**: command A reads the entry only as a file present on
   disk (stem match); it does not read its content, so further *content* edits to
   the entry draft do not invalidate this projection. A **stem change** or a
   **map-token change** does — then re-run `inputs/project.py` (it fails loudly
   via `missing`/`dangling`, measured in A1–A3).
4. The projected landing remains the parent's to perform at the real repo and
   re-measure at the records commit; the scratch-clone commits are measurement
   apparatus, not lane history.

## 7. Replay recipe

```bash
# 0) fresh scratch clone at base
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /var/tmp/ex14-scratch
# 1) run the projection (runner in this dir; expects git repo paths above)
python3 inputs/project.py \
  --entry-file inputs/entry-literal-rev4.md \
  --stem 2026-10-19-arc3-r3-evm-optimizer-shapes \
  --new-line-file inputs/new-line-primary.txt \
  --label projection-replay --out <somewhere>.json
# expect: PROJECTION_PASS true; command_a_after = 83/83, 14/14, missing [], dangling []
# 2) attacks
python3 inputs/attacks.py   # expect ATTACKS_AS_PREREGISTERED: True
```

Alternative whole-patch replay: `git apply inputs/base-to-projected-rev4.patch`
in a clone at `c07af80f…`, commit, run command A (recipe A) at the commit.