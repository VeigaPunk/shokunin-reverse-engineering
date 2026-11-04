# ExecC3 — R71-C3 independent rederivation

Full report: `.ufo/waves/round-71/w1/ExecC3/rederive.md`.

- Independent parser: base 88 rows/88 existing unique paths; shapes 78×7 cells, 4×8 round-69 cells, 6×6 round-70 cells. Six defects exactly `pinned-empty`.
- Scratch owner-only repair: 0 nonconformant/88 paths; exactly six changed lines; all five round-69 lines retained byte-identically (`diff` exit 0).
- Frozen census at base **exit 1**, at freeze **exit 1**, each with six defects; selftest **exit 0, 14/14**; legacy census3 at base **exit 2**, `registry row must have seven cells`.
- Frozen census SHA256 matches container pin `a7746d2ade8946c112ed097268df7ba905f0632a0af8b9e3375dc6ea7c42d528`.
- Exact row reconstructions: `ExecC3/independent-base.json`; simulated repair: `ExecC3/independent-repaired.json`, `six-row-repair.json`; evidence: `census-base.json`, `census-freeze.json`, `census-selftest.stdout`, `legacy-base.stderr`, `round69-{base,repaired}.lines`, `commands.json`, `summary.json`. Reproduction driver: `rederive.py`.
- Risk: simulation is not a landed repair. Parent must measure the eventual record revision; no claim of future success. Frozen selftest's case named five-cell actually constructs four cells (short-row branch still exercised).
- No lane implementation changed, installs, git mutation, or delegation. Exclusive scratch removed; command scratch paths are provenance only. LSP unavailable in exposed tools.

VERDICT: not-met at freeze — six round-70 pinned-empty defects remain; scratch-only six-row owner repair yields zero nonconformant rows.
