# R43RevClaims — pre-freeze line-by-line review of the draft claims

**Verdict: DEFECTS FOUND — 5 must-fix sentences before the freeze, 9 should-fix.** Everything else in the draft is implementable as written and matches the round-42 tools it ports.

Reviewed draft: `plans/round-43-claims.md` working-tree state `md5 57245e91268a2a87b39e52bc27697fa3` (uncommitted wave-1 amendments; the file was under live L1 amendment during this review — commit `1ed29de2` plus the `## Wave-1 amendments` section, 10 items). Line numbers below are that file's.

Seat bounds honored: read-only in the lane; the only writes are this report and `artifacts/R43RevClaims/` (gate receipt copy, unblob LICENSE copy). No tools installed (nothing needed installing).

---

## 1. What I ran (evidence base)

| check | command | observed |
|---|---|---|
| gate do-nothing at base | `python3 -I -B tools/round-41/local-source-gate.py --root . --rev 6b9e64fe… --json` | exit **1**, `rows_total 134`, `rows_checked 19`, `rows_failed` = exactly the plan's 18 rows, S126 green `[resolved/url-cell] src[file]` — receipt copied to `artifacts/R43RevClaims/gate-at-base-6b9e64fe.json` |
| gate CLI surface | argparse `--help` on `tools/round-41/local-source-gate.py` | flags are `--root --rev --sources --map --json --selftest`; **`--json-out` does not exist** (rejected, exit 2) |
| gate provenance | `git log -1 -- tools/round-41/local-source-gate.py` | `d764389e` (round-41 freeze) — "byte-identical to the round-41 committed bytes" is re-derivable |
| SKILL v4 table region | region = marker line → end of first table, at `d1681696…` vs base `6b9e64fe…` | both `sha256 bfb21ce8a1f001bfcbd9a6da6d2bd1b4533d0e902263d7998fe73d0438adfb43` — the region the claim re-freezes is unmoved at base |
| frozen-tool drift | `git log d1681696..base -- tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,fixtures.json} tools/round-41/local-source-gate.py corpus/evidence/local-sources.json tools/round-39/gen-squashfs.py` | empty — nothing the predicates freeze drifted since the round-42 freeze |
| r42 stop receipt | `jq` over `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` | `exit_code 1`, `matched 78`, `n 78`, `bindings_false ["observed_features_match_declared"]`; `combo_unseen_majority.need 12`, 19 unseen — byte-committed as the draft states |
| r42 freeze control | `jq .exit_code` on `.ufo/waves/round-42/controls/c2/c2-counter-at-freeze.json` | `2` — "counter at the freeze exits 2" convention holds |
| C02 declared tuple | `jq` over `corpus/evidence/round-42/c2/heldout/manifest.json` | C02 `declared_features.gap_kinds = ["extractor-failure","unpublished-entry"]`, `declared_extras.max_depth = 1` — matches the CTL-C1-2 red-arm text; observed adds `depth-limited` (r42 spotcheck §2) |
| dev arm / fixtures / r41 receipts | `ls` + `jq` at base | `corpus/evidence/round-42/c2/dev/` (78 carriers, manifest seed `e48947bb…`), `corpus/evidence/round-42/c2/fixtures/` populated, `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` present |
| landing absence at base | `git ls-tree base corpus/evidence/round-42/` | no `local-sources/` — the copies are pure post-freeze landings |
| S135 bytes | `curl https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE` | 1068 B, `sha256 67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e` — matches the draft's `67303bbd…`; copy in `artifacts/R43RevClaims/unblob-26.6.4-LICENSE` |
| base registry | `git show base:corpus/SOURCES.md` | 134 rows (S001–S134), **no S135/S136/S137** |
| map at base | `git show base:corpus/evidence/local-sources.json` | version 1, **one entry (S126)** → `corpus/evidence/round-41/s126/…` (present at base) |
| r42 counter port source | read `tools/round-42/c2-counter.py` (`CLAIM_BINDINGS`, lookup/combo_unseen code, CLI) | CLI `--root --rev --freeze --json-out --selftest` matches the draft's C1 counting command; exit vocabulary includes `no_manifest_at_rev` (exit 2) as the draft's unmoved-command requires |
| r42 generator port source | read `tools/round-42/heldout-gen-v4.py` (argparse, manifest write, `observed_features`) | supports `--seed --out --classes --combos --arm --run --verify --scratch --fixtures-dir --tuple-check-absent` — the draft's data-procedure command ports; the refusal/`--tuple-check`/`--carriers-only`/exit-4 modes named in amendment 1 are new code with concrete specs |

---

## 2. Answers to the assigned questions

**(a) Can the named tool implement each predicate sentence as written?** Yes for every sentence except the five flagged in §4 — three are unimplementable as written (M2 map-freeze contradiction, M4 receipt production, M5 registry byte-identity enforcement), two were made ungrammatical by over-deletion in the live edit and lost load-bearing clauses (M1a, M1b).

**(b) Is each after-state ONE concrete value one command re-derives over committed bytes?** Yes except: the C2 receipt (no command named that produces it — M4); the registry byte-identity clause (no named binding — M5); the C2 map freeze-state (undefined — M2); the CTL-C1-2 green arm's input directory (unnamed — S1); the 5 MiB / no-firmware clauses (plan-level assertions — S7).

**(c) Are the two frozen-path lists complete against the predicates?** C1: complete for the counter's reads *given amendment 3* (CTL-C2-7b deliberately unported, so its absence from the list is correct — I checked the r42 counter does read `LOOKUP_7B` and the amendment removes that read); two human-facing additions recommended (S2). C2: incomplete/ambiguous — the map is listed as a frozen path but the landing must add 17 entries to it (M2).

**(d) Can the kill rules fire before data?** Yes, both. All four C1 controls and both C2 controls are freeze-time procedures on committed bytes; none needs claim data. C2's kill-rule safety, however, depends on resolving M2: if the map were committed at the freeze with 18 entries and no copies, CTL-C2-0 and CTL-C2-1's absent-arm collapse into the same run.

**(e) Fresh-start rule (run-10, do-nothing controls for BOTH claims, scored before data).** Satisfied: CTL-C1-0 (counter at freeze exits 2 `no_manifest_at_rev` — matches the r42 counter's actual `Unevaluable` path I read at line 1106) and CTL-C2-0 (gate at freeze exits 1, 18 rows — I reproduced exit 1/18 rows at the base; the freeze-time receipt will read identically since the freeze precedes the landing). Neither do-nothing control can reach its claim's target. QUALITY 84 dry-runs: C1 is covered by CTL-C1-3 plus the counter selftest the amendment records (74/74); C2's positive dry-run receipt is unnamed (S8).

**(f) Separability — does C2 truly read nothing C1 writes?** Yes at the tool level: C1 writes `tools/round-43/*` + `corpus/evidence/round-43/c1/heldout/`; C2 reads `corpus/SOURCES.md`, the map, the copies, the gate — zero overlap. C1 writes nothing C2 reads. The paragraph's *"the shared file is this plan"* is nonetheless inaccurate (S6): `corpus/SOURCES.md` is read by both predicates (C1: the S135 license citation; C2: the 18 host-local rows and now the appended-row census). Neither claim writes it — the S135+ appends are the frontier step's landing — so separability of *writes* holds; only the sentence overclaims.

---

## 3. Line-by-line predicate audit

### P43-C1 (lines 43–65)

| sentence (line) | tool that implements it | verdict |
|---|---|---|
| table region byte-identical to `d1681696` (44–46) | c1-counter region extraction (ports r42 `rule_block`+`skill_block_drift`) | OK — region hash verified equal at base |
| interpreter/evaluator byte-identical at d1681696/freeze/REV (46–48) | counter frozen-tool checks | OK — no drift d1681696..base (verified) |
| held-out set path, command, first-added-after-freeze (49–51) | `manifest_after_freeze`, `first_add` bindings | OK — command flags all exist in the port source |
| class structure 27×2+24=78 (51) | `classes_two_each`, `n_equals_twice_classes` | OK — r42 manifest measured 78/28 classes |
| **"and the same tuple (the round-42 stop binding, now expected true)" (51–52)** | — | **M1a — broken sentence, two clauses deleted (see §4)** |
| `generator.tuple_check` recorded; refusal red/green in controls (52–53) | new counter binding + CTL-C1-2 | OK — spec'd concretely by amendment 1 (`--tuple-check DIR`, exit 3, `REFUSE C02 … depth-limited`) |
| interpreter == evaluator on every held-out envelope (54) | `evaluator_covers_all`-family bindings | OK |
| combo-unseen ≥12/24; lookup reported-not-bound (55–59) | `combo_unseen_majority` bound; lookup score reported | OK — **this clause was fixed mid-review** (was: fused lookup-run as the bound, which contradicted the r42 counter where `res['lookup']['binding']=False`; now matches, including the 19/24 measurement) |
| **"the round-41 C1 receipts and the evaluator's pair" (60)** | `real_receipts_depth_limited`, `legacy_dev_envelopes` | **M1b — "the round-42 dev-arm envelopes get" deleted (see §4)** |
| carriers regenerate; seed == freeze; subject digest == carrier sha256 (61–63) | `carriers_regenerated`, `seed_matches_freeze`, `envelopes_valid` | OK |
| fixtures pinned + S135 citation (63–64) | `fixture_scope` (now a real FROZEN_PATHS entry per amendment 3) | OK — S135 bytes verified live |
| no frozen C1 path changed after freeze (64–65) | `frozen_drift` | OK |

Generator-change paragraph (67–86): implementable — the manifest-write-behind-run inversion, corrected `combo_declared` predictor, `--carriers-only`, plain `--seed --out` exit 4, and `--tuple-check DIR` are concrete, and the OOD-vacuity/eight-field-match limits (amendment 9) close the self-report hole I would otherwise have raised. The conditional C02-shape sentence ("measured 42.2 % of seeds … the unconditional demonstration is the CTL-C1-2 red arm") is honest — accepted.

Kill rules (85–97): CTL-C1-0/1/3 need nothing but committed bytes; CTL-C1-2's red arm names a concrete command on the committed r42 set. **S1**: the green arm's input directory ("a directory whose manifest declares the observed tuples") is unnamed — commit it under `.ufo/waves/round-43/controls/c1/` and name the path.

### P43-C2 (lines 117–129)

| sentence (line) | tool that implements it | verdict |
|---|---|---|
| map binds every out-of-lane URL path to one in-lane regular file under `corpus/evidence/round-42/local-sources/` (117–120) | gate `check_path` (copy exists, in-lane, regular file, digest equal) | OK — gate semantics verified against source; R42LocalSrc's 17-copy + S126 disposition matches |
| entry digest == copy sha256; row-pinned digest == entry/source digest (121) | gate digest + `row-pin-conflict` + `source_sha256` checks | OK — matches gate source exactly (url-cell pins only; `digests_in(URL.sub(...))`) |
| gate exits 0 (121–122) | gate exit | OK at the measured revision |
| gate tool byte-identical to round-41 bytes (122) | `git log` provenance | OK — last touch `d764389e` (r41 freeze), verified |
| 5 MiB bound; no third-party firmware (122–123) | — | **S7 — plan-level assertion, no named check** |
| copy digests re-verify against live host where it exists; 15/18 live-equal; 3 host-absent bind to r42 build receipts (123–126) | seat audit (two independent) | OK as procedure — but see S5 on the gate's own host-binding |
| **registry "byte-identical to the base plus exactly the appended round-43 rows (S135, S136, S137)" (127–129)** | — | **M3 — S136/S137 don't exist yet and the frontier step says ONE row (line 186); M5 — no tool binds this clause (see §4)** |

Target/counting/controls (131–139): see M4 and S8. Kill rule (139): fires pre-landing under the M2-resolved reading. Disclosed limits (140–142): see S5 (the "advisory output without changing its exit" sentence is false for the three `source_sha256` entries).

---

## 4. Must-fix before the freeze (with replacement text)

**M1 — P43-C1 lines 50–52 and 60: two over-deletions in the live edit dropped load-bearing predicate clauses.** The sentence now reads "…(27 named classes × 2 plus 24 combo carriers, n = 78) and the same tuple (the round-42 stop binding, now expected true)" — "the same tuple" has no referent, and the `observed_features_match_declared` predicate (the very binding named in the Target line, "observed_features_match_declared true") has vanished from the predicate text. Line 60 reads "the round-41 C1 receipts and the evaluator's pair" — "the round-42 dev-arm envelopes get" was deleted, leaving a dangling fragment.
*Replacement (restore the pre-edit text, which matches the r42 plan's predicate and the counter's binding list):*
> "…with the same class structure as round 42 (27 named classes × 2 plus 24 combo carriers, n = 78) and the same `declared_features` single-key contract (R41-CL1); every envelope's observed six-field tuple equals its declared tuple (the round-42 stop binding, now expected true); … the round-41 C1 receipts and the round-42 dev-arm envelopes get the evaluator's pair; …"

**M2 — C2 freeze-integrity vs the map: the plan never says when the map lands, and both readings break something.** Frozen paths (line 199) list `corpus/evidence/local-sources.json` as an ordinary frozen path, but the landing must add 17 entries to it; the freeze-integrity rule (line 20) would make every C2 score inadmissible. If instead the map is committed at the freeze, then CTL-C2-0 (do-nothing) and CTL-C2-1's absent-copy arm are the same run, and "Controls scored at the freeze (before the copies land)" misleads. The copies carry the annotation "(added after the freeze — landing paths, not pre-landing bytes)"; the map carries nothing.
*Replacement (recommended — keeps CTL-C2-0 and CTL-C2-1 distinct, matches "before the copies land"):* in the Frozen paths section, change the C2 map entry to:
> "`corpus/evidence/local-sources.json` (landing path — its 17 new entries land in the landing commits; the pre-existing S126 entry is preserved byte-for-byte, JSON-value-equal to the base entry)";

and add one sentence to the C2 predicate or the freeze-integrity paragraph:
> "For C2 the landing commits may add map entries and copies and change nothing else: the gate tool, this file, the S126 entry, and `corpus/SOURCES.md` rows other than the appended round-43 rows are untouched in FREEZE..REV; the S126 preservation is one command — `test "$(git show <BASE>:corpus/evidence/local-sources.json | jq -cS '.sources|to_entries')" = "$(git show <REV>:corpus/evidence/local-sources.json | jq -cS '.sources|to_entries|map(select(.key==\"/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv")))'"`."

(The alternative — commit the full 18-entry map in the freeze commit and annotate it "committed at the freeze; untouched in FREEZE..REV" — is workable too, but collapses CTL-C2-0 into CTL-C2-1's absent arm; pick one and write it down.)

**M3 — the appended-row census is internally inconsistent.** Line 128 binds "exactly the appended round-43 rows (S135, S136, S137)"; line 186 still says S135 is "the round's one new registry row"; the base registry has 134 rows and the working tree has no S135/S136/S137 yet. "Exactly" needs a closed list at freeze time.
*Replacement:* either open and name S136/S137 in the Frontier step (what are they? the assimilation entry's staged rows?) and keep line 128's closed triple — or, if only S135 lands, line 128 becomes "plus exactly the appended round-43 row S135". C1's citations name only S135 and are fine either way.

**M4 — the C2 counting command cannot produce the receipt the plan requires.** `local-source-gate.py` has no `--json-out` (verified: argparse rejects it, exit 2); JSON comes from `--json` on stdout; and the R43SentProv receipt shape (argv, gate sha256, resolved revision, exit code — line 137) is a wrapper shape nothing in the plan generates. "Counting command: `… --root <LANE> --rev <REV>` (exit 0, and `jq '.rows_failed | length' <receipt>` prints 0)" is therefore not one re-derivable command: text mode prints the human verdict, and no committed receipt path is named.
*Replacement:* name the producer and the paths, e.g.:
> "Counting command: `python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV> --json | <receipt-wrapper> > .ufo/waves/round-43/l1/scores/c2-gate-at-<REV>.json` (exit 0; the receipt records argv, the gate tool's sha256, the resolved revision, the table sha256, the map sha256, and the exit code; `jq '.rows_failed | length' .ufo/waves/round-43/l1/scores/c2-gate-at-<REV>.json` prints 0). Freeze-time control receipts: `.ufo/waves/round-43/controls/c2/ctl-c2-0-do-nothing.json`, `ctl-c2-1-sandbox-digest-mismatch.json`."

**M5 — the registry byte-identity clause has no enforcing tool, and the gate alone would green a registry edit.** If a commit in FREEZE..REV edited S023's URL cell to drop the host path, the gate would green that row *without any copy* — the clause exists to forbid exactly this, but nothing binds it.
*Replacement:* add to the C2 receipt requirements:
> "the receipt records `git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..<REV> -- corpus/SOURCES.md` — exactly the appended round-43 row lines (one insertion each) and zero deletions."

---

## 5. Should-fix (calibration/robustness, not blockers)

- **S1** (line 97): name the CTL-C1-2 green arm's input directory and commit it under `.ufo/waves/round-43/controls/c1/`.
- **S2** (lines 193–196): C1 frozen list — add `tools/round-39/gen-squashfs.py` (the writer; the r42 plan listed it; untouched d1681696..base, verified) and `.ufo/waves/round-43/controls/c1/` (committed at the freeze, must stay untouched). The counter enforces both dynamically, but the human-facing list should name them.
- **S3** (line 137): "the receipt names the map version" — the gate JSON carries only the map *path*; add `map_sha256` to the receipt shape (one `sha256sum`).
- **S4** (lines 140–142): the disclosed limit "host paths that drift later re-red the row in the gate's advisory output without changing its exit while the copy stands" is **false for the three entries carrying `source_sha256`** (S003's container, S023, S082's extra.db — all showed `src[file]` in the R42LocalSrc receipt): drift of those host objects flips the gate to exit 1 (`source-digest-mismatch`). Either disclose that explicitly or drop `source_sha256` from those entries. (This is also live: amendment 5 already records three host objects gone — the S035 pair and S081's npx cache. Good catch, fold S4 in next to it.)
- **S5** (lines 149–150): separability — replace "the shared file is this plan" with "the shared reads are this plan and `corpus/SOURCES.md` (C1: the S135 row's license citation; C2: the 18 host-local rows and the appended-row census); neither claim writes either file".
- **S6** (lines 151–181): amendments 8 and 10 duplicate the SKILL-marker item; merge them.
- **S7** (lines 122–123): "no committed copy exceeds the 5 MiB bound" — name the one-liner in the receipt (`git ls-files -z corpus/evidence/round-42/local-sources | xargs -0 stat -c %s | sort -n | tail -1`; R42LocalSrc's largest is 2 048 000 B) or accept it as a plan-level assertion; "no third-party firmware image" stays a plan-level assertion (the dispositions are ghidra/go/rea-agents/pacman objects).
- **S8** (QUALITY 84, C2 side): name the positive dry-run receipt — gate green on the prepared pack in a sandbox clone, committed before the freeze (e.g. `.ufo/waves/round-43/controls/c2/dry-run-green.json`). CTL-C2-0/1 are both negative arms; the round-41-closure D4 dry-run requirement wants the green arm's receipt on record.
- **S9** (line 131): the C2 target says `rows_total ≥ 129` — fine, but with the registry at 134 + the M3 rows it will read 135–137; tighten to `rows_total == <base 134> + <number of appended rows>` once M3 closes, so the receipt catches a accidentally-dropped row too.

---

## 6. Already-fixed mid-review (verified, no action)

The wave-1 amendments (committed to the working tree during this review) correctly resolved, with evidence: the C1 landing path (round-42 destination, matching the prepared map — and commit `1ed29de2` correctly kept the copies' round-42 provenance); the lookup clause (now bound/report-split exactly as the r42 counter implements it, including the 19/24 measured value I confirmed in the receipt); the tuple-check interface (`--tuple-check DIR`, exit 3, green arm); the live-object audit (15/18 live-equal, 3 host-absent bound to build receipts); the predictor correction rationale (42.2 % refusal rate without the `published`-derived `reached` — plausible against the r42 manifest where C02's `declared_extras` show `max_depth 1` beside a failing root chunk); the R42-V2 prefile-gate remedy; the SKILL status-marker placement rule (appended to the line *before* the marker, so the frozen region — marker line → table end, whose hash I verified — stays byte-identical).

## 7. Residual risks and verification gaps

- `tools/round-43/` does not exist yet (executors build the ports); M1's restored clauses and amendment 1/3's specs are the contract the L1 must diff the ports against before freezing. The counter's selftest (74/74 claimed) should be re-run by the integrator, not re-verified here.
- R43SentProv's receipt wrapper was still running at review time; M4/S3/S8 name what it must produce — I did not see its output.
- The r43 held-out set does not exist (post-freeze data, by design); the `combo_unseen_majority ≥ 12` floor is seed-dependent (r42 drew 19) — an honest fail-possible binding, correctly labeled.
- S135's sha is verified from the live upstream; S136/S137 are unnamed, so their content cannot be checked (M3).
- Gate `--selftest` passed 23/23 in R42LocalSrc's round; I did not re-run it (nothing about the gate changed).

Report: `.ufo/waves/round-43/w1/R43RevClaims.md` · artifacts: `.ufo/waves/round-43/w1/artifacts/R43RevClaims/{gate-at-base-6b9e64fe.json, unblob-26.6.4-LICENSE}`
