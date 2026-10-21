# Fixture19 — `historical_root_injection` source review (R23-C1)

Seat: KaidokuR23.Fixture19 · leaf · source review only. No suite, counter, or selftest execution; no mutation runs; no installs.
Candidate: 2838351450ff1ee4baa620c962a1153450d53311 · Baseline B: aa1450b82f9ede35aada63efe8a34e01c6e02f72.
Method: `git show <candidate>:PATH` for every source read; `git rev-parse`, `git diff --stat`, `git log --stat` on commits; `sha256sum` on blobs.
Labels: **observed** = read from candidate bytes or a named peer artifact; **inferred** = traced from source, not executed; **unknown** = not established.

## Verdict

- **Expected triple is correct at candidate.** `{exit 2, count null, finding unevaluable}` (expected-v2.json:98-102) matches the candidate's guard path for this input [inferred: count-c1.py:66-68 → :167-169]. Peer RunSelftest.md:42 reports the same triple from one designated run [peer-observed]. No wrong expectation found.
- **Distinguishes the stated fault only partially.**
  - Yes: removing the round-22 tree guard, or narrowing it to deletions/modifications or to bound tuples, changes this case's outcome (F3 rows M1, M6, M7).
  - No: the bindable-witness path the name refers to (F1); a guard anchored to the parent or to the worktree (F3 M2, M3); in-place edits (F3 M4); the reason for exit 2 (F2).
- **Weak mutation: yes** (F1, F3). **Weak expectation: yes** (F2). **Under-justified policy: yes** (F4).
- **Oracle independence:** literal and template-independent. The fail-closed policy is co-designed with the counter (F4).

## 1. Pins and inputs (candidate blobs)

| Blob at candidate | sha256 | Pin or check |
|---|---|---|
| frozen/expected-v2.json | 458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f | count-c1.py:25 `SELFTEST_MANIFEST_SHA256` ✓ |
| frozen/fixture.json (83 lines) | a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b | expected-v2 `inputs` ✓; `base` (fixture.json:2) = count-c1.py:26 `BASELINE` ✓ |
| tools/counter-fixtures.py (116 lines) | f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f | expected-v2 `inputs` ✓ |
| tools/count-c1.py (DUT, 173 lines) | f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2 | **not pinned** (peer RunSelftest F2) |
| round-22/tools/count-c1.py (legacy) | c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879 | count-c1.py:23 `LEGACY_SHA256` ✓ |
| round-22/evidence/c1 tree, base = candidate | b83fc459dca64a8356480b1ebc8309b4de65de71 | identical [observed] |
| frozen/expected.json = expected-v1.json | ad1b446268e8ada9c5cc9ca084827dad4dba1fafc374ee55925b56c9e5d0fc24 | older manifest, positive only [observed] |
| frozen/counter-fixtures-v1.py | 96e65034bcf2206c0e9c6335da264695f4741ed91e9a357c56484e6cd35e2849 | not the pinned harness (see §6) |

## 2. Case trace at candidate [inferred from source]

1. The base is the positive state. counter-fixtures.py:35-36 hard-resets to `fixture['base']` and cleans. :37 deep-copies the documents. :38 uses the default selection `inspect-signal-decoders`.
2. The only mutation is :93-94. It writes `{}` to `.ufo/waves/round-22/evidence/c1/new-control.json`. :100-102 stage it with the round-22 directory. The commit follows, and :104 sets `rev` = HEAD.
3. `measure()`: the legacy sha passes (count-c1.py:62-63), and so does the catalog check (:64-65). `rev:.ufo/waves/round-22/evidence/c1` differs from `BASELINE:…`, so :66-68 raise `ValueError('historical_evidence_changed')`.
4. `main()`: :167-168 catch it and produce `{"error": "historical_evidence_changed", "finding": "unevaluable"}` with code 2. :169 prints it.
5. Harness :111-112: observed `{exit 2, count None, finding 'unevaluable'}` equals expected, so the case passes.

The case is positive plus one file. Its only effect is the guard.

## 3. Findings

### F1 — medium — the payload cannot exercise the named fault (weak mutation)

- [observed] `{}` has no `ok` or `data`. The R22 binder returns 2 at `.ufo/waves/round-22/tools/count-c1.py:74`, so the file can never be a witness.
- [observed] Historical is measured at BASELINE (count-c1.py:81). New citations are restricted to `ROOTS[1]` (:97). The injected file is therefore visible only to the tree guard (:67).
- [inferred] Without :67-68 the case flips to exit 1, count 2 (positive base). So it does kill guard removal. It never tests whether a bindable round-22 envelope can raise the R23 count or put a T1 verb into the count without a round-23 witness. That is the fault the case name and the W1 critic describe.
- **Re-evaluation of W1 CriticSeparation.md F1 (lines 11-14, 18, 100):** the counterexample (bindable round-22 envelope cited by an S058 entry) is **closed at candidate** [inferred] by three separate mechanisms: :81 (BASELINE anchor), :97 (round-23-only citation), and :67-68 (tree guard). The W1 remedy (tuple-set compare, finding `historical_root_changed`) was not adopted. The candidate uses a full-tree compare with finding `unevaluable` and error `historical_evidence_changed`. The expectation matches the candidate, not the W1 wording. No case regression-tests the closed path.
- Recommendation: add a sibling case that injects a bindable copy of a fixture document, for a verb not otherwise historical, and cites it from an eligible S058 entry. Expected: exit 2.

### F2 — medium — the expectation cannot show which check fired (weak expectation)

- [observed] counter-fixtures.py:111-112 compare exit, count, and finding only. `error` (count-c1.py:168) is never compared. Six exit-2 cases share this triple (RunSelftest.md:66-70; Fixture06.md:48-50, peer reports).
- [observed] A refinement to the peer claim that a hardwired `sys.exit(2)` passes all six. A bare exit 2 with no JSON fails this case: `json.loads('')` raises, so `finding` is None, which is not 'unevaluable' (:108-110). The case passes any counter that prints `finding: unevaluable` with exit 2 from one of the five caught classes (count-c1.py:167).
- Recommendation: assert `error == 'historical_evidence_changed'`. This needs a re-freeze and a new pin, which were not done here.

### F3 — medium — guard-mutant blind spots (weak mutation)

Mutant results are [inferred from harness structure; not executed].

| Mutant | This case | Whole 21-case suite |
|---|---|---|
| M1 no tree guard (drop :67-68) | exit 1, count 2 → fails | killed |
| M2 guard compares `rev^` instead of BASELINE | pass | survives: every case is one commit on base (:35-36, :100-104), so parent = BASELINE |
| M3 guard reads the worktree, not `rev:` | pass | survives: every case commits before measuring |
| M4 name-list compare instead of tree compare | pass | survives: round-22 evidence changes are only add (:93-94) and unlink (:95-96), never in place |
| M5 additions-only guard | pass | killed only by inherited_lost (:95-96) |
| M6 deletions/modifications-only guard | exit 1 → fails | killed |
| M7 bound-tuple-only guard (W1 wording) | exit 1 → fails | killed |
| M8 exit 2 from a different cause | pass | survives (F2) |
| M9 historical measured at `rev` (:81) | pass (guard fires first) | survives; latent. The only bindable round-22 T1 envelope is identify-flutter-build (identify-godot.envelope.json has `ok:true`, same verb; inspect-dart-aot-saber.envelope.json has `ok:false`), so this is count-equivalent on this snapshot [observed envelope facts] |

Recommended additions, not applied. Each needs a new frozen manifest and pin:
- Two-commit chain: C1 injects, C2 is clean. Expect exit 2. Kills M2.
- Clean commit plus an uncommitted injection in the worktree. Expect exit 1, count 2. Kills M3.
- In-place content edit of identify-godot.envelope.json with names unchanged. Expect exit 2. Kills M4.
- Assert `error`. Kills M8.

### F4 — low — exit 2 is a policy choice that frozen text does not force

- [observed] claims.json:28 (candidate): "Historical R22 witnesses preserved; new evidence only under round-23/evidence/c1." count-c1.py:6: "never extended by new files under the old root."
- [inferred] Both sentences are satisfied by a non-fail-closed policy: ignore the injection and report exit 1, count 2. Fail-closed is well motivated, since the frozen read set was violated. The text still does not force it.
- [observed provenance] expected-v2.json, count-c1.py, and counter-fixtures.py were created in one commit (2b40aec, per `git show --stat`). `git log` shows no later change under frozen/ or tools/. W1 CriticSeparation.md:18 prescribes "historical_root_injection (expected exit 2)". The literal values do not depend on the DUT. The policy comes from the same design lineage, and git cannot show that the expectation predates that design. [unknown: authorship order inside 2b40aec]
- Recommendation: state fail-closed in count-c1.py's docstring or in the claims, so the expectation is traceable. Or relax the expectation to exit ∈ {1, 2} with count ≤ 2 and no extension.

## 4. Independent-template check [observed]

- counter-fixtures.py imports only stdlib modules (copy, json, os, pathlib, subprocess, sys, tempfile). The DUT runs as a subprocess with `-I -B` (:105-106). The file imports no count-c1, round-21, or round-22 decision code.
- Expected values are literal JSON (expected-v2.json:98-102) and hash-pinned (count-c1.py:25). The harness never writes expectations from DUT output.
- fixture.json documents are hand-authored synthetic templates (`control: "synthetic, never a producer observation"`). The injected `{}` is a literal.
- Verdict: template-independent. The policy coupling is F4.

## 5. Positive-preservation

- By construction, the only delta from `positive` is line :94.
- The guard does not fire on the real candidate [observed]: `rev-parse 2838351…:.ufo/waves/round-22/evidence/c1` equals `rev-parse aa1450b…:…` (b83fc459dca64a8356480b1ebc8309b4de65de71). `git diff --stat aa1450b 2838351 -- .ufo/waves/round-22/evidence/c1` is empty, with exit 0.
- Peer-observed positive: `1 | 2 | c1_incomplete` (RunSelftest.md:24).

## 6. Side notes for L1 (outside this case)

- [observed] frozen/counter-fixtures-v1.py lacks the branches for absolute_citation, meta_false, meta_array, sibling_refusal, historical_root_injection, inherited_lost, and catalog_changed. Those branches are at current tools-file lines 58-63, 71-72, and 93-102. This file is not the pinned harness. Run against expected-v2, those cases would fail, since no mutation yields exit 1. It is a stale file inside a "frozen" directory. I did not run it.
- [peer, not re-verified] RunSelftest F3: `command()` raises RuntimeError on a git failure, and count-c1.py:167 does not catch it, so a setup failure would escape uncaught. That should not affect this case, because it stages changes before committing.
- [observed] No ignore rule hides the injected path or the round-23 evidence. `.ufo/waves/round-23/.gitignore` contains `/runtime/` and `/worktrees/`. The root `.gitignore` contains `__pycache__/` and `*.pyc`.

## 7. Produced files and hashes

- `.ufo/waves/round-23/w2/Fixture19.md` (this report). Its own sha256 is reported in the final message, because a file cannot embed its own hash.

## 8. Installs

- None. The review was read-only. git 2.56.0 was pre-existing and used read-only.

## 9. Open risks and verification gaps

- Nothing was executed. All results are static traces; peer RunSelftest output is cited, not re-derived.
- count-c1.py (the DUT) is not pinned. The counted result ties to this commit only through this report (peer RunSelftest F2).
- The binder's acceptance of the round-23 synthetic envelope rests on the peer-observed positive, not on my re-derivation.
- M1, M2–M4, and M9 are source-level predictions, not executed.
