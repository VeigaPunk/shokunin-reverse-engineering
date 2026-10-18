# CR2 — critic: verdict inflation + smuggled claims (arc2-loop1-round8)

Snapshot: 2026-10-18 ~19:55-03, HEAD `5f4e9b9`, working tree clean except untracked `.ufo/waves/arc2-loop1-round8/`. Custody verified 5/5 (below). The live control was observed read-only; I signaled nothing.

## 1. Verdict

**C3 — NOT VERIFIED at my close; outcome direction observed but unsealed.** The natural control `arc2-r8-ctl` reached a terminal **OOM-kill** at 19:53:10-03 (4m42.945s wall, 11m54.335s CPU, 9G memory peak, 1G swap peak, `Restart=no`, `NRestarts=0`). Per C3's own gate ("Sealed outcome required; in-flight at close → C3 not verified"), the kill satisfies the *direction* (kill → disable proven necessary) but **no r8 envelope is sealed**: `.ufo/waves/arc2-loop1-round8/receipts/` contains only `config-pre-pair.txt`. Any seat or parent record writing "C3 verified" or "(attribution confirmed)" before an envelope lands in receipts/ + the append-only correction lands is **verdict inflation**. The parenthetical in the claim text is outcome-conditional; at snapshot it reads as presupposed — treat as a spec, never as a result.

**C1 — admittable, with two wording constraints; not yet landed (no inflation yet, prospective attack).** Per `AXES.md` §Capabilities (:57-64), rows enter only through a round demonstrating the capability running; r6/r7 sealed entries supply that (`git ls-files` confirms both tracked; r7 `arc2-r7-pe` exit 0 per `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13`). Constraints: (a) the row must carry the mitigation qualifier — "contained" is true only WITH the validated-name analyzer-disable; today's natural control **disproves unmitigated containment** (9G+1G-swap peaks = caps hit, killed); citing the r8 control as containment evidence would be a smuggled reversed claim. (b) first-working round must be **r7** — r6 never completed (`provider_timeout` at ~900s; `corpus/README.md:22` state text), so r6 demonstrates containment-without-completion, not a passing run.

**C2 — claim wording is a fork; one reading double-counts r7, the other is a real move.** The caller-independent-services lesson row **already landed in r7**: `corpus/README.md:166` present at HEAD and at commit `8cc81a8` (`git show 8cc81a8:corpus/README.md | grep -c caller-independent-services` → 1), and r7's own SCORECARD section claims it as r7-C3 (SCORECARD.md:1129-1131). If round-8 C2 means *landing* that row → **double-counted r7 move**. The coherent reading, matching r7's carried-debt phrase "the r7-lesson's own index row (same deferred coupled-pair shape)" (SCORECARD.md:1155-1156), is a **dedicated coverage-map row for `2026-10-18-arc2-r7-pe-wall`** — which does not exist: its token sits inside row `corpus/README.md:22`'s entries cell whose state text still describes only the r6-era ~900s deadline kill. The parent must record which reading C2 is; ambiguity here is itself an inflation vector. The regression half of C2 is verified at HEAD by me (below).

## 2. Evidence

- **Custody 5/5**: `awk 'NR>1{print $1}' receipts/config-pre-pair.txt` vs fresh `sha256sum` of the 5 listed files → `diff` empty, "CUSTODY 5/5 MATCH" (receipt lines 2-6: devin mcp_config, omp mcp.json, kimi config.toml, .bashrc, .profile).
- **Control outcome**: `journalctl --user -u arc2-r8-ctl --no-pager` → `Oct 18 19:53:10 … kernel OOM killer killed some processes in this unit` / `Main process exited … status=1/FAILURE` / `Failed with result 'oom-kill'` / `Consumed 11min 54.335s CPU time over 4min 42.945s wall clock time, 9G memory peak, 1G memory swap peak.` `systemctl --user show` → `Result=oom-kill`, `ExecMainStatus=1`, `Restart=no`, `NRestarts=0` (terminal; no further signal needed or sent).
- **Control artifact, seal-ready**: `/var/tmp/arc2-l8r8-ctl/stdout.json` (20294 B, sha256 `ba95181c8a8597f08c85d3a75e664732a48bd7a1810c0395d69f4c013f71ed14`); header: `error: Analysis failed / code: cancelled / message: Analysis was cancelled. Start it again when ready.`; `details.diagnostics.target_sha256 = 7a2ccd688f6c…` — byte-identical to the r7 artifact (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:11`), so the control exercised the same target.
- **Attribution support (inference)**: the kill landed at 4m43s — far short of even the old ~900s deadline — so the failure is memory-class at the caps, not time-class; that plus preset being the only difference vs r7's mitigated run (7.9G peak, 1424.663s, exit 0, `:13`/`:17`) supports "disable necessary for completion". It does **not** confirm the stronger r7 wording "The disabled analyzers removed the memory driver" (`:17`) — the natural run shows memory still grows past 9G; the disable kept peak under cap, it did not remove the driver.
- **C2 regression half, run by me at HEAD**: `python3 .ufo/gates/citation-drift/citation-drift-probe.py` → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`. `python3 .ufo/gates/c1-census-v10.py --quiet` → `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, G2 ok, G7/G11 empty. Pointer resolution: `SCORECARD.md:69` cites `corpus/README.md:179` → line 179 is the Runtime-obs depth frontier bullet reading "held, not frontier" — resolves.
- **Denominator check (r5 counting lesson)**: `git ls-files corpus/knowledge/` = 82 tracked incl. `.gitkeep` → **81 `.md` knowledge files** ↔ command A 81/81. No discrepancy.
- **No r8 surface exists yet**: `grep -n "arc2-loop1-round8\|round8" SCORECARD.md LOG.md` → nothing; no capability row mentions a user-service analyze (`grep -in "user-service" SCORECARD.md` → narrative mentions only).

## 3. Verbatim-landable

C3 append-only correction draft (append to `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` after "Not examined", or as an addendum block; seal the envelope into `.ufo/waves/arc2-loop1-round8/receipts/` first — cite its sha256 here in place of `<ENVELOPE_SHA>`):

```
Erratum/correction (arc2-loop1-round8, 2026-10-18): the natural-preset control
user service `arc2-r8-ctl` (same artifact sha256 7a2ccd688f6c…, no disabled
analyzers, 9G cap + 1G swap cap, 7200s deadline unused) was kernel-OOM-killed
at 4m42.945s wall / 11m54.335s CPU with 9G memory peak and 1G swap peak
(`Result=oom-kill`; envelope <ENVELOPE_SHA>). This confirms the analyzer
disable was necessary for the round-7 completion: the kill is memory-class
(well under even the old ~900s deadline) and preset is the only run
difference vs this entry's mitigated hold (7.9G peak, 1424.663s, exit 0).
Wording scope: the disable kept peak under the caps and let the run finish;
it did not remove the memory driver (the natural run grows past 9G) — :17's
"removed the memory driver" is hereby scoped accordingly. Rerun id-stability
(:7) stays UNKNOWN: this control runs a different preset and therefore
different request bytes (QUALITY.md:25), so it cannot settle id stability.
```

C1 capability-row wording constraints (for the row the round lands): name it "contained (9G cap, validated-name analyzer-disable) user-service analyze of the 91.6MB Godot ARM64 PE"; evidence pointer = `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:13-17` (+ r6 entry for the containment/lifetime distinction); **first-working round = r7 (arc2-r7-pe exit 0)** — not r6. Do not cite the r8 natural control as containment evidence; it is the necessity proof, and it points the other way.

C2 recording constraint: record round-8 C2 as (pick one explicitly) — (a) "regression verification of r7's landed pair (README:166 row; SCORECARD:69→README:179 re-point) at close: probe findings=0, census PASS" — verified by CR2 at HEAD `5f4e9b9`; or (b) "new move: dedicated coverage-map row for `2026-10-18-arc2-r7-pe-wall` + coupled re-point", which additionally requires writing that row with state text reflecting the r7 wall-falls/mitigated outcome and the r8 natural-control confirmation, and re-checking the :174/:22 staleness below in the same commit.

## 4. Labels

- **Observation**: `corpus/README.md:174` frontier bullet (">90MB PE scale") still carries pre-fall guidance (~900s deadline / bisect 2-5MB), and map row `:22`'s state text still describes only the r6-era deadline kill — both contradict the r7 wall-falls record (`2026-10-18-arc2-r7-pe-wall.md:19`) at the index layer. Index integrity only (SCORECARD.md:23 scope limit), so non-blocking; but a round narrative claiming "freshness improved" should either fix them in C2-reading-(b)'s commit or name them carried debt.
- **Observation**: r7's carried-debt phrase "the r7-lesson's own index row" (SCORECARD.md:1155-1156) is ambiguous against the already-landed lessons row (:166, present at `8cc81a8`) — the r8 records should reconcile the phrase to mean the dedicated coverage-map row (reading b).
- **Inference**: kill-at-4m43s ⇒ memory-class failure ⇒ disable necessary for r7 completion (supported, pending seal); "removed the memory driver" (r7:17) is NOT supported as confirmed and should be scoped, not rewritten (append-only).
- **Unknown**: rerun analyze-id stability — untouched by this round's control by construction (content+params keying, `QUALITY.md:25`; r7:7); must remain listed as open. Also unknown until sealed: whether any watch seat captured natural-run decompile-worker samples (would strengthen the per-worker attribution beyond preset-difference logic).
