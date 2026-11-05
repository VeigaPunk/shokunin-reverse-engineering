# ExecRegress88 — round 89 no-harm regression (findings)

Full evidence: `.ufo/waves/round-89/w1/ExecRegress88/report.md` with receipts in that directory.

| # | label | controls | exit | wall time |
|---|---|---|---|---|
| R1 round-88 class, round-89 repair, REA on | `recovered 4 of 4` (nested r87 regression `8 of 8`) | N1, N2, N3 true | 0 | 204.91 s |
| R2 round-87 class, round-87 repair, REA on | `recovered 8 of 8` | N1, N2, N3 true | 0 | 135.18 s |
| S1–S4 selftests (round-87 repair, round-88 repair, round-88 battery, round-89 repair) | `SELFTEST cases=33/11/6/16 failures=0` | — | 0, 0, 0, 0 | not timed (`bc` missing) |
| A1 ablation of R1, `--no-rea` | `recovered 0 of 4` (nested r87 `8 of 8`) | N1, N2, N3 true | 1 | 123.37 s |

- Ablation: only the `rea_recover` arm differs between R1 and A1 (`REA disabled (--no-rea)` on all four cases). The other arms are unchanged. The counter gates REA credit on that arm; this does not show the repair depends on REA.
- The round-89 repair meets the round-87 population through R1's nested regression (`recovered 8 of 8`, controls true), in both R1 and A1.
- One first attempt of R1 exited 2 (`work_unusable`, the `--work` dir did not exist). It is not counted; the reported R1 is the successful re-run.
- Host load from peer seats makes wall times noisy; the 81.5 s R1–A1 gap is not a clean per-arm cost.
- Pins re-hashed and matching (repair `332917f2…070`, battery `f6f5ed61…720` for the round-89 counter, `a01ed622…160` for the round-88 battery, `96da7d8e…c24` for the round-87 repair, upx `cf2f6e7c…969` `upx 5.2.0`, REA `a5003023…6a` package.json).
- Verdict: no-harm regression **pass** on the round-88 class (4 of 4), the round-87 class (8 of 8), and all four selftests. The ablation is red as expected.
- No tools installed or upgraded. No git mutation. Scratch removed.
