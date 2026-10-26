# R41C1Collide — exact commands

Everything below ran in `S=/fast/scratch/hyaku/kaidoku-r41/R41C1Collide`
(`export TMPDIR="$S"`), lane `R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
artifacts `A=$R/.ufo/waves/round-41/w1/artifacts/R41C1Collide`.
No reserved carrier (FRITZ!Box 3490/5490/5491/7560 images, L3/L4) was read,
run, carved or copied; every input here is a fresh lane-built tree or the
already-burned round-40 development evidence.

## 1. build the fresh AVM-genuine dev carriers (deterministic)

    python3 -I -B "$A/build-dev.py" "$S/carriers3" \
        "$R/tools/round-40/gen-squashfs.py"
    # rc=0, prints  id  sha256  size  per carrier:
    #   A-xz fef3fc128c7c87d4ebfc50d156bae09344e6dde0179f832b8d2b094ab1f2543b 70729
    #   A-gz 050a477f1c686187fdd1850b5710de5250dd2c4c3ede8fa7458b4e7fc8a1d1ce 70729
    #   B-xz 8d40d56d4f0591b7918aec1c327c746ed577e357aa3e770ca016526676c0687a 70726
    #   C-xz 36356f93b5649f3aa18d0146938ecd24ffb701c4a9d20d26007a86631955393f 14560
    #   D-xz bf6c6975e406bf01cd0ca49679c9cc842e373ffdbd48625ddf832e099e3aaa3c 30691
    #   E-xz a062c5e7fc7533b89f2edfcb61bfbe84025aaa68b429dac237c48e41a79851b4 40916
    # a second build into a fresh dir printed the same six sha256 values
    # (byte-identical regeneration; A/B/C also matched the pre-D/E build).

## 2. extract with REA 6.5.0 (fresh outdir per run, parent pre-created)

    mkdir -p "$S/out"
    for c in A-xz A-gz B-xz C-xz D-xz; do
      REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
      npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
          --max-depth 1 "$S/carriers3/$c/carrier.sqsh" "$S/out/$c" \
          > "$S/rea-$c.log" 2>&1          # rc=0
    done
    REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
    npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
        --max-depth 1 "$S/carriers3/E-xz/carrier.sqsh" "$S/out/E-xz-d1" > "$S/rea-E-xz-d1.log"
    REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
    npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
        --max-depth 2 "$S/carriers3/E-xz/carrier.sqsh" "$S/out/E-xz-d2" > "$S/rea-E-xz-d2.log"
    # wrapper probe: a tar holding A-xz's image as var/tmp/filesystem.image
    tar -C "$S/wrap" -cf "$S/wrap.tar" var/tmp/filesystem.image
    REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
    npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
        --max-depth 2 "$S/wrap.tar" "$S/out/wrap-d2" > "$S/rea-wrap-d2.log"

## 3. hypothesis checks (H1..H4) and the three-matcher score

    cp "$S/rea-E-xz-d1.log" "$S/rea-E-xz.log"     # default-loop naming
    python3 -I -B "$A/verify-publish.py" --lane "$R" --carriers "$S/carriers3"
    python3 -I -B "$A/score-matchers.py" --lane "$R" --carriers "$S/carriers3" \
        --json "$S/scores-all.json" \
        --receipts "$S/rea-E-xz-d2.log=$S/carriers3/E-xz/oracle.tsv=$S/carriers3/E-xz/nonregular.tsv=E-d2-outer-oracle" \
                   "$S/rea-E-xz-d2.log=$S/inner-oracle.tsv=$S/empty-nonreg.tsv=E-d2-inner-oracle-probe" \
                   "$S/rea-wrap-d2.log=$S/carriers3/A-xz/oracle.tsv=$S/carriers3/A-xz/nonregular.tsv=wrap-d2-carrier-oracle" \
                   "$S/C-shadow.log=$S/carriers3/C-xz/oracle.tsv=$S/carriers3/C-xz/nonregular.tsv=C-shadow-DERIVED" \
                   "$S/A-materialised.log=$S/carriers3/A-xz/oracle.tsv=$S/carriers3/A-xz/nonregular.tsv=A-materialised-DERIVED" \
                   "$S/A-nogap.log=$S/carriers3/A-xz/oracle.tsv=$S/carriers3/A-xz/nonregular.tsv=A-nogap-DERIVED" \
                   "$R/corpus/evidence/round-40/c1/V1/after.json=$R/corpus/evidence/round-40/c1/V1/oracle.tsv=$R/corpus/evidence/round-40/c1/V1/nonregular.tsv=r40-V1" \
                   "$R/corpus/evidence/round-40/c1/V2/after.json=$R/corpus/evidence/round-40/c1/V2/oracle.tsv=$R/corpus/evidence/round-40/c1/V2/nonregular.tsv=r40-V2" \
                   "$R/corpus/evidence/round-40/c1/L1/after.json=$R/corpus/evidence/round-40/c1/L1/oracle.tsv=$R/corpus/evidence/round-40/c1/L1/nonregular.tsv=r40-L1" \
                   "$R/corpus/evidence/round-40/c1/L2/after.json=$R/corpus/evidence/round-40/c1/L2/oracle.tsv=$R/corpus/evidence/round-40/c1/L2/nonregular.tsv=r40-L2"

## 4. tool census used

    rea-agents 6.5.0 (npx, package cache only)      npx -y rea-agents@6.5.0 --version  -> 6.5.0
    unblob 26.6.4                                   unblob --version                  -> 26.6.4
      executable_sha256 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09
    sasquatch-v4be 4.5.1 (in ~/.local/bin)          -v                                -> 4.5.1
    sasquatch 4.5.1 (standard BE)                   cross-check only
No tool was installed, upgraded, moved or removed; no pacman transaction ran.
