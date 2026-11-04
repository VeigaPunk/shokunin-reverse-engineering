# CriticClaims — scoped findings (round 68, wave w1)

Seat: critic. Scope: attack R68-C1 and R68-C2 by measurement. Full dossier with every command:
`w1/CriticClaims/attack.md`; receipts: `w1/CriticClaims/receipts/`.

Frozen inputs re-hashed before use and identical to the container pins
(`a300d831…` registry-conformance.py, `48ef4c68…` packed-elf.py, `0657ee08…` controls.py); both selftests green
(11 and 13 cases). No tracked file edited; no commit, index or jj mutation; no subagent dispatched.

## Verdicts

**R68-C1 — survived as a predicate, with two latent under-constraints.**
The repair is real and minimal: base `fcbe200…` reproduces `mismatches 2 / scope 69 / rows 73` naming exactly the two
round-67 instruments (A1 confirmed). At HEAD (`6ffa9ce`) it is **not met** — `mismatches 4 / scope 71 / rows 73` — because
the four rows exist only as an uncommitted worktree diff (`git diff --stat HEAD -- SKILL.md` = 4 insertions, 77 rows).
Scoring the worktree text through the instrument's pure functions gives exactly `0 / 71 / 77`, so the predicate is
reachable by precisely the four rows; `--rev` reads git objects, so it is unmeasurable until committed.

- (a) Regime width: implemented scope 71 of **332** existing tools (21.4%). Each filter suppresses a real class —
  threshold 41 dropped: 97 scope / 30 unregistered (26 of 26 legacy tools unregistered); own-round rule dropped:
  102 / 33; exists filter dropped: 109 / 42; all widened: 114 / 45. Disclosed in every receipt.
  → survived as disclosed; "mismatches 0" is 0 over 21% of the tree.
- (b) `scope_size 71`: arithmetic yes (69 + 2, measured), **necessity falsified**. Fixture: drop the
  `avm-le-counter.py` citation from round-67's plan, cite the uncited `tools/round-68/controls.py`, delete the avm row and
  add a controls row → `0 / 71 / 77`, ok true, **with one of the four narrated rows absent**. Also brittle: citing
  `controls.py` truthfully in the plan gives scope 72, mismatches 5. The triple is a count over mutable plan text,
  not a membership pin.
- (c) Row naming a different file: **falsified** — exact string equality required. 13 variants (suffix `.bak`, `/x`,
  no extension, `./`, double slash, trailing space, glob, wrong round dir, cyrillic homoglyph, case swap, doubled
  backticks, extra cell text) all leave the target unregistered and add a `row_absent`. Note: an unparseable row is
  silently dropped (fails closed).
- (d) `thin` prose gaming: **falsified as a guarantee** — `"note 0 (zero); item 1 (one); tag 2 (two)"` passes with no
  exit-code semantics. Not exploited: 77/77 rows name all three codes, and a segment-start grammar keeps 77/77 green
  while rejecting the prose fixture (receipt `thin-segment-start.json`).

**R68-C2 — survived; the route is real, reproducible, and independently corroborated.**
Frozen-instrument rerun at the base: exit 0, `met_target true`, `carriers_matched 2`, `control_ok true`, `failing []`,
`before_procedures [3,3]`, packed shas byte-identical to the committed receipt (`e8b6c9e7…`, `1727faf9…`), all arms true,
control rc 2/2, refusal 4841 bytes with `FUN_00103fa0` (receipt `c2-frozen-at-base.json`).

- (a) Identity: establishes `upx --best`/`upx -d` is byte-exact for these two carriers on upx 5.2.0 (unpacked sha equals
  the pin). Does not establish provenance of third-party artifacts, any other packer version, or authenticity of the
  pin; it is an in-run round trip of the packer's own output. → survived as narrowly stated.
- (b) `recovery_ok`: **tautological**. Identity ⇒ byte equality; REA is content-deterministic (same bytes under two
  names give identical counts for both packed and SHT-stripped files), so recovery cannot fail except through
  nondeterminism, and it is strictly weaker than identity. Redundant arm, not an error.
- (c) `before` = 3 procedures: my artifact hypothesis **falsified by counter-fixture**. `strip --strip-section-headers`
  on the *unpacked* original (0 sections, `upx -l` rc 2) still yields 165/6/161; only the packed bytes give 3/3/3.
  Corroborated by rizin (packed `binsz 0x228` = 552 B vs nosh `0x6d80`), `readelf -l` (6 phdrs, 2 LOAD, entry 0xb780),
  `strings` (42 vs 195), and a refusal that fires at the entry point too. → survived.

## Defects to route (none falsify a predicate as measured)

1. **Before-arm floor ≠ predicate.** `before_ok` is `< floor` (50/25), not `== 3`; exit 0 does not entail "exactly 3".
   L1 must read `before_procedures`.
2. **A6's upx pin has no value and is not enforced.** `UPX_SHA256 = None` is never assigned or compared; A6 names a pin
   without a value while distinguishing "RECORDED … never pinned" for the npx lock. Observed:
   `/usr/bin/upx` `cf2f6e7c…`, `upx 5.2.0`. Judge-side fix: assert the receipt's `packer.sha256`/`version` against the
   round's declaration.
3. **`detected` can be true on a failed readelf** (`section_count("") == 0`, error text → 0) and the readelf run is not
   recorded. Latent; record/require rc 0 at the next freeze.
4. **The committed before-arm receipt is not attributable to the frozen instrument.**
   `l1/pre/c2-dryrun-at-base.json` records `instrument.sha256 7ee286c0…`; `c2-skiprun.json` records `ff11d8ec…`; neither
   is `48ef4c68…` and neither exists in any commit (all four commits of the file hash to `48ef4c68…`), while the
   container declares `instrument_supersessions: []`. The `c2-real` control consumes that receipt. The frozen rerun
   supersedes it empirically — use `receipts/c2-frozen-at-base.json` or disclose.
5. **A9 is not met by the pre receipts**: both record `rev: "main"` (argv alias, never resolved) and
   `instrument.rev: null` (generated before the instruments were committed). My reruns populate both fields when a sha is
   passed to a committed file. Pass full shas for every scored run; optionally record `rev_resolved`.

## Impacted axes

- calibration: the metric's denominator is derived from plan text, so the repair can be satisfied by shrinking the
  population (demonstrated) and the exact 71 breaks on a truthful plan addition; `thin` accepts prose.
  Smallest safe corrections: judge-side scope-**set** equality plus a `c1-scope-shrink` control at the next freeze;
  segment-start thin grammar (77/77 rows stay green).
- coverage: redundant `recovery_ok`, dateless/unenforced upx pin, `detected` conflation, and a before-arm receipt from an
  uncommitted build. Smallest safe corrections: value assertions on `before_procedures` / `packer.*`; replace the
  before-arm receipt with the frozen rerun; record readelf rc at the next freeze.

**Must not be accepted as evidence:** the `7ee286c0` before-arm receipt as a frozen-instrument measurement (and its
`c2-real` inheritance); `0 / 71 / 77` as proof that the four rows were added (it is a count, shown green with a row
missing); A6's "pinned by sha256 and version" as an enforced pin.

**Unknown:** whether the uncommitted four-row worktree diff is byte-identical to what the build seat commits; whether the
older receipt builds differed semantically from the frozen one (bytes are gone; the frozen rerun reproduces every field).

Tooling: nothing installed or upgraded; no package-manager transaction (pacman paused); no L0 question. Scratch
`/fast/scratch/hyaku/kaidoku-r68/CriticClaims/` removed at exit.
