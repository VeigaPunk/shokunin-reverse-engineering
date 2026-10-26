# Verbatim envelope excerpts (generated from summary.json)

Each block is one REA 6.5.0 `extract-firmware` envelope reduced to the members the
triage features read. Full envelopes: `envelopes/<case>/envelope.json`.

## `sh-alone-le-d1` — max_depth 1, le, carrier sha256 `e012483818951f64c5ecdbaf318dcbc26ca96b9f4ed143caf9d350a969227a2b`

- features: `H=['squashfs_v4_le'] G=['depth-limited'] D=[] BE=n/a SR=no P=3` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract']`
- chunks: [('$input', 'squashfs_v4_le', False)]
- diagnostics: []
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `None` | `None` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `depth-limited-nested`

## `sh-intree-le-d1` — max_depth 1, le, carrier sha256 `ac500aa5bb0036ed0218be8aa1d6ea73ef6122bd60f0d4b2f6e9a87c1d9dbd5e`

- features: `H=['squashfs_v4_le'] G=['depth-limited', 'unpublished-entry'] D=[] BE=n/a SR=no P=3` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract']`
- chunks: [('$input', 'squashfs_v4_le', False)]
- diagnostics: []
- unpublished entries: [('firmware.bin_extract/etc/link_rel', 'symlink', '../usr/share/data.bin')]

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/etc/link_rel",
      "kind": "unpublished-entry",
      "provider_id": null,
      "range": null,
      "relative_path": "firmware.bin_extract/etc/link_rel",
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `None` | `None` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `depth-limited-nested`

## `sh-escaping-le-d1` — max_depth 1, le, carrier sha256 `5af64ea2bc6d0d2c42cb0fbfc83e360edb831b369a5658a0468a9828ec02d281`

- features: `H=['squashfs_v4_le'] G=['depth-limited'] D=[] BE=n/a SR=yes P=3` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract']`
- chunks: [('$input', 'squashfs_v4_le', False)]
- diagnostics: [('$input', 'MaliciousSymlinkRemoved')]
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `None` | `None` |

- v2 interpreter: `escaping-symlink-removed` / `expect-link-absent` (rule 8); draft-v3 transcription: `depth-limited-nested`

## `sh-both-le-d1` — max_depth 1, le, carrier sha256 `5e079ec78bedd56f73c9920b3e468e223504e83c58d56535bc1720bef9a90ad0`

- features: `H=['squashfs_v4_le'] G=['depth-limited', 'unpublished-entry'] D=[] BE=n/a SR=yes P=3` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract']`
- chunks: [('$input', 'squashfs_v4_le', False)]
- diagnostics: [('$input', 'MaliciousSymlinkRemoved')]
- unpublished entries: [('firmware.bin_extract/etc/link_rel', 'symlink', '../usr/share/data.bin')]

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/etc/link_rel",
      "kind": "unpublished-entry",
      "provider_id": null,
      "range": null,
      "relative_path": "firmware.bin_extract/etc/link_rel",
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `None` | `None` |

- v2 interpreter: `escaping-symlink-removed` / `expect-link-absent` (rule 8); draft-v3 transcription: `depth-limited-nested`

## `sh-alone-le-d3` — max_depth 3, le, carrier sha256 `e012483818951f64c5ecdbaf318dcbc26ca96b9f4ed143caf9d350a969227a2b`

- features: `H=['squashfs_v4_le'] G=[] D=[] BE=n/a SR=no P=5` OP=`extract_firmware` PV=`unblob`
- `coverage`: `complete`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `[]`
- chunks: [('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_le', False), ('$input', 'squashfs_v4_le', False)]
- diagnostics: []
- unpublished entries: []

```json
{
  "extraction_gaps": []
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `2` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `clean` / `none` (rule 10); draft-v3 transcription: `clean`

## `tw-two-le-d2` — max_depth 2, le, carrier sha256 `a48437bb543409624ed8938b5893b3dcd40e15ef77f6cc51a80ef4d29f3fe9e6`

- features: `H=['squashfs_v4_le'] G=['depth-limited'] D=[] BE=n/a SR=no P=8` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner_a.sqsh_extract', '$output/firmware.bin_extract/inner_b.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/inner_a.sqsh', 'squashfs_v4_le', False), ('$output/firmware.bin_extract/inner_b.sqsh', 'squashfs_v4_le', False), ('$input', 'squashfs_v4_le', False)]
- diagnostics: []
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner_a.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner_b.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner_a.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `1` |
| `firmware.bin_extract/inner_a.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner_a.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner_b.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `1` |
| `firmware.bin_extract/inner_b.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner_b.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `depth-limited-nested`

## `lk-links-le-d3` — max_depth 3, le, carrier sha256 `70b90751bc7ea546e4144ce3324bdee272e7a1a2b4e1bde8b5d17fb7ccfb7d0f`

- features: `H=['squashfs_v4_le'] G=['depth-limited', 'unpublished-entry'] D=[] BE=n/a SR=yes P=7` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh', 'squashfs_v4_le', False), ('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_le', False), ('$input', 'squashfs_v4_le', False)]
- diagnostics: [('$output/firmware.bin_extract/inner.sqsh', 'MaliciousSymlinkRemoved')]
- unpublished entries: [('firmware.bin_extract/inner.sqsh_extract/mid/keep_link', 'symlink', 'note.txt')]

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/mid/keep_link",
      "kind": "unpublished-entry",
      "provider_id": null,
      "range": null,
      "relative_path": "firmware.bin_extract/inner.sqsh_extract/mid/keep_link",
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1385 | `8a46c233bc2f3a626827703889c6fb565b1c5254a4286815ba9de32e6beac97e` | `8a46c233bc2f3a626827703889c6fb565b1c5254a4286815ba9de32e6beac97e` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/mid/note.txt` | 12 | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `2` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `escaping-symlink-removed` / `expect-link-absent` (rule 8); draft-v3 transcription: `depth-limited-nested`

## `pf-partial-le-d3` — max_depth 3, le, carrier sha256 `cee67d2e09c28ad224f2010d1e3d364586f5d2b410459492b51cfe03e9c897ae`

- features: `H=['squashfs_v4_le'] G=['depth-limited', 'extractor-failure'] D=[] BE=no SR=no P=8` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/damaged.sqsh', 'squashfs_v4_le', True), ('$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh', 'squashfs_v4_le', False), ('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_le', False), ('$input', 'squashfs_v4_le', False)]
- diagnostics: [('$output/firmware.bin_extract/damaged.sqsh', 'ExtractCommandFailedReport')]
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "7bca61a18c2e24f811bce926abefe387b4e009310796c1962f95828397e96f76",
      "dependencies": [],
      "handler": "squashfs_v4_le",
      "input_path": "$output/firmware.bin_extract/damaged.sqsh",
      "kind": "extractor-failure",
      "provider_id": "841595:2",
      "range": {
        "length": 1098,
        "offset": 0
      },
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/damaged.sqsh` | 1098 | `9a6d5edb3f4d4ba72b0c7d1d0c5fa1a6344aa7adf5533a748b05212bf6a6da87` | `9a6d5edb3f4d4ba72b0c7d1d0c5fa1a6344aa7adf5533a748b05212bf6a6da87` | `1` |
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1276 | `d6756de801c696d3bc787943728f2acabfdab25d403e83813edd6ca481634d18` | `d6756de801c696d3bc787943728f2acabfdab25d403e83813edd6ca481634d18` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/mid/note.txt` | 12 | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `2` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `partial-body-failure`

## `pf-partial-be-d3` — max_depth 3, be, carrier sha256 `c1e21a36e8f48fa58434394379810b79f6d8d9b922581c10c224d93fdc73f482`

- features: `H=['squashfs_v4_be'] G=['depth-limited', 'extractor-failure'] D=[] BE=yes SR=no P=8` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/damaged.sqsh', 'squashfs_v4_be', True), ('$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh', 'squashfs_v4_be', False), ('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_be', False), ('$input', 'squashfs_v4_be', False)]
- diagnostics: [('$output/firmware.bin_extract/damaged.sqsh', 'ExtractCommandFailedReport')]
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "7bca61a18c2e24f811bce926abefe387b4e009310796c1962f95828397e96f76",
      "dependencies": [],
      "handler": "squashfs_v4_be",
      "input_path": "$output/firmware.bin_extract/damaged.sqsh",
      "kind": "extractor-failure",
      "provider_id": "1101255:2",
      "range": {
        "length": 1098,
        "offset": 0
      },
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/damaged.sqsh` | 1098 | `e13a347f88ced5d6db60635e4f83d4542dd7c187336f6be36996d394800dc608` | `e13a347f88ced5d6db60635e4f83d4542dd7c187336f6be36996d394800dc608` | `1` |
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1272 | `0ec9e359d68add30b697d77a831e3acd996399a8a8e8f4eed69d0a748aeb5e3b` | `0ec9e359d68add30b697d77a831e3acd996399a8a8e8f4eed69d0a748aeb5e3b` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh` | 1098 | `b0deb46379ce2b311b2204d86a7917ea2ba737684dc02fdd8ff2cffefdaff524` | `b0deb46379ce2b311b2204d86a7917ea2ba737684dc02fdd8ff2cffefdaff524` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/mid/note.txt` | 12 | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `2` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `partial-body-failure`

## `ta-tail-le-d3` — max_depth 3, le, carrier sha256 `904f9f00045bfbe54d3bb304ae56a1ea3ebf23455347138c58107fba44a74556`

- features: `H=['squashfs_v4_le'] G=['depth-limited', 'unknown-chunk-handler'] D=[] BE=n/a SR=no P=11` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh', 'squashfs_v4_le', False), ('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_le', False), ('$output/firmware.bin_extract/padded.sqsh', None, False), ('$output/firmware.bin_extract/padded.sqsh', 'squashfs_v4_le', False), ('$input', 'squashfs_v4_le', False)]
- diagnostics: []
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    },
    {
      "continuation_id": "51021a447b385197d243985f86ffccfe122a26eb1618932f8ae0f707483cd8d7",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/padded.sqsh",
      "kind": "unknown-chunk-handler",
      "provider_id": "869708:5",
      "range": {
        "length": 4096,
        "offset": 1098
      },
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1276 | `d6756de801c696d3bc787943728f2acabfdab25d403e83813edd6ca481634d18` | `d6756de801c696d3bc787943728f2acabfdab25d403e83813edd6ca481634d18` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh` | 1098 | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `78098cf4de2d4ffb11ff1368097064ba05b78d56088ae90909258581b96e5bb6` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/mid/note.txt` | 12 | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `2` |
| `firmware.bin_extract/padded.sqsh` | 5194 | `9702f3c6e0368bf498ea3aef8ebeb93c4706a486a0fb4b69931a35615b18f0df` | `9702f3c6e0368bf498ea3aef8ebeb93c4706a486a0fb4b69931a35615b18f0df` | `1` |
| `firmware.bin_extract/padded.sqsh_extract/0-1098.squashfs_v4_le_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `2` |
| `firmware.bin_extract/padded.sqsh_extract/0-1098.squashfs_v4_le_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `2` |
| `firmware.bin_extract/padded.sqsh_extract/1098-5194.unknown` | 4096 | `9155cce97849dbe63fc23c947eaad214d1779415a30437c17e48ca99d8c4c675` | `None` | `None` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `depth-limited-nested`

## `dp-alone-be-d3` — max_depth 3, be, carrier sha256 `2b714618b45d9e81990efe0400c5927f5b0fd4409ad931b965f9e281c3cbec11`

- features: `H=['squashfs_v4_be'] G=['depth-limited'] D=[] BE=n/a SR=no P=7` OP=`extract_firmware` PV=`unblob`
- `coverage`: `partial`; `ok`: `True`; REA exit `0`; subject digest matches carrier: `True`
- `depth_limited_paths`: `['$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract']`
- chunks: [('$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh', 'squashfs_v4_be', False), ('$output/firmware.bin_extract/inner.sqsh', 'squashfs_v4_be', False), ('$input', 'squashfs_v4_be', False)]
- diagnostics: []
- unpublished entries: []

```json
{
  "extraction_gaps": [
    {
      "continuation_id": "3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab",
      "dependencies": [],
      "handler": null,
      "input_path": "$output/firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract",
      "kind": "depth-limited",
      "provider_id": null,
      "range": null,
      "relative_path": null,
      "root_file_range": null
    }
  ]
}
```

| published relative_path | size | sha256 | reported_sha256 | analysis_depth |
|---|---|---|---|---|
| `firmware.bin_extract/etc/banner.txt` | 16 | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `2345ab04619f66b5c7ff36e6b58d8a6329b1dbe7a1c35737896499bb86e2b103` | `1` |
| `firmware.bin_extract/inner.sqsh` | 1272 | `0ec9e359d68add30b697d77a831e3acd996399a8a8e8f4eed69d0a748aeb5e3b` | `0ec9e359d68add30b697d77a831e3acd996399a8a8e8f4eed69d0a748aeb5e3b` | `1` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh` | 1098 | `b0deb46379ce2b311b2204d86a7917ea2ba737684dc02fdd8ff2cffefdaff524` | `b0deb46379ce2b311b2204d86a7917ea2ba737684dc02fdd8ff2cffefdaff524` | `2` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/deep/leaf.bin` | 700 | `412b77784c8b83fc7884247161d33a76b3d9b4ea46dedaad6eded7e628b19840` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/inner2.sqsh_extract/payload/hello.txt` | 20 | `df445dded9682a9b848401947cc9e04a2203fab8484f127c5c1ebbd09d1d352b` | `None` | `None` |
| `firmware.bin_extract/inner.sqsh_extract/mid/note.txt` | 12 | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `ff8f02e226c4fad6ce1334f5227c2ffaa974d97b0305762a16b97914f4451941` | `2` |
| `firmware.bin_extract/usr/share/data.bin` | 2048 | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `67225248192204e09b2d32b57ad6ae0e4ef7775b75ccae9adaba04b6ebca1c34` | `1` |

- v2 interpreter: `unclassified` / `none` (rule None); draft-v3 transcription: `depth-limited-nested`

