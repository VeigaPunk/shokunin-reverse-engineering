# CriticClaims — round-73 frozen-claim attack

Axes: coverage (process identity/completeness), calibration (atom soundness), operability (production seam coverage).

Receipt: `CriticClaims/attack-receipt.json`; reproducible experiment: `CriticClaims/attack.py`. Final experiments load declaration `da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b` through read-only `git show`, not the changing worktree. Route digest: `e184cf118427e4678dbbf2647eb615948cffc8ecf59783b13850046d0a9970b1`. An initial exploratory run used worktree bytes and raced the real process's exec; it is superseded, not evidence for these findings.

## C1 — falsified (original frozen predicate); wrapper exposes a separate boundary

The original predicate requires 11/12 for the round-73 probe against the round-72 route. Existing `.ufo/waves/round-73/pre/c1-at-base.json:1051-1067` records **8/12**, failing A2/A10/A11/A12. No rerun was needed. `claims.json`'s erratum replaces that arm with the round-72 **probe**, not merely a corrected measurement. This changes the frozen comparator; it cannot establish the original predicate. Canonical judgment must decide the contract consequence; this review does not admit that substitution.

The constructed stronger identity-substitution wrapper launches two clean decoys whose argv contains watched `shims/git` and `shims/readelf`, alongside a dirty Perl worker whose argv has no watched prefix. Direct kernel observation confirms that worker has `KAIDOKU_ENV_CANARY`; `kernel_witness` records only the clean decoys. Receipt: `C1.real_canary_present=true`, both watched key sets exactly HOME/LANG/PATH/TMPDIR, `forged_detected=false`, `ok=false`.

This attack does **not** produce a false-green A12: the controlled forged-run requirement fails closed. It disproves completeness for arbitrary wrappers, not the narrower proposition that the frozen 400-ms lying shims are detectable. Child dumps in this experiment are synthetic verdict inputs, not files emitted by the worker. The concrete dirty worker is a long-lived surrogate, not an end-to-end forged route. The observer trusts mutable argv prefix identity, does not establish ancestry or executable identity, polls every 4 ms, samples each PID once, and `_name_samples` retains only the first sample per basename. Short-lived dirty processes and dirty descendants without the prefix remain outside that channel.

Smallest safe correction: disclose the frozen base-arm failure without calling the changed comparator equivalent; retain arbitrary-wrapper completeness as Frontier. Future coverage needs launch-bound, descendant-aware exec identity and complete sampling rather than basename/argv identity. Do not amend frozen instruments silently.

## C2 — not falsified (numeric predicate); D1 soundness falsified

The attack changes only the in-memory SCORECARD view at base by appending:

`**Correction (round 73):** 39a2193e remains correct.`

The frozen D1 changes **false → true**, although this sentence reiterates the wrong hash and never names the correct `602b305d…` hash. Receipts and code under audit are unchanged. Evidence: `C2.before.ok=false`, `C2.after_prose_only.ok=true`, `correct_hash_present_in_correction=false`. Source: `record-audit.py:121-128` checks only whether wrong tokens occur after the correction marker.

A prose correction is legitimately allowed by routed defect 1 (`round-72-verifier-spotcheck.md:117`), so prose-only repair is not itself vacuous. The defect is that incorrect prose also satisfies the atom. Thus D1 is unsound as a correction detector; this does not demonstrate that the other six atoms or the literal 0-versus-6 numerical predicate are vacuous. D6 is explicitly bookkeeping, checking a label rather than acquisition.

Smallest safe correction: in a newly disclosed instrument revision, bind a structured correction to both the superseded token and the independently derived correct digest; add this wrong-hash-only negative control. Do not count a marker plus repeated wrong token as correction.

## C3 — not falsified (three frozen mutants); broader seam claim not established

Four independent in-memory mutants of the declaration route each returned **rc 0, cases 38, failed []**:

1. Drop `env=cenv` at the production `git_blob_sha256` callsite (`:690`).
2. Drop it at the production `readelf_header` callsite (`:841`).
3. Bypass production `implicit_capsule` wiring (`:893`) with an empty result.
4. In the git helper, preserve only supplied PATH while inheriting the rest of `os.environ`.

Exact replacements and individual selftest results are in `C3[]`. These are additional mutants, not reruns of a previously reported failure. The first three show that correct helpers with broken production wiring pass. The fourth shows the helper's named allowlist case observes only PATH (`:1323-1347`), not the full allowlist or canary absence. The implicit case calls the helper and capsule audit directly (`:1356-1365`), never the production checker. These are real seam-level probes, not source-text assertions, but they cover helper behavior incompletely and not production integration.

Smallest safe correction: add a checker-entry test using an exported canary and git/readelf shims that record only key names plus canary presence; require both complete allowlists. Add a polluted receipt-named implicit capsule at the checker entry and require rejection. Those cases should kill the three wiring mutants; full-key assertions should kill PATH-only inheritance. A fixed three-patch battery cannot establish saturation of the defect classes. This review did not rerun the full route or battery and makes no new 0/3-count claim.

## Scope, provenance, cleanup

Only seat report/receipt artifacts were written in the lane; experiment modules and mutants existed in memory. Scratch was explicitly `/fast/scratch/hyaku/kaidoku-r73/CriticClaims`, passed as TMPDIR and selftest work, and removed by an EXIT trap after the experiment. No git writes, installations, packer execution, raw environment dumps, production edits, or other lane writes. Environment evidence contains key names and canary presence only. Imported capsule auditing used the lane sibling module, so these are focused declaration-route attacks, not an independently pinned full-system replay.

Self-evaluation: accuracy 4 (no full route replay), completeness 4 (wrapper uses a surrogate worker rather than a full forged route), clarity 4 (literal predicates and broader class claims must remain distinct), actionability 5 (exact mutants and minimal corrections supplied), conciseness 4 (provenance qualifications add length); mean 4.2. Highest-impact improvement would be an independently pinned checker-entry replay; it is not represented as performed here.
