import hashlib
import json
import re
from pathlib import Path

R = Path.cwd()


def read_json(path):
    return json.loads((R / path).read_text())


def decode_asset(path, encoding):
    raw = (R / path).read_bytes()
    if encoding == "hex":
        text = raw.decode("ascii").strip()
        if text.startswith("0x"):
            text = text[2:]
        decoded = bytes.fromhex("".join(text.split()))
    else:
        decoded = raw
    return raw, decoded


def selectors_in(obj):
    found = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in {"selector", "selectors", "planted_selectors"}:
                if isinstance(value, str) and re.fullmatch(r"(?:0x)?[0-9a-fA-F]{8}", value):
                    found.add(value.removeprefix("0x").lower())
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and re.fullmatch(r"(?:0x)?[0-9a-fA-F]{8}", item):
                            found.add(item.removeprefix("0x").lower())
                elif isinstance(value, dict):
                    for item in value.values():
                        if isinstance(item, str) and re.fullmatch(r"(?:0x)?[0-9a-fA-F]{8}", item):
                            found.add(item.removeprefix("0x").lower())
            found |= selectors_in(value)
    elif isinstance(obj, list):
        for value in obj:
            found |= selectors_in(value)
    return found


def expected_selectors(path):
    p = R / path
    if p.suffix == ".txt":
        return {m.group(1).lower() for m in re.finditer(r"(?m)^\s*(?:0x)?([0-9a-fA-F]{8})\b", p.read_text())}
    data = json.loads(p.read_text())
    if isinstance(data.get("planted_selectors"), dict):
        return {x.lower() for x in data["planted_selectors"].values()}
    if isinstance(data.get("selectors"), list):
        return {x.removeprefix("0x").lower() for x in data["selectors"]}
    if isinstance(data.get("selectors"), dict):
        return {x.removeprefix("0x").lower() for x in data["selectors"].values()}
    if isinstance(data.get("entries"), list):
        return {x["selector"].removeprefix("0x").lower() for x in data["entries"] if isinstance(x, dict) and isinstance(x.get("selector"), str)}
    return selectors_in(data)


def ops(data, end=None):
    end = len(data) if end is None else min(end, len(data))
    pc = 0
    out = []
    while pc < end:
        start = pc
        opcode = data[pc]
        pc += 1
        imm = b""
        if 0x60 <= opcode <= 0x7f:
            width = opcode - 0x5f
            imm = data[pc:min(pc + width, end)]
            pc += width
        out.append((start, opcode, imm))
    return out


def probe(label, probe_path, asset_path=None, encoding=None, expected_path=None):
    d = read_json(probe_path)
    n = d["normalized_result"]
    funcs = n["functions"]
    sels = [f["selector"].removeprefix("0x").lower() for f in funcs]
    code = bytes.fromhex(n["bytecode"]["hex"])
    code_sha = hashlib.sha256(code).hexdigest()
    rawmeta = d.get("raw_result", {}).get("metadata", {})
    end = rawmeta.get("bytecodeOffset")
    decoded = ops(code, end)
    push4 = [(pc, imm.hex(), decoded[i + 1][1] if i + 1 < len(decoded) else None)
             for i, (pc, op, imm) in enumerate(decoded) if op == 0x63]
    jumps = {pc for pc, op, _ in decoded if op == 0x5b}
    offsets_ok = None
    if funcs and all("bytecode_offset" in f for f in funcs):
        offsets_ok = sum(f["bytecode_offset"] in jumps for f in funcs)
    selector_sites = {sel: [pc for pc, val, _ in push4 if val == sel] for sel in set(sels)}
    shape = "" 
    if label.startswith("r4-"):
        xor_sites = sum(1 for i, (pc, op, imm) in enumerate(decoded)
                        if op == 0x63 and i + 4 < len(decoded)
                        and [decoded[i + 1][1], decoded[i + 2][1], decoded[i + 3][1], decoded[i + 4][1]] == [0x81, 0x18, 0x61, 0x57])
        shape = f"xor-chain-sites={xor_sites} offset-rule={sum(f.get('bytecode_offset') == selector_sites.get(f['selector'].removeprefix('0x').lower(), [-100])[0] + 11 for f in funcs if selector_sites.get(f['selector'].removeprefix('0x').lower()))}/{len(funcs)}"
    elif label.startswith("r3-"):
        gt = sum(1 for _, _, following in push4 if following == 0x11)
        eq = sum(1 for _, _, following in push4 if following == 0x14)
        shape = f"push4={len(push4)} GT={gt} EQ={eq}"
    elif label.startswith("r1-"):
        eq = sum(1 for _, _, following in push4 if following == 0x14)
        shape = f"push4={len(push4)} EQ={eq}"
    eq = "n/a"
    if expected_path:
        exp = expected_selectors(expected_path)
        eq = str(set(sels) == exp and len(sels) == len(exp))
    print(f"PROBE {label}: functions={len(funcs)} unique={len(set(sels))} dispatch={dict(sorted({x:sum(1 for f in funcs if f.get('dispatch') == x) for x in {f.get('dispatch') for f in funcs}}.items()))} planted-set-equal={eq} decoded-bytes={len(code)} decoded-sha256={code_sha} probe-sha-match={code_sha == n['bytecode']['sha256']} offsets-JUMPDEST={offsets_ok}/{len(funcs) if offsets_ok is not None else 'n/a'} {shape}")
    if asset_path:
        encoding = d.get("parameters", {}).get("encoding", encoding)
        raw, actual = decode_asset(asset_path, encoding)
        input_sha = hashlib.sha256(raw).hexdigest()
        actual_sha = hashlib.sha256(actual).hexdigest()
        print(f"ASSET {label}: {asset_path} encoding={encoding} file-bytes={len(raw)} file-sha256={input_sha} decoded-bytes={len(actual)} decoded-sha256={actual_sha} input-sha-match={input_sha == n['artifact']['sha256']} decoded-match={actual == code}")
    return d, code, decoded, jumps, push4


CASES = [
    ("r1-rv2-hex64", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt"),
    ("r1-rv2-raw64", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-raw-6.4.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.bin", "raw", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt"),
    ("r1-rv2-hex67", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.7.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt"),
    ("r1-many", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/probe-many.json", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/Rv2Many.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/expected-many.txt"),
    ("r1-kdx-hex67", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-hex-6.7.0.json", None, None, ".ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/planted-K.json"),
    ("r1-kdx-raw67", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-raw-6.7.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-07/target-KdxToken.runtime.bin", "raw", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/planted-K.json"),
    ("r1-smoke-creation", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-EX02-smoke-bin-6.4.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/out/Smoke_sol_Smoke.bin", "raw", None),
    ("r1-rv2-creation", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.creation.hex", "hex", None),
    ("r3-vault-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/planted-K.json"),
    ("r3-vault-nopt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-nopt-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.nopt.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/planted-K.json"),
    ("r3-carrierb-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-opt200-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/planted-B-opt200.json"),
    ("r3-carrierb-noopt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-noopt-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-noopt.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/planted-B-noopt.json"),
    ("r3-carrierB", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/probe/probe-runtime-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/planted-K.json"),
    ("r3-carrierB-error", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/attack/probe-runtime-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/attack/out/CarrierBErr.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/planted-K.json"),
    ("r3-rv2opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.planted-K.json"),
    ("r3-carrierA-control", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/probe-carrierA-hex-6.4.0-rerun.json", ".ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/carrier-A.hex", "hex", None),
    ("r4-carrierV", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex", "hex", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json"),
    ("r4-ex09", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-hex-6.4.0.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-09/vyper/Ex09Vault.runtime.hex", "hex", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-09/planted/planted-K.json"),
    ("r4-steward", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/EX03-6.4.0-hex.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-03/runtime.hex", "hex", None),
    ("r4-carrierW", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/CarrierW-6.4.0-hex.json", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.runtime.hex", "hex", None),
    ("r4-smoke", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/Smoke-6.4.0-hex.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/Smoke.runtime.hex", "hex", None),
]

RESULTS = {}
for case in CASES:
    RESULTS[case[0]] = probe(*case)

print("DISPATCH-DETAILS")
for label in ("r1-rv2-hex64", "r3-vault-opt", "r3-vault-nopt", "r3-carrierb-opt", "r3-carrierb-noopt", "r3-carrierB", "r3-rv2opt", "r3-carrierA-control", "r4-carrierV", "r4-ex09"):
    d, code, decoded, jumps, push4 = RESULTS[label]
    if label.startswith("r1-") or label.startswith("r3-"):
        branch_ops = {"GT": sum(op == 0x11 for _, _, op in push4), "EQ": sum(op == 0x14 for _, _, op in push4)}
        print(f"{label}: prologue={code[:20].hex()} raw-PUSH4={len(push4)} branch-ops={branch_ops}")
    else:
        offsets = [f.get("bytecode_offset") for f in d["normalized_result"]["functions"]]
        print(f"{label}: prologue={code[:20].hex()} XOR-shape={sum(1 for i,(pc,op,imm) in enumerate(decoded) if op == 0x63 and i+4 < len(decoded) and [decoded[i+j][1] for j in range(1,5)] == [0x81,0x18,0x61,0x57])} offsets={len(offsets)} push4-plus-11={sum(off == next((pc+11 for pc,val,_ in push4 if val == f['selector'].removeprefix('0x').lower()), -1) for f,off in zip(d['normalized_result']['functions'],offsets))} offset-minus-12-JUMPDEST={sum(off-12 in jumps for off in offsets)} offset-JUMPDEST={sum(off in jumps for off in offsets)}")

print("RV2TOKEN-ERRATUM")
d, code, decoded, jumps, push4 = RESULTS["r1-rv2-hex64"]
meta = d.get("raw_result", {}).get("metadata", {})
end = meta.get("bytecodeOffset", len(code))
selectors = [f["selector"].removeprefix("0x").lower() for f in d["normalized_result"]["functions"]]
print(f"metadata-code-end={end} trailer-len={len(code)-end} trailer-has-16ee4b79={code.find(bytes.fromhex('16ee4b79'))} code-PUSH4-eq={sum(1 for pc,imm,nxt in push4 if imm in selectors and nxt == 0x14)}")
creation = bytes.fromhex(read_json(".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json")["normalized_result"]["bytecode"]["hex"])
print(f"creation-bytes={len(creation)} embedded-runtime-occurrences={creation.count(code)} embedded-runtime-bytes={len(code)}")

print("CREATION-EMBED-CHECKS")
for label, path in [
    ("r3-vault-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.creation.bin"),
    ("r3-vault-nopt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.nopt.creation.bin"),
    ("r3-carrierb-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.creation-opt200.hex"),
    ("r3-carrierb-noopt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.creation-noopt.hex"),
    ("r3-carrierB", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.creation.hex"),
]:
    _, runtime, _, _, _ = RESULTS[label]
    raw = (R / path).read_bytes()
    blob = raw if path.endswith(".bin") else bytes.fromhex(raw.decode("ascii").strip().removeprefix("0x"))
    occurrences = blob.count(runtime)
    print(f"{label}: creation-bytes={len(blob)} runtime-bytes={len(runtime)} embedded-runtime-occurrences={occurrences}")

print("VYPER-ABI-SET-CHECKS")
for label, abi_path, ids_path in [
    ("r4-carrierV", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/abi.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/method-identifiers.json"),
    ("r4-steward", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-03/abi.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-03/method-identifiers.json"),
    ("r4-carrierW", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.abi.json", ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.method-identifiers.json"),
    ("r4-smoke", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/Smoke.abi.json", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/method-identifiers.txt"),
]:
    abi = read_json(abi_path)
    method_ids = json.loads((R / ids_path).read_text())
    signatures = {item["name"] + "(" + ",".join(arg["type"] for arg in item.get("inputs", [])) + ")"
                  for item in abi if item.get("type") == "function"}
    expected = {method_ids[sig].removeprefix("0x").lower().zfill(8) for sig in signatures if sig in method_ids}
    observed = {f["selector"].removeprefix("0x").lower().zfill(8) for f in RESULTS[label][0]["normalized_result"]["functions"]}
    nonfunctions = sorted(set(method_ids) - signatures)
    print(f"{label}: ABI-functions={len(signatures)} method-id-keys={len(method_ids)} nonfunction-keys={nonfunctions} probe-functions={len(observed)} set-equal={observed == expected}")

print("GHIDRA-LIST-CHECK")
ghidra = (R / "corpus/knowledge/2026-10-13-ghidra-install.md").read_text()
module_line = next(line for line in ghidra.splitlines() if "contains 35 modules:" in line)
module_names = module_line.split("contains 35 modules: ", 1)[1].split(". x86 ships", 1)[0].split(",")
print(f"candidate-list-names={len(module_names)} unique={len(set(x.strip() for x in module_names))} candidate-line-count=35 round2-erratum=34 arc3-erratum=34 live-directory=not-rechecked-outside-repo")

