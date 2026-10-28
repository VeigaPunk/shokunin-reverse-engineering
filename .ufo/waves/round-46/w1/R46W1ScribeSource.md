# R46W1ScribeSource — S142 opened live: row, Gate block, and the arm's documented limits

Seat: source opener for round 46 wave 1 (`kaidoku-shokunin`). Read-only on the lane tree;
the only files written are this report and `w1/R46W1ScribeSource/row.md`.

## Behavior

Fetched `https://git-scm.com/docs/git-log` twice (2026-10-28T16:58:01Z and 16:59:05Z), HTTP
200, 375,834 bytes each, both
`sha256:0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`, `cmp` exit 0.
Located the `--diff-merges=<format>` section (raw offset 253596, line 6043 of the saved
copy), the `first-parent` value anchor (offset 255613, line 6069) and the defining sentence
(offset 256017, line 6072):

> Show full diff with respect to first parent. This is the same format as --patch produces
> for non-merge commits.

Presence was proven against the saved copy, not against a live recollection: the first
clause is contiguous in the raw bytes (`grep -c` → 1); the whole quote is present after tag
stripping and whitespace normalisation (`True`), because the page wraps after "same" and
puts `--patch` inside its own `<span>`. The quote is 19 whitespace-delimited words (20 with
hyphens split) — inside the claim's ≤25-word bound.

Wrote the 11-column row (11 cells, checked mechanically) with `used-by
corpus/lessons/round-46.md`, and the three-line Gate block. Both are in
`w1/R46W1ScribeSource/row.md`, paste-ready.

Then probed the documented behaviour in a one-commit fixture repo (`git -C "$D" init`,
toplevel asserted equal to `$D`, fixed identity/dates so the merge is deterministic:
`a05988037ecf09f016a042da887ac1dc7e405d15`, resolution bytes neither parent has). Plain
`git log --name-status` prints **no** file for the merge; `-m` alone prints the merge
**twice** (default `separate`, one per parent); `--diff-merges=first-parent` after `-m`
prints it once with `M f.txt`; reversing the two flags restores the two-entry output,
because the later option wins. This is the evidence that the arm `R45-CL6` asked for exists
and is what it says — and the evidence that its correctness is order-sensitive.

## Gates

The predicates themselves (`attest.py --profile v2`, `registry.py --profile v2`) were
**not run** by this seat — that is the executor lanes' job, and running them here would
double-count. What this seat gates is the source row it produced:

| gate | value | result |
|---|---|---|
| HTTP status of both fetches | 200, 200 | pass |
| byte size / digest stable across fetches | 375,834 / `0a73e33b…`, `cmp` 0 | pass |
| quote located, ≤25 words | 19 words, 3 raw offsets recorded | pass |
| quote present in the saved copy | raw-contiguous clause 1; whole quote `True` after tag strip | pass |
| row cell count | 11 | pass |
| `used-by` names the round-46 lesson | `corpus/lessons/round-46.md` | pass |

## Touched surfaces

- `.ufo/waves/round-46/w1/R46W1ScribeSource/row.md` (new)
- `.ufo/waves/round-46/w1/R46W1ScribeSource.md` (this report)
- Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeSource` (removed after the
  receipts above were transcribed; nothing under `/tmp` was used)
- No file under `plans/`, `tools/`, `corpus/`, `SKILL.md`, `LOG.md`, `SCORECARD.md`, the
  fleet repo, `.ufo/state/`, `.ufo/watchdog.log` or `.scratch/` was written. No git/jj
  mutation; only `rev-parse`, `log`, `show`, `cat-file`, `status`, `merge-base
  --is-ancestor` were used. No tool installed.

## Findings

**F1 — the row's pin is reproducible, and it already matches a landed fetch.** Two of my
fetches agree byte-for-byte. `corpus/lessons/round-46.md:27` records a third fetch at
`2026-10-28T16:49Z` with the same size and digest. I did not observe that fetch; I observed
only that string in the file. Three records, one digest.

**F2 — the word count in the landed Gate is wrong as written.** `corpus/lessons/round-46.md:27`
says the quote is "(21 words)". It is **19** whitespace-delimited tokens; 20 if hyphens are
split (`non-merge` → 2, `--patch` → 1) and 20 if counted by alphanumeric runs
(`re.findall(r"[A-Za-z0-9_.]+")`). I could not construct a method that yields 21. This does
not touch any predicate clause (the claim's bound is ≤25, not an equality), so it is a
record-accuracy defect, not a target defect. Exact command in `row.md` R3.

**F3 — the page does not say "only".** The seat brief and the landed `teaches` cell both
describe the value as showing the diff "against the first parent only". The page's words
are "with respect to first parent"; `first parent only` and `first-parent only` occur 0
times in the page text, and the two occurrences of "only the first parent" belong to the
unrelated traversal option `--first-parent` and to `--exclude-first-parent-only`. The
"one diff, first-parent side" reading is **inference** from the value name plus the
`--patch`-shape sentence — correct, and confirmed by the probe, but it must not be
presented as a quotation. If the L1 keeps "only" in the `teaches` cell, it should be read as
the lane's inference. [INFERENCE]

**F4 — the arm is order-sensitive and nothing pins the order.** Measured, same fixture:
`-m` alone → merge emitted twice (per-parent `separate` output); `-m` then
`--diff-merges=first-parent` → once; `--diff-merges=first-parent` then `-m` → twice again.
`tools/round-46/gate.py:99` passes them in the working order (`-m` first), so the frozen arm
is correct as written, but a reorder would silently widen the arm to per-parent diffs and
still exit 0. `--diff-merges=first-parent` alone produces the same single entry (the `-m` is
redundant for this arm, not harmful). Routed as an observation for the L1, not fixed here:
nothing in the frozen instrument or in block 23's `merge` row records the ordering
dependency.

**F5 — the landed row already existed; my independent row agrees with it.** `corpus/SOURCES.md`
at HEAD (`04252247`) already carries `S142`, first entered at `227d6982`, 142 rows total,
and the freeze `31820472784284727546808acc31b3ea1e73919b` is an ancestor of HEAD. I derived
the row from the page without copying it. All 11 columns agree in substance; my draft adds
the two anchor ids (`#Documentation/git-log.txt---diff-mergesformat`,
`#Documentation/git-log.txt-first-parent`) and names the re-fetch stability. The one wording
difference is F3's "only".

**F6 — `first-parent` and `1` are the same value.** The page gives them one shared `<dd>`,
so a gate that accepts `--diff-merges=1` would be reading the same documented behaviour;
nothing in block 23 depends on the spelling.

## Out of scope / not run

- `tools/round-46/attest.py` and `registry.py`, their `--selftest`/battery runs, and the
  `.ufo/waves/round-46/controls/` receipts: not run here.
- `SKILL.md` block 23 text, the census, and the registry section: read only for the row
  format; not edited, not scored.
- `corpus/SOURCES.md`: not edited (L1 pastes the row).
- The 16:49Z fetch recorded in the lesson: not reproducible by me (I cannot rewind to that
  second); only its recorded digest is compared.

## Artifacts

- `.ufo/waves/round-46/w1/R46W1ScribeSource/row.md` — row (11 cells), Gate block, presence
  proof, arm probe table, six receipts with exit code, stdout sha256 and UTC time.
- `.ufo/waves/round-46/w1/R46W1ScribeSource/receipts/` — the raw captures those receipts
  name (`quote.out`, `grep_raw.out`, `cells.out`, `fetch2.out`, `sha2.out`,
  `arm_probe.out`, `index.tsv`) plus the probe script `arm_probe.sh`; the fetched HTML
  itself is not retained in the lane — its digest is the pin.
- `.ufo/waves/round-46/w1/R46W1ScribeSource.md` — this report.
