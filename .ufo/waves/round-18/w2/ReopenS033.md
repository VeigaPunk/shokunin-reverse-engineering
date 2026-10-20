# Re-open SOURCES S033 — wave 2 falsification (KaidokuR18.ReopenS033)

HOLDS

REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (baseline `9011581d84527ba34c675f9cf912e54d2e72d470`). 2026-10-20, live upstream re-check. No tool installs; no lane writes except this report. All `git`/`git show` reads at REV.

## Row under test

`corpus/SOURCES.md:39` at REV (`git show REV:corpus/SOURCES.md`, column set at `corpus/SOURCES.md:5`): id S033, source Ghidra PR #9348 (+ `.patch` URL), kind `community`, tier `B`, scope "Same subject as S032 … author's claim that Ghidra's `GoMapType` lacks `internal/abi.SwissMapType`; a lead, not a mechanism proof", anchor = title + state open/not merged + head `a214355…` + `.patch` sha256 `ae5dc2e3…` stable on two fetches, teaches opens `supersedes S032 —`, status `mined`, opened `2026-10-20`, recheck `90d`, used-by `corpus/lessons/round-18.md`.

## Checks (command → exit code → result)

1. Head commit reproduces. OBSERVATION:
   `git ls-remote https://github.com/NationalSecurityAgency/ghidra refs/pull/9348/head` → exit 0 → `a214355498e84aa86280be0c31c955aaf94f2d12  refs/pull/9348/head` = row's head (SOURCES.md:39) and `.ufo/waves/round-18/evidence/s032-digests.json` `pull_head` (tracked at REV, `git show REV:<path>` exit 0).

2. `.patch` digest stable. OBSERVATION (three fresh fetches, 2026-10-20):
   `curl -fsSL …/pull/9348.patch -o pN.patch; sha256sum pN.patch` → exit 0 ×3 → `ae5dc2e3e28f3f64feb32ba7df9659626a5173328b83a6b5e3914fcfa3b70a11` all three, 9115 bytes each = row's digest exactly; matches both digests recorded in `s032-digests.json`.

3. Title verbatim + state. OBSERVATION:
   `curl -fsS https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348` → exit 0 → `state=open merged=False`, `title='Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries'`, `head_sha=a214355…` — title byte-equal to anchor's Title cell and to the Gate quote. INFERENCE: `merge_commit_sha` is also populated (`b25164e7…`) while `merged=False`; GitHub fills it for open PRs as a preview merge ref — not a merge; row's "state open, not merged" stands on `state`/`merged`.

4. Scope faithful to PR content. OBSERVATION:
   patch text (same fetch as 2): `Subject: [PATCH 3/3] Golang: resolve stripped 1.24/1.25 maps as SwissMapType`; body names `internal/abi.SwissMapType` for Go 1.24/1.25; counts `SwissMapType`=6, `GoMapType`=7. Supports scope's "author's claim that `GoMapType` lacks `internal/abi.SwissMapType`"; "a lead, not a mechanism proof" matches the unmerged community status (tier B). OBSERVATION: patch commit subjects differ from the PR title (patch 1/3 is "don't let one bad type abort all type markup"); the row anchors the PR title, which is what the API and PR page carry — no conflict.

5. Supersession rationale reproduces. OBSERVATION:
   `curl -fsSL …/pull/9348 | sha256sum` → exit 0 → `21de8209131d4657007d667c483a49c3366a2eab69b005847c4b82373b8e1136` — a fresh digest differing from S032's recorded page digest `436c0f63…` (SOURCES.md:38) and from all three L1 page digests in `s032-digests.json`. Confirms teaches: rendered-page sha256 is fetch-time only; the patch digest is the stable identity. (`s032-digests.json` records exactly 3 distinct page digests and 2 equal patch digests.)

6. Gate quote. OBSERVATION: `corpus/lessons/round-18.md:32-34` at REV — S033 quote `Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries` = 9 words ≤ 25, contiguous, byte-equal to live PR title (check 3). Admit row at `round-18.md:24`; tier summary "3 tier A, 1 tier B community" at `round-18.md:43` matches S033 being the sole tier-B/community new row; R17-S032-DIGEST correction at `round-18.md:56` names the same title/state/head/patch-digest anchor.

7. Bookkeeping hygiene. OBSERVATION: `git diff 9011581...REV -- corpus/SOURCES.md` → numstat `11 1`; deleted lines contain no `^-|S0` row (grep count 0, exit 1); the single deletion is the route-diagnosis census bullet (S032 dropped from its tail), additions are rows S033–S036 plus census bullets. Matches `round-18.md:42` "No in-place S001–S032 cell changed".

## Verdict reasoning

Agree with the row as filed. Every anchor element (title, open/not-merged state, head `a214355…`, patch sha256 `ae5dc2e3…`) reproduces live on 2026-10-20, the tier/kind (community, B) and hedged scope ("a lead, not a mechanism proof") are correctly conservative for an unmerged third-party PR, the Gate quote is verbatim and within the word cap, and the supersession of S032 is justified by a reproduced page-digest non-reproducibility plus a stable patch digest. No discrepancy found. Only caveat (INFERENCE, non-blocking): anchor stability rests on the PR staying open at head `a214355…`; if the PR is updated or merged, the `90d` recheck should re-run checks 1–2 — the row already anticipates this by keying on content-addressed identity rather than page bytes.
