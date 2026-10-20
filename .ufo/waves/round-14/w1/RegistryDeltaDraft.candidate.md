# Registry delta candidate — C1 `used-by` append (round 14, wave 1)

Status: **proposal only, not applied.** `corpus/SOURCES.md` was opened read-only and is unchanged.
Owner of application: L1 (planner/integrator). Author of this draft: `KaidokuR14.RegistryDeltaDraft`.

Basis: the **final** C1 entry candidate `.ufo/waves/round-14/w1/GoEntryDraft.candidate.md`
(2026-10-20, 19,539 bytes) and its "Sources reopened for this entry" table.
C1 entry target path (claims-bound): `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`.

## 0. Correction to the earlier frozen shape (read first)

An earlier 02:22 draft of the C1 candidate cited `S003`–`S006`; the final 02:23 candidate cites
**`S001`, `S003`, `S004`, `S007`** and contains **zero** `S002`/`S005`/`S006` tokens. Verified by
`grep -o` counts on the final file. The delta below follows the final file.

Consequence: **do not append the entry path to S005 or S006.** The entry does not cite them, so a
used-by append there would be a false registry claim (worse than leaving the round-13 citation alone).
`S005`/`S006` receive no cell change of any kind.

**Claims mismatch for L1, not for this seat:** `claims.json` C1 still lists sources
`S003`, `S004`, `S005`, `S006`. The final entry cites `S001`, `S003`, `S004`, `S007`. Either the claim's
`source` list or the entry's citations must be reconciled by L1; the registry must follow the integrated
artifact, never the stale claim list. This seat does not edit `claims.json`.

## 1. Preconditions (all must hold before applying)

- **P1** The C1 entry exists on disk at the exact claims-bound path
  `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`.
  (Checked 2026-10-20: it did **not** exist yet; only the candidate under `w1/` existed.)
- **P2** That integrated entry still cites the row's source id in its sources table. Apply a row's
  append only if the entry cites that id; the integrated text is authoritative over both the draft and
  `claims.json`.
- **P3** If the integrated entry uses a different filename, this delta is **stale**: L1 must substitute
  the actual path in every new cell and re-check P1, rather than apply the literal path below.
- **P4** No other cell may change. `status`, `opened`, `recheck`, `scope`, `anchor`, `teaches`,
  `source`, `kind`, `tier` stay byte-identical. No row is added, removed, reordered, or superseded.

Rationale for P1/P2: `sources-census.sh` check **E11** reports `used-by` paths missing on disk, and a
`used-by` must name the artifact that actually cites the row.

## 2. Frozen delta — four `used-by` cells only

All four rows are currently `mined`; the new reference is **appended after** the round-13 reference,
never substituted for it.

| file line | id | column | old cell (exact) | new cell (exact) |
|---|---|---|---|---|
| 7 | S001 | `used-by` (11th cell) | `corpus/lessons/round-13.md` | `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` |
| 9 | S003 | `used-by` (11th cell) | `corpus/lessons/round-13.md` | `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` |
| 10 | S004 | `used-by` (11th cell) | `corpus/lessons/round-13.md` | `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` |
| 13 | S007 | `used-by` (11th cell) | `corpus/lessons/round-13.md` | `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` |

Separator is comma + one space. `sources-census.sh` splits the cell on `,` and trims each path
(parser at `scripts/sources-census.sh`, `mined` branch), so both paths are validated by E11.

### Apply discipline

The old cell value `corpus/lessons/round-13.md` also occurs on the other 18 rows. **Do not global-replace.**
Anchor each edit on the row id at the stated line, and replace only that row's final table cell.
Line numbers are as of baseline `767adafb97e2eef6980e2ad873d357e16721c467`; if the registry moved, locate by
the unique `| S00N |` prefix instead of the line number.

## 3. Explicit no-change cells (measured, not assumed)

| id | status | recheck | why unchanged |
|---|---|---|---|
| S001 | `mined` | `on-release` | Entry cites `SKILL.md:168-169` for the target-free metadata route; row scope and anchor unaffected. |
| S003 | `mined` | `on-release` | Entry cites the installed archive; digest still `f00d29c…8d804`, `GoRttiMapper.java:79` still exact. |
| S004 | `mined` | `on-release` | Commit `385e8cd…fa174` reopened 2026-10-20; title, date, and range diff unchanged; still upstream, not installed. |
| S007 | `mined` | `on-release` | Entry cites `ChangeHistory.md:564,582,585`; header still `Ghidra 12.1.4 Change History (September 2026)`, file digest `c6b2530…65c4`. |
| S005 | `mined` | `on-release` | **No append**: final entry cites neither S005 nor S006. Row stays exactly as is. |
| S006 | `mined` | `on-release` | **No append**: final entry cites neither S005 nor S006. Row stays exactly as is. |

No row is re-statused. `mined` already means "cited by an artifact"; adding a second citing artifact does
not change the status enum, and no rejection/admission event occurred. `on-release` remains the correct
cadence because each anchor is pinned to the installed Ghidra 12.1.4 artifact, the installed REA skill, or
an upstream commit whose relevance is only re-judged when a release ships it.

## 4. Conditional extension — NOT part of the frozen delta

Apply this **only if** (a) L1 creates `corpus/lessons/round-14.md`, (b) that lesson's Gate cites the row id,
and (c) this is staged **after** section 2. Otherwise omit it.

| id | old cell after section 2 | conditional new cell |
|---|---|---|
| S001 | `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` | `…, corpus/lessons/round-14.md` |
| S003 | same | `…, corpus/lessons/round-14.md` |
| S004 | same | `…, corpus/lessons/round-14.md` |
| S007 | same | `…, corpus/lessons/round-14.md` |

Reason for the guard: an E11 failure would be introduced by naming a lesson that does not exist or does
not cite the row. The frozen delta in sections 1–3 is complete without this extension.

## 5. Validation for the integrator (not run by this seat)

After applying section 2 and before any lesson append:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Expected: `kaidoku<TAB>ok` and exit 0, with `FLEET.rows` unchanged from the pre-delta census.
A `E11 … missing used-by …` line means P1/P2/P3 failed — revert that cell, do not edit the entry path
into the registry as a workaround.
A path-less verification that the intended rows changed:
`grep -n "2026-10-20-r14-go-version-diagnosis" corpus/SOURCES.md` should return exactly four lines:
S001, S003, S004, S007.

## 6. Limitations

- This draft asserts only registry routing. It does not admit, review, or endorse the C1 entry's content.
- Source facts verified are those in the companion report; no Ghidra analysis, REA call, or target run
  supports this delta.
- The C1 entry is a sibling candidate, not yet at its integrated path; its final citation table may change
  again. P2 re-checks against the integrated text.
- The claims/entry source mismatch is reported, not resolved, here.
