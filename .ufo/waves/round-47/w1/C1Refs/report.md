# R47-C1 clause 8 — verification, candidate and attacks (seat C1Refs)

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze and measured revision
`5017e1f7299c3a812e87e7950148f54313dd279e` (re-derived: `git log --format=%H -1 --
plans/round-47-claims.md tools/round-47/`). Everything below was produced read-only on the lane
tree; every candidate and attack ran in a one- or two-commit fixture repo under
`/fast/scratch/hyaku/kaidoku-r47/C1Refs` (removed at yield).

Axis read: **coverage** = every separately-checked sub-binding of clause 8 has a green probe and a
red probe; **depth** = the clause is attacked for vacuity and for a conflict with the battery that
gates it; **calibration** = each quoted value is a receipt field or a reported exit code, never a
restatement of the claim.

## 1. The claim's clause 8 and the code that computes it

`plans/round-47-claims.md:83-84` at the freeze:

> 8. `refs >= 3`, every reference carries a line selector and resolves at `--rev`, the path set
>    is validated, and `corpus/lessons/round-46.md` is cited; both sha256 pins match.

Landed-surface sentence the predicate abbreviates (`plans/round-47-claims.md:60-66`):

> at least three citations carry a line selector while resolving at the measured revision inside
> `corpus/lessons/`, `corpus/knowledge/`, `plans/` or `tools/round-47/`, and
> `corpus/lessons/round-46.md` is among them; the block carries `mutations_sha256:<64 hex>` equal to
> the digest of `tools/round-47/exact.py`'s own `MUTATIONS` name list in order, and
> `interpreter_sha256:<64 hex>` equal to the sha256 of `tools/round-47/exact.py` at the measured
> revision.

The implementation (`tools/round-47/exact.py`, `check_refs` at `:152-176`, clause-8 block at
`:262-291`):

```python
HARD_REF = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")
ALLOW = ("corpus/lessons/", "corpus/knowledge/", "plans/", "tools/round-47/")
MUST_CITE = "corpus/lessons/round-46.md"
...
def check_refs(block, files, hard):
    bad, cited = [], set()
    for name, first, last in HARD_REF.findall(block):
        if not name.startswith(ALLOW): bad.append(f"{name}: outside the validated path set"); continue
        cited.add(name)
        if name == SELF: continue          # identified by its own sha256 pin, not by a line selector
        if hard and not first: bad.append(f"{name}: no line selector"); continue
        count = line_count(files, name)
        if count is None: bad.append(f"{name}: absent at rev"); continue
        start, end = int(first or 1), int(last or first or 1)
        if not (1 <= start <= end <= count): bad.append(f"{name}:{start}-{end} outside 1..{count}")
    return bad, cited
```

and in `score`: `receipt["refs"] = len(HARD_REF.findall(block))`; failing clauses
`refs < 3`, `unresolved or unvalidated citations: N`, `does not cite corpus/lessons/round-46.md`,
`interpreter sha256 pin does not match the bytes at rev` (the `mutations_sha256` twin lives in
clause 6 at `:237-247`).

## 2. The freeze receipt (do-nothing), exact command

```
$ HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1Refs python3 -I -B \
    tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --freeze 5017e1f7299c3a812e87e7950148f54313dd279e \
    --rev    5017e1f7299c3a812e87e7950148f54313dd279e \
    --json-out .ufo/waves/round-47/w1/C1Refs/receipt.json
```

| field | value |
|---|---|
| exit | **1** (UTC `2026-10-28T17:54:40Z`) |
| `failing` | `["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]` |
| `block_present` / `marker_occurrences` / `rule_blocks` | `0` / `0` / `23` |
| `frozen_derived` / `frozen_path_changed` / `touched` / `restored` | `["tools/round-47/", "plans/round-47-claims.md"]` / `[]` / `0` / `[]` |
| `battery` | `{"skipped": "artefact fails a structural clause first"}` |
| stdout sha256 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` |

This reproduces the claims' `## Before` bullet exactly (`block_present 0`, `rule_blocks 23`,
`marker_occurrences 0`). One wording divergence: the claims say the battery "cannot even be built
(`marker blocks 0`)", but the CLI never calls `run_battery` when a structural clause is already
red — the freeze receipt says `skipped`. Calling `run_battery` directly at the freeze does print
`{"error": "cannot build a battery: marker blocks 0"}` (run in scratch, same UTC day), so a
control receipt that quotes the error string has to come from the library call, not the CLI.

## 3. Candidate: the failing list empties, end to end

Candidate text is `rows.md`. Two-commit fixture repo: commit 1 = the lane's bytes at the freeze
(SKILL.md still 23 blocks), commit 2 = SKILL.md with the candidate block appended as the last
craft block; then the frozen counter's own CLI:

```
$ python3 -I -B <lane>/tools/round-47/exact.py --root <fx> --freeze <c1> --rev <c2>
```

| run | v3 exit | `failing` | battery |
|---|---|---|---|
| candidate block 24 | **0** | `[]` | `forgeries_total 4`, `v2_green 4`, `v3_green 0`, `genuine_green 1`, `crash 0` |
| same block, `--profile v2` | 0 | `[]` | — |
| candidate + a fifth row on `R46-CL2` (clause 8 untouched) | 1 | only `["rows 5 != 4", "routed cardinality {'R46-CL2': 2, 'R46-CL3': 1, 'R46-CL4': 1, 'R46-CL6': 1} != each of [...] exactly once"]` | `{"skipped": ...}` |

So with block 24 present the two structural reds of §2 disappear and nothing clause-8-shaped
appears; the third row shows the list carrying *only* the other clauses (3 and 4) when clause 8 is
deliberately left green. Fixture commits (ephemeral, deleted): `f502b91a`→`e5778c45` (candidate),
`ae5280b9`→`65fb871b` (fifth row). v3 stdout sha256
`267d7c86b685ccbf736e42dee5cba2265ab8796cabcd99c559e20d29b40ebe39`; every battery fixture reports
`v2_exit 0, v3_exit 1` — the four holes are measured, not asserted.

Clause 8 values on the candidate: `refs 10`, `cited ["corpus/lessons/round-46.md",
"plans/round-47-claims.md", "tools/round-47/exact.py"]`, `unresolved []`,
`mutations_sha256 == 19a2166e…a112` (match), `interpreter_sha256 == dcef54f1…412c` (match),
`gate_order_literal 1`, `gate_order_reversed 0`.

The uncommitted working-tree block (not this seat's write; it changed between two of my reads —
arm cells went from `` `symbol` (the equality) `` to bare `` `symbol` `` — so a sibling is editing
`SKILL.md` now) also measures exit 0 with the battery green on the same harness. That is
consistent with `rows.md`, but `rows.md` is the stable reference.

## 4. Clause-8 sub-bindings: green and red probes

Each red row fails **only** clause 8 — every other clause stays green in that fixture.

| probe | what it isolates | verdict |
|---|---|---|
| `F` `tools/round-46/gate.py:99` added | path-set validation is a string prefix; the gate path is not in `ALLOW` | exit 1 `tools/round-46/gate.py: outside the validated path set` |
| `G` `round-46.md:0-66` | selector lower bound | exit 1 `corpus/lessons/round-46.md:0-66 outside 1..102` |
| `H` `round-46.md:57-103` | selector upper bound (file has 102 lines) | exit 1 `…:57-103 outside 1..102` |
| `I` interpreter pin zeroed | pin is compared with sha256 of the bytes at rev | exit 1 `interpreter sha256 pin does not match the bytes at rev` |
| `J2` every `round-46.md` cite swapped to `round-45.md` | must-cite binding | exit 1 `does not cite corpus/lessons/round-46.md` |
| `M` one selector dropped from a cites | per-occurrence selector requirement | exit 1 `plans/round-47-claims.md: no line selector` |
| `R` single remaining citation | `refs >= 3` floor | exit 1 `refs 2 < 3` |
| `P2` floor padded by SELF, two selected cites | F2 | exit 0 — the divergence |
| `D` three repeats of one line | F1 | exit 0 — the divergence |
| `E` `plans/:1`, `tools/round-47/:1-2` | F3 | exit 0 at rev, exit 1 only inside the battery |
| `B` candidate | all of the above green | exit 0, `failing []` |

Attacks that returned **negative** (the clause holds): a `..` traversal inside an allowed prefix
(`corpus/lessons/../../SCORECARD.md:1`) does not resolve — `git show <rev>:<path>` returns
non-zero, so it lands in `absent at rev`; the reason is git's own refusal, not a counter check.

## 5. Findings against the frozen clause (do not fix frozen bytes)

**F1 — clause 8 is satisfiable by a content-free citation set.** Three repeats of one line —
`` `corpus/lessons/round-46.md:57`, `corpus/lessons/round-46.md:57`, `corpus/lessons/round-46.md:57` ``
plus the two SELF mentions in the narrative — give `refs 6` over **two distinct paths**
(`corpus/lessons/round-46.md`, `tools/round-47/exact.py`), `unresolved []`, exit **0**, battery
green. Nothing binds a citation to the row it is supposed to ground.

**F2 — `refs >= 3` counts occurrences, not selected citations.** The claim says "at least three
citations carry a line selector"; the code counts every `HARD_REF` match, and `SELF` needs no
selector. Proof fixture `P2`: the prose lesson cite is removed, the Refs line is
`` `tools/round-47/exact.py`, `corpus/lessons/round-46.md:57`, `plans/round-47-claims.md:1` `` —
`refs 5`, exactly **two** selector-carrying non-SELF citations, exit **0**, battery green. The
floor is padded by the interpreter's own path, which is cited three times (narrative, pin line,
Refs).

**F3 — a directory resolves as a reference.** `plans/:1` and `tools/round-47/:1-2` pass at the
lane rev (`git show <rev>:plans/` is a tree listing; `plans/:1` is inside `1..1`), exit 0 with
`refs 6`. The path set is validated by string prefix only, so "the path set is validated" does not
mean "a file". (At the battery's fixture rev this same block goes red — see F4 — which is the only
reason it would ever be caught.)

**F4 — clause 8 and clause 9 partition the citation universe, and the battery decides it.** The
battery's fixtures come from `_fixture_files` (`exact.py:344-352`): `SKILL.md`,
`plans/round-47-claims.md`, `tools/round-47/exact.py`, `tools/round-46/gate.py`,
`corpus/lessons/round-46.md`, `corpus/lessons/round-45.md`. Any citation outside that set scores
red **inside** the battery even though it resolves at rev. Measured on identical block text with
one added knowledge citation:
clause 8 exit **0** (`refs 11`, `unresolved []`), full counter exit **1** with
`["battery v2_green 0 != 4", "battery genuine_green 0 != 1"]`, every one of the four forgeries
`v2_exit 1`. So block 24 must cite only lessons/plans (and the interpreter), or the landing cannot
be green.

**F5 — F4 collides with `corpus/QUALITY.md` Row 77(a), and the cost is measurable.** Row 77(a)
(`corpus/QUALITY.md:139`): the depth proxy "counts only `corpus/knowledge/` citations inside
`## Queue-drain craft` blocks". Recipe A (verbatim from `SCORECARD.md` `## Measurement recipes`)
run in the same two fixtures:

| landing | counter | `citation_resolved_rules` | `depth_score` | `uncited_rules` |
|---|---|---|---|---|
| block 24 with no knowledge cite (green) | exit 0 | `23/24` | **9.58** | `[24]` |
| block 24 + `corpus/knowledge/…gate-stop.md:40-66` | exit 1 (battery) | `24/24` | 10.0 | `[]` |

That is M46-4 recurring by construction: with the frozen clause 9 satisfied, the round-47 depth
claim lowers the depth proxy it raises. The L1 cannot have both on these bytes; it must either
land 23/24 and record the harm in the round report, or land 24/24 and report clause 9 unmet.

**F6 — `--selftest` is not runnable as written (R46-CL8 class).** `python3 -I -B
tools/round-47/exact.py --selftest` exits **2** — argparse demands `--root/--freeze/--rev` before
the selftest branch is reached. The runnable form adds them
(`--root <lane> --freeze <F> --rev <F> --selftest`) and prints
`EXACT_SELFTEST: cases=16 failures=0`, exit 0, stdout sha256 `0249b80f…8aaa`. A landing report that
quotes the bare form records a could-not-evaluate, not a measurement.

**F7 — clause 8's red cases are only partly self-tested.** The selftest carries
`red-ref-no-selector`, `red-ref-outside-allowlist`, `red-pin-mismatch`; it has **no** case for
`refs < 3` and **no** case for the missing must-cite. Both are real (probes `R` and `J2`), so the
instrument's own discrimination does not cover two of clause 8's four bindings.

## 6. Lane state after the freeze (context; not this seat's claim)

The lane moved while I measured. Both facts below are receipts, not judgements:

| measurement | command | result |
|---|---|---|
| frozen paths drifted | `--freeze 5017e1f7… --rev a631bba01633d2b5353306a569be4ce2e683d364` (`count-head.out`, UTC `17:57:54Z`, sha `37c62584…c280`) | **exit 2**, `reason frozen_path_changed`, `blob_changed ["plans/round-47-claims.md", "tools/round-47/"]`, `touched ["plans/round-47-claims.md", "tools/round-47/record.py"]`, `restored ["tools/round-47/record.py"]` |
| the same rev under the last frozen-path commit | `--freeze 07d2894e… --rev a631bba0…` (`count-head2.out`, `17:58:24Z`, sha `238cebab…4485`) | **exit 1**, `failing ["battery v2_green 0 != 4", "battery genuine_green 0 != 1"]`, `refs 9`, `cited` includes `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` — F4 on the real lane |
| A2's declared freeze no longer evaluates | `--freeze 62e33f7d --rev a631bba0` | exit 2, `blob_changed ["tools/round-47/"]` |
| A6 changed the interpreter | `sha256sum` of `tools/round-47/exact.py` at `f54b3b6d` vs at the freeze | `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5` vs `dcef54f1…412c`; block 24's `interpreter_sha256` follows the new bytes (pin match `True`) |
| live verdict after A6 | `--freeze f54b3b6de9085d3db449ed5d0916296cb29c1f6d --rev 31b092d17e77f5064c919383a9bc1e6cbfd2d1ff` (`count-live.out`, `17:59:37Z`, sha `b95251e8…c0a3`) | **exit 0**, `failing []`, `rule_blocks 24`, battery `4 / 4 / 0 / 1 / 0` |

Consequence for R47-C1: the frozen pathspec now last moved at `f54b3b6d` (a seven-commit series
`5017e1f7`, `9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`, `f54b3b6d`), so any
measurement that passes `--freeze 5017e1f725…` to a rev after A1 exits 2, and the interpreter whose
clause 8 I verified (`dcef54f1…` at the freeze) is no longer the bytes that score the block. The
claim's freeze sentence ("the commit that first contains this file and `tools/round-47/`") is
false for the current scoring bytes — the M46-3 `freeze-moved-N-times` class, now at N = 7.

Discarded probe: a scoped-repair fixture I built to drop the landed knowledge citation was
mis-scoped (`skill.index(", \`corpus/knowledge/")` matched block 23's citation first) and produced
a 23-block tree; it is not cited anywhere and its files are not among the receipts.

## 7. What I did not run

- No lane-tree write, no commit, no `SKILL.md` edit; `git status`/`show`/`ls-tree` only.
- No landing measurement on the real lane: block 24 is uncommitted in a tree a sibling is editing,
  and my seat may not commit. The landing measurement is the L1's, on the revision it lands.
- `tools/round-47/record.py` (R47-C2) untouched — other seats own it.

## 8. Receipts in this directory

| file | what it is | sha256 |
|---|---|---|
| `receipt.json` | the freeze counter receipt (§2) | `88fafc60…f28ba` (identical bytes to stdout) |
| `count-freeze.out` | captured stdout of §2 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` |
| `runs.json` | 18 clause-8 probes (lane / fixture / battery verdicts) | `6e12fda7fd1c69ef1c8602bf979d539fbcd4ea42745323401ec785215112ccae` |
| `landing.json` | end-to-end CLI runs + recipe A for three landings (§3, F5) | `0e235124b674b8525313968f69892365ba3cc7a8fa9dedc778a9aee653a99de3` |
| `selftest.out` | runnable selftest, 16 cases (F6) | `0249b80f58085f0d52cca3f7ae3f731d88d38dd4daaca6f84cefa023e3028aaa` |
| `count-head.out` | counter with the freeze argument and a post-A1 rev (§6) | `37c625849576a5b2b88f043580ff7fa4cfeb09b8ceece4ca38081fbf2143c280` |
| `count-head2.out` | the same rev under `07d2894e` (§6) | `238cebab7a5c6a3d4240acb31910c2d4840a0ac88976cf5dc6d4f54b44674485` |
| `count-live.out` | live verdict under A6 (exit 0) | `b95251e88c4adc085f9317a12b34f8b2e4385235e5f1f886ed176bca5219c0a3` |
| `drive.py`, `land.py`, `recipeA.py` | the harnesses that produced the above | — |
| `rows.md` | the paste-ready block and its computed selectors | — |
