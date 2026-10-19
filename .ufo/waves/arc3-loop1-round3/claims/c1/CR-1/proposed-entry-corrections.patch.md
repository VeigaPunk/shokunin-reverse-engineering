# CR-1 proposed corrections to the r3 C1 entry draft (patch text — NOT applied)

Seat CR-1 · chain c1 · critic · 2026-10-19. Target: `claims/c1/records-drafts/
knowledge-entry-draft.md` rev 2 (`2026-10-19-arc3-r3-evm-optimizer-shapes`).
Corpus is not written by this seat; this is text for the parent/scribe.
Everything below is measured; commands and outputs in this seat's
`claims/c1/CR-1/recon/` (`r1-claim-refutations.txt`, `meta-count.txt`,
`legcmp.txt`, `audit-c1.txt`).

Independent verification first (so the patch is not a rewrite by taste): my
byte-level census of every runtime leg in this entry — VaultB 13/13 (opt and
nopt), carrierB@EX-04 11/11, CarrierB 8/8, CarrierBErr 8/8, Rv2TokenOpt 5/5,
carrier-A 3/3 — reproduces the entry's sets, `missing=[]`, `extra=[]`, and all
non-planted constants the entry names (`4e487b71`, `1309a563`, `1dc930eb`,
`30cd7471`, `3c3332b9`, `43000825`). The three edits below are the only
divergences I found.

## Edit 1 — id-domain comparator (line 45, verbatim fragment)

OLD (verbatim, end of the observation):

```
compare by `subject.digest.sha256` + payload when citing other seats' ids.
```

NEW:

```
compare by the decoded `normalized_result.bytecode.sha256` + function payload
when citing other seats' ids. Measured this round: `subject.digest.sha256` is
the *input file's* digest, so it changes with costume while the decoded bytes
do not (hex leg `optB-hex-6.4.0.json`: subject `a07bef2e…` = sha256 of the
hex-text file incl. its trailing newline, decoded `ed6c8a76…`; raw leg:
subject = decoded). Comparing ids across hex/raw legs via `subject.digest`
would report a spurious identity change.
```

## Edit 2 — where the CBOR-trailer constant lives (line 41, verbatim fragment)

OLD (verbatim fragment):

```
Rv2TokenOpt's `PUSH4` set is 5 selectors out of 7 immediates (the other two are `4e487b71` and the CBOR trailer constant `43000825`)
```

NEW:

```
Rv2TokenOpt's `PUSH4` set is 5 selectors out of 7 whole-file immediates (the
other two are `4e487b71` and `43000825`, the latter read by a whole-file sweep
out of the terminal CBOR trailer — `solc`+version bytes `736f6c63 43000825`;
the code region ends at byte 925 and holds 6 immediates: the 5 selectors +
panic)
```

## Edit 3 — replace "no erratum is needed" with an append-only correction paragraph

OLD (verbatim, lines 68-70):

```
- For the r1 entry: no erratum is needed — its recheck line is still true
  (re-derived this round); its narrowed Unknowns are stated in THIS entry
  (append-only convention; do not rewrite the r1 bytes).
```

NEW:

```
- For the r1 entry: its recheck line is still true (re-derived this round).
  Two of its other statements are corrected here by append, not by rewriting
  the r1 bytes (add the following sentence to the entry's observation list):
  "Two r1 statements are corrected by this round's byte-level census:
  (a) r1's creation-leg observation reads 'creation blobs carry no runtime
  dispatch table' — measured false: `Rv2Token.creation.hex` (1,971 B) embeds
  the runtime and its five `EQ;PUSH2;JUMPI` sites, and this round's creation
  legs embed 7/9/10/11/13 EQ sites; the probe's 0-function result on creation
  blobs is tool scope (parsed-and-empty), not byte-level absence.
  (b) r1's 'sole non-dispatch PUSH4 constant (`16ee4b79` @1900)' is a
  metadata artifact: `Rv2Token.runtime.hex` ends its code region at byte 1890
  and the code region contains zero non-dispatch PUSH4 immediates; the cited
  constant sits at byte 1901 inside the CBOR trailer (r1's extractor swept the
  whole file — same class as `43000825` above)." The narrowed Unknowns are
  stated in THIS entry.
```

## Landing recipe

Apply edits 1-2 in place on the draft (line-neutral within those lines); apply
Edit 3 as a replacement of the bullet; then re-derive the draft's identity per
rule #14 (its revision log line "final"). No other line of the draft conflicts
with my measurements, including its CBOR-trailer note (cborLength 51,
`bytecodeOffset 1568` — equals my computed codeEnd for VaultB.opt200) and its
dispatch-shape observation (GT/EQ splits: VaultB 2 pivots, carrierB@EX-04 1
pivot / 12 legs, CarrierB 1 pivot — independently re-derived).

## Residual (no patch proposed)

- The draft is silent on creation-leg probes; silence is accurate. If the
  parent wants one line: the round's creation legs (EX-10, EX-04, EX-12,
  carrier-A) return 0 functions while embedding their runtime dispatch tables —
  consistent with Edit 3's corrected framing.
- EX-12's pre-registered empty-file control expects an `invalid_request`
  refusal; the measured result is parsed-and-empty success (n=0, decoded
  `e3b0c442…`). Not an entry-text issue — a control-expectation delta for
  EX-12/the parent to adjudicate.