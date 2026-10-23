# ConnSiblingsRust — round 30, wave 1 sibling-overlap scan (read-only)

## Result and axes

**Verdict: holds — no sibling lane holds ground on the round-30 surface.** Across all
20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` there is **zero**
occurrence of `.dep-v0`, `inspect_rust_binary` / `inspect-rust-binary`,
`auditable_metadata`, `RustBinaryImage`, `RustAuditable`, `RustBinaryService` or
`rust-auditable`. The only sibling occurrences of any listed term are three
`cargo-auditable 0.7.7-1` rows in tsukuroi's pacman **sync-database listings**, which
denote an Arch package name and carry no `.dep-v0`, REA or refusal content
(§2). **Nothing is absorbed; one cite-not-absorb note (§2) and one fleet-level
false-negative hazard (§5).**

Axes in view: **R30-C1 coverage** (the positive input class and its province claim) and
**R30-C2 depth** (the refusal-signature table). The move in §6 is offered against C1's
coverage evidence and leaves C2 untouched.

[obs] Scope: the 21 `*-shokunin` directories under the fleet root
(`ls -d /home/vgpnk/Projects/shokunin/*-shokunin/ | wc -l` → `21`, exit 0, 02:47:19Z).
Kaidoku is the lane under test and is excluded from the sibling verdict; it was read
only for boundary comparison. The two lane-like non-`*-shokunin` paths
(`mori-shokukin`, `tameshi-shokukin`) and the empty `kaidoku-sh2` were also searched.

[obs] Method: per-lane `grep` calls, one lane per call, patterns
`dep-v0|cargo-auditable|inspect[-_]rust[-_]binary`, then
`…|auditable_metadata|RustBinaryImage|uvx|uv 0\.13`, then
`rust-auditable|RustAuditable|RustBinaryService|dep-v0`, then
`cargo.{0,20}auditable|auditable.{0,20}cargo`. No REA call, no carrier or mutant
executed, no network request, no lane write except this report, no installs.

[obs] Label convention: `[obs]` observed here; `[inf]` inference; `[unk]` unknown.
The `grep` tool does not surface a process exit code; its zero-match report is
`No matches found` (grep exit-1 semantics) and it is reported as such, never as a
measured exit code. Raw log with every pattern/path pair and outcome:
`/fast/scratch/hyaku/kaidoku-r30/seats/w1/ConnSiblingsRust/scan-log.md`,
sha256 `13ede4fd2d635975f6279397dfa3c2112dee3a7f34a1c6b464d76b395e2d72b0`.

## 1. Per-sibling hits

| sibling lane | hits on the five terms | disposition |
|---|---|---|
| audio-shokunin | none | no overlap |
| chousa-shokunin | none | no overlap |
| game-dev-2d-shokunin | none | no overlap |
| game-dev-3d-shokunin | none | no overlap |
| kagi-shokunin | none substantive; `uvx` only as a substring of scratch tokens `kagi-r28-c1-v0z2quvx` (`.ufo/waves/round-28/retained-probes/CheckNoHarm/receipts/c1-cand.json:11,13,15` and the `sandboxes/` twin) | false positive |
| kake-shokunin | none substantive; `uvx` in `.ufo/waves/round-23/gen_w2.py:86`, `.ufo/waves/round-23/w2-spec.json:526`, `w2-dispatch.json:1001` (dispatch prompt) and `.ufo/waves/round-35/w1/CriticC2Conditions.md:12` (`uvx --with cmarkgfm==2024.11.20`) | tooling record |
| kama-shokunin | none | no overlap |
| kasegi-shokunin | none | no overlap |
| kengaku-shokunin | none substantive; `uvx webarena-verified` in `.ufo/waves/round-29/scratch/falsify/FCritNovelty/fetch/wav_readme.md:21,35,38,64` (fetched third-party README) | tooling record |
| kotoba-shokunin | none substantive; `uvx` inside a binary strings dump `.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:89685,160982` (MIME table) | false positive |
| kotodama-shokunin | none substantive; `uv 0.13.0` tooling records (`.ufo/waves/round-50/build/ReviewReadmeRev.md:134`, `.ufo/waves/round-51/falsify/ReviewCSec05.md:116`, `.ufo/waves/round-58/build/ExecHarmCheck58.md:188`, `.ufo/waves/round-58/control/MutLegIsolation58.md:82`) | tooling record |
| kumitate-shokunin | none substantive; `uv 0.13.0` (`.ufo/waves/round-40/build/ExecMutLedger.md:57`, `ScribeSourceMTE.md:37`) | tooling record |
| lore-shokunin | none | no overlap |
| mado-shokunin | none substantive; `uvx` in the rounds 17–19 installer-class tripwire (`.ufo/waves/round-18/drafts/TwInstallerChannels.patch:12,117`, `.ufo/waves/round-18/tripwire/r18-installers/expected.json:34`, `compound-and-wrappers.jsonl:4`, `.ufo/waves/round-18/w1/reports/TwInstallerChannels.md:61`, `.ufo/waves/round-19/w1/reports/TwInstallers.md:46`) | tooling record |
| mori-shokunin | none substantive; `uvx` in `.ufo/waves/round-17/falsify/ConformanceAudit.md:94` (tool-channel list) | tooling record |
| revenger-shokunin | none substantive; `uv 0.13.0` in `.ufo/waves/round-61/build/ExecEvmOracleR22.md:50`, `ExecEvmOracleR23.md:65`, `ExecEvmOracleR24.md:58`, `ExecEvmOracleR26.md:52`, `ExecSelectorKeccak.md:67`, `SrcSolidityAbiSelector.md:62`, `falsify-w3/W3EvmPairR19R21.md:6`, `W3EvmR25R26Targets.md:34` | tooling record |
| souji-shokunin | none | no overlap |
| tabi-shokunin | none | no overlap |
| tameshi-shokunin | none substantive; `uv 0.13.0` in the round-23/25/26/27/28 reports (e.g. `.ufo/waves/round-25/w1/C2Determinism.md:52,265`, `C2LiveCheck.md:172`, `NoHarmMonitor.md:259`, `.ufo/waves/round-23/fresh-adjudication-draft.json:26`) | tooling record |
| **tsukuroi-shokunin** | **`cargo-auditable 0.7.7-1` × 3** (see §2) | name-only, cite-not-absorb |

[obs] The bare word `auditable` was searched literally in 8 lanes (audio, chousa,
game-dev-2d, game-dev-3d, kagi, kake, kama, kasegi); every hit is the ordinary English
adjective in receipt/auditability prose (e.g. `audio-shokunin/corpus/live/r77-scout/probe_a3b_override_extent.py:6`,
`chousa-shokunin/corpus/lessons/2026-10-16-gate-behavioral-baseline.md:108`), never a
cargo or Rust sense. The discriminating co-occurrence patterns
(`rust…auditable`, `auditable…rust`, `cargo…auditable`, `auditable…cargo`) were run on
all 20 siblings; the only matches anywhere are the three tsukuroi files in §2.

[obs] Sensitivity control: `RustBinaryImage|auditable_metadata` on
`kaidoku-shokunin/tools` matches `tools/round-30/c1-rust-positive.py:7,66,71,108,281`
and `tools/round-30/c2-rust-refusals.py:123,132,135,139,143,177,391`. The search method
does find these tokens where they exist; the sibling zero-results are not a tool blind
spot.

## 2. The one sibling occurrence: tsukuroi's package-name listings

[obs] Exact hits:

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/host-extra-pkglist.txt:756` → `cargo-auditable 0.7.7-1`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/official-extra-pkglist.txt:758` → `cargo-auditable 0.7.7-1`
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/stable-extra-pkglist.txt:758` → `cargo-auditable 0.7.7-1`

(adjacent line in each: `cargo-audit 0.22.2-1` at `:755` / `:757` / `:757`.)

[obs] Provenance of those files, read in the same directory:
`supplemental-measurements.txt:8-11` records `md5sum /var/lib/pacman/sync/{core,extra,multilib}.db`
→ `e96d1a0fed34b2245280d39bad1901d8` (:9), `6ae3ab01dc16504115c2a424578e4c37` (:10),
`8e3bc2efa7344914cabc83014d897778` (:11); the two *downloads* differ
(`8dbc3bdfe0a7860a38d2f39eb7989087  dl-stable-extra.db`, `991e76f34e00d2edb56fa2b550db2556  dl-official-extra.db`,
:29-30). `ExecMirrorTimestamps.md:13` states "These are repository-entry comparisons,
not installed-package upgrade counts."

[obs] Independent check that these are **not** an installed set:
`pacman -Q uv python-uv python-uv-build cargo-auditable` printed four
`error: package '<name>' was not found` lines, `pacman-query-exit=1` (02:50:40Z), and
`which -a uv uvx` resolves only to `/home/vgpnk/.local/bin/{uv,uvx}` with no `/usr/bin/uv`.

**Cite-not-absorb note (tsukuroi).** Cite these three lines only as the fleet's *prior
sense* of the string "cargo-auditable": an Arch package name in a mirror/sync-database
listing, produced for tsukuroi's round-24 mirror-age measurement. Do **not** absorb them
as evidence about the `.dep-v0` section format, as a carrier or fixture, as a
dependency-package count, or as any input to P1-pass or P2-match; they contain no
section bytes, no package list and no REA output, and tsukuroi's own report disclaims
installed-package reading. The round-30 entry
(`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`) will be the fleet's first
artifact where "cargo-auditable" denotes the *format*; one provenance sentence
distinguishing the two senses is enough, and it should carry these three paths.

**Second, weaker adjacency (same lane, same files).** [obs] tsukuroi's listings also
carry `uv 0.13.1-1` (`host-extra-pkglist.txt:14048`), `uv 0.13.4-1`
(`stable-extra-pkglist.txt:14056`), `uv 0.13.5-1` (`official-extra-pkglist.txt:14056`)
and the diffs `host-vs-stable-extra.txt:2121`, `stable-vs-official-extra.txt:38`. These
are repository-entry versions of the *pacman* uv, a different object from the uv 0.13.0
PyPI wheel members frozen as R30-C1 carriers. Cite-not-absorb: do not read the sibling
rows as a host uv version, and do not read them as a carrier source; the host carries no
pacman uv at all (previous paragraph).

## 3. Adjacent ground that is not a sibling (kaidoku's own prior rounds, and the fleet record)

[obs] The frozen claims already cite the lane's own prior ground in the C1 `surface`
text: `corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md` and
`corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md` ("no .dep-v0 found"),
and the C2 `limits` names the 6.5.0 dist JavaScript and node v24.21.0.
`.ufo/waves/round-29/w1/ConnectorSiblings.md` is the round-29 precedent for this scan
type; it is the lane's own record, not sibling ground.

**Cite-not-absorb note (prior rounds).** Cite those two entries as the *null-metadata*
prior state only. They are not positives and not refusal data: the round-10 work was
produced against `rea-agents@6.7.0`
(`.ufo/waves/arc3-loop1-round10/claims/c1/EX-4.md:3` "in REA 6.7.0"; `:11` "the host's
cached `rea-agents@6.7.0`") while round 30 measures the pinned 6.5.0
(`claims.json` `rea_pin.package` = `rea-agents@6.5.0`, `package_json_sha256`
`a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`). Do not treat the
round-10 path-sensitivity finding as a 6.5.0 datum, and do not let the surface sentence
imply one pin produced both.

[obs] Tension worth stating, not smoothing: `EX-4.md:22` records that the round-10 probe
envelope has `auditable_metadata:null` on `/usr/bin/rustc`, i.e. the verb returned ok
with null metadata. The round-30 C2 counter predicts the *refusal* message
`Dependency section is not file-backed` for a zero-size section
(`tools/round-30/c2-rust-refusals.py:132`) — a different outcome class from the round-10
observation. These are not contradictory (different inputs), but a reader who merges
them will state a refusal that the round-10 bytes did not produce. Keep them separate.

[obs] Fleet-level (not a lane): `/home/vgpnk/Projects/shokunin/MANIFEST.json:5339` and
its four frozen copies under `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/frozen/*/MANIFEST.json:5339`
each carry the round-10 note "C1 coverage: inspect_rust_binary ev_ formula CLOSED
(88->89; second verb family; path-sensitive semantic projection)". Those five files are
the only non-lane occurrences of `inspect_rust_binary` in the fleet.

**Cite-not-absorb note (fleet MANIFEST).** "88->89" is a *knowledge-file count* (the
round-10 report's own table reads "corpus 88 … 89 files"), not a SCORECARD row label;
`grep 'S088|S089|S090|S091'` on `kaidoku-shokunin/SCORECARD.md` returns S088 (and
S087/S084) lines and no S089/S090/S091 line, so the round-30 claim rows S089 and S090
are unoccupied. [obs] The MANIFEST note must not be used as round-30 evidence: it
records a closure, not a `.dep-v0` positive, and it says nothing about refusals.

## 4. Host-identity evidence behind C1's `carriers` sentence

[obs] `claims.json` `claims[0].carriers` asserts "host ~/.local/bin/uv and uvx are
byte-identical to the manylinux x86_64 members and are not separate carriers". That
sentence has no producing command in any frozen instrument; it is checkable now, and it
holds:

```
sha256sum /home/vgpnk/.local/bin/uvx /home/vgpnk/.local/bin/uv
2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d  /home/vgpnk/.local/bin/uvx
3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0  /home/vgpnk/.local/bin/uv
stat -c "%s %n" … → 332008 /home/vgpnk/.local/bin/uvx ; 39714040 /home/vgpnk/.local/bin/uv
                                                              # exit 0, 02:47Z window
```

against the frozen list `corpus/evidence/round-30/c1/carriers.tsv:2-3`
(`elf-x86_64-uv` sha256 `3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0`,
size 39714040, member `uv-0.13.0.data/scripts/uv`; `elf-x86_64-uvx` sha256
`2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`, size 332008, member
`uv-0.13.0.data/scripts/uvx`). Both digests and both sizes are equal. [inf] The sentence
is therefore supported, and the carrier count of 16 stands with the host copies
correctly excluded as non-carriers.

## 5. The one non-obvious hazard: a fleet-root search is a silent false negative

[obs] Rooted at the fleet root with default settings, `dep-v0` and `cargo-auditable` both
report `No matches found` — **both wrong**, since `kaidoku-shokunin/tools/round-30/*.py`
contains `.dep-v0` and tsukuroi's three files contain `cargo-auditable`. Rooted the same
way with `gitignore:false`, the same patterns report `Grep timed out after 30s`.

[obs] Cause: `/home/vgpnk/Projects/shokunin/.gitignore:1` is `*-shokunin/`, so a
default search rooted at the fleet root skips every lane tree; lines 2-3 re-include only
`scripts/fixtures/sources-census/**/*-shokunin/` (synthetic fixture lanes). A fixture
search was run and found nothing (`scripts/fixtures` → `No matches found`), but the
asymmetry remains: a root-level search can return *some* synthetic-lane hits and thereby
look like it covered the fleet while every real lane was skipped.

[inf] This matters to round 30's verification surface, not to its predicates: any seat
(or closure reviewer) who checks "does any sibling name this verb / this section" with a
fleet-root search will get a false negative, and the round-29 precedent's own
verification section prescribes the correct form (explicit `*-shokunin` globs). Neither
frozen counter is affected — both `unmoved_command` forms are lane-scoped
(`git -C <LANE> show …`).

## 6. Proposed move (one)

**Give C1's `carriers` sentence and its province claim a producing command by landing a
single read-only fleet-adjacency receipt in the wave-1 record — outside the frozen
instruments and outside `claims.json`.** One bounded artifact (e.g. a section in the
round-30 wave-1 evidence, or a provenance block in the C1 entry at integration), holding
exactly three lines, each with the command that produced it:

1. **Host identity:** `sha256sum /home/vgpnk/.local/bin/uv /home/vgpnk/.local/bin/uvx`
   plus `stat -c %s` → the two digests and two sizes quoted in §4, with the observation
   time, tied to `carriers.tsv:2-3`. This turns the claim's byte-identity sentence from
   an assertion into a receipt, and it is the *only* place the host copies enter the
   record — explicitly as non-carriers.
2. **Fleet adjacency:** the search recipe (`/home/vgpnk/Projects/shokunin/*-shokunin`
   globs, hidden and ignored files included, one lane per search) and its result — zero
   sibling hits for `dep-v0`, `inspect[-_]rust[-_]binary`, `auditable_metadata`,
   `RustBinaryImage`; exactly three `cargo-auditable` name-only rows in tsukuroi, cited
   per §2 with the disclaimer that they are sync-database listings. This is the
   evidence that the province gain is the lane's alone.
3. **The search-mode disclosure:** the fleet root's `.gitignore:1` `*-shokunin/` makes a
   root-level search a silent false negative (§5), so the recipe in line 2 is the form
   the receipt asserts, and a root-level search result may not be used to restate it.

Affected axes: **C1 coverage improves** — its province/uniqueness side becomes
reproducible and its host-identity sentence becomes evidence-backed, with no change to
the predicate, the target line, the carrier list or the carrier count (16). **C2 depth is
unharmed** — no prediction, mutant, message or the frozen `predictions.tsv` is touched.
Nothing is admitted, scored or integrated by this report.

## 7. Risks

- [obs] `claims.json` is frozen by its first commit and the three instruments are pinned
  by sha256 in it; a receipt that edits either would break the freeze. The move therefore
  lands in the wave record / entry provenance only, and must not be cited as amending a
  predicate or target.
- [obs] Host file identity is mutable: `uv self update` or a download would change
  `~/.local/bin/uv`. The receipt must carry the observation time and must not be re-run
  later as if it were the same measurement.
- [obs] `pacman -Q` is a query, not a transaction (the host-wide pause is respected); the
  receipt must not be read as an install census, and the four "not found" lines are the
  whole of that observation.
- [inf] The fleet-adjacency result is a snapshot of the lane trees at 2026-10-23T02:5xZ.
  A sibling lane that later adds Rust/`.dep-v0` material, or material inside a nested
  `.jj`/sandbox copy already present, could change it; the recipe makes that cheap to
  re-check.
- [unk] Whether any *future* round will need the same scan for the PE/thin-Mach-O
  refusal branches; this scan found no sibling ground there either, so it cannot be
  sourced from a sibling.

## 8. Verification

- `sha256sum /home/vgpnk/.local/bin/uv /home/vgpnk/.local/bin/uvx` → expect
  `3e801df892439f5cde65d8b51ea69b69abff199ef37cc3cae4481be15d592df0` and
  `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`; `stat -c %s` →
  `39714040` and `332008`. Compare with `corpus/evidence/round-30/c1/carriers.tsv:2-3`.
- Per lane: search `dep-v0|cargo-auditable|inspect[-_]rust[-_]binary|auditable_metadata|RustBinaryImage`
  with the lane as the root → expect zero matches in all 20 siblings; expect matches only
  in `kaidoku-shokunin` (tools/round-30 and corpus). Expect exactly three files matching
  `cargo-auditable` in `tsukuroi-shokunin`, at the three lines in §2.
- False-negative demonstration: the same patterns rooted at
  `/home/vgpnk/Projects/shokunin` with default settings → expect `No matches found`
  despite the lane hits above; with `gitignore:false` → expect a traversal timeout.
  `read /home/vgpnk/Projects/shokunin/.gitignore` → expect `*-shokunin/` on line 1.
- `grep 'S088|S089|S090|S091' kaidoku-shokunin/SCORECARD.md` → expect S088/S087 lines
  and no S089/S090/S091 line.

## 9. Commands, timestamps, exit codes, installs

- Session window 2026-10-23T02:40Z–02:52Z; harness-stamped anchors
  `2026-10-23T02:47:19Z` (`date -u` with the lane listing, exit 0),
  `2026-10-23T02:49:39Z` (scratch dir creation, exit 0),
  `2026-10-23T02:50:23Z` and `2026-10-23T02:50:40Z` (log hashing, exit 0). The harness
  does not stamp each tool call, so grep outcomes are reported without individual times.
- `pacman -Q uv cargo-auditable` → two `error: package … was not found` lines, exit 1.
  `pacman -Q uv python-uv python-uv-build cargo-auditable` → four such lines,
  `pacman-query-exit=1`. `which -a uv uvx` → only `/home/vgpnk/.local/bin/{uv,uvx}`.
  `ls -l /usr/bin/uv` → `No such file or directory`.
- `sha256sum /usr/bin/uv /home/vgpnk/.local/bin/uv` → one `No such file or directory`
  error plus the host digest, overall exit 1 (the `/usr/bin/uv` leg is the expected miss).
- `sha256sum /home/vgpnk/.local/bin/uvx /home/vgpnk/.local/bin/uv` with `stat -c "%s %n"` → exit 0.
- Raw log: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ConnSiblingsRust/scan-log.md`,
  sha256 `13ede4fd2d635975f6279397dfa3c2112dee3a7f34a1c6b464d76b395e2d72b0`.
- Installs: **none**. No pacman transaction (host-wide pause respected), no `uv tool`,
  no `npx`, no binary fetched. No REA run. No subagent. No git or jj command anywhere.
- Writes: this report only, inside the lane. No carrier, mutant, corpus, tools or
  `.ufo` file other than this report was touched.

Report: .ufo/waves/round-30/w1/ConnSiblingsRust.md
