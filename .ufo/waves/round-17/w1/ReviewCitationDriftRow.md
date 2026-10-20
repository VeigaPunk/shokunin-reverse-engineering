# ReviewCitationDriftRow — SKILL.md:448 guidance + citation-drift gate pins (r17 w1)

Advisory, author-side. Read-only: this report is the only file written. No probe grade run, no
REA verb, no Ghidra, no carrier, no installs. Method: `git show`/`git diff`/sha256, source read of
`.ufo/gates/citation-drift/citation-drift-probe.py`, the two drafts
(`w1/draft-skill-section.md`, `w1/draft-readme.md`), and one `python3 -I <probe> --help`
(exit 0, observed 2026-10-20).

## 1. Defect confirmed, and bounded (observation)

`SKILL.md:448` advertises the relative, non-isolated form:
`python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> --table … --expected …`.
The only retained **isolated and absolute** execution is `.ufo/waves/round-16/verification.json:317-334`
(label `citation-strict`; argv `:318-330`; `cwd` `:332`; exit 0 `:333`; `clean findings=0` `:334`).
Three deltas, not one:

1. no `-I` (`:319-320` has it);
2. relative `--root .` / `--table` / `--expected` versus absolute argv (`:322-329`);
3. the receipt ends `--strict` (`:330`) while the row advertises the **non-strict** default. Under
   `contract.md:80-88` (`exercised_match` = normalized command equals an exercised argv modulo the
   leading `python3`), fixing (1)+(2) alone still leaves the row an `unlabelled_variant` against the
   strict-only receipt.

Impact is bounded, so do not overstate it: the probe never reads CWD (`grep getcwd|os.chdir` empty;
only `git -C <root>`), but the relative `--table`/`--expected` are opened against CWD
(`citation-drift-probe.py:289-303`), and `root_ok`/`rev_ok` run first (`:264-277`). Invoked outside
the lane root the row therefore exits **2** with `root_unreadable` / `revision_unresolvable` /
`pointer_table_unreadable`, never a false "reported" grade. This is a truthfulness-of-guidance
defect (R16-INVOCATION), not a live wrong verdict.

## 2. Exact isolated absolute argv

The draft row (`w1/draft-skill-section.md:13`) already carries the correct strict shape; it matches
the r16 receipt token-for-token except `<REV>`:

```
python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --table /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json --expected /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/expected.json --strict
```

If L1 instead keeps the row's original advertised default (probe semantics, "0 reported"), the
replacement is the same string **without** the trailing `--strict`. Either way:
- keep literal absolute paths and the `<REV>` placeholder (a `$LANE`/`~` token would not match an
  exercised argv); keep this argument order;
- `-I` is safe: the probe imports stdlib only (`citation-drift-probe.py:50-58`), and
  `python3 -I <abs probe> --help` exits 0 (observed);
- no `--snapshot-dir` is needed **now**: the table has zero `@slug` targets (`grep '"@'` = 0);
  the `config-toml-landmarks` pin at `expected.json:15-16` is inert. If a future entry adds `@`,
  the row must add `--snapshot-dir /home/…/.ufo/gates/citation-drift` or the run returns CNE
  `pointer_table_unreadable` (`citation-drift-probe.py:140-151`).

**Claim-blocking delta (medium).** The draft row cites only pre-round receipts: `commands[17]` of
`.ufo/waves/round-16/verification.json` and `commands[9]` of `.ufo/waves/round-15/verification.json`
(verified: index 9, label `citation-strict`, exit 1, rev `7ad23fe1…`, no `-I`); the row at HEAD
cites none. C1(b) additionally requires the row be **re-exercised this round** with its isolated
absolute argv and the receipt retained. L1 must
run the advertised argv at the landing rev and add that receipt (e.g. `.ufo/waves/round-17/verification.json`
`commands[N]`) to the row's receipt list. Note the row text "the unflagged default … is an
unexercised variant" becomes stale if L1 also runs the non-strict form; update whichever claim the
actual receipts make true.

**Integration hazard (medium).** Only draft line 13 is payload. Draft lines 11-12 are the table
header/separator context; copying the whole block into `SKILL.md` would duplicate the existing
header at `SKILL.md:445-446`. Replace `SKILL.md:448` with the single data row, one physical line.

**Minor (low).** (a) "run from the repo root" is redundant and re-introduces CWD framing; with
absolute `--root`/`--table`/`--expected` the entry is CWD-independent. (b) The row stays
`probe / kaidoku` while advertising `--strict` gate semantics; the cell states the map, so this is
self-describing, but if L1 prefers the kind to match the mode, use `gate / kaidoku` and adjust the
intro sentence at `SKILL.md:440-443` (no line shift). (c) Exact selftest form: `--selftest` reads
**only** `--expected` (`citation-drift-probe.py:486-487`, `:405-410`); `--root/--rev/--table/--strict`
are ignored. It creates temp git repos (`:349-367`), so the "isolated temp fixture repos" wording
must stay.

## 3. Do README/SKILL edits move the pins?

As drafted: **no.** Both drafts keep every pinned citing line and the one anchor phrase, and neither
gate file changes.

- `pointer-table.json` digest recomputed today = `7994eec7…789d1` = pin at `expected.json:12`
  (match True). Table and expected are unchanged at HEAD (`git diff --stat 27b8fc1 HEAD --
  SKILL.md corpus/README.md .ufo/gates/` empty).
- `skill-registry-citation-drift-row` (`pointer-table.json:439-443`) is an `anchor` with **no
  `pin_line`**, `must_match "frozen-run preflight"`. The draft row keeps that phrase; row 448 may
  therefore change shape and length without a table edit.
- `skill-rule14-*` (`pointer-table.json:358`/`369`/`381`/`393`) pin the **citing** lines
  `SKILL.md:246/248/252/254`. Row 448 is below them, and the new section is appended after
  `SKILL.md:507` (EOF). Hard boundary: any insertion at or above line 254 breaks those four.
- `shonen-skill-range` (`pointer-table.json:249`) reads `SKILL.md:81-314` for the phrase at
  `SKILL.md:233`; unaffected by either edit.
- `readme22-*` (`pointer-table.json:168`/`180`) cite `corpus/README.md:22`; `readme175-*`
  (`:206`/`217`/`229`) cite `:175`; `sc69-readme-177` (`:53`) reads `SCORECARD.md:69` →
  `README:180`; `sc72-readme-nitrow` (`:64`) reads `SCORECARD.md:72` → `README:138`. The README
  draft edits line 35 in place and inserts at line 182 (after the last Frontier bullet at 181), so
  lines 22/138/175/180 keep their numbers and text. No pointer entry cites a README line ≥182.
  Unsafe: any newline at or before 180 (≤22 breaks `readme22`, ≤138 adds `sc72`, ≤175 adds
  `readme175`, ≤180 adds `sc69`); a new coverage-map/Knowledge row is therefore a red.
- SCORECARD/LOG: all pins there cite lines ≤1435 (SCORECARD) / ≤1442 (LOG); the round appends at
  EOF (`SCORECARD.md` 2348+, `LOG.md` 2031+), so no shift. Do not rewrite the quoted LOG lines
  1012/1442 — corrections are new appended lines (draft-log-entry.md already says this).

Only one operation affects the frozen inputs: **any byte change to `pointer-table.json`**. Then
`expected.json:12` must be re-pinned in the same commit or the next run exits 2
`pointer_table_tampered` (`citation-drift-probe.py:294-308`; same-commit re-pin rule at
`citation-drift-probe.py:39-40` and the row's pinned-values cell). Recommendation:
do not touch the table this round; the existing anchor plus the retained receipts discharge
R16-INVOCATION without reopening the frozen input. `expected.json`'s `frozen_run` block
(`:3-10`, rev `679af5d…`, verdict `failed`) is **inert** — the probe never reads it (only
`pointer_table` `:294`, `snapshots` `:154`, `selftest` `:409`); a run at the r17 rev is a different
measurement by that note alone, and needs no edit.

## 4. Residual risk / verification gaps

- I did not execute the probe (read-only seat; L1 owns the single re-exercise). The grade path is
  traced statically; `expected.json` "13 cases" order checked against `:18-84`.
- `invocation-audit.py` is not committed at review time (`.ufo/waves/round-17/tools/` absent), so
  the row match rests on `contract.md:80-88`; if the implementation treats `--strict` as optional
  or does not wildcard `<REV>`, the conclusion changes.
- The corrected row's re-exercise must run at the **landing** rev to evidence the new row text; the
  r16 receipt is still byte-reproducible (gate files unchanged) but predates the edit.
- New prose line cites into installed Ghidra sources in the draft section (e.g. `GoVer.java:65`)
  are not in the pointer table and are not graded; a wrong line there would not redden the gate
  (other seats own that check).
