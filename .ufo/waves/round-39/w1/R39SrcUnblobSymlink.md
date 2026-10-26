# R39SrcUnblobSymlink — DONE

Verdict: DONE. unblob 26.6.4 symlink-sanitisation source opened and byte-compared; SOURCES row drafted (11 columns, 12 pipe characters, none inside cells).

## Receipts (artifacts/R39SrcUnblobSymlink/)
- Implementing file: `python/unblob/extractor.py` (found via grep MaliciousSymlinkRemoved under the uv tool install; also `report.py` for the class).
- URL: https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — access 2026-10-26T16:39:23Z (access-utc.txt), HTTP 200, 4129 B, sha256 `1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a`. Installed copy (`.../site-packages/unblob/extractor.py`) sha256 identical; `cmp` = same. Saved: up-extractor.py, headers hdr-extractor.py.txt.
- URL: .../26.6.4/python/unblob/report.py — HTTP 200, 10553 B, sha256 `2329783fc645de8aae94b82443277bceb6ceac968549ff65917c7b2d454cc9ee`, identical to installed. Saved up-report.py.
- Tag 26.6.4 -> commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` (GitHub API git/ref/tags/26.6.4, type commit) — matches S110/S112.

## Lines (extractor.py, `fix_symlink` 50-92)
- 58-65: `is_recursive_link` (path.resolve() RuntimeError) -> log, `MaliciousSymlinkRemoved(link, target)`, `path.unlink()`.
- 67-71: empty raw target -> `path.unlink()` only, NO report.
- 73-77: absolute target: leading "/" stripped (re-rooted under outdir); relative target: `path.resolve()`.
- 79: `safe = is_safe_path(outdir, target)`; `is_safe_path` (file_utils.py:34-39) = `basedir.joinpath(path).resolve().relative_to(basedir.resolve())`, False on ValueError.
- 81-87: **escaping -> remove + report**: `if not safe:` -> log "Path traversal attempt through symlink, removing", `MaliciousSymlinkRemoved(link=path.as_posix(), target=target.as_posix())`, `task_result.add_report`, `path.unlink()`.
- 88-91: safe -> link rewritten to a relative link (`os.path.relpath(outdir.joinpath(target), start=path.parent)`).
- Docstring 51-56 quote (18 words, verbatim incl. typo): "either removed it it attempts to traverse outside of the extraction directory or rewritten to be fully portable".
- report.py 133-138: `class MaliciousSymlinkRemoved(ErrorReport)`, `severity: Severity = Severity.WARNING`, fields `link: str`, `target: str` (registered in the report union at line 350).
- Callers of `fix_extracted_directory` (callers.txt): processing.py lines 447 (MultiFile), 654, 678 (chunk extraction paths); it also does `fix_permission` (files |= 0o644, dirs |= 0o775, skips symlinks).

## Caveats for the claim text
- Docstring is looser than the code: relative links are also checked (target = `path.resolve()`), absolute links are re-rooted into outdir not removed, so an absolute link such as `/etc/passwd` inside the tree is kept as a relative link into the extraction dir. Only links that resolve outside outdir, loops, and empty targets are deleted; empty targets are deleted silently (no report).
- Report severity is WARNING, not ERROR — a triage rule keyed on "error" diagnostics would miss it.
- This is a source-reading row only; it says nothing about sasquatch output or any carrier. [INFERENCE] The sanitiser runs on unblob's own extraction dir, so any REA/unblob path will apply it; I did not run REA or any carrier this wave.

## SOURCES row (artifacts/R39SrcUnblobSymlink/sources-row.md; id S118 assumes S117 is the highest committed id — L1 renumber if siblings also draft S118)
| S118 | unblob extractor symlink sanitiser at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py | code | A | unblob 26.6.4's post-extraction symlink rule (fix_symlink, fix_extracted_directory) and the MaliciousSymlinkRemoved report class (report.py lines 133-138) only; not sasquatch behaviour, not any carrier's outcome, not other versions | tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089; HTTP 200, 4129 B, sha256 1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a, byte-identical to the installed unblob 26.6.4 copy; `fix_symlink` lines 50-92: line 79 `safe = is_safe_path(outdir, target)`, lines 81-87 `if not safe:` builds `MaliciousSymlinkRemoved(link=..., target=...)`, `task_result.add_report`, `path.unlink()`; docstring lines 53-55 "either removed it it attempts to traverse outside of the extraction directory or rewritten to be fully portable"; a symlink loop (lines 58-65) is also removed with the same report; an empty target (lines 68-71) is removed with no report; safe targets are rewritten relative (lines 89-91); report.py `MaliciousSymlinkRemoved` severity WARNING fields link and target | State the symlink rule before data: an escaping or looping symlink is deleted and reported as MaliciousSymlinkRemoved, an in-tree one is kept as a relative link, so an absent link in the output tree plus that report is the rule firing, not extraction loss | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md |

No tools installed/updated; no scratch used.
