# TruthS032 — R17-S032-DIGEST discharge attack (REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94)

HOLDS

Axes attacked: calibration (is every number/hash in the correction true?), depth (re-derivation from live external ground truth, not intra-repo strings), operability (every command reproducible).

## Commands run (all exit codes pasted)

```
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94
  → exit 0; open_count 0, named_open_count 0, substance_open_count 0; R17-S032-DIGEST closed via
    named "superseding-row", substance "s033-anchor-commit", substance "s032-digests-evidence"
python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470
  → exit 0; open 6 (named 6, substance 6), incl. R17-S032-DIGEST   # red state reproduced
  … same with --strict → BASE_STRICT_EXIT=1; REV_STRICT_EXIT=0
for i in 1 2 3; do curl -sSL https://github.com/NationalSecurityAgency/ghidra/pull/9348 -o /tmp/page$i.html && sha256sum /tmp/page$i.html && wc -c < /tmp/page$i.html; done   → exit 0
  a1a14b4f8f39… 403460 | 2b7232d701ce… 403460 | a7a10c3e788c… 403460   # 3/3 distinct; none == 436c0f63…
curl -sSL …/pull/9348.patch -o /tmp/p1.patch && curl -sSL … -o /tmp/p2.patch && sha256sum /tmp/p1.patch /tmp/p2.patch
  → exit 0; both ae5dc2e3e28f3f64feb32ba7df9659626a5173328b83a6b5e3914fcfa3b70a11 (byte-stable, 2 fresh + 2 recorded fetches)
git ls-remote https://github.com/NationalSecurityAgency/ghidra refs/pull/9348/head   → exit 0; a214355498e84aa86280be0c31c955aaf94f2d12
curl -sS https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348 → state=open merged=False
  title='Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries' head.sha=a214355498e84aa86280be0c31c955aaf94f2d12 commits=3
grep -n '^From [0-9a-f]\{40\}' /tmp/p1.patch → lines 1/52/106: 1aa79ff…, a94872c…, a214355498e84aa86280be0c31c955aaf94f2d12
  # mbox final commit == pinned head; the first-line 1aa79ff… is commit 1/3, no contradiction
git show 9011581…:corpus/SOURCES.md | grep '^| S032' | sha256sum  == git show b2aad08…:… same → bb62c87d… both (S032 row byte-identical)
git diff 9011581…..b2aad08… -- corpus/SOURCES.md | grep -c '^-[^-]' → 0 (append-only confirmed); rows 32 → 36
git cat-file -e b2aad08…:.ufo/waves/round-18/evidence/s032-digests.json → TRACKED (added at eb6c266, the frozen-predictions commit)
blob-at-REV sha256 7e8f1c56… == worktree 7e8f1c56… (9 dirty worktree files are all untracked wave-2 dispatch artifacts)
programmatic row-vs-API compare → title==api True; state==open True; merged False; head==api_head True; patch_digest_claim True; teaches startswith 'supersedes S032 —' True; 'fetch-time' in anchor True
```

## What re-derived TRUE (observations, at REV unless noted)

- Defect text (round-17-verifier-spotcheck.md:147): S032's page sha256 `436c0f63…` not reproduced by fetches `028dbb7d…`/`f3841de0…`. Correction chosen: supersede via new S033 row anchored on title/state/head/patch digest, page digests marked fetch-time only (corpus/SOURCES.md:39).
- S033 row claims all verified against live external state: exact title, state open, not merged, head `a214355…` (ls-remote AND GitHub API agree; head unmoved since the 15:38Z recording), `.patch` sha256 `ae5dc2e3…` stable (4 total fetches, 2 mine), page digest fetch-time-only (3 fresh digests, all distinct, none equal `436c0f63…`). No falsity, no new overstatement found in the row's anchor or teaches cells.
- `.patch` mbox is internally consistent with the head: 3 commits, final `From a214355…` (patch line 106); the row never claims otherwise.
- claims.json amendment numbers reproduced: baseline 6 open (named 6, substance 6) → 0 at REV; `--strict` exit 1 → 0. SOURCES "No in-place S001–S032 cell changed" (corpus/lessons/round-18.md:42) holds: zero deleted lines, S032 row hash identical across baseline→REV, rows 32→36 (round-18.md:43).
- Evidence file at REV identical to worktree; recorded `s032_recorded_digest` `436c0f63…` never observed in any of 6 fresh fetches (21 cumulative distinct-digest observations across seats) — supports "never reproduces" [INFERENCE from repeated non-observation].

## Findings (residual risk; none breaks the claim)

1. **[tool, minor] `s032-digests-evidence` is weaker and mislabeled vs its own detail text.** routed-defects.py:776-781 passes on `len(digests) >= 2` over ALL 64-hex strings anywhere in the JSON (`_hex64s_in`, :718-728). The reported "5 distinct 64-hex page digests" decomposes as 3 page + 1 patch + 1 superseded S032 recorded digest — only 3 are page digests. corpus/lessons/round-18.md:66 states the rule as "40-hex head plus ≥2 recorded page digests"; the artifact itself satisfies the stricter rule (3 genuine page digests), so the corpus claim stands, but the implemented check would also pass with zero page digests (e.g. two patch digests alone).
2. **[tool, minor] `s033-anchor-commit` is a shape check, not an identity check.** routed-defects.py:757-763 only regexes a 40-hex in the anchor cell; a well-formed wrong commit would pass. Compensated here by my live ls-remote + API match (both `a214355…`), so the pinned value is true at REV.
3. **[corpus, wording] The defect's literal remedy ("Anchor the row … or qualify the digest as fetch-time only", spotcheck:147) was implemented as supersession: S032's own row (SOURCES.md:38) still displays `436c0f63…` unqualified.** The supersession is discoverable only via S033's teaches cell and round-18.md:42,56. The digest appears nowhere else (grep: no `436c0f63` in the r17 knowledge entry or round-17.md), and the lesson explicitly discloses the keep-unchanged choice, so this is not an overstatement — but a reader citing S032 alone still meets an unqualified digest. [INFERENCE: acceptable under append-only discipline; substance of the remedy met.]
4. **[corpus, minor] S033 teaches cell attributes non-reproduction to "(per-request tokens)"** while the evidence file's own ScoutPr9348Reopen note names a second source: "residual after token normalization is the repo open-PR counter". Conclusion ("fetch-time only") unaffected; the cause list is partial.
5. **[verification gap] "9 fetches, 9 distinct page digests" (RevBaseS032) and "4/4 … equal length 403382" (ScoutPr9348Reopen) are seat-asserted strings with no enumerated digests retained** — not re-derivable from artifacts. Independent of them, my own 3+3 fetches establish non-reproduction and byte-stability of the patch. Live page length is now 403460 ≠ 403382, i.e. the page also drifts across time, which further supports (never undermines) the fetch-time-only conclusion [observation].

## Verdict

Closure of R17-S032-DIGEST is **deserved**: every checkable number/hash/state claim in the correction re-derives true against live external ground truth and against Git objects at REV; the red-at-baseline → green-at-REV delta reproduces exactly as claimed. Findings 1–2 are checker-precision residuals (the tool under-verifies what the corpus separately gets right); findings 3–5 are wording/retention residuals already disclosed or immaterial to the conclusion.

No tools installed (none needed).
