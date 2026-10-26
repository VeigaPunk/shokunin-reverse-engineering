# R38W2AssimMirror — scratch-mirror census for the admitted append (addendum §10)

Seat: executor (leaf). Axes: coverage, calibration. Milestone: round 38 attempt 2 — falsify the
landing. Advisory only: nothing in the lane was edited; no VCS mutation was run (read-only
`git show/archive/status/diff` only). Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2AssimMirror`
removed after artifacts were copied; every number below is reproducible from the artifacts beside
this report.

## 0. Verdict

**CONFIRMED for the census gate — the S116 row + S110 cell edit are census-clean (exit 0, zero
E-codes on both the minimal-append and the full landed mirror) — DEFECTS FOUND in the append
elsewhere: the committed entry carries one false correction, the S110 anchor does not locate the
lines its widened scope now cites, and the live worktree entry is not the landed bytes.**

The seat's blocking condition (E03/E04) does not occur. Neither does any other E-code.

## 1. What was mirrored

| mirror | content | registry sha256 | rows |
|---|---|---|---|
| `fullBase` | `git -C <lane> archive 77091b49` (whole tree) | `5a4c1c8c3ed0a5fd01e03bc57e93b00a563b35f8e5dc791e966e4f4251b92ef6` | 111 |
| `fullMin` | `fullBase` + **only** the S110 row replaced by the 0fc61133 S110 row + the 0fc61133 S116 row inserted after S111 + `corpus/knowledge/2026-10-26-unblob-format-matrix.md` added at its repo path | `9ca320b380492622572948281aabec77dd051324468f19443c8c76dca9c45f9f` | 112 |
| `fullHead` | `git -C <lane> archive 0fc61133` (whole tree) | `4182cd058779c2585a405b6b18e4e17c15c3870a5cd195d7180eb2b6b7dd9129` | 116 |

Minimality is not asserted, it is measured: `diff fullMin/corpus/SOURCES.md fullHead/corpus/SOURCES.md`
yields exactly four added lines — the excluded rows `S112`, `S113`, `S114`, `S115` — and nothing
else. Cell-level check on the S110 edit: only columns 5 (scope) and 11 (used-by) changed; `id`,
`source`, `kind`, `tier`, `anchor`, `teaches`, `status`, `opened`, `recheck` are byte-identical to
base (`artifacts/R38W2AssimMirror/registry-cell-diff-and-worktree-drift.txt`). The landed row's
status/recheck are therefore untouched, as the lesson claims. The S116 row carries all 11 cells
(`docs`/`A`/`mined`/`2026-10-26`/`180d`/entry path), NF=13.

Faithfulness: the lane's live `corpus/SOURCES.md` is byte-identical to `fullHead`'s
(`4182cd05…`), so the full mirror really is the landed registry, not a reconstruction.

Commands (exact):

```
git -C <lane> archive 77091b492cc53f8743bd0701b1e7d5e66123dd84 | tar -x -C $S/fullBase
git -C <lane> archive 0fc6113376a156fddc3ec385386d71c3a4a9f690 | tar -x -C $S/fullHead
cp -a $S/fullBase $S/fullMin   # then the two-line python splice + cp of the entry
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md --today 2026-10-26
```

## 2. Census results (exit codes and every finding)

| target | exit | E-codes | W04 | `ok` line |
|---|---|---|---|---|
| `fullBase` (control) | **0** | 0 | 9 | yes |
| `fullMin` (the append under test) | **0** | 0 | 9 | yes |
| `fullHead` (landed registry) | **0** | 0 | 10 | yes |
| live `corpus/SOURCES.md` (read-only control) | **0** | 0 | 10 | yes |
| corpus-only mirror (`mA_min`, the literal "copy corpus" reading) | 1 | **2 × E11** | 9 | — |

Finding sets: `diff <(grep -v ok fullBase) <(grep -v ok fullMin)` → **empty**. The append adds no
finding of any kind; the new W04 in `fullHead` belongs to **S112**, not to S116 (S112 re-uses
S108's URL under a different scope string). The nine W04 rows are byte-for-byte the nine rows that
`.ufo/waves/round-38/census-start.txt` recorded before the append (S033, S047, S054, S062, S069,
S083, S090, S092, S102), so the `--today 2026-10-26` control run also reproduces the L1's start
census.

Full outputs: `artifacts/R38W2AssimMirror/validate-fullBase.txt`, `validate-fullMin.txt`,
`validate-fullHead.txt`, `validate-lane-real.txt`, `validate-corpusonly-mirror.txt`,
`rowcounts.txt`.

## 3. Method correction — a corpus-only archive is not a valid §10 mirror

With `--file`, `resolve_targets` sets the E11 root to `realpath(dirname(file)/..)`, i.e. the
**mirror root**, not the corpus directory (`scripts/sources-census.sh:497-501`). Two base rows cite
used-by paths outside `corpus/`:

| id | used-by cell | present at base |
|---|---|---|
| S036 | `corpus/lessons/round-18.md, SKILL.md` | `SKILL.md` (root) present; `corpus/SKILL.md` absent |
| S081 | `tools/round-27/xpin-attribute.mjs, corpus/lessons/round-27.md` | root path present; `corpus/tools/…` absent |

A mirror built from `git archive <rev> corpus` therefore emits `E11 S036 missing used-by SKILL.md`
and `E11 S081 missing used-by tools/round-27/xpin-attribute.mjs` and exits 1 **on pristine base**
(verified: pristine `mA`, exit 1). Those two E11 are mirror artefacts, not lane defects, and they
would mask a real E11 introduced by an append. The §10 pattern must archive the whole lane tree;
that is what `fullBase`/`fullMin`/`fullHead` do, and they are clean.

## 4. Gate teeth (six mutants) and two blind spots

Mutants were applied to `fullMin` only (`artifacts/R38W2AssimMirror/mutants.txt`):

| # | mutation | result | exit |
|---|---|---|---|
| M1 | delete `corpus/knowledge/2026-10-26-unblob-format-matrix.md` | `E11 S110` **and** `E11 S116` (both used-by cells) | 1 |
| M2 | append the S116 row a second time | `E03 S116 duplicate id` + `E04 S116 …within scope …` | 1 |
| M3 | inject S112 with S108's exact scope (same URL, no `supersedes`) | `E04 S112 duplicate url … within scope …` | 1 |
| M4 | typo the entry name in both used-by cells (`formats-matrix`) | `E11 S110`, `E11 S116` | 1 |
| M5 | indent the S116 row by four spaces | **no error, exit 0**, rows 111 | 0 |
| M6 | `--today 2026-10-25` (one day before the append's `opened`) | `E08` on S116 and on the pre-existing S107–S111 | 1 |

So the append is load-bearing in the gate: removing the entry, misnaming it, duplicating the row or
re-using a scope all fail. Two blind spots the L1 should know about:

- **M5 — a four-space-indented row is silently ignored.** The parser treats 0–3 leading spaces as a
  row and 4+ as code (`sources-census.sh:40-41, 608-617`). A mis-indented append produces `ok`, exit
  0 and a *lower* row count. `validate` alone cannot see it; the §10 receipt must carry the row
  count (111 → 112 for this append, 116 for the full set), which is why §1/§2 record it.
- **Same-document re-registration always passes.** `E04` compares the literal scope text, so any
  reworded scope on a repeated URL is only `W04` (by design — the round-38 lesson says so). S108/S112
  are one document (`sha256 2d7b901b…`) under two scopes; the gate can confirm the pair is *declared*
  but never that the two scopes are genuinely distinct.

Instrument sanity: `sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`,
`selftest` → exit 0, **96 killed, 0 SURVIVED**.

## 5. The appended entry, re-verified against live bytes

Own fetches (not the wave-1 seats' bytes), 2026-10-26T03:44Z-era tags, receipts in
`artifacts/R38W2AssimMirror/anchor-live-recheck.txt`:

| claim (S116 row / entry) | measured |
|---|---|
| `https://unblob.org/formats/` HTTP 200, 216890 B | 200, **216890 B** |
| sha256 `8f8c29af…bbc5` | `8f8c29aff33d5aa1ee2a69f8a66f272d45fa3dd98d271c95337c3ff15a65bbc5` |
| 97 `<h2 id=` sections | **97** |
| `id="squashfs-v4-be"` present | 1 occurrence |
| meta "more than 30 different …" × 3 | **3** |
| ten SquashFS sections, incl. `SquashFS (v3-Broadcom)` and `SquashFS (v4-broadcom)` | exactly those ten ids; heading texts reproduce the entry's mixed capitalization |
| ZIP "Does not support encrypted ZIP files." | present; ZIP section is **Partially supported** |
| S110 README 235 lines, sha256 `6544d60f…` | **235 lines, 7580 B, `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716`** |
| S110 "78+" at lines 5 and 22 (the widened scope cell) | line 5 `…for **78+ archive, compression, and file-system formats**…`; line 22 `- **78+ supported formats** — …` |

**Defect (content, committed bytes).** The landed entry (0fc61133, `c9427380…`) states:

> the staged "42 vendor-attributed entries" was a count of the word `Vendor` (42 occurrences), not a
> per-handler attribution count.

That negation is false. The page carries `<strong>Vendor:</strong>` in **42 distinct sections** (42
occurrences = 42 sections, one each), i.e. it *is* a per-section count. The census cannot see this —
`validate` checks row shape, enums, dates and used-by existence, never entry prose — so the §10 gate
was green while the admitted prose was wrong about the source it admits.

The live worktree already replaces that sentence, and its replacement is exactly right against the
same bytes: 42 of 97 sections carry one `Vendor:` field, and the single literal value `unknown` is
`squashfs-v3-non-standard` (raw: `<li><strong>Vendor:</strong> unknown</li>`). Its added numbers also
check out: **89** `<p class="admonition-title">Fully supported</p>`, **8** `Partially supported`,
**97** `<strong>Handler type:</strong>` sections (the page-wide 90th "Fully supported" is the table
header `Fully supported?`, which is why "counted per section" matters).

## 6. The S110 anchor does not locate the new scope lines

The edited scope cites "its own \"78+\" format-count sentence (**lines 5, 22**)". The row's anchor
cell was not touched: it still carries `235 lines, sha256 6544d60f…; line 49 "For SquashFS support,
also install [sasquatch]…"`. Every other row of this append locates its scope (`S112` anchor:
`lines 24-70`; `S116` anchor: byte count + sha256 + 97 sections + the meta sentence). The claim is
true (verified above), but a reader cannot reach the newly cited lines from the registry row, and no
census code exists for anchor completeness. Recorded as a calibration defect in the landed bytes;
one extra clause in S110's anchor (`lines 5, 22 "78+…"`) would close it.

## 7. Worktree drift — the landed entry is not the file on disk

`git status --porcelain -- corpus/` at 2026-10-26T07:02Z shows three modified corpus files:

```
 M corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md
 M corpus/knowledge/2026-10-26-unblob-format-matrix.md
 M corpus/lessons/round-38.md
```

Entry sha256: worktree `b641e7d9…`, 0fc61133 `c9427380…` (10 insertions / 8 deletions; mtime
2026-10-26T04:01:06-03:00, i.e. during this wave). The entry text names the author: "Wave-2 seat
`R38W2SrcS116` caught an earlier draft…" `[INFERENCE: an in-flight sibling edit, not an L1 or
attempt-1 leftover — the mtime and the self-naming comment both point at wave 2]`. The other two
files were touched in the same second.

Census impact: none — `validate` only asks that the used-by path exist, and a mirror built with the
live entry bytes also exits 0 (`validate-fullMin-worktree-entry.txt`). Documentation impact: my §2/§5
verdicts are about the **committed** bytes; the bytes a reader sees today differ, and `0fc61133` no
longer describes them. Whatever the L1 decides, the round's "landed" receipt and the file must be
reconciled before the round closes.

## 8. What this adds to the round's record

1. The addendum §10 gate passes for the S116 append and for the landed registry: exit 0, zero
   E-codes, no new findings versus pristine base — and it is not vacuous (six mutants, four of them
   failing).
2. The §10 recipe needs three amendments: archive the **whole tree** (else E11 lies), record the
   **row count** (else a mis-indented row vanishes silently), and remember the gate says nothing
   about entry content or anchor completeness — the two defects found here both live below its waterline.
3. The committed entry contains a false correction about S116's vendor count; the correct statement
   is the uncommitted one.
4. The live worktree is dirty in three corpus files; the landed commit is not the working state.

## 9. Evidence

Artifacts (`.ufo/waves/round-38/w2/artifacts/R38W2AssimMirror/`): `validate-fullBase.txt`,
`validate-fullMin.txt`, `validate-fullHead.txt`, `validate-lane-real.txt`,
`validate-corpusonly-mirror.txt`, `validate-fullMin-worktree-entry.txt`, `mutants.txt`,
`rowcounts.txt`, `registry-cell-diff-and-worktree-drift.txt`, `anchor-live-recheck.txt`.

Tooling: no installs or upgrades were needed; `sasquatch*`/`unblob` were not invoked; no REA call
was made. Census script: fleet copy `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
sha256 `3fb72615…` (selftest 96 killed / 0 survived / exit 0). Fetches: `curl -fsSL` only, exit 0,
into scratch; `s116.html` sha256 re-checked. Limits: `--today 2026-10-26` was passed explicitly, so
the E08 result in M6 is a deliberate date shift, not a run on a different day.
