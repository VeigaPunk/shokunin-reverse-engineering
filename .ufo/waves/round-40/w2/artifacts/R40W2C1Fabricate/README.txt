R40W2C1Fabricate artifacts (round-40 wave 2, seat R40W2C1Fabricate)
No vendor firmware bytes and no extracted vendor files are stored here (AVM licence).
Vendor carriers are cited only by sha256:
  V1 ac4098bd11a76f8ad001faac0f1a5e018708d9b03943dfebb2b18a24e0038e95 (5442392 bytes)
  V2 5ccc7614263e4b4b392025e1561e071a744b6464a4c88548633e87f71f3d089b (26013550 bytes)
Files:
  fab.py                 fabricator: builds an after-receipt from oracle.tsv + nonregular.tsv + carriers.json
                         pin/length + ONE committed receipt of another carrier. Runs no REA, reads no carrier bytes.
  fab/*.env.json         the fabricated envelopes that were scored (bare REA `data` objects).
  cmp.py / projection-equality.out
                         frozen counter's own projection()/projection_diff() (plus-extractor) comparing each
                         fabricated envelope with the real committed receipt projection at 42c10a58.
  matrix.py / matrix.out mutation matrix over the fabricated L1 receipt (which projection key / clause refuses it).
  clauserun.py / clauserun.out
                         drives the real frozen counter over sandbox commits, one mutant per run.
  score-fab-L1.json      frozen counter on a sandbox whose ONLY change is the fabricated L1 receipt.
  score-fab-all.json     frozen counter with V1, V2 and L1 receipts all fabricated (L2 real, untouched):
                         carriers_matched 3, exit 1 -- the same score as the genuine lane at 42c10a58.
  score-coverage_complete.json / score-truthful_mime_types.json / score-tables_only_no_gaps.json
                         single-mutant runs refused by projection_ok / gaps_ok.
  score-raw_result_fiction.json / score-metadata-fiction.json
                         single-mutant runs that are ACCEPTED (unchecked receipt fields).
  score-unminted_evidence_id.json
                         evidence_id_ok is self-consistency only (an id not minted for the bytes fails).
  fetch-vendor.log       fetch-vendor.py receipt (pins, member sha256) -- no bytes.
Sandbox clones lived under /fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate (removed after the run);
freeze 7fce3086, measured revision 42c10a58, fabricated receipt commits 0dcaa6b1 / 2a62ac6d.
