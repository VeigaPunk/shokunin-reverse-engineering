## CLAIM
Format audit of entry 3–4 draft artifacts: entry 3's row stems break command A's map regex; E3D/E4D/G4 carry none of the house metadata fields; E4D still admits lane-A's synthetic SQLite result against ruling (b).

## METHOD
Read E3D/E4D/E3V/E4V/G3/G4/Z3/Z4, M1/M2 (map rows), K3/K4 (table rows), `SCORECARD.md:92-123`, `corpus/README.md:11-15,59-66`, `corpus/QUALITY.md:11-24`, protocol `CORPUS.md:17-19`. Ran command A against HEAD `411175e` (read-only `git show`); regex-simulated the projected map section with M1/M2 rows appended in memory. No probes/network; only this file written.

## FINDINGS
- Ruling (a): E3D.md:2 proposes hyphenated `2026-10-16-l7-03-inspect-electron-fuses.md`, and E4D.md:11-12 / M2.md:10,15 are hyphenated — but M1.md:13 and K3.md:10 use `2026-10-16-l7-03-inspect_electron_fuses`, and K4.md:10 uses `2026-10-16-l7-04-inspect_sqlite_database`. `re.findall(r'2026-10-\d{2}-[a-z0-9-]+', row)` returns the truncated `2026-10-16-l7-03-inspect` (`-04-inspect` likewise). Simulation against hyphenated files (ruling a): as-drafted `mapped=75/78, missing=[-01,-02,-03 stems], dangling=[3 truncated tokens]`; underscore→hyphen normalization gives `mapped=78, missing=[], dangling=[]`; entry 3 alone costs one each (`mapped=77, missing=['2026-10-16-l7-03-inspect-electron-fuses'], dangling=['2026-10-16-l7-03-inspect']`). Caveat: only the `## Coverage map` section feeds command A; K3/K4 table rows are index-coherence, not counted by it.
- Ruling (d): no `source:`, `verified-at:`, or `recheck:` anywhere in E3D.md, E4D.md, or G4.md (grep; E6D.md:12-14 shows the pattern; `CORPUS.md:17-19`; G3.md:10; Z3.md:8). E3D.md:8 / E4D.md:8 also propose no H1.
- Ruling (b): E4D.md:2,8 presents both carriers as entry substance; Z4.md:16 and E4V.md:10 exclude lane-A's `/tmp/luna-round-6-leg-6.sqlite` absent retained bytes/recipe (`QUALITY.md:22`); G4.md:10-23 is B-only and admission-shaped.
- Command A at `411175e` (exact output): `{"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 72, "mapped": 72, "missing": [], "rule_blocks": 9, "revision": "411175e337c0725ae9bee3fd478ae9bf05bedf3f"}`.

## THREATS
Simulation is projected, not post-landing; the 72-entry byte-identity claim is unverifiable pre-landing. SC3/SC4/CC5 are untracked (`git ls-files` output empty); E3D.md:8 cites `CC5.md:13-16` and K3.md:10 cites `SC3.md:9-12` — anchor landed text on tracked receipts. Adjacent (not my scope): M1.md:11-12 (entries 1–2) share the underscore defect; E5D also lacks the metadata fields.

## VERDICT
FINDING: hyphen-normalize K3:10/M1:13/K4:10 stems, add H1 + `source:`/`verified-at:`/`recheck:` to the entry 3–4 drafts (or use G4's B-only body for 4), and drop the lane-A synthetic from entry 4.
