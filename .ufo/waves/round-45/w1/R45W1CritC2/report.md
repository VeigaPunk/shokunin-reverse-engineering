# R45-C2 — pre-data falsification of the frozen predicate and `c2-counter.py`

Seat `R45W1CritC2` (critic). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (2026-10-28 12:27:20 -0300).
Rule followed: claims file is the rule; frozen bytes read-only; every receipt below carries
command, exit code, stdout sha256 and UTC. All probes ran with `TMPDIR=$S`,
`S=/fast/scratch/hyaku/kaidoku-r45/R45W1CritC2`; `$S` removed after receipts were copied.

Instrument under test: `tools/round-45/c2-counter.py` at the freeze,
sha256 `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025`
(`git show <freeze>:tools/round-45/c2-counter.py` == worktree bytes; frozen tree
`b6f95ad973671477df6a20f0699cfc480def1c935d8356cd08dc542f89798124` over
`-- plans/round-45-claims.md tools/round-45`).

## 0. Headline

The **target is genuinely met at the landing** (`e715263c`, and `HEAD`): six real registry
rows, exact first cells, real verdict maps, counter exit 0. The **"Before" is authentic**:
my freeze and base receipts are byte-identical to the committed controls.

But the **frozen predicate is materially weaker than the claim text says**, in four places,
and one of them is an integrity arm that prints `met_target: true` on a frozen-bytes change:

| # | claim sentence | status |
|---|---|---|
| F1 | "a touch makes the counter exit 2 `frozen_path_changed` and print no `met_target`" | **FALSE** for a merge-introduced touch (verified exit 0, `met_target: true`) |
| F2 | "some SKILL.md registry row's **first cell is exactly** that path" / "provenance is stated as exact path equality, never as 'names a path'" | **FALSE** — `re.search` inside cell 0; an embedded `see \`path\` (wrapper)` registers (verified exit 0) |
| F3 | "the lane's own registry" (rows in the registry) | **UNENFORCED** — rows in a code fence, an HTML comment, or under no registry heading all register (verified exit 0) |
| F4 | "a bare 'non-zero' cell is thin" | **TRUE only for column 3** — no header validation, and any cell containing the tokens `0`, `1`, `2` passes ("0 rows, 1 column, 2 bytes") (verified exit 0) |

Everything else the claim asserts about the base/freeze/kill-rule reproduced exactly (§2, §4).
This is a **calibration finding, not a data finding**: the instrument that measures the
calibration axis overstates its own strictness. Nothing here says the landing is fake.

## 1. Attack table (the five asked, plus what fell out)

Each row is a fixture repo (`git -C "$D" init -q`, `--show-toplevel == $D` asserted) holding
`SKILL.md`, `plans/round-45-claims.md` and the real six-path `registry-scope.json`; the
**frozen** counter was run unmodified: `python3 -I -B $S/c2-counter.frozen.py --root $D
--freeze HEAD --rev HEAD`. Receipt: `c2-attacks.json` (sha256 `0c86da25…`).

| # | attack | expected per claim | observed | exit |
|---|---|---|---|---|
| A0 | control: six real rows under a registry heading | 0 | met, rows 6 | **0** |
| A2a | the six rows inside a ```` ``` ```` code fence | 1 | met, rows 6 | **0** ← bypass |
| A2b | the six rows inside `<!-- … -->` | 1 | met, rows 6 | **0** ← bypass |
| A2c | fenced copy + commented copy (a *draft*) | 1 | met, rows 12 | **0** ← bypass |
| A2d | rows under `## Scratch notes`, no registry heading anywhere | 1 | met, rows 6 | **0** ← bypass |
| A5 | exit cell `0 rows, 1 column, 2 bytes` | 1 (`thin`) | met, thin [] | **0** ← bypass |
| A5b | exit cell `0/1/2` | 1 (`thin`) | met, thin [] | **0** ← bypass |
| A5c | columns swapped: real exit column bare `non-zero`, gate column `0`…`1`…`2` | 1 (`thin`) | met, thin [] | **0** ← bypass |
| A4 | one row, cell 0 = "`…c1-counter.py` and `…c1-run.sh`" | 1 (both not satisfied by one row) | unregistered `['tools/round-44/c1-run.sh']`, rows 5 | **1** ✔ attack fails |
| A3 | scope names `tools/round-45/ghost.py`, which exists at no rev; a good row names it | 1 or 2 | met, unregistered [] | **0** ← bypass (disclosed) |
| A6 | cell 0 = ``see `path` (wrapper)`` (embedded, not exact) | 1 | met | **0** ← bypass |
| A7 | fenced good rows *first*, honest `non-zero` rows after | 1 | met, rows 12 | **0** ← bypass (first-wins) |
| A7b | honest `non-zero` rows first, good rows after | 1 | thin = all six | **1** ✔ (order-dependent) |
| A8 | six rows naming other tools (`tools/round-40/*`) | 1 | unregistered 6 | **1** ✔ kill rule holds |
| A9 | cell 0 = backticked `…counter.py.bak` | 1 | unregistered 6, rows 0 | **1** ✔ (backtick-anchored) |
| A9b | cell 0 = backticked `…counter.py --selftest` | 1 | unregistered 6, rows 0 | **1** ✔ |
| A9c | cell 0 = backticked directory `tools/round-44/` | 1 | unregistered 6, rows 0 | **1** ✔ |
| A10 | **combined minimal exploit**: §3 | 1 | met, rows 6 | **0** ← cheapest |

### Attack 1 — do the six scope paths really lack rows at the freeze?

Yes, and the claim's numbers are exact.
`git show <freeze>:SKILL.md | grep -c 'round-44'` → **0**; `grep -c 'round-45'` → **0**;
each of the six paths → **0** occurrences. All six paths **exist** at the freeze
(`git cat-file -e <freeze>:<path>` → present, six of six).

```
python3 -I -B tools/round-45/c2-counter.py --root "$PWD" \
  --freeze f762b727… --rev f762b727… --json-out …/c2-freeze.json
```
exit **1**, `unregistered` = the six, `registered []`, `thin []`, `registry_rows 39`,
`scope_size 6`, `frozen_path_changed []`. sha256 `f61c6b99…`; 2026-10-28T15:39:10Z.
`diff` against `.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json` → **identical**.
Base `149133d4` → exit **2** `scope file absent at rev`; `diff` against
`controls/ctl-c2-0-base-unevaluable.json` → **identical**. Landing `e715263c` → exit **0**;
`HEAD` `faa875bc` → exit **0**, `registry_rows 45` (`c2-e715263c.json`, `c2-head.json`).
No merges in `FREEZE..HEAD` (`git rev-list --merges` → 0), so F1 is latent this round.

### Attack 2 — code fence / HTML comment

`parse_rows` is line-oriented: `s.startswith("|")` then `s.strip("|").split("|")`. It tracks
no fence state, no comment state, no heading state. A draft table that was never published
scores the target. The three variants A2a/A2b/A2c all exit 0 with `rows 6`/`rows 12`.
Note the direction of the danger: a **fenced or commented-out draft** is exactly the state a
careful author leaves behind while drafting the landing.

### Attack 3 — does the counter verify the tool EXISTS at the revision?

**No.** `evaluate()` calls `show()` only for `SCOPE` and `SKILL.md`; it never probes the scope
paths. A3: a six-path scope whose last path is `tools/round-45/ghost.py` (absent from the
tree) scores exit **0**, `unregistered []`. A row for a deleted instrument therefore passes —
the registry can name a dead tool and the calibration gate stays green.

This one is **already disclosed and routed**: `SKILL.md:1643-1645` ("Limit: `c2-counter.py`
checks that a row names the path, not that the tool exists at `--rev` (routed R45-CL2)") and
`corpus/lessons/round-45.md:73-75`. The disclosure is accurate. It is a known limit, not a
hidden defect — but it is the limit that makes F2/F3 worse: registry *provenance* is the whole
subject of the claim, and "names" is all that is checked.

### Attack 4 — can a single row satisfy two scope paths?

**No.** A4: `ROW_TOOL.search(cells[0])` returns one match, `by_tool` keys on it; the second
path in the same cell is never registered (exit 1, `unregistered ['tools/round-44/c1-run.sh']`).
A8 confirms the other half: six rows naming other tools leave all six unregistered (exit 1).
The kill rule's sentence "Row counting cannot substitute for path equality" **holds**. The
residue is F2: the cell may *contain* the path, so equality is at the backticked-span level,
not the cell level. A9/A9b/A9c show the regex is anchored by the closing backtick, so
`…py.bak`, `…py --selftest` and directory cells all correctly fail.

### Attack 5 — prose naming 0/1/2 without a verdict map

**Yes, satisfiable.** `exits_ok` is `all(re.search(r"\b%d\b" % d, cell) for d in (0,1,2))` —
pure token containment on `cells[2]`. A5 `0 rows, 1 column, 2 bytes` → exit **0**.
A5b `0/1/2` → exit **0**. No verdict word ("met"/"not met"/"unevaluable") is required, and the
header is never checked, so A5c passes with the *real* exit column reading `non-zero` because
`cells[2]` happens to be the gate prose. The kill-rule sentence "a bare 'non-zero' cell is
thin" is true only when the bare cell sits in column 3 *and* no other column supplies the
tokens.

## 2. Freeze-integrity arm — the one defect that is not merely permissive

Arm probes (`c2-freeze-arm.json`, sha256 `5df2b9dd…`), same fixture shape, one post-freeze commit:

| probe | exit | `frozen_path_changed` |
|---|---|---|
| add `tools/round-45/extra.txt` | **2** | `['tools/round-45/extra.txt']` |
| append `plans/round-45-claims.md` | **2** | `['plans/round-45-claims.md']` |
| rename `tools/round-45/x.py` | **2** | `['tools/round-45/x2.py']` |
| delete `tools/round-45/` | **2** | the four files |
| touch then `git revert` (restore in history) | **2** | `['plans/round-45-claims.md']` |
| touch `SKILL.md` only (not frozen) | 0 | `[]`, `met_target: true` |

So the directory pathspec, the restore-in-history rule and the non-frozen `SKILL.md` case are
all correct. The arm is nevertheless false on merges:

```
freeze..rev contains a merge commit whose resolution appends one line to
plans/round-45-claims.md; neither parent commit touches a frozen path.

c2-counter (frozen)      -> exit 0, met_target: true, frozen_path_changed: []
frozen-path-preflight    -> exit 1, verdict frozen_path_changed,
                            touched:[{path: plans/round-45-claims.md, status: M}]
c1-counter (frozen)      -> exit 1 for block-22 clauses, frozen_path_changed: []  (arm missed)
```

Receipts: `c2-evil-merge.json` (sha256 `d388e518…`), `preflight-evil-merge.json`
(sha256 `56f39bec…`). `git diff --stat <freeze> <rev> -- <frozen>` shows the frozen file
differs by one insertion; `git log --name-only <freeze>..<rev> -- <frozen>` prints nothing
(plain `git log` suppresses merge diffs), while `git log -m --diff-merges=first-parent`
prints it.

Why this matters more than a permissive parser: the claim's own **Freeze-integrity rule** says
a score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path, and
that "a touch makes the counter exit 2 `frozen_path_changed` and print no `met_target`". An
inadmissible score is printed as `met_target: true`. This is a **regression of a defect the
lane already scored red**: `plans/round-44-claims.md:28-30` records "Freeze-walk port source:
`tools/round-43/c1-counter.py` (merge-aware `git log -m --diff-merges=first-parent`, status
filter, tree blob backstop) — NOT round-42's walk, which **misses merge-commit edits**
(R44ConnPattern probe, control scored red on the round-42 walk)." Round 45's `c2-counter.py:52-56`
is the round-42 walk. `c1-counter.py:52-53` is the *same three lines*, and it misses the same
merge (verified). The preflight is the only frozen instrument that gets this right — and its
selftest has no merge case, so that behaviour is untested there.

Latent, not live: 0 merges in `FREEZE..HEAD`, so the claimed pass at `e715263c` is admissible
today. It stops being admissible the first time a lane reconciliation or `jj` merge lands in
the range.

## 3. The cheapest bypass (named)

**Six fenced table rows, embedded paths, junk exit cell, anywhere in `SKILL.md`.**

```
## Random notes

```
draft, not published
| see `tools/round-44/c1-counter.py` (wrapper) | ?? | 0/1/2 |
… five more, one per scope path …
```
```

Verified end-to-end as one fixture (`c2-cheapest-bypass.json`, sha256 `c5bd3c1f…`, 2026-10-28T15:44:29Z):
442-byte `SKILL.md`, no registry heading, no table header, no verdict map, paths only
*contained* in cell 0, exit cell `0/1/2` → **exit 0, `met_target: true`, `thin []`, `unregistered []`**.
No registry row exists, no exit semantics are stated, and the text is visibly a draft. Cost:
one paste. It needs A2 (fence), A6 (containment) and A5b (token cell) at once; each was
verified separately and the union is verified here.

Cheapest **freeze** bypass (different object): `git merge --no-commit` + one appended line +
`git commit`, one commit, no side-branch commit needed.

## 4. Verified clean (so the critique is calibrated)

- Base exit 2, freeze exit 1, landing 0, HEAD 0 — all reproduced; controls byte-identical.
- The landing rows themselves are honest: `SKILL.md:1636-1641`, first cell exactly
  `` `tools/round-44/c1-counter.py` `` etc., third column real verdict maps
  (`0 met; 1 not met; 2 could-not-evaluate …`). The counter's 0 is earned by these bytes.
- `scope_size` is read from `registry-scope.json`, not assumed; a 5-path scope fails (selftest
  `red-scope-size`, exit 1).
- Scope completeness: the union of `tools/**/*.py|sh` named by the two claim files is **8**,
  but `tools/round-42/c1-counter.py` and `tools/round-43/c1-counter.py` are named by
  `plans/round-44-claims.md:306-308` as "audit-only port sources" under **Frozen paths**, not
  as claim-carrying instruments. The six is defensible for "round-44/45 claim-carrying
  instruments". **Minor precision defect:** `registry-scope.json:why` says round-44 "names
  c1-counter.py, c1-run.sh and c2-counter.py" — it names those five; the sentence understates
  what it names and should say why the two port sources are excluded.
- Claim citation `corpus/lessons/round-44-verifier-spotcheck.md:166` resolves and does carry
  the routed registry gap ("no SKILL.md registry rows for the round-44 counters").
- C2 selftest at the freeze: 7 cases, 0 failures, exit 0 (matches `controls/c2-selftest.txt`).

## 5. Impacted axes

- **calibration — direct.** C2 is the calibration claim. Its gate accepts a fenced draft with
  a junk exit cell, and its own documentation (`SKILL.md:1629-1630`) asserts the stronger
  guarantee that A6 falsifies. A calibration instrument whose advertised strictness exceeds its
  implementation is the failure mode the axis exists to catch.
- **depth — indirect.** R45-C1 shares the same freeze-integrity rule and the same merge-blind
  walk (`c1-counter.py:52-53`, verified). Block 22's decision table may cite the preflight
  safely; it cannot cite "both counters implement the arm" as it stands.
- **coverage — no claim this round**, no impact found.

Not found: duplicate scope paths, wrong-path substitution, single-row double-count, or a
suffix/args/directory cell passing. The kill rule's *path*-equality half is sound.

## 6. Smallest safe corrections (frozen bytes are not touched by this seat)

Nothing in `tools/round-45/` or `plans/round-45-claims.md` can change in-round without
`frozen_path_changed`, so:

1. **Landed prose (not frozen, correct now):** `SKILL.md:1629-1630` says a row counts "only
   when its first cell is that exact backticked path". The instrument enforces "the first cell
   contains a complete backticked `tools/….py|sh` span". Either weaken the sentence to what is
   enforced, or keep the sentence and add one clause naming the enforced check. Smallest edit
   that removes false provenance.
2. **Route R45-CL5 (new, higher severity than CL2):** both R45 counters' freeze arms are
   merge-blind. Use the round-43 walk the lane already blessed —
   `git log -m --diff-merges=first-parent --name-status` **plus the tip blob comparison** the
   preflight already implements (`blob_changed` is what actually caught the evil merge) — and
   add a `red-evil-merge` selftest case to both counters *and* to the preflight's 11.
3. **Wave 2 must not treat the frozen counter as the falsifier of the registry claim.** Two
   mutants it currently cannot tell apart: (a) the landing rows moved into a fence/comment —
   still exit 0; (b) a merge-introduced frozen touch — exit 0. If wave 2 asserts "the counter
   goes red", it will be wrong on both. Add the two mutants and score the *landing* against the
   strong predicate (exact cell, registry heading, header-validated exit column) by an
   augmented check, or record the claim as met-on-bytes with an explicit instrument-weakness
   note.
4. **Minor:** correct `registry-scope.json:why` (it names five round-44 paths, not three) in the
   next refreeze; scope membership itself is right.

Side finding, offered not scored (wave-1 instrument verification): `tools/round-45/c1-counter.py:60`
does `skill.split("## Queue-drain craft ", 1)[1]` unguarded. A `SKILL.md` that lacks that exact
heading (with trailing space) raises an uncaught `IndexError` with a traceback and exit 1,
where the contract wants exit 2 could-not-evaluate. Repro: fixture `SKILL.md` with
`## Queue-drain craft` and no trailing space → `IndexError: list index out of range` at line 60.
That is a misclassified exit, not a pass — but a crashing instrument cannot emit `met_target`
either, so it is safe, just wrong.

## 7. Receipts (all in this directory; lane UTC 2026-10-28)

| file | sha256 | command / exit |
|---|---|---|
| `c2-freeze.json` | `f61c6b997f6151ea3cd086bce9625ad6e1a27e558c5c3c74961023d705d2c630` | counter `--freeze F --rev F`; exit 1; identical to committed control |
| `c2-base.json` | `9c09b1d76b1a3bf1df8b934ca0e851a5eb0bbf27ce83c395fb1ef208ee36c9f3` | counter `--freeze B --rev B`; exit 2; identical to committed control |
| `c2-e715263c.json` | `3efa93b556a14435bfc11a5ba08516c457a130b0d34d50a4393e85c2d9c79447` | counter at landing; exit 0 |
| `c2-head.json` | `042ff4dd269348821b4525ad2062843f8eb6d6e60c631db7f1637cf92f34c4bd` | counter at `faa875bc`; exit 0 |
| `c2-attacks.json` | `0c86da2514cc4bc996d3c0ef275fb585c6a0306f01325014d169bfa3df8f872e` | A0–A8 matrix; fixture repos |
| `c2-attacks-extra.json` | `4ee75ca049fc9d13f8d7dc284a5bcd13e0d5ead4e69a2830dcc17270cd566bff` | A9/A9b/A9c receipts; exit 1 each, `rows 0` |
| `c2-cheapest-bypass.json` | `c5bd3c1ff4976c17e7f288c17f4cd3de0d1345e9e2b7926d121906dd7361eb0b` | A10; exit 0, met |
| `c2-freeze-arm.json` | `5df2b9ddd2cb2160eeab23bd259564d32a39420963a578256920468cb4ece6db` | six arm probes |
| `c2-evil-merge.json` | `d388e518d5d506fb765a7357084b16e4e26578c7d1830ae8fa777690d9295644` | counter on evil merge; exit 0, met true |
| `preflight-evil-merge.json` | `56f39bececff76018a39513e895248d72b52a22beb00ce410e67b6ed61a99fab` | preflight on same history; exit 1 |

Not run (stated, not passed): the C1 counter's full selftest and any C1 scoring; the round-44
c1/c2 selftests asserted green by the registry rows; S140/S141 quote verification; the wave-2
spec. No frozen byte was modified; no git state was mutated; scratch removed after copying.
No tool installs were needed.
