# connect-dart-symbols — author-side receipts (KaidokuR23.ConnectDartSymbols)

Status: author-side probe receipts, **not** outside verification and **not** an
admission. L1 owns integration and any R23-C1 counting.

These receipts exist to connect the R22 Saber `inspect-dart-aot` refusal
(`.ufo/waves/round-22/evidence/c1/inspect-dart-aot-saber.*`, source S055) to the
exact contract that REA 6.5.0 applies, and to a carrier generation that
satisfies it.

| file | sha256 | what |
|---|---|---|
| `inspect-dart-aot-saber-1330203.envelope.json` | `7ee2c3c0b9254e1f1c96a78b43fdf7023f4d206eab74543df30fe7d2a2ab84c1` | exact stdout, exit 0 |
| `inspect-dart-aot-saber-1330203.run.json` | `4b263db8e6060a659f1cf81aab3df025b4014afecdd59258464d57351fe7938d` | argv/env/exit/target sha256 |
| `inspect-dart-aot-saber-1340303.envelope.json` | `22d1acd01c8dcb71d0bc63bf516e23114e25ef1615b790cf621b9631ebb7c69d` | corroborating run, exit 0 |
| `inspect-dart-aot-saber-1340303.run.json` | `34f4ab462e0df49d6f9ff476e619f6bf2e01da750824771da5c8e1e8f78b3db3` | argv/env/exit/target sha256 |
| `identify-flutter-build-saber-1330203.envelope.json` | `3d56fe45b4a3d0428091128229e41c6a9fbc686180b3a1ac66fe0c24c56b9626` | same carrier, coverage complete |
| `identify-flutter-build-saber-1330203.run.json` | `9660b55cc8ed0046f67adace0e75636777c2696e5b111f5b918f9fe196b8cd60` | argv/env/exit/target sha256 |
| `carriers.json` | `652f05a626078250f617f7f4f3b5d64ca56d286b8654137757a5009ba983f2c6` | 3-carrier ELF matrix (dynsym, headers, Dart strings) |
| `fetch.json` | `6beac67b0f6361accc59729c969965b9b8f0f777f5beaca7dd1ed65b11566f2d` | archive URLs, index entries, sha256 matches |
| `preflight_dart_carrier.py` | `08d0c4605c41f6b091d5b5d09172c5254eaf3bbffa8bf8bcf5f5c7b4b105514c` | offline gate predicate, exit 0/3/4/2 |

Reproduce the gate without REA (read-only; no APK execution):

```
python3 -I -B preflight_dart_carrier.py saber-1330203.apk   # exit 0, legacy-complete (Dart 3.11.4)
python3 -I -B preflight_dart_carrier.py saber-1340303.apk   # exit 0, legacy-complete (Dart 3.12.2)
python3 -I -B preflight_dart_carrier.py saber.apk           # exit 3, new-layout (Dart 3.13.2)
```

Artifacts (not retained here): F-Droid archive
`https://f-droid.org/archive/com.adilhanney.saber_1330203.apk`
sha256 `a7b1f5c8c077aafc8903eb8246d9b6f5fc8ebb4829dc5cb32bd2cdd8ba3ea618`.
