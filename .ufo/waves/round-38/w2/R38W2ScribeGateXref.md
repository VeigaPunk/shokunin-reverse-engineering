# R38W2ScribeGateXref — Gate decisions cross-referenced at `0fc61133`

**Verdict: DEFECTS FOUND (registration, not verdicts).** All 13 Gate decisions in
`corpus/lessons/round-38.md` are represented — 5 admitted sources with lane rows and `used-by`, 3
assimilation decisions (1 admit → rows S116+S110, 2 refusals → no lane row, staged rows only), 5
quarantine verdicts (staged/absent-defect rows, none admitted). None is overturned. What fails is
pointer registration: one lesson pointer resolves to nothing in-lane, two decisions rest on
uncommitted host state, the scratch-mirror census gate certified an S112 row that was not the row
that landed, and registry row S113 registers one of the two carrier digests it scopes.

Full table: `.ufo/waves/round-38/w2/artifacts/R38W2ScribeGateXref/gate-xref.md` (decision × registry
row × citing entry × pointer × resolution, plus the collision/census items and the "no committed
evidence" list).

## What I resolved (all at `0fc6113376a156fddc3ec385386d71c3a4a9f690`)

| decision | row | pointer | resolution |
|---|---|---|---|
| S112 admit | lane S112, `mined` | none named | PARTIAL — digest `2d7b901b…9287` committed via S108 + `w1/R38ScoutUnblobHandler.md`; L1's own re-open uncaptured |
| S113 admit | lane S113, `mined` | `w1/R38ScoutUnblobFixtures.md` | YES — but see D4 |
| S114 admit | lane S114, `mined` | `w1/R38ScoutFreetzAvm.md` + round-37 `probes/avm.txt` | YES — byte-checked: `c1c43f6f…a5d5`, 1496 B |
| S115 reject | lane S115, `rejected`, used-by `—` | `w1/artifacts/R38CrossToolK4/7z-refusal.txt` | YES — all four carriers, `exit_code=2` |
| S116 admit | lane S116, `mined` (digest in row) | none named | PARTIAL — committed capture is wave-1's `sources-live.txt`; L1 fetch uncaptured; independent refetch by me identical |
| ADMIT matrix | S116 + S110 edited | staged package (read-only, present) | YES; corrections' arithmetic uncaptured (D7) |
| REFUSE compatibility-precondition | none (correct); staged S165 | staged entry (present); lane S110/S112 | YES on the negative half; positive `ls -la` uncommitted (D9) |
| REFUSE avm-branch | none; staged S189–S192 | staged entry (present) | YES; tsvs exist and are tracked in shokuknow (D9 wording) |
| S150 refuse | staged S150; register line 82 | `w1/R38ExecQuarantine.md` + `quarantine-verdicts.txt` | YES |
| staged S113 adopt-with-anchor | staged S113 (line 315) | same verdicts file | YES (22 `hreflang` = 21 + `x-default`) |
| S117 unverifiable | staged S117 (line 316) | same | YES (202, 0-byte body) |
| S136 adopt-with-anchor | staged S136 (line 317) | verdicts + lane entry | YES — `2 of 24 verbs are` at line 8 |
| S147 adopt-with-anchor | staged S147 (line 318) | lesson: `` `HOST-CONTRACT.md` line 41 `` | **NO** (D3) |

## Findings

- **D1 (medium) — the end census has no pointer.** The lesson says attempt 2's registry "validates
  exit 0 in the real lane (end census in the report)". No L1 report and no post-append census receipt
  exists at `0fc61133`; the only committed census receipts are pre-append
  (`w1/artifacts/R38CriticSourcedClaim/census-receipts.txt`: real lane RC=0 on 111 rows; mirror files
  RC=1 with `E12=0 E-other=0`). I reproduced it: full `git archive 0fc61133` to scratch, then
  `scripts/sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-26` → one
  `W04 S112 … across scopes`, **RC=0**. The claim is true; the receipt is missing.
- **D2 (medium) — the census gate certified a row that did not land.** `append-block.normalized.md`
  S112 (sha `984bcc96…d35f7e`, the block the mirror gate validated) scopes "`squashfs_v4_be` magic
  PATTERNS and the `SquashFSv4BEHandler` EXTRACTOR binding … S108 … already scopes … the `-le`/`-be`
  argv" with recheck `on-release`; the landed S112 row scopes "v4 BE extractor dependency and argv …
  only" with recheck `180d`. So the gate's exit-0 result does not certify the landed S112 bytes, and
  the argv scope the validated block deliberately reserved to S108 is duplicated in the landed row
  (W04 documents the URL reuse, not the scope overlap). Landed bytes are clean only because of my run.
- **D3 (medium) — S147's lesson pointer does not resolve.** `git ls-tree` → 0 files matching
  `host.contract`; the bare name `HOST-CONTRACT.md` names nothing in the lane. The resolvable chain is
  committed round-35 evidence (`w1/R35ReconQuarantine.md:174-178`: `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`,
  3,386 B, `sha256 ab36b310…58fe`, line 41 quote, line 46 heading) plus the live host file, whose
  sha256 I confirmed as `ab36b310b285c0278bef2a62ccdc5effe9cdc2d232e4e684452c17be264b58fe` (3,386 B).
  Round 38 commits no capture. Two calibration errors ride along: (a) the lesson drops wave 1's
  conflict — the quote says `rea-agents@6.7.0` / 207 tools while the lane's pinned package is
  `"version": "6.5.0"` (`…/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json`), so an
  "adopt-with-anchor" row carries a fact that is false on this host; (b) "the heading names … are
  wrong" overstates — line 41 is a bullet under `## State as of this writing` (39), and line 46's
  heading is literally `## Expected \`doctor\` output on this host`, i.e. one name wrong, one right.
- **D4 (low–medium) — registry S113 registers one oid for two carriers.** Its locator quotes only
  `squashfs_v4.nopad.bin` (`a29ddc15…56ed`, 307 B = K4). K3 is `squashfs_v4.bin` (`9c7c523c…97c0`,
  4096 B) — verified by me from the committed carrier (`K4/carrier.bin` = `a29ddc15…56ed`/307 B;
  `K3/carrier.bin` = `9c7c523c…97c0`/4096 B) — and that digest appears in no `corpus/SOURCES.md` row,
  only in `.ufo/waves/round-38/c1/carriers.json` and the wave-1 report. The S113 flip condition ("an
  oid differs from the lane carrier digest") is therefore evaluable for K4 only.
- **D6 (low) — L1 live re-opens uncaptured** for S112 (03:43) and S116 (03:44). Byte identity is
  carried by earlier committed captures and by my refetch (`http=200 bytes=216890`,
  `sha256 8f8c29af…bbc5`), not by an L1 artifact.
- **D7 (low) — the ADMIT's correction arithmetic is unrecorded**: 97 `<h2 id=`, ten SquashFS sections,
  `v4-broadcom` spelling, 42 × `Vendor`, "Does not support encrypted ZIP files" are absent from
  `sources-live.txt`. I rechecked live: 97 / ten / 3 × `SquashFS (v4-broadcom)` (spelling as the entry
  says) / 42 / 1 — all hold.
- **D8 (info) — the collision map is stale by construction.** `collisions` = S106–S111 (6) against the
  pre-append registry (111). Staged S112, S113, S114, S115 and S116 all exist in
  `merge/kaidoku/SOURCES.append.md`, so the append creates five new id collisions that any future
  assimilation must renumber.
- **D9 (info) — refusal wording.** "S190/S191 are campaign-local … that the lane does not hold" is
  true for `kaidoku-shokunin` but the tsvs exist and are `git ls-files`-tracked in
  `/home/vgpnk/Projects/shokuknow` (`lanes/kaidoku/round9/work/lead2-avm-branch.tsv`,
  `lanes/kaidoku/round7/work/r7-local-measurements.tsv`), and the r7 `M5` row does read
  `not installed … No module named 'unblob'`. The refusal's stated reasons (unpinned `/main/` S189;
  contradicting sibling entry) stand. REFUSE #1's positive fact is verified live by me
  (`sasquatch` 382824 B, `sasquatch-v4be` 436232 B, `unblob` uv-tool link).

## Decisions with no committed evidence at `0fc61133`

1. S147 anchor bytes (inherited round-35 digest only; lesson pointer unresolvable).
2. REFUSE #1's `ls -la ~/.local/bin/...` observation.
3. The end census ("in the report") — no report, no receipt.
4. ADMIT correction arithmetic (D7).
5. L1's own S112/S116 refetches (D6).

## Calibration

- Bytes I recomputed myself: `probes/avm.txt` sha256/1496 B; K3/K4 `carrier.bin` sha256+size;
  `unblob.org/formats/` sha256/216890 B/counts; `HOST-CONTRACT.md` sha256/3386 B; `rea-agents` 6.5.0;
  lane registry row count 116; `reg-ids` 111 / `staged-ids` 132 / `collisions` 6; S110 status+recheck
  unchanged base→landed; census `validate` RC=0 on the landed registry.
- [INFERENCE]: staged-register line numbers and package paths are unchanged since 2026-10-24 — I checked
  existence and the cited row text, not a digest of those files. The quarantine register's own row
  lines (82, 315–318) match the wave-1 verdict file.
- I did not re-run any C1/C2 counter, control, carrier or oracle, and did not refetch the zenn/IEEE/adb
  pages (peer `R38W2Quarantine` holds that ground).

## Touched surfaces

- Wrote: `.ufo/waves/round-38/w2/R38W2ScribeGateXref.md`,
  `.ufo/waves/round-38/w2/artifacts/R38W2ScribeGateXref/gate-xref.md`.
- Read-only: `git ls-tree/cat-file/show/grep/archive` on the lane at `0fc61133` (and `77091b49` for the
  S110 base comparison); `scripts/sources-census.sh` on a scratch extraction; one `curl`;
  `merge/kaidoku/**`, `.ufo/waves/corpus-expansion-1/absent-defect-register.md`, two shokuknow tsvs,
  `~/.agents/.../HOST-CONTRACT.md`, the pinned REA `package.json`.
- No VCS mutation; no REA run; no tool installed (nothing needed); scratch
  `/fast/scratch/hyaku/kaidoku-r38/R38W2ScribeGateXref` removed after use.

## Out of scope / for the L1

- Suggest (advisory): give S147 a real locator (`~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`
  + `sha256 ab36b310…58fe`, line 41) and record the 6.5.0/6.7.0 conflict; add K3's oid to row S113;
  commit the post-append census receipt so "exit 0 in the real lane" is self-evidencing; note that the
  validated S112 block ≠ landed S112 row; renumber staged S112–S116 before the next assimilation.
