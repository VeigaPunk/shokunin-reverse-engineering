# derived receipts — NOT runs

`derived/*.after.json` are one-line projections of a real receipt, made to put
one clause of the scoring rule under a matcher they cannot both satisfy.  Each
file names its base receipt and the single mutation.  They are evidence about
the MATCHER, never about REA.

## C-shadow.after.json   (base: receipts/C-xz.after.json)
Removed exactly one element from `normalized_result.files`: the entry whose
`relative_path` is `firmware.bin_extract/etc/conf`.  Everything else, including
`files` order, shas and the depth-limited gap, is byte-for-byte the run.

  before: 3 files = etc/conf, etc/version, opt/x/etc/conf   (etc/conf and
          opt/x/etc/conf carry the same sha256, by construction of tree C)
  after : 2 files = etc/version, opt/x/etc/conf

This is the "identical bytes at a deeper path" shape: an oracle row `etc/conf`
is still satisfied by `firmware.bin_extract/opt/x/etc/conf` under a suffix rule
(false PASS) and is not satisfied under either exact rule.  A real REA run
publishes both files, so on live data the two rules agree — the defect is
latent, which is why it needs a projection to be visible.

## A-materialised.after.json   (base: receipts/A-xz.after.json)
Appended one element to `normalized_result.files`:
`{"relative_path": "firmware.bin_extract/bin/busy", "size": 40000,
  "sha256": sha256("derived materialised symlink")}` — i.e. a regular file
published at the exact path of the `bin/busy` symlink entry, with the
`unpublished-entry` gap left in place.  This is the shape a still-lax matcher
must reject; all three rules do, which shows the exact rules do not weaken
`nonregular_unpublished_ok`.

## A-nogap.after.json   (base: receipts/A-xz.after.json)
Removed the `unpublished-entry` gap (the `depth-limited` gap stays).  All three
rules report `required gap absent on ['bin/busy']`; the check is still
load-bearing under the exact rules.

## ../inner-oracle.tsv, ../empty-nonreg.tsv
The inner filesystem's single row (`inner/only.txt`, 19 bytes) used as a probe
oracle for the depth-2 receipt, and an empty non-regular table so only the
oracle check varies.  The inner row is NOT the carrier's filesystem: the probe
measures whether a matcher credits a nested publication to a top-level row.
