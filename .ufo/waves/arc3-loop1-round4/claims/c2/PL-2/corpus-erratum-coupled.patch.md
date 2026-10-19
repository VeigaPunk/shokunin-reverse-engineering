# PL-2 r4 — coupled corpus erratum for the Ghidra feature count (patch text)

Target: `corpus/knowledge/2026-10-13-ghidra-install.md` (seats never write corpus;
this is text for the parent). Append at EOF, append-only convention.

Why it is coupled: `PROVINCE.md:46`'s repair (`35 features` -> `34 features`)
would otherwise leave the lane asserting 34 while the corpus entry the row's
sibling facts come from still says 35 in its claim line — and that entry's own
enumerated list holds 34 names (re-derived 2026-10-19: list vs live directory,
zero differences in both directions). Land both or neither.

Literal text to append:

```markdown
## Erratum (arc3-loop1-round4, append-only)

- The Candidate line above reads "35 feature modules"; its own enumerated list
  holds 34 names, and the live directory matches that list exactly (34 dirs,
  0 non-dir entries; `ls -1 Ghidra/Features | wc -l` = 34, re-derived
  2026-10-19). The count is 34; the list was right. PROVINCE.md:46 carried the
  same miscount and was repaired to 34 in the same commit.
```
