# CriticSource — R22-C1 S051+ source predicate (author-side critic, not admission)

Seat `KaidokuR22R.CriticSource-6`, a recovery W2 leaf. This is not a returned W1 seat. Lane HEAD is `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`, baseline B is `7787fea4d6fd718726de92ed20759d11ce7b8b48`, and the freeze commit is `75f04a446c61761182145c058e545551ca4ecd76`. Every mutation ran in a private `/tmp` git clone that was deleted afterwards. The lane was not written apart from this report and `CriticSource.json`. I ran no REA calls, opened no network or device connection, and installed nothing (no tool installs and no pacman transactions).

Axes judged: **coverage** and **calibration**.

## Verdict

The S051+ predicate (`count-c1.py:43-58`) only checks that a source row is *linked* to the entry. It never checks that the row is *primary-source support* for the counted verb. In a scratch clone, four counterexamples kept `identify-flutter-build` counted, or added a verb, with no real round-22 primary source. The census gate in `no_harm` rejects none of them. On the current authored evidence the measured result is not inflated: the single counted verb really is cited by S051 (docs) and S052 (docs). The defect is latent, and C1's "sourced" claim reads stronger than the predicate enforces.

## Commands and observed exits (all read-only on lane objects)

| argv | exit | observed |
|---|---|---|
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev 7787fea` | 1 | `t1_exercised_count 0`, `catalog_zero_count 20` (matches `claims.json:19` before_expected) |
| same `--rev 75f04a4` | 1 | 0/6, zero 20 |
| same `--rev 2ee3d9f` | 1 | `t1_exercised ["identify-flutter-build"]`, 1/6, zero 19; bound `ev_3458b996…866b` in `evidence/c1/identify-godot.evidence.json` |
| `git show 75f04a4:.ufo/waves/round-22/tools/count-c1.py > tmp; python3 -I -B tmp --root <LANE> --rev 7787fea` / `--rev 2ee3d9f` | 1 / 1 | 0/6 / 1/6 (the frozen counter gives the same numbers at both revisions) |
| `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --selftest` | 0 | `counter_controls_clean`; all_six 6, missing_source 0, refusal/split/uncited/duplicate 0 |
| `python3 -I -B .ufo/waves/round-22/tools/counter-fixtures.py --claim C1 --counter .ufo/waves/round-22/frozen/count-c1.py --root <LANE>` | 1 | `counter_controls_failed`; missing_source exit 0 count 6 (the red reproduces) |
| same with `--counter .ufo/waves/round-22/tools/count-c1.py` | 0 | `counter_controls_clean` |
| `sha256sum frozen/count-c1.py tools/count-c1.py` | 0 | `d7f67075…04aa` (= `75f04a4` blob) vs `5fbc6868…dd61` |
| `sha256sum frozen/count-c2.py tools/count-c2.py` | 0 | `d3bec8db…3096` (= `75f04a4` blob) vs `0d51a87f…7f47` |
| scratch mutation driver `python3 -I -B /tmp/kaidoku-r22-criticsource/mutate.py` (source below) | 0 | the 13 rows below; every per-mutation counter exit was 1, stderr empty |

## Mutation results (base `2ee3d9f`, counter `tools/count-c1.py` inside the clone)

| mutation | count | predicate correct? | census (`scripts/sources-census.sh`) catches? |
|---|---|---|---|
| control_unmodified | 1 | — | — |
| **own_work_only** — the entry's `source:` line cites only S053, the lane's own evidence file | **1** | **no**: self-citation counts as sourced | no (`own-work` is a valid kind, tier A allowed; census l.655) |
| **fabricated_tierC_row_only** — new `S054 \| nothing opened \| own-work \| C \| none…\| mined \| 2026-10-21` with the entry in used-by; entry cites only S054 | **1** | **no**: kind, tier, source and anchor are never read | warning W01 only; warnings never change status (census l.17-18, 31) |
| **flutter_docs_row_sources_gdb_verb** — new entry mentions `debug-with-gdb`, cites S051 (Flutter build-modes) and a 2-member record `{"evidence_id":"ev_c…c","operation":"debug_with_gdb"}` in `evidence/c1/gdb.json`; S051 used-by gains that entry | **2** (adds debug-with-gdb) | **no**: eligibility is per entry, not per verb; Flutter docs "source" a gdb verb | no |
| negated_prose_cite — `source: none; S051 was not consulted` | 1 | weak: any `S###` token in the line counts | n/a |
| source_line_in_body_only — frontmatter line removed, `source: S051` appended to the body | 1 | weak: first `source:` line anywhere in the file | n/a |
| row_outside_registry_in_leads — S051 row placed under `## Leads`, Registry rows stripped of the entry | 1 | no | **yes**: E12 |
| duplicate_id_later_row_wins — second `S051` (tier C) added with the entry in used-by | 1 | no (dict overwrite, l.48) | **yes**: E03 |
| gfm_escaped_pipe_drops_rows — `\|` inside the teaches cell | 0 | drops the row silently | **yes**: E01 NF≠13 (contract-consistent) |
| round22_row_opened_next_day — `opened 2026-10-22` | **0** | stricter than the claim: a round-22 row is lost | no (valid date) |
| used_by_excludes_entry | 0 | correct | — |
| status_not_mined (`screened`) | 0 | correct | — |
| pre_round_row_S050 (entry cites S050 with matching used-by) | 0 | correct | — |

Separability probe (scratch clone): starting from B, I checked out only C1's declared `touches` plus the counters from `2ee3d9f` (`tools/`, `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`, `evidence/c1/`). Result: **0/6, exit 1**. After also checking out `corpus/SOURCES.md`: **1/6, exit 1**.

## Findings

### F1: the predicate checks linkage, not primary-source support (coverage and calibration)

- **Where:** `count-c1.py:47` reads only `cells[1]` id, `cells[8]` status and `cells[9]` opened. It never reads `cells[3]` kind, `cells[4]` tier, `cells[2]` source or `cells[6]` anchor.
- **Same blind spot in the fixtures:** the C1 positive fixture uses an `own-work` row as its "source" (`counter-fixtures.py:53`), so the controls encode self-citation as valid.
- **Counterexamples:** own_work_only, fabricated_tierC_row_only and flutter_docs_row_sources_gdb_verb above. S053 (`SOURCES.md:59`) is `own-work`, and its source *is* `evidence/c1/identify-godot.evidence.json`, the very record `bind` counts. So the "sourced" condition can be met by the same artifact that the evidence condition already requires.
- **Claim impact:** `claims.json:13` ("cite S### rows opened in round 22") is literally satisfied. `corpus/lessons/round-22.md:13` "Primary source text teaches limits", however, is not enforced by the counter.
- **Smallest safe correction (fixable defect):**
  1. In `count-c1.py:47`, also require `cells[3] != "own-work"`, or at minimum require `cells[4] == "A"` together with at least one non-own-work row among the entry's cited rows.
  2. Change fixture row S051 (`counter-fixtures.py:53`) to kind `docs`.
  3. Add fixture mutants `own_work_only` (expect exit 1, count 0) and `tier_c_row` (expect exit 1, count 0).
- **Effect on the current result:** the entry also cites S051 and S052 (kind `docs`, tier A, `SOURCES.md:57-58`), so the measured 1/6 still holds after this change. I have not run the patched counter; that outcome is inference.

### F2: sourcing is per entry, not per verb (calibration; a tradeoff for the judge)

- **Where:** `count-c1.py:50-58` builds `eligible` once per entry. Any verb mentioned in an eligible entry then inherits that entry's source rows (`:59-72`).
- **Counterexample:** flutter_docs_row_sources_gdb_verb (count 2).
- **Why this is a tradeoff, not a fix:** topical support cannot be checked mechanically without a scope-to-verb contract. Requiring a row's scope or teaches cell to name the verb would also fail the current S051 and S052 rows, whose scope cells don't name `identify-flutter-build`.
- **Smallest safe correction:** in the `count-c1.py:7-8` docstring and any C1 verdict, say "the entry cites a mined round-22 row whose used-by names it". Do not say "primary-source support". The canonical judge should treat source *relevance* as un-gated.
- The fabricated 2-member record in that mutant also relies on round-21 `bind` being local binding only (declared at `count-c1.py:10`). That limit is outside this seat's scope.

### F3: separability statement is false for C1 (calibration and identity)

- **Where:** `claims.json:36` says "C1 counter reads only corpus/knowledge and evidence/c1". But `count-c1.py:44` reads `corpus/SOURCES.md`, and the counter also loads round-20/21 helper code from the working-tree `--root` rather than from `--rev` (`count-c1.py:26-35`).
- **Missing touch:** `claims.json:22` C1 `touches` omits `corpus/SOURCES.md`.
- **Observed:** C1's touches alone give 0/6; adding `SOURCES.md` gives 1/6.
- **Smallest safe correction:** the C1 isolated-diff verification must include the S051–S053 rows in `corpus/SOURCES.md` (and `corpus/lessons/round-22.md` if a used-by path must exist on disk for census E11). Record that dependency in the verification receipt. `claims.json` is frozen and is not edited here.

### F4: post-freeze counter change with ambiguous authority and red provenance (identity and false provenance)

- **Where:**
  - `tools/count-c1.py` and `tools/count-c2.py` differ from their freeze-commit bytes, which are kept in `frozen/` (hashes above).
  - `claims.json:18,28` bind the *path* `.ufo/waves/round-22/tools/count-c{1,2}.py`, not a hash. Both `frozen/` and `tools/` are tracked, so there are two candidate counters.
  - The change is declared (`corpus/lessons/round-22.md:47-60`).
- **Monotonicity (observed and by reading):**
  - The C1 successor is a pure filter. `eligible` is a subset of all entries, and the witness loop is the same as round-21 `_measure`, so it can only lower the count.
  - The frozen and successor counters give identical results at B (0/6) and at `2ee3d9f` (1/6).
  - Leftover output inconsistency: `targets[verb].entries` and `unsupported_candidates` still come from the unfiltered round-21 pass (seen at `2ee3d9f`: entries 1, unsupported 2).
- **Provenance defect:**
  - `verify/red-C1.json` and `verify/red-C2.json` record argv `--counter …/tools/count-c1.py` and `…/tools/count-c2.py`, but `corpus/lessons/round-22.md:49-50` says the red came from `--counter .ufo/waves/round-22/frozen/count-c1.py`.
  - Re-running the recorded red-C1 argv today exits **0**, clean. It no longer reproduces the stored exit 1.
  - The red reproduces only with `frozen/count-c1.py` (exit 1, missing_source count 6).
  - Neither record carries a counter sha256. [INFERENCE] The red was captured while `tools/` still held the frozen bytes; `frozen/` and `red-*.json` share the 09:51 mtime.
- **Smallest safe correction:**
  1. Re-record both red controls with the argv naming `frozen/count-c{1,2}.py`, together with that file's sha256 (`d7f67075…`, `d3bec8db…`).
  2. Record the successor sha256 (`5fbc6868…`, `0d51a87f…`) in the delivered green receipts.
- **For the canonical judge:** whether a declared, strictly narrowing post-freeze counter is admissible is the judge's call, not a fixable defect.

### F5: date literal is stricter than the claim (coverage risk, false negative only)

- **Where:** `count-c1.py:47` uses `cells[9] == "2026-10-21"`, while `claims.json:13` says "opened in round 22 (S051 onward)".
- **Observed:** round22_row_opened_next_day gives 0. A W2 report arriving after the date rollover that opens a new S05x row for a T1 verb would be dropped.
- **Why the date check is redundant:** baseline `SOURCES.md` ends at S050 (`git show 7787fea:corpus/SOURCES.md | grep -c '^| S05'` gives 1, the S050 row), so `id >= 51` already marks the round boundary.
- **Smallest safe correction:** replace the equality with `cells[9] >= "2026-10-21"` (ISO comparison), or drop the date and keep id≥51 plus "row absent at baseline".

### F6: minor parser looseness, low severity (calibration)

- Any `S###` token in the first line that starts with `source:`, anywhere in the file, qualifies (`count-c1.py:55-56`). The negated_prose_cite and source_line_in_body_only mutants both count.
- **Correction:** take only the first line of the file when it starts with `source:`, and match only ids followed by a URL or path token. Optional.
- Duplicate ids, rows outside the Registry, and escaped pipes are accepted or dropped by the counter, but the `no_harm` census gate rejects them (E03, E12, E01). These are mitigated, provided the census exit is actually checked at final.

## Primary-source support of S051–S053 (judged only on authored evidence)

| row | kind / tier | supports what in the entry | local verifiability |
|---|---|---|---|
| S051 Flutter build modes (`SOURCES.md:57`) | docs / A | the entry's "debugging information is stripped" limit (entry l.13); quote in `corpus/lessons/round-22.md:11` | **unknown**: no retained page copy or fetch receipt in the lane (rg for `build-modes` hits only knowledge, lessons, SOURCES and wave prompts). It was not reopened, because the contract forbids remote connections. |
| S052 Android NDK ABIs (`SOURCES.md:58`) | docs / A | the `/lib/<abi>/lib<name>.so` convention (entry l.13); quote in `corpus/lessons/round-22.md:12` | **unknown**, same as S051 |
| S053 own-work (`SOURCES.md:59`) | own-work / A | the parsed negative itself | verifiable locally but circular for "sourced" (F1) |

Neither S051 nor S052 bears on `identify-flutter-build`'s operation. They bound its interpretation, and the entry says so itself (l.13). That matches the claim's limited scope but is not verb-level support (F2).

The S051 teaches cell ends with "static APK metadata does not establish source recovery". That is lane inference written inside a tier-A docs row, not text from the page (`corpus/lessons/round-22.md:11` quotes only "Debugging information is stripped out."). **Correction:** move the clause to the knowledge entry's Inference paragraph, or mark it as lane inference. Prior SOURCES rows must stay byte-identical, so only the new S051 row is affected.

## Impacted axes

- **coverage:** F1, F2, F5, F3.
- **calibration:** F1, F2, F3, F4, F6.

## Scratch mutation driver (deleted from /tmp after the run; reproduce verbatim)

```python
#!/usr/bin/env python3
"""Scratch-clone mutations of R22-C1's S051+ source predicate. Never touches the lane."""
import json, subprocess, sys, tempfile
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67"
ENTRY = "corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md"
SRC = "corpus/SOURCES.md"
COUNTER = ".ufo/waves/round-22/tools/count-c1.py"
GDB_ID = "ev_" + "c" * 64

def sh(*argv, cwd):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=True).stdout

def rows(text):
    return {l.split("|")[1].strip(): l for l in text.splitlines() if l.startswith("| S05")}

def set_cell(line, index, value):
    cells = line.split("|"); cells[index] = " " + value + " "; return "|".join(cells)

def set_used_by(line, value):
    return set_cell(line, 11, value)

def mutations(entry, sources):
    r = rows(sources); src_line = entry.splitlines()[0]; out = {"control_unmodified": {}}
    out["own_work_only"] = {ENTRY: entry.replace(src_line, "source: S053 `.ufo/waves/round-22/evidence/c1/identify-godot.evidence.json`")}
    fabricated = "| S054 | nothing opened | own-work | C | none | none | none | mined | 2026-10-21 | on-release | " + ENTRY + " |"
    out["fabricated_tierC_row_only"] = {ENTRY: entry.replace(src_line, "source: S054"), SRC: sources.replace(r["S053"], r["S053"] + "\n" + fabricated)}
    out["negated_prose_cite"] = {ENTRY: entry.replace(src_line, "source: none; S051 was not consulted")}
    out["source_line_in_body_only"] = {ENTRY: entry.replace(src_line + "\n", "") + "\nsource: S051\n"}
    stripped = sources
    for sid in ("S051", "S052", "S053"):
        stripped = stripped.replace(r[sid], set_used_by(r[sid], "corpus/lessons/round-22.md"))
    out["row_outside_registry_in_leads"] = {SRC: stripped.replace("## Leads (unopened)\n", "## Leads (unopened)\n\n" + set_used_by(r["S051"], ENTRY) + "\n")}
    s053s = set_used_by(r["S053"], "corpus/lessons/round-22.md")
    out["duplicate_id_later_row_wins"] = {SRC: stripped.replace(s053s, s053s + "\n" + set_cell(set_used_by(r["S051"], ENTRY), 4, "C"))}
    gdb_path = "corpus/knowledge/2026-10-21-r22-gdb-unrelated.md"
    out["flutter_docs_row_sources_gdb_verb"] = {
        gdb_path: f"source: S051 https://docs.flutter.dev/testing/build-modes (Release)\nverified-at: 2026-10-21\nrecheck: none\n\ndebug-with-gdb {GDB_ID} .ufo/waves/round-22/evidence/c1/gdb.json\n",
        ".ufo/waves/round-22/evidence/c1/gdb.json": json.dumps({"evidence_id": GDB_ID, "operation": "debug_with_gdb"}),
        SRC: sources.replace(r["S051"], set_used_by(r["S051"], r["S051"].split("|")[11].strip() + ", " + gdb_path))}
    piped = dated = status = sources
    for sid in ("S051", "S052", "S053"):
        piped = piped.replace(r[sid], set_cell(r[sid], 7, r[sid].split("|")[7].strip() + " (a \\| b)"))
        dated = dated.replace(r[sid], set_cell(r[sid], 9, "2026-10-22"))
        status = status.replace(r[sid], set_cell(r[sid], 8, "screened"))
    out["gfm_escaped_pipe_drops_rows"] = {SRC: piped}
    out["round22_row_opened_next_day"] = {SRC: dated}
    out["used_by_excludes_entry"] = {SRC: stripped}
    out["status_not_mined"] = {SRC: status}
    s050 = next(l for l in sources.splitlines() if l.startswith("| S050 "))
    out["pre_round_row_S050"] = {ENTRY: entry.replace(src_line, "source: S050"), SRC: sources.replace(s050, set_used_by(s050, s050.split("|")[11].strip() + ", " + ENTRY))}
    return out

def main():
    results = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r22-criticsource-") as d:
        clone = Path(d) / "lane"
        sh("git", "clone", "-q", "--no-checkout", LANE, str(clone), cwd=d)
        sh("git", "checkout", "-q", REV, cwd=clone)
        sh("git", "config", "user.name", "critic", cwd=clone); sh("git", "config", "user.email", "critic@invalid.local", cwd=clone)
        entry = (clone / ENTRY).read_text(); sources = (clone / SRC).read_text()
        for name, files in mutations(entry, sources).items():
            sh("git", "checkout", "-q", "-f", REV, cwd=clone); sh("git", "clean", "-qfd", cwd=clone)
            for rel, text in files.items():
                p = clone / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text)
            sh("git", "add", "--all", cwd=clone); sh("git", "commit", "-qm", name, "--allow-empty", cwd=clone)
            rev = sh("git", "rev-parse", "HEAD", cwd=clone).strip()
            proc = subprocess.run([sys.executable, "-I", "-B", str(clone / COUNTER), "--root", str(clone), "--rev", rev], capture_output=True, text=True)
            try: data = json.loads(proc.stdout)
            except ValueError: data = {}
            results.append({"mutation": name, "exit": proc.returncode, "t1_exercised": data.get("t1_exercised"), "t1_exercised_count": data.get("t1_exercised_count"), "stderr": proc.stderr[-400:]})
    print(json.dumps({"base_rev": REV, "counter": COUNTER, "results": results}, indent=1))

if __name__ == "__main__":
    main()
```

Raw per-mutation outputs are in `CriticSource.json`.

## Blockers and unknowns

- I could not verify the live page content of S051 and S052 locally, because the contract forbids remote connections and the lane keeps no page copy.
- Every patched counter outcome named under "Smallest safe correction" is inference; none was run.
- Later W2 reports were not considered.
