# CritDigest — is `mutations_sha256` a behavioural pin? (R47-C1 clause 6)

Seat `CritDigest`, round 47 wave 1. Target: `plans/round-47-claims.md` R47-C1 clause 6
(`mutations_sha256` over `"\n".join(name for name, _ in MUTATIONS)`) and clause 9 (the battery
counts), against `tools/round-47/exact.py@1e2c3102`, block 24 at `SKILL.md:632`.
Lane tree read-only; every mutation was applied to a copy under
`/fast/scratch/hyaku/kaidoku-r47/CritDigest/` (git fixture repos, one commit each).

## Verdict

**predicate too weak, here is what closes it.**

`mutations_sha256` is a *label manifest*, not a behaviour pin. Five rewrites of the four
mutators leave it byte-identical and the counter green; one pure label rename moves it and
forces a re-pin. The battery that clause 6's "denominator" is supposed to defend reports
`forgeries_total 4, v2_green 4, v3_green 0` on a mutation list that mutates nothing at all.

## Frozen facts (re-derived, not read)

```
sha256("\n".join(["substring-arm","duplicate-routed-id","stale-mutations-digest","flag-order-drift"]))
  = 19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112   (block pin: equal)
sha256(HEAD:tools/round-47/exact.py)
  = dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c   (block pin: equal)
```

Mechanism: `tools/round-47/exact.py:96` builds `MUT_DIGEST` from `n for n, _ in MUTATIONS` —
the first tuple element only — and `exact.py:250` compares the block's pin against it. The
function object is never hashed. Both pins are therefore jointly satisfiable by *any* file
named `tools/round-47/exact.py`: the landing author pastes both values from whatever the file
says, and nothing compares the file to the claims file's frozen sentence about what the four
forgeries do.

## Counterexample 1 — behaviour changes, digest identical, counter green

Fixture `fx-a1a` (= lane at `1e2c3102`, one commit, then one commit that edits only
`tools/round-47/exact.py` and refreshes `interpreter_sha256`, which a landing legitimately does):

```python
def _m_substring_arm(block, spec):
    return block, {}          # was: rewrite every arm cell to "order-ish"
```

Names untouched ⇒ `MUTATIONS` name list untouched ⇒ `mutations_sha256` unchanged.
`exact.py:368-371` sees `text == block and not overrides`, records
`{"error": "mutation was a no-op"}`, **counts it as `v2_green += 1`** and continues:

| fixture | what changed in `exact.py` | `mutations_sha256` | counter exit | battery |
|---|---|---|---|---|
| `fx-genuine` | nothing | `19a2166e…` | **0** | 4 / 4 / 0 / 1 / 0, no `error` entry |
| `fx-a1a` | `_m_substring_arm` → no-op | `19a2166e…` | **0** | 4 / 4 / 0 / 1 / 0, `substring-arm` = `mutation was a no-op` |
| `fx-a1b` | **all four** mutators → no-op | `19a2166e…` | **0** | 4 / 4 / 0 / 1 / 0, four `mutation was a no-op` |
| `fx-a1c` | staleness forgery weakened `MUTATIONS[:3]` → `[:2]` | `19a2166e…` | **0** | 4 / 4 / 0 / 1 / 0 |
| `fx-a1d` | `_m_substring_arm` rewritten to zero the block's `interpreter_sha256` instead of the arm cells | `19a2166e…` | **0** | 4 / 4 / 0 / 1 / 0 |

`fx-a1b` is the decisive one: a counter whose four forgeries all do nothing satisfies clause 9
exactly, and `mutations_sha256` — the clause that exists because "deleting a mutation changes
the denominator" (R46-CL4) — does not move.

`fx-a1d` shows the no-op guard alone is not enough: the mutator is *not* inert, it is
re-pointed. `v2` has no interpreter-pin clause, so `v2_exit 0`; `v3` fails with
`interpreter sha256 pin does not match the bytes at rev` — a real `v3` kill, but of a defect the
row calls `symbol`. Clause 9 counts `v2_exit 0 -> v2_green` and `v3_exit 1 -> not v3_green`
without ever reading *which* clause fired, so the `symbol` row's forgery can measure the
interpreter pin and still count.

Command (every fixture; full receipts in `receipts/*.meta`, `receipts/*.json`):

```sh
cd /fast/scratch/hyaku/kaidoku-r47/CritDigest/fx-a1b
python3 -I -B tools/round-47/exact.py --root "$PWD" --freeze "$(git rev-parse HEAD)" \
  --rev "$(git rev-parse HEAD)" --json-out .ufo/waves/round-47/w1/CritDigest/fx-a1b.recheck.json
# exit 0, utc 2026-10-28T17:58:48Z, stdout sha256 a34d3e70cb65811d48b3081228eaba01309c3c13244f0ac87f9998640a1b2e77
```

## Counterexample 2 — name edit changes the digest, behaviour identical, counter green

Fixture `fx-a2b`: rename the string `"stale-mutations-digest"` → `"stale-digest-pin"` in
`MUTATIONS`, rename the same token in block 24's prose (clause 6 requires each name to appear in
the block), re-paste both pins. No function body changes; `_m_stale_digest` still raises nothing,
still forges a wrong digest, still fails the same clause.

| | names digest | mutator-body digest | counter exit | battery |
|---|---|---|---|---|
| `fx-genuine` | `19a2166e…` | `65357c12…` | 0 | 4 / 4 / 0 / 1 / 0 |
| `fx-a2b` (rename only) | `5190d1f7…` | `65357c12…` (**unchanged**) | 0 | 4 / 4 / 0 / 1 / 0, identical `v3_failing` strings |

So the pin churns on a label and does not churn on a neutering. That is the exact inversion of
what clause 6 claims to buy ("a deleted mutation changes the printed digest").

## What the clause should have hashed

Not the names. Hash the **mutation apparatus**, i.e. what actually decides the battery:

```python
MUT_DIGEST = hashlib.sha256("\n\n".join(
    [inspect.getsource(fn).strip() for _, fn in MUTATIONS] +
    [inspect.getsource(h).strip() for h in (rewrite_rows, _table_span, table, _cells, _rows)] +
    [repr(x) for x in (ORDER, REVERSED, GATE46, MARKER, HEADER, VOCAB, ROUTED,
                       MUT_PIN.pattern, SELF_PIN.pattern)]).encode()).hexdigest()
```

Measured separation of that preimage (labels excluded) over the same six fixtures — the body
column in the table above: unchanged by the rename (`65357c12` in both `fx-genuine` and
`fx-a2b`), changed by every one of the four behavioural rewrites
(`fx-a1a 4deb48c3`, `fx-a1b e1e41e4e`, `fx-a1c c5a1932b`, `fx-a1d 8ed62973`).

One honest caveat the L1 should carry into block 24's wording: `_m_stale_digest`
(`exact.py:80`) computes its forged value from `MUTATIONS[:3]`, so the *labels* are part of that
one mutator's behaviour. A labels-free preimage is only fully rename-invariant if the staleness
forgery derives its bogus value from something that is not the label list (e.g. a literal
64-hex constant, or the real digest with one byte flipped). My `fx-a2b` measurement shows the
coupling: the *verdict* is identical, but the bytes the forgery writes differ, which is why an
effects-based digest also moves on a rename. Hash sources, and keep the staleness forgery
label-free.

And for the battery: a per-mutation expected clause belongs in the same preimage, so that
re-pointing `substring-arm` at the interpreter pin changes the pin:

```python
EXPECTED = {"substring-arm": "arm cells not exact vocabulary tokens",
            "duplicate-routed-id": "routed cardinality",
            "stale-mutations-digest": "mutations_sha256 does not match",
            "flag-order-drift": "gate.py flag order"}
```

## Smallest safe correction (two lines of clause, no new clause, no frozen byte edited here)

1. `exact.py:96` — replace the name-only preimage with the source/constant preimage above, and
   require `battery.noop == 0` and `v3_failing` to contain `EXPECTED[name]` for each mutation.
   This alone kills `fx-a1a`, `fx-a1b`, `fx-a1c`, `fx-a1d`, because the pinned value moves when
   a body moves, even after the landing author re-pastes `interpreter_sha256`.
2. `exact.py:290` — add `("noop", 0)` to the clause-9 key tuple, and make `exact.py:368-371`
   count the no-op into `out["noop"]` instead of `v2_green`. Today an inert forgery is *rewarded*
   as a green v2 hole; that is the single reason a battery that measures nothing scores 4/4/0.

Because clause 6's target is `failing == []`, both edits must land together: (1) makes the pin
mean something, (2) makes the count mean something. Neither needs a new clause, a new file, or a
change to clause 9's thresholds — the counts are already computed correctly, they are just
computable by an inert list.

## Collateral for the L1 (outside this seat's verdict, inside its evidence)

- **The declared freeze is stale.** `--freeze 62e33f7d` (the A2 freeze) against HEAD exits **2**
  `frozen_path_changed: [tools/round-47/, tools/round-47/record.py]`
  (`receipts/freeze-probe.meta`, utc 2026-10-28T17:59:12Z, stdout sha256 `da9a2c5e…`), and
  `git diff --stat 62e33f7d..HEAD -- tools/round-47/` = `record.py 21 insertions(+), 4 deletions(-)`.
  `2e4ae43` (A3) and `1e2c3102` (A4) touch `tools/round-47/` and are **not disclosed** in
  `plans/round-47-claims.md`, which discloses A1 and A2 and states "Nothing in this file or in
  `tools/round-47/` changes after the freeze" and "a change makes both counters exit 2
  `frozen_path_changed`". Two of my six fixtures exit 0 *only because* the claims-file sentence
  "the four forgeries mutate the landed block … one defect class at a time" is prose that
  nothing checks. Measure at the commit that actually carries HEAD's frozen bytes (the directory
  pathspec gives `1e2c3102`) and disclose A3/A4 in the round report; the claims bytes themselves
  are frozen and must not be edited to say so.
- **`gate.py` `restored` false positive on a directory entry.** `tools/round-46/gate.py:172`
  computes `restored` as `touched` minus `changed` normalised with `rstrip("/")`; when
  `frozen_derived` holds a directory (`tools/round-47/`), `changed` carries the directory while
  `touched` carries the file, so `tools/round-47/record.py` is reported `restored` although
  `git diff --quiet 62e33f7d..HEAD -- tools/round-47/record.py` exits 1 (DIFFERS). The verdict
  (exit 2) is right; only the message is wrong. Do not read `restored` as "tamper-then-restore"
  when the frozen set names a directory. Frozen infrastructure — report, do not fix.

## Not run

- C2 (`tools/round-47/record.py`) — another seat owns it; I only ran `exact.py`.
- No counter run against the real lane *with* the battery at HEAD (only the `--no-battery` freeze
  probe): the battery builds fixture repos under `gate.scratch`, and the six copies here already
  carry HEAD's bytes committed. The genuine run at HEAD's bytes is `fx-genuine` (exit 0).
- No install of any tool; `python3` 3.13 and `git` only.
