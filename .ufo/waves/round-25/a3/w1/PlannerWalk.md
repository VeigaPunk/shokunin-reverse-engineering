# PlannerWalk — three candidate claims for the lane's next round

Seat: leaf planner data walk. Target: propose next-round claims with one counting command over committed bytes each, a concrete after value, and the axis moved. Measured lane rev: `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76`. All times UTC 2026-10-22. Lane read-only; scratch `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/`. No REA request was made; no tool was installed.

## Read
`PROVINCE.md` Frontier (`:84-93`), `corpus/README.md` Frontier (`:187-197`), Known gaps (`:199-206`, identity bullet `:203`), coverage map crash row (`:32`); `SCORECARD.md` owned axes (`:19-31`), round-24 planned (`:2907-2910`), round-25 planned (`:3059`); frozen claims `.ufo/waves/round-25/a2/claims.json`, `corpus/claim-freezes.tsv`, `tools/round-25/*`.

## Observations

O1 — **Zero-mention coverage residue is fenced, not a candidate.** Command `python3 -I -B .ufo/waves/round-24/tools/count-c1.py --root <LANE> --rev 08c7a729…`, exit 0, 2026-10-22T10:44:40Z. Excerpt: `"catalog_total": 153, "catalog_zero_count": 12`, list `list-cutter-sessions, cutter-command, debug-with-gdb, debug-with-rizin, list-frida-devices, list-frida-processes, instrument-with-frida, inspect-adb-package, list-adb-services, inspect-adb-window, start-adb-activity, stop-adb-app`. Verdict: 5 adb + 3 frida + 2 cutter + 2 debugger verbs are all Adjacent/blocked by the round-22/23 tables; a coverage claim here would absorb refused ground. Observation.

O2 — **The freeze ledger is red at the tip and blind to the attempt-scoped claims file.** Command `python3 -I -B .ufo/waves/round-24/tools/freeze-gate.py --root . --rev 08c7a729… --disclosures corpus/claim-freezes.tsv`, exit 1, 2026-10-22T10:52:32Z. Excerpt: `"audited": 12, "clean": 1, "disclosures": {"exact": 11, "of": 12, "missing": ["round-25"]}`; round-25 finding `INSTRUMENT_ABSENT tools/round-25/instrument-custody.py` plus `INSTRUMENT_REVISED commits ["fafdd283…"]`. `.ufo/waves/round-25/a2/claims.json` appears in no `freezes[]` entry (its regex is anchored to `.ufo/waves/round-N/claims.json`). The a2 entry cites two tools absent from its pin map; `cited-instruments.json`, exit 0, 10:54:22Z: pinned `c1-calibration.py, c2-coverage.py`; cited `resolve-selectors.py, tally-resolution.py`; `"cited_unpinned"` = those two. `git ls-tree 7ef837a -- tools/round-25` (exit 0) shows the two absent at the a2 freeze; present at the tip. Observation. This is exactly the round-24 planned extension still unlanded (`SCORECARD.md:2907-2910`).

O3 — **Exactly one organic core is currently sub-cap.** Decompressed identity in `organic-core-identity.json`, exit 0, 10:53:15Z: `/var/lib/systemd/coredump/core.chrome_crashpad.1000.…215760….zst`, compressed 49,672 B, decompressed **17,608,704 B**, sha256 `5bc56706261968c46427a25b1db226be2f8a02ab8bbec317cb685134fa62ebff`, magic `7f454c46`, under the 33,554,432 B cap. `coredumpctl info 215760` excerpt: `Signal: 7 (BUS) si_code: BUS_ADRERR`, command line `chrome_crashpad_handler … --annotation=prod=Electron --annotation=ver=42.1.0`, executable `/chrome_crashpad_handler` from a `/tmp/.mount_appimarqapgK/` AppImage mount (Grok Bot 0.72.0). The only other core, `core.waybar…1730…zst`, decompresses to 291,749,888 B; that size exceeds the cap, and the over-cap refusal semantics are recorded in `2026-10-13-r2-crash-inspect-probe.md` (I did not re-run the refusal). Observation for the size and metadata; inference for the refusal. The round-1 survey counted 174 cores, so retention decay is real.

O4 — **The CBOR metadata-trailer surface is already held.** `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:28` decodes the same `a2 64 69706673 58 22 … 64 736f6c63 43 000825 00 33` trailer (solc 0.8.37) on a committed carrier. A decode of the six round-25 carriers at the tip (`cbor-trailer-scan.json`, `git show` reads, exit 0, 2026-10-22T10:58:28Z) prints `with 4 without 2`: four solc carriers carry `solc 0.8.37` + a 34-byte IPFS multihash + `0033`; `stewardtoken` and `carrierv` carry none. It adds no surface. Verdict: rejected as duplication, not proposed.

O5 — **Evidence-id controls exist, but never under one pin.** Observation from `corpus/knowledge/`: two-path controls exist at 6.4.0 for `analyze`/`inspect` (`2026-10-13-r5-01-riscv-bypass.md:85`) and the `function` verb (`2026-10-14-r9-02-queue-a-ops-2.md:146-169`; the Known-gaps bullet calls it `analyze_function`), and at 6.7.0 for `inspect-artifact` (r11), `inspect-evm-interface` (arc3-r7), `inspect-rust-binary` (arc3-r10), `inspect-go-binary` (arc3-r12). At the lane's operative carrier pin `rea-agents@6.5.0` there is no control for any of them. `id-controls-scan.json` (`git show` reads at the tip, exit 0, 2026-10-22T10:58:28Z) locates all six control statements. The Known-gaps sentence (`README.md:203`) still converts a 6.4.0 aside into a verb-family rule for `analyze`/`inspect` with no citation to r5-01.

## Candidate C-A — calibration: make the freeze ledger as wide as the evidence chain

- **Claim:** after the commit, an extended gate audits every retained claims file (12 top-level + `.ufo/waves/round-25/a2/claims.json` = 13), reads not only `claims.json` strings but every instrument named by a claim's cited knowledge entry, and requires a ledger row whose verdict and finding codes equal its own; the round-26 claims freeze is audited by the same gate before measurement. Historical claims files stay byte-unchanged; the two round-25 dispositions are separate ledger rows plus a scope-disclosure file.
- **Command:** `python3 -I -B .ufo/waves/round-26/tools/freeze-scope.py --root <LANE> --rev <REV> --disclosures corpus/claim-freezes.tsv` (Git-object reads only; instrument committed before the round-26 claims freeze).
- **Before (measured, O2):** `audited 12`, `exact 11`, `missing ["round-25"]`, exit 1; a2 audited 0 times; `cited_instruments 4`, `audited 2`, `uninspected 2`.
- **After:** `audited 13`, `exact 13`, `missing []`, `stray []`, `cited_instruments 4`, `uninspected 0`, exit 0; ledger rows `round-25 FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED` and `round-25-a2 FLAGGED INSTRUMENT_ABSENT,INSTRUMENT_REVISED` with pointers; round-26 CLEAN. The a2 freeze is **disclosed, not repaired** — its instruments were genuinely absent at `7ef837a`.
- **Axis:** calibration. **One-round size:** one script extension (regex + entry-citation scan + disclosure parsing), two ledger rows, one disclosure file, one self-audit; no probes, no web, no REA. It cannot be smaller because the ledger must agree with the extended gate, and the two round-25 rows are the counterexamples that make the extension testable.
- **Risk:** the ledger is author-written, so the gate proves agreement, not truth; the anchored pattern must not pick up the round-23 runtime clone copies (measured: 34 `claims.json` paths exist, 21 of them under `round-23/runtime|worktrees`).

## Candidate C-B — coverage: first organic-recorded-crash holding

- **Claim:** one organic, sub-cap core is inspected end to end and held: a committed identity receipt (path, compressed/decompressed size, sha256), a REA 6.5.0 run record (exit 0, argv names `inspect-recorded-crash` and the core path), the envelope (`format: "elf-core"`, `ev_` id, thread registers, signal), and a knowledge entry whose `source:` line cites the envelope and id. The coverage-map row `corpus/README.md:32` and `PROVINCE.md:84-86` move from "organic cores too big" to "one sub-cap organic core held; larger cores still refused".
- **Command:** `python3 -I -B tools/round-26/organic-core.py --root <LANE> --rev <REV>` — reads only committed bytes; counts the one frozen target as complete when all four artifacts verify and the core size/sha256 in the receipt match the envelope subject.
- **Before:** 0/1. The held crash evidence is a deliberate `crash-godot` self-kill (`r2-06`, `r4-13`); no organic core has an envelope or entry.
- **After:** `cores_complete 1, cores_total 1, entry_sourced 1, map_row 1`, exit 0; core identity as O3 (17,608,704 B, sha256 `5bc567…`, SIGBUS/BUS_ADRERR).
- **Axis:** coverage (a new edge class, "organic crash corpora", under an already-held mechanism; the lane's own map calls it a coverage frontier). **One-round size:** one pwntools run on 17.6 MB, one entry, one map row, one PROVINCE line. It cannot be smaller without losing the entry; it cannot be much larger without adding the >cap cores, which have no knob.
- **Risk:** retention decay or host change between freeze and run. The claim must re-verify the core at freeze and withdraw rather than substitute if it is gone; the 291,749,888 B waybar core is over cap and is **not** a fallback. The core is a crashpad-handler core, not app logic: the entry must claim registers/segments/notes, not application behaviour.

## Candidate C-C — depth: one-pin evidence-id identity table

- **Claim:** the eight native reader verbs `analyze, inspect, decompile, xrefs, read-bytes, function, instructions, inspect-binary-layout` each get base, same-path repeat and byte-identical-copy runs at `rea-agents@6.5.0`; a committed table records, per verb, the three ids, the copy subject digest, and the verdict `path-sensitive` or `content-keyed` (or `no-id`). `corpus/README.md:203` is rewritten as a pointer to the table, with every lane-owned verb clause carrying a table citation or `unknown`.
- **Command:** `python3 -I -B tools/round-26/id-identity.py --root <LANE> --rev <REV>` — 8 rows; each row needs three committed envelope records whose `subject.digest.sha256` agree, ids equal/unequal as the verdict says, and 0 uncited lane-owned clauses in the identity bullet.
- **Before:** 0/8 at 6.5.0. Existing controls: `analyze`, `inspect` and `function` at 6.4.0, four `inspect-*` families at 6.7.0; five of the eight native readers (`decompile`, `xrefs`, `read-bytes`, `instructions`, `inspect-binary-layout`) have no two-path control at any pin. `README.md:203` has one uncited lane-owned clause (`analyze`/`inspect`; the source is `r5-01:85`, unlisted).
- **After:** `rows_complete 8, rows_total 8, uncited_clauses 0`, exit 0; one knowledge entry and one table.
- **Axis:** depth (a decision table with named per-verb outcomes replaces a family-wide assertion). **One-round size:** 24 CLI calls on one 30,800 B ELF pair (~2–5 min of Ghidra imports), one table, one entry, one README sentence. Smaller would leave the operative pin untested; larger would pull in the JS/APK/WASM families whose carriers dominate runtime.
- **Risk:** `inspect` may mint the same id as `analyze` (r5-01 observed `ev_e9a735a2…` for both), which must be recorded as an alias finding, not hidden by choosing only one verb; `function` envelopes are multi-MB (r3: 6.2 MB) so the table should store ids, subject digests and sha256s rather than whole envelopes; if a verb returns no `ev_` id, the row is `no-id`, not a failure.

## Rejected or fenced ground (why not proposed)

- 12 zero-mention catalog verbs — all Adjacent/blocked (O1).
- Organic cores >32 MiB — no cap knob; waybar 291,749,888 B over cap (O3).
- `.jsc` → source mapper — real frontier (`README.md:190`); a bytecode-to-source mapper is larger than one round, and the host's `jscd` tables stop at V8 14.6 (`README.md:24`) while the target is V8 14.8.
- sasquatch — AUR-only, pacman paused; 7z fallback already covers the path.
- Alternate providers (IDA/Hopper/JEB) and macOS surfaces — operator-owned/unsupported.
- CBOR metadata trailer — already held (O4).
- Debugger/Frida/adb ownership — Adjacent; no absorption (PROVINCE round-22/23 exclusions).

## Artifacts (sha256)

| file | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/zero-mention-tip.json` | `62953ab65ddc2cc0963b0b3a992c8cc956e3fd74996261ae2655287e4ad18cbd` |
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/freeze-gate-tip.json` | `d8fae8262dbd6fe5d88f10c5986014098646f9350df8d48cebbd7cdb0fa47a56` |
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/cited-instruments.json` | `e300051fc77f63656e667c29e214ca93ca879b516e40abe602948788d7a2afa5` |
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/organic-core-identity.json` | `d07e66fce93069b85d25e426c2d33275d4a141d5fc45aac7a137c56effaaadfd` |
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/cbor-trailer-scan.json` | `a50d624739c26b1acad7581cfc89ff0864a4105ebf13b24fb9ef5d215c892595` |
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/PlannerWalk/id-controls-scan.json` | `7a096b6466a596b3524bf3d950f9d0de4c7fef2f4b6fde45b1e6f26e34cfe40d` |

Labels: O1–O5 observation; candidate after values are targets, not results; the a2 instrument-absence is observation at `7ef837a`, and C-A discloses it rather than claiming it clean.
