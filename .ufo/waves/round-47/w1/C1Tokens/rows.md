# C1Tokens — block-24 table rows governed by R47-C1 clause 5

Seat `C1Tokens`, round 47 wave 1. Frozen surface `plans/round-47-claims.md@5017e1f7299c3a812e87e7950148f54313dd279e` — clause 5 at `plans/round-47-claims.md:76-77` — and `tools/round-47/exact.py@5017e1f7299c3a812e87e7950148f54313dd279e`.

Clause 5 is computed by `tools/round-47/exact.py:235-243`:

```python
arm = [r[2].strip("` ") if len(r) > 2 else "" for r in rows]
receipt["arm_tokens"] = arm
if hard:
    if any(a not in VOCAB for a in arm):
        failing.append(f"arm cells not exact vocabulary tokens: {arm}")
else:
    if any(not any(t in a.lower() for t in VOCAB) for a in arm):
        failing.append("arm cells outside the vocabulary")
```

`VOCAB = ("symbol", "once", "digest", "order")` (`tools/round-47/exact.py:35`). `hard` is `profile == "v3"`. The v3 test is tuple membership of the whole stripped cell, so it is an equality on that cell and never a containment test on a substring.

## The rows this seat drafts (v3-arm cells)

| routed id | v3 arm cell (paste verbatim) | why that token is the binding |
| --- | --- | --- |
| R46-CL2 | `symbol` | the cell is stripped and then compared for equality, so `blobberish`, `order-ish`, `symbolmap` and `the symbol arm` all fail under v3 while the v2 profile passes them |
| R46-CL3 | `once` | one routed id per trigger cell, each of the four exactly once — the arm token names that cardinality binding |
| R46-CL4 | `digest` | `mutations_sha256` pins the counter's own list in order, so a deleted mutation moves the digest instead of shrinking the denominator |
| R46-CL6 | `order` | the flag-order clause over the round-46 history arm: the literal pair once, the reversed pair zero times |

These four cells are the ones clause 5 governs. They are the only cells of the block clause 5 reads (`r[2]`, the third column). Everything else in the block below is drafted to the other clauses and verified together with these.

## Ready-to-paste block 24

Insert as the **last** craft block: immediately after block 23 (`SKILL.md:612-631`) and before the `## Config custody for live-probe rounds (SOP)` heading (`SKILL.md:632`). Canonical bytes = the fenced text below plus exactly one trailing newline, **1916 bytes**, sha256 `a57ce1214f830ca62fe7ef52e3b4d9403814a6e616ad5e9e39b9408f22e0694b`.

```markdown
- **24. An exact binding is an equality, not a containment.** <!-- exactness-table v3 --> Block 23 stated the arms; this block states the four ways its own clause text was satisfiable without the property it named, one row per defect the round-46 spot-check routed (`corpus/lessons/round-46.md:51-69`). Each v3-arm cell is a binding, not a vocabulary hit: the cell is stripped of backticks and spaces and then compared for equality, so `order-ish` fails `order` and `blobberish` fails `symbol` (`plans/round-47-claims.md:76-77`). The interpreter is pinned twice — by its own bytes and by a digest over its mutation list in the counter's order (substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift) — so deleting a mutation moves the printed digest instead of shrinking the denominator the claim is judged on. `tools/round-47/exact.py` interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112.

  | trigger | v2 hole | v3 arm | exit |
  | --- | --- | --- | --- |
  | R46-CL2 — a cell passes because some vocabulary token is a substring of it | the arm check is `token in cell.lower()`, so `blobberish` scores where `symbol` was meant (`corpus/lessons/round-46.md:57-59`) | symbol | 1 |
  | R46-CL3 — an id is satisfied by appearing in some row, not in its own row | the routed-id check asks at-least-once, so a row may claim a group it does not address (`corpus/lessons/round-46.md:60-62`) | once | 1 |
  | R46-CL4 — the mutation list carries no digest | `forgeries_total` is checked while a deletion silently changes the denominator (`corpus/lessons/round-46.md:63-64`) | digest | 1 |
  | R46-CL6 — the history arm's flag order is unenforced | `-m` after `--diff-merges=first-parent` prints a merge twice and restores the blindness (`corpus/lessons/round-46.md:65-69`) | order | 1 |
```

Verified twice on one-commit fixtures whose `SKILL.md` is the freeze's `SKILL.md` with exactly these bytes inserted at that point: `receipt-cli-full.json` (the block before this file existed) and `receipt-cli-rows.json` (the counter executed on the fenced bytes of this file, fixture rev `ea3cf1f03bd6b0b991a4918576044f751bfc456d`) — both exit 0, `failing: []`, battery `4/4/0/1/0`.

## Citation selectors, measured at 5017e1f7299c3a812e87e7950148f54313dd279e

| citation as pasted | selector | resolves at rev | file sha256 at freeze | lines |
| --- | --- | --- | --- | --- |
| `corpus/lessons/round-46.md:51-69` | `51-69` | yes | `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc` | 102 |
| `corpus/lessons/round-46.md:57-59` | `57-59` | yes | `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc` | 102 |
| `corpus/lessons/round-46.md:60-62` | `60-62` | yes | `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc` | 102 |
| `corpus/lessons/round-46.md:63-64` | `63-64` | yes | `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc` | 102 |
| `corpus/lessons/round-46.md:65-69` | `65-69` | yes | `0da8a24c02f828495035ddf7e3481ef1d4c39485a422be9d9818f27fa6ff0bdc` | 102 |
| `plans/round-47-claims.md:76-77` | `76-77` | yes | `c8615eb811f598a35cad514523225e320185ec3c6481035fc95f844071e41f67` | 190 |
| `tools/round-47/exact.py` — none: SELF is exempt from the selector rule (tools/round-47/exact.py:149-150) | `none: SELF is exempt from the selector rule (tools/round-47/exact.py:149-150)` | exempt | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | 561 |

`tools/round-46/gate.py` (sha256 `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c`, 247 lines) is read by clause 7 and is **never named in the block**: `tools/round-46/` lies outside `ALLOW` (`tools/round-47/exact.py:36`), so one path token naming it would fail clause 8 with `outside the validated path set`. The block says "the history arm's flag order" in prose and lets the counter read that file itself.

Every other mention of a cited path in the block carries its selector; a bare `corpus/lessons/round-46.md` in the prose would fail clause 8 with `no line selector` under v3 (`tools/round-47/exact.py:151-153`).

## sha256 values the block must carry

| pin | value | derivation |
| --- | --- | --- |
| `mutations_sha256` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` | sha256 over `"\n".join(name for name, _ in MUTATIONS)`, counter order |
| `interpreter_sha256` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | sha256 of `tools/round-47/exact.py` bytes at 5017e1f7299c |
| block sha256 | `a57ce1214f830ca62fe7ef52e3b4d9403814a6e616ad5e9e39b9408f22e0694b` | the fenced text plus one newline (1916 bytes) |

The block states all four mutation names because clause 6 requires them named (`tools/round-47/exact.py:252-255`); the digest alone is not enough.

