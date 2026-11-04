# Round-80 source gate — L1's own openings (2026-11-04)

Snapshots (this round, L1): `.ufo/waves/round-80/l1/sources/`
| file | url | http | bytes | sha256 |
|---|---|---|---|---|
| `rfc8259.txt` | https://www.rfc-editor.org/rfc/rfc8259.txt | 200 | 28360 | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| `re.html` | https://docs.python.org/3/library/re.html | 200 | 257722 | `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6` |

## Admits

1. **RFC 8259, section 4 (Objects), line 322** — quote (8 words):
   "The names within an object SHOULD be unique."
   Located: `grep -n 'SHOULD be unique' rfc8259.txt` -> `322:`; section header `^4.  Objects` at line 316.
   Digestion: grounds the duplicate-cell refusal as an interoperability rule (SHOULD, not MUST), which is
   exactly the strength the lane claims: a record declaring one client twice is malformed for the lane's
   purposes, and the parser reports it instead of collapsing it.
2. **Python 3 `re` documentation, `\b`, line 747** — quote (14 words):
   "Matches the empty string, but only at the beginning or end of a word."
   Located: `grep -n 'Matches the empty string, but only at the beginning or end of a word' re.html` -> `747:`,
   under `<section id="b">` for the `\b` escape.
   Digestion: grounds the exact-token (delimited) match — a token binds only where both sides are word
   boundaries or line edges, so `rea-agents@6.7.0` cannot bind inside `rea-agents@6.7.05`.

## Rejects

1. **Wikipedia, "JSON"** (https://en.wikipedia.org/wiki/JSON), opened this round (snapshot in the wave dir,
   `w1/ScribeSources/wiki-json.html`, 478308 B). Located text: "JSON objects that contain multiple members with
   the same name. The behavior of implementations processing objects with duplicate names is unpredictable."
   Reason for reject: tertiary source, and the same article quotes ECMA-404 saying the syntax "does not
   require that name strings be unique" — as a row it would sit against the rule it appears to illustrate.
   Flip: admit only if a claim needs the grammar-versus-interoperability distinction as its evidence.
2. **Stack Overflow question on duplicate JSON keys** — opened (snapshot `w1/ScribeSources/so-dupkeys.html`,
   5753 B) and found to be a Cloudflare challenge page ("Just a moment..."), not the content. Class:
   `unreachable`, not fabrication. No row; retained as a rejected-to-open candidate.
