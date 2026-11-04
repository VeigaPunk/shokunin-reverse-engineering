# Round 68 — the registry census and the packed route

Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; the operative freeze is the commit that first adds
`.ufo/waves/round-68/claims.json` (`1eaf596e5f241762349fbd102c9e09ec1df18e3f`); the instruments, the
six control arms and the base dry runs were committed at `6020eb60`, before the freeze
(`claims.json` §`declaration_pointer`, atom A0). Two claims on distinct axes, causally separable:
**R68-C1** (calibration, capability acquisition) is a conformance census over the lane's own
instrument inventory, repairing the four registry rows the round-67 outside closure routed (its
defect 2); **R68-C2** (coverage, capability acquisition) is the packed-ELF triage route — detect a
packer's stub, unpack it, require the original's bytes, recover the original's REA inventory. Neither
verdict is taken here: the after-arms belong to the L1's data run and the closure belongs to the
non-author judge. This lesson records what the round's own artifacts show, what the round's source
work admits and refuses, and the defects the wave found in those artifacts.

## Gate

Access date for every source below: **2026-11-03**. The round's source work is
`.ufo/waves/round-68/w1/ScoutSource/gate.md` plus the row it drafted (`row.S270.md`). The base blob
carries no `S269` (`git show fcbe200f…:corpus/SOURCES.md | grep -c '^| S269'` = 0): both rows are
this round's, S269 for the manual's `NOTES FOR LINUX [general]` sentence in `doc/upx.pod` (in the
working tree at this reading, `git diff corpus/SOURCES.md` = 1 insertion) and S270 for the ELF386
sentence, drafted. This seat re-opened the same pages independently — receipt
`.ufo/waves/round-68/w1/ScribeLesson/gate-fetch.json`, fetched copies beside it — and the fetched
bytes are identical (same sha256) on every candidate both seats opened: the front page is
`f07678bd…1fa7` (this seat measures 5 059 B, ScoutSource's table states 5 056 B — M68-5), the
manual URL is a `404` of `9 379 B` / `b6205073…0368`, and the ELF386 sentence is unchanged at tag
`v5.3.0` (`39 224 B`, `9b980dca…d3c35`, line 484) from the tag the row pins. The row is **S270**;
no source id is asserted by this seat beyond the one the gate names.

| # | candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|---|
| (a) | **S270** — UPX 5.2.0 manual, `doc/upx-doc.txt` at tag `v5.2.0` (commit `034b6d0d81c53998c07ad6f34bfead6f5c5445ce`), section `NOTES FOR LINUX/ELF386` | https://raw.githubusercontent.com/upx/upx/034b6d0d81c53998c07ad6f34bfead6f5c5445ce/doc/upx-doc.txt — HTTP 200, 37 208 B, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (identical on ScoutSource's second fetch); quote at fetched-bytes lines 441-442, heading at 433, byte offset 18 963. Independently re-measured by this seat at tag `v5.3.0`: 39 224 B, sha256 `9b980dca…d3c35`, the same sentence at line 484 | "Packed programs will be byte-identical to the original after uncompression." (11 words) — a **format-scoped** round-trip guarantee for the one format both R68-C2 carriers are (Linux ELF), distinct from S269's `NOTES FOR LINUX [general]` sentence in `doc/upx.pod` | **admit**, as the row grounding R68-C2's identity arm — scoped to the ELF family, with the manual's own limits quoted in the row's anchor: `--exact` "is work in progress and is not supported for all formats yet" (v5.3.0 lines 101-106) and the PE section's "result may not be byte-identical" (v5.3.0 lines 759-764) | a carrier whose format section carries a qualifier the ELF386 section does not (the PS1/EXE section's "until further notice", v5.2.0 line 595; the WIN32/PE carve-out) or a packing mode other than the documented default (`--exact`) flips the row: the ELF386 sentence is then not the statement about that carrier, and the format's own section must be quoted |
| (b) | UPX front page — https://upx.github.io/ | HTTP 200, 5 059 B, sha256 `f07678bd16df1e713cac0c04bd2eb0b3d2accfb98c589f6f63911d6f32ad1fa7`; no tag, commit or version anywhere in the bytes; `byte-identical` 0 occurrences, `checksum` 1 (the "safe" bullet: "you can list, test and unpack your executables. Also, a checksum of both the compressed and uncompressed file is maintained internally") | a landing page states the operations (list, test, unpack) and an internal checksum; it states **no** byte identity and names **no** revision | **reject as a rule source**: a locator with no revision identity, and no statement that grounding identity requires | if the claim needed only "unpacking is a documented operation", the page's prose would serve — and the revisioned manual serves that better |
| (c) | the manual page the project's own site implies — https://upx.github.io/upx-doc.html | HTTP **404**, 9 379 B, sha256 `b620507312c5e97566a3c6cfaf99144fefc18a0da7d941401dfa0f5f58fb0368`; body is the GitHub Pages "Page not found" | the URL does not resolve; the manual ships in the repository (`doc/upx-doc.html`, `.txt`, `.pod`, `upx.1`), not from the project site | **reject**: an unreachable locator is not a source | the page reappears at that path with a versioned body |
| (d) | Debian manpages mirror — https://manpages.debian.org/unstable/upx-ucl/upx.1.en.html | HTTP 200, 61 251 B, sha256 `40e69ca3…fbb8`; renders the same 11-word sentence; page header `upx(1) — upx-ucl — Debian unstable`, package `upx-ucl 4.2.4-2`, synopsis `upx 4.2.4` | the sentence exists, but under **4.2.4**, while the route runs `/usr/bin/upx` = `upx 5.2.0` (sha256 `cf2f6e7c…c969`, recorded in the base receipt's `packer` block) | **reject**: quoting it attributes a 4.2-era sentence to the 5.2.0 binary the measurement uses | a mirror whose rendered text is versioned to the packer the route pins |
| (e) | ManKier mirror — https://www.mankier.com/1/upx | HTTP 200, 48 794 B, sha256 `ba8b23d7…b06`; same sentence; `revision` 0, `commit` 0, `tag ` 0 occurrences | same text as (a) under a locator that names no revision | **reject**: upstream-tip text cannot be tied to the pinned packer | a mirror that prints the upstream tag/commit it renders |

A receipt is not a source either: `l1/pre/c2-dryrun-at-base.json` shows two carriers whose unpacked
sha256 equals their pins, which is the *measurement* the identity arm makes; it cannot say why
identity holds or where the guarantee stops. The row's ground is the format section, not the run.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M68-0 | self-assessment/registry (inherited; the round-67 outside closure's defect 4): the plan named two instruments the registry did not carry, so the lane's own inventory under-reported by exactly the gates it had just run | `.ufo/waves/round-68/l1/pre/c1-at-base.json`: `unregistered` = `tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`, `mismatches 2`, `registry_rows 73`, `registry_paths 73`; `git show fcbe200f:SKILL.md`, rows between the two instrument-registry v2 markers = 73 (independently re-counted by this seat), none of them round-67 | **PROTOCOL §Gate standard — Registry + Delivery** ("closure grades no gate conformant until its registry row exists at the lane's *registry home*"). No in-lane check compared plan text to the table; the criterion was applied from outside, by the round-67 closure §1 defect 4 | the four rows (the two round-67 instruments and this round's two counters) plus R68-C1 itself, so the comparison is machine-checked instead of remembered; the rows were in the working tree at this reading (`git diff SKILL.md` = 4 insertions), so the repair is only real once committed and measured at that commit |
| M68-1 | provenance/revision binding: both base receipts name a moving ref and a null instrument revision, so the before-arm cannot be tied to a commit from its own bytes | `l1/pre/c1-at-base.json` `"rev": "main"` (line 56) and `instrument.rev: null` (line 6); `l1/pre/c2-dryrun-at-base.json` identical in both fields | **PROTOCOL §Gate standard — Two evidences** ("A verdict names the revision it was measured against … a run over a moving worktree is not comparable to one over the cited commit"), reinforced by atom A9, which was written to close the round-67 closure's routed defect 6 | run with `--rev <sha>` at the measured revision and record `instrument.rev` as the commit that bears the instrument; the after receipts are the ones that must carry both, and this is a condition on them, not a claim |
| M68-2 | freeze binding: the C2 before receipt was produced by bytes the freeze does not carry | `l1/pre/c2-dryrun-at-base.json` `instrument.sha256` = `7ee286c03391dc464c90a3f24498258bfef09dd89300aa9a246fd35ac85ef25c`; the frozen instrument and the file at its only commit (`6020eb60`) are `48ef4c68…5276e` (`git show 6020eb60:tools/round-68/packed-elf.py` piped to `sha256sum`); the token `7ee286c0` appears nowhere else in the wave; `instrument_supersessions` = `[]` | **QUALITY #33** (an instrument change is disclosed as an appended supersession with a re-taken before record; an undisclosed change is the finding), read with R68-C2's kill rule ("an undisclosed post-freeze instrument edit") | re-take the before record with the frozen bytes, or append a disclosed supersession naming `7ee286c0…`, the reason and the re-taken record; the after receipt must name `48ef4c68…` |
| M68-3 | declaration vs delivery: two plans name six instruments each that never existed, and nothing read plan text against the tree until this round's census | `l1/pre/c1-at-base.json` `named_but_absent` = 12 paths: `tools/round-51/{c1-controls,c1-counter,c1-run,fetch-vendor,misroot-sweep,sqfs-triage-v6}` and the same six under `round-52`; `git ls-tree -r --name-only fcbe200f -- tools/round-52` = 0 files, and `tools/round-51` holds only `census3.py`/`census3.json`; the names are in `plans/round-51-claims.md:68-71,193,247` and `plans/round-52-claims.md:72-73,199,253` | **PROTOCOL §Evidence standard** ("Everywhere the protocol says *evidence*, it means a resolvable pointer: a repo path, a command and its output, a commit, or an external document") read with the plans' own registry clause (`plans/round-51-claims.md:171`: every new `.py`/`.sh` under `tools/round-51/` gets exactly one row) — a path that never resolves is not a pointer, and the clause that would have noticed was never enforced | the census reports the set and excludes it from scope (A4); the durable repair is a named erratum on each plan (or landing the tools), and the set must keep being reported rather than silently dropped. Cause is **unknown** here: no round-51/52 report was opened, so this lesson does not assert why the tools were never committed |
| M68-4 | scope/over-generalisation of a documented guarantee: the route asserts identity for every carrier, while the manual grants it per format and only for the default packing mode; the route records neither the format nor the packing mode | `tools/round-68/packed-elf.py:242` packs with `[UPX, "--best", "-q", "-o", packed, orig]` — no `--exact`; `identity_ok` is a bare sha equality (`:257-258`); the carrier records in `c2-dryrun-at-base.json` carry `arms, before_floor, control, id, ok, orig_counts, packed_counts, packed_sha256, pin, refusal, runs` — no `format` key; the manual's caveats are S270's own: `--exact` WIP (v5.3.0 101-106), WIN32/PE "may not be byte-identical" (759-764) | **QUALITY #107** ("a rule generalised from one carrier family names the family and the class it cannot see") and §Gate standard §Scope's rule that a source is used at its own scope; the reviewer's criterion is the same one M67-0 earned | record each carrier's executable format (the REA `analyze` envelope already emits `"format":"elf"`) and whether the pack used `--exact`; state in the route's docstring and the row's anchor that identity is asserted for the ELF family under default packing, so a PE carrier is a could-not-evaluate or an `--exact` run, never a silent failure |
| M68-5 | numeric claim vs its own artifact: the scout table gives the front page as `5 056` bytes while the committed copy is `5 059` bytes (the sha256 in the same row is the hash of the 5 059-byte file, so the size alone is wrong) | `.ufo/waves/round-68/w1/ScoutSource/gate.md` candidate a1, column `bytes`, vs `ls -l .ufo/waves/round-68/w1/ScoutSource/fetch/upx-github-io.html` = 5 059 and this seat's independent fetch (`gate-fetch.json`, `size_download` 5 059) | **PROTOCOL §Evidence standard** ("A numeric claim carries its counting command") — a size typed beside a sha that was computed, not counted | the size is corrected in the lesson's Gate row (5 059 B) and the Gate row carries the sha, which is the checkable value; the closure should re-measure sizes from the committed bytes rather than trust a copied number |

## Outcome

Every line below is the L1's to fill from the after-run receipts; none is asserted here.

- [L1] **R68-C1 — after.** `python3 -I -B tools/round-68/registry-conformance.py --root <lane>
  --rev <sha> --json-out <receipt>` at the measured revision: `mismatches 0`, `scope_size 71`,
  `registry_rows 77`, exit 0, receipt naming both `rev` and `instrument.rev`.
- [L1] **R68-C1 — before and controls.** The base arm (`l1/pre/c1-at-base.json`) reports
  `mismatches 2` naming exactly `tools/round-67/avm-le-counter.py` and
  `tools/round-67/mutation-battery.py`, with `scope_size 69`, `registry_rows 73`,
  `legacy_unregistered 26`, `named_but_absent 12`; the two false-green arms
  (`c1-shortcut-self` 0/72, `c1-constant-zero` 0) stay green as controls
  (`l1/pre/controls-at-base.json`, 6 arms, `ok true`).
- [L1] **R68-C2 — after.** `packed-elf.py --pkg <rea-agents> --work <scratch>` over the two pinned
  carriers: `carriers_matched 2` of `target 2`, `control_ok true`, `failing []`, exit 0,
  `before_procedures [3, 3]`, and `instrument.sha256 48ef4c68…5276e`; per carrier every arm true
  (`detected`, `before_ok`, `identity_ok`, `recovery_ok`, and `refusal_ok` on the carrier that pins
  an address), the unpacked inventory equal to the original's (`167/30/190` on jq, `99/29/103` on
  xxd, per A2), and the non-packed original neither listed (`upx -l` nonzero) nor decompressible
  (`upx -d` nonzero) — jq's base dry-run `control {list_rc 2, decompress_rc 2}` is the shape, and
  xxd carries no refusal arm (`refusal: null`, no `refusal_ok`), which is the predicate's
  "on the carrier that pins an address".
- [L1] **Arithmetic the after-arm must land on (inference, not a measurement).** Scope grows by the
  two round-68 tools the plan's counting commands name (`69 + 2 = 71`); registry rows grow by the
  four repairs (`73 + 4 = 77`). The plan does not name `tools/round-68/controls.py` in a counting
  command, so the control driver is outside the census's regime; if the after run reports 72 the
  premise of the predicate, not the census, is wrong.
- [L1] **Freeze integrity, disclosed.** `instrument_supersessions` is empty at the freeze; any later
  edit to either instrument is a disclosed supersession with a re-taken before record (QUALITY #33),
  and every after receipt names the instrument sha it ran (M68-2 is the reason this line is not
  optional).
- [L1] **Wave.** `r68-w1`, 13 seats (policy band 8–16; attack seats: 1 reviewer, 1 critic, 2
  mutation-testers = 4 of 13), settled/dead counts from `l1/records/r68-wave-status.json`, every
  seat with a report.
- [L1] **Repairs carried.** The round-67 entry's correction block is **appended but uncommitted** at
  this reading: the entry's bytes at `2dd5f2cd`, `fcbe200f`, `6020eb60`, `1eaf596e` and `6ffa9ce1`
  contain no `round 68 (appended` line (`grep -c` = 0 at each), while the working tree carries the
  `## Correction — 2026-11-03, round 68` block citing `b55d5e87…` superseded and `e66ba022…` actual.
  Same state for the four registry rows (`git diff SKILL.md` = 4 insertions), S269 in
  `corpus/SOURCES.md` (1 insertion) and the new `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`
  (untracked). Every one of these must be committed before the after-arm, because both counters read
  their subjects at `--rev`; the base arm stays valid precisely because the base blob is unchanged.
  The QUALITY #100 companion row, the prefile receipt, the retired `corpus/claim-freezes.tsv` and the
  round-67 report's prompt-hash erratum are the L1's to confirm.
- [L1] **Trend and admission.** Not asserted here: the lesson records behaviour, not a verdict.

## Census

Round start (base `fcbe200f…`, recorded 2026-11-03): `.ufo/waves/round-68/l1/census-start.txt` —
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` **exit 0**, **19 standing
W04** duplicate-URL warnings, `ok` on
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, and no count line (the file's
last line is `exit=0`). The population the start file does not print, re-counted by this seat from
the base blob (`git show fcbe200f…:corpus/SOURCES.md`, 11-column rows split on `|`): **175 rows**,
tier `A=161 B=9 C=5`, status `mined=166 rejected=9`, malformed rows **0** — the same 175 the round-67
census ended on, i.e. no source row has been added since. The registry side at the same revision:
**73 rows** between the two instrument-registry v2 markers (`git show fcbe200f…:SKILL.md`), matching
the base receipt's `registry_rows 73`.

Round end [L1]: at this reading two source rows are in flight for one manual — S269 for the general
section (working tree, 1 insertion into `corpus/SOURCES.md`) and S270 for the ELF386 sentence
(drafted) — and the plan's frontier step named one. The start is **175 rows**, so the end is 176 if
one lands and 177 if both do; the end value is the L1's to read from the census, not this lesson's to
predict. What the lesson can say is that the start's 19 W04 are named debt, not a clean bill, and
that the row count at both ends is a measurement with a counting command (`SOURCES.md` 11-column
rows), not a remembered number.
