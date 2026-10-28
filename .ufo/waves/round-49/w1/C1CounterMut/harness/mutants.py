# Mutation table for the DRAFT c1-counter.py. Each entry: id, description, edits.
# edits: list of (old, new, expected_count). CLAUSES drops are generated separately.
import re
M = []
def m(id_, desc, *edits):
    M.append((id_, desc, list(edits)))

m('M01-handler-any', 'handler_ok accepts a receipt if the frozen handler is ANY chunk handler (membership, not equality)',
  ("and d['squashfs_handlers'] == [handler])", "and handler in d['squashfs_handlers'])", 1))
m('M02-handler-true', 'handler_ok is constant True (handler binding ignored)',
  ("d['handler_ok'] = (isinstance(handler, str)", "d['handler_ok'] = (True or isinstance(handler, str)", 1))
m('M03-oracle-sha-ignored', 'oracle_hits ignores the sha256 of the published file (path+size only)',
  ("if fsha != sha or not same_rel(fp, rel, root):", "if not same_rel(fp, rel, root):", 1))
m('M04-oracle-size-ignored', 'oracle_hits ignores the census size',
  ("if want_size is not None and fsize != want_size:", "if False:", 1))
m('M05-root-naive-prefix', 'under_root uses a naive prefix test (x_extract owns x_extract2/...)',
  ("return p.startswith(root.rstrip('/') + '/')", "return p.startswith(root.rstrip('/'))", 1))
m('M06-projection-true', 'rerun projection comparison forced true (fabricated receipt passes projection_ok)',
  ("d['projection_ok'] = eq", "d['projection_ok'] = True", 1))
m('M07-rerun-skipped', 'counter never reruns REA; projection_ok forced true when the rerun is skipped',
  ("if raw is not None and d['carrier_pin_ok'] and not dev_arm:", "if False and not dev_arm:", 1),
  ("                else:\n                    d['projection_ok'] = False\n                    d['projection_skipped']",
   "                else:\n                    d['projection_ok'] = True\n                    d['projection_skipped']", 1))
m('M08-evidence-id-unchecked', 'evidence_id_ok ignores whether stored id equals recomputed id',
  ("d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]", "d['evidence_id_ok'] = (key in ev", 1))
m('M09-freeze-drift-off', 'frozen_path_changed never raises (drift reported but not enforced)',
  ("if drift:\n        raise FrozenPathChanged(drift)", "if False:\n        raise FrozenPathChanged(drift)", 1))
m('M10-freeze-prefixes-off', 'freeze walk ignores FROZEN_PREFIXES (tools/round-49/ directory and oracle tree)',
  ("    prefixes = FROZEN_PREFIXES\n", "    prefixes = ()\n", 1))
m('M11-freeze-A-ignored', 'freeze walk: a re-added frozen path (A) never counts as a change',
  ("                if existed_cache[path]:\n                    touched.add(path)", "                if False:\n                    touched.add(path)", 1))
m('M12-freeze-blob-backstop-off', 'freeze walk: no endpoint blob-equality backstop',
  ("        if a.stdout.strip() != b.stdout.strip():\n            touched.add(path)", "        if False:\n            touched.add(path)", 1))
m('M13-sourced-used-by-off', 'sourced: SOURCES used-by is not checked for the entry',
  ("and (ENTRY in used or STEM in used):", "and True:", 1))
m('M14-sourced-opened-off', 'sourced: SOURCES opened date is not checked',
  ("c[8] == OPENED and (ENTRY", "True and (ENTRY", 1))
m('M15-province-row-entry-off', 'province_core_row does not require the entry path cite',
  ("and ENTRY in r\n", "and True\n", 1))
m('M16-frontier-stem-off', 'frontier_note does not require the entry stem on the line',
  ("FRONTIER_MARK in l and STEM in l", "FRONTIER_MARK in l and True", 1))
m('M17-frontier-token-off', 'frontier_note does not require a SquashFS v1/v2 token',
  ("                             and SQFS12_TEXT_RE.search(l)\n", "                             and True\n", 1))
m('M18-core-row-v2-off', 'province_core_row does not require squashfs_v2 token',
  ("'squashfs_v1' in r and 'squashfs_v2' in r and SQFS12_TEXT_RE.search(r)", "'squashfs_v1' in r and SQFS12_TEXT_RE.search(r)", 1))
m('M19-coverage-map-off', 'coverage_map_row does not require the stem',
  ("STEM in l for l in cm if", "True for l in cm if", 1))
m('M20-entry-source-off', 'entry source ids are never collected (sourced always fails) -- sanity, expected killed',
  ("            if line.startswith('source:'):", "            if False:", 1))
m('M21-magic-check-off', 'layout_probe ignores the frozen-endianness magic check',
  ("    if not d['magic_ok']:\n        reason", "    if False:\n        reason", 1))
m('M22-s-minor-off', 'layout_probe ignores s_minor',
  ("    elif not d['s_minor_ok']:", "    elif False:", 1))
m('M23-s-major-off', 'layout_probe ignores s_major',
  ("    elif not d['s_major_ok']:", "    elif False:", 1))
m('M24-layout-handler-off', 'layout_probe ignores s_major-implied handler vs frozen handler',
  ("    elif not d['handler_ok']:", "    elif False:", 1))
m('M25-bytes-used-off', 'layout_probe does not check bytes_used against the file',
  ("d['bytes_used_sane'] = SB_SIZE <= bu <= len(raw)", "d['bytes_used_sane'] = True", 1))
m('M26-chain-witness-off', 'layout_probe does not check the metadata chain witness',
  ("and its + 2 + length == dts)", "and True)", 1))
m('M27-compression-off', 'layout_probe does not compare observed compression with the frozen class',
  ("    elif normalize_compression(expect.get('compression')) is not None and \\\n            d['compression'] != normalize_compression(expect.get('compression')):",
   "    elif False:", 1))
m('M28-carve-off', 'carve_ok is constant True (extra bytes past the chunk end accepted)',
  ("and d['layout'].get('size') == ce)", "and True)", 1))
m('M29-chunk-end-nopad', 'chunk_end ignores zero-padded rounding (always end of data)',
  ("    for pad_size in (4096, 1024):", "    for pad_size in ():", 1))
m('M30-tree-check-off', 'tree_ok is constant True (committed __output__ tree not compared)',
  ("    d['tree_ok'], d['tree_note'] = tree_check(root, rev, troot, tdigest,\n                                                     rows)",
   "    d['tree_ok'], d['tree_note'] = True, 'off'\n            _unused = (troot, tdigest,\n                                                     rows)", 1))
m('M31-receipt-fresh-add-only', 'receipt_fresh only requires a first add (no freeze ancestry check)',
  ("d['receipt_fresh'] = bool(add) and add != freeze \\\n                    and is_ancestor(root, freeze, add)", "d['receipt_fresh'] = bool(add) and add != freeze", 1))
m('M32-is-ancestor-off', 'receipt_fresh: ancestry of freeze never checked (is_ancestor always True)',
  ("    p = git(root, 'merge-base', '--is-ancestor', ancestor, descendant, check=False)\n    return p.returncode == 0",
   "    return True", 1))
m('M33-carrier-fresh-off', 'carrier_fresh_ok constant True',
  ("d['carrier_fresh_ok'] = pin is not None and pin not in prior", "d['carrier_fresh_ok'] = True", 1))
m('M34-envelope-counter-key-off', 'evidence_envelope_ok ignores exit_code key (score receipt with counter_sha256 only still checked, exit_code key not)',
  ("d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}\n                                                 & set(env))",
   "d['evidence_envelope_ok'] = not ({'counter_sha256'}\n                                                 & set(env))", 1))
m('M35-operation-off', 'operation_ok ignores operation name and provider',
  ("d['operation_ok'] = (env.get('operation') == 'extract_firmware'\n                         and isinstance(prov, dict) and prov.get('id') == 'unblob')",
   "d['operation_ok'] = True", 1))
m('M36-provenance-substring-only', 'provenance_ok: segment test is substring only; absolute/.. checks removed',
  ("    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):\n        return False\n    if PROV_SEGMENT not in output_directory:",
   "    if not isinstance(output_directory, str):\n        return False\n    if PROV_SEGMENT not in output_directory:", 1))
m('M37-target-ge', 'met_target uses carriers_matched >= 1 instead of == target',
  ("and res['carriers_matched'] == target", "and res['carriers_matched'] >= 1", 1))
m('M38-gap-structural-1', 'frozen gap rule: depth-limited allowance 1 instead of 0',
  ("'structural': {'depth-limited': 0, 'unknown-chunk-handler': 0},", "'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0},", 1))
m('M39-gaps-ok-true', 'gaps_ok is constant True (disposition check bypassed)',
  ("    d['gaps_ok'] = ok\n", "    d['gaps_ok'] = True\n", 1))
m('M40-nonreg-unpub-off', 'nonregular_unpublished_ok constant True',
  ("d['nonregular_unpublished_ok'] = root_value is not None and not esc", "d['nonregular_unpublished_ok'] = True", 1))
m('M41-shape-off', 'path_shape_ok constant True (trailing-slash/.. spellings accepted)',
  ("    d['path_shape_ok'] = shape_ok\n", "    d['path_shape_ok'] = True\n", 1))
m('M42-subject-off', 'subject_pin_ok constant True',
  ("d['subject_pin_ok'] = d['subject_sha256'] == pin", "d['subject_pin_ok'] = True", 1))
m('M43-chunks-off', 'chunks_ok constant True (extraction_failed chunks accepted)',
  ("d['chunks_ok'] = not chunk_failed(env)", "d['chunks_ok'] = True", 1))
m('M44-carrier-pin-off', 'carrier_pin_ok constant True (carrier bytes not hashed against the pin)',
  ("d['carrier_pin_ok'] = (raw is not None and pin is not None\n                                   and hashlib.sha256(raw).hexdigest() == pin)",
   "d['carrier_pin_ok'] = True", 1))
m('M45-carrier-size-off', 'carrier_size_ok constant True',
  ("d['carrier_size_ok'] = (raw is not None\n                                    and isinstance(c.get('size'), int)\n                                    and len(raw) == c.get('size'))",
   "d['carrier_size_ok'] = True", 1))
m('M46-sb-layout-sanity', 'layout_probe: starts_sane check removed', 
  ("d['starts_sane'] = bool(d['bytes_used_sane'] and SB_SIZE <= its < dts <= bu)", "d['starts_sane'] = True", 1))
m('M47-projection-profile-core', 'projection uses the core profile (plus-extractor keys dropped)',
  ("profile = spec.get('projection', DEFAULT_PROFILE)", "profile = 'core'", 1))
m('M48-counter-identity-off', 'receipt_identity_ok always True',
  ("def receipt_identity_ok(doc):", "def receipt_identity_ok(doc):\n    return True, 'off'\n\ndef _receipt_identity_ok_unused(doc):", 1))
m('M49-layout-ok-constant', 'layout_probe verdict constant True (superblock probe skipped)',
  ("    d['ok'] = reason is None\n", "    d['ok'] = True\n", 1))
m('M50-freeze-walk-empty', 'measure: frozen_drift walk returns [] (freeze walk dropped; FROZEN_PREFIXES irrelevant)',
  ("    drift = frozen_drift(root, freeze, rev, spec)\n", "    drift = []\n", 1))
m('M53-gap-kind-any', 'disposition_check accepts any gap kind on a non-regular entry',
  ("        if kind not in allowed.get(entry_kind, []):", "        if False:", 1))
m('M54-removal-not-exclusive', 'disposition_check allows an entry both gapped and removed',
  ("            if gapped.get(hits[0]):", "            if False:", 1))
m('M55-disposition-required-off', 'disposition_check never requires a disposition for a required non-regular entry',
  ("        if gapped.get(rel) or removed_rels.get(rel):\n            continue", "        continue", 1))
