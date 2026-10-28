# ScribeSources — round 47, wave 1

Gesture: draft the round's `corpus/SOURCES.md` rows, open every URL myself, verify the landed rows
rather than assume them, and reject what does not earn an id.

**Snapshot.** Sources measured `2026-10-28T17:49Z–17:54Z`; the lane's HEAD moved during the seat
(`3186f69b → 1e2c3102 → 04469ee8 → f54b3b6d → a0753786`). Every lane fact below names the revision
or the UTC time at which it was read; findings F4/F5 are about that movement, so the times are part
of the evidence.

**Verdict on my own deliverable:** two new admitted rows (`S145`, `S146`), two landed rows verified
sound (`S143` admitted, `S144` rejected), one candidate refused as a duplicate (`S142`), one optional
scope repair offered for `S143`. Nothing was written into `corpus/SOURCES.md`,
`corpus/lessons/round-47.md`, `SKILL.md`, `SCORECARD.md`, `plans/` or `tools/`.

## Behaviour

1. Read `plans/round-47-claims.md` in full before the first command; took the row shape and the
   round's obligations from it, not from the prompt.
2. Ran registry-first: census, next free id, and three duplicate checks *before* opening a page.
   The registry maximum at the first freeze (`5017e1f7`) is `S142`; in the worktree at measurement
   time it was `S144` (the S143 and S144 rows arrived in `e856beb5`), so the next free id is `S145`.
3. Opened six URLs directly with `curl`, recording HTTP status, byte count, page sha256 and UTC time
   for each, and located every quote by searching the fetched bytes.
4. Independently reproduced the pins of the two landed rows (`S143`, `S144`) instead of trusting them.
5. Grepped the two counters for the facts the new rows teach (`sys.path` inserts at
   `exact.py:23-24`, `record.py:28-29`; `set` usage at `exact.py:143,269`, `record.py:110-112`), so no
   row rests on a claim I did not read in the code.
6. Probed the counter's own freeze gate at four successive declared freeze pointers, because the
   frozen set includes a file (`record.py`) that the *other* claim owns.

## Gates

Exits are semantic: `0` met, `1` not met, `2` could-not-evaluate. Every receipt line in
`ScribeSources/receipts*.jsonl` carries argv, exit, stdout sha256, stdout bytes and UTC. The drivers
are committed beside them (`receipts.py`, `receipts2.py`, `receipts3.py`), so each pass is
re-runnable; page pins are summarised in `ScribeSources/pins.json`.

| gate | command (abbreviated) | exit | result |
|---|---|---|---|
| registry census | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `144` rows; next free `S145` |
| `re` page pin | `curl -sS -o re.html -w 'http=%{http_code} bytes=%{size_download}' https://docs.python.org/3/library/re.html` | 0 | HTTP 200, 257,706 B, sha256 `f169ed065bf6e6ad779dd7049e6e4ce4ac1081c10eb3f40cd079b0a1f9d11f6a` — **equals S143's landed pin** (R01) |
| `re.fullmatch` anchor | `grep -c 'id="re.fullmatch"' re.html` | 0 | `1` (R02) |
| `re` version marker | `grep -o 'Python 3\.1[0-9]' re.html` | 0 | `3.15` (R04) — the `/3/` alias is development docs |
| `re` 3.14 pin | `curl … https://docs.python.org/3.14/library/re.html` | 0 | HTTP 200, 250,047 B, sha256 `755a744674c17bdfa46b2753508b89e3e2431b1621a1f481290af521819cec7e` (R05); its `re.fullmatch` extraction is **byte-identical** to `/3/`'s (both sha256 `58c6c5854e67…`, R03 = R06) |
| `-I` passage | `curl … /3/using/cmdline.html` | 0 | HTTP 200, 171,073 B, sha256 `c19141f2030687e14e00e73fff1ed482c3608813dfdc66a0b0931b92bb2902ac`; "Run Python in isolated mode. This also implies -E, -P and -s options." (R07/R08) |
| `-B` passage | extraction of "won’t try to write .pyc files" | 0 | located (R09) |
| `-I` at 3.14 | `curl … /3.14/using/cmdline.html` | 0 | HTTP 200, 160,951 B, sha256 `a1ebda77…`; extraction identical to `/3/`'s (`a46120cb6617…`, R11 = R08) |
| hashlib passage | `curl … /3/library/hashlib.html` | 0 | HTTP 200, 121,928 B, sha256 `fc778efd702a9324aa999577997ac2231c84567f79f134ba6a3cb252127be6c1`; "digest of the concatenation of the data fed" located (R12/R13) |
| HOWTO reject claim | `grep -c fullmatch regex.html` | 0 | `0` — and `0` in tag-stripped text too; S144's rejection is factually right (R14/R15) |
| `--diff-merges` duplicate | `curl … https://git-scm.com/docs/git-log` | 0 | HTTP 200, 375,834 B, sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a` — **equals S142's pin** (R16) |
| interpreter | `python3 -V` | 0 | `3.14.8` (R17) |
| `-I` flags live | `python3 -I -B -c '…sys.flags…'` | 0 | `isolated 1 nowrite 1 safe_path 1 ignore_env 1 no_user_site 1` (R18) |
| `-I` ignores PYTHONPATH | `PYTHONPATH=/evil python3 -I -B -c '…'` vs without `-I` | 0/0 | `False` under `-I`, `True` without (S01/S02) — the flag discriminates |
| `-I` path0 | `python3 -I -B -c '…sys.path[0]'` vs bare | 0/0 | `'/usr/lib/python314.zip'` vs `''` (S03/S04) |
| frozen tree at the first freeze | `git ls-tree -r --name-only 5017e1f -- tools/round-47/` | 0 | exactly `exact.py`, `record.py` (R23) |
| frozen path now | `git hash-object tools/round-47/{record,exact}.py` vs `git rev-parse 5017e1f:…` | 0/0 | at 17:54:20Z `exact.py` unchanged (`fb21a166`), `record.py` `ace4f6df` ≠ `1f8e7928` (S05/S06); by 17:58:54Z `exact.py` had moved too (`dd17c33a`) |
| worktree cleanliness | `git status --porcelain tools/round-47/` | 0 | empty at 17:54:20Z (S08) — the change was committed, not staged |
| `__pycache__` in the frozen path | `find tools/round-47 -name '*.pyc'`; `git check-ignore -v …` | 0/0 | two `.pyc` files, ignored by `.gitignore:1:__pycache__/`, absent from the frozen tree (S09/S10) |
| C1 counter at freeze `5017e1f` | `python3 -I -B tools/round-47/exact.py --root … --freeze 5017e1f --rev HEAD --no-battery` | **2** | `frozen_path_changed: ["plans/round-47-claims.md","tools/round-47/","tools/round-47/record.py"]` (T01) |
| C1 counter at freeze A1 `9018c53b` | same, `--freeze 9018c53b` | **2** | same reason and same three paths (T02) |
| C1 counter at freeze A4 `1e2c3102` | same, `--freeze 1e2c3102` | **2** | `frozen_path_changed: ["tools/round-47/","tools/round-47/record.py"]` (T03) |
| C1 counter at freeze A5 `07d2894e` | same, `--freeze 07d2894e` | **2** | `frozen_path_changed: ["tools/round-47/","tools/round-47/exact.py"]` (T04) |

**Discarded measurements (disclosed).** (a) The first pass stored the `PYTHONPATH` probe's env dict in
the wrong parameter, so both arms ran without it and returned identical stdout (sha256
`7fc755fadc1b…` both). `R19`/`R20` are left in `receipts.jsonl` unchanged and are **not** evidence;
`receipts2.jsonl` `S01`/`S02` replace them and do discriminate. (b) A first `T04` run fed
`git rev-parse 07d2894e^!`, which prints commit *and* parent, so the counter exited 2
`unknown freeze revision`; that run is not cited — `receipts4.jsonl` re-runs it with
`git rev-parse --verify 07d2894e^{commit}`.

## Touched surfaces

- Written: `.ufo/waves/round-47/w1/ScribeSources.md`, `.ufo/waves/round-47/w1/ScribeSources/{sources.md,
  receipts.jsonl, receipts2.jsonl, receipts3.jsonl, receipts4.jsonl, pins.json, receipts.py,
  receipts2.py, receipts3.py}`.
- Read-only: `plans/round-47-claims.md`, `corpus/SOURCES.md`, `corpus/lessons/round-47.md`,
  `SKILL.md`, `tools/round-47/{exact,record}.py`, `tools/round-46/gate.py`, `.gitignore`, and
  `git log/show/hash-object/rev-parse/ls-tree/status`.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r47/ScribeSources` removed after the receipts were copied.
  Nothing was written under `/tmp`; no git/jj mutation was issued in the lane or in a fixture; the
  counter probe used `--no-battery` and no `--json-out`, so it wrote no file inside the lane.
- Installs: **none** (`curl`, `python3`, `git` already present).

## Findings

**F1 — S143's pin reproduces exactly; its URL is a moving alias.** HTTP 200, 257,706 B,
`f169ed06…` on two independent fetches, matching the landed row. But `/3/` served **Python 3.15
development** docs, while the counting command runs **3.14.8**. The teaching is not version-sensitive
— the `re.fullmatch` passage and the `-I` passage both extract byte-for-byte identically from `/3/`
and `/3.14/` (identical extraction sha256) — so this is a scope-wording repair, not a defect. Exact
replacement sentence in `ScribeSources/sources.md` § "One recommended repair".

**F2 — S144's rejection claim is true.** `fullmatch` occurs `0` times in the fetched bytes and in the
tag-stripped text; the pin `5e205f7d…`/165,172 B matches the landed row. No change needed. This seat
reached the same source and verdict independently and therefore adds no second rejected id.

**F3 — `tools/round-47/__pycache__/` exists inside a declared frozen path.** Two `.pyc` files
(`exact.cpython-314.pyc`, `record.cpython-314.pyc`), matched by `.gitignore:1:__pycache__/` and absent
from `git ls-tree 5017e1f -- tools/round-47/`, which holds exactly two files. Not a freeze violation
today, but it proves a counter run without `-B` already happened in the frozen directory, and a freeze
set computed by directory listing (or `git add -f`) would absorb it. `-B` prevents new writes; it does
not remove these.

**F4 — the claims file declares two amendments; the repo carries six.** At `a0753786`
(`2026-10-28T17:58:54Z`):

```
$ git log --format='%h %s' 5017e1f..HEAD -- tools/round-47/ plans/round-47-claims.md | wc -l
6
```

`A1 9018c53b`, `A2 62e33f7d`, `A3 2e4ae434`, `A4 1e2c3102`, `A5 07d2894e`, `A6 f54b3b6d`. The claims
file (`plans/round-47-claims.md:23-41`) contains disclosure paragraphs for **A1 and A2 only** and
states "the freeze is a series of **two**, disclosed". A3 (`record.py +11/−2`), A4 (`+3/−1`), A5
(`+7/−1`) and A6 (`exact.py`, citing `f54b3b6d`) change the frozen instruments with no claims-file
paragraph; A2 additionally rewrote `SKILL.md` *after* the landing commit `e856beb5`, so block 24's arm
cells were re-written post-landing. `corpus/lessons/round-47.md:3-4` and `.ufo/waves/round-47/` receipts
do record A5/A6 — the stale document is the claims file, i.e. the round's own rule. Either extend it to
A3–A6 or re-declare the freeze at the last commit that touches those paths. This is the same defect
class the round exists to close (a record that disagrees with the repo), now sitting in the record of
the freeze itself.

**F5 — the freeze gate makes every earlier freeze pointer unscoreable for *both* claims, so "causal
separation" holds for data but not for scoring.** `gate.freeze_state` (`tools/round-46/gate.py:144-199`)
derives the frozen set at both ends, unions it, and returns 2 when any entry is `touched` or
`blob_changed` between freeze and rev — and `tools/round-47/` is a directory entry in that set, so *any*
child change reports the directory too. Measured, at `HEAD=a0753786`:

| `--freeze` | exit | `frozen_path_changed` |
|---|---|---|
| `5017e1f` (first freeze) | 2 | `plans/round-47-claims.md`, `tools/round-47/`, `tools/round-47/record.py` |
| `9018c53b` (A1, the claims file's "declared freeze") | 2 | same three |
| `1e2c3102` (A4, the lesson's declared freeze) | 2 | `tools/round-47/`, `tools/round-47/record.py` |
| `07d2894e` (A5) | 2 | `tools/round-47/`, `tools/round-47/exact.py` |

C1 never reads `record.py`, yet a C2-only commit to `record.py` blocks C1's score; the converse holds
for A6's `exact.py` edit against C2. The claims file's "Causal separability … Either lands and scores
without the other" is therefore true of *what each counter reads* and false of *what each counter can
be scored against*: only the newest commit touching `tools/round-47/` or `plans/round-47-claims.md` is
a scoreable freeze, and any landing after it re-blocks both.

**F6 — worktree-dirty is a distinct exit and was live during this seat.** `freeze_state` returns
`2 frozen_worktree_dirty` for an uncommitted change to a frozen path (`gate.py:186-191`), separately
from `2 frozen_path_changed`. At `~17:50Z` `tools/round-47/record.py` was dirty (blob `79fb27a8`,
`+3/−5`, removing the window-pair binding); by `17:54:20Z` the tree was clean and the change had
landed as A1. A counter receipt from that window that exits 2 for a *dirty* frozen path is reporting
the environment, not the claim — but note it is the same instrument the A1 paragraph describes, so the
two reasons must not be conflated when the L1 reconciles sibling receipts.

**F7 — checked, not a defect.** Because `-I` ignores every PYTHON* variable, `PYTHONHASHSEED` cannot be
pinned, so any set-derived output order would be run-unstable. It is not: `exact.py:143,269` uses the
set only for membership and sorts before emitting, and `record.py:110-112` uses `mapped` only in
`stems & mapped`. No receipt of either counter depends on hash order.

## Out of scope (not attempted, by contract and by seat)

- Did not run `record.py`, did not build the C1 battery (`--no-battery`), did not score either claim,
  and did not read `l1/scores/*.json` — scoring is the L1's and the reviewers' seats.
- Did not edit frozen bytes, `SKILL.md`, `SCORECARD.md`, `corpus/`, `LOG.md`, or any sibling lane, and
  issued no mutating git/jj command.
- Did not fetch PDF/HTML mirrors of any source and did not search beyond the six URLs named in the
  seat brief plus the four version/duplicate controls.

## Artifact paths

- `ScribeSources/sources.md` — the drafts: two ready-to-paste 11-column rows, the verification of the
  landed rows, the optional S143 repair, the duplicate refusal, and the landing conditions
  (census `142 → 146`, two lesson table lines, two `**Admit**` lines).
- `ScribeSources/receipts.jsonl` — 33 receipts, pass 1 (includes the two discarded env probes).
- `ScribeSources/receipts2.jsonl` — 14 receipts, pass 2 (env repair + frozen-path re-measurement).
- `ScribeSources/receipts3.jsonl` — 3 receipts, pass 3 (freeze gate at `5017e1f`, A1, A4).
- `ScribeSources/receipts4.jsonl` — 1 receipt, pass 4 (freeze gate at A5).
- `ScribeSources/pins.json` — the seven page pins (http, bytes, page sha256, fetch UTC).
- `ScribeSources/receipts{,2,3}.py` — the drivers that produced them.

Report: .ufo/waves/round-47/w1/ScribeSources.md
