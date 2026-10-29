# Receipts — seat SrcReopenUnblob, round-50 attempt-2 wave 3 (2026-10-29)

All commands run from `$S=/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenUnblob` (removed after receipts were copied here). No REA invocation, no git mutation, no lane-tree write outside this seat's report + artifact dir. No tool installs (operator tooling authorization not used). Disk-guard status before the pass: `/fast/scratch/hyaku` 39% use, 497.2G free (exit 0).

## R1 — Fetch unblob 26.6.4 SquashFS handler source

- Command (cwd `$S`):
  `curl -sS -o unblob-26.6.4-squashfs.py -w 'HTTP_STATUS=%{http_code} SIZE=%{size_download}\n' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
- Exit code: 0
- stdout: `HTTP_STATUS=200 SIZE=19842`
- UTC: 2026-10-29T20:34:12Z
- Body: 19,842 bytes, 590 lines, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`
- Saved: `unblob-26.6.4-squashfs.py` (this dir)
- Match: attempt-1 reference (19,842 B, sha256 `2d7b901b…`) and S108's pinned hash — byte-identical.

## R2 — Baseline census validate (pristine scratch copy of corpus/SOURCES.md)

- Fixture: `$S/fixture/kaidoku-shokunin/` = lane copy of `corpus/` (whole dir) + `SKILL.md` + `tools/round-27/xpin-attribute.mjs`, so every used-by path (`corpus/…` ×248, `tools/…` ×1, `SKILL.md` ×1) resolves under the fixture lane dir (usedby_findings checks `[ -e "$dir/$path" ]` with `dir = realpath(dirname(file)/..)`; under `--file` the lane id prints as the literal `file`).
- Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/fixture/kaidoku-shokunin/corpus/SOURCES.md`
- Exit code: 0 (`file ok` line present)
- UTC: 2026-10-29T20:38:19Z
- stdout sha256: `ee9b71f65fb8e2283949707de467530c62ced908b140a0da3ed2ae78c4852d21`
- stdout: 18 × W04 warnings + `file ok …` (pre-existing W04 includes `file W04 S112 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes`)
- Saved: `validate-baseline.out` (this dir)

## R3 — Census validate after appending draft S245 row

- Change: draft S245 row appended directly after the S248 row (line 159 of the fixture copy; Registry table still contiguous, before the blank lines and `## Paths`).
- Command: identical to R2, run on the modified copy.
- Exit code: 0 (`file ok` line retained)
- UTC: 2026-10-29T20:40:04Z
- stdout sha256: `806a9353c9600b80070d333dc54ef65a715ee2eb89026937cc91d7881bc6f073`
- stdout: 19 × W04 + `file ok …`. Diff vs R2 is exactly one line:
  `file<TAB>W04<TAB>S245 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py across scopes`
  (the trailing "Command exited with code 1" in the session log was `diff`'s own exit code for a non-empty diff, not a tool failure)
- Saved: `validate-s245.out` (this dir)
- No E-code, no E04, no E11 on the draft row; the only new finding is the predicted W04, which per the script's own contract "warnings do not affect clean lanes" (validate exit stays 0).
