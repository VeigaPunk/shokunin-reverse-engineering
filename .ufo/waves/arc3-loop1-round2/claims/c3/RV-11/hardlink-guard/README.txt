== write-guard evasion via hardlink (scratch-only proof) ==
guard: cmd_capture refuses --out when out.resolve() is one of the 5 custody paths (custody-pair.py:565 of 112d01dc)
setup: printf 'scratch custody bytes' > guarded.conf; ln guarded.conf alias.out
before: sha256(guarded.conf)=8af5b1d57c249f39...
run:    python3 custody-pair.py capture --out alias.out --paths guarded.conf --label hardlink-probe
result: exit=0 — no refusal; alias.out shares the inode with guarded.conf, so the receipt was written THROUGH the path guard
after:  sha256(guarded.conf)=3fc32a0a432dbc30... ; file now begins '# custody-pair receipt v2 ...'
