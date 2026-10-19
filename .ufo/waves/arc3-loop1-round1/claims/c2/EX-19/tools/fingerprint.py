import ast, hashlib, json, sys
path = sys.argv[1]
src = open(path).read()
tree = ast.parse(src)
out = {"file_sha256": hashlib.sha256(src.encode()).hexdigest(), "nodes": []}
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        seg = ast.get_source_segment(src, node)
        out["nodes"].append({
            "kind": type(node).__name__, "name": node.name,
            "lineno": node.lineno, "end_lineno": node.end_lineno,
            "sha256": hashlib.sha256(seg.encode()).hexdigest()})
print(json.dumps(out, indent=1))
