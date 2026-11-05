# Seat ScribeKnowledge — round 95, wave w1

**Item.** Draft the knowledge entry, the S320 registry row and the lesson drafts for
R95-C1 (calibration, receipt world-binding) and R95-C2 (depth, craft block 34). No
lane file was edited; every artifact is a draft in the seat directory for the L1 to
land.

**Declaration commit (frozen, read-only):** `4bda1d1dd3788973f10e61212b70df18b3b14ea0`
(base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`).

## Axes

- **coverage** — every named deliverable exists as a draft with a verified path:
  knowledge entry, S320 row, `## Motive` / `## Gate` / `## Mistakes` lesson text.
- **depth** — each claim in the knowledge entry is traceable to a path or a byte
  value; the four bindings, the O_NOFOLLOW rule and the mkstemp mechanism are stated
  with their measured evidence, not paraphrased.
- **calibration** — the S320 row was parsed by the fleet's own census instrument in a
  clone at the declaration commit, in both arms (consumers absent → the two expected
  `E11` findings; consumers present → exit 0, no finding against S320).
- **freshness** — the source was re-fetched live on 2026-11-05 and is byte-identical
  to the two committed fetches (same 76506 bytes, same sha256).

## Files written (all under the seat directory)

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScribeKnowledge/`

| file | what it is |
|---|---|
| `knowledge.md` | the knowledge-entry draft for `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`; opens with the provenance trio (`source:` / `verified-at:` / `recheck:`) and carries sections (a) the `O_NOFOLLOW` rule with the located quote, (b) why a predictable `<json-out>.tmp` is an escape path and why `mkstemp` removes it, (c) the four bindings and their typed reasons, (d) the measured before/after, (e) the named limits verbatim |
| `s320-row.md` | the single 11-column registry row for `corpus/SOURCES.md` (id S320, kind docs, tier A, status mined, opened 2026-11-05, recheck on-release, used-by the two landing files) |
| `lesson-drafts.md` | draft text for `corpus/lessons/round-95.md`: `## Motive`, `## Gate` (URL, access date, HTTP status, byte size, sha256, located quote, admit/reject), `## Mistakes` (class · evidence pointer · captured-by · fix) |
| `verify.md` | the verification record: every command, exit code, output and receipt path |
| `receipts/census-runA.out` / `.err` / `.rc` | census run A (row present, its two `used-by` consumers absent) — exit 1 |
| `receipts/census-runB.out` / `.err` / `.rc` | census run B (row present, both consumers present) — exit 0 |
| `receipts/s320-open2-live-refetch.html` | this seat's live re-fetch of the man page (76506 bytes) |
| `receipts/s320-live-refetch.sha256` | its digest |
| `receipts/v2-rc-mismatch-probe.py` | the probe that measured the `rc-disagree` naming observation |
| `validate/` | the census fixture: the clone's `corpus/SOURCES.md` with the S320 row inserted, plus every path named in a `mined` row's `used-by` cell copied from the clone at the same relative path (152 paths, 0 missing) |

Also written at the lane path named by the prompt: this report,
`.ufo/waves/round-95/w1/ScribeKnowledge.md`.

## Gates exercised

**G1 — the S320 row parses in the registry (census, run B).**
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file
<SEAT>/validate/corpus/SOURCES.md` → **exit 0**. No `E*` line of any code; no finding
of any code against `S320`; the same 32 `W04` lines as the round's committed
before-receipt `.ufo/waves/round-95/census-before.txt` (the sorted `W04\tS…` id sets
diff as identical — the new row adds no duplicate-URL warning). Row shape: exactly 11
cells, no `|` inside any cell; kind `docs`, tier `A`, status `mined`, opened
`2026-11-05` (≤ today, so `E08` silent), recheck `on-release` (symbolic, so `E09`
silent), `used-by` = the two landing paths.

**G2 — the same row before its consumers land (census, run A).** Same command, same
fixture, the two `used-by` consumers removed → **exit 1**, and the only two `E*` lines
in the entire run are

```
file	E11	S320 missing used-by corpus/knowledge/2026-11-05-r95-receipt-world-binding.md
file	E11	S320 missing used-by corpus/lessons/round-95.md
```

which is the landing requirement (the row must land with its two consumers), not a
defect in the row.

**G3 — the S320 source is fresh and byte-identical.** The two committed fetches
`.ufo/waves/round-95/l1/scores/s320-open2-fetch{1,2}.html` are both 76506 bytes with
sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`, matching
`plans/round-95-claims.md` and `.ufo/waves/round-95/claims.json`. This seat's live
re-fetch (`curl -sS -o live-open2.html -w 'HTTP %{http_code} bytes=%{size_download} …'`)
returned **HTTP 200, 76506 bytes**, same sha256.

**G4 — the located quote is located, with its byte-level caveat.** In the raw HTML the
sentence is split across three lines and carries `<i>`/`<b>` markup, so it is **not** a
raw contiguous byte substring; after tag-strip, entity decode and whitespace
normalisation it is exact:
`If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP`
followed in the normalised text by
`Symbolic links in earlier components of the pathname will still be followed.`
The page footer reads `Linux man-pages 6.19            2026-02-08`; the provenance
block reads `This page was obtained from the tarball man-pages-6.19.tar.gz`.
`O_NOFOLLOW` occurs 5 times on the page; only the 2nd carries the quoted rule.

**G5 — the four bindings.** Read from the frozen bytes at `4bda1d1d`:
`tools/round-95/c1-agreement-v2.py` (docstring `:9-18`, implementations `:129-166`)
carries `label-not-frozen`, `label-not-recomputed`, `revision-not-bound`,
`pins-not-bound` as four separate typed branches, so a fixture that violates exactly
one binding is refused with exactly that one reason. The committed receipt
`.ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
confirms it: each of the four forgeries carries exactly its intended single reason
and the honest leg carries `reasons: []`.

**G6 — the measured before/after quoted in the knowledge entry** is read from the
committed receipts only (`.ufo/waves/round-95/pre/` and `.ufo/waves/round-95/l1/scores/`).
The round-95 counting commands were **not** re-run by this seat: the claim says the
L1 already measured them at `4bda1d1d` and that they must not be re-measured at a
different revision.

## Findings

**F1 (naming observation, measured; no frozen byte changed; no kill-rule clause).**
`tools/round-95/c1-agreement-v2.py:19` lists the inherited atoms as `not-valid`,
`stdout-disagree`, `rc-disagree`, `predicted-mismatch`, but **`rc-disagree` is never
emitted by the code** — `grep -n 'rc-disagree' tools/round-95/c1-agreement-v2.py`
matches only that docstring line. The round-94 counter it inherits has no typed
reasons at all (three booleans `valid`/`agree`/`predicted`; the rc is folded into
`agree` at `tools/round-94/c1-receipt-agreement.py:70-75`). A probe (fixture: receipt
`exit 1`, stdout agreeing, `.rc` file `7`) run through
`c1-agreement-v2.py --dir <fx> --prefix p --case F1` returned the reason list
`["stdout-disagree", "pins-not-bound"]` — the rc mismatch is reported **under
`stdout-disagree`**, because the receipt/stdout/rc triple is compared as one
conjunction. The three reasons the code can actually emit for the inherited atoms
are `not-valid`, `stdout-disagree`, `predicted-mismatch`
(`c1-agreement-v2.py:104`, `:117`, `:129`). Impact on the claim: none — the four world
bindings, the four intended reasons and the honest leg are unaffected, and the
committed receipt is unchanged. The knowledge draft states the observed behaviour
rather than the docstring's list. The L1 and the canonical judge should note that the
v2 docstring overstates the inherited reason vocabulary.

**F2 (a supporting measurement that strengthens section (b)).** On this host
(Python 3.14.8) `tempfile.mkstemp` opens its temp file with
`_os.O_RDWR | _os.O_CREAT | _os.O_EXCL | _os.O_NOFOLLOW` (`os.O_NOFOLLOW` = 131072,
present). So the standard library applies the man page's own trailing-component rule
directly, in addition to the name being unpredictable; the generated name
(prefix + random + suffix, observed `x.gobplze2.tmp`) does not coincide with a
pre-planted `<json-out>.tmp`. Recorded in the knowledge draft and `verify.md` (V4).

**F3 (cross-check on a sibling's draft, read-only).** The seat's own files do not
include craft block 34 — that is seat `ScribeC2Block`. As a read-only cross-check,
each frozen manifest row of `.ufo/waves/round-95/manifests/block34-after.json` was
tested against `w1/ScribeC2Block/quality-rows.md`: exactly one of QUALITY 191/192
carries **all** of that row's frozen keywords
(`consistent label rewrite` → 191; `counts that do not recompute the label` → 191;
`revision field not the measured tree` → 192; `temp-file symlink escape` → 192). No
sibling file was edited and no claim of this seat depends on it.

**F4 (a landing requirement, flagged for the L1).** The S320 row's `used-by` names
`corpus/knowledge/2026-11-05-r95-receipt-world-binding.md` and
`corpus/lessons/round-95.md`, neither of which exists at `4bda1d1d`. The row, the
knowledge file and the lesson file must land in the same commit or the census fires
`E11` (measured: run A vs run B above). Recorded as row M95-a in the lesson draft.

## Out of scope (deliberately not done)

- The round-95 counters were not re-run at a different revision (the claim forbids
  re-measuring a different revision; the L1 already measured at `4bda1d1d`).
- Craft block 34 and QUALITY 191/192 were not drafted — they are seat
  `ScribeC2Block`'s item. This seat only cross-checked the sibling's draft.
- The `## Mistakes` section does not assert any round-95 mistake beyond the three
  carried round-94 defects (M94-e, M94-f, SentinelWrite F1) that the committed
  receipts support; a placeholder marks where the L1 appends the wave's own findings.
- No lane file was edited; no git mutation was run in the lane; no host state was
  changed; no pacman transaction was run; no tool was installed or upgraded
  (python 3.14.8, git 2.56.0, curl 8.23.0, gawk 5.4.1, bash 5.3.20 were already
  present), so the tooling directive has nothing to record.
- The scratch dir `/fast/scratch/hyaku/kaidoku-r95/ScribeKnowledge` was deleted
  before this report was written.

## Reproduce

```
S=/fast/scratch/hyaku/kaidoku-r95/ScribeKnowledge; mkdir -p "$S/tmp" "$S/work"
git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
git -C "$S/clone" checkout -q 4bda1d1dd3788973f10e61212b70df18b3b14ea0
git -C "$S/clone" rev-parse --show-toplevel   # must equal $S/clone
# insert SEAT/s320-row.md after the S319 row of $S/clone/corpus/SOURCES.md
# copy every mined row's used-by path from $S/clone into SEAT/validate/ at the same relative path
# copy SEAT/knowledge.md -> SEAT/validate/corpus/knowledge/2026-11-05-r95-receipt-world-binding.md
# copy SEAT/lesson-drafts.md -> SEAT/validate/corpus/lessons/round-95.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScribeKnowledge/validate/corpus/SOURCES.md
```

Exit 1 with the two `E11` lines when the two consumers are absent; exit 0 with no
finding against S320 when they are present.
