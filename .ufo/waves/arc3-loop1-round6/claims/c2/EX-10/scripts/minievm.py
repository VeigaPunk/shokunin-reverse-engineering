#!/usr/bin/env python3
"""Tiny EVM interpreter for the dispatch prologues (EX-10, arc3-r6). Read-only trace."""
import sys

class EVM:
    def __init__(self, code, calldata=b'', trace=False, stop_pc=None):
        self.code=code; self.calldata=calldata; self.stack=[]; self.mem=bytearray(4096)
        self.pc=0; self.trace=trace; self.log=[]; self.steps=0; self.stop_pc=stop_pc
    def pop(self): return self.stack.pop()
    def push(self,v): self.stack.append(v & ((1<<256)-1))
    def mload(self,off):
        off &= (1<<256)-1
        chunk=self.mem[off:off+32].ljust(32,b'\0')
        return int.from_bytes(chunk,'big')
    def mstore(self,off,val):
        off &= (1<<256)-1
        self.mem[off:off+32]=val.to_bytes(32,'big')
    def codecopy(self,dst,off,size):
        dst&=0xffff; off&=0xffff; size&=0xffff
        chunk=self.code[off:off+size].ljust(size,b'\0')
        self.mem[dst:dst+size]=chunk
    def run(self, max_steps=400):
        while self.pc < len(self.code) and self.steps < max_steps:
            if self.stop_pc is not None and self.pc == self.stop_pc:
                self.log.append((self.pc,'STOP_PC','',None)); break
            self.steps += 1
            pc=self.pc; op=self.code[pc]; self.pc+=1
            name=f'OP_{op:02x}'; imm=b''
            if 0x60<=op<=0x7f:
                k=op-0x5f; imm=self.code[self.pc:self.pc+k]; self.pc+=k
                self.push(int.from_bytes(imm,'big')); name=f'PUSH{k}'
            elif op==0x5f: self.push(0); name='PUSH0'
            elif 0x80<=op<=0x8f:
                n=op-0x7f; self.push(self.stack[-n]); name=f'DUP{n}'
            elif 0x90<=op<=0x9f:
                n=op-0x8f; self.stack[-1],self.stack[-1-n]=self.stack[-1-n],self.stack[-1]; name=f'SWAP{n}'
            elif op==0x01: a=self.pop(); b=self.pop(); self.push(a+b); name='ADD'
            elif op==0x02: a=self.pop(); b=self.pop(); self.push(a*b); name='MUL'
            elif op==0x03: a=self.pop(); b=self.pop(); self.push(a-b); name='SUB'
            elif op==0x04: a=self.pop(); b=self.pop(); self.push(0 if b==0 else a//b); name='DIV'
            elif op==0x06: a=self.pop(); b=self.pop(); self.push(0 if b==0 else a%b); name='MOD'
            elif op==0x10: a=self.pop(); b=self.pop(); self.push(1 if a<b else 0); name='LT'
            elif op==0x11: a=self.pop(); b=self.pop(); self.push(1 if a>b else 0); name='GT'
            elif op==0x12: a=self.pop(); b=self.pop(); self.push(1 if self.signed(a)<self.signed(b) else 0); name='SLT'
            elif op==0x13: a=self.pop(); b=self.pop(); self.push(1 if self.signed(a)>self.signed(b) else 0); name='SGT'
            elif op==0x14: a=self.pop(); b=self.pop(); self.push(1 if a==b else 0); name='EQ'
            elif op==0x15: a=self.pop(); self.push(1 if a==0 else 0); name='ISZERO'
            elif op==0x16: a=self.pop(); b=self.pop(); self.push(a&b); name='AND'
            elif op==0x17: a=self.pop(); b=self.pop(); self.push(a|b); name='OR'
            elif op==0x18: a=self.pop(); b=self.pop(); self.push(a^b); name='XOR'
            elif op==0x19: a=self.pop(); self.push(((1<<256)-1)^a); name='NOT'
            elif op==0x1a: a=self.pop(); b=self.pop(); self.push((a.to_bytes(32,'big') if a<256 else (0).to_bytes(32,'big'))[0] if False else ((b>>(8*(31-a)))&0xff if a<32 else 0)); name='BYTE'
            elif op==0x1b: a=self.pop(); b=self.pop(); self.push((b<<a) if a<256 else 0); name='SHL'
            elif op==0x1c: a=self.pop(); b=self.pop(); self.push((b>>a) if a<256 else 0); name='SHR'
            elif op==0x1d: a=self.pop(); b=self.pop(); self.push(self.signed(b)>>a if a<256 else (0 if self.signed(b)>=0 else -1)); name='SAR'
            elif op in (0x30,0x32,0x33,0x34,0x38,0x3d,0x46,0x47,0x58): 
                self.push(0); name={0x30:'ADDRESS',0x32:'ORIGIN',0x33:'CALLER',0x34:'CALLVALUE',0x38:'CODESIZE',0x3d:'RETURNDATASIZE',0x46:'CHAINID',0x47:'SELFBALANCE',0x58:'PC'}[op]
            elif op==0x35: a=self.pop(); self.push(int.from_bytes(self.calldata[a:a+32].ljust(32,b'\0'),'big')); name='CALLDATALOAD'
            elif op==0x36: self.push(len(self.calldata)); name='CALLDATASIZE'
            elif op==0x39:
                dst=self.pop(); off=self.pop(); size=self.pop(); self.codecopy(dst,off,size); name='CODECOPY'
            elif op==0x50: self.pop(); name='POP'
            elif op==0x51: a=self.pop(); self.push(self.mload(a)); name='MLOAD'
            elif op==0x52: a=self.pop(); b=self.pop(); self.mstore(a,b); name='MSTORE'
            elif op==0x53: a=self.pop(); b=self.pop(); self.mem[a]=b&0xff; name='MSTORE8'
            elif op==0x54: a=self.pop(); self.push(0); name='SLOAD'
            elif op==0x55: a=self.pop(); b=self.pop(); name='SSTORE'
            elif op==0x56:
                dst=self.pop(); name='JUMP'
                self.maybe_log(pc,name,imm,dst)
                if self.code[dst]!=0x5b: raise Exception(f'bad jump {dst} at {pc}')
                self.pc=dst; continue
            elif op==0x57:
                dst=self.pop(); cond=self.pop(); name='JUMPI'
                self.maybe_log(pc,name,imm,{'dst':dst,'cond':cond})
                if cond:
                    if self.code[dst]!=0x5b: raise Exception(f'bad jumpi {dst} at {pc}')
                    self.pc=dst
                continue
            elif op==0x5b: name='JUMPDEST'
            elif op==0x5a: self.push(10_000_000); name='GAS'
            elif op==0x00: name='STOP'; self.maybe_log(pc,name,imm); break
            elif op==0xfd: name='REVERT'; self.maybe_log(pc,name,imm); break
            elif op==0xfe: name='INVALID'; self.maybe_log(pc,name,imm); break
            else: raise Exception(f'unsupported op {op:02x} at {pc}')
            self.maybe_log(pc,name,imm)
        return self.pc, list(self.stack)
    def signed(self,v):
        return v-(1<<256) if v>=1<<255 else v
    def maybe_log(self,pc,name,imm,extra=None):
        if self.trace:
            self.log.append((pc,name,imm.hex(),extra,[hex(x) for x in self.stack]))

if __name__=='__main__':
    code=open(sys.argv[1],'rb').read()
    sel=bytes.fromhex(sys.argv[2]) if len(sys.argv)>2 else b''
    cd=(sel+b'\0'*28) if sel else b''
    stop=int(sys.argv[3]) if len(sys.argv)>3 else None
    e=EVM(code, cd, trace=True, stop_pc=stop)
    end,st=e.run()
    for row in e.log[:60]:
        print(row[:4], 'stack=', row[4] if len(row)>4 else None)
    print('END pc=',end,'stack=',[hex(x) for x in st[-4:]],'log_len=',len(e.log))
