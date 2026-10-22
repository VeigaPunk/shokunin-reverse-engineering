# CapinfosFacts: premise of routed defect 5 (round-24 capinfos disagreement)

Seat: KaidokuR26.CapinfosFacts. Leaf member; read-only on the lane; no subagents, no installs, no REA run. Only this report was written in the lane.
Date: 2026-10-22, about 12:13 to 12:23 UTC. Lane HEAD c27f445e. Routed text: corpus/lessons/round-25-verifier-spotcheck.md:196-197 (commit a0639d8e).

## 1. Verdict

A new QUALITY criterion is needed. The S071 flip does not already cover the lesson.

| Premise element | Verdict | Basis |
|---|---|---|
| Capinfos was rejected as a row | holds | corpus/lessons/round-24.md:23 |
| S071 later admitted the manual | holds | corpus/SOURCES.md:77; corpus/lessons/round-24.md:85-87 |
| No QUALITY criterion covers it | holds | Command C2: no commit in all history touched capinfos in QUALITY.md |
| The flip records the lesson | fails: it records the instance, not the rule | Section 5, R1 to R7 |
| A criterion is the right remedy | holds, narrow | Section 7, draft row 35 |

Note: QUALITY row 34 (QUALITY.md:44) already cites round-24-verifier-spotcheck.md, for the C2 item only. "Citing the r24 spot-check" therefore does not by itself show coverage of the capinfos item.

## 2. What was rejected, and why

- Rejected: capinfos(1) 4.6.9 as a source row. corpus/lessons/round-24.md:23, commit 69e82c48 (2026-10-21 13:59:00 -03:00). Quote: "Not needed: REA's pcap output already records counts/times." Flip clause: "a claim that depends on capinfos semantics directly."
- Same exclusion in the search log: corpus/SOURCES.md:135 ("not needed for a held claim").
- Basis: the L1 opened the manual (sha256 76a23815...f61, round-24.md:23). It did not search REA's consumer code, and the row cites no REA line.
- Conflict on the day: the frozen R24-C1 sourced line requires witness rows including "Wireshark 4.6.9 tshark/capinfos manuals" (.ufo/waves/round-24/claims.json:24, identical at freeze 5dc49bfe, 13:44:44 -03:00, and at 69e82c48). The rejection came 14 min 16 s after the freeze.

## 3. What flipped it

- Trigger: residual reviewer ResHonesty-2, finding 7, at .ufo/waves/round-24/residual/KagiR27-2.ResHonesty-2.md:42-49. REA dist/pcap/PcapProvider.js:330 runs `capinfos -M`; lines 339-342 and 366-369 take file type, packet count and times from it. Quote at :47: "which is exactly the row's flip condition".
- Accepted in commit 5c88c05b (2026-10-21 15:18:48 -03:00): round-24.md:82-87 ("the capinfos rejection was wrong and its flip fired"); SOURCES.md:76 (S070 supersedes S066, cites PcapProvider.js:330), :77 (S071 admitted; "the earlier rejection is reversed because its flip condition fired"), :137 (search-log reversal); LOG.md:2800-2801.
- Outside check in commit 18e7eb6d (2026-10-21 18:33:04 -03:00): round-24-verifier-spotcheck.md:44 ("Disagree with the initial not-needed rejection; agree with its recorded flip") and :61 ("initial rejection was wrong").

## 4. Timeline (local -03:00; UTC in brackets)

| When | Commit | Event | Where |
|---|---|---|---|
| 10-21 13:44:44 [16:44:44Z] | 5dc49bfe | Round-24 claims frozen. R24-C1 counts inspect-pcap-capture; sourced line names the tshark/capinfos manuals | claims.json:18, :24 (git grep at 5dc49bfe) |
| 10-21 13:59:00 [16:59:00Z] | 69e82c48 | Capinfos rejected. S066 admitted, citing TsharkCaptureProvider.js and pcapAnalysis.js (hash only), not PcapProvider.js. Envelope already holds packet_count 4 and capinfos_version. claims.json gains instrument_supersessions; sourced line unchanged | round-24.md:23; SOURCES.md:72, :135; l1-pcap-capture-dns.envelope.json (git grep at 69e82c48); claims.json diff 5dc49bfe..69e82c48, +4 -1 |
| 10-21 15:18:48 [18:18:48Z] | 5c88c05b | Residual flip: S070 and S071 admitted; capinfos -M sentence added to the knowledge entry; LOG entry | SOURCES.md:76-77, :137; round-24.md:82-93; knowledge file :111-112; LOG.md:2800-2801 |
| 10-21 18:33:04 [21:33:04Z] | 18e7eb6d | Outside spot-check agrees with the flip and disagrees with the rejection | round-24-verifier-spotcheck.md:44, :61 |
| 10-22 06:30:53 [09:30:53Z] | 0e333eb2 | QUALITY row 34 from the spot-check's C2 verdict; SCORECARD and LOG record the round verdict only | QUALITY.md:44; LOG.md:2954; SCORECARD.md:3048; round-25-verifier-spotcheck.md:158-159 |
| 10-22 08:53:49 [11:53:49Z] | a0639d8e | Round-25 spot-check routes defect 5 (lane base for round 26) | round-25-verifier-spotcheck.md:196-197 |

## 5. Why the flip does not cover the lesson

- R1. It records the instance, not the rule. The S071 row gives the reversal and its trigger (SOURCES.md:77). No line tells a future L1 to search consumer code before a "not needed" rejection. QUALITY row 33 covers instrument freezes only (QUALITY.md:43). No QUALITY commit ever named capinfos, S066, S070, S071 or tshark (command C2).
- R2. The trigger was already true when the rejection was written (inference). The flip clause is "a claim that depends on capinfos semantics directly" (round-24.md:23). R24-C1's frozen verb list includes inspect-pcap-capture (claims.json:18). That verb's file type, packet count and times come from capinfos -M (PcapProvider.js:330, 339-341, 366-368). The envelope committed with the rejection holds packet_count 4 and capinfos_version. So "fired" (SOURCES.md:77) describes a condition that was met from the start. Falsifier: if "depends directly" meant "a claim text names capinfos", R2 fails; R1 and R3 to R7 still hold.
- R3. One search would have shown the dependency. Command C7 (read-only search of the installed 6.5.0 package) returns 119 lines in 14 files, 7 of them pcap-named. Key hits: PcapProvider.js:330 (capinfos -M) and :361-362 (count cross-check); PcapOutput.js:13 ("capinfos -M ... provides exact numbers"); domain/pcap/pcapAnalysis.js:59 ("File format as capinfos reports it"); contracts/pcap/pcapToolContracts.js:6 and :20 ("Requires caller-supplied capinfos and tshark"). S066 names pcapAnalysis.js by sha256 (SOURCES.md:72; the hash matches the installed file) but cites no line, so whether the L1 read it is unknown.
- R4. The contradiction sat in the frozen file for 14 min 16 s. Nothing compared the sourced line with the rejection until the residual review (ResHonesty-2.md:49).
- R5. The rejection was not registered. Lane precedent keeps rejected sources as rows with status "rejected" and a flip clause: S022 (SOURCES.md:28) and S028 (SOURCES.md:34). The capinfos rejection lived only in the lesson table and the search log, so the registry cannot show it or audit its flip. ResSources-2.md:114-116 calls the precedent mixed (the round-23 guide was also unregistered).
- R6. The source-level outside decision is not in SCORECARD or LOG. Their entries record only the round verdict (LOG.md:2954; SCORECARD.md:3048). The capinfos disagreement (round-24-verifier-spotcheck.md:44) is in neither. QUALITY row 34 requires SCORECARD and LOG to record "each outside closure decision (admitted or rejected, with the spot-check path)" (QUALITY.md:44). Read broadly, row 34 is unmet here; read narrowly, it is silent. The lane has not settled which.
- R7. The nearest rules miss this case. Signal 4 ("REA supports/refuses X" from docs or memory, QUALITY.md:53) and signal 6 ("Tool X is broken/missing" without checking REA's spawn wrapper, QUALITY.md:55) are weak-material signals (QUALITY.md:46), not admission criteria. Neither covers "already records" or "not needed" rejections.

## 6. What the flip does cover (fair counterweight)

- The instance is reversed and recorded in at least nine places: round-24.md:82-93; SOURCES.md:76-77, :137; LOG.md:2800-2801; knowledge file :21, :111-112; spot-check :44, :61; ResHonesty-2.md:42-49.
- The wrong rejection is preserved: round-24.md:23 is unchanged since 69e82c48 (command C3), as the spot-check asked (:44).
- No held claim relies on the rejection now: the R24-C1 sourced line is met by admitted rows S064 to S071, and the knowledge entry cites S070 and S071 (knowledge :1, :112).
- Corpus search for other fired flips finds none (command C8). Conditional rejections recur (S022, S028, capinfos, and round-25's S068 narrowing at round-25.md:49), but only capinfos has a fired flip. Recurrence of the failure is not shown. The case rests on the cost of the missing check (one search) and on QUALITY.md:3-5, where criteria grow from lessons.

## 7. Draft QUALITY row 35 (not applied; the lane owner decides)

```
| 35 | A source rejected because a tool or provider already supplies its information ("not needed", "already records", "reject as a row") is a registry row with status rejected and a flip clause. It is decided only after a recorded search of the installed consumer code for that tool's name at the measured revision (command, tree, hits as file:line). A hit in code that fills a retained field is a flip: the row is admitted at decision time, and its flip clause is judged against those hits then, not at residual review. A no-hit result is recorded as "no hit in <tree> at <rev> for <terms>", never as proof of non-use. A later reversal supersedes the rejected row and keeps it visible. | corpus/lessons/round-24.md:23 (capinfos rejected: "Not needed: REA's pcap output already records counts/times"; consumer dist/pcap/PcapProvider.js:330 runs capinfos -M); corpus/lessons/round-24.md:82-93 (flip fired at residual review); corpus/lessons/round-24-verifier-spotcheck.md:44, :61; corpus/lessons/round-25-verifier-spotcheck.md:196-197 (defect 5) | — |
```

Red check: the round-24 text run against the installed 6.5.0 package must fail, because the search hits PcapProvider.js:330. Placement: QUALITY, because the rejection decided what held claims could rely on (claims.json:24), and QUALITY.md:57 hands claim admission to this bar. If the lane also wants registration rules in SOURCES.md, add a one-line pointer there.

## 8. Side defects for the L1 (not edited by me)

- SOURCES.md:137 count is wrong: "included 6 families as rows S064–S071 (three of them supersessions)". S064 to S071 holds two supersessions (S069 supersedes S065 at :75; S070 supersedes S066 at :76). The third is S072 (:78), outside that range. "6 families" against 8 rows also needs a line.
- SOURCES.md:77 says the condition "fired". R2 says it was already met; the wording should say so.
- ResHonesty-2.md:49 cites claims.json:25 for the sourced line. It is :24 at 5dc49bfe and at 69e82c48 (command C4).
- round-24.md:23 has no pointer to the reversal at :82-93. An appended pointer helps readers and rewrites nothing.
- The frozen sourced line (claims.json:24) still names the capinfos manuals; it is now met by S071. Disclose it; do not rewrite frozen text.

## 9. Verification gaps and limits

- No REA run, no capinfos or tshark run, no installs, no lane edits. The consumer search is a text search of the installed package only.
- I did not open the online capinfos page. The retained copy's hash matches S071 (76a23815...f61).
- Unknown: whether the L1 read pcapAnalysis.js or PcapProvider.js before 69e82c48. I show only that the bytes existed and were hashed.
- R2 is inference and is labelled as such. R1 and R3 to R7 rest on the cited files and commands.
- Commit times are git committer times, not authenticated authoring times.
- Working tree equals HEAD for the seven lane files cited (command C6).

## 10. Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/CapinfosFacts/)

| File | sha256 |
|---|---|
| one_grep_capinfos.py | 35b05f0d12ff5c76bcb14c39d46771debe1b4ab7556bf40def52e876f716daa8 |
| one-grep-capinfos.txt | b55352c80e9d52107556cf030538ec7efcb27a622c0fd995f743b575ea21599a |
| git-facts.txt | 5284f466b43ffc1d23c68a0ddb4d2cb44cd2d66a52233d82cdc27414018bc172 |
| git-facts-2.txt | 4f8ba7ddfd24632aede20380940e507d1afbf71ed5b41c62ce8c72a73da239fd |
| sha256-capinfos-facts.txt | 2093aaaf7b58ab51e3b19a5ba193be8676f264c41bb0d26ccd38c1bf271a2c67 |
| sha256-rea-contract-read.txt | 4edf08e21ce9b1233ef2ef828dbddf62ab1c7cd11706f00e1e9f10c8b249c5c6 |

## 11. Sources and evidence opened (access date 2026-10-22; no web source opened)

1. Retained capinfos(1) 4.6.9 manual, .ufo/waves/round-24/sources/capinfos-4.6.9.adoc, sha256 76a23815609fd0b3b6da63c27a548a7c658744b5cc1ad59f131cc1cf4e275f61. Line 131: "Displays the number of packets in the capture file." Line 218: "Print raw (machine readable) values in long reports."
2. REA 6.5.0 dist/pcap/PcapProvider.js, sha256 16a4d813665208bd4f99229f431e0379a6e8b31d72a717d6c451c38833ed64d4. Line 330: `["-M", "--", snapshot.path]`. Lines 339-341 and 366-368 read.
3. REA 6.5.0 dist/domain/pcap/pcapAnalysis.js, sha256 7651b4c5582b62513196146b7aa08043fab93d0848ce7f8680523d867597c641. Line 59: "File format as capinfos reports it (pcap vs pcapng)."
4. REA 6.5.0 dist/contracts/pcap/pcapToolContracts.js, sha256 b7056ccbd8c55a59f5ab71e71fe42db2dd2e306abc5ec53c72ab2c2bb9edf753. Lines 6 and 20 as quoted in R3.
5. REA 6.5.0 dist/pcap/PcapOutput.js, sha256 bdd0c450dfdeb404b8c5ebec67f0d33020239dbce19cebcc0cf2a18118e623eb. Line 13: "capinfos -M with a C locale provides exact numbers".
6. Hashed only, not read: TsharkCaptureProvider.js (fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549) and PcapNativeBound.js (24811182c301a73ec1cb9792f31d6db911aec9c9f1bf71cf4bc7932bb0838cd2). Both match the hashes that S066 and S070 record.
7. Lane records read at HEAD (blob equals working tree): round-24.md, round-24-verifier-spotcheck.md, round-25-verifier-spotcheck.md, QUALITY.md, SOURCES.md, knowledge file 2026-10-21-r24-pcap-family-envelopes.md, claims.json; LOG.md and SCORECARD.md read, not hashed. Hashes are in sha256-capinfos-facts.txt.

## 12. Commands (producing command, exit code, UTC)

- C1 sha256sum over the REA and lane files, output to sha256-capinfos-facts.txt: exit 0, 12:16:07Z.
- C2 git --no-pager log --all -S TERM -- corpus/QUALITY.md, for capinfos, S066, S070, S071 and tshark: no output each, exit 0, 12:16:07Z; repeated in git-facts.txt section G at 12:18:48Z.
- C3 git log -S for 'reject as a row', '| S066 |', '| S071 |', 'rejection was wrong', 'excluded 1 (capinfos' and 'from `capinfos -M`': each exit 0, 12:16:07Z and 12:19:51Z (git-facts.txt, git-facts-2.txt).
- C4 git grep -n at 5dc49bfe, 69e82c48 and HEAD (claims.json, round-24.md, knowledge file, envelope, SCORECARD, LOG, QUALITY): exit 0, 12:18:48Z.
- C5 git diff --stat and git diff 5dc49bfe 69e82c48 -- claims.json: exit 0, 12:19:51Z.
- C6 git ls-tree HEAD and git hash-object on seven lane files: blob ids equal; exit 0, 12:18:48Z.
- C7 python3 -I -B one_grep_capinfos.py: exit 0, 12:21:00Z; output in one-grep-capinfos.txt.
- C8 Read, grep and glob tool calls for line citations and the corpus flip search: the tools returned no exit codes; outputs as cited, 12:14 to 12:23Z.
- Installs: none. REA runs: none. Lane writes: this report only.
