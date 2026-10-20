# RevBaseProducerRev — falsification of C1's R17-PRODUCER-REV baseline premise

Baseline under test: `9011581d84527ba34c675f9cf912e54d2e72d470` (= `refs/heads/main`).
Defect text: `corpus/lessons/round-17-verifier-spotcheck.md:139`.

**Verdict: OPEN at `9011581` — the defect is genuine and unclosed; it is not "already-closed".**
The routing text is nevertheless **mis-stated in two particulars** and **understates the scope** of
the missing evidence. The contract's closure check (`contract.md:36-37`) is **too weak**: it can be
turned green without naming the producer at all.

Labels: **OBS** = read directly from a command output pasted below. **INF** = reasoned from OBS.

---

## 1. Producer map derived from Git objects

OBS. Tool revisions are exactly the three commits touching
`.ufo/waves/round-17/tools/carrier-run.py` (command C2). The four shape bits below are pairwise
distinct across the three tool blobs, so each receipt is attributable to exactly one revision.

| pass | receipt window (UTC) | `runs/pro-aether/receipt.json` blob | `child_env_keys` / `mid_run_drift_steps` / `carrier.md5_pre` / `retained_logs[].binding.md5_ok` | only matching tool blob | tool commit |
|---|---|---|---|---|---|
| 1 | 13:47:05.97 → 14:00:05 (run-log) | `413d2b97…` at `da64646` and `95e34db` | F / F / F / F | `2711674` (`bc964acd…`) | 13:46:45Z |
| 2 | 14:27:41.94 → 14:40:02 (run-log) | `d552512e…` at `d0ab299`, `b31975d`, `9011581` | T / T / F / F | `95e34db` (`c536e3e4…`) | 14:27:35Z |
| (verification tool) | — no receipt carries its shape — | — | T / T / T / T | `d0ab299` (`f91bbc76…`) | 14:47:24Z |

- **OBS** `d0ab299` is the only revision of the tool containing any `md5` (C3); `md5_pre` is
  assigned at `d0ab299:.ufo/waves/round-17/tools/carrier-run.py:340-344`, `md5_ok` is seeded at
  `:132` and passed at `:148-152`, call site `:395-396`.
- **OBS** `95e34db`'s `bind_session` returns only `{logfile_ok, target_ok}`
  (`95e34db:…/carrier-run.py:130`); it assigns `child_env_keys` (`:311`) and
  `mid_run_drift_steps` (`:396`) and never computes an MD5.
- **OBS** `2711674`'s tool assigns neither `child_env_keys` nor `mid_run_drift_steps`; it only
  records `carrier.sha256_pre` (`2711674:…/carrier-run.py:302,351`).
- **INF** the producer is *not* self-declared: the receipt records `python: "3.14.8 …"` and
  `orig_argv: ["python3","-I","-B","tools/carrier-run.py",…]` with a **relative path and no
  digest** (C8). Attribution rests on two independent lines:
  1. key shape matches exactly one tool blob;
  2. commit-time bracketing — `95e34db` committed 14:27:35Z, **6 s before** the first second-pass
     step at 14:27:41.944Z; `d0ab299` committed 14:47:24Z, **7m22s after** the 14:40:02Z end.
- **OBS** the receipt blob is unchanged from `d0ab299` through `b31975d` to `9011581`
  (`d552512e…`, C6): S *committed* the second-pass receipts, it did not re-run them.
- **OBS** the lesson's window `14:27:41–14:40:02Z` matches `runs/run-log.txt` at `9011581`
  (`started 2026-10-20T11:27:41-03:00` … `end 2026-10-20T11:40:02-03:00`).

So the lesson's core facts are confirmed: pass 2 = `95e34db` tooling, and its receipts lack
`carrier.md5_pre` and the md5 binding field.

---

## 2. Is the remedy present at `9011581`? (OBS)

No. The remedy ("name the producing revision per pass wherever 'measured source revision' is
cited") is absent from every delivered attribution site:

- `SCORECARD.md:2352-2358` names one **"Measured source revision"** `d0ab299…` and one
  "verification evidence revision" `b31975d…`. `git show 9011581:SCORECARD.md | grep -c 95e34db`
  returns **0** (C9, exit 1).
- `LOG.md:2071` names `d0ab299…` as "Source revision". `LOG.md:2096-2101` states the second-pass
  window and then says "Replicate expectations were frozen at `95e34db` before it" — `95e34db` is
  attached to the **freeze of expectations**, not to the receipts' producer.
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1-2` names `da64646…` (first pass,
  as a lane commit) and `2711674…` (predictions frozen); it describes the second pass as
  "14:27–14:40 UTC with the hardened capture tool" with **no revision**.
- The map *is* already recorded in the routing documents
  (`corpus/lessons/round-17.md:122`, `corpus/lessons/round-17-verifier-spotcheck.md:73`), but those
  are the lesson files, not the delivered provenance claims the remedy targets. A lenient reviewer
  must not count them as closure; §5 explains why the contract's file set excludes them, and why a
  marker-only check cannot enforce that exclusion.

**Result: OPEN.** C1's baseline premise for this defect is not falsified.

---

## 3. Mis-statements inside the defect, and one scope understatement

**(a) "which were added before S" is false — they were added *in* S.** OBS: `md5` first appears in
`d0ab299`'s `carrier-run.py` (blob `f91bbc76…`) and in no earlier blob (C3). `d0ab299`'s commit
time is `2026-10-20 11:47:24 -0300` = **14:47:24Z**, exactly the S the lesson names. Correct
wording: "…which S's `carrier-run.py` adds, and which the second pass therefore predates."

**(b) `binding.md5_ok` is not a receipt-level path.** OBS: no receipt has a top-level `binding`
key. The value is `retained_logs[].binding.md5_ok`, and in pass-2 receipts that key is **absent**,
not null — `95e34db`'s `bind_session` does not create it (`95e34db:…/carrier-run.py:130`). A check
written against a top-level `binding` reports "absent" for every receipt in every revision and
proves nothing.

**(c) Scope understated.** OBS: 16/16 committed receipts (8 at `da64646`, 8 at `9011581`) lack
`carrier.md5_pre`, and none has a non-null md5 binding (C10). Pass 1 predates even the `md5_ok`
key. The correction must therefore not imply pass 2 is uniquely affected. It also means
`SCORECARD.md:2364`'s "all 16 receipts `receipt-validate.py` exit 0 (MD5-anchored binding)" can be
true only as a validator-time re-derivation from the on-disk carrier
(`d0ab299:…/receipt-validate.py:143-150`), because the validator accepts a missing field
(`md5_ok is not False`, `:177`). The **count** half of that sentence belongs to R17-VALIDATE16;
keep the two corrections separate so the same evidence is not counted twice.

**(d) Cause (INF).** `d0ab299`'s subject is "… second carrier pass … (source revision)". The lane's
"source revision" denotes the commit that *carries* the measurements; that diverges from the
revision that *produced* them whenever a tool is fixed after the run and the run is not repeated.
The correction should say this, otherwise the per-pass producer line looks like bookkeeping rather
than the fix for a misattribution.

---

## 4. Minimal objective test that distinguishes open from closed

A receipt-based test is the **wrong instrument**: `claims.json` non-goals forbid editing round-17
retained receipts/logs, so "does pass-2 `receipt.json` contain `carrier.md5_pre`?" is invariant at
every revision and can never turn green without violating the non-goal. The distinguishing
predicate must be textual, but evidence-linked:

Closed at REV ⟺ both:

1. **Oracle guard (invariant).** `runs/pro-aether/receipt.json` at REV still has the `95e34db`
   shape — `child_env_keys` ∧ `mid_run_drift_steps` present, `carrier.md5_pre` absent, no `md5_ok`
   key in `retained_logs[0].binding` — and that shape matches exactly one of the three
   `carrier-run.py` blobs. If this changes, the receipts were rewritten and the correction is void
   (exit 2, not "closed").
2. **Attribution.** In each document that states the round's measurement provenance, one sentence
   names the pass and its fingerprint-derived producer in the *producing* role. For pass 2:
   `(second pass|pass 2|14:27)[^.]{0,300}95e34db62f2693c455d7ee4dfef24b8f3ebc007d` whose match is
   **not** a `frozen|expectations` clause; for pass 1, the same relation with
   `271167473d87ef710f07ecdd98caf0ce12091686`.

Clause 1 is the oracle for *which* hash is correct; clause 2 is the only thing a text-only fix can
change. Baseline fails clause 2 at every delivery site (§2); a correct fix passes; a marker-stuffed
tree fails clause 2 while passing a shape-only check (§5).

---

## 5. Evaluation of the contract definition

`contract.md:36-37`:
> **R17-PRODUCER-REV**: `SCORECARD.md` and the r17 knowledge entry each have a line containing
> `R17-PRODUCER-REV` and at least two distinct 40-hex hashes.

**Primary verdict: too weak — it admits a concrete false close.** OBS: the knowledge entry's
**line 1 already contains exactly two distinct 40-hex hashes** (`da64646…`, `2711674…`, C11), and
`SCORECARD.md:2353-2356` already contains `2711674…`, `d0ab299…`, `b31975d…`. Appending
`R17-PRODUCER-REV` to knowledge line 1 and reflowing one SCORECARD line turns the check green while
attributing pass 2 to nothing — in fact while displaying the *other* two revisions. The check tests
marker presence and hash density, not the pass→revision relation; it passes just as readily on the
"first pass / predictions frozen" pair (`da64646`, `2711674`) as on `95e34db`+`d0ab299`.

**Secondary: mis-scoped, and too strong in format.**
- The remedy says "wherever 'measured source revision' is cited". At `9011581` the round-17 site
  set is `SCORECARD.md:2352-2358` and `LOG.md:2071` (`corpus/lessons/round-17.md:145` is a lesson;
  `SCORECARD.md:2297` is the *round-16* section). **LOG.md is not in the check's file set**, and
  the knowledge entry never uses the phrase. A fix that satisfies the remedy at every real citation
  site is judged open (false-open), while the marker trick is judged closed (false-close).
- Requiring two 40-hex hashes on *one* line is stricter than the lane's own prose: SCORECARD
  already splits baseline/freeze/measured/verification one per line (`2352-2356`). A correct
  two-line correction fails on formatting, not calibration.
- The defect text abbreviates the producer as `95e34db`; the check requires 40-hex. Copying the
  defect text verbatim into the correction fails. Minor, but state the full hash in both.

**Recommended replacement** (for `contract.md:36-37` and `routed-defects.py`):
- (a) guard: pass-2 receipt shape == `95e34db` shape and ≠ `d0ab299` shape at REV (red ⇒ exit 2).
- (b) attribution: `SCORECARD.md` **and** `LOG.md` each contain, within one sentence adjacent to a
  "second pass"/"pass 2" token, the full `95e34db62f2693c455d7ee4dfef24b8f3ebc007d`, and the
  sentence does not place that hash in a `frozen`/`expectations` clause. Require the knowledge
  entry to carry the marker plus the same mapping (its line 1 is the pass-location claim), or drop
  it from the mandatory set and add `LOG.md`.
- (c) required selftests: baseline → 1; marker appended to knowledge line 1 → **still 1**
  (anti-false-close); `95e34db` present only as "frozen at" → **still 1**; correct two-line
  correction → 0; receipts rewritten to the `d0ab299` shape → 2.

Cheapest repair if the minimal form is kept: require one of the two hashes to be exactly
`95e34db62f2693c455d7ee4dfef24b8f3ebc007d`. That closes the demonstrated false-close at near-zero
cost, but still accepts a reversed role assignment — a floor, not the correct check.

---

## 6. Residual risk and verification gaps

- `W18/tools/routed-defects.py` does not exist in the working tree (`ls .ufo/waves/round-18/tools/`
  → `revpin.py` only, C12), so this review tests the contract text only. The implementation must be
  checked against §5 when written; no finding is made against a tool that does not exist.
- Read-only mandate honoured: no `routed-defects.py` execution, no REA, no Ghidra, no carrier
  execution, no `jj`, no git write. Report is the only file written.
- The pass-1 producer `2711674` is **INF** from key shape plus timing, not from a self-declared
  field. If the L1 asserts it, phrase it as "produced by the `2711674` tool, inferred from the
  receipt key set".
- Out of scope: whether pass-2 receipt *content* is otherwise sound (R17-VALIDATE16 / C2). §3(c)
  flags only the shared evidence so it is not double-counted.

---

## 7. Command log (each command with its exit code)

| # | command (abridged) | exit | what it showed |
|---|---|---|---|
| C1 | `git log -1 --format='%H %ci %s' 9011581 da64646 95e34db d0ab299 b31975d 8e7642c` | 0 | commit identities/times; S = `d0ab299` at 14:47:24Z |
| C2 | `git log --format='%h %ci %s' -- .ufo/waves/round-17/tools/carrier-run.py` | 0 | exactly three tool revisions: `2711674`, `95e34db`, `d0ab299` |
| C3 | `for r in <above>; do git show $r:…/carrier-run.py \| grep -nE 'md5\|child_env_keys\|mid_run_drift'; done` | 0 | `md5` only at `d0ab299`; `child_env_keys`/`mid_run_drift_steps` first at `95e34db` |
| C4 | `git show <rev>:…/runs/pro-aether/receipt.json \| python3 -c '<key dump>'` for `9011581`,`da64646`,`95e34db` | 0 | pass-2 keys include `child_env_keys`,`mid_run_drift_steps`; `carrier` = path/sha256_pre/sha256_post only; `binding` = logfile_ok/target_ok only |
| C5 | same for **all 8** receipts at both revs (`git ls-tree … \| grep receipt.json`) | 0 | 8 receipts per rev; pass-1 lacks the two keys, pass-2 has them |
| C6 | `git rev-parse <rev>:…/runs/pro-aether/receipt.json` for `da64646`,`95e34db`,`d0ab299`,`b31975d`,`9011581` | 0 | `413d2b97…` then `d552512e…` ×3 → receipts unchanged from S to baseline |
| C7 | `git rev-parse <rev>:…/tools/carrier-run.py` for `2711674`,`95e34db`,`d0ab299` | 0 | `bc964acd…`, `c536e3e4…`, `f91bbc76…` |
| C8 | `git show 9011581:…/runs/pro-aether/receipt.json \| python3 -c '<python/orig_argv dump>'` | 0 | no tool digest; `orig_argv` names relative `tools/carrier-run.py` |
| C9 | `git show 9011581:SCORECARD.md \| grep -c 95e34db` | **1** | count 0 — SCORECARD never names the pass-2 producer |
| C10 | md5 audit over all 16 receipts (python one-liner per label) | 0 | `md5_pre` absent and `md5_ok` key absent for 16/16 (both revs) |
| C11 | `git show 9011581:…r17-go-carrier-diagnostics.md \| python3 -c '<40-hex per line>'` | 0 | only line 1 has ≥2 distinct 40-hex: `da64646…`, `2711674…` |
| C12 | `ls .ufo/waves/round-18/tools/` | 0 | `revpin.py` only; `routed-defects.py` absent |
| C13 | `git grep -n 95e34db 9011581 -- …` | 0 | only `LOG.md:2097` ("frozen at") plus lesson files |
| C14 | `git show 9011581:…/runs/run-log.txt` (both revs) | 0 | pass 2 = `11:27:41-03:00`→`11:40:02-03:00` = 14:27:41→14:40:02Z |
| C15 | python pass-window over all receipts (both revs) | 0 | pass 1 starts 13:47:05.97Z; pass 2 starts 14:27:41.94Z |
| C16 | `git show d0ab299:…/receipt-validate.py \| grep -nE 'md5\|binding'` | 0 | md5 re-derived from disk (`143-150`); `md5_ok is not False` (`177`) accepts a missing field |
| C17 | `git merge-base --is-ancestor <r> 9011581` for six revs | 0 | all ancestors of the baseline |
| C18 | `git show 95e34db:…/carrier-run.py \| sed -n '118,160p'` | 0 | `bind_session` without md5; `{logfile_ok, target_ok}` only |
| C19 | `grep -n -A3 R17-PRODUCER-REV .ufo/waves/round-18/contract.md` | 0 | the check text quoted in §5 (lines 36-37) |

No installs or upgrades were made (host pacman paused; nothing was needed).
