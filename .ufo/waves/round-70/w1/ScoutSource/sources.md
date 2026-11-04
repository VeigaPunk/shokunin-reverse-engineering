# ScoutSource — round-70 w1: the environment-contract source, and the second-candidate screen

Seat: `ScoutSource` · wave `r70-w1` · access date **2026-11-04** (UTC 04:17:30Z)
Scope read: `tools/round-70/packed-elf.py` and `tools/round-70/seam-probe.py` at the frozen pins
(re-verified below). No repository edit was made; this file and the two snapshots beside it are the
only bytes this seat wrote in the lane tree.

## 1. Fetch evidence

Command (run with cwd = scratch root `/fast/scratch/hyaku/kaidoku-r70/ScoutSource`):

```
curl -sS -o <file> -w 'HTTP:%{http_code}\nBYTES:%{size_download}\n' <url>
sha256sum <file>
```

| candidate | URL | HTTP | bytes | sha256 | fetched (UTC) | page version |
|---|---|---|---|---|---|---|
| subprocess (primary) | `https://docs.python.org/3/library/subprocess.html` | 200 | 208 648 | `4b88b8316a05baadaa7b2dd254c320a40b5406d8158a57f2a50b55b4d872a2c7` | 2026-11-04T04:17:30Z | “Python 3.15.2 documentation” |
| tempfile (screen) | `https://docs.python.org/3/library/tempfile.html` | 200 | 75 198 | `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560` | 2026-11-04T04:17:30Z | “Python 3.15.2 documentation” |

Both snapshots were copied into this findings directory before the scratch root was removed, and the
copy was re-hashed: identical digests and byte counts.

**Live-page drift, observed:** the same `subprocess.html` URL was opened in round 60 as
**208 624 B, sha256 `6e86cc82…09685b`** (S260's row, fetched 2026-11-01); three days later it serves
**208 648 B, sha256 `4b88b831…a2c7`**. The URL is not a stable object — every quote below is pinned
to *this* snapshot's hash and byte offsets, and a reviewer re-fetching the URL must compare the hash
first (this is why the row carries a 90-day recheck rather than `on-release`).

- `subprocess.html` — 208 648 B, `4b88b8316a05baadaa7b2dd254c320a40b5406d8158a57f2a50b55b4d872a2c7` (local name in this dir)
- `tempfile.html` — 75 198 B, `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560`

No tool was installed or upgraded for this seat (curl + `python3` stdlib only).

## 2. Located quotes (verbatim, with anchors)

Rendered-HTML quotes that cross inline markup are labelled **composite** per QUALITY #42; every
offset below is a byte span in the file whose sha256 is named above, so a reviewer can re-find the
run with `python3 -c 'b=open("subprocess.html","rb").read(); print(b[OFF:END])'`.

### 2.1 The env contract — `#subprocess.Popen` (primary anchor)

- Section: the `class subprocess.Popen(...)` entry, `<dt ... id="subprocess.Popen">` at raw line 606;
  the env description is the paragraph at **raw lines 881–883**, bytes **88438–88718**.
- **Q1 (composite, 19 words)** — bytes `88438–88591`:

  > If env is not None, it must be a mapping that defines the environment variables for the new process

- **Q2 (plain text, 14 words)** — bytes `88623–88718`:

  > these are used instead of the default behavior of inheriting the current process’ environment

- The full sentence is 33 words (Q1 + `; ` + Q2), over the ≤25-word bound; it is recorded here as
  two contiguous verbatim clauses, not as a spliced quote. The same wording occurs a second time
  under `#subprocess.run` (`<dt ... id="subprocess.run">` raw line 270; env description raw lines
  310–311, bytes 24711–24991) — the page states the contract twice, identically.
- **Q3 (composite, 13 words)** — the admonition directly under the same paragraph, raw lines
  888–890, bytes **89257–89338**:

  > If specified, env must provide any variables required for the program to execute

  (The rest of that admonition is Windows/`%SystemRoot%`-specific and out of scope for this Linux
  lane; it is not quoted as contract.)

### 2.2 The second candidate — `#tempfile.mkdtemp` (screen only)

- Section: `<dt ... id="tempfile.mkdtemp">` raw line 476; description raw lines 478–485.
- **T1 (19 words, plain)** — raw lines 478–480:

  > Creates a temporary directory in the most secure manner possible. There are no race conditions in the directory’s creation.

- **T2 (composite, 18 words)** — raw lines 481–482, bytes 48549–48749:

  > The user of mkdtemp() is responsible for deleting the temporary directory and its contents when done with it.

- **T3 (composite, 9 words)** — raw line 485:

  > mkdtemp() returns the absolute pathname of the new directory.

- Absence finding (relevant to the reject below): `grep -Eic 'unique|distinct|collision|collide'
  tempfile.html` → **0** (exit 1, the no-selected-lines status S259 documents). The page states
  private creation, no creation race, caller-owned cleanup and an absolute return path; it states
  **no per-call name uniqueness guarantee**.

## 3. Grounding against the frozen claims (R70-C2)

Claim text (`.ufo/waves/round-70/claims.json`, R70-C2): arms `A3_child_env_allowlist` and
`A6_home_no_tmp`, 7 of 7 required at the measured revision, 0 of 7 against the round-69 tools at
the base.

**S272 (Q1 + Q2 + Q3) grounds, precisely:**

1. **The default is inheritance.** `env=None` is documented as “the default behavior of inheriting
   the current process’ environment” (Q2). So a `subprocess.run(argv)` that omits `env` hands the
   packer child the caller’s whole environment, HOME and TMPDIR included — the M69-11 / S-1 class
   the round closes. The doc gives the default a name; it does not by itself show any instrument
   omitting `env`.
2. **A mapping replaces, it does not merge.** Q1 (“used instead of”) is what makes `build_child_env`
   a real allowlist: the four returned keys are the child’s entire environment, so a caller’s
   extra variables cannot leak in. This is the mechanism A3 asserts a case for
   (`child-env-allowlist`: `sorted(ce) == sorted(CHILD_ENV_KEYS)`).
3. **The mapping must be self-sufficient.** Q3 (“env must provide any variables required”) is why
   the allowlist carries `PATH` and `LANG`: a `{"HOME": ...}`-only mapping would leave the packer
   child unable to resolve `upx` or a locale. The instrument reads the parent `PATH` once and
   copies it into the mapping (`build_child_env`, packed-elf.py:154–167) rather than inheriting it.
4. **A parent without HOME cannot supply one.** Because the mapping is the whole child environment,
   A6’s expectation follows from Q1: with the parent stripped to `PATH`+`LANG`
   (seam-probe.py:126–138, `keep_home=False` at :272), a correct builder still yields a `HOME`
   under `--work`, and the only route to a `/tmp` `HOME` is the instrument’s own source — which A6
   checks separately by literal absence of `os.environ.get("HOME", "/tmp")`
   (seam-probe.py:57, `TMP_FALLBACK_PATTERN`; packed-elf.py’s `build_child_env` has no such read).

**Arms that rest on S272 — 2 of 7:**

| arm | rests on | where |
|---|---|---|
| A3_child_env_allowlist | Q1 (replacement ⇒ allowlist) + Q3 (PATH/LANG must be carried) | `packed-elf.py:121,154–167`; cases at `:716–723`; registry at `:123` (23 cases); predicate `seam-probe.py:229–232` |
| A6_home_no_tmp | Q1 (mapping defines the child env ⇒ parent HOME absence is irrelevant) | `seam-probe.py:271–282`; instrument wiring at `packed-elf.py:321,539–540,563–589` |

**Adjacent, not resting:** A4 injects its broken `node` through the harness’s own `env` mapping
(`seam-probe.py:129–130`), which is only the instrument’s whole `PATH` because of Q1 — but A4’s
assertion is a typed `broken_tool` and no traceback, an error-typing property the page says nothing
about.

**Not grounded by S272:** A1 (hash before exec), A2 (threaded pinned path), A5 (packer exec-format
refusal), A7 (per-run work dir). The page is silent on pinning, argv identity, exec format and
scratch naming.

What S272 does **not** do: it does not measure any arm. The arms remain measurements of the frozen
probe; the row makes the requirement intelligible and names the mechanism, and its scope is the
documented API contract, not this lane’s instrument behaviour.

## 4. Decisions

### 4.1 ADMIT — S272, Python `subprocess` env contract

Reason: it is the row the round plan already names — `plans/round-70-claims.md` §2b: “R70-C2's
A3/A6 arms rest on the Python `subprocess` environment-contract row opened this round (a new row:
children inherit the parent environment unless `env` is passed — the ground for the allowlist
builder)”. It grounds a mechanism no other registry row carries: inheritance is the default, a
mapping is a substitution, and the mapping must be self-sufficient.
A3 and A6 both depend on that mechanism.

**Boundary against the earlier row on the same page.** `corpus/SOURCES.md` already carries **S260**
for this URL (round 60). Its scope is disjoint and stays untouched: S260 grounds “the recommended
way to invoke child processes is the `run` helper with argv args”, i.e. the *composition style*
(`tools/round-60/annotation-sweep.py`), and its quote is the `Using the subprocess Module` sentence
(19 words). S272 grounds the *`env` parameter's substitution semantics* — inheritance when `None`,
replacement when a mapping is given, and self-sufficiency of that mapping — a mechanism S260 does
not state and no other registry row carries. The two rows are therefore complementary rather than
duplicates; S272's `teaches` cell names S260 by id so the boundary is visible in the registry, and
S260's own snapshot (different bytes, see the drift note in §1) is left as filed.

### 4.2 REJECT — tempfile `mkdtemp` page, as a SOURCES row for this round

Reason (four parts, each checkable):

0. **It is not an overlap reject.** The `tempfile` page grounds sentences the `subprocess` page
   does not (private creation, caller-owned cleanup, absolute return path), so on the question “does
   a second row add a claim the subprocess row does not ground?” the answer is yes. The rejection is
   on **demand**: no frozen R70 claim consumes any of those added sentences, and the one arm the
   candidate was fetched for (A7, per-run work) turns on a property the page never states.

1. **The arm it was fetched for does not need it.** A7 asserts that two battery runs record
   different `work_dir` strings (`seam-probe.py:284–301`; the same predicate as
   `forged-receipts.py:265,274–275`). That is a measurement of the instrument, not a documented
   property: the page states **no** uniqueness/distinctness guarantee (0 hits for
   `unique|distinct|collision|collide`), so a row could not ground the predicate it would be cited
   for without overclaiming.
2. **Consumer-code search (QUALITY #36), command and hit count:**
   `grep -c "mkdtemp" tools/round-70/*.py` → contract-probe 2, controls 4, forged-receipts 2,
   mutation-check 2, packed-elf 3, seam-probe 6 (19 call/mention sites — all scratch creation).
   `grep -nE 'st_mode|0o700|stat\(|unique|distinct|collision' tools/round-70/*.py` → **7 hits, all
   the word `distinct` in the `work_dir` predicate** (forged-receipts 28/265/274/275,
   seam-probe 31/284/301). **0** hits on mode, ownership, permission bits, absolute-path or
   name-uniqueness predicates. The page’s stated properties (private creation, no creation race,
   caller cleanup, absolute return) are matched by no claim predicate; they describe the lane’s
   scratch discipline, which the seat contract already binds operationally.
3. **The page’s quotable sentences do not carry the arm’s premise.** T2 (cleanup ownership) and T3
   (absolute path) are true of the design but unasserted by the claims; T1’s “no race conditions in
   the directory’s creation” is about safe creation against a hostile shared directory, not about
   two sequential calls differing.

**Flip condition (when this decision reverses):** admit the row when any of
(a) a claim compares a receipt’s scratch-dir **mode/ownership/privacy** or **absolute-path**
property as a predicate; (b) a claim cites “no race conditions in the directory’s creation” as the
security ground for a scratch arm; or (c) CPython’s page states per-call **uniqueness/distinct
names** explicitly (today: 0 occurrences; if that wording appears, the A7 predicate becomes
doc-groundable and the reject fires the flip).

## 5. Proposed SOURCES.md rows

Registry column order: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

```
| S272 | CPython 3 documentation, The Python Standard Library, `subprocess` (Python 3.15.2) — https://docs.python.org/3/library/subprocess.html#subprocess.Popen | docs | A | The `env` parameter's stated substitution semantics on the 3.15.2 page: a non-None mapping defines the new process's environment and is used *instead of* the default inheritance, and the mapping must carry the variables the program needs — not OS-level `execve` mechanics, not any instrument's behaviour, not the Windows `%SystemRoot%` note | Snapshot fetched 2026-11-04T04:17:30Z (HTTP 200, 208 648 B, sha256 `4b88b8316a05baadaa7b2dd254c320a40b5406d8158a57f2a50b55b4d872a2c7`); dt `subprocess.Popen` raw line 606, description raw lines 881–883, bytes 88438–88718: composite 19-word clause "If env is not None, it must be a mapping that defines the environment variables for the new process" + plain 14-word clause "these are used instead of the default behavior of inheriting the current process’ environment" (33-word sentence split per QUALITY #42); note raw lines 888–890, bytes 89257–89338, 13 words; same wording under `subprocess.run` raw lines 310–311 | Passing `env` replaces the child environment rather than extending it, so a fixed key set is a genuine allowlist and every variable the child needs (PATH, LANG) must be added explicitly; omitting `env` is the one route by which the parent's environment — HOME and TMPDIR included — reaches the child. Grounds `build_child_env`'s four-key allowlist and the receipt-reported `child_env` the A3/A6 arms read. Same page as S260, disjoint scope: S260 grounds the `run()`-helper argv composition style, this row the `env` substitution semantics. | mined | 2026-11-04 | 90d | corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md |
| S273 | CPython 3 documentation, The Python Standard Library, `tempfile` (Python 3.15.2) — https://docs.python.org/3/library/tempfile.html#tempfile.mkdtemp | docs | A | `mkdtemp`'s stated creation and cleanup properties (secure creation, no creation race, creating-user-only access, caller deletes, absolute return path); **not** per-call name uniqueness, which the page does not state | Snapshot fetched 2026-11-04T04:17:30Z (HTTP 200, 75 198 B, sha256 `edf721761f0de44769b1fb817b8105447a9a8cecb1d6df1c6347a804db442560`); dt `tempfile.mkdtemp` raw line 476, description raw lines 478–485; `grep -Eic 'unique|distinct|collision|collide' tempfile.html` = 0 (exit 1) in the fetched bytes | REJECTED for round 70: no claim predicate reads a documented `mkdtemp` property — `grep -c "mkdtemp" tools/round-70/*.py` = 19 scratch sites and `grep -nE 'st_mode|0o700|stat\(|unique|distinct|collision' tools/round-70/*.py` = 7 hits, all the `work_dir` distinctness predicate, none on mode/ownership/absolute-path/name-uniqueness; A7's distinct-`work_dir` expectation is measured, and the page states no uniqueness guarantee. Flip: admit when a claim compares scratch-dir mode/ownership/absolute-path, or cites "no race conditions in the directory's creation" as a security ground, or the page gains explicit uniqueness wording. | rejected | 2026-11-04 | 180d | corpus/lessons/round-70.md |
```

Notes for the registry edit:

- S272 is the next unused id (last filed: S271; `corpus/SOURCES.md` holds 178 rows). S273 is
  proposed **only** because this seat's screen produced a reject that must stay locatable with its
  flip clause; it consumes an id exactly as the existing rejected rows S022 and S028 do. If the
  lane's convention this round is to keep rejects in the lesson `## Gate` only, drop S273 and keep
  §4.2 as the record — S272 stands either way.
- `used-by` for S272 is the round-70 knowledge entry path fixed by the wave generator,
  `.ufo/waves/round-70/gen-w1.py:329`: `corpus/knowledge/2026-11-04-r70-provenance-bound-receipts.md`.
  S273's `used-by` is `corpus/lessons/round-70.md` (the Gate that carries this screen).
- Recheck: 90 d for S272 (docs page, matching the recent Python-docs rows S266–S268); 180 d for
  the rejected S273 (it must be re-read only if its flip condition fires).

## 6. Verification performed and remaining unknowns

Verified (commands run, results observed):

- Frozen bytes: `git show 4737a54:tools/round-70/packed-elf.py | sha256sum` =
  `1601a5b8…021880` and `…/seam-probe.py` = `ffb2a168…ad357a6`, both equal to the working-tree
  files and to the pins in `.ufo/waves/round-70/claims.json` — the wiring cited in §3 is the frozen
  wiring.
- `REGISTERED_CASES` holds 23 entries (`packed-elf.py:123`), and the three child-env cases are
  members (`child-env-allowlist`, `child-env-home-in-work`, `child-env-no-tmp`, `:716–723`), which
  is what `seam-probe.py:58,229–232` checks against `st["cases"] == 23`.
- Every packer child invocation carries `env=packer_env_cenv` (`packed-elf.py:563,567,573,587,589`),
  built from the run root at `:539–540`. The `env`-omitting spawns are exactly the non-packer
  children — `run()`'s default (`def run(..., env: dict | None = None)` at `:249–252`, used by
  `rea()` at `:259`) and the two direct `git` calls at `:358` and `:493` — so git/readelf/node
  inherit by design while no packer child can (`[INFERENCE]` that this inheritance is the documented
  default, which is Q2's subject).

Remaining unknowns / inference marks:

- The cited URL is the unversioned `…/3/library/…` page; it served the 3.15.2 build on 2026-11-04.
  The sha256 pins the snapshot, not the URL: a later docs edit changes the hash and must be
  re-fetched (the 90-day recheck).
- `[INFERENCE]` The page describes the API contract, not the syscall: that the mapping is handed to
  `execve` as the complete environment vector is CPython behaviour, not a sentence on this page.
  Nothing in the round's predicates depends on the syscall-level statement.
- A3 asserts on the *pure builder* and the committed case registry; it does not spawn a packer child
  and read that child's `environ`. A reviewer wanting a child-level observation (e.g. a canned child
  printing its environment) will not find one in A3 — flagged for the attack seats, and not a defect
  of this source row, whose scope is the documented contract.
- The A6 arm's `rc == 1` expectation is an instrument contract; the page says nothing about exit
  codes.

Scratch: `/fast/scratch/hyaku/kaidoku-r70/ScoutSource/` held only the two fetches; both were copied
here and re-hashed, then the scratch root was removed (`rm -rf`), so no citable evidence lives under
`/tmp` or the scratch root.

VERDICT: met — S272 admitted (subprocess env contract, HTTP 200 / 208 648 B / sha256 `4b88b831…a2c7`, Popen raw lines 881–883 and note 888–890, 19+14+13-word located quotes) grounding R70-C2 A3+A6 (2 of 7 arms); tempfile page rejected as a row with its consumer search (19 `mkdtemp` sites, 7 hits all on the `work_dir` distinctness predicate) and flip condition recorded; instruments' frozen bytes matched to the claims pins.
