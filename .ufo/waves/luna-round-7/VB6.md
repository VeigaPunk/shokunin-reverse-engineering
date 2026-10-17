## CLAIM
Four lane-A seat disagreements touch the six entries; all are tabulated with final dispositions — three confirm parent rulings (b)/(c)/(d), the E4V objection is rejected because the leg-3–8 receipts are tracked at HEAD 411175e. No unresolved disagreement blocks landing.

## METHOD
Read-only: round-7 seats Z2/G2/E2V/E3D/G3/Z3/E4D/E4V/G4/F6/F8/M1/M2; round-6 legs 3–8 receipts, SC1–SC6, RV3; `QUALITY.md`; `CORPUS.md:17-19`; `git log`/`status`/`ls-tree` at HEAD 411175e. No probes, network, or tracked-file edits.

## FINDINGS
| Disagreement | Final disposition |
|---|---|
| **Z2 carrier split (entry 2, leg-4).** Lanes hit different artifacts — Signal `.node` `1b44ed…d14d1f7` (`receipts/leg-4.md:21`) vs `/usr/bin/rg` `d006ac…ecae42` (`receipts-B/leg-4.md:17`); Z2.md:8 demands separate identities, no same-target corroboration (G2.md:28, E2V.md:13 concur). | **Ruling (c) adopted.** Entry 2 anchors lane-B `/usr/bin/rg`; lane A stays a named, separate fallback (M1.md:12 likewise distinct). |
| **G3 fields catch (entry 3, leg-5).** E3D's proposed entry lacks `source:`/`verified-at:`/`recheck:` (G3.md:10; none in E3D.md; contract CORPUS.md:17-19). | **Ruling (d) adopted, all six entries.** Pattern: E6D.md:12-14; drafts E1D/E2D/G2/E3D/E4D/E5D lack fields (F8.md:10). G3's `E3D.md:12-26` pointer is stale — file ends :14, proposal :8 (Z3.md:8). |
| **G4 fixture catch (entry 4, leg-6).** Lane-A's generated 8 KiB fixture `/tmp/luna-round-6-leg-6.sqlite` (`71ac0b8e…5872b`; `receipts/leg-6.md:10-12`; RV3.md:5) retains no bytes/recipe — criterion 12 unmet (QUALITY.md:22); G4.md:22,25 excludes it (E4V.md:10, F6.md:8, F8.md:9 concur). | **Ruling (b) adopted.** Entry 4 admits only lane-B's real pnpm-index inventory (`receipts-B/leg-6.md:23-28,35`, `3701a7e3…9728`); strip the synthetic sample from E4D.md:8 and M2.md:19. |
| **E4V misread (entry-4 citations).** E4V.md:13-19 quotes all three named paths `??` and an empty `git ls-tree`, declaring the receipts non-durable at HEAD. | **Rejected.** At HEAD 411175e `git status --short -- …` shows only `?? …/SC4.md`; `git ls-tree -r --name-only HEAD -- …` lists both leg-6 receipts. Commits bc91424/411175e (19:52:00/19:53:26) predate every round-7 artifact (≥19:56) — the quoted state is unreproducible; F8.md:10 agrees. SC1–SC6 are untracked: auxiliary anchors only. E4V's fixture caveat survives via row 3. |

Adjacent stale-absence claims (E1D:2,30 "E1V absent"; Z2:5,8 "E2D/G2 absent") are documented by F8.md:11 and leave these dispositions unchanged.

## THREATS
Dispositions rest on retained HEAD evidence, not re-execution; E4V's historical run context is unrecoverable. Scout files SC1–SC6 remain untracked. Command A counts, map edits, and prior-entry byte-identity are parent scope, unverified here.

## VERDICT
CLEAN — four divergences disposed: (c)/(d)/(b) confirmed; E4V rejected as misread; no open lane-A disagreement blocks the six entries.
