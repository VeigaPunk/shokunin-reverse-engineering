# CensusRun — round-17 wave-2 falsify: frozen census + used-by citation audit

Lane revision under attack: `da64646adcb19c1ede7537b799b8c7d283fe43da` (kaidoku-shokunin
`corpus/SOURCES.md`, 65 lines, 30 rows S001–S030). Full command outputs:
`.ufo/waves/round-17/w2/census.txt`. No installs; no files outside `w2/` touched.

## Ran (all from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`)

- Every frozen manual command in `/home/vgpnk/Projects/shokunin/CORPUS.md:131-148`
  verbatim against `corpus/SOURCES.md`.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
- Deep check (assigned): for every `mined` row, each `used-by` path was `grep -Fw`'d
  for its own `S###` id — 53 (id, path) pairs.
- Reverse check (unassigned bonus): every `corpus/**/*.md` file was scanned for
  `S\d{3,}` tokens and diffed against the cited rows' `used-by` sets.

## Frozen-census results — all clean (OBSERVATION)

- rows = 30; malformed rows (NF≠13) = 0; duplicate ids = none.
- tier histogram `A=26 B=2 C=2`; status `mined=28 rejected=2`, queued=0. Zero queued
  rows is consistent with the `## Leads (unopened)` section carrying unadmitted
  leads instead (SOURCES.md:59-65).
- enum violations / `community`-at-A: none (B at S016, C at S022/S028).
- every mined `used-by` path exists on disk (checked relative to lane root).
- Validator: `kaidoku\tok\t.../SOURCES.md`, exit 0 — including its E12
  outside-Registry, E04 duplicate-URL, E08/E09 date checks, which the frozen
  commands do not cover.
- Evasion probe: exactly 32 `^|` lines — 30 rows + header + separator; no
  lower-case/malformed-id row hiding outside the `S[0-9]{3,}` regex; ids are
  contiguous 1–30 with no gap or skip.

## Used-by ↔ citation audit — forward direction clean (OBSERVATION)

All 53 mined-row `used-by` entries resolve to existing files that literally contain
the row's own id as a word (`grep -Fw`). No `NO-CITE`, no `MISSING-FILE`.

## Findings — reverse direction (missing `used-by` membership)

A strict reading of CORPUS.md:107-108 — "`used-by` — repo-relative paths of the
knowledge entries or lessons citing the row" — treats the field as a completeness
claim over citers, and "lessons" plausibly covers `corpus/lessons/*.md` including
verifier spotchecks. Under that reading (OBSERVATION + INFERENCE):

1. **`corpus/lessons/round-17.md` cites S023 (line 65) but S023's `used-by`
   (SOURCES.md:29) omits it.** The same line 65 is the round-17 `## Gate` log
   recording S023's `used-by` old→new; the logged "new" value
   (`round-17.md:65`) also omits `corpus/lessons/round-17.md`. Every other row
   touched this round self-lists it: S003 and S024–S030 all carry
   `corpus/lessons/round-17.md` in `used-by` (confirmed by the 53-pair grep).
   Inconsistent with its own sibling edits in the same commit.
   Weakening precedent (OBSERVATION): `corpus/lessons/round-14.md:55` cites
   S005/S006 only in a "rows are unchanged" gate-log sentence, and S005/S006
   exclude round-14.md — so a convention exists where a gate-log-only mention
   does not force `used-by` membership. Round-17.md:65 is exactly such a
   gate-log-only mention for S023. **Verdict: asymmetric bookkeeping at worst;
   defensible under the round-14 precedent. Low severity.**
2. **`*-verifier-spotcheck.md` files cite 16 row ids none of which list the
   spotcheck file** (e.g. `round-15-verifier-spotcheck.md:117,119,151-153` cite
   S003/S007/S023; `round-16-verifier-spotcheck.md:114,149-152` cite S003/S023).
   If "lessons" in CORPUS.md:107 includes spotcheck files, every spotcheck round
   has left `used-by` incomplete since round 13. If it does not, the convention
   is applied consistently — every spotcheck cite is excluded. **Verdict:
   consistent convention, under-specified contract language; not a row defect.**

## Bounded no-finding

Within the four named attack surfaces — malformed rows, enum violations, missing
`used-by` paths, mined rows whose `used-by` file does not cite the id — **zero
defects**. The registry at da64646 passes every frozen census invariant and the
maintained validator (`ok`, exit 0). The only residual is the `used-by`
completeness question above, which is contract ambiguity (CORPUS.md:107), not a
falsified row.

## Tools/versions

System `gawk`, `grep`, `sort`/`uniq`, python3 (with `-B`, scratch under /tmp only).
No installs performed.
