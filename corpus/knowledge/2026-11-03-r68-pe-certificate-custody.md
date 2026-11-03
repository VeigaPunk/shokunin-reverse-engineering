source: S273, S274
verified-at: 2026-11-03

# PE certificate evidence, not signer trust

## Opened primary sources

S273 Microsoft PE Format, https://learn.microsoft.com/en-us/windows/win32/debug/pe-format, Optional Header Data Directories and Attribute Certificate Table, opened 2026-11-03. S274 WIN_CERTIFICATE, https://learn.microsoft.com/en-us/windows/win32/api/wintrust/ns-wintrust-win_certificate, Members, opened 2026-11-03 (page updated 2025-10-07). No full pages retained.

[OBSERVATION] PE's certificate directory uses a file position rather than the usual relative virtual address. The format page describes traversal by rounded entry lengths and requires the rounded total to equal the directory size. Later wording says the stored length includes padding. These statements do not license guessing where a DER object ends. The structure page identifies length, revision, type, and variable bytes; it does not make a parsed record a verified signature.

## Gate

Official format/API documentation -> tier A for layout declarations. Admit the directory exception and bounded record traversal. Reject the inference that structurally readable certificate bytes prove signer identity, chain trust, cryptographic integrity, or successful Windows loading.

## Craft

1. Bind the optional-header magic, declared optional-header extent, and directory count before reading directory4.
2. Use its stored file offset directly. Section RVA translation is the wrong coordinate system here.
3. Keep every record in physical order. Separate the bytes inside the declared length from any outside-length alignment bytes, retaining each digest and location.
4. Bound every addition and require exact table exhaustion. A zero or short length must not loop.
5. Label this a structural evidence profile. Cryptographic verification and DER interpretation are separate tasks.

[UNKNOWN] Authenticode integrity, signer identity, trust-store decisions, loader acceptance, full PE validity and semantic certificate content remain untested. The independent round68 contract declares conservative structural exclusions. Odd declared lengths are descriptive traversal support, not a declaration of complete WIN_CERTIFICATE conformance.
