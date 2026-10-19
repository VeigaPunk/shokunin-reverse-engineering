# CR-2 seat report — arc3-loop1-round4, chain c2, role critic

Seat CR-2 | chain c2 | critic | 2026-10-19 | repo HEAD
`015e1bab914713568f339fd53999bc180459cc40` (re-checked with `git rev-parse`;
unchanged through this seat's work). Task: attack — repair overreach (rewriting
current text, scope creep into PROVINCE's authority/boundary statements,
availability→holding language); check every patch text.

Writes by this seat: this report + `claims/c2/CR-2/` only. No git mutation; no
PROVINCE/SKILL/SCORECARD/corpus/README/LOG write; custody paths never opened.
Scratch under `/var/tmp/cr2` (never `/tmp`). Lane: devin
(`devin/deepseek-v4-1-flash-max`) — the declared fallback dispatch, not a lane
signal.

## 1. Work performed (evidence pointers)

**Instruments built by this seat** (all copied under `claims/c2/CR-2/evidence/`,
self-tested before use):

- `scan-all-patches.py` (`a032c8ae…`) — byte-level conformance sweep: for every
  fenced `-`/`+` hunk of every patch text, every context and `-` line must be
  byte-equal to a base line, and `#-` must equal `#+` (line neutrality). Ran
  over **20 patch files / 64 hunks**; transcript `scan-all-patches.out`
  (`d83eaca6…`).
- `overreach-check.py` (`a9cba2cd…`) — the seat-line checker in four classes:
  CLASS1/1b (edit outside the claim's declared census unit; Core-table edits
  split out), CLASS2 (authority/boundary clause touched in any *changed span*,
  via difflib opcodes against a 14-regex authority inventory), CLASS3
  (net-new holding language, block-scoped, with qualifier exemptions), CLASS4
  (promotion language: `(Core, …)` naming a leg whose corpus entry reads
  "RESULT-class, no Core promotion"); plus census-UNDECLARED hazard detection
  and the pinned invariants (PROVINCE.md:18 needles, SHONEN:12→88-116 range).
  Self-test: 5 hand-built positives all fire; baseline-vs-baseline CLEAN.
- `scratch-verify.sh` (`58a15dd4…`) — one-command pipeline: fresh `git clone
  --shared` → apply → overreach → census → RV-4 `census-diff.py` → citation-drift
  probe at a scratch commit. This covers a gap in RV-4's harness, which runs the
  census but **not** the probe.

**Patch texts checked (21 applied candidates, each on a fresh scratch clone):**
EX-14's demo (`507b0061…`), complete v1 (`8a0e12ff…`), complete v2
(`0b8ad045…`); EX-11 A–D; EX-13's seven (evm, pe-subtypes, jeb, crashes,
fallback-readers, cross-version, pe-wall); EX-12 asar row; PL-2
`candidate-repairs` and `candidate-with-s5`; RV-5 f2b and x2; EX-15's
8-hunk landing set (A6a variant — its hunks 6/7 are mutually exclusive by
design); plus this seat's corrected variant. Gate table: `final-gate-table.out`
(`20f043d8…`).

**Baselines re-derived first-hand:** PROVINCE.md `d075a3c6…` / 162 lines;
census v10 `d0772ce8…` PASS 0/0/0/0; probe `e2665074…` findings=0; command A
83/83, 14/14, 10.0/10.0 at HEAD.

**Independent staleness derivation** (the attack's ground truth): all five
Frontier bullets checked against admitted corpus state by this seat —
`cli-arm64.exe` 136 procedures (r3-08 entry); 91.6MB target held mitigated
(arc2-r7) + r8 no-disable control OOM at 9G; JEB probe refusal
(`r2-provider-capability-matrix.md:99`, `r12-02:203`); macOS `unsupported_host`
×10; EVM bullet doubly stale (r1 + r3 entries). Vyper leg cross-checked on
C1's live artifacts: EX-03's `runtime.hex` carries **all 22** ABI-derived
selectors at valid dispatch sites (my own probe run re-derived 22/22 at
`ev_6b8a15c4…`, decoded `1846469bd2…`, matching EX-06's envelope), and the
PUSH4 census shows the 9 "missing" selectors of EX-03's decoder each collide
on a `% 22` slot with a recovered partner — **EX-03's `dispatch-decode.txt`
(13/22 PARTIAL) is the faulty instrument**, not the probe.

## 2. Proposed changes (patch-text paths)

- `claims/c2/CR-2/proposed-x1-context-fix.patch.md` (`1ac7b43d…`) — the X1 hunk
  with its malformed context line repaired (context-free `-`/`+` hunk, so it
  applies at `--fuzz=0`). Measured: exit 0 both dry-run and apply, 162 → 162
  lines, after-sha `db692fcf…`; transcript `x1-context-fix-run.out`
  (`93b8dd28…`). Land instead of EX-14 v2's hunk 6.
- `claims/c2/CR-2/proposed-corrected-complete.patch.md` (`66490480…`) — EX-14
  v2 hunks 1–5 + this corrected hunk 6 as one artifact. Measured on a fresh
  clone: census PASS, census-diff CLEAN, probe findings=0, 162 lines,
  after-sha `8bb35a2cf158…`.
- No change proposed to any seat's authority over its own patch text; the
  corrected artifact is offered for the parent's landing decision.

## 3. Before → after measurement for the chain's claim

The frozen claim: *stale count N → 0; PROVINCE line count unchanged; census
PASS at the work tree after the parent applies the patches.*

| unit | before (HEAD) | after (each candidate, scratch) |
|---|---|---|
| PROVINCE.md | `d075a3c6…` / 162 lines | 21/21 applied candidates **162 lines** |
| census v10 | PASS 0/0/0/0 | PASS 0/0/0/0 on 21/21 |
| census-diff (RV-4) | — | CLEAN, 0 new gated loci on 21/21 |
| citation-drift probe | findings=0 | findings=0 on 21/21 |
| byte conformance | — | 62/64 hunks byte-clean over 20 patch files; **2 defects, both the same X1 context line** (EX-14 v1 + v2) |
| overreach checker | — | 12 CLEAN; 9 flagged (details §4) |
| `patch --fuzz=0` | — | v2 fails 5/6 hunks; corrected artifact fails 4/6 (EX-14 v2's remaining four hunks are leading-context-only and are inherently fuzz-tolerant — see §4 A3) |

Stale-count: VZ-2's instrument reads `stale=9` — **identically on the base and
on every patched tree** (its verdicts are literal arguments to `add(...)`; only
`claim_present` is computed from the document). It cannot certify the
after-state; the after-state certificate is the per-candidate clause audit
(e.g. EX-14's `v2-clause-audit.txt` shows 6/6 old literals gone, and this seat's
sweep reproduces all six). VZ-2's own script was revised mid-wave
(`e6eef574…` → `7facc43f…`, 26 → 28 rows), so the chain verdict's quoted
identity is stale against the delivered bytes.

## 4. Attacks / refutations attempted, with verdicts

**A1 — repair overreach: rewriting current text / wrong column.** CLASS1/1b
fired on 9 candidates, every time for the same reason: they edit **Core-table
rows outside the claim's declared census unit** (Frontier bullets +
surface-summary claims). `:62` (host fallback readers) in EX-14 v2, EX-13-fall,
PL-2 ×2; `:46`/`:50` in EX-15 and PL-2; `:49` in EX-12.
**Verdict: sustained as a classification finding, not as a falsehood** — every
one of these repairs is *true* (I re-derived each: `7z`/`xxd`/`radare2`/`strace`/
`upx` present at `/usr/bin`, Ghidra Features = 34 dirs, pacman cache 1350 vs
1556, 12 `.asar` on host vs 9 named). The defect is that the claim's own count
("stale N → 0") is computed over a declared unit, and folding Core-table rows
into it widens what is counted without saying so. EX-15 and EX-12 do name their
Core items as out-of-unit/additions; **EX-14 v2 does not** — it lands `:62`
inside a patch whose header reads "4/6 stale rows". *Reported for the parent's
counting decision; none of it voids a repair.*

**A2 — availability → holding language.** CLASS3, block-scoped:
**1 sustained** (EX-14 v1 and demo: `real solc-0.8.37 carriers (Core, arc3-r1);
vyper-compiled bytecode untested` — the "Core" is the defect, below), and the
two remaining hits were **refuted after refinement**: EX-11-A `:83`
("91MB Godot ARM64 template held (arc2-r7)") and EX-11-C `:139` ("HELD at arc2
r7") use *held* for the analyzed **target/wall**, which is the lane's own
established vocabulary (`corpus/README.md:22` "the 91.6MB Godot ARM64 PE HELD";
`:175` "CLOSED, not frontier"). EX-14 v2's `:92` (`legs held K/K
(RESULT-class)`) is qualified in its block. **No capability claim anywhere
reads availability→holding unqualified.** Census G7 agrees (its own `held`
detector fires on none of the patched trees).

**A3 — the X1 malformed hunk (hard defect).** EX-14 v2 hunk 6 carries a context
line `…compare-application-versions is no longer` that is not in the base
(base: `still`). Reproduced byte-for-byte. Mechanism, measured on minimal
cases: a hunk whose only context is a leading line fails `--fuzz=0` even when
that context is *correct* (t1), unless it reaches EOF or carries trailing
context (t2); with default fuzz=2, a **wrong** leading context is tolerated and
the `-`/`+` replacement applies anyway (t4) — which is exactly what happens to
v2: the applied tree reads `:157 still` / `:158 refused since r2: r12-02
drained the row…`, a sentence asserting both the r2 refusal and its own
falsification. **Verdict: sustained.** RV-4 recorded this class on an earlier
revision (`defect-ex14-v2-malformed-hunk4.txt`); it **survives into the current
v2 bytes** (`0b8ad045…`). The chain verdict and EX-14's own clause-audit both
quote the repaired form ("is no longer refused since r2") — **that string
occurs nowhere in the applied file**; the certificate quotes text the bytes do
not contain. My corrected hunk (§2) lands clean at `--fuzz=0`.

**A4 — promotion-language overreach (CLASS4).** Three candidates name
`(Core, arc3-r1/r3)`: EX-14 v1, EX-14 demo, EX-15's A6a/A6b hunks.
**Sustained** — both cited entries open "RESULT-class, no Core promotion", and
PROVINCE has zero `arc3` occurrences pre-patch. EX-14 v2 fixed its own
instance (drops `Core`, states `RESULT-class`); **EX-15's two EVM variants
still carry it**. (The `(Core, r4-09)` marker on the
`compare_javascript_export_shapes` clause is a *different* item with its own
promotion record and is correctly kept everywhere.)

**A5 — scope creep into authority/boundary statements.** CLASS2 over changed
spans: **refuted for all 21 candidates** — no repair touches the Adjacent
section, the availability-vs-holding doctrine, the registry non-authority
clause, the installer refusal, or any `(unowned)` marker. The SHONEN-pinned
safety clause stays at `:114` inside 88-116 in every applied tree, and
PROVINCE.md:18 keeps both probe needles. Frontier edits land in 73-93/133-162;
nothing above `:116` shifts (162 lines held everywhere).

**A6 — census/probe blind spots exploited?** The Frontier region is
UNDECLARED, so the census cannot see claim truth there; every candidate that
writes into it was checked by hand (byte sweep + clause audit), not by the
gate. The probe pins only :18 and the SHONEN range; both hold everywhere.
No candidate introduces a gate+needle into 72-118 (hazard check: none).

**A7 — EX-03's Vyper decode (cross-chain attack on C1's evidence).** EX-03's
`dispatch-decode.txt` reports 13/22 PARTIAL while this seat's fresh probe and
EX-06's envelope both return 22/22 on the same bytes. The PUSH4 census (my own)
shows all 22 selectors present at valid `% 22` slots; the 9 "missing" ones
collide with recovered partners, so EX-03's slot-occupancy assumption (one
selector per slot) is what fails. **Verdict: the decoder is faulty; the probe
and the entry's K/K claim stand.** Flagged for C1's parent — the artifact is
still on disk and will mislead a reader who trusts it over the envelope.

## 5. Blockers

None for the seat task. Named gaps and residuals for the parent:

1. **Land the corrected X1 hunk, not v2's hunk 6** — otherwise the round ships
   a self-contradictory sentence and a certificate that quotes absent bytes.
2. **Decide the Core-table items' column.** Nine candidates repair Core rows
   outside the declared unit; they are true but uncounted. Either the round
   says so (advisory, like EX-15's and EX-12's own framing) or it re-scopes.
3. **VZ-2's census instrument cannot measure the after-state** (hardcoded
   verdicts) and its delivered sha (`7facc43f…`) differs from the one the chain
   verdict quotes (`e6eef574…`). Its new C2/C3 rows (Ghidra features 35→34;
   asar archives 9→12) are corroborated by this seat but have **no repair
   candidate in any patch text** — C3's asar row is in no seat's set.
4. **EX-15's EVM hunks carry the `(Core, arc3-r1/r3)` defect**; if the parent
   lands EX-15's set instead of EX-14 v2, apply the same fix v2 made.
5. **EX-03's `dispatch-decode.txt`** (13/22 PARTIAL) is a false negative on
   Vyper; the probe's 22/22 is correct (re-derived twice independently).
6. Every identity in this report was re-derived after the last write of each
   artifact; the gate table (`final-gate-table.out`) pins the clone HEAD and the
   instrument shas used.
