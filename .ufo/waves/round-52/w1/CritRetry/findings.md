# CritRetry — round 52, wave 1: attack on the projection retry policy (R52-C1)

Seat: `CritRetry` (critic). Scope: the retry policy the round-52 claims admit
(`plans/round-52-claims.md:105-114`), read against the round-50 before-state receipt
(`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`) and the v1 counter's projection
rerun code (`tools/round-50/c1-counter.py`) plus its closest successor
(`.ufo/waves/round-51/l1/drafts/c1-counter.py`).

**Verdict: the retry policy as written in the round-52 claims is NOT admissible.**
Four independent defects, any one of which is enough to reject it. The decisive one
(F1) is that the mechanism the policy is built on is misidentified: the failure the policy
retries is **not** the round-50 `provider_timeout` flake class, and it is **not** proven
transient; it is a **Node-side (REA) `readlink` on a symlink that unblob is concurrently
unlinking and recreating**, i.e. a real TOCTOU inside the extraction, whose occurrence
probability is a function of how many absolute-target symlinks the carrier has. That
changes what the honest control must be.

No REA run was performed. All probes used a local 3-line stub `.mjs` package; the real
`rea-agents` package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` was
read but never executed. Receipts: `receipts.json` (4 probes, exact command, exit code,
stdout sha256, UTC time). No tool was installed. Scratch removed after copying.

---

## F1 — CRITICAL. The retried failure is misidentified; the policy is admitted on a mechanism that the evidence contradicts.

**Counterexample.** The claims' retry bullet rests on two sentences:

> "allows up to 3 attempts on REA's own `provider_timeout` (**the proven flake class**) and
> up to 2 attempts on an `execution_failure` whose failing diagnostic is an ENOENT naming a
> path inside the extraction tree"

and, in the r51 disposition it cites as authority:

> "r51 disposition: no retry policy is admitted **without proof able to fail**"

Both framings are wrong about the evidence in the lane.

**(a) The ENOENT is not in the "proven flake class", and the two classes are not the same
kind of event.** `provider_timeout` is a *host-load* timeout: REA's own 120 s
`FIRMWARE_LIMITS.timeoutMs` deadline firing on a loaded host (`tools/round-50/c1-counter.py:2068-2071`).
The ENOENT is a **TOCTOU inside the extraction**. The committed reason is:

```
ENOENT: no such file or directory, readlink '/fast/scratch/hyaku/kaidoku-r50/c1-after-work2/
c1-counter.rcz52k9z/rerun-g7581/rea-firmware-Ft6F7W/extracted/firmware.bin_extract/
usr/www.myfritz/avme/cgi-bin/luacgi'
```

That text is the **Node/JS** error form, not Python's. Measured (`probe4`): Node's
`readlink` rejection is `ENOENT: no such file or directory, readlink '<path>'`; Python's
`os.readlink` is `[Errno 2] No such file or directory: '<path>'`. unblob 26.6.4 is Python
(`.../site-packages/unblob/extractor.py`), so **unblob did not raise this** — REA's own
JavaScript did. The relevant REA site is `dist/firmware/FirmwareFiles.js:184`:

```js
linkTarget: stat.isSymbolicLink() ? await readlink(path) : null,
```

Note the asymmetry: the `lstat` at the same site (`:158`) **is** ENOENT-guarded
(`return undefined` → `continue`), but the `readlink` at `:184` is **not**. So the
inventory can `lstat` a symlink successfully and then `readlink` it after it has vanished.

And it vanishes because **unblob deletes and recreates it**. `unblob/extractor.py:89-91`:

```python
relative_target = os.path.relpath(outdir.joinpath(target), start=path.parent)
path.unlink()
path.symlink_to(relative_target)
```

`unlink()` then `symlink_to()` — a window in which the path does not exist. And REA runs
that inventory **concurrently with the still-running unblob process**: `cli.js:14481` polls
`inventoryFirmwareOutput(context.outputBudget.root, ...)` inside the
`while (!await supervisor.waitForOutputClose(100))` loop, and `outputBudget.root` is
unblob's own `--extract-dir` (`cli.js:15124-15130`).

**The window is opened exactly by the absolute-target symlinks.** unblob only rewrites a
symlink when its target is absolute (`extractor.py:78-81`). Measured per carrier from the
frozen oracle tables:

| carrier | class | total symlinks | **absolute-target** symlinks | round-50 rerun |
|---|---|---|---|---|
| c6430 | Cable | 568 | 58 | `projection_ok: true` |
| c6490 | Cable | 613 | 54 | `projection_ok: true` |
| g7581 | FRITZ!Box | 639 | **120** | `projection_ok: false` (ENOENT) |
| g7582 | FRITZ!Box | 639 | **120** | `projection_ok: true` |

The failing path `usr/www.myfritz/avme/cgi-bin/luacgi` is in the oracle with the
**absolute** target `/usr/www/cgi-bin/luacgi` (`tools/round-50/oracle/g7581.nonregular.tsv:774`)
— it is one of g7581's 120. g7582 has the identical set of 120 and did **not** fail in the
same run. So the failure probability scales with the absolute-symlink count and is
**stochastic, per-attempt** — it is a race, and the round-50 observation is n=1.

**(b) The r51 disposition is quoted backwards.** The claims cite the r51 disposition as
*"no retry policy is admitted without proof able to fail"* and treat the deterministic-ENOENT
fixture as discharging that condition. The actual r51 text (`plans/round-51-claims.md:351-352`)
is:

> "The ENOENT diagnostic alone does not prove a retry-safe environmental race;
> **no new retry policy is admitted.**"

That is unconditional. The qualifier *"without proof able to fail"* appears **nowhere** in
`plans/round-51-claims.md` or in the round-51 wave (`grep -rn "without proof able to fail" plans/
.ufo/waves/round-51/` → the only hit is `plans/round-52-claims.md:107` itself). The
round-52 claims manufacture the permission they then exercise. Round 51's actual position
was: *the diagnostic alone does not prove a retry-safe race* — and the claims do not
address that at all; they substitute a weaker, invented condition and satisfy it.

**Impacted axes.** Coverage (the claim misses or over-claims), calibration (a n=1 race is
promoted to a retry budget), false provenance (a disposition is quoted with a condition it
does not contain, and the L1 would be asked to carry a policy round 51 refused).

**Smallest safe correction.** Do **not** admit an ENOENT retry in R52-C1 at all. Round 51's
unconditional refusal stands and is not discharged by a fixture that shows the policy can
fail — that fixture proves the policy is *not* a no-op, which is a different (and much
weaker) property than "the failure is retry-safe". Instead: (i) state in the claims that
the round-50 g7581 miss has **two** causes and that the second is **not repaired** this
round; (ii) if the L1 still wants the retry, ground it in the *measured* mechanism — the
REA-side unguarded `readlink` at `FirmwareFiles.js:184` racing unblob's `unlink`/`symlink_to`
at `extractor.py:89-91` — and cite it as a SOURCES row, because that is the only thing
that makes a retry *principled* (the race is in the frozen toolchain, so a rerun on a fresh
extraction root genuinely can win) rather than hopeful; (iii) amend the claims text to
quote the r51 disposition **verbatim**, not with an invented qualifier; and (iv) state the
honest stop explicitly: if g7581's rerun hits the ENOENT again, **the claim misses as
frozen** — which the claims already say, and which F5 shows the port as written would not
honour.

---

## F2 — CRITICAL. The control the claims specify cannot demonstrate what they say it demonstrates, and the predicate it exercises is far broader than the one the claims state.

**Counterexample.** The claims demand:

> "a frozen control (**deterministic-ENOENT fixture tree**) demonstrates the same failure
> surviving all attempts still scores **red**, so the policy is shown able to fail"

Two problems.

**(a) "deterministic" is the opposite of the real failure, and the distinction the
assignment asks for is not stated.** The real g7581 failure is a **race** — g7582 has the
identical 120 absolute-target symlinks and passed in the same run. A deterministic-ENOENT
fixture therefore proves only that *the policy is not a no-op* (it can exhaust and go
red). It proves **nothing** about whether the real failure is transient. The claims never
distinguish these two properties, so the reader is invited to read "the policy is shown able
to fail" as "the policy is shown to be the right fix". The honest statement is the
opposite-shaped one: *the fixture shows the policy cannot silently turn a persistent
failure into a green; it cannot show that a transient failure is recovered.*

**(b) The exhausted-ENOENT path in the closest ancestor of the v2 counter does not score
red — it scores exit 2 (could-not-evaluate).** Measured (`probe2`, against
`.ufo/waves/round-51/l1/drafts/c1-counter.py`, sha256 `1787291d…`): with the stub package
raising the exact ENOENT every time, the runner performed **3** invocations and the measure
stage took the branch at draft `:2555-2571`:

```
measure_stage_branch: "RerunEnvError -> exit 2 (could-not-evaluate, NOT red)"
```

That branch raises `RerunEnvError` for `provider_timeout` **and** for the ENOENT
`execution_failure`, so an exhausted ENOENT is *unevaluable*, never a verdict. The claims
say the same failure "still scores **red**". So either the v2 counter must **split** the
inherited branch — treating exhausted-ENOENT as red (exit 1) while exhausted-timeout stays
exit 2 — or the control as written **fails**, and the L1 inherits a policy whose own
required control is red-on-arrival. This is not a nit: exit 1 vs exit 2 is the difference
between "the claim misses" and "we could not evaluate", and the claims' honest-stop
sentence depends on which.

**(c) The predicate the claims state is much narrower than the one the ancestor
implements, and the narrow one is the one that matters.** The claims require "an
`execution_failure` whose failing diagnostic is an ENOENT **naming a path inside the
extraction tree**". The ancestor's predicate (draft `:2135-2137`) is a substring test over
the *whole serialized error object*:

```python
enoent_flake = (err_obj.get('code') == 'execution_failure'
                and 'ENOENT' in err_text and 'readlink' in err_text)
```

Measured (`probe2`, `predicate_breadth`): this predicate returns **True** for
(i) an ENOENT naming a path **outside** the extraction tree (`/etc/ld.so.preload`) and
(ii) an ENOENT that appears only in the boilerplate `message` with an unrelated
`details.diagnostics.reason`. Both are supposed to be **False** under the claims' wording.
A substring test cannot tell "the extraction tree" from "anywhere"; the v2 predicate must
parse the path out of `details.diagnostics.reason` and check containment in the attempt's
extraction root. That is a *new* predicate, not a port — and the claims describe it as if
it were a port of an existing one.

**Impacted axes.** Calibration (a control that cannot fail the claim it certifies),
coverage (a predicate that retries unrelated failures), false provenance.

**Smallest safe correction.** Specify the control exactly, in the claims, as three
*separate* frozen cases with named expected verdicts, and state the exit-code semantics
explicitly:

| case | construction | expected |
|---|---|---|
| ENOENT-EXHAUST | stub raises the recorded ENOENT every attempt | **exit 1, red** — and the claims must say so, because the ancestor's branch gives exit 2 |
| ENOENT-RECOVER | stub raises the recorded ENOENT once, then succeeds | the run is green **and** the receipt names `attempts: 2` |
| ENOENT-OUTSIDE | stub raises an ENOENT naming a path outside the extraction tree | **no retry** — one attempt, then red |

And the predicate must be stated as *parse the path from `details.diagnostics.reason`;
retry iff it is under the attempt's extraction root* — not as a substring test. If the L1
prefers the substring test, then the claims must say "an ENOENT anywhere", which is a
weaker and less honest policy, and the honest-stop must widen accordingly.

---

## F3 — HIGH. The retry can mask a real defect: the frozen projection is blind to `link_target`, so a green-after-retry can be green over a different tree.

**Counterexample.** The assignment asks whether a retry can mask a real defect — an
extractor that fails path X on runs 1 and 2 but passes run 3 by scheduling luck. Here the
masking is not merely possible, it is **structurally unguarded**: the frozen projection
cannot see the field that the race perturbs.

Measured (`probe3`, against `tools/round-50/c1-counter.py`): the projection's
`unpublished_entries` rows are built as `[kind, relative_path]` **only** — `link_target` is
dropped (`c1-counter.py:1841-1843`). Two envelopes that differ **solely** in
`unpublished_entries[0].link_target` project **EQUAL**:

```
link_target_changed_absolute_vs_rewritten: {"projection_equal": true, "differing_keys": []}
```

For contrast, dropping the entry entirely *is* caught (`differing_keys:
["unpublished_entries"]`).

Now combine with F1's mechanism. The race is: unblob `unlink()`s the absolute-target
symlink and recreates it with a **relative** target. The committed g7581 receipt records
exactly that rewritten value:

```
"firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi"  kind=symlink
link_target = "../../../www/cgi-bin/luacgi"      <- REWRITTEN (relative)
```

while the frozen oracle records the **absolute** original `/usr/www/cgi-bin/luacgi`
(`tools/round-50/oracle/g7581.nonregular.tsv:774`). So a rerun that observes the symlink
**before** unblob's rewrite (absolute target) versus **after** (relative target) produces
envelopes the projection declares **equal**. `gaps_ok`/`nonregular_unpublished_ok` compare
against the oracle's *detail* column, but `link_target` is not compared to it anywhere in
the counter — `grep -n "link_target" c1-counter.py` returns only the two places that
**write** it (`:2699`, `:3671`), never a comparison.

**The retry therefore widens a masking surface.** Before the retry, an ENOENT made the
carrier red — the failure was visible. After the retry, the same carrier can go green with
a *different* symlink target, and the frozen comparator cannot tell. The claims' control
set contains **no arm** for this: CTL-OLD/CTL-NEW are rule-scoped disposition controls,
CTL-DN/CTL-JUNK are rule mutants, M1–M4 are gap-rule mutants — none exercises a
*projection-level* difference between an absolute and a rewritten link target. A retry
policy that changes the number of runs is exactly the policy that needs a
*content-equivalence* control on the thing it makes reachable.

**Impacted axes.** Coverage (a green that does not mean the tree is the same), calibration.

**Smallest safe correction.** Either (a) add `link_target` to the frozen projection's
`unpublished_entries` row (a one-line change to the projection builder, but it changes the
frozen comparator and must be stated in the claims and applied to **both** sides), or
(b) add a frozen control that runs the **same carrier bytes** through two independent
extractions and requires the projections to agree *including* link targets, and record
that the counter currently cannot check this. If (b) alone is chosen, the claims must
state the limitation in the same sentence as the retry policy, because the retry is what
makes it reachable. Do **not** leave this implicit: a retry policy whose own comparator
cannot see the difference between the two states of the raced file is a policy that
converts a visible red into an invisible green.

---

## F4 — HIGH. On the success path the attempt count and the failing diagnostic are dropped: the receipt cannot show that a retry happened, let alone why.

**Counterexample.** The claims require "each rerun on a fresh extraction root **with
attempt count and failing diagnostic recorded**". The ancestor does not do this on the
success path, and the v1 code does not do it at all.

Measured (`probe2`, r51 draft): stub raises the recorded ENOENT on attempt 1 and succeeds
on attempt 2. The stub was invoked **2** times — the retry happened. The payload the
runner returned on success:

```
runner_status: "ok"
payload_keys: ["normalized_result", "stub_success", "subject"]
attempts_in_payload: null
enoent_readlink_retry_recorded: false
```

The reason is structural: `replayed` (which holds `attempts` and `enoent_readlink_retry`)
is attached **only** to the `no_data` failure return (`draft:2146-2154`; v1
`c1-counter.py:2083-2087`). The success return is `return 'ok', data` (`draft:2155`;
v1 `:2088`) — a bare envelope, no replay record. The v1 counter is worse: it never had an
ENOENT branch at all, so its `attempts` is `1` in the committed receipt
(`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`, `carriers.g7581.projection_error.replayed.attempts = 1`),
which is exactly what `RevProvReadme.md:22` recorded.

Even on the **failure** path the diagnostic is lossy: the ancestor captures
`err_text[:300]` (`draft:2141`). Measured (`probe`, probe_C): the recorded error object
serialises to **717** characters; the 300-char cut truncates the failing **path** mid-name
(`.../usr/www.myfritz/avme/cg`) and **drops `"retryable": false` entirely**
(`drops_retryable_false: true`) — the very field that says the producer judged it
non-retryable. The captured text ends mid-path, so a reader cannot even identify which
path failed.

**Impacted axes.** Calibration and auditability — the receipt is the only artifact the
score stands on, and it cannot distinguish "succeeded first try" from "succeeded on the
third try after two ENOENTs". For a claim whose stated risk is *"the retry masks a real
defect"*, the receipt that would evidence the masking is the one thing the retry discards.

**Smallest safe correction.** The replay record must survive the success path. Concretely:
return `('ok', data, replay)` (or attach `replayed` to the success envelope) so the
receipt carries `attempts` and the failing diagnostic on **every** carrier, including
successes. And capture the **full** `details.diagnostics.reason` (plus the parsed path and
the `retryable` flag), not a 300-char prefix — the truncation must not be able to hide
which path failed or that the producer said `retryable: false`. The claims' phrase "with
attempt count and failing diagnostic recorded" must be made checkable: name the receipt
fields (`attempts`, `enoent_retry_path`, `enoent_retry_reason`) so the score can assert
their presence.

---

## F5 — HIGH. The budget ("up to 2 attempts") is arbitrary, contradicts the inherited constant, and the claims' own numbers do not match the code they port.

**Counterexample.** The claims specify "up to 3 attempts on REA's own `provider_timeout`
... and up to 2 attempts on an `execution_failure` whose failing diagnostic is an ENOENT".

The ancestor has **one** constant, `MAX_REA_ATTEMPTS = 3` (`draft:1979`; v1 `:1923`), and
**one** shared counter `attempts` used by both branches. Measured (`probe2`): with the stub
raising the ENOENT every time, the runner performed **3** invocations — the ENOENT branch
gets 3, not 2, unless the v2 counter introduces a **second** constant and a **second**
counter. That is a design change, not a port, and the claims do not say so.

Meanwhile the *justification* for the numbers is absent:
- The claims call `provider_timeout` "**the proven flake class**". Measured: there is **no**
  committed carrier receipt containing `provider_timeout` — `grep -l provider_timeout
  corpus/evidence/round-50/c1/*/*.json` → empty; all four carriers' `run.json` record
  `rea_attempts: 1`. The only `provider_timeout` receipts in the lane are two **dev-arm
  probes on different carriers** (`a7530`, `a7590` — `a7530`/`a7590` are **not** among the
  four; `grep -c "a7530\|a7590" tools/round-50/carriers.json` → 0), and both **exited 1
  after 3 attempts** — i.e. the probe exhausted the budget and still failed. So the flake
  class is attested by **two failures on non-carrier probes**, not by a successful recovery.
- Why 2 for the ENOENT and not 3? No argument is given, and **n=1** (one observed ENOENT,
  one non-occurrence on g7582) cannot justify any specific budget.
- The claims do not say whether the two budgets are **shared** (as in the ancestor: one
  counter, both branches) or **separate** (3 for timeout, 2 for ENOENT, independently). The
  wording "allows up to 3 attempts on X and up to 2 attempts on Y" reads as separate
  budgets; the ancestor's code has one shared counter. Two readings, different behaviour,
  and the freeze must pick one.

**Impacted axes.** Calibration (an unjustified budget), coverage (the honest-stop fires on
an arbitrary threshold).

**Smallest safe correction.** Either justify the numbers or admit they are arbitrary and
say so: *"the attempt budget is a round-52 choice, not a measured quantity; the corpus
contains one observed ENOENT (g7581) and one non-occurrence (g7582), which bounds nothing."*
State explicitly whether the two budgets are shared or separate, and name the constants in
the claims so the frozen code can be checked against them. Do not call `provider_timeout`
"the proven flake class" when the lane's own evidence for it is two exhausted probes on
carriers outside the measured set.

---

## F6 — MEDIUM. The honest-stop sentence exists but the port as written would not honour it, and the counter's own exit-code semantics make "red" ambiguous.

**Counterexample.** The claims say (`:113-114`):

> "If `g7581`'s projection still fails after the policy exhausts, the claim is missed as
> frozen — honest stop, no narrowing, no amendment."

This is the right sentence and it is present. But two mechanical gaps stand between it and
the receipt:

1. **Exhausted-ENOENT is exit 2 in the ancestor, not red** (F2b). Under exit 2 the
   counter reports "could-not-evaluate", and the L1's scoring must not read that as a
   pass. The claims should say which exit the exhausted case produces and require the
   score to treat it as **not met**.
2. **The harness has its own, different retry policy.** `tools/round-50/c1-run.sh:733-735`
   retries **only** on `provider_timeout` (`C1_REA_ATTEMPTS:-3`) and exits **3** on a failed
   receipt (`:854-856`). The round-52 claims promise a `tools/round-52/c1-run.sh` (`:93`)
   but say nothing about its retry policy, while the counter-side policy is specified in
   detail. If the data-run harness and the score-time counter disagree about what is
   retryable, the receipt the counter scores may not exist. This is exactly the "second
   convention" defect the round-51 audit already recorded for the controls' divergent
   `REA_ATTEMPTS = 5` + `time.sleep(15)` policy (`.ufo/waves/round-51/w1/SimpV1Audit/audit.md:29`,
   finding A6) — and it would be reproduced.

Also worth stating in the claims: nothing in the retry policy can be exercised pre-freeze
(the pre-freeze controls are explicitly "rule-scoped, over committed bytes, **no live
rerun** — F2", `:115-116`), so the retry's own behaviour is **first observed during the
data run** — i.e. the first time the policy can fail is the first time the claim is at
stake. The claims should say that the retry policy is therefore **unverified** at the
freeze, and that its only pre-freeze evidence is a fixture whose semantics the freeze
itself must pin (F2).

**Impacted axes.** Coverage and honesty of the verdict; duplicate authorities.

**Smallest safe correction.** Name the exit code for each exhaustion case; require
`tools/round-52/c1-run.sh` to carry the **same** retry predicate and budgets as
`tools/round-52/c1-counter.py` (one convention, or an explicit statement of which arm
governs and why); and add one line to the claims acknowledging that the retry policy is
unverified at the freeze and first exercised during the data run.

---

## Summary of demanded controls (the exact design I would require)

The round-52 claims need a **retry-policy control set** that is separate from the
rule-scoped controls, because the retry policy is exercised by the *runner*, not by the
rule. Frozen, named, and each with an expected exit code:

| id | construction (offline, stub REA package) | expected |
|---|---|---|
| **CTL-RP-EXHAUST** | stub raises the recorded g7581 ENOENT on every attempt | **exit 1**, `attempts == budget`, receipt names the failing path and `retryable:false`; **not** exit 2 |
| **CTL-RP-RECOVER** | stub raises the recorded ENOENT once, then returns a good envelope | **exit 0**, and the receipt carries `attempts == 2` **and** the failing diagnostic — this is the arm the ancestor's success path cannot satisfy (F4) |
| **CTL-RP-OUTSIDE** | stub raises an ENOENT naming a path **outside** the extraction tree | **no retry** (one attempt), red |
| **CTL-RP-PATH** | stub raises an ENOENT naming a path inside the extraction tree but **not** the recorded one | retried (the policy is about the *class*, not the single path) — pins the predicate's scope |
| **CTL-RP-LINKTARGET** | two extractions of the same bytes, one observing the absolute target and one the rewritten relative target | projections must agree **including link_target**; today they agree while differing, so this arm is RED as written and the counter must be changed or the limitation stated (F3) |
| **CTL-RP-NOOP** | stub always succeeds | **attempts == 1**, no retry — proves the policy is not a no-op that silently retries everything |

Each arm must record: the exact stub argv, the invocation count, the exit code, the
per-attempt diagnostic, and the receipt fields asserted. The claims must then state, in
one place, the **predicate** (parse the path from `details.diagnostics.reason`; retry iff
it is under the attempt's extraction root), the **budgets** (and whether shared), the
**exit code per exhaustion case**, and the **receipt fields** that carry the evidence
(`attempts`, the failing path, the failing reason, the `retryable` flag).

---

## Falsified assumptions I checked and did **not** report as findings

- **`provider_timeout` really is a host-load flake and the 3-attempt policy is justified
  for it** — the *policy* is inherited and its history is documented
  (`c1-counter.py:2068-2071`), but the lane's committed evidence for it is thin (F5). Not
  a finding against the timeout branch itself.
- **A retry on a fresh extraction root genuinely can win the race** — yes: the race is
  between REA's inventory and unblob's `unlink`/`symlink_to` inside one run; a fresh
  extraction root re-rolls it. So a retry is *not* futile in principle. My objection is to
  the claims' **justification** (misidentified class, invented disposition permission,
  unjustified budget), not to the idea.
- **The g7581 ENOENT was caused by unblob** — **falsified**: the message is Node's, and
  unblob is Python. The round-50 wave-4 note records it as "unblob ENOENT on `readlink`"
  (`.ufo/waves/round-50/w4/RevC1MissReceipt.md:62`) — that attribution is wrong and is
  worth correcting wherever it is inherited.
- **The retry could turn a red into a pass without the comparator noticing** — **true**
  (F3), via `link_target` blindness, not via attempt-count loss (which is a receipt
  defect, F4, not a verdict defect).

## Scope limits of this review

- No REA run; the mechanism in F1 is derived from the frozen tool sources and from the
  committed receipt, not from a reproduction. The claim "the race is stochastic" rests on
  g7581 failing and g7582 (identical 120 absolute symlinks) passing **in the same run** —
  strong, but a single observation pair.
- The lane's committed corpus contains exactly **one** ENOENT occurrence. Every
  probability statement here is therefore an inference from mechanism plus one
  observation, and is labelled as such.
- I did not evaluate the round-52 C2 (triage v6) material, the gap-rule law, the census,
  or the fetch/provenance chain — out of scope for this seat.
- The v2 counter does not exist yet (`tools/round-52/` is absent), so F2/F4/F5 are
  attacks on the *specification* the L1 would implement, not on landed code.
