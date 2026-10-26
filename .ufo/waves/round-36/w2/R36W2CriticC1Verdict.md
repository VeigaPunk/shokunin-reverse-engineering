# R36W2CriticC1Verdict — is R36-C1 verified, an honest stop, or unprovable?

Seat: `R36W2CriticC1Verdict` (leaf critic, wave 2 — falsify the integrated landing). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`,
base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`, C1 landing `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95`,
integration tip `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (lane HEAD at measurement time
`6f2ba761bb5bcd6482d45523379376dcb6a386f6`, `.ufo/waves/` only). Read-only git; the frozen counter was
executed unmodified; nothing in the lane was written except this file.

## Verdict

**R36-C1 is verified — but not by its counter.** The frozen target is met at the measured revision
(`carriers_matched 4`, all five bindings true, exit 0, re-derived by me at `ffc81341`, `01a44dbf` and
`6f2ba761`), the frozen kill family did not fire (all three controls exit 1), and the substance of the
predicate — a sasquatch-enabled `extract-firmware` run publishing every frozen-oracle regular file, and a
no-sasquatch run publishing none and naming the dependency — is reproduced independently, four times in
wave 1 (§3.4) and again at the tip by the wave-2 executor. It is **not** an honest stop: a stop requires a
counter miss or a target-meeting frozen control, and neither exists. It is **not** unprovable: the
predicate-relevant receipt content is reproducible by any third party from lane-retained fixture bytes and
digest-pinned public releases with pinned tools (§3.5).

The qualification is load-bearing and must be stated wherever the claim is credited: **the counter's green
measures repository content, not the event.** I re-demonstrated that on the *landed* documents themselves
(§2): a fixture built from the `ffc81341` tree with the four `after.json` fabricated from the oracle,
re-stamped with the package's own digest rule, all `*-run.json` sidecars deleted, and bindings byte-identical
to the landing scores `met_target: true`, exit 0 — while the same envelopes are **rejected by the pinned
package's own `parseEvidence`** under both 6.5.0 and 6.7.0. So a green C1 receipt is exactly as strong as
the provenance of the bytes it hashes; this round's provenance rests on the independent re-runs, and the
lane's own record says so (`SCORECARD.md:3391`, lesson M36-4, `QUALITY.md` 78).

Two documentation debts remain attached to the coverage credit (§4), both one-line, neither touching the
frozen predicate: the moved surface's old text still reads as current at `PROVINCE.md:156-157` and
`corpus/README.md:44`, superseded only by reference.

## 1. What I measured (exact commands, outputs, exit codes)

Counter bytes are identical at the freeze, at both measured revisions and at HEAD:
`5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5` for
`790561d4:tools/round-36/c1-counter.py`, `ffc81341:…`, `01a44dbf:…`; `git diff --stat 790561d4 01a44dbf --
tools/round-36/` is empty. The receipts the claim is scored on are unchanged from their landing commit:
`git diff --stat 3310d8fa ffc81341 -- corpus/evidence/round-36/c1/` is empty.

```
$ python3 -I -B tools/round-36/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --rev ffc813417d3bceeeb7b028b12ce0be8a5dc33d95 \
    --freeze 790561d4e3aca732a434081aa9573ec2fa5fd7d0 \
    --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95"}
EXIT=0
```

Same output shape and exit 0 at `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` and at
`6f2ba761bb5bcd6482d45523379376dcb6a386f6`. At the base the same command exits **1** with
`carriers_matched 0`, `carriers_unchanged false` and every binding false. The three frozen controls each
exit 1 with `met_target false` (`controls/ctl-c1-{0,1,2}-*.out`); `ctl-c1-1` (all bindings present, no
sasquatch pipeline) is the one that would matter for coverage, and it scores `carriers_matched 0`.

The counter is therefore not vacuous: it separates base from tip, and it separates a sasquatch-less
pipeline from a sasquatch-enabled one (§3.3). What it does not separate is real from fabricated receipts
(§2).

## 2. The counter's green is content-only — demonstrated on the landed tree, not on a hand-built one

Wave-1 `R36CriticC1Shortcut.md` F1/F2 built a fixture with its own binding documents. I built the cheaper,
stronger version: **the landed documents are the bindings**, so the only thing I changed is the thing under
attack.

Fixture (scratch, `git -C "$D" rev-parse --show-toplevel` == `$D` asserted before the first commit):

1. `git archive ffc81341 | tar -x` → the full C1 landing tree; `K*/after.json` removed; committed as
   fixture freeze `cd5b5caf6fb6e9ebd81ce7291dc3b7b4b6d6381d`.
2. Four `after.json` fabricated from `K*/oracle.tsv` + the carrier sha in `carriers.json`, each with
   `subject.digest.sha256`, `provider.id = unblob`, `operation = extract_firmware`,
   `normalized_result.files = [{relative_path, sha256}]`, `extraction_gaps: []`, and an `evidence_id`
   computed with REA's own projection/digest rule; **all `K*/{after,before,oracle}-run.json` deleted**.
   Committed as `caf05e01fde9284dc24e1c87938ee16c209d8471`.
3. Byte check: `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` and the entry in the fixture are
   identical to `ffc81341:` (`sha256sum` of `git show` outputs, four `same`).

| item | fabricated | genuine (lane) |
|---|---|---|
| K1 `after.json` | 647 B | 12,230 B |
| K2 | 796 B | 19,335 B |
| K3 | 303,696 B | 4,362,742 B |
| K4 | 303,696 B | 4,362,857 B |
| total | 608,835 B | 8,757,164 B (14.4×) |

The fabricated ids equal `xpin-attribute.mjs`'s 6.5.0 and 6.7.0 recomputation (K1
`ev_3557629bd4ff959a30405831de165b7fa5bfcd126728cce055248f40083728d7`, K3
`ev_71e923dc5904ca31ad75e8ba94ce43d07bea3789769b0ad7c5eddad5028e9758` — the same two ids wave-1's F1
produced from independently written code), and `xpin --parse` **rejects every one** of them under both pins
(`Invalid discriminator value. Expected 'hopper' | … | 'raw-binary'`). Deleting the run sidecars also
removes the only committed artifact that names the sasquatch binary, its sha256, its version, the carrier
sha and the exit code.

Frozen counter on that fixture:

```
$ python3 -I -B tools/round-36/c1-counter.py --root <fixture> --rev caf05e01fde9284dc24e1c87938ee16c209d8471 \
    --freeze cd5b5caf6fb6e9ebd81ce7291dc3b7b4b6d6381d --pkg65 <rea-agents 6.5.0>
{"bindings": {"coverage_map_row": true, "entry_present": true, "entry_source_ids": ["S107", "S108", "S109"],
 "opened_source_rows": ["S107", "S108", "S109"], "province_core_row": true, "province_core_section": true,
 "sourced": true}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true,
 "revision": "caf05e01fde9284dc24e1c87938ee16c209d8471"}
EXIT=0
```

Why, in code: `measure()` reads exactly ten kinds of path with `git show` — `carriers.json` (freeze + rev),
`K*/oracle.tsv` (freeze + rev), `K*/before.json`, `K*/after.json`, the xpin tool, `PROVINCE.md`, the entry,
`corpus/SOURCES.md`, `corpus/README.md` (`tools/round-36/c1-counter.py:83,144,147,158-159,164,199,204,212,226`).
No read of `K*/after-run.json`, no `parseEvidence`, no `raw_result`, no carrier image (the fixture holds
only the K1/K2 fixture images; K3/K4's carriers are not in the lane at all), no `Frontier`/`AUR` text. The
verdict is `carriers_unchanged ∧ matched == 4 ∧ bindings` (`:231`) — a statement about writable bytes.

This confirms, at lower cost, wave-1 F1 and the wave-2 executor's §6, and it is the sharpest form: the
green needs no fabricated binding documents, only four JSON files worth 0.61 MB.

## 3. Why that does not make R36-C1 unprovable

### 3.1 The claim's after-state is one value and it re-derives

Prompt §9: "Declare each after-state as one concrete value that the closure can re-derive with one command
over committed bytes." The after-state is `carriers_matched == 4` with five named bindings; I re-derived it
three times (§1) over committed bytes at three revisions. Compliant.

### 3.2 No universal clause escapes the enumeration

"every regular file of the frozen independent unsquashfs oracle" is enumerated row-by-row (`oracle.tsv`:
3/4/2130/2130) and the counter checks equality with `oracle_files`; "for each of the four frozen carriers"
is the frozen set. The claim excludes big-endian/AVM, vendor-mangled images and 7z re-testing explicitly,
and no knowledge/Core wording extends the credit past "LE SquashFS v4" (`PROVINCE.md:372`,
`corpus/README.md:89`). Compliant.

### 3.3 The kill rule did not fire, and the controls are the right shape for the class they cover

The three frozen controls exit 1. The do-nothing control cannot reach the target (base: `carriers_matched 0`,
all bindings false). `d2e46ef5` — all four receipt pairs already 4/4, entry not yet landed — also exits 1,
so the green depends on the C1 documentary landing as declared, not on the receipts alone. The counter also
kills the classes it was built for: cross-carrier replay (`after_subject_ok` false), a one-row oracle miss
(`2129 != 2130`), an id-stale forged copy (`ctl-c1-2`), and post-freeze oracle/carrier edits. The class it
does **not** cover is the self-consistent forgery of §2 — a control-coverage gap, not a reading error.
§9 forbids changing the predicate or control family after any seat has scored (the kumitate-r42 rule), so the
gap is recorded for the next round, not repaired here.

### 3.4 Four independent reproductions carry the provenance the counter cannot

The receipts the predicate reads are byte-identical to the ones the wave-1 seats reproduced
(`3310d8fa → ffc81341` evidence diff empty). Each seat re-ran the frozen harness or the REA CLI from its own
scratch and compared field-for-field:

| carrier | reproduction | oracle | before / after | attribution |
|---|---|---|---|---|
| K1 | `w1/R36ExecReproK1.md` | 3 rows, `diff` clean | 3/3 files after, 0 before; gap names `sasquatch` | `xpin` recompute; run-local fields enumerated (258/131 leaf keys) |
| K2 | `w1/R36ExecReproK2.md` | 4 rows, `diff` rc 0 | 4/4 after, 0/4 before | isolation PATH with all 96 other `~/.local/bin` entries present → delta caused by `sasquatch` alone; frozen harness reproduces the same receipts |
| K3 | `w1/R36ExecReproK3.md` | 2130 rows, byte-identical | 2147-file set identical (2130/2130 oracle, 17 recursion extras), before 0/2130 | sasquatch-only PATH probe reproduces the identical set; independent ELF section-table offset (944632) |
| K4 | `w1/R36ExecReproK4.md` | 2130 rows, `cmp` clean | 2147-file set identical, before 0/2130 | `sasquatch-v4be`-only probe cannot substitute; offset 936456 derived independently; REA CLI run directly, not via the harness |

What makes these more than a capability demo: the reproduced artifact includes structures a forger cannot
take from the oracle — 17 recursion extras per AppImage at `analysis_depth` 1/2/null, `published_bytes`
51,122,564 / 51,792,724, symlink `unpublished-entry` gaps, and run-scoped `provider_id` families. The
fabrication hypothesis has to explain those as having been authored independently of a real run; a real run
produces them by construction. The forged envelopes of §2 are 0.61 MB of oracle rows precisely because they
cannot.

The chain of custody closes at the measured revision: the receipts at `ffc81341` equal those at `3310d8fa`;
the sidecars at the tip record `exit 0`, `sasquatch_sha256 ad02d27a…4754`, version `unsquashfs 4.5.1
(2022/03/17)`, carrier sha, UTC stamps (oracle/before 04:17:49Z, after 04:22:42Z — oracle frozen first).

### 3.5 The claim is reproducible by an outsider in minutes

K1/K2 carrier bytes are committed (`corpus/evidence/round-36/c1/fixtures/`), K3/K4 are public releases whose
digests equal `carriers.json`; tools are pinned (`rea-agents` 6.5.0 by cache root, unblob 26.6.4, sasquatch
4.5.1 `ad02d27a…`, `unsquashfs` 4.7.5). Four seats did it, and the wave-2 executor repeated the harness
runs at the tip. "Unprovable" in this lane's precedent (r33-C1) meant no evidence could be authored or
obtained at all; here it is a command anyone can run.

Two limits worth stating so the word "independent" is not over-read, both already disclosed in the entry's
"Oracle method and its limits": for K3/K4 the oracle is a different version of the same code family
(sasquatch is a patched squashfs-tools 4.5.1), so agreement is expected [INFERENCE], not a second
implementation; a genuinely code-separate second oracle exists for K3 only (the AppImage runtime's
`--appimage-extract`, 2130/2130, `w1/R36ExecAppImageExtract.md`), and K4 rests on `unsquashfs` 4.7.5 alone
(no `qemu-aarch64` on this host). K1/K2 additionally check against committed source trees.

## 4. The one honest debit: the moved surface still reads as unmoved in place

This is wave-1 `R36CriticRoutedCoverage.md` Counterexample 1, narrowed by the landing. At the measured and
integration revisions:

- `PROVINCE.md:156-157` — `- **sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback /
  covers the carved-image path today.` **unchanged** from the base. The supersession is a note at
  `PROVINCE.md:374`, inside the `## Round-36 additions to Core` section, 218 lines away and by reference
  (`PROVINCE.md:156-157`; `…:149-150 before this round's 7-line Adjacent addition`).
- `corpus/README.md:44` — the Firmware row still ends `AppImage SquashFS carved but recursion blocked by
  missing sasquatch`. The supersession is the coverage-map row at `corpus/README.md:89` ("Dated supersession
  of the Firmware row's … (2026-10-13 state, kept as history)"). The README *Frontier* line does carry its
  dated note adjacent (`corpus/README.md:232-233`).

Neither is a predicate miss — the predicate requires the Core row, and §9 requires the surface to be named
with a command that shows it unmoved (the base counter, exit 1), both satisfied. But it is a
duplicate-authority reading hazard of exactly the class `M36-1` was written for: a cold reader of the
Frontier list or the Firmware row still sees "(AUR-only)" and "recursion blocked" as current. The house
precedent argues for in-place annotation: the `>90 MB PE scale wall` bullet in the same Frontier list
carries `CLOSED (arc2-r7: …)` inside the bullet, and `corpus/README.md:233` annotates its Frontier line
adjacent.

## 5. Smallest safe corrections (none touches a frozen predicate, counter, carrier or oracle)

1. **`PROVINCE.md:156-157`** — append a dated parenthetical inside the bullet, e.g. `— LE SquashFS v4
   recursion moved to Core 2026-10-26 (2026-10-26-r36-sasquatch-squashfs-recursion); "(AUR-only)" was one
   route and the producer documents a Debian package; big-endian/AVM and vendor-mangled images stay
   Frontier.` One line; keeps the history, removes the duplicate authority.
2. **`corpus/README.md:44`** — append the same dated marker to the Firmware row itself, or point the row at
   the round-36 coverage row; today the correction sits two sections away.
3. **For the closure, state the warrant where the claim is credited**: "met under the frozen counter;
   provenance by four independent reproductions" — as `SCORECARD.md:3391` already does. Do not let the
   green receipt stand alone as provenance; §2 is the demonstration of why.
4. **Next round, not this one** (post-data edits are forbidden): either an executable counter (run unblob
   twice per carrier and compare to the committed receipts *and* the oracle) or a mandatory sidecar
   cross-check the counter reads (`sasquatch` sha/version, carrier sha, exit code, envelope digest). The
   current selftest's 13 red cases cover stale-id forgeries but not a self-consistent one; add that case.

## 6. Reconciliation with the other seats

- `w1/R36CriticC1Shortcut.md` (F1/F2, F3–F7): confirmed. My §2 reproduces F1 in a cheaper form and extends
  it — the landed documents are the bindings, `parseEvidence` rejects the records, and the run sidecars are
  absent. Its §8 root cause ("a capability claim measured as a data claim") is correct; its correction 1
  (out-of-band witness) is satisfied by the four reproductions and the wave-2 re-runs, and corrections 2–3
  are next-round instrument work.
- `w1/R36CriticRoutedCoverage.md` Counterexample 1: the code fact stands (the counter never reads the
  Frontier bullet, `c1-counter.py:199-203`); its construction "met while both surfaces still say the
  capability is missing" is now **partly** the real tip — the old text is verbatim at both named sites, with
  the supersession present but elsewhere. Severity drops from "coverage could be credited with both
  surfaces false" to "two one-line documentation debts", because the notes exist and name the exact lines.
- `w2/R36W2ExecC1Final.md` §5–§8: agrees on every number (counter green at both revisions, selftest 14/14,
  oracle regeneration, live re-runs, forge acceptance) and flags the same PROVINCE debt. No disagreement.
- `w1/R36ExecReproK1..K4.md`: no disagreement; their per-carrier numbers match the committed receipts I read
  (`after_oracle_hits` 3/4/2130/2130, `before_oracle_hits` 0, gap presence/absence, `oracle_frozen` true).

## 7. Impacted axes

| axis | impact | why |
|---|---|---|
| coverage (C1's axis) | **moved, bounded** | one real surface (LE SquashFS v4 recursion) now governed in Core, evidenced on 4 carriers including two shipped AppImages; the frontier text that says otherwise remains in place, so the credit must be read as "Core addition", not "retirement". No re-score of a held rule: base counter exit 1, `CTL-C1-1` exit 1 |
| calibration | **positive, one small debit** | the round's own record separates counter from provenance (`SCORECARD.md:3391`, M36-4, QUALITY 77–78) and the entry discloses the oracle lineage limit (K3 has a second oracle, K4 does not). Debit: §4's in-place annotations. No overclaim found in SCORECARD/README/lesson wording |
| freshness | positive | S107–S109 opened 2026-10-26 and cited by the entry; the 32-round stale "(AUR-only)" premise is corrected (by note, not in place) |
| depth / operability / adjacency | unaffected | no claim touches them; BE/AVM and vendor-mangled images stay Frontier and are named as unmeasured |

## 8. Limits of this review

- I did not install, upgrade or run any extractor; I did not re-extract any carrier. Provenance for the
  receipts rests on the four wave-1 reproductions and the wave-2 executor's live re-runs, whose numbers I
  cross-checked against the committed receipts and against two independently produced id values (§2); I did
  not re-derive them myself.
- The fixture in §2 is a scratch repository; its commits are quoted for traceability only and were removed
  with the scratch. Everything needed to rebuild it is in this file (§2 steps 1–3) plus the lane's own
  `git archive ffc81341`.
- The counter was run unmodified; no frozen predicate, counter, carrier, oracle or harness was changed.
- Node v24.21.0, Python 3.14.8, git 2.56.0; `rea-agents` 6.5.0 from
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. No tool installed, upgraded or removed
  (nothing to record for the 2026-10-19 tooling directive). No pacman transaction. No campaign tool in
  `/home/vgpnk/Projects/shokuknow`. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2CriticC1Verdict` removed
  after this report; no cited evidence lives under `/tmp` or scratch.
