# Scratch-only mutation harness for the S152 row: writes variants of the scratch clone registry.
import sys
base = open(sys.argv[1], encoding='utf-8').read().split('\n')
idx = [i for i, l in enumerate(base) if l.startswith('| S152 ')]
assert len(idx) == 1, idx
i = idx[0]
variants = {
  'variant-a': lambda l: l.replace('| supersedes S147 — tier A to B', '| tier A to B'),
  'variant-b': lambda l: l.replace('corpus/lessons/round-49-verifier-spotcheck.md |', 'corpus/lessons/no-such-lesson.md |'),
  'variant-c': lambda l: l.replace('| B | Popper', '| C | Popper'),
}
for name, f in variants.items():
    out = list(base); out[i] = f(base[i])
    assert out[i] != base[i], name
    open(sys.argv[2] + '/' + name + '.md', 'w', encoding='utf-8').write('\n'.join(out))
    print(name, 'written', out[i].count('|'), 'pipes')
