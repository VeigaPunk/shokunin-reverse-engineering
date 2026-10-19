#!/usr/bin/env python3
"""EX-19 prototype: needle-liveness + floors applied to the pre-landing instrument.
Generates a patched scratch copy (never the real gate) and reports success."""
import sys
src = open('/var/tmp/ex19/instrument/pre-landing-v10.py', encoding='utf-8').read()
OLD_G2 = '    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)'
NEW_G2 = ('    total_loci = sum(c["loci"] for c in counts.values())\n'
          '    needles_live = [bool(p.search(s)) for p, s in\n'
          '                    ((PIN, "rea-agents@6.7.0"), (VER, "6.5.0"),\n'
          '                     (PTR, "~/.kimi-code/config.toml:1478"))]\n'
          '    g2_ok = len(out.get("current-ok", [])) > 0 and total_loci > 0 and all(needles_live)')
OLD_P = '    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))'
NEW_P = ('    print("G2 positive-assertion guard: %s (current-ok=%d total-loci=%d needles=%s)" %\n'
         '          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])), total_loci, needles_live))')
for old, new in ((OLD_G2, NEW_G2), (OLD_P, NEW_P)):
    assert src.count(old) == 1, old
    src = src.replace(old, new)
open('/var/tmp/ex19/instrument/proto-p1.py', 'w', encoding='utf-8').write(src)
print('wrote proto-p1.py')
