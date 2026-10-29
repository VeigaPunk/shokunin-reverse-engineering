#!/usr/bin/env python3
"""Offline check of the DRAFTED PROVINCE.md bindings against the FROZEN counter's
documentation-binding predicates.

This seat runs no REA and no counter scoring: it imports the byte-frozen counter
(`tools/round-50/c1-counter.py`) only to reuse its exact constants and helper
functions (`section`, `cells`, `HANDLER_RE`, `AVM_MARKER_RE`, `LE_AVM_RE`, `ENTRY`,
`STEM`, `CORE_HEADING`, `FRONTIER_MARK`), then applies the same predicates the
counter applies to `PROVINCE.md` at `c1-counter.py:2440-2482` to the DRAFT text.

Usage: python3 -I -B check-bindings.py <draft.md> <lane-root>
Exit: 0 all drafted bindings hold, 1 at least one fails.
"""
import hashlib
import importlib.util
import json
import os
import sys


def load_counter(lane):
    path = os.path.join(lane, 'tools', 'round-50', 'c1-counter.py')
    spec = importlib.util.spec_from_file_location('r50c1counter', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # module body only; main() is __main__-guarded
    return mod, path


def draft_block(text):
    """The first fenced ```markdown ... ``` block of the draft file."""
    out, inside = [], False
    for line in text.splitlines():
        if not inside and line.strip() == '```markdown':
            inside = True
            continue
        if inside and line.strip() == '```':
            break
        if inside:
            out.append(line)
    return '\n'.join(out)


def bindings(mod, prov_text, readme_text):
    sec = mod.section(prov_text, mod.CORE_HEADING)
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b = {}
    b['province_core_section'] = sec is not None
    b['province_core_row'] = any(
        mod.HANDLER_RE.search(mod.cells(r)[0])
        and mod.AVM_MARKER_RE.search(r.replace(mod.ENTRY, ''))
        and mod.ENTRY in r
        for r in rows)
    b['frontier_note'] = any(mod.FRONTIER_MARK in l and mod.STEM in l
                             and mod.LE_AVM_RE.search(l.replace(mod.STEM, ''))
                             for l in prov_text.splitlines())
    cm = mod.section(readme_text, '## Coverage map') if readme_text else None
    b['coverage_map_row'] = bool(cm) and any(
        mod.STEM in l for l in cm if l.lstrip().startswith('|'))
    return b


def main(argv):
    draft_path, lane = argv[1], argv[2]
    mod, counter_path = load_counter(lane)
    draft = open(draft_path, encoding='utf-8').read()
    block = draft_block(draft)
    readme = ('# R\n\n## Coverage map\n\n| section | entries | state |\n|---|---|---|\n'
              '| SquashFS LE-AVM (`hsqs`) v4 through REA `extract-firmware` | '
              '`2026-10-28-r50-avm-le-squashfs-core` | **Core** — four carriers |\n\n'
              '## Other\n')
    got = bindings(mod, block, readme)

    # Variant B: the attempt-2 declaration's stem, applied to the same draft text.
    v2 = block.replace(mod.ENTRY, 'corpus/knowledge/2026-10-29-r50-le-avm-hsqs-core.md')
    v2 = v2.replace(mod.STEM, '2026-10-29-r50-le-avm-hsqs-core')
    readme_v2 = readme.replace(mod.STEM, '2026-10-29-r50-le-avm-hsqs-core')
    got_v2 = bindings(mod, v2, readme_v2)

    out = {
        'counter_path': counter_path,
        'counter_sha256': hashlib.sha256(open(counter_path, 'rb').read()).hexdigest(),
        'counter_entry_constant': mod.ENTRY,
        'counter_stem_constant': mod.STEM,
        'draft_sha256': hashlib.sha256(open(draft_path, 'rb').read()).hexdigest(),
        'draft_block_lines': len(block.splitlines()),
        'note_is_one_line': sum(1 for l in block.splitlines()
                                if mod.FRONTIER_MARK in l) == 1,
        'draft_bindings': got,
        'variant_b_attempt2_stem_bindings': got_v2,
        'variant_b_note_is_one_line': sum(1 for l in v2.splitlines()
                                          if mod.FRONTIER_MARK in l) == 1,
    }
    ok = all(got[k] for k in ('province_core_section', 'province_core_row',
                              'frontier_note', 'coverage_map_row')) and out['note_is_one_line']
    out['verdict'] = 'ok' if ok else 'FAILED'
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
