# C1 REGISTRY-PINNED review

Axes: calibration (C1); freshness and depth were not assessed.

## Findings

### Medium — `s_registry` can falsely close REGISTRY-PINNED on an unrelated existing path

**Observed in the immutable main snapshot:** `SCORECARD.md:2488` says the `pins` row has no persisted baseline and `buildinfo-probe` names its constants' source; `corpus/lessons/round-19.md:61` makes the corresponding named correction. `SKILL.md:542` says `pins` is a probe with no persisted expected digest, and `SKILL.md:545` names `.ufo/waves/round-17/tools/buildinfo-probe.py`. Re-reading those source blobs supports the current statements: `pins.py:62-72,75-106` snapshots values at instants and compares two snapshots without an external expected digest; `buildinfo-probe.py:29-53` contains the magic, header, field, and info-sentinel constants. Thus **the current main row is substantively correct**; no actual false close was found at main.

The counter is weaker than that substance. `routed-r18.py:263-282` only requires one `Pinned values` token to be the special no-baseline phrase, or one extracted `.ufo/...` / `corpus/...` string to occur in the revision's tree. It does not verify that the path is the probe source or that the cited file contains the claimed constants. The existing selftest codifies this looseness: `routed-r18.py:376-385` marks a `go-buildinfo-probe` row pointing to `corpus/lessons/round-19.md` green merely because the path exists.

**Observed focused mutation (isolated clone initially detached at main):** I changed only the mutant clone's `SKILL.md:545` pin to `corpus/README.md`, which exists but is the corpus index (`corpus/README.md:1-9`), not the probe source, and committed that mutation as `b233317e6564e5d25772fa13bb7335fcea5466da`. With the unchanged named corrections still present, `routed-r18.py --strict` reported `R18-REGISTRY-PINNED named=true, substance=true`, `open_count=0`, exit 0. This is a reproduced **false-close capability**, not a finding that main itself is false-closed. The baseline-to-main count therefore overstates the strength of this one substance check unless the actual row is separately inspected as above.

### Low — a failed recursive tree listing is reported as an open defect, not unusable input

**Observed in controlled error injection:** `s_registry` captures the `git ls-tree -r --name-only` return code at `routed-r18.py:267` but never checks it; a failed listing leaves `paths` empty and falls through to the “names no path” failure at lines 279-282. I used a temporary `git` wrapper in the isolated clone that returned 42 only for that `ls-tree -r` call and delegated other Git calls. The main-revision counter then marked only REGISTRY-PINNED substance false (`open_count=1`) and strict-exited 1, rather than reporting could-not-evaluate. The tool contract says unusable input exits 2 (`routed-r18.py:13`); the failure path loses that distinction. This was injected, not observed on B or main.

## Counter results and commands

The observed `refs/heads/main` was `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (rev-parse exit 0). I used a `--no-hardlinks` temporary clone detached at that exact commit. Its routed tool blob was `ae1651db86bf3c1262025f624b392c4851f4cb42`; the lane working-tree tool hashed to `07f2c527c1d24b6036acd8bd8b1229e2598acac9`, so I discarded the initial working-tree-script invocations and used only the exact-main clone for the results below.

- `python3 -I -B /tmp/kr19-w2-regpin.06pVq2/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-regpin.06pVq2/repo --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict` — `open_count=7`, `named_open=7`, `substance_open=7`; REGISTRY-PINNED was named=false/substance=false; counter exit 1.
- `python3 -I -B /tmp/kr19-w2-regpin.06pVq2/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-regpin.06pVq2/repo --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict` — `open_count=0`, `named_open=0`, `substance_open=0`; REGISTRY-PINNED was named=true/substance=true; counter exit 0.
- The same command with `--rev b233317e6564e5d25772fa13bb7335fcea5466da --strict` on the false-pin mutation — `open_count=0`, REGISTRY-PINNED named=true/substance=true; counter exit 0.
- `PATH=/tmp/kr19-w2-regpin.06pVq2/repo/.testbin:$PATH python3 -I -B /tmp/kr19-w2-regpin.06pVq2/repo/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-regpin.06pVq2/repo --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict` — injected `ls-tree -r` failure yielded `open_count=1`, REGISTRY-PINNED named=true/substance=false; counter exit 1.

No false open was observed on the valid B or main inputs; B's seven-open result is expected. The failure-injection result is the only observed false-open classification. The only production-tree write for this assignment is this report; mutation and fault-injection files/commit were confined to the temporary clone.

## Residual risk and verification gaps

- The direct evidence supports the *current* `pins` and `go-buildinfo-probe` row contents, but the counter does not check their semantic relation. A future wrong-but-existing path can close the defect. The false-close was tested; no production files were changed.
- Scope was the REGISTRY-PINNED substance, not an independent audit of the other six `s_*` checks. Their green/red states above are the counter's output only.
- Main `SCORECARD.md:2493` still says the final measured verdict will be appended after verification; this report's counter measurement is not an edit to that row.
- No `lsp` device is mounted (`read xd://lsp` returned “No such tool”), so status/references/definition/diagnostics were unavailable. Literal grep was used only to locate correction lines; conclusions above come from exact-commit reads and focused execution, not grep as semantic proof.
- No build, broad suite, formatter, REA call, or install was run. `routed-r18.py --selftest` was not run; its relevant registry fixture was inspected at `routed-r18.py:376-385` and the false-close behavior was reproduced separately.
