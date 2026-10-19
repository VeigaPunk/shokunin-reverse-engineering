# EX-31 — census interplay: census verdict at HEAD across EX-21's landing

Seat EX-31 · chain c2 · role executor · wave `arc3-loop1-round3` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Instrument:
`.ufo/gates/c1-census-v10.py`, sha256
`d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5` (bracketed
before and after every run below; unmodified throughout). No git mutation, no
edit to any gate file, no edit to a scoped file (`PROVINCE.md`, `SKILL.md`,
`SCORECARD.md`); this seat's only repo writes are `claims/c2/EX-31/**` and this
report. Scratch lives in `/var/tmp/ex31-sim` (never `/tmp`).

Seat-line claim under test: **after EX-21 lands its revision of
`.ufo/gates/custody-pair/`, the census at HEAD still reads PASS** — the tool edit
is under `.ufo/gates`, outside the census's declared scope.

**Result: PASS, and stronger than required — the census output is
byte-identical before and after the landing** (`c8d97713…` both sides, exit 0,
three runs). The gate revision moves nothing in the census.

---

## 1. Work performed (evidence pointers)

| what | evidence |
|---|---|
| instrument identity, bracketed around every run | sha256 above == `evidence/pre/instrument-sha256.txt`; re-checked after the post run (§3) |
| repo rev at baseline | `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311` (`evidence/pre/head-rev.txt`) |
| pre-EX-21 census (text + json + true exit codes) | `evidence/pre/census-pre-EX21.txt` / `.json` / `.exit` |
| pre-run reproducibility pair | `evidence/pre/census-pre-EX21-twice.txt` — `c8d97713…` twice, byte-identical |
| worktree == HEAD for the three scoped files | `evidence/pre/scoped-files-clean.txt` (empty porcelain), `scoped-files-blobhash-{worktree,head}.txt` |
| the scope table, quoted | `evidence/pre/scope-table.txt` (`SCOPE` at `c1-census-v10.py:215-238`) |
| why `.ufo/gates` is out of scope | `c1-census-v10.py:509` — `files = sorted({s[0] for s in SCOPE})`, i.e. exactly `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`; no `.ufo/**` path is ever read from `--root` |
| out-of-scope attack (planted drift inside a gate file) | `evidence/sim/attackA-gate-drift.txt` — `PASS 0/0/0/0`, exit 0 |
| interaction matrix (8 variants on scratch roots) | `evidence/sim/v*.txt`, `v*.diff`, `variant-sha256s.txt`, `poll-for-EX21.sh` |
| mid-flight census while EX-21 was writing | `evidence/after/census-midflight-EX21.txt`, `midflight-tool-sha256.txt` |
| post-EX-21 census at HEAD (+json, +repair pair) | `evidence/after/census-post-EX21.txt` / `.json` / `.exit`, `census-post-EX21-twice.txt`, `gate-sha256-after.txt` |
| custody-path identity, read-only, before and after | `evidence/pre/custody-hashes-pre.txt` vs `evidence/after/custody-hashes-post.txt` — 5/5 identical |

## 2. Proposed changes

**None.** This seat authors no patch text and edits no repo file outside its own
artifact directory. The gate revision is EX-21's write; the census instrument is
chain c1's instrument. §4 records one *measured constraint* for the round's
coupled landing (the custody-pair registry-row text must stay locus-free) — a
measurement, not a proposal, and it names no edit.

## 3. Before → after measurement (the seat's claim)

**(a) Pre-EX-21 baseline** at rev `c07af80f` (worktree blob-identical to HEAD for
the three scoped files):

```
$ TMPDIR=/var/tmp python3 .ufo/gates/c1-census-v10.py --root <repo>
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1496 loci=9
SKILL.md       lines=390  loci=2
SCOPE-ERRORS (marker assertions): []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      # exit 0
```

Output digest of the two baseline runs (byte-identical):
`c8d977136e5f191d2f564827066ec121520acf5542bd06cf41409510252bb4fa`.

**(b) Mid-flight** — EX-21 still writing; `custody-pair.py` sampled at
`1287c9d60af6a4f82b083d2120707ccc6e34948632f5f078ba04116e9784444b`: census
`VERDICT: PASS`, exit 0, digest unchanged
(`evidence/after/census-midflight-EX21.txt`). An already-changed gate file moves
nothing.

**(c) Post-EX-21 at HEAD** — captured 2026-10-19T10:16:51-03:00, after the gate
pair had held still for three consecutive 30-s samples (`custody-pair.py`
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, gate
README `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193`, 42331
and updated bytes respectively; the same tree also carried EX-41's
citation-drift edits, so this run covers the combined landing):

```
$ TMPDIR=/var/tmp python3 .ufo/gates/c1-census-v10.py --root <repo>   # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1496 loci=9
SKILL.md       lines=390  loci=2
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)      # exit 0
```

- Text and `--json` runs both exit 0 (`evidence/after/census-post-EX21.exit`).
- Second post run byte-identical (`census-post-EX21-twice.txt`).
- **Pre and post outputs are byte-identical** (`cmp` clean): the landing's
  side-effect on the census is exactly zero.
- Instrument sha re-derived after the post run: unchanged `d0772ce8…`.

**(d) Out-of-scope proof by construction.** Attack A: a scratch root whose
`.ufo/gates/custody-pair/custody-pair.py` carries `kimi 6.7.0`,
`rea-agents@6.7.0` and `~/.kimi-code/config.toml:1` — exactly the tokens the
census censuses inside a scoped file — still reads `VERDICT: PASS 0/0/0/0`,
exit 0. Together with the minimal 3-file root (no `.ufo/` at all) also reading
PASS, both directions are covered: the verdict function reads the three scoped
files and nothing else.

**(e) Anchor invariance.** The census's L2 anchors are read live from the three
client configs (`c1-census-v10.py:124-134`, `251-263`). The five custody paths
were hashed read-only before and after EX-21's work: **5/5 identical**
(`diff` of `evidence/pre/custody-hashes-pre.txt` vs
`evidence/after/custody-hashes-post.txt` shows only the PRE/POST marker), and the
three live anchors are identical (`live-anchors-pre.txt` == `live-anchors-post.txt`).
The post-landing PASS is therefore not an artifact of a moved anchor — the
revised tool's selftest/receipt work left every operator config byte-identical.

## 4. Attacks / refutations attempted, with verdicts

| # | attack | measured result | verdict |
|---|---|---|---|
| A | flip the census by planting census tokens inside a gate file | `PASS 0/0/0/0` exit 0 (planted `kimi 6.7.0`, `rea-agents@6.7.0`, `~/.kimi-code/config.toml:1`) | **refuted** — the gate dir is out of scope |
| B | benign coupled edit to the custody-pair registry row (`SKILL.md:390`, the row C2's claim says is re-landed in the same commit): `15 fixture cases` → `17 fixture cases (D2/D3/D6 closures)` | `PASS 0/0/0/0` exit 0, SKILL loci 2 → 2 | benign; a safe form exists |
| C | same row carrying a live client token + bare version (`kimi 6.7.0`) | `FAIL undeclared=1` exit 1, locus `SKILL.md:390 [bare 6.7.0]` | **hazard is real** |
| D | same row carrying an absolute `path:line` pointer (`~/.kimi-code/config.toml:12`) | `FAIL undeclared=1` exit 1, locus `SKILL.md:390 [ptr …]` | **hazard is real** |
| E | benign line growth after row 390 (one new continuation line) | `PASS 0/0/0/0` exit 0 | safe: growth below the last scoped SKILL.md row shifts no scoped locus |
| F | round-3 records row appended to `SCORECARD.md` past the declared bound, carrying `kimi 6.7.0` | `FAIL undeclared=1` exit 1, locus `SCORECARD.md:1498 [bare 6.7.0]` | **records text must stay locus-free** |
| G | row matching `REA_GATE` but carrying no version and no pointer (`… mcp_config.json; npx cache untouched`) | `PASS 0/0/0/0` exit 0 | refines the rule: `REA_GATE` alone is not a locus |
| H | bare `6.7.0` in a row with no gate token | `PASS 0/0/0/0` exit 0 (unit fails `REA_GATE`, never classified) | the gate regex is a pre-filter, not a detector |

Measured rule for the landing: a censused locus is a unit that (i) matches
`REA_GATE` (`rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|mcp_servers|devin|\bomp\b|kimi|npx`,
case-insensitive) **and** (ii) carries `rea-agents@x.y.z`, a bare `6.x.y`, or —
only when neither is present — an absolute or `~`-rooted `.json|.toml|yaml`
`path:NNN` pointer. Every such locus must sit in a declared `SCOPE` row; the
declared SKILL.md rows end at `:20` and the declared SCORECARD.md rows at `:855`
(`c1-census-v10.py:215-238`), so a locus at `SKILL.md:390` or anywhere past
`SCORECARD.md:855` reads UNDECLARED → `FAIL` exit 1. Corollary for EX-21's
coupled registry-row update and for the round's records text: describe the
revision without a version literal, without an `@`-pin, without a client config
filename and without a `path:NNN` pointer (SC-4's drafted section already
follows this; §2/§3 of `claims/c2/records-drafts/scorecard-section-draft.md`
reaches the same conclusion from its own scratch simulation).

## 5. Blockers

None. Two notes for the parent:

- The census reads the **worktree** (`--root`), so "at HEAD" above means the
  current worktree at rev `c07af80f`; the round's work commit does not exist yet
  (no git mutation by this seat). The post-landing row §3(c) pins the exact gate
  hashes it was taken against — if either gate file changes after
  2026-10-19T10:16:51-03:00, that row must be re-taken
  (`/var/tmp/ex31-post.sh` reproduces it in one command).
- Untracked `__pycache__` residue exists in all three gate dirs
  (`.ufo/gates/`, `.ufo/gates/citation-drift/`, `.ufo/gates/custody-pair/`;
  `git status --porcelain` in `evidence/after/gate-sha256-after.txt`) — exclude
  it from the round's commit (the round-2 precedent did).

---

### Self-identity (re-derived after the last revision; rule #14)

`evidence/self-identity.txt` carries the sha256 of this file, its `wc -l`, the
instrument sha at that moment, and the re-derivation command — written last.

---

### Late-join addendum (2026-10-19, chain-c2 late-join seat — rule #14 re-derivation)

The wave's token-plan lane died mid-run; this seat re-entered at HEAD `c07af80f`
and **verified the sections above rather than redoing them**. Every number below
was re-derived by this seat; captures live in `evidence/independent/`.

**Re-derived, all confirming:**

- census at HEAD, 4 independent runs (2 full, 1 `--json`, 1 `--quiet`): `VERDICT:
  PASS`, exit 0, output digest `c8d97713…` — byte-identical to the landed pre- and
  post-captures (`evidence/independent/census-at-head-*`, `midflight-mode.txt`).
- instrument `d0772ce8…` and the three scoped files unchanged; their git blob
  hashes at HEAD match `evidence/pre/scoped-files-blobhash-{head,worktree}.txt`
  as sets (my own `diff` of the sorted lists: identical).
- the 8-variant attack matrix rebuilt from scratch at `/var/tmp/ex31-rev/sim/`:
  every verdict reproduced (A/B/E/G/H PASS; C/D/F FAIL undeclared=1) —
  `evidence/independent/variant-*.txt`.
- the mid-flight capture's differing digest is **mode, not content**: that file is
  exactly `census --quiet` output + an `exit=0` line (13 lines vs 93);
  `midflight-mode.txt` proves the match by `diff`.
- custody pair 5/5 identical pre/post, live anchors identical — the PASS is not an
  anchor artifact.

**New finding (F1) — census echoes target-file line content on a pointer miss.**
`ptr_check()` (`c1-census-v10.py:370-384`) reads the pointer target's line and
returns it in the STALE reason; the reporter prints reasons verbatim. Attack D
against the real repo therefore printed the first 60 chars of
`~/.kimi-code/config.toml:12` — an API-key line — into the run's stdout. This seat
**did not store that output**: the capture is redacted
(`evidence/independent/variant-D.txt`) and the class is reproduced with a
synthetic value (`secret-echo-finding.txt`). Patch text (proposal only; the
instrument belongs to chain c1):
`proposed-census-ptr-redaction.patch.md` — tested on a scratch copy, verdict
surface byte-identical, secret replaced by a truncated sha256
(`patched-copy-verification.txt`). The real instrument was never modified.

**Missing artifact completed:** §Self-identity above referenced
`evidence/self-identity.txt`, which had never been written (the lane died first).
This seat wrote it, with a digest re-derived after this addendum landed.