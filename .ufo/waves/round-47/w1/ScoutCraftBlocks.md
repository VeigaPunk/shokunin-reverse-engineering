# ScoutCraftBlocks — craft rule blocks at the round-47 freeze

Subject: `SKILL.md` at `5017e1f7299c3a812e87e7950148f54313dd279e` only.
Git blob `173d93bbd281577488f17ec45311e3c23f3561e7`. sha256 `9bb902a1a1c9f20a31620f4bf8259433ec1fdd4f88ba211394ff9ea44b586f5c` (299931 bytes).
`## Queue-drain craft ` occurs once, at line 81:
`## Queue-drain craft (rounds 5-12, distilled in round 13)`.
The prefix has its trailing space (`tools/round-47/exact.py` blob `fb21a16686633fc3b2d0f6d82910bf9e5eb8b0ac`, lines 30 and 101–106). A missing trailing space would be exit 2, not a block count.
No install. Resolver is the seat script, not an import of `exact.py`.

## Where `## Config custody` begins

Line **632**, the only such heading in the freeze blob:

`## Config custody for live-probe rounds (SOP)`

That heading is the craft-section terminator. `craft_section` keeps the text before `\n## ` and drops everything after it (`exact.py:106`). The craft body is therefore lines 82–631. The next `- **` bullets in the file are the SOP list, not craft blocks:

| line | opener (freeze `git grep`) |
|---|---|
| 641 | Freeze the pre-pair before the round's first probe |
| 656 | Why the shell files are in scope |
| 668 | Read-only, always — the pair never edits a config |
| 673 | Take the post-pair after the last leg exits and every session is |
| 681 | `` `tail -n3` is not a config selector on a five-hash receipt `` |
| 687 | Compare same-round only |
| 694 | Drift disposes the claim, not the config |
| 701 | Commit both receipts tracked |

Zero indented `^- \*\*` items inside the craft section. The intro paragraph before the first bullet has no marker and no path citation.

## What a craft block is

Same split the counter uses (`exact.py:109-110`):

```text
re.split(r"(?m)^- \*\*", craft_section(skill))[1:]
```

23 blocks. `<!-- exactness-table v3 -->` occurs **0** times (`git grep -F` exit 1). No block is block 24. Ordinals 1–21 have no `N. ` title prefix. Only ordinal 22 and 23 do, and those prefixes match the ordinal.

## Resolver (written for this seat)

A citation is a path token with an optional `:N` or `:N-M` selector (hyphen, en dash, or em dash). Prefixes: `corpus/`, `plans/`, `tools/`, `.ufo/`, or a root file `SCORECARD.md` / `LOG.md` / `PROVINCE.md` / `SKILL.md`. A trailing sentence dot is stripped.

It resolves at the freeze when `git cat-file -t REV:path` is `blob` or `tree`, and, if a selector is present, the object is a blob and `1 <= start <= end <= len(splitlines())`. No selector does not fail existence; it is reported bare. A block with zero citations would be `vacuous`. None are.

This is not command A. Command A, copied from `record.py` `depth_pair` and checked with `git show` (what `gate.show` returns), sees only `corpus|plans|tools` paths, defaults a missing selector to line 1, and treats a block as resolved only when it has at least one such path and every one fits. Paths outside that prefix are invisible to it.

"Resolves" here means the path exists and a present selector lands inside the blob. It does not mean the cited lines say what the prose claims.

## Every block

| # | line | titled | marker | cites | bare | trees | every citation resolves | command A |
|---|---:|---:|---|---:|---:|---:|---|---|
| 1 | 86 | — | none | 10 | 0 | 0 | yes | yes (10) |
| 2 | 108 | — | none | 4 | 0 | 0 | yes | yes (4) |
| 3 | 118 | — | none | 8 | 0 | 0 | yes | yes (8) |
| 4 | 137 | — | none | 5 | 0 | 0 | yes | yes (5) |
| 5 | 151 | — | none | 4 | 0 | 0 | yes | yes (4) |
| 6 | 162 | — | none | 2 | 0 | 0 | yes | yes (2) |
| 7 | 170 | — | none | 1 | 0 | 0 | yes | yes (1) |
| 8 | 175 | — | none | 6 | 0 | 0 | yes | yes (6) |
| 9 | 187 | — | none | 3 | 0 | 0 | yes | yes (3) |
| 10 | 196 | — | none | 4 | 1 | 0 | yes | yes (1) |
| 11 | 207 | — | none | 3 | 0 | 0 | yes | yes (1) |
| 12 | 219 | — | none | 2 | 0 | 0 | yes | yes (2) |
| 13 | 233 | — | none | 2 | 0 | 0 | yes | yes (2) |
| 14 | 240 | — | none | 5 | 1 | 0 | yes | yes (1) |
| 15 | 256 | — | none | 9 | 0 | 0 | yes | yes (9) |
| 16 | 279 | — | none | 5 | 0 | 0 | yes | yes (3) |
| 17 | 293 | — | none | 8 | 1 | 0 | yes | yes (6) |
| 18 | 316 | — | `<!-- sqfs-triage-table v1 -->` | 5 | 1 | 0 | yes | yes (5) |
| 19 | 351 | — | `<!-- sqfs-triage-table v2 -->` plus an actions comment | 6 | 1 | 0 | yes | yes (6) |
| 20 | 387 | — | `<!-- sqfs-triage-table v3 -->` plus an actions comment | 3 | 2 | 0 | yes | yes (1) |
| 21 | 457 | — | `<!-- sqfs-triage-table v4 -->` plus an actions comment | 9 | 8 | 0 | yes | yes (1) |
| 22 | 547 | 22 | `<!-- freeze-integrity-table v1 -->` | 11 | 2 | 2 | yes | yes (11) |
| 23 | 612 | 23 | `<!-- freeze-integrity-table v2 -->` | 11 | 3 | 0 | yes | yes (9) |

Titles:

1. Evidence ids are content-addressed per verb family — never substitute ids across invocation shapes.
2. Raw file vaddrs must be pre-shifted +0x100000 into Ghidra space for every native verb on ELF PIE/DYN.
3. Refusal families and cost classes.
4. Four authority grades — cite a conclusion at the grade its envelope declares.
5. Input contracts are shape-gated.
6. Module attribution is caller-attested, not proven.
7. Tool acceptance ≠ correctness.
8. Census rows can be defects — check holdings before exercising.
9. Provisioning hints can be wrong — verify the gate, not the hint.
10. Citations into an operator-mutable file anchor by stanza key + receipt, never by bare line number.
11. Config custody is a pre/post-pair — a zero-drift claim without its own pre-pair is void.
12. Long Ghidra analyze runs are transient user services, not scoped processes.
13. A mitigation claim carries its natural control: same target, caps, and deadline; only the treatment is absent.
14. An artifact that records its own byte-identity must re-derive that identity after every revision; a stale self-identity voids the verification block, not the work.
15. A parsed-and-empty result is a statement about the parser's scope, never proof of byte absence — settle byte questions with a census (decode, locate, hash), not with the probe's function count.
16. Co-land every truth dependency.
17. Evidence-id field sensitivity is projection-local — measure it per operation, never infer it from the `ev_` prefix.
18. SquashFS `extract-firmware` outcome triage (round 39).
19. SquashFS `extract-firmware` outcome triage v2 (round 40).
20. SquashFS `extract-firmware` outcome triage v3 (round 41).
21. SquashFS `extract-firmware` outcome triage v4 (round 42).
22. 22. Freeze integrity is an instrument, and every arm has a red case.
23. 23. Freeze-integrity evidence is only evidence when its own forgeries fail.

126 citations. 104 carry a selector and sit inside the blob (`in_range`). 20 are blobs with no selector. 2 are trees with no selector. Zero absent paths. Zero selectors outside the file. No non-hyphen range separator turned up. Scout 23/23. Command A 23/23 (101 `HARD_REF`s; the other 25 citations are `.ufo/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, or `PROVINCE.md`, which command A does not see). That 23/23 is the same shape as the claims file's "observable 23/23", and it is not evidence those 25 outside paths were checked by command A.

Bare and tree citations (still exist at the freeze; not line-addressed):

| block | citation | kind | lines at freeze |
|---|---|---|---:|
| 10 | `.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt` | blob, no selector | 6 |
| 14 | `SCORECARD.md` | blob, no selector | 3661 |
| 17 | `.ufo/waves/arc3-loop1-round12/claims/c2/EX-16.md` | blob, no selector | 34 |
| 18 | `tools/round-39/sqfs-triage.py` | blob, no selector | 1134 |
| 19 | `tools/round-40/sqfs-triage-v2.py` | blob, no selector | 1533 |
| 20 | `SKILL.md` | blob, no selector | 1737 |
| 20 | `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` | blob, no selector | 3261 |
| 21 | `SKILL.md` | blob, no selector | 1737 |
| 21 | `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` | blob, no selector | 5623 |
| 21 | `.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/trx-img-with.json` | blob, no selector | 1 |
| 21 | `.ufo/waves/round-42/w1/artifacts/R42C2TableDraft/measurements.md` | blob, no selector (four times) | 289 |
| 21 | `.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/x86-fs-with.json` | blob, no selector | 1 |
| 22 | `tools/round-45/frozen-path-preflight.py` | blob, no selector | 315 |
| 22 | `plans/round-45-claims.md` | blob, no selector | 175 |
| 22 | `tools/round-45/` | **tree**, twice | `git show` listing is 6 lines, exit 0 |
| 23 | `tools/round-46/attest.py` | blob, no selector | 669 |
| 23 | `SKILL.md` | blob, no selector (twice) | 1737 |

The two `tools/round-45/` hits are real directory citations (`--pathspec tools/round-45/` and "the whole `tools/round-45/` directory"), not a truncated file path. `git cat-file -t` is `tree`. `git show REV:tools/round-45/` exits 0 and prints a six-line listing (`c1-counter.py`, `c2-counter.py`, `frozen-path-preflight.py`, `registry-scope.json`, plus the `tree …` header and a blank line). Command A then defaults the missing selector to line 1, and line 1 falls inside that listing, so the block counts as resolved. That pass is a listing accident, not a file:line check. A scout that required a blob would call those two unresolved. This seat's stated rule calls them resolved as directories and flags them.

`exact.py` v3 `check_refs` is a different bar (line selector required, allowlist `corpus/lessons|knowledge`, `plans/`, `tools/round-47/` only) and it scores only the marked block. It does not apply to these 23 blocks at the freeze, because the marker is absent. Do not read "resolves" in this table as "would pass clause 8".

Full per-citation rows: `ScoutCraftBlocks/stdout2.txt` lines 81–206.

## What would break block 24's `block_is_last`

Source, freeze blob of `exact.py`, lines 191–195: `block_is_last` is `blocks[-1] is block`, where `block` is the single craft block that contains `<!-- exactness-table v3 -->`. Failure text: `marker block is not the last craft block`. The title check `block.startswith("24. ")` is a separate clause (line 196) and is not `block_is_last`.

At the freeze the marker is absent, so the clause is not yet true or false of a landed block. Position:

- The last craft block is ordinal 23 at line 612. Nothing in the craft section follows it.
- In-memory append of a fake `- **24. … <!-- exactness-table v3 -->` immediately before the line-632 heading: `rule_blocks` 24, marker ordinal 24, `block_is_last` true, followers `[]`.
- In-memory insert of that same fake block immediately before ordinal 23: `block_is_last` false. The only follower is ordinal 23, title `23. Freeze-integrity evidence is only evidence when its own forgeries fail.`
- Inserting the marker block before ordinal *k* leaves ordinals *k* through 23 as the breakers. Appending it after ordinal 23 leaves none.
- The eight SOP bullets at lines 641–701 are outside `craft_section`. They do not break `block_is_last` no matter where block 24 sits inside the craft section.

So: **no existing craft block breaks the clause if block 24 is the last `^- \*\*` before line 632.** **Ordinal 23 is the block that breaks it if 24 is inserted before 23** (the placement a "before the last block" edit would make). Ordinals 1–22 break it only if the marker block is placed before them.

Not a freeze fact, recorded so it is not confused with one: at 2026-10-28T17:56:55Z the worktree `SKILL.md` (toplevel checked, `git show` of the freeze blob exit 0) had 24 craft blocks, and worktree block 23 was the freeze block-23 text plus one trailing newline (`work_is_freeze_plus_newline True`, lengths 4341 vs 4340). That newline is the split artifact of a following `- **` versus a following `\n## `, not an edit of the rule. The enumerate run at 17:55:43Z saw a clean `SKILL.md` status and `diff --stat REV HEAD -- SKILL.md` of 13 insertions, with worktree block 24 last, carrying the v3 marker, and Config custody shifted to line 643. HEAD moved during this scout (`2e4ae434…` at 17:53:04Z, `1e2c3102…` at 17:54:28Z), so that worktree shape is not the freeze and is not pinned to a single HEAD here.

## Measurements

Ledger, commands, exits, and stdout hashes: `.ufo/waves/round-47/w1/ScoutCraftBlocks/report.md`. Canonical run is M5.
