# CriticCounter — falsification of `.ufo/waves/round-19/tools/routed-r18.py` (C1 counter)

Scope: attack the C1 counting tool for self-certification, fabrication acceptance,
unrelated-path acceptance, unknown-cause handling. Question assigned: "it runs code
from REV: do tests actually recompute substance?"

Observed main tip: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`).
Mutation clone: `/tmp/kr19-w2-CriticCounter` (`git clone -q --no-hardlinks`, detached at the tip).
All mutation commits are in that clone only; the lane was never written. No installs.

## Commands (all with exit codes)

- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-CriticCounter --rev d0690fd... --strict` → **exit 0**, `open_count 0` (all 7 named+substance green).
- `... --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict` → **exit 1**, `open_count 7, named_open 7, substance_open 7`. Red baseline holds.
- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --selftest` → **exit 0**, `SELFTEST: CLEAN cases=13`.
- `python3 -I .ufo/gates/citation-drift/citation-drift-probe.py --root <clone> --table ... --expected ... --strict --rev refs/heads/main` → **exit 1**, `CITATION_DRIFT_VERDICT: failed findings=5` (drift findings on PROVINCE/SCORECARD/README at the tip).
- `... --rev '@{0}'` → **exit 0**, resolved `rev: c974b45…` (the current HEAD of the clone — evaluated, not refused).
- `... --rev 'main@{0}'` → **exit 0**, resolved `rev: d0690fd…`.
- `... --rev 'HEAD~00'` → **exit 2** refused; `... --rev 'HEAD@{0}'` → **exit 2** refused.
- `GIT_DIR=/tmp/kr19cc-env/otherepo/.git GIT_WORK_TREE=... ... --root /tmp/kr19-w2-CriticCounter --rev refs/heads/main` → output `"rev": "d1d39e363e558fc02bd6f06f74daa256b90e6d1d"`, open 7 — the other repo's `main`, not the clone's. `--root` silently ignored.
- Mutation commits (one defect each), counter run per commit:

| commit | mutation | result |
|---|---|---|
| `5960b6d` (M1) | swap go1.24.6↔go1.25.0 sha256 in `## Installs` | **open 0 — false green** |
| `eafdbf7` (M2) | all 4 seats `cause:"unknown"`, `source:"SCORECARD.md:1"` | **open 0 — false green** |
| `4dfac6d` (M3) | all 4 seats `cause:"plausible fabricated cause: disk full"`, `source:"/nonexistent/path/transcript.jsonl:1"` | **open 0 — false green** |
| `c673c02` (M4) | registry row: `.ufo/fabricated/pins.json` **and** real probe path | **open 0 — false green** |
| `713e939` (M5) | registry row: `corpus/lessons/round-19.md` (real, unrelated) | **open 0 — false green** |
| `5a16d04` (M6) | registry row: only `.ufo/fabricated/pins.json` | open 1 — correctly red |
| `67cc2d4` (M7) | forged strict-baseline receipt, `open_count:777`, `"fabricated":true`, argv `/fake/path` | **open 0 — false green** |
| `89d0d5c` (M8) | `_validator_pin` hardcodes the digest, never reads the pinned blob | **open 0 — false green** |
| `8e36581` (M9) | dead seats `cause:""` (negative control) | open 1 — correctly red |
| `c974b45` (M10) | named line `- R18-INSTALL-RECORD: declined; no fix performed…` | **open 0 — false green** |

## Findings

### F1 — STRICT-BASELINE is self-certified; the "run" is never re-executed (fabrication)
`s_strict_baseline` (`routed-r18.py:165-189`) checks only internal consistency:
receipt JSON parses, `rev`/`argv`/`exit` fields are *self-reported*, stdout/stderr
re-hash to receipt fields, `tool_sha256` equals the blob at `tool_rev`, and
`open_count` is parsed out of the retained stdout — an author-written file. The
routed defect (spotcheck `:195`) says the exit-1-at-`9011581` claim "has no
retained receipt"; the fix retains bytes but the counter never re-runs
`routed-defects.py` against `9011581d…`. M7 (observation): a wholly fabricated
receipt/stdout pair — `open_count:777`, `"fabricated":true`, argv under `/fake` —
is accepted, defect closed. The retained stdout's `open_count 6` at d0690fd is
trusted verbatim today the same way.

### F2 — DEADSEAT-RECORD: seat set is recomputed; cause/source are presence-only (unknown-cause + fabrication)
`s_deadseat` (`:216-240`) genuinely recomputes the missing-report set from
`a245bb0`'s registration/report git objects — membership is real recomputation.
But `cause`/`source` need only be non-empty strings (`:236-239`). Observations:
M2 (`cause:"unknown"`, `source:"SCORECARD.md:1"`) green; M3 (invented cause,
nonexistent transcript path) green; M9 (empty string) red. The routed defect
(`:197`) demanded retained *failure causes*; a record of four "unknown"s or four
invented causes satisfies the counter. `source` is never checked to exist or to
be a transcript reference.

### F3 — REGISTRY-PINNED accepts unrelated and mixed fabricated paths
`s_registry` (`:243-262`): `if not any(c.rstrip(".:") in paths for c in cited)` —
one existing path anywhere in the cell suffices, and nothing checks the path is
a probe/baseline artifact. M4 (fabricated + real together) and M5 (real but
unrelated `corpus/lessons/round-19.md`) are green; only an all-fabricated cell
(M6) is red. The defect (`:198`) is "name the path or state no persisted
baseline" — naming an unrelated real path is a passing non-answer.

### F4 — INSTALL-RECORD is token presence without version↔digest association
`s_install` (`:265-276`) checks that each version string and each sha256 occur
*somewhere* in `## Installs`, plus the substring `go.dev`. M1 swaps the two
digests so `go1.24.6` pairs with the go1.25.0 archive hash and vice versa — a
wrong record, not just a loose one — and stays green. The defect (`:199`)
required tool/version/channel/sha recorded; the counter verifies the tokens,
not the record.

### F5 — The counter's own `--rev` refusal is bypassable by `@{…}` reflog selectors
`main()` (`:397-400`) refuses only `HEAD`, `@`, and `HEAD~`, `HEAD^`, `HEAD@`,
`@~`, `@^` prefixes. Observation: `--rev @{0}` and `--rev main@{0}` are accepted
and evaluate the *current HEAD / current main* (resolved `rev` printed in the
JSON is whatever the reflog yields at run time) — exactly the HEAD-derived /
moving-state class that R18-HEAD-ALIASES routed and that the probe now refuses
via `"@{" in rev` (`citation-drift-probe.py:346-347`). A counter whose own gate
is weaker than the gate it certifies undermines the "never the working tree,
pinned REV" contract (`:8-9`): under `@{0}` the "REV" silently follows the
checker's HEAD. `@{-1}`/`@{u}` happen not to resolve in this clone, but `@{0}`
and `main@{0}` do.

### F6 — `--root` is silently overridden by inherited `GIT_DIR`/`GIT_WORK_TREE`
`Git.run` (`:46-49`) passes `-C root` but inherits the caller environment; git
env vars override `-C`. Observation: with `GIT_DIR` pointing at an unrelated
empty repo, `--rev refs/heads/main` resolves and reports `rev:
d1d39e363e558f…` — *that* repo's commit — while `--root` still says the lane.
The selftest scrubs `GIT_*` (`:329-332`) but `main()`/`evaluate` do not, so the
production path is env-poisonable in jj-colocated or hook contexts. Consequence
is a wrong-repo measurement, which the JSON reports with no warning.

### F7 — HEAD-ALIASES substance green while the probe's own verdict is FAILED
`s_head_aliases` (`:206-208`) treats any non-2 exit on `refs/heads/main` as
"evaluates". Observation: the probe currently exits **1** at d0690fd with 5
`citation_dead` findings and `VERDICT failed`; the counter still reports
substance green with the why-string "refs/heads/main evaluates" — which
overstates: it cannot distinguish "evaluates clean" from "evaluates and fails".
(Inference: arguably within the defect's letter — the defect asked for refusal
coverage, not a clean main — but the why-string claims more than was measured,
and an always-exit-1 probe would also pass.) Also, the counter samples 6 alias
spellings while the probe refuses the full `@{…}`/pseudo-ref family
(`:546-558`); a probe weakened to refuse only the fixture's 6 strings is
indistinguishable (self-certification: fixtures and probe are both REV-supplied).

### F8 — Named corrections and the repaired oracle are self-certifying
- `named()` (`:284-289`) requires only a line starting `- R18-<ID>:` in both
  files. M10: `- R18-INSTALL-RECORD: declined; no fix performed, disagree with
  routing` counts as a correction. Observation.
- `s_validator_digest` exercises `_validator_pin` from REV (`:118-143`); M8
  hardcodes the correct digest (never reads the pinned blob) and stays green —
  the counter verifies the oracle *responds* correctly on two probes, not that
  it *reads the pin*. This is the inherent limit of running REV's code: the
  fixture discriminates behavior on its inputs, not mechanism.
- For the record, MIDMAP's fixture is discriminating within its scope
  (observation): `_is_analyze_step` (`receipt-validate.py:134-`) identifies the
  analyze step by argv/`step`/`name`, not position, and the red/green pair does
  exercise "pin_checks on a non-analyze step doesn't count" — the specific list
  branch the defect named. This is the strongest check in the file.

### Positive observations (calibration, not all bad)
- Red baseline reproduces exactly: 7 open at `8a8da7e`, both `named` and
  `substance` (exit 1). The `7 → 0` sweep is measured.
- Crash-is-open (`:304-305`), exit-2-on-unusable-input, per-defect mkdtemp with
  `filter="data"` tar extraction, `--no-optional-locks` — all sound.
- Dead-seat *membership* and validate16 copy digests are genuinely recomputed
  from git objects, not tokens.

## Assessment against the claim

C1's falsifiable claim is "open 7 at 8a8da7e → 0 at the delivered revision". The
counter does recompute for MIDMAP, VALIDATOR-DIGEST (partially), DEADSEAT
membership, and HEAD-ALIASES refusal coverage. But **3 of 7 substance checks
(STRICT-BASELINE, REGISTRY-PINNED, INSTALL-RECORD) are satisfiable by tokens or
self-consistent fabrications, and DEADSEAT's annotation half is presence-only**:
M1/M2/M3/M4/M5/M7/M10 all leave `open_count 0` while the routed defect remains
unfixed or the record is wrong. Calibration impact: the delivered `0` is
reachable without the substance the defects demanded, so `open_count` overstates
closure. These are fixable counter defects (tighten the checks), not a reason
the judge must reject the claim — the current artifacts happen to be honest —
but the counter does not falsify a dishonest fix, which is what it is for.

## Smallest safe corrections

1. STRICT-BASELINE: re-run the `tool_rev` blob from mkdtemp against `B18` and
   require exit 1 + `open_count` matching the retained stdout (the round-18 tool
   is pure git-object reads; this is cheap).
2. DEADSEAT: reject `cause`/`source` in a stoplist (`unknown`, `n/a`, `tbd`);
   require `source` to name at least one path readable at REV or a transcript
   reference corroborated by `w1/DeadSeatHistoryR18.md`.
3. REGISTRY-PINNED: require *every* cited `.ufo/`/`corpus/` path to exist at REV
   (change `any`→`all`), or restrict the cell to the probe's own path.
4. INSTALL-RECORD: match `version … sha` on the same line/entry
   (`re` per line), not section-wide tokens.
5. `main()`: reuse the probe's `moving_rev_cause` logic — at minimum add
   `"@{" in rev` and `_PSEUDO_REFS` — and scrub `GIT_*` from `Git.run`'s env.
6. HEAD-ALIASES: treat exit 1 as a reported finding state, not silently
   "evaluates"; extend `ALIASES` to the probe's full refusal family (`@{0}`,
   `main@{1}`, `ORIG_HEAD`, …) so a weakened probe is caught.

Evidence integrity: all mutation commits exist at `/tmp/kr19-w2-CriticCounter`
(branches m1–m10); no lane writes beyond this report; no installs performed
(git 2.56.0, python 3.14.8 already present).
