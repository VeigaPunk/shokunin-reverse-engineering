# ToolCustody — round 19 wave 2

Reviewed the custody-pair diff from baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` to the observed `refs/heads/main` tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`. No production files were edited; this report is the only lane write.

## Findings (severity order)

### P3 — Registry selftest count is inconsistent with the landed test

- **[Observation]** The modified custody-pair row at `SKILL.md:449` still says `28 fixture cases` in its self-invocation text, while the same row's round-19 note says `selftest 31 cases`. `README.md:229-252` also documents 31 cases, including the two round-18 repo-header cases and the round-19 subdirectory case. The observed selftest passed 31/31.
- **Impact:** The registry's selftest inventory is internally contradictory and understates the current suite in the field that describes self-invocation.
- **Recommendation:** Change the registry's `28 fixture cases` to `31` and list the three repo-context cases consistently with `README.md:244-248`.

## Behavior and compatibility review

- **[Observation]** The fix is correctly scoped: `cmd_capture` resolves the `--repo` path (`.ufo/gates/custody-pair/custody-pair.py:773-779`); `repo_context` retains that path as `arg`, obtains `root` from `git rev-parse --show-toplevel`, and runs HEAD, branch-tip, and status queries against the same `repo` (`:397-420`). `render_receipt` emits both `repo-root` and `repo-arg` (`:424-443`).
- **[Observation]** The selftest's `repo-root-is-toplevel-not-subdir-arg` fixture creates `repo/sub/deep` and checks that `repo-root` is the top level, the subdirectory is not `repo-root`, `repo-arg` is the supplied directory, and the branch-tip relation remains true (`:1420-1449`). The README names this case and states the 31-case total (`README.md:229-252`).
- **[Inference]** The red condition is real by inspection: baseline code initialized `root` to the `--repo` path, while the new assertion requires the parent repository top level and explicitly rejects the subdirectory. I did not run a pre-fix mutation; only the requested selftest was executed.
- **[Observation]** Keeping `RECEIPT_VERSION = 2` is compatible with the in-repo verifier: the change adds a comment/header line (`repo-arg`) and corrects the `repo-root` value, without changing PATH stanza fields (`:227`, `:429-443`). `parse_receipt` reads the version and splits/parses PATH stanzas (`:532-553`); `cmd_verify` consumes those parsed sections (`:838-869`) and does not consume repo header metadata. The round-19 verifier caller still invokes `selftest --scratch` expecting exit 0 (`.ufo/waves/round-19/verify.py:528-530`); the registry capture invocation remains applicable (`SKILL.md:449`). No in-repo caller migration is indicated.
- **[Inference / residual risk]** An out-of-repository consumer that interprets `# repo-root:` as the former `--repo` argument could observe the corrected meaning under v2. The new `repo-arg` field preserves that path, but external readers were not available to inspect; this is not evidence that such a consumer exists.

## Verification and gaps

Commands and observed exits:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
  -> 279e8b19c51658bfd05b9e31a1c0894ab2e70537; exit 0
mktemp -d /var/tmp/kr19-w2-custody-XXXXXX
  -> /var/tmp/kr19-w2-custody-87zzsl; exit 0
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /var/tmp/kr19-w2-custody-87zzsl/repo
  -> exit 0
git -C /var/tmp/kr19-w2-custody-87zzsl/repo checkout -q --detach 279e8b19c51658bfd05b9e31a1c0894ab2e70537
  -> exit 0
python3 -I -B /var/tmp/kr19-w2-custody-87zzsl/repo/.ufo/gates/custody-pair/custody-pair.py selftest
  -> CUSTODY_PAIR_SELFTEST: CLEAN cases=31 passed=31 failed=0 exit=0; process exit 0
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=8 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0..279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- .ufo/gates/custody-pair/custody-pair.py .ufo/gates/custody-pair/README.md
  -> exit 0
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=5 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0..279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- SKILL.md
  -> exit 0
rm -rf -- /var/tmp/kr19-w2-custody-87zzsl /dev/shm/custody-pair-selftest-6fyzk9q3
  -> exit 0
```

- **[Observation]** Only the custody-pair selftest was run; no build, broad suite, or mutation test was run. The isolated clone and selftest scratch directory were removed.
- **[Observation]** No LSP device is mounted (`read xd://lsp` returned “No such tool”). Caller/header searches therefore used literal text search as fallback, not semantic proof; LSP references/definition/diagnostics are unavailable in this session.
- **[Verification gap]** The subdirectory case asserts `repo-HEAD-is-branch-tip: yes`, but does not compare the receipt's exact HEAD/tip hashes or dirty value with the fixture repository. The implementation uses the same `repo` argument for those Git queries (`:411-420`), so this is a test-coverage limit, not an observed behavior defect.
