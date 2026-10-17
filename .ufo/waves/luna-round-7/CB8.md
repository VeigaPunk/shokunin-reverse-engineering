## CLAIM
Round-6 receipts are admissible for the round-7 coverage entries as *retained documentary* evidence under an explicit per-entry provenance line — not as a "held this round" claim, and never with "independently reproduced" phrasing.

## METHOD
Read fleet rules `/home/vgpnk/Projects/shokunin/PROTOCOL.md:328-347,480-483`, `CORPUS.md:23,34-36`, `corpus/QUALITY.md:11,16,17,20`; round-6 receipts and both MANIFESTs; audit seats BC1, BC2, BC3, CB10; `.ufo/reports/luna-round-6/kaidoku.md:53-56`. Commands: `git ls-tree -r --name-only HEAD -- .ufo/waves/luna-round-6/receipts .ufo/waves/luna-round-6/receipts-B` (26 files tracked at HEAD 411175e); `sha256sum` of receipts-B/leg-{1..10} vs MANIFEST (10/10 match); `grep -rln "\.ufo/waves" corpus/knowledge/ | wc -l` (58 of 72); `git rev-parse HEAD:<receipt>`.

## FINDINGS
- The rules bind the pointer, not the author: evidence is "a resolvable pointer … at closure time" (PROTOCOL.md:341; CORPUS.md:23) and `corpus/` inherits that standard (:480-483); QUALITY 1/6 admit a repo path plus Evidence ID or exact reproducing call. Non-author verification is demanded only at gate marks (PROTOCOL.md:64-67), so self-authorship is not itself a bar — 58/72 existing entries already cite `.ufo/waves`.
- Durability holds: all 20 legs are tracked at HEAD and lane-B's MANIFEST recomputes 10/10, but lane-A's pins L1 only (`receipts/MANIFEST.txt`, 1 line; kaidoku.md:53). `git rev-parse HEAD:<receipt>` gives an author-independent blob pin for every leg — stronger than the self-authored MANIFEST (BC1:16), which predates leg-3's 19:10:19 write (BC3:14).
- What cannot be claimed: lane-A receipts carry no seat line (`grep -c Seat:` → 0); authorship is textual and unsigned (BC3:14; CB10:18); current legs 7/8 are compare-seat receipts (CC7/CC8) replacing unrecoverable BB7/BB8 originals (kaidoku.md:55-56; BC2:18); CB1:4,13 built a hash-consistent forgery by copying lane-A stdout — run-vs-copy is undecidable, so cross-lane hash agreement evidences the claim class, not independent execution.

## THREATS
No fresh probe or carrier re-hash was permitted; my 10/10 recount trusts a self-authored pin (blob pins I read mitigate, but no second seat re-ran them). E*V/G*/Z*/Q* reviews are same-lane second looks, not independence. Criterion 10's literal "this round" (QUALITY.md:20) is unsatisfied for any "held" reading — hence the framing below.

## VERDICT
FINDING: admit the round-6 receipts, but each entry must state provenance inline — run round/date and commit `bc91424`, `source:` receipt path + line ranges + `git rev-parse HEAD:<path>` blob pin, the run's Evidence ID, seat attribution marked textual/unsigned, the legs 7-8 custody defect where cited, and "not re-executed in luna-round-7"; `recheck:` carries live re-establishment; no "held/works/Core" or "independent" wording.
