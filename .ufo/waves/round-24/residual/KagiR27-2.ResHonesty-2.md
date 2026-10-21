# Round-24 residual seat — honesty and disclosure (KagiR27-2.ResHonesty-2, critic)

Scope: `corpus/lessons/round-24.md`, `PROVINCE.md` §§ Round-24, `SKILL.md` § round 24 and
`.ufo/waves/round-24/claims.json` at lane commit `69e82c48`, plus the uncommitted LOG/SCORECARD
round-24 sections in the working tree. Axes checked: coverage wording, decryption, tool provenance,
wave conduct, calibration framing, and missing disclosures. I only read the lane. My scratch
outputs are in `/fast/scratch/kaidoku-r24/seats/KagiR27-2.ResHonesty-2/`. I installed nothing.

## Verdict

**Overclaims and missing disclosures found; not clean.** Both headline numbers reproduce at
`69e82c48` with the current instruments: C1 is 4/4 (`c1_complete`, catalog zero 12), and C2 is
11/11 exact, round-24 CLEAN, exit 0. The text around those numbers overstates four things:

- what C2 measures;
- how fully the TShark build is pinned;
- the boundary on decryption keys;
- the capinfos source decision.

It also leaves out several conduct and timing facts. Two items are tradeoffs the canonical judge should weigh rather than defects: the C2 metric can be reached by transcribing the gate's output, and the post-freeze self-disclosure path is what lets round 24 count itself CLEAN. I do not call the round verified.

## Findings

### Calibration framing (C2)

1. **Under the frozen instrument, the C2 result fails, and nothing says so.** Observation: I ran
   `git show 5dc49bfe:.ufo/waves/round-24/tools/freeze-gate.py > gate-frozen.py; python3 -I -B gate-frozen.py --root <LANE> --rev 69e82c48 --require-clean round-24 --disclosures corpus/claim-freezes.tsv`. It exits **1** with disclosures `exact 9 of 11`, mismatched `round-17` and `round-18`. With the revised gate the same command exits 0, 11/11.
   `claims.json:55` and lesson lines 45–50 say the supersession "changes only historical verdict codes … not the before value … or the round-24 target". Both statements are true, but the after-value under the frozen instrument is never reported. S068, which the round cites, asks for deviations to be reported "so their impact can be assessed"; this impact is 9/11 and a red exit. Impacted axis: calibration.
2. **The 0/10 → 11/11 headline changes its denominator and includes the round grading itself.** The frozen before value is "0/10 … no round-24 freeze" (`claims.json:32`). The after value adds round-24, which the same author graded CLEAN. On the before denominator, the after is 10/10, all FLAGGED. The lesson (`round-24.md:7-8`) says "0/10 → all freezes". The uncommitted SCORECARD and LOG say "0/10 → 11/11". Neither says one of the eleven is the measuring round's own self-assessment. Impacted axis: calibration.
3. **"Disclosed" means the author's ledger agrees with the gate, so it can be reached by copying.** `corpus/claim-freezes.tsv` is written by the author, and the gate counts a row as disclosed when its verdict and code set equal the gate's own output (`freeze-gate.py:153-163`). The gate's docstring admits this (`:33-35`). The lesson, SCORECARD and SKILL registry present it as "disclosed with machine-checked instrument status". Inference: any ledger produced by pasting `freeze-gate.py` output scores N/N. The 0 → 11 change records that a file was written, not a judgment that was checked. This is a tradeoff for the judge, not a fixable defect.
4. **Round 24 is CLEAN only because the frozen file was edited after the freeze.** `instrument_supersessions` was appended to `claims.json` in `69e82c48`, after the freeze `5dc49bfe` (`git diff 5dc49bfe 69e82c4 -- .ufo/waves/round-24/claims.json` shows the edit is append-only). At the supersession commit itself, round-24 is FLAGGED: `freeze-gate.py --rev 9fb4eacd --require-clean round-24` exits 1, `required_failed ["round-24"]`. Round 22 (revised and unpinned) is FLAGGED; round 24 (revised and self-disclosed) is CLEAN. The headline "round-24 CLEAN" should say "CLEAN after one self-disclosed post-freeze supersession, FLAGGED at `9fb4eacd`". This is a tradeoff for the judge.

### Provenance and timing

5. **`declared_at` is later than the freeze commit that contains it.** `claims.json:6` reads `"declared_at": "2026-10-21T16:50:00+00:00"`. In this repo the jj-style committer time marks when a commit's content was finalized. The freeze commit `5dc49bf` has committer time `2026-10-21T13:44:44-03:00`, which is 16:44:44 UTC. That is about 5 minutes earlier than `declared_at`, and after-evidence was already produced by then: envelope runs at 16:45:41–16:45:47 UTC (`l1-*.run.json`, committed in `74cd4e3`, committer 16:45:57 UTC). A declaration time that postdates the C1 after-evidence is false provenance in a round about freeze discipline. The commit order itself is fine: instruments 16:44:07 → claims 16:44:44 → envelopes 16:45:57, all UTC. Also undisclosed: the instrument commit's author time is 16:04 UTC, but its content was finalized only 37 seconds before the freeze.
6. **"Pinned build" overstates the tool pins.** `tool-pins.json` `binaries` pins only `bin/tshark` (`00ed7bde…`) and `bin/capinfos`. `ldd bin/tshark` shows the dissector code lives in `lib/libwireshark.so.19` (sha256 `52c9467f…06a5`), plus `libwiretap`/`libwsutil`. None of these is pinned. TLS decryption also runs through system `libgnutls.so.30`/`libgcrypt.so.20`, which come from pacman, are unpinned, and are not recorded. REA itself says "Installed libraries … and dissector plugins are trusted and not fully fingerprinted" (`l1-packet-capture-http.envelope.json` limitations[3]). The `tool-pins.json` `limits` field does not mention this. Overclaims built on it:
   - `PROVINCE.md:293` "Removing or replacing the pinned TShark returns these verbs to the round-22 refusal state";
   - knowledge entry `:26-28` "A missing or replaced binary at that path ends every holding below";
   - `SKILL.md:750` "pinned build".

   Inference: a replaced `libwireshark.so` or a different TShark 4.x would not cause a refusal. REA reads the configured command; it does not check pins.
7. **The capinfos rejection is factually wrong, and its own flip condition is met.** Lesson `round-24.md:23` rejects capinfos(1) because "REA's pcap output already records counts/times". REA6.5.0 `dist/pcap/PcapProvider.js` (sha256 `16a4d813…64d4`) gets those counts and times from capinfos:
   - `:330` runs `capinfos -M -- <snapshot>`;
   - `:339-342` and `:366-369` set `file_type`, `packet_count` and `capture_start` from the capinfos metadata;
   - `:362` fails if tshark's packet count disagrees.

   The held `inspect-pcap-capture` observations (4 packets, 17 packets, 2004/2018 capture times, pcap vs pcapng) therefore depend directly on capinfos semantics, which is exactly the row's flip condition.

   In addition, `claims.json:25` `sourced` lists "Wireshark 4.6.9 tshark/capinfos manuals", but the capinfos manual was rejected as a row. S066 (`SOURCES.md`) cites `TsharkCaptureProvider.js` and `pcapAnalysis.js`, but not `PcapProvider.js`, the file that actually produces the pcap-capture summaries and the 300-CPU-second ceiling. The knowledge entry's ":94 … pcap provider reports its own inherited ceilings (300 CPU seconds)" has no source row.
8. **The signature check is weaker than "signature-checked" suggests.** The signing key was fetched from keys.openpgp.org (`tool-pins.json` `signature_check`). No web-of-trust path exists, and no independent anchor for the fingerprint `5A5ADBA7…AEEA` was recorded (for example, Wireshark's published key page). The tarball is not retained, and the build directory was deleted. The only retained build record is the cmake configure log; there is no ninja build or install log. The "no web-of-trust path" caveat is disclosed. The plain phrase "signature-checked official source" in the lesson, LOG, PROVINCE and knowledge entry is not qualified. Also unrecorded: `/usr/bin/ninja` (pacman `ninja 1.13.2-3`, pre-existing) was used for the build.

### Decryption

9. **The boundary "no decryption keys" is false as written.** `claims.json:26` C1 `boundary` reads "… no decryption keys". My independent block walk of `evidence/c1/captures/tls12-dsb.pcapng` finds two Decryption Secrets Blocks:
   - offset 96: type `0x544c534b`, 184 bytes, `# first\nCLIENT_RANDOM …`;
   - offset 5224: 176 bytes, `CLIENT_RANDOM …`.

   TShark applied these key-log secrets, and the counted envelope `l1-pcap-capture-tls` returns decrypted `http_request_uris` `https://example.com/` and `https://example.net/`. So keys were present in the input and were used. Only "lane-supplied" keys were absent. The knowledge entry (`:59-64`) and SKILL (`:758`) disclose this correctly, and my walk reproduces their offsets. The frozen claim boundary and `not_claimed: ["decryption"]` do not, and REA's envelope limitation ("encryption … can hide higher-level fields") is silent on decryption. The block walk is cited as "Observation" with no retained command or output. Not load-bearing for the count: `inspect-pcap-capture` is also held through the DNS envelope (inference from `count-c1` `targets`).
10. **The wave spec told probes not to decrypt, but the inputs decrypt automatically.** `gen-wave1.py:51` (ProbeTlsSni on `tls12-dsb.pcapng`, "No keys, no decryption") and `:63` (ProbeQuicHttp2 on `quic-with-secrets.pcapng`, "WITHOUT supplying any secrets file") are both DSB-bearing inputs that TShark decrypts unasked. Moot this round because no BUILD seat ran, but the spec would have produced contradictory instructions.

### Wave conduct

11. **The committed lesson never mentions that the BUILD wave did not run.** The lesson has no word on the 85-seat BUILD wave refused 20/20 (`wave1-refusals.jsonl`, 20 rows: 15 committed in `69e82c48`, 5 uncommitted). The only account is in the uncommitted LOG. Statements that assume BUILD ran:
    - `SKILL.md:774` registry: "none in the instrument (BUILD selftest items attack it)";
    - lesson M24-1 fix: "(BUILD selftest item)";
    - knowledge `:100`: "those are round-24 BUILD probe questions".

    Zero BUILD seats ran, so no BUILD item attacked anything.
12. **The selftest was written after the final commit, then cited as a control.** `tools/selftest.py` and `measure/selftest-69e82c48.jsonl` are untracked. `selftest.py` mtime is 14:01:19 −03:00 (17:01 UTC), after the `69e82c48` committer time of 16:59 UTC. It is not pinned in `instruments`, and its expected values for the after-state were written after the after-state existed: `c2_clean_at_rev` expects `[0, 11, []]` and `c1_positive_at_rev` expects `[0, 4]`. The LOG's "Selftest 17/17 red/green controls" does not disclose this. QUALITY32 requires selftest "expected outcomes are frozen before the demonstration". This selftest is an L1 post-hoc check, not a frozen or independent control.
13. **No committed after-measurement records exist.** `measure/` holds the before records and untracked no-harm and selftest files, but no after-c1 or after-c2 record. The uncommitted SCORECARD row says "(counting command, measured revision in the final section below)", and no such final section exists. My reruns (scratch `c1-head.json`, `c2-head.json`) reproduce 4/4 and 11/11, but the round's own record of those values is missing.
14. **The start-census conformance defect is disclosed only in an untracked file.** `measure/start-census.json` `measurement_scope` reads "the live start census was not taken before SOURCES.md changed (disclosed conformance defect)". It is absent from the lesson's Mistakes table, the SCORECARD, and the LOG, which says only "census exit 0 with the carried four W04". It belongs in Mistakes.
15. **The LOG promises findings that are not there.** The uncommitted LOG says the residual review's "findings and dispositions are appended to the round-24 lesson". They are not yet. The residual roster is verified as 4 critic and 4 reviewer (`residual-dispatch.json`), refused once, then spawned (`residual-attempts.jsonl`).
16. **A refused probe is cited without a record.** Knowledge `:76-78` cites a comma-joined `--fields` refusal as an "L1 probe before the retained run". No run record is retained for it, although `run-rea.py` keeps one for every producer call. This is minor: refusals are not counted, but the cited observation has no evidence behind it.

### Coverage wording

17. **Mostly honest, with one caveat on pcap-client.** "Finite proxy 10.0 → 10.0, delta 0", "finite family, not the network-forensics domain", and R23 T1 staying 4/6 are all accurate. Catalog zero 16 → 12 reproduces. The caveat: `inspect-pcap-client` counts as one of 4 held verbs, but its envelope has `subject: null` and "Artifact identity is unavailable". It echoes configured paths and versions and reads no capture. PROVINCE `:288` discloses this. The "holds all four verbs … on public test captures" wording in PROVINCE `:281-283` and the knowledge entry `:10` does not.

### Cross-reference (confirmed from sibling KagiR27-2.ResSources-2 F1)

18. **The REA argv is described with the wrong output flag.** Knowledge `:73` says REA builds `-r … -T fields … -2 … -Y … -d … -e` (citing S066, `TsharkCaptureProvider.js:203-217`). SOURCES `:72` (S066 teaches) and `:71` (S065 scope `-T fields`/`-e`) repeat it. Observation: `TsharkCaptureProvider.js:201-218` passes `-n -r capture -T json --no-duplicate-keys --temp-dir=. [-2] [-c N] [-Y f] [-d v]… -e frame.number -e <field>…`. The retained `l1-packet-capture-http.envelope.json` `normalized_result.tool.arguments` is exactly `['-n','-r','capture','-T','json','--no-duplicate-keys','--temp-dir=.','-2','-Y','http.request','-e','frame.number','-e','http.request.uri','-e','ip.src']`. A source row teaches an argv its own pinned file contradicts. The count is unaffected. Fix: change "`-T fields`" to "`-T json`", and list `-n`/`--no-duplicate-keys` and the implicit `frame.number` field, in all three places. The S065 scope should name `-T json`, and `-e` with json output, not `-T fields`.

Checked and found clean:

- README blank separators are restored before `## Knowledge`, `## Lessons` and `## Frontier`.
- Instrument pins match the blobs at freeze.
- Current `count-c1.py` matches its pin.
- `freeze-gate.py` HEAD equals the supersession sha256 `8a71fe84…`.
- The tshark and capinfos digests on disk equal the pins.
- The S066 quote "30 CPU seconds" matches `TsharkCaptureProvider.js:263`. The pcap envelopes' 300 seconds is a different provider, and the knowledge entry `:91-95` keeps the two apart.

## Recommended L1 action

These are the smallest safe corrections, all disclosure-only. No count changes.

1. **Lesson § Claim-freeze audit and SCORECARD C2 row:**
   - add "frozen instrument `5dc49bfe` at the final rev: 9/11 exact, exit 1 (r17/r18 rows written to the revised codes)";
   - restate C2 as "10/10 prior freezes disclosed (all FLAGGED) + round-24 self-assessed CLEAN after supersession; round-24 FLAGGED at `9fb4eacd`";
   - add one sentence that the ledger is checked for agreement with the gate, so N/N can be reached by transcription.
2. **`claims.json` `declared_at`:** leave it unchanged, because the file is frozen. Disclose in the lesson that it postdates the freeze commit (16:44:44 UTC) and the C1 envelope runs (16:45 UTC), and treat the commit object time as the freeze time.
3. **`tool-pins.json` `limits`, PROVINCE `:293`, knowledge `:26-28`, SKILL `:750`:** say that only the two launchers are pinned, that `libwireshark.so.19` (`52c9467f…`), `libwiretap` and `libwsutil` plus system libgnutls/libgcrypt/libpcap are unpinned, and that a replaced library or another TShark 4.x would not cause a refusal. Either pin the `lib/` digests or drop "replaced".
4. **capinfos row (lesson `:23`, SOURCES search log):** correct the rationale, since REA's `PcapProvider.js:330-369` takes `file_type`, `packet_count` and capture times from `capinfos -M`. Either admit capinfos(1) as a row (the flip has fired) or narrow the pcap-capture holding to the TShark-derived fields. Add `dist/pcap/PcapProvider.js` (`16a4d813…`) to S066 or to a new row, as the source of the summaries and the 300-second ceiling. Note that `claims.json` `sourced` names a capinfos manual that was not admitted.
5. **Lesson § Tooling, Limits and Mistakes:**
   - say "embedded TLS key-log secrets (two DSBs, offsets 96/5224) were present in an input and applied by TShark; the frozen boundary 'no decryption keys' means no lane-supplied keys";
   - retain the block-walk command and output;
   - qualify "signature-checked" as "good signature from a keyserver-fetched key with no independent fingerprint anchor";
   - record the pre-existing pacman ninja 1.13.2-3 as a build dependency.
6. **Wave conduct, in the committed lesson:**
   - zero BUILD seats ran (20/20 refused);
   - replace "BUILD selftest items attack it" (`SKILL.md:774`, M24-1) with "L1 post-hoc selftest only";
   - say that `selftest.py` was written after `69e82c48`, is unpinned, and has after-state expectations set after observation;
   - commit the selftest and the after-c1/after-c2 records, or write the missing SCORECARD "final section";
   - move the start-census defect into Mistakes;
   - commit the 5 remaining refusal rows.

7. **Knowledge `:73`, SOURCES `:71-72`:** change `-T fields` to `-T json`, as in finding 18.

Checks the main agent should run after correcting: rerun `freeze-gate.py` at the new rev with both the frozen (`5dc49bfe`) and revised blobs, and confirm both results appear in the record. Also confirm the new disclosure text is reachable from the committed lesson rather than only from the uncommitted LOG.
