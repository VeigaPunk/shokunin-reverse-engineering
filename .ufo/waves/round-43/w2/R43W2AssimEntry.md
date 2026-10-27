# R43W2AssimEntry — assimilation entry falsification

## Verdict

No actionable falsification found in the assigned checks. The landed knowledge entry's S136/S137 provenance order, release matrix, digest values, corrected round-36 claims, S107 overlap qualification, and limits calibration agree with the retained evidence reviewed here. This is a read-only review of committed lane bytes at measured `HEAD` **5856614ac4bf7f2363bbcd1956644474a82108e5** (freeze `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`). The lane worktree had unrelated/untracked orchestration changes; none were used as evidence.

## Checks and evidence

1. **Provenance trio order — consistent.** Landed entry `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md` starts with `source: S136`, then `source: S137`, followed by `verified-at:`, `recheck:`, and `ground:`. The S136 and S137 citations resolve to the matching `corpus/SOURCES.md` rows. The landed S137 citation does not mistakenly assign the asset list to the rendered page; it says tag links only and sends asset facts to S136.

2. **Tag, size, digest values — consistent with API receipt.** Retained source `.../w1/artifacts/R43ScribeAssim/receipts/rel-r43.json` has SHA-256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0`; receipt projection `capture-projection.txt` lines 2–56 records the eight tags/date/body lengths and 44 assets. The entry's eight-row table agrees with these tag/date/asset counts and the principal package sizes. Its six v4.5.1-6 digests match the API projection receipt and the S136 registry row; for amd64, `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` agrees with S107. The matrix's dbgsym size statements also match the projection receipt. The retained receipt supports the crucial exception: `sasquatch-v1.0` has only the two amd64 assets; the other seven releases have six assets each.

3. **R36 falsifications — corrected, not reversed.** `corpus/lessons/round-36.md` line 42 states the two rejected assertions: every release has a package per architecture, and a release body pairs upstream 4.5.1 with package 1.0. The landed entry directly falsifies each universal: v1.0 is amd64-only; no body contains standalone `1.0`. The retained `version-pair-scan.txt` gives body lengths `645,560,0,0,0,38,0,0` and no standalone token in any body, with the only body naming upstream 4.5.1 being v4.5.1-1's “Rebased on top of squashfs-tools 4.5.1”.

4. **S107 overlap citation — accurate and bounded.** `corpus/SOURCES.md` S107 identifies v4.5.1-6, its publish date, six-asset set, and amd64 digest, and explicitly limits itself to that release's asset set/date/amd64 digest. The entry correctly identifies these as overlap and distinguishes new coverage (eight-release matrix, v1.0 architecture gap, digest-presence pattern, arm64/armhf digests, body finding). It does not claim S107 independently supports those broader findings.

5. **Body-limit calibration — consistent.** The entry separates API fields from rendered-page evidence and states that the matrix is an API observation, not downloaded/verified package content or a behavior/licensing claim. It discloses that only the newest release has API-published digests and older assets are not downloaded. The API-capture size comparison is explicitly normalized: round-42's compact receipt is 87,700 bytes without trailing newline, while this round's raw pretty response is 107,313 bytes; the apparent delta is serialization, not payload drift. This matches the grounding receipt's comparison of both captures reserialized to 87,700 bytes and its seven mutable `download_count` differences. For page instability, the entry's 349,255-byte `89e7377d…` fetch and same-size `56632d0f…` second fetch match the scribe retained receipt and page-fetch2 record; its round-42 349,266-byte `71ebf160…` reference matches the grounding receipt. The stable recheck is a projection rather than a response digest, consistent with the disclosed volatile counters and page bytes.

## Commands / outputs / exit codes

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --oneline -5 && git -C ... rev-parse HEAD && git -C ... status --porcelain | head -20` — observed tip `5856614ac4bf7f2363bbcd1956644474a82108e5`; unrelated modified `w2.ready`, root `SCORECARD.md`/`SHONEN.md`, and untracked orchestration paths were present. Exit 0.
- File reads (read-only): frozen plan; landed entry; S136/S137 and S107 in `corpus/SOURCES.md`; round-36 lesson lines 38–46; `R43AssimGround.md` and its fetch receipt; scribe `capture-projection.txt`, `capture-diff-r42-r43.txt`, `version-pair-scan.txt`, `page-fetch2.txt`, `sha256-manifest.txt`. Tool reads returned content; no whole-repository check was run.
- Attempted `read xd://lsp` as availability check: returned “No such tool: xd://lsp” and listed mounted devices, with no LSP device available. Thus no semantic references/definition/diagnostics run; conclusions rely on direct text and retained receipt bytes, not grep as semantic proof.
- No network fetch, firmware access, extractor, test, formatter, linter, install, or scratch probe was run. No scratch directory was created; no cleanup was needed. The artifact directory is reserved and empty.

## Residual risk / gaps

This seat checked retained bytes and receipt consistency, not the live upstream endpoint, package-byte identity, or the factual truth of upstream-published metadata beyond those retained captures. Those are outside this assigned read-only reproduction. No LSP service was mounted, so semantic cross-reference analysis was unavailable.

Report: `.ufo/waves/round-43/w2/R43W2AssimEntry.md`
