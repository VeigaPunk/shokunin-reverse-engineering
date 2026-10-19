# SEAT VZ-1 | CHAIN c1 | ROLE convergence — arc3-loop1-round4 (2026-10-19)

Task (seat line): poll seats every 60s (max 25 checks); reconcile into
`claims/c1/verdict.md`: VERIFIED or NOT-VERIFIED (an honest stop is a
NOT-VERIFIED for the positive claim, reported as such) + evidence + named debt.
Seat report last.

Repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`015e1bab914713568f339fd53999bc180459cc40` at every read (no seat commits; the
parent integrates). Scratch `/var/tmp/vz1r4/` (never `/tmp`, EDQUOT standing).
No git mutations. Custody paths read-only (hash/stat only; demos not run by this
seat). No LOG/SCORECARD/SHONEN/corpus/SKILL/PROVINCE/README writes. Writes:
`claims/c1/verdict.md` + this report + `claims/c1/VZ-1/` only.

## 1. Work performed (evidence pointers)

Poll loop: `claims/c1/VZ-1/poll.log` (25×60s poller; seat-dir and claims-dir
listings every tick). Baseline was measured **before** any seat output existed,
so the "before" side is independent of the wave.

1. **Baseline at HEAD (first-hand, before any seat artifact landed).** Command A
   (SCORECARD recipe A, `git show` form) → `{"knowledge_files":83,"mapped":83,
   "missing":[],"dangling":[],"citation_resolved_rules":14,"rule_blocks":14,
   "coverage_score":10.0,"depth_score":10.0}` —
   `VZ-1/evidence/baseline-commandA.json`. Citation-drift probe: findings=0
   exit=0 in **default and `--strict`**; `--selftest` 13/13 exit 0; pointer-table
   sha256 `1b3ab955…` equals the expected pin (`baseline-probe-*.txt`,
   `baseline-pointer-table.sha256`).
2. **Vyper install receipt re-derived.** `vyper --version` →
   `0.4.3+commit.bff19ea2`; `bin/vyper` sha256 `615f792c…`;
   `bin/python` → `/usr/bin/python3.14` sha256 `d78f9cf7…` — all equal to
   EX-04's and PL-1's receipts. EX-02's `attest-output.txt` shows all 8 wheels
   byte-identical to their pinned payloads (157 vyper files `differ=0
   missing=0`). No install by this seat.
3. **K/K re-derivation across five carriers (this seat's own third keccak
   path).** `js-sha3@0.8.0` (r1 receipted prefix) over each compiled ABI,
   set-equality vs the planted file and the sealed envelope:
   `CarrierV` **15/15** on 7 legs, `Ex09Vault` **7/7** on 5 legs,
   `StewardToken` **22/22** on 2 legs, `CarrierW` **9/9** on 2 legs, `Smoke`
   **4/4** on 2 legs — **18 legs**, `abi == env == planted` true, `missing_vs_env
   []`, `extra_vs_env []`, `dispatch:"abi"` everywhere.
   Evidence: `VZ-1/evidence/vyper-kk-rederive.txt`.
4. **Recheck line, verbatim (the entry's own command).**
   `TMPDIR=/var/tmp/r4-recheck npx -y rea-agents@6.4.0 inspect-evm-interface
   …/EX-04/out/runtime.hex hex --format json` → id `ev_d1792f57…`, 15 functions,
   all `dispatch:"abi"`, decoded `57d6fd0a…`; envelope sha256 **`68415a3d…`** —
   byte-identical to RV-2's copy, EX-05's mirror, RV-1's and SC-1's runs
   (five-way). Raw leg (`runtime.bin raw`) also 15/15. Evidence:
   `VZ-1/evidence/recheck-carrierv-640.json`, `recheck-carrierv-raw.json`.
5. **Opcode-boundary `PUSH4` census (this seat's own disassembly).**
   `CarrierV`: 21 `PUSH4` immediates, 16 distinct — the 15 selectors plus
   `08c379a0` ×6 **only**; `69656e74` is **not** an opcode-boundary immediate (it
   sits inside a `PUSH32` payload at pc=723, the revert string `insufficient`);
   `89402a72` (`__default__`) occurs **0** times.
   Evidence: `VZ-1/evidence/push4-census-independent.txt`.
6. **Dispatch-site shape census (this seat's own).** Every ABI function's
   `PUSH4` site classified by its following bytes: **53 selectors across 4
   carriers** (CarrierV 15, StewardToken 22, Ex09Vault 7, CarrierW 9), all at
   genuine `PUSH4 sel; DUP2; XOR` Vyper compare sites — **0 selectors without a
   compare-shaped site**.
7. **Offset rule + jump table, re-derived.** `bytecode_offset == push4_pc + 11`
   **15/15** (push4_pc = the PUSH4 opcode position) and `byte[offset−12] == 0x5b`
   **15/15**; the `0x600` table's 13 uint16 entries are all JUMPDESTs,
   `0x5e7` ×3 sentinel, `selector % 13` matches the bucket heads, and
   `table_off + 13*2 == len(runtime)` exactly.
8. **Mutability delta, re-derived.** 7/15 agree, 8/15 read `payable`
   (declared view ×5, nonpayable ×2, pure ×1); the divergence tracks **argument
   count** (8/8 arg-taking diverge, 7/7 zero-arg agree) with the fused guard
   `PUSH1 <4+32·nargs> CALLDATASIZE LT CALLVALUE OR PUSH2 …` at the body head;
   the same class reproduces on r3 solc carriers (this seat's re-measurement:
   VaultB.opt200 13/13, CarrierB 7/8, carrierB@EX-04 10/11 — both divergences
   arg-taking). Evidence: `finding-F3-inference-mechanism.txt`.
9. **Clone projection (the landing pre-flight).** Fresh `git clone
   --no-hardlinks` at HEAD + the entry literal (extracted between the draft's
   markers: 32 lines / 18,166 B / `da42d9a2…`) + the additive token line →
   commit `36680c2a…`; `git diff --name-status` = exactly `M corpus/README.md` +
   `A corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md`; command A = **84/84,
   missing [], dangling [], 14/14, 10.0/10.0**; **prior-83 byte-identical: 83/83,
   diffs=0, missing=0**; README **190 → 190**, after-sha `1cd05260…` (byte-equal
   to SC-1's independent rehearsal). Citation-drift probe at the projected
   commit: findings=0 in both modes. Evidence:
   `VZ-1/evidence/projection-commandA.json`.
10. **Instruments (read-only).** `.ufo/gates/c1-census-v10.py` → **PASS
    `stale=0 ambiguous=0 undeclared=0 unresolved=0`**, scope-errors `[]`,
    unreadable `[]`, G2 floor ok. `custody-pair.py selftest` → **CLEAN 28/28**
    (scratch base; no writes to the real custody target by this seat).
11. **Entry citation audit.** All **16/16** `ev_` ids the entry cites resolve to
    real envelopes with the stated payload; every path citation in the entry's
    `source:`/`Sources:` lines resolves against its seat dir (0 unresolved).
12. **Read (not re-run):** PL-1 plan+report, EX-01 census, EX-02 install+attest,
    EX-03 report+decoder, EX-04 report+attacks, EX-05 attacks/crosschecks, EX-06
    report, EX-07 pre-registration + r3-Unknowns patch, EX-08 report, EX-09
    analysis, EX-10 rerun+report, SC-1 report+ledger+drafts, RV-1 report+patch,
    CR-1 SUMMARY+patch, records-drafts (4 files).

## 2. Proposed changes

- **`claims/c1/verdict.md`** (rev 1 at 14:15Z; **rev 2** after RV-2's grade landed)
  — the chain verdict: **VERIFIED**.
- **Repair texts cited by the verdict** (authored by other seats, or by this
  seat where named):
  - F1 → `RV-1/proposed-entry-correction.patch.md` (`7d90b514…`).
  - F2 → `VZ-1/evidence/finding-F2-same-path-sentence.txt` §Repair (this seat's
    own finding; no other seat has drafted text for it).
  - F3 → `VZ-1/evidence/finding-F3-inference-mechanism.txt` §Repair (this seat's
    own finding).
  - CR-1's five entry edits → `CR-1/proposed-entry-corrections.patch.md`.
  - EX-07's r3-entry Unknowns patch → `EX-07/proposed-r3-unknowns-correction.patch.md`.
  - The landing pair → `records-drafts/knowledge-entry-draft.md` +
    `records-drafts/map-token-patch.md` (SC-1).
- **No repo-surface change by this seat** (the freeze's write scope).

## 3. Before → after measurement for the chain's claim

| quantity | before (this seat, HEAD) | after (this seat, clone projection) |
|---|---|---|
| command A | 83/83, missing [], dangling [], 14/14, 10.0/10.0 | **84/84**, same fields, clone `36680c2a…` |
| prior-83 knowledge files | — | **byte-identical 83/83** (0 diffs, 0 missing) |
| README | 190 lines, `a451ad16…` | **190 lines**, after-sha `1cd05260…` |
| diff name-status | — | exactly `M corpus/README.md` + `A …/2026-10-19-arc3-r4-evm-vyper-leg.md` |
| Vyper K/K (5 carriers / 18 legs) | not measured pre-wave (the r1/r3 Unknown) | `abi == env == planted` true on all 18; 0 missing / 0 extra; `dispatch:"abi"` |
| zero false positives | — | 21 `PUSH4` sites, 6 non-selector (`08c379a0`), none reported |
| offset reading | r1/r3 rule: "offsets land on JUMPDESTs" | **0/15** on JUMPDEST; `push4_pc + 11` 15/15 |
| recheck line | — | `ev_d1792f57…`, envelope `68415a3d…` (five-way identical) |
| probe (citation-drift) | findings=0 (default+strict) | findings=0 at the projected commit (default+strict) |

Honest-stop branches (venv infeasible / typed refusal / partial recovery): **not
triggered** — the install succeeded (py3.14, source-built `immutables`), every
runtime leg recovered K/K, and creation/trap legs are parsed-and-empty **by
their declared classes**.

## 4. Attacks / refutations attempted, with verdicts

| attack | verdict |
|---|---|
| "the chain cannot even start — vyper is uninstallable on this host" | **REFUTED** — EX-02's install landed; this seat re-derived the compiler identity; EX-01's census showed the cp314 `immutables` wheel gap and the source build closed it |
| "the K/K is the extractor parroting a planted list" | **REFUTED** — third independent keccak path (js-sha3 over the compiled ABI) reproduces the planted sets on 5 carriers |
| "zero extras is vacuous" | **REFUTED** — real decoys present and unreported |
| "some reported selector is a false positive" | **REFUTED** — 53/53 selectors at genuine compare sites |
| "the entry's recheck line does not reproduce" | **REFUTED** — five-way byte-identical envelope |
| "the projection breaks the prior 83 / is not line-neutral" | **REFUTED** — 83/83 identical, README 190 → 190 |
| "the landing breaks the citation-drift gate" | **REFUTED** — findings=0 both modes at HEAD and at the projection |
| "the entry's `69656e74` sentence reproduces" | **SUSTAINED (RV-1)** — it does not; F1 |
| "the entry's `same path` sentence is true" | **SUSTAINED (this seat)** — it is false; F2 |
| "the payable-read delta is a Vyper dispatcher-shape effect" | **SUSTAINED (this seat + EX-04 A4)** — it tracks argument count and reproduces on solc; F3 |
| "the entry's SC-1 inventory citation / EX-09 brace expansion resolve" | **SUSTAINED (RV-2 R-F1/R-F2)** — both re-verified by this seat (`ls`; re-expansion: 2 of 12 names absent) |
| "the id-domain `var-*` legs demonstrate path-sensitivity" | **SUSTAINED (RV-2 A1)** — they are cwd/TMPDIR variants at one path |
| "EX-03's 13/22 decoder reading means the probe over-reports" | **REFUTED** — all 22 selectors sit at genuine `PUSH4` sites (my byte scan); the decoder is scope-limited |
| "a solc-shaped reconciler is safe on this tree" | **SUSTAINED (CR-1)** — empty on 33/33 Vyper carriers; 100% false-extra rate on 7 of 26 digest groups |
| "the r3 entry's 6.7.0-specific delta is still accurate" | **SUSTAINED (EX-07)** — it is a 6.5.0 boundary |
| "EX-10's id-domain battery is unnecessary" | **REFUTED as an attack** — it sharpened r3's path-sensitivity caveat into "path-keyed, not inode/mtime-keyed" and measured the symlink refusal class |

## 5. Blockers

None for this seat's task. Named gaps for the parent:

- **RV-2's grade gap is CLOSED** (rev 2): its report + `quality-grade.md` landed
  at 14:17Z with verdict ACCEPT-WITH-FIXES; its four fixes (R-F1 SC-1 inventory
  path, R-F2 the EX-09 brace expansion's two nonexistent names, R-F3 provenance
  wording, R-F4 the missing QUALITY-row-15 corpus citation) and two advisories
  are folded into the verdict's debt 6, each re-verified by this seat. **All 16
  c1 seats now have reports.**
- **F1/F2/F3 plus RV-2's R-F1..R-F4 must be applied to the entry literal before
  landing.** F2 and F3 have no patch text from any other seat — the parent can
  take this seat's repair text from `VZ-1/evidence/`.
- **CR-1's Edits 1, 3, 4, 5 are sustained but unapplied** (Edit 2 is already
  satisfied by the draft). Edits 4 and 5 (the reconciler hazard and the
  count-vs-set rule) are the round's most portable findings and are absent from
  the draft.
- **The landing itself is parent-side** — the entry file, the token, the work
  commit, command A at the records commit, the custody post-pair.
- The r3 entry's "6.7.0-specific" Unknown is superseded by EX-07's measurement
  (6.5.0 boundary); whether it is in this round's edit scope is the parent's
  call.

## 6. Self-identity (re-derived after the final write, rule #14)

| artifact | bytes | sha256 |
|---|---|---|
| `claims/c1/verdict.md` | see `VZ-1/evidence/SHA256SUMS.txt` | see sidecar |
| `seats/VZ-1.md` (this file) | — | sidecar only |

This report's own hash is **not** self-quoted (any revision of this file voids
it — the r1 D9 class): `VZ-1/evidence/SHA256SUMS.txt` records the identity of
every artifact in `VZ-1/evidence/` plus the verdict as measured after the final
writes; `sha256sum -c` over that file passes. The verdict's row is its identity
as measured after the verdict's last edit; re-derive both rows if either file is
revised.
