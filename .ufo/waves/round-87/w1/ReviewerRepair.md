# ReviewerRepair — R87-C1 scoped findings

Verdict: **sound-with-limits**. Full review: `.ufo/waves/round-87/w1/ReviewerRepair/review.md`.

- Provenance clause: PASS. The repair imports only argparse, json, struct and sys, opens only --in and --out, and never runs the packer.
- Counter `--no-rea` on the committed repair (`ReviewerRepair/counter-norea.json`): repair_rc0, windows_only, test_ok and identity hold 8/8. N1 4/4, N2 0/4 recovered, N3 4/4. rea_recover is false only because REA was disabled, so the receipt reads exit 1, as designed.
- REA on jq's restored bytes (`ReviewerRepair/rea-jq-restored.json`): procedure_count 167 = declared.
- F1 MEDIUM: rea_recover is implied by identity (the REA input equals the pinned original), so it is a pin-consistency check, not separate repair evidence.
- F2 MEDIUM: the repair refuses mixed-method chains (libz `--lzma`: method 0x02 first block, then 0x0e), including the intact file. It fails safe. Scope the Core row to the measured `--best` population. See `ReviewerRepair/probe-out-of-population.txt` (24/27).
- F3 LOW: N2 holds through upx's adler check, not the repair (the repair returns rc 0 on corrupt input; the do-nothing control also passes N2).
- F4 LOW: the jq/xxd stub `cmp edx,'UPX!'` word stays tampered, so the repaired file is not byte-identical to the original packed file. It still runs and `upx -d` still restores the pin.
- F5–F7 LOW: uncaught exceptions exit 1 with no receipt; N1 counts rc None as a refusal; windows_only does not limit how many windows change.
- No tools installed.
