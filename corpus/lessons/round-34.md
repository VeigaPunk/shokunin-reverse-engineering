# Round 34 — public ELF version-needs depth

Base: `ec3125ad3d130d92f888a4128dfaa2982f36fff7`. One claim, R34-C1 / depth, on native ELF ground already held. No coverage widening or new REA capability is claimed. Coverage/depth/calibration are tied at 10 in the base SCORECARD, none retired; depth is a lowest axis. Outside round 33: rejected-honest-stop (`round-33-verifier-spotcheck.md`), acknowledged in LOG before this round's measurement.

## Claim and order

P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.

Target: 12 matched carriers, with each carrier matching both schedules and all document checks true. This is the same sentence used in the counter and the frozen plan. Independently authored expected records come from GNU readelf, not the proposed parser. The L1-authored counter's second schedule permutes printable string-table names on private never-executed copies, retaining lengths, offsets and raw recorded hash fields. Those copies are metadata-decoding challenges, not claimed loader-valid executables. Original public carrier copies remain byte-exact. No production reader scoring occurs before control receipts land. The held round-33 builder task is not reconstructed.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M34-1 | false unchanged-file statement | `round-33-verifier-spotcheck.md:27-29`: round-33 report:8 says SKILL unchanged, retained per-file diff is `72 0` | QUALITY 18 did not require per-file unchanged evidence | Appended LOG/report correction; new QUALITY 65 uses that real contradictory diff as its red case. SKILL gained its CHPE table and registry. PROVINCE's empty diff remains supported. Filed report unchanged. |
| M34-2 | vacuous freeze cleanliness | `round-33-verifier-spotcheck.md:129-135`; `.ufo/waves/round-34/prep/R34FreezeSchema-files/receipts/receipt.json` | QUALITY 33/55/61 lacked claims-map schema validation | Successor rejects seven old false-CLEAN maps with exit 3; outer selftest asserts exit and schema finding. Historical no-map claims remain unevaluable, not repaired or credited. |
| M34-3 | historical pin chain without forward pointer | `round-33-verifier-spotcheck.md:137`; `.ufo/waves/round-33/prep/R33ChpeParser-independent.json` | QUALITY 18 | Appended JSON correction links directly to `text-checker-supersession.json`, preserves old digest, and names the normalization-only successor and its landed commit. No carrier claim is inferred. |

## Gate

Opened-source candidates: S103 LSB 5.0.0 symbol-version requirement layout; S104 pinned glibc 2.42 integer/width/structure definitions; S105 System V gABI draft for GNU-specific record authority. The latter is a real reject, not an intentionally malformed invented source.

- **S103 admitted, scope bounded.** URL `https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html`, accessed 2026-10-23. Capture `.ufo/waves/round-34/prep/R34SourceNovelty-files/lsb-symversion.html`, SHA-256 `982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91`, §10.7.4, line 717: “Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered.” (21 words.) The page supplies the layout/meaning, not numeric section constants or observed host loader behavior.
- **S104 admitted, scope bounded.** URL `https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h`, accessed 2026-10-23. Capture `R34SourceNovelty-files/glibc-elf.h` under the same prep directory, SHA-256 `fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f`; lines 1124–1133 and 1153–1161 define the two structures; line 459 quote: “Version needs section.” (3 words, contiguous code comment.) `Elf64_Half`/`Word` are uint16/uint32 at lines 28/33. Its `vna_other /* Unused */` comment is not adopted as the field meaning; S103 line 937 defines the version index.
- **S105 rejected for GNU version-needs authority.** URL `https://www.sco.com/developers/gabi/latest/contents.html`, accessed 2026-10-23. Capture `R34SourceNovelty-files/gabi-contents.html`, SHA-256 `860a69166779d1c2264867df76c750e21af9f9f185fd451659be64e794da18b0`, line 3: “System V Application Binary Interface - DRAFT - 10 June 2013” (11 words). The bounded sweep over this contents file plus opened section-header, symbol-table and dynamic chapters finds zero `verneed`, `vernaux`, `gnu.version`, `symbol version`, `SHT_GNU` hits (`prep/R34SourceNovelty.md:70-76`, captured files). Generic symbol-table/dynamic definitions do not define the GNU requirement records. **Flip:** an opened chapter/revision explicitly defines Verneed/Vernaux or `.gnu.version_r`. Unfetched chapters are not an absence claim.

New rows only: no existing source status/recheck/used-by cell is changed. S103/S104 are mined by the new knowledge entry; S105 remains rejected and is used by this lesson. Search log and independent source reopens are round evidence, not evidence of runtime behavior. Current outside non-author admit/reject spot-check is pending; lane-dispatched reviewers are not outside verifiers.

## Routed limits and exclusions

R33-C1 remains unprovable. `R33FixtureBuilder` output and derivatives and `U064N008Hf47eb933` remain held, untouched and excluded. New work uses public existing host binaries and a static metadata decoder, not exploit-shaped or malware-shaped binary authoring.

The old CHPE count-limit `>`→`>=` mutant survives the existing 107-case selftest. The round-34 bounded private replay now kills the metadata-span mutation (four mismatches), resolving the old EAGAIN inconclusive result, while tag detection still rests only on JSONDecodeError. Evidence: `prep/R34ParserBounds.md` and `R34ParserBounds-files/`. None of these instruments is used for R34-C1 admission. The old disk-command scanner remains lexical, with cwd/alias/variable/relative-path blind spots; a clean scan is not non-execution proof.

The five r32 wrapper survivors and archived `pe_own_compare`, `verify_quotes`, `independent-pe` secondary selftest defects remain excluded unless a separately retained successor demonstrates a specific repair. No historical frozen instrument or historical claim verdict is rewritten.

R34LegacyGaps adds isolated successor demonstrations, not historical repairs: four C1 acceptance-wrapper mutants are killed by source-independent text/JSON boundary cases (20-case successor selftest); quote-support successor has 9 cases and two kills; the archived independent comparator has a 31-check one-carrier text/JSON red/green replay. The original frozen wrapper remains unchanged; source/id checks remain lexical, Git acquisition/same-second ordering is unexercised, C2v3 is banned, `pe_own_compare` remains unrun, and archived quote identity/drift rows remain uncovered. Evidence: `.ufo/waves/round-34/prep/R34LegacyGaps-files/run-receipt.json`, 19 checks passed and 1 explicitly not run. None is R34-C1 admission evidence.

Before the freeze, one static public carrier (`e12`, `/usr/bin/sln`) was selected with no requirement/string table. Its second schedule is the same empty-record control, not a fabricated string table; the other eleven receive the counter's unpredictable nonidentity ASCII renaming. The final predicate explicitly says “wherever requirements are present.” No production counter or reader scored the twelve-row target before this prospective wording was fixed. Development-reader binaries are digest-disjoint from the twelve originals (`R34Expected-files/selection.json`).

## Containment and scope

No carrier is executed. This is an instruction and static code property, not a universal OS-enforced no-execution claim. Targets are mode 0644 copies. No runtime loader acceptance, function behavior, dependency authenticity, version satisfiability, exploitability or security verdict is inferred from metadata. Source trees, sibling lanes and operator configuration are read-only. The L1 alone writes lane VCS through the jj helper. Tool installs are recorded separately; none is assumed. The round's stale-lane state is one active steered round only, never another kaidoku mission.
