# CritClaims — round 52 pre-freeze attack on `plans/round-52-claims.md`

Seat: CritClaims (critic, leaf; no dispatch). Round base `c525de54…`, claims draft `ab0eafedc41402b43b41a4362084119578dfe7ce`.
Scope: sizing rules, the C1 do-nothing control (CTL-OLD), the C2 before-arm, causal separability, and the rule text.
Method: read-only lane access; offline probes in a fixture clone under scratch; no REA, no downloads, no commits, no lane writes.
Receipts: `receipts/probes.txt` (commands, exit codes, UTC, stdout sha256), `receipts/v5-base-labels.json`,
`receipts/census-probe-after-one-row.json`.

Severity: **critical** = claim as written cannot be closed as stated; **high** = false or unreachable clause; **medium** = clause the counter does not enforce or unnamed artifact; **low** = hygiene.

---

## 1. CRITICAL — the C1 closure predicate is not one command re-derivable over committed bytes

**Counterexample.** The predicate (claims lines 85–92) is `python3 -I -B tools/round-52/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --receipts corpus/evidence/round-52/c1 --json-out <OUT>`. The same predicate requires `carriers_matched == 4`, `projection_ok` (a live REA rerun, claims lines 104–113), `carrier_pin_ok`/`carrier_present` (vendor bytes from `/fast/scratch/…/carrier-cache`, which the claims say is not committed), and `census_rederived_ok` (an `unsquashfs` re-read of the carrier bytes). The round-50 counter this is ported from still requires `--pkg65` and exits 2 without it (`tools/round-50/c1-counter.py:2564-2566`, `usage: --root --rev --freeze --pkg65 required`). The predicate as written therefore names a command that cannot run and whose live clauses cannot be re-derived from committed bytes.

**Sizing-rule breach.** "Declare each after-state as one concrete value that the closure can re-derive with one command over committed bytes." The closure duties (`.ufo/prompts/closure/kaidoku-round-51.md` items 2–3) are greps, `wc`, `jq`, git and census counts over committed bytes; they do not run REA or fetch vendor images.

**Smallest correction.** Split the predicate into two named commands with one sentence each:
(a) **receipt-verdict** (closure-reproducible): the counter run in a mode that reads only `corpus/evidence/round-52/c1/<id>/after.json` and `.ufo/waves/round-52/l1/scores/c1-after.json` at REV, checks their sha256 against the score's `evidence_digests`, and reports `carriers_matched`, `bindings`, `bindings_false`, `exit_code`; (b) **live-measurement** (L1 only, data run): the `--pkg65`/`--carrier-cache` invocation, declared as not re-derivable at closure. Name the closure-readable fields explicitly. Do not claim "re-derivable over committed bytes" for the live clauses.

---

## 2. HIGH — "every binding true … each re-derivable by the counter" includes items the counter does not read

**Evidence.** Claims lines 167–172 list `SCORECARD.md` coverage head `141/141 → 142/142`, the LOG entry, and the entry receipt citations as landing bindings "each re-derivable by the counter". `grep -c 'SCORECARD\|LOG.md' tools/round-50/c1-counter.py` = **0**. The round-50 `BINDINGS` tuple (`c1-counter.py:432-434`) has nine names; none reads SCORECARD or LOG. The coverage-map clause itself is verified: at `ab0eafed`, 141 knowledge `.md` stems and 141 stems present in the `## Coverage map` section (`receipts/probes.txt` R6 line; python probe in this seat), so the `141/141` head is true, but no counter checks it.

**Smallest correction.** Enumerate the exact boolean binding names (the v2 `BINDINGS` tuple) with a field-to-document map. Move SCORECARD/LOG/receipt-citation checks to separately named acceptance checks, not counter bindings.

---

## 3. HIGH — the C2 before-arm is not generatable at the claims-draft base with any committed instrument (circularity), and its command is defective

Three independent defects in the same arm:

**3a. The `--freeze` ancestry gate.** The predicate includes `--freeze <FREEZE>`. The v5 instrument refuses a freeze that is not an ancestor of REV (`sqfs-triage-v5.py:1261-1263`). The freeze is a later commit, so the before-arm at `ab0eafed` exits **2**. Measured (R2, real resolved hash `1842addcef3458515859b928b92d9bbd0a46c5d5`): `sqfs-triage-v5: could not evaluate: freeze '1842addc…' is not an ancestor of 'ab0eafed…'`, exit 2. The claims text has zero occurrences of `ancestor`; the r51 CritClaims finding 1 (critical) on this exact issue is not applied.

**3b. The `--table tools/round-50-c3` flag does not exist.** `grep -c "'--table'" tools/round-50-c3/sqfs-triage-v5.py` = **0** (R4). `tools/round-50-c3/` holds only `sqfs-triage-v5.py`; the v5 table bytes live in `SKILL.md` at the base revision (block 26, `SKILL.md:548-585`), not in that directory. The before command as written cannot run.

**3c. Circularity.** The "1 violation" before-state is an output of the v6 executability audit, which the claim itself ships. No committed tool at `ab0eafed` computes `executability_violations`. What *is* generatable today: v5 labels over the 126 envelopes at base (R3: `pair_mismatches 0`, `evaluator_missing 0`, exit 0; labels in `receipts/v5-base-labels.json`); 7 `legacy-body-failure` envelopes, of which one (`dmg_Z3_v3ddwrt_inode_table`, ddwrt family) is the only one whose family is in the no-reader set (ddwrt 6/7 NO-READER, `receipts`/`reader-census.txt`). So the number 1 is reproducible by a ~10-line independent check over committed bytes, but only if that check is written, frozen and committed **before** the table lands, and it must read block 26 at BASE, not the v6 evaluator's action. The claims do not say this.

**Honesty verdict on 3c.** The audit *can* be an independent witness if (i) it is a separate pre-freeze script over `SKILL.md` at BASE plus the reader-census receipt, and (ii) the damaged body's own reader outcome is named. The current text does neither. The witness is also not fully independent of v6's table authority: the census is family-level, and the r51 CritTriV6 finding 2 notes that all nine damaged subject digests lack direct census rows. The claim should name the damaged sha (`839c17a8…`, per the r51 critic) and its own reader receipts as the witness, or state that the audit is a family-policy count.

**Smallest correction.** Freeze a separate witness script (`tools/round-52/`, registered) that reads block 26 at BASE and the named reader receipts; commit its before receipt in the freeze commit with the exact command (no `--freeze`, no `--table`); keep the v6 audit as the after-arm; state the family-level basis.

---

## 4. HIGH — `census_outside 0` at the landing is unreachable as written

**Counterexample (measured, R5).** In a fixture clone at `ab0eafed` I added one backticked registry row for `tools/round-52/c1-counter.py` inside the `instrument-registry v2` block and committed it (fixture only). `python3 -I -B tools/round-51/census3.py --root <clone> --rev HEAD --check` → **exit 1**, `registry_paths 57`, `census_paths 56`, `census_outside ["tools/round-52/c1-counter.py"]`.

**Consequence.** The claims require every new `.py`/`.sh`/`.json` under `tools/round-52/` to get a registry row (Registry bullets, claims lines ~112 and ~200). That is ≥7 new rows (`gap-rule.json`, `c1-counter.py`, `c1-controls.py`, `c1-run.sh`, `fetch-vendor.py`, `misroot-sweep.sh`, `sqfs-triage-v6.py`). Unless `tools/round-51/census3.json` is regenerated, the after-state has `census_outside ≥ 7`, so C2's "`census_outside 0` at both before and after" is false. The claims never name the regeneration, and the v6 "embedded census clause" would read a stale artifact. The regeneration is itself a write to a round-51 artifact and must be named under the freeze.

**Smallest correction.** Name the `census3.json` regeneration as a freeze-commit item with its own before/after receipt; or drop the no-regression binding and count it as a named risk.

---

## 5. HIGH — causal separability is false, and a cross-claim obligation is not in C2's spec

**5a. Shared write surface.** Claims line 24 says the two claims "share no write surface except record sections in `SCORECARD.md` and `LOG.md`". Both claims add rows to the single `<!-- instrument-registry v2 -->` block in `SKILL.md`, and census3 reads that block (`census3.py:20-22,96`). Shared file alone is not fatal; the false sentence is the problem.

**5b. Unmet obligation.** The C1 law (claims lines 67–69) says R52-C2's block 27 "supersedes or scopes" SKILL's *"`symlink` and `special` both count"* phrasing. `grep -c special claims` = 1 (only that C1 line). The C2 spec (lines ~190–215) does not mention it. The SKILL text still reads, in block 26 rows `in-tree-symlink-metadata` and `mixed-symlinks`: "one `unpublished-entry` gap per link or special file" (`SKILL.md:~587-589`), which contradicts the device law: a char-device row carries **no** disposition. Under the C1 law the contradiction is live, and C2 as written does not remove it.

**Smallest correction.** Name one owner for the registry block and the special-node correction; add the correction to C2's block-27 spec with a grep-checkable sentence; restate separability as "C1 and C2 each read the other's frozen registry row, with the registry ordering frozen as a common prerequisite".

---

## 6. HIGH — the C1 projection retry policy has no pre-data control for either side, and the kill rule omits it

**6a. Unscored policy.** The retry policy (claims lines 104–113) is "claimed and controlled": only the deterministic-ENOENT side (`must stay red`) is described. The kill rule (lines 146–148) names CTL-NEW red, CTL-OLD = 4, and mutants green; it does not name the retry control. A retry policy with no committed control that it can succeed is unverified before data.

**6b. No control for `projection_ok` at all.** CTL-OLD and CTL-NEW evaluate the disposition verdict over committed envelopes (`gaps_ok ∧ nonregular_unpublished_ok`), so they cannot exercise `projection_ok`. A counter that has the law but no retry scores CTL-NEW 4/4 and still fails g7581 live. The claim's own "cheapest control that skips the claimed work" is therefore not committed for the second cause (the r50 miss has two causes; claims lines 98–104).

**6c. The evidence that supports transience is not cited.** The r50 g7581 failure is `execution_failure`, ENOENT on `readlink …/usr/www.myfritz/avme/cgi-bin/luacgi` on the **rerun**. That path is a real oracle entry: `tools/round-50/oracle/g7581.nonregular.tsv:774`, `usr/www.myfritz/avme/cgi-bin/luacgi  symlink  /usr/www/cgi-bin/luacgi`. In the committed **data-run** envelope `corpus/evidence/round-50/c1/g7581/after.json` the same link is an `unpublished_entries` record and an `unpublished-entry` gap (`relative_path firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi`), and it is **not** in `MaliciousSymlinkRemoved`. The same bytes succeeded in the data run and failed on the rerun. That asymmetry is the best evidence for a transient, and it is not in the claim.

(Retracted: an earlier probe of mine suggested this path was absent from the oracle. It is present at line 774. The r51 CritRuleDerive statement holds.)

**Smallest correction.** Add two frozen fixtures to the kill rule: a transient-ENOENT fixture (fails attempt 1, succeeds attempt 2 → green) and a deterministic-ENOENT fixture (fails all attempts → red). Cite the data-run/rerun asymmetry as the stated reason for the policy. Add a pre-data control that exercises `projection_ok` with the law but no retry, expecting red on g7581.

---

## 7. HIGH — a false factual premise in the C2 rationale

**Evidence.** Claims line ~218: "The two clean ddwrt no-pad `_ddefault` envelopes keep `clean` (their readers succeeded; no route change)." The committed reader census (`git show ab0eafed:.ufo/waves/round-50/w3/ExecTriageV5/receipts/reader-census.txt`) lists `squashfs_v3_ddwrt` `squashfs_v3.be.nopad.bin` (`daa8e72d355d`) and `…le.nopad.bin` (`e7482db480f9`) as **NO-READER (both refuse)**, unsquashfs exit 1 and 7z exit 2. Only `squashfs_v3_le.bin` is readable. The sasquatch extraction succeeded; the independent readers did not. The two `_ddefault` envelopes are therefore on no-reader bytes, exactly the residue the r51 CritTriV6 finding 1 names.

**Consequence.** A keep-`clean` decision may stand, but on a false premise. The claim must say "sasquatch succeeded; readers refuse; `clean` is kept as an extractor-success label, disclosed as oracle-less", and the audit scope (FAILED-body only) must say that the two clean rows are outside it.

---

## 8. MEDIUM — CTL-DN is not a semantic do-nothing; CTL-OLD is not pinned per carrier

**CTL-DN.** Claims lines 134–135: "the v2 counter against a do-nothing fixture tree (no receipts) exits 1 or 2, never 0", labelled "semantic red". An empty tree is missing input; a counter that cannot evaluate passes it. This is the r51 CritClaims finding 6 again, unapplied. Rename it a fail-closed input control and pin one exit and one reason.

**CTL-OLD.** The claim pins the aggregate "2 of 4". Committed round-50 values confirm the per-carrier vector `{c6430: gaps_ok true, c6490: true, g7581: false, g7582: false}` (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`; `carriers[*].gaps_ok`). Pin the vector, and make any deviation (not only "yielding 4") a stop.

---

## 9. MEDIUM — "round-52 carrier table" is an unnamed artifact

**Evidence.** Claims line 80: "the four pins are listed in the round-52 carrier table's `prior_pins`". No path is named. The existing committed table is `tools/round-50/carriers.json` (four vendor carriers, `prior_pins` absent; `target 4`, `projection plus-extractor`). The claim also says `tools/round-50/carriers.json` joins `PRIOR_CARRIER_TABLES`, which is a different thing. The r51 CritClaims finding 8 is unapplied.

**Smallest correction.** Name the exact committed path and schema; put it in the frozen set; add a negative control (a fifth unlisted pin is rejected).

---

## 10. MEDIUM — the coverage axis label is contestable under the fleet's own rule

**Evidence.** Claims lines 62–63 and 77–82: the four carriers, pins and bytes are unchanged from round 50; the new input is a corrected rule; the promotion `hsqs` Frontier → Core rests on the 4/4 re-measurement, "not on new carrier coverage". The sizing rule (claims ~line 200, kaidoku r29) says re-scoring a rule the lane already holds on new inputs is quality work, never coverage. Here the rule is new and the inputs are held. Frontier→Core is listed as a coverage surface, so the label is defensible, but the claim is one re-scored measurement with a changed rule.

**Smallest correction.** Leave the label to the canonical judge, but state the reasoning in the claim: the coverage surface is the frontier entry, and the measured input is held by design (option b). Do not describe the 4/4 as new coverage evidence.

---

## 11. MEDIUM — C2 mutation battery and selftest are not enumerated, and not in the counting command

**Evidence.** Claims lines ~188–200 name "the committed mutation battery" and "a green selftest" but not the mutation IDs or count. The v5 CLI runs `--selftest` as a separate mode (`sqfs-triage-v5.py:2267`). The predicate command (line ~206) does not include `--selftest`. The r51 CritClaims finding 7 is unapplied.

**Smallest correction.** Enumerate mutation IDs and count; name the selftest command as a separate acceptance check with its own exit code, or make the counting command run it.

---

## 12. LOW — the C2 changed-pair set is named only partially

**Evidence.** The claims say "only the named ddwrt pair changes". The before/after set should be pinned: one pair, `dmg_Z3_v3ddwrt_inode_table`, `legacy-body-failure/cross-read-legacy` → `legacy-body-unreadable/preserve-unresolved`; legacy-body-failure population 7 → 6; new label population 0 → 1 (measured base population: 7, `receipts/v5-base-labels.json`).

---

## Sizing and control checks passed (no finding)

- **CTL-OLD is the cheapest skip-the-law control.** Measured consistency: under the round-50 rule the four carriers give `gaps_ok` `{T,T,F,F}`, matching the committed score (see §8). The full predicate's do-nothing is already committed: the round-50 counter at its freeze exits 1 at `carriers_matched 2` (`c1-after-attempt2.json`).
- **The law's arithmetic holds on committed bytes.** Oracle char-device rows: c6430 1, c6490 1, g7581 13, g7582 13 (total 28). The FRITZ!Box 13 include `dev/led 247:0`, so twelve others, as the claims state. Every oracle symlink on all four carriers is accounted (`unpublished-entry` gap or `MaliciousSymlinkRemoved`): 639/639, 639/639, 613/613, 568/568 (fixture-free check, `receipts/probes.txt` not repeated here; re-derivable with the committed `after.json` and `*.nonregular.tsv`). Device rows are the only unaccounted class, so the "no disposition for a device" law fits the data.
- **depth-limited gap fields** (`input_path` `$output/firmware.bin_extract`, `continuation_id` `3b54e297…`, `relative_path` null) are present in all four envelopes, as F8 requires.
- **C2 v5 labels at base:** 126 envelopes, `pair_mismatches 0`, `evaluator_missing 0`, exit 0 without `--freeze` (R3; `receipts/v5-base-labels.json`).
- **Knowledge coverage map:** 141/141 stems mapped at `ab0eafed` (§2).

## Limits

- No REA invocation, no vendor download, no commit in the lane or fleet repo. Git writes were confined to a `git clone --shared` fixture under scratch (`git rev-parse --show-toplevel` checked before each commit).
- Probes are offline and cover the v5 tool and census3 only; the v6 and v2 instruments do not exist, so their behaviour is inferred from claim text, not executed.
- The reader-census outcomes for the damaged ddwrt sha are cited from the r51 CritTriV6 receipts, not re-run here.
- The r51 "`provider_timeout` is a proven flake class" wording is not verified by this seat.
