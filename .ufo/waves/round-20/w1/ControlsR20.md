# Controls R20

## Findings

- **Observation — implementation:** Added `.ufo/waves/round-20/controls-r20.py` in the detached baseline clone. It reads immutable Git objects and checks the command-A coverage/depth proxies, exact prefix and QUALITY constraints, prior history, and SOURCES append-only/cell rules (`.ufo/waves/round-20/controls-r20.py:15-86,89-149,152-266,277-349`). The routed-fix exception list is explicit at `:19-27`; changed existing SOURCES cells are returned individually as `old`/`new` plus a printable `old -> new` string (`:226-242,258-265`).
- **Observation — measured baseline:** BASE and SOURCE both equal `14f0260ad319ecc26994381b2415d5a999003375` (detached clone HEAD confirmed). Result passes: command A is 97/97 mapped with no missing/dangling entries, and depth is 17/17 (both scores 10.0); QUALITY rows 1–22 are present, ordered, and byte-identical; LOG/SCORECARD lengths are 151,282/182,993 bytes; prior lessons and round-17/18/19 runs/predictions are unchanged; no paths were deleted; SOURCES has 39 rows and no cell changes. The actual command output is pasted below.
- **Observation — selftest:** Final selftest last line: `SELFTEST: CLEAN cases=12`; exit code 0. One initial selftest invocation exited 1 because its adversarial-cell fixture replaced the matching header cell before the row cell. The fixture was narrowed to S001, and the required rerun passed all 12 cases. Both invocations are disclosed below.
- **Observation — patch:** Patch contains only `.ufo/waves/round-20/controls-r20.py`; `git diff --cached --stat`: `1 file changed, 474 insertions(+)`. Patch: `.ufo/waves/round-20/w1/patches/ControlsR20-2.patch`.
- **Inference / limit:** The coverage and citation-depth fields preserve the finite command-A proxy; they do not establish semantic coverage or citation support. The requested baseline-as-source run validates the frozen baseline, not the later integrated revision.
- **Blocker:** LSP definition/reference/refactor support was unavailable in the provided tool inventory; no cold LSP response was treated as evidence of symbol absence. No install/update was needed.

## Commands and exits

1. `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-ControlsR20-2 && git -C /tmp/kr20-ControlsR20-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-ControlsR20-2 rev-parse 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; output `14f0260ad319ecc26994381b2415d5a999003375`.
2. `git -C /tmp/kr20-ControlsR20-2 rev-parse HEAD` — exit 0; output `14f0260ad319ecc26994381b2415d5a999003375`.
3. `python3 -I -B .ufo/waves/round-20/controls-r20.py --selftest` — initial run exit 1; exact last line `SELFTEST: FAILED cases=12 fails=1` (fixture defect described above).
4. A read-only inline `runpy` diagnostic of `source_table`/`compare_sources` on synthetic S001/S002 bytes returned normally and showed the test replacement hit the header; it was not a shell process and had no separate process exit code.
5. `python3 -I -B .ufo/waves/round-20/controls-r20.py --selftest` — final run exit 0; exact last line `SELFTEST: CLEAN cases=12`.
6. `python3 -I -B .ufo/waves/round-20/controls-r20.py 14f0260ad319ecc26994381b2415d5a999003375 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; stdout and explicit `EXIT_CODE=0`:

```json
{
  "base": "14f0260ad319ecc26994381b2415d5a999003375",
  "checks": {
    "base-map-resolves": true,
    "coverage-not-harmed": true,
    "depth-not-harmed": true,
    "no-deleted-path": true,
    "prefix:LOG.md": true,
    "prefix:SCORECARD.md": true,
    "prior-lessons-unchanged": true,
    "prior-round-17-18-19-runs-predictions-unchanged": true,
    "quality-rows-1-22-byte-identical": true,
    "quality-rows-1-22-order-preserved": true,
    "quality-rows-1-22-present-once": true,
    "source-map-resolves": true,
    "sources-existing_cells_limited_to_status_recheck_used_by": true,
    "sources-header_unchanged": true,
    "sources-rows_append_only": true
  },
  "details": {
    "LOG.md": {
      "base_bytes": 151282,
      "source_bytes": 151282
    },
    "SCORECARD.md": {
      "base_bytes": 182993,
      "source_bytes": 182993
    },
    "command_a": {
      "base": {
        "citation_resolved_rules": 17,
        "coverage_score": 10.0,
        "dangling": [],
        "depth_score": 10.0,
        "knowledge_files": 97,
        "mapped": 97,
        "missing": [],
        "rule_blocks": 17
      },
      "source": {
        "citation_resolved_rules": 17,
        "coverage_score": 10.0,
        "dangling": [],
        "depth_score": 10.0,
        "knowledge_files": 97,
        "mapped": 97,
        "missing": [],
        "rule_blocks": 17
      }
    },
    "deleted_paths": [],
    "prior_lessons_changed": {
      "added": [],
      "changed": [],
      "deleted": []
    },
    "prior_runs_predictions_changes": {
      "added": [],
      "changed": [],
      "deleted": []
    },
    "quality": {
      "after_rows": 22,
      "before_rows": 22,
      "changed_rows": [],
      "first_22_byte_identical": true,
      "first_22_ordered": true,
      "required_rows_present_once": true
    },
    "routed_fix_tool_allowlist": [
      ".ufo/gates/c1-census-v10.py",
      ".ufo/gates/citation-drift/citation-drift-probe.py",
      ".ufo/gates/custody-pair/custody-pair.py",
      ".ufo/waves/round-17/tools/receipt-validate.py",
      ".ufo/waves/round-18/tools/head-rev-lint.py",
      ".ufo/waves/round-18/tools/jj-red-before.py",
      ".ufo/waves/round-19/tools/wave-outcomes.py"
    ],
    "routed_fix_tool_changes": [],
    "sources": {
      "after_rows": 39,
      "appended_rows": [],
      "before_rows": 39,
      "changed_cells": [],
      "disallowed_changes": [],
      "missing_ids": []
    }
  },
  "failed": [],
  "pass": true,
  "source": "14f0260ad319ecc26994381b2415d5a999003375"
}
EXIT_CODE=0
```

7. `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-ControlsR20-2 add -A && git -C /tmp/kr20-ControlsR20-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/ControlsR20-2.patch && git -C /tmp/kr20-ControlsR20-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; stat: `.ufo/waves/round-20/controls-r20.py | 474 ++++++++++++++++++++++++++++++++++++`, `1 file changed, 474 insertions(+)`.
