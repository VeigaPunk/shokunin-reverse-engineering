# RegistryDraft candidate (round 16, w1) — drafts only, not applied

Targets are read-only for this seat. L1 integrates. No gate semantics change. No command was executed by this seat.

Sources: `SKILL.md:450` (quote-fidelity row), `SKILL.md:487` (go-snapshot-inventory row), `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` (recheck line), `.ufo/waves/round-15/boundary-fixtures/expected.json`, `.ufo/waves/round-15/verification.json` (retained argv/stdout).

## A. quote-fidelity row, column "Pinned values / write scope" (SKILL.md:450, last cell)

Replace the whole last cell with the text below. Only the pinned-values cell changes; the other cells in row 450 stay byte-identical. The text contains no `|`.

```text
`.ufo/waves/round-14/fixtures/expected.json` pins every manifest and source excerpt; frozen source-inventory coverage is required. Supplemental round-15 boundary baseline `.ufo/waves/round-15/boundary-fixtures/expected.json` is a separate invocation (`python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-15/boundary-fixtures/expected.json`) and pins `raw-accepted.json` (exit 0, no findings), `rendered-rejected.json` (exit 1, `quote_not_contiguous@raw-literal`) and their shared `raw-source.md` excerpt; these are limitation controls for raw substring absence, not rendered-quote detection and not a new gate capability. The round-14 pin file is unchanged by this addition. Normal modes read only; selftest creates/removes its isolated fixture tree under `/var/tmp` or `QUOTE_FIDELITY_SELFTEST_DIR`. Raw UTF-8 substring and Markdown/single-line HTML heading consistency only: no upstream authenticity, full-document completeness, semantic support, or whole-registry verdict. Manual-only submissions are excluded by QUALITY #17, not detected by this tool; any machine verdict on such a claim is void.
```

Notes for L1:
- The finding ID is `raw-literal`, the quote `id` in the fixture (`rendered-rejected.json:18`; `expected.json` pin; retained stdout in `verification.json`). Do not write `@rendered-text`; see report F1.
- The rendered-rejected digest is not written in the cell. The pin lives in `expected.json` (`92c8904b…`), not the stale `bc97c469…` in older prose; see report F2.

## B. go-snapshot-inventory row (SKILL.md:487) — whole row

Replace the whole row with the text below. The command is the exact argv retained in `.ufo/waves/round-15/verification.json` (labels `snapshot-inventory` and `inventory-determinism`, both exit 0, byte-identical stdout). The script path is absolute because the retained argv used it.

```text
| go-snapshot-inventory | probe / kaidoku | `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`; exit 0 inventory complete, exit 2 could-not-evaluate (script EXIT table); read-only JSON inventory, not a conformance verdict | no selftest or gate claim | `.ufo/waves/round-15/inventory.json` retains the stdout of that argv (stdout SHA-256 `ad06fadc0166e172d65325e3366375e2d4a9730d714d154bbcd98137539bb2fe`) with filename/size/SHA-256 and selected JSON structure; omitting `--select` selects the script default `1.25.0 1.26.0`, a different inventory; read-only installed resources, stdout only; rerun and compare bytes manually |
```

Notes for L1:
- The row's `Entry` text before this draft was `python3 .ufo/waves/round-15/snapshot-inventory.py --ghidra …` with no `-I` and no `--select`. That is not the retained argv and cannot reproduce `ad06fadc…` (script default `--select` is `1.25.0 1.26.0`, `snapshot-inventory.py:66,414`).
- The `-I` flag and absolute path are the exercised form. A relative path from repo root would read the same files but is not the exercised argv; keep the absolute path if the goal is exact reproduction.

## C. corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md line 3 (`recheck:`) — for L1 integration only

Replace line 3 with the text below. Everything after the command (`; compare retained …`) stays unchanged.

```text
recheck: `python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/snapshot-inventory.py --ghidra /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC --select 1.24.7 1.25.7 1.26.8`; compare retained `.ufo/waves/round-15/inventory.json` filename/size/SHA-256 and parsed summaries, and reopen S003 anchors below. A changed inventory is drift to investigate, not an automatic failed support verdict.
```

This aligns the knowledge recheck with the exercised argv (lesson routed defect 1). The prose at lines 52-57 says the recheck "ran twice"; that remains accurate after this change because the argv is the same one retained in `verification.json`.

## D. Frozen-run argv, for the record (retained, not re-executed here)

From `.ufo/waves/round-15/verification.json`, label `boundary-frozen`:
`python3 -I /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py --frozen /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/boundary-fixtures/expected.json` → exit 0, `mode=frozen manifests=2 findings=0`, both pins `match`.

Exercised form uses an absolute `--frozen` path. Section A writes the repo-relative form used by the existing round-14 cell; that relative form is NOT separately exercised in retained evidence and works only when the working directory is the repo root. L1 may prefer the absolute form for exact reproduction. Inside `expected.json`, manifest and source paths resolve against that file's directory (`quote-fidelity.py:353`), independent of the working directory.
