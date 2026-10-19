# C3 verdict — custody-pair residual closures (chain convergence, seat VZ-3)

Wave `arc3-loop1-round4` · chain c3 · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD (committed revision)
`015e1bab914713568f339fd53999bc180459cc40` (no seat commits; parent integrates).
Frozen claim: `claims-frozen.md:59-77`. Seat line: VZ-3, reconcile into this file.
Evidence: `claims/c3/VZ-3/vz3-reconciliation.txt` (sections 1-8 are this seat's raw
first-hand captures; re-derived after the last append, rule #14).

## Verdict: **VERIFIED** on every leg this seat could measure on the landed bytes — **with one named uncovered leg** (the SKILL.md registry row, §R1) and the commit itself left to the parent (no seat commits)

Rationale: the frozen claim requires (a)-(c) closed with declared classes,
selftest 22 → ≥24 with new fixtures and sabotage arms, (d) adjudicated with the
ruling text landed in the README, the registry row + README re-derived
same-commit, the round's live pair (revised tool) verifying MATCH 5/5 with every
receipt self-pinning the new tool sha256, and command A unchanged. On the landed
bytes: (a)-(c) close with the declared `USAGE 2` class in **both** sidecar
spellings; selftest is **28/28 CLEAN** with all 22 prior names retained and three
new fixture pairs that each go DIRTY under a targeted mutant; the (d) ruling text
is in the landed README and the wave's own `readme_ruling()` check reads 0 → 10
hits; the live pair verifies `MATCH 5/5` with and without the gate and both
receipts self-pin `29bb45ae…`; command A is unchanged at 83/83, 14/14, 10.0/10.0.
The registry row is **not in the tree** (§R1) — EX-21's patch text for it is sound
and line-neutral but unapplied, so that leg of the claim is unmet by
non-application, not by defect.

## 1. Landed identities (this seat's re-derivation, rule #14)

| object | before (HEAD `015e1ba`) | landed (worktree) |
|---|---|---|
| `.ufo/gates/custody-pair/custody-pair.py` | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 L) | **`29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf`** (1343 L, 65,902 B) |
| `.ufo/gates/custody-pair/README.md` | `f30df42e0a547a0aefd21590c0f975acf06d91161fcb6db77c8934960efeb193` (185 L) | **`9d9400dab7ff7072375c13fad43c02dde0f3923a58cf3af0d50fa3384535022a`** (272 L, 15,293 B) |
| `SKILL.md` | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` (390 L) | **unchanged — still `5eec51c0…`**; the row lands only as EX-21's patch text (§R1) |
| `git status` | clean for the gate dir | ` M` both gate files (parent's to commit) |

The README was rewritten five times inside ~3 min (observed digests `4a8f44c2…`
→ `91fd386b…` → `9a631196…` → `125e7e02…` → `9d9400da…`, the last being EX-21's
attribution + one-clause correction edit); the identity above is the **settled**
value, and every README-side check in this file (§2 rows 6, 10; §6 A6, A7) was
re-run on those `9d9400da…` bytes: ruling hits 10, distinct-path basis present,
`cases=28` present, four `custody-readme-*` anchors 1-2 hits, probe 0 findings in
both modes. The tool was written once (`mtime 11:09:25-0300`) and never moved.

## 2. Claim components — status and evidence

| # | Component | Status | Evidence (this seat, on the landed bytes) |
|---|---|---|---|
| 1 | (a) sidecar path scope closed | **VERIFIED** | spelling A `--out X --paths X.sha256` → exit 2, measured file sha unchanged; spelling B `--out X.sha256 --paths X` → exit 2, **no** neighbour and **no** second sidecar created; spelling B2 (bystander neighbour already exists) → exit 2, bystander sha unchanged. All three re-measured on a scratch copy of the landed bytes |
| 2 | (b) `out.parent.mkdir` class closed | **VERIFIED** | `--out pfile.txt/rec.txt` → exit 2, `USAGE: cannot create the receipt directory ([Errno 17] File exists: …)`, traceback count 0; `--out ''` stays the declared USAGE (selftest case + my own probe) |
| 3 | (c) coverage gate counts distinct paths | **VERIFIED** | 5× duplicate v2 stanzas `--require-paths 5` → exit 2, `REFERENCE-COVERAGE: 1/5`; v1 **sums** dupe shape → exit 2; v1 **pipe** dupe shape → exit 2; 5 **distinct** paths → `MATCH 5/5 exit 0` (control unchanged) |
| 4 | selftest 22 → ≥24 with new fixtures | **VERIFIED: 28** | `CUSTODY_PAIR_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0`; the 22 prior case names are all retained verbatim; the six new names are `coverage-gate-rejects-duplicate-stanzas`, `coverage-gate-passes-distinct-five`, `refuses-sidecar-over-measured-file`, `refuses-receipt-over-sidecar-neighbour`, `out-parent-not-a-directory-usage-exit`, `both-sides-absent-is-agreement-match` |
| 5 | sabotage arms (each fix load-bearing) | **VERIFIED** | my own three targeted mutants on the landed bytes: MUT-A (guard limited to `out`) → selftest DIRTY 26/28, exactly the two sidecar cases FAIL, and A/B/B2 all return to exit 0 + clobber; MUT-B (mkdir back outside) → DIRTY 27/28, exactly `out-parent-not-a-directory-usage-exit` FAIL and the raw traceback at exit 1 returns; MUT-C (stanza basis) → DIRTY 27/28, exactly `coverage-gate-rejects-duplicate-stanzas` FAIL and the v1-sums dupe gate returns to silent exit 0 |
| 6 | (d) adjudicated, ruling text landed in the README | **VERIFIED** | landed README carries the ruling; EX-27's own `readme_ruling()` regexes read **0 hits** on the r3 README and **10 hits** on the landed one; behaviour unchanged by design (both-absent `MATCH exit 0`, `compared=0/11`) and now carrying the note `both sides record the path absent — … not a verified presence`; an error on either side still reads `UNEVALUABLE 14` |
| 7 | live pair (revised tool) MATCH 5/5, receipts self-pin the new sha | **VERIFIED** | `claims/c3/EX-21/receipts/live-{pre,post}.txt`, both `# tool: … 29bb45ae…`; this seat's own re-verify: pair `MATCH 5/5 exit 0` and `--require-paths 5` identical; post vs `--live` `MATCH 5/5`; both sidecars `sha256sum -c` OK; my own independent capture pair with the landed tool also `MATCH 5/5` |
| 8 | registry row + README re-derived same-commit | **NOT MET for the row half** | README is landed and re-derived (§1). The **SKILL.md registry row is byte-unchanged** from HEAD (`5eec51c0…`) and still says "22 fixture cases" with a write-guard cell that names only the `--out` guard — see §R1 |
| 9 | command A unchanged | **VERIFIED** | verbatim SCORECARD recipe at `015e1ba`: `83/83, missing [], dangling [], 14/14, 10.0/10.0` — identical before and after the landing (the gate dir is not in command A's scope; measured to confirm no collateral) |
| 10 | no-harm instruments | **VERIFIED** | citation-drift probe `reported findings=0` / `strict clean findings=0` / selftest 13/13; c1 census `PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)` — all re-run after the landing |
| 11 | backward compatibility (r3 receipts still verify) | **VERIFIED** | r3 `config-post-pair-v2r3.txt` vs `--live` with the landed tool → `MATCH 5/5`; r3 pre vs r3 post → `MATCH 5/5`; r3 post vs my landed-tool post receipt → `MATCH 5/5`; v1 shapes on the landed tool keep their declared classes (`MATCH-V1-PARTIAL 5/5 exit 0` for sums; `CONTENT-DRIFT exit 10` with `LABEL-DEFECT` for the canonical stanza, the recorded operator-side drift in `~/.kimi-code/config.toml`) |

## 3. Before → after (the discriminating numbers, VZ-3 first-hand)

| quantity | before (`7cd19c3c…`) | after (`29bb45ae…`) |
|---|---|---|
| (a) spelling A | exit 0, measured `X.sha256` **clobbered** | **exit 2**, sha unchanged |
| (a) spelling B | exit 0, neighbour + `X.sha256.sha256` created | **exit 2**, neither created |
| (a) spelling B2 | exit 0, bystander neighbour clobbered | **exit 2**, bystander unchanged |
| (b) mkdir under a file | exit 1, raw `FileExistsError`/`NotADirectoryError` traceback | **exit 2**, declared USAGE message |
| (c) 5× dupe stanza `--require-paths 5` | exit 0, `MATCH paths=1/1`, 0 coverage lines | **exit 2**, `REFERENCE-COVERAGE: 1/5` |
| (c) v1 sums/pipe dupe shapes | sums exit 0; pipe exit 2 (mixed) | **both exit 2** |
| (c) 5 distinct paths control | exit 0 `MATCH 5/5` | exit 0 `MATCH 5/5` (unchanged) |
| (d) README ruling hits | 0 | **10** |
| selftest | `CLEAN cases=22` | **`CLEAN cases=28`** |
| tool bytes / lines | 54,279 / 1155 | 65,902 / 1343 |
| live pair (revised tool) | — | `MATCH 5/5 exit 0`, self-pin `29bb45ae…` |
| command A | 83/83, 14/14, 10.0/10.0 | 83/83, 14/14, 10.0/10.0 |

## 4. Cross-seat reconciliation (what each c3 seat delivered, and my check on it)

| seat | artifact | VZ-3 check |
|---|---|---|
| EX-21 (implementer) | the landed pair, `matrix/before-probes.out` + `after-probes.out`, `receipts/live-{pre,post}.txt`, `selftest/selftest-landed-28cases.out`, `patch/skill-registry-row.patched.md` | identities re-derived; its after-probes reproduce on my own runs; its receipts re-verified by this seat's own invocation; its row patch verified sound and line-neutral (§R1); **one defect named**: its `(d)` leg is mislabeled (see §R2) |
| EX-22 (before-state) | `baseline.md` (`6f3846b1…`), `transcripts/` (108 captures) | its before-state agrees with mine on all three legs (a)/(b)/(c) at `7cd19c3c…`; its line-653 traceback reference matches my own |
| EX-23 (sidecar probe) | `sidecar-injection.py` (`ad4f9694…`), `before-probe.out`, `scratch-guarded-variant.py` (`b61cee68…`) | its BASE probe reproduced byte-for-byte by this seat modulo label/timestamp (my run adds the D consequence leg it lacked: `CONTENT-DRIFT exit 10`); its scratch variant is a **half-fix** (closes A, leaves B/B2) — the landed guard closes all three, so the variant is superseded |
| EX-24 (mkdir + fixtures) | `harness/build-*.sh`, `before/`+`after/`+`after/landed/` matrices, `evidence/SKILL.proposed.md` (`68435482…`), `evidence/landed-29bb45ae.py` | its `after2` variant independently re-run by this seat: `CLEAN cases=24`; `sabotage2` (cases without the fix) `DIRTY 22/24` with exactly its two new cases failing; its `landed-matrix` records the landed tool; its own SKILL proposal is **stale** (§R1) and its report says so |
| EX-25 (landed-revision attacks) | seat report; 12 attacks, five residuals, `IDENTITY-after.txt` (152 digests) | its **R4** (five hardlink names for one inode pass the distinct-path gate) reproduced first-hand by this seat: 5 stanzas / 1 inode / `MATCH 5/5 exit 0` — recorded as §R5; its R5 (bad-second duplicate masks an unevaluable copy) is outside this claim's letter and not re-run here |
| EX-26 (ruling) | `ruling.md`, `proposed-readme-ruling.patch.md`, `evidence/ruling-block.txt` (`8e0a88ee…`) | its ruling block inserted verbatim on a scratch copy of the r3 README reproduces its claimed digest `f54d9467…` exactly and takes `readme_ruling()` 0 → 6; **its claimed line count is off by one** (215, not 214) — §R3; the landed README adopts its ruling content with one clause corrected by EX-21 |
| EX-27 (regression battery) | `harness/regress-r4.py`, `runs/regress-r3-baseline-7cd19c3c.*`, `runs/regress-r4-battery-landed.*` | its r3-phase baseline and r4-phase landed run recorded; its `readme_ruling()` regexes are the instrument I re-ran for the (d) leg; its r4 battery reports 72 hold / 0 fail / 1 observed-only |
| SC-3 (scribe) | `ledger.md`, `harness/injections.sh`, `evidence/{before,after}/**`, `records-drafts/LOG-entry-draft.md` | its before-column reproduces my numbers; its **R1 (half-fix risk) is confirmed and now closed by the landing**; its compound (c)+(d) case (a 5-absent-path reference reading `MATCH 5/5` while passing the gate) reproduced first-hand by this seat — the landed revision changes (c) but **not** (d)'s class, so the compound case still reads `MATCH 5/5` (named as §R4); its after-column, re-measured on the landing, agrees with mine |
| RV-7 (mutation) | `probe.py`, `mutant-build.py`, `evidence/BASE-*.json`, `DRESS-*`, `MUT-*.json` | its diagonal matrix reproduces on its own revisions; on the **landed** revision its `mutant-build.py` matches only the coverage shape (`changed=True` for MUT-C, no match for A/B), so I built my own three mutants (§2 row 5) |
| RV-8 (patch review) | `prereg.md`, `class-map.sh`, `class-map-BEFORE.out` (`00b3253c…`), `anchors-head.out` | its pre-registered protocol is the shape this verdict follows; its before-state agrees; its own blocker (target not landed) is now resolved by the landing |
| CU-1 (cross/custody) | seat report + 39-file manifest | its four residual reproductions agree with mine; its `--require-paths` attack verdict ("real and open at the landed revision") is now **superseded by the landing** — re-measured closed |

## 5. Named residuals (measured; none voids the measured legs)

**R1 — the SKILL.md registry row is updated only as an unapplied patch text (the
claim's one open leg).**
`SKILL.md` is byte-unchanged (`5eec51c0…`, 390 L) and its `custody-pair` row still
reads "22 fixture cases" with a write guard that covers only `--out`. The landed
tool runs **28** cases and guards the receipt **and** its derived sidecar **and**
sidecar-shaped neighbours. EX-21's seat report and its patch dir landed **after**
this seat's first check, so the record is: a **sound, current** row patch now
exists — `claims/c3/EX-21/patch/skill-registry-row.patched.md`, sha256
`8e56f3d9ce21d16b2c46a398ad52aa2723c295008a76145b928265bdc88a68bf`, verified by
this seat: the diff against the live `SKILL.md` is **exactly one line** (line 390)
with **390 → 390** lines (line-neutral); the row-line digests reproduce
(`a94e79d9…` → `8f8e5408…`, matching EX-21's claims); and the patched row carries
28 fixture cases (no stale "22"), the derived-sidecar + sidecar-shaped-neighbour
guard, the **distinct resolved paths** gate basis, the receipt-directory USAGE
class, and the both-absent ruling — with no stale `7cd19c3c` token. All three
graded SKILL anchors stay alive in the patched file (1 hit each). The superseded
alternative `claims/c3/EX-24/evidence/SKILL.proposed.md` (`68435482…`, 24-case
wording) is **stale** and must not be applied. The claim leg is therefore
**unmet only because the row is not yet in the tree** — the parent applies it in
the same commit as the gate pair (§7.1).

**R2 — EX-21's own (d) probe is mislabeled (report-level, not result-level).**
`harness/before-probes.sh` writes `gone.conf`, captures receipt A, **deletes the
file**, then captures receipt B — so its "both-sides-absent" leg measures
one-side-absent and reads `ABSENT exit 13` in both the before and after
transcripts. The true both-sides-absent shape (file absent for both captures)
reads `MATCH exit 0` — measured by this seat, by SC-3's ledger, and by EX-26's 14
fixtures. The landed README's ruling text is correct; only EX-21's probe label is
wrong. Recorded so the records do not quote its `ABSENT 13` as the (d) result.

**R3 — EX-26's claimed patched line count is off by one.**
Inserting `evidence/ruling-block.txt` (1834 B, 29 lines, ends with a newline)
immediately before `## Exit codes (declared)` with no extra blank line reproduces
EX-26's claimed digest `f54d9467030bb250f85f11f18d8575e7eec9082ab76610de9681bf0fef847e10`
exactly, but the file is **215 lines**, not the 214 claimed (185 + 30 inserted
lines). The digest is the identity and it reproduces; the line count is an
arithmetic nit of the same species as r3's R3.

**R4 — the (c)+(d) compound case survives by design (the ruling's own limit).**
A reference of five cleanly-absent stanzas passes the distinct-path gate and
reads `MATCH 5/5 exit 0` with `SHA256-CONTRACT: 0/0` — a reference that examined
nothing reads clean. The landed (c) fix counts the five distinct paths, so the
gate is honest about *what it counted*; the (d) ruling declares the `MATCH` an
agreement on absence, not a verified presence, and the row now carries that note.
This is the frozen claim's chosen adjudication ("adjudicate and document … only
error-carrying stanzas are UNEVALUABLE"), so it is **adjudicated, not a defect** —
but the records must not quote an all-absent `MATCH 5/5` as a content witness.
The stronger forms SC-3 lists (an opt-in `--require-present N`, or a
`--require-custody-set` identity gate) remain un-landed proposals.

**R5 — the distinct-path gate counts NAMES, not files (EX-25's R4; confirmed
first-hand).** Five hardlink names for **one** inode pass `--require-paths 5` and
read `MATCH 5/5 exit 0` (my own probe: 5 stanzas, 1 distinct inode, exit 0). The
landed code matches its declared unit — distinct *resolved path names*, the same
basis as its `unaccounted:` list — so this is a unit-scope limit, not a coding
defect, and it is outside the frozen claim's letter. EX-25 filed a patch text;
an inode-basis or canonical-set gate (`--require-custody-set`) would close it.
Related, also from EX-25 and outside this claim's letter: a duplicate stanza with
an error-carrying copy at position 2 of 5 still reads `MATCH exit 0` where the
bad-last ordering reads `UNEVALUABLE 14` (pre-existing, unchanged by the landing).

**R6 — the commit itself is the parent's.** The gate pair and the row patch must
land **in the same commit**; a landed tool with a stale row is the current state
of the worktree, and the round's receipts self-pin `29bb45ae…`, so any later tool
revision voids them. The parent must also re-run the probe (both modes) and the
census after the row patch lands, and re-derive every identity this file quotes.

**R7 — receipts and the records.** `claims/c3/EX-21/receipts/live-*.txt` self-pin
`29bb45ae…` and their sidecars re-derive (both `OK`). The records commit must
quote the **settled** README digest (`9d9400da…`), not any of the four
intermediate values (§1), and the row patch's own digest once it is applied.

## 6. Attacks/refutations attempted by this seat (with verdicts)

| # | attack | verdict |
|---|---|---|
| A1 | "the landing is a half-fix: spelling A closed, B/B2 open" (SC-3's R1, EX-23's variant, my own earlier measurement of RV-7's DRESS) | **REFUTED on the landed bytes** — all three spellings exit 2 with the victims byte-unchanged. It was a real risk: RV-7's DRESS and EX-23's variant both exhibit exactly that half-fix |
| A2 | "the new selftest cases are decorative" | **REFUTED** — three targeted mutants redden exactly their own cases (2, 1 and 1 FAILs respectively) and nothing else; the landed control is 28/28 |
| A3 | "the (b) fix regresses `--out ''` or a fresh parent" (CR-4 item 6 / SC-3's R2) | **REFUTED** — `--out ''` is a declared USAGE, and the fresh-parent capture still succeeds (selftest + my own probe) |
| A4 | "the (c) fix breaks the legitimate distinct-path reference" | **REFUTED** — 5 distinct paths still `MATCH 5/5 exit 0`; 1-of-5 still refuses with the coverage line |
| A5 | "the landing breaks the r3 receipts / v1 shapes" | **REFUTED** — r3 post vs live, r3 pre vs r3 post, r3 post vs my landed-tool receipt: all `MATCH 5/5`; v1 shapes keep their declared classes (sums `MATCH-V1-PARTIAL 5/5`; canonical stanza `CONTENT-DRIFT 10` + `LABEL-DEFECT`, the recorded operator-side drift) |
| A6 | "the ruling text is a decoration that does not reproduce" | **REFUTED** — EX-26's block reproduces its digest exactly on a scratch copy and takes the wave's own check 0 → 6; the landed README takes it to 10 |
| A7 | "the landing broke a graded anchor or the probe" | **REFUTED** — all seven `skill-registry-*`/`custody-readme-*` anchors grade 1-2 hits with `re.M`; probe 0 findings both modes, selftest 13/13; census PASS |
| A8 | "EX-21's before/after transcripts are narrative, not measurement" | **PARTIALLY SUSTAINED** — its before/after probe legs reproduce on my own runs (A/B/B2/C), but its **(d) leg is mislabeled** and reads `ABSENT 13` where the true shape reads `MATCH 0` (§R2). The result-level legs stand; that one label does not |
| A9 | "the claim's registry-row leg is satisfiable as stated" | **SUSTAINED as an open leg, then bounded** — the row in the tree is byte-unchanged and stale (§R1), but EX-21's landed patch text is sound and line-neutral, so the leg is unmet only by non-application. Reported, not absorbed |
| A10 | "EX-21's registry-row patch is stale like EX-24's" | **REFUTED** — applied on a scratch copy the patch changes exactly line 390 (390 → 390 lines), reproduces both claimed row digests, carries the 28-case count, the sidecar/neighbour guard and the distinct-path basis, and keeps all three graded SKILL anchors alive |
| A11 | "the distinct-path gate is the strong close EX-24's patch text offered" (EX-25's R4) | **PARTIALLY SUSTAINED** — five hardlink names for one inode pass the gate and read `MATCH 5/5 exit 0` (my own probe, 5 stanzas / 1 inode). The gate is honest about its declared unit (distinct resolved path **names**); it is not a distinct-**file** gate and not a canonical-set gate. Outside the frozen claim's letter; recorded as §R5 |

## 7. Closing procedure (what the parent must do to make the claim fully true)

1. **Apply the row patch (§R1).** Apply
   `claims/c3/EX-21/patch/skill-registry-row.patched.md` (`8e56f3d9…`) — replace
   the single `| custody-pair |` line in `SKILL.md` with its counterpart
   (verified: exactly one line changes, 390 → 390). Do **not** apply
   `claims/c3/EX-24/evidence/SKILL.proposed.md` (stale, 24-case wording).
2. **Land the gate pair and the row in one commit** — the receipts self-pin
   `29bb45ae…`, so a later tool revision voids them; re-pin any graded citation
   the row rewrite moves.
3. **Re-run after the row lands:** the citation-drift probe (both modes), the
   census, and `sha256sum` of every identity this file quotes (rule #14).
4. **Do not quote** EX-21's `(d)` `ABSENT 13` leg (§R2), EX-26's 214-line claim
   (§R3), or an all-absent `MATCH 5/5` as a content witness (§R4) in the records.
5. Records: quote the settled README digest `9d9400da…` (the value after EX-21's
   final attribution edit; the earlier `125e7e02…` is superseded) and the tool
   `29bb45ae…`; command A stays 83/83, 14/14, 10.0/10.0 (re-measure at the
   records commit).

## Verdict basis note (evidence discipline)

Every row above cites a landed file plus a command result or digest measured by
this seat against the landed bytes; no seat report was treated as evidence
without a first-hand re-derivation. The reconciliation capture
(`claims/c3/VZ-3/vz3-reconciliation.txt`) holds the raw outputs. This seat wrote
no real target: the gate pair, the custody paths, LOG.md, SCORECARD.md, corpus/,
SKILL.md and PROVINCE.md were read-only (hash/stat/`git show` only); all mutation
ran on scratch copies under `/var/tmp/vz3` (`/tmp` never used); no git mutations.
