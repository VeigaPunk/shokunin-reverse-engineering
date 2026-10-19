#!/usr/bin/env python3
"""Linear disassembler for a .bin range; prints pc/bytes/mnemonic. Usage:
disasm.py <bin> [start] [end]"""
import sys

OPS = {0x00:'STOP',0x01:'ADD',0x02:'MUL',0x03:'SUB',0x04:'DIV',0x05:'SDIV',0x06:'MOD',0x07:'SMOD',
0x08:'ADDMOD',0x09:'MULMOD',0x0a:'EXP',0x0b:'SIGNEXTEND',0x10:'LT',0x11:'GT',0x12:'SLT',0x13:'SGT',
0x14:'EQ',0x15:'ISZERO',0x16:'AND',0x17:'OR',0x18:'XOR',0x19:'NOT',0x1a:'BYTE',0x1b:'SHL',0x1c:'SHR',
0x1d:'SAR',0x20:'KECCAK256',0x30:'ADDRESS',0x31:'BALANCE',0x32:'ORIGIN',0x33:'CALLER',0x34:'CALLVALUE',
0x35:'CALLDATALOAD',0x36:'CALLDATASIZE',0x37:'CALLDATACOPY',0x38:'CODESIZE',0x39:'CODECOPY',0x3a:'GASPRICE',
0x3b:'EXTCODESIZE',0x3c:'EXTCODECOPY',0x3d:'RETURNDATASIZE',0x3e:'RETURNDATACOPY',0x3f:'EXTCODEHASH',
0x40:'BLOCKHASH',0x41:'COINBASE',0x42:'TIMESTAMP',0x43:'NUMBER',0x44:'PREVRANDAO',0x45:'GASLIMIT',
0x46:'CHAINID',0x47:'SELFBALANCE',0x48:'BASEFEE',0x49:'BLOBHASH',0x4a:'BLOBBASEFEE',
0x50:'POP',0x51:'MLOAD',0x52:'MSTORE',0x53:'MSTORE8',0x54:'SLOAD',0x55:'SSTORE',0x56:'JUMP',0x57:'JUMPI',
0x58:'PC',0x59:'MSIZE',0x5a:'GAS',0x5b:'JUMPDEST',0x5c:'TLOAD',0x5d:'TSTORE',0x5e:'MCOPY',
0x5f:'PUSH0',0xf0:'CREATE',0xf1:'CALL',0xf2:'CALLCODE',0xf3:'RETURN',0xf4:'DELEGATECALL',0xf5:'CREATE2',
0xfa:'STATICCALL',0xfd:'REVERT',0xfe:'INVALID',0xff:'SELFDESTRUCT'}

def main():
    path = sys.argv[1]
    b = open(path,'rb').read()
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    end = int(sys.argv[3]) if len(sys.argv) > 3 else min(len(b), start+160)
    i = start
    while i < end:
        op = b[i]
        if 0x60 <= op <= 0x7f:
            n = op-0x5f
            imm = b[i+1:i+1+n]
            print(f"{i:5d}  {imm.hex():>64s}  PUSH{n}")
            i += 1+n
        else:
            name = OPS.get(op)
            if name is None and 0x80 <= op <= 0x8f: name = f"DUP{op-0x7f}"
            if name is None and 0x90 <= op <= 0x9f: name = f"SWAP{op-0x8f}"
            if name is None and 0xa0 <= op <= 0xa4: name = f"LOG{op-0xa0}"
            print(f"{i:5d}  {b[i]:02x}  {name or ('UNKNOWN_%02x'%op)}")
            i += 1

if __name__ == '__main__':
    main()