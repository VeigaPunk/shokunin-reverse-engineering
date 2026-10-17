## CLAIM
At pinned HEAD `6e2ee8f`, all ten canonical receipts are present and hash-valid; all ten predictions match (10/10 ≥ 9). L9 counts only if all six names are absent. Command A/token controls reproduce. Config hashes match the prior sentinel, but round-interval zero drift lacks a before/after pair.

## METHOD
Read `P0.md:7-21`, receipts 1–10, `leg-2-tools.txt`, and `SE2.md:5-16`. A read-only Python census checked canonical inventory (excluding RV3 replays), receipt/stdout hashes, JSON-RPC results, tool-name order and L9 proof. Hash snapshots one second apart matched. Ran Command A/token extraction at frozen HEAD and `git diff --quiet`; no probe or config edit.

## FINDINGS
All stdout hashes recompute. L1 exact `6.4.0`; L2 has 170 unique names in JSON-RPC order; L3–L8 each return `-32602`, `Tool <name> not found`; L9 six fixed-string checks are absent/exit 1; L10 returns jq-bound `inspect_binary_layout` evidence (`receipts/leg-10.md:7-25`). N/10=10/10. Command A: 78/78, 9/9, no missing/dangling, scores 10.0; token set equals 78 file stems, SHA-256 `c6c025f3aee5fb93966f9da4eca22ade1ac3af9207d9ad26b8bca6807f6ae83b`; tracked diff clean. `SE2.md:9-13` reports four hashes matching the established sentinel; mtimes predate L1.

Receipt SHA-256: L1 `af959f64e22a37fd7a5ba369009fd689b65fe51a77f3b23f986d5082ecb0bfcd`; L2 `f298e8f1e94574491e975bce94f2445f9c7dce0cfbe980acf8c0e844f8a7fef1`; L3 `1be7e4f92c9de9c76edb156addee15114ebc3cd04abce4505ffa0ac877e33e1b`; L4 `aa4aa7a3a8bd651596dac73c5e688aaa965091414a3ada3b85bc3b59dae4721f`; L5 `3de61417614f30a5ae37356bf450a4707dfefb8c8d7af26b13f0b4f68f5031e2`; L6 `fa6efe333c54a48ae4c0768afecffa3d4440c34b3a844df714419868a1ff1621`; L7 `c10466b7dfcfea177f43431c5b1d61395e7b322173063175fb6d9ba1ed2eaa0b`; L8 `a1cc891be45ca7da4d9903bc6b6823048a1bcb1310bba8edf0577f90c812cbb3`; L9 `8377d652b298fcce80701d338797333cda86a1d7d02478481bd84e038537c2ee`; L10 `c89eea7a368c780ffe4ab6026e883300fa9f612484b1cf79ac75871cebd32d7b`.

Final hash command (repo root):
`python3 -B -c 'from pathlib import Path;import hashlib,re;d=Path(".ufo/waves/luna-round-8/receipts");p=[d/f"leg-{i}.md" for i in range(1,11)];assert {x.name for x in d.glob("leg-*.md") if re.fullmatch(r"leg-\d+\.md",x.name)}=={x.name for x in p} and all(x.is_file() and not x.is_symlink() and x.stat().st_size for x in p);print(*[f"{x.name} {hashlib.sha256(x.read_bytes()).hexdigest()}" for x in p],sep="\n")'`

## THREATS
`SE2.md:16` notes no round-8 pre-L1 capture; current hashes match older sentinels, not a true pair. Hashes do not prove execution (`CA1.md:8-11`). MCP protocol differs across L2 and L3–L5 (`RE3.md:12`). No durable pre-dispatch digest (`CA8.md:8-11`).

## VERDICT
FINDING: 10/10 predictions and frozen-source controls match; strict zero config drift across the battery remains unproven without round-8 pre/post hashes.
