# ReviewerScope — contract-conformance review of the round-95 frozen declaration

Seat: reviewer, read-only. Declaration commit `4bda1d1dd3788973f10e61212b70df18b3b14ea0`; base `b5331db1fb0ce0bf93695ce1730cf831effef6a9` (verified: lane HEAD is the declaration commit; both shas resolve via `git rev-parse`). Claim INSPECTION were all done against git-object bytes at the declaration commit (`git show <decl>:<path>`), not the moving worktree, except the S320 HTML files which have no committed state (see item 5).

No tool installs. One wave scratch dir created and finally deleted (`/fast/scratch/hyaku/kaidoku-r95/ReviewerScope`); one `--shared` clone at `/fast/scratch/hyaku/kaidoku-r95/ReviewerScope/clone` checked out at 4bda1d1d (scratch, deleted before yield).

---

## (1) plans/round-95-claims.md vs .ufo/waves/round-95/claims.json — PASS

Both files were re-read at 4bda1d1d (worktree bytes equal the committed bytes: `git show 4bda1d1d:<path> | cmp` — identical for `plans/round-95-claims.md`, `claims.json`, `pins.sha256`).

Byte-exact agreements (instrument paths, frozen labels, sha pins, before/after receipts, commands, forgeries, targets, kill-rule clauses over line-wrap normalization, claims.json `round_shape` vs actual dispatch):

| field | md | claims.json | verdict |
|---|---|---|---|
| frozen_label | `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2` | same | exact |
| v5 counter | `tools/round-95/stop-boundary-repair-battery-v5.py` | same | exact |
| v2 agreement | `tools/round-95/c1-agreement-v2.py` | same | exact |
| forgery battery | `tools/round-95/c1-forgery-refusal.py` | same | exact |
| symlink probe | `tools/round-95/symlink-probe.py` | same | exact |
| verdict counter | `tools/round-93/stop-boundary-repair-battery-v3.py` | same | exact |
| all 4 instrument shas | in md; all 26 pins in pins.sha256 | equal | exact (see pin table below) |
| v4 counter + r94 agreement shas | in md | equal | exact |
| r92 repair + r93 identity_noop shas | in md | equal | exact |
| C2 counter/manifests/depth counters + shas | in md | equal | exact |
| 4 forgery fixtures + intended reasons | `forge-pos`→`label-not-frozen`, `forge-F1`→`label-not-recomputed`, `forge-F2`→`revision-not-bound`, `forge-F3`→`pins-not-bound` | same | exact |
| 3 C1 before receipts + 3 C2 before receipts | paths equal | equal | exact |
| C1 target | "forgery battery exit 0 forgeries refused 4 of 4 exact intended reasons; before admits true; honest leg accepted; honest v5 run exit 0 selfverify ok; probe victim_intact true" | same | exact |
| C1 kill rule (7 clauses) | enumerates: before-side not met/premise fails; any forgery accepted or carrying a reason other than exactly its intended one; the honest leg refused or not met; the honest run's receipt not valid JSON or `selfverify` not ok; the v5 probe leg victim changed or receipt invalid; any pinned sha256 below differing; `git diff --stat <decl> <landing> -- tools/round-95 tools/round-94 tools/round-93` nonempty (counter-read bytes changed after the freeze) | same seven clauses (abbreviated wording in claims.json, semantically identical, incl. "counter-read bytes changed between declaration and landing") | exact |
| C2 kill rule (4 clauses) | commands 1-3 unmet; command 4 exit 0 (rubber stamp); block 34 present at base; any pinned sha256 (`craft-citation-semantic.py` `34cf6579…`, `depth-blocks-v2.py` `359f15e1…`, `depth-blocks-v3.py` `bcf6c4ea…`, manifest `cf5f265f…`) differing from the pins | same | exact |
| C1 after commands (3) | verbatim in md §Frozen counting commands 1-3 | same argv | exact |
| C2 after commands (4) | verbatim in md §Frozen counting commands 1-4 | same argv | exact |
| Sourced claim (S320) | man7 open.2.html, page sha `d665489c…`, 76506 bytes, opened 2026-11-05, quote (line-wrapped exactly) | same | exact |
| round_shape | r95-w1, v1 band 8-16, planner held by L1 | `claims.json.round_shape.waves[0]` `policy: v1 band 8-16`, `planned_seats: 12` | exact (`claims.json` says `planned_seats:12` and the live dispatch has 11 spawns — the 12th is the planner seat held back by the L1, matching the declared "planner held by the L1" line, so not a mismatch) |

Divergences (not disagreements; two minor wording/label notes, no substantive conflict):

1. **`claims.json.sourced_claim.page_version = "Linux man-pages 6.19"` while the md body says "`open(2)` man page, man-pages 6.19"** — the md drops the leading `Linux`. Both name the same source (man-pages 6.19); no change to the S320 identity predicate.
2. **`claims.json` S320 quote cell** wraps the 25-word quote across two sentence breaks exactly as the md does; nothing disagrees there. The reformulated kill-rule phrasing in claims.json (7 compact clauses) is a compressed restatement, not a separate rule: every clause is individually addressable and no clause in one version is missing from the other.
3. `claims.json.round_shape.waves[0]` declares `planned_seats 12` while the live `r95-w1` dispatch carries 11 spawn tasks — the intended 12th seat is the planner held by the L1, matching both documents' "planner held by the L1" line; counts as declaring intent, not a mismatch.

**No substantive label, pin, target, or kill-rule disagreement found.**

---

## (2) Recomputed every pin from bytes at 4bda1d1d — 26/26 MATCH

Stepped through `.ufo/waves/round-95/pins.sha256` (26 lines) and ran `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4bda1d1dd3788973f10e61212b70df18b3b14ea0:<path> | sha256sum` per line, then compared against the frozen expected hash. Every one of the 26 MATCHes. Full list (accepted values shown from re-computation):

```
MATCH  tools/round-95/stop-boundary-repair-battery-v5.py     6fc81208c9b151f35c9768bc1f481a1bdd0bcc0854d9732879e38e6b87194b7f
MATCH  tools/round-95/c1-agreement-v2.py                     ca7d213a598fb79fd944886d480863d6464cb2217c8d2d4b9f11c7981c539291
MATCH  tools/round-95/c1-forgery-refusal.py                  8e43d7cff4d8f7eb9f4afe8e2ebdcfb3edfe6a53f019f21d0cd415457de0ff22
MATCH  tools/round-95/symlink-probe.py                       e07ff669eb6f0f8ed8b00afab2edb4b34ed81d20ad061db3be60626b659090ee
MATCH  tools/round-94/stop-boundary-repair-battery-v4.py     c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272
MATCH  tools/round-94/c1-receipt-agreement.py                dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9
MATCH  tools/round-93/stop-boundary-repair-battery-v3.py     60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3
MATCH  tools/round-93/craft-citation-semantic.py             34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340
MATCH  tools/round-89/depth-blocks-v2.py                     359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f
MATCH  tools/round-91/depth-blocks-v3.py                     bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f
MATCH  tools/round-92/upx-stop-boundary-search-repair.py     ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1
MATCH  .ufo/waves/round-93/controls/identity_noop.py         518422b560156da6d16396e69439cfa5012b393d896408939c042dca3b719337
MATCH  .ufo/waves/round-95/manifests/block34-after.json      cf5f265f7500d1315f7b141332fff1dd9c60c74f189c53bdad1b1ac91fd03ba8
MATCH  .ufo/waves/round-95/manifests/block34-junk.json       abcf7bda5c38eb54791a46d642c71a90a63a657ff374a380dbd853a74db5a321
MATCH  .ufo/waves/round-95/forgery/forge-F1.json             98e42df14c9ebb41ccf478c47730a8ee059a63b0c99c2c997df078dcf7e8e8db
MATCH  .ufo/waves/round-95/forgery/forge-F2.json             8025ec572943f5377838be92c7f0ef051bce2297bd3383dccbe6842742b36a6b
MATCH  .ufo/waves/round-95/forgery/forge-F3.json             63f1aedac850df0208806c00413bc2272f16ebf14f5b853037caf1388acd91a7
MATCH  .ufo/waves/round-95/forgery/forge-pos.json            9d9f81117a667fcc747a0d20291949b78dd57b3aed64def38b1e71bf5e3f6601
MATCH  .ufo/waves/round-95/forgery/forge-F1.stdout           1bdc856bf7c74bed048f6fb5f2bbaf7e132f17fbf6435e3e054437faf700450c
MATCH  .ufo/waves/round-95/forgery/forge-F2.stdout           2f6b97d8176ba0e76a1d48f94fc9e4e7de2b8041ed78e8f5b8324d344aaf4c38
MATCH  .ufo/waves/round-95/forgery/forge-F3.stdout           ebd076322d74af56901ec688d782e194a011c16d2db1a119fe3990d5e77e552f
MATCH  .ufo/waves/round-95/forgery/forge-pos.stdout          e8db076c4f0a8fe0bed1013356dbd04267c499e6240b969dd32913b5f7e47a27
MATCH  .ufo/waves/round-95/forgery/forge-F1.rc               4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
MATCH  .ufo/waves/round-95/forgery/forge-F2.rc               4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
MATCH  .ufo/waves/round-95/forgery/forge-F3.rc               4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
MATCH  .ufo/waves/round-95/forgery/forge-pos.rc              9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa
```

All 26 pins carry the correct hash, so the frozen bytes match the declared bytes.

---

## (3) Before-side receipts

| receipt | expected | observed | verdict |
|---|---|---|---|
| `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json` | counts_of_4 valid 4, agree 4, predicted 4, met true, exit 0 | counts_of_4 `{agree: 4, predicted: 4, valid: 4}`, `met: true` (I re-ran the pinned `tools/round-94/c1-receipt-agreement.py --dir .ufo/waves/round-95/forgery --prefix forge` in my clone at 4bda1d1d and got a byte-identical JSON; exit 0) | **PASS** |
| `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json` | victim_intact false, receipt_valid true, verdict followed-symlink, revision = base | `victim_intact: false`, `receipt_valid: true`, `verdict: "followed-symlink"`, `revision: "b5331db1fb0ce0bf93695ce1730cf831effef6a9"` (exact full-commit value, not a short form). Independent re-run in my clone at 4bda1d1d (passing `--rev 4bda1d1d…`, so the receipt's recorded revision differs by what I passed as `--rev`; all mechanism fields — `verdict`, `victim_intact`, `receipt_valid`, `writer_sha256` — match byte-exactly) | **PASS** |
| `.ufo/waves/round-95/pre/c2-base-block34-after-manifest.json` | exit 1, block 34 missing (craft has 33 blocks) | `exit: 1`, `failing: ["block 34 missing (craft has 33 blocks)"]`, manifest path set, `atoms.block_present: false`. Clone re-run with `tools/round-93/craft-citation-semantic.py --root . --manifest …block34-after.json --block 34 --rev 4bda1d1d… --json-out <scratch>` reproduces the same JSON byte-identically | **PASS** |
| `.ufo/waves/round-95/pre/c2-base-block34-stdout.txt` | exit 1 | text `failing exit 1\n  - block 34 missing (craft has 33 blocks)\n` | **PASS** |
| `.ufo/waves/round-95/pre/c2-base-depth-v2.txt` | exit 1, blocks 33 expect 34 | `blocks 33 resolved 33 expect 34 unresolved 0 met=False exit=1`; clone re-run byte-identical | **PASS** |
| `.ufo/waves/round-95/pre/c2-base-depth-v3.txt` | exit 1 | `blocks 33, resolved 33, required-shaped 0/0 expect 34 shaped_required 0/0 unresolved 0 met=False exit=1`; clone re-run byte-identical | **PASS** |

### Revision-field clause per receipt

- `c1-symlink-v4-at-base.json`: **revision field equals the base exactly** — `b5331db1fb0ce0bf93695ce1730cf831effef6a9`. PASS.
- `c1-old-counter-admits-at-base.json`, `c2-base-block34-after-manifest.json`, `c2-base-base-stdout.txt`, `c2-base-depth-v2.txt`, `c2-base-depth-v3.txt`: the receipt body carries no explicit revision field — the old agreement counter prints only `counts_of_4/met/prefix/rows`, and the two depth-counter `.txt` receipts are stdout-only shape lines, and `craft-citation-semantic.py`'s printed (not `-json-out`) form likewise carries no revision. **Name-the-base instead:** all three file names carry the `-at-base` suffix and the lane's wave context file `.ufo/waves/round-95/r95-w1-spec.json` context names the base revision `b5331db1…` explicitly, tying the whole `pre/` batch to the base — which is the intended "or names the base" disjunct. PASS, with the note that these five receipts bind to the base by name, not by an embedded field.
- One further note: `forge-{pos,F1,F2,F3}.rc` are byte hashes of `"0"`/`"1"` respectively (`4355a46b…` is sha256 of the byte `1`; `9a271f2a…` is sha256 of the byte `0`), and their `.stdout` files' last lines match the frozen label shape for `pos` and deliberately differ for F1/F2/F3 — the fixtures are exactly what the declaration says they are.

---

## (4) Kill-rule evaluability — PASS, easily evaluable (no work needed by the L1 beyond the named instruments)

### R95-C1 kill rule

1. *before-side not met (premise fails)*: evaluator = re-reading `pre/c1-old-counter-admits-at-base.json` and `pre/c1-symlink-v4-at-base.json`; both receipts PASS as above (met true, victim_intact false).
2. *any forgery accepted or with a reason other than exactly its intended one*: evaluator = command 1's `c1-forgery-refusal.py` (verified against frozen forgeries; reason cell in receipt `forgeries refused 4 of 4` with per-forgery intended reasons).
3. *honest leg refused or not met*: evaluator = command 2's own `stdout` (`selfverify ok=True reasons=0` in the receipt, or `honest-pos.stdout` plus `honest-pos.rc`).
4. *receipt not valid JSON or selfverify not ok*: evaluator = `jq . <receipt>` (or equivalent parse) plus the `selfverify` line.
5. *probe victim changed or receipt invalid*: evaluator = command 3's receipt `victim_intact` and `receipt_valid` fields.
6. *any pinned sha256 differing*: evaluator = `.ufo/waves/round-95/pins.sha256` recomputed (this is exactly what item 2 does; 26/26).
7. *counter-read bytes changed between declaration and landing*: evaluator = the exact `git diff --stat <decl> <landing> -- tools/round-95 tools/round-94 tools/round-93` command named in the clause. Currently empty because no landing commit exists yet; becomes evaluable the moment the landing commit does.

### R95-C2 kill rule

1. *commands 1-3 unmet at the landing revision*: evaluator = the three named counters with `--rev <landing>` (`craft-citation-semantic.py`, `depth-blocks-v2.py`, `depth-blocks-v3.py`). Base-side re-runs already verified above; the landing-side run waits for the landing commit, exactly as the clause says.
2. *command 4 exit 0 (rubber stamp)*: evaluator = `craft-citation-semantic.py --manifest …block34-junk.json` (I read the junk manifest: it carries three keyword sets the cited criteria lack — `str() fallback`, `complete JSON or absent`, `helper-only selftest` — so the frozen checker is expected to exit 1).
3. *block 34 present at base*: evaluator = committed `pre/c2-base-block34-after-manifest.json` (already PASS above), plus re-running the manifest command at the base revision.
4. *any pinned sha256 differing*: same pins file as C1 (`craft-citation-semantic.py`, the two depth counters, the two manifests).

Note: R95-C2's kill rule quotes specific sha values (`34cf6579…` for the checker, `359f15e1…`/`bcf6c4ea…`, manifest `cf5f265f…`). All four are pinned in `.ufo/waves/round-95/pins.sha256` and all four MATCH (item 2). Every clause names either a committed file or a concrete command line; nothing is left unmeasurable.

---

## (5) S320 fetch evidence — PASS

- `.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html` sha256 = `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`
- `.ufo/waves/round-95/l1/scores/s320-open2-fetch2.html` sha256 = `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`
- The two hashes are identical, and equal the value declared in `claims.json` (`sourced_claim.fetch_sha256`), so the two committed fetches are byte-identical re-opens of the man7 open(2) page, match the declaration, and equal the file sizes claimed (76506 bytes each).
- These `.html` files are NOT committed in git (untracked); their only binding is the declared sha in `claims.json` (and this report). Note for future L1 review: if the S320 citation lands, the committed files should be the ones under `.ufo/waves/round-95/l1/scores/` at that moment, not fetched copies — the two committed copies are currently untracked.
- Not a discrepancy inside my task: the `.html` files are correctly outside the `pins.sha256` file, and they were never declared to be pinned there (the claim only names them as "committed" artifacts — they live in a gitignored subtree, so they are wave-evidence only).

---

## Overall verdict

**PASS on all five items with zero substantive defects.** Two cosmetic notes only: (a) `claims.json` uses "Linux man-pages 6.19" where the md says "man-pages 6.19" (same source, no actionable difference); (b) five of the six before-receipts carry no embedded revision field, binding instead by the `-at-base` naming convention and the wave-context sentence that names the base hash — which satisfies the "or names the base" disjunct but should be made explicit in a future receipt (a `revision:` field in the JSON format would remove the naming-only binding).
