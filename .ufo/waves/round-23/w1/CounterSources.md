# CounterSources — R22 source eligibility and the exact `used-by` parse

Seat: KaidokuR23.CounterSources (read-only leaf). Scope: read R22 source eligibility and the
exact `used-by` parse, then enumerate the requirements for R23 new-source eligibility and
for inherited R22 preservation. No counter was executed, no REA verb was invoked, no
debugger/Frida/device/carrier action was taken. Paths are relative to
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless absolute.

Labels: **OBSERVED** = read from a file or produced by a read-only command in this seat;
**INFERRED** = consequence of the observed code, not executed; **UNKNOWN** = not established.
Observation cutoff: 2026-10-21, before concurrent seats' round-23 knowledge/evidence writes
became visible to this seat; every pin and eligibility statement below is against commit
`a3c92eb` (the frozen round-23 baseline), not the live worktree.

## 1. Inputs actually read (OBSERVED)

| Input | Fact |
|---|---|
| `.ufo/waves/round-23/claims.json` | R23-C1, six T1 verbs, `sourced` = "New knowledge cites opened/mined S058+ with exact used-by"; `counting_command` = `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <LANE> --rev <REV>`; falsifiers include `same verb double counted`, `source linkage absent`, `inherited identify lost`, `copy erases parent refusal`, `refusal counted`, `mere mention counts` |
| `.ufo/waves/round-22/tools/count-c1.py` | sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879` (worktree and `git show a3c92eb:`) |
| `.ufo/waves/round-20/tools/verb-coverage.py` | sha256 `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f` (matches R22 `HELPER_SHA256`) |
| `.ufo/waves/round-21/tools/verb-coverage.py` | sha256 `615369384bf821a44e4d3c458006ed169939025d8fd3415f318ae37bb52f887b` (matches R22 `HELPER_SHA256`) |
| `corpus/SOURCES.md` at `a3c92eb` | sha256 `5ae5e7ed539d092d801d1c521cb3a0cfa6d89ff82e38b8d86c0c8d5b4f777ebd`; 57 rows, max `S057`, no duplicate id, no malformed 13-cell row (read-only Python mirror below, exit 0) |
| `git -C <lane> diff --name-status aa1450b a3c92eb` | exit 0; only `.ufo/waves/round-23/{before-r22-c1,claims,start-census}.json` added plus `LOG.md`, `SCORECARD.md`; **nothing under `corpus/` or `.ufo/waves/round-22/` changed** |
| `.ufo/waves/round-23/before-r22-c1.json` | retained R22 counter run at `aa1450b`, exit 1, `t1_exercised_count: 1` |
| `.ufo/waves/round-22/verify/final/after-c1.json` | retained R22 final run at `e9db7e2`, exit 1, `t1_exercised_count: 1`, script sha `c925918f…` |
| `.ufo/waves/round-22/verify/final/source-rows.json` | rows before 50 → after 57; `old_rows_identical: true` |
| `scripts/sources-census.sh` (at `/home/vgpnk/Projects/shokunin/`) | census contract, E01–E12/W01–W04, read-only |
| `corpus/QUALITY.md:39,41,42` | QUALITY 29 (source + Evidence linkage), 31 (original envelope, refusal ancestry), 32 (revision-bound, no unreviewed helpers) |
| `corpus/lessons/round-22.md:59-67` | the QUALITY-29 repair: filter each counted entry by its source line, mined S051+ row, matching used-by; C1 `missing_source` falsely counted 6 before the repair |

Read-only parse mirror used in this report (no counter execution): an inline Python copy of
`count-c1.py:124-141` applied to `git show a3c92eb:corpus/SOURCES.md` and to each
`corpus/knowledge/` blob at `a3c92eb`; exit 0. Results are in §2.4/§3.

## 2. R22 eligibility, exactly (OBSERVED at the cited lines)

### 2.1 Where the inputs come from

- `measure()` resolves one commit (`count-c1.py:101-107`) and reads every blob with
  `git show <resolved-rev>:<path>` (`:115-119`). Worktree bytes are not read; a missing
  `corpus/SOURCES.md` raises `blob_revision_unreadable` → exit 2 (fixture `missing_registry`
  expects exit 2, `counter-fixtures.py:152`).
- Knowledge entries are every tree blob under `corpus/knowledge/` at that rev
  (`:131-137`, using `r20.KNOWLEDGE_PREFIX` = `corpus/knowledge/`, `verb-coverage.py:34`).
- The legacy pass sets `r20.EVIDENCE_PREFIX` and recompiles `r20.CITED` from the R22 module
  global `EVIDENCE_PREFIX` (`count-c1.py:33,109-110`), so the prefix is swappable per call
  but the citation regex is rebuilt only inside `measure()`.

### 2.2 SOURCES.md row parse (`count-c1.py:121-130`)

`cells = [cell.strip() for cell in line.split("|")]`, then a row counts only if
`len(cells) == 13 and re.fullmatch(r"S[0-9]{3,}", cells[1])`.

Verified on the S054 row: cell index `0` = `""`, `1` = id, `2` = source, `3` = kind,
`4` = tier, `5` = scope, `6` = anchor, `7` = teaches, `8` = status, `9` = opened,
`10` = recheck, `11` = used-by, `12` = `""`. The leading and trailing `|` are mandatory;
11 content columns must yield exactly 13 split cells.

- Any extra `|` inside any cell makes `len(cells) > 13`; the row is **silently skipped** by
  the counter (no error). Census `validate` instead reports `E01` (`sources-census.sh:635-638`).
- A duplicate id anywhere in the file raises `duplicate_source_id` (`:126-128`) → the whole
  run is **unevaluable (exit 2)**, not a non-count. Census also reports `E03`.
- The counter does not restrict rows to the `## Registry` section. A well-shaped row under
  `## Paths` would be read by the counter, but census reports `E12` (`sources-census.sh:620-624`),
  so Registry-only is required by the no-harm census, not by the counter loop.
- `kind` (cell 3), `recheck` (cell 10) and the source URL text are unconstrained here;
  census constrains them (E05/E09/E04).

### 2.3 Row eligibility predicate (`count-c1.py:129`)

```python
if int(cells[1][1:]) >= 51 and cells[4] in ("A", "B")
   and cells[8] == "mined" and cells[9] == "2026-10-21":
       source_rows[cells[1]] = cells[11].split(",")
```

So an R22-eligible row needs: numeric id ≥ 51, tier exactly `A` or `B`, status exactly
`mined`, opened exactly `2026-10-21`. The threshold is **numeric** (`S051`, not a lexical
comparison), and the date is an exact string. `S050` is excluded. R22 fixtures pin each
negation: `source_queued`, `source_old_date`, `source_old_id`, `tier_c_only`,
`source_wrong_used_by` all expect count 0, exit 1 (`counter-fixtures.py:84-104,152`).

### 2.4 `used-by` parse and entry eligibility (`count-c1.py:130,138-142`)

- The used-by cell is split on `,` only: `cells[11].split(",")`. There is no escape, no
  quote handling, no link/backtick/glob handling.
- At comparison time each part is `part.strip()` (Python whitespace strip at both ends):
  `path in [part.strip() for part in source_rows.get(sid, [])]`.
- `path` is the exact git tree path of the knowledge blob, e.g.
  `corpus/knowledge/2026-10-21-r23-example.md`. Matching is **exact string equality**,
  case-sensitive, with no path normalization and no directory/prefix match.
- The first line of the entry is `text.partition("\n")[0]`; it must `startswith("source:")`.
  IDs are `re.findall(r"\bS[0-9]{3,}\b", source)`; this regex is **not** `re.ASCII`-flagged.
- The entry is eligible if **any** extracted id maps to an eligible row whose used-by list
  contains this exact path. Eligibility is stored as a set of entry **texts**
  (`eligible.add(text)`), not paths: two byte-identical files at different paths are both
  eligible if either path is listed.

Mirror output on crafted cells (entry path `corpus/knowledge/2026-10-21-r23-example.md`):

| used-by cell form | match |
|---|---|
| `corpus/knowledge/2026-10-21-r23-example.md` | true |
| `  corpus/knowledge/2026-10-21-r23-example.md  , corpus/lessons/round-23.md` | true |
| `` `corpus/knowledge/2026-10-21-r23-example.md` `` | false (backticks stay in the part) |
| `corpus/knowledge/2026-10-21-r23-example.md.` | false (trailing period stays) |
| `[x](corpus/knowledge/2026-10-21-r23-example.md)` | false |
| `<corpus/knowledge/2026-10-21-r23-example.md>` | false |
| `corpus/knowledge/` | false (directory, not a file path) |
| `corpus/knowledge/2026-10-21-r23-*.md` | false (glob) |
| `knowledge/2026-10-21-r23-example.md` | false (missing `corpus/`) |
| `corpus/knowledge/2026-10-21-R23-EXAMPLE.md` | false (case) |

First-line mirror (same regex/startswith as the counter):

| first line | ids |
|---|---|
| `source: S058 https://example.org/x` | `['S058']` |
| `source:S058` | `['S058']` (a space after the colon is not required) |
| `source: none` | `[]` |
| `# title` then `source: S058` on line 2 | not parsed (only line 1) |
| `source: S057 \`.ufo/waves/round-23/evidence/c1/S058-probe.json\`` | `['S057','S058']` — an id-shaped filename injects an id |
| `source: S059a` | `[]` (trailing `a` blocks the `\b`) |
| `source: s058` | `[]` (case-sensitive id) |
| `source: (S060)` | `['S060']` |

Actual R22 used-by values (OBSERVED at `a3c92eb`):

| row | used-by |
|---|---|
| S051, S052, S053, S054, S057 | `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md, corpus/lessons/round-22.md` |
| S055 | `corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md, corpus/lessons/round-22.md` |
| S056 | `corpus/lessons/round-22.md` |

Consequence: the lesson path alone never makes a knowledge entry eligible; only an exact
`corpus/knowledge/<file>.md` part does. The same comma+trim grammar is used by census
`usedby_findings` (`sources-census.sh:538-569`), which additionally requires the path to
exist on disk (`E11`) — so the entry file must be present when census runs, and committed
at the measured revision when the counter runs.

### 2.5 Evidence citation and envelope binding (`count-c1.py:145-166`)

For a verb to be exercised, **one** knowledge entry must simultaneously satisfy four things:

1. It matches the verb with `r20.command_pattern` (`verb-coverage.py:99-105`): hyphen or
   underscore form, ASCII token boundaries, case-insensitive. A catalog mention inside a
   list is not enough by itself.
2. It cites the evidence file by **exact full path**. `cited_prefixes` (`:127-129`) returns
   the matched path strings (only a trailing `.` is stripped); the loop condition is
   `path not in cited` (`count-c1.py:154`). Unlike the R20 helper's `is_cited`
   (`verb-coverage.py:132-133`), the R22 measure does **not** expand a directory citation:
   citing `.ufo/waves/round-23/evidence/c1/` alone yields no witness. Fixture
   `directory_citation` expects 0 (`counter-fixtures.py:135,152`).
3. The entry text contains a literal `ev_<64 hex>` id (`HEX64`, `verb-coverage.py:36`) that
   also occurs inside the cited blob; otherwise the pair is skipped (`count-c1.py:157`).
4. `bind_cli` (`:69-99`) accepts the blob: JSON object with `ok` and `data`; `ok is True`;
   no structural refusal anywhere (error/errors, refusal `code`/`status`, non-zero
   `exit_code`); `meta.command` exactly equals the hyphenated verb; `data` is a dict with
   `evidence_id` and `operation`; the operation equals the pinned mapping
   (`debug-with-gdb → gdb_console`, `debug-with-rizin → rizin_debug_command`, else
   hyphen→underscore, `:34-35`); every descendant dict/list is ok/not refused; then
   `r21.bind` requires the id to fullmatch `ev_[0-9a-fA-F]{64}` and the exact operation.
   Duplicate JSON members and NaN/Infinity are unevaluable (`verb-coverage.py:20-27`).

An entry that is eligible but has no bound witness (e.g. the verb is only mentioned, or the
envelope is a refusal) leaves `exercised: false`; the counter still increments `entries`.

### 2.6 What R22 actually produced (retained, not re-run here)

`before-r22-c1.json` (rev `aa1450b`, exit 1) and `verify/final/after-c1.json`
(rev `e9db7e2`, exit 1) both report:

- `t1_exercised: ["identify-flutter-build"]`, `t1_exercised_count: 1`, `t1_total: 6`;
- identify witnesses: `ev_6a84742a…` in `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json`
  and `ev_3458b996…` in `.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`;
- identify `unsupported_candidates`: `identify-godot-run.json`, `identify-godot.evidence.json`
  (metadata/bare extracted data do not bind);
- `inspect-dart-aot`: `entries: 1`, `exercised: false`;
- the other four verbs: `entries: 0`.

Why the Dart entry did not count (OBSERVED): the entry
`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md` is eligible (S055's
used-by names it), but the cited refusal envelope
`.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.envelope.json`
(sha256 `2b13cb8fad6d21fdd9633e8fc28d5e06326c6fe0e119462d54f77966e3c5c145`) has
`ok:false`, `error.code: unsupported_target` and **contains no `ev_` id at all**; the entry
prints only the identify id. So no `(entry, ev, path)` triple binds for that verb.

## 3. Requirements for R23 new-source eligibility (INFERRED from §2 + claim text)

These are normative requirements for a **new** witness counted under
`.ufo/waves/round-23/evidence/c1/`. None is verified yet; no round-23 evidence exists at
this reading.

**R1 — Row placement and shape.** Append the new source as a row inside `## Registry` with
leading and trailing `|` and exactly 11 content columns; no literal `|` anywhere in a cell
(a pipe silently drops the row from the counter and is E01 in census).

**R2 — New id.** `S058` or higher (`int(id[1:]) >= 58`), not colliding with any other id in
the file (duplicate ⇒ the entire measurement is exit 2). Keep the 3-digit zero-padded form;
the counter regex accepts 3+ digits but `S58`/`s058` do not match.

**R3 — Row fields for the new-witness gate.** tier exactly `A` or `B`; status exactly
`mined`; opened exactly `2026-10-21` (the BuildCounter contract fixes this date; census E08
also requires opened ≤ today). `community` may not be tier A (census E10). `kind` must be one
of census's enum (E05) — `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`.

**R4 — Exact used-by.** The `used-by` cell must contain the entry's **exact repo-relative
path** as a bare comma-separated item, with no backticks, trailing period, Markdown link,
angle brackets, glob, directory, or leading `./`. The path must exist on disk when census
runs (E11) and be committed at the measured rev for the counter. Lesson paths are allowed in
the cell but never confer entry eligibility.

**R5 — Entry file.** A committed regular blob under `corpus/knowledge/` whose **first line**
starts exactly `source:` and contains an `S058+` id; the id must be visible on that line
(ids in the body do not count). Prefer `source: S058 <canonical URL or retained path>`.

**R6 — New-witness gate is stricter than the legacy one.** The R22 `measure()` internally
accepts any eligible row ≥ 51. A round-23 entry that cites only `S051`–`S057` (even with a
correct used-by) is "eligible" to the legacy pass but **must not** back a new R23 witness.
The R23 counter must apply, per newly counted witness, the additional predicate:
`id >= 58 AND tier in {A,B} AND status == mined AND opened == 2026-10-21 AND
entry_path in row.used_by`, in addition to the legacy measure's acceptance. This is the
`source linkage absent` / `new source relevance or ownership unsupported` boundary.

**R7 — Evidence location.** The binding envelope must be a committed blob under
`.ufo/waves/round-23/evidence/c1/` (subdirectories are allowed by `startswith`), and the
entry must cite its exact full path. New evidence must not be a copy of the R22 envelopes;
historical evidence remains under `round-22/evidence/c1` and is only read by the R22 pass.

**R8 — Envelope contract.** The envelope must be the original producer CLI envelope:
`ok:true`, `meta.command` exactly the hyphenated verb, `data.evidence_id` `ev_<64 hex>` and
`data.operation` the pinned operation (`identify_flutter_build`, `inspect_dart_aot`,
`gdb_console`, `rizin_debug_command`, `inspect_signal_decoders`,
`decode_signal_recording`), no error/refusal/exit_code anywhere, no duplicate JSON members.
A detached data copy or a derived file has no `meta.command` and cannot bind; a refusal id
printed in an entry is rejected by `bind_cli`.

**R9 — One measured commit.** Entry, `used-by` row, and evidence must all exist at the same
resolved commit passed to `--rev`. Untracked worktree files are invisible to `git show`.
Order: create entry and evidence → append row naming the entry → census `validate` exit 0 →
commit → measure.

**R10 — Census no-harm.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kaidoku` must exit 0 after the append. Practical constraints: E03 no duplicate id; E04 no
same URL+scope unless `teaches` contains `supersedes S###`; E08 opened not future; E11 every
used-by path exists; E12 keep rows in the Registry section. W01/W04 warnings do not fail
exit 0 (the frozen baseline already carries three W04 rows).

**R11 — Attribution, not mere presence.** The new witness must be attributable to a single
round-23 entry that supplies the verb, the exact evidence path and the id, and that entry
must itself satisfy R4–R6. An entry that is merely "eligible" via an old row cannot donate
its eligibility to a new binding.

**R12 — Linkage is not relevance.** Passing R1–R11 establishes local source linkage only.
The claim's `new source relevance or ownership unsupported` falsifier remains manual: the
entry must state its scope and limits, and must not turn static parsing into execution or
dynamic-debugger ownership (this wave has no debugger/Frida/device work).

Minimum compliant chain (template only, **not executed**):

```
| S058 | <title — canonical URL> | docs | A | <scope/limits> | <section/date> | <what it teaches> | mined | 2026-10-21 | 90d | corpus/knowledge/2026-10-21-r23-<slug>.md |
```
```
source: S058 <canonical URL or retained evidence path>
...
<verb> `ev_<64 hex>` `.ufo/waves/round-23/evidence/c1/<file>.json`
```
with `S058.used-by` = `corpus/knowledge/2026-10-21-r23-<slug>.md` (bare, exact).

## 4. Inherited R22 preservation (INFERRED from no-harm + observed pins)

**P1 — R22 counter bytes stay fixed.** `.ufo/waves/round-22/tools/count-c1.py` sha256
`c925918f…b1879`. The R23 counter should pin this digest and load `measure`/`bind_cli` from
the measured commit, not from the worktree.

**P2 — R20/R21 helper bytes stay fixed.** `cfbf1880…` and `61536938…`; `revision_helpers`
(`count-c1.py:50-66`) re-reads them at the measured rev and refuses on digest mismatch
(committed change ⇒ exit 2) while an uncommitted drift must never execute (fixture
`helper_drift` expects the clean 6/6 fixture to still count, `committed_helper_change`
expects exit 2).

**P3 — Retained catalog stays readable.** `.ufo/waves/round-20/verify/round20/verb-coverage.json`
at the measured rev; `r21._measure` requires 153 unique string commands
(`verb-coverage.py` in round-21, catalog validation). Do not substitute installed JS.

**P4 — R22 evidence/c1 stays byte-identical** (seven files at `a3c92eb`):
`identify-flutter-build-saber.envelope.json` `143af76e…4b`,
`identify-flutter-build-saber.run.json` `6b2c24d9…8f`,
`identify-godot-run.json` `5c3d94f8…88`,
`identify-godot.envelope.json` `1ea324b2…0a`,
`identify-godot.evidence.json` `397aeeb7…4f`,
`inspect-dart-aot-saber.envelope.json` `2b13cb8f…45`,
`inspect-dart-aot-saber.run.json` `d1eaa23f…4a`.
The two identify envelopes are the historical witness pair.

**P5 — R22 knowledge entries stay byte-identical**:
`2026-10-21-r22-flutter-static-boundary.md` `405ab83c…21334` and
`2026-10-21-r22-flutter-positive-dart-refusal.md` `417482ef…c7dd8`.
Editing either first line or its body can drop the historical witness.

**P6 — SOURCES rows S001–S057 unchanged.** Digest `5ae5e7ed…ebd` at `a3c92eb`; the R22
verifier recorded `old_rows_identical: true` (`source-rows.json`). Do not add a round-23
entry path to an S051–S057 used-by; that would both violate no-harm and let a new entry
masquerade as legacy-eligible.

**P7 — The R22 pass must keep R22 semantics.** Call `measure()` with
`EVIDENCE_PREFIX = ".ufo/waves/round-22/evidence/c1/"` and the legacy ≥51 eligibility (do
**not** apply the S058 gate to the historical pass). It must reproduce k=1 with the same two
identify witnesses; a lower result is the `inherited identify lost` falsifier.

**P8 — Union by verb, not addition.** Final `k = |{verb exercised in either pass}|`; a new
identify witness cannot raise k (`same verb double counted`); report `k/6` and the exact
incomplete count `6-k`; exit 0 only at 6/6, 1 when incomplete, 2 when unevaluable; no
mastery preclaimed.

**P9 — Isolation properties.** Clear inherited `GIT_*`, set
`GIT_NO_REPLACE_OBJECTS=1` (`count-c1.py:190-194`), resolve one commit, never import the
measured tree's helper bytes without the digest check, and never fall back to worktree code.

**P10 — Mentions are not holds.** `catalog_zero`/`catalog_mentioned_count` are recomputed
from the retained catalog and will change when round-23 entries mention new verbs. Mention
growth must never be reported as exercised coverage; `entries` counts mention-only and
ineligible entries too.

**P11 — Do not touch R22 frozen artifacts.** `.ufo/waves/round-22/frozen/` (including
`expected-v2.json` sha256 `1abdd9df…0bb8`, which the R22 `--selftest` pins) and the frozen
counter copies remain as retained. R23 selftests must be separately authored inputs and
expected outcomes (QUALITY 28/32), not calls to the legacy fixture builder.

## 5. Failure modes the counter author/L1 must actively avoid

- **F1 — truncated witness list.** `bound_evidence` is `witnesses[:5]` and carries no entry
  path (`count-c1.py:161-166`). Applying the S058 gate from this list alone can miss a
  witness or attribute it to the wrong entry. The R23 wrapper needs its own entry-level
  attribution while reusing `bind_cli` for the actual binding decision.
- **F2 — duplicate source id aborts everything.** One duplicated S-id anywhere yields
  `unevaluable` (exit 2), including two identical rows.
- **F3 — silent row drop.** An extra `|` in a cell removes the row from counter eligibility
  with no exit-2 signal; census E01 is the only detector. Check both.
- **F4 — first-line-only source.** A title-first entry is ineligible (fixture
  `source_not_header`, expected 0), even if `source: S058` appears below.
- **F5 — exact used-by.** Backticks, a trailing period, a Markdown link, a glob or a
  directory all fail (mirror §2.4); a filename containing a comma or space is unusable.
- **F6 — directory citation.** R22 measure does not expand `.../c1/` citations; the exact
  `.json` path must appear in the entry.
- **F7 — refusal without an id.** A refused envelope may carry no `ev_` id (the Dart case);
  citing its path cannot bind, and printing a refusal id would still be rejected.
- **F8 — text-keyed eligibility.** Identical entry bytes at another path inherit
  eligibility (set of texts); do not treat a distinct path as proof of its own linkage.
- **F9 — id-shaped filenames.** `S0\d\d` inside a cited path on the source line is parsed
  as an additional source id; it is harmless only while the exact used-by match is still
  required, but it can make a debugging output look like an S058 link.
- **F10 — non-ASCII boundary.** The source-line id regex is not ASCII-flagged; a non-ASCII
  word character adjacent to the id suppresses the match.

## 6. Unknowns

- **U1.** `.ufo/waves/round-23/tools/count-c1.py` does not exist at this reading; the
  claim's `counting_command` is prospective. No R23 counter behavior was observed.
- **U2.** The BuildCounter seat's S058+ gate implementation, and whether it rejects an
  entry that is legacy-eligible only via S051–S057, is unobserved.
- **U3.** The new S058+ rows/URLs are not chosen (SourceRegistry seat); id collision and
  census E04 outcomes are unknown until the rows exist.
- **U4.** `.ufo/waves/round-23/evidence/c1/` does not exist yet; no new witness exists;
  the inherited measured state remains k=1 (identify only).
- **U5.** Source relevance and scope admission remain manual; no dynamic debugger/Frida
  ownership is established by any source row in this wave.
- **U6.** Whether the measured revision for R23 will include all entries/rows/evidence is
  an L1 integration step; a rev that omits any of them silently changes eligibility.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CounterSources.md`
  — this report; no other output was produced (read-only seat).
  Report sha256 (body bytes, excluding this one line): `cdc99cde1f598609cc0f3d8d1a89165df141b88e9efcb439521f5a3b53ab63b2`

## Installs

None. No tool was installed, upgraded, or configured; no package manager was invoked.

## Open risks

- The R23 counter can be written to pass a shape check while still accepting an
  S051-only entry as a "new" witness if the gate is applied only to the union boolean
  (F1/R6). That is the main vacuity risk and needs a named negative control (round-23
  entry citing S057 with correct used-by must not raise k).
- Silent row-shape failure (F3) can make a legitimate new source vanish without an exit-2;
  only census E01 plus an explicit per-verb `entries/witnesses` report exposes it.
- Copying or editing R22 artifacts would make P4–P7 unverifiable; all R22 bytes must be
  pinned by digest before any integration commit.
- A same-verb new witness on identify can look like progress if the output reports witness
  totals instead of `t1_exercised_count`; the exit contract must stay verb-union based.
