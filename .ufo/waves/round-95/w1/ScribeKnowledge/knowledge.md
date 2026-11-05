source: S320 — open(2), Linux man-pages 6.19 — https://man7.org/linux/man-pages/man2/open.2.html, anchor 'the O_NOFOLLOW description, man-pages 6.19'. The registry row is S320 in corpus/SOURCES.md; the draft row is `.ufo/waves/round-95/w1/ScribeKnowledge/s320-row.md`.
verified-at: 2026-11-05, commit 4bda1d1dd3788973f10e61212b70df18b3b14ea0. The frozen round-95 counter is tools/round-95/stop-boundary-repair-battery-v5.py, sha256 6fc81208c9b151f35c9768bc1f481a1bdd0bcc0854d9732879e38e6b87194b7f; the strengthened instrument is tools/round-95/c1-agreement-v2.py, sha256 ca7d213a598fb79fd944886d480863d6464cb2217c8d2d4b9f11c7981c539291.
recheck: on-release. Re-fetch the page with `curl -fsSL https://man7.org/linux/man-pages/man2/open.2.html` and re-hash it; the located quote must still read as quoted, and the page's footer must still name Linux man-pages 6.19.

## (a) What the `open(2)` documentation states about `O_NOFOLLOW`

The `O_NOFOLLOW` entry of the `open(2)` page states the rule verbatim. The located
quote, exact after tag-stripping and whitespace normalisation of the fetched HTML,
is:

> "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP"

The same entry continues, in the next sentence of the page:

> "Symbolic links in earlier components of the pathname will still be followed."

The rule therefore has two halves, both of which the page states: the refusal applies
to the **trailing component only**, and the failure is the errno `ELOOP`, not `ENOENT`
and not a silent success. The `ELOOP` entry of the same page's `ERRORS` section repeats
the errno for the `O_NOFOLLOW` case: "ELOOP path was a symbolic link, and flags specified
O_NOFOLLOW but not O_PATH."

Evidence for the page itself: two byte-identical fetches are committed at
`.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html` and
`.ufo/waves/round-95/l1/scores/s320-open2-fetch2.html`, each 76506 bytes, each
sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`. The page
footer reads `Linux man-pages 6.19            2026-02-08`, and the provenance block
reads "This page was obtained from the tarball man-pages-6.19.tar.gz", which is the
"man-pages 6.19" the anchor names.

Where the quote lives: the quote is **not** a raw contiguous byte substring of the
HTML. In the raw file the sentence is broken across lines and carries markup —

```
       <b>O_NOFOLLOW</b>
              If the trailing component (i.e., basename) of <i>path</i> is a
              symbolic link, then the open fails, with the error <b>ELOOP</b>.
```

— so it is exact only after tag-stripping (`<i>`/`<b>` removed), HTML entity decoding
and whitespace normalisation. The `O_NOFOLLOW` flag appears five times on the page:
in the file-creation-flag list, in the flag description quoted above, twice in the
`O_PATH` discussion (where `O_PATH` overrides the `O_NOFOLLOW` behaviour), and once in
the `ERRORS` list. Only the second occurrence carries the quoted rule.

## (b) Why a predictable `<json-out>.tmp` is an escape path, and why `mkstemp` removes it

A receipt writer that writes to a **predictable** path — the output path plus a fixed
suffix — gives a local attacker who can write in that directory the ability to
pre-place a symlink at that exact name. The writer then opens the name it was told to
open: the kernel resolves the trailing symlink, the write lands on the link's target,
and the file the writer believes it produced is somewhere else entirely. The
`O_NOFOLLOW` rule above is the shape of the defence: a trailing symlink must make the
open fail rather than be followed, and only the trailing component is protected, so
the protection has to be applied to the **specific file** the writer is about to
create, not to the directory above it.

`tempfile.mkstemp` removes the predictability rather than defending against the
attack. It creates the temporary file fresh, with `O_CREAT | O_EXCL` semantics and a
random name, in the **same directory** as the intended output, and returns an open
descriptor to the file it actually created.

Measured on this host (Python 3.14.8, `inspect.getsource(tempfile)`): the module's
open flags are `_os.O_RDWR | _os.O_CREAT | _os.O_EXCL`, and — because the platform
provides it — `| _os.O_NOFOLLOW` is added when the attribute exists
(`os.O_NOFOLLOW` = 131072 here). So on Linux `mkstemp` applies the page's own rule
directly: the trailing component it opens cannot be a symlink, because `O_NOFOLLOW`
makes that open fail rather than follow it. The generated name is the prefix plus a
random component plus the suffix (observed: `x.gobplze2.tmp` for prefix `x.`), so it
does not coincide with the predictable `<json-out>.tmp` a local attacker would
pre-plant.

Four properties follow, and all four are load-bearing here:

1. the name is not guessable, so a symlink cannot be pre-planted at it;
2. `O_EXCL` means that even a name collision fails the create instead of opening an
   existing object, so a planted file is never adopted;
3. the file is in the receipt's own directory, so the later `os.replace(tmp, path)` is
   a same-directory rename and therefore atomic within that filesystem;
4. (measured above) the create itself carries `O_NOFOLLOW` on this platform, so the
   trailing-component rule of the man page is applied by the standard library as
   well as the unpredictability.

The round-94 writer `tools/round-94/stop-boundary-repair-battery-v4.py` used the
predictable name `<json-out>.tmp` plus a rename. That is exactly the shape the page
describes: the rename protected the *final* path from truncation, but the *temporary*
path was still a symlink a local attacker could pre-plant, and the writer followed it.
The measured evidence is committed at
`.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`: `victim_intact false`,
`tmp_is_symlink false` (the planted symlink had been replaced by the writer's own
file), `verdict "followed-symlink"`, `receipt_valid true` — the receipt was valid and
the victim was overwritten.

The round-95 writer `tools/round-95/stop-boundary-repair-battery-v5.py` changes only
that: `write_receipt` calls `tempfile.mkstemp(dir=d, prefix=os.path.basename(path) +
".", suffix=".tmp")`, writes, `flush()`es, `fsync()`s, and only then `os.replace`s onto
the target path. The measurable consequence is recorded at
`.ufo/waves/round-95/l1/scores/c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`:
`verdict "hardened"`, `victim_intact true`, `receipt_valid true`, `tmp_is_symlink true`,
`tmp_left true` — the planted symlink is still there, untouched and unread, because the
writer never opened that name.

## (c) The four bindings of the round-95 agreement instrument and their typed reasons

The round-94 instrument `tools/round-94/c1-receipt-agreement.py` binds only
receipt ↔ stdout ↔ rc agreement and the predicted met/exit per run name. It reports
three booleans per run (`valid`, `agree`, `predicted`) and no typed reasons at all —
the rc is folded into the `agree` boolean (`out["agree"] = (… and int(rc_text) ==
s_exit)`, `tools/round-94/c1-receipt-agreement.py:70-75`). The round-94 critic showed
that a receipt pair whose `label` is rewritten consistently in both files, and a
wholly fabricated triple, both pass it (M94-e). The round-95 strengthened instrument
`tools/round-95/c1-agreement-v2.py` keeps every round-94 atom and adds four world
bindings, each with its own typed reason:

| binding | typed reason | the rule it enforces |
|---|---|---|
| label bound to the frozen expect | `label-not-frozen` | when `met_target` is true the receipt's `label` must equal the frozen `--expect` string |
| label recomputed from its own counts | `label-not-recomputed` | the label's six segments must recompute from the receipt's own `counts` (with `--intact-total`, default 6) |
| revision bound to the measured tree | `revision-not-bound` | the receipt's `revision` must equal the full 40-hex resolution of `--rev` (via `git rev-parse --verify`) |
| pins bound to that tree's bytes | `pins-not-bound` | `verdict_sha256` must equal sha256 of `git show REV:tools/round-93/stop-boundary-repair-battery-v3.py` and `counter_sha256` must equal sha256 of `git show REV:<receipt.tool>` |

The instrument's own module docstring carries the same four reasons and their rules
(`tools/round-95/c1-agreement-v2.py:9-18`), and each binding is implemented as a
separate typed branch in `row()` (`tools/round-95/c1-agreement-v2.py:129-166`), so a
fixture that violates exactly one binding is refused with exactly that one reason.

An observation about the inherited atoms, measured by this seat (it is a naming
observation, not a change to any frozen byte): the v2 docstring lists the inherited
reasons as `not-valid`, `stdout-disagree`, `rc-disagree`, `predicted-mismatch`, but
`rc-disagree` is never emitted by the code. A probe run of v2 against a fixture whose
`.rc` file disagrees with the receipt's `exit` (receipt `exit 1`, `.rc` `7`, stdout
otherwise consistent) returned the reason list `["stdout-disagree", "pins-not-bound"]` —
the rc mismatch is reported under `stdout-disagree`, because the receipt/stdout/rc
triple is compared as one conjunction. The three reasons the code can actually emit
for the inherited atoms are `not-valid`, `stdout-disagree` and `predicted-mismatch`
(`tools/round-95/c1-agreement-v2.py:104`, `:117`, `:129`). This does not change any of
the four world bindings and does not change the measured target: the committed forgery
receipt carries exactly the four intended reasons and the honest leg carries none.

The craft row that states these rules in the corpus is `corpus/QUALITY.md` row 191
(label bindings) and row 192 (revision and temp-file bindings); those rows land with
the round-95 craft block 34 landing. The frozen keyword atoms that the semantic
counter checks are carried in `.ufo/waves/round-95/manifests/block34-after.json`:
row `consistent label rewrite` → QUALITY 191 must contain `bound to the frozen expect label`
and `when met_target is true`; row `counts that do not recompute the label` → QUALITY 191
must contain `recompute the label from its own counts`; row `revision field not the
measured tree` → QUALITY 192 must contain `full measured revision` and `git rev-parse`;
row `temp-file symlink escape` → QUALITY 192 must contain `unique temporary name` and
`planted`.

## (d) The measured before and after

**Before** — the do-nothing controls, committed at the declaration freeze and measured
at base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`:

- `.ufo/waves/round-95/pre/c1-old-counter-admits-at-base.json`: the pinned round-94
  counter over the four committed forged triples prints `counts_of_4` with `valid 4`,
  `agree 4`, `predicted 4`, `met true`, exit 0. The round-94 instrument admitted all
  four forgeries; the before-side of R95-C1 is met.
- `.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json`: the frozen probe against the
  pinned v4 writer reports `victim_intact false`, `receipt_valid true`, `verdict
  "followed-symlink"` — the F1 mechanism reproduced on the public path.

**After** — measured at the declaration commit
`4bda1d1dd3788973f10e61212b70df18b3b14ea0`, in `.ufo/waves/round-95/l1/scores/`:

- `c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json` and
  `c1-forgery-stdout.txt`: `forgeries refused 4 of 4; before admits True; honest
  accepted True`, `met true`. Each forgery carries exactly its intended single typed
  reason: `forge-pos` → `label-not-frozen`, `forge-F1` → `label-not-recomputed`,
  `forge-F2` → `revision-not-bound`, `forge-F3` → `pins-not-bound`. The honest leg
  (`honest-pos`) is accepted with an empty reason list, `exit 0`, `met true`.
- `honest-pos.json` / `honest-pos.stdout` / `honest-pos.stderr` / `honest-pos.rc`: the
  honest public v5 run at the declaration revision exits 0 (`honest-pos.rc` reads
  `0`, `honest-pos.stderr` is empty) and its stdout carries both
  `selfverify ok=True reasons=0` and
  `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`.
- `c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json`: the v5 probe leg
  exits 0 with `victim_intact true`, `receipt_valid true`, `verdict "hardened"`.

The frozen label is the same string as rounds 93 and 94:
`repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`.

## (e) The named limits of the round-95 claims, verbatim

From `plans/round-95-claims.md` (R95-C1, "Named limits (stated before data)"):

> The strengthened bindings bind the receipt to the world it claims; they do not
> authenticate provenance — a wholly re-authored triple whose stdout/rc/pins/revision/label
> all consistently describe the honest world at the honest revision is indistinguishable
> from an honest capture at the byte level, and catching it needs independent stdout/rc
> custody, not another receipt field. The symlink probe covers the `<json-out>.tmp`
> name; it does not model a hostile `--json-out` directory symlink (parent-dir swap is
> out of scope this round). The honest world's `--expect` binding runs only when
> `met_target` is true; refusal labels are legitimately free-form. The fixture set is the
> four committed forgeries, not a claim about unlisted forgery classes.

From `plans/round-95-claims.md` (R95-C2, "Named limit (stated before data)"):

> The keyword atom is a vocabulary check (QUALITY 188 residual): a criterion that
> carries the keywords passes whether or not it states the rule. C2 does not claim more
> than the vocabulary check plus the junk-manifest control.

This entry inherits those limits and adds none of its own: it records what the
`open(2)` page states, what the round-95 instruments measured, and where each number
comes from. It does not claim that a receipt proves its own provenance, that the probe
covers a parent-directory symlink swap, or that the keyword check verifies the truth of
a criterion.
