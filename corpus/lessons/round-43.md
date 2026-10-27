# Round 43 — measured v4 tuple calibration and local-source resolution

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743`; round-43 freeze and measured commits are recorded in `plans/round-43-claims.md` and the C1/C2 score receipts under `.ufo/waves/round-43/l1/scores/`. L1 `KaidokuR43a2`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M43-1 | premature filing: a report committed before every dispatched wave settled can miss late seat evidence and leave uncommitted artifacts | `corpus/lessons/round-41-verifier-spotcheck.md` §1/§5 D1 (2 tracked edits and 16 untracked paths at filing); run-9 `File only after WAVE-DONE` rule in `.ufo/prompts/kaidoku-round-43.md` §6 | QUALITY #47 and the run-9 WAVE-DONE rule | Wait for the orchestrator's WAVE-DONE and `<wave>-results.json` for every ready file before reporting; red historical r41 filing state is documented in the cited spot-check; this round's report is held until all wave handoffs are received. |

## Gate

### Sources opened this round (2026-10-27)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S135 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE | 2026-10-27T08:17:52Z (`.ufo/waves/round-43/w1/R43SrcLicense.md`) | `LICENSE:5` — “Permission is hereby granted, free of charge, to any person obtaining a copy” (12 contiguous words) |
| S136 | https://api.github.com/repos/onekey-sec/sasquatch/releases | 2026-10-27T08:18:09Z (`.ufo/waves/round-43/w1/R43AssimGround.md`) | `JSON $.tag_name` — `"sasquatch-v4.5.1-6"`; projection `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]` re-derived at 08:19:46Z and 08:48:41Z |
| S137 | https://github.com/onekey-sec/sasquatch/releases | 2026-10-27T08:19:46Z (`.ufo/waves/round-43/w1/R43AssimGround.md`) | page `<title>` “Releases · onekey-sec/sasquatch”; `grep -c sasquatch_1.0_amd64.deb` returned 0 |

### Admission and rejection

- **Admit** `sasquatch-prebuilt-package-inventory` as `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`, citing S136/S137. R43AssimGround re-opened the API and rendered page, re-derived all 8 releases / 44 assets, and found the round-42 flip did not fire; R43CritAssim confirmed the re-grounded entry's scope and non-duplication (`.ufo/waves/round-43/w1/R43AssimGround.md` §§1–5; `R43CritAssim.md` §1). The cited API row is `mined`; the page row is used only for its tag-link/negative asset-name observation.
- **Reject** the staged `sasquatch-unblob-compatibility` candidate; it repeats held compatibility ground and the entry expressly makes no package/unblob compatibility claim. Keep the earlier REJECT and its flip condition; no reversal is claimed (`.ufo/waves/round-42/w1/R42Assim.md` `## 1`, rechecked by `R43CritAssim.md` §1).
- **Reject** payload-absent S150 from the assimilation registry: live Zenn fetch returned HTTP 200 but the cited heading/phrase was absent; R43Quarantine classifies this as fabrication-class and keeps it refused. S113/S136/S147 were present with anchor caveats, S117 unverifiable rather than fabricated; none was cited by the admitted entry, so no quarantine row was appended (`.ufo/waves/round-43/w1/R43Quarantine.md` §§3–5).
- The 0–3-space id collision guard returned 134 registry ids, 132 staged ids, 29 collisions (S106–S134); the scratch indented fixture showed the column-zero extractor misses rows. S136/S137 were normalized to the lane registry after S135; the staged package rows were not appended (`.ufo/waves/round-43/w1/R43AssimGround.md` §3).
- Census before → after: `corpus/SOURCES.md` 134 → 137 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); source-census start is `.ufo/waves/round-43/census-start.txt` (exit 0), round-end command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exited 0 (`kaidoku ok`, `.ufo/waves/round-43/l1/sources-census-end.txt`). The scratch append gate is `.ufo/waves/round-43/assimilation/mirror-census.txt`, exit 0 with S135–S137 and both admitted-entry paths present. The non-author closure spot-check is in the round report.
