#!/usr/bin/env python3
"""Insert a candidate queue-drain rule text after rule #13 in a scratch SKILL.md."""
import pathlib, sys
tree, rulefile = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
rule = rulefile.read_text()
if not rule.endswith('\n'):
    rule += '\n'
p = tree/'SKILL.md'
lines = p.read_text().splitlines(keepends=True)
start = next(i for i, l in enumerate(lines) if l.startswith('## Queue-drain craft'))
end = next(i for i in range(start+1, len(lines)) if lines[i].startswith('## '))
# last non-blank line before end = rule #13's last line
last = max(i for i in range(start, end) if lines[i].strip())
new = lines[:last+1] + ['\n'] + [rule] + lines[last+1:]
p.write_text(''.join(new))
print(f'inserted after line {last+1} (section {start+1}-{end})')
