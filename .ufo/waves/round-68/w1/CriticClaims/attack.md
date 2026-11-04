# CriticClaims — attack on R68-C1 and R68-C2

Seat: `CriticClaims` (critic, wave w1). Leaf: no subagent dispatch, no tracked-file edit, no index/jj/git mutation.
Target: kaidoku-shokunin round 68, base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`, operative freeze
`1eaf596e5f241762349fbd102c9e09ec1df18e3f`. Measured HEAD during the attack: `6ffa9ce1119ec01c953494d8f5b28e419efad646`.

Every number below is an **observation** with the command that produced it, unless labelled **inference** or **unknown**.
Scratch root `/fast/scratch/hyaku/kaidoku-r68/CriticClaims/` (created and removed inside this seat); receipts copied to
`.ufo/waves/round-68/w1/CriticClaims/receipts/`.

Frozen inputs verified before use:

```
sha256sum tools/round-68/*.py
a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315  registry-conformance.py
48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e  packed-elf.py
0657ee080ba92459cfc2916715dce8c0f1c49930e03c8c3d36ac60dbd5618fb4  controls.py
```
Both selftests green: 11 cases (`registry-conformance.py --selftest`), 13 cases (`packed-elf.py --selftest`).

---

## 1. R68-C1 — verdict summary

| sub-question | verdict |
|---|---|
| (a) regime chosen to make the count small | **survived as disclosed** — the regime is load-bearing (each filter suppresses a real unregistered class) but it is printed in every receipt |
| (b) `scope_size 71` follows necessarily | **falsified as necessity** — 71 is a count over mutable plan text; a different tree reaches (0, 71, 77) with one of the four required rows absent |
| (c) a row naming a different file passes | **falsified** — exact string equality is required; 13 variants all fail closed |
| (d) `thin` gameable by prose | **falsified as a guarantee, not exploded** — a prose cell passes, but 77/77 real rows also pass a stricter segment-start grammar |

State observation first, because it bounds everything else: **at HEAD the claim is not met**.

```
python3 -I -B tools/round-68/registry-conformance.py --root . --rev HEAD
-> scope_size 71, registry_rows 73, mismatches 4,
   unregistered = [r67/avm-le-counter.py, r67/mutation-battery.py,
                   r68/packed-elf.py, r68/registry-conformance.py]
python3 ... --rev 1eaf596e5f241762349fbd102c9e09ec1df18e3f
-> scope_size 71, registry_rows 73, mismatches 4 (same four paths)
python3 ... --rev fcbe200f6739c38939e0dabf3f251de2cc6bd727
-> scope_size 69, registry_rows 73, mismatches 2,
   unregistered = [r67/avm-le-counter.py, r67/mutation-battery.py]   (base arm reproduces exactly: A1 confirmed)
```

The four repair rows exist during this review only as an **uncommitted worktree diff** (`git diff --stat HEAD -- SKILL.md`
= `4 ++++`, rows 73 -> 77). The census reads git objects (`git show REV:SKILL.md`), so the worktree repair is not
measurable at any `--rev` until it is committed. Scoring the worktree text through the instrument's pure functions:

```
python3 -B c1probe.py
census(plans@HEAD, SKILL.md-worktree, existing@HEAD)
-> mismatches 0, scope_size 71, registry_rows 77, unregistered [], thin [], ok true
```

So the predicate's triple is reachable, and the minimal diff that reaches it is exactly the four rows. That part of the
claim is sound.

### (a) Regime width — numbers, not opinion

Independent extraction (my own tokenizer, `extract.py`, not the instrument's `TOOL_RE`), HEAD:

```
existing blobs under tools/ at HEAD : 332
registry rows at HEAD               : 73      (77 with the four-row worktree diff)
scope under the implemented regime  : 71      (71/332 = 21.4% of the tool tree)
```

| widening | scope | unregistered | command |
|---|---|---|---|
| implemented: own-round, N>=41, exists | **71** | **4** | `python3 -B c1attack2.py` §a |
| threshold 41 dropped (all rounds, own, exists) | 97 | 30 | same |
| own-round rule dropped (any plan, any round, exists) | 102 | 33 | same |
| exists-at-rev filter dropped (own, N>=41) | 109 | 42 | same |
| all three widened | 114 | 45 | same |

The suppressed classes are real, not theoretical: **26 of 26** pre-41 named tools that exist are unregistered
(`legacy_unregistered`, printed in every receipt), and **12** named tools do not exist at the revision
(`named_but_absent`, printed). The own-round rule hides 31 more tools that exist and are cited somewhere but are not
cited by their own round's plan (102 - 71).

Verdict **survived as disclosed**: the narrowing is declared in A4 and every suppressed class is printed in the receipt,
so a reader can see the denominator. What the claim's "mismatches 0" establishes is therefore
"0 mismatches over the 21% of the tool tree the regime admits", not "the registry conforms". That is a tradeoff the
claim text already states ("over the lane's own instrument inventory"); it is not a hidden filter.

### (b) Does `scope_size 71` follow necessarily from the two plan entries plus base 69?

Arithmetic: yes, on this tree — 69 + 2 = 71, measured at HEAD and at the freeze. The two new citations are in
`plans/round-68-claims.md`, both exist at HEAD, nothing else in `plans/` changed between base and HEAD.

Necessity: **falsified**. `scope_size` is a cardinality over plan *text*, which is part of the measured tree and is
freely editable. Fixture (`c1attack2.py` §b, pure functions, no repo mutation): drop the `avm-le-counter.py` citation from
`plans/round-67-claims.md`, add an existing but uncited `tools/round-68/controls.py` to `plans/round-68-claims.md`,
delete the `avm-le-counter.py` row and add a `controls.py` row:

```
mismatches 0, scope_size 71, registry_rows 77, ok true, avm_row_present false
```

That is the predicate's exact triple while **one of the four rows the claim narrates is absent and the tool it registers
stays unregistered** — it simply left scope. Control: deleting the row without the compensating plan edit gives
`mismatches 1` (as it should). So (0, 71, 77) does not pin membership; only the arithmetic of a net-zero edit.

The count is also brittle in the other direction: naming the round's own control driver in its plan (a legitimate
disclosure — `tools/round-68/controls.py` is cited nowhere) gives `scope_size 72, mismatches 5`. The 71 breaks on a
truthful addition.

Impacted axis: calibration. The metric's denominator is derived from the artifact under measurement, so the repair can be
satisfied by shrinking the population. Smallest safe correction (judge-side, no re-freeze): the after-arm receipt must
record the **sorted scope list**, and the judge asserts `scope == base_scope ∪ {the two r68 instruments}`
(69 + 2 = 71 with membership), not the cardinality. A control arm `c1-scope-shrink` should be added at the next
instrument revision; the six committed controls cover self-compare and constant-zero, neither of which is this shortcut.

### (c) Can a row that names a *different* file pass?

**Falsified** — no. Base rows built for every existing regime path except the target, then exactly one variant row
(`c1attack2.py` §c):

| variant | target still unregistered | mismatches |
|---|---|---|
| exact (control) | no | 0 |
| `…/avm-le-counter.py.bak` | yes | 2 |
| `…/avm-le-counter.py/x` | yes | 2 |
| `…/avm-le-counter` (no extension) | yes | 2 |
| `./…/avm-le-counter.py` | yes | 2 |
| `…/avm-le-counter.py ` (trailing space in cell) | yes | 2 |
| `…//avm-le-counter.py` | yes | 2 |
| `…/avm-le-counter.py*` | yes | 2 |
| `tools/round-66/avm-le-counter.py` | yes | 2 |
| cyrillic `а` homoglyph | yes | 2 |
| `…/AVM-le-counter.py` | yes | 2 |
| doubled backticks | yes | 1 |
| path + extra cell text | yes | 3 |

Exact string equality on the cell-0 path is required, and every near-miss also lands in `row_absent` (a second mismatch).
One parsing note, low severity and fails closed: a row whose cell 0 is not a single backticked token (doubled backticks)
is **silently dropped** — it is not parsed as a row at all, so it produces neither a registration nor a `row_absent`.
A human reading SKILL.md sees a row; the census sees nothing. No forgery follows (the path is still unregistered), but a
malformed row is indistinguishable from an absent one in the receipt.

### (d) Is `thin` gameable by a cell that merely contains "0", "1", "2" in prose?

**Falsified as a guarantee.** The grammar is
`(?:^|[;|]\s*|\s)0\s*(?:[=:]|\s+[A-Za-z(])` (and 1, 2), searched anywhere in the cell:

```
python3 -B c1attack2.py §d
"note 0 (zero); item 1 (one); tag 2 (two)"      -> thin 0, mismatches 0   (no exit-code semantics at all)
"see 0 (alpha), 1 (beta), 2 (gamma)"            -> thin 0, mismatches 0
"rc 0 met; rc 1 not met"                        -> thin 1 (correctly flagged: 2 absent)
"2 of 2 carriers; 3 procedures; 0 stderr"       -> thin 1 (accidental 2 match, no 1)
```

So a cell with zero verdict content passes the arm. **Not exploded in the real registry**: all 77 rows (73 committed +
4 worktree) name all three codes. Under a stricter segment-start grammar (code at a top-level `;`/`|`/`/` segment start,
followed by `=`, `:` or a word) **77/77 remain green and the prose fixture is rejected** (`thin2.py` +
segment-start probe):

```
{"rows": 77, "rows_green_under_segment_start_grammar": 77, "prose_fixture_passes": false}
```

That is the smallest safe correction for this arm, and it costs no row. It is an instrument edit, so it can only land at
the next freeze; the current after-arm is not harmed by the hole because no row exploits it (measured).

---

## 2. R68-C2 — verdict summary

| sub-question | verdict |
|---|---|
| (a) is identity circular when the pinned original is in the same run | **survived as a statement about this packer** — it establishes `upx -d` is byte-exact here, nothing about third-party artifacts |
| (b) is `recovery_ok` a tautology given sha identity | **falsified as independent evidence** — entailed by identity + content determinism; zero added information |
| (c) is the `before` arm (3 procedures) a missing-section-header artifact | **falsified my own hypothesis; the arm survived** — a SHT-stripped *unpacked* jq yields 165 procedures, not 3 |

Reproduction first: the whole before-arm is reproducible with the **frozen** instrument at the base revision.

```
python3 -I -B tools/round-68/packed-elf.py --root <lane> \
  --rev fcbe200f6739c38939e0dabf3f251de2cc6bd727 \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work <scratch>/c2run --json-out receipts/c2-frozen-at-base.json
exit=0  met_target true  carriers_matched 2  control_ok true  failing []  before_procedures [3,3]
instrument {"rev":"6020eb6064c9196764d9921ec070e34bc9308fb9",
            "sha256":"48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e"}
jq  arms {detected,before_ok,identity_ok,recovery_ok,refusal_ok} all true
    orig 167/30/190  packed 3/3/3  unpacked 167/30/190  sections 0  ctrl rc 2/2
    refusal packed rc 1 invalid_request; unpacked rc 0, 4841 bytes, FUN_00103fa0 present
xxd arms {detected,before_ok,identity_ok,recovery_ok} all true
    orig 99/29/103   packed 3/3/6  unpacked 99/29/103   sections 0  ctrl rc 2/2
```

Field-for-field identical to `l1/pre/c2-dryrun-at-base.json`. Packed shas reproduce byte-for-byte
(`e8b6c9e7…` jq, `1727faf9…` xxd), so `upx --best` is deterministic on this build.

### (a) Identity — what sha-equality with the pin establishes

Establishes, measured: `upx --best` then `upx -d` returns bytes whose sha256 equals the carrier pin
(`upx -d -q -o back-jq packed-jq`; `sha256sum back-jq` = `e8156675…`). Byte-exact round trip for jq and xxd on
upx 5.2.0.

Does **not** establish:
- that a third-party packed artifact (unknown or modified packer, the actual triage case) unpacks to a known original;
- that the "original" is authentic against an external source — the pin is a literal in the instrument compared to
  `/usr/bin/jq` on this host, so "identity" means "unpacked == the host's own file", not provenance;
- that the packed bytes on disk were produced from the pinned original.

It is circular **in-run** in the narrow sense: the run packs the pinned original and then unpacks its own output, so the
arm is a round-trip property of one packer version. Verdict **survived**: the claim says "unpack with sha identity" and
that is exactly what it delivers; it must not be read as identification of shipped artifacts.

### (b) Is `recovery_ok` a tautology?

**Falsified as independent evidence — yes, it is entailed.** `identity_ok` asserts byte equality between the unpacked
file and the pinned original; REA's inventory is content-determined. Measured determinism (same bytes, different file
names, two carriers):

```
packed-jq 3/3/3 -> packed-jq-2ndname 3/3/3
nosh-jq 165/6/161 -> nosh-jq-2ndname 165/6/161
```

Given identity, `rec_counts == orig_counts` cannot fail except through instrument nondeterminism, so the arm is a
determinism check, not a recovery check. It is also strictly weaker than identity: two *different* byte strings with
coinciding counts would pass it, so it cannot substitute for identity when identity fails. Removing it would not weaken
the claim; keeping it does not double the evidence. (Counts *are* content-sensitive — nosh 165/6/161 vs orig 167/30/190 —
but that sensitivity is identity's job.) The claim's phrase "recover the original's REA inventory" is therefore satisfied
trivially. Verdict on the arm: **redundant, survived as harmless**; the claim should not count it as an independent arm.

### (c) Is "3 procedures" a REA artifact of the missing section header?

My hypothesis: `detected` already asserts "no section header table", so `before` (3 procedures) might be that same fact
re-read. **Falsified by the decisive fixture** — strip the section headers from the *unpacked* original, leave it
uncompressed:

```
strip --strip-section-headers -o nosh-jq orig-jq
readelf -SW nosh-jq   -> "There are no sections in this file."   (0 section entries)
file nosh-jq          -> ELF 64-bit ... dynamically linked ... no section header
upx -l nosh-jq        -> rc 2 (not packed)
REA analyze nosh-jq   -> 165 procedures / 6 segments / 161 strings
REA analyze packed-jq ->   3 procedures / 3 segments /   3 strings
```

A section-header-less but uncompressed binary still yields 165 procedures. So the collapse to 3 is **not** a
missing-SHT artifact; it is the stub.

Independent second readers on the packed bytes agree:

```
readelf -lW packed-jq -> 6 program headers, 2 LOAD (RW + R E at vaddr 0x9000), entry 0xb780
                         the code region is present only as compressed bytes
file packed-jq        -> ... statically linked, no section header
rizin -N -q -c iI packed-jq -> "WARNING: Failed to initialize section header", binsz 0x00000228 (552 B)
rizin -N -q -c iI nosh-jq   -> binsz 0x00006d80 (28032 B)
strings -n 8: orig 195 lines, packed 42, nosh 177
```

rizin sees the packed image as a 552-byte stub of a 14036-byte file — the "stub, not the program" reading is not
REA-specific. Verdict **survived**.

Refusal arm, bonus measurement — it is not an address-range artifact either:

```
readelf -lW packed-jq -> max LOAD vaddr 0x9000 + 0x33aa = 0xc3aa, so the pinned 0x103fa0 is out of range
decompile packed @0x103fa0 -> rc 1 invalid_request
decompile packed @0xb780   -> rc 1 invalid_request   (entry, INSIDE the packed image: still refused)
decompile back-jq @0x103fa0 -> rc 0, 4841 bytes, FUN_00103fa0 present
decompile nosh-jq @0x103fa0 -> rc 0, 4841 bytes, FUN_00103fa0 present
```

A blanket refusal on packed bytes, not an out-of-range refusal; and it follows the bytes, not the section table.

### C2 defects found (none of them falsify the predicate; all need routing)

1. **The `before` arm is a floor, not the predicate's 3.** `before_ok = packed_procedures < min_orig_procedures // 2`
   (50 for jq, 25 for xxd). A run reporting 49 procedures would be green and violate the predicate's "exactly 3
   procedures". Exit 0 therefore does **not** entail the predicate; L1 must assert `before_procedures == [3,3]` from the
   receipt (it is recorded). Observation: current value is 3/3.
2. **The upx pin has no value and is never enforced.** `packed-elf.py:53  UPX_SHA256 = None  # set at run time` — the
   constant is never assigned or compared (grep: only the definition and the receipt field; `upx_env` computes
   `sha256_file(UPX)` and records it). The docstring says "the packer is /usr/bin/upx pinned by sha256 and version", and
   A6 says "the packer /usr/bin/upx by sha256 and version" — but A6 names **no value** and the code checks none. The same
   atom explicitly distinguishes "RECORDED … never pinned" for the npx lock, so its vocabulary does distinguish the two,
   which makes A6 false as written: a pin with no pin value. Observed: `/usr/bin/upx` sha256
   `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`, version `upx 5.2.0`. Judge-side correction
   (no re-freeze): require the after-arm receipt's `packer.sha256`/`packer.version` to equal the values the round
   declares, and declare them. Instrument-side (next freeze): compare or drop the word "pinned".
3. **`detected` can be true on a failed readelf.** `section_count("") == 0` and
   `section_count("readelf: Error: Not an ELF file") == 0` (measured on the pure helper), and `detected = upx -l rc 0
   AND sections == 0`. The readelf run is not recorded in the receipt (only the derived integer), so a receipt cannot
   distinguish "no sections" from "reader failed". Latent: a failing readelf would have to coincide with `upx -l` rc 0.
   Correction: record the readelf run and require rc 0, or record `readelf_ok`.
4. **The committed before-arm receipt is not attributable to the frozen instrument.**
   `l1/pre/c2-dryrun-at-base.json` records `instrument.sha256 = 7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c`;
   `l1/pre/c2-skiprun.json` records `ff11d8ec27cbce94b4790041ed4e0dc4dfffa241cb243ece24e08491c415a302`. Neither is the
   frozen `48ef4c68…`, and neither exists in any commit (`git log --all -- tools/round-68/packed-elf.py` lists four
   commits and **all four** blobs hash to `48ef4c68…`). The container declares `instrument_supersessions: []`. The
   controls driver consumes the `7ee286c0` receipt for its `c2-real` arm, so that control inherits the mismatch.
   The measurement itself is unaffected — my frozen-instrument rerun above reproduces every field — but the receipt in
   the container evidences a build that was never committed. Correction: replace
   `l1/pre/c2-dryrun-at-base.json` with a frozen-instrument receipt (one exists:
   `receipts/c2-frozen-at-base.json`), or disclose the supersession in the container.

---

## 3. Cross-cutting: A9 / revision naming

A9 requires receipts to name "the measured revision (rev) and the revision that bears the instrument (instrument.rev)".
Measured on the committed pre receipts:

```
git show 6020eb60:.ufo/waves/round-68/l1/pre/c1-at-base.json   -> rev "main", instrument.rev null
git show 6020eb60:.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json -> rev "main", instrument.rev null
```

`rev` is the argv string, never resolved (`result["rev"] = rev`), so a receipt run with `--rev main` names a branch, not
the revision that was measured — the base arm cannot be re-bound to `fcbe200…` from the receipt. `instrument.rev` is null
because the receipts were generated before the instruments were committed (they were then committed *with* them at
6020eb60; `git log --diff-filter=A -- …` = 6020eb60 for all three). My reruns show both fields populate correctly when a
sha is passed and the file is committed (`rev fcbe200…`, `instrument.rev 6020eb60`).

This is the same class as the round-67 routed defect 6 that A9 exists to close: the receipt records an alias, not a
binding. Correction (cheap, operator-side): pass a full sha to `--rev` for every scored run; optionally have the
instrument record `rev_resolved = git rev-parse <rev>^{commit}` and require 40-hex.

---

## 4. Impacted axes and smallest safe corrections

- **calibration (R68-C1).** Repair is real and minimal: base 2 → the four rows → 0, with the worktree text scoring
  exactly (0, 71, 77). Vulnerabilities, both latent: `scope_size`/`registry_rows` are counts over artifacts the round can
  edit (plan text, the registry itself), so the predicate does not pin membership — demonstrated with a different tree
  that is green while `avm-le-counter.py` stays unregistered — and `thin` accepts prose. Smallest safe corrections:
  judge-side scope-set equality and a `before_procedures`-style value read; instrument-side segment-start thin grammar
  (77/77 rows stay green) and a `c1-scope-shrink` control at the next freeze.
- **coverage (R68-C2).** Route is real, reproducible, and independently corroborated (rizin, readelf -l, strings,
  SHT-stripped control). Vulnerabilities: `recovery_ok` is entailed by identity (redundant arm, not an error); the upx
  "pin" has no value and is not enforced (A6 false as written); `detected` conflates "no sections" with "readelf
  failed"; and the before-arm receipt names an uncommitted instrument build. Smallest safe corrections: judge-side value
  assertions on `before_procedures`, `packer.sha256`, `packer.version`; replace the before-arm receipt with the
  frozen-instrument rerun; record/require readelf rc at the next freeze.

**Reject vs tradeoff.** Nothing here falsifies either predicate as measured. What the canonical judge must **not** accept
as evidence: (i) `l1/pre/c2-dryrun-at-base.json` as a receipt of the frozen instrument, and its `c2-real` control
inheritance; (ii) the "0, 71, 77" triple as proof that the four rows were added — it is proof of a count; (iii) A6's
"pinned by sha256 and version" as an enforced pin. Everything else is a disclosed narrowing or a redundant arm.

**Unknown.** Whether the uncommitted four-row diff is byte-identical to what the build seat commits (I scored the
worktree text at review time; the commit may differ). Whether the older `7ee286c0`/`ff11d8ec` builds differ semantically
from the frozen one — the bytes are gone; my frozen rerun supersedes the question empirically.

---

## 5. Command log (every number above)

```
# fingerprints / environment
sha256sum tools/round-68/*.py; upx --version; sha256sum /usr/bin/upx /usr/bin/jq /usr/bin/xxd
sha256sum /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json; node --version

# C1 census at three revisions (frozen instrument)
python3 -I -B tools/round-68/registry-conformance.py --root <lane> --rev <base|HEAD|freeze> --json-out <scratch>/…
# C1 pure-function scoring of the worktree SKILL.md
python3 -I -B c1probe.py
# C1 widenings + different-file rows + different-tree fixture + prose fixtures
python3 -I -B extract.py <rev>; python3 -I -B c1attack2.py; python3 -I -B thin.py; python3 -I -B thin2.py

# C2 carriers + second readers
cp /usr/bin/jq orig-jq; upx --best -q -o packed-jq orig-jq; sha256sum orig-jq packed-jq
upx -l packed-jq; upx -l orig-jq; readelf -SW packed-jq; readelf -lW packed-jq; file packed-jq orig-jq
rizin -N -q -c 'iI' packed-jq; rizin -N -q -c 'iI' nosh-jq; strings -n 8 <f> | wc -l
strip --strip-section-headers -o nosh-jq orig-jq; readelf -SW nosh-jq; upx -l nosh-jq
node <pkg>/scripts/rea.mjs analyze --format json <packed|nosh|orig>-jq
node <pkg>/scripts/rea.mjs decompile packed-jq 0x103fa0|0xb780 --format json
node <pkg>/scripts/rea.mjs decompile back-jq|nosh-jq 0x103fa0 --format json
upx -d -q -o back-jq packed-jq; sha256sum back-jq; upx -d -q -o dtest-out dtest-jq

# C2 frozen-instrument end-to-end at the base revision
python3 -I -B tools/round-68/packed-elf.py --root <lane> --rev fcbe200f… --pkg <rea> --work <scratch>/c2run \
  --json-out receipts/c2-frozen-at-base.json      # exit 0, met_target true, [3,3]

# provenance
git log --all --format='%H' -- tools/round-68/packed-elf.py
git show <c>:tools/round-68/packed-elf.py | sha256sum   # all four = 48ef4c68…
git log --diff-filter=A --format=%H -- .ufo/waves/round-68/l1/pre/<receipt>
python3 -I -B tools/round-68/registry-conformance.py --selftest   # 11 cases green
python3 -I -B tools/round-68/packed-elf.py --selftest             # 13 cases green
```

Tooling: nothing installed, nothing upgraded; no package manager transaction was run (pacman is paused host-wide); no L0
question. Every path written is absolute, inside this seat's wave directory or its scratch, which was deleted at exit.
