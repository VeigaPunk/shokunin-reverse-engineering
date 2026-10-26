# R40W2MistakeHunt — round-40 `## Mistakes` rows

**Verdict: DEFECTS FOUND** — five round-40 mistake classes, each with a gate that is red on the
round-40 bytes and green on a repaired fixture or a corrected variable (5/5 rows demonstrated, plus
one live defect inside the frozen C2 generator). I attacked: the frozen C1 counter's path-domain
join, the carrier-pick independence clause, report placement/identity in the wave-1 tree, the frozen
`partial-body-failure` damage recipe, and the vendor-byte handling rule.

Seat `R40W2MistakeHunt`, leaf (no subagents, no background jobs, never messaged `agent://all`).
Lane `0b15c8b2` at read time; measured revision `42c10a58`, freeze `7fce3086`. Wrote only
`.ufo/waves/round-40/w2/R40W2MistakeHunt.md` and
`.ufo/waves/round-40/w2/artifacts/R40W2MistakeHunt/`. No VCS mutation (read-only `git show`, `log`,
`ls-tree`, `cat-file`, `rev-parse`). REA 6.5.0 ran only through the CLI, only on synthetic carriers I
built in scratch — no REA/unblob run touched V1, V2, L1, L2, any vendor member or any C2 held-out
carrier. No vendor firmware byte was fetched, copied or cited; only pins. No tool installed,
upgraded or moved. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40W2MistakeHunt` removed at exit; the
fixtures it built are reproduced by `artifacts/R40W2MistakeHunt/run-all.sh`.

## 1. Methods and what each gate reads

Everything below is from committed bytes plus one measurement class (MH-4) that builds its own
carriers with the frozen writer and reads them with the pinned extractor. The tools are in the
artifacts directory, all pure stdlib, all re-runnable with `python3 -I -B`:

| tool | reads | decides |
|---|---|---|
| `mh1-suffix-domain.py` | `c1/<ID>/{after.json,nonregular.tsv,oracle.tsv}` at a revision | whether the frozen `same_rel` join is the promised equality test, in the publication binding and in the gap-resolution binding |
| `mh2-candidate-reservation.py` | a candidate reservation record (`carriers.json` shape) + a tree of run records | whether a reserved candidate ever became a run subject |
| `mh3-report-placement.py` | a wave dir + `swarm-registry.json` | registry↔report coverage, seat identity, duplicate report bytes under `artifacts/` |
| `mh4-recipe-fit.py` | the frozen writer `gen-squashfs.py`, the frozen target-selection code in `heldout-gen-v2.py`, REA `extract-firmware` | whether a damaged carrier reaches the class tuple (`handler`, `extraction_failed`, published files, gap kind) |
| `mh5-vendor-bytes.py` | a pin record (sha256+length) + a tree, optionally every git blob | whether restricted bytes exist in the worktree or in any commit |

`runs.txt` is one pass of `run-all.sh` on this host (Linux 7.2.11-arch1-1, python 3.14.8, unblob
26.6.4, sasquatch-v4be 4.5.1, node v24.21.0): **28 printed commands — 6 environment, 22 gate
runs — and the gate runs are 12 `exit=0` and 10 `exit=1`**, no tracebacks. Each block prints the
command, its output and its exit code.

## 2. Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| **MH-1** | **one path helper, two path domains.** The frozen counter's `nonregular_unpublished_ok` promises "no published regular file path **equals** a non-regular entry path" but tests a *suffix* (`same_rel`), and the same helper resolves gap paths; a regular file whose tail is a symlink's path reads as a materialised symlink, and a gap recorded on that regular file reads as a symlink gap | `tools/round-40/c1-counter.py:54` (docstring "equals") vs `:606-607` (`same_rel` = `==` or `endswith('/'+rel)`), used at `:643-649` (`nonregular_published`) and `:660-676` (`gap_check` resolution); the colliding names are the lane's own: `tools/round-40/mk-l-carriers.py:60-66` (`usr/bin/busy` regular, `bin/busy -> /usr/bin/busy`); measured `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json` L2 `nonregular_published: ["firmware.bin_extract/usr/bin/busy"]`, `nonregular_unpublished_ok: false` while `gaps_ok: true`; the published `usr/bin/busy` sha256 `e28f81fc…4870` 40000 B is the oracle's own regular file; the 70-case selftest has no colliding name (`grep -c busy c1-counter.py` = 0, `.ufo/waves/round-40/controls/c1/c1-counter-selftest.json` `cases: 70`) | **no one before the freeze**: the counter selftest's fixture names are disjoint (`etc/motd` / `dev/console` / `libfoo.so`), those carriers' receipts first exist at `73c7bf9c`, and the wave-1 control suite recommended the exact-root clause (`w1/artifacts/R40C1Controls/CONTROL-SUITE.md:215` §5.2) but its executed form still has no such case | compare **after the receipt's recorded chunk root** (`raw_result.report[*].task.path` basename) for all three bindings (`mh1-suffix-domain.py`): frozen → L2 hit + exit 1, exact → 0 hits + exit 0 on all four receipts, oracle unchanged 697/697 · 8/8 · 7/7 · 6/6; a published symlink path is still caught (2/2), `wrong-root` publication refused (oracle 0/6 vs frozen 6/6), a bogus gap on the regular file's path refused (frozen accepts it, exit 1) |
| **MH-2** | **a pick is not a reservation.** The vendor scout published V2 = `FRITZ.Box_7430-07.31` into the shared wave-1 artifact tree; a sibling recon seat used the same member as a "development" input (its stated exclusion was only "not V1"), so the pick was burned and had to be replaced at freeze assembly | `w1/R40C1VendorScout.md:1,39` (pick), `:88` ("The L1 should decide" on the licence); `w1/artifacts/R40C1ReconGaps/env-7430-member-d1.json.gz` `subject.digest.sha256 = b919a6a2…` (a REA run on the 7430 member), `image-pins.txt` 7430 image `3dd6940c…`; `R40C1ReconGaps.md:35` "Neither image is V1"; the swap is recorded only in prose (`plans/round-40-claims.md` "Changes from the draft" bullet 1) and the frozen V2 is 6820v1 `3948449d…` (`c1/carriers.json`) | L1 at freeze assembly (the swap); no gate, and neither seat was wrong locally | a reservation record written at pick time + a pre-freeze scan of run-record **subjects** (`mh2-candidate-reservation.py`, classifying `run`/`unblob`/`pin`): draft-7430 rig → 1 fatal hit (`env-7430-member-d1.json.gz`) exit 1; frozen `carriers.json` (V1+V2) → 0 fatal (29 pin citations) exit 0 |
| **MH-3** | **a report can be committed twice, and a retry seat's report can land inside `artifacts/` under an id no registry member carries** — the second authority is never marked non-authoritative | three byte-identical pairs in one commit: `w1/R40SrcAvmVendor.md` ≡ `artifacts/R40SrcAvmVendor.md` (`1df870c7…`), `w1/R40SrcReaOps.md` ≡ `artifacts/R40SrcReaOps.md` (`d0f7972f…`), `w1/R40ConnSibling.md` ≡ `artifacts/R40ConnSibling-2/R40ConnSibling.md` (`3a19c93f…`); the w1 copy's header declares `Seat: R40ConnSibling-2` while the registry member is `R40ConnSibling` (`w1/swarm-registry.json`, 42 members, all 42 with a report) | `w1/R40Sentinel.md:218-222` (§2.5 found the **two top-level** copies, not the nested one) | `mh3-report-placement.py`: red on the lane bytes with **6 findings** (2 `report-at-artifacts-root`, 3 `duplicate-report`, 1 `seat-identity`), green (0 findings) on a fixture that deletes the two copies, files the nested one as `w1/R40ConnSibling-2.md` and registers that id; deleting a report from the clean fixture re-fires `missing-report` (branch proven live) |
| **MH-4** | **a post-dry-run fix changed the variable the dry run did not implicate.** The clean result was attributed to the compressor and "fixed" by pinning gzip, while the frozen recipe still writes **0x00** — the byte the round's own recon measured as absorbed — and the frozen docstring still asserts zeros always fail. The measured determinant is the zeroed block's *compressed* length, on both compressors [INFERENCE: the decompressor fallback chain absorbs a zero stream when it can produce at least the block's expected length] | `tools/round-40/heldout-gen-v2.py:226-231` (comment: "a zeroed single-block xz file extracted clean, so the partial recipe is pinned to gzip"), `:558-566` (docstring, sentence at `:564-565`: "Zeros are an invalid gzip header and an invalid .xz stream, so the decompressor fails"), `:591` (`payload[start:start+length] = bytes(length)`, no 0xFF anywhere in the file); `w1/R40C2ReconPartial.md:96-105` §2.1 fill table (`00` absorbed, `ff` fails, measured on gzip); measured matrix in §3 | the L1 dry run `df4fef39` / `H22` found the clean case (recorded in the frozen comment) | measured with the frozen writer + frozen target selection + REA, fill byte as the single variable (`mh4-recipe-fit.py`): **zero fill** on semi-compressible content → `extraction_failed=False`, no gap → reads `clean` on **gzip and xz** (4/10 not-fit, exit 1); **0xFF** on the same ten shapes → `extractor-failure` with published files on all 10 (exit 0). Direct sasquatch confirms the damage: zero fill exits 0 with a 3100-byte **all-zero** `zz.bin`, 0xFF exits 1 `FATAL ERROR: writer: failed to read/uncompress file` |
| **MH-5** | **restricted vendor bytes were written into the lane's own artifact tree**; the only thing that kept them out of the freeze commit was a sentinel's size survey ~47 minutes before the commit — no gate | `w1/R40Sentinel.md:108-109` measured `artifacts/R40C1VendorV1/carrier-v1-be.sqsh` = 5,442,392 B (= the whole V1 carrier, AVM vendor bytes) in the worktree; `SHA256SUMS.txt` (15:23:58) and `carrier-v1-be.sqsh.REMOVED-by-L1.sha256`; `git cat-file -e 7fce3086:<carrier>` → rc 128 (absent), `<marker>` → rc 0; `git log --all -- <carrier>` → empty | `w1/R40Sentinel.md` §2.1; removal by L1 (`.REMOVED-by-L1.sha256`) | pin-keyed scan (`mh5-vendor-bytes.py`), length-first then sha256, worktree **and** `git cat-file --batch-all-objects`: fixture holding registered bytes → 2 fatal (tree + blob), exit 1; same tree after removal → 0, exit 0; the lane with the real V1/V2 pins and `--git` → `pins=2 candidates=0 fatal=0`, exit 0, 0.26 s |

## 3. Red/green evidence (`artifacts/R40W2MistakeHunt/runs.txt`)

**MH-1** — the L2 false positive and its blast radius:

```
$ mh1-suffix-domain.py --root LANE --rev 42c10a58 --matcher frozen --oracle
V1 … hits=0 | oracle=697/697
V2 … hits=0 | oracle=8/8
L1 … hits=0 | oracle=7/7
L2 … hits=1 ['firmware.bin_extract/usr/bin/busy<-bin/busy'] | oracle=6/6
exit=1
$ … --matcher exact --oracle          (same four carriers)
V1 … hits=0 | oracle=697/697 … L2 … hits=0 | oracle=6/6
exit=0
```

Controls that keep the fix honest: exact matcher + materialised symlink → 2 hits (caught);
exact + `deeper` (`…/sub/bin/busy`) → 0 hits (a foreign subpath is not the entry's path);
frozen + `wrong-root` (CTL-C1-14's overlay) → oracle **6/6** (false pass), exact + `wrong-root` →
oracle **0/6** (refused). Gap binding, same helper: frozen accepts a gap recorded on
`firmware.bin_extract/usr/bin/busy` (a regular file) as resolving to `bin/busy` (exit 1), exact
refuses it (exit 0); every path-resolved real gap (263/85/2/2; the fourth gap per carrier is the structural
`depth-limited`) resolves to exactly one entry under **both** matchers, so the correction moves no
committed data.

**MH-2** — `draft-7430 → fatal=1 (run, env-7430-member-d1.json.gz); frozen carriers.json →
fatal=0 (29 pin citations)`. The gate keys on run subjects, so the scout's own pins table does not
trip it.

**MH-3** — `6 findings on the lane (2 report-at-artifacts-root, 3 duplicate-report, 1 seat-identity) → 0 on the
repaired fixture → 1 (missing-report) when one report is deleted from that fixture`, so both the
positive and the coverage branch are live.

**MH-4** — one variable apart (fill byte), ten shapes:

```
s1/s2/s3 (pattern, 26-136 B per 4 KiB compressed block)  fill=00 → failed=True, gap, fits
h1 (3100 B, 1 block) / h2 (7093 B, 2 blocks), compressed block 1.7-1.8 KiB (~57% of the data):
h1-gzip-00 → failed=False files=2 gaps=[]   h1-xz-00 → failed=False files=2 gaps=[]
h2-gzip-00 → failed=False files=2 gaps=[]   h2-xz-00 → failed=False files=2 gaps=[]
h1/h2 with fill=ff → failed=True, files=2, gaps=[extractor-failure]  (all four)
```

Direct extractor on the gzip/zero-fill carrier: `exit=0`, 11 fallback lines, `zz.bin` = 3100 bytes
**all zeroes**; on gzip/0xFF: `exit=1`, `FATAL ERROR: writer: failed to read/uncompress file`.
So the envelope that reads `clean` carries a *corrupt* published file — the failure mode is silent.

**MH-5** — `fixture with registered bytes → fatal=2 (tree + git blob)`, `after removal → fatal=0`,
`lane + real pins + --git → pins=2 candidates=0 fatal=0`, and a fixture repo (toplevel asserted
before any commit) proves the git arm finds a committed same-length blob (`object c83c893e…`).

## 4. Forward findings (live, not just historical)

1. **The frozen C2 recipe still writes the absorbed byte.** `heldout-gen-v2.py:591` writes zeros and
   the docstring above it is false in the large-compressed-block regime on both compressors
   (§3). The committed held-out set is *honest anyway*: H21/H22 are `gzip` with the zeroed block
   37 B and 26 B long (`manifest.json` `damage.block_length`), so the fallback fails and
   `run.json` records `failed_chunks: ["squashfs_v4_be"]`, `files: 5/3`, `gaps: ["extractor-failure"]`.
   The risk is future use of the generator (a different tree/material, a different block size) and
   the false statement in frozen code. Cheapest correction: set the fill to `0xFF` per §2.1 *and*
   assert the measured tuple per class — but the carriers' bytes would change, so it needs a new
   seed/freeze; until then the honest step is to record the measured tuple in the manifest.
2. **The C1 control suite's vocabulary is mostly not the frozen counter's.** Of the 17
   binding-shaped tokens its rows cite, 4 exist in `tools/round-40/c1-counter.py`
   (`evidence_id_ok`, `gaps_ok`, `oracle_ok`, `run_provenance_ok`) and **13 do not**:
   `carrier_blocklen_le_ok`, `carrier_marker_ok`, `control_table_not_frozen`, `distinct_carriers_ok`,
   `doc_control_table_frozen`, `doc_frontier_note_consistent`, `failed_chunk_ok`,
   `frozen_paths_clean`, `oracle_shape_ok`, `publication_ok`, `receipt_descends_freeze_ok`,
   `rerun_projection_ok`, `subject_ok` (`grep -c` = 0 each). The
   executed C1 kill rule is exactly CTL-C1-0 plus the 70 selftest cases
   (`controls/c1/c1-counter-selftest.json`: `cases 70, green_ok 5, red_ok 65`). So the one control
   that would have separated suffix from exact publication (row CTL-C1-14, "an exact
   `<extract_root>/<rel>` match is required") was never scored, and the round's own design doc had
   already named the defect MH-1 hit.
3. **False-positive vs false-negative.** The counter's hit on `usr/bin/busy` is a *false positive*
   (a violation that did not occur); the claim's 3/4 is a *false negative* (a true statement not
   promoted). `4d62ee5a`'s subject and `corpus/README.md:250` both say "counter suffix false
   negative". The lesson should not propagate that direction; the smallest correction is the
   wording, e.g. "counter suffix false positive → claim false negative".
4. **The freeze commit's author date precedes three artifacts it contains** (latent, no frozen rule
   reads it). `7fce3086` author `2026-10-26 15:04:17 -0300`, committer `16:13:52 -0300`; inside it,
   `w1/R40Sentinel.md` mtime 15:26:03 and `R40C1VendorV1/SHA256SUMS.txt` 15:23:58 (the carrier
   removal). `grep -rn 'author\|committer\|--date\|%ad\|%cd' tools/round-40/*` → 0 hits, and the
   freeze-integrity rule is ancestry-based, so nothing is mis-scored today; but any future
   author-date ordering claim ("controls before data", "wave 1 before the freeze") would read the
   freeze as predating evidence it contains. Cheapest correction: cite the committer date in the
   claims' freeze sentence, or state that the freeze commit was amended.

## 5. Calibration — what these rows do not establish

- **MH-1 does not move R40-C1.** A frozen counter cannot be repaired retroactively; the L1's
  `4d62ee5a` demotion stands, and the exact matcher is the path a round-41 re-freeze would take.
  The four committed receipts are green under the corrected join, so no carrier or oracle changes.
- **MH-4 does not move R40-C2.** The 26 held-out envelopes were measured, not asserted; their
  partial carriers land the right tuple for the reason above. The defect is in the generator's
  robustness and in its own comment, not in the scored data.
- **MH-2, MH-3, MH-5 are process rows.** None touches a scored binding: no counter reads
  `artifacts/**.md` (the doc bindings read `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
  the entry), so the duplicate reports and the burned 7430 candidate changed no number.
- **Not tested:** whether a *future* zero fill could also be absorbed for tiny blocks under a
  different sasquatch build (the fallback chain is version-specific: sasquatch 4.5.1 here);
  whether `sasquatch-v4be -ll` acceptance (the scout's observation) shares the fallback path. Both
  are [INFERENCE] boundaries, not findings.
- The L2 carrier's shape is *good* test design (an absolute symlink whose target also exists as a
  regular file, `mk-l-carriers.py:60-66`); the tree was not the mistake — the helper was.

Report: `.ufo/waves/round-40/w2/R40W2MistakeHunt.md`
