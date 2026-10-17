## CLAIM
Independent verification of item-4's jq-shadow "benign" bleed chain (D1–D4): where the safety language actually sits, whether the current refusal is `PROVINCE.md:114-116`, and whether D2's append-only qualification covers the bleed.

## METHOD
Read-only at HEAD `a280e07` (`git status --porcelain` → no tracked modifications; `git diff --exit-code` on the r2/r3 corpus files + PROVINCE.md → clean, exit 0). Read `PROVINCE.md:104-117`; `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:1-30,200-242`; `corpus/knowledge/2026-10-13-r3-jq-provenance.md:55-70,130-140`; `SCORECARD.md:74-84`; `corpus/lessons/2026-10-15-round-1.md:145-155`; `.ufo/waves/luna-round-9/{D1,D2,D3,D4}.md`. Counted safety tokens (`benign|safe|trust|malicious|compromise|legit`) across all six `corpus/knowledge/*jq*` entries. No probes, network, or writes.

## FINDINGS
- Refusal location: `PROVINCE.md:114-116` — the lane never answers "is it safe, trustworthy, or licensed for reuse"; `:107-109` is anti-trigger + installer scope. P0's correction confirmed. `SCORECARD.md:79` and `corpus/lessons/2026-10-15-round-1.md:149-153` still cite the stale `:107-109`.
- r2 bleed lines: `:12` ("Benign payload"), `:217` ("benign payload, genuine artifact"), `:219` ("not binary compromise"), `:236-237` ("benign, intentional agent-installed"). D2's scope sentence names only `:217` and `:236-237`; D4's broaden-to-`:217-219` is supported (`:219` is safety language). `:12` sits inside D2's `:10-13` evidence cite but is not named in the scope sentence.
- Scope gap: r3 provenance repeats "benign, intentional install" (`:60`) and "no malicious or accidental pathway indicated" (`:136`); an r2-only append leaves these standing (D3's point, verified). Item-4's text names the jq-shadow entry, so extending to the r3 companion is the parent's adjudication.
- Containment: the other four jq knowledge entries contain zero safety tokens (grep counts 0/0/0/0) — bleed confined to these two files.
- Append point: the r2 entry ends at `:242`; the proposed note is append-only-legal as drafted.

## THREATS
Not re-verified offline: the sha256/upstream-release identity claims and install intent (cited from the corpus, not re-run). D2's wording was reviewed from `D2.md`, not a landed append. Retaining scoped "benign" (D2/D4) vs replacing it (D3) is a policy call; evidence supports scoping, and D3's r3-gap is real.

## VERDICT
FINDING: D2's qualification names only `:217`/`:236-237` — verified bleed at r2 `:12`/`:219` and r3 `:60`/`:136` is unaddressed; broaden scope and refresh the stale SCORECARD/lessons pointers before integration.
