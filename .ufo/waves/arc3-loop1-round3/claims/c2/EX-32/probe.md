# EX-32 — probe interplay: citation-drift probe at HEAD after EX-21

Seat EX-32 · chain c2 · role executor · wave arc3-loop1-round3 · 2026-10-19.
Task (seat line): *"probe interplay: citation-drift probe at HEAD after EX-21 →
findings=0 both modes; the tool revision must not stale any needle."*

Typed claims under test:

1. **Probe-clean**: with EX-21's custody-tool revision in the tree, the
   citation-drift probe at HEAD reads `findings=0` in both modes (probe mode
   `reported findings=0 exit=0`; `--strict` `clean findings=0 exit=0`), selftest
   13/13.
2. **Needle-invariance**: the custody-tool revision stales no pinned needle in
   `pointer-table.json` — the table digest still equals its `expected.json` pin,
   and every needle target still resolves under the revised tree.

STATUS: **complete** (late-join seat, 2026-10-19). Baseline + controls were
measured by the first EX-32 run; the post-EX-21 measurement was left a
PLACEHOLDER when the wave was interrupted. This seat completed §5 and
independently re-derived every number in it from a fresh harness
(`/var/tmp/ex32lj/`, distinct from the §4 `/var/tmp/ex32r3/` clone). Verdicts:
claim 1 (probe-clean at HEAD) **holds**; claim 2 (needle-invariance of the
custody revision) **holds** (§5a). One *additional* stale needle was found and
attributed to the registry row, not the tool (§5b), and the §2 re-anchor is
confirmed as its fix in four worlds (§5c).

## 1. Method

The probe is blob-scoped: it grades Git objects at `--rev`
(`citation-drift-probe.py:100` `git_show`, `:125-137`, `:229-233`), so an
uncommitted worktree edit is invisible to it. Until the parent lands the round's
work commit, the strongest available measurement of the post-revision state is a
scratch clone of the repo at HEAD `c07af80f…` into which EX-21's settled files
are copied and committed; the probe then runs against that clone. Scratch root
`/var/tmp/ex32r3/` (never `/tmp`); the real repo is read-only to this seat.

## 2. Baseline at HEAD `c07af80f` (before EX-21 lands)

Commands (repo root):

```
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict
python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
```

Outputs (`evidence/probe-head.out`, `probe-head-strict.out`,
`probe-selftest.out`):

- `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` (rc 0)
- `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` (rc 0)
- `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`

Instrument digests at baseline (`evidence/hashes-baseline.txt`):

| Object | sha256 |
|---|---|
| pointer-table.json | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` (== `expected.json` `pointer_table` pin) |
| expected.json | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |
| citation-drift-probe.py | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| custody-pair.py (pre-EX-21) | `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa` (round-2 final) |

Worktree-vs-HEAD byte identity for all 17 needle target files: **17/17 SAME**
(`evidence/worktree-vs-head.txt`; only dirty path in the repo is
`.ufo/waves/arc2-loop1-round10/C3.md`, not a needle target).

## 3. Needle inventory and EX-21's footprint

Mechanical inventory (`evidence/needle-inventory.txt`): 31 `entries` + 4
`quoted` = 35 needles over 17 distinct target files. **No needle target is under
`.ufo/gates/`** — the custody tool's own files are not needle targets.

EX-21's footprint per the frozen C2 claim: `.ufo/gates/custody-pair/custody-pair.py`,
its `README.md`, the SKILL.md custody-pair **registry row** (same commit), and
new receipts under the wave tree. Of these, the only needle-target file is
`SKILL.md`, carrying two needles:

- `skill-registry-row` (anchor; content `interactive-r1-recovery \| gate /
  kaidoku`, no line pin) — the interactive-r1 row, not the custody row.
- `shonen-skill-range` (extracted; SHONEN.md:6 cites `SKILL.md:81-255`;
  `must_match` = rule #13, which lives at `SKILL.md:233`; registry section
  starts at `:379`, custody row at `:390`).

Safety argument, measured (not assumed): any edit whose first changed SKILL.md
line is > 255 cannot stale `shonen-skill-range`, and the registry region
(`:379-390`) is below that line. Controls in §4 test exactly this.

## 4. Controls in the scratch clone (harness discrimination)

Clone: `/var/tmp/ex32r3/clone` at `c07af80f` (probe in clone at HEAD:
`reported findings=0`, `clean findings=0`).

- **Negative control — EX-21-shaped edit**: appended a revision marker to
  `custody-pair.py` and `README.md`, swapped `15 fixture cases` → `17 fixture
  cases` in the SKILL.md custody row, committed.
  Result: `reported findings=0 exit=0` / `clean findings=0 exit=0`
  (`logs/sim-ex21-shape-probe.out`, `logs/sim-ex21-shape-strict.out`).
- **Positive control — needle-staling edit**: 30-line insertion at the top of
  SKILL.md (shifts rule #13 out of the cited 81-255 range), committed.
  Result: `CITATION_DRIFT: citation_dead entry=shonen-skill-range SHONEN.md:6
  cites SKILL.md:81-255, which lacks 'A mitigation claim carries its natural
  control'`; `reported findings=1 exit=0` / strict `failed findings=1 exit=1`
  (`logs/sim-stale-probe.out`, `logs/sim-stale-strict.out`).
  The harness therefore detects a SKILL.md line-range stale if one exists.

Clone reset to `c07af80f` afterwards (SKILL.md sha `c134afcb…` restored).

### 4b. Needle-class fragility under a tool revision (forward-looking attack)

C3's round claim extends the pointer table to arc3-era citations, and the C2
named-debt text names "custody receipt conventions" as an arc3-era citation
class — i.e. the r3 table may plausibly gain needles into
`.ufo/gates/custody-pair/`. Those needles would live in the same round as EX-21's
active revision of that tool. Measured on the clone, with a synthetic two-entry
table (`/var/tmp/ex32r3/synth/synth-table.json`, sha256 `066447df…`, re-pinned in
a scratch `expected.json`):

- pre-revision: both a `kind=anchor` needle (`CUSTODY_PATHS` tuple, content
  anywhere) and a `kind=exact` needle pinned to `.ufo/gates/custody-pair/
  custody-pair.py:111` resolve → `reported findings=0 exit=0`;
- after an EX-21-shaped mid-file insert (5 lines at :11, tool 889 → 894 lines):
  the **anchor survives** (no finding), the **line-pinned exact needle reads
  `citation_dead … :111 lacks '^CUSTODY_PATHS = \('`** → `findings=1`
  (`logs/synth-post.out`, copied to `evidence/synth-post.out`).

Typed consequence: line pins into the custody tool are fragile under the very
revision this round lands; anchor-class needles (or extracted needles with a
`window`) are the only forms that can coexist with EX-21's churn. If the landed
r3 table extension contains bare line pins into `.ufo/gates/custody-pair/`, the
interlock fails and this dossier's §5 measurement will show it.

## 5. Post-EX-21 measurement — LATE JOIN, re-derived independently

Filled 2026-10-19 by the late-join EX-32 seat. EX-21 froze at tool
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 ln) /
README `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` (185 ln),
re-derived here with `sha256sum`. Because the revision is uncommitted, every
reading below is taken in a **fresh clone** (`/var/tmp/ex32lj/clone`, pristine at
`c07af80`) into which the real-target bytes are copied and committed — a
different harness from §4's `/var/tmp/ex32r3/clone`, so the numbers below are an
independent re-derivation, not a re-run. Harness:
`per-entry-sweep.py` (this seat's) grades **every** entry through the probe's own
`check_entry`, so a reddened needle is attributable to its entry id rather than
counted in aggregate.

### 5a. The seat-line claim HOLDS — the custody revision stales no needle

World H2 = EX-21's tool + README + the **landed 57-entry table** (`bfc42f1b…`)
+ the **round-2 SKILL.md row** (`c134afcb…`):

```
CITATION_DRIFT_VERDICT: reported findings=0 exit=0     (evidence/late-H2-custody-landedtable.out)
CITATION_DRIFT_VERDICT: clean findings=0 exit=0        (…-strict.out)
PER_ENTRY_SWEEP graded=61 clean=61 non_clean=0         (evidence/late-H2-sweep.out)
CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0
```

61 = 57 `entries` + 4 `quoted`. The revision's footprint is confined to
`.ufo/gates/custody-pair/` plus the wave tree, and **no needle target lives in
`.ufo/gates/custody-pair/custody-pair.py`** (0 entries) — the four custody
README anchors are `kind=anchor` with no `pin_line`, and all four re-derive
`HIT` against the revised README (`f30df42e…`) *and* against the pre-revision
blob, so the README rewrite neither breaks nor blurs them. Isolation control
(§5d) shows the tool revision alone, with the table held at either revision, is
needle-neutral. **Claim 2 of the seat line: CONFIRMED by re-derivation.**

### 5b. The collision is the registry row, not the tool (independently reproduced)

World G = the canonical landing — EX-30's registry row (`SKILL.md` `03832723…`)
+ the landed table + the revised tool/README:

```
CITATION_DRIFT: citation_dead entry=skill-registry-custody-pair-row SKILL.md: no line matches 'precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA'
CITATION_DRIFT_VERDICT: reported findings=1 exit=0     (evidence/late-G-landed-table.out)
CITATION_DRIFT_VERDICT: failed findings=1 exit=1       (…-strict.out)
PER_ENTRY_SWEEP graded=61 clean=60 non_clean=1         (evidence/late-G-sweep.out)
  NON_CLEAN id=skill-registry-custody-pair-row findings=citation_dead
```

This reproduces §1's prediction from a second harness: at the coupled landing
the probe is red, and the sole stale needle is the registry row — 60 of 61
needles stay clean. The row candidate does not matter: EX-21's own draft
(`5eec51c0…`) reddens identically (evidence/late-E-ex21row-landedtable.out,
`findings=1`, strict `exit=1`).

### 5c. The §2 re-anchor fixes it in every world (four-way robustness)

| world | SKILL.md | table | reported | strict |
|---|---|---|---|---|
| C | EX-30 row `03832723…` | re-anchored `a810bd17…` | `findings=0` | `clean findings=0` |
| D | **round-2 row** `c134afcb…` | re-anchored `a810bd17…` | `findings=0` | `clean findings=0` |
| E | EX-21 row `5eec51c0…` | landed `bfc42f1b…` | `findings=1` | `failed findings=1` |
| F | EX-21 row `5eec51c0…` | re-anchored `a810bd17…` | `findings=0` | `clean findings=0` |

(evidence/late-C-reanchored*.out, late-D-reanchored-oldrow*.out,
late-E-ex21row-landedtable*.out, late-F-ex21row-reanchored*.out; sweeps
`late-D-sweep.out`, `late-F-sweep.out` both `graded=61 clean=61 non_clean=0`.)

The optional-group form is therefore safe **before** the landing (D: round-2
row still matches) and **after** it (C/F), and holds for either row draft. This
is the "must not stale any needle" half of the seat line discharged for the fix
as well as for the tool. The re-anchored table regenerates **byte-identically**
(`json.dumps(obj, indent=2, ensure_ascii=False) + "\n"` → `a810bd17…`, equal to
the scratch artifact this seat did not author), and the re-pinned `expected.json`
moves only the digest value → `e33f0e2d…`, no trailing newline, `snapshots` and
`frozen_run` untouched.

### 5d. Isolation and controls

- **Isolation (H)** — EX-21's tool + README alone, table and SKILL.md at their
  `c07af80` bytes: `reported findings=0` / `clean findings=0`
  (evidence/late-H-custody-revision-alone*.out). The custody revision by itself
  moves nothing.
- **Negative control (J)** — a *committed* 30-line insertion at the top of
  SKILL.md, on the re-anchored table: the harness reddens with **5** findings
  (`shonen-skill-range` plus the four `skill-rule14-*` extracted needles),
  reported `exit=0` / strict `failed findings=1 exit=1`
  (evidence/late-J-negative-control*.out). Restored, re-committed → `findings=0`
  (late-K-restored.out). The harness discriminates; the §5a/§5c zeros are not
  vacuous.
  Method note: the first attempt at this control edited the worktree **without
  committing** and read `findings=0` — the probe grades Git objects, so an
  uncommitted edit is invisible to it. The control only became a control once
  committed. Recorded because it is exactly the trap §1 warns about.
- **Per-entry discrimination** (evidence/late-row-discrimination.txt) — the
  re-anchored regex still reddens a reversed chain, an UNEVALUABLE-after-ABSENT
  ordering, and an `UNEVALUBLE` typo. It *accepts* a row whose chain is followed
  by junk (`… > MATCH > UNEVALUABLE;`) — measured, and **inherited**: the
  round-2 needle accepts that string too, so the re-anchor introduces no new
  laxity. A tightened form `… > MATCH(;|\||$)` closes it while keeping both real
  worlds green; offered to EX-41 as an optional strengthening, not a claim
  requirement.

### 5e. Identity discipline (rule #14) and an honest record of the earlier clone

Every digest above was re-derived at write time (`sha256sum`), never copied:
evidence/late-hashes.txt carries the full manifest, and
evidence/late-worktree-vs-head.txt re-derives worktree-vs-`c07af80` identity for
all 20 needle targets (19 `SAME`, 1 `DIFF` — `.ufo/gates/custody-pair/README.md`,
the round-3 real-target write; `SKILL.md` is `SAME` at the worktree because the
row patch is not applied there).

One discrepancy is recorded rather than smoothed, and its cause is now
established. The earlier run's clone (`/var/tmp/ex32r3/clone`) ends with
`SKILL.md` `62de3922…`, which is **not** byte-equal to the round-2 base
(`c134afcb…`), to EX-30's final patched form (`03832723…`), or to EX-21's
(`5eec51c0…`). Re-deriving it here identifies the source: applying
`/var/tmp/ex32r3/patch-test/registry-row.diff` (sha256 `dbd79a63…`) to a
pristine `SKILL.md` reproduces `62de3922…` exactly. That diff is **not** EX-30's
final embedded diff (`7c4a7a68…`, the one rendering `03832723…`), so the earlier
clone was built from a **superseded draft** of the registry-row patch text, and
its landing measurement therefore describes a row form that no longer exists.
§1's conclusion is unaffected — it is reproduced here from both official drafts
(§5b) — but the earlier clone's §5 numbers were not re-derivable from the
artifacts that survived it. §5a–§5d supersede them with re-derivable ones.

At HEAD in the real repo (uncommitted tree, `--rev HEAD` grades the committed
blobs): `reported findings=0` / `clean findings=0`, selftest `13/13`
(evidence/late-head*.out, late-selftest.out); per-entry sweep `graded=61
clean=61 non_clean=0` (evidence/late-real-sweep.out).

## 6. Residuals / named gaps

- The probe grades committed blobs; the final "at HEAD after EX-21" reading is
  only obtainable at the round's work commit. Integration duty (for the parent):
  re-run `citation-drift-probe.py --root . --rev <work-commit>` in both modes
  once the work commit exists; expected `findings=0` per §5.
- Interfacing risk, named: if the round's single work commit also lands C1's
  corpus/README map row and/or C3's extended pointer table, those are *other*
  needle surfaces (readme22/readme175 pins; the table itself) and are outside
  this seat's interlock (EX-32 r2 precedent: C1 line-neutral token).

### 6b. Live needle-target integrity incident (observed 2026-10-19T13:25Z, resolved)

A **concurrent seat clobbered a needle-target file** during this run, and this
seat observed both the clobber and its reversal:

- **13:25:02Z** — `.ufo/waves/arc3-loop1-round1/claims/cross/receipts/
  config-pre-pair.txt` (the target of anchor entry `custody-readme-v1-stanza-example`)
  was overwritten with **304 insertions / 51 deletions** of unrelated content:
  `== VZ-4 C2 after-state suite ==`, selftest transcripts, a
  `/var/tmp/vz4r3-late/...` receipt path. The round-1 CU-1 receipt's 52 lines
  were replaced wholesale. `git status` showed it `M`.
- **13:25:55Z** — the file was **restored byte-identically** to the `c07af80`
  blob (sha256 `b8ed1936…`, `git diff` empty, 52 lines, `captured-by: SEAT CU-1`
  present again). `git status` no longer lists it.

**Impact: none on the recorded measurements.** The probe grades Git objects at
`--rev`, so a worktree edit is invisible to it — the §5 readings are unaffected,
and a re-run after the restoration still gives `findings=0` both modes with a
`61/61` sweep (re-verified at 13:26Z). The clobber never entered a commit.

**Why it is recorded anyway:** a seat whose scratch recipes write tool output
*into the repo tree* can clobber a needle target, and had this one landed in the
work commit the anchor would have gone dead. Two protections exist and both
worked here — the restoration, and the probe's blob-scoping. Recommended for the
parent: before the landing commit, run `per-entry-sweep.py` (or the probe) **and**
`git status --short` together, so any unintended worktree write is visible next
to the needle verdict. The VZ-4 seat's own recipes should write to `/var/tmp`
only (this incident is a scope slip, not a design flaw in its suite).