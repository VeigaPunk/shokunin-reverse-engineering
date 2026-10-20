# Round 14 — BaselineMeasures (factual baseline, counting only)

- Lane: `KaidokuR14.BaselineMeasures` (leaf; no subagent dispatch; no tests, gates, builds or linters run)
- Measured revision: `767adafb97e2eef6980e2ad873d357e16721c467` (HEAD, `round-13: integrator admits verified source-curation capability only`)
- Access date: 2026-10-20 (UTC; `date -u` at measurement: 2026-10-20T05:15:13Z)
- Working tree: `git status --porcelain` = `?? .ufo/waves/round-14/` only. `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md` match HEAD (`git diff --stat HEAD` empty), so working-tree reads of those paths equal the pinned commit.
- Not committed: this report is an untracked write; no git state was changed.
- Tools: none installed or upgraded. Used pre-existing `git`, `python3` 3.14.7, `gawk`, `sha256sum`, `grep`, `find`. Nothing needed installing under RULES.md.
- Network: none used. S004/S005 URL rows were not opened.

## 1. Command A — knowledge count and coverage-map index

Recipe A is the body of `SCORECARD.md` "Measurement recipes" (HEAD lines 86–125). It reads Git objects only and was run unmodified with `REV` set to HEAD:

```
$ REV=767adafb97e2eef6980e2ad873d357e16721c467
$ python3 - "$REV" <<'PY'
... recipe A body (SCORECARD.md at HEAD, lines 90-125) ...
PY
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 91, "mapped": 91, "missing": [], "revision": "767adafb97e2eef6980e2ad873d357e16721c467", "rule_blocks": 17}
```

Supplementary prints from the same run:

```
map_tokens_total_occurrences 95 distinct 91
rule_block_count_raw 17
```

Tree cross-check:

```
$ git ls-tree -r --name-only $REV -- corpus/knowledge | grep -c '\.md$'
91
$ git ls-tree -r --name-only $REV -- corpus/knowledge | grep -vc '\.md$'
1          # corpus/knowledge/.gitkeep
```

Findings:
- Knowledge `.md` files: 91. Mapped: 91. Missing from map: none. Dangling map tokens: none.
- Coverage proxy 10.0. Per SCORECARD, this is index integrity only, not domain coverage.
- Queue-drain rule blocks: 17; citation-resolved: 17; depth proxy 10.0.
- The 95 map-token occurrences name 91 distinct files; 4 tokens repeat across rows. The set comparison is unaffected.

## 2. Source registry — `corpus/SOURCES.md` at HEAD

Census, as recorded in `.ufo/waves/round-14/claims.json` `before_census`:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

Matches the `before_census` output in `claims.json` (same line, exit 0).

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	rows	22
kaidoku	tier.A	20
kaidoku	tier.B	1
kaidoku	tier.C	1
kaidoku	status.mined	21
kaidoku	status.rejected	1
FLEET	rows	22        (FLEET missing 0; tier.invalid 0; status.queued 0; status.invalid 0)
exit=0
```

Independent recount from the pinned object (`git show $REV:corpus/SOURCES.md`, awk over `| Sxxx |` rows; column 5 = tier, column 9 = status):

```
rows=22
tier A=20
tier B=1   (S016, Trail of Bits write-up)
tier C=1   (S022, rejected, JSC Decompiler)
status mined=21
status rejected=1   (S022)
ids: S001 … S022 (contiguous)
```

Go-related rows (C1 ground):

| id | tier | status | kind | note |
|---|---|---|---|---|
| S003 | A | mined | code | Ghidra 12.1.4 Base source archive (local path); SHA-256 in row |
| S004 | A | mined | code | GP-6528 Go 1.26 commit (URL; not opened here) |
| S005 | A | mined | code | GoReSym README at commit d7f23b7 (URL; not opened here) |
| S006 | A | mined | docs | BSim tutorial (local path) |

Local hash check (no network):

```
$ sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804  (7,481,132 bytes)
```

Equals the S003 digest in the registry row. S006 and ChangeHistory local docs exist on disk (`test -e`). The S003 archive was not unzipped; `GoRttiMapper.java` and `GoApiSnapshot.java` were not read in this lane.

Registry-to-knowledge link: `git grep -n -E '\bS00[3-6]\b' $REV -- corpus/knowledge` returns no lines. No knowledge file at HEAD cites S003–S006. The rows' `used-by` column names `corpus/lessons/round-13.md`.

## 3. Target entry absence (C1)

```
$ test -e corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md   → ABSENT
$ git ls-tree -r --name-only $REV | grep 'knowledge/2026-10-2'     → (no output)
```

No `2026-10-2x` knowledge file exists at HEAD. Newest knowledge files are the 2026-10-19 arc3 set.

Go-adjacent knowledge at HEAD (`git grep -l -i -E 'pclntab|rtti|go1\.2[0-9]|1\.26' $REV -- corpus/knowledge`): four files — `2026-10-13-r3-node-addons`, `2026-10-13-r4-10-real-version-pair` (Go 1.25.7→1.26.8 symbol-recovery collapse), `2026-10-16-l7-01-inspect-go-binary` (Docker `go1.26.5-X:nodwarf5` metadata), `2026-10-19-arc3-r12-go-evidence-id-domain`.

Grep fact: `git grep -n -i -E 'GoRttiMapper|version gate|GoApiSnapshot' $REV -- corpus` hits only `SOURCES.md` (S003 row) and `lessons/round-13.md` (S003 row). No knowledge file at HEAD names the Ghidra Go RTTI version gate or the missing-snapshot path. This is a grep result, not a coverage judgment.

## 4. C2 gate absence (quote-location fidelity)

```
$ test -e .ufo/waves/round-14/tools/quote-fidelity.py   → ABSENT (directory .ufo/waves/round-14/tools does not exist)
$ find /home/vgpnk/Projects/shokunin -name 'quote-fidelity*' | wc -l   → 0
$ git grep -n -i -E 'quote-fidelity|quote_location|go-version-diagnosis' $REV -- .
767adafb…:SCORECARD.md:2169: …S022, and agreed with those source dispositions. The two quote-fidelity
```

Working-tree grep for `quote_location_mismatch` (repo-wide, untracked included) hits only round-14 artifacts: `.ufo/waves/round-14/spec.json`, `dispatch.json` (both spec the gate's finding codes), `w1/ReviewS017.md` (sibling review), and this report. No gate code exists at HEAD or in the working tree.

Registration and criterion check at HEAD:
- `SKILL.md`: no quote-location gate registration (`git grep` for the gate name returned nothing in SKILL.md).
- `corpus/QUALITY.md`: 15 admission rows (read in full). None addresses quote location; they cover sources, falsifiability, domain, artifact identity, observation/inference labels, Evidence IDs, limitations, versions, runtime provenance, availability, empty results, carrier bytes, grep -o counting, and Evidence-ID domain.

Prior defects the C2 gate would have to catch (from pinned HEAD files):
- S017 spliced quotation — `corpus/lessons/round-13.md:65`: the earlier gate text combined the `--normalize` CLI row with wording from a different View8 section. The corrected contiguous sentence is "Replace address-derived function identifiers with deterministic names based on parse order." (12 words).
- S018 mislocated quote — `corpus/lessons/round-13.md:66`: the quote is at Check Point `Introduction` line 87 (heading line 77), not `Decompiled output`. A correction-time fetch hit an AWS WAF page; a non-author re-open located it.
- Both are append-only corrections (`lessons/round-13.md:63-66,74`; `lessons/round-13-verifier-spotcheck.md:13`). Neither has an automated check at HEAD.

## 5. Calibration baseline (scope of this lane)

- Command B (rubric alignment) was not run; the lane is counting-only. No calibration numeric value is re-derived here.
- SCORECARD calibration row at HEAD (line 25) is historical: `0 → 10`, 2026-10-15/16 receipts.
- For C2's own observable, the baseline is: gate absent, QUALITY criterion absent, S017/S018 defects recorded only as prose corrections.

## 6. Stale or discrepant text observed (report-only; not repaired)

1. `SCORECARD.md:23` (top coverage row) reads `78/78 … measured 3395b6d`. HEAD measures 91/91 by command A. Later measured-at entries carry the current numbers; the headline row is historical.
2. `SCORECARD.md:46` (C6) reads "Current map is 70/72, missing r14-01 and r14-02". HEAD measures 91/91 with no missing tokens; C6 is a round-13-era statement.
3. Registry-to-knowledge link gap: S003–S006 have no citing `corpus/knowledge` file at HEAD (see §2). This predates C1.

## 7. Limitations

- Command A counts tokens and file stems. It does not verify that a map row describes its file's content.
- The census validates shape and columns only. It does not check quote text, URL liveness, or source truth.
- No gate, test, or build was run. `sources-census.sh` and recipe A are counting instruments; exit codes are reported as observed.
- `git status` and `git diff --stat HEAD` show no drift in `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`. That is a tree-level presence check, not a per-file hash of every file.
- S004/S005 were not opened. S003 was hashed, not read.

## 8. Executable record (summary)

| # | command | exit | result |
|---|---|---|---|
| 1 | recipe A (`python3 - "$REV"`) at 767adafb | 0 | 91/91 mapped; missing []; dangling []; 17/17 rules; 10.0/10.0 |
| 2 | `git ls-tree -r --name-only $REV -- corpus/knowledge \| grep -c '\.md$'` | 0 | 91 |
| 3 | `sources-census.sh validate --root … kaidoku` | 0 | `kaidoku ok …/SOURCES.md` |
| 4 | `sources-census.sh census --root … kaidoku` | 0 | rows 22; A20/B1/C1; mined21/rejected1; FLEET missing 0 |
| 5 | `git show $REV:corpus/SOURCES.md \| awk …` | 0 | rows=22; same tier/status split |
| 6 | `sha256sum …/Base-src.zip` | 0 | `f00d29c2…d804` = registry S003 digest |
| 7 | `test -e` for target and gate paths | 1 (absent) | target ABSENT; gate ABSENT |
| 8 | `git grep` for gate and version-gate terms at HEAD | 0 | SCORECARD.md:2169 prose; registry/lesson rows only |
| 9 | `git grep -E '\bS00[3-6]\b' -- corpus/knowledge` | 1 (no match) | no knowledge file cites S003–S006 |
| 10 | `find … -name 'quote-fidelity*' \| wc -l` | 0 | 0 |
