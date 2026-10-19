#!/usr/bin/env python3
"""Minimal concrete EVM for dispatch-path tracing (CR-2 r6). No external deps."""
import sys, pathlib

def run(code, selector, max_steps=2000, callvalue=0, trace=False):
    stack=[]; mem=bytearray(1<<16); pc=0; steps=0; log=[]
    MASK=(1<<256)-1
    cd = selector.to_bytes(4,'big') + bytes(28+32*16)
    while steps < max_steps:
        steps+=1
        if pc>=len(code): return {'stop':'ran-off','pc':pc,'log':log,'stack':stack}
        op=code[pc]; at=pc; pc+=1
        if trace: log.append((at,op,list(stack)))
        if op==0x00: return {'stop':'STOP','pc':at,'log':log,'stack':stack}
        if op==0x5f: stack.append(0)
        elif 0x60<=op<=0x7f:
            n=op-0x5f; stack.append(int.from_bytes(code[pc:pc+n],'big')); pc+=n
        elif 0x80<=op<=0x8f:
            stack.append(stack[-(op-0x7f)])
        elif 0x90<=op<=0x9f:
            i=op-0x8f; stack[-1],stack[-1-i]=stack[-1-i],stack[-1]
        elif op==0x01:
            a=stack.pop(); b=stack.pop(); stack.append((a+b)&MASK)
        elif op==0x02:
            a=stack.pop(); b=stack.pop(); stack.append((a*b)&MASK)
        elif op==0x03:
            a=stack.pop(); b=stack.pop(); stack.append((a-b)&MASK)
        elif op==0x06:
            a=stack.pop(); b=stack.pop()
            if b==0: return {'stop':'MOD0','pc':at,'log':log,'stack':stack}
            stack.append(a%b)
        elif op==0x10:
            a=stack.pop(); b=stack.pop(); stack.append(1 if a<b else 0)
        elif op==0x11:
            a=stack.pop(); b=stack.pop(); stack.append(1 if a>b else 0)
        elif op==0x14:
            a=stack.pop(); b=stack.pop(); stack.append(1 if a==b else 0)
        elif op==0x15:
            a=stack.pop(); stack.append(0 if a else 1)
        elif op==0x16:
            a=stack.pop(); b=stack.pop(); stack.append(a&b)
        elif op==0x17:
            a=stack.pop(); b=stack.pop(); stack.append(a|b)
        elif op==0x18:
            a=stack.pop(); b=stack.pop(); stack.append(a^b)
        elif op==0x19:
            stack.append((~stack.pop())&MASK)
        elif op==0x1b:
            shift=stack.pop(); val=stack.pop(); stack.append((val<<shift)&MASK)
        elif op==0x1c:
            shift=stack.pop(); val=stack.pop(); stack.append(val>>shift if shift<256 else 0)
        elif op==0x35:
            o=stack.pop(); stack.append(int.from_bytes(cd[o:o+32],'big'))
        elif op==0x36: stack.append(len(cd))
        elif op==0x34: stack.append(callvalue)
        elif op==0x33: stack.append(0)
        elif op==0x39:
            dest=stack.pop(); off=stack.pop(); size=stack.pop()
            mem[dest:dest+size]=code[off:off+size]
        elif op==0x37:
            dest=stack.pop(); off=stack.pop(); size=stack.pop()
            mem[dest:dest+size]=cd[off:off+size]
        elif op==0x51:
            o=stack.pop(); stack.append(int.from_bytes(mem[o:o+32],'big'))
        elif op==0x52:
            o=stack.pop(); v=stack.pop(); mem[o:o+32]=v.to_bytes(32,'big')
        elif op==0x56:
            pc=stack.pop()
        elif op==0x57:
            dst=stack.pop(); cond=stack.pop()
            if cond: pc=dst
        elif op==0x5b: pass
        elif op==0x50: stack.pop()
        else:
            return {'stop':f'UNSUPPORTED_0x{op:02x}','pc':at,'log':log,'stack':stack}
    return {'stop':'step-limit','pc':pc,'log':log,'stack':stack}

if __name__=='__main__':
    code=pathlib.Path(sys.argv[1]).read_bytes()
    sel=int(sys.argv[2],16)
    r=run(code,sel,trace=False)
    print('stop',r['stop'],'pc',r['pc'],hex(r['pc']),'stack',[hex(x) for x in r['stack'][-8:]])
