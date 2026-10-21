# ProvinceAppend: round-23 PROVINCE append source review (author-side)

Seat: KaidokuR23.ProvinceAppend. Leaf source review; no subagents, no REA producer replay, no target/device/remote/process access, no counter run, no peer report edited.
Candidate: 2838351450ff1ee4baa620c962a1153450d53311 (`round-23: retain measured four-of-six coverage and refusal controls`). Baseline B: aa1450b82f9ede35aada63efe8a34e01c6e02f72. Candidate bytes read only via `git show` / `git diff` / `git grep` / `git ls-tree` at that revision. Line numbers refer to candidate blobs unless marked B.

Scope: PROVINCE.md append that date-supersedes the R22 sigrok sentence, without changing the disposition partition; offline envelope expansion must not claim hardware or debugger ownership.

Verdict: NOT ACCEPTED as written. The append is purely additive (no prior line rewritten), and its factual payload matches S058 and S061. But as the disposition statement for the six T1 verbs it fails four checks: (F1) inspect-dart-aot is held in four round-23 artifacts and unheld in one; (F2) the two sigrok verbs are never named in PROVINCE; (F3) the supersession covers only one clause of the R22 sigrok sentence; (F4) the supersession cannot be ordered by date. F5 (an Adjacent placement that is not recorded) is a further medium-low gap. The counter numerator is not affected by PROVINCE prose (P2); these findings concern admission readability and partition integrity.

## Findings

Labels: observed = read or grep at candidate; [INFERENCE] = not observed directly.

### F1. HIGH. inspect-dart-aot disposition contradicts across round-23 artifacts (observed)
- PROVINCE.md:211-212 (R22, unchanged): "`inspect-dart-aot` refused Saber's missing dynamic snapshot symbols and is not held." The supersession at :222-223 names only the sigrok clause, so this sentence is not superseded.
- PROVINCE.md:232-233 (append): "(S061) holds static inspect-dart-aot on the exact archived Saber1330203 APK ...". It does not carry S061's carrier-conditional qualifier.
- corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md:5 heading "Dart AOT parsing is carrier-layout conditional"; :57-59 "That is enough for a conditional held-verb observation".
- corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:117 (blob 6c14cce6): "Dart parsing and both debugger verbs remain unheld; prior R22 identify remains one verb". This reads as a verb-level unheld disposition.
- SCORECARD.md:2827-2828: "cumulative sourced held1/6→4/6 ... Exact held set is inherited identify, inspect-dart-aot, inspect-signal-decoders and decode-signal-recording." LOG.md:2650 "cumulative1/6→4/6". corpus/README.md:72 "held narrowly".
- Effect: the same verb is held in SCORECARD, LOG, README and the PROVINCE append, and unheld in S058:117. PROVINCE, which defines held (:30-32), states neither the verb-level nor the carrier-level disposition.
- Repair (PROVINCE, in scope): state explicitly that inspect-dart-aot is held only as a carrier-conditional success on Saber1330203, that the Saber1360103 invocation stays not held (R22 :211-212 for that carrier), and that the verb is counted once.
- Repair (cross-file, owner = S058 author, out of item): reconcile S058:117 with S061:57-59 and SCORECARD:2827-2828.

### F2. MEDIUM. The two sigrok verbs are never named in PROVINCE (observed)
- `git grep` for verb names over candidate PROVINCE.md returns only identify-flutter-build (:207), inspect-dart-aot (:211, :233) and debug-with-gdb / debug-with-rizin (:214). inspect-signal-decoders and decode-signal-recording do not appear anywhere in PROVINCE.md.
- The append's "holds REA6.5.0 decoder discovery ... and file-only UART decode" (:224-226) and "Offline recording envelopes fit artifact evidence" (:229) therefore assign a held or in-domain status to unnamed operations.
- The R22 paragraph (:207-218) names verbs in backticks; the append does not follow that precedent.
- Repair: name both verbs in backticks, each with its own disposition.

### F3. MEDIUM. The supersession covers one clause of the R22 sigrok sentence (observed)
- PROVINCE.md:217-218: "The sigrok verbs remain unexercised; no recording decode or hardware contact is claimed." This has two clauses.
- The append supersedes only "that sigrok verbs were unexercised" (:222-223).
- The surviving clause "no recording decode ... is claimed" directly conflicts with :225-226 "file-only UART decode". As written, the file both disclaims and asserts recording decode.
- Repair: supersede both clauses by name, for example "supersedes the R22 statements that sigrok verbs were unexercised and that no recording decode is claimed; no hardware contact remains unclaimed".

### F4. MEDIUM. "Date-supersedes" cannot be resolved by date (observed)
- PROVINCE.md:175 "REA6.5.0, observed 2026-10-21." (R22 block) and :220 "### Round-23 offline envelope additions — 2026-10-21". Both carry the same calendar date.
- Ordering therefore rests only on file position and the round label. The phrase "the round-22 instant's statement" (:222) names an instant that the date cannot locate.
- Repair: add an explicit ordering anchor, for example the baseline commit aa1450b82f9ede35aada63efe8a34e01c6e02f72, or a time with zone, and cite the R22 block by heading. If the round label is intended as the ordering key, say so.

### F5. MEDIUM-LOW. "remain Adjacent/unowned" asserts a prior placement that is not recorded (observed)
- PROVINCE.md:229-230: "hardware acquisition and device control remain Adjacent/unowned, not absorbed into this province."
- The Adjacent section (:95-116) has five bullets: malware triage, non-REA dynamic analysis, source-available reconstruction, installing engines, quality verdicts. None names hardware, acquisition, device control, sigrok or logic analyzers. A case-insensitive grep for hardware|acquisition|sigrok|logic|device over candidate PROVINCE.md finds no Adjacent entry. The only pre-append hardware statement is the R22 non-claim at :218.
- The same assertion recurs in corpus/lessons/round-23.md:74-75 ("Hardware remains Adjacent/unowned") and SKILL.md:722 ("Still Adjacent/unheld"). Neither is the disposition authority.
- Repair: add an Adjacent bullet in the file's existing "(unowned)" style, or reword to "not claimed and unowned; no Adjacent placement is recorded".

### F6. MEDIUM-LOW. PROVINCE's held-ground prerequisite is unmet at LOG level (observed)
- PROVINCE.md:30-32: "ground moves to Core only after an end-to-end probe lands a LOG.md entry citing its evidence_id and subject sha256."
- LOG.md round-23 block (2587-2663): zero `ev_` identifiers (grep count 0). Subject digests are partial: APK a7b1f5c8... at LOG round-23 body; AppImage abbreviated "SHA25649d2f597…9f50b614" at LOG.md:2639. The launcher digest 50fe43590a7b... (S058:101-102) is absent from LOG.
- Evidence IDs exist only in S058 (:15 ev_940cf7bb…, :50 ev_bcadf773…, :75 ev_1d361f25…) and S061 (:29 ev_d2ff19d7…).
- Effect: the held dispositions asserted in PROVINCE have no LOG entry carrying the IDs the file requires. Repair belongs to the LOG owner (L1). PROVINCE should either cite the IDs or withhold "holds" until LOG carries them.

### F7. LOW. "holds" collides with PROVINCE's term of art (observed)
- PROVINCE.md:30-31 defines "available, not held". The append uses "holds" for dispositions (:225, :233). S058:8 "This entry holds two REA verbs" also uses it as held.
- Recommend "records" for the source-content sense, and "held (conditional)" for disposition.
- "fit artifact evidence" (:229) is domain-fit prose, not an ownership grant. The following sentence and :241-242 disclaim ownership. Acceptable with the wording change in F2.

### F8. LOW. Qualifiers dropped relative to S061 (observed)
- S061:35: "libapp.coverage:complete is scoped to the reader's section/header contract." The append at :234-235 says "section/header coverage is complete" without the scope phrase.
- S061:5 and :57-59 ("carrier-layout conditional", "conditional held-verb observation") are not carried into the append (see F1).

### F9. LOW. Digit/space gluing, pre-existing and corpus-wide; cause inferred (observed; [INFERENCE] on cause)
- In B: PROVINCE.md:175 "REA6.5.0" (B line identical); SCORECARD.md:2786 "Held0/6→1/6" (before the diff hunk at :2798, so unchanged from B).
- In round-23 additions: S058:17 "reports110", :41 "at960000Hz", :76 "retains12885", :88 "this6.5.0", :111 "ceilings1GiB", :107 "sigrok-cli0.7.2"; LOG.md:2650 "cumulative1/6→4/6"; SCORECARD.md:2827 "held1/6→4/6".
- Not claim-affecting: count-c1.py reads SOURCES.md (:69-70, :86) and JSON envelopes, not these prose tokens. Legibility and any regex over prose are affected.

### F10. LOW. Compressed carrier labels (observed)
- "Saber1330203" (PROVINCE.md:233) and "Saber1360103" (:236) drop the underscore of saber_1330203.apk and saber_1360103.apk.
- Identity is recoverable: S061:14 (URL), S061:18-19 (sha256 a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618); R22 file line 3 (sha256 de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720).
- Not an error. For checkability from PROVINCE alone, the append should cite the S061 URL or digest for "exact archived" (:232-233).

## Passed checks (observed)

- P1. Byte-level no-harm. `git diff -U0 B C -- PROVINCE.md` is one hunk, `@@ -218,0 +219,24 @@`, with zero deletions. stdout sha256 a696a47ac838686fd9646d50b302c8ba99b30b857d52b6930b89103295bf6612 (this host). Lines 1-218 are identical to B. The R22 table rows (:188-203), the R22 Dart sentence (:211-212) and the R22 sigrok sentence (:217-218) are not rewritten.
- P2. Counter independence. count-c1.py derives `held` from `targets[verb]['exercised']` (:127-130). PROVINCE prose is not an input; only corpus/SOURCES.md is read from the corpus (:69-70, :86). The mention-counts falsifier is therefore not reachable through PROVINCE text. The counter was not executed (not a designated Run seat).
- P3. Refusal preservation. PROVINCE.md:236-237 keeps the Saber1360103 refusal "valid and unchanged". The R22 file (corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md:15) records that operation as "not held or counted", which is consistent.
- P4. Debugger and hardware non-expansion. PROVINCE.md:239-242 and S058:114-116 ("No target/device execution, attach, hardware acquisition or debugger ownership is claimed or credited") agree. No debugger or hardware row is added.
- P5. Factual payload. Decoder discovery (S058:13-20), signature-module load failure (S058:21-24), synthetic UART decode (S058:37-60), and digest-pinned public UART decode (S058:64-67, sha256 01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61) match the append's sentences at :224-230. S061 section/header complete and string pool partial (S061:35, :50) matches :234-235.
- P6. Stale W1 re-evaluation. No round-23 PROVINCE proposal file exists at candidate: `git ls-tree -r --name-only <C> -- .ufo/waves/round-23 | grep -i province` returns nothing. There is nothing to re-evaluate for this item.

## Produced files and hashes

- Report: .ufo/waves/round-23/w2/ProvinceAppend.md (this file). Its sha256 is reported in the seat's final message, not here (self-reference).
- Candidate reference blobs and digests:
  - PROVINCE.md @C: blob 537880d0e488ef584d198b4988409169ca5fca1d; sha256 541a5b209031045240e76ca5915705ecd475ac4841cc2fbb6701ef28c9e0844c; 242 lines.
  - PROVINCE.md @B: blob 918434dda2379f6342db9a4e26c2a7cc3706cd57; sha256 dbf757fec564e1fdb5497cf773dbd11021a5f464ecab2802f780a1c78691ed97; 218 lines.
  - corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md @C: blob 6c14cce624550135d19b587358b820886f096bcc; sha256 7598d2cb436ceee4b6dc01c10869a9db0cd0f49afaf971aa02eb9f771aee6c35.
  - corpus/knowledge/2026-10-21-r23-dart-legacy-layout-boundary.md @C: blob 7d24fb83a4c081464486925dcafce668351b1587; sha256 22711853c6a9ee31ce31669db17e8c8bef95892ba9c6831321704c2bd0178351.
  - LOG.md @C blob 9966bfb7d5791d847f39a20f73896a6388b3684b; SCORECARD.md @C blob 7f2adb4e1d3519c316c4a735a98c960e59966951; corpus/lessons/round-23.md @C blob 96ffed835e65069d5f9ca448a5873f40fa4f1175; corpus/README.md @C blob b5863fc2e307696571d225c55370bf2ab8c99232; SKILL.md @C blob e21f0b113b3e9ab3356ed998652bef66fb8b5e84.
- Commands run, all read-only: git show, git diff, git log, git rev-parse, git ls-tree, git grep, git status (one call, see Open risks), sha256sum, sed/grep/awk over git show output. No command failed in a way that changed a finding.

## Installs or none

None. No package, tool, runtime or global configuration was installed or updated. No pacman transaction. No host service touched.

## Open risks

- Lane index: one `git status --porcelain=v1 --branch` ran without `--no-optional-locks`. Git may refresh the `.git/index` stat cache. No content edit was intended; disclosed against the lane's index read-only rule.
- Not re-measured: "4/6" is inherited from LOG.md and SCORECARD.md text and the frozen verify artifacts. count-c1.py was not run.
- Not verified: evidence files cited by S058/S061 were not opened. Knowledge-file claims were checked against their text only, and only where the PROVINCE append depends on them. claims.json was read from the worktree path; HEAD equals the candidate and `git diff --quiet <C> -- .ufo/waves/round-23/claims.json` exits 0, so the bytes equal the candidate.
- Out-of-item observations for owning seats, not reviewed in depth:
  - (a) S058:94 cites `sigrok-extraction.json`, and the SOURCES S058 row cites `evidence/sources/sigrok-cli.1`. Both sit outside the claim rule "new evidence only under round-23/evidence/c1".
  - (b) S061:2 cites a connector scope deviation. The round-23 LOG block discloses ConnectDartSymbols production-tree writes by an advisory seat.
  - (c) corpus/README.md diff against B removes three blank separator lines (B:73, B:160, B:177) and adds three rows (C:72, C:159, C:176). LOG round-23 says the rows consume existing separator lines, so this is likely benign; not examined further. The pre-round-rows no-harm check belongs to the README owner.
- Residual wording risk: the compressed "Saber1330203" label (F10) and the "holds" vocabulary (F7).
