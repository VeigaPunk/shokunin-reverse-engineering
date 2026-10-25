# ACensusNow — round-34 (r34b) wave 2: registry census of `kaidoku`

Seat: census/queue cross-check for the R34-C2 stop attack. Assigned scope (verbatim): run
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`, report exit, row counts
by tier and any W/E findings; then count data rows and ids in `corpus/SOURCES.md` with two
independent patterns honouring 0–3 leading spaces.

Nothing here reopens R34-C2, repairs a frozen instrument, edits a registry/doc/receipt, or awards a
score. All VCS calls are read-only (`git status`, `git log`, `git show`, `git diff`, `git
cat-file`, `git ls-tree`); no add/commit/stash/checkout/reset/pull/push, no jj mutation.

## Headline

- Assigned command: **exit 0**, lane `kaidoku` → `ok`, **0 E**, **9 × W04**, first run
  `2026-10-25T07:28:09Z`. The output is **byte-identical** (`sha256 340e91f6…`) to the wave-start
  receipt `.ufo/waves/round-34/r34b/census-start.txt`, and stayed identical on two later byte
  states (§2). The registry is contract-clean in every state I measured.
- **Two independent patterns agree**: 105 rows / 105 unique ids on the pre-edit bytes, **106 / 106**
  on the bytes present now (a third, cut-based extractor and 108−2 structural arithmetic agree).
- **The registry moved four times during this wave**, and one of those states was **committed**:
  landing commit `66b84027` ("… land the stopped claim's record — … S106, knowledge entry …",
  `2026-10-25T07:32:25Z`) **contains no `S105` row**, while **12 citations** in
  `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`, `corpus/lessons/round-34.md`,
  `corpus/QUALITY.md`, `SCORECARD.md` and `LOG.md` point at S105. The row was restored 30 s after
  the commit and **that restore is still uncommitted** (` M corpus/SOURCES.md`).
- Also still true from the frozen tree: `c79bbe7b` names `S106` as the round's only
  `sources_opened_this_round`, but that revision contains **no S106 row**. The citation was
  backfilled only after the freeze.
- Both are record defects of the A/5/F5 family, not capability data. Candidate id **F6**; the L1
  lands, I do not.

## 1. Assigned run (exact argv, exits, UTC)

```
$ cd /home/vgpnk/Projects/shokunin
$ date -u +%Y-%m-%dT%H:%M:%SZ            # 2026-10-25T07:28:09Z
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
EXIT=0
```

E-findings: 0 (`grep -cE '\tE[0-9]+\t'` over the captured output = 0). W-findings: 9, all `W04`
(same URL across scopes); by the script's own contract W-codes never change lane status.

Reproduced verbatim on the later byte states:

| run UTC | `file` sha256 | exit | E | W | same bytes as census-start? |
|---|---|---|---|---|---|
| 07:28:09Z | `5abcd365…` | 0 | 0 | 9 | yes — `diff -u … census-start.txt` rc 0 |
| 07:30:25Z | `3c79e486…` | 0 | 0 | 9 | yes — captured `sha256 340e91f6…` |
| 07:33:21Z | `77707752…` | 0 | 0 | 9 | yes — `diff` rc 0, captured `340e91f6…` |

Consequence: the W04 set predates the wave (census-start mtime `04:04 −03:00` = `07:04Z`, before
the `07:13:11Z` freeze) and is invariant across three different registries. It is background, not a
wave-1 artefact, and it cannot be used either way on the stop.

## 2. The file moved four times; only sha256 keeps the epochs apart

| state | bytes present in | sha256 | size | rows | id set | tier A/B/C | mined/rejected |
|---|---|---|---|---|---|---|---|
| A | `8897a67` blob = frozen `c79bbe7b` blob = my 07:28:09Z read | `5abcd365…` | 122580 | 105 | S001…S105 | 99/5/1 | 101/4 |
| B | worktree at `07:29:16Z` (transient) | `3c79e486…` | 124743 | 105 | S001…S104, **S106** (no S105) | 99/5/1 | 102/3 |
| C | **committed** `66b84027` at `07:32:25Z` | `3c79e486…` (same blob as B) | 124743 | 105 | same as B | 99/5/1 | 102/3 |
| D | worktree at `07:32:55Z` → still current at `07:34:12Z` | `77707752…` | 125359 | **106** | S001…S106, monotonic | **100/5/1** | 102/4 |

Evidence (each value measured, not inferred):

```
$ stat -c '%y %s' corpus/SOURCES.md
2026-10-25 04:29:16.860582856 -0300 124743     # B written = 07:29:16Z
2026-10-25 04:32:55.203689238 -0300 125359     # D written = 07:32:55Z
$ git cat-file -s HEAD:corpus/SOURCES.md ; git cat-file -p HEAD:corpus/SOURCES.md | sha256sum
124743
3c79e486cbf77be968f3db7a1b16353c2ce0fde70bc84d1f2a5b4f086e109209  -
$ git log -1 --format='%H %cI %s'
66b840274390d0868c913a544947f9eb40a4ffe6 2026-10-25T04:32:25-03:00
round-34: land the stopped claim's record — SCORECARD section, LOG entry, lesson M34-5..M34-11, QUALITY 68-73, SKILL instrument registry, S106, knowledge entry and README rows
$ git status --porcelain -- corpus/SOURCES.md
 M corpus/SOURCES.md
```

`census` mode tracked the change exactly as the tool saw it:

```
# 2026-10-25T07:28:16Z (state A)
kaidoku	rows	105   tier.A 99   tier.B 5   tier.C 1   status.mined 101   status.rejected 4
# 2026-10-25T07:30:14Z (state B)
kaidoku	rows	105   tier.A 99   tier.B 5   tier.C 1   status.mined 102   status.rejected 3
# 2026-10-25T07:33:21Z (state D)
kaidoku	rows	106   tier.A 100  tier.B 5   tier.C 1   status.mined 102   status.rejected 4
FLEET rows 106 / tier.A 100 / tier.B 5 / tier.C 1 / tier.invalid 0 / status.queued 0 /
FLEET status.mined 102 / status.rejected 4 / status.invalid 0 / missing 0
```

(`kaidoku` is the only lane passed, so `FLEET` equals the lane; no sibling registry was read.)

## 3. Two independent patterns (0–3 leading spaces honoured)

State D — current bytes `sha256 77707752…`, 125359 B, measured `2026-10-25T07:32:25Z–07:34:12Z`:

**P1 — file-wide row regex.** `[[:space:]]` admits 0–3 indent; anchored on `\|`:
```
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
106
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort -u | wc -l
106
```

**P2 — section-scoped `awk -F'|'` field parse**, independent of the id regex: re-derives the
`## Registry` section from headings, normalises the split to exactly 11 cells (`n==12` counting the
leading empty field), and requires cell 1 to full-match `^S[0-9]{3,}$`:
```
$ awk '… registry section; n==12 && id ~ /^S[0-9][0-9][0-9]+$/ …' corpus/SOURCES.md
106                       # rows
106                       # unique ids (array length)
tier.A=100  tier.B=5  tier.C=1
```

**P3 (bonus, orthogonal tool)** — `cut -d'|' -f2` unique ids: 106. **Structural arithmetic**:
108 table lines in `## Registry` − header − separator = **106** data rows.

Raw-cell tallies agree with the tool: `cut -f5` → 100 A / 5 B / 1 C; `cut -f9` → 102 mined /
4 rejected.

State A (pre-edit, `5abcd365…`): P1 105 rows / 105 unique ids, P2 (awk split) 105 / 105.
State B (`3c79e486…`): P1 105 / 105, P2 105, P3 105. The id hole then was exactly `S105`
(`MISSING 105..105`, ids `S001…S104 + S106`); state D closes it (`unique=106`, monotonic, no gaps,
no duplicate ids).

Indentation is inert here: `grep -cE '^ +\|'` = 0 — every registry row sits at column 0, so the
parser's 0–3-space latitude (exercised by the script selftest at widths 0/1/2/3) is unused by the
real file.

## 4. Defect: the landing commit for the stop's record deleted `S105` (candidate F6)

```
$ git show 66b84027 --unified=0 -- corpus/SOURCES.md | grep -E '^[+-]\| S'
-| S105 | System V ABI draft — https://www.sco.com/developers/gabi/latest/contents.html | spec | A | Candidate authority for GNU …
+| S106 | GNU binutils readelf version-needs reader — https://sourceware.org/git/?p=binutils-gdb.git;a=blob_plain;f=binutils/readelf.c;hb=6ce87bbc… | code | A | …
$ git log --oneline -S'S105 | System V ABI draft' -- corpus/SOURCES.md
66b84027 …                                   # the deleting commit is the landing commit itself
8897a67f …                                   # the commit that introduced the row
$ git cat-file -p HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S105[[:space:]]*\|'
0
$ git cat-file -p HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S106[[:space:]]*\|'
1
```

Why it matters, stated as facts:

- `S105` is cited **12 times** across `corpus/knowledge/2026-10-23-r34-elf-version-needs.md`,
  `corpus/lessons/round-34.md`, `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md` and
  `corpus/SOURCES.md` (`grep -rno 'S105' corpus/ SCORECARD.md LOG.md SKILL.md | wc -l` = 12).
  At `HEAD` the registry has no row to resolve those citations to — the committed record is
  internally dangling, exactly in the S105/S100 CHPE-rejection lineage the same commit edits.
- The row was **restored 30 s later** (state D) and is **byte-identical to the frozen row**
  (`git cat-file -p c79bbe7b:corpus/SOURCES.md | grep '^| S105' | sha256sum` =
  `grep '^| S105' corpus/SOURCES.md | sha256sum` = `2912dcb9…`), i.e. an accidental
  delete-during-insert, not an editorial supersede. The restore is **uncommitted**.
- `validate` cannot see any of this: it returned `ok` on A, B and D with the *same* bytes
  (`340e91f6…`). E03/E04/E11 all operate on what is present, never on what a citation needs, and
  E11 is a filesystem-presence test (`test -e` on `used-by`), so an untracked target satisfies it.

The defect is therefore the same shape as disclosed F5 ("receipts were untracked at first audit
time"), now one layer down: the artefact is the registry itself, the untracked item is the repair,
and the committed tree is the thing that is wrong. I draft nothing beyond this sentence: the L1
decides whether F6 enters the stop record, and the only faithful fix is to land the already
byte-identical S105 row (or to disclose the hole), not to touch frozen instruments.

## 5. Frozen-tree cross-check: the claim's only opened source postdates its own freeze

```
$ git log -1 --format='%cI %s' c79bbe7b
2026-10-25T04:13:11-03:00                    # = 2026-10-25T07:13:11Z
round-34: freeze R34-C2 pre-freeze shortcut-replay gate …
$ git cat-file -p c79bbe7b:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S106[[:space:]]*\|'
0
$ git cat-file -s c79bbe7b:corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md
fatal: path '…-stop.md' exists on disk, but not in 'c79bbe7b…'
$ git ls-tree -r --name-only c79bbe7b | grep -c r34b
1                                            # only .ufo/waves/round-34/r34b/claims.json
$ git cat-file -p c79bbe7b:.ufo/waves/round-34/r34b/claims.json | sha256sum   # == worktree
de3afbfb61d70fee177392b256719bb665ad07d999303999381442120facd828  -
```

The frozen claim revision pins `"sources_opened_this_round": ["S106"]` (26 pins, pins byte-identical
to `.ufo/waves/round-34/r34b/instruments.json`'s 26-entry map — consistent with the disclosed F1
container repair), yet at that same revision the registry has no S106 row, the stop knowledge doc
does not exist, and the only r34b path in the tree is `claims.json`. The citation was made good at
`07:29:16Z`/`07:32:25Z`, i.e. **after** the freeze, and its knowledge target is still tracked only
because commit `66b84027` happened to include it.

## 6. Bearing on the stop

- The census neither rescues nor contradicts the stop. It is a cleanliness datum: the registry is
  contract-clean on every state I ran (0 E, 9 pre-existing W04), so no E/W finding can be used to
  argue the R34-C2 measure was wrong; nothing here touches the GREEN/red verdicts, the seven
  registered classes, the frozen counter, the 8/8 target, or `owned scores 10→10`.
- It adds negative pressure on the **record** arm only: a stop whose authority is "frozen at
  `c79bbe7b`" now has (i) a citation in its claim that is absent from the frozen tree, and (ii) a
  landing commit that deleted a registry row still cited 12 times, with the repair left uncommitted.
  Neither is a capability datum, and neither justifies reopening or scoring.
- No score is awarded or implied by this seat.

## 7. Risks / blockers

- Any census or validate receipt produced during this wave must pin `sha256` of the file it read —
  mine: `5abcd365…` (07:28:09Z), `3c79e486…` (07:30:25Z), `77707752…` (07:33:21–07:34:12Z). A
  path-only receipt would have silently blended four different registries, and the *findings* were
  identical across all of them, so findings alone cannot detect the drift.
- The worktree is still dirty (` M corpus/SOURCES.md`); `HEAD` currently under-reports the registry
  by one row (S105) and is therefore the version a fresh reader would get.
- No blockers: the assigned command ran, both independent counts closed on every state, and every
  number above carries a command, exit and UTC.

## 8. Tooling

No installs or upgrades (nothing needed): host bash/coreutils/gawk/python3 plus read-only git
plumbing only. No pacman transaction attempted. No ELF carrier, fixture, reader or counter executed;
no build, lint or bulk test suite run.

## Verdict

**`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, lane `ok`,
0 E / 9 W04, byte-identical findings (`340e91f6…`) on three different byte states; `SOURCES.md`
counts 106 data rows and 106 unique ids at `sha256 77707752…` by three independent patterns
(105/105 on the pre-edit bytes `5abcd365…`), tiers 100 A / 5 B / 1 C, status 102 mined / 4
rejected; and the stop's own landing commit `66b84027` committed a registry missing `S105` — a row
cited 12 times, with the byte-identical restore left uncommitted — while the frozen revision
`c79bbe7b` cites `S106` as its only opened source before that row exists: two F5-class record
defects (candidate F6), not capability data, and no score moves.**
