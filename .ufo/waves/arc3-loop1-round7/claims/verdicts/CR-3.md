# CR-3 — arc3-loop1-round7 reconciliation

Seat CR-3, verdicts/convergence chain, 2026-10-19. I compared the frozen claims with peer artifacts and re-ran the relevant checks. The working tree was at records HEAD `ebdcc8eb1cf01134e9ed01f2402fe97736a8b804`; the frozen work revision is `2fba56fe7d54cfb94ca9332c11cea81667b3b289`. The current census gate is SHA-256 `8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca`. Scratch runs used `/var/tmp`; the only repository write from this seat is this verdict artifact.

## Rulings

- **C1 operability — BLIND SPOT REPRODUCED; RV-2 IS THE NARROWER SCRATCH CANDIDATE.** Correct the frozen pointer locator to `~/.kimi-code/config.toml:3546`; `:3298` is a historical receipt suffix. RV-2's candidate preserves clean PASS and fails on a dead pointer. It remains unlanded; do not combine it with PL-2's broader variant.
- **C2 coverage — BOUNDED PATH/CANONICALIZATION RESULT REPRODUCED; LANDING HOLD.** EX-6's one-verb result is reproducible, but it does not derive the full Evidence-ID formula. Its draft lacks the required opening `recheck:` field and its recipe omits two tested dimensions. The reported 86/86 result is an in-memory overlay, not a post-landing Command A measurement.
- **C3 calibration — LIVE COUNT REPRODUCED; NO-EDIT ADJUDICATION RECORDED.** The cache has 1,350 archives, 206 fewer than the dated 1,556 receipt. Keep that receipt as a 2026-10-13 historical observation; `PROVINCE.md:50` remains an unqualified current-count residual.

## C1 — pointer census blind spot

The baseline command `python3 .ufo/gates/c1-census-v10.py --json` exited 0 / PASS. Output: Province 162 lines / 6 loci; Scorecard 1,757 / 9; Skill 413 / 2; `current_ok_per_file={"PROVINCE.md":17,"SCORECARD.md":14,"SKILL.md":3}`; `frontier_rows=14`, `frontier_errors=[]`, `g2_ok=true`, and all stale/ambiguous/undeclared/unresolved/scope-error/G11 counts were zero. The JSON had 19 keys.

Direct classification of `PROVINCE.md:18` in block `15-26` emitted only the `pin` assertion (`kimi`, `6.7.0`, `current-ok`), not a `ptr` assertion. The instrument code at `.ufo/gates/c1-census-v10.py:525-530` filters path occurrences when another locus exists. The physical line names `~/.kimi-code/config.toml:3546` as the 2026-10-19 re-read and `:3298` as a historical receipt pointer (`PROVINCE.md:18`). The path-bearing `PTR` regex matches `:3546`; the bare `:3298` text is not a full path match. Direct calls to `ptr_check` for both lines returned `stale` because neither config line contains a `rea-agents` pin; the current pointer is therefore genuinely unevaluated by baseline classification, not current by `ptr_check`.

I independently ran RV-2's scratch candidate, SHA-256 `1e7ee0d9b7c89074de9eef37c0da4f8684848f59450219192b329e81c6822f8c`:

```text
python3 /var/tmp/kaidoku-rv2-arc3-r7.o_aelzy4/c1-census-v10-ptr-rv2-final.py --root /var/tmp/kaidoku-rv2-arc3-r7.o_aelzy4/clean-tree --json
exit=0 verdict=PASS
counts: PROVINCE 162/6, SCORECARD 1757/9, SKILL 413/2
current_ok_per_file: PROVINCE=20 SCORECARD=14 SKILL=3
frontier_rows=14 frontier_errors=[] g2_ok=true declared_fail_classes=[]

python3 /var/tmp/kaidoku-rv2-arc3-r7.o_aelzy4/c1-census-v10-ptr-rv2-final.py --root /var/tmp/kaidoku-rv2-arc3-r7.o_aelzy4/seeded-dead-pointer-final --json
exit=1 verdict=FAIL
unresolved: PROVINCE.md block 15-26, pointer line 18, :999999 beyond EOF (4150 lines)
frontier_rows=14 frontier_errors=[] g2_ok=true
```

PL-2 is a different, broader patch candidate. VZ-1 reports its clean counters as 21/16/3 versus RV-2's 20/14/3 and notes its receipt/scope behavior differs; both patch texts are scratch-only (`claims/verdicts/VZ-1.md:24-30`). Select RV-2 for the frozen current-pointer gap; do not combine their code or counters. No gate edit is authorized by this reconciliation.

## C2 — bounded Evidence-ID characterization

Command A was run against the frozen work commit using the recipe at `SCORECARD.md:88-124`:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":85,"mapped":85,"missing":[],"revision":"2fba56fe7d54cfb94ca9332c11cea81667b3b289","rule_blocks":15}
```

Using REA 6.7's installed CLI script and the retained 1,517-byte carrier, I repeated six calls under `/var/tmp/cr3-r7/evm` with `node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-evm-interface <path> raw --format json` (the relative-path case ran from `/var/tmp/cr3-r7/evm`; the TMPDIR case changed TMPDIR from A to B). All calls had input SHA-256 `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`, 15 normalized functions, 15 unique selectors, and function-payload SHA-256 `3394626e1e49bdb2714faf1fbc942f20dfcbd2a35547a2de18e3c2005adbe1ce`.

- Repeating the absolute `A/carrier.bin` path returned `ev_dbed853a2cfecc2db20836776b783ab83419f8c016c6b81b01ad8bafe5ce8ea7` both times.
- The same resolved path via a relative argument and with `TMPDIR` changed returned the same ID and equal response data.
- Identical bytes at `B/carrier.bin` returned `ev_cd6cfc4279cbdf43afcd1cf36ed6a9161f896ecd39064c3787f993f5da94a6db`; identical bytes renamed to `A/renamed.bin` returned `ev_7e27999fb2cb2c68aff9ff286459ceb7ac3f36cf7728a52cb31b81eb6075825e`.

This independently reproduces the bounded path effect recorded by EX-6 (`claims/c2/EX-6/evidence/matrix-summary.txt:10-19`) and CN-1 (`claims/verdicts/CN-1/evidence/evidence-id-domain/`): same-path repeats and equivalent path spelling/TMPDIR are stable, while a changed parent or basename changes the ID with decoded bytes and normalized functions unchanged. Raw IDs differ across the peers' distinct scratch roots, as expected from that path sensitivity; compare carrier/function hashes, not IDs across roots. The full ID formula remains unverified.

I select EX-6, not the alternative Vyper drafts, as the one C2 candidate, consistent with VZ-1 (`claims/verdicts/VZ-1.md:32-46`). Its entry draft currently has `source:` and `verified-at:` but no opening `recheck:` field (`claims/c2/EX-6/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md:10-12`); the contract requires all three opening fields (`~/.kimi-code/skills/shokunin/protocol/CORPUS.md:17`). The recipe at draft lines 36-49 also omits the basename-renamed and relative-argument variants in its evidence matrix. Correct the draft/recipe before landing. VZ-1's 86/86 overlay (`claims/verdicts/VZ-1.md:36-44`) is projected in memory only; no corpus entry/map token has landed and no after-landing Command A run exists.

## C3 — pacman archive count

Fresh read-only measurements on 2026-10-19 agreed:

```text
find /var/cache/pacman/pkg -maxdepth 1 -type f -name '*.pkg.tar.zst' -printf 'x' | wc -c -> 1350
Python pathlib direct-child regular-file count                               -> 1350
1350 - 1556                                                                 -> -206
```

The 1,556 figure is in `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`, explicitly `verified-at: 2026-10-13`. It is a dated cache inventory receipt, not a current count. I record the frozen claim's allowed **no-edit adjudication** here: retain it as a historical observation because archive inventory varies with cache retention. This count says nothing about current signatures, signature coverage, archive bytes, or package integrity. The same adjudication does not date the repeated 1,556 in `PROVINCE.md:50`; flag that summary as discrepant if read as a live inventory. Any Province/source correction needs separate authorization. C3 peers agree on the live count/delta; their erratum versus no-edit preferences are both allowed by the frozen claim.

## Write boundary and follow-up

No gate, corpus, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, or `LOG.md` was changed. C1's selected patch remains unlanded; C2 is blocked on the draft/recipe correction and a real post-landing Command A run; C3 records no corpus/source edit and leaves the `PROVINCE.md:50` residual for separately authorized work. This reconciliation is per-claim, not a scalar round verdict.
