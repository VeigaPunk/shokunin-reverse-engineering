#!/usr/bin/env bash
out="${@: -1}"
mkdir -p "$out/firmware.bin_extract/etc"
printf "motd\n" > "$out/firmware.bin_extract/etc/motd"
sleep 977 &
sleep 978
printf '{"data":{"operation":"extract_firmware","parameters":{"output_directory":"%s"}}}\n' "$out"
