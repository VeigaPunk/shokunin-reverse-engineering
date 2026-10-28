# R44Debt — round 44 debt ledger: every disclosed limit as an honest-stop backstop

**Seat:** `R44Debt` (leaf — no subagent dispatch). **Lane:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
**Lane `main` at ledger time:** `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717`; claims base
`c29360e3ba5381a5ab69e372d0d9577970f85018` is an ancestor (`git merge-base --is-ancestor` exit 0).
**Draft this ledger enumerates:** `plans/round-44-claims.md`, sha256
`1e2d3eacb2e9914d451d8374e63961ea6720aa67cac46e719236eaf7aef0c54f` (blob committed at `fc5eb54a`,
the pre-freeze draft). If the freeze amends the claims, this ledger must be re-derived against the
amended bytes; row ids stay stable so amendments can be diffed.

**Purpose.** Each row is a limit the draft *discloses*. A disclosed limit is a promise that the
claim does not cover it — so it is also the place where a later round could quietly assume the
opposite. These rows are the backstops: a claim may not be scored, promoted, or called "done"
by silently retiring one. A row leaves this table only through its exit condition, evidenced by a
committed receipt/artifact. Every round's lesson must re-list the still-open ids verbatim;
dropping one is the defect class `debt-dropped` (a claim-side analogue of the round-39
`carried-debt` convention).

**Disposition rules.**
1. `open` — disclosed, no exit evidence. Default state for all rows below.
2. `closed` — exit condition met, with the receipt path named in the row's closing entry (append,
   never rewrite the row).
3. A row may be **re-scoped** only by a claim amendment recorded in `## Changes from the draft`,
   never by editing this table's text in place.

## Grounding performed by this seat (read-only; no data procedure, no REA, no lane writes)

All commands run from the lane root unless noted; `TMPDIR`/scratch honoured; no fixture or clone
mutated. Observed results below are the only evidence used to make the "thin"/"unexercised" rows
concrete; textual disclosures are quoted with their draft line numbers.

| # | command | observed |
|---|---|---|
| G1 | `git rev-parse HEAD`; `git merge-base --is-ancestor c29360e3… HEAD` | `f5fb8d59…`; ancestor exit 0 |
| G2 | `sha256sum plans/round-44-claims.md` | `1e2d3eac…c54f` (236 lines) |
| G3 | `stat -c '%n %s' corpus/evidence/round-42/c2/fixtures/*.bin` | the four carriers are 4096 bytes each; the dir also holds v2ns/v3/v3adapt/v3bc/v3ddwrt/v3ns fixtures (v3ddwrt-be is 320 B) |
| G4 | `file` on the four carriers + `v2ns-{le,be}` | v1-le "version 1.0, **compressed**"; v1-be "version 1.0, **uncompressed**"; v2-le "version 2.0, **compressed**"; v2-be "version 2.0, **uncompressed**"; `v2ns-{le,be}` → "**data**" (no recognisable magic). The BE "uncompressed" verdict is a `file(1)` misparse — see G11 and the defects section; my first pass wrongly took it as fact and D-07 is corrected below. |
| G5 | `/usr/bin/unsquashfs -version` | `unsquashfs version 4.7.5 (2026/03/01)` — oracle identity matches the draft |
| G6 | `/usr/bin/unsquashfs -lls <carrier>` ×4 | v1 LE/BE: 3 regular files `apple.txt` 6 B, `banana.txt` 7 B, `cherry.txt` 7 B + root dir; v2 LE/BE: 4 regular files `apple1..4.txt` 7 B + root dir; no symlink, no device, no subdirectory beyond the root |
| G7 | `/usr/bin/unsquashfs -lls v2ns-le…bin`; `7z l v2ns-le…bin` | `FATAL ERROR: Can't find a valid SQUASHFS superblock` (non-zero); 7z: `Cannot open the file as archive`, `Errors: 1` — both disclosed refusals reproduce |
| G8 | `find corpus/evidence/round-44/oracle` | 6 `__output__` expected trees (v1 LE/BE, v2.0 LE/BE, v2.1 LE/BE) + 4 further extracted trees (`v1le/v1be/v2le/v2be`, provenance not established by this seat); `manifest.json` pins unblob `26.6.4` commit `1fcc7a0a…`, MIT, and states its grounds as "NOT handler code, NOT extractor behaviour, NOT a C1 carrier" |
| G9 | presence checks for every path the draft cites | present: `tools/round-42/c1-counter.py`, `tools/round-42/fixtures.json`, `tools/round-39/gen-squashfs.py`, `corpus/lessons/round-43{,-verifier-spotcheck}.md`, `corpus/evidence/round-42/c2/heldout/`, `.ufo/waves/round-43/l1/scores/*.json`, `.ufo/waves/round-43/w1/R43Quarantine.md`, `SKILL.md`; **absent**: `.ufo/waves/round-44/l1/probe-fixture-404.txt` (the `stale-premise` red receipt the draft cites — `.ufo/waves/round-44/l1/` is empty); `tools/round-44/` exists and is empty; `corpus/evidence/round-44/` is untracked (`??` in `git status`), so the oracle trees are fetched but not yet in a commit |
| G10 | `grep -c 'planned (round' SCORECARD.md`; `ls -d considerthese` | 9 `planned (round …)` rows (the category-(d) surface exists); `considerthese`: no such directory (confirms the draft's one-line report) |
| G11 | `/usr/bin/unsquashfs -s <carrier>` ×4 (my own run, after reading peer `R44C1FixtureAudit.md` N1 — independently reproduced, not taken on trust) | all four: "Inodes are compressed", "Data is compressed"; both v2: additionally "Fragments are compressed", 1 fragment, "Duplicates are removed"; block size 32768 (v1) / 65536 (v2); `unsquashfs` reads the four as valid LE/BE 1:0 and 2:0. `file` disagrees on compression for both BE images and prints the v1 block size as `-32768`. |

## Ledger (28 rows; `claim` = the draft section that owns the limit)

| id | debt (the limit, made concrete) | claim | why-disclosed (draft anchor) | future-round-exit-condition |
|---|---|---|---|---|
| D-01 | Carrier set is four 4096-byte MIT fixtures holding 3 (v1) / 4 (v2) regular files of 6–7 bytes with no directories, symlinks or devices (G3, G6). The claim promotes the *handler family through REA on the frozen carriers*, not v1/v2 images in general. | R44-C1 | `plans/round-44-claims.md:110-112` "four 4 KiB fixtures with 3–4 regular files each is a thin carrier set … not every v1/v2 image"; carrier table `:47-52` | A future C-round scores ≥1 carrier with ≥1 directory level, ≥1 multi-block member, and ≥1 duplicate-content pair, whose after-receipt + oracle census + counter exit 0 are committed; until then PROVINCE/Frontier language must say "handler family on four frozen fixtures". |
| D-02 | No published v1/v2 rootfs carrier: the two probe routes returned nothing fetchable (404 at `archive.openwrt.org/whiterussian/rc6/openwrt-brcm-2.4-squashfs.trx`; DD-WRT beta listing empty). Coverage rests entirely on lab/MIT fixtures, so a real vendor image's alignment/padding/vendor mangling is unmeasured for v1/v2. | R44-C1 | `:112-115` | A published v1 or v2 image is fetched under the frozen-URL convention (200 listing receipt + digest pin), added to `carriers.json`, and its after-receipt scores `carriers_matched` including it; or the probe is re-derived with dated listing receipts and "no published v1/v2 carrier exists" becomes standing claim language. |
| D-03 | `squashfs_v2_nonstandard` (v2ns) stays Frontier: no independent reader reads it — `unsquashfs` 4.7.5 FATALs on the superblock, `7z` 26.04 refuses, `file` reports only "data" (G4, G7); the draft adds that backhand has no v2ns profile (not re-checked by this seat). A same-tool oracle is not an oracle, so the handler gets no coverage credit even though REA may name it. | R44-C1 | `:54-56` | A producer-independent reader (new backhand profile, patched-magic kernel mount, or a published v2ns image with an authoritative manifest) yields a member census matching REA's extraction for both v2ns byte orders; then a v2ns-scoped claim can be declared and the Frontier text retired. |
| D-04 | `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, `squashfs_v4_broadcom` stay Frontier: no frozen carrier+independent-oracle pair exists for them in this round, so the existing Core rows cover only the already-measured variants (v3 standard/DD-WRT, AVM-BE). | R44-C1 | `:115-117`; PROVINCE `Round-42 frontier note` (`PROVINCE.md:416`) | Per handler: a frozen carrier with a producer-independent oracle tree, an after-receipt whose handler binding is EXACT, and a counter exit 0; each handler retires independently — a round that moves one must not widen the others. |
| D-05 | gzip v3 bodies stay Frontier: compression-family handling for v3 is unmeasured through REA. | R44-C1 | `:116`; `PROVINCE.md:416` | A gzip-v3 carrier with an independent oracle scores through REA `extract-firmware` (handler binding exact) and the Core row names gzip v3 explicitly; until then no statement may imply v3 coverage includes gzip bodies. |
| D-06 | LE AVM (`hsqs`), AVM kernels, and nested sub-images below depth 1 stay Frontier. The v1/v2 promotion does not touch AVM layout, kernel-format carving, or recursion depth > 1. | R44-C1 | `:116-117`; `PROVINCE.md:408,416` | Each item separately: LE AVM with an oracle census; an AVM kernel receipt; a nested `filesystem_core` image at depth 2 with a receipt — and the depth-budget dependency named in the receipt gap, not assumed. |
| D-07 | Compression coverage is thin and the draft's stated oracle property is false: all four carriers are gzip/zlib-compressed (G11 — inodes+data, v2 also fragments, "Duplicates are removed"), every member is 6–7 bytes, v1 has no fragment support and v2 has one fragment, so no multi-block member, no fragment boundary crossing, no duplicate-file dedup and no xattr/sparse case is exercised. The draft at `:85-86` records "`v2be` is uncompressed (measured 2026-10-28: `file` reports …)" — `file(1)` mislabels both BE images, so the "oracle property" is a `file` misparse and must not reach the counter as a fact. | R44-C1 | `:85-86` (the "uncompressed" statement, contradicted by G11); carrier table `:47-52` | A carrier with ≥1 multi-block member, ≥1 fragment-bearing v2 file, and ≥1 duplicate-content pair is scored; and `:85-86` is corrected before freeze (compression read from the superblock, not `file`), so the claim's oracle-property text is true. |
| D-08 | The non-regular gap rule is unexercised and one allowance is free: all four oracle trees contain only regular files (G6), so `unpublished-entry`, `MaliciousSymlinkRemoved` and `depth-limited` have **no positive witness**, while the predicate still grants "at most one structural `depth-limited`" without binding it to an oracle row. On this carrier set the rule is a zero-row conjunction, and the allowance could absorb a real publication failure in a later carrier. | R44-C1 | `:67-70` "one `unpublished-entry` gap or one `MaliciousSymlinkRemoved` diagnostic per symlink; at most one structural `depth-limited`; no `unknown-chunk-handler`" | A v1/v2 carrier whose oracle tree holds a symlink (and, separately, a device node) is scored, giving each gap arm a red/green witness; the `depth-limited` allowance is replaced by a row-identity binding naming the oracle entry it accounts for. |
| D-09 | Oracle independence is only partial and the draft does not claim otherwise: `unsquashfs` 4.7.5 is "a different producer than sasquatch", but the S138 `__output__` trees come from unblob — the same project whose handler runs through REA — and the draft calls them "a second, cross-checking oracle" with no producer-independence statement. `manifest.json` itself scopes them as "NOT handler code, NOT extractor behaviour, NOT a C1 carrier" (G8). | R44-C1 | `:82-86` | The round names the S138 tree producer and shows it differs from sasquatch (fixture-authoring tool + commit), or adds a third producer (e.g. `7z` where it reads v1/v2) as a per-carrier oracle; until then C1's independence rests on unsquashfs alone and the lesson must say so. |
| D-10 | The fetched oracle set is larger than the carrier set: 6 `__output__` trees (v1 LE/BE, v2.0 LE/BE, **v2.1 LE/BE**) against 4 carriers (G8). The v2.1 trees are unbound — read as assets they suggest v2.1 coverage that no carrier, receipt or counter row supports. | R44-C1 | `:47-52` carrier table; frozen paths `:213-215` ("the `__output__` fixture trees … into `corpus/evidence/round-44/oracle/`"); `manifest.json` | v2.1 LE/BE carriers are added to `carriers.json` and scored (if the unblob 26.6.4 fixtures exist), or the manifest marks the v2.1 trees `unbound: true` with the reason, so `__output__` count cannot be read as coverage. |
| D-11 | The superblock probe is *validated against `file(1)` output*, and `file` is demonstrably wrong on two fields the predicate binds: it calls both BE images "uncompressed" while `unsquashfs -s` reads all four as compressed, and it prints the v1 block size as `-32768` (real 32768) (G4, G11). So the draft's validation reference is a tool that disagrees with the image on BE compression and v1 block size; a probe tuned to `file` would inherit the misparse, and "verified against `file`" is not verification. | R44-C1 | `:56-57` "superblock probe … verified against `file` output"; `:85-86` | Compression / major / block size are asserted against `unsquashfs -s` (producer-independent of `file`) and a frozen control feeds mutated superbytes (bad magic, swapped major, compression id outside the frozen set) that must red the probe; `file` is dropped from the validation chain or kept only for endianness, where G11 shows it agrees. Until then the probe is an instrument assertion. |
| D-12 | The counters are dry-run only on dev-arm inputs before the freeze; the positive after-side arm on a real REA run is post-freeze by contract — "Data procedure (after the freeze, never before)", seats never run `c1-run.sh`. So the first real envelope this counter sees is the round's own data, CTL-C1-2 (fabricated envelope) is the only pre-freeze after-side-shaped positive dev arm, and CTL-C1-3 (sasquatch stripped) the only negative. | R44-C1 | `:27-29` "dry-run end to end, as frozen, with dev-arm inputs before the freeze"; `:92-94`; CTL list `:95-109` | A round that reuses a prior round's frozen after-receipt (already captured) dry-runs the full positive path pre-freeze, or the data-procedure rule is narrowed so one dev carrier may be run before the freeze. Until then an after-side counter bug costs the round rather than the freeze. |
| D-13 | **Carried, not re-disclosed:** the counter-time REA rerun proves the committed receipt's projection equals a real run's projection; it does not prove *which process* wrote the committed receipt (round-42's R40-CL2). Round-44 C1 restates the rerun binding ("a fabricated receipt cannot equal a real run") without repeating the provenance caveat, so a reader can over-read it. | R44-C1 | `:71-74` (rerun projection) vs round-42 `plans/round-42-claims.md:80-82` "it cannot prove which process wrote the committed receipt (R40-CL2 stays open)" — **absent from round 44** | A provenance-bearing receipt (harness-written transcript + runner-written `run.json` + stdout sha256 + host attestation, captured by a process the counter did not author) makes receipt authorship checkable; or the round writes the explicit decision that provenance is out of scope, so the caveat stops being silently unstated. |
| D-14 | The four carriers were round-42 C2 **held-out inputs**; using them as R44-C1 carriers consumes that held-out property. The draft states the fact but not the consequence: the lane now has no held-out v1/v2 inputs for a future cold test. | R44-C1 | `:44-45` "they were round-42 C2 held-out *inputs*, never a C1 carrier" | A future round designates a fresh held-out set (sources not used as carriers by any claim) before claiming a cold v1/v2 generalisation result; until then no "held-out" language may be attached to v1/v2. |
| D-15 | The rubric enumerates only the statements it froze; a mismatch outside the frozen set is "a new-found defect for the lesson, not counter ground". Calibration therefore measures exactly the enumerated surface, and a real mismatch one row outside the set is invisible to the target. | R44-C2 | `:169-170` | The counter (or a successor) covers a statement class outside the round-44 set, evidenced by a mismatch found outside it at REV and now enumerated; until then every lesson must list out-of-rubric findings as findings, never fold them into `mismatches`. |
| D-16 | Check-pass ≠ truth. The counter reads committed bytes and "cannot verify that a repaired statement is *true*, only that the check passes"; the mitigation (each check re-derives the asserted value) bounds the failure modes but does not remove them — a pointer can resolve to the wrong claim, a count can be re-derived from the wrong file set. | R44-C2 | `:170-173` | Each rubric check is paired with a semantic arm (the pointer's target must contain the claim id; the count must be derived from the exact file set the statement names) and a seeded-wrong control reds that arm; the rubric then states per-check what it proves and what it does not. |
| D-17 | Append-only repair leaves the wrong original text standing. Frozen blobs must stay equal, so a correction lands as a dated appended note; the counter treats `(frozen-text mismatch at BASE) + (appended correction at REV)` as repaired. A reader (or a future rubric that does not know the append convention) still hits the unqualified wrong line. | R44-C2 | `:224-230` "repairs land as NEW lines/notes at REV, the frozen blobs are compared … not REWRITTEN" | Statements carry versioned ids; the frozen original is marked superseded in place (a one-token edit bound by the rubric's expected bytes) and the counter resolves the latest version, so stale text never stands as current and the append-only arm is no longer needed. |
| D-18 | The freeze-integrity rule has a declared exception: the C2 counter's `frozen_path_changed` arm is relaxed for rubric-named paths, with the diff bound to "exactly the rubric's expected edit bytes" as row-identity checks. If that binding is weaker than the rule it replaces, a mid-round edit to a frozen self-assessment file passes where the global rule would red. | R44-C2 | `:229-236` | Either no C2 repair needs an in-place edit (all append-only) and the relaxation arm is deleted from the counter, or a frozen control shows an unexpected edit to a rubric-named path reds under the row-identity binding, and the relaxation's scope is printed in the receipt. |
| D-19 | Vacuity / honest stop: if the wave-1 census finds **zero** mismatches at base, C2 stops. The claim's target is then already satisfied do-nothing, and the round can report only that fact — it cannot produce a calibration landing. | R44-C2 | `:150-152` (CTL-C2-0), `:167-168` (kill rule), `:174-175` (zero-mismatch stop); contract row "If the wave-1 census finds ZERO mismatches at base, the C2 claim STOPS (honest stop)" | The round that lands with `mismatches > 0` at BASE and `0` at REV over an independently enumerated rubric — the only shape that evidences the predicate; a zero-base census must be re-derived next round rather than inherited. |
| D-20 | Calibration ≠ capability. A calibration claim counts mismatches between the lane's self-assessment and repo state; it "is not a coverage assertion", so `mismatches == 0` can coexist with a thin corpus — and would be reported as a calibration success in the same round that moved no capability. | R44-C2 | `:125-126` | Calibration statements are bound to capability rows whose evidence is re-derived (rubric categories (a)/(e)), i.e. at least one target statement's truth is re-derived from a receipt rather than from a count; otherwise the axis model stops treating zero mismatches as evidence about any other axis. |
| D-21 | Rubric admissibility at freeze ("a rubric entry the landing cannot satisfy is refused at freeze time, not loosened later") is a seat judgement, not a counter check. Nothing in the frozen counter can reject a rubric whose entries are trivially satisfiable. | R44-C2 | `:147-148` | The counter has a freeze-time `--rubric-audit` that reds an entry with no red arm (its asserted value must differ from, or be contradicted by, some constructible state), demonstrated by a control; until then CTL-C2-1's single seeded mismatch is the only proof that any check can fail. |
| D-22 | Category (d) carries escape hatches: a `planned (round N+1)` row matches if it "carry[s] an explicit `(after a steer)`/`superseded` marker". The marker is free text; a planned row can pass with no work done and no citation, and the match against "what round N+1 actually worked" is judged by the rubric author, not an external oracle. | R44-C2 | `:139-141`; 9 such rows exist at base (G10) | A marker must cite a resolving receipt (steer commit, score receipt, or the superseding round's claims section) and the counter checks that citation exists at REV; append-a-marker is then no longer sufficient. |
| D-23 | Category (e) checks `met`/`not met` against the cited receipt's exit code and headline fields — receipts are read as committed bytes and C2 never reruns the cited counter. A fabricated or stale receipt therefore passes calibration (the only rerun proof in the round is C1's counter-time rerun, scoped to C1). | R44-C2 | `:141-142` | At least one cited counter is re-executed at REV and its output compared by the rubric (feasible once the data-procedure rule permits seats to run counters, currently L1-only), or the rubric explicitly grades receipt-derived verdicts as a lower evidence class so `mismatches == 0` is not read as receipt authenticity. |
| D-24 | Shared-surface tolerance: C2 shares `corpus/README.md` with C1 and reads the coverage-map row count **at REV, not a frozen integer**, so C1's later landing is tolerated. Consequence: the check proves count + stem-set agreement (`missing []`/`dangling []`), not that C1's added row maps the right entry — a present-but-wrong map row cannot red C2. | R44-C2 | `:177-186` separability; `:142-143` category (f) | The rubric adds a content arm binding each map row to the knowledge stem's own `source:`/receipt identifiers, so a wrong-but-present row reds; until then the tolerance's blind spot is stated in the receipt. |
| D-25 | §10 assimilation is unexercised: `Assimilation: none` — the 5-row quarantine slice's standing verdicts are *carried* from round 43 (1 fabrication-class refuse, 3 present-with-anchor, 1 unverifiable) and no staged row is adopted; the re-derivation rides wave-1 seat R44Quarantine. | plan (Frontier step) | `:193-196` | A round adopts an admitted row, evidenced by the appended corpus/SOURCES row and the admission verdict; or the slice is re-derived one last time and a terminal disposition is recorded (slice closed, nothing adoptable), so the carried table stops being re-checked every round. |
| D-26 | The `considerthese/` surface does not exist; the draft's handling is "one report line". The §10 consideration path is therefore not exercised at all this round. | plan (Frontier step) | `:196-197` | The directory appears and is processed under the standing §10 procedure, or the lane records a dated "surface not applicable" note that a later round must re-check rather than assume. |
| D-27 | The `stale-premise` fix (verify URL existence via the directory-listing API before pinning; never guess the fixture API shape) is enforced by **seat discipline**, not by the tooling: this round's 404 was a manual probe, and the red receipt it cites (`/.ufo/waves/round-44/l1/probe-fixture-404.txt`) was **absent** at ledger time (G9), so the red already lacks its committed witness. | plan (Mistake to mine) | `:198-203` | The frozen-URL convention is mechanical: the local-source gate (or an equivalent linter) refuses a URL cell without a committed 200 listing receipt, with a red control showing a guessed URL fails; and the 404 probe receipt is committed before the freeze or the mistake row loses its evidence. |
| D-28 | Freeze-scope collateral: `SKILL.md` is byte-frozen **whole** "so a mid-round instrument row can't silently move". The intended protection also freezes every unrelated byte of a 251 KB file for the round, so legitimate instrument-registry maintenance is deferred and the C2 rubric's citations to its rows are pinned to base bytes. | plan (Frozen paths) | `:216-218`; `stat SKILL.md` = 251325 B | Instrument-registry rows move to their own file with a narrower freeze scope (or the rubric cites row ids re-resolved at REV), so a single registry row is pinned without freezing the whole craft document. |

### Coverage of the draft's disclosure-bearing text (nothing in the draft left unmapped)

| draft lines (sha256 `1e2d3eac…`) | what the draft says | rows |
|---|---|---|
| `:27-29` | counters dry-run on dev-arm inputs only | D-12 |
| `:44-45` | carriers were round-42 held-out inputs | D-14 |
| `:54-57` | v2ns no independent reader; same-tool oracle is not an oracle; probe verified against `file` | D-03, D-11 |
| `:66-70` | non-regular gap rule with one structural `depth-limited` allowance | D-08 |
| `:71-74` | counter-time rerun ⇒ fabricated receipt cannot equal a real run | D-13 |
| `:82-86` | unsquashfs a different producer; S138 a second cross-checking oracle; "`v2be` is uncompressed" (**contradicted** — defect 1) | D-07, D-09 |
| `:92-94` | data procedure after the freeze, seats never run it | D-12 |
| `:110-114` | thin 4 KiB/3–4-file set; published v1/v2 rootfs unfetchable | D-01, D-02 |
| `:115-117` | v2ns, v3bc/v3ns, v4bc, gzip v3, LE AVM, AVM kernels, depth-1 nesting stay Frontier | D-03, D-04, D-05, D-06 |
| `:125-126` | calibration is not a coverage assertion | D-20 |
| `:139-143` | rubric categories (d) marker hatch, (e) receipt verdicts, (f) count + missing/dangling | D-22, D-23, D-24 |
| `:147-148` | unsatisfiable rubric entry refused at freeze time | D-21 |
| `:150-152`, `:167-168`, `:174-175` | zero-mismatch base stops C2 | D-19 |
| `:164-166` | text-only repairs, append-only, never history rewrite | D-17 |
| `:169-173` | rubric enumerates only frozen statements; check-pass ≠ truth | D-15, D-16 |
| `:182-184` | shared `corpus/README.md`, count read at REV not frozen | D-24 |
| `:193-197` | assimilation none; `considerthese/` absent | D-25, D-26 |
| `:198-203` | `stale-premise` URL-guess 404, red receipt path | D-27 |
| `:216-218` | whole-`SKILL.md` byte freeze | D-28 |
| `:224-233` | append-only landing mechanics; declared frozen-path relaxation | D-17, D-18 |

Nothing in the draft's disclosed-limits paragraphs is unmapped; the items that are *only in this
ledger* are D-13 (round 42's R40-CL2 caveat, absent from the round-44 draft), the round-42
held-out consequence in D-14 (the draft states the fact, not its cost), and the `file(1)` misparse
recorded as defect 1 below.

## Draft defects found while enumerating (verbatim conflict, for the L1 before the freeze)

These are not debt rows: they are statements in the draft that the evidence contradicts, recorded
so the freeze does not inherit them.

1. `plans/round-44-claims.md:85-86` says "`v2be` is uncompressed (measured 2026-10-28: `file`
   reports "version 2.0, uncompressed"); that is an oracle property, not a counter assumption."
   **Contradicted by `unsquashfs -s`** (G11): v2-be and v1-be both report "Inodes are compressed /
   Data is compressed", v2 has "Fragments are compressed" and one fragment, all four carry
   "Duplicates are removed". `file(1)` mislabels big-endian SquashFS and prints the v1 block size
   as `-32768` (real 32768). Consequences: (a) the stated "oracle property" is false, so the claim
   text must be corrected before freeze or the predicate inherits it; (b) the predicate's clause
   "verified against `file` output" (`:56-57`) names a tool that disagrees with the image on the
   exact fields it is supposed to validate — the counter must read compression/major/block size
   from the superblock and compare against `unsquashfs -s`; (c) D-07 is re-derived accordingly
   (compression-path thinness, not "BE is uncompressed"). Independently found by peer seat
   `R44C1FixtureAudit` (`.ufo/waves/round-44/w1/R44C1FixtureAudit.md`, note N1) and reproduced
   here from my own `unsquashfs -s` run — the two reports agree.
2. `plans/round-44-claims.md:200` cites `.ufo/waves/round-44/l1/probe-fixture-404.txt` as the
   `stale-premise` red receipt; that path does not exist at ledger time (G9), so the mistake row
   has no committed evidence. (Also D-27 and pre-freeze observation 3.)

## Which rows are stop backstops (do not confuse a debt with a kill rule)

- **Kill rules already in the draft** (a control meeting the target stops the claim before data):
  C1 CTL-C1-0/1/2/3; C2 CTL-C2-0 (zero base mismatches) and CTL-C2-1 (seeded mismatch greens).
  Rows D-19 and D-21 are the debt-side view of those stops; they are not additional kill arms.
- **Rows that must block a "met" verdict if their exit is not evidenced:** D-01, D-02, D-07, D-08,
  D-09, D-11 (scope and instrument validity of the coverage statement); D-13, D-14 (evidence
  provenance / held-out status); D-15, D-16, D-17 (what the calibration number means); D-24
  (shared-surface blind spot).
- **Draft defect 1 must be closed before the freeze** (the `file(1)`-based probe validation and the
  false "v2be is uncompressed" oracle property): otherwise C1's predicate binds both a wrong
  instrument reference and a false stated property of the image.
- **Rows that are pure carry-forward** (must be re-listed, never re-litigated as new): D-03, D-04,
  D-05, D-06, D-13, D-19, D-23, D-25, D-26.
- A row whose exit condition is met **mid-round** (e.g. D-27's receipt committed before the freeze)
  is still marked `open` in this file: only the landing round can close it, with the pointer.

## Carried debt from earlier rounds that this draft does not re-disclose

| id | debt | status | note |
|---|---|---|---|
| R40-CL2 | Counter-time rerun equality cannot prove which process wrote a committed receipt. | open (rounds 40 → 44) | Round 42 disclosed it; round 44 C1 restates the rerun binding without the caveat (D-13). Not to be silently upgraded to "fabrication-proof". |
| R41-D4 | Score receipts must carry `counter_sha256` and `counter_sha256_at_freeze`. | carried in `:25-29` | Re-disclosed; kept here so the ledger shows it is not new. |
| R41-D5 | Chunk-extract root publication must be segment-bounded. | carried in `:66-67` | Re-disclosed in the predicate. |
| M43-2 | Diff expectations are row-identity checks over the appended block, never raw numstat. | carried in `:232-233` | D-18 depends on this being true; if M43-2's binding is not frozen with the rubric, D-18's relaxation is unsafe. |
| round-43 quarantine slice | 5 rows: 1 fabrication-class refuse (S150), 3 present-with-anchor (S113 corrected, S136, S147), 1 unverifiable-not-fabrication (S117). | carried (D-25) | Slice sha256 `7383a90e…` per `.ufo/waves/round-43/w1/R43Quarantine.md`. |

## Pre-freeze state observations (not debt; freeze gates the L1 must close)

These are facts about the tree at ledger time, recorded because the ledger is the audit trail, not
because they are disclosed limits:

1. `corpus/evidence/round-44/` (the fetched oracle trees + `manifest.json`) is **untracked**
   (`git status --porcelain` → `?? corpus/evidence/round-44/`); the draft requires these committed
   before the freeze, content-addressed by S138 (`:213-215`).
2. `tools/round-44/` exists and is **empty** at ledger time — `carriers.json`, `c1-run.sh`,
   `c2-rubric.json` and both counters are still to be installed by the L1 from
   `.ufo/waves/round-44/w1/artifacts/<Seat>/`.
3. `.ufo/waves/round-44/l1/probe-fixture-404.txt` is **absent** while the draft cites it as the
   `stale-premise` red receipt (D-27) — commit it or the mistake row has no evidence.
4. `plans/round-44-claims.md` has `## Changes from the draft` → "(to be filled by wave-1
   amendments before the freeze — none yet)"; any amendment changes the draft hash this ledger
   enumerates, and the ledger must be re-derived (ids stable).
5. The ledger covers the draft **as written**. The one wave-1 peer report it uses — `R44C1FixtureAudit`
   note N1, the `file(1)` misparse — was independently reproduced here with my own `unsquashfs -s`
   run (G11) and is recorded as defect 1, not taken on trust; other seat findings are not imported.
   A defect class no seat enumerated belongs in the landing round's lesson as a new row, not as a
   silent edit here.

## Artifact

- This report: `.ufo/waves/round-44/w1/R44Debt.md` (only lane write by this seat; no artifact
  directory authored — the row set is textual and needs no tooling).
- Scratch used: `/fast/scratch/hyaku/kaidoku-r44/` (reader runs only; no fixture writes).
- No REA, unblob, sasquatch or `tools/round-44/c1-run.sh` invocation; readers only
  (`file`, `/usr/bin/unsquashfs -lls`, `/usr/bin/unsquashfs -s`, `7z l`, `git`, `sha256sum`, `stat`).
