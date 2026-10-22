# CensusEnd: SOURCES census and row counts (kaidoku round 26, wave 2)

Seat: KaidokuR26.CensusEnd, leaf. Scope: the SOURCES census and row counts. Attacked wave 1 (CensusCheck, SourceRowRegistry, LessonMistakes, CapinfosFacts) on this scope. The lane was read-only; this file is the only lane write. Fixtures and clone live in /fast/scratch/hyaku/kaidoku-r26/seats/w2/CensusEnd/. No REA call. Access date 2026-10-22; no web sources. Tools: none installed or upgraded (host git, gawk, awk, grep, sha256sum and the Python kernel only).

## Verdict
- Census validate exit 0. Output is five W04 warnings and `kaidoku ok`. The W04 set is byte-identical at a0639d8e and c327772653, so there are no new warnings.
- Row count: 78 at a0639d8e, 80 at c327772653, 80 in the worktree. "78 to 80" holds. The +2 is S079 and S080.
- One census defect fails (F1, medium): the duplicate-URL key keeps Markdown trailing punctuation, so a same-scope plain-URL duplicate passes with exit 0. Nothing in the lane is hidden today. Wave-1 CensusCheck calls the trailing backtick cosmetic; I disagree.

## Census output and exit
Times are UTC, from file mtimes (local -03:00 converted).
1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`: exit 0, 13:00:17Z. stdout sha256 75ae4b16…3ec3bde (same bytes as wave-1 census-worktree.out). stdout:
   kaidoku W04 S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
   kaidoku W04 S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
   kaidoku W04 S054 duplicate url developer.android.com/ndk/guides/abis across scopes
   kaidoku W04 S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
   kaidoku W04 S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
   kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
   stderr empty.
2. `sources-census.sh census kaidoku`: exit 0, 13:03:24Z. rows 80; tier.A 74; tier.B 5; tier.C 1; status.mined 78; status.rejected 2; missing 0.
3. `sources-census.sh overdue kaidoku --today 2026-10-22`: exit 0, 13:03:24Z. No overdue line; 80 cadence lines.
4. Sandbox clone, explicit directory argument: validate at a0639d8e exit 0 (13:01:51Z) and at c327772653 exit 0 (13:01:50Z). Both stdout files are byte-identical (sha256 39ea3bbc…426639e) and carry the same five W04 lines.
5. `sources-census.sh selftest` with TMPDIR in scratch: exit 0, 96 killed, 0 survived, finished 13:07:06Z.

## Row counts (`git show REV:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'`)
- a0639d8e: 78. Ids S001 to S078, unique, no gaps. Blob c1d9d8a2…
- c327772653: 80. Ids S001 to S080, unique, no gaps. Diff from base is four inserted lines, the two rows S079 and S080. Blob 7264b4cf…
- Worktree at HEAD fe3eb4ed (13:01:50Z): 80. `git diff --quiet c327772653 -- corpus/SOURCES.md` exit 0, so identical to c327772653.
- Rows with leading spaces: 0. Four-digit ids: 0. The script census agrees (78 and 80).
- Earlier counts cited in w1/LessonMistakes.md (row at line 90) verified: 18e7eb6d 72, 7ef837a4 74, cce7504a 78, a0639d8e 78.

## Findings
F1 (medium; reproduced; latent in the lane). The duplicate-URL key keeps trailing punctuation, so E04 misses plain-form duplicates.
- Code: `sources-census.sh` `url_of`, lines 600-605. It takes the first `https?://[^[:space:]|]+` in the source cell, drops a fragment and one trailing slash, lowercases the host, and keeps everything else. The keys for S038 and S047 end in "`,"; S035 ends in ")".
- Repro, clean fixtures (every used-by set to an em dash, so E11 noise is absent). Base is the c327772653 SOURCES with the S083 row added: plain `https://go.dev/dl/?mode=json&include=all` in S047's scope. Result: exit 0; no E04 or W04 for S083; only the pre-existing S047 W04 line (fx-clean-plain.out, 13:06:31Z). Same base with S084 in the code-span form: exit 1 and an E04 line for S084 whose key is the same URL with a trailing backtick and comma (fx-clean-tick.out). The same duplicate passes or fails depending only on that backtick.
- Lane impact now: none found. An emulation of these key rules (Python kernel; only its JSON output is saved, emulation.json) reproduces the five W04 at both revisions with zero E04, and finds no pair of rows whose keys differ only in trailing punctuation.
- The script selftest passes (96 killed) and does not cover this: its fixtures use plain URLs only (grep for a code-span URL in the script: 0 hits), so a regression would not be caught.
- Suggested fix, not applied (lane and script untouched): strip trailing characters from the set ` , ; . ) ' " ] from the first URL before keying; add selftests for plain versus code-span duplicates within one scope (expect E04) and across scopes (expect W04).

F2 (low; documentation drift; no exit effect). `overdue` prints `cadence` lines for NNd rechecks too and appends `opened=`. The header (script lines 34-37) documents cadence lines for symbolic rechecks only, with no `opened=` field. Code at lines 676-677. Observed: `kaidoku cadence S008 recheck=180d opened=2026-10-19`, exit 0, 13:03:24Z.

F3 (low; dangling pointer; not a census defect). w1/LessonMistakes.md rows at lines 26 and 90 cite `.ufo/reports/round-25/kaidoku.md` ("stated 74", "72 at 18e7eb6d"). That path is absent from the worktree (`ls`: No such file or directory), and `git log --all -- .ufo/reports/round-25/kaidoku.md` prints nothing. The 72, 74, 78, 78 counts verify; the report-side claim cannot be checked from the lane.

F4 (info). Wave-1 claims re-checked:
- CensusCheck F1 and F2 (exit 0; five W04 pre-exist): hold.
- CensusCheck F3 (78 at base; working copy byte-identical to base at 12:17Z): base count holds; the identity was true then and is superseded by the S079 and S080 rows.
- CensusCheck F4 (S079 and S080 unused at 12:12Z): held then; both are now used, and neither has a W04 or E-code.
- CensusCheck F5 (corpus/lessons/round-26.md absent at 12:14Z): superseded; both used-by paths resolve at c327772653 (no E11).
- SourceRowRegistry self-check (79 rows, tier.A 73, mined 77 with S080 alone): consistent with the final 80, 74, 78 once S079 is added.
- CapinfosFacts (count sentence about S064 to S071 at round-24 search log): not re-verified in full at c327772653; not relied on here.

## Residual risk and gaps
- The worktree is HEAD fe3eb4ed at 13:01:50Z and the L1 is still landing commits, so worktree counts can move. The committed-revision counts cannot.
- F1 is reproduced in scratch fixtures, not as a live lane failure.
- The emulation covers only the key rules (url_of, W04, E04). E01 to E12 results come from validator output, not a re-derivation.
- Not checked: the `shared` mode, and S079 and S080 cell content beyond validator rules (the wave-1 seats cover content).
- fx-trailing/ is a discarded first fixture (probe placed after the Paths section); nothing relies on it.

## Artifacts (scratch /fast/scratch/hyaku/kaidoku-r26/seats/w2/CensusEnd/, sha256)
- validate-fleet.out 75ae4b1633b3d7ba5d3ee4add8a4e57ba12b0a48011d3bdce9fd8269b0ec3bde (exit 0, 13:00:17Z)
- validate-fleet.err e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 (empty)
- census-kaidoku-fleet.out 7c73777bcdb118a151bce20c15811b63bc2102a87a7f6d5677d68f23e151a032
- overdue-kaidoku-fleet.out f12bf1c06df2107460f5639d47ba50fe723d1179eeb8e8d6233940c087666f7c
- census-c3277726.out c91c44d974eabbbb6603fe3aa45a3dacfe525e89383f54d514b585cfdb8bcd82; census-a0639d8e.out 0321b0c48183ca45366007a92acbfc971d644daaf01a6ed143cae1ee7be6ee7c
- validate-c3277726.out and validate-a0639d8e.out, both 39ea3bbcab0c6d947342681be8755e216257e11d6409e483f7bf4c620426639e
- emulation.json e82fcbe9e9292f865de8ce1d147d515b04cce868e15c2b048bfcaeda87264f46
- fx-clean-base.out b0adfff925a69b5eb8f6dbc0366a5479299505e614f5f98a039309d350e6b34d; fx-clean-plain.out 2884d28e47ba55baf5a90c06bd67b05e8888bd68d1cc320e6e94087e23eb4ce3; fx-clean-tick.out 9710f645a84136380aeffaeec2d0b57dd3e0d4422e77c487745eede0ee276668
- fx-plain.out db76dd3930d4f9f434769e9e5da432a4ef0d73cec0b423f5386fe0841b5428f5; fx-tick.out 314e133a35a718124cad2a27515b6d260fb906904cd3efd56db0dcec61819a34; fx-e04-plain.out 962a64a9acb5519b9c0f460f43d678e0bb055b70c59b78c3a3e78067c3302a26; fx-e04-tick.out bb0f6a26b7acfa44ea2e0ddbffc35341eaa3c099a799f03e965f428305114775
- clean-base.md 353db5411d6bdf1cdfc72b28a85f34b6db22a6ef21f68d18e2f9d8fa6a70f2f4; orig-c3277726.md 945900936762151ad8544c8a0f66179d5c119aefe562e82a067b1085f6ae4657
- ids-a0639d8e.txt 36cddbedbeaa08685120926a7ae76d73ba2836532376a8254608f90bbf419362; ids-c3277726.txt 537447d99d5df8e963d9e303c4aa344bcba329ddcef44a2699309f6ac38f2139
- selftest.out 6f61744e1183d1ece7e10a73bbcca20d4ab75553e593744fc9103e9d3ca864dc (exit 0)
- /home/vgpnk/Projects/shokunin/scripts/sources-census.sh (read only): 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30
