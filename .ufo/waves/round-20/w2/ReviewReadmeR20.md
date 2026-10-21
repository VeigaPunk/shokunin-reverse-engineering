HOLDS

[OBSERVATION] `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- corpus/README.md | cat -n | sed -n '1,80p'` — exit 0. The Archives & packages row is extended in place at `corpus/README.md:27` with the Harmony entry and scoped HAP limitations; the Go row at `:35` adds the Go 1.24.6 forecast entry. The new Static tool verbs row occupies the former blank line 69; `## Knowledge` remains at `:70`. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show B:corpus/README.md | wc -l` and the same command with S each returned 190 (exit 0), so the additions do not shift later coordinates.

[OBSERVATION] `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && diff <(git ls-tree -r --name-only 14f0260ad319ecc26994381b2415d5a999003375 -- corpus/knowledge/) <(git ls-tree -r --name-only 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- corpus/knowledge/)` — exit 1 (expected additions): exactly five new knowledge files, all represented in the map: Go forecast (`README.md:35`), Harmony graph (`:27`), and objdump architecture, Rizin command, and WASM interfaces (`:69`).

[OBSERVATION] Ran the S Git-object body of `.ufo/waves/round-20/controls-r20.py` with B and S (exit 0); its `command_a.source` reports 102 knowledge files, 102 mapped, `missing: []`, `dangling: []`, `coverage_score: 10.0` (B: 97/97). Exact invocation:

```sh
python3 -I -B -c 'import subprocess,sys; root="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; rev="5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9"; p=".ufo/waves/round-20/controls-r20.py"; f=root+"/"+p; src=subprocess.check_output(["git","-C",root,"show",rev+":"+p]); sys.argv=[f,"14f0260ad319ecc26994381b2415d5a999003375",rev]; exec(compile(src,f,"exec"),{"__name__":"__main__","__file__":f})'
```

[OBSERVATION] Git-object pointer assertions at S — exit 0: `corpus/README.md:175` points to `SCORECARD.md:1216`, r7 lines 13–37, and round-8 E2 lines 23–45; each target contains its expected cited text. `SCORECARD.md:69` points to `corpus/README.md:180`, whose text still says “held, not frontier.” Assertion command:

```sh
python3 -I -B -c 'import subprocess as s; R="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; V="5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9"; L=lambda f:s.check_output(["git","-C",R,"show",V+":"+f],text=True).splitlines(); r=L("corpus/README.md"); c=L("SCORECARD.md"); a=L("corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md"); b=L(".ufo/waves/arc2-loop1-round8/E2.md"); assert "SCORECARD.md:1216" in r[174] and "rerun id-stability" in c[1215]; assert "r7-pe-wall.md:13-37" in r[174] and any("Wall taxonomy closure" in x for x in a[12:37]); assert "round8/E2.md:23-45" in r[174] and any("Result: oom-kill" in x for x in b[22:45]); assert "corpus/README.md:180" in c[68] and "held, not frontier" in r[179]; print("PASS README:175 SCORECARD/r7/r8 and SCORECARD:69→README:180")'
```

[INFERENCE] No README mapping or pinned-coordinate defect found in scope. Residual limit: command A is a stem-to-map integrity check, not validation of the knowledge entries’ substantive claims; those were not audited here.