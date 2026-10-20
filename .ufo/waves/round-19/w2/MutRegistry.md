# R18-REGISTRY-PINNED mutation check

## Finding — Medium: the registry gate checks path resolvability, not that the path is the probe's pinned-value source

**Observation.** At observed `refs/heads/main` tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, the `go-buildinfo-probe` row at `SKILL.md:545` cited `.ufo/waves/round-17/tools/buildinfo-probe.py` as the file holding the Go build-info constants. In an isolated clone at that tip, strict `routed-r18.py` returned `open_count=0`, `substance_open=0`, exit 0.

I changed only that row in the `/tmp` clone to cite the nonexistent `.ufo/waves/round-17/tools/not-a-real-buildinfo-probe.py`, committed the mutation there as `92076b0782a44e29c38a19b7f79784858c8d9e0e`, and reran the strict gate. `R18-REGISTRY-PINNED` reopened (`named=true`, `substance=false`, reason `go-buildinfo-probe: Pinned values names no path that exists at REV`); `open_count=1`, exit 1.

I then changed only that row to cite the unrelated, existing `corpus/lessons/round-18.md`, committed as `b39d2abc8ed5e7921fe55768977b9ba89642e34a`, and confirmed that path exists in that revision (`git cat-file -e ...:corpus/lessons/round-18.md`, exit 0). The lesson is about routed R17 defects, revision pins, and the Swiss-map replay (`corpus/lessons/round-18.md:1-10`), not the build-info probe's constants. Despite this unrelated path, the strict gate returned `R18-REGISTRY-PINNED` `substance=true`, `open_count=0`, exit 0.

**Inference.** Yes: this counterexample demonstrates that this check establishes resolvability only. In `.ufo/waves/round-19/tools/routed-r18.py:267-281`, it lists the revision's tracked paths and passes when *any* extracted `.ufo/` or `corpus/` citation is present; it does not establish that the citation identifies the stated probe source or validate file contents/digests. The row-specific green selftest (`routed-r18.py:376-385`) tests an existing path, but does not distinguish a semantically unrelated existing path.

## Commands and exit codes

All mutations and routed checks below were confined to `/tmp/kr19-w2-MutRegistry-kTAHRJ`; no production files were edited.

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
# exit 0; 279e8b19c51658bfd05b9e31a1c0894ab2e70537

git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-MutRegistry-kTAHRJ && git -C /tmp/kr19-w2-MutRegistry-kTAHRJ checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537 && git -C /tmp/kr19-w2-MutRegistry-kTAHRJ rev-parse HEAD && git -C /tmp/kr19-w2-MutRegistry-kTAHRJ status --short
# exit 0; detached HEAD matched the observed tip; status output empty

python3 -I -B /tmp/kr19-w2-MutRegistry-kTAHRJ/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutRegistry-kTAHRJ --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# exit 0; open_count=0, substance_open=0

git add SKILL.md && git -c user.name=MutRegistry -c user.email=mutregistry@example.invalid commit -q -m 'test registry path absence' && git rev-parse HEAD
# exit 0; 92076b0782a44e29c38a19b7f79784858c8d9e0e

python3 -I -B /tmp/kr19-w2-MutRegistry-kTAHRJ/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutRegistry-kTAHRJ --rev 92076b0782a44e29c38a19b7f79784858c8d9e0e --strict
# exit 1; only R18-REGISTRY-PINNED reopened, open_count=1

git add SKILL.md && git -c user.name=MutRegistry -c user.email=mutregistry@example.invalid commit -q -m 'test unrelated existing registry path' && git rev-parse HEAD
# exit 0; b39d2abc8ed5e7921fe55768977b9ba89642e34a

git cat-file -e b39d2abc8ed5e7921fe55768977b9ba89642e34a:corpus/lessons/round-18.md
# exit 0

python3 -I -B /tmp/kr19-w2-MutRegistry-kTAHRJ/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutRegistry-kTAHRJ --rev b39d2abc8ed5e7921fe55768977b9ba89642e34a --strict
# exit 0; R18-REGISTRY-PINNED substance=true, open_count=0
```

## Residual risk and verification gaps

- An incorrect but tracked path can satisfy `REGISTRY-PINNED`; the check cannot by itself support a claim that the registry's cited file is the actual source of the stated pinned values.
- No LSP device/server was available: `read xd://lsp` returned “No such tool: xd://lsp”. I used literal grep only to locate `SKILL.md:545`; semantic evidence above is from direct reads of the checker and controlled runs, not grep output.
- The requested mutation was exercised through the real strict checker in a detached clone. The standalone `--selftest` was not run; no broad suite was run.
