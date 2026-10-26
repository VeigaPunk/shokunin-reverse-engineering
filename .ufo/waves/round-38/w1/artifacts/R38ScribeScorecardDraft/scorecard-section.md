# SCORECARD round-38 section + LOG.md entry — DRAFT

Seat: `R38ScribeScorecardDraft` (leaf, wave 1). **Nothing here is integrated.** This file is the
drop-in text for the L1; every `[L1-FILL]` is a value that cannot be known before the after
receipts are committed and the landing revision exists. No lane surface was edited by this seat.

Observed inputs (read-only): base `77091b492cc53f8743bd0701b1e7d5e66123dd84`, freeze
`e059ca9391642d5b71b6662cabcbdce0d9308719`, controls commit
`efd5c47a72a50b3a434783f82268fb4a96e636a1`, claims `plans/round-38-claims.md`, counters
`tools/round-38/{c1,c2}-counter.py`, harness `tools/round-38/c1-run.sh`, carriers
`.ufo/waves/round-38/c1/carriers.json`, controls `.ufo/waves/round-38/controls/`, draft receipts
under `.ufo/waves/round-38/w1/artifacts/`.

---

## A. SCORECARD.md section (append after the round-36 section, before its trailing blank line)

```markdown
## Round 38 — standard big-endian SquashFS v4 to Core, and self-assessment mismatch to zero

Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`; freeze `e059ca9391642d5b71b6662cabcbdce0d9308719` (`plans/round-38-claims.md`); controls `efd5c47a72a50b3a434783f82268fb4a96e636a1`. Round 37 was an honest stop at the pre-freeze probe stage with no claim frozen (`corpus/lessons/round-37-verifier-spotcheck.md`); round 38 relaunches it and carries the routed defects R37-CL1..CL3 and R36-CL1..CL6. Both claims below were scored against the seven frozen controls before any claimed data; all seven controls exit 1 (`.ufo/waves/round-38/controls/`).

| claim | axis / surface | before | after | counting command | measured at | verdict (author) |
|---|---|---|---|---|---|---|
| R38-C1 | coverage — `PROVINCE.md` Frontier bullet `sasquatch` (big-endian/AVM note) → `## Round-38 additions to Core`; entry `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`; `corpus/SOURCES.md` row opened 2026-10-26; `corpus/README.md` coverage-map row | `carriers_matched 0`, `met_target false`, exit 1 at base and at the freeze; `carriers_unchanged false` at base only because `carriers.json` is absent there; bindings all false except `frontier_note`, already true pre-claim (`.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/c1-at-base.json`, `c1-at-freeze.json`; controls `ctl-c1-0-do-nothing.json`, `ctl-c1-1-three-carriers.json` → 3, `ctl-c1-2-wrong-handler.json` → 0, all exit 1) | [L1-FILL] `carriers_matched`, every binding, `carriers_unchanged`, exit | `python3 -I -B tools/round-38/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --freeze e059ca9391642d5b71b6662cabcbdce0d9308719 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>` | [L1-FILL] | [L1-FILL] — target is `carriers_matched == 4` and every binding true; see the draft-stage disclosure below before writing met/honest-stop |
| R38-C2 | calibration — SCORECARD `## Owned axes` / `## Capabilities` rows, SHONEN.md boxes, and PROVINCE `## Core` / `## Frontier` rows vs observed repo state | `mismatches 1`, `guards_ok false`, exit 1 at base and at the wave-1 tip; sole unresolved pointer `prov_core:REA MCP server` → `evidence/doctor/`; 48 pointers, `missing_units []`, `pointers_not_fewer true`, 7/7 internal assertions agree; command A 124/124 files mapped, 17/17 rule blocks; command B 9/9; craft range `SKILL.md:81-314`; Adjacent range `PROVINCE.md:97-125` (`.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/c2-at-base.json`, `c2-at-tip.json`; control `ctl-c2-0-do-nothing.json`; negative controls `ctl-c2-1-junk-count.json`, `ctl-c2-2-delete-bad-pointer.json`, `ctl-c2-3-substitute-other-document.json`, all exit 1) | [L1-FILL] `mismatches 0`, `guards_ok true`, exit | `python3 -I -B tools/round-38/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 --json-out <RECEIPT>` | [L1-FILL] | [L1-FILL] — target is `mismatches == 0` and `guards_ok` with the base's `evidence/doctor/` pointer repaired to a resolving pointer to the same document |

Owned scores: coverage 10 → 10 ([L1-FILL]: 124/124 knowledge files mapped at base and at the wave-1 tip, `git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'` → 124 and `## Coverage map` stems → 124, intersect 124; a landed round-38 entry makes it 125/125 and the row must be re-stated in the same landing); depth 10 → 10 (17/17 rule blocks resolved, same recount command; unchanged); calibration 10 → 10 (proxy saturated since luna-round-3; the move is the mismatch count [L1-FILL] 1 → 0, not a score). The finite proxies retire no domain axis. Provisional: no axis harmed by the round [L1-FILL at the landing revision]. Retired: none.

Capability row, conditional on the C1 landing admitting it:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| REA SquashFS recursion through sasquatch for big-endian v4 | `extract-firmware` publishes every regular file of a standard big-endian SquashFS v4 payload through unblob 26.6.4's `squashfs_v4_be` handler **when `sasquatch-v4be` is reachable on `PATH`**; with the extractor absent the same run publishes 0 bytes and reports `missing-extractor-dependency` naming `sasquatch-v4be`. AVM-BE and vendor-mangled images are not demonstrated | [L1-FILL] `corpus/evidence/round-38/c1/`; `tools/round-38/c1-run.sh`; `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` | round 38 |

Entry rule for that row: enter it only if the C1 landing stands and the receipts it cites show the handler name, zero gaps on every claimed carrier, and the extractor dependency stated as above. The dependency is part of the wording: `R38ExecAfterK3` measured arm A (clean `PATH`) at 0/4 oracle files with a `missing-extractor-dependency` gap and arm C (shim exposing only `sasquatch-v4be`) at 4/4 with zero gaps (`.ufo/waves/round-38/w1/R38ExecAfterK3.md` §2-3). The frozen predicate's prose "no external extractor dependency" is **not** satisfied by that measurement; the counter itself tests only `extraction_gaps == []`, so a receipt produced with the extractor present scores, but the claim's premise is falsified. The L1/closure must rule on this before the capability row or the C1 verdict is written. Draft-stage clause table (not claim data): `.ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/draft-carrier-clauses.tsv`, produced by `python3 -I -B .ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/draft-clauses.py --root .`; all ten draft envelopes recompute their stored evidence id under the 6.5.0 rule (`node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents 6.5.0 root> --pkg67 <same> *.wrapped.json`, exit 0, `.ufo/waves/round-38/w1/artifacts/R38ScribeScorecardDraft/xpin-recompute-drafts.txt`).

Assimilation: [L1-FILL] — theme `merge/kaidoku/` sasquatch/unblob/AVM, per-entry gate with ≥1 admit and ≥1 reject, id-collision check and quarantine hand-check before any append; census start `.ufo/waves/round-38/census-start.txt` (9 `W04` warnings in 10 lines, `kaidoku ok` last line; runner exit [L1-FILL]). `considerthese/` is absent in this lane (one report line). Not claimed: AVM-BE, vendor-mangled images, anything about the extracted programs, or that `sasquatch-v4be` is optional.

- **planned (round 39):** [L1-FILL] — must not be written from this seat; the round-38 outcome (met vs honest stop) decides whether big-endian coverage continues or the premise itself is the next claim.
- **retired:** none.
```

---

## A0. Freeze-drift warning the L1 must resolve before filling any C1 value

Observed after the freeze and during wave 1: `tools/round-38/c1-counter.py` is **modified in the
worktree and keeps changing** — `git status --porcelain` → ` M tools/round-38/c1-counter.py` (the
only modified tracked file); `git diff --numstat` → `38 20 tools/round-38/c1-counter.py`; frozen
blob at `e059ca93` sha256 `a7a62b098709035607375078a12d2668bb6d36bbabfc5a7459f04d00a9516db8`;
worktree sha256 `211059785dc2a17a10f90d24505abdad5f85f671cbd0ff422e2dc8db1b8acf1e` at
03:23:27 -03:00 and `733be0168527fec193f70441752ef561e1f402789e6b67fd280547357a312967` minutes
later. Peer seats recorded the same drift (`R38ExecSelftests.md` §4, with an `03:22:04` →
`f27f982b…` step; `R38MutC1/uncommitted-counter-diff-{vs-HEAD,snapshot2}.diff`).

The diff rewrites the predicate separator sentence from "run with stock unblob 26.6.4; no external
extractor dependency" to "run with sasquatch-v4be available, as unblob 26.6.4's `SquashFSExtractor`
requires"; adds a paired committed `before.json` per carrier that must publish none of the oracle
and name `sasquatch-v4be` as a missing extractor dependency; and moves the handler/gap checks onto
the after envelope. The frozen rule in `plans/round-38-claims.md` says "the counter, predicate,
carriers and oracle are never changed after this commit".

Consequence for the draft above: the counting command names `tools/round-38/c1-counter.py`, but
executing that path now runs the *modified* worktree script, while `--rev`/`--freeze` only pin the
git objects it reads. A landing scored with the worktree script would score a predicate the freeze
does not contain. Before any `[L1-FILL]` C1 value is written, either score the frozen blob
(`git show e059ca9391642d5b71b6662cabcbdce0d9308719:tools/round-38/c1-counter.py`, sha256
`a7a62b09…16db8`) or re-freeze the amended claim in a new commit and record that as the claim's
freeze. This seat neither reverted nor ran either version (`[L1-FILL]`).

---

## B. LOG.md entry (append at the end of `LOG.md`)

```markdown
## 2026-10-26 — round 38 (relaunch of round 37): standard big-endian SquashFS v4 toward Core, and the self-assessment mismatch count

- Base `77091b492cc53f8743bd0701b1e7d5e66123dd84`; freeze `e059ca9391642d5b71b6662cabcbdce0d9308719` (`plans/round-38-claims.md`, counters + selftests + harness + carriers + instruments + census start; R36-CL1 stamp committed); controls `efd5c47a72a50b3a434783f82268fb4a96e636a1`. Round 37 was an honest stop at the pre-freeze probe stage with no claim frozen (`corpus/lessons/round-37-verifier-spotcheck.md`, `rejected-honest-stop`); this round carries R37-CL1..CL3 and R36-CL1..CL6.
- Seven frozen controls were scored with the frozen counters before any claimed data, all exit 1: C1 `ctl-c1-0-do-nothing` (`carriers_matched 0`), `ctl-c1-1-three-carriers` (3), `ctl-c1-2-wrong-handler` (0); C2 `ctl-c2-0-do-nothing` (`mismatches 1`), `ctl-c2-1-junk-count`, `ctl-c2-2-delete-bad-pointer`, `ctl-c2-3-substitute-other-document` (`.ufo/waves/round-38/controls/`; `exit` field read from each receipt). Counter selftests, as reported by `R38ExecRecountBase` §3 and matching the case counts `plans/round-38-claims.md` names: C1 15 cases (1 green / 14 red, exit 0), C2 14 cases (1 green / 13 red, exit 0).
- Pre-claim recount at base `77091b49`, freeze `e059ca93` and wave-1 tip `9c9d496b`: C1 exit 1 at all three (`carriers_matched 0`; `carriers_unchanged false` at the base only because `carriers.json` is absent there); C2 exit 1 at all three (`mismatches 1`, `guards_ok false`, the sole unresolved pointer `prov_core:REA MCP server` → `evidence/doctor/`; command A 124/124 mapped, 17/17 rule blocks; command B 9/9; craft `SKILL.md:81-314`; Adjacent `PROVINCE.md:97-125`). Receipts `.ufo/waves/round-38/w1/artifacts/R38ExecRecountBase/`; both do-nothing receipts reproduce the frozen controls key-for-key.
- R38-C1 (coverage): four frozen BE v4 carriers — K1/K2 synthetic standard-BE gzip trees (`tools/round-37/gen-squashfs.py`), K3/K4 unblob 26.6.4 `squashfs_v4_be` integration fixtures — against the frozen `corpus/evidence/round-37/c1/K*/oracle.tsv`. Wave-1 draft receipts name `squashfs_v4_be` on all four carriers and recompute their evidence ids under the 6.5.0 rule (10 envelopes, exit 0). Draft clause state, **not claim data**: K1 5/5 and K3 4/4 only with `sasquatch-v4be` reachable — with a clean `PATH` the same carriers publish 0 files and report `missing-extractor-dependency` naming `sasquatch-v4be`; K4's draft receipt has 4/4 with zero gaps and its own dep-probe shows the same carrier at 0 files with that gap when the extractor is withheld (`R38ExecAfterK4/dep-probe/env-nosasq-gap.json` vs `env-v4beonly-ok.json`); K2 publishes 3/3 but carries one `unpublished-entry` gap (the symlink `var/lib/run-link`), which fails the frozen `after_gaps_empty` clause. The frozen premise "stock unblob 26.6.4 handles standard BE v4 without any external extractor" is therefore falsified on these carriers (`.ufo/waves/round-38/w1/R38ExecAfterK3.md` §2-4). Reported, not repaired — the predicate, counter, carriers and oracle are unchanged after the freeze. After receipts [L1-FILL]; counter result [L1-FILL].
- R38-C2 (calibration): [L1-FILL] doctor-pointer repair + count/range upkeep; counter result [L1-FILL].
- Instruments: `tools/round-38/{c1-counter.py,c2-counter.py,c1-run.sh,gen-controls.py}`, carriers `.ufo/waves/round-38/c1/carriers.json`, instruments map `.ufo/waves/round-38/instruments.json` (R36-CL4). Harness `after` mode at the freeze created the output root with `mkdir -p`, which REA refuses ("Extraction output root already exists"); fixed by the L1 in `cb4326b2` during wave 1 and re-run exit 0. The freeze-time failure receipt is kept as evidence (`.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/harness-after-mode-failure.txt`).
- Routed defects landed as fixes at the freeze: R37-CL1 (receipts committed/cited), R37-CL2 (`avm.txt`, `be-squashfs_v4{,.nopad}.bin` provenance through the SOURCES gate), R37-CL3 (`## Gate` decisions incl. the 7-Zip rejection), R36-CL1 (the `w2.ready.dispatched` stamp), R36-CL2 (dated pointer names the entry stem), R36-CL4 (instrument map), R36-CL6 (receipt identity = subject digest). R36-CL3/R36-CL5 blind spots are disclosed against the successor counters and left for the wave to falsify. [L1-FILL: verify each landed fix against the freeze commit before keeping this bullet.]
- Freeze drift reported in wave 1: `tools/round-38/c1-counter.py` was modified in the worktree after the freeze (` M` in `git status --porcelain`; 38 insertions / 20 deletions; worktree sha256 `21105978…`, frozen blob `a7a62b09…`). The diff changes the P38-C1 predicate sentence and adds paired before receipts. [L1-FILL: the landing must state whether it scored the frozen blob or re-froze the amended claim; no after value may come from the modified script without that decision.]
- Census start `.ufo/waves/round-38/census-start.txt` captured before any registry edit: 10 lines, 9 `W04` duplicate-URL warnings, last line `kaidoku ok …/corpus/SOURCES.md`; the runner's exit code is [L1-FILL] (this seat read the file, did not re-run the census). The R36-CL1 stamp `.ufo/waves/round-36/w2.ready.dispatched` is present at the freeze (`git cat-file -e e059ca93:.ufo/waves/round-36/w2.ready.dispatched` → present). Assimilation [L1-FILL]. `considerthese/` is absent in this lane.
- Tooling: no install or upgrade by this seat. [L1-FILL: record the L1's wave installs, if any.]
```

---

## C. Verdict placeholders and their inputs

| placeholder | what must be true to fill it | command that produces the value |
|---|---|---|
| C1 after `carriers_matched`, bindings, exit | the four `corpus/evidence/round-38/c1/K*/after.json` are committed at the measured revision | the C1 counting command in row A, `--rev <landing>` |
| C1 verdict | `met_target true` (then "met under the frozen rule", with the extractor-dependency wording disclosed) **or** `met_target false` (honest stop, no counter/predicate edit) | same |
| C2 after `mismatches`, `guards_ok` | the `evidence/doctor/` pointer is repaired to a resolving pointer to the same document, and the four stated counts / three stated ranges match `observed{}` | the C2 counting command in row A |
| owned coverage denominator | the round-38 entry is in `corpus/knowledge/` **and** has a `## Coverage map` row | `git ls-tree -r --name-only <REV> corpus/knowledge | grep -c '\.md$'`; the map/stem intersection printed by `c2-counter.py` `observed.command_a` |
| capability row | C1 landing admitted, and the row keeps the `sasquatch-v4be` dependency in its wording | C1 receipts + `R38ExecAfterK3.md` §3 |

## D. Limits of this draft

- **Freeze drift during wave 1.** `tools/round-38/c1-counter.py` is modified in the worktree
  (sha256 `21105978…` vs frozen `a7a62b09…`; §A0). The before values quoted in §A come from the
  receipts produced with the frozen script; no after value may be produced by the modified one
  without a re-freeze decision. This seat did not revert, run or validate the modified script.
- The only values measured by this seat are the base/freeze/tip counter receipts already committed
  to artifacts by `R38ExecRecountBase`, the command A/B recount printed above, the draft clause
  table and the xpin recomputation. Nothing was committed, and no counter was run at a landing
  revision because none exists.
- The draft clause table reads seat artifacts, not `corpus/evidence/round-38/`; it must not be
  cited as claim data.
- `[INFERENCE]` The K2 `unpublished-entry` gap is the symlink `var/lib/run-link`; the oracle lists
  only the three regular files, so the gap is structural for that carrier, not a lost member.
  The counter's `after_gaps_empty` clause does not distinguish the two.
- `[INFERENCE]` If the L1 lands the on-`PATH` receipts and calls C1 met, the "no external extractor
  dependency" sentence in `plans/round-38-claims.md` remains an unearned premise; it should be
  disclosed in the SCORECARD row and the knowledge entry rather than silently dropped.
