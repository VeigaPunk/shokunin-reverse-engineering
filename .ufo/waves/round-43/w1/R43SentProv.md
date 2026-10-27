# R43SentProv — provenance and hygiene bindings for everything round 43 will commit

**Verdict: DEFECTS FOUND** — the C2 landing is proven green verbatim at the amended destination, the
commit invocation for the 2,048,000-byte tar is measured, and no firmware bytes enter the tree; but the
draft carries two high-severity contract defects (P43-C2's SOURCES byte-identity clause is falsified by
the round's own S135 append; C2 declares its own landing bytes frozen and lands them after the freeze) and
three provenance gaps (C2's counting receipt retains no argv/tool/revision field; the map's `rebuild` cell
is not runnable; "every copy re-verifies against the live host object" holds for 15 of 18 entries, not 18).

Seat: R43SentProv (sentinel, provenance/hygiene). Leaf member: no subagents, no background jobs.
Scratch `S=/fast/scratch/hyaku/kaidoku-r43/w1-R43SentProv` (removed; every clone/run lived there).
Base read `6b9e64fe7e0de202d9383baad5792fbfe039a743`; the lane moved during this seat — the L1 amended the
plan at `1ed29de2cdd6061315fb2f5478d5029b7d570675` ("amend draft C2 landing path to the prepared round-42
destination") while I was reading, and every measurement below is against `1ed29de2` or the artifact pack
that the amendment now names. Nothing was written outside this report and `artifacts/R43SentProv/`.

Artifacts delivered (all under `.ufo/waves/round-43/w1/artifacts/R43SentProv/`):

| file | what it is |
|---|---|
| `audit-local-source-copies.py` | fresh host re-verification of the 18 map entries (read-only, stdlib) |
| `host-audit.json` | its receipt: 15 live-equal, 3 host-absent, 0 mismatches |
| `receipt-wrap.py` | QUALITY-18/21 receipt wrapper (argv, tool digest, resolved revision, exit, stdout) |
| `receipts/c2-gate-pre-landing-lane.json` | do-nothing gate at lane HEAD `1ed29de2`: exit 1, 18 rows |
| `receipts/c2-gate-landing-form.json` | same gate after landing, sandbox clone, exit 0 (form demonstration) |
| `receipts/c2-gate-post-landing-sandbox.json` | raw gate JSON, green, 19 records |
| `receipts/c2-gate-pre-landing-sandbox.json` | raw gate JSON, red, 18 rows `no-copy-named` |
| `receipts/c2-gate-red-dropped-copy.json` | red control: copy removed → exit 1 `copy-missing` |
| `receipts/c2-gate-red-corrupt-copy.json` | red control: one byte appended → exit 1 `copy-digest-mismatch` |
| `ts-*.json` | `evidence-timestamps.py` runs at HEAD on `.ufo/waves/round-42`, `.ufo/waves/round-43`, `plans` |

Tools installed: **none** (no pacman/npx/uv/`~/.local/bin` write this seat). No REA, unblob or extractor run;
only `file`, `tar -t/-xO`, `git`, `jj` reads and Python stdlib. No VCS mutation of the lane or fleet; the only
commits made were inside a `git clone --shared` sandbox (fixture identity `-c user.name=fx -c user.email=fx@fx`).

---

## 1. QUALITY 23 — which round-43 files carry zoned timestamps, and the check

**Which files.** Timestamps enter the round through prose and receipts, not through the counters:

* `.ufo/waves/round-43/w1/**` — seat reports and their tool receipts. In the working tree at 2026-10-27T08:26:19Z,
  **20 files** carry a zoned timestamp; the newest is `2026-10-27T05:22:55.615968-03:00`
  (`w1/artifacts/R43RevRevenger/placement.patch`), then `2026-10-27T08:20:30Z`
  (`w1/artifacts/R43ScribeAssim/drafts/*`, `receipts/page-probe.txt`). **0 future-dated.**
* `plans/round-43-claims.md` — one zoned instant (S135 opened `2026-10-27T08:08Z`). Measured clean at
  `1ed29de2` (§1 run 3).
* `corpus/evidence/round-43/**` — **will carry none** if the new tools follow the round-42 precedence, which
  I measured: the round-42 score receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` has 0 zoned
  timestamps, `corpus/evidence/round-42/c2/heldout/manifest.json` has 0, and 40 sampled envelope JSONs have 0.
  A `generated_at` / `utc_start` field added to `heldout-gen-v4r43.py` or `c1-counter.py` would create the
  whole risk class; do not add one. The admissible instant is the commit's `%cI`.

**The check (exact, no `--json-out` — that flag does not exist and returns exit 2, measured).**

```
python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <LANE> --rev <SHIP> --path .ufo/waves/round-43 --strict
python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <LANE> --rev <SHIP> --path corpus/evidence/round-43 --strict
python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py --root <LANE> --rev <SHIP> --path plans --strict
```

All three must exit 0 at the commit that ships them; the tool reads Git objects only (`git blame --porcelain`),
so it must run **after** the freeze/integration commit, and again at the measured revision.

**Measured now** (`--root <LANE> --rev 1ed29de2`): `.ufo/waves/round-43` → exit 0, findings 0, skipped 0;
`plans` → exit 0, findings 0, skipped 0; `.ufo/waves/round-42` → exit 0, findings 0, **skipped 201** (binary
blobs, each one a review obligation under QUALITY 23); `corpus/evidence/round-42/c2/heldout` → exit 0,
findings 0, skipped 78. Scope the round-43 check to the two round-43 trees plus `plans`: a 201-entry skip list
is not reviewable, a 0-entry one is.

**This report's own exposure.** The newest instant it cites is `2026-10-27T08:26:19Z`; any commit introducing
this file must have `%cI` at or after that (it will — the seat wrote it at that instant).

---

## 2. QUALITY 18/21 — what each new receipt must retain

Round-43 receipts come in four kinds. The binding below is the minimum each must carry; the round-42 C2 score
receipt already has the right shape for the counter family and can be copied field for field.

| receipt | must retain | keys the tool actually recomputes (QUALITY 21 — name these, never the verdict word) |
|---|---|---|
| C1 score at REV (`c1-counter.py`) | `argv`, `revision`, `revision_arg`, `freeze`, `freeze_arg`, `exit_code`, `counter_sha256`, `counter_sha256_at_freeze`, per-binding booleans, `generator.tuple_check` | `matched`, `n`, `observed_features_match_declared`, each `claim_bindings` entry, `counter_sha256` (digest of the file that ran) |
| C1 freeze controls `CTL-C1-0..3` | `argv`, revision = freeze, exit, and for CTL-C1-2 the **absence** of the manifest after the run (`manifest_path` + `manifest_written: false`) | `exit_code` 2 / 3, `declared_tuple_unobserved`, the per-carrier observed-vs-declared diff list |
| C1 post-freeze data | heldout `manifest.json`: `seed`, `generator.sha256`, per-carrier `declared_features` and `observed_features`, `tuple_check` verdicts; per-carrier `subject` digest | carrier `sha256`, envelope `subject` digest vs carrier sha256, `seed == FREEZE` |
| C2 score at REV (`local-source-gate.py`) | `argv`, `tool_sha256`, `tool_digest_at_rev`, `revision` (full hash) + `revision_arg`, `exit_code`, and the embedded gate JSON | `records[].paths[].sha256` (the copy digest the gate recomputes), `reason`, `source_digest_check`, `row_pin_scope`/`url_cell_pins`, `table_sha256`, `rows_total`, `rows_checked`, `rows_failed` (the id list) |
| C2 controls `CTL-C2-0/1` | `argv`, revision, exit, map sha256; for the stub control the sandbox path and the removal/corruption performed | `rows_failed` ids and per-path `reason` (`no-copy-named` / `copy-missing` / `copy-digest-mismatch` with expected+actual) |

**Measured gap — the gate is not self-describing.** `local-source-gate.py` records no `argv`, no digest of
itself, and no dedicated revision field: its `--json` output's keys are exactly `exit, map, map_present,
records, root, rows_checked, rows_failed, rows_total, table, table_sha256` (measured), and the revision appears
only inside `table` as `git:<rev>:corpus/SOURCES.md`. The round-42 seat's green receipt additionally names
`root` = `/fast/scratch/hyaku/kaidoku-r42/R42LocalSrc/fx.YLKK/lane`, a scratch path that no longer exists —
a receipt that cannot say which tree resolved the copies. **Remediation:** run the gate through the wrapper
supplied here,

```
python3 -I -B .ufo/waves/round-43/w1/artifacts/R43SentProv/receipt-wrap.py \
  --out .ufo/waves/round-43/l1/scores/c2-at-<REV>.json --git-root <LANE> --rev <REV> \
  --tool tools/round-41/local-source-gate.py -- tools/round-41/local-source-gate.py --root . --rev <REV> --json
```

which adds `argv`, `tool_sha256`, `tool_digest_at_rev` (sha256 of `<REV>:<tool>` from Git objects),
`revision` resolved by `rev-parse --verify`, `revision_arg`, `exit_code`, and the tool's stdout verbatim.
Measured on the landed sandbox: `tool_sha256 = tool_digest_at_rev = cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7`
(the round-41 committed bytes), `revision` = the sandbox landing commit, `exit_code` 0
(`receipts/c2-gate-landing-form.json`); the same wrapper against lane HEAD gives `exit_code` 1 with the 18 ids
(`receipts/c2-gate-pre-landing-lane.json`). The wrapper deliberately writes **no timestamp** (§1).

**QUALITY 21, concretely.** "The gate exits 0" is a verdict, not a measurement: cite
`rows_failed: []` (the list), `records[].paths[].sha256` for the 17 copies, `table_sha256`
(`8c6c53143741b03a4261049b50844d2179be3b139f0f2769c7e2acc147bf2ed5` at `1ed29de2`), and
`source_digest_check: file` for the 4 entries that have `source_sha256` — **not** the `reason: resolved`
string. Likewise "the copy re-verifies" must name the digest pair, not `ok: true`.

---

## 3. Large-file sweep and the exact commit invocation

**Base sweep** (`git ls-tree -r -l 6b9e64fe -- corpus/evidence .ufo/waves/round-42`, blobs > 1 MiB):

| bytes | path |
|---|---|
| 4,362,857 | `corpus/evidence/round-36/c1/K4/after.json` |
| 4,362,742 | `corpus/evidence/round-36/c1/K3/after.json` |
| 2,939,928 | `corpus/evidence/round-34/elf/e10.bin` |
| 2,852,279 | `corpus/evidence/round-41/c1/V4/after.json` |
| **2,048,000** | `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-dist-cited-members.tar` |
| 1,195,144 | `corpus/evidence/round-34/elf/e05.bin` |
| 1,097,344 | `corpus/evidence/round-34/elf/e11.bin` |

The C2 landing adds **exactly one** new file over 1 MiB — the 2,048,000-byte S048 tar. The other 16 copies are
≤ 719,095 B (pack total 17 files / 4,281,141 B), so the helper's 10 MiB `--allow-large` guard is **not**
triggered; the 1 MiB `snapshot.max-new-file-size` boundary **is**.

**Helper semantics, measured** (`jj 0.45.1`; effective `snapshot.max-new-file-size = 1MiB` in this lane,
`jj --ignore-working-copy config get snapshot.max-new-file-size`; `scripts/hyaku/jj-lane.sh:655-663`):

* a **named directory** is tracked like `git add <dir>` (`jj file track -- root:"<dir>"`, line 662, no
  `--include-ignored`). Measured in a fresh colocated repo: `d/small.txt` (6 B) and `d/big.bin` (1,572,864 B)
  under `root:"d"` → `jj diff --summary -- 'root:"d"'` printed **only** `A d/small.txt`; jj advised
  `jj file track --include-ignored d/big.bin`.
* a **named file** is tracked with `--include-ignored` (line 658), which admits files over the size limit.
  Measured: `jj file track --include-ignored -- 'root-file:"d/big.bin"'` → `jj diff --summary` printed
  `A d/big.bin` (1,572,864 B).
* `jj-lane.sh:639` refuses a named file over 10 MiB without `--allow-large` (not our case).

**The invocation the L1 must use for the C2 landing commit** (`lane.id = kaidoku`, `lane.branch = main`,
both verified in git config; paths relative to the lane, as `cmd_commit` canonicalises them with
`realpath -m --relative-to=.`):

```
/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh commit \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin --as kaidoku -m "<message>" -- \
  corpus/evidence/round-42/local-sources/ \
  corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-dist-cited-members.tar \
  corpus/evidence/local-sources.json
```

Naming the directory alone would silently drop the 2,048,000-byte tar (measured above) and the gate would go
red with `copy-missing` for S048 — the QUALITY-84 / M41-3 failure. Naming the tar explicitly is what makes it
tracked; `validate_change_scope` (`jj-lane.sh:556`) accepts the change because it lies under a requested path.
No `--allow-large` needed (2,048,000 < 10,485,760).

**Post-commit presence check** (QUALITY 84: `git ls-tree` vs disk — measured in the landed sandbox):

```
git -C <LANE> ls-tree -r -l <REV> -- corpus/evidence/round-42/local-sources corpus/evidence/local-sources.json \
  | awk '{n++; s+=$4} END {print n, s}'
```

must print `18 4292882` (17 copies + the map; measured identical in my sandbox landing). Anything less means
the tar (or another file) was skipped.

---

## 4. Misroot sweep — current state and the copy-then-delete procedure

**Current state: clean.** Fleet root `git --no-optional-locks status --porcelain --untracked-files=normal`
prints **0** untracked entries; `ls /home/vgpnk/Projects/shokunin/*/R43*.md` → none; no `R43*.md` at the fleet
root, the lane root, `plans/` or `corpus/`. The lane's untracked set is exactly the wave-1 dispatcher's
(`.ufo/waves/round-43/w1-validate.out`, `w1.ready`, `w1.ready.dispatched`, `w1/`).

**Risk.** A seat that reports `Report: R43Xxx.md` (relative) from its fleet-root cwd creates an **untracked
file in the fleet repo** — invisible to the lane, visible as drift to the orchestrator — and a seat that writes
an absolute path under `/home/vgpnk/Projects/shokunin/.ufo/...` writes into the fleet's tree.

**Sweep (run by the L1 before the freeze commit, and again before the integration commit):**

```
cd /home/vgpnk/Projects/shokunin
git --no-optional-locks status --porcelain --untracked-files=normal \
  | sed -n 's/^?? //p' | grep -E '(^|/)R43[A-Za-z0-9_-]*\.md$'
ls /home/vgpnk/Projects/shokunin/*/R43*.md 2>/dev/null
```

For each hit `h`: `sha256sum -- "$h"`; `cp -p -- "$h" <LANE>/.ufo/waves/round-43/w1/`; `sha256sum` the
copy and require equality; `rm -- "$h"`; re-run the sweep and require empty output. If the destination name
already exists, do **not** overwrite — message the L1 with the digest pair. Never `git add`/`git rm` in the
fleet repo: the misrooted file is untracked, so deletion removes no committed state.

---

## 5. Licence and no-firmware-bytes audit (C2 copies)

**No third-party firmware bytes.** Magic scan of all 17 copies: no `\x7fELF`, no `hsqs`/`sqsh`, no ZIP
signature. Payloads are text, JavaScript, gzip and tar; every tar member was listed and every member is
source or metadata:

| copy | members | content |
|---|---|---|
| `S003/Base-src-go-rtti-members.tar` (61,440 B) | 2 | `GoApiSnapshot.java` (15,566 B), `GoRttiMapper.java` (41,672 B) |
| `S035/internal-abi-go1.25.0.tar`, `…1.24.6.tar` (81,920 B each) | 28 each | Go stdlib `src/internal/abi/*.go` |
| `S048/rea-agents-6.5.0-dist-cited-members.tar` (**2,048,000 B**) | 23 | npm `dist/**.js`; largest member `cli-runtime/cli.js` 1,813,387 B |
| `S081/rea-agents-6.7.0-dist-cited-members.tar` (51,200 B) | 3 | 2 JS + `package.json` |
| `S082/extra-db-tinyxxd-1.3.17-1-desc.tar` (10,240 B) | 1 | pacman `desc` (1,246 B) |

**Licence bases** (measured, one [INFERENCE]): S001/S002 operator skill files (internal); S003/S006/S007
Ghidra 12.1.4 → Apache-2.0 (`LICENSE` head read); S040/S048/S056/S066/S081/S083 rea-agents → **MIT**
(`package.json` of 6.5.0 live and of 6.7.0 inside the S081 tar both say `"license": "MIT"`); S023 the Ghidra-
packaged Go typeinfo JSON → Apache-2.0 as part of the Ghidra tree; S035 the 28 Go stdlib files → BSD-3
[INFERENCE: the installed `go1.27.3` tree ships no `LICENSE` file, so the clause rests on the Go project's
standard licence, not on a text I opened]; S082 desc/mtree/pacman slice → metadata facts, no licence field in
`desc`; S126 the sibling-project TSV. S135 (unblob 26.6.4 LICENSE, MIT) is **not yet in `corpus/SOURCES.md`**
(grep finds S130–S134 only), so the fixtures' licence citation is still pending the freeze — see D1.

**Fresh host re-verification (this round, `host-audit.json`).** 18 map entries:

* **15 live-equal**: 12 by file digest (S001, S002, S006, S007, S023 — also `gzip -dc` digest equal,
  S040, S056, S066, S083, S082/desc, S082/mtree, S126) and 3 by archive member-by-member
  (S003 2/2, S048 23/23, S082 extra.db 1/1). **0 mismatches.**
* **3 host-absent**: `S035` ×2 (`/home/vgpnk/.local/opt/go-1.25.0`, `go-1.24.6` no longer exist; only
  `go1.27.3` is installed) and `S081` (`/home/vgpnk/.npm/_npx/a1722018f28f9df2` gone; `npm cache ls` has the
  6.5.0 tarball but **not** 6.7.0). Their only remaining authority is the map digest plus the round-42 seat's
  receipts.

**Map replacement is a strict superset** of the committed map: 1 entry → 18, old keys ⊆ new, and the S126
entry is **field-identical** (all 7 keys, incl. `sha256` and `sha256_file`), so landing the prepared map loses
nothing. Row pins: only S126's URL cell pins a digest (`f205807d…`, `row_pin_scope: url-cell`, entry equal);
S035 and S082 are the only multi-path rows.

**Bound checks.** No copy exceeds 5 MiB (max 2,048,000 B). The landing **duplicates 4,281,141 B already
committed at base** under the artifact tree (`git ls-tree -r -l 6b9e64fe -- .ufo/waves/round-42/w1/artifacts/
R42LocalSrc/corpus/evidence/round-42/local-sources` → 17 blobs, same 4,281,141 B); that is the cost of the
amended destination and needs no action, only acknowledgement in the round's census.

---

## 6. Wave-2 attack surface — receipts wave 2 must be able to re-derive

Name these in the wave-2 items; each line is a command plus an expected value, not a verdict.

**C1**
1. `c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>` → exit 0, `matched == n == 78`,
   `observed_features_match_declared: true`, `counter_sha256 == counter_sha256_at_freeze`; every
   `claim_bindings` key present (a binding that reads a field the generator writes under another key fails
   silently — QUALITY 84).
2. Generator in scratch: `heldout-gen-v4r43.py --seed <FREEZE> --out <S>/heldout --run --scratch <S>` →
   byte-identical carriers (compare all 78 `carrier.sqsh` sha256 and the manifest).
3. Refusal: feed the round-42 C02 manifest tuple to the same check → exit 3, `declared_tuple_unobserved`,
   **no manifest written** (assert the path's absence).
4. `indep-eval-v4.py --envelopes <heldout> ` vs `sqfs-triage-v4.py <envelopes>` → identical (label, action)
   pairs for all 78; then the round-41 C1 receipts and the round-42 dev arm through the evaluator.
5. `CTL-C2-7-lookup.md` through the frozen interpreter → `combo_unseen_majority` ≥ 12 of 24 (exact count).
6. `git diff --name-only <d1681696>..<REV> -- tools/round-42/sqfs-triage-v4.py tools/round-42/indep-eval-v4.py`
   empty, and the SKILL v4 table region re-extracted and hashed against `d1681696`.
7. `git cat-file -e <FREEZE>:tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}` — all
   three present at the freeze (absent today; see D7).
8. S135 row present at REV, digest = `67303bbd…` (1,068 B), and `tools/round-42/fixtures.json` pins matching
   the committed fixtures.

**C2**
9. Gate at REV through the wrapper → exit 0, `rows_failed: []`, `rows_total` ≥ 129 (134 at `1ed29de2`;
   135 after S135), 19 records; independently recompute all 17 copy digests.
10. Red controls replayed in a fresh clone: dropped copy → `copy-missing`; one appended byte →
    `copy-digest-mismatch` with expected+actual; a stub at the old host path → still red (round-38 lesson).
    Measured this round: `S001 copy-missing` and `S040 copy-digest-mismatch c4d56e03… vs 42a90fe4…`.
11. `audit-local-source-copies.py --map … --copies-tsv … --root <pack> --root <LANE>` → 15 live-equal,
    3 host-absent, 0 mismatches (re-derive, do not trust my file).
12. No copy > 5 MiB; magic scan clean (no ELF/squashfs/zip).
13. Map entry set == the set of out-of-lane paths at REV (no missing key, no orphan entry).

**Cross-cutting**
14. QUALITY 84 evidence-tracked: `git ls-tree -r -l <REV> -- corpus/evidence/round-43 corpus/evidence/round-42/local-sources corpus/evidence/local-sources.json`
    vs disk; the landing alone must show `18 4292882`.
15. QUALITY 23: the three `evidence-timestamps.py --strict` runs of §1 at the shipping rev.
16. Frozen-path invariance: `git diff --name-only <FREEZE>..<REV> -- <each frozen path>` empty — with the C2
    landing explicitly exempted (D2) or it will read `frozen_path_changed`.

---

## 7. Defects

### D1 — HIGH — P43-C2's SOURCES byte-identity clause is falsified by the round's own S135 append

*Exploit path:* the freeze appends S135 to `corpus/SOURCES.md` (plan §Frontier step) while P43-C2 requires
"the `corpus/SOURCES.md` table itself is byte-identical to the base except nothing". At the measured revision
the table differs by one added row, so a literal reading of the frozen predicate is **false at REV** — and a
counter that implements the literal text (or a wave-2 reviewer who does) reds an otherwise green landing.
*Evidence:* `git diff --stat 6b9e64fe..HEAD -- corpus/SOURCES.md` → empty today; `grep '^| S13' corpus/SOURCES.md`
→ S130–S134 only, no S135; the plan names S135 as appended this round (LICENSE, 1,068 B, `67303bbd…`).
*Impact:* the claim's own predicate cannot be satisfied by the round's own frontier step; whichever lands
second breaks the other. *Smallest remediation:* reword P43-C2 to the 18 rows' URL cells plus "the only
base..REV delta in the table is the appended S135 row", and add a binding `sources_delta_is_s135_only`
(`git diff --unified=0 <base>..<REV> -- corpus/SOURCES.md` unfiltered additions = the S135 row).

### D2 — HIGH — C2 declares its own landing bytes frozen, then lands them after the freeze

*Exploit path:* the freeze-integrity rule (both claims) says a score at REV is admissible only if no commit in
`FREEZE..REV` touches a frozen path, "a later restore does not un-block (exit 2 `frozen_path_changed`)".
C2's frozen-path list contains `corpus/evidence/local-sources.json` and the copies under
`corpus/evidence/round-42/local-sources/`, and the same plan lands both **between freeze and REV** ("added
after the freeze — landing paths, not pre-landing bytes"). Under the rule as written, the C2 score is
inadmissible by construction; the C2 counter is the gate, which implements no freeze check at all, so nothing
mechanical catches it — wave 2 would be the first reader to notice.
*Evidence:* plan §Frozen paths (C2) vs §R43-C2 ("landing paths … after the freeze"); gate JSON keys measured:
no `frozen_paths_changed` field (the C1 counter's receipt has one, the gate's does not).
*Impact:* either the freeze rule or the claim is wrong; a reader applying the rule rejects a green score.
*Smallest remediation:* move the two entries out of C2's frozen-path list and bind the landing explicitly —
`first_added_after_freeze` per copy + map, plus `map_bytes_at_freeze_absent` — mirroring round-42 C1's
`manifest_after_freeze` / `manifest_before_envelopes` bindings. Keep the 18-row red control (CTL-C2-0) as the
"unmoved at freeze" half; that is what makes the pair honest.

### D3 — MEDIUM — the C2 counting receipt is not self-describing (no argv, no tool digest, revision only inside `table`)

*Exploit path:* a green receipt cannot be re-run from itself; the round-42 seat's receipt names a scratch
`root` that no longer exists, so "which tree resolved the copies" is unrecoverable. QUALITY 18 requires the
producing argv and the measured revision; QUALITY 21 forbids "exit 0" standing in for the recomputed values.
*Evidence:* gate output keys measured (list in §2); `receipt-wrap.py` run adds the missing fields and resolves
`revision` (`c2-gate-landing-form.json`, `c2-gate-pre-landing-lane.json`).
*Impact:* wave 2 must rebuild the invocation by hand; a `--rev` typo is undetectable. *Smallest remediation:*
use the supplied wrapper (or add `argv`/`self_sha256`/`revision` to the gate — the wrapper is smaller and
touches no frozen byte).

### D4 — MEDIUM — the map's `rebuild` cell is uniform and not runnable as written

*Exploit path:* all 17 new entries carry the same string `python3 build-copies.py --out <lane> --tarball-dir
<dir>`. From the lane root that is `python3: can't open file '<LANE>/build-copies.py'` (measured). The helper
is committed at `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/build-copies.py`, and it **hard-requires**
`dl/rea6.7.0.tgz` with digest `20958a66…` (`build-copies.py:317-327`), which is absent on this host — so a full
rebuild is impossible today, not merely undocumented.
*Impact:* "every copy is rebuildable" is untestable from the committed text; S081's copy cannot be rebuilt or
live-verified. *Smallest remediation:* record the exercised invocation verbatim in the C2 receipt (and/or in
the round's report): `python3 -I -B .ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/build-copies.py --out
<fresh-dir> --tarball-dir <dir with dl/rea6.7.0.tgz>`, with the tarball digest and the statement that today's
host lacks it.

### D5 — MEDIUM — "every copy re-verifies against the live host object" holds for 15 of 18 entries

*Exploit path:* P43-C2 asserts all copies re-verify against live host objects this round. Three cannot:
S035 ×2 (host go trees removed) and S081 (npx 6.7.0 cache removed). A wave-2 reviewer following the
predicate literally reds the claim for a host change that is not the lane's fault.
*Evidence:* `host-audit.json` — 15 `live-equal` (12 digests + 3 archives, 2+23+1 members), 3 `host-absent`,
0 mismatches. *Impact:* predicate/reality mismatch; a scorer reads the claim as unmet.
*Smallest remediation:* reword to "every copy whose host object still exists re-verifies (15/18), and the 3
host-absent entries (S035 ×2, S081) are named with their bytes bound by the map digest and the round-42 seat
receipt", or pin the upstream tarballs in a seat receipt (go1.25.0 release, rea-agents-6.7.0.tgz
`20958a66…`) — the latter converts the 3 into verifiable entries if a seat re-fetches them.

### D6 — LOW — the gate's live re-verification covers 4 of 18 entries

*Exploit path:* `source_digest_check: file` appears only for entries carrying `source_sha256` — S003, S023,
S082 extra.db, S126 (counted: 4 of 18). The other 14 green on copy↔map digest alone, so a stale map entry
whose copy is intact never reds.
*Evidence:* `gate-with-copies`-class receipts and my `host-audit.json` (`map_entries_with_source_sha256: 4`).
*Impact:* the gate cannot detect host drift for 14 entries; the claim's "fresh row-pin audit" is a seat
activity, not a gate property. *Smallest remediation:* either add `source_sha256` to the 10 file-sourced
entries my audit proved equal (each then re-checks on every future run — but a legitimately updated upstream
turns the gate permanently red; state that trade-off), or keep the map as is and record the audit as its own
receipt, with the claim saying the gate checks copies while the audit checks sources.

### D7 — LOW — the C1 frozen tools do not exist yet (freeze readiness)

*Exploit path:* `tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}` are named as frozen
paths and as the claim's instruments, but `ls tools/round-43` fails. A freeze that lands without them makes
`counter_sha256_at_freeze` undefined and CTL-C1-* unrunnable.
*Evidence:* `ls tools/round-43` → no such directory; `git cat-file -e 1ed29de2:tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}`
→ `MISSING` for all three (measured). *Impact:* the freeze would be internally inconsistent. *Smallest remediation:* the pre-freeze
check `for p in …; do git cat-file -e <FREEZE>:$p || echo missing $p; done` (run on the freeze commit before
the controls are scored).

### D8 — LOW — the timestamp gate's skip list on a wave tree is 201 binaries

*Exploit path:* running `--path .ufo/waves/round-42` yields 201 `skipped` entries, each a review obligation
under QUALITY 23; a 201-item manual review is not done, so the check becomes formal. `.ufo/waves/round-43`
has 0 skips today.
*Impact:* a real future-dated line could hide behind an unreviewed skip. *Smallest remediation:* scope the
round-43 check to `.ufo/waves/round-43`, `corpus/evidence/round-43`, `plans` (measured: 0/0/0 skips) and
record that scoping in the receipt.

### Confirmed sound (no action)

* The C2 landing is **green verbatim** at the amended destination: sandbox clone of `1ed29de2`, copies +
  map copied unchanged → gate exit 0, 19 records, `rows_failed []`, `rows_total` 134, all 17 copy digests
  matched, `table` pinned to the landing commit.
* Do-nothing control is red at HEAD: exit 1, `rows_failed` = the 18 ids, reason `no-copy-named` (the round-41
  map has no entry for them), S126 `resolved` — the draft's "shows it unmoved" command is accurate.
* Red controls are genuinely red (`copy-missing`; `copy-digest-mismatch` with expected/actual) and green after
  restore — the round-38 "must not green on a stub" property holds for the gate's vocabulary.
* `corpus/SOURCES.md` is byte-identical base..HEAD (the C2 clause is true *today*; D1 is about the freeze).
* No firmware bytes, no ELF/squashfs magic, no copy over 5 MiB; map replacement is a strict superset with the
  S126 entry field-identical.
* Fleet root and every lane root are free of misrooted reports; the lane's only untracked entries are the
  wave-1 dispatcher's.

---

## 8. Accounting

* Tools installed/upgraded: **none**. Nothing written to `~/.local/bin` or any PATH directory.
* Runs: `git`/`jj` reads in the lane and fleet; `file`, `tar -t/-xO`, `gzip -dc`, `sha256sum`, `npm cache ls`;
  `local-source-gate.py` (read-only), `evidence-timestamps.py` (Git objects only), `indep-eval-v4.py --help`,
  `sqfs-triage-v4.py --help`. One `git clone --shared` sandbox
  (`$S/fx.RfS8/lane`, fixture identity, `rev-parse --show-toplevel` asserted before the only commits there).
* REA / unblob / sasquatch: not run. No published firmware image touched.
* Scratch removed: `/fast/scratch/hyaku/kaidoku-r43/w1-R43SentProv`. Nothing citable remains outside
  `artifacts/R43SentProv/` and this report.
