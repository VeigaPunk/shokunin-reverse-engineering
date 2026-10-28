# R44W2C2Freeze — R44-C2's freeze check covers five paths and one directory; the claim's own frozen set is much larger, and four post-freeze mutations of claim-frozen paths score **green**

Seat `R44W2C2Freeze`, round 44 wave 2 (falsification of the landing and the record).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`, measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`, lane tip at dispatch
`c86ea508188c50e2645b1f9bba65df4177cda6b1` (now `8bb1090af3fef64477c4337855e4347472db2701`).

Scope of this seat: **freeze-integrity coverage of the R44-C2 counter, not its arithmetic.**
Baseline reproduced first (so every arm below is a delta on a known-green instrument):

```
python3 -I -B tools/round-44/c2-counter.py --root <clone> --rev 55bcce69… --freeze c48f8a4… \
        --work <scratch>/work-base --json-out <scratch>/base.json
→ exit 0, entries_evaluated 80, mismatches [], frozen_path_changed [], met_target true
  counter_sha256 085192ea6c3f3f4d67c58ce459ef06e1febd0b668dc367ccfbdd12661736c277 (== at freeze)
  stdout sha256 b4e4a26b3ccbed91c5c1927e6d6b2111cdec62f84064ebbd642c167ebbfaf132, wall 4.44 s
```

Environment: one `git clone --shared` of the lane at
`/fast/scratch/hyaku/kaidoku-r44/R44W2C2Freeze/clone` (`git rev-parse --show-toplevel` asserted
equal to that path before every commit inside it), `TMPDIR` under the same scratch dir. Every arm
is an isolated detached commit **whose parent is `55bcce69`** (each arm switches back to
`55bcce69` first), identity `-c user.name=R44W2C2Freeze -c user.email=…@scratch.invalid`, inside
the throwaway clone only. No tool was installed (none was needed; pacman is paused host-wide).

---

## 1. What the C2 counter actually enumerates

The freeze check is `freeze_integrity()` (`tools/round-44/c2-counter.py:595`). Its input set is
built entirely by `parse_rubric()` (`:328`):

| source | anchor | members |
|---|---|---|
| `C2_DEFAULT_FROZEN` | `tools/round-44/c2-counter.py:134` | `SCORECARD.md`, `SHONEN.md`, `SKILL.md` |
| rubric `frozen_paths` | `tools/round-44/c2-rubric.json` | `SCORECARD.md`, `SHONEN.md`, `SKILL.md` |
| rubric `expected_edits` keys | `tools/round-44/c2-rubric.json` | `SCORECARD.md` (bound-append arm, 8 exact lines) |
| hard-coded instrument paths | `c2-counter.py:455-456` | `tools/round-44/c2-rubric.json`, `tools/round-44/c2-counter.py` |
| rubric `frozen_dirs` | `c2-counter.py:480-483` | `tools/round-44` — every path **under it that appears in the FREEZE..REV union walk** |

Executed receipt confirms exactly five frozen paths plus one directory prefix (`base.json`):

```
frozen_paths = ['SCORECARD.md', 'SHONEN.md', 'SKILL.md',
                'tools/round-44/c2-counter.py', 'tools/round-44/c2-rubric.json']
frozen_dirs  = ['tools/round-44']
freeze_notes = SCORECARD.md bound_edit_applied; SHONEN.md / SKILL.md / c2-counter.py / c2-rubric.json unchanged
```

`SCORECARD.md` is therefore *relaxed* (append-only, exact 8-line block) and `SHONEN.md`,
`SKILL.md`, the counter and the rubric are strict. **Nothing else is looked at.** The list is
hard-coded/declared in the instrument; it is never derived from the claim file's own
`## Frozen paths` section.

## 2. The claim's frozen set vs. the counter's set

`plans/round-44-claims.md:305-315` — "Byte-frozen (change ⇒ `frozen_path_changed`, exit 2)":

| # | claims-frozen family (line) | enumerated by the C2 counter? | who covers it |
|---|---|---|---|
| 1 | `plans/round-44-claims.md` (`:307`) | **NO** | C1 counter only (`c1-counter.py:273`, `FROZEN_PATHS[0]`) |
| 2 | `tools/round-44/` directory incl. `control-fixtures/**` (`:307-308`, `:311`) | yes (dir pathspec) | both |
| 3 | `tools/round-42/fixtures.json` (`:308`) | **NO** | C1 counter only |
| 4 | `tools/round-42/c1-counter.py` (`:308`) | **NO** | C1 counter only |
| 5 | `tools/round-43/c1-counter.py` (`:308`) | **NO** | **neither** (C1's `FROZEN_PATHS` names the round-42 port source, not the round-43 one; `grep -c "round-43/c1-counter.py" c1-counter.py` → 0) |
| 6 | four C1 carrier bins (`:309`) | **NO** | C1 only, and only through the per-carrier pin binding (`carrier_pin_ok`), not the freeze walk |
| 7 | four oracle trees `corpus/evidence/round-44/oracle/` (`:310`) | **NO** | C1 only (`FROZEN_PREFIXES`, `c1-counter.py:286`) |
| 8 | round-42 v3 C1 receipt inputs; round-42/43 heldout receipts for CTL-C1-4 (`:311-312`) | indirectly, via `tools/round-44/control-fixtures/{c1,c4}/` | both (directory) |
| 9 | `SKILL.md` (`:312`) | yes (strict) | both |
| 10 | `corpus/SOURCES.md` "after S138/S139 are added in FREEZE" (`:312`) | **NO** | **neither freezes its bytes** (C1 reads it at REV for the registry binding, `c1-counter.py:2172`; C2 exports it) |
| 11 | "all historical score receipts explicitly pinned by path and digest in C2's rubric" (`:313`) | **NO** — and no digest binding exists in the rubric | nobody |

Item 10 is internally contradictory in the frozen text itself: the same file appears at
`plans/round-44-claims.md:318` under "NOT frozen — BASE-pinned in the C2 rubric … `corpus/SOURCES.md`
*for C2 only* (… no later SOURCES edit is permitted by either claim)". The prohibition is stated and
unimplemented; the two sentences cannot both be satisfied by one instrument.

## 3. Arms — one mutation each, all parented on `55bcce69`, all scored against `c48f8a4`

Command shape for every row (`<name>` = arm):

```
python3 -I -B <clone>/tools/round-44/c2-counter.py --root <clone> --rev <arm-commit> \
        --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --work <scratch>/work-<name> \
        --json-out <scratch>/<name>.json --seat R44W2C2Freeze
```

Every run creates `--work` (`mkdir -p`) before scoring — an absent `--work` is silently ignored by
the counter and makes it cite the tempdir in every entry command (F-7).

| arm | path mutated post-freeze (one change) | arm commit | exit | `frozen_path_changed` | `met_target` | wall | stdout sha256 |
|---|---|---|---|---|---|---|---|
| **claims** | `plans/round-44-claims.md` — appended a "Post-freeze amendment" withdrawing the C1 target (`carriers_matched == 0`); +5 lines (numstat `5 0`) | `ee444b5aec35e6f8de6767b977fd2faa62a78eb7` | **0** | `[]` | **true** | 4.31 s | `d7b47e25206446e0e798b6f60450c2b5a7e3b61aaeeddcdc6c732fed20de25f3` |
| **sources** | `corpus/SOURCES.md` — appended a comment line (no table row) | `aa06568296c7b82ff5d2b8492725c42bef9629da` | **0** | `[]` | **true** | 4.28 s | `6fcff74471a36a70fa4941e7daee8faed0e51f0077c6390dc3cbdf7e08914b5d` |
| **r43** | `tools/round-43/c1-counter.py` — appended two lines | `18b08e4d8084c8120506888062ef7f7e816e211f` | **0** | `[]` | **true** | 4.44 s | `0cf2b5e75ceedd10efdb2292fdc0484cdce83a74bd492ff1ed7c8048ee60a90d` |
| **carrier** | carrier bin `corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin`, one byte flipped at offset 100 (`sha256 b45925fa…e23e71` → `1209f508…dc0763`) | `5abdb0b4756443030028d211c9f0c9be47253977` | **0** | `[]` | **true** | 4.59 s | `c3790edfa1bff66b51c83fdab2693a52e773f99d6feec9e3f9479de05de0d621` |
| **oracle** | `corpus/evidence/round-44/oracle/squashfs_v1/little_endian/__output__/squashfs_v1.0_le.bin_extract/apple.txt`, line appended | `90f82d2cc746ba55a75f4800efe8aad0d39088a4` | **0** | `[]` | **true** | 4.56 s | `79ada2412ca7a3425042381a2960b366ba5bda8bc78b28d0c875e92c1d362ce1` |
| **receipt** | `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`, one byte (`\n`) appended — the receipt C2-e07 re-derives its verdict from | `846fe860673465542e1f9f06e909ad752254a341` | **0** | `[]` | **true** | 4.56 s | `f42982e60b245aeb34806966f8bc31989961aa1543f53844f3ab4898f891ebb6` |
| **shonen** (control, declared path) | `SHONEN.md` — comment line appended | `17d75f94f12ad5bc7bc31771a029bd11f6cd7893` | **2** | `["SHONEN.md"]` | false | 0.07 s | `89448ef8644af285955d600fcae2e7d2869f4772ab06319a132e5997cae5f16f` |
| **r44dir** (control, declared dir) | `tools/round-44/control-fixtures/c3/manifest.json` — one byte appended | `e8c4776147e7673bd354c7b8c295338ef497aa6e` | **2** | `["tools/round-44/control-fixtures/c3/manifest.json"]` | false | 0.07 s | `977e006841759ca9b0b3694c8b9213ab5cda7098a5ca7768e64607147b8e94b0` |

The two controls show the instrument is not simply green: for a **declared** path it reds with exit 2
before evaluating a single entry (0 entries, 0 mismatches). The green rows are therefore coverage
gaps, not a broken counter.

Relevance to the measured revision — the six uncovered families are untouched inside the measured
range, so the 80/80 number itself is not false:

```
git -C <lane> log --oneline c48f8a4..55bcce69 -- plans/round-44-claims.md corpus/SOURCES.md \
    corpus/evidence/round-42/c2/fixtures corpus/evidence/round-44/oracle
→ (no output)
```

What is false is the inference the record draws from it: `frozen_path_changed []` does not certify
the claim's freeze clause, and the identical `met_target true / exit 0` is returned for revisions
that rewrite the claim text, the SOURCES registry, the frozen port source, the carrier bytes, the
oracle tree, or a receipt a verdict is derived from.

## 4. Numbered defects (for the L1)

**F-1 (high) — `plans/round-44-claims.md` is not in the C2 freeze set.**
Path: `tools/round-44/c2-counter.py:134` (`C2_DEFAULT_FROZEN`), `:455-456`, rubric
`tools/round-44/c2-rubric.json` `frozen_paths`/`frozen_dirs` (= `tools/round-44` only).
Command (arm `claims`): see §3. **Exit 0, `frozen_path_changed []`, `met_target true`, 80/80** on a
commit whose only change is a 5-line post-freeze amendment withdrawing the C1 target. Expected under
`plans/round-44-claims.md:305-307`: exit 2 `frozen_path_changed ["plans/round-44-claims.md"]`.
Impact: the claim's admissibility conjunct ("no commit in FREEZE..REV touches a frozen path of that
claim") is not evaluated by the claim's own instrument; a rewritten claim and an untouched claim are
indistinguishable at scoring time. C1's counter does enumerate this path, so the round is not blind
overall — but the C2 score never speaks to it.

**F-2 (high) — `corpus/SOURCES.md` is byte-frozen in the claim text and frozen by neither counter.**
Paths: `plans/round-44-claims.md:312` (byte-frozen) vs `:318` (listed NOT frozen "for C2 only",
with "no later SOURCES edit is permitted by either claim"); `tools/round-44/c2-counter.py:144`
exports it, never freezes it; `tools/round-44/c1-counter.py:2172` reads it at REV, never freezes it.
Command (arm `sources`): **exit 0, `frozen_path_changed []`, `met_target true`.** The two sentences
at `:312` and `:318` cannot both hold; whatever the L1 intended, no instrument enforces either.

**F-3 (medium) — `tools/round-43/c1-counter.py` is a named frozen port source and is covered by
neither counter.** Paths: `plans/round-44-claims.md:308`; absent from
`tools/round-44/c1-counter.py:272-286` (`FROZEN_PATHS` has `tools/round-42/c1-counter.py` only;
`FROZEN_PREFIXES` is `tools/round-44/`, `corpus/evidence/round-44/oracle/`). Command (arm `r43`):
**exit 0, `frozen_path_changed []`, `met_target true`** after a post-freeze edit to the port source
the C1 counter was ported from.

**F-4 (medium) — the "historical score receipts pinned by path and digest in C2's rubric" family has
no digest binding and no freeze coverage.** Paths: `plans/round-44-claims.md:313`;
`tools/round-44/c2-rubric.json` — 27 `(e)` entries carry a `__RECEIPT__` path but
`0` entries carry a sha256 for that path (`entries with sha256 in (a)/(e): 0`), and no receipt path
is in `frozen_paths`. Command (arm `receipt`), appending one byte to
`.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` (the receipt `C2-e07-r40-c1-verdict` derives its
verdict from): **exit 0, `frozen_path_changed []`, mismatches [], `met_target true`.** The clause is
therefore vacuous as written, and the bytes a verdict rests on are mutable post-freeze without
notice.

**F-5 (informational) — carrier bins and `corpus/evidence/round-44/oracle/**` are outside the C2
freeze set.** Arms `carrier` / `oracle`: both **exit 0, `met_target true`** with the frozen bytes
changed (carrier `b45925fa…e23e71` → `1209f508…dc0763`). They are covered by the C1 instrument
(oracle via `FROZEN_PREFIXES`; carriers via the pin binding, not the freeze walk). So the round is
not blind here — but `met_target true` from the C2 counter is not evidence either way.

**F-6 (M44-2 / `tools/round-45/frozen-path-preflight.py`) — it catches the graded incident, but only
with the one pathspec the record actually used, and that pathspec misses the claim file.**
Measured:

| invocation (`--root <lane>`, freeze `c48f8a4`) | rev | exit | receipt |
|---|---|---|---|
| `--pathspec tools/round-44` | `c86ea508` | **1** — `frozen_path_changed`, 8 `touched` (all `c86ea508 M`), 8 `blob_changed` | `.ufo/waves/round-44/l1/preflight-c86ea508.json` |
| `--pathspec tools/round-44` | `55bcce69` | 0 — clean | `.ufo/waves/round-44/l1/preflight-55bcce69.json` |
| `--pathspec tools/round-44` | `81bcc65e` (claims-only commit, clone) | **0 — clean**, `touched []` | `artifacts/R44W2C2Freeze/preflight-claims-only.json` |
| `--pathspec plans/round-44-claims.md` | `81bcc65e` | **1** | `artifacts/R44W2C2Freeze/preflight-claims-path.json` |
| *no* `--pathspec` | `8bb1090a` (lane tip) | **1** — 557 `touched`, `blob_changed []` (every path in the range, including `.ufo/waves/**`, `LOG.md`) | `artifacts/R44W2C2Freeze/preflight-none.json` |

So: the fix **does** catch M44-2 exactly as claimed (red on `c86ea508`, green on `55bcce69`,
`--pathspec tools/round-44`), and the tool is honest about exit codes. But it is a manual checker,
not a gate: (a) the demonstrated pathspec is the directory alone, and with that same pathspec a
commit that rewrites the frozen claim text returns `verdict clean, exit 0` — the fix reproduces the
counter's path list instead of the claim's; (b) its default (no pathspec) flags *every* path in
`FREEZE..REV`, so it cannot be wired bare into a commit sequence (557 false paths on the real
range); (c) nothing invokes it — no git hook, no runner reference; the only references are the
lesson, `corpus/QUALITY.md` row 77, `LOG.md`/`SCORECARD.md` prose, the wave spec, and the two
receipts. R44-CL1's "wire it into the round's commit sequence" therefore is necessary but not
sufficient: wiring it with `--pathspec tools/round-44` would have caught M44-2 and would still miss
F-1..F-4.

**F-7 (medium, instrument hazard) — an absent `--work` is silently ignored, and the fallback embeds
the tempdir in every entry command.** Paths: `tools/round-44/c2-counter.py:1205-1207`
(`base = work or os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()`;
`tempfile.mkdtemp(…, dir=base) if os.path.isdir(base) else tempfile.mkdtemp(…)`), versus
`tools/round-44/c1-counter.py:451-461` (`scratch_root()` does `os.makedirs(WORK_OVERRIDE,
exist_ok=True)` and deliberately never calls `gettempdir()`; its docstring names the class:
"R44-SCR-TMP"). Observed: my first pass passed `--work <scratch>/work-base` without creating it; all
7 evaluable receipts then embedded `<tmp>/c2-counter.<rand>/repo` in `entries[].command` (80
occurrences in `base.json`). Re-run with `mkdir -p` first: the workdir is created under `--work`, and
`grep -o '/tmp/…'` over the whole artifact set returns **0**. A second probe with an explicit,
existing `TMPDIR` and an uncreated `--work` lands under `TMPDIR`
(`…/tmp/c2-counter.hrtv590_/repo`, exit 0; the probe receipt was deleted with the probe), so
`tempfile.gettempdir()` *is* honoured — the `/tmp` form is the default-environment outcome (no
`--work` directory, no `TMPDIR`), which is exactly how the L1's and wave-1 receipts were produced. Verdicts are unchanged between the two
passes (`base` stdout sha identical, `b4e4a26b…f132`), so only the citation is affected — but the
citation rule is part of the record, and the same fallback explains the wave-1 C2 control receipts
and `l1/c2-score-at-55bcce69.json` (peer report, `R44W2SentScope`). Fix for round 45: mirror
`c1-counter.py` — `os.makedirs` the `--work`/`HYAKU_SCRATCH` base, never fall through to the tempdir.

## 5. Verdict on the record

- **The measured number is honest.** `55bcce69` is a strict ancestor of the violating commit, no
  commit in `FREEZE..55bcce69` touches any of the six path families in §2 (empty `git log`
  above), the instrument's own hash equals its freeze hash (`085192ea…36c277`), and the tip-red is
  committed twice (`.ufo/waves/round-44/l1/{c1,c2}-score-at-tip.json`, exit 2 with the 8-file list;
  lesson M44-2 says so in words). Exit 2 at `c86ea508` and the lesson's statement "both exit 2
  `frozen_path_changed` instead of 0/1" check out.
- **The freeze binding is not demonstrated, only asserted.** R44-C2's Target says
  `mismatches == 0 … frozen_path_changed []`; at the measured revision that is true, but the same
  pair of values is produced after the claim text is rewritten (F-1). The record should state which
  frozen paths the instrument covers, not merely that the list was empty. The lesson's M44-2 cell
  already says the enforcement lived only in the scoring counter ("fix (shown able to fail): none");
  the gap is that the *scoring counter's own list* is the short one.
- **M44-2 as a classification is correct; its routed fix is under-specified.** `freeze-violation`
  with a directory pathspec, discovered at the tip, is the right class; the honest measure-at-ancestor
  and disclosure are adequate for this round. The fix closes the directory family only.

## 6. Smallest safe correction (for the L1; I changed nothing)

1. Give the C2 rubric one authoritative `frozen_paths` entry for **each** family at
   `plans/round-44-claims.md:305-315` — at minimum `plans/round-44-claims.md`,
   `corpus/SOURCES.md` (or delete the `:312` sentence and keep only `:318`, consistently),
   `tools/round-42/fixtures.json`, `tools/round-42/c1-counter.py`, `tools/round-43/c1-counter.py`,
   the four carrier bins and the `corpus/evidence/round-44/oracle/` prefix (add it as a
   `frozen_dirs` entry; `freeze_integrity` already handles prefixes correctly — see the `r44dir`
   arm). The rubric change is inside `tools/round-44/`, so it must land *in the freeze*, and the
   counter's own hash moves accordingly.
2. Either add `digest` fields for each `(e)` entry's `__RECEIPT__` and a freeze check on that path,
   or delete the "pinned by path and digest" clause from `:313` (F-4). Pick one; both are one-line
   changes to frozen text, so the next freeze must do it, not this one.
3. Run `tools/round-45/frozen-path-preflight.py` with the **same** pathspec list as (1) — one list,
   two consumers, or the two instruments will keep disagreeing. Its bare default is unusable; make
   the pathspec required (or read it from the claim), and add the red arm `81bcc65e`-style
   (claims-only commit → must be exit 1) to the round-45 red/green pair, which currently only proves
   the directory family.

## 7. Receipts

All receipts are under
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w2/artifacts/R44W2C2Freeze/`
(`*.json` full counter receipts, `*.stdout` the printed summary, `sha256-manifest.txt` covering both
sets, plus the four preflight receipts). Scratch tree
`/fast/scratch/hyaku/kaidoku-r44/R44W2C2Freeze/` (clone + nine `work-*` dirs) was deleted after the
artifacts were copied. Every archived receipt was produced with an existing `--work` directory under
that scratch root: `grep -o '/tmp/[A-Za-z0-9._/-]*' *.json` over the artifact set returns 0 matches
(F-7 explains the first pass, which was re-run for exactly this reason). No lane file, counter, rubric, frozen byte or production doc was modified; the
only commits made are inside the throwaway `git clone --shared` described in §3, each on a detached
head parented at `55bcce69`, with the clone's toplevel asserted before every commit.

Axis impact: **calibration (R44-C2)** — the claim's freeze-integrity binding is instrument-verified
for 5 paths + 1 directory and asserted for 6 further frozen families, four of which I showed scoring
green when mutated. **Coverage (R44-C1)** untouched by this seat, but F-5/F-6 bear on the M44-2 record
and on R44-CL1's fix.
