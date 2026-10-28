# C1Digest — block 24 rows governed by R47-C1 clause 6

Clause 6 is the `mutations_sha256` pin plus the four-mutation-name statement. Everything below
was measured, not copied: each value carries the command that produced it and the receipt that
holds its stdout (`.ufo/waves/round-47/w1/C1Digest/receipts/`).

Measured revision `REV = 2e4ae43463aabdae707f8c8a4daa41441ad67a71` (round-47 A3).
Block 24 as landed at `REV`: `sha256 692b6d6847b88e17aee75fe280d2fb8d61261f797bd11ad9953e9c58b58f0292`,
2129 bytes. Counter at `REV` with `--freeze REV`: **exit 0, `failing []`, battery green**
(`receipts/e4-lane-self-freeze.out`, stdout sha256 `43cc50b19a3aea0e7e9d48f7a2e62c9ec4851948922b4b5e184630708a8481d4`).

## 1. The clause and the code it names

`plans/round-47-claims.md:99-100` at `REV` (78-79 at the freeze — see §5):

> 6. `mutations_sha256` equals sha256 over `"\n".join(name for name, _ in MUTATIONS)` of the
>    counter's own mutation list, and the block names all four mutation names.

`tools/round-47/exact.py:92-96` at `REV` (the denominator):

```
MUTATIONS = [("substring-arm", _m_substring_arm),
             ("duplicate-routed-id", _m_duplicate_id),
             ("stale-mutations-digest", _m_stale_digest),
             ("flag-order-drift", _m_flag_order)]
MUT_DIGEST = hashlib.sha256("\n".join(n for n, _ in MUTATIONS).encode()).hexdigest()
```

`tools/round-47/exact.py:246-255` at `REV` (the check; the pin regex is line 41,
`MUT_PIN = re.compile(r"mutations_sha256:([0-9a-f]{64})")`):

```
    if hard:
        m = MUT_PIN.search(block)
        receipt["mutations_sha256"] = m.group(1) if m else None
        receipt["mutations_sha256_expected"] = MUT_DIGEST
        if not m or m.group(1) != MUT_DIGEST:
            failing.append("mutations_sha256 does not match the counter's own mutation list")
        names = [n for n, _ in MUTATIONS]
        unnamed = [n for n in names if n not in block]
        if unnamed:
            failing.append(f"mutation names not stated in the block: {unnamed}")
```

## 2. Values, each with its own derivation

| value | what it is | how it was derived (run in the lane root, read-only) |
|---|---|---|
| `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` | the `mutations_sha256` pin | `git show 2e4ae43:tools/round-47/exact.py` → `MUTATIONS` parsed twice, once with `ast` and once with `re`, both giving `["substring-arm","duplicate-routed-id","stale-mutations-digest","flag-order-drift"]` → `hashlib.sha256("\n".join(names).encode()).hexdigest()`; equals the module's own `MUT_DIGEST` |
| `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | the `interpreter_sha256` pin | `git show 2e4ae43:tools/round-47/exact.py \| sha256sum` (identical to the freeze blob's) |
| `b7d3e477e2f6bf3d7967a55c17dfe2d5d314c968b61e88ac4ea75e41251ac61a` | digest over the first **three** names — the stale pin the battery plants | `sha256("\n".join(names[:3]))`; it is exactly what `_m_stale_digest` substitutes (`exact.py:80-84`) |
| `bd0aaf6e051a8ee7f58492fa8ee49ca062fb8ad3335becfe6f84ceee01425fc6` | digest over the **sorted** names | `sha256("\n".join(sorted(names)))` — red, so "in order" is enforced |
| `39af8d103e715b3ba9d853e99d749a68d3e03c47b2cb0135d6e9fef6850de1c6` | digest with a **trailing newline** | `sha256("\n".join(names) + "\n")` — red, so the join is exactly `"\n".join` with no terminator |

One-line re-derivation:

```sh
python3 -c 'import hashlib;n=["substring-arm","duplicate-routed-id","stale-mutations-digest","flag-order-drift"];print(hashlib.sha256("\n".join(n).encode()).hexdigest())'
# -> 19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112
```

## 3. Paste-ready: the pin sentence (block intro, all of clause 6 lives here)

Verbatim from the landed block at `REV`, unchanged and correct:

```
Interpreter pin: `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the counter's own mutation list is pinned as `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`. Source S143.
```

Two constraints this sentence must keep, both measured:

- Both pins sit inside the **marked block** (the counter searches `marked[0]` only, `exact.py:247`).
  A pin written in block 23 or anywhere else does not count.
- The four names must appear as **substrings of the block text** (`exact.py:252-255`) — not
  necessarily in a `mutations` sentence, not necessarily in an order, and not necessarily true
  (see §6, K7).

## 4. Paste-ready: the row clause 6 governs — R46-CL4 (`digest`)

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | `forgeries_total` is compared with a number the code computes, and nothing pins the list | `digest` | 1 |

The arm cell is **only the token**. Clause 5 compares `cell.strip("\` ")` for equality
(`exact.py:235-239`), so `digest: the block pins sha256 over …` — the form block 24 carried in
commit `e856beb5` — fails clause 5 while satisfying clause 6 (`receipts/e2-pre-A2-rows.out`,
exit 1, single failing entry: `arm cells not exact vocabulary tokens`). The mechanism belongs in
the v2-hole cell (as above) or in an `Arms:` paragraph under the table.

The other three rows, in the same bare-token form (whole block also archived as
`receipts/variant-blocks/landed-at-2e4ae43.md`):

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | containment over a lowercased cell, so any superstring passes | `symbol` | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the id check asks whether the id appears in *some* row | `once` | 1 |
| R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice and blinds the arm | the argument order is a convention no clause reads | `order` | 1 |

Optional explanatory paragraph, measured green as
`receipts/variant-blocks/candidate-arms-paragraph.md` (`sha256 7e4ba9033b764128ac9d1804976adf6faa0e2c77f5631d45c6d4e0bd30041e7e`,
`receipts/raw/P1-candidate.out`, exit 0, battery 4/4/0/1/0). It restores what the bare token
stops saying, without touching an arm cell:

```
  Arms: `symbol` — the cell, stripped of backticks and spaces, must equal one token of `symbol`, `once`, `digest`, `order`, so `order-ish` and `blobberish` fail where the v2 substring test passed. `once` — every row names exactly one routed id and the multiset over the four rows is exactly R46-CL2, R46-CL3, R46-CL4 and R46-CL6, each once, so a duplicate claim and a five-row table both fail. `digest` — the block pins sha256 over the counter's own mutation names joined by a newline in list order and names all four, so a mutation added, dropped or reordered elsewhere breaks the pin; the digest over the first three names alone is `b7d3e477e2f6bf3d7967a55c17dfe2d5d314c968b61e88ac4ea75e41251ac61a`, which is the stale pin the battery plants. `order` — the round-46 gate's history arm must contain the literal `"-m", "--diff-merges=first-parent"` exactly once and the reversed pair zero times, so one argument reorder fails the block.
```

Note the paragraph carries no path token: `tools/round-46/gate.py` is **outside** the citation
allowlist (`exact.py:36`, `ALLOW`), so the arm's own subject can only be named as "the round-46
gate's history arm". A block that writes that path fails clause 8 with
`outside the validated path set`.

## 5. Citation line selectors actually used, and their drift

At `REV` the block's citations resolve (`refs 8`, no `unresolved_citations`, `e4` receipt):

| selector | resolves in | line count at `REV` |
|---|---|---|
| `corpus/lessons/round-46.md:57-66` | R46-CL2/CL3/CL4/CL6 | 102 |
| `corpus/lessons/round-46.md:21` | M46-2, the un-pinned denominator | 102 |
| `corpus/lessons/round-46.md:89-95` | R46-CL7, digits vs meanings | 102 |
| `plans/round-47-claims.md:45-113` | causal separability → clause 6 of the C1 predicate | 211 |
| `plans/round-47-claims.md:141-176` | R47-C2 prior state → its clause 6 | 211 |

Clause 6 itself moved from `plans/round-47-claims.md:78-79` at the freeze (190 lines) to
`:99-100` at `REV` (211 lines): amendments A1-A3 insert prose above it. The block's
`plans/round-47-claims.md:45-113` still contains the predicate, but only because the range is
wide. See §6, K8: the counter scores **resolution**, not address correspondence, so a selector
can slide off its subject and stay green.

## 6. What clause 6 does *not* bind (each measured)

| probe | change to the landed block | counter | receipt |
|---|---|---|---|
| K1 | `mutations_sha256` := digest over the first three names | exit 1, **exactly** `mutations_sha256 does not match the counter's own mutation list` | `receipts/raw/K1-digest-first3.out` |
| K2 | pin := digest over the sorted names | exit 1, same single entry | `receipts/raw/K2-digest-sorted.out` |
| K3 | pin := digest with a trailing newline | exit 1, same single entry | `receipts/raw/K3-digest-trailing-nl.out` |
| K4 | the four names removed from the intro | exit 1, **exactly** `mutation names not stated in the block: [all four]` | `receipts/raw/K4-names-removed.out` |
| K5 | K1 + K4 together | exit 1, those two entries and nothing else | `receipts/raw/K5-both-broken.out` |
| **K6** | a second, **stale** `mutations_sha256:b7d3e477…` added under the table | **exit 0** — `MUT_PIN.search` reads the first pin only | `receipts/raw/K6-second-stale-pin.out` |
| **K7** | names kept, but the sentence now says the battery scores only `flag-order-drift` and the other three "are named here as unscored" | **exit 0** — the check is `n in block`, so a block may deny the binding it satisfies | `receipts/raw/K7-names-denied.out` |
| **K8** | `plans/round-47-claims.md:45-113` → `:45-50`, label unchanged | **exit 0** — resolution-only (clause 8) | `receipts/raw/K8-citation-wrong-content.out` |
| **N1** | one `MUTATIONS` entry replaced by a no-op mutator (in-process monkeypatch, not a block edit) | **exit 0** with `forgeries_total 4, v2_green 4, v3_green 0, crash 0` while the fixture entry reads `mutation was a no-op` | `receipts/noop-mutator.json` |

Reading of N1: clause 6 pins the *names* of the denominator, not the mutation functions
(`MUT_DIGEST` is built from `n for n, _ in MUTATIONS`, `exact.py:96`). A dead mutator is counted
as a green v2 forgery (`exact.py:351-357`) and clause 9 still passes. The guards that remain are
the `interpreter_sha256` pin (clause 8, self-referential at `--rev`) and the freeze arm: a change
to `tools/round-47/` after the freeze makes both counters exit 2 `frozen_path_changed`
(`gate.py:192-194`), and a *dirty* worktree copy exits 2 `frozen_worktree_dirty`
(`gate.py:187-191`) — which is what keeps "the executing list" and "the committed bytes" equal.

Bottom line: clause 6 is satisfied by the block at `REV` and it does fail for every digest or
name it computes (`K1`-`K5`), but it is a **pin, not a proof**: `K6`, `K7` and `N1` are three
distinct forgeries that leave it green.
