# Round 69 — the route's gate can fail, its contract is typed, and a shared object joins the carriers

Lane `kaidoku`, round 69, attempt 1. Base `d7d9a62cc70935304e600ed0dee864fc4f1751f7`; operative freeze
`f15998102f1ce3569e61faa2ac6f286bc414538e` (the commit that first adds
`.ufo/waves/round-69/claims.json`, re-derived with `git log --diff-filter=A --format=%H -1 -- …`).
Three claims on three axes, all capability acquisitions: **R69-C1** calibration (the five 2026-11-03
mutation survivors killed by the instrument's own selftest through the `evaluate_carrier()` arm seam),
**R69-C2** operability (typed exit-2 contract, enforced UPX pin, per-carrier format/mode records),
**R69-C3** coverage (a pinned packed shared object, `/usr/lib/libz.so.1.3.2`, beside the two
executables). Declaration `plans/round-69-claims.md`; container `.ufo/waves/round-69/claims.json`.
The predicates are judged as frozen; nothing here narrows, widens or re-freezes one, and **no verdict
is taken** — `.ufo/waves/round-69/l1/scores/` held no receipt when this draft was written (measured
`ls`, 2026-11-04T02:37Z), so every after value is an `[L1]` placeholder. The C1 before-arm and the C2/C3
before-arms are committed and are cited below as measured, not re-run.

## Gate

Access date **2026-11-03** (-03; re-opened by this seat at 2026-11-04T02:41Z). S270 was staged in the
working tree (`corpus/SOURCES.md` `M`, +2 lines, 23:37:20) but is **not committed** at this writing; the
source bytes below are the live ones, fetched by this seat. The ScoutSource seat had produced no
`sources.md` when this draft was written (`.ufo/waves/round-69/w1/ScoutSource/` empty), so these rows
are this seat's own opens.

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) UPX 5.2.0 generated manual page, `doc/upx.1` at tag `v5.2.0` (S270) | https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx.1, opened 2026-11-03: HTTP 200, **40 077 B**, sha256 `09552b3cf4e9073c288060b8f50ed1c1dde3dca89dcaf1230367b6c3e15d4e25`; fetched-bytes line 164 is `\&\fB\-\-version\fR: print the version of \fBUPX\fR`, i.e. the rendered **`--version: print the version of UPX`** (6 words, `printf '%s' … \| wc -w`); the internal-checksum sentence at lines 112-114 | the tag's own bytes pin the packer's documented identity probe and its internal-checksum statement — the surface A3 compares `packer.version` against and the surface A4/A6 pin by hash; **the quote is a roff-rendered reading, not a byte-literal substring** (`grep -c 'print the version of UPX' doc/upx.1` = 0 because of `\fB`/`\-` escapes) | **admit** (S270, kind `docs`, tier A at the pinned tag; scope = identity probe + checksum statement, never a byte-identity guarantee) | the bytes at the tag change, the quote line moves, or the registry requires byte-literal quotes — then the literal locator is (b)'s line 99, same 6 words |
| (b) the same manual in plain text, `doc/upx-doc.txt` at the same tag (S269's URL) | https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt, opened 2026-11-03: HTTP 200, **37 208 B**, sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` (equal to S269's pin); `    --version: print the version of UPX` at fetched line 99, byte offset 3 653, **6 words**, one occurrence | the same sentence, same tag, byte-literal this time; a new row would duplicate S269's URL and S270's scope while adding no claim | **not a row**: recorded here as a secondary locator inside S270's anchor cell (the round-68 pod/TXT precedent) | S269 is ever split by scope, or a row must quote literal bytes without roff escapes |
| (c) GitHub release page at the tag | https://github.com/upx/upx/releases/tag/v5.2.0, opened 2026-11-03: HTTP 200, **162 743 B**, sha256 `d9770b01652949f0fcf667d985767d1b0f7fbff9847c66342e2c10454296fad1`; the working-tree lesson draft records the same URL as **162 744 B**, sha256 `53033ceb745eb2ab…` (its own fetch); `grep -c 'print the version'` = **0**; the page names `UPX 5.2.0` and links `upx-5.2.0-*.tar.xz` | a release page announces the release and hosts assets; it states no CLI flag contract, and two fetches of the same URL returned different byte counts and digests, so it cannot anchor a row whose evidence is a sha256 | **reject as this round's row** (tier-C lead at most); the two-fetch divergence is itself the disproof of byte identity | the release body quotes the OPTIONS paragraph (`--version`/`--exact`) and the page's bytes are stable across two fetches |
| (d) Arch manual pages mirror `upx(1)` | https://man.archlinux.org/man/upx.1.en, opened 2026-11-03: HTTP 200, **47 791 B**, sha256 `aed1c12a62e54bbe04f718e9184b3c912dbf254fc98233771809e8536143ea04`; renders `upx 5.2.0` once and `print the version` once | the version matches the pin, but the page is bound to the Arch package build, not to the upstream tag: its bytes are re-rendered per site build and may carry distro patches; it names no upstream commit | **reject**: revision identity is a package version, not a source revision, and the bytes are not the upstream artifact | a mirror that prints the upstream tag and commit it renders, or that serves the tag's own bytes |

A receipt is not a source here either: `l1/pre/c2-at-base.json` prints the host packer's version and
sha256 (`upx 5.2.0`, `cf2f6e7c…`) but cannot say why a version string identifies a build. The ground is
the packer's own documented probe, and the byte-level identity is the sha256 pin, not the string.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M69-1 | gate strength — a survivor is closed only by a case that feeds the mutated function a false input (**the round-68 M68-6 class**) | `l1/pre/c1-at-base.json`: all five mutants `verdict "survived"`, `cases 13`, `failed []`, `expect_case null`, `rc 0`, `pristine.cases 13`; the round-68 wave showed the same five green on a real run (`corpus/lessons/round-68.md` M68-6, `.ufo/waves/round-68/w1/MutPacked/mutants.md`) | QUALITY #108, routed at round 68 | `evaluate_carrier()` is a pure function of one model dict (`tools/round-69/packed-elf.py:155-173`) and production calls it (`:414-427`); `_model()` (`:464-478`) plus five `arm-pack-*-false` cases (`:516-529`) each override exactly the arm's field and assert both `arms[arm] is False` and `ok is False`; `REGISTERED_CASES` counts 20 and `case-inventory` (`:541-542`) asserts the executed name list. The battery's r69 patch set binds each mutant to its declared case (`mutation-check.py:56-72,145-150`). After-arm: `[L1]` |
| M69-2 | scope — a rule generalised from one carrier family must name the family and the class it cannot see (**the round-68 M68-4 class**) | `.ufo/waves/round-68/l1/scores/c2-at-landing.json` carrier keys measured: `arms, before_floor, control, id, ok, orig_counts, packed_counts, packed_sha256, pin, refusal, runs, section_count, source, unpacked_counts, upx_list_rc` — no `kind`, no `format`, no `packing_mode`, no `name`; `l1/pre/c2-at-base.json` A5: `jq: missing ['name','format','packing_mode']`, `xxd: …`; `l1/pre/c3-at-base.json`: `"kinds": [null]` | QUALITY #107, routed at round 68 | `CARRIERS` declares `kind` per carrier and `before_max_procedures` per class (`:69-85`); the receipt writes `name`, `kind`, `format`, `packing_mode` (`:417,432`) and `before_ceiling_ratio = ceiling/original` (`:436-438`); the route's own limit is x86-64 ELF under UPX 5.2.0 default packing — packed static binaries and every non-ELF class stay Frontier (`PROVINCE.md` round-69 frontier note, working tree) |
| M69-3 | provenance — a receipt is not a receipt unless its declared consumer can parse it | the filed bytes (`git show HEAD:…`) start `+ /usr/bin/python3 -I -B tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-68/l1/scores/c2-at-landing.json`, so `json.load` raises `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`; the body from line 2 parses (`target 2`, `met false`); 502 B; no `rev` and no `instrument.sha256` — the checker's output schema (`:309-314`) has no such key. At 23:40:51 the working tree removed the echo line (`git diff`: one deletion) and the file now parses — but the command survives nowhere and the body still names neither revision nor instrument | this seat, 2026-11-04T02:37Z; the edit measured at 02:42Z | after receipts written through `--json-out` (pure JSON carrying `rev` + `instrument.sha256`); a base receipt that must become parseable keeps its command in a sibling record or a `command` field, and the rewrite is disclosed with the instant |
| M69-4 | membership — a claim field is not a check on the population (**the round-68 M68-9 class**) | `w1/ReviewerGates/attacks.json`: `missing-identity-arm` rc 0 `met true` with jq's arms carrying no `identity_ok`; `one-carrier-no-arms` rc 0 `met true` with one carrier, `arms {}`, and top-level `carriers_matched 3`; `explicit-false-arm` correctly rc 1. Source: `:283-284` compares the receipt's `carriers_matched` to `len(CARRIERS)`, never to `len(receipt["carriers"])`; `:299-301` iterates only supplied arms; `:292-294` takes `kind` as declared | ReviewerGates B2; source read by this seat | routed to the next freeze — a required-arm inventory per carrier, `len(carriers) == target`, and pinned carrier ids; the frozen instrument is not edited |
| M69-5 | relation on an unvalidated numeric domain | `attacks.json` `nan-ratio` rc 0 `met true` with one carrier's `before_ceiling_ratio` NaN; `packed-elf.py:303` rejects only `not isinstance(ratio,(int,float)) or ratio > 0.75`; `nan > 0.75` is False and `isinstance(nan, float)` is True; boundaries are right (`0.75` passes, `0.7501` fails); the control family exercises only `0.9` (`l1/pre/controls-at-base.json` `c3-loose-ceiling` rc 1) | ReviewerGates B3; source read by this seat | routed — `math.isfinite(ratio)` and a re-derivation of the ratio from ceiling/original; the frozen instrument is not edited |
| M69-6 | validator scope — internal arithmetic is not the declared inventory | `attacks.json` `mutation-invented-kills` rc 0 `{"defects": [], "mutants": 1, "ok": true}` and `probe-invented-arms` rc 0 `{"arms": 6, "defects": [], "ok": true}`; `mutation-check.py:173-203` checks row shape and survivor derivation only; `contract-probe.py:219-247` checks booleans, observation presence and `arms_passed`/`failed` arithmetic only | ReviewerGates A1 | routed — validate against `REGISTERED_CASES` and the six frozen arm ids; narrow validators are real but are not certification, and the predicates separately name the exact ids/counts |
| M69-7 | evidence — a snapshot claim names no instant | `w1/SentinelScope/audit.md` §1.1 prints `git status --porcelain --untracked-files=no` → 0 lines and concludes "No tracked file is modified"; four tracked files were modified at 23:36:55-23:37:20 (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`, mtimes) and `git status` at 02:37Z lists all four as ` M`; the audit file's own mtime is 23:37:50 | this seat, 2026-11-04T02:37Z | record the instant beside the status output and re-read it at write time; the modifications are the landing drafts, which belong to the L1, not to a seat — the defect is the undated claim, not the drafts |
| M69-8 | number drift — a count is a measurement and carries its command (**the round-68 M68-5 / R68-V5 class, recurring in this round's own lesson draft**) | `corpus/lessons/round-69.md` (working tree, 23:38:19, uncommitted) Gate row says the line-164 quote is "(5 words)"; `printf '%s' '--version: print the version of UPX' \| wc -w` = **6**. The landed S270 row states no word count, so only the draft is affected | this seat, 2026-11-04T02:37Z | the count is 6 in this draft; the fix is the command at write time, which R68-V5 already made the rule and which the draft did not run |

## Outcome

[L1] The L1's data run had produced no receipt when this draft was written (`.ufo/waves/round-69/l1/scores/`
was empty at 2026-11-04T02:37Z). Every line below is a placeholder the L1 fills with the after numbers;
no verdict is taken here, and the peer drafts cited above are not claim input.

- [L1] **R69-C1 — after.** `[L1]` survivors, `[L1]` killed with each kill's `failed` naming its declared
  case, `[L1]` `killed_wrong_case`, `[L1]` `pristine.cases` and `[L1]` `pristine.ok`, at the landing
  revision `[L1]`. Before (measured here from `l1/pre/c1-at-base.json`, base `d7d9a62c…`): survivors
  `[M1_identity, M2_recovery, M3_detected, M4_before, M5_control]`, `pristine.cases 13`, exit 1.
- [L1] **R69-C2 — after.** `[L1]` `arms_passed` of 6, `[L1]` per arm (A1_missing_node, A2_work_unusable,
  A3_packer_version, A4_packer_sha256, A5_carrier_record, A6_packer_pin), over the measured run's
  receipt `[L1]`. Before (measured here from `l1/pre/c2-at-base.json`): `arms_passed 0` of 6, all six
  named, `instrument_sha256 48ef4c68…`, `rev d7d9a62c…`, exit 1.
- [L1] **R69-C3 — after.** `[L1]` `met`, `[L1]` `target`, `[L1]` `carriers_matched`, `[L1]` `control_ok`,
  `[L1]` `failing`, `[L1]` `before_ceiling_ratio` per carrier, `[L1]` kinds. Before (body measured here
  from `l1/pre/c3-at-base.json`): `target 2`, `carriers_matched 2`, `met false`, `kinds [null]`, five
  failing clauses including `no shared-object carrier: kinds [None]` and both `before_ceiling_ratio
  None > 0.75`, exit 1.
- [L1] **Wave and landing.** `[L1]` seats settled of `[L1]`, `[L1]` dead, every seat artifact present
  `[L1]`, the landing revision the after-receipts name `[L1]`, and the repairs R68-V1..V6 `[L1]`.

## Census

- Start (measured at the base `d7d9a62c`, the declaration `616a5f2f` and the freeze `f1599810`:
  `git show <rev>:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'` → **176** at all three):
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exit 0, 176 rows,
  19 standing W04, malformed 0 (`.ufo/waves/round-69/l1/census-start.txt`; the receipt lists the
  19 W04 lines and `ok`, no count field — the 176 is this measurement).
- [L1] End: `[L1]` rows at the landing revision (`[L1]` malformed, `[L1]` W04; the same 19 are expected).
  Note for the reader of the numbers: the working tree at writing already carries the uncommitted S270
  row (`corpus/SOURCES.md` `M`, +2 lines, 23:37:20), so a live census reads 177 **before** the landing;
  the end value must be read at the landing revision, not from the uncommitted tree.
