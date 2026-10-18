# CR3 — C3 attack: dispositions must be auditable, not labels

**Verdict — PARTIAL REFUTE.** The carried-debt trail shows real safe landings, but the landed records alone do not prove a complete per-item disposition of the R1–R4 missed-item set. A three-label register is verifiable only if it is an atomic, source-anchored crosswalk with evidence and closure criteria. If a compound source bullet gets one label, or an item disappears from a later carried-debt paragraph, that is paperwork, not disposition.

**Axes:** completeness; evidence-backed classification; safe landing / no-silent-retirement.

## Evidence and re-derivation

I archived the record commits (no checkout) and printed the relevant lines from those trees. Exact commands:

```sh
W=/var/tmp/arc2-l5r5-CR3-records-20261018165408-3830616
for spec in 'r1 165057e' 'r2 679af5d' 'r3 158a966' 'r4 0e8c96b'; do
  set -- $spec; mkdir -p "$W/$1"
  git archive --format=tar "$2" SCORECARD.md LOG.md PROVINCE.md SKILL.md corpus/README.md corpus/lessons/2026-10-15-round-1.md corpus/knowledge/2026-10-13-mcp-registrations.md corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md | tar -xf - -C "$W/$1"
done
python3 - "$W" <<'PY'
from pathlib import Path
import sys
w=Path(sys.argv[1])
for rev, specs in {
 'r2':[('LOG.md',1058,1065)],
 'r3':[('LOG.md',1111,1116)],
 'r4':[('LOG.md',1133,1158),('SCORECARD.md',919,933)],
}.items():
 print(f'[{rev}]')
 for file,a,b in specs:
  lines=(w/rev/file).read_text().splitlines()
  print(f'{file}:{a}-{b}')
  for i in range(a,min(b,len(lines))+1): print(f'{i}: {lines[i-1]}')
PY
```

Observed excerpts from those archived trees:

```text
[r2] LOG.md:1058-1063
- Carried debt: SCORECARD.md:270 stale `:157` parenthetical; MINT.md:10,
  corpus/QUALITY.md:18, lessons/2026-10-15-round-1.md:82,
  corpus/knowledge/2026-10-13-mcp-registrations.md:9,:80,:88 (dead
  `:1284/:1287` pointers), r4-16-frontier-rescan.md:43; SCORECARD.md:291
  (dated, historical); systemd user env + ~/.bash_profile carrier limits;
  Kimi-side rea load probe.
[r3] LOG.md:1111-1114
- Carried debt: LOG.md:1005/:1018 receipt-anchored :2940 references (named
  correction = this entry); lessons/2026-10-15-round-1.md:82; errata-internal
  dead-token rise (unit stated); E22 census scope drift; C3 probe debt; E11's
  unreproduced 0-byte probes; the 17.7MB agent-browser PE rung (unrun).
[r4] LOG.md:1133-1136
- C3 freshness — LANDED at `265e1aa`: census v10 ... PASS 0/0/0/0 at the work tree; lessons:82
  append-only erratum ...
LOG.md:1141-1146
- Round infrastructure — the decisive 91.6MB PE run ... OOM-killed ...
  next attempt: REA_GHIDRA_DISABLED_ANALYZERS + worker reduction.
LOG.md:1154-1157 / SCORECARD.md:920-926
- Carried debt: lessons:37 / LOG.md:685 / rubric.json:61 ...; 60/64 dispatch defect;
  probe frozen-guard ...; GhidraClient.js:607 ...; E22 v9's superseded fence ...
```

The R2 list is not one item: it combines already adjudicated `SCORECARD.md:270`, several distinct pointer loci, an explicitly historical record, two environment-carrier limits, and a live-load probe. The R3 list also mixes outcomes. The R4 records verify three concrete landings from that R3 bundle: the lessons erratum, census v10, and citation-drift probe (`LOG.md:1127-1136`; `.ufo/gates/c1-census-v10.py`; `.ufo/gates/citation-drift/`). The archived R4 carried-debt summary still names other discrete obligations (`SCORECARD.md:919-926`, `LOG.md:1154-1157`).

Two R3 leaves have no closure evidence in the R4 carried-debt summary: E11's two 0-byte `configuration_invalid` probes and the unrun 17.7 MB `agent-browser` rung (`LOG.md:1111-1114`). The R4 wave report mentions a *different* possible 0-byte scratch-capture hazard and asks for a parent spot-check (`.ufo/waves/arc2-loop1-round4/V3.md:109,242`); that is not evidence that E11's two probe outcomes were reproduced or dispositioned. A content search found the R3 references in `LOG.md:1114` and `SCORECARD.md:849`; the R4 report's carried-debt block at `LOG.md:1154-1157` does not include either item. This proves a traceability gap in the landed summaries, not that no separate R5 row exists.

The safe landings are independently inspectable: R2's record identifies the README-label / SCORECARD-pointer repairs and Kimi-pin/custody updates (`LOG.md:1017-1040`); R3 identifies the content-anchored pointer errata (`LOG.md:1077-1083`); R4 identifies the lesson, census and probe landings (`LOG.md:1127-1136`). The changed files are in the cited commits' archived trees. Example current anchors: `PROVINCE.md:8-18`, `corpus/README.md:90`, `SKILL.md:219-243`, `corpus/knowledge/2026-10-13-mcp-registrations.md:92-111`, `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:938-975`, and `corpus/lessons/2026-10-15-round-1.md:190-206`.

Searches run:

- `Grep` pattern `0-byte|zero-byte|17\.7 ?MB|agent-browser|17\.7MB` in `LOG.md` returned `LOG.md:1114` only.
- Same pattern in `SCORECARD.md` returned `SCORECARD.md:849` (E11's two 0-byte probes); it did not return the 17.7 MB rung.
- Same pattern in `.ufo/waves/arc2-loop1-round4` returned V3's hazard/spot-check note at `V3.md:109,242`, not an E11 re-run or 17.7 MB run.

I read, but did not run, `.ufo/gates/c1-census-v10.py`: it reads live home config files in `live_pins()` (`:74-77`, `:124-134`, `:377-380`). No live probes were run this round, so I make no fresh census-PASS claim; the safe-landing checks above are static archive/file-state checks.

## What makes C3 verifiable

The three dispositions are useful triage, not closure proof. The register must preserve one row per atomic source finding, with: immutable origin (round/seat and source path:line or content anchor), exact claim/failure mode, the item-specific disposition and rationale, evidence, and an explicit closure/reopen test. Compound bullets must split whenever their leaves have different outcomes. Add a separate terminal state for already-landed or adjudicated items; `landable-now` is not the same as `landed`, and a no-change adjudication is not a debt label. `named-debt` requires a named owner and reopen trigger. `operator-owned` requires evidence for the boundary and a no-edit statement; with no live probe, current live state remains unknown.

A valid audit should report a source-item denominator and reconcile every item from the frozen R1–R4 inputs to exactly one row. Merely counting filled disposition cells cannot detect omitted debt or laundering a compound into one convenient label.

## Text for the parent to land VERBATIM

```text
C3 disposition acceptance rule: freeze the R1–R4 source-item list before assigning statuses, then reconcile every atomic finding to one register row keyed by its source round and stable path/content anchor. Split compound bullets where their leaves have different outcomes. Each row records the exact claim, disposition (landable-now / named-debt / operator-owned), evidence, rationale, and closure or reopen test. Track outcome separately: landed, adjudicated-with-cause, or still-open; never call an already-landed item “landable-now.” A named debt needs an owner and reopen trigger. An operator-owned item needs evidence for the ownership boundary and an explicit no-edit disposition; absent a permitted live check, its current live state is unknown. C3 passes only when the frozen source denominator is fully cross-walked, each status is evidence-backed, and all safe landings have an independently checkable before/after proof. A missing row or a label without its evidence is unresolved, not dispositioned.
```

## Conclusions

- **OBSERVATION:** R2 and R3 carried-debt bullets contain multiple independently actionable leaves (`LOG.md:1058-1063`, `1111-1114`).
- **OBSERVATION:** R4 records three safe R3 landings, while its carried-debt summary does not carry forward the E11 0-byte probes or the unrun 17.7 MB rung (`LOG.md:1127-1136`, `1154-1157`; `SCORECARD.md:919-926`). V3 requests a spot-check, not a disposition.
- **INFERENCE:** A labels-only register can pass while omitting findings or collapsing mixed-state bullets; the landed record trail does not independently establish completeness. The work is verifiable if the register uses the acceptance rule above and includes a frozen denominator.
- **UNKNOWN:** Whether the concurrent R5 register has separate rows and evidence for these dropped leaves; whether E11's probe failures were reproduced elsewhere; whether the 17.7 MB rung was intentionally retired or remains open. No live check was made, by instruction.
