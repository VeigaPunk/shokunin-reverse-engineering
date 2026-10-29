#!/usr/bin/env bash
# SrcReopenAvmIndex: verify HEAD results against frozen carriers.json pins, crosscheck
# listing sizes vs ETag hex, confirm attempt-1 quote row. Emits receipt lines only.
set -u
S=/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenAvmIndex
hval() { # file, header-regex
  grep -iE "^$2:" "$1" 2>/dev/null | tail -1 | sed -E "s/^[^:]+: //" | tr -d '\r'
}
echo "== A. HEAD pins vs carriers.json frozen pins =="
check() { # id lm_pin et_pin
  id=$1; lmp=$2; etp=$3
  lm=$(hval "$S/head/$id.hdr" 'last-modified')
  et=$(hval "$S/head/$id.hdr" 'etag')
  cl=$(hval "$S/head/$id.hdr" 'content-length')
  v=DRIFT; [ "$lm" = "$lmp" ] && [ "$et" = "$etp" ] && v=MATCH
  echo "PIN $id lm='$lm' et='$et' cl=$cl | pin_lm='$lmp' pin_et='$etp' -> $v"
}
check g7581 'Mon, 19 Aug 2024 12:33:29 GMT' '"66c33b99-1e87000"'
check g7582 'Mon, 19 Aug 2024 12:36:33 GMT' '"66c33c51-1ec3000"'
check c6490 'Mon, 04 Sep 2023 17:07:51 GMT' '"64f60ee7-25e6800"'
check c6430 'Tue, 05 Sep 2023 09:10:35 GMT' '"64f6f08b-223f800"'
echo "== B. ETag size-hex -> decimal vs HEAD Content-Length and listing size =="
for h in 1e87000 1ec3000 25e6800 223f800; do
  printf 'HEX 0x%s = %d\n' "$h" "$((16#$h))"
done
echo "== C. attempt-1 located quote (7581 row) =="
strip() { sed -e 's/<[^>]*>//g' -e 's/  \+/ /g' "$1"; }
strip "$S/idx/fritzbox-7581.body" | grep -F 'FRITZ.Box_7581-07.18.image'
if strip "$S/idx/fritzbox-7581.body" | grep -F 'FRITZ.Box_7581-07.18.image' \
   | grep -F '19-Aug-2024 12:33' | grep -qF '32010240'; then
  echo "QUOTE_CONFIRMED name+date+size all present"
else
  echo "QUOTE_MISSING"
fi
echo "== D. pinned rows in each model index (tag-stripped) =="
strip "$S/idx/fritzbox-7581.body"       | grep -F 'FRITZ.Box_7581-07.18.image'
strip "$S/idx/fritzbox-7582.body"       | grep -F 'FRITZ.Box_7582-07.18.image'
strip "$S/idx/fritzbox-6490-cable.body" | grep -F 'FRITZ.Box_6490_Cable-07.57.image'
strip "$S/idx/fritzbox-6430-cable.body" | grep -F 'FRITZ.Box_6430_Cable-07.30.image'
echo "== E. base index lists the four model dirs =="
for m in fritzbox-7581 fritzbox-7582 fritzbox-6490-cable fritzbox-6430-cable; do
  grep -oE "<a href=\"$m/\">$m/</a>[^<]*" "$S/idx/base.body" | sed -e 's/<[^>]*>//g' -e 's/  \+/ /g'
done
echo "== F. listing size vs HEAD Content-Length equality =="
lsize() { strip "$1" | grep -F "$2" | awk '{print $NF}'; }
echo "g7581 listing=$(lsize "$S/idx/fritzbox-7581.body" 'FRITZ.Box_7581-07.18.image') head=$(hval "$S/head/g7581.hdr" 'content-length')"
echo "g7582 listing=$(lsize "$S/idx/fritzbox-7582.body" 'FRITZ.Box_7582-07.18.image') head=$(hval "$S/head/g7582.hdr" 'content-length')"
echo "c6490 listing=$(lsize "$S/idx/fritzbox-6490-cable.body" 'FRITZ.Box_6490_Cable-07.57.image') head=$(hval "$S/head/c6490.hdr" 'content-length')"
echo "c6430 listing=$(lsize "$S/idx/fritzbox-6430-cable.body" 'FRITZ.Box_6430_Cable-07.30.image') head=$(hval "$S/head/c6430.hdr" 'content-length')"
