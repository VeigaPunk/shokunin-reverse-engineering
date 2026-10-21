# W2 EntryPeErratum-3 — round-20 erratum on `corpus/knowledge/2026-10-13-pe-surface.md`

**VERDICT: HOLDS** — prefix preservation is byte-exact and the re-run sweep reproduces. One phrasing nit (no substance impact).

Checked 2026-10-21T04:21:23-03:00. All rev-scoped reads via `git show`/`git cat-file` at B=14f0260ad319ecc26994381b2415d5a999003375, S=5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 (never the working tree). Scratch: `/tmp/entry-*` only, outside the lane.

## 1. Append-only prefix preservation — HOLDS (observation)

- `git show 14f0260a…:corpus/knowledge/2026-10-13-pe-surface.md` → 8889 B, sha256 `e238dc87736916f000564a90665d84a6e6887f91b18c249354e6bf8f71d4cc39` (exit 0).
- `git show 5c0b46c4…:corpus/knowledge/2026-10-13-pe-surface.md` → 9495 B, sha256 `4b8cf81bdf0fe2a60af3eaddca813ebdc16f8b678df984d7a10d4101ddcd6f38` (exit 0).
- `cmp` B vs S → `EOF on /tmp/entry-peesurface-B.md after byte 8889` (exit 1 = B is a strict prefix); `cmp` B vs `head -c 8889` of S → exit 0. First 8889 bytes byte-identical.
- `git diff --stat B S -- <path>` → `1 file changed, 8 insertions(+)`, 0 deletions; single hunk `@@ -78,3 +78,11 @@` appending at end (erratum = S:82-89).
- History: exactly one commit between B and S touches the file — `8451e471095464aea05aa9cc09aca3c8852cea23`, committer `2026-10-20T18:14:34-03:00`, author `2026-10-20T18:01:54-03:00` ("round-20: integrate C2 knowledge … W1 reports"). Append-only holds per-commit, not just net effect.
- Erratum date "2026-10-20" is date-only (no zone, outside the D2 explicit-zone gate); corroborated by commit committer time, not future-dated vs the 2026-10-21 check clock.
- Working tree matches S for this file (`git diff --stat S -- <path>` empty, exit 0) — no drift.

## 2. Re-run sweep reproducibility — HOLDS (observation)

- Exact erratum command re-run: `for t in rabin2 r2 radare2 rz-bin rizin xxd; do command -v $t; done` → `/usr/bin/rabin2`, `/usr/bin/r2`, `/usr/bin/radare2`, `/usr/bin/rz-bin`, `/usr/bin/rizin`, `/usr/bin/xxd`, exit 0. All six resolve under `/usr/bin`, as the erratum claims.
- `rizin -v` → `rizin 0.8.2 @ linux-x86-64` (exit 0) — matches erratum "(rizin 0.8.2)" and the entry's retained `evidence/c2/rizin/rizin-version.stdout:1` at S.

## 3. Erratum's cross-reference and honesty — HOLDS (observation + inference)

- Referenced `corpus/knowledge/2026-10-20-r20-rizin-command-observation.md` exists at S (10255 B); its PE leg targets the round-2 setuptools `cli-64.exe` (sha256 `bbb3de57…`, the PE this file discusses at B:78-81), receipts under `.ufo/waves/round-20/evidence/c2/rizin-pe/` with `ev_` ids (`01-iI` → `ev_42df7881…`). Spot-checked at S: `01-iI/receipt.json`, `jq-iI-1.stdout`, `rizin-version.stdout`, `carrier-identity.md` all present (`git cat-file -e` OK). "execute-rizin-command is now held on this PE" is accurate.
- `command -v mono monodis pedump` → exit 1 (all absent, 2026-10-21): the "mono/monodis/pedump were not re-checked" disclosure is conservative; they remain absent, so re-checking would not have changed the erratum's substance.

## 4. Phrasing nit — not a falsification (observation)

Erratum says "re-running **its own sweep**", but its quoted command is not the original verify line at B:68 (`for t in rabin2 r2 radare2 rz-bin mono monodis pedump; …`). It is the original 17-tool sweep's missing set (B:66-67: rabin2, r2, radare2, rz-bin, mono, monodis, pedump, xxd) minus the mono family, plus `rizin` — which the original missing list omits even though its own heading (B:65) names rizin (internal inconsistency in the historical 2026-10-13 text, preserved unmodified as required). The erratum transparently quotes the exact command run and discloses the mono skip, so this is loose wording, not misrepresentation.

## Residual risk / gaps

- Sweep reproduces on 2026-10-21 only; PATH state is environment-dependent, not pinned (inherent to a `command -v` claim).
- Did not re-execute REA receipts (out of scope; ReplayRizin/RerunRoutedS seats own replay). Evidence existence at S verified, contents spot-read only.
