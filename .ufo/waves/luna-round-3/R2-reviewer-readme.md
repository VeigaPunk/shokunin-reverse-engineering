## CLAIM
At HEAD `a9580ebdcd3ab0b5c346619cceb487af3e0842ac`, the README convergence target is not met: `corpus/README.md:169` still states the universal path-sensitive rule and gives no family-scoped exception citation.

## METHOD
Read-only corpus review: `git grep -n -F 'Evidence ids are' HEAD -- corpus/README.md` → `HEAD:corpus/README.md:169:- Evidence ids are \`f(content, path, params)\` — path-sensitive, three-lane corroboration r4; cite \`subject.digest.sha256\` for cross-path identity.` Checked the evidence at `git show HEAD:corpus/knowledge/2026-10-14-r9-02-queue-a-ops-2.md` lines 146–169.

## FINDINGS
The README preserves the universal `f(content, path, params)` and cross-path digest prescription at line 169. The cited counterexample says `analyze_function` ids are `f(content, params)` with path not hashed and cross-path identity in the id (r9-02:146–158); it further says module attribution is in `subject`, which the id does not authenticate, and request bytes must be pinned when module identity matters (r9-02:159–169). The README line does not cite or scope itself to that family.

## THREATS
This is a HEAD-only textual check; no live REA probes or network were used. Scope is README convergence only; no judgment on the SKILL site or command-A controls.

## VERDICT
FINDING: `corpus/README.md:169` retains the universal path-sensitive rule instead of family-scoped wording with the r9-02 citation.
