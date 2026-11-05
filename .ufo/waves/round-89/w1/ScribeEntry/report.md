# ScribeEntry — round-89 knowledge entry draft (kaidoku, L1 integrates)

Seat: `ScribeEntry` (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; base
`0ec2bb4016655f605657d6e0e700ec2e6893ac27`. Scratch
`/fast/scratch/hyaku/kaidoku-r89/ScribeEntry/` — receipts copied into the seat directory first, then
the tree deleted before yield. No mutating git/jj command ran; no tool was installed or upgraded; no
pacman transaction was made.

## Drafted files (this seat's only production output)

| file | what it is |
|---|---|
| `.ufo/waves/round-89/w1/ScribeEntry/knowledge/2026-11-04-r89-binfo-field-value-class.md` | the knowledge entry draft, 101 lines (limit 120) |
| `.ufo/waves/round-89/w1/ScribeEntry/README-rows.md` | the `corpus/README.md` coverage-map row, Knowledge-index row and frontier-note paragraph drafts, plus the number→receipt table and a shape note |
| `.ufo/waves/round-89/w1/ScribeEntry/receipts/refusals.json` | this seat's refusal probes against the **declared** bytes `332917f2…` (four inputs, verbatim stderr, exit codes, sha256 of each input and output) |
| `.ufo/waves/round-89/w1/ScribeEntry/receipts/refusals-worktree-revision.json` | the same four probes against the **landed** revision `664b973a…` |
| `.ufo/waves/round-89/w1/ScribeEntry/receipts/selftest.txt` | the declared bytes' selftest, run from `HEAD:tools/round-89/upx-field-value-repair.py` at the time of this seat's work (16 cases, failures 0) |
| `.ufo/waves/round-89/w1/ScribeEntry/receipts/selftest-worktree-drift.txt` | the landed revision's selftest (22 cases, failures 0) |
| `.ufo/waves/round-89/w1/ScribeEntry/receipts/depth-at-head.json` | the target-aware depth counter at HEAD `7edab6ae5` |

The seat directory is the only place these files were written. `corpus/knowledge/` and
`corpus/README.md` were **not** touched — the L1 integrates.

## The entry's content, and the receipt behind every number

Every numeric claim in the entry is stated by a committed receipt; the mapping is:

| entry claim | receipt |
|---|---|
| `recovered 4 of 4`, `met_target true`, exit 0, `controls_ok` all true (`N1-refuse-plain`, `N2-corrupt-payload`, `N3-intact-idempotent`, `isolation`), round-88 class regression `recovered 4 of 4` rc 0 | `.ufo/waves/round-89/pre/c1-candidate-at-declaration.json` (committed) |
| tamper per carrier: jq 252→244, xxd 249→241, libz 201→193, dinit 226→218, and every repaired file equal to its packed pin (`repaired_equals_packed` true) | same receipt, `cases[].tamper` and `cases[].repaired_equals_packed` |
| REA 6.5.0 counts of the unpacked result: jq 167/30/190, xxd 99/29/103, libz 184/29/199, dinit 1268/29/1111 | same receipt, `cases[].rea.counts` |
| the unchanged round-88 repair scores `recovered 0 of 4` with all four controls true, exit 1, and the tampered file's `upx -t` refusal is `Exception: compressed data violation` on all four carriers | `.ufo/waves/round-89/pre/c1-base-r88-repair.json` (committed) |
| `identity` and `naive-global` each `recovered 0 of 4`, exit 1, `N1-refuse-plain` false (rc 0) | `.ufo/waves/round-89/pre/c1-control-identity.json`, `…/c1-control-naive.json` (committed) |
| round-87 class regression `recovered 8 of 8`; round-88 class regression `recovered 4 of 4` with its nested round-87 arm `recovered 8 of 8` | `.ufo/waves/round-89/l1/scores/c1-r87class-regression.json`, `…/c1-r88class-regression.json` (committed) |
| nine field classes on two carriers = 18 cells, 14 answer rc 1 and 4 answer rc 0, with the verbatim `upx -t` texts | `.ufo/waves/round-89/l1/scores/block29-cells.json` (committed) |
| the survivor key `(total <= u_len, total, -derived)`; the `intact` / `chain-geometry` / `field-value` classes; the stored-value-blind scan | `tools/round-89/upx-field-value-repair.py:63-106` and `:130-135` (committed at `9da6c980d`) |
| docker-init's three survivors 136 / 226 / 440 accounting 123,942,159 / 851,288 / 850,696 against `u_len` 851,288, with 226 the winner | `.ufo/waves/round-88/w1/ExecGeomCross/evidence/docker-init.derive.json` (committed) |
| the repair's refusal set and exit codes (2 / 1 / 2) and the frozen pin's selftest (16 cases, failures 0) | this seat's `receipts/refusals.json` and `receipts/selftest.txt` |
| the round-88 cost profile 1.02 s / 14.22 s / 221.85 s at 800 / 3,200 / 12,800 candidates | `.ufo/waves/round-88/l1/scores/c1-candidate-scan-scaling.json` (committed) |

## What the entry says, in short

- **The class.** A block-0 `b_info.sz_cpr` that is in range but wrong. Every bound the packer applies
  to the field passes, so the refusal moves one stage later: `upx -t` answers
  `Exception: compressed data violation` where the zeroed value answers
  `CantUnpackException: b_info corrupted`.
- **Why the packer's arithmetic gate stays silent.** The gate is a comparison on the field's value
  (`sz_cpr = sz_unc + 1` answers `header corrupted`, the PackHeader gate); an in-range wrong value
  satisfies the field comparison and fails later, at the payload stage, on the decompressed bytes.
  That is why the class is defined by the tamper's *value domain*, not by the refusal string
  (QUALITY 164).
- **The derivation and its accounting bound.** Round 88's chain law with the stored value taken out of
  the gate: the first block's `sz_cpr` is the distance from `b0 + 12` to the next plausible `b_info`
  candidate whose chain reaches the end-of-chain sentinel, bounded by `sz_unc0`; among survivors the
  candidate accounting for the most of the PackHeader's declared `u_len` wins, key
  `(fits_u_len, total, -derived)`. The stored value is not an input at all — it is read only after
  the derivation, to decide the class.
- **The three classes.** `intact` (stored equals derived, output byte-identical), `chain-geometry`
  (stored is zero), `field-value` (any other value, in range or not) — one write at `b0+4`.
- **The refusal set.** Not a little-endian ELF; no validated PackHeader; no derivable first block.
- **Named limits.** No decompression (the counter's `upx -t`/`upx -d` arms are the guard); payload
  corruption invisible to the structural walk; one field on four carriers, block 0 only; the
  round-88 cost profile carried forward, with the round-89 repair's own curve **unmeasured**.
- **The `source:` line** names S311 and S312 (the rows opened this round), S306, S309 and S310, and
  the three base-present knowledge entries the round rests on.

## Findings for the L1

1. **The repair was revised in-round while this seat worked; the entry now covers both revisions.**
   At the time of my probes the working-tree copy of `tools/round-89/upx-field-value-repair.py`
   hashed `664b973a3fb129f5920a4f583fee3810183f54a082841c77ba67039332285c37` against the declared
   `332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070`; the L1 has since committed
   that revision (`7edab6ae5`, "repair revision (typed refusals, input guards)") with a
   `claims.json` `supersessions` entry naming both hashes. The entry's class, rule, survivor key,
   three classes, measured arms and limits are identical in both revisions — only the refusal
   surface and the selftest count differ (16 -> 22 cases). My drafts therefore state the refusal set
   for the declared bytes *and* for the landed revision, with a receipt for each
   (`receipts/refusals.json`, `receipts/refusals-worktree-revision.json`,
   `receipts/selftest.txt`, `receipts/selftest-worktree-drift.txt`). Nothing in the entry's
   substantive claims depends on which revision lands.
2. **The declared bytes' third refusal was untyped, and the landed revision fixes it.** A
   little-endian ELF with no validated PackHeader exited 1 with an uncaught `r87repair.Refused`
   traceback, not the tool's own rc-2 `refused:` line — while the SKILL registry row for this tool
   states `rc 2 on a refusal` (`SKILL.md:1960`). The counter's `N1-refuse-plain` arm tests
   `rc != 0`, so it could not tell a crash from a refusal; the declared candidate receipt records
   `N1-refuse-plain` rc 1 on all four carriers, against rc 2 for the unchanged round-88 repair. The
   landed revision converts it, so all three refusals are now rc 2. The entry states both.
3. **The README row shapes are inconsistent at the file level, and the round-89 rows inherit it.**
   The `## Coverage map` table's declared header has 3 columns and every row has 3 cells, but the
   round-89 coverage row already landed at `corpus/README.md:130` has **4** cells (one more than the
   table). The `## Knowledge` table's header has 4 columns and 126 rows have 4 cells, but the
   round-88 index row at `:269` has **2** cells (no `source`, no `verified-at`) and the round-89
   index row at `:270` has **3** (no `source`); two other index rows are short the same way
   (`:140`, `:141`) and one has 5 (`:139`). The drafts in `README-rows.md` use the *declared* table
   shape rather than copying the round-88 row's literal shape, and the shape note records why.
4. **The round-89 repair's cost curve is unmeasured in any committed receipt.** The round-88 numbers
   the entry carries are the round-88 tool's. The only seat-level probe of this tool
   (`.ufo/waves/round-89/w1/SentinelR89/report.md`, an uncommitted seat report whose cost receipt is
   still in flight) read 8.378 s at 800 candidates and 125.489 s at 3,200 — an order of magnitude
   slower than the round-88 curve on a comparable family, because this repair scans every `l_info`
   candidate instead of skipping the ones whose stored `sz_cpr` is non-zero. The entry claims no
   bound for this round's repair and marks the curve unmeasured.
5. **The counter's `isolation` arm is claimed by the entry as a control.** The entry states that the
   counter runs each invocation in a private directory and that the `isolation` control records the
   listing each invocation saw — which is what the receipt's `isolation` cells contain. The
   SentinelR89 seat report (uncommitted) argues that arm cannot fail, because the listing is taken
   before the child runs. The entry does not claim the arm is discriminating; it reports what the
   receipt states. If the L1 wants the arm's strength characterised, that belongs to the attack
   seats, not to this entry.
6. **The plan's prose pin is stale.** The task prose and the dispatch/spec quote the repair at
   `048e2c8e…`; the frozen container (`pre/c1-red-control-container.json`), the committed receipt and
   the file on disk all say `332917f2…`. The SentinelR89 report records the same conflict (F13). The
   entry quotes the container's pin.
7. **The refusal message is carrier-dependent, and the committed 2-carrier probe does not show it.**
   The committed cell receipt (`l1/scores/block29-cells.json`) covers jq and xxd — both main
   executables — and records `header corrupted` for `sz_cpr := sz_unc + 1`. Two wave seats measured
   the shared object answering `CantUnpackException: corrupt b_info` for the same class:
   `.ufo/waves/round-89/w1/ExecMatrix/matrix.json` (4 carriers × 12 classes; `header corrupted` on
   three, `corrupt b_info` on libz) and `.ufo/waves/round-89/w1/ScoutUpxSrc/report.md` §4 (libz, on
   fresh packs). The ScoutUpxSrc report also notes that the block-0 bound is evaluated before the
   shlib/main split, so the two paths word the same field differently. The entry records this as a
   `[observation]` under the cell table: the class, not the message, is the stable key. Neither
   measurement is a committed receipt, so the entry cites them as wave-seat receipts, not as
   committed evidence.
8. **The source scout's own adjudication corrects the entry's S311 line.** `ScoutUpxSrc/report.md` §4
   says the entry's S311 source line reads as if `corrupt b_info` were the single carrier-facing
   message. The entry keeps S311 as the source row but the new `[observation]` above states the
   carrier split, so the line no longer implies one message for all carriers.

## Commands run by this seat, with exit codes

| command | exit | note |
|---|---|---|
| `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` (declared bytes, extracted from `HEAD` at the time of this seat's work) | 0 | `SELFTEST cases=16 failures=0` |
| `python3 -I -B tools/round-89/upx-field-value-repair.py --selftest` (landed revision) | 0 | `SELFTEST cases=22 failures=0`; hash `664b973a…` |
| `python3 -I -B tools/round-89/upx-field-value-repair.py --in <4 refusal inputs> --out <path>` (declared bytes) | 2 / 1 / 2 / 1 | `receipts/refusals.json` |
| the same four probes (landed revision) | 2 / 2 / 2 / 2 | `receipts/refusals-worktree-revision.json` |
| `python3 -I -B tools/round-89/depth-blocks-v2.py --root <lane> --rev HEAD --expect-blocks 29 --json-out <receipt>` | 0 | `blocks 29 resolved 29 expect 29 unresolved 0 met=True exit=0` at HEAD `7edab6ae5` (`receipts/depth-at-head.json`) |
| `sha256sum tools/round-89/*.py`, `git status --porcelain`, `git log`, `git show`, `git diff` | 0 | read-only |
| `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show HEAD:tools/round-89/upx-field-value-repair.py` | 0 | extracted to scratch for the declared-bytes probes |

No verification of the round's claims was performed by this seat beyond reading the committed
receipts; the depth-counter run above is a read of the counter's own output, reported verbatim.

## Hygiene

- Files written: only under `.ufo/waves/round-89/w1/ScribeEntry/`.
- `corpus/knowledge/`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, `plans/`,
  `.ufo/waves/round-89/claims.json`, the pre-freeze receipts and every sibling seat's directory were
  read but not modified.
- Scratch `/fast/scratch/hyaku/kaidoku-r89/ScribeEntry/` deleted after the receipts were copied here.
  The first deletion was verified: `ls -d /fast/scratch/hyaku/kaidoku-r89/ScribeEntry` -> "No such
  file or directory", rc 2. The tree was re-created afterwards to capture the landed revision's
  refusal probes and re-taken the depth receipt, and is deleted again in this seat's final step
  (`rm -rf`, verified by absence).
