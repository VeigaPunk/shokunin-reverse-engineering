#!/bin/sh
# sasquatch-shaped shim: accepts unblob's argv, delegates to unsquashfs.
args=""; outdir=""; inpath=""
while [ $# -gt 0 ]; do
  case "$1" in
    -be|-le|-no-exit-code) shift ;;
    -f) shift ;;
    -d) outdir="$2"; shift 2 ;;
    -*) shift ;;
    *) inpath="$1"; shift ;;
  esac
done
echo "SHIM $*" >> /fast/scratch/hyaku/kaidoku-r42/R42C1Sentinel/shim-hits.log
exec /usr/bin/unsquashfs -processors 1 -f -q -d "$outdir" "$inpath"
