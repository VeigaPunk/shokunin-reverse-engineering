Harness self-test doubles for the oracle arm's failure paths. They are NOT oracles and never
enter a receipt: `oracle-exit3.py` writes valid tables + a disagreeing report and exits 3 (F9);
`oracle-dup.py` writes a duplicate regular relpath and exits 0 (F10); `oracle-nojson.py` omits
`--json` from --help (F11).
