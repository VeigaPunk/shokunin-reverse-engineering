source: S321 — `/usr/bin/printf` (host binary), sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`, measured by `tools/round-96/fresh-source2-check.py` with receipt `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`; plus the wave evidence for the kill-rule closure: the before receipts `.ufo/waves/round-96/pre/c1-legacy-rule-at-base.json`, `.ufo/waves/round-96/pre/c1-v5-admits-unbound-at-base.json`, `.ufo/waves/round-96/pre/c1-probe-writer-unbound-at-base.json` and the after receipts `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json`, `.ufo/waves/round-96/l1/scores/honest-pos.json`, `.ufo/waves/round-96/l1/scores/honest-pos-red-head-not-bound.json`, `.ufo/waves/round-96/l1/scores/c1-symlink-v6-at-decl.json`. The registry row is S321 in `corpus/SOURCES.md`; the draft row is `.ufo/waves/round-96/w1/ScribeKnowledge/sources-row.md`.
verified-at: 2026-11-05 (the measured landing revision is named in `corpus/lessons/round-96.md` `## Measured`; the counter bytes are the supersession bytes at `3baac2ef4b9b2830d299125b8184ca06d9e6584d`, unchanged at the landing). The round-96 counter is `tools/round-96/stop-boundary-repair-battery-v6.py`, sha256 `7d7d559ac144eda6d163dd1d9ab26ed95ac089e18ccbb029bd91ae4277e46c06`; the counting command is `tools/round-96/kill-rule-v2.py`, sha256 `3b8c7583c9c9d6aa9e42a6a8e718d16bac4371a4fbdf7fd345f0190b1dc9bb5f`; the probe is `tools/round-96/symlink-probe-v2.py`, sha256 `67b74a4b9f884464efc8021f584d6eeb4447b13e65f3882a41025ff58dfa11ec`; the S321 measurement tool is `tools/round-96/fresh-source2-check.py`, sha256 `124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9`. All four digests are the committed `.ufo/waves/round-96/pins.sha256` values.
recheck: `sha256sum /usr/bin/printf` (must print `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf`) plus a fresh-source2-check rerun: `python3 -I -B tools/round-96/fresh-source2-check.py --root . --work <scratch> --rev <HEAD> --json-out <receipt>` — exit 0 with stdout `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0`.

## (a) The kill-rule blind-spot class: a rule that never reaches the gate it asserts

Round 95 froze a kill rule and its counting command was green, but the rule could not
see five of the ten mutants it was supposed to kill. The reason is structural, and the
class generalises beyond this lane: **the rule's checks never called the instrument's
`main()`, and never ran the probe**, so every gate that lives inside `main()` — the
writer's `fsync`, the forced self-verification, the fail-closed exit code, the public
revision binding — was outside the rule's reach, and the probe's own verdict was never
read.

The formalised round-95 rule is committed as
`tools/round-96/legacy-kill-rule.py` (sha256
`2192da45bdf581cf1272c9a8c58e0a0059b26b591c9d1a7bf1395c3838d23939`) with its four
checks `(i)` counter selftest, `(ii)` agreement selftest, `(iii)` forgery selftest,
`(iv)` forgery battery. Measured at the base `0ea695e826f2dca53dd55ac0bafead93de26b173`,
it kills **5 of 10** mutants, and the survivors are exactly five named mutants —
receipt `.ufo/waves/round-96/pre/c1-legacy-rule-at-base.json` (`label "r95-rule mutants
killed 5 of 10"`, `counts {killed: 5, mutants: 10}`, `exit 1`):

| mutant | the edit | why the frozen rule could not see it |
|---|---|---|
| M2 | `os.fsync` removed from the writer | the rule never called `write_receipt`, so no `fsync` ever happened inside the checked process |
| M3 | the self-verification forced to `ok` (`selfverify = {"ok": True, "reasons": []}`) in the counter's `main()` | the rule ran the *selftest*, not the *public* path whose self-verification was forced |
| M4 | the fail-closed `code = 1` removed from `main()` (`if code == 0 and not selfverify["ok"]: code = 1` → `pass`) | the fail-closed exit lives in `main()`, which the rule never called |
| M6 | the `revision-not-bound` branch removed from the v6 counter's `verify_receipt` | the legacy rule ran the **round-95** counter's selftest, which carries no wrong-revision case, and the round-95 agreement instrument (not the v6 `verify_receipt`) for the forgery legs — so the branch the mutant deletes was never exercised |
| M10 | the probe's verdict hard-coded (`"verdict": "hardened"`, `"met": True`) | the rule never ran the probe, so it never compared the probe's receipt to the truth |

The five that *were* killed are M1 and M5 (the legacy rule's check `i-counter-selftest`
fails on both) and M7, M8, M9 (checks `ii-agreement-selftest`, `iii-forgery-selftest`
and `iv-forgery-battery` fail on all three) — the mutants whose effect is visible in a
selftest or in a forgery battery, which is exactly the surface the frozen rule did
touch. The pattern is the finding: **a rule's coverage is the set of gates its
commands actually execute, not the set of gates the instrument claims to have.**

The successor rule `tools/round-96/kill-rule-v2.py` closes the class by adding the
named checks the round-95 mutation seat specified, each aimed at one unreachable gate:

| check | what it executes | what it kills |
|---|---|---|
| K-selftest | the counter's and the agreement's `--selftest` (v6 carries 13 cases, the agreement 5) | M1, M5, M6, M7, M8, M9 |
| K-forgeries | `verify_receipt` of the counter over the six round-96 forgeries **with the intended single reason required exactly**, plus the four round-95 forgeries refused | the unbound-field class (section (b)) |
| K-agreement | the round-95 agreement instrument as a subprocess, exact reasons, honest triple accepted | the agreement-reason class |
| K-dmain | the counter's `main()` with a faked verdict: honest exits 0; shortrev, rewrite and notrecomp exit non-zero; a run without `--json-out` exits 2 | M3, M4, M5 and the green-without-a-receipt gap |
| K-fsync | an instrumented count of `os.fsync` during `write_receipt` is ≥ 1 | M2 |
| K-probe | the probe's receipt content: `verdict == "hardened"` **iff** `victim_intact and receipt_valid`, and `met` stating the same | M10 |
| r95 battery regression | the round-95 forgery battery re-run must exit 0 | a rule change that breaks the prior round's battery |

The "what it kills" column above is read from the **measured** mutant rows of
`.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` (which check has `ok: false`
for each mutant), not from the declared `kills_via` strings in
`.ufo/waves/round-96/mutants.json`. The two differ in one place, and the difference is
worth recording rather than smoothing over: the mutant table declares M6
(revision-binding removal) to be killed by "K-dmain shortrev", but the measured receipt
shows **M6 is killed by K-selftest** — the v6 counter's selftest carries a
wrong-revision case, so the mutant fails the selftest before the negative control
reaches it. M6 is killed either way; the *attribution* of the kill is what the receipt
records. (M5, declared "K-selftest verify-catches-not-frozen", is measured as failing
both K-selftest and K-dmain/rewrite.) The measured attribution per mutant:

```
M0  killed=false  (identity control — no failing check)
M1  killed=true   K-selftest
M2  killed=true   K-fsync
M3  killed=true   K-dmain (notrecomp, rewrite, shortrev)
M4  killed=true   K-dmain (notrecomp, rewrite, shortrev)
M5  killed=true   K-selftest, K-dmain/rewrite
M6  killed=true   K-selftest
M7  killed=true   K-agreement, K-selftest
M8  killed=true   K-agreement, K-selftest
M9  killed=true   K-agreement, K-selftest
M10 killed=true   K-probe
```

The after receipt `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` records the
result at the declaration: `label "mutants killed 10 of 10; forgeries refused 10 of 10;
negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1"`, `exit 0`,
`identity_not_killed true` — the identity mutant M0 must **not** be killed, or the rule
is a blanket refusal rather than a discriminator. The honest arm's own K-dmain rows
read `pos` exit 0, `shortrev` exit 1, `rewrite` exit 1, `notrecomp` exit 1, `nojson`
exit 2; K-fsync reads `fsync_calls 1`; the two selftests read
`SELFTEST cases=13 failures=0` and `SELFTEST cases=5 failures=0`; the r95 battery
regression reads exit 0.

One honest reading of that receipt belongs here, because it is the same class seen from
the other side: the honest arm's K-probe row reads `verdict "followed-symlink"`,
`victim_intact false`, `receipt_valid true`, `met false` — the probe is *correct* there
because the writer it was pointed at is the round-94 v4 writer, which does follow the
planted link. K-probe scores consistency, not hardness: the honest arm passes because
the probe's verdict agrees with the truth about the writer it was given. The hardened
leg is the separate public probe run (section (c)).


**Provenance of the declaration-time receipts (corrected at landing).** The receipts `.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json`, `honest-pos.json` and `c1-symlink-v6-at-decl.json` name the declaration revision `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` in their `revision` field, but they were measured while the disclosed v6 fix (`resolve_rev` accepting `HEAD`) existed only as uncommitted working-tree bytes. The critic (`w1/CriticC1.md` finding 3) showed that `honest-pos.json` records a `counter_sha256` equal to the `3baac2ef` bytes, not the bytes at its named revision. A receipt that names a revision its bytes do not come from is the same class this entry describes, so the landing re-measurement at a clean committed tree is the receipt of record; the declaration-time receipts are kept as evidence of the iteration and are not cited as clean-tree measurements.

## (b) The unbound fields: a receipt that claims what it does not check

The same round's critic found six receipt fields the counter recorded but never bound —
and, worse, a self-verification that could be skipped entirely. The before arm is
committed as `tools/round-96/r95-unbound-at-base.py` (sha256
`bf006dfec04f61182733f4f98bfe3c9bbb636ff216b20d2813839ca10c46bdbf`), measured against
the pinned round-95 counter `tools/round-95/stop-boundary-repair-battery-v5.py`
(sha256 `6fc81208c9b151f35c9768bc1f481a1bdd0bcc0854d9732879e38e6b87194b7f`,
`target_bytes_identical_to_rev true`). The receipt
`.ufo/waves/round-96/pre/c1-v5-admits-unbound-at-base.json` records:

- **5 of 6 forgeries accepted**, `label "unbound accepted 5 of 6 (1 crash); nojson exit 0"`,
  `exit 0`;
- **typed refusals: 0** (`unbound {accepted: 5, crashed: 1, typed_refusals: 0, total: 6}`);
- the sixth fixture crashes with a bare `KeyError: 'fresh_scored'` instead of a typed
  refusal;
- the no-`--json-out` scenario **exits 0** with `receipt_written false` — a green verdict
  with no receipt at all.

The six committed forgeries (`.ufo/waves/round-96/forgery/forge-<name>.{json,stdout,rc}`)
each violate exactly one binding, and each is bound by the v6 counter with a typed
reason. The intended reasons are frozen in `.ufo/waves/round-96/mutants.json`
(`forgery_reasons`), and the after receipt confirms every one is refused with **exactly**
that reason (`exact: true` on all six rows of K-forgeries):

| fixture | the field it leaves unbound | typed reason |
|---|---|---|
| `forge-unlabelled` | the counts object has no `fresh_scored` key | `counts-missing-key:fresh_scored` |
| `forge-met-lying` | `met_target false` while the label still equals the frozen expect | `met-not-recomputed` |
| `forge-head-mismatch` | `head` is not the full 40-hex resolution of the measured tree | `head-not-bound` |
| `forge-counter-pin` | `counter_sha256` does not match the counter's bytes | `counter-pin-not-bound` |
| `forge-verdict-pin` | `verdict_sha256` does not match the verdict code's bytes | `verdict-pin-not-bound` |
| `forge-repair-pin` | `repair_sha256` does not match the bytes at `--repair-cmd` | `repair-pin-not-bound` |

The v6 counter's `verify_receipt` (`tools/round-96/stop-boundary-repair-battery-v6.py`)
implements these as separate branches, so a fixture that violates exactly one binding
is refused with exactly that one reason. Two further properties are worth naming
because they are the difference between a *typed refusal* and a crash:

- the counts schema is checked first (`count_problems`), so a missing key is
  `counts-missing-key:<k>` and a mistyped one is `counts-type:<k>` — never a `KeyError`;
- the met direction is bound **downward**: a receipt whose label equals the frozen
  `--expect` but that claims `met_target false` is refused (`met-not-recomputed`); the
  met-true direction keeps the round-95 reason `label-not-frozen`.

And the receipt is now **mandatory**: `--json-out` is required on the public path, a run
without it refuses before scoring with exit 2 and a typed `receipt-required` line, so a
green verdict cannot exist without a verified receipt. The after receipt
`.ufo/waves/round-96/l1/scores/honest-pos.json` records the honest public run at the
declaration revision: `exit 0`, `met_target true`, `label "repaired 12 of 12; wrong 0;
unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"`, and its
stdout `.ufo/waves/round-96/l1/scores/honest-pos.stdout` reads `selfverify ok=True
reasons=0` (stdout file `.rc` reads `0`, `.stderr` is empty).

**The fail-closed gate is demonstrated, not asserted.** The disclosed supersession
commit `3baac2ef4b9b2830d299125b8184ca06d9e6584d` exists because the v6 counter's
`resolve_rev` accepted only hex revisions, so the honest run was invoked with `--rev
HEAD`, the receipt's `head` came out `None`, and the run **failed closed**. The red
evidence is committed as the four files
`.ufo/waves/round-96/l1/scores/honest-pos-red-head-not-bound.{json,stdout,stderr,rc}`:
the receipt JSON records `head null` (and no `selfverify` key at all), the `.stdout`
reads `selfverify ok=False reasons=1` followed by the label line ending `met True exit 1`,
the `.stderr` reads `selfverify reason: head-not-bound`, and the `.rc` file reads `1`.
(The receipt JSON's own `exit` field reads `0` — that is the *battery's* inner exit,
which was fine; the **process** exit is the `.rc` file's `1`.) A met-True verdict that
cannot be bound to a measured tree is refused with exit 1 — that is the `head-not-bound`
gate firing on the honest arm, and it is kept as evidence rather than deleted.

## (c) The probe's own write escape, and its closure

The round-95 probe wrote its **own** `--json-out` receipt with `open(..., "w")`. A
symlink planted at that path was therefore followed and the victim file consumed — the
probe was measuring the writer's escape while itself escaping. The before/after driver
is committed as `tools/round-96/probe-writer-legs.py` (sha256
`82b4e2a3e314adbeeb347a2ec9033572c6cb0fcb4ac261096d24df3a23f49584`); both legs point
the probe at a writer path that does not exist, so the writer subprocess fails fast and
the exercised surface is exactly the probe's own receipt write. The receipt
`.ufo/waves/round-96/pre/c1-probe-writer-unbound-at-base.json` records the difference:

- **before** (`tools/round-95/symlink-probe.py`): `victim_intact false` — the victim
  was consumed;
- **after** (`tools/round-96/symlink-probe-v2.py`): `victim_intact true` — the victim
  survived, and the receipt is still readable through the path.

The closure is the same hardened writer the counters use — a unique `mkstemp` temporary
name in the receipt's own directory, `flush`, `fsync`, then `os.replace` onto the
target, which swaps a planted link instead of following it. The public probe leg
against the v6 counter is committed at
`.ufo/waves/round-96/l1/scores/c1-symlink-v6-at-decl.json`: `verdict "hardened"`,
`victim_intact true`, `receipt_valid true`, `tmp_is_symlink true`, `tmp_left true` —
the planted symlink is still there, untouched and unread, because the writer never
opened that name.

## (d) The second fresh source (S321): closing the round-93 carried limit

Round 93 carried the limit "the fresh-pack arm has one source (`/usr/bin/env`)". The
round's sourced step opens a **second** one: `/usr/bin/printf`, a host binary with
sha256 `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`
(little-endian x86-64 ELF, packable by upx 5.2.0 on this host).

The measurement is `tools/round-96/fresh-source2-check.py` (sha256
`124f71f75548c9c46e6e2fdf88c569c54cd2a3339abcdcbb4dd9561915d008f9`), which drives the
**unchanged** round-92 helpers (`stop-boundary-battery-v2.py`, sha256
`f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874`, and
`stop-boundary-repair-battery.py`, sha256
`63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`); the frozen v3
verdict code and its `FRESH_SOURCES` pin are untouched. Four properties are measured:
pack determinism (two `upx --best` packs are byte-identical), no collision with any
public carrier's packed bytes, the intact control (the repair on the pristine packed
image returns it byte-identical), the near cells (the last block's `sz_cpr` moved by
the round-92 near deltas is repaired) and the far cells (the same block moved by the
round-92 far deltas is refused).

The committed receipt `.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`
(measured at the base `0ea695e826f2dca53dd55ac0bafead93de26b173`) reads:

```
label = "fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1"
met_target = true
exit = 0
counts = {"far": 2, "far_refused": 2, "near": 2, "repaired": 2}
deterministic = true
collides_public_packed = false
intact_identity = true
blocks = 5
packed_sha256 = "95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6"
source = "/usr/bin/printf"
source_sha256 = "b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7"
```

The four cells are: two near cells (deltas −7 and +7, block 31358) both classed
`repaired` with `rc 0` and `box_after ["in", "out"]`, and two far cells (deltas −40 and
+40) both classed `refused` with `rc 2` and `box_after ["in"]` — the far refusal is
typed by the round-92 repair tool itself
(`"refused": "stop-boundary: no green value in the +/-16 window (spots [(31358, 206)], the packer refuses the input and every in-window candidate)"`).

**This measurement is supplementary and is not part of the frozen label.** The frozen
R96-C1 label is `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3
of 3; probe consistent 1 of 1; honest accepted 1 of 1`, and the frozen battery label is
`repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12;
fresh-roundtrip 2 of 2`. The S321 label is a **different** string
(`fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1`) and measures
**source diversity** of the held-out arm, not a new repair capability: the round-93
carried limit "the fresh-pack arm has one source" is closed as a diversity claim, and
nothing here widens the repair class, the carrier set, or the declared window.

## (e) Named limits carried from the declaration

These are the limits stated before the data in `plans/round-96-claims.md`
(R96-C1, "Named limits (stated before data)") and they are carried, not closed:

1. **No provenance authentication.** The v6 bindings bind a receipt to the world it
   claims; they do not authenticate provenance. A wholly consistent re-authored triple
   whose every field describes the honest world is byte-indistinguishable from an
   honest capture.
2. **K-probe reads only the receipt.** It checks that the probe's receipt is
   self-consistent (`verdict == "hardened"` iff `victim_intact and receipt_valid`). A
   probe that lies consistently with a manipulated victim state is not caught by
   consistency alone.
3. **The mutant table is the declared ten plus the identity control** — M0 (identity,
   must not be killed) and M1–M10 — not a claim about all possible mutants. The five
   round-95 survivors are *adapted* to the v6 counter bytes and the v2 probe; they are
   not new mutants.
4. **K-dmain fakes `v3.score` in-process.** The negative-control scenarios substitute
   the verdict code's `score` function rather than exercising the real battery; the
   real battery path is exercised by the honest public run and the probe legs, not by
   the negctl scenarios.
5. **The fsync count is instrumented at the Python level**, by replacing `os.fsync`
   with a counting wrapper — not `strace`.
6. **The `head` binding forces `--rev == HEAD` on every green run.** A landing receipt
   re-run must pass `--rev <HEAD>`; a run with a stale or symbolic revision
   fails closed (section (b)).

Unchanged from earlier rounds and still open: PE and Mach-O packed inputs remain
unmeasured.

## (f) Limits the wave's attacks found (not closed here; routed to round 97)

The round's attack seats (`.ufo/waves/round-96/w1/`) found limits outside the frozen predicate. They are recorded, not repaired: changing a counter after its scoring would change the rule the claim was scored under (the kill-rule clause in `plans/round-96-claims.md`).

- **`met_target` type (ReviewerInstruments H-1; CriticC1 A5/A6).** `verify_receipt` tests `met_target` only with `is True` and `is False`. A receipt that omits `met_target` or carries `null` or the string `"true"` verifies clean, and `main` then exits 0 with `met None`. No frozen fixture or mutant covers it.
- **`head` is a commit pointer, not a byte binding (CriticC1 finding 3; ConnectorOverlap).** `head == revision` proves the commit name, not the bytes measured. A dirty working tree can be measured under a clean commit's name; the declaration-time receipts above are that case. Byte binding needs `git cat-file blob <rev>:<path>` for the pins, as `kumitate-shokunin/scripts/receipt-bind.mjs` does.
- **The kill rule does not run a `--rev` other than HEAD (CriticC1 finding 4, M11).** A mutant that sets `receipt["head"] = resolve_rev(root, args.rev)` survives the frozen rule; only a scenario with a non-HEAD revision kills it, and the frozen rule has none.
- **The kill rule does not bind its own green exit to a receipt (ReviewerInstruments M-2).** `--json-out` is optional on `kill-rule-v2.py`; v6 requires it.
- **Bool and extra-key counts (CriticC1 finding 5, M12; finding 1).** No bool fixture exists; a count key outside the nine `COUNT_KEYS` is not bound.
- **Unbound pins and fields (CriticC1 finding 1).** `repair_cmd` (while its sha256 matches), `public_met` / `public_label`, and the imported `imported_r92_battery_sha256` / `imported_v2_sha256` are recorded and not bound.
- **The probe's K-check runs the unhardened writer (CriticC1 finding 6, P2).** A probe that always reports `followed-symlink` survives K-probe; the hardened discrimination is the separate public leg, outside the label.
- **Writer durability is a call count (SentinelWrite F3/F5; ReviewerInstruments L-3).** K-fsync counts one call; it does not check the call precedes the replace, and the directory is not fsynced. The fleet model is `souji-shokunin/census/round-60/wave/w1/S60ExecRecorder/souji-receipt-write.py` (file fsync, then directory fsync).
- **The probe's own write escape is not in the frozen label (MutationC1 N7, M96-h).** Reverting the probe's receipt write to `open("w")` leaves every frozen check green: the K-probe honest leg runs the unhardened writer, and no check plants a link at the probe's receipt path. The hardened probe is measured only by the public leg. Route: a planted-link leg on the v6 writer, as a frozen check, round 97.
- **A crash counts as a kill (MutationC1 N9).** A mutant that makes `count_problems` raise a `KeyError` turns the rule red for the wrong reason. Route: distinguish a crash from a false verdict.
- **The frozen command is cwd-dependent (M96-j).** The regression leg's relative `--honest-dir` is safe only from the tree root.
- **Sibling writer still live (ConnectorOverlap).** `kake-shokunin/scripts/instrument_receipts.py:643-646` at `bde9869144f69c5a459c0d2c93f5135922fe3a8d` writes `destination + ".tmp"` through a plain `open`. Routed to the owning lane through the round-96 report; not edited here.

---

*Draft provenance: seat ScribeKnowledge, round 96 attempt 1. Nothing in this draft
edits a lane file; the L1 lands the entry, the S321 row and the lesson sections
together, so the row's `used-by` paths exist on disk at the landing commit.*
