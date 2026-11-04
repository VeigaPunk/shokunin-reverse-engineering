## Erratum — round 66 close (append-only, QUALITY #65)

The per-group table above ("The closure — 30 pinned entries") counts the `venv identity` group as
**four** entries while listing five pinned paths — `parse/__init__.py`, `parse/__init__.pyi`,
`parse-1.22.4.dist-info/METADATA`, `parse-1.22.4.dist-info/RECORD`, `venv/pyvenv.cfg` — and the
sha-pinned map holds five keys under `venv/` (`tools/round-65/jsc-closure-matrix.py`, `CLOSURE`).
The table's 30-entry total survives that miscount only because the probe is counted twice: once as
the Electron 42.2.0 probe cache under `artifacts` and once as the probe path under `harness`, so
the five groups sum to 31 slots over 30 distinct paths — `len(CLOSURE)` 27 plus the three external
pins (probe, node, interpreter). Check:

```bash
python3 -I -B -c "import importlib.util; s=importlib.util.spec_from_file_location('m','tools/round-65/jsc-closure-matrix.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(len(m.CLOSURE), sum(1 for k in m.CLOSURE if k.startswith('venv/')))"
```

-> `27 5`, and `len(m.CLOSURE) + 3` -> `30`. The grouping, not the closure run or its receipts, was
wrong. The filed sentence is not rewritten; this erratum supersedes its group count.
