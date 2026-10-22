# Wave 2 review: tools/round-27/xpin-attribute.mjs vs claims.json R27-C2 tool_contract

Seat: KaidokuR27.ReviewXpinTool. Reviewed at lane tip 4084d8975b684a8837b1c858eea0008ce9ab49e0 (branch main);
tool working tree clean (`git status --porcelain tools/round-27/` empty, 15:35:57Z), last commit touching it
97358f759a531f7ebc0354fb937d546da8d3b8bd 2026-10-22T12:15:28-03:00. Node v24.21.0. No installs made.

## Verdict: HOLDS

The tool satisfies every clause of the frozen tool_contract. No blocking defect found; two low-severity
observations and one inference noted below.

## Checks (all runs 2026-10-22 UTC; scratch /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReviewXpinTool, S)

C1. Own digest import per pin — HOLDS (observation). loadPin (lines 156-191) imports
    `<root>/dist/domain/canonicalDigest.js` separately for pkg65 and pkg67 and checks the export is a
    function; idUnderPin hashes with `pin.digestCanonicalValue`. No cross-pin sharing, no local digest code.
C2. Own projection text, not retyped — HOLDS (observation + falsification run). For each pin the tool reads
    that pin's evidence.js text, extracts `const semanticProjection = ...;` with a string/comment/bracket-aware
    scanner and evaluates it with `new Function` (lines 84-152). Decisive run E, 15:40:49Z, exit 0:
    after deleting the `limitations` line from a scratch copy of the 6.5.0 pin (S/pkg65-mod), the tool printed
    `...analyze-base.json  ev_14f9d92f...  ev_bd1d65e27bc4...  ev_a4c519507a09...  none` — id65 changed and
    attribution flipped 6.5.0 to none. A retyped projection would be immune to that edit. The package's own
    computeEvidenceId (evidence.js:176, 6.5.0) is exactly `ev_ + digestCanonicalValue(semanticProjection(e), "Evidence")`,
    the same formula the tool applies.
C3. Missing text — HOLDS (observation; three variants, all exit 2, empty stdout, named pin in message):
    - evidence.js absent: `6.5.0: cannot read package files under S/fake-noevidence: Cannot find module ...evidence.js` (15:41:45Z, exit 2).
    - definition absent from text: `6.5.0: no "const semanticProjection" definition in evidence.js` (15:41:45Z, exit 2, fake pin G1).
    - definition renamed to semanticProjectionX in a real copy: `6.5.0: cannot evaluate semanticProjection: semanticProjection is not defined` (15:40:50Z, exit 2).
C4. Exit codes — HOLDS (observation). Happy path exit 0 (15:39:24Z, 15:39:25Z). All error paths observed exit 2:
    unreadable JSON, non-object envelope, missing .data, missing args, bad pin, mid-batch failure. Contract fixes
    only success=0; 2-on-error is consistent and stderr-carried.
C5. Output columns — HOLDS (observation). Default mode, exit 0, 15:39:24Z, exactly 5 TAB fields per line
    (awk fieldcount=5 x3), matching `<path as given> TAB <stored> TAB <id65> TAB <id67> TAB <attribution>`;
    attribution values seen: 6.5.0, none, both. Stored id read from `.data.evidence_id`.
C6. Three round-26 envelopes — HOLDS (observation). Exit 0, 15:39:24Z, attribution `6.5.0` with id65 equal to
    the stored id for analyze-base (ev_14f9d92f...), xrefs-copy (ev_d591ef8c...), inspect-binary-layout-repeat
    (ev_294a449c...). Consistent with the reported 24/24 r26 agreement (full recount is seat RecountC2's item).
C7. --parse mode — HOLDS (observation). Exit 0, 15:39:25Z, 3 fields: `parseEvidence-6.5.0 accept` and
    `parseEvidence-6.7.0 reject:Evidence semantic identifier does not match its record` on all three envelopes;
    each pin's own parseEvidence is used (loadPin checks the export; parseUnderPin reports the first zod issue).
    The 6.7.0 reject is expected: a 6.5.0-ruled stored id cannot match the 6.7.0 recompute.
C8. Records without relationship_coverage — HOLDS (observation). Scratch nocov.json = analyze-base with the key
    deleted (value was null in the original). Run 15:40:32Z, exit 0: stored == id65 == id67, attribution `both`.
    Mechanism verified in both pins' sources: 6.5.0 spread keeps the key undefined when absent, 6.7.0 assigns
    undefined, and both canonicalDigest.js files skip undefined-valued object keys (line 64). No crash, no
    inserted or defaulted field — the record is passed to each projection exactly as stored.
C9. Malformed file — HOLDS (observation, 15:39:24-25Z, each exit 2, stdout empty):
    `{not json` -> `cannot read envelope: Expected property name or '}' in JSON at position 1`;
    `[1,2,3]` -> `envelope is not a JSON object`; `{"schema":"x"}` and `{"data":"str"}` -> `envelope has no ".data" evidence record`;
    no envelopes -> `no envelope paths given`.

## Findings by severity

- Blockers: none.
- Low 1 (behavior, not a contract breach): all-or-nothing output. `main` buffers every line and writes once at
  the end; on a mid-batch InputError the whole batch prints nothing (mixed run good+bad, 15:39:25Z, exit 2,
  stdout_bytes=0). A 100-envelope batch with one bad tail file yields zero usable rows. Contract only specifies
  per-envelope lines with exit 0, so this is an operability note, not a fail.
- Low 2 (guard depth): the extraction guard `statement.includes(marker)` is substring-based, so
  `const semanticProjectionX` passes it (run C3 variant three routed to the evaluation guard instead). Net
  behavior is still safe (exit 2, precise message), so no impact on the claim.
- Inference (not run): a record whose `.data.evidence_id` is missing yields stored = "" and attribution `none`
  by code reading of attribute(); no crash path seen. Unverified by execution.

## Residual risk and verification gaps

- I ran 3 of 24 r26 envelopes plus one derived record; full 24-envelope agreement is attested by the checker run
  and seat RecountC2, not re-executed here.
- The 6.7.0 ids come from the 6.7.0 package's code applied to 6.5.0-produced records (rule fit); per the claim's
  own limits, no 6.7.0 runtime behavior was exercised, by me or by the tool.
- Extraction correctness rests on the current dist text (no regex literals or external identifiers inside the
  statement; verified by reading both packages' evidence.js). A future dist shape with regex literals containing
  unbalanced brackets could confuse the scanner; guarded only by the evaluation guard failing closed (exit 2).

## Artifacts (under S; sha256)

- default.out 44e49a49d845aea94c1ad56f0ddfe97b422c92370324a541e0893893ff5dea8f (C5, C6)
- parse.out 07ffd51c9171afd320d48f20863e28140ba5b72a7dbc5bbe194774b063ae041f (C7)
- nocov.json 7ee619fd69fa51942585649f4670ef115eefe812af63413170e050eeb70b5496; nocov.out 4e7e776aa31db8e0e8d783603df0007041e178d70460c239930c911cdfeed125 (C8)
- mod.out 4ae7884a393e095370f1f384731810e7dc668d3c8670c429af5ba187728e9a67 (C2 falsification)
- noproj.out e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty); noproj.err 2a9e6a9092bcd4c761b683d0248677e9c80a147305f3aa1823d5aab7830483d5 (C3)
- nofiles.err fbf367d781cdb701f45c86df7e19161ec63cf046f3281c05dedcb82145546beb; g1.err d7a3416a517d46e6e608f8d941ec8ba82488e877d091a673a06ce8ef285280b2; g2.err 2132f468f6e95b0a972304d82cb3126bb6cdb1764d24990bc6a73fda15542bdd (C3)
- mixed.err c4d20eb3ee0827dae73e608e63bb7a48e8ba9ff9a5a9e12de5d68eeb539689fb (Low 1); noargs.err c56148b29a34310a9628904b60e246222dc6c0dc0b4b33e11e69138efea1e5f7 (C4)
- bad-truncated.json 92072df399cb74703f8e86f450d552bc0bb01eeeb98a90985a1b7772c8fd0016; bad-array.json a615eeaee21de5179de080de8c3052c8da901138406ba71c38c032845f7d54f4; bad-nodata.json baaadc98adc0eb80921693b0ffd31ed284571d6e24da4eceb14b6f465b0ffc74; bad-datastring.json a8750c2c53aba661f764b845e8e93109aa8199ec3c322dc759e02aa5b6ffcc38 (C9)
- Mutated pin copies: pkg65-mod/dist/domain/evidence.js 32ea6cce689af33b898fd84318783129626f66f815160efd5f11d8433b0941e2; pkg65-noproj/dist/domain/evidence.js 1880c157805eb0e65a39b8ebfad96462386e1e38c02788ea3282d624c98f4101; fake-nomarker/dist/domain/evidence.js 1edbfcc9806143b8209615b639188358dd64a33fd555879bf9834fb88bf324d0

Bounds: read-only on the lane except this report; scratch pins copied from the npx cache with a node_modules
symlink for zod resolution; no lane refs touched, no jj/git writes, no installs (node v24.21.0 preexisting).
