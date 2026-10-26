R39CL2Registry — retained evidence index
=======================================
Base revision for every read: a2f64e1da78afcf8cc39287106604dbcc270844c (lane main).
Lane path used below as <LANE> = /home/vgpnk/Projects/shokunin/kaidoku-shokunin.
PKG65 = /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
All commands ran with `cd <LANE>`, TMPDIR=<seat scratch>, HYAKU_SCRATCH=/fast/scratch/hyaku.
No REA run, no carrier build, no held-out carrier touched, no network fetch.

1. Counter self-tests (stdout quoted in the report)
   python3 -I -B tools/round-35/c1-coverage-counter.py --selftest            -> exit 0  "C1_SELFTEST: ok / green=0 red=1"
   python3 -I -B tools/round-35/c2-calibration-counter.py --selftest         -> exit 0  "C2_SELFTEST: ok / green=0 red=1"
   python3 -I -B tools/round-38/c1-counter.py --selftest --pkg65 $PKG65      -> exit 0  {"cases":15,"green_ok":1,"red_ok":14,"failures":[]}
   python3 -I -B tools/round-38/c2-counter.py --selftest                     -> exit 0  {"cases":14,"green_ok":1,"red_ok":13,"failures":[]}

2. tools/round-37/c1-counter.py — three reachability probes
   a) --selftest --pkg65 $PKG65                                              -> exit 2  argparse: "--root, --rev, --freeze" required
   b) --root <LANE> --rev <BASE> --freeze <BASE> --selftest --pkg65 $PKG65   -> exit 1  FileNotFoundError at selftest()/make_fixture (line 323)
      (scratch leak: /fast/scratch/hyaku/kaidoku-r37/selftest/green created by this probe; left in place, not deleted, because the path is shared)
   c) --root <LANE> --rev <BASE> --freeze <BASE> --pkg65 $PKG65              -> exit 1  TypeError: a bytes-like object is required, not 'str' (load_oracle, line 93)

3. Missing-argument exit codes (six tools, no args)
   python3 -I -B tools/round-35/c1-coverage-counter.py     -> 2
   python3 -I -B tools/round-35/c2-calibration-counter.py  -> 2
   python3 -I -B tools/round-38/c1-counter.py              -> 2
   python3 -I -B tools/round-38/c2-counter.py              -> 2
   python3 -I -B tools/round-38/freeze-drift.py            -> 2
   python3 -I -B tools/round-38/intended-doc.py            -> 2

4. Harness usage paths (no REA invoked)
   bash tools/round-37/c1-run.sh                                     -> exit 2  "usage: ... before|after K OUTDIR [SCRATCH]"
   bash tools/round-37/c1-run.sh before KNOPE <out>                   -> exit 1  "unknown carrier KNOPE" (undeclared code)
   bash tools/round-38/c1-run.sh                                     -> exit 1  "line 24: 1: mode" (${1:?})
   bash tools/round-38/c1-run.sh nope X <out>                        -> exit 2  "usage: ...{before|after|oracle}..."

5. Fixture A — freeze-drift (git fixture, -c user.name/email only, verified toplevel = itself)
   D=$(mktemp -d "$S/fx.XXXX"); git -C "$D" init -q
   test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
   mkdir -p "$D/plans" "$D/tools/round-38"; printf 'a\n' > "$D/plans/round-38-claims.md"
   printf 'b\n' > "$D/tools/round-38/c1-counter.py"
   git -C "$D" add -A; git -C "$D" -c user.name=fx -c user.email=fx@fx commit -qm f1   # F1
   printf 'a2\n' >> "$D/plans/round-38-claims.md"
   git -C "$D" add -A; git -C "$D" -c user.name=fx -c user.email=fx@fx commit -qm f2   # F2
   python3 -I -B tools/round-38/freeze-drift.py --root "$D" --freeze F2 --rev F2 tools/round-38/c1-counter.py --json-out freeze-drift-clean.json   -> exit 0
   python3 -I -B tools/round-38/freeze-drift.py --root "$D" --freeze F1 --rev F2 plans/round-38-claims.md --json-out freeze-drift-drift.json      -> exit 1
   python3 -I -B tools/round-38/freeze-drift.py --root "$D" --freeze deadbeef --rev F2 plans/round-38-claims.md --json-out freeze-drift-unknown-rev.json -> exit 2
   python3 -I -B tools/round-38/freeze-drift.py --root "$D" --freeze F2 --rev F1 plans/round-38-claims.md   -> exit 2 (freeze not an ancestor; no receipt file kept, output was a JSON verdict on stdout)
   Commit ids: see fixture-commits.txt.

6. Fixture B — intended-doc (base: PROVINCE row names `evidence/doctor/`, which resolves nowhere;
   rev: row names `.ufo/waves/round-19/evidence/doctor/`, a document that exists at base and is
   unchanged)
   python3 -I -B tools/round-38/intended-doc.py --root "$D2" --rev R --base B --file PROVINCE.md \
       --unit 'REA MCP server' --intended .ufo/waves/round-19/evidence/doctor/   -> exit 0  "bound"      (intended-doc-bound.json)
   same with --rev B (base tree, un-named path)                                  -> exit 1  "not-bound"  (intended-doc-notbound.json)
   same with --rev deadbeef                                                      -> exit 2               (intended-doc-unevaluable.json)
   Commit ids: see fixture-commits.txt.

7. Fixture C — registry-immutable (fixture B's tree carries the SOURCES row; the rev widens the
   scope cell; fixture D3 makes a status + used-by change only)
   bash tools/round-38/registry-immutable.sh "$D2" B R   -> exit 1  "S100 changed columns: 6"   (registry-immutable-scope.jsonl)
   bash tools/round-38/registry-immutable.sh "$D3" B2 R2 -> exit 0  silent                      (registry-immutable-ok.txt, 0 bytes)

8. gen-controls — five fixture kinds (no REA, counters' own fixtures)
   python3 -I -B tools/round-38/gen-controls.py c1-1 --out ctl-c1-1.json   -> exit 0  {"counter_exit":1,"kill":false}
   ... c1-2, c2-1, c2-2, c2-3 likewise -> exit 0 each; receipts in ctl-*.json
   c1-0 / c2-0 not exercised.

9. gen-squashfs — six builds from one tree (usr/bin/hello, etc/app.conf, etc/hello-link -> ../usr/bin/hello)
   python3 -I -B tools/round-37/gen-squashfs.py tree img-le.sqsh  --endian le  --comp gzip  -> exit 0  magic 68737173 ("hsqs")
   python3 -I -B tools/round-37/gen-squashfs.py tree img-be.sqsh  --endian be  --comp gzip  -> exit 0  magic 73717368 ("sqsh")
   python3 -I -B tools/round-37/gen-squashfs.py tree img-avm.sqsh --endian avm --comp gzip  -> exit 0  magic 73717368 ("sqsh")
   python3 -I -B tools/round-37/gen-squashfs.py tree img-le2.sqsh --endian le  --comp gzip  -> exit 0  byte-identical to img-le.sqsh
   python3 -I -B tools/round-37/gen-squashfs.py tree img-le-xz.sqsh --endian le --comp xz   -> exit 0
   python3 -I -B tools/round-37/gen-squashfs.py tree                     -> exit 2  argparse (missing "out")
   Images are kept here as evidence (504 bytes each) and are not carriers.

10. Fixture-file digests checked against the round-38 record
   sha256sum tools/round-38/selftest/* -> equal to .ufo/waves/round-38/w1/R38ExecSelftests.md:33-34
   (full digests in registry.md, row 13).
