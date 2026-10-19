# proposed-contract-denominator — patch text for the v2 custody tool

Authored by SEAT EX-28 (chain c2, executor, wave arc3-loop1-round3). **Patch text only**:
`.ufo/gates/custody-pair/` is EX-21's write target this round. Verified against revision
`03bd6242470ac8d27ea832af6bcb71049ccfad92f2ba8c878b30f51b5211bd83` (51,868 B, 1,109 lines,
mtime 2026-10-19 10:11:16 -03); line numbers shift with every revision — match on text.
Measurements: `v1-compat.md` §5 (A4, A4b, A9, A5/A6) and `ev2/atk-strip-sha.txt`,
`ev2/atk-omit-sha-after.txt`, `ev2/atk-dup-lastgood.txt`, `ev2/atk-binary.txt`, `ev2/atk-tilde.txt`.

## 1. The contract denominator (measured hole, highest value)

At `custody-pair.py:579-582` the contract line counts only rows where **both** sides carry `sha256`:

```python
sha_pairs = [r for r in rows if r["sha_agree"] is not None]
sha_agree = sum(1 for r in sha_pairs if r["sha_agree"])
print("SHA256-CONTRACT: %d/%d paths agree on sha256 (v1/v2 receipts compare on this field)"
      % (sha_agree, len(sha_pairs)))
```

Measured consequences (revision `03bd6242`):

* `ev2/atk-strip-sha.txt` — R1 with the kimi stanza's `SHA256:` line removed → `SHA256-CONTRACT: 4/4`.
  The kimi content drift is masked; only the incidental `mode 600→644` difference surfaced it
  (`moved=mode`). A same-mode rewrite on a stripped stanza is invisible.
* `ev2/atk-omit-sha-after.txt` — a one-stanza v1 reference with no `SHA256:` at all, then the fixture's
  content swapped for equal-size/equal-mode bytes: `MATCH-V1-PARTIAL … SHA256-CONTRACT: 0/0`, **exit 0**.

Proposal (keeps every existing line, adds one):

```
# in verify_sets, before the print
sha_ref  = sum(1 for s in ref_sections if "sha256" in s)
missing  = [s["path"] for s in ref_sections if "sha256" not in s]
print("SHA256-CONTRACT: %d/%d paths agree on sha256 (%d/%d reference stanzas carry sha256)%s"
      % (sha_agree, len(sha_pairs), sha_ref, len(ref_sections),
         "" if not missing else "; OMITTED-SHA256: " + " ".join(missing)))
# and, when missing: one finding per omitted reference stanza, class METADATA-DRIFT
#   OMITTED-SHA256: <path>  (v1 reference stanza carries no sha256; content unverified)
```

Companion gate for scripts, mirroring `--require-paths`: `verify --require-sha N` exits 2 with
`SHA256-CONTRACT: …` when fewer than N reference stanzas carry sha256. `--require-paths 5 --require-sha 5`
is the strict form for the round's own pre/post pair.

## 2. Ambiguous duplicate paths (measured A9)

`verify_sets:542-543` builds `ref_by = {s["path"]: s for s in ref_sections}` — last row wins.
`ev2/atk-dup-lastgood.txt`: a sums reference holding a *tampered* row followed by the correct row for the
same path reads `MATCH-V1-PARTIAL 1/1 exit 0`; with the tampered row last it reads exit 10
(`ev2/atk-dup.txt`). Verdict: ambiguous input is resolved silently instead of flagged.

Proposal: build the dicts from a fold that records collisions —
`DUPLICATE-PATH: <path> (n rows in reference; sha256 disagree)` as a note on the row, worst-case merge
(class = worst of the duplicates), or exit 2 USAGE under a new `--strict`. Do not silently keep the last.

## 3. Path-string forms read as custody events (measured A5/A6)

`parse_receipt:437` accepts any text after the digest as the path, so GNU `sha256sum -b` output
(`<hex> */home/...` → key `*/home/...`, `ev2/atk-binary.txt`) and `./`/`~` spellings
(`ev2/atk-dotpath.txt`, `ev2/atk-tilde.txt`) key differently from the live side and read
`ABSENT` exit 13 — fail-closed, but indistinguishable from a path that disappeared. Proposal: strip an
optional `*`/`./`, `expanduser()` the parsed path at parse time, and add a `PATH-FORM: <raw>` note when
the raw spelling differs from the normalized key. (Round-1 receipts use absolute spellings, so this is
robustness, not a back-compat break.)

## 4. Not proposed

`EXISTS: no` both-sides MATCH stays as is: a synthetic receipt that claims absence on both sides has
nothing to compare, and the real round-2 D2 defect (EACCES recorded as `exists=no`) is closed by the
`UNEVALUABLE` exit-14 path added this round (`custody-pair.py:37-45,103-105`, selftest cases 16-17).