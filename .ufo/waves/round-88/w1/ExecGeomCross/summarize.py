#!/usr/bin/env python3
"""summarize.py - ExecGeomCross cross.json builder.

Consumes the per-carrier derive records produced by geomx.py and adds the
three discriminating measurements:
  * strict-contiguous reading of the geometry rule (no loader-resume step);
  * rule ablations (smallest-derived only, largest-total only);
  * the exact byte window the committed repair changes.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geomx  # noqa: E402  (own module, written from scratch for this seat)

S = os.environ.get("GEOMX_WORK") or os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.abspath(__file__))
NAMES = ["jq", "xxd", "libz.so.1.3.2", "docker-init"]


def strict_contiguous(d, ph_off, ph, lin):
    """The literal reading: the chain from b0 (patched) reaches the sentinel
    without any resume step, and the candidate's own run does too."""
    b0 = lin["b0"]
    sz_unc0, _ = struct.unpack_from("<II", d, b0)
    m0 = d[b0 + 8]
    methods = {m0, ph["method"]}
    out = []
    for s1 in range(b0 + 13, ph_off - 12):
        b = geomx.block_at(d, s1, ph_off, methods)
        if b is None:
            continue
        derived = s1 - (b0 + 12)
        if not 0 < derived <= sz_unc0:
            continue
        dd = bytearray(d)
        struct.pack_into("<I", dd, b0 + 4, derived)
        stop, _blocks = geomx.walk(bytes(dd), b0, ph_off, methods)
        if not geomx.is_sentinel(dd, stop, ph_off):
            continue
        e2, _b2 = geomx.walk(bytes(dd), s1, ph_off, methods)
        out.append({"derived": derived, "chain_from_b0_sentinel": True,
                    "chain_from_candidate_sentinel": geomx.is_sentinel(dd, e2, ph_off)})
    return out


def ablate(cands):
    """What each tie-break alone would pick."""
    if not cands:
        return {}
    return {
        "smallest_derived_only": min(cands, key=lambda c: c["derived"])["derived"],
        "largest_total_only": max(cands, key=lambda c: c["uncompressed_accounted"])["derived"],
        "fits_then_largest_then_smallest": sorted(
            cands, key=lambda c: (c["fits_u_len"], c["uncompressed_accounted"], -c["derived"]),
            reverse=True)[0]["derived"],
    }


def main() -> int:
    nb = json.load(open(os.path.join(S, "neighbourhood.json")))
    cv = json.load(open(os.path.join(S, "committed_validation.json")))
    seg = json.load(open(os.path.join(S, "segments.json")))
    td = json.load(open(os.path.join(S, "tampered_d.json")))
    ld = json.load(open(os.path.join(S, "losers_d.json")))
    recs, carriers = {}, []
    for n in NAMES:
        r = json.load(open(os.path.join(S, n + ".derive.json")))
        recs[n] = r
        work = os.path.join(S, "work", n)
        b0 = r["block0"]["off"]
        window = list(range(b0 + 4, b0 + 8))
        ph_off = r["packheader"]["offset"]
        ph = {"version": r["packheader"]["version"], "format": r["packheader"]["format"],
              "method": r["packheader"]["method"], "u_len": r["packheader"]["u_len"]}
        lin = {"b0": b0}
        try:
            tampered = open(os.path.join(work, n + ".tampered"), "rb").read()
            committed = open(os.path.join(work, n + ".committed"), "rb").read()
            diff = [i for i in range(len(tampered)) if tampered[i] != committed[i]]
            strict = strict_contiguous(tampered, ph_off, ph, lin)
        except FileNotFoundError:
            # archived evidence: the byte diff and the strict-reading count were
            # measured during the wave and are kept in diffs.json so cross.json
            # reproduces after scratch removal
            rec = json.load(open(os.path.join(S, "diffs.json")))[n]
            diff = rec["changed_byte_offsets"]
            strict = [{"archived": True}] * rec["strict_contiguous_candidates"]
        intact = r["block0"]["sz_cpr_intact"]
        derived = (r["geometry"]["chosen"] or {}).get("derived")
        carriers.append({
            "name": n, "carrier_path": r["carrier"], "orig_sha256": r["orig_sha256"],
            "packed_sha256": r["packed_sha256"], "packed_size": r["packed_size"],
            "packheader": {k: r["packheader"][k] for k in
                           ("offset", "version", "format", "method", "level",
                            "u_len", "c_len", "u_file_size")},
            "l_info": {"l_magic": r["l_info"]["l_magic"], "l_info": r["l_info"]["l_info"],
                       "b0": r["l_info"]["b0"], "l_lsize": r["l_info"]["l_lsize"],
                       "p_progid": r["l_info"]["p_progid"],
                       "p_filesize": r["l_info"]["p_filesize"],
                       "p_blocksize": r["l_info"]["p_blocksize"]},
            "locator_agreement": r["locator_agreement"],
            "block0": r["block0"],
            "intact_sz_cpr": intact, "derived_sz_cpr": derived,
            "derived_equals_intact": derived == intact,
            "committed_derived_sz_cpr": r["committed"].get("derived_sz_cpr"),
            "agreement": r["agreement"],
            "offsets_scanned": r["geometry"]["offsets_scanned"],
            "structural_candidates": r["geometry"]["structural_candidates"],
            "sentinel_reaching_candidates": r["geometry"]["sentinel_reaching_candidates"],
            "candidates": [{"derived": c["derived"], "next_block": c["next_block"],
                            "uncompressed_accounted": c["uncompressed_accounted"],
                            "fits_u_len": c["fits_u_len"],
                            "chain_from_candidate_alone_reaches_sentinel":
                                c["chain_from_candidate_alone_reaches_sentinel"],
                            "sentinel": c["sentinel"], "resume": c["resume"]}
                           for c in r["candidates"]],
            "ambiguity": r["ambiguity"],
            "upx_t_tampered": r["tampered_upx_t"],
            "winner": r["winner"],
            "committed": {k: r["committed"].get(k) for k in
                          ("exit", "class", "derived_sz_cpr", "output_sha256",
                           "output_byte_identical_to_packed")},
            "changed_byte_offsets_committed_vs_tampered": diff,
            "changed_bytes_inside_szcpr_window": all(i in window for i in diff),
            "sz_cpr_window": [window[0], window[-1]],
            "strict_contiguous_candidates": len(strict),
            "rule_ablations": ablate(r["candidates"]),
            "committed_validation": cv[n],
            "upx_t_neighbourhood": nb[n],
            "neighbourhood_unique": (sorted(int(v) for v, x in nb[n]["probes"].items()
                                            if x["exit"] == 0) == [int(nb[n]["true"])]),
        })
    summary = {
        "carriers": len(carriers),
        "derived": {c["name"]: c["derived_sz_cpr"] for c in carriers},
        "agreement_all": all(c["agreement"] for c in carriers),
        "derived_equals_intact_all": all(c["derived_equals_intact"] for c in carriers),
        "committed_byte_identical_all": all(
            c["committed"]["output_byte_identical_to_packed"] for c in carriers),
        "upx_t_restores_all": all(c["winner"].get("restored_matches_orig") for c in carriers),
        "upx_t_tampered_refused_all": all(c["upx_t_tampered"]["exit"] != 0 for c in carriers),
        "tampered_refusal_message_all_b_info_corrupted": all(
            any("b_info corrupted" in ln for ln in c["upx_t_tampered"]["stderr"])
            for c in carriers),
        "changed_window_only_all": all(c["changed_bytes_inside_szcpr_window"] for c in carriers),
        "strict_contiguous_candidates_total": sum(c["strict_contiguous_candidates"] for c in carriers),
        "extra_candidates_beyond_chosen": {
            c["name"]: [a for a in c["ambiguity"] if not a["chosen"]] for c in carriers},
        "extra_candidates_passing_upx_t": {
            c["name"]: [a["derived"] for a in c["ambiguity"] if not a["chosen"] and a["upx_t_exit"] == 0]
            for c in carriers},
        "rule_ablations": {c["name"]: c["rule_ablations"] for c in carriers},
        "committed_validated_all": all(
            c["committed_validation"].get("upx_t_exit") == 0
            and c["committed_validation"].get("upx_d_exit") == 0
            and c["committed_validation"].get("restored_matches_carrier") for c in carriers),
        "neighbourhood_unique_all": all(c["neighbourhood_unique"] for c in carriers),
        "tampered_upx_d_refused_all": all(td[n]["upx_d_exit"] != 0 for n in NAMES),
        "segment_geometry": seg,
        "tampered_upx_d": td,
        "losing_candidates_upx_d": ld,
        "losing_candidates_passing_upx_d": [v for v, r in ld.items() if r["upx_d_exit"] == 0],
    }
    out = {"seat": "ExecGeomCross", "round": 88, "claim": "R88-C1",
           "rule_under_test": ("sz_cpr0 = candidate - (b0+12) for the next plausible b_info "
                               "whose chain (with loader-resume) reaches the end-of-chain "
                               "sentinel, 0 < sz_cpr <= sz_unc; winner maximises "
                               "(fits_u_len, accounted total, -derived)"),
           "independence": ("geomx.py written from scratch for this seat; no import of "
                            "tools/round-88 or tools/round-87; anchors located by PackHeader "
                            "checksum and by the l_info magic word, cross-checked against the "
                            "u_file_size redundancy"),
           "pins": {"upx_sha256": "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969",
                    "upx_version": "upx 5.2.0",
                    "rea_pkgjson_sha256": "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c",
                    "r87_module_sha256": "96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24"},
           "summary": summary, "carriers_detail": carriers}
    p = os.path.join(OUT, "cross.json")
    json.dump(out, open(p, "w"), indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
