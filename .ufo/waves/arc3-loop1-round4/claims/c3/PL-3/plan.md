# PL-3 — C3 plan: custody-pair residual closures (four closures + the landed gap analysis)

Seat PL-3 · chain c3 · role planner · wave `arc3-loop1-round4` · 2026-10-19.
Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. No git mutation; no custody
path written, renamed or `utime`d (read-only sha256/stat capture only); scratch
`/var/tmp/pl3` only (never `/tmp` — standing EDQUOT rule). Every file written by
this seat is under `claims/c3/PL-3/`.

## 0. Status: the plan's primary content is a GAP ANALYSIS, not a fresh patch

**The seat line's premise no longer holds.** It says "plan C3 (custody residuals):
the four closures … patch sources `round3/claims/c2/{EX-24,CR-3,CR-4,RV-8}/`". By
the time this seat could measure, **C3's designated writer (EX-21) had already
landed all four closures in the real target**:

| object | r3 landed (my before-state) | landed during this wave |
|---|---|---|
| `.ufo/gates/custody-pair/custody-pair.py` | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 L) | **`29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`** (1343 L) |
| `.ufo/gates/custody-pair/README.md` | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` (185 L) | **`9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`** (272 L) |

Evidence: `evidence/identities.txt`, `evidence/live-vs-base.diff` (283 lines),
`EX-21.md` §1-2 in the same wave's seats dir. EX-21's own report records that it
polled `claims/c3/` twice, found no PL-3 plan, and proceeded on the named patch
texts per its seat line's fallback clause — **not a defect of this seat**; the
schedules simply interleaved. This plan therefore does the thing that is still
worth doing and cannot be duplicated: **re-measure the four closures first-hand on
the landed bytes, prove the new selftest cases are load-bearing, and name what the
landing did NOT close.**

So: no candidate patch is required for (a)-(d). A validated fallback candidate
exists anyway (`candidate/`, §5) in case the landing is reverted; it is not the
recommendation.

## 1. Identities (rule #14 — re-derived at write time)

| file | sha256 | lines |
|---|---|---|
| `gen-candidate.py` | `e40e0d953162365807cc9e9a128e2282a4c80ff499fc75a434ed823eaf81142a` | — |
| `candidate/custody-pair.py` | `35d0c2f09af19b109ad4e31a0cc8c97c5d96c59fa9d5c2fc14c98d99d6a281f1` | 1285 |
| `candidate/README.md` | `5b048ebcb34a408c55681dc7ca698b1a1dd788df1710d1085f6fa2b097f00110` | 230 |
| `evidence/identities.txt` | `dcb73619be60e1b9272d62a9e88a6dc3fc12f958291c820d1f73890cc20fce1f` | — |
| `evidence/a-sidecar.txt` | `b9fa5e7054e17053804dc4a210074cba30bdf72a805571dddd8a8394e065d84a` | — |
| `evidence/b-mkdir.txt` | `466b65c0811954314eead77152809a4d219e866a31314d946295366d329cceb0` | — |
| `evidence/c-coverage.txt` | `f2e3c782f605cb1734b398d529649568b90063a7bbabb4f5158b3de149852f50` | — |
| `evidence/d-both-absent.txt` | `90ae00f7e8e3d86eb0ffbd1f75e0644d10bee63c4020e7136a81b8b820664e7c` | — |
| `evidence/g1-unstattable-failopen.txt` | `ad0ab5c3b1f53e3f9263c0ff777a77abe9145aa28ee26f22bd3a57f1dd81b4e6` | — |
| `evidence/g2-hardlink-coverage.txt` | `a72dd73f7e8ec4470fd13cec0b464c538f64cc16fc0d72b75bd52fc5c1e7b209` | — |
| `evidence/g3-stale-surfaces.txt` | `790b308e618fe5d1c721f353aaa1f9fd08bd3863f1a25ca47ff272a840b124dc` | — |
| `evidence/g4-sabotage-arms.txt` | `530576c38adc95b5ee0030ea469abd80fce2d505fe9ebde8eae48358a0a3729a` | — |
| `evidence/g4-mutant-build.py` | `8c5997654f4e707553739c2eb8076b23d635892010b68c2e0bf9956db51ca8fe` | — |
| `evidence/live-vs-base.diff` | `1bef563892bf4b6da2f264de7cbc6dc9d2314234cef638430ae7383ec54d3298` | 283 |

Sabotage mutants (built on scratch from the landed bytes, one hunk reverted each):
`M1-no-sidecar-arm` `7a15ddab8c52b73519876344aac8b9b5157b2c9ac0eff0be6adb7742e5ac3d06`,
`M2-stanza-count` `ca3680dd63dc09bab7005e0e082d8d94946180944eef63e3b7172327e400010d`,
`M3-unguarded-mkdir` `b252f5f45ee8c9df3d7b2999463ad75545d572a7470e2150fcd45789e91e2664`,
`M4-no-absent-note` `e10e9fe8d06c0b64993709beacd8997c386a4318d23c15d7cf2164b2f8536d38`.

Rebuild them with `evidence/g4-mutant-build.py`
(`8c5997654f4e707553739c2eb8076b23d635892010b68c2e0bf9956db51ca8fe`) — it pins the
landed base digest, asserts each hunk occurs exactly once, and reproduces all four
digests above on a fresh run (verified).

## 2. The four closures, measured first-hand base → landed

### (a) sidecar scope — CLOSED as declared `USAGE 2`

| vector | before `7cd19c3c…` | landed `29bb45ae…` |
|---|---|---|
| `--out vic --paths vic.sha256` | **exit 0**, `vic.sha256` clobbered `e5e88eba…`→`3cc33fc7…` | **exit 2**, sha unchanged `e5e88eba…` |
| symlinked sidecar `alias.sha256 -> vic.sha256`, `--out alias --paths vic.sha256` | exit 0, **measured file clobbered** (my own added vector) | **exit 2**, `measured-vic` intact |
| mirror direction `--out X.sha256 --paths X` | exit 0 (r3; RV-8 gap 2) | **exit 2**, no neighbour, no second sidecar |

Evidence `evidence/a-sidecar.txt`. Note this seat's third vector is **stronger than
either r3 patch text asked for**: the landed guard's neighbour set
(`{Path(str(g) + ".sha256")}`) refuses the receipt aimed at a measured file's
sidecar-shaped neighbour, which is what closes the mirror direction that RV-8's
minimal text correction ("drop the words 'or sidecar'") would have left open.

### (b) `out.parent.mkdir` guard — CLOSED as declared `USAGE 2`

| injection | before | landed |
|---|---|---|
| `--out <regular-file>/rec.txt` | `FileExistsError` traceback, exit 1 | `USAGE: cannot create the receipt directory ([Errno 17] …)`, exit 2, 0 traceback lines |
| `--out <regular-file>/sub/r.txt` | `NotADirectoryError` traceback, exit 1 | `USAGE: … ([Errno 20] Not a directory …)`, exit 2 |
| `--out ''` / `'.'` / `'/'` (CR-4 item 6 trap) | USAGE 2 (base already correct) | USAGE 2, message `--out carries no usable name, so no sidecar path can be derived` |
| ordinary fresh nested parent (no-over-refusal control) | exit 0 | **exit 0** |

Evidence `evidence/b-mkdir.txt`. CR-4 item 6 warned that the naive sidecar fix
(`Path("").with_name(...)`) turns `--out ''` into a `ValueError` traceback; the
landed code derives the sidecar inside a `try/except ValueError` and returns
USAGE — the trap is closed, verified by direct probe.

### (c) distinct-path coverage counting — CLOSED as declared `USAGE 2`

| vector | before | landed |
|---|---|---|
| `v2-dupe-5x` (5 stanzas, 1 path) `--require-paths 5` | **exit 0**, `MATCH paths=1`, 0 coverage lines | **exit 2**, `REFERENCE-COVERAGE: 1/5 …` |
| `v1-dupe-5x` (sums shape) `--require-paths 5` | exit 0, `MATCH-V1-PARTIAL` | **exit 2**, `1/5 …` |
| canonical 5-path reference `--require-paths 5` | exit 0 | exit 0 `MATCH 5/5` (no false positive) |

Evidence `evidence/c-coverage.txt`, fixtures from
`round3/claims/c2/EX-24/fixtures/`. `distinct_paths()` returns the resolved-path
set and `reference_coverage()` counts it, so count and `unaccounted:` share one
basis — exactly EX-24's proposed change, extended to the USAGE message wording
("distinct paths").

### (d) both-sides-absent MATCH — ADJUDICATED and documented, behavior kept

Ruling: **declared design, kept, and annotated in the run output.** Landed
behaviour, re-measured: both sides absent → `MATCH compared=0/11 exit 0`, now
carrying the note `both sides record the path absent — the MATCH is an agreement
on absence, not a verified presence (declared ruling: only error-carrying stanzas
are UNEVALUABLE)`; an error on either side stays `UNEVALUABLE 14`; receipt
`EXISTS: no` vs a live-present path reads `ABSENT 13` (asymmetry control measured,
both directions). Evidence `evidence/d-both-absent.txt`.

This matches the frozen claim's own words — "adjudicate and document (declared
design: only error-carrying stanzas are UNEVALUABLE) or close with a flag, per the
wave's evidence". The wave's evidence (r3 `verdict.md` §R-item, EX-28's A3,
EX-26's F2) supports keeping it, so the flag option is correctly **not** taken.

## 3. Selftest: the claim's 22 → ≥24 bar

Landed: **`CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`**
(`evidence/g3-stale-surfaces.txt`). The claim asked ≥24; 28 clears it, and the
r3 twenty-two names are all retained.

**Sabotage arms — each landed round-4 case is load-bearing** (`evidence/g4-sabotage-arms.txt`):

| mutant (one hunk reverted) | result |
|---|---|
| M1 drop the sidecar from the guard candidate list | DIRTY 27/28 — `refuses-sidecar-over-measured-file` FAIL (and the clobber returns) |
| M2 restore the stanza-count basis | DIRTY 27/28 — `coverage-gate-rejects-duplicate-stanzas` FAIL |
| M3 move `mkdir` back outside the guard | DIRTY 27/28 — `out-parent-not-a-directory-usage-exit` FAIL (traceback at exit 1 returns) |
| M4 drop the both-absent row note | DIRTY 27/28 — `both-sides-absent-is-agreement-match` FAIL |

Each arm fails **exactly one** case — the coverage is additive and each closure is
fenced by its own case. (Independent corroboration: VZ-3's verdict §2 row 5
records three of its own mutants with the same isolation property.)

## 4. What the landing did NOT close — the planner's actionable output

### G1 — the inode arm fails open when the measured path is unstattable (OPEN, not in the frozen four)

**This is a real, first-hand-measured hole at the landed revision, and no r4
artifact names it** (searched: `grep -rli 'unstattable'` over
`.ufo/waves/arc3-loop1-round4/` returns only this seat's own evidence file).

Shape (`evidence/g1-unstattable-failopen.txt`):

```
measured : <sandbox>/blocked/watch.conf   (parent chmod 000 — lstat fails)
out      : <sandbox>/outside/alias.conf   (hardlink of the measured file)
$ capture --out outside/alias.conf --paths blocked/watch.conf
exit=14                                   # UNEVALUABLE, the declared class
RECEIPT: outside/alias.conf  sha256=c6bcd18d…   # the receipt landed ON the measured inode
victim: 31737209… → c6bcd18d…             # the measured file was DESTROYED
control: same hardlink alias with a stattable measured path → exit 2, refused
```

`_same_file()` wraps `os.stat` in `try/except OSError: return False`, so when the
scoped path cannot be stat'ed the inode arm silently reports "not the same" and
the tool clobbers a file it simultaneously records as unevaluable. This is
**r3 `CR-4/proposed-write-guard.patch.md` item 8**, deliberately left out of the
frozen four (it was not in the wave's named debt), and it survives the landing.
Severity: low under the declared threat model (an actor able to create the alias
can already write the file), but the contract sentence is absolute and is untrue
for this class:

- tool docstring item 5 (landed): "refuses `--out` when the output would resolve
  to — or share an inode with — any path being captured"
- README (landed): "…or by inode (a hardlink alias is refused too)"

**Recommendation (parent's call, one of two, both small):** either (i) fail
closed — refuse `--out != '-'` when any measured path carries `stat_error` (the
alias check cannot be proven; the receipt can still be produced with `--out -`),
or (ii) amend both contract sentences with the caveat and file the residual. A
fencing selftest case (`refuses-out-when-measured-path-is-unstattable`) should
accompany (i); the existing `unevaluable-never-matches` case covers the verify
side but not this guard arm.

### G2 — coverage gate counts distinct NAMES, not distinct FILES (OPEN, already named by VZ-3 §R5)

Re-measured first-hand at the landed bytes: five hardlink names for **one** inode
capture `OK paths=5/5` and verify `--require-paths 5` → `MATCH 5/5 exit 0`
(`evidence/g2-hardlink-coverage.txt`; `stat` shows one inode `12115289`).
This is EX-25's patch text (`proposed-hardlink-inode-key.patch.md`) and VZ-3's
§R5. **It is not a defect** — the landed unit is "distinct resolved path names",
which is what its own `unaccounted:` list uses, and the gate is honest about what
it counted. Recorded here as the third of the wave's unit-scope limits, with the
inode-key or `--require-custody-set` forms available as an opt-in.

### G3 — wording: the coverage line still says "paths present", not "distinct paths" (OPEN, cosmetic)

The landed USAGE *message* says "distinct paths" and the README §D3 says
"**distinct resolved paths**", but the emitted `REFERENCE-COVERAGE:` line itself
still reads `%d/%d paths present in reference` (`custody-pair.py` line 649), as
does the docstring at line 47. EX-24's patch text asked for the line's count to
share the basis — it does, numerically (`len(have)`); only the noun is stale.
One-word fix, no behavior change; worth folding into whatever commit lands next
(the tool's bytes are otherwise frozen by the receipts' self-pins, so this is a
"next revision" item, not a reason to re-cut this one).

### G4 — the SKILL.md registry row is still unapplied (OPEN, the claim's own leg)

`SKILL.md` remains `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f`
(390 L) and its `custody-pair` row still says **"22 fixture cases"** (count 1) with
no "distinct" token and no "sidecar-shaped neighbour" token
(`evidence/g3-stale-surfaces.txt`). EX-21's patch text
(`EX-21/patch/skill-registry-row.patched.md`, `8e56f3d9…`) is sound, line-neutral
(390 → 390, exactly one line changed, all graded anchors alive — this seat
re-verified the line counts, the single `| custody-pair |` row, and the
precedence anchor). VZ-3 §R1 reached the same conclusion; this seat's independent
counts agree. **The parent applies it in the same commit as the gate pair.**

## 5. Fallback candidate (validated, not recommended)

`candidate/` holds this seat's own anchored generator output — an independent
implementation of the same four closures from the pinned r3 base:

- `gen-candidate.py` asserts every anchor occurs **exactly once** and refuses on a
  moved base (it refused correctly at first run, which is how the mid-wave landing
  was detected); 12 anchors, all `anchor ok`.
- Candidate tool `35d0c2f0…` (1285 L): selftest **26/26 CLEAN**; closes (a) for
  `--out X --paths X.sha256` and the symlinked-sidecar form, (b) for both mkdir
  shapes, (c) with `REFERENCE-COVERAGE: n/N distinct paths …`, and annotates (d).
- **Known gap vs the landed version:** my candidate does **not** close the mirror
  direction `--out X.sha256 --paths X` (measured: still exit 0) because it lacks
  the neighbour set the landed guard added. The landed revision is strictly
  stronger; do not prefer the candidate.

## 6. Claim bar — before → after for the C3 claim

| claim element | required | measured at the landed revision |
|---|---|---|
| (a)-(c) closed with declared classes | yes | **yes** — USAGE 2, all three; both sidecar spellings |
| (d) adjudicated, ruling in README | yes | **yes** — ruling section landed, run-output note landed |
| selftest 22 → ≥24 with new fixtures | yes | **yes — 28/28 CLEAN** |
| sabotage arms | yes | **yes** — 4 mutants, each fails exactly its own case |
| registry row + README re-derived same-commit | yes | **README yes; row NO** (G4, patch text ready) |
| live pair (revised tool) MATCH 5/5 | yes | **yes** — EX-21's pair self-pins `29bb45ae…`, both sidecars `OK`; this seat's own fresh pair also `MATCH 5/5`; the r3 pair re-verifies `MATCH 5/5` under the landed tool |
| every receipt self-pins the new sha256 | yes | **yes** — `# tool: … 29bb45ae…` in both |
| command A unchanged | yes | **yes** — 83/83, 14/14, 10.0/10.0 at HEAD `015e1ba` |

## 7. Attacks / refutations attempted, with verdicts

| # | attack | verdict |
|---|---|---|
| A1 | "the landed fixes are cosmetic (exit-code theatre)" | **REFUTED** — each before-state was destructive or traceback-class: the sidecar vector destroyed a measured file, the mkdir vector died at exit 1 outside the declared map, the padded reference passed the gate silently. After: bytes unchanged, declared class, gate refuses |
| A2 | "the new selftest cases are decorative" | **REFUTED** — four mutants, each failing exactly its own case (G4 evidence) |
| A3 | "the (a) fix over-refuses ordinary runs" | **REFUTED** — fresh parents, cross-directory neighbours, distinct five-path references, and canonical 5/5 pairs all stay exit 0 |
| A4 | "the (a) fix introduces the `--out ''` ValueError (CR-4 item 6)" | **REFUTED** — `''`, `'.'`, `'/'` are declared USAGE 2 |
| A5 | "the (c) fix breaks legitimate distinct-path references" | **REFUTED** — 5 distinct paths `MATCH 5/5 exit 0`; the canonical r3 pair still `MATCH 5/5` gated |
| A6 | "the (d) ruling is a costume over a fail-open" | **PARTIALLY SUSTAINED, then bounded** — the both-absent MATCH *is* a vacuous pass (`compared=0/11`, `SHA256-CONTRACT: 0/0`) and an all-absent 5-stanza reference passes the gate and reads `MATCH 5/5` (VZ-3 §R4). It is bounded by the declared ruling + the run-output note, and the frozen claim chose adjudication. Records must not quote it as a content witness |
| A7 | "the contract sentences are true as written" | **REFUTED for one class** — G1: the inode arm does not refuse when the measured path is unstattable, and the file is clobbered at exit 14. Not named by any other r4 artifact |
| A8 | "the distinct-path gate is a distinct-file gate" | **REFUTED** — G2: five hardlink names, one inode, gate passes. Declared unit is names; recorded as a unit-scope limit |
| A9 | "the landing is complete (row included)" | **REFUTED** — G4: `SKILL.md` byte-unchanged, row still "22 fixture cases" |
| A10 | "PL-3's absence blocked the chain" | **REFUTED as a blocker, SUSTAINED as a schedule fact** — EX-21 proceeded on the named patch texts per its fallback clause and landed a correct revision; this seat's plan is therefore gap analysis, and the one thing it adds that no other seat measured is G1 |

## 8. Blockers

None for this seat's own task. Two facts the parent must carry:

1. **The landing already happened** (tool `29bb45ae…`, README `9d9400da…`), so this
   plan is not a pre-landing artifact; it must be read as the post-landing
   verification + gap list.
2. **G1 (unstattable fail-open) is unrecorded elsewhere** — if the parent wants it
   closed, it needs a new tool revision, which voids every receipt that self-pins
   `29bb45ae…` (EX-21's live pair and the round's records). Cheapest correct path:
   land it in the *next* round with a fresh pair, or amend the contract sentences
   now and file it as named debt.
