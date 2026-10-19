# EX-24 proposed patch texts — write-path mkdir class (arc3-loop1-round4, chain c3)

Seat EX-24 · executor · 2026-10-19. Patch text only: this seat writes no scoped
file. Bases and identities re-derived at write time; every diff here was applied
to a pristine copy as a proof: §1 with `patch -p1` (verified to yield exactly
`30451e3a…`), §3 with `patch -p0` (verified to yield exactly `68435482…`, line
count held at 390).

Status summary: the **tool** patch is superseded by EX-21's landed revision
(`29bb45ae…`, which closes the same residual in the CR-3 §3 shape) and the
**README** patch is superseded by the landed README (`125e7e02…`). The **SKILL
row** patch is still applicable and is the one item the round may still want.

## 1. Tool — `out.parent.mkdir` into the guarded region (SUPERSEDED)

Base: `.ufo/gates/custody-pair/custody-pair.py` sha256
`7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 lines).

```diff
--- a/.ufo/gates/custody-pair/custody-pair.py
+++ b/.ufo/gates/custody-pair/custody-pair.py
@@ -650,8 +650,8 @@
             print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                   " (path or inode): %s" % out, file=sys.stderr)
             return EXIT_USAGE
-        out.parent.mkdir(parents=True, exist_ok=True)
         try:
+            out.parent.mkdir(parents=True, exist_ok=True)
             out.write_text(text, encoding="utf-8")
             digest = sha256_file(out)
             sidecar = out.with_name(out.name + ".sha256")
```

Byte-identical to `evidence/after.diff` (`806117ae…`, 12 lines). Result:
`30451e3a…` (1155 lines) — L1/L3/A1/A3c read `USAGE: write failed (…) exit 2`,
zero tracebacks; `--out ''` and the L4 fresh-parent path unchanged.

Rejected alternative (filed with its counter-measurement,
`evidence/flag-only.diff` `5f4e2e43…`, 13 lines): an explicit
`if out.parent != out and not out.parent.is_dir(): … USAGE` pre-check. It reaches
exit 2 on the failure legs but **over-refuses** the legitimate fresh-parent case
(`--out <fresh>/sub/r.txt` → exit 2 instead of 0). Not a candidate.

## 2. Selftest — the two cases (filed as the independent case set)

Case bodies: `harness/mkdir-cases.py.txt` (`3283c8c6…`); applied on top of the
injection by `harness/build-after2.sh` (`bca145f8…`), producing `ac2cd74e…`
(`evidence/fixture.diff` `9289c649…`, 37 lines). Both cases are inserted
immediately before `    passed = sum(1 for _, ok, _ in cases if ok)` and use only
`root`/`fixture` (no custody path):

- `mkdir-guard-nondir-parent-usage-exit` — in-process `cmd_capture` with
  `--out <regular-file>/sub/receipt.txt` → assert `EXIT_USAGE`, the parent file's
  bytes unchanged, and no directory created through the file.
- `mkdir-guard-subprocess-no-traceback` — the same shape in a subprocess →
  assert `EXIT_USAGE` and `"Traceback" not in stderr`.

Evidence: `after2` reads `CLEAN cases=24 passed=24 failed=0`; the same cases with
the fix reverted (`a6273c28…`) read `DIRTY cases=24 passed=22 failed=2 exit=3`
(both FAIL). Grafted onto the landed revision the pair reads `CLEAN 30/30`.
Superseded on the real target by EX-21's `out-parent-not-a-directory-usage-exit`
(landed selftest `CLEAN cases=28`).

## 3. SKILL.md row — declared classes + case count (APPLICABLE)

Base: `SKILL.md` sha256
`5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` (390 lines).
Diff: `evidence/skill-row.diff` (`c369f73d…`, 8 lines); patched document:
`evidence/SKILL.proposed.md` (`68435482…`, 390 lines — **line-neutral**).

Verified: `patch -p0 -i evidence/skill-row.diff` on a pristine copy applies with
no fuzz/reject and yields exactly `68435482…`; line count 390 → 390.

Three same-line substitutions inside the `custody-pair` row:

1. `refused write, unusable selftest scratch base)` →
   `refused write — including a receipt directory that cannot be created, e.g. a non-directory path component — unusable selftest scratch base)`
2. `same command with \`selftest\`; 22 fixture cases —` →
   `same command with \`selftest\`; 24 fixture cases —`
3. `` `--paths X --out X` and a hardlink alias → 2; `` →
   `` `--paths X --out X` and a hardlink alias → 2, a non-directory `--out` parent → 2 (in-process and subprocess); ``

Landing note: if the round prefers to track the landed 28-case revision, clauses
2 and 3 should read 28 with the landed case name
(`out-parent-not-a-directory-usage-exit`) instead of my two case names; clause 1
is revision-independent. The row is one physical line — any edit must keep it a
single line.

## 4. README — SUPERSEDED (do not apply)

`evidence/readme.diff` (`9207e548…`) + `evidence/README.proposed.md`
(`7ac6f9c4…`) were generated against the pre-landing README `f30df42e…`; they add
the residual-(b) bullet, the 22 → 24 case count and the mkdir case names. The
landed README `125e7e02…` already carries residual (b) at `:137`, the 28-case
count at `:225`/`:242`, and the both-absent ruling at `:151`. Filed for the
record only.

## 5. Identity table (re-derived at write time)

| object | sha256 |
|---|---|
| base tool (before) | `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` |
| landed tool (after, EX-21) | `29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf` |
| landed README | `125e7e0225133738b9b780d6edbb37ded54b4a19de3263cf1c29911d97188186` |
| SKILL.md base | `5eec51c089e57f5d5806b4728261fb8c959637580a73aed7be4cddc1866b8f3f` |
| my injection | `30451e3a2ca9b93ad29f70f6f3202227fd17ca6f8d202afbce469811dac72a6d` |
| my injection + cases | `ac2cd74efe02c61c4e57cfd3dbbc48184f44db8d067d9c8431fab826c2bdcdcc` |
| my cases, fix reverted | `a6273c285c8c008345ead2dc9b0972e39037ae608060f000706b085b989fb59d` |
| landed fix reverted (mut-b) | `b252f5f45ee8c9df3d7b2999463ad75545d572a7470e2150fcd45789e91e2664` |
| `is_dir()` alternative | `dadda060d2a6e98be7ba8b9d1b450a55f25afa06d7b79e116d906f96d677fb22` |
| CR-3 §3 sketch (independently built) | `f7dda34bb8ff11cc28d8acd95bb3288179d33119ed12af52cd226212383ac9da` |
