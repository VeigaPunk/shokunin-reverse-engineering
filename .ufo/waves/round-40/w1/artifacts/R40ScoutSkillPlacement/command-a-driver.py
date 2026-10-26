import importlib.util,sys,json
spec=importlib.util.spec_from_file_location('c2','/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
root,rev=sys.argv[1:3]
print(json.dumps(m.command_a(root,rev),sort_keys=True), m.heading_range(m.show(root,rev,'SKILL.md'),'## Queue-drain craft',lambda l:l.startswith('## ')))
