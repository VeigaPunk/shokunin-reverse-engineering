# Round-23 timestamp review

## Findings (by severity)

### Medium — `--strict` does not reject unreviewed binary skips

**Observed source:** `corpus/QUALITY.md:33` requires every zoned timestamp in the round's committed evidence tree to be checked and requires the strict checker to exit 0. The inherited checker at `.ufo/waves/round-20/tools/evidence-timestamps.py:207-210` skips an entire blob if it contains any NUL byte; it records the path but does not scan any lines. Its output says skipped blobs “need review” (`:254-255`), while strict mode returns 1 only for a nonzero `unexempted_finding_count` (`:448-450`), not for a skip. Thus an unreviewed NUL-containing file can coexist with a successful strict exit; exit 0 alone is not evidence that every zoned timestamp was checked. This is a declaration/gate gap, not an observed future-dated timestamp in round 23. The current run below had zero skips.

**Committer-time check:** The implementation does use the intended time field: `_parse_blame` consumes Git's `committer-time` (`:129-161`), and `collect` compares each parsed timestamp against that line's committer epoch converted to UTC (`:212-240`). It does not use blame's author-time. No defect found in this part of the inherited rule.

## Round-23 command and observed run

Use this from the lane root **after the final shipping commit**, so `HEAD` is the shipping revision. This adds a fail-closed zero-skip condition to the inherited strict command; it prints skip paths and fails if any remain. Do not use `--allow` for the shipping scan.

```bash
set -o pipefail
python3 -I -B .ufo/waves/round-20/tools/evidence-timestamps.py \
  --root "$PWD" --rev "$(git rev-parse HEAD)" \
  --path .ufo/waves/round-23 --strict \
| python3 -I -c 'import json,sys; r=json.load(sys.stdin); s=r["summary"]; print(json.dumps(s, sort_keys=True)); [print("SKIP", x["path"], x["reason"]) for x in r["skipped"]]; sys.exit(1 if s["files_skipped"] else 0)'
```

**Observed command at current `HEAD` `a3c92eb6bc70984e90ae5b895412de978840b2c5`:**

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/evidence-timestamps.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev HEAD --path .ufo/waves/round-23 --strict
```

Exit 0; stderr empty. Summary: `files_scanned=3`, `files_skipped=0`, `finding_count=0`, `unexempted_finding_count=0`. The three tracked paths at that revision were `before-r22-c1.json`, `claims.json`, and `start-census.json`. The same zero-skip wrapper above also returned successfully on this revision.

**Scope limitation:** This is not a round-23 shipping scan. The current `HEAD` is the baseline and `git status --short --untracked-files=all -- .ufo/waves/round-23` reports 420 untracked entries; the checker reads Git objects at `--rev`, not the working tree (`:8-10`, `:81-114`). The observed exit 0 covers only those three committed paths. Run the command above again with the actual final shipping revision at `HEAD`; retain its JSON summary and exit. `.ufo/waves/round-23/.gitignore:1-2` excludes `/runtime/` and `/worktrees/`, so those ignored paths are not part of the current committed scan.

## Residual risk and verification gaps

- A final shipping revision has not been measured. No claim is made about timestamps or binary skips in the final round-23 tree.
- A skip-free wrapper prevents silent skips; if a future workflow permits skips, each listed skipped blob needs a separate retained review before claiming completeness.
- LSP is unavailable in this environment: `read xd://lsp` returned `No such tool`. Source conclusions above come from direct reads at the cited lines; search output was used only to locate sources.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewTimestamps.md` — self SHA-256 is supplied in the final handoff.

## Installs

None.
