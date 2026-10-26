# R40RevCensus — SOURCES.md registry pre-check, row template, next id, gate mirror test

DONE — registry validates clean (exit 0, W04 warnings only), gate selftest 92/92 mutants killed, next free id is **S123**, 11-column template + status/used-by/recheck rules delivered; scratch mirror: well-formed S123/S124 rows validate `ok` exit 0, a row with an escaped pipe fails `E01 fields=12` exit 1.

## 1. Mandated registry pre-check

Command (fleet root):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Full output (transcript: `.ufo/waves/round-40/w1/artifacts/R40RevCensus/00-precheck-validate-kaidoku.txt`):

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
kaidoku	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
kaidoku	W04	S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes
kaidoku	W04	S117 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md across scopes
kaidoku	W04	S119 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
EXIT=0
```

- **Exit 0.** All findings are W04 (same URL across scopes) — warnings never change the exit code per the script contract (lines 31–33). No E-codes, no lane findings.
- Census totals (`.ufo/waves/round-40/w1/artifacts/R40RevCensus/01-census-kaidoku.txt`): `rows=122`, `tier.A=114 tier.B=7 tier.C=1`, `status.mined=117 status.rejected=5 status.queued=0`, `missing=0`, fleet rows 122, exit 0.
- Gate health: `sources-census.sh selftest` → all 92 checks `killed` (no SURVIVED), `selftest ok`, exit 0 (`.ufo/waves/round-40/w1/artifacts/R40RevCensus/02-selftest.txt`).

## 2. Contract source

Frozen contract v1 (kaika, 2026-10-19) is carried in full in `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns" (lines 64–150): shape, 11-column header, per-cell definitions, rules 1–6, and the frozen manual census commands. The maintained gate `scripts/sources-census.sh` implements E01–E12 / W01–W04 and accepts 0–3 leading spaces on table rows (4+ spaces = indented code, ignored).

## 3. Exact 11-column row template

Header + separator, verbatim from `kaidoku-shokunin/corpus/SOURCES.md` lines 5–6:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

A row is one line: 11 cells = awk `NF=13`. Full fill-in template with per-cell constraints is in `.ufo/waves/round-40/w1/artifacts/R40RevCensus/20-row-template-and-rules.md`. Structure cross-checked against the live rows via awk field indices `$2=id $4=kind $5=tier $9=status $11=recheck $12=used-by` (contract's own census commands) and against S112–S122:

```
S112|code|A|mined|2026-10-26|180d| corpus/knowledge/2026-10-26-r38-…, corpus/knowledge/2026-10-26-r39-…
S115|own-work|A|rejected|2026-10-26|180d| —
S117|docs|A|mined|2026-10-26|on-release| corpus/knowledge/2026-10-26-unblob-format-matrix.md
S122|code|A|mined|2026-10-26|on-release| corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md
```

(all 11 rows S112–S122 extracted; statuses mined×10 + rejected×1, rechecks `180d`/`on-release`, used-by comma-separated lists or `—`.)

## 4. Next free id: S123

Evidence:

- `grep -cE '^ {0,3}\| S[0-9]{3}' corpus/SOURCES.md` (lane root) → **122**
- max id: `grep -oE '^ {0,3}\| S[0-9]{3,}' … | grep -oE 'S[0-9]+' | sort -V | tail -1` → **S122**
- contiguity: S001…S122 all present, none missing (per-id grep loop), and the gate reports no duplicate ids (E03 would fire).
- Census `rows=122` agrees.

→ the next row is **S123**, then S124, … appended inside `## Registry` after the S122 line (appending after the section end is E12).

## 5. Rules for the changeable cells (status / recheck / used-by)

Contract rule 2 (append-only): only `status`, `recheck`, `used-by` change in place, each logged old→new in the round lesson; a correction is a new row whose `teaches` opens `supersedes S0NN —` (this phrase also exempts the row from E04 same-URL-same-scope, and the rejected status exempts it too — gate lines 644–652).

- **status** — enum `queued|mined|rejected` only (else E07; `watch` is explicitly not a status). `mined` requires ≥1 used-by path (`mined` + `—` = W03); `rejected` rows keep their `REJECTED: <reason>; flip: …` teaches (<8 chars = W02) and are E04-exempt.
- **recheck** — a valid ISO calendar date, day cadence `NNd`, or symbolic cadence word (`on-release`, `annual`); anything else E09 (gate lines 663–667). ISO dates/cadences go overdue at `opened + N` days; symbolic cadences are reported by `overdue`, never judged overdue.
- **used-by** — repo-relative paths (relative to the lane root `kaidoku-shokunin/`), **comma**-separated (the maintained E11 check splits on comma only; `;` makes the whole cell one bogus path), or `—`. On a `mined` row every path must exist on disk (else E11, one finding per missing path — verified live, §6). `tier C` + `mined` + non-`—` = W01.
- **No `|` inside any cell** — including markdown-escaped `\|`: awk `-F'|'` still splits there, inflating the row to 12 cells (NF=14) → E01. Demonstrated below.

## 6. Scratch mirror test (gate red/green, `--file`)

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40RevCensus`; gate = `scripts/sources-census.sh`; `--today 2026-10-26`.

**(a) Well-formed rows pass.** Minimal registry (`corpus/SOURCES.md`: header + separator + S123 `queued|90d|—` + S124 `own-work, A, mined|180d|used-by R40RevCensus/dummy-cite.md` with the target file created under the resolution base) → `file ok <path>`, **EXIT=0** (artifacts `10-mirror-minimal-SOURCES-pass.md`, `11-mirror-minimal-pass.transcript.txt`).

**(b) Escaped pipe fails the gate.** Same mirror + one row S125 containing `demo \| breaks` in the source cell → `file E01 S125 fields=12`, **EXIT=1** (artifacts `12-mirror-minimal-SOURCES-fail.md`, `13-mirror-minimal-fail.transcript.txt`).

**(c) Full-copy control.** Appending the same two dummy rows to a full copy of the real registry and validating with `--file` produced a transcript **byte-identical** to the pristine copy's (`diff` empty; artifact `14-fullcopy-control-diff.txt`) — i.e. the two added rows contribute zero findings; S124's used-by path resolved cleanly (deleting its target flipped exactly one new finding: `E11 S124 missing used-by R40RevCensus/dummy-cite.md`).

[INFERENCE from gate code + (c)] The E11 flood a full copy shows under `--file` from scratch is a resolution-base artifact, not a registry defect: E11 resolves paths against `dirname(file)/..` (script `resolve_targets`), which is the lane root only when the file lives at `<lane>/corpus/SOURCES.md`. L1 validating the committed file via `validate --root … kaidoku` gets the correct base — as §1 shows, exit 0.

## 7. Residual risk / notes for L1

- W04 warnings are expected and permitted (12 rows share URLs across scopes, e.g. rea-agents-6.5.0.tgz on S083/S090/S092/S119). No action needed for freeze; do not "fix" by deleting rows (append-only contract).
- Cosmetic: S047's URL sits in backticks, so the gate's normalized URL keeps a trailing backtick (S047 W04 line). Warning-only; avoid backtick-wrapping URLs in new rows.
- The frozen manual census examples in CORPUS.md assume column-zero rows; the maintained parser additionally accepts 0–3 leading spaces. New rows: write at column zero.
- No tools were installed or upgraded for this seat; no VCS mutations; scratch `/fast/scratch/hyaku/kaidoku-r40/R40RevCensus` removed at finish; all cited evidence copied into the artifacts dir (all files < 5 MB).

**Artifacts** (all under `.ufo/waves/round-40/w1/artifacts/R40RevCensus/`): `00-precheck-validate-kaidoku.txt`, `01-census-kaidoku.txt`, `02-selftest.txt`, `10-mirror-minimal-SOURCES-pass.md`, `11-mirror-minimal-pass.transcript.txt`, `12-mirror-minimal-SOURCES-fail.md`, `13-mirror-minimal-fail.transcript.txt`, `14-fullcopy-control-diff.txt` (empty = identical transcripts), `20-row-template-and-rules.md`.
