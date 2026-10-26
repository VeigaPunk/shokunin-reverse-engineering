# R38W2CritGateBypass — QUALITY 79/80 as the fix for M38-1/M38-2

**Verdict: DEFECTS FOUND.** QUALITY 79 as specified does not close the class M38-1 names, and the
landing it is supposed to police *ships* the amendment: the documented counting command at the tip
prints `carriers_matched 4`, the verdict of record is `3`, and the counter at the documented path is
byte-identical to the version the lesson labels "NOT-THE-RULE".

All five bypasses named in the seat brief reproduce — two on **real lane bytes** (a later "first
freeze": `--freeze f1010f67 --rev 3b960fe5` → exit 0; the harness amendment: `c1-run.sh` at
`cb4326b2` is clean under the default set), three in **fixtures driven by the frozen tool** with the
lane's own path shapes (new counter path, `xpin-attribute.mjs`, `carriers.json` as a symlink).
Two more fall out of the design and are shown here: `--rev` is unbound from the receipt it vouches
for, and a caller-chosen path list makes any revision clean. The lesson's **fail** demonstration is
real and reproduces byte-identically; its **pass** demonstration is at an earlier revision and
therefore cannot discriminate. QUALITY 80's operative test is a manual path argument that the
tool's own default set omits, and its saved evidence proves the veto, not the criterion.

Everything below is read-only git plus fixtures under `/fast/scratch/hyaku/kaidoku-r38/R38W2CritGateBypass`
(removed on exit). No lane file outside this report and `artifacts/R38W2CritGateBypass/` was written.
No tool was installed.

---

## 0. The rule under attack, quoted

`corpus/QUALITY.md:87` (79): *"Before any score is cited, `tools/round-38/freeze-drift.py --freeze
<first freeze> --rev <measured>` runs over the claim's kill-rule paths (claims doc, counters,
carriers, oracles) and must print zero commits. … the amendment is reported, never adopted."*

Three properties that sentence needs and the tool does not have:

| property | tool behaviour | evidence |
|---|---|---|
| `<first freeze>` is derived, not chosen | `--freeze` is any ancestor; no first-ness test | §2.2, §3.1 |
| the measured revision **ships** the freeze bytes | tool prints a commit list; it never requires equality | §3.0 (P7), §3.5 |
| the exit-0 receipt binds the claim it scored | tool never reads a receipt | §2.3, §2.4 |

---

## 1. The lesson's fail/pass demonstration

**Fail leg — real.** Reproduced byte-identically:

```
$ python3 -I -B tools/round-38/freeze-drift.py --root . \
    --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --rev 077e212b tools/round-38/gen-controls.py
{"verdict":"drift", "drift":[{"commit":"efd5c47a72a50b3a434783f82268fb4a96e636a1", …,
          "paths":["tools/round-38/gen-controls.py"]}]}          exit=1
```
Same commit, same path list as `.ufo/waves/round-38/l1/freeze-drift-gen-controls.json`. The M38-1
leg (`freeze-drift-077e212b.json`, default paths) also reproduces: `f1010f67`, `79f69347`, exit 1.

**Pass leg — real tool behaviour, but non-discriminating.** The clean leg is
`freeze-drift-cb4326b2.json`, and `cb4326b2` is the **parent** of the first amendment
(`git log --graph`: `79f69347 ← cb4326b2 ← 9c9d496b ← efd5c47a ← e059ca93`). The interval is empty
of drift because nothing had drifted yet, so the pair `(rev 077e212b, drift)` / `(rev cb4326b2,
clean)` differs in **both** revision and path set. It shows the tool can print clean; it does not
show the tool separates a first freeze from an amendment.

A discriminating pair has to hold the revision fixed. It exists in the lane, one commit later, and
is *worse* for the criteria (§5.1):

```
$ … --freeze e059ca93 --rev efd5c47a                     → verdict=clean  commits=[]
$ … --freeze e059ca93 --rev efd5c47a tools/round-38/gen-controls.py → verdict=drift  commits=['efd5c47a']
```

---

## 2. Bypasses proven

Fixture `artifacts/R38W2CritGateBypass/fixture.sh` (revs `F=84a8c6af … A6=4fe27d4d`, kept
transcript `pingate-transcript.txt`) commits a frozen claims doc + the five default paths, then one
commit per bypass. `fx2-symlink.sh` is the symlink fixture; `real-lane-probes.sh` is the lane run
(`artifacts-real-lane-probes.txt`).

### 2.1 A new counter at a new path
```
CASE A1-default :: gate_exit=0 verdict=clean 0      # commit adds tools/round-38/c1-counter-v4.py + its receipt
CASE A1-explicit :: gate_exit=1 verdict=drift 1     # only when the new path is passed by hand
```
The criterion says the gate runs "over the claim's kill-rule paths (… counters …)"; the tool runs
over a **code constant** (`DEFAULT`, 5 entries) plus whatever the caller adds. A counter that
narrows the predicate is invisible unless its path is guessed. **Smallest correction:** the counter
the receipt names must be, byte for byte, a counter the freeze held — in the repo or copied out of
it. Demonstrated: `counter-not-in-freeze` fires on A1 (§6).

### 2.2 A later commit offered as the "first freeze" — **real lane**
```
$ … --freeze e059ca93 --rev 3b960fe5           → drift ['f1010f67','79f69347']   (honest)
$ … --freeze f1010f67 --rev 3b960fe5           → clean  []                        (offered)
```
`f1010f67`'s own subject is *"round-38: freeze v3"* and `79f69347`'s is *"freeze v2"* — the lane
named its amendments "freezes", so offering one as `<first freeze>` is not even a lie in the lane's
vocabulary. The L1's own stored receipt already does it:
`.ufo/waves/round-38/l1/scores/c1-v3-at-3b960fe5-NOT-THE-RULE.json` has `"freeze":
"f1010f677a53ecf0e671952ce1bf4f44d51e151b"`. Nothing in the criterion or the tool distinguishes
first from later. **Smallest correction:** derive the freeze —
`git log --reverse --format=%H -- plans/round-38-claims.md | head -1` — which on this lane returns
exactly `e059ca9391642d5b71b6662cabcbdce0d9308719` (P8), and refuse an asserted `--freeze` that
differs. Demonstrated: `freeze-not-first` fires on fixture A6 and on the v3 receipt (§6).

### 2.3 `--rev` is unbound from the receipt it vouches for
```
CASE A7-rev-unbound :: gate_exit=0 verdict=clean    (receipt asserts revision A4; gate was told F)
```
The tool's receipt records `rev` — the value it was handed. Nothing compares it with the counter
receipt's `revision` field, so an L1 can run the counter at the tip and the gate at the freeze.
**Smallest correction:** read the counter receipt and require `revision == --rev` and
`freeze == derived`. Demonstrated: `receipt-rev-unbound` fires on A7 and on `tip-c2` (§6).

### 2.4 Amendment through the receipt-producing harness
```
CASE A2-default :: gate_exit=0 verdict=clean 0      # tools/round-38/c1-run.sh + K1/after.json rewritten post-freeze
CASE A2-explicit :: gate_exit=1 verdict=drift 1
```
Real lane, matched pair at one revision:
```
$ … --freeze e059ca93 --rev cb4326b2                                     → clean
$ … --freeze e059ca93 --rev cb4326b2 tools/round-38/c1-run.sh            → drift ['cb4326b2']
```
and at the landing the harness differs from the freeze (P7: `c1-run.sh` in the differing set). The
predicate fixes "run with stock unblob 26.6.4"; the harness is what decides that, and it is outside
the tool's default set by construction — the lesson says so itself (M38-4: "The harness is outside
the kill-rule set"). **Smallest correction:** the harness is a rule path; add `c1-run.sh` and
`gen-controls.py` to the closed set.

### 2.5 Carrier bytes swapped (path omitted from the kill-rule set)
```
CASE A4-default :: gate_exit=0 verdict=clean 0      # corpus/evidence/round-37/c1/K1/carrier.sqsh → "SWAPPED-…"
CASE A4-explicit :: gate_exit=1 verdict=drift 1
```
The default set carries `carriers.json` and `oracle.tsv` but not the carrier binaries the manifest
names, so a swap is gate-clean. The counter is blind too — it never reads carrier bytes, only
`after.json.subject.digest.sha256` against the manifest pin (wave 1 found the counter's half first:
`w1/artifacts/R38CriticClaimsC1/l-carrier-bytes-swapped.json`, `carriers_unchanged` compares JSON
only; the gate's half is §2.5 here). Net: the extraction claim is decoupled end-to-end from the committed carrier bytes; nothing
in QUALITY 79 changes that. **Smallest correction:** add `corpus/evidence/round-37/c1/*/carrier.*`
to the closed set (does not fix the counter's half — that is QUALITY 77/78 territory).

### 2.6 A rule surface reached through a symlink — `fx2`
```
CASE fx2-freeze-modes            :: 120000 .ufo/waves/round-38/c1/carriers.json  120000 corpus/evidence/round-37/c1/K1/oracle.tsv
CASE fx2-freeze-drift-default    :: exit=0 verdict=clean
CASE fx2-freeze-drift-explicit   :: exit=0 verdict=clean     # even with both paths passed
CASE fx2-diff-of-listed-paths    :: (empty = identical)
CASE fx2-real-counter            :: exit=1  json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```
The freeze commits `carriers.json` → `carriers.real.json` and `oracle.tsv` → `oracle.real.tsv`; the
amendment edits **only the targets** (4 carriers → 1, oracle row changed). `git log --name-only`
and `git diff --quiet` both compare identical link text, so the gate is clean on both the default
and the explicit path list. The counter does not go green — it reads the link text via `git show`
and `measure()`'s bare `json.loads(frozen)` raises — but the crash exits **1**, the same code as an
honest "target not met", and writes no receipt. So a rule weakened through a link is gate-clean and
scored "not met": indistinguishable from a legitimate miss. **Smallest correction:** every kill-rule
path must be a regular blob (`100644`/`100755`) at both revisions. Demonstrated:
`non-regular-kill-rule-path` fires on fx2 at both revisions (§6).

### 2.7 Editing the helper the counter imports (`tools/round-27/xpin-attribute.mjs`)
```
CASE A3-default :: gate_exit=0 verdict=clean 0
CASE A3-explicit :: gate_exit=1 verdict=drift 1
```
The gate is blind, but this is **not** a scoring bypass for C1: the counter reads the helper **at the
freeze** (`evidence_ids(root, freeze, …)` → `show(root, freeze, XPIN)`), so an amendment at the
measured revision cannot move C1's evidence ids. Two live exposures remain, neither gated:
1. any counter that reads the helper at `rev` (the natural way to write one) flips with it;
2. `--pkg65` points outside git (`/home/vgpnk/.npm/_npx/…/rea-agents`) and is neither pinned nor
   version-checked — the predicate says "rea-agents 6.5.0 rule", the counter accepts any root.
**Smallest correction:** the helper is a rule path, and the receipt must record the package root's
digest (`QUALITY 78` already asks for "the package root that the recompute used" — the receipt does
not carry it).

### 2.8 (found) The clean verdict is only as strong as the caller's path list
```
$ … --freeze e059ca93 --rev 3b960fe5 corpus/evidence/round-37/c1/K1/oracle.tsv   → verdict=clean
```
That is the QUALITY 79 command with a narrower list, at the landing, exit 0. A gate receipt that
prints `paths` is auditable; nothing in the criterion says which list is *the* list, so the receipt
`freeze-drift-cb4326b2.json` ("clean") and this one are the same kind of artefact.

---

## 3. The criterion permits adoption, and the landing adopted

This is the deepest defect and it is not a fixture: **the amendment is the shipped bytes.**

```
P7  efd5c47a: gen-controls.py
    3b960fe5: plans/round-38-claims.md  tools/round-38/c1-counter.py  tools/round-38/c1-run.sh  tools/round-38/gen-controls.py
    0fc61133: (same four)
P9  frozen  counter (sha256 a7a62b098709, extracted from e059ca93) at 3b960fe5 → carriers_matched=3 met_target=False
    shipped counter (tools/round-38/c1-counter.py at the landing) at 3b960fe5 → carriers_matched=4 met_target=False
```
`git diff --numstat e059ca93 0fc61133 -- tools/round-38/c1-counter.py` is `52 20` (claims doc `48 35`),
and the shipped counter is **exactly the v3 bytes** the lesson labels "NOT-THE-RULE"
(`sha256 d9aa8b62…` at `3b960fe5` and at `0fc61133`; the freeze's is `a7a62b09…`). The shipped
claims doc is headed **"# kaidoku round 38 — frozen claims (freeze v2)"** with a *"Freeze v2 note
(pre-scoring amendment)"* and a kill rule that now reads *"never changed after the v2 commit"*
(`plans/round-38-claims.md:72`). The shipped counter changes the predicate in substance — it adds a
`before` arm and replaces `after_gaps_empty` with `after_no_missing_extractor_gap` (only
`missing-extractor-dependency` gaps fail) — and the shipped predicate text inverts the freeze's
premise ("run with `sasquatch-v4be` available" vs "no external extractor dependency").

The shipped pair does not even agree with itself: the claims doc was not touched after `79f69347`
(v2 text, header "freeze v2"), while the counter at that path is `f1010f67`'s v3 bytes. A reader who
runs the documented command executes v3 against a v2 predicate.

So: the *score of record* is honestly the v1 verdict, but the *rule a later reader runs* is v3 at the
documented path. QUALITY 79's "reported, never adopted" is satisfied for the citation and violated
for the artefact. Freeze-drift printing two commit shas is not a barrier to shipping the amendment;
it is a bookmark. **Smallest correction:** either (a) require byte equality at the measured/landing
revision over the rule set (`git diff --quiet FREEZE REV -- …`), or (b) require the frozen counter to
be preserved at an immutable path that the claims doc's counting command names
(`tools/round-38/c1-counter.v1.py`). (a) is what §6 implements. Note (b) is the only option that
works for a claim already landed, so the criterion should probably require both: (b) at freeze time,
(a) at citation time.

---

## 4. `freeze-drift.py` is unpoliced and post-dates the freeze it judges

```
P12 tools/round-38/freeze-drift.py at e059ca93: ABSENT      (added at 3b960fe5)
```
The gate is not in its own `DEFAULT`, not in `CLOSED`, and did not exist in the freeze it is used to
judge. A later L1 can edit `DEFAULT` — it is a list literal in the tool — and the gate keeps
exiting 0. §2.8 shows the same effect without touching the file: the list is an argument. **Smallest
correction:** from the next round the gate is itself a kill-rule path; and record `paths` in the
receipt *and* cross-check it against the tool's frozen `DEFAULT`.

---

## 5. QUALITY 80

### 5.1 The M38-2 defect passes the M38-1 gate, at the same revision
```
$ … --freeze e059ca93 --rev efd5c47a                                     → clean    (QUALITY 79 as written)
$ … --freeze e059ca93 --rev efd5c47a tools/round-38/gen-controls.py      → drift ['efd5c47a']
```
`efd5c47a` is the commit that landed the seven control receipts **and** the generator fix. The
criterion's operative test is therefore a prose clause ("run `freeze-drift.py` over the generator
path too") that lives in QUALITY 80, not in the tool's default set and not in QUALITY 79's command
line. An L1 that runs the QUALITY 79 command verbatim gets exit 0 on the exact defect QUALITY 80
exists for. **Smallest correction:** one command, closed set — add `gen-controls.py` (and
`c1-run.sh`, carrier bytes, the helper) to `DEFAULT`, so M38-1 and M38-2 cannot be gated separately.

### 5.2 Two of QUALITY 80's clauses are unsatisfiable for the round that introduces it
* "Control generators **and control receipts** land **in** the freeze commit": the receipts landed
  at `efd5c47a` (`…/round-38/controls/ctl-c*.json`, 7 files, after the freeze). The lesson's M38-2
  fix cell is honest about this ("none: no rule required…"), but the criterion text reads as a
  retrospective requirement the round never met.
* "a control replays at the freeze revision to the receipt's verdict": at `e059ca93` the frozen
  generator passes `'1'/'2'/'3'` where `c2_fixture` branches on the control *names*, so CTL-C2-1/2/3
  mint the repaired green fixture (`w1/R38ReviewerControlReplay.md` F1–F3). Replaying at the freeze
  cannot give the receipts' exit 1. The criterion should say "from the round after"; as written it
  invites a later reader to believe round 38 complied.
The saved evidence (`freeze-drift-gen-controls.json`, exit 1) proves the **veto**, not either
clause. It is a good veto; it is not a control for the criterion's own text.

---

## 6. Proposed correction, shown able to fail

`artifacts/R38W2CritGateBypass/pin-gate.py` (175 lines, stdlib only) implements the six
corrections above: derived freeze; byte equality over a closed rule set; mandatory receipt bound to
`--rev` and the derived freeze; counter identity by content (repo or copy); claim data reported but
exempt (its provenance is QUALITY 78's independent re-run); regular-blob type check.

**Fails on every bypass, in a fixture** (`pingate-transcript.txt`):
```
PINGATE F..A0 docs-only (pass leg)           exit=0 clean []
PINGATE F..A1 new counter path               exit=1 drift ['counter-not-in-freeze']
PINGATE F..A2 harness+after receipt          exit=1 drift ['bytes-differ']
PINGATE F..A3 xpin helper                    exit=1 drift ['bytes-differ']
PINGATE F..A4 carrier bytes                  exit=1 drift ['bytes-differ']
PINGATE F..A5 carriers.json symlink          exit=1 drift ['non-regular-kill-rule-path', 'bytes-differ']
PINGATE F..A6 counter amended                exit=1 drift ['non-regular-kill-rule-path', 'bytes-differ', 'counter-not-frozen']
PINGATE A6 offered as 1st freeze             exit=1 drift ['freeze-not-first', …]
PINGATE receipt rev != measured rev          exit=1 drift ['receipt-rev-unbound']
```
**Passes on a docs-only commit**, so the pass leg is at *the same history* as the fail legs.

**On real lane bytes** (`pin-*.json`):
```
freeze-rev  exit=0 clean []                                    # e059ca93 with a receipt naming it
controls    exit=1 ['bytes-differ']                            # gen-controls.py at efd5c47a  ← M38-2
landing-v1  exit=1 ['bytes-differ']                            # claims doc, c1-counter, c1-run.sh, gen-controls.py
tip-c2      exit=1 ['bytes-differ','receipt-freeze-unbound']   # C2 receipt has no freeze field at all
v3-receipt  exit=1 ['bytes-differ','receipt-freeze-unbound','counter-not-frozen']
```
The `landing-v1` row is the finding of §3 stated as a gate result: the claim's own score receipt is
honest, but the revision it names does not ship the rule it was scored by. Note this gate would
**refuse** round 38's landing, which is the correct answer for a criterion that says "never adopted"
— the lesson must say so rather than imply the amendment was contained.

---

## 7. Two incidental defects found while testing the gate

1. **False provenance in the lesson under attack.** `corpus/lessons/round-38.md:11` cites
   `.ufo/waves/round-38/l1/scores/c2-final.json`; that file does not exist (`P11`). The committed
   receipt is `c2-at-0fc61133.json`, and `SCORECARD.md:3406` repeats the same non-existent path. The
   lesson's Routed-defects section claims "every receipt this round cites is committed" (R37-CL1).
   Fix: re-point both to `c2-at-0fc61133.json`.
2. **C1's stop has three failing bindings, the record names one.** Running the frozen counter at the
   landing (`P9`) gives `carriers_matched=3` *and* `province_core_section=false`,
   `province_core_row=false` — the claim's Core row never landed (the commit subject says "BE v4
   entry (not promoted)"). The lesson's verdict line says the stop is "`carriers_matched 3`, K2 fails
   on one `unpublished-entry` gap". The verdict is right; the stated reason is incomplete.
3. **Related counter false positive (QUALITY 77 family, counter-side; found in wave 1 by
   `w1/R38CriticClaimsC1.md` §4, independently reproduced here).** The `frontier_note` binding
   is `'big-endian' in line and 'superseded' in line` anywhere in `PROVINCE.md`. `PROVINCE.md:157`
   satisfies it with *"superseded for LE SquashFS v4 … big-endian/AVM stays here"* — a sentence that
   keeps BE in Frontier, the opposite of the predicate's "the round-38 frontier note supersedes the
   big-endian Frontier bullet". The binding is true on a line that refutes the claim it scores.

---

## 8. Axes

| axis | impact |
|---|---|
| **calibration** | primary. Verdict reason understates (2 bindings + 1 carrier); lesson cites a non-existent receipt; QUALITY 79/80 evidence pairs are (drift, different rev/path set), so neither criterion has a discriminating control |
| **coverage** | secondary. The C1 claim's *identity* changed between freeze and landing (external-dependency premise inverted, before-arm added); the shipped artefact scores a different claim than the one frozen, and the coverage surface (`PROVINCE` Core row) never landed |
| **depth** | none. No depth claim is affected by any of this |

---

## 9. Smallest safe correction, in one place

1. **Freeze identity:** derive from the first commit touching the claims doc; refuse assertions.
2. **Bytes:** `git diff --quiet FREEZE REV` over a closed rule set — claims doc, both counters,
   `carriers.json`, oracles, carrier bytes, `gen-controls.py`, `c1-run.sh`, `xpin-attribute.mjs`,
   the gate itself. Claim data (`after.json`/`before.json`) is exempt and reported.
3. **Receipt:** mandatory; `revision == --rev`, `freeze == derived`; the counter named in `argv`
   must be some freeze counter's bytes; the package root's digest is recorded.
4. **Type:** kill-rule paths are regular blobs at both revisions.
5. **Wording:** QUALITY 80 dated forward-only; QUALITY 79's command is one invocation with the
   closed set (i.e. the tool's `DEFAULT`, not an operator's list).
6. Re-point `lesson:11` / `SCORECARD:3406`; state C1's three failing bindings; tighten
   `frontier_note` to match the predicate or report it as unmet.

---

## 10. Limits

* I did not re-run REA extract-firmware; all scores here reuse the committed receipts and the frozen
  and shipped counters over them. The extractor premise (M38-3) is out of this seat's scope.
* The fixture's `A5`/`fx2` counter outcome is a real counter invocation on `fx2` (`exit=1`,
  `JSONDecodeError`), not a model of one; the `A5` variant was inferred from the same code path
  before the `fx2` run and is superseded by it.
* [INFERENCE] A counter written to read `xpin-attribute.mjs` at `rev` flips with a helper edit; I
  did not write such a counter, and the shipped C1 reads at `freeze`.
* The freeze counter's identity is not inferred: `e059ca93:tools/round-38/c1-counter.py` hashes to
  `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8` (17469 B), the same sha and size
  wave 1 records for v1 (`w1/R38CriticClaimsC1.md:26`), and the L1's `c1-v1-at-3b960fe5.json` argv
  names a copy of it; the shipped v3 is `d9aa8b62…` at both the landing and the tip.

Artifacts: `artifacts/R38W2CritGateBypass/{pin-gate.py, fixture.sh, run-pingate.sh,
fx2-symlink.sh, real-lane-probes.sh, pingate-transcript.txt, fx2-transcript.txt,
artifacts-real-lane-probes.txt, pin-*.json, frozen-counter-at-landing.json,
shipped-counter-at-landing.json, shipped-counter-at-tip.json, probe-receipt-at-*.json}`.
