# ScribeLesson.md — seat summary (kaidoku round-71, w1)

Draft `corpus/lessons/round-71.md` prepared at
`.ufo/waves/round-71/w1/ScribeLesson/round-71.md` (L1 lands it); full seat report at
`.ufo/waves/round-71/w1/ScribeLesson/report.md`.

- Header: base `82c8e620…` (round-70 lane tip: report, close, non-author spot-check), declaration `329208cf…` (five instruments under `tools/round-71`, the claims plan, the census-start receipt), freeze `b827a8b5…` (first commit adding `.ufo/waves/round-71/claims.json`) — all git-verified read-only against the lane repo.
- Three claims seeded from `plans/round-71-claims.md` + `.ufo/waves/round-71/claims.json`; every measurement-dependent cell carries `<L1 fills: …>`.
- `## Gate`: S273 (GFM 4.10 tolerance sentence, declared ADMIT candidate) and S274 (tempfile `mkdtemp`, declared REJECT) — fetch cells quote the scout's committed `fetch-receipt.txt` (sha256s `b153d814…` and `edf72176…`, the latter byte-identical to the round-70 seat snapshot); quote/confirmation cells await `ScoutSource/sources.md` (not yet present at draft time). Spot-check placeholder left for the non-author closure.
- `## Mistakes`: M71-1 registry-row-shape (grounded: `l1/pre/c3-at-base.json` — 88 rows, six nonconformant at SKILL.md lines 88–93, each `['pinned-empty']`; r51 census3 exit 2 since `616a5f2f`), M71-2 launcher-artifact (LC_CTYPE coercion; `PYTHONCOERCECLOCALE=0` + the declared pop; captured-by the raw-log allowlist assertion), M71-3 placeholder for the wave's strongest finding.
- Census start recorded: exit 0, 179 rows, 21 W04 (20 standing + S272) — `.ufo/waves/round-71/l1/census-start.txt`, committed at `329208cf`. End census `<L1 fills>`.
- Finding for the L1 (erratum, append-only): the frozen container's A0/`declaration_pointer` name `46366cc5…` with the declaration's subject ("the five tools, this plan, the census-start receipt"), but git shows `46366cc5` is the pre-receipts commit (`l1/pre/*` + `gen-claims.py`); the declaration commit carrying those files is `329208cf…`. Instrument pins are content sha256s and unaffected.
- Bounds: wrote only `w1/ScribeLesson/round-71.md`, `w1/ScribeLesson/report.md`, `w1/ScribeLesson.md`; scratch root created and removed; no tool installed; all git commands read-only; no mutations, no commits, no pushes.

VERDICT: met — lesson draft, Gate/Mistakes seeds and census start delivered with grounded evidence; container A0/declaration_pointer hash erratum named (`46366cc5` is the pre-receipts commit, `329208cf` is the declaration).
