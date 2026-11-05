# ReviewerC2 — R89-C2 attack report (round 89, kaidoku)

Seat: reviewer, attack surface: craft rule block 29 + `tools/round-89/depth-blocks-v2.py`.
Scratch `/fast/scratch/hyaku/kaidoku-r89/ReviewerC2/` deleted before yield; all receipts live in
`.ufo/waves/round-89/w1/ReviewerC2/receipts/`. No tools installed (pacman guard respected; nothing
needed). No git mutation anywhere; fixture repo used `git init`+`commit` only, with
`rev-parse --show-toplevel` asserted equal to the fixture dir before the first commit.

## 0. Pin verification

- `sha256sum tools/round-89/depth-blocks-v2.py` →
  `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f` — equals the frozen pin.
- Tool source read in full before running. Split key `## Queue-drain craft ` (trailing space),
  block split `(?m)^- \*\*` inside the section (terminated at the next `\n## `), resolve at
  `--rev` via `git show REV:path`, shape floor `MIN_WORDS 25` / `MIN_SPANS 2`,
  `met_target = blocks == N and resolved == blocks and not unresolved`, exit = met ? 0 : 1,
  `--expect-blocks` required (exit 2 without it).
- `--selftest`: `SELFTEST cases=10 failures=0`, exit 0.

## 1. Re-derivation (task item 1)

Commands exactly as assigned (`python3 -I -B`, absolute tool path, `--root <lane>`):

| arm | stdout (verbatim) | exit | receipt |
|---|---|---|---|
| `--rev 0ec2bb4016655f605657d6e0e700ec2e6893ac27 --expect-blocks 29` | `blocks 28 resolved 28 expect 29 unresolved 0 met=False exit=1` | 1 | `receipts/c2-base-rederive.json` |
| `--worktree --expect-blocks 29` | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` | 0 | `receipts/c2-worktree-rederive.json` |

Both reproduce the pre-freeze receipts (`pre/c2-depth-at-base.json`: 28/28/29 met false exit 1 —
matched field for field). Extra arms I ran:

- `--rev HEAD --expect-blocks 29` (HEAD = `8bbb40cc0`, the block-29 landing commit):
  `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` — green at the committed tip,
  not only the worktree.
- Negative target control `--rev HEAD --expect-blocks 28`:
  `blocks 29 resolved 29 expect 28 unresolved 0 met=False exit=1` — the target is enforced, not
  inferred (QUALITY 157 holds: a wrong N goes red).
- Base receipt JSON confirms `unresolved: []` and `resolved: 28`, i.e. the base red is purely the
  count, exactly as the "before" state claims.

## 2. Red worlds (task item 2)

Six worlds built in scratch from verbatim base blocks 1–2 (with their cited knowledge docs) plus
the adversarial block; scored with the pinned counter, `--worktree` unless noted. `expect` equals
the block count of each world, so any `met=True` is a true pass of the adversarial block.

| world | adversarial block | blocks | resolved | met | exit |
|---|---|---|---|---|---|
| w1-stub | one-line citation-only stub | 3 | 2 | false | 1 |
| w2-one-span | ≥25 words, exactly 1 backticked span, valid citation | 3 | 2 | false | 1 |
| w3-past-eof | valid shape, cites `:3-9` of a 3-line doc | 3 | 2 | false | 1 |
| w4-future-doc-rev | cites a doc absent from the commit, `--rev HEAD` | 3 | 2 | false | 1 |
| w4-future-doc-worktree | same world, doc present, `--worktree` | 3 | 3 | **true** | **0** |
| w5-duplicate | verbatim duplicate of block 1 appended | 3 | 3 | **true** | **0** |
| w6a-fenced-valid | valid rule line inside a ```` ``` ```` fence | 3 | 3 | **true** | **0** |
| w6b-fenced-stub | stub line inside a ```` ``` ```` fence | 3 | 2 | false | 1 |

Verbatim refusal problems (from the receipts):

- w1: `shape:words:4<25`, `shape:spans:1<2` — matches the pre stub control's failure mode.
- w2: `shape:spans:1<2` only — the words floor passed at ≥25, so the spans floor is what refuses.
- w3: `range:2026-01-01-past-eof.md:3-9 of 3` — out-of-range end refused.
- w4-rev: `absent:2026-11-04-created-this-round.md:absent at HEAD: corpus/knowledge/2026-11-04-created-this-round.md: fatal: path '…' does not exist in 'HEAD'`

Which pass: the duplicated block (w5), the valid block inside a fence (w6a), and the this-round
document under `--worktree` (w4-wt). Assessment:

- w4-wt is by design: `--worktree` reads the moving tree; the frozen predicate runs
  `--rev <measured rev>`, and my item-4 check shows block 29 cites nothing absent at base, so no
  this-round doc is hiding behind the worktree pass. Residual exposure exists only if a future
  invocation swaps `--rev` for `--worktree`.
- w5/w6a are counter blindnesses with no live instance today — see §5.

## 3. Shape floor vs pre-existing blocks (task item 3)

Sweep reusing the pinned counter's own `rule_blocks`/`shape` over the base craft section
(`sweep.py`, output `sweep.json`): blocks 1–28 at `0ec2bb40` range **39–2,902 words** and
**2–354 spans** — exactly the plan's declared range. `below_floor: []` — **no real block falls
below `MIN_WORDS 25` or `MIN_SPANS 2`**, so the floor removes nothing at base. Same result in the
worktree (1–29). Nearest to the floor is **block 7** (39 words, 2 spans — minimum on both axes);
any trim there flips it unresolved and turns the run red (fail-closed), not silently green.

## 4. Separability (task item 4)

Block 29 (`SKILL.md:735-737`, worktree = landing commit byte-for-byte, see §5) cites exactly:

| citation | exists at `0ec2bb40` | base lines |
|---|---|---|
| `corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md` | yes | 99 |
| `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` | yes | 125 |
| `corpus/knowledge/2026-11-04-r86-record-agreement.md` | yes | 27 |

All three are the base-present entries the frozen plan names. The one knowledge document created
this round, `2026-11-04-r89-binfo-field-value-class.md` (C1's entry), is **not** cited by block 29.
**Verdict: separable** — block 29 resolves at the base revision's corpus; the plan's QUALITY 159
statement holds. Consistently, a synthetic block citing a base-absent doc is refused under `--rev`
(w4-rev, exit 1).

## 5. Integrity of block 29 and the worktree

- Craft-section bytes (from `## Queue-drain craft ` through `## Config custody`) hash
  `7e848f9e5e8b6c07d4571e23b9f66375ae2fc7a6ed8304ecfe6b9fef479b53de` identically at
  `8bbb40cc0:SKILL.md`, `HEAD:SKILL.md`, and the on-disk worktree file. Block 29's text is
  unchanged since it landed (commit `8bbb40cc0`); it did not exist at base (the required red
  state), so no older text exists to diff against.
- The worktree is dirty: `git status --porcelain -- SKILL.md` → ` M SKILL.md`; the diff is exactly
  4 added registry rows at `SKILL.md:1958+` (round-87/88/89 instrument registrations), written by a
  concurrent seat during this review. They lie outside the craft section and outside C2's surface;
  the `--rev HEAD` green arm makes C2 robust to them.
- Block 29 vs block 28: share 2 of 3 citations (cite-token Jaccard 0.75). Not a duplication:
  block 28 is the round-88 refusal-text triage table (17 tampers × 4 carriers), block 29 is the
  round-89 field-value-class table with the stored-value-blind derivation law; different decision
  content, explicit supersession framing. 245 words / 34 spans.

## 6. Findings by severity

**HIGH — none.** No kill-rule arm fired: blocks 29/29, resolved 29/29, no unresolved, base red,
stub world red (reproduced), block 29 cites only base-present documents.

**MED-1 — declared evidence absent at review time.** The claims container names C2's evidence
`.ufo/waves/round-89/w1/ExecMatrix/matrix.json` ("produced this round by the ExecMatrix seat");
`.ufo/waves/round-89/w1/ExecMatrix/` does not exist yet (`ls: cannot access …: No such file or
directory`). Consequently block 29's sentence "On two pinned carriers packed by `upx 5.2.0`" (and
the landing commit's "2-carrier cell receipt") is **unverifiable against evidence today**. Note the
tension to check when it lands: C1's frozen population is four carriers and block 28 says "four
sha256-pinned carriers × seventeen single-field tampers", while block 29's tamper sentence says
two. The C2 predicate is explicitly judged on the counter, so this does not block C2 — but the L1
should not integrate until matrix.json exists or the block-text/evidence mismatch is dispositioned.

**MED-2 — duplicate blindness.** The counter has no duplicate/near-duplicate arm: a verbatim
re-copy of an existing block scores green (w5, `met=True exit=0`). Within the frozen predicate a
pure append is caught by count (30 ≠ 29 → red), but a copy that **replaces** an existing block
(count stays 29, all resolve) passes every arm, and no kill-rule clause names it. Mitigation now on
record: the craft-section sha256 above — the L1 can pin it at integration to make any post-review
block mutation detectable.

**LOW-1 — fence-blind block split.** The splitter/regexes ignore markdown fences: a rule-shaped
line inside a code fence counts as a block (w6a green; w6b shows the fence offers no shelter from
the floor either). No live instance: 28/28 at base and 29/29 resolved prove no real block is a
fence artifact today. Latent hygiene risk only.

**LOW-2 — `--worktree` trusts the moving tree.** A doc created this round resolves under
`--worktree` (w4-wt). The guard is the invocation convention (`--rev <measured>` in the frozen
predicate), not the tool. Keep every measured arm on `--rev`.

**INFO.** Block 7 is floor-adjacent (39 words / 2 spans) — fail-closed if trimmed, acceptable.
Negative target control and selftest both behave (§1).

## 7. Verification gaps

- I did not mutation-test the counter's internals (e.g., `PATTERN` anchoring, the `\n## `
  section terminator) — out of my seat's four items; the stub/one-span/past-EOF/absent-doc arms I
  ran are behavioral, not mutant-level.
- ExecMatrix's matrix.json absent → the "two pinned carriers" cell of block 29 rests on evidence I
  could not read (MED-1).
- The registry rows appearing mid-review in the worktree belong to a concurrent seat; I verified
  they do not touch C2's surface but did not review their content.
