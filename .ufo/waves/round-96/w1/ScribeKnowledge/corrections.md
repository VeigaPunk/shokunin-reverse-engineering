# Draft — the R95-VD-2 correction entry for `corpus/lessons/round-96.md`

Seat ScribeKnowledge, round 96 attempt 1, lane kaidoku. This is the seat draft of the
append-only correction entry; the L1 appends it to `corpus/lessons/round-96.md` (a file
that does not exist at the declaration commit `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`;
the L1 creates it and lands the S321 row in the same commit).

**Scope note.** This draft carries **one** correction: R95-VD-2, the numeric claim in
the round-95 lesson prose that stated no counting command. The round's other two
routed corrections are carried elsewhere and are *not* drafted here: R95-VD-1
(landing-revision receipts) is discharged by the round's own after-side receipts naming
the landing revision, and R95-VD-3 (the four round-95 instruments carry no registry
rows) is the registry-row work in R96-C2, which belongs to the craft-block seat.

---

## Corrections (append-only)

- **R95-VD-2 · the round-95 lesson's count of the `O_NOFOLLOW` occurrences on the
  `open(2)` page is wrong: the tag-stripped page states the flag six times, not five.**
  Superseded text (two places, both quoted verbatim; neither is edited — the round-95
  bytes are historical and stay as they were):
  1. `corpus/lessons/round-95.md:19`, in `## Gate`, "Admit / reject": "Not admitted
     from the same page: the `O_PATH` interaction and the other `O_NOFOLLOW`
     occurrences (the page states the flag five times; only the description carries the
     rule)."
  2. `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md:41`, in section (a):
     "The `O_NOFOLLOW` flag appears five times on the page: in the file-creation-flag
     list, in the flag description quoted above, twice in the `O_PATH` discussion (where
     `O_PATH` overrides the `O_NOFOLLOW` behaviour), and once in the `ERRORS` list. Only
     the second occurrence carries the quoted rule."

  **Correction.** The count is **six**, not five. The round-95 enumeration was
  arithmetically right about the five it listed — the file-creation-flag list, the flag
  description, the two `O_PATH` occurrences, and the `ERRORS` entry — but it **missed
  one occurrence**: the `HISTORY` section's own entry for the flag
  (`O_NOFOLLOW` / `POSIX.1-2008`), which is the sixth statement of the flag on the
  page.

  **Counting command (the command the round-95 prose omitted):**

  ```
  $ python3 -c "import re,html;s=open('.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html','rb').read().decode('utf-8','replace');print(html.unescape(re.sub(r'<[^>]+>','',s)))" > /tmp/s320-stripped.txt
  $ grep -o 'O_NOFOLLOW' /tmp/s320-stripped.txt | wc -l
  6
  ```

  The count is **6 both before and after tag-stripping** — `grep -o 'O_NOFOLLOW'`
  over the committed fetch `.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html`
  (76 506 B, sha256
  `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`) also returns
  **6**, because every occurrence of the flag on this page is written as the bare
  token `O_NOFOLLOW` and none of them is split across a tag boundary. The tag-stripping
  step therefore does not change the number, which is why the two counts agree.

  **The six occurrences, in page order, each located:**

  | # | page location | the sentence carrying it |
  |---|---|---|
  | 1 | the file-creation-flag list, "The file creation flags are `O_CLOEXEC`, `O_CREAT`, `O_DIRECTORY`, `O_EXCL`, `O_NOCTTY`, `O_NOFOLLOW`, `O_TMPFILE`, and `O_TRUNC`." | the flag named in the list of creation flags |
  | 2 | the `O_NOFOLLOW` description | the quoted rule: "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP" — **this is the only occurrence that carries the rule** |
  | 3 | the `O_PATH` discussion | "When O_PATH is specified in flags, flag bits other than `O_CLOEXEC`, `O_DIRECTORY`, and `O_NOFOLLOW` are ignored." |
  | 4 | the `O_PATH` discussion | "If path is a symbolic link and the O_NOFOLLOW flag is also specified, then the call returns a file descriptor referring to the symbolic link." |
  | 5 | the `ERRORS` list | "ELOOP path was a symbolic link, and flags specified O_NOFOLLOW but not O_PATH." |
  | 6 | the `HISTORY` section | "O_NOFOLLOW" / "POSIX.1-2008" — the flag's own history entry, the occurrence the round-95 enumeration missed |

  **What the correction does not change.** The round-95 conclusion is unaffected:
  only occurrence 2 carries the trailing-component rule, so only that occurrence is
  admitted as the row's anchor and the other five remain unadmitted grounds. The row
  S320 (`corpus/SOURCES.md`, `open(2), Linux man-pages 6.19`) is **not** edited, and no
  registry row is added, removed or re-scoped by this correction — a corrected count
  is not a new source. The lesson's *admit/reject decision* is unchanged: the same five
  non-description occurrences (now six in total on the page) are still not admitted as
  rows, and the row-change log for this round still records **S321 appended, no
  existing row edited**.

  **Class:** a numeric claim without its command (the round-95 lesson's own prose
  defect, routed as R95-VD-2 in `plans/round-96-claims.md`). **Captured by:** the
  round-95 verifier spot-check, which read the page's `HISTORY` section against the
  lesson's enumeration; not by any lane counter — no instrument in the lane counts
  occurrences of a token in a fetched page, which is why the count needed a command
  rather than a re-read. **Fix:** this entry, appended to the round-96 lesson with the
  counting command above, so the number is re-derivable by the reader.

---

*Draft provenance: seat ScribeKnowledge, round 96 attempt 1. The counting command was
run by this seat against the committed round-95 fetch
`.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html` (both the raw and the
tag-stripped form return 6). No round-95 file is edited by this seat or by the
correction; the entry is append-only in `corpus/lessons/round-96.md`.*

---

## A second observation this seat found while drafting (reported, not a correction)

The round-96 mutant table `.ufo/waves/round-96/mutants.json` declares a `kills_via`
string per mutant. The after receipt
`.ufo/waves/round-96/l1/scores/c1-at-decl-worktree.json` records which check actually
failed for each mutant. The two agree for nine of the ten mutants and **disagree for
M6**:

```
M6  declared kills_via: "K-dmain shortrev (r95 survivor; named kill: revision case)"
M6  measured:            killed by K-selftest   (K-dmain did not fail)
```

M6 removes the `revision-not-bound` branch from the v6 counter's `verify_receipt`. The
v6 counter's own selftest carries a `verify-catches-wrong-revision` case, so the
mutant trips **K-selftest** before the negative control reaches the deleted branch;
K-dmain's `shortrev` scenario still exits non-zero for other reasons and therefore
still reads `ok: true`. **M6 is killed either way**, so the frozen label, the frozen
kill rule and the mutant table are unaffected; only the *attribution* of the kill
differs from the declared string.

This is reported here rather than corrected, because the mutant table is frozen (the
declaration: "Predicates, counters, kill rules, manifests, pins, fixtures and targets
are frozen: you never re-declare, rename, re-target, or edit a counter, label,
manifest, fixture or pin"), and because a corrected kill-attribution string is not a
change in what the rule kills. The knowledge entry
`corpus/knowledge/2026-11-05-r96-kill-rule-coverage.md` reports the **measured**
attribution and names the divergence, so the corpus carries the measured fact and the
frozen table stays untouched. If the L1 prefers to carry this as a lesson mistake row
instead, the row's shape is *class · evidence pointer · captured-by · fix* and the
evidence pointer is the pair of committed files named above.

