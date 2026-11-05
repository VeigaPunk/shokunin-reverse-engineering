# Seat ScribeKnowledge — verification record

Seat directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScribeKnowledge/`
Scratch (deleted before yield): `/fast/scratch/hyaku/kaidoku-r95/ScribeKnowledge`
Clone: `git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"`,
then `git -C "$S/clone" checkout -q 4bda1d1dd3788973f10e61212b70df18b3b14ea0`.
`git -C "$S/clone" rev-parse --show-toplevel` → `/fast/scratch/hyaku/kaidoku-r95/ScribeKnowledge/clone`
(asserted before any write into the clone). The lane was never mutated: only
`git -C … log/show/diff/status/rev-parse/cat-file/ls-tree/grep`-class reads were run
against the lane, and the clone is a separate `--shared` clone.

## V1 — the S320 row parses in the registry, and its `used-by` consumers resolve

**Fixture.** The registry copy under test is
`SEAT/validate/corpus/SOURCES.md` — the clone's `corpus/SOURCES.md` at
`4bda1d1dd3788973f10e61212b70df18b3b14ea0` with the draft row
`SEAT/s320-row.md` inserted directly after the `S319` row (line 236).

Because `sources-census.sh --file` resolves `used-by` paths relative to the
**parent of the registry file's directory** (`resolve_targets`: `dir_abs=$(realpath
-- "$(dirname -- "$file_abs")/..")`), the fixture root is `SEAT/validate/`. So that
the run measures the new row rather than a wall of unrelated dangling `used-by`
findings, every path named in a `mined` row's `used-by` cell was copied from the clone
into `SEAT/validate/` at the same relative path (152 paths, 0 missing in the clone).

**Command.**

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScribeKnowledge/validate/corpus/SOURCES.md
```

**Run A — the row present, its two `used-by` consumers absent.** Exit **1**.

```
file	E11	S320 missing used-by corpus/knowledge/2026-11-05-r95-receipt-world-binding.md
file	E11	S320 missing used-by corpus/lessons/round-95.md
```

Those are the only two `E*` lines in the whole run (`grep -P '\tE[0-9]+\t'` returns
exactly the two lines above). 32 `W04` lines, identical id-for-id to the round's
committed before-receipt `.ufo/waves/round-95/census-before.txt` (diff of the
sorted `W04\tS…` id sets: identical) — the new row adds no duplicate-URL warning,
because `man7.org/linux/man-pages/man2/open.2.html` is not in the registry yet.
Receipt: `receipts/census-runA.out`, `receipts/census-runA.err` (empty),
`receipts/census-runA.rc` (`1`).

**Run B — the row present, both `used-by` consumers present** (the knowledge file
`SEAT/knowledge.md` copied to `SEAT/validate/corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`,
and the lesson draft `SEAT/lesson-drafts.md` copied to
`SEAT/validate/corpus/lessons/round-95.md`). Exit **0**.

```
file	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScribeKnowledge/validate/corpus/SOURCES.md
```

No `E*` line at all; no finding of any code against `S320` (`grep -P '\tS320\t'` on
the output returns nothing); the same 32 `W04` lines as before. Exit **0**.
Receipt: `receipts/census-runB.out`, `receipts/census-runB.err` (empty),
`receipts/census-runB.rc` (`0`).

**Row shape checks (own script, not a lane instrument).** The row splits into
exactly **11** cells; no cell contains a `|`. The cell values are: id `S320`; kind
`docs` (in the census kind enum); tier `A`; status `mined`; opened `2026-11-05`
(≤ today 2026-11-05, so `E08` does not fire); recheck `on-release` (a symbolic
cadence, so `E09` does not fire); `used-by` = the two paths above, comma-separated.

## V2 — the S320 source: byte-identical committed fetches, and a live re-fetch

Committed fetches (read-only, in the lane):
`sha256sum .ufo/waves/round-95/l1/scores/s320-open2-fetch{1,2}.html` → both
`d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`; both 76506 bytes.
This matches the digest named in `plans/round-95-claims.md` and in
`.ufo/waves/round-95/claims.json` (`fetch_sha256`).

Live re-fetch by this seat (2026-11-05, into scratch, no lane write):

```
curl -sS -o live-open2.html -w 'HTTP %{http_code} bytes=%{size_download} url=%{url_effective}\n' \
  https://man7.org/linux/man-pages/man2/open.2.html
→ HTTP 200 bytes=76506 url=https://man7.org/linux/man-pages/man2/open.2.html
sha256sum live-open2.html → d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789
```

Copied into the seat as `receipts/s320-open2-live-refetch.html` with
`receipts/s320-live-refetch.sha256`.

**The located quote.** Measured on the committed fetch with a tag-strip +
entity-decode + whitespace-normalise pass:

- raw contiguous byte substring of the HTML: **absent** (the sentence is split across
  three lines and carries `<i>`/`<b>` markup);
- after normalisation: **present**, exactly:
  `If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP`
  (followed in the normalised text by ` Symbolic links in earlier components of the pathname will still be followed.`).

The page footer reads `Linux man-pages 6.19            2026-02-08` and the provenance
block reads `This page was obtained from the tarball man-pages-6.19.tar.gz`.
`O_NOFOLLOW` occurs 5 times on the page; the quoted rule is the 2nd occurrence.

## V3 — the four bindings: a measured naming observation (no frozen byte changed)

The v2 module docstring lists the inherited atoms as `not-valid`,
`stdout-disagree`, `rc-disagree`, `predicted-mismatch`
(`tools/round-95/c1-agreement-v2.py:19`). A grep shows `rc-disagree` appears
**only** in that docstring line and is never emitted by the code; the round-94
counter it inherits has no typed reasons at all (three booleans `valid`, `agree`,
`predicted`; the rc is folded into `agree` at
`tools/round-94/c1-receipt-agreement.py:70-75`).

Measured with a probe in the clone (`receipts/v2-rc-mismatch-probe.py`): a fixture
whose receipt says `exit 1`, whose stdout line agrees, and whose `.rc` file says
`7`, run through
`tools/round-95/c1-agreement-v2.py --dir <fx> --prefix p --case F1`, returns the
reason list `["stdout-disagree", "pins-not-bound"]` — the rc mismatch is reported
**under `stdout-disagree`**, because the receipt/stdout/rc triple is compared as one
conjunction. The three reasons the code can actually emit for the inherited atoms
are `not-valid`, `stdout-disagree`, `predicted-mismatch`
(`tools/round-95/c1-agreement-v2.py:104`, `:117`, `:129`).

This is a naming observation only. It does not change any of the four world
bindings, does not change the committed measurement, and does not fire any kill-rule
clause: the committed forgery receipt
`.ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`
carries exactly the four intended reasons (`label-not-frozen`,
`label-not-recomputed`, `revision-not-bound`, `pins-not-bound`) and the honest leg
carries an empty reason list. It is recorded in the knowledge draft's section (c)
and flagged here for the L1 and the canonical judge.

## V4 — `mkstemp`'s own open flags on this host (supports knowledge section (b))

```
python3 -c "import tempfile,inspect; print(inspect.getsource(tempfile))"
→ _text_openflags = _os.O_RDWR | _os.O_CREAT | _os.O_EXCL
  if hasattr(_os, 'O_NOFOLLOW'): _text_openflags |= _os.O_NOFOLLOW
os.O_NOFOLLOW == 131072   (present on this host)
```

So `tempfile.mkstemp` opens its temporary file with `O_CREAT|O_EXCL|O_NOFOLLOW` on
Linux: the man page's trailing-component rule is applied by the standard library, in
addition to the name being unpredictable. The generated name is prefix + random +
suffix (observed `x.gobplze2.tmp` for prefix `x.`), so it does not coincide with a
pre-planted `<json-out>.tmp`. Python 3.14.8 on this host.

## V5 — the sibling craft draft's QUALITY rows carry the frozen keyword atoms

The seat's own files do not include craft block 34 (that is seat `ScribeC2Block`).
As a cross-check only, this seat read
`.ufo/waves/round-95/w1/ScribeC2Block/quality-rows.md` and tested each frozen
manifest row against it: for every row of
`.ufo/waves/round-95/manifests/block34-after.json`, exactly one of QUALITY 191/192
carries **all** of that row's frozen keywords —

| manifest row | QUALITY row carrying all its keywords |
|---|---|
| `consistent label rewrite` | 191 |
| `counts that do not recompute the label` | 191 |
| `revision field not the measured tree` | 192 |
| `temp-file symlink escape` | 192 |

This is a read-only cross-check on a sibling's draft file; no sibling file was
edited and no claim of mine depends on it.

## What was NOT run

- The round-95 frozen counting commands (the forgery battery, the honest v5 run, the
  symlink probe, the craft-citation and depth counters) were **not** re-run by this
  seat. The claim says the L1 already measured them at `4bda1d1d` and that the
  counters must not be re-measured at a different revision; this seat reads those
  committed receipts only.
- No host change was made, so there is nothing to file as a named host need.
- No tool was installed or upgraded (the census script, `curl`, `python3` and `git`
  were already present), so the tooling directive records nothing.
