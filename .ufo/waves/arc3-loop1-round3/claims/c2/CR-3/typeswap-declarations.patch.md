# CR-3 — proposed declaration patch (patch text, NOT applied)

Seat CR-3 · chain c2 (critic) · wave `arc3-loop1-round3`. The real targets
(`.ufo/gates/custody-pair/{custody-pair.py,README.md}`) are EX-21's write target; this
seat wrote nothing there. Apply decision and authorship belong to EX-21 / the parent.

Anchors (re-aim if the revision moved; rule #14):

- tool `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09` (1155 lines)
- README `039993ed83345a3416ec59dd611f520409178b653137ffe21a137b3675ea4435` (146 lines)

Every item below is backed by a measured row in `typeswap-matrix.md` (transcripts
`matrix-BEFORE.out` / `matrix-AFTER2.out`).

## 1. README: the exit map must carry exit 14 (the EACCES class) — RESOLVED at `f30df42e`

State at measurement time (`039993ed`, 146 lines, 13:14:01Z): exit 14 is returned by
C1/C2/C3/C4b/C6b/C14b/C15b/D4b in `matrix-AFTER2.out`; `README:87-95` had no 14 row and
`README:101` omitted it from the precedence line, while `tool:103-105,115` declared it.
At `f30df42e` (185 lines, 13:15Z) the README carries the 14 row (`README:122`), the
expanded USAGE row (`README:123`) and the precedence term (`README:130-131`). The diff
below is kept only as the record of the transient; **do not apply it** against
`f30df42e`.

```diff
--- a/.ufo/gates/custody-pair/README.md
+++ b/.ufo/gates/custody-pair/README.md
@@ -90,13 +90,17 @@
 | 10 | `CONTENT-DRIFT` | `SHA256` differs on ≥1 path |
 | 11 | `REWRITE-DRIFT` | digest equal but `inode`/`ctime`/`mtime` moved on ≥1 path (same-content rewrite) |
 | 12 | `METADATA-DRIFT` | digest + identification times equal but `mode`/`uid`/`gid`/`size`/`type` differ, or an `EXTRA-PATH` appears on the candidate side, or a receipt's own epoch/render pair is inconsistent (`LABEL-INCONSISTENT`), or a v1 label defect is reproduced (`LABEL-DEFECT`) |
 | 13 | `ABSENT` | ≥1 reference path is missing on the candidate side |
-| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, or a refused/failed write |
+| 14 | `UNEVALUABLE` | a path exists but could not be evaluated (EACCES on open, or a stat error other than ENOENT); the receipt is still written, carrying `STAT-ERROR`/`READ-ERROR` |
+| 2 | `USAGE` | bad arguments, unreadable/unparsable receipt, a refused/failed write, an `--require-paths` coverage shortfall, or an unusable `selftest --scratch` dir |
 | 3 | `SELFTEST-FAIL` | a selftest case failed |
 
-`capture` exits `0` with every requested path present (5/5 for the default set)
-and `13` when at least one requested path is absent — the receipt is written
-either way, recording `EXISTS: no`.
+`capture` exits `0` with every requested path present (5/5 for the default set),
+`14` when at least one path is present-but-unevaluable, else `13` when at least one
+requested path is absent — the receipt is written either way, recording
+`EXISTS: no` (or the `STAT-ERROR`/`READ-ERROR` line for the unevaluable class).
 
-Severity precedence for the verdict of a `verify` run: `CONTENT-DRIFT` >
-`ABSENT` > `REWRITE-DRIFT` > `METADATA-DRIFT` > `MATCH`. The report always prints
+Severity precedence for the verdict of a `verify` run: `CONTENT-DRIFT` >
+`UNEVALUABLE` > `ABSENT` > `REWRITE-DRIFT` > `METADATA-DRIFT` > `MATCH`. The report always prints
```

## 2. README/docstring: declare `TYPE: other` and the symlink scope

Measured: B1/B2/B4b/B6b — a directory or fifo stanza (no `SHA256`) verifies as
`MATCH-V1-PARTIAL` with a vacuous `SHA256-CONTRACT: 0/0`; a change inside a captured
directory's subdir is invisible; C16b/A4b/A5b — a symlink stanza pins the target string,
never the referent.

```diff
--- a/.ufo/gates/custody-pair/README.md
+++ b/.ufo/gates/custody-pair/README.md
@@ -52,6 +52,15 @@
 ## Receipt fields (v2)
 
+Scope of the content pin (measured in round-3 CR-3's type-swap matrix):
+
+- Only regular files and symlinks carry `SHA256` (files: file bytes; symlinks: the
+  target string). A stanza with `TYPE: other` — an interpreter's directory, fifo,
+  socket, device — carries **no content pin**; its changes are visible only through
+  the stat identity fields (`INODE`/`CTIME`/`MTIME`/`SIZE`/`MODE`). Such a stanza
+  verifies as `MATCH-V1-PARTIAL` with `SHA256-CONTRACT: 0/0`, which is the vacuous
+  (not a satisfied) contract state.
+- A captured directory pins **one stat, not a tree**: changes below its first level
+  are outside the receipt's reach.
+- A symlink is pinned as the link object (`lstat` + the target string); the referent
+  is never opened, so the referent's later creation, deletion, or content change is
+  invisible to `verify` by design.
```

## 3. Tool: `--out` parent that is not a directory → USAGE (the surviving traceback)

Measured (BEFORE and AFTER): `capture --out pfile.txt/rec.txt` → `FileExistsError`
traceback, exit 1 (`matrix-AFTER2.out:603-620`). `out.parent.mkdir(...)` at `tool:653`
sits outside the `try` that owns the declared "refused or failed write" class.

```diff
--- a/.ufo/gates/custody-pair/custody-pair.py
+++ b/.ufo/gates/custody-pair/custody-pair.py
@@ -650,7 +650,11 @@
             print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                   " (path or inode): %s" % out, file=sys.stderr)
             return EXIT_USAGE
-        out.parent.mkdir(parents=True, exist_ok=True)
+        try:
+            out.parent.mkdir(parents=True, exist_ok=True)
+        except OSError as exc:  # e.g. a path component is a regular file
+            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
+                  file=sys.stderr)
+            return EXIT_USAGE
         try:
             out.write_text(text, encoding="utf-8")
```

## 4. Selftest cases for the shapes this seat measured (names first)

Add three cases (the count sentence `README:126,138` and `tool` assertions must then be
re-derived — the r8 coupled-landing precedent):

- `dangling-symlink-capture-and-retarget` — A1/A2/A3: dangling capture exits 0 with
  `TYPE: symlink` + target-string sha; retarget → `CONTENT-DRIFT`; referent creation →
  `MATCH` (the declared scope of §2).
- `directory-stanza-has-no-content-pin` — B1/B2/B4b: `TYPE: other` receipt verifies
  `MATCH-V1-PARTIAL`; a deep change under it stays `MATCH-V1-PARTIAL exit 0` (the
  declared blind spot, asserted so it cannot silently change).
- `out-parent-not-a-directory-usage-exit` — C8 after §3: exit 2, `USAGE` on stderr, no
  traceback, no partial receipt left behind.

## 5. Wording-only (W2/W3/W4, no behavioral change)

- W2 (`README:92`): the METADATA-DRIFT clause should say what was measured for a
  directory change with mtime restored — `size` **plus ctime** move and the reading is
  METADATA-DRIFT, not REWRITE-DRIFT (B3).
- W3: type swaps (file↔dir↔symlink) ordinarily land in `REWRITE-DRIFT` (the inode moves
  with the type), so the `type differ` clause of METADATA-DRIFT is shadowed; one sentence
  stating the observed assignment (B5/D5b/D6b) prevents a reader from expecting a
  `METADATA-DRIFT` on type swaps.
- W4: the `REFERENCE-COVERAGE` line prints its `unaccounted:` list from the canonical
  5-path set even when the gate passes (`1/1` case, `matrix-AFTER2.out:718-730`); one
  clarifying sentence — or omitting the list when the gate passes — removes the ambiguity.