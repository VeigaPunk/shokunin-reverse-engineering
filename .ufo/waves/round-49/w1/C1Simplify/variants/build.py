import ast, sys
SRC = sys.argv[1]; OUT = sys.argv[2]; groups = sys.argv[3].split(',')
src = open(SRC).read(); lines = src.split('\n')
t = ast.parse(src)
drop = set()
def take(node):
    for l in range(node.lineno, node.end_lineno + 1): drop.add(l)
def argparse_flag(node, flags):
    return (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'add_argument'
            and node.value.args and isinstance(node.value.args[0], ast.Constant)
            and node.value.args[0].value in flags)
allnodes = list(ast.walk(t))
for g in groups:
    if g == 'A':   # dead defs and selftest helpers never executed in any run
        for n in allnodes:
            if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'HANDLER_RE' for x in n.targets): take(n)
            if isinstance(n, ast.FunctionDef) and n.name in ('legacy_same_rel', 'spec_plants', 'mk_same_runner', 'runner_for'): take(n)
    if g == 'B':   # --dev-arm path (counter dev_arm() and its flags)
        for n in allnodes:
            if isinstance(n, ast.FunctionDef) and n.name == 'dev_arm': take(n)
            if isinstance(n, ast.If) and isinstance(n.test, ast.Attribute) and n.test.attr == 'dev_arm' and not n.orelse: take(n)
            if argparse_flag(n, ('--dev-arm', '--arm-dir', '--arm-ids', '--run-rea')): take(n)
    if g == 'C':   # --verify-receipt and --no-rerun (never executed; not in the plan command)
        for n in allnodes:
            if isinstance(n, ast.If) and isinstance(n.test, ast.Attribute) and n.test.attr in ('verify_receipt', 'no_rerun') and not n.orelse: take(n)
            if argparse_flag(n, ('--verify-receipt', '--no-rerun')): take(n)
    if g == 'D':   # silent-admit branch: gate reads receipt field removed.silent, never set on the frozen table
        for n in allnodes:
            if isinstance(n, ast.FunctionDef) and n.name == 'silent_detail_matches': take(n)
            if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'allowed_details' for x in n.targets): take(n)
            if isinstance(n, ast.If) and isinstance(n.test, ast.BoolOp) and not n.orelse and any(
                    isinstance(v, ast.Call) and getattr(v.func, 'id', '') == 'silent_detail_matches' for v in ast.walk(n.test)): take(n)
out = [l for i, l in enumerate(lines, 1) if i not in drop]
open(OUT, 'w').write('\n'.join(out))
print('removed lines', len(drop))
