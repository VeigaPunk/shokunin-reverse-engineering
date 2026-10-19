"""Straight-line stack simulator for the dispatch header (seat CR-1, arc3-r6).

Values are ints when concrete; symbolic values are ('sym', text). Memory is a
bytearray; CODECOPY fills it concretely when args are concrete.
Stops at the first JUMP/JUMPI whose target/condition is not fully concrete,
or at RETURN/REVERT/STOP, or after --max ops.
"""
import sys

from disasm import NAMES, load, sweep

M = (1 << 256) - 1


def sym(x):
    return ('sym', x)


def is_sym(v):
    return isinstance(v, tuple)


def fmt(v):
    if is_sym(v):
        return v[1]
    return hex(v) if v > 0xffff else str(v)


def run(path, maxops=60):
    code = load(path)
    mem = bytearray(4096)
    stack = []
    ops = sweep(code)
    for i, (pc, op, imm) in enumerate(ops[:maxops]):
        nm = NAMES.get(op, f'0x{op:02x}')
        before = list(stack[-6:])
        try:
            if 0x60 <= op <= 0x7f or op == 0x5f:
                stack.append(int.from_bytes(imm, 'big') if imm else 0)
            elif 0x80 <= op <= 0x8f:
                n = op - 0x7f
                stack.append(stack[-n])
            elif 0x90 <= op <= 0x9f:
                n = op - 0x8f
                stack[-1], stack[-1 - n] = stack[-1 - n], stack[-1]
            elif op == 0x35:  # CALLDATALOAD
                stack.append(sym('CD[%s]' % fmt(stack.pop())))
            elif op == 0x36:
                stack.append(sym('CDSIZE'))
            elif op == 0x34:
                stack.append(sym('CALLVALUE'))
            elif op == 0x39:  # CODECOPY dest,off,len (top=dest)
                d, o, n = stack.pop(), stack.pop(), stack.pop()
                if all(not is_sym(v) for v in (d, o, n)):
                    chunk = code[o:o + n]
                    mem[d:d + len(chunk)] = chunk
                    stack.append(0)  # placeholder marker unused
                    stack.pop()
                else:
                    print('CODECOPY symbolic', fmt(d), fmt(o), fmt(n))
            elif op == 0x51:  # MLOAD
                o = stack.pop()
                if is_sym(o):
                    stack.append(sym('M[%s]' % fmt(o)))
                else:
                    stack.append(int.from_bytes(mem[o:o + 32], 'big'))
            elif op == 0x52:  # MSTORE
                o, v = stack.pop(), stack.pop()
                if not is_sym(o) and not is_sym(v):
                    mem[o:o + 32] = v.to_bytes(32, 'big')
            elif op == 0x50:
                stack.pop()
            elif op in (0x01, 0x02, 0x03, 0x04, 0x06, 0x10, 0x11, 0x14,
                        0x16, 0x17, 0x18, 0x1b, 0x1c):
                a, b = stack.pop(), stack.pop()
                if is_sym(a) or is_sym(b):
                    fn = {0x01: '+', 0x02: '*', 0x03: '-', 0x04: '/', 0x06: '%',
                          0x10: '<', 0x11: '>', 0x14: '==', 0x16: '&',
                          0x17: '|', 0x18: '^', 0x1b: '<<', 0x1c: '>>'}[op]
                    stack.append(sym('(%s %s %s)' % (fmt(a), fn, fmt(b))))
                else:
                    r = {0x01: a + b, 0x02: a * b, 0x03: (b - a) % (M + 1),
                         0x04: b // a if a else 0, 0x06: b % a if a else 0,
                         0x10: int(b < a), 0x11: int(b > a), 0x14: int(a == b),
                         0x16: a & b, 0x17: a | b, 0x18: a ^ b,
                         0x1b: (b << a) & M, 0x1c: b >> a}[op]
                    stack.append(r)
            elif op == 0x15:
                a = stack.pop()
                stack.append(sym('!%s' % fmt(a)) if is_sym(a) else int(a == 0))
            elif op == 0x19:
                a = stack.pop()
                stack.append(sym('~%s' % fmt(a)) if is_sym(a) else M ^ a)
            elif op in (0x56, 0x57):
                if op == 0x56:
                    t = stack.pop()
                    print(f'{pc:4d} {nm} {before} -> target {fmt(t)}')
                else:
                    t = stack.pop()
                    c = stack.pop()
                    print(f'{pc:4d} {nm} {before} -> cond {fmt(c)} target {fmt(t)}')
                if op in (0x56, 0x57) and i + 1 < len(ops):
                    print('     next op:', NAMES.get(ops[i + 1][1], '?'))
                return
            else:
                stack.append(sym(nm))
        except IndexError:
            print(f'{pc:4d} STACK UNDERFLOW on {nm}')
            print('  stack(top last):', [fmt(v) for v in stack])
            return
        if i < 55:
            print(f'{pc:4d} {nm:8s} {" ".join(fmt(v) for v in before):45s} '
                  f'-> {" ".join(fmt(v) for v in stack[-4:])}')


if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 60)
