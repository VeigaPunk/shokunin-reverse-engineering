## CLAIM
Independent tail audit of `corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md` at HEAD `a280e07`: the round-9 qualification is not landed and the EOF append point is clean. New defect: the ready-to-append drafts scope "both 'benign' occurrences (`:217,236-237`)", but a third instance — capital-B "Benign payload" at `:12` — escapes that enumeration (case-sensitive greps miss it), so landing the note as written leaves `:12` unqualified and the note's own count inaccurate.

## METHOD
Read-only; HEAD = `a280e07133f52f719b0805fc73c0b997e77b5062`. Commands: `grep -n -i "benign" FILE`; `grep -n "byte-identical" FILE`; `grep -n "round.9\|Safety-verdict scope" FILE` (empty); `sha256sum FILE` vs `git show HEAD:FILE | sha256sum`; `tail -c 64 FILE | sha256sum`; `sed -n '100,102p;114,116p' PROVINCE.md`; `git diff --exit-code HEAD -- FILE PROVINCE.md` (exit 0). Read `D2.md`, `Z4.md`, `SCORECARD.md:77-80`. No probes, network, `/tmp`, or deletions.

## FINDINGS
1. Tail state: 16,295 bytes / 242 lines, EOF LF-terminated; worktree sha256 `541f3499c811b023f4a19e1aacef0129ef34222990f928de9f3d0a54fe4dbf2e` == HEAD == T2 baseline; tail-64 sha256 `374023ff74d8225e9b4bb03a9b530a79c1156fcf8501534f71ee27a3361e3bd7` reproduced. Last heading `## Errata (round 3)` (`:221`); EOF is a clean append point.
2. Qualification absent: no round-9/safety-scope text (`round.9` and `Safety-verdict scope` greps empty); both cited sites still read unqualified.
3. Occurrence census: `grep -n -i benign` → `:12` "Benign payload", `:217` "benign payload", `:236`/`:237` "benign, …". `D2.md:10` and `Z4.md:10-12` enumerate only `:217,236-237` and call them "both"; `SCORECARD.md:77-80` repeats the pair. A case-sensitive `benign` grep hides `:12`, which likely explains the miss.
4. Adjacent verdicts: `:219` "not binary compromise" and `:204-205` "genuine, unmodified" are affirmative-absence statements; the generic disclaimer clause should be phrased to cover them.
5. PROVINCE `:114-116` refusal verbatim (also `:100-102` malicious/benign labeling refusal); PROVINCE diff empty.

## THREATS
Drafts unlanded; this is revision guidance, not an edit. Line numbers are HEAD-relative; an append below `:242` is safe. Post-landing check: `head -c 16295` sha + tail-64 `374023ff…`; keep command A 79/79, 9/9. D3's r3-file bleed stays out of scope (`Z5.md:11`). Corpus digest claims are cited, not re-derived.

## VERDICT
FINDING: the append must cover the third "benign" site `:12` ("Benign payload"); the drafts' "both occurrences `:217,236-237`" enumeration is under-inclusive.
