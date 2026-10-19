# RV-3 quality checklist — grading method for the c1 knowledge entry

Target: `claims/c1/EX-12/knowledge-entry.patch.md` (per `claims/c1/PL-1/plan.md:269-280`).
Authorities: `corpus/QUALITY.md` (15 admission criteria + 6 weak-material signals),
`corpus/knowledge/2026-10-13-r3-evm-interface.md` (r3-07 structure: header staging
comment → title → intro → Candidates (claim/source/verify/verified-at/suggested) →
Run log → Summary → Errata), and the frozen C1 claim (`claims-frozen.md:14-38`).

Note on counts: `PL-1/plan.md:320` says "QUALITY.md's 16 criteria"; the file as it
stands has **15** admission rows (`corpus/QUALITY.md:9-25`) + **6** weak-material
signals (`:29-36`) = 21 table rows. This grade uses the file as written.

## Method

1. Apply the patch to a throwaway tree (extracted HEAD copy; scratch outside the repo,
   `/home/vgpnk/.cache/rv3-arc3/` — `/tmp` was quota-exhausted fleet-wide).
2. Run the worktree-variant of SCORECARD recipe A; require knowledge_files 82,
   mapped 82, missing [], dangling [], rules 13/13.
3. Confirm prior-81 knowledge files byte-identical (sha256 per file vs HEAD copy).
4. Structural + criterion checks on the new entry (scripted where possible).
5. Cross-check every cited hash/id/count against the landed artifacts (EX-02, EX-05,
   EX-06, EX-07, RV-2, EX-10) — an entry claim is admitted only if its citation
   resolves to a landed artifact whose own sha256 I recomputed.
6. Hard gates (from the frozen claim + wave couplings):
   - entry file stem == map token `2026-10-19-arc3-r1-evm-real-solc`
     (RV-4 `map-token.frozen.patch`, verified PASS);
   - K/K recovery with `dispatch:"abi"` on real solc bytecode;
   - both encodings (raw|hex) verified; positional-encoding quirk retained;
   - real-bytecode delta vs r3-07 is the entry's core (mutability/argument signal
     where stubs reported `pure`/empty — CR attack (c), plan.md:321);
   - observation/inference/unknown labels; EVMole output labeled upstream inference;
   - limitations: worker limits, SHA-256 ≠ Keccak code hash, no RPC/runtime execution,
     creation-code kind unknown;
   - version pins: solc 0.8.37, rea-agents pin used, evmole@0.9.3;
   - occurrence counts via `grep -o … | wc -l` (criterion 13; no `grep -c`);
   - no fabricated evidence: every `ev_…` id and 64-hex sha must resolve.

## QUALITY.md admission criteria → mechanical check

| # | criterion (short) | check |
|---|---|---|
| 1 | resolvable source | repo path / command output present; cross-check vs landed artifacts |
| 2 | falsifiable or opinion | claims carry commands + expected outputs |
| 3 | domain-specific | REA/EVM specifics, no generic advice |
| 4 | absolute path + stable identity | `/home/vgpnk/…` or wave paths + sha256 for each artifact |
| 5 | observation/inference/unknown labels | label vocabulary present; EVMole = inference |
| 6 | Evidence ID / exact reproducing call | `ev_…` ids + command lines; ids resolve in landed JSON |
| 7 | names what was NOT examined | limitations section (worker caps, no RPC, kind unknown) |
| 8 | version pins + claim source | solc 0.8.37, rea-agents@x, evmole@0.9.3, live-run source |
| 9 | runtime-behavior provenance | `runtime_execution: not-performed` stated; no behavior asserted |
| 10 | "held" on a real carrier this round | real solc runtime probed this round; provider status |
| 11 | empty vs excluded distinction | any zero/empty result states parsed-and-empty vs excluded |
| 12 | carrier bytes/recipe retained | `.sol` inline or path + settings + sha256s |
| 13 | `grep -o … | wc -l` for counts | grep -c absent; counts reproducible |
| 14 | (superseded by 15) id domain | per-verb-family statement w/ corpus citation |
| 15 | id domain per verb family | `inspect-evm-interface` id domain stated; path-sensitivity if claimed |

Weak-material signals 1-6 checked as red flags (behavior-from-strings, "no X" without
command, floating target, docs-vs-live availability, static-as-runtime, "tool broken").

## Verdict scale

- **accept** — all hard gates pass; no required fix.
- **accept-with-fixes** — no hard-gate failure, but named required fixes (each with
  the criterion/line it violates and the fix).
- **reject** — hard gate fails (wrong stem, missing K/K, fabricated citation, etc.).
