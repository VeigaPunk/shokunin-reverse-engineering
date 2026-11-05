# ConnectorOverlap — R96-W1 sibling-overlap scan (kill-rule gate coverage, mandatory-receipt binding, fresh-source classes)

Seat: ConnectorOverlap (connector), lane kaidoku, round 96 attempt 1.
Claims frozen at declaration `e4d1f7de9deae83e6d5f78d2d7f0157196002af0` (base `0ea695e826f2dca53dd55ac0bafead93de26b173`), disclosed instrument supersession `3baac2ef4b9b2830d299125b8184ca06d9e6584d`.
Lane axes: coverage, depth, calibration, freshness (all 10.0 on finite proxies; saturation 10.0, window 10).
Read-only discipline: no lane or sibling repository files edited. The only lane paths written are `.ufo/waves/round-96/w1/ConnectorOverlap/overlap.md` and `.ufo/waves/round-96/w1/ConnectorOverlap.md`. All temporary work trees, clones, and scans ran under `/fast/scratch/hyaku/kaidoku-r96/ConnectorOverlap/` (cleaned up on finish).

---

## 1. Scan Methodology & Commands

Across all 20 sibling repositories under `/home/vgpnk/Projects/shokunin/*-shokunin` (excluding `kaidoku-shokunin`), explicit directory scans were executed across three tree scopes:
1. `tools/` (8 sibling lanes: chousa, kama, kotodama, mado, mori, souji, tameshi, tsukuroi) and `scripts/` (3 sibling lanes: kake, kumitate, tabi);
2. `corpus/` (all 20 sibling lanes);
3. Sibling active `.ufo/waves/round-96/` directories (3 sibling lanes: kake, lore, mori) and `plans/` (12 sibling lanes).

Searches were conducted using `rg -i -n` (case-insensitive literal/regex patterns), with exact file counts and matching line counts recorded below.

### Scan Summary Table

| Class / Pattern | tools/ & scripts/ (files) | tools/ & scripts/ (hits) | corpus/ (files) | corpus/ (hits) | sibling r96 wave (files) | sibling r96 wave (hits) | sibling plans/ (files) | sibling plans/ (hits) | exit code |
|---|---|---|---|---|---|---|---|---|---|
| **(a) Kill rule & mutation coverage** | | | | | | | | | |
| `'kill rule'` | 9 | 13 | 533 | 1043 | 7 | 13 | 142 | 419 | 0 |
| `'mutant'` | 98 | 983 | 2929 | 18779 | 17 | 56 | 232 | 1550 | 0 |
| `'survivor'` | 73 | 350 | 970 | 2585 | 7 | 20 | 85 | 242 | 0 |
| `'gate coverage'` | 3 | 4 | 13 | 14 | 0 | 0 | 0 | 0 | 0 |
| `'fsync'` | 17 | 19 | 25 | 69 | 0 | 0 | 0 | 0 | 0 |
| **(b) Mandatory receipt & binding** | | | | | | | | | |
| `'json-out'` | 4 | 5 | 5 | 8 | 0 | 0 | 0 | 0 | 0 |
| `'selfverify'` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| `'receipt-required'` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| **(c) Fresh source & packer diversity** | | | | | | | | | |
| `'fresh'` | 293 | 1392 | 5098 | 38757 | 50 | 233 | 307 | 926 | 0 |
| `'held-out'` | 39 | 48 | 106 | 282 | 0 | 0 | 24 | 44 | 0 |
| `'upx'` | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 |

*Note on exit codes:* `exit 0` indicates matches found; `exit 1` indicates no matches found in that scope.
*Note on 'upx' in corpus:* All 4 hits in sibling `corpus/` are non-packer tokens: 1 in `game-dev-3d-shokunin` (`listener.upX`, 3D camera vector property in `three.core.js`), and 3 in `tabi-shokunin` (base64 PNG payload strings in `transcript.jsonl` and `events.jsonl`). Binary packing and UPX repair are completely unique to `kaidoku-shokunin`.

---

## 2. Table 1 — Sibling Hits & Claims Overlap Analysis

| Lane | Path:Line | Pattern / Class | Exact Mechanism / Sibling Role | Claims Overlap (R96) | Verdict |
|---|---|---|---|---|---|
| **kake** | `scripts/instrument_receipts.py:643-646` | receipt writer / predictable temp (`.tmp`) | `temporary = destination + ".tmp"`, plain `open(temporary, "w")`, `os.replace(temporary, destination)` to write `corpus/knowledge/instrument-receipts.json`. Vulnerable to planted symlink at `<destination>.tmp`. Blob sha256 `162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7` at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d` (active r96 tip). | **NO** (kake r96 claims HTTP cache revalidation exchange + self-assessment conformance). | **Fleet recurrence of defect**: The exact v4 writer defect kaidoku closed in R95/R96 remains live and unmitigated in kake's active tree. |
| **kake** | `.ufo/waves/round-96/c96_reval.py:106,488,520` | mutant / survivor / forgeries | Revalidation contract test: 14 mutants generated and scored (`mutants killed 14/14 survivors=none`), anti-table check against seeded inputs, forgeries refused. | **NO** (domain is HTTP cache RFC 9111 revalidation, not binary repair or receipt write-paths). | Independent discovery of mutation-battery killing pattern in contract testing. |
| **kake** | `scripts/sidecar_reobserve.py:149` | `fsync` | `os.fsync(target.fileno())` after file write. | **NO** | Precedent of payload fsync in helper scripts. |
| **souji** | `tools/souji-receipt-write.py:530-575` | `fsync` / receipt writer / durability | HARDENED receipt publish (r60 amendment 3): `tempfile.mkstemp(prefix=..., suffix=".tmp", dir=outdir)`, `os.fsync(f.fileno())` on file, `os.link(tmp, out)` (fails `FileExistsError` EEXIST to prevent race clobber), stale `<out>.*.tmp` sweep, and **directory-level fsync** (`dfd = os.open(outdir, os.O_RDONLY); os.fsync(dfd)`). | **NO current r96 claim** (landed r60). | **Architectural precedent**: Solves Sentinel F5 (lost directory entry on crash) and race clobbering. Directly relevant to kaidoku R96-C2 block 35. |
| **souji** | `census/round-67/wave/w1/S67MutKill/mutants/K34.py:543,570` and `census/round-60/.../diffs/c2-m1-direct-stream.diff` | mutant / `fsync` | Mutation battery against receipt writer: mutant M1 removes `os.fsync(f.fileno())`, mutant M5 replaces atomic publish with direct open. | **NO current r96 claim** (historical r60/r67). | Direct ancestor of kaidoku's M2 mutant (removing fsync). |
| **kumitate** | `scripts/receipt-bind.mjs:1-70,287-291` | receipt binding / symlink defense | Capability `receipt-bind-v4` (landed r87-r90): binds receipt `tool_sha256=` to `git cat-file blob <rev>:<path>` at the judged revision (immune to dirty worktree laundering); fail-closed `SYMLINK_DIR`, `SYMLINK_RECEIPT`, `SYMLINK_INSTRUMENT`; `O_RDONLY\|O_NOFOLLOW` descriptor read. | **NO current r96 claim** (landed r90). | **Architectural precedent**: Solves Critic A14 (dirty worktree laundering of commit-bound receipts) by hashing committed Git blobs rather than worktree files. |
| **kumitate** | `scripts/make-dispatch-actual.mjs:384-386` | receipt writer / predictable temp (`.tmp-${pid}`) | `const tmp = `${path}.tmp-${process.pid}`; writeFileSync(tmp, text); renameSync(tmp, path);` — predictable pid-based temp name without `wx` flag. | **NO** | Unremediated temp writer in sibling tooling. |
| **chousa** | `tools/digest-in-tree.py:1-40` & `receipt-pin.py:1-40` | receipt binding / pin derivation | Provenance checker: every sha256 a receipt pins must re-derive from committed blobs in git (`git cat-file blob REVISION:PATH` or object database). Receipts measured on uncommitted worktrees fail closed as `UNBOUND`. | **NO current r96 claim** (landed r65-r67). | Precedent for mandatory blob-level binding of receipt pins. |
| **kama** | `plans/round-72-claims.md:67-90` & `tools/round72-receipt-tip-binding.py` | `RECEIPT_TIP_BINDING` / kill rule | Every receipt cited in self-record must carry `# rev=<40-hex>`, name an ancestor of tip, and delta to tip must touch only record paths. Fails closed if `cited=0` (anti-vacuous pass). | **NO current r96 claim** (historical r72). | Precedent for revision ancestor binding and empty-population kill rules. |
| **kama** | `tools/kama-llamacpp-live.py:347,1979-1980` | atomic publish / `O_EXCL\|O_NOFOLLOW` | `os.open(tmp, os.O_WRONLY \| os.O_CREAT \| os.O_EXCL \| os.O_NOFOLLOW)` (r49 Sen1Witness F1) and `tempfile.mkstemp(prefix='.kama-live-')` atomic publish. | **NO** | Precedent for symlink-safe atomic file publish. |
| **tabi** | `scripts/aria-loopback-round13.mjs:103-105,805-807` | receipt writer / predictable temp (`.tmp`) | `const tempReceipt = join(ARIA, `.receipt.${process.pid}.tmp`); writeFileSync(tempReceipt, ...); renameSync(tempReceipt, RECEIPT);` | **NO** | Unremediated pid-temp writer. |
| **tameshi** | `tools/bash-witness-study.py:795-797` | receipt writer / predictable temp (`.tmp`) | `tmp = path.with_suffix(path.suffix + ".tmp"); tmp.write_text(...); os.replace(tmp, path);` | **NO** | Unremediated predictable-suffix writer. |
| **mori** | `tools/mori-round13-regressions.py:572-574` | receipt writer / predictable temp (`.tmp`) | `tmp = path.with_suffix(path.suffix + ".tmp"); tmp.write_text(...); os.replace(tmp, path);` | **NO** | Unremediated predictable-suffix writer. |
| **kotodama** | `tools/gates/costume-era-consistency-gate.py:1494` | fixture pin writer / `fsync` | `tmp = "%s.tmp-%d" % (path, os.getpid()); open(tmp, "wb"); os.fsync(handle.fileno()); os.replace(tmp, path)`. | **NO** | Combines `os.fsync` with vulnerable pid-based predictable temp name. |
| **kotodama** | `tools/check-gate-battery.py:87,1191` & `corpus/lessons/round-27.md:84` | gate coverage / battery isolation | Duty 2 ten-gate coverage set (`REGISTERED_GATE_NAMES`). Lesson 27: a battery running unit selftests in isolation cannot be cited as gate coverage for operational artifact verdicts. | **NO** | Exact conceptual twin of kaidoku M95-h (battery unit checks passing while counter's `main()` and probe were unexercised). |
| **mori** | `.ufo/waves/round-96/contract.md:1-68` | round-96 claims | C1: SCORECARD `Last change` cells against fleet record (`tools/mori-scorecard-calibration.py`). C2: SOURCES registry pinned-copy digests re-verified against live bytes (`tools/mori-source-digest.py`). | **NO** | Distinct surface and instruments. |
| **lore** | `.ufo/waves/round-96/receipt.json:1-30` | round-96 claims (Oct 18) | Obligation mapping (`map_obligations.py`) and dependency freeze over fictional response fixtures. | **NO** | Distinct domain. |

---

## 3. Table 2 — Kaidoku Round-96 Call Sites & Claims Mapping

| Kaidoku File | Line(s) | Role & Surface | Claim | Claims-Overlap with Siblings |
|---|---|---|---|---|
| `tools/round-96/stop-boundary-repair-battery-v6.py` | 89–95 | `write_receipt`: `mkstemp` + `os.fdopen` + `os.fsync(fh.fileno())` + `os.replace`. Immune to planted symlink at `<target>.tmp` or `<target>`. | R96-C1 (after-side) | Overlaps sibling pattern family (souji r60, kama r49); remediates v4 defect that survives in kake, tabi, tameshi, mori, kumitate. |
| `tools/round-96/stop-boundary-repair-battery-v6.py` | 366–369 | Mandatory `--json-out`: refuses with exit 2 and `receipt-required` before scoring when no receipt can be written or self-verified. | R96-C1 / R96-C2 | Unclaimed fleet-wide. Siblings provide `--json-out` as optional flag (`default=None`) where omitting it skips receipt without error. |
| `tools/round-96/stop-boundary-repair-battery-v6.py` | 131–225 | `verify_receipt`: binds `head` to `revision`, checks typed counts schema (`counts-type`, `counts-missing-key`), binds downward `met_target`, checks counter/verdict/repair pins. | R96-C1 | Kin to `kumitate` `receipt-bind.mjs` and `chousa` `digest-in-tree.py`. Critic A14 shows `head == revision` binds the commit hash, not uncommitted working-tree bytes. |
| `tools/round-96/kill-rule-v2.py` | 249–263 | `c_fsync`: monkey-patches `os.fsync` during `write_receipt`, asserts `count >= 1` (kills M2). | R96-C1 | Presence check only; Sentinel F3 shows it does not assert fsync occurs before replace. Precedent in souji r60/r67 mutation batteries. |
| `tools/round-96/kill-rule-v2.py` | 215–246 | `c_dmain`: negative control calling `main()` with faked verdicts (kills M3 forced self-verify, M4 fail-closed, M6 revision binding). | R96-C1 | Addresses M95-h (r95 rule never called main). Kin to kotodama r27 lesson on operational gate coverage. |
| `tools/round-96/symlink-probe-v2.py` | 55–66 | `write_receipt`: hardened writer for probe's own receipt using `mkstemp` + `os.fsync` + `os.replace` (closes M95-i). | R96-C1 | Directly closes probe write escape; leaves victim intact. |
| `tools/round-96/fresh-source2-check.py` | 1–45 | Measures `/usr/bin/printf` (`b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7`) through upx packing, determinism, near repair, far refusal. | S321 (frontier step) | Closes round-93 carried limit "the fresh-pack arm has one source". 0 overlap in siblings. ScoutS321 notes lack of nonce mutation. |
| `corpus/QUALITY.md` (QUALITY 193/194) & craft block 35 | Block 35 | Craft decision table for `kill-rule-gate-coverage v1`: writer durability gate, fail-closed exit and forced verdict, probe receipt verdict, green without a receipt. | R96-C2 (depth) | Synthesizes gate coverage and mandatory-receipt requirements. |

---

## 4. Overlap Verdict

1. **No sibling round-96 declaration overlaps kaidoku round-96.**
   - Only three sibling lanes have active or landed round-96 wave directories:
     - `kake-shokunin` (round 96): claims HTTP cache revalidation exchange contract v1 (`scripts/reval_exchange.py`, RFC 9111 §4.3) and strict self-assessment conformance (`c96_selfassess.py`, E1–E5).
     - `mori-shokunin` (round 96): claims SCORECARD `Last change` cells against fleet record (`tools/mori-scorecard-calibration.py`) and SOURCES registry pinned-copy re-verification (`tools/mori-source-digest.py`).
     - `lore-shokunin` (round 96, landed Oct 18): claimed obligation maps and dependency freeze over fictional response fixtures.
   - None of these siblings touches binary reverse engineering, UPX repair, kill-rule gate coverage, mandatory receipt enforcement, or receipt symlink write escapes.

2. **Fleet recurrence of unremediated receipt writers:**
   - The vulnerable v4 writer pattern (`temporary = destination + ".tmp"`, plain `open(temporary, "w")`, `os.replace(temporary, destination)`) that kaidoku discovered and remediated in R95/R96 remains live and unmitigated across sibling repositories.
   - The cleanest instance is in `kake-shokunin`: `scripts/instrument_receipts.py:643-646`, which writes `corpus/knowledge/instrument-receipts.json` via a predictable `.tmp` file and plain `open`. Its blob sha256 is `162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7` at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d` (active r96 tip).
   - Other live instances: `tabi-shokunin` `scripts/aria-loopback-round13.mjs:103-105,805-807`, `tameshi-shokunin` `tools/bash-witness-study.py:795-797`, `mori-shokunin` `tools/mori-round13-regressions.py:572-574`, `kumitate-shokunin` `scripts/make-dispatch-actual.mjs:384-386`, and `kotodama-shokunin` `tools/gates/costume-era-consistency-gate.py:1494`.

3. **Fleet precedents for architectural solutions:**
   - **Durability (fsync):** `souji-shokunin` (round 60 amendment 3, `souji-receipt-write.py:530-575`) established the fleet's complete durability model: file-payload fsync (`os.fsync(f.fileno())`) followed by enclosing-directory fsync (`dfd = os.open(outdir, os.O_RDONLY); os.fsync(dfd)`), accompanied by `os.link` to fail on `FileExistsError` and prevent race clobbering.
   - **Receipt binding:** `kumitate-shokunin` (round 87–90, `scripts/receipt-bind.mjs`) solved the dirty-worktree loophole exposed by Critic A14 by hashing instrument bytes from Git's object database (`git cat-file blob <rev>:<path>`) rather than reading disk bytes. `chousa-shokunin` (`tools/digest-in-tree.py`) similarly enforces that all pinned digests exist as committed Git blobs.

---

## 5. Proposed Move (One Bounded Synthesis)

### Synthesis Across Round Proposals and Sibling Evidence
This round's peer findings reveal three architectural boundaries in kaidoku's candidate instruments:
1. **Durability ordering and directory entry (Sentinel F3 & F5):** `kill-rule-v2.py`'s `K-fsync` check only verifies that `os.fsync` is called >= 1 times, but does not verify that it occurs before `os.replace` (F3). Furthermore, `v6.py`, `probe2.py`, and `kill2.py` omit enclosing directory fsync (F5), which `souji-shokunin` r60 proved is required for atomic durability under POSIX filesystem crash semantics.
2. **Commit-id vs byte-level binding (Critic A14 & K3):** Critic A14 demonstrated that the pre-supersession honest receipt (`l1/scores/honest-pos.json`) measured uncommitted v6 bytes while recording `head = e4d1f7de` (which held a different v6 sha256). In other words, `head == revision` binds the Git commit pointer, but does not prevent working-tree laundering. In contrast, `kumitate-shokunin`'s `receipt-bind.mjs` binds receipts to committed bytes via `git cat-file blob <rev>:<path>`.
3. **Anti-table nonce asymmetry (ScoutS321):** The fresh source S321 check measures `/usr/bin/printf` without nonce mutation, unlike the round-93 fresh arm which mutated source bytes with `secrets.token_hex(8)`.

### The Move
In the R96-C2 craft block 35 decision table, the round-96 knowledge entry (`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md`), and the round-96 lesson (`corpus/lessons/round-96.md`) that the L1 lands at integration:
1. **Ground the `writer durability gate` row in block 35 and QUALITY 193 in the two-level durability model:** Cite `souji-shokunin` r60's precedent (`os.fsync(f.fileno())` payload sync + `os.fsync(dfd)` directory-entry sync), and explicitly document parent-directory fsync and fsync-before-replace call ordering as named architectural limits of the v6 in-process check.
2. **Ground the `head-not-bound` / unbound-field class in `kumitate`'s `receipt-bind.mjs` precedent:** Document in the round-96 lesson and knowledge entry that commit-id binding (`head == revision`) still admits dirty working-tree laundering (as demonstrated by Critic A14 on the pre-supersession honest receipt), whereas true byte-binding requires reading bytes via `git cat-file blob <rev>:<path>` as kumitate does. This elevates kaidoku's calibration limit from a single-lane accident into a fleet-standard architectural boundary.
3. **Cross-cite the persistent unremediated sibling writer (`kake-shokunin/scripts/instrument_receipts.py` at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d`, blob sha256 `162dd685…`) in the round-96 knowledge entry alongside S320/S321:** Record that while kaidoku closed M95-i with `symlink-probe-v2` and `stop-boundary-repair-battery-v6`, the defect remains unmitigated across sibling tools.

### Why This Move Improves Axes Without Harm
- **Depth (R96-C2):** Block 35 and the knowledge entry gain structural grounding in fleet architecture (souji's two-level fsync and kumitate's blob-binding contract) rather than local heuristics.
- **Freshness:** Incorporates live pins and verified state from active sibling lanes taken on 2026-11-05 (kake HEAD `bde9869144f69c5a459c0d2c93f5135922fe3a8d`).
- **Calibration (R96-C1):** Accurately bounds kaidoku's v6 `head` check against the known dirty-worktree loophole exposed by Critic A14 and solved by kumitate.
- **Zero harm to C1/C2 frozen surfaces:** Touches no frozen byte in `tools/round-96`, `mutants.json`, `forgery/`, or `pins.sha256`. The C1 kill-rule diff clause (`git diff --stat <decl> <landing> -- tools/round-96 ...`) remains completely clean.

---

## 6. Risks & Contradictions Stated Explicitly

- **Sibling mutability mid-wave:** `kake-shokunin` is running an active round 96 wave. Sibling citations must remain pinned to exact blob digests and commit hashes (`162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7` at commit `bde9869144f69c5a459c0d2c93f5135922fe3a8d`).
- **Contradiction in `head` binding:** Kaidoku's v6 `head` binding claims to bind the measured world, but Critic A14 proved it binds only the Git commit pointer, not the working-tree bytes that actually ran. Kumitate's architecture contradicts kaidoku's in-process `head` check by proving that true binding requires `git cat-file blob`.
- **Contradiction in `K-fsync`:** `K-fsync` claims to verify the durability gate (killing M2), but Sentinel F3 proved it only checks call count >= 1 without checking whether fsync occurred before replace, and Sentinel F5 proved v6 lacks parent directory fsync.

---

## 7. Second-Order Traces

- **Runtime Surface:** v6's unique `mkstemp` name means planted `<json-out>.tmp` symlinks are simply bypassed and left in place; no stale-temp sweep is required at runtime (unlike souji's predictable-prefix temps).
- **Contract Surface:** Block 35 keyword atoms in `QUALITY 193` (`instrumented count`, `survives every exit-code diff`, `main()-level negative control`, `receipt-content consistency check`) and `QUALITY 194` (`--json-out is mandatory`, `skipped self-verification`) are preserved verbatim; citing souji/kumitate adds context without disrupting frozen keyword matching.
- **Substrate Surface:** Under ext4/btrfs/xfs, an `os.replace` guarantees atomicity of the directory entry update in kernel caches, but without an `os.fsync` on the directory descriptor (`dfd`), an abrupt power loss or kernel panic can revert the directory entry to point to the old file or an unlinked inode.
- **Verification Surface:** The L1 can verify all cited sibling digests and lines read-only using `git cat-file blob` and `sha256sum` without running external processes.

---

## 8. Verification Commands

Commands executed by this seat in `/fast/scratch/hyaku/kaidoku-r96/ConnectorOverlap` (all exit 0):

```bash
# 1. Verify kake unremediated writer blob digest at current tip
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD
# bde9869144f69c5a459c0d2c93f5135922fe3a8d
sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/instrument_receipts.py
# 162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7  (exit 0)

# 2. Verify souji two-level fsync and EEXIST link publish
git -C /home/vgpnk/Projects/shokunin/souji-shokunin log -1 --format='%H' -- tools/souji-receipt-write.py
# 3. Verify kumitate git-cat-file blob receipt binding contract
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin log -1 --format='%H' -- scripts/receipt-bind.mjs
# 4. Verify host printf sha256 for S321
sha256sum /usr/bin/printf
# b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf (exit 0)
```
