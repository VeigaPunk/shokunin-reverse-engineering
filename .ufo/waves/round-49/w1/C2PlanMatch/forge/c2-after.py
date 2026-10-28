#!/usr/bin/env python3
"""Build the GREEN C2 fixture ("after" state) in a scratch clone made by mkclone.sh.
usage: c2-after.py <clone>   -> commits "dev after", prints DEV_AFTER=<hash>.
Derives every number from the clone's own committed bytes; writes the lesson corrections, rows
S147/S148, the two search-log entries and the SCORECARD correction section (dev fixture only)."""
import hashlib, os, re, shutil, subprocess, sys
D = sys.argv[1]
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SNAP = L + '/.ufo/waves/round-49/draft/snapshots'
git = lambda *a: subprocess.run(['git', '-C', D] + list(a), capture_output=True, text=True).stdout
assert git('rev-parse', '--show-toplevel').strip() == D
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(f'{D}/{p}', encoding='utf8').read()
def digs(p):
    x = subprocess.run(['git', '-C', D, 'show', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9:' + p], capture_output=True).stdout
    return sha(x), sha(x[:-1] if x.endswith(b'\n') else x)
os.makedirs(f'{D}/corpus/evidence/round-49/c2', exist_ok=True)
for f in ('popper.html', 'sysexits.html'):
    shutil.copy(f'{SNAP}/{f}', f'{D}/corpus/evidence/round-49/c2/{f}')
pop = sha(open(f'{SNAP}/popper.html', 'rb').read()); sx = sha(open(f'{SNAP}/sysexits.html', 'rb').read())
c1r, c1s = digs('.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json')
c2r, c2s = digs('.ufo/waves/round-48/l1/scores/c2-final-33f65a91.json')
les = f"""# Round 49 — lessons (dev fixture)

## Corrections to round 48

- A1 declared=b6f7ca2a6391964dfdedd477cd560bd42159873a stale=0f06251bf6a3a6964c715f67243d4df12e854258
- A2 dead=663f30ee7516942a0120e7de68fe88356e680822 actual=663f30ee751694fb0970e7de68fe88356e680822
- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a
- A4 seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers
- A5 c1_raw={c1r} c1_stripped={c1s} c2_raw={c2r} c2_stripped={c2s} report_c1={c1s[:8]} report_c2={c2s[:8]}
- A6 row=S147
- A7 row=S148
"""
os.makedirs(f'{D}/corpus/lessons', exist_ok=True)
open(f'{D}/corpus/lessons/round-49.md', 'w').write(les)
q1 = "falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific"
r47 = f"| S147 | Stanford Encyclopedia of Philosophy, Karl Popper — https://plato.stanford.edu/entries/popper/ | docs | A | The falsifiability criterion as the demarcation of an empirical check | `2. Backdrop to Popper’s Thought`; \"{q1}\" (21 words), accessed 2026-10-28, sha256 `{pop}` | supersedes S145 — S145 located the quote under §2 \"The Problem of Demarcation\"; the page puts it under §2 \"Backdrop to Popper’s Thought\", directly before §3. | mined | 2026-10-28 | 180d | corpus/lessons/round-49.md |"
q2 = "The command was used incorrectly, e.g., with the wrong number of arguments, a bad flag, bad syntax in a parameter, or whatever."
r48 = f"| S148 | sysexits.h(3head) Linux manual page — https://man7.org/linux/man-pages/man3/sysexits.h.3head.html | docs | A | BSD exit-code convention: the named EX_USAGE status | `DESCRIPTION`, EX_USAGE entry; \"{q2}\" (22 words), accessed 2026-10-28, sha256 `{sx}` | supersedes S146 — EX_USAGE is 64, not 2; the lane's 0/1/2 meanings are its own convention, not sysexits, and the reachable page is the `3head` section. | mined | 2026-10-28 | 180d | corpus/lessons/round-49.md |"
e48 = "- 2026-10-28 round 48 (late entry, written in round 49) — Question: which source grounds the falsifiability criterion for a check, and does sysexits ground exit 2? identified 2, screened 2, included 1, excluded 1; rows 144 → 146."
e49 = "- 2026-10-28 round 49 — Question: do the S145/S146 locators and rationale survive a re-open? identified 2, screened 2, included 2, excluded 0; rows 146 → 148."
rg = rd('corpus/SOURCES.md').split('\n')
i = max(k for k, x in enumerate(rg) if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', x))
rg[i + 1:i + 1] = [r47, r48]
rg = '\n'.join(rg).replace('\n## Leads (unopened)', '\n' + e48 + '\n' + e49 + '\n\n## Leads (unopened)', 1)
open(f'{D}/corpus/SOURCES.md', 'w').write(rg)
sc = rd('SCORECARD.md').rstrip('\n') + "\n\n## Record corrections — round 49\n\n- A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed\n"
open(f'{D}/SCORECARD.md', 'w').write(sc)
git('add', '-A'); git('commit', '-q', '-m', 'dev after')
print('DEV_AFTER=' + git('rev-parse', 'HEAD').strip())
