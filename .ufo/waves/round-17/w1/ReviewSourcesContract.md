# Review — `corpus/SOURCES.md` against CORPUS.md contract v1 (round 17)

Read-only review at baseline `b563c799d97774aae4351276fe43cb897311e349`. Labels:
**[OBS]** = command output I ran; **[INF]** = inference from contract/dispatch text.

**Verdict: conformant today, no blocking defect.** The registry passes every contract
census, the next unused id is **S024**, and round 17 can resolve exactly **two** of the
five lead bullets (partially) — but the lead lifecycle and the draft-row set leave three
medium gaps that L1 must decide explicitly rather than discover at integration.

## 1. Next unused id — S024 [OBS]

`23` rows; max id `S023` (`corpus/SOURCES.md:29`); `grep -rn 'S02[4-9]' corpus/` returns
nothing (only `.ufo/waves/round-17/*.json` plan text). So **S024** is next, and the wave
spec already reserves `S024+` for four candidates. Allocation if all are admitted, in
draft order: **S024** Go `debug/buildinfo` source, **S025** Go release history,
**S026** Go experiment-suffix doc, **S027** Ghidra upstream status. Ids are contiguous
and may not be skipped or reused (`CORPUS.md:89`); a candidate that is not opened takes
no id.

## 2. Registry census [OBS]

Contract commands (`CORPUS.md:135-147`) from the lane root:

- rows `23`; malformed rows `0`; duplicate ids: none; tier `A=21 B=1 C=1`;
  status `mined=22 rejected=1`.
- mined rows with a nonexistent `used-by` path: none.
- `opened` all ISO; `recheck` all in `{on-release, 90d, 180d, 365d}` — 0 violations
  (`CORPUS.md:105-106`).
- maintained validator: `kaidoku\tok\t.../corpus/SOURCES.md`, exit `0`.
- `NF==13` on every row doubles as the "no `|` inside any cell" check
  (`CORPUS.md:89`): a pipe would split a cell and raise NF.

## 3. Exact rules for a new row

Columns are fixed at `CORPUS.md:86` and enumerated `:89-108`. Row-writing checklist:

1. **Opened by the row's author in the round that writes it** (`:112`). The wave
   `DraftSourcesRows` prompt says "each opened by YOU this round", so the opener is that
   seat; the round lesson Gate must name the opening seat, never imply a scout's fetch
   was the author's open. **[INF]** on the seat-vs-author reading; **[OBS]** that prior
   rounds recorded reopens explicitly (`corpus/lessons/round-16.md:28`).
2. **Gate, per row**: URL, access date, ≤25-word quote with its location (`:112-115`).
   The draft file is *not* the Gate — L1 transcribes into `corpus/lessons/round-17.md`.
3. **`anchor`** = exact section/line + revision, never a bare homepage (`:99-100`).
   For Go rows this means a tag (`go1.27.0`, `go1.23.12`) or a release heading + date;
   `latest`/`master` is acceptable only when `scope` explicitly says "master, not a
   release", as S004 already does (`corpus/SOURCES.md:10`).
4. **No `|` in any cell** (`:89`). Go source quotes may contain `||`/`|`; quote only
   contiguous pipe-free spans or reword `teaches`. Escaping is not allowed — the pipe is
   the delimiter.
5. **`kind`/`tier`**: Go source `code`, Go docs `docs`, both tier A for their own
   behavior; `scope` must carry the version boundary (`:91-98`). A tier is scoped, never
   global.
6. **`recheck`** `on-release` for Go docs/source and Ghidra upstream (`:105-106`).
7. **`status`**: `queued` until `used-by` is non-empty, then `mined` (`:103-104`).
8. **Corrections**: a *wrong* row is corrected by a new row whose `teaches` opens
   `supersedes S0NN —`; narrower-than-later is not wrong (`:116-118`). So a later
   GoReSym release or Ghidra release note **adds** a row and never edits S004/S005.
9. A draft candidate is not a row: "an index row is a claim. Write the row when the file
   exists" (`CORPUS.md:46`); nothing may cite `S024` before it is in the table.

## 4. Exact rules for `used-by` (and coupled status) changes

- **Only `status`, `recheck`, `used-by` change in place**, and **each change is logged
  old→new in the round lesson** (`CORPUS.md:116-118`). Precedent: round-14
  `corpus/lessons/round-14.md:53-55`, round-15 `:41-43`, round-16 `:82-85`.
- **Repo-relative, lane-root-relative paths of knowledge entries or lessons only**
  (`:107-108`). Never absolute, never `.ufo/...` (including this wave's draft), never a
  receipt.
- **The path must exist when `SOURCES.md` is committed** (census `:146-147`); the
  premature-reference mistake is already recorded at `corpus/lessons/round-15.md:67`.
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` is contract-mandated and
  `corpus/lessons/round-17.md` is the lesson target — add each only once it exists.
- **Coupled transition [INF]**: the first citation both appends the path and flips
  `queued→mined`, and both are logged; the two are one edit, not two. Derived from
  `:103` ("mined (cited by ≥1 path in used-by)") and `:116`.
- **Rows round 17 is entitled to touch**: S003 (`:9`, 7 paths) and S023 (`:29`, 4 paths)
  only; append the two r17 paths to each. S004/S005/S007 keep their cells unless a
  correction row is written.

## 5. Leads (`corpus/SOURCES.md:49-55`) — what round 17 can actually resolve

| anchor | lead | resolvable now? | basis |
|---|---|---|---|
| `:51` | IEEE S&P 2022 lifter SoK | **No** | C1/C2 contain no lifting work; primary is paywalled (Crossref-only earlier); no dispatched seat. |
| `:52` | LLM4Decompile `2403.05286` | **No** | No LLM-decompiler axis this round; opening it would be a row with no teaching use, against `:123-125`. |
| `:53` | GoReSym releases after `d7f23b7…` | **Yes** | `ScoutGoReSymReleases` is dispatched to that exact URL and "resolves a SOURCES lead or records it still open". In scope: C2 bounds the second parser with a `go1.27.0` carrier. |
| `:54` | version-matched `.jsc` route (Electron 42 / V8 14.8) | **No** | No Electron artifact this round. Also stale: `jscd` v0.1.0 was already exercised and hard-refuses V8 14.8 (`corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md:206-208`), and the lead does not cite it. |
| `:55a` | Ghidra release notes after 12.1.4 for GP-6528 | **Yes** | `ScoutGhidraUpstreamGo` is dispatched to `.../ghidra/releases` and its prompt says it "resolves/advances the SOURCES lead". |
| `:55b` | IDA/Hopper/JEB official provider refs | **No** | Operator-gated surfaces, untouched this round; an unopened provider reference cannot become a row. |

The three *new* row candidates (Go buildinfo docs, Go release history, experiment suffix)
are **not** among these leads — legitimate (`:83` makes leads optional, not a queue), but
it means round 17's new rows are carried by C2, not by the leads section. `:53` and
`:55a` are the only leads whose opening is dispatched this round.

## 6. Findings

**F1 · medium · calibration — the contract does not govern a lead's exit.**
`:83` says `Leads (unopened)` are "bullets; a lead is not evidence and never a row", and
`:116` allowlists only row cells, so nothing states what happens when a lead is opened.
Round 17 will open `:53` and half of `:55`; leaving them verbatim makes the file assert
that opened things remain unopened — a false negative claim. `:55` also bundles a
resolved half (release notes) with an unresolved half (operator-gated providers) in one
bullet, so it must be split. Do one of: remove the resolved bullet(s) and log the old→new
bullet text in the round lesson (extends `:116`'s logging to non-row text), or annotate
`resolved — S0NN` in place. Either is defensible; silently leaving them is not. Record
the choice in the lesson so the next round does not re-litigate it.

**F2 · medium · depth — one buildinfo row cannot ground both carriers.**
C2 pins `shfmt` at `go1.27.0-X:nodwarf5` and `esbuild` at `go1.23.12`
(`.ufo/waves/round-17/pilot/README.txt`). Rule 1 allows **one** ≤25-word quote per row
(`:112-115`), so a row pinned to one tag grounds one revision only. `buildinfo-probe.py`
depends on flag/inline semantics that could differ across 1.23→1.27, and the repo has no
Go toolchain to diff tags locally (`which go` empty; no `/usr/lib/go`; `pacman -Q go`
exit 1; `~/go` holds only an empty `pkg/`) — so a single row would let the probe's 1.23
path look source-grounded when it is not. Either write two rows (one per tag) or scope
S024 to `go1.27.0` and have the Gate say explicitly that `go1.23.12` is ungrounded.

**F3 · medium · depth — the lead with a scout has no row seat.**
`DraftSourcesRows` drafts four candidates: buildinfo source, release history, experiment
suffix, Ghidra upstream status. GoReSym releases is **not** one of them, yet `:53` is
dispatched to `ScoutGoReSymReleases`. So the round can resolve `:53` and ship no row, or
ship an undrafted one. Decide explicitly: a release claiming 1.26/1.27 → draft the row
(next free id) with tag + located quote; no such release → the artifact is a **search-log
entry with its sweep** (`:126-128`, `CORPUS.md:39-40`), because "no release after
`d7f23b7` claims it" is a negative claim and needs the URL list and count, plus a revised
`:53`. S005 itself must not be edited either way (its claim stays true at its pinned
commit).

**F4 · low — pipe hazard on the new rows.** `:89` forbids `|` in any cell; Go source
quotes may contain `||`. Run the malformed census (`:137`) after integration, not just
by eye.

**F5 · low — `:54` is stale relative to retained local evidence.** The lead reads as if
nothing local tests the `.jsc` route, while `knowledge/2026-10-13-r4-07-jsc-bytecode.md`
records an exercised `jscd info` refusal at V8 14.8. Not resolvable this round, but when
it is, it should start from that retained result rather than re-deriving it.

**F6 · observation — the status histogram carries no signal.** Zero `queued` rows; every
opened row is `mined` on arrival. Contract-consistent (`:103`), but do not cite
`mined=22` as source maturity.

## 7. Verification gaps

- No lead page was fetched by me (read-only scene; no network read); §5 rests on the
  leads' own text and the `wave1-spec.json` dispatch prompts, not on the pages.
- Scout outputs were not available at review time; F3's open answer is by design.
- I did not run or read `DraftSourcesRows` output (not yet written).
- No installs or upgrades; nothing to record.
