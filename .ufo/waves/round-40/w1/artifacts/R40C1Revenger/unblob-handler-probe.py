#!/usr/bin/env python3
"""Invoke unblob 26.6.4's own SquashFS handler code on one image.

Runs in the unblob uv-tool interpreter:
  /home/vgpnk/.local/share/uv/tools/unblob/bin/python

It calls SquashFSv4BEHandler.calculate_chunk (the chunk-boundary arithmetic)
and reproduces SquashFSExtractor.extract's endian/marker branch exactly
(unblob/handlers/filesystem/squashfs.py:33-56) without spawning sasquatch.
"""
import sys
from pathlib import Path

from unblob.file_utils import Endian, File, StructParser, get_endian
from unblob.handlers.filesystem.squashfs import (
    SquashFSv4BEHandler,
    SquashFSv4LEHandler,
)

path = Path(sys.argv[1])
handler = SquashFSv4BEHandler()
with File.from_path(path) as f:
    endian = get_endian(f, 0x73717368)
    chunk = handler.calculate_chunk(f, 0)
    print(f"magic-endian={endian}")
    print(f"chunk={chunk}")

with File.from_path(path) as f:
    struct_parser = StructParser(SquashFSv4LEHandler.C_DEFINITIONS)
    header = struct_parser.parse(
        SquashFSv4LEHandler.HEADER_STRUCT, f, Endian.BIG
    )
    is_avm = header.bytes_used == header.mkfs_time
    print(f"bytes_used={header.bytes_used} mkfs_time={header.mkfs_time} "
          f"is_avm={is_avm}")
    print(f"argv_tail={['-be'] if not is_avm else '[] (no -be)'}")
