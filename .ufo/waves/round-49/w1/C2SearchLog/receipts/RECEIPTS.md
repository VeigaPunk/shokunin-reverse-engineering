# C2SearchLog receipts (A8 review, round 49 wave 1)

All UTC 2026-10-28. Scratch: `/fast/scratch/hyaku/kaidoku-r49/C2SearchLog` (removed after copy). Lane tree: read-only (`git show`, `git grep`-class reads only). Mutations ran in clone `.../C2SearchLog/clone` (identity `r49-dev`, set in the clone only; toplevel asserted equal to the clone dir before commit). No tool installed or upgraded.

| # | command (abridged; full paths under scratch) | exit | output / sha256 (stdout unless noted) |
|---|---|---|---|
| R1 | `bash .ufo/waves/round-49/draft/mkclone.sh <clone>` | 0 | `DEV_FREEZE=541044b67aa88025be78900666086b832de3d3d3` — `mk.out` sha256 031b1b096026132f02e2b1a3deb5aac3514158a3bd86c7d5c1638a549c516046 |
| R2 | `python3 .ufo/waves/round-49/draft/c2-after.py <clone>` | 0 | `DEV_AFTER=77580bf4503066fa093564641026e761bb4b34bb` — `after.out` sha256 0799a69df3a84a14b91f50010351d0da282b2485c5c872016049dd44ebaccb33 |
| R3 | `python3 -I -B <clone>/tools/round-49/c2-mismatch.py --root <clone> --rev 77580bf4 --freeze 541044b6 --json-out af.json` | 0 | `mismatches 0`, `atoms_total 9`, A1–A9 `ok true`; stdout sha256 64805124445e1807c021973927e7929a0adaabd918f1dc613e1d306088f97fc8 |
| R4 | same as R3 with `--battery` | 0 | stdout sha256 33d895c2ebcf5e2b7aa54fe36312e78a8d93d5b8a3d3ad944544a864ba32b915 |
| R5 | same as R3 with `--rev 541044b6` (FREEZE) | 1 | `mismatches 9`; A8 `round 48: 0 matching search-log entries, want 1` and `round 49: 0 matching …`; stdout sha256 8b469c5b68abc0c7947cd674a703f32cb34800ebfa7b381cc17082938e217d6c |
| R6 | `python3 -I -B a8_probe.py` (in-memory `Overlay` of REV SOURCES.md; calls the counter's `score`) | 0 | per-case A8 result in `a8_probe.out`; sha256 21dd8b080bb4afd616999ea150017c33acac3329856b981a523a41e56506fbdb |
| R7 | `python3 -I -B dup_probe.py` (duplicate S148 row overlay) | 0 | A8 `[]`, all atoms green, census line count 149; sha256 3fbafad2264b86226d4ab969aed6cc15c9d3429dc70656a1e390b707db213127 |
| R8 | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at 61b87d74 / 8847042a / e4f2cfa5 / 77580bf4 | 0 | 144 / 146 / 146 / 148 |
| R9 | `git show 8847042a:corpus/SOURCES.md` status column (awk) | 0 | S145 mined, S146 rejected (13 fields each); at 77580bf4: S147 mined, S148 mined |
| R10 | `sha256sum .../round-49/draft/tools/round-49/c2-mismatch.py` vs clone copy | 0 | both 90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f |
| R11 | `curl -sS -L --max-time 60 -o <f> -w '%{http_code} %{size_download}' <url>` ×3 (live re-open, 2026-10-28 21:11Z) | 0 | popper: HTTP 200, 118135 B, sha256 2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207 (= S145/S147 pin; = draft snapshot); sysexits.h.3head: HTTP 200, 12725 B, sha256 d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340 (= S148 pin; = draft snapshot); sysexits.h.3: HTTP 404, 196 B, sha256 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880 (= S146 pin) |
| R12 | python normalised-text probe of the live Popper page (`<[^>]+>`→space, html.unescape, whitespace collapse) | 0 | quote 1 and quote 2 present; `Backdrop to Popper’s Thought` heading at offset 8875, quote at 12284, `The Problem of Demarcation` section heading at 12989 → S147 locator (§2 Backdrop) correct; S145 locator (§2 The Problem of Demarcation) wrong. 3head page contains `EX_USAGE 64` and the S148 quote. |

Live copies are saved beside this file: `live_https___plato_stanford_edu_entries_popper__.html`, `live_https___man7_org_linux_man_pages_man3_sysexits_h_3head_html_.html`, `live_https___man7_org_linux_man_pages_man3_sysexits_h_3_html_.html`.
Counter JSON receipts: `af.json`, `afb.json`, `fz.json` (and `*.stdout` copies); probe outputs: `a8_probe.out`, `dup_probe.out`; dev fixture outputs: `mk.out`, `after.out`.
Not run: any search for new candidates (none is in scope for A8); the full C1 controls (not in scope); `c1-run.sh` (forbidden).
