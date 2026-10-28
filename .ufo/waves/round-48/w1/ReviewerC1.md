# ReviewerC1 — surgical correctness review of `tools/round-48/meanings.py`

Seat: reviewer. Scope: `tools/round-48/meanings.py` (R48-C1 counter). Read-only on the lane;
probes ran against a byte copy at `$S/mod/` (sha256 `00f768c5…` = worktree = freeze bytes).

## 0. Freeze lineage — the prompt's declared SHA is superseded (read before adjudicating)

`git log -- plans/round-48-claims.md` shows FOUR amendment commits after the prompt's
declared freeze `dc73587a` (= A1, 15:41 -0300):

| commit | amendment | fix |
|---|---|---|
| `ac02a79f` | A2 | exit-0 classifier false-red on `failing` in prose |
| `f3a7afc4` | A3 | census clause compared dict `==` list (never equal) |
| `0f06251b` | A4 | `0=not met` scored success; rows written `\|  \`p\`` skipped |

The claims file's own rule ("the declared freeze is the commit that carries this
paragraph") makes **`0f06251b` (A4) the live freeze**; HEAD `663f30ee`, worktree clean
under `tools/round-48/` + `plans/` (verified `git status --porcelain`, `sha256` match).
Receipt `rc-stale.json`: running against the prompt's `--freeze dc73587a` exits **2**
`frozen_path_changed` (`tools/round-48/` + `plans/round-48-claims.md` changed) — correct
behavior, and the proof that A1 is dead. **All findings below are on the A4 bytes**
(file sha256 `00f768c52a78f18a359c193cff08728a8dd8989e45121e7d496012d93d2649d0`, 735 lines).

A4 absorbed three of the assigned suspects before this seat ran: the census `dict==list`
(always-false → `derived.get("paths")`, :437), the `0=not met` opposite-polarity green
(→ `NEGATED`, :62,242), and the `\|  \`path\`` skipped row (→ `ROW_START`, :201,191,209).
What follows is what survives A4.

## 1. Findings (by severity)

### F1 — `SEG` matches a digit inside a word: hole in BOTH directions — HIGH
`meanings.py:57` `SEG = re.compile(r"(?<![0-9])([012])\s*=\s*")`, consumed at :217-223.

The lookbehind only excludes a preceding `[0-9]`; a preceding *letter* passes, so `x0=`
is a segment mark.

- **False-green (forgery-positive).** A verdict cell with NO real `N=` segments still
  parses and classifies green because the junk letters fold into segment text:
  `_segments("x0=met; x1=preferred; x2=refus")` → `{'0': 'met; x', '1': 'fail; x'…}`
  → `meaning_classes` → `{'0':'success','1':'not-met','2':'unevaluable'}`. End-to-end:
  registry verdict `x0=met; x1=preferred; x2=refus` → `score()` exit **0**
  (`probes.json: forge-letter-prefix-segments`). The claim's "`N=meaning` segments"
  clause binds nothing structural.
- **False-red.** Legitimate prose containing `sha1=`, `p2=`, `h2=` etc. injects phantom
  marks → order check `["0","1","2"]` fails → `{}` → error. `0=met, sha1=abc pinned;
  1=not met; 2=could-not-evaluate` → exit **1** (`probes.json: falsered-sha1`,
  `falsered-p2`). Same class as the A2 defect — prose that must be written dishonestly
  to satisfy the counter.
- Fix shape: `(?<![0-9A-Za-z_])([012])\s*=` or a `(?:^|[;\s])` left context.
- Related absorption: `0=met;1=fail;2=err;9=more` parses (`9=more` folds into segment 2);
  `=0=met` (leading `=`) also matches. Both green-able variants of the same anchor gap.

### F2 — `NEGATED` enumerates two phrases; opposite-polarity green survives A4 — HIGH
`meanings.py:62` `NEGATED = re.compile(r"\bnot\s+met\b|\bno\s+verdict\b")`, guard at :242.

A4 blocked only the literal counterexample. Every other negation phrasing still classifies
the exit-0 segment as `success` (`SUCCESS` matches `met`/`verified`/`ok`; `NEGATED` sees
nothing):

- `0=never met; 1=preferred; 2=refus` → all three classes → `score()` exit **0**
  (`probes.json: forge-never-met`)
- `0=not verified; 1=preferred; 2=refus` → **0** (`forge-not-verified`)
- `0=met under no circumstances; …` → `success` (unit probe)
- `0=ok but error-prone; …` → **0** (`forge-token-stuffing`) — token stuffing: an
  unevaluable-text segment carrying one `ok` reads as success. This also defeats the
  `swapped-meaning` forgery if the genuine exit-2 text contains any success token.

### F3 — meaning classes are unanchored substrings: nonsense text passes — HIGH
`meanings.py:59` `NOTMET` has `red`, `fail`, `refus` without `\b`; `UNEVAL` :61 has
`refus` bare. `meaning_classes` :236-244 checks each class only on its own segment.
- `1=preferred` → not-met (`pre[fer]red` contains `red`); `1=declared` → not-met;
  `1=scored` → not-met; `2=refus` → unevaluable (refusal/refused/anything `refus*`).
- Combined with F2 the fully-green nonsense map `0=never met; 1=preferred; 2=refus`
  is the R46-CL7 class the claim exists to close — re-opened lexically.
- Other side (false-red): `2=errors` carries no unevaluable token (`\berror\b` ≠
  `errors`), `0=meets the target` no success token — legitimate prose rejected
  (unit probes; A2-class).

### F4 — `check_refs` `SELF` skip is a free, unvalidated citation — MEDIUM
`meanings.py:267-268`: `cited.add(name)` runs **before** `if name == SELF: continue`,
which bypasses the line-selector check, existence check, and range check.
- `tools/round-48/meanings.py:99999` → `bad: []`, `cited: [SELF]` — resolves with a
  selector beyond EOF (unit probe).
- The mandated pin line already contains a bare `tools/round-48/meanings.py`
  HARD_REF (block template :611), so every conforming block's `refs` counts SELF for
  free: baseline `refs=6` with 5 written refs (`probes.json` receipt `cited`).
  `self-out-of-range-cite` → exit **0**: SELF contributes toward the "≥5 resolving
  citations" floor while never resolving.

### F5 — directory citations satisfy the knowledge-entry and refs floor — MEDIUM
`meanings.py:53` `HARD_REF` matches `corpus/knowledge/`; `line_count` :256 counts
`git show rev:dir/` output — a **tree listing**, not a file.
Verified: `git show HEAD:corpus/knowledge/` → `tree HEAD:corpus/knowledge/` + names.
- `corpus/knowledge/:3` resolves (selector ≤ listing lines) and satisfies the
  `MUST_KNOW` clause: a directory is not "a `corpus/knowledge/` entry".
- `probes.json: forge-dir-floor` → exit **0** with refs =
  `corpus/lessons/round-47.md:30-50` + three *directory* citations
  (`corpus/knowledge/:3`, `corpus/lessons/:5`, `tools/round-48/:5`) + free SELF.
  Single-level `plans/` cannot match (`/` must be followed by ≥1 name char);
  every two-level dir can. Fix: reject names ending `/` in `check_refs`, or
  `git rev-parse rev:path` + object-type check (`blob`, not `tree`).

### F6 — a data row of pure dashes is silently dropped — MEDIUM
`meanings.py:169-170`: any table line whose cells are all `:?-{2,}:?` or empty is
skipped before row counting. `| -- | -- | -- | -- |` as a third data row → `rows=2`
→ `probes.json: dashes-extra-row` exit **0**. Clause 2 says "exactly two data rows of
exactly four cells"; the third row is present in the artefact and uncounted — a
contentless row evades the exit-cell and id checks entirely (exit cell `--` never
reaches the `{0,1,2}` test :347).

### F7 — `run_battery` counts a no-op mutation as a forgery AND v2-green — MEDIUM
`meanings.py:518-521`: `if text == skill and not overrides: forgeries_total += 1;
v2_green += 1`. A mutation that changes nothing inflates both counters, so the
battery's `4/4` assertion can be satisfied with fewer than four real forgeries.
Unreachable on the current path (battery only runs when genuine is green, where all
four mutations do mutate; the `permuted-arm` no-op needs <2 rows, impossible when
green requires 2) — latent self-fulfilling denominator, flag for the next amendment
rather than a live kill.

### F8 — `ID` matches routed ids as substrings — LOW
`meanings.py:56` `ID = re.compile(r"R4[67]-CL\d+")`, applied at :358.
`xR46-CL7` → `['R46-CL7']`; `R46-CL7-and-friends` → `['R46-CL7']`. Trigger cells
`xR46-CL7` + `anything R47-CL10xx` → exit **0** (`forge-substring-id`). The
`\d+` tail is greedy so `R46-CL70` doesn't collide; only leading junk is unanchored.

### F9 — `HARD_REF` selector tail unanchored — LOW
`meanings.py:53`: `findall` ignores residue after `(\d+)`. `round-47.md:5garbage` and
`round-47.md:5-` both resolve as `:5` (unit probes). A malformed selector reads as a
clean one. Inverted `:2-1` correctly fails (:277).

### F10 — census re-derivation compares only `paths` — LOW
`meanings.py:437` `derived.get("paths") == doc["paths"]`. A committed `census2.json`
with correct `paths` but forged `rule`/`named_but_absent`/`per_claims_file` → exit 0
(`stale-census-fields-ignored`). Stale metadata ships unexamined.

### F11 — `exec` of `census2.py` is not a sandbox — LOW (mitigated by freeze pin)
`meanings.py:302` `exec(compile(tool, CENSUS_TOOL, "exec"), ns)` — `ns` carries no
`__builtins__` override, so exec'd code has full privileges. Demonstrated: an
`import os; open(…).write(…)` tool body executed and created `$S/EXEC_PROOF`.
Mitigation verified: `gate.freeze_state` (gate.py:144-195) pins `tools/round-48/` by
directory pathspec — any touch in `freeze..rev` or dirty worktree → exit 2 before
`score` runs, so only frozen bytes can ever be exec'd. Latent hazard, not a live hole
today; the `# noqa: S102` comment is accurate.

## 2. Assigned suspects checked and cleared

- **Off-by-one in segment splitting (:224-227).** `end = marks[i+1].start()` is the
  digit's start (lookbehind is zero-width); slice + `strip().rstrip(";").strip()` is
  exact. `0=;`/`0=ok ;;` fail closed. Not a defect.
- **`_segments` rstrip.** Only trailing `;`+ws stripped; interior `;` preserved as
  text (this is what lets F1's `; x` garbage through, but rstrip itself is correct).
- **Regex across cells.** `HARD_REF`'s char class excludes `|`; `ID`/`SEG`/`UNEVAL`
  run per-cell; `MUT_PIN`/`SELF_PIN` per-block (cells are block text — intended).
  Cleared.
- **Exit-code semantics.** Malformed craft heading → 2 via Malformed (:308); absent
  census → Malformed → 1; non-Malformed exception (e.g. `KeyError` in `census_text`,
  `AttributeError` on non-dict census) → `main_guard` → 2 (gate.py:238-243). Boundary
  defensible: absent-at-rev scored as violation 1.
- **Battery wiring.** `with_battery` runs only on genuine green (:542-546); battery
  assertions apply under both profiles (:461-466). `--no-battery` can yield green
  without battery evidence — documented operator affordance, not a defect.
- **Interpreter pin.** `MUT_DIGEST` is `inspect.getsource` of the *running* file —
  correctly bound to worktree bytes, which `dirty()` (gate.py:132-141) pins to frozen
  bytes before scoring. Sound.

## 3. Selftest fidelity gap

`selftest`'s `census_text` stub returns `{'paths': list}` (:647), thinner than the
real tool's 4-key dict — it exercises `derived.get("paths")` but cannot catch an F10
regression. Selftest passed on A4 bytes (`MEANINGS_SELFTEST: cases=18 failures=0`).

## 4. Receipts (report dir `w1/ReviewerC1/`)

| receipt | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| `rc-v3.json` | `python3 tools/round-48/meanings.py --root . --freeze 0f06251… --rev HEAD --profile v3` | 1 | `7bdf3376…` | ~19:04 |
| `rc-v2.json` | same, `--profile v2` | 1 | `6ab3d688…` | ~19:04 |
| `rc-stale.json` | same, `--freeze dc73587a` | 2 | `badb2295…` | ~19:04 |
| `probes.json` | in-memory `score()` battery, copied module | 0 | `f0a50103…` | 19:05:55 |

Live-lane v3 receipt: `marker_occurrences 0`, `frozen_path_changed []`, battery skipped
— correct pre-landing do-nothing red. Probes ran read-only via `score(skill, files,
"v3", "selftest", battery=None)` on `$S/mod/` copies; no lane bytes touched, no fixture
repos needed (all findings are parse/classifier level).

## 5. Installs

None. `python3` host binary only. `/tmp` untouched (`TMPDIR`/`HYAKU_SCRATCH`=$S).

## 6. Bottom line for L1

The A4 freeze bytes are still bypassable on the claim's core clause: F1+F2+F3 give
multiple exit-0 verdict maps carrying no `N=` structure and opposite-polarity/nonsense
meanings — the R46-CL7 hole, one amendment deeper. F4+F5 weaken the citation floor to
one real file cite. Block 25 landing will additionally trip F1's false-red arm if any
verdict text writes `sha1=`-style tokens. Recommend amendment A5 before landing; all
repro inputs above are directly pasteable.
