# PL-2 — C3: G21 append-past-register residual

## Outcome

**REPRODUCED.** A new, locus-free bullet after the last registered Frontier line is silently accepted by the current gate. A proposed G21 section/bullet-start check was exercised only on a scratch copy: it preserves the pristine PASS and fails the seeded overrun as `FRONTIER-UNEVALUABLE`. This artifact contains patch text only; the gate and custody tool were not edited.

## Re-derived evidence

- **Seat/claim mapping — VERIFIED:** `claims-frozen.md:51-65` makes C3 an instrument/custody move with scratch measurement; `:67-72` maps PL-1..4 to c3.
- **Revision identity — VERIFIED:** `git rev-parse HEAD` returned `5694506a862c32d2f7aac44935778bce4b6184f2`; `git log -1 --format='%h %s'` returned `5694506 arc3-loop1-round9: records — SCORECARD round section, LOG entry, round report + scope re-key to EOF (measured at work commit eb5a2c4)`. `git show --format=fuller --no-patch eb5a2c4` identified work commit `eb5a2c4af9d910bb7a3d4fced780f4641e341a24`.
- **Gate identity — VERIFIED:** current `.ufo/gates/c1-census-v10.py` SHA-256 is `a9bb20e4c3ac9986db0fe9ea4000412e8d145a379e88dd0c0a2020a8afa2189b`; the same path at work commit `eb5a2c4` hashes to `0f8be0e1ba525de12273466e122de0c8c5cdc24671aa3f61bb07368093875f78`. The current source contains G21's fixed register at `:279-308`, checks only those entries at `:422-444`, derives `max_end` from SCOPE/FRONTIER at `:614-629`, calls `frontier_check` at `:632-633`, and turns its errors into `FRONTIER-STALE` or `FRONTIER-UNEVALUABLE` at `:667-680`. The existing text output and exit status are at `:701-712`.
- **Boundary — VERIFIED:** the current `PROVINCE.md` is 162 lines (also the file ends at `PROVINCE.md:162`). The register's final span is `PROVINCE.md:161-162` (`c1-census-v10.py:307`). Runtime reports 14 fixed G21 rows; no registered check enumerates additional bullet starts in the named sections.
- **Command A — VERIFIED, not needed for this C3 measurement:** its source-derived recipe is `SCORECARD.md:88-124`. No coverage/depth score claim is made here.

## Scratch seeded-fault measurement

Scratch root: `/var/tmp/kaidoku-pl2-c3-dx0ux_wf`. The harness copied only the gate and its three scoped inputs (`PROVINCE.md`, `SKILL.md`, `SCORECARD.md`) into separate `pristine/` and `seeded/` trees. It appended this locus-free synthetic row to the scratch `seeded/PROVINCE.md`, making it line 163:

```text
- **PL-2 seeded unregistered Frontier** — synthetic scratch-only claim with no earned anchor.
```

The runs invoked the copied gate with `--root <tree> --quiet`; the live-pin lookup was read-only. Captured output (unchanged gate):

```text
--- current_pristine: exit=0 ---
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)

--- current_seeded: exit=0 ---
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

The same proposed insertion was applied only to a second scratch copy of the Python gate. It did not alter or run against the repository gate. Captured output:

```text
--- patched_pristine: exit=0 ---
PROVINCE.md    lines=162  loci=6
FRONTIER register (G21): 14 rows asserted, errors: []
DECLARED FAIL CLASSES: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)

--- patched_seeded: exit=1 ---
PROVINCE.md    lines=163  loci=6
FRONTIER register (G21): 14 rows asserted, errors: ['PROVINCE.md:163 unregistered Frontier bullet (G21 frontier register)']
DECLARED FAIL CLASSES: ['FRONTIER-UNEVALUABLE']
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

**Gap verdict — REPRODUCED:** current gate exits 0 / PASS on the seeded line 163. **Candidate closure verdict — VERIFIED on scratch only:** it stays PASS on the unmodified 162-line tree and exits 1 on the same seeded overrun. This is not a claim that HEAD is fixed.

## Proposed gate patch text (not applied)

Insert in `frontier_check()` after the existing `for (f, s, e, req, forb) in FRONTIER` loop and before its `return errs` (`.ufo/gates/c1-census-v10.py:422-444`):

```python
    registered_starts = {
        start for name, start, _, _, _ in FRONTIER if name == "PROVINCE.md"
    }
    section_level = None
    province_lines = filelines.get("PROVINCE.md")
    if province_lines is not None:
        for line_no, line in enumerate(province_lines, 1):
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
            if heading:
                level = len(heading.group(1))
                title = heading.group(2).strip().lower()
                if title == "frontier" or title.startswith("round-4 frontier"):
                    section_level = level
                elif section_level is not None and level <= section_level:
                    section_level = None
                continue
            if (section_level is not None and BULLET.match(line)
                    and line_no not in registered_starts):
                errs.append("%s:%d unregistered Frontier bullet (G21 frontier register)"
                            % ("PROVINCE.md", line_no))
```

This reuses G21's existing `frontier_errors`/`FRONTIER-UNEVALUABLE` reporting path; it does not expand SCOPE or change the meanings of existing rows. Any future Frontier-section edit still needs its register re-key and a rerun of the real gate in the landing commit. The patch has not been landed or verified on the repository instrument.

## Scope note

Only this seat artifact was written. The gate, custody-pair tool, corpus, SKILL, SCORECARD, PROVINCE, and LOG were not changed. Scratch artifacts remain under `/var/tmp/kaidoku-pl2-c3-dx0ux_wf`.
