#!/usr/bin/env python3
"""How often does a seed draw a C02-shaped combo (the R42-CL1 predictor fault)?

Uses the FROZEN generator's own `combo_draw` / `combo_factors` / `combo_declared`
(imported by path, `-B` so no bytecode is written) so the numbers are the frozen
draw's numbers, not a re-implementation.

A "C02 shape" is a draw where:
  * the depth budget is 1 and nothing is wrapped in a container (no `capped`),
  * the body is a generated v4 image (`body_v4`), whose damage recipe zeroes a
    LATE data block, so the extractor publishes earlier files (`published`
    'nonzero' in `combo_declared`),
  * damage is effective (not shadowed by a dependency failure),
  * no residue tail and no sibling chunk,
and therefore the frozen `reached` clause (combo_declared:943) says the ceiling
was never reached, while REA was measured (round-42 C02) to mint
`depth-limited` on exactly this shape.

Usage: c02-shape-sim.py <heldout-gen-v4.py> <fixtures.json> [n_seeds]
"""
import hashlib
import importlib.util
import json
import sys


def load(path):
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('frozen_gen', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def is_c02_shape(f):
    capped = bool(f['wrap']) and f['max_depth'] == 1
    dep_eff = bool(f['dep']) and not capped
    dmg_eff = bool(f['damage']) and not dep_eff and not capped
    if capped or dep_eff or not dmg_eff or f['max_depth'] != 1:
        return False
    return not (bool(f['residue']) or bool(f['two_chunk']))


def main(argv):
    gen_path = argv[1]
    pins_path = argv[2]
    n = int(argv[3]) if len(argv) > 3 else 500
    g = load(gen_path)
    pins = g.load_fixture_pins(pins_path)
    seeds_with, draws, per_seed, example = 0, 0, [], None
    for index in range(n):
        seed = hashlib.sha256(f'probe{index}'.encode()).hexdigest()[:40]
        count = 0
        for k in range(1, g.FAMILIES['combo'] + 1):
            _rng, factors = g.combo_draw(seed, k, pins)
            if is_c02_shape(factors):
                count += 1
                if example is None:
                    example = (seed, k, factors)
        per_seed.append(count)
        seeds_with += count > 0
        draws += count
    print(json.dumps({
        'seeds': n,
        'seeds_with_at_least_one_c02_shape': seeds_with,
        'rate': round(seeds_with / n, 4),
        'c02_shapes_per_24_combos': round(draws / n, 4),
        'max_per_seed': max(per_seed),
    }, indent=1))
    if example:
        seed, k, factors = example
        kept = {key: factors[key] for key in
                ('base', 'second_v4', 'links', 'residue', 'wrap', 'damage',
                 'dep', 'max_depth', 'body_v4')}
        print(f'example: seed {seed} combo C{k:02d} factors {json.dumps(kept, sort_keys=True)}')
        print('  frozen combo_declared -> '
              + json.dumps(g.combo_declared(factors), sort_keys=True))
        print('  observed on the round-42 C02 carrier -> '
              + '{"be_argv":"yes","gap_dependencies":[],'
                '"gap_kinds":["depth-limited","extractor-failure","unpublished-entry"],'
                '"handler_set":["squashfs_v4_be"],"published":"nonzero",'
                '"symlink_removed":false}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
