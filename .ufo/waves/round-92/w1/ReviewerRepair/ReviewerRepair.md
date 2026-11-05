# ReviewerRepair — round 92 (seat 2a) — attack the R92-C1 frozen predicate and counter

Lane: kaidoku. Declaration commit measured: `11f8606178dfd9e72001b31daf412c5463106a63` (HEAD of `$S/clone`).

## Instruments I wrote

All in the seat dir `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/w1/ReviewerRepair/`:
- `attack-cheat_pinned_pack.py` (8a93c0c1d090160a9bc179b9ed5159e5eb05bea56ea2eb2bc5518770fdc73749) — Q1/Q2 counterfeit: identifies the carrier among the five pinned paths by diffing, then decides purely from the 4-byte window delta ≤16 (NO packer verdict, NO `upx -t` run); writes the carrier's pristine packed bytes cached under `$TMPDIR/cheatcache`. Far/refuses otherwise with a typed refusal.
- `attack-identity_pass.py` — Q4 identity passthrough: always rc 0 and output == the input unchanged.

All frozen-counter runs were executed inside a fresh clone at the frozen commit with `python3 -I clone/tools/round-92/stop-boundary-repair-battery.py --root clone --repair-cmd <candidate below> --work <scratch> --rev attack-11f8606 --expect 'repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10' --json-out receipt.json`.

Q1 first-run notes (honest defect trail): the initial prototype had a bug (`cur <= stored` bound that wrongly rejected +7/+40 value cases). It scored 5 of 10. That buggy variant was re-run under the frozen counter and its receipt is preserved: `receipt-attack1-cheat-partial.json` (`repaired 5 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met False, exit 1). The fixed prototype then scored the full label: `receipt-attack1-cheat.json` (rc 0, met True). Both receipts plus the fix diff (single-line: `0 < cur <= stored` → `0 < cur ... and cur != stored`) are on disk in this seat dir for audit.

## Walk91 receipt (evidence for Q5)

```
# rebuild a tampered jq cell (−7 on the last block)
python3 -I  (from probe snippet) … tampered block 9911 stored 174
# round-91 tool directly on the tampered cell:
python3 -I clone/tools/round-91/upx-stop-boundary-repair.py --in probe/jq-tampered --out probe/jq-out
  → rc 2; stdout: {"tool": "tools/round-91/upx-stop-boundary-repair.py", "class": "T7-chain-stop-boundary",
     "refused": "stop-boundary: the walk's last storable block has no successor that accounts for the declared
                 u_len (30800) and `upx -t` refuses the input (prefix 5 blocks, stored_total 22585); this class
                 is refused, not repaired"}
  out-file-exists: no
# round-91 tool on the intact packed bytes:
python3 -I clone/tools/round-91/upx-stop-boundary-repair.py --in probe/jq-packed --out probe/jq-out-i
  → rc 0; stdout: {"break_index": null, "class": "intact", "delta": null, "derived_sz_cpr": null, "stored_sz_cpr": null}
```
`walk91.txt` and `walk91-intact.txt` (in the seat dir) hold the two stdout transcripts.
`probe-info.json` (seat dir) records per-carrier: packed sha256, block count, last block offset, `sz_cpr`, `sz_unc`, two-pack determinism, in-range counts for ±7 and ±40, and 33 legal values inside the ±16 window on every carrier.

---

## (1) Can a repair pass the frozen label without the packer verdict?

**Exactly one command, run three times.** Exit codes recorded below. **Result: YES, rc 0 — packer verdict is NOT needed.**

```
run 1 (buggy prototype, cur<=stored bound left in):
  python3 -I clone/tools/round-92/stop-boundary-repair-battery.py --root clone \
    --repair-cmd tools/round-92/attack-cheat_pinned_pack.py --work $PWD/run-cheat/work \
    --rev attack-11f8606 --expect 'repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10' \
    --json-out $PWD/run-cheat/receipt.json
  → rc 1; stdout: "repaired 5 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10 met False exit 1"
  copy: receipt-attack1-cheat-partial.json
run 2 (fixed bound, drops cur<=stored, keeps only delta<=16):
  same command, --work $PWD/run-cheat/work2
  → rc 0; stdout: "repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10 met True exit 0"
  copy: receipt-attack1-cheat.json
run 3 (identity passthrough, unrelated to packer verdict):
  same shape with --repair-cmd tools/round-92/attack-identity_pass.py, --work $PWD/run-ident2/work
  → rc 1; stdout: "repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 0 of 10 met False exit 1"
  copy: receipt-attack2b-identity-donothing.json
```

**Severity: HIGH.** The frozen R92-C1 counter (`tools/round-92/stop-boundary-repair-battery.py`, sha256 pinned in `claims.json` at `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc`, verified) counts `repaired` purely structurally: `rc == 0 AND out == packed`. It never references `v2.packer_test` (the `upx -t` verdict helper) anywhere in `score_cell`, `score`, or `main`. A carrier-read counterfeit that knows only (a) the five carrier paths and (b) "if the file differs from the pristine packed bytes in <4 bytes, restore them" passes the entire frozen label without ever asking the packer. This is exactly the class of counterfeit the round-91 CriticClaims defined and R92-C2 was supposed to kill: the C1 coverage claim's `met_target true` is therefore **admitting a cheat, not measuring a repaired capability**. A candidate built in the round-92 wave (`tools/round-92/upx-stop-boundary-search-repair.py`) could produce identical numbers with zero genuine unpack-repack reasoning if it embeds the same carrier table.
Receipt: `receipt-attack1-cheat.json` (met True, rc 0, counts `repaired 10 / wrong 0 / unsafe 0 / intact 5 / far-refused 10`).

## (2) Is `out == packed` a sound identity check?

**Result: the check is sound only insofar as the packer is deterministic on this host — which I measured true (three independent `upx --best` runs on each of the five carriers are byte-identical; see probe log below); it is NOT sound as a repair-definition in general and does not consult the packer verdict at all.**

- Three independent `v2.pack(src, work, env)` calls (fresh scratch dirs) for each of the five carriers produced byte-identical output; all three `packed_sha256` values match the frozen counter's own receipt field `carriers[cid].packed_sha256` exactly (`jq e8b6c9e76b54...`, `xxd 1727faf91c38...`, `libz a9c544e6da4f...`, `dinit b67ce1bdda27...`, `xz-unseen a7b4d929441c...`). Receipt: `receipt-attack1-cheat.json` (carriers block), probe log: `probe-info.json`.
- Command: `v2.pack()` invoked thrice per carrier, each inside a fresh mkdtemp box; sha256 compared via `hashlib.sha256(fresh).hexdigest() == d["carriers"][cid]["packed_sha256"]`. Exit 0 (all five matched, 5/5 `third-pack match: True`).
- **Defect (Q2, MED):** because `repaired == (out == packed)` with no `packer_test(out)` call, a byte-identical output is counted as `repaired` even if the tool wrote that output without ever validating it green via `upx -t`. A smuggled-in pristine image (our Q1 counterfeit) or an output produced by arbitrary mechanics (e.g. reading the packer cache from a temp file the caller happened to have, or steganographically-sized segments) is indistinguishable from a genuine derive-and-restore. Anchoring to `packed` also hardwires the counter to the packer's byte-level determinism: on a packer version where `--best` output varies (e.g. embedded timestamps), an honest tool that restores bytes correctly *and* returns green would be classified `wrong` or `unsafe`, a false negative that suppresses credit without any counterfeit. Neither direction is exercised in the current counter because the packer IS deterministic on this host.

## (3) Far cells (+/-40): range and refusal-arm scope

**Result: every far cell is in range for all five carriers (10 far cells, all `0 < value <= sz_unc`); the far refusal arm counts only `class == "refused"` (code: `far_refused = sum(1 for c in far if c["class"] == "refused")`, which excludes `repaired`, `silent`, `unsafe`, `wrong`, `other`).** No leakage or out-of-range far cell observed in the cold run or in any of the three counter runs (all 10 `far_class = refused` in `receipt-attack1-cheat.json`). **Severity: LOW — no defect found.** Far values (delta -40/+40) for each carrier at block offset recorded in `receipt-attack1-cheat.json` (`far values: [('jq',-40,134),('jq',40,214), ('xxd',-40,123),('xxd',40,203), ('libz',-40,16972),('libz',40,17052), ('dinit',-40,4273),('dinit',40,4353), ('xz-unseen',-40,812),('xz-unseen',40,892)]`).

## (4) Could a repair that outputs the tampered input unchanged pass any arm?

**Result: NO for the scored cells; it fails the label.** The frozen counter's arithmetic counts a `silent` cell (output byte-identical to input, rc 0) differently from `refused`/`repaired`/`far-refused` and the `--expect` string is a fixed literal, so `repaired 10 of 10` and `far-refused 10 of 10` are simultaneously unreachable with any silent cell. Receipt `receipt-attack2b-identity-donothing.json`: counts `repaired 0 / wrong 0 / unsafe 0 / intact 5 / far 0`, exit 1, met False. **Severity: LOW — no defect found.** However, note (see Q1) that the label is achievable with a counterfeit that knows the carriers, so the safe-armed SKIP does not rescue the claim from Q1.

## (5) Does the do-nothing control honestly measure round-91 behaviour?

**Result: yes, and the frozen pre receipt agrees.** Read `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json` (declaration staging, not touched by me): label `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met False, exit 1, revision base-73a882712, repair command `tools/round-91/upx-stop-boundary-repair.py`. Manually re-drove the round-91 tool's STOP-boundary path under the frozen counter myself at the frozen commit (`$S/clone`): yields `rc 2` per cell with no output (`typed` per the v2 counter; positive-control receipt `c2-positive-v2-round91.json`, met True). So each cell counts as `refused` (the counter's only rc!=0-no-output arm), matching the frozen pre receipt, and the round-91 tool never writes the output for a stop-boundary cell (my direct call: `python3 -I clone/tools/round-91/upx-stop-boundary-repair.py --in probe/jq-tampered --out probe/jq-out` in clone → rc 2 JSON `{"refused":"stop-boundary: ..."}`, no output file; see `walk91.txt` for confirmation of the refusal body). The do-nothing control is honest: it genuinely measures that round 91 refuses all 10 cells and passes no intact cell, giving the frozen `met False, exit 1`. **Severity: LOW — no defect found.** Command: `sha256sum .ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json` (read-only; no edit).

---

## Severity table

| Q | Finding | Severity |
|---|---|---|
| 1 | Packer verdict not needed to pass the frozen label (`cheat_pinned_pack` replica achieves `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, met True, exit 0, with zero `upx -t` calls) | **HIGH** |
| 2 | `out == packed` rest on packer determinism (measured OK here) but does not consult `packer_test` on the output; a byte-identical smuggled image is indistinguishable from a repair | MED |
| 3 | Far cells all in range for all five carriers; far-refused counts only `refused` class | LOW (no defect) |
| 4 | Identity-passthrough scores all 10 as `silent`, 0 as `refused`/`repaired`, met False — cannot pass any frozen arm | LOW (no defect) |
| 5 | Do-nothing control honestly reproduces round-91 refusal-only behaviour at base revision | LOW (no defect) |

## Verification gaps and residual risk

- The packer-determinism probe covers five carriers on one host at one pinned/SHA-verified packer build; no claim that determinism holds on other hosts or packer versions.
- My Q1 counterfeit caches pristine packed bytes under `$TMPDIR/cheatcache` (`$TMPDIR` scratch, deleted after this seat's moves); the counterfeit's cache write is a persistence trick that a stricter counter could check (e.g. declaring that no fresh pack was made during scoring, or invoking `v2.packer_test(out, env, work)` before classifying a cell as `repaired`). I flagged this as a fix-up recommendation for the L1 wave, not executed.
- I did not modify any lane file; every counter run was done in a clone at the frozen commit (`git clone --shared` + `git -C clone checkout 11f8606...` verified `HEAD = 11f8606178dfd9e72001b31daf412c5463106a63`).

## Seat hygiene

- Seat dir: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-92/w1/ReviewerRepair/` (everything I wrote is there; nothing outside, nothing in lane tools/ or plans/).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r92/ReviewerRepair`: deleted at seat close (`rm -rf -- $S`), after copying into the seat dir: `receipt-attack1-cheat.json`, `receipt-attack1-cheat-partial.json`, `receipt-attack2-identity.json`, `receipt-attack2b-identity-donothing.json`, `probe-info.json`, `stdout-attack1-cheat.txt`, `stdout-attack1-cheat-partial.txt`, `stdout-attack2-identity.txt`, `walk91.txt`, `walk91-intact.txt`. (The identity runs' stdout is also reproduced inline in section (4).)
- No pacman, no pacman-shadowing. No lane git mutation, no sysctl, no `~/.local/bin` writes, no fleet-root tracked file writes.
