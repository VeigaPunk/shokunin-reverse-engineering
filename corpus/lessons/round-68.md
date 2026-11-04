# Round 68 — the registry census and the packed route

Base `fcbe200f6739c38939e0dabf3f251de2cc6bd727`; the operative freeze is the commit that first adds
`.ufo/waves/round-68/claims.json` (`1eaf596e5f241762349fbd102c9e09ec1df18e3f`); the instruments, the six
control arms and the base dry runs were committed at `6020eb60`, before the freeze (`claims.json`
§`declaration_pointer`, atom A0). Two claims on distinct axes, causally separable: **R68-C1**
(calibration, capability acquisition) is a conformance census over the lane's own instrument inventory,
repairing the four registry rows the round-67 outside closure routed (its defect 2); **R68-C2**
(coverage, capability acquisition) is the packed-ELF triage route — detect a packer's stub, unpack it,
require the original's bytes, recover the original's REA inventory. Neither verdict is taken here: the
after-arms belong to the L1's data run and the closure belongs to the non-author judge.

## Gate

Access date for the source: **2026-11-03**. Evidence: `.ufo/waves/round-68/w1/ScoutSource/{gate.md,fetch/}`
and the L1's own re-open under `/fast/scratch/hyaku/kaidoku-r68/Source/`.

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) UPX 5.2.0 documentation, `doc/upx-doc.txt` at tag `v5.2.0`, section `NOTES FOR LINUX/ELF386` | https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt, opened 2026-11-03: HTTP 200, 37 208 B, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`; heading at fetched-bytes line 433, quote at lines 441-442, one occurrence in that section; the same sentence is repeated per format (ATARI/TOS 192, DOS/COM 211, DOS/SYS 253, DJGPP2/COFF 287, LINUX/SH386 487, LINUX/386 530, PS1/EXE 594 with `until further notice`), and `--exact` at lines 101-106 bounds identity as work in progress for some formats | "Packed programs will be byte-identical to the original after uncompression." (11 words) — a format-scoped round-trip guarantee for `linux/elf386`, the class both carriers belong to | **admit** (S269, docs, tier A, opened 2026-11-03, recheck 180d, used-by the round-68 entry) | — |
| (b) the same manual in POD form, `doc/upx.pod` at `v5.2.0` (both wave drafts called this row S270; the landed registry carries one row, S269, with the general-Linux passage as a secondary locator) | https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.pod, opened 2026-11-03: HTTP 200, 35 451 B, sha256 `cc93ccea…a1c31c2`; quote at lines 459-460 under `=head2 NOTES FOR LINUX [general]` | "UPX keeps your original program untouched. This means that after decompression you will have a byte-identical version" (17 words) — a general-Linux statement, one step weaker than the ELF386 one | **not a second row**: recorded as a secondary locator inside S269's anchor cell; a row would duplicate the scope | a pod-only rendering (no `doc/upx-doc.txt` at the tag) would make this the row |
| (c) UPX front page | https://upx.github.io/, opened 2026-11-03: HTTP 200, 5 059 B (a seat measured 5 056 B on its own fetch — M68-5), sha256 `f07678bd…d1fa7`; no tag, commit or version anywhere in the bytes; `byte-identical` 0 occurrences | the page names list/test/unpack and an internal checksum, but states no byte identity and names no revision | **reject as this round's row**: a locator with no revision identity, and no statement the identity arm needs | if a claim needed only "unpacking is a documented operation" the page's prose would serve |
| (d) `https://upx.github.io/upx-doc.html` | opened 2026-11-03: HTTP **404**, 9 379 B, sha256 `b6205073…b0368`; body is the GitHub Pages "Page not found" | the URL does not resolve; the manual ships in the repository (`doc/upx-doc.html`, `.txt`, `.pod`, `upx.1`) | **reject**: an unreachable locator is not a source | the page reappears at that path with a versioned body |
| (e) Debian manpages mirror `upx.1` | https://manpages.debian.org/unstable/upx-ucl/upx.1.en.html, opened 2026-11-03: HTTP 200, 61 251 B, sha256 `40e69ca3…fbb8`; page header `upx-ucl 4.2.4-2` | the same 11-word sentence, under **4.2.4**, while the route runs `/usr/bin/upx` 5.2.0 (sha256 `cf2f6e7c…c969`) | **reject**: quoting it attributes a 4.2-era sentence to the 5.2.0 binary the measurement uses | a mirror whose rendered text is versioned to the packer the route pins |
| (f) ManKier mirror | https://www.mankier.com/1/upx, opened 2026-11-03: HTTP 200, 48 794 B, sha256 `ba8b23d7…b06`; `revision`/`commit`/`tag ` 0 occurrences | same text, no revision identity | **reject**: upstream-tip text cannot be tied to the pinned packer | a mirror that prints the upstream tag/commit it renders |

A receipt is not a source either: `l1/pre/c2-dryrun-at-base-frozen.json` shows two carriers whose
unpacked sha256 equals their pins — the *measurement* the identity arm makes — and cannot say why
identity holds or where the guarantee stops. The ground is the format section.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M68-0 | self-assessment/registry (inherited from round 67): the plan named two instruments the registry did not carry, so the lane's own inventory under-reported by exactly the gates it had just run | `l1/pre/c1-at-base.json`: `unregistered` = `tools/round-67/avm-le-counter.py`, `tools/round-67/mutation-battery.py`, `mismatches 2`, `registry_rows 73`; `git show fcbe200f:SKILL.md` rows between the registry markers = 73, none of them round-67 | **PROTOCOL §Gate standard — Registry + Delivery** (a closure grades no gate conformant until its row exists); no in-lane check compared plan text to the table | `tools/round-68/registry-conformance.py` plus the four rows; the before/after is the claim's own counter |
| M68-1 | provenance/revision binding: both base receipts name a moving ref and a null instrument revision, so the before-arm cannot be tied to a commit from its own bytes | `l1/pre/c1-at-base.json` `"rev": "main"`, `instrument.rev: null`; `l1/pre/c2-dryrun-at-base.json` identical in both fields | **PROTOCOL §Gate standard — Two evidences** (a verdict names the revision it measured), reinforced by atom A9 | after-arms run with `--rev <sha>` and record `instrument.rev`; the re-taken base record is `l1/pre/c2-dryrun-at-base-frozen.json` |
| M68-2 | freeze binding: the C2 before receipt was produced by bytes the freeze does not carry | `l1/pre/c2-dryrun-at-base.json` `instrument.sha256` = `7ee286c0…`; the frozen instrument and the file at its only commit `6020eb60` are `48ef4c68…`; `instrument_supersessions` = `[]` | **QUALITY #33** (an instrument change is disclosed with a re-taken before record; an undisclosed change is the finding), read with R68-C2's kill rule | the before record was re-taken with the frozen bytes (`c2-dryrun-at-base-frozen.json`, `instrument.sha256 48ef4c68…`, `instrument.rev 6020eb60`, measured `fcbe200f`); the draft receipt stays committed and is disclosed here and in the report |
| M68-3 | declaration vs delivery: two plans name six instruments each that never existed, and nothing read plan text against the tree until this round's census | `l1/pre/c1-at-base.json` `named_but_absent` = 12 paths: `tools/round-51/{c1-controls,c1-counter,c1-run,fetch-vendor,misroot-sweep,sqfs-triage-v6}` and the same six under `round-52`; `git ls-tree -r --name-only fcbe200f -- tools/round-52` is empty | **PROTOCOL §Evidence standard** (every evidence pointer resolves) | the census reports the set on every run; the two plans stay as filed (they are historical), the finding is named, not repaired |
| M68-4 | scope/over-generalisation of a documented guarantee: the route asserts identity per carrier while the manual grants it per format and only for the default packing mode; the carrier records name neither | `tools/round-68/packed-elf.py` packs with `upx --best` (no `--exact`); `identity_ok` is bare sha equality; the carrier records carry no `format` key; S269's own `--exact` caveat | **QUALITY #107** (a rule generalised from one carrier family names the family and the class it cannot see) | the entry's Limits section states UPX 5.2.0 / `linux/elf386` / default packing only; a carrier record that names format and mode is routed to the next freeze |
| M68-5 | measurement slip in a rejected candidate: two seats fetched the same front page and reported 5 059 B and 5 056 B | `w1/ScoutSource/gate.md` (5 056) vs `w1/ScribeLesson/gate-fetch.json` and the L1's fetch (5 059 each, sha256 equal) | **QUALITY #21** (a count carries the command that produced it) | the row is rejected, so no verdict depends on the count; the mismatch is recorded rather than smoothed |
| M68-6 | gate strength: all five packed-route mutants survive `--selftest` **and** a real green run; only a modelled false-input scenario distinguishes them | `w1/MutPacked/mutants.md` (M1 `identity_ok ≡ True`, M2 recovery self-compare, M3 detection without the section clause, M4 before-arm self-compare, M5 control dropped from `fold`; each 13/13 selftest green, real route green, killed only by `S1`–`S5`) | **QUALITY #108** (a survivor is closed only by a case that feeds the mutated function a false input) | routed: the next freeze adds arm-false cases to `packed-elf.py`'s selftest; the frozen instrument is not edited post-freeze |
| M68-7 | scope self-exclusion: the lane's control driver is itself an unregistered instrument | `controls.py` is named by no plan, so the census regime cannot see it (`scope_size 71`) | atom A5 declares the four-row repair surface | declared in the report; a later regime that counts control drivers would reopen the scope |
| M68-8 | registry row vs code: two cells described behaviour the instrument does not implement | `w1/ReviewerGates/review.md` ADV-2 (the packer pin is recorded, never enforced) and ADV-3 (a missing `node` or a bad `--work` raises a traceback and exit 1, not the promised 2) | **QUALITY #21** (a retention statement is admitted only with a command that prints the keys) | the two SKILL rows were corrected at landing to say "recorded, not enforced" and to name the exit-1 edge; the code change is routed to the next freeze |
| M68-9 | predicate scope: the frozen R68-C1 predicate binds a cardinality (`scope_size 71`), not a membership, and `scope_size` counts plan text the round may edit, so a net-zero edit reaches the triple with one repair row deleted and its instrument out of scope | `w1/CriticClaims/attack.md` §1b fixture: dropping the `avm-le-counter.py` citation, citing `controls.py` in round 68's plan, deleting the row and adding a `controls.py` row reports `mismatches 0, scope_size 71, registry_rows 77, ok true` with `avm_row_present false`; the control (row deleted, no compensating edit) reports `mismatches 1` | **QUALITY #111** (a declared inventory is not its own population) read as a membership rule: a count over a population is not a check on the population | membership verified post-freeze from the frozen module's own extractor (`l1/scores/c1-scope-membership.json`: base ∪ the two round-68 instruments, no drops, all four repair rows present); a `c1-scope-shrink` control and a receipt that emits the sorted scope list are routed to the next freeze |
| M68-10 | scope: a seat wrote a fixture receipt into the instrument's own directory instead of its wave directory | `tools/round-68/registry-conformance.receipt.json` (22:44, `rev main`, `mismatches 1`, `duplicate_rows [tools/round-67/reg.py]` — a MutRegistry duplicate fixture), untracked at the pre-file check | the pre-file gate's tree-clean step (`tools/round-29/prefile-check.sh` step 1); the wave context named the seat's own directory | moved byte-for-byte to `w1/MutRegistry/receipts/stray-lane-root-duplicate-fixture.receipt.json` under the round's entry, and the tree-clean step then passed |

## Outcome

- **R68-C1 — measured, both arms.** Base `fcbe200f`: `mismatches 2`, `scope_size 69`, `registry_rows 73`,
  unregistered = the two round-67 instruments (`l1/pre/c1-at-base.json`, exit 1). With this round's plan
  in the tree and before the rows: `mismatches 4`, `scope_size 71` (`w1/ExecRegistry/own-freeze.json`,
  an independent extractor). After the four rows land: `mismatches 0`, `scope_size 71`,
  `registry_rows 77` (`l1/scores/c1-at-landing.json`, exit 0), and membership independently verified
  (`l1/scores/c1-scope-membership.json`: base ∪ the two round-68 instruments, no drops, the four rows present). `legacy_unregistered` 26 (rounds 35-40,
  out of regime) and `named_but_absent` 12 are reported on every run.
- **R68-C2 — measured.** `carriers_matched 2` of 2, `control_ok true`, every arm true on both carriers,
  `before_procedures [3, 3]`, unpacked sha256 equal to the pins, originals neither listed nor
  decompressible (`l1/scores/c2-at-landing.json`, exit 0). A third carrier (`/usr/bin/gzip`, 230/31/235)
  reproduced every arm in the wave (`w1/ExecPacked/probe.json`), which is a generalisation probe, not
  claim input.
- **Wave.** `r68-w1`, 13 seats (4 executor, 1 reviewer, 1 critic, 2 mutation-testers, 1 sentinel,
  1 scout, 1 connector, 2 scribes), attack share 4/13. Seats settle per `r68-w1-results.json`; the
  critter's output is recorded in the report's seat table.
- **Outside closure — pending.** This lesson does not self-certify either verdict; the Gate admits and
  rejects above are the closure's to re-open.

## Census

Round start (base `fcbe200f`, recorded 2026-11-03T22:40Z): `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku` exit 0, 175 rows, the 19 standing W04 (`l1/census-start.txt`).
Round end: 176 rows after S269, malformed rows 0, the same 19 W04 (`l1/census-end.txt`).
