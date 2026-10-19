# SUPERSEDED measurement — instrument r9-v1 (`82fb807e…`), fixture layout v1

This directory was captured before the fixture redesign (manifest_version 2) and
against the first landed r9 revision (`82fb807e…`, global floor `current-ok > 0`).

Both are superseded:

* the roots at that time carried current-ok loci only in SCORECARD.md, which the
  later per-file floor (r9-v2+) would treat as a floor violation — hence
  `current-ok-ctl` etc. were re-keyed to one loud locus per file;
* the r9 floor and its output line changed shape twice after this capture
  (per-file block-count `c95a5cf3…`, per-file detection-count `df9ffdf9…`/`a4c16763…`).

Kept only as the historical datum that the *first* landed floor read
`current-ok loci=0, total loci=1` on the folded-block tree and FAILed it (F-1 in
the fixture README). Current measurements: `measurements/before-6f1d19ff/` and
`measurements/after-a4c16763/`.
