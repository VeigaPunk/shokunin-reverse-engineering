#!/usr/bin/env python3
"""Round 29 R29-C1 producer: write and compile fresh EVM carriers (not a counter).

Each carrier is one Solidity contract holding a published interface's function list (ERC-20 with
EIP-2612, ERC-721, ERC-1155, ERC-4626, Ownable/AccessControl/Pausable, Uniswap V2 pair, router and
factory, WETH9, Multicall3 block getters, Chainlink aggregator, OpenZeppelin TimelockController,
Compound GovernorBravo, Safe owner manager, ENS registry, ERC-2981 and NFT-drop admin). Bodies only
read every argument (value types into typed storage, dynamic types through keccak256(abi.encode)),
so no library and no link placeholder exists. Compiled with solcjs 0.8.37 standard JSON, no
optimizer, evmVersion default. Writes corpus/evidence/round-29/c1/src/<name>.sol and
compiled/<name>.runtime.hex and compiled/<name>.abi.json, plus carriers.tsv (carrier, runtime,
abi, runtime_sha256, abi_sha256). Run once, before the freeze; the output is frozen.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = "corpus/evidence/round-29/c1"

IFACES = [
    ("Erc20Permit", ["name()", "symbol()", "decimals()", "totalSupply()", "balanceOf(address)",
                     "transfer(address,uint256)", "allowance(address,address)", "approve(address,uint256)",
                     "transferFrom(address,address,uint256)",
                     "permit(address,address,uint256,uint256,uint8,bytes32,bytes32)", "nonces(address)",
                     "DOMAIN_SEPARATOR()", "increaseAllowance(address,uint256)", "decreaseAllowance(address,uint256)"]),
    ("Erc721Full", ["ownerOf(uint256)", "safeTransferFrom(address,address,uint256)",
                    "safeTransferFrom(address,address,uint256,bytes)", "setApprovalForAll(address,bool)",
                    "getApproved(uint256)", "isApprovedForAll(address,address)", "tokenURI(uint256)",
                    "tokenOfOwnerByIndex(address,uint256)", "tokenByIndex(uint256)", "supportsInterface(bytes4)",
                    "baseURI()", "mint(address,uint256)", "burn(uint256)"]),
    ("Erc1155", ["balanceOf(address,uint256)", "balanceOfBatch(address[],uint256[])",
                 "safeTransferFrom(address,address,uint256,uint256,bytes)",
                 "safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)", "uri(uint256)"]),
    ("Erc4626", ["asset()", "totalAssets()", "convertToShares(uint256)", "convertToAssets(uint256)",
                 "maxDeposit(address)", "previewDeposit(uint256)", "deposit(uint256,address)", "maxMint(address)",
                 "previewMint(uint256)", "mint(uint256,address)", "maxWithdraw(address)", "previewWithdraw(uint256)",
                 "withdraw(uint256,address,address)", "maxRedeem(address)", "previewRedeem(uint256)",
                 "redeem(uint256,address,address)"]),
    ("AccessOwnable", ["owner()", "transferOwnership(address)", "renounceOwnership()", "pendingOwner()",
                       "acceptOwnership()", "hasRole(bytes32,address)", "getRoleAdmin(bytes32)",
                       "grantRole(bytes32,address)", "revokeRole(bytes32,address)", "renounceRole(bytes32,address)",
                       "DEFAULT_ADMIN_ROLE()", "paused()", "pause()", "unpause()"]),
    ("UniV2Pair", ["token0()", "token1()", "factory()", "getReserves()", "price0CumulativeLast()",
                   "price1CumulativeLast()", "kLast()", "mint(address)", "burn(address)",
                   "swap(uint256,uint256,address,bytes)", "skim(address)", "sync()", "initialize(address,address)",
                   "MINIMUM_LIQUIDITY()", "PERMIT_TYPEHASH()"]),
    ("UniV2Router", ["WETH()", "addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256)",
                     "addLiquidityETH(address,uint256,uint256,uint256,address,uint256)",
                     "removeLiquidity(address,address,uint256,uint256,uint256,address,uint256)",
                     "removeLiquidityETH(address,uint256,uint256,uint256,address,uint256)",
                     "swapExactTokensForTokens(uint256,uint256,address[],address,uint256)",
                     "swapTokensForExactTokens(uint256,uint256,address[],address,uint256)",
                     "swapExactETHForTokens(uint256,address[],address,uint256)",
                     "swapExactTokensForETH(uint256,uint256,address[],address,uint256)",
                     "getAmountsOut(uint256,address[])", "getAmountsIn(uint256,address[])",
                     "quote(uint256,uint256,uint256)", "getAmountOut(uint256,uint256,uint256)",
                     "getAmountIn(uint256,uint256,uint256)"]),
    ("UniV2Factory", ["getPair(address,address)", "allPairs(uint256)", "allPairsLength()",
                      "createPair(address,address)", "feeTo()", "feeToSetter()", "setFeeTo(address)",
                      "setFeeToSetter(address)"]),
    ("Weth9", ["deposit()", "withdraw(uint256)"]),
    ("Multicall3Getters", ["getBlockHash(uint256)", "getBlockNumber()", "getCurrentBlockCoinbase()",
                           "getCurrentBlockDifficulty()", "getCurrentBlockGasLimit()", "getCurrentBlockTimestamp()",
                           "getEthBalance(address)", "getLastBlockHash()", "getBasefee()", "getChainId()"]),
    ("ChainlinkAggregator", ["latestRoundData()", "getRoundData(uint80)", "latestAnswer()", "latestTimestamp()",
                             "latestRound()", "getAnswer(uint256)", "getTimestamp(uint256)", "description()",
                             "version()"]),
    ("Timelock", ["getMinDelay()", "isOperation(bytes32)", "isOperationPending(bytes32)", "isOperationReady(bytes32)",
                  "isOperationDone(bytes32)", "getTimestamp(bytes32)",
                  "hashOperation(address,uint256,bytes,bytes32,bytes32)",
                  "schedule(address,uint256,bytes,bytes32,bytes32,uint256)",
                  "execute(address,uint256,bytes,bytes32,bytes32)", "cancel(bytes32)", "updateDelay(uint256)"]),
    ("GovernorBravo", ["propose(address[],uint256[],string[],bytes[],string)", "queue(uint256)",
                       "castVote(uint256,uint8)", "castVoteWithReason(uint256,uint8,string)", "state(uint256)",
                       "proposalCount()", "votingDelay()", "votingPeriod()", "proposalThreshold()", "quorumVotes()",
                       "getVotes(address,uint256)", "delegate(address)", "delegates(address)",
                       "getCurrentVotes(address)", "getPriorVotes(address,uint256)"]),
    ("SafeOwners", ["getOwners()", "getThreshold()", "isOwner(address)", "nonce()",
                    "addOwnerWithThreshold(address,uint256)", "removeOwner(address,address,uint256)",
                    "swapOwner(address,address,address)", "changeThreshold(uint256)", "enableModule(address)",
                    "disableModule(address,address)", "isModuleEnabled(address)", "setGuard(address)", "VERSION()"]),
    ("EnsRegistry", ["owner(bytes32)", "resolver(bytes32)", "ttl(bytes32)", "setOwner(bytes32,address)",
                     "setSubnodeOwner(bytes32,bytes32,address)", "setResolver(bytes32,address)",
                     "setTTL(bytes32,uint64)", "recordExists(bytes32)", "setRecord(bytes32,address,address,uint64)"]),
    ("NftDropAdmin", ["royaltyInfo(uint256,uint256)", "setDefaultRoyalty(address,uint96)", "contractURI()",
                      "setBaseURI(string)", "withdrawAll()", "maxSupply()", "mintPrice()", "setMintPrice(uint256)",
                      "publicMint(uint256)", "airdrop(address[],uint256[])"]),
]

VALUE = {"address", "uint256", "uint8", "uint64", "uint80", "uint96", "bytes32", "bytes4", "bool"}
DYN = {"bytes": "bytes calldata", "string": "string calldata", "address[]": "address[] calldata",
       "uint256[]": "uint256[] calldata", "string[]": "string[] calldata", "bytes[]": "bytes[] calldata"}


def contract(name, sigs):
    lines = ["// SPDX-License-Identifier: MIT", "pragma solidity ^0.8.20;", "", "contract %s {" % name]
    for t in sorted(VALUE):
        lines.append("    %s internal v_%s;" % (t, t))
    lines.append("    bytes32 internal v_dyn;")
    for sig in sigs:
        fname, rest = sig.split("(", 1)
        types = [t for t in rest[:-1].split(",") if t]
        params, body = [], []
        for i, t in enumerate(types):
            params.append("%s a%d" % (DYN.get(t, t), i))
            if t in VALUE:
                body.append("v_%s = a%d;" % (t, i))
            else:
                body.append("v_dyn = keccak256(abi.encode(a%d));" % i)
        if not body:
            body.append("v_uint256 = block.number;")
        lines.append("    function %s(%s) external { %s }" % (fname, ", ".join(params), " ".join(body)))
    lines.append("}")
    return "\n".join(lines) + "\n"


def main():
    os.makedirs(os.path.join(LANE, OUT, "src"), exist_ok=True)
    os.makedirs(os.path.join(LANE, OUT, "compiled"), exist_ok=True)
    sources = {}
    for name, sigs in IFACES:
        src = contract(name, sigs)
        rel = "%s/src/%s.sol" % (OUT, name)
        with open(os.path.join(LANE, rel), "w", encoding="utf-8") as f:
            f.write(src)
        sources[name + ".sol"] = {"content": src}
    req = {"language": "Solidity", "sources": sources,
           "settings": {"optimizer": {"enabled": False},
                        "outputSelection": {"*": {"*": ["abi", "evm.deployedBytecode.object"]}}}}
    tmp = os.path.join(LANE, OUT, "compiled", ".solc-out.json")
    with open(tmp, "wb") as f:
        subprocess.run(["solcjs", "--standard-json"], input=json.dumps(req).encode(), stdout=f, check=True)
    raw = open(tmp, "rb").read()
    os.remove(tmp)
    out = json.loads(raw[raw.index(b"{"):])
    errs = [e for e in out.get("errors", []) if e.get("severity") == "error"]
    if errs:
        for e in errs:
            print(e.get("formattedMessage"), file=sys.stderr)
        return 1
    rows = ["\t".join(["carrier", "runtime", "abi", "runtime_sha256", "abi_sha256"])]
    for i, (name, sigs) in enumerate(IFACES, 1):
        c = out["contracts"][name + ".sol"][name]
        hexs = c["evm"]["deployedBytecode"]["object"] + "\n"
        abi = json.dumps(c["abi"], indent=1) + "\n"
        rt, ab = "%s/compiled/%s.runtime.hex" % (OUT, name), "%s/compiled/%s.abi.json" % (OUT, name)
        with open(os.path.join(LANE, rt), "w", encoding="ascii") as f:
            f.write(hexs)
        with open(os.path.join(LANE, ab), "w", encoding="utf-8") as f:
            f.write(abi)
        rows.append("\t".join(["n%02d" % i, rt, ab, hashlib.sha256(hexs.encode()).hexdigest(),
                               hashlib.sha256(abi.encode()).hexdigest()]))
    with open(os.path.join(LANE, OUT, "carriers.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    print("carriers=%d compiler=%s" % (len(IFACES), subprocess.run(["solcjs", "--version"], capture_output=True, text=True).stdout.strip()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
