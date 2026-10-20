#!/usr/bin/env bash
# Round-18 synthetic carrier recipe (QUALITY #12: full regenerating recipe).
# Toolchains: official go.dev tarballs, sha256 checked against
# https://go.dev/dl/?mode=json&include=all (go1.24.6 bbca37cc…8712, go1.25.0 2852af0c…b613),
# unpacked to ~/.local/opt/go-<ver>. Builds 12 carriers = {1.24.6,1.25.0} x {swiss,noswiss} x {methods,nomethods,nethttp}
# (nethttp added at round-18 wave-1 integration after CriticC3: the methods/nomethods pair
# is predicted non-diagnostic; nethttp carries aether's 40-byte-slot named maps)
# into ${OUT:-bin}/ and prints "<sha256>  <file>". Never executes a carrier.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out=${OUT:-$here/bin}
mkdir -p "$out"
cache=$(mktemp -d /tmp/kr18-gocache.XXXXXX)
trap 'chmod -R u+w "$cache"; rm -rf "$cache"' EXIT
for ver in 1.24.6 1.25.0; do
  GO=$HOME/.local/opt/go-$ver/bin/go
  for layout in swiss noswiss; do
    exp=""; [ "$layout" = noswiss ] && exp=noswissmap
    for prog in methods nomethods nethttp; do
      name=s${ver//./}-$layout-$prog
      ( cd "$here/src/$prog" && env -i HOME="$HOME" PATH=/usr/bin:/bin GOTOOLCHAIN=local GOFLAGS= \
          CGO_ENABLED=0 GOOS=linux GOARCH=amd64 GOAMD64=v1 GOEXPERIMENT="$exp" \
          GOCACHE="$cache/c" GOPATH="$cache/p" GOENV=off \
          "$GO" build -trimpath -buildvcs=false -o "$out/$name" . )
    done
  done
done
cd "$out" && sha256sum s1*
