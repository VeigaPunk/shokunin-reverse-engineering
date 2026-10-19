import hashlib
import json
from pathlib import Path

R = Path.cwd()


def file_bytes(path):
    return (R / path).read_bytes()


def decoded_hex(path):
    raw = file_bytes(path)
    text = raw.decode("ascii").strip().removeprefix("0x")
    return raw, bytes.fromhex("".join(text.split()))


def report_file(path, encoding="raw"):
    raw = file_bytes(path)
    value = bytes.fromhex(raw.decode("ascii").strip().removeprefix("0x")) if encoding == "hex" else raw
    print(f"FILE {path}: file_bytes={len(raw)} file_sha256={hashlib.sha256(raw).hexdigest()} decoded_bytes={len(value)} decoded_sha256={hashlib.sha256(value).hexdigest()}")
    return value


SOURCES = [
    ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol",
    ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/Rv2Many.sol",
    ".ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/KdxToken.sol",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/VaultB.sol",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/carrierB.sol",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/src/CarrierB.sol",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/src/attack/CarrierBErr.sol",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/src/CarrierV.vy",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-09/vyper/Ex09Vault.vy",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-03/token.vy",
    ".ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/src/CarrierW.vy",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/Smoke.vy",
]
print("SOURCE-IDENTITIES")
for path in SOURCES:
    raw = file_bytes(path)
    print(f"{path}: bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")

print("ABI-IDENTITIES")
for path in [
    ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.abi.json",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.abi.json",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.abi-opt200.json",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.abi.json",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.abi.json",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/abi.json",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-03/abi.json",
]:
    raw = file_bytes(path)
    print(f"{path}: bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")

print("KDX-HEX-RECONSTRUCTION")
kdx = file_bytes(".ufo/waves/arc3-loop1-round1/claims/c1/EX-07/target-KdxToken.runtime.bin")
kdx_hex = kdx.hex().encode("ascii") + b"\n"
print(f"runtime_bytes={len(kdx)} runtime_sha256={hashlib.sha256(kdx).hexdigest()} reconstructed_hex_file_bytes={len(kdx_hex)} reconstructed_hex_sha256={hashlib.sha256(kdx_hex).hexdigest()}")
kdx_hex_actual = file_bytes(".ufo/waves/arc3-loop1-round1/claims/c1/EX-07/target-KdxToken.runtime.hex")
print(f"actual_hex_file_bytes={len(kdx_hex_actual)} actual_hex_file_sha256={hashlib.sha256(kdx_hex_actual).hexdigest()} exact-reconstruction-match={kdx_hex_actual == kdx_hex}")

print("CREATION-DIGEST-DOMAINS")
creation_cases = [
    ("r1-Rv2Token", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.creation.hex", "hex", ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.bin"),
    ("r1-Smoke", ".ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/out/Smoke_sol_Smoke.bin", "hex", None),
    ("r3-VaultB-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.creation.bin", "raw", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.bin"),
    ("r3-carrierB-opt", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.creation-opt200.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.bin"),
    ("r3-CarrierB", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.creation.hex", "hex", ".ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.bin"),
    ("r4-CarrierV", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/creation.bin", "raw", ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin"),
]
for label, creation_path, encoding, runtime_path in creation_cases:
    c = report_file(creation_path, encoding)
    if runtime_path:
        runtime = report_file(runtime_path)
        print(f"EMBED {label}: exact-runtime-occurrences={c.count(runtime)}")

print("R3-RV2OPT-METADATA")
p = ".ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.4.0.json"
d = json.loads(file_bytes(p))
b = bytes.fromhex(d["normalized_result"]["bytecode"]["hex"])
end = d["raw_result"]["metadata"]["bytecodeOffset"]
code = b[:end]
selectors = {x["selector"].removeprefix("0x").lower() for x in d["normalized_result"]["functions"]}
push4 = []
pc = 0
while pc < len(code):
    op = code[pc]
    if op == 0x63 and pc + 5 <= len(code):
        push4.append((pc, code[pc + 1:pc + 5].hex()))
    pc += 1 + (op - 0x5f if 0x60 <= op <= 0x7f else 0)
needle = bytes.fromhex("43000825")
print(f"bytecode-bytes={len(b)} code-end={end} code-PUSH4-ops={len(push4)} code-selector-PUSH4={sum(v in selectors for _, v in push4)} trailer-43000825-offset={b.find(needle)} trailer-solc-marker-offset={b.find(bytes.fromhex('736f6c63'))} trailer-has-43000825={needle in b[end:]}")

print("R3-CARRIERA-OFFSETS")
p = ".ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/probe-carrierA-hex-6.4.0-rerun.json"
d = json.loads(file_bytes(p))
b = bytes.fromhex(d["normalized_result"]["bytecode"]["hex"])
instructions = []
pc = 0
while pc < len(b):
    op = b[pc]
    width = op - 0x5f if 0x60 <= op <= 0x7f else 0
    imm = b[pc + 1:pc + 1 + width]
    instructions.append((pc, op, imm))
    pc += 1 + width
branch_targets = [imm[0] for i, (_, op, imm) in enumerate(instructions[:-1])
                  if op == 0x60 and instructions[i + 1][1] == 0x57]
jumpdests = [pc for pc, op, _ in instructions if op == 0x5b]
for f in d["normalized_result"]["functions"]:
    off = f["bytecode_offset"]
    print(f"selector={f['selector']} reported={off} opcode-at-reported={b[off]:02x} reported-is-JUMPDEST={off in jumpdests} matches-PUSH1-JUMPI-immediate={off in branch_targets}")
print(f"PUSH1-JUMPI-immediates={branch_targets} actual-JUMPDEST-PCs={jumpdests}")

print("NO-CORE-ENVELOPES")
for p in [
    ".ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json",
    ".ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-hex-6.4.0.json",
    ".ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json",
]:
    d = json.loads(file_bytes(p))
    n = d["normalized_result"]
    print(f"{p}: confidence={d.get('confidence')} authority={d.get('authority')} runtime_execution={n.get('runtime_execution')} discovery_completeness={n.get('discovery_completeness')}")
