<!-- CANONICAL TEMPLATE: the block below must stay byte-identical to the canonical
     SHONEN.md seed in PROTOCOL.md (upstream main repo, master HEAD, block headed
     "The canonical `SHONEN.md` seed (verbatim -- kaidoku is the only substitution)",
     lines 419-428), modulo kaidoku = the minted repo directory name. Regenerate from
     PROTOCOL.md on gate changes; never hand-edit. -->

# kaidoku — Promotion checklist

Promotion to shokunin requires all of:

- [x] SKILL.md contains real decision tables, error patterns, checklists, cited sources
  verifier: r3 integrator report (gate closed; roster status re-asserts non-author review) — .ufo/reports/round-3/kaidoku.md:22-25,49-54; decision-table rows re-verified against the knowledge entries by r5 consistency audit — .ufo/waves/kaidoku-r5/04-audit-consistency.md:132-139
- [x] At least one end-to-end domain task executed and logged in LOG.md
  verifier: r1 integrator report, "## End-to-end task (shonen checklist)" — .ufo/reports/round-1/kaidoku.md:21-27; logged in-repo — LOG.md:9-11; r2 audit re-ran ~100 r1 verify commands, 0 disproven — .ufo/reports/round-2/kaidoku.md:10-16; caveat: the r1 commit checked this box without a recorded verifier (flagged by the r2 audit) — LOG.md:25-31
- [x] Instructions executable by an agent without oral context
  verifier: fresh audit lanes re-ran corpus verify commands verbatim against live host state — .ufo/waves/kaidoku-r2/01-audit-A.md:1-5, .ufo/waves/kaidoku-r3/01-audit-A.md:1-3; 55+/29+ confirmations, 0 contradictions — .ufo/reports/round-2/kaidoku.md:10-16, .ufo/reports/round-3/kaidoku.md:10-11; blanket closure asserted — .ufo/reports/round-3/kaidoku.md:49-54; caveat: box was self-checked at r1 before those audits (flagged) — LOG.md:25-31
- [x] No cross-domain bleed (PROVINCE.md still accurate)
  verifier: r2 audit registry refresh, zero drift — .ufo/reports/round-2/kaidoku.md:45-49; r3 consistency audit found and fixed province drift — .ufo/reports/round-3/kaidoku.md:14-16; caveat: r5 consistency audit documents fresh PROVINCE drift (stale Frontier bullets, wrong REA_APKTOOL_JAR key) — .ufo/waves/kaidoku-r5/04-audit-consistency.md:12-53,183-191 — accuracy claim contested pending the round-5 repairs
