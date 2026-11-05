# ScoutS319 — independent non-author re-open of the S319 source (Python `json` docs) and host probes

Seat: `ScoutS319` (scout). Lane: `kaidoku`, round 94, attempt 1.
Declaration commit read: `dd4524916a0332bb65f83525532da1c1b8d709de` (base `8a40ceb6516bb38c19c37bcbff2bb3332f31c832`).
Lane is READ-ONLY for this seat: nothing outside this seat directory was written; all counters/probes ran in
`/fast/scratch/hyaku/kaidoku-r94/ScoutS319` (clone at the declaration commit) and a scratch clone.

Scope of this seat: (1) re-fetch the S319 source and compare to the Gate sha; (2) locate the Gate's quote with its
section heading and anchor and note the page's Python version label; (3) host probes of the `default` hook on
`python3`; (4) a per-row verdict. No edits, no lane mutations, no subagent dispatch (leaf seat).

---

## 1 — Source re-fetch

Command lines (run from scratch, absolute paths):

```
mkdir -p /fast/scratch/hyaku/kaidoku-r94/ScoutS319/tmp
cd /fast/scratch/hyaku/kaidoku-r94/ScoutS319
curl -fsSL -D headers.txt -o json2.html -w '%{http_code} %{size_download}\n' \
  https://docs.python.org/3/library/json.html          # exit 0
curl -fsSL -o json.html -w '%{http_code} %{size_download}\n' \
  https://docs.python.org/3/library/json.html           # exit 0
sha256sum json.html json2.html
```

Observed:

| item | value |
|---|---|
| HTTP status | `200` (both fetches) |
| byte size | `116296` (both fetches; `content-length: 116296` in `headers.txt`) |
| sha256 (fetch 1) | `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0` |
| sha256 (fetch 2) | `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0` |
| `last-modified` | `Thu, 05 Nov 2026 12:49:35 GMT` |

**Gate sha256** (from `.ufo/waves/round-94/claims.json` → `sourced_claim.sha256`, and
`plans/round-94-claims.md` → "Sourced claim (frontier step)"):
`8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0`.

**The Gate's sha MATCHES** — byte-for-byte, on two independent fetches made 2026-11-05 (the recorded
`opened` date). The page bytes have not drifted since the Gate opened the source.

---

## 2 — The quote: location, heading, anchor, version label

The Gate's quoted string (claims.json `sourced_claim.quote`, plans/round-94-claims.md line 105) is:

> It should return a JSON encodable version of the object or raise a TypeError.

### 2.1 It is NOT a contiguous raw byte substring

```
python3 -c 's=open("json.html").read(); print(s.count(q))'   # q = the Gate quote
→ 0
```

Raw contiguous occurrences: **0**. Reason (observed in the source bytes): the sentence is line-wrapped
(`...of the object\nor raise a ...`) and `TypeError` is wrapped in Sphinx cross-reference markup:

```html
It should return a JSON encodable version of the object
or raise a <a class="reference internal" href="../builtins/exceptions.html#TypeError" title="TypeError"><code class="xref py py-exc docutils literal notranslate"><span class="pre">TypeError</span></code></a>.
```

### 2.2 After tag-strip + whitespace normalisation it is EXACT, twice

```
python3 - <<'EOF'
import re, html
s = open('json.html', encoding='utf-8').read()
plain = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s)))
q = "It should return a JSON encodable version of the object or raise a TypeError."
print(plain.count(q))          # → 2
EOF
```

Both occurrences, with their nearest section heading and anchor:

| # | raw offset / line in `json.html` | nearest `<h2>` section heading | nearest `<dt id=…>` anchor | containing text |
|---|---|---|---|---|
| 1 | 43313 / line 426 | **Basic Usage** (`id="basic-usage"`) | **`id="json.dump"`** (line 373) | the `default` parameter bullet of `json.dump(obj, fp, …)`: *“default (callable \| None) – A function that is called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a TypeError. If None (the default), TypeError is raised.”* |
| 2 | 82572 / line 749 | **Encoders and Decoders** (`id="encoders-and-decoders"`) | **`id="json.JSONEncoder"`** (line 668) | the `json.JSONEncoder` class description: *“If specified, default should be a function that gets called for objects that can’t otherwise be serialized. It should return a JSON encodable version of the object or raise a TypeError. If not specified, TypeError is raised.”* |

### 2.3 Anchor verification

`grep -n -o -E 'id="json\.(dump|dumps|JSONEncoder)"' json.html` →

```
373:id="json.dump"
456:id="json.dumps"
668:id="json.JSONEncoder"
```

`id="json.dump"` **is present** and is the anchor that contains occurrence 1.

**Correction to the item's premise (for the L1):** the sentence does **not** appear under `json.dumps`.
The `json.dumps` block (line 456) contains only *“Serialize obj to a JSON formatted str using this conversion table. The arguments have the same meaning as in dump().”* The `default`-hook sentence lives under `json.dump` (parameter list) and `json.JSONEncoder` (class description). A registry row that anchors this quote to `json.dumps` would be mis-anchored; the correct anchors are `json.dump` and/or `json.JSONEncoder`.

### 2.4 Page's Python version label

```
grep -o -E '<title>[^<]*</title>' json.html
→ <title>json — JSON encoder and decoder &#8212; Python 3.15.2 documentation</title>
```

**Page label: `Python 3.15.2 documentation`.** The URL `https://docs.python.org/3/library/json.html` is the
*current-stable alias*, not a pinned version — so the page bytes at this URL drift with each Python release.
Cross-check on pinned version URLs (fetched today, HTTP 200):

| URL | sha256 | page label | Gate sentence (normalized) |
|---|---|---|---|
| `/3/library/json.html` | `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0` | 3.15.2 | 2 occurrences |
| `/3.14/library/json.html` | `45dde67b649925d62297248d0c7f0597f287021a5546ad3daa13fa190f88d870` | 3.14.10 | 2 occurrences |
| `/3.13/library/json.html` | `f2e17fb3ae2eb9c04261a84022b3a1f978c846043aa33edaab1effae6881da3b` | 3.13.18 | 2 occurrences |

The sentence is **version-stable wording** across 3.13/3.14/3.15; only the page bytes drift.

### 2.5 Curation risk on the registry row (flagged, not decided)

- `corpus/SOURCES.md` **already holds this exact URL**: row **S050** — “Python JSON library documentation —
  https://docs.python.org/3/library/json.html”, anchor *“Python 3.15.0 documentation, Standard Compliance and
  Interoperability; Repeated Names Within an Object”*, opened 2026-10-21, used-by `corpus/lessons/round-21.md`.
- **Observed drift**: S050's recorded label is **Python 3.15.0**; the same URL now serves **3.15.2** (today's
  `last-modified` 2026-11-05). The unversioned `/3/` alias has already moved under S050.
- Lane precedent for a repeat URL: **S300** was *rejected* (“duplicate admission of the same scope already held
  by S286”) and **S303** *rejected* (“the registry already holds this URL in five scopes”); the accepted flip is
  *“a materially distinct proposition supported by a newly opened locator.”*
- **Consequence for the L1/Scribe**: S319 is a materially distinct proposition (the `default`-hook contract) with a
  distinct anchor (`json.dump` / `json.JSONEncoder`) and a distinct locator (sha + today's date), so it is
  admissible — but it must be scoped as a distinct proposition and **must not** be a bare re-add of S050's URL
  with S050's anchor, and it should carry a recheck that anticipates `/3/` alias drift.
- **Id space is free**: the highest existing id in `corpus/SOURCES.md` is **S318** (`grep -o -E '^\| S[0-9]{3} \|'`
  → tail `S316|S317|S318`); `grep -c -E '^\| S319 \|' corpus/SOURCES.md` → 0. No S319 collision.

---

## 3 — Host probes (`python3`, no lane writes)

Interpreter (observed):

```
command -v python3   → /usr/bin/python3     (symlink → python3.14)
python3 -V           → Python 3.14.8
sys.version          → 3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]
```

Probes run as `python3 -I -B <script>` / `python3 -I -c …`; each case run in an isolated subprocess so exit codes
are the case's own exit code (`receipts/probes.py`, `receipts/probes.out`, `receipts/probes2.py`,
`receipts/probes2.out`).

### 3.1 The three requested probes

| probe | command (exact) | exit | stdout | stderr |
|---|---|---|---|---|
| (a) bytes, no `default` | `python3 -I -c 'import io,json; json.dump({"x": b"a"}, io.StringIO())'` | **1** (uncaught `TypeError` → process exit 1) | `TypeError: Object of type bytes is not JSON serializable` (captured via `except TypeError` + `raise SystemExit(1)`) | — |
| (b) `default` returns a length dict | `python3 -I -c 'import io,json; json.dump({"x": b"a"}, io.StringIO(), default=lambda o: {"bytes": len(o)}); print("OK")'` | **0** | `OK` | — |
| (c) `default` returns `str(o)` (the fallback the v4 writer refuses) | `python3 -I -c 'import io,json; json.dump({"x": object()}, io.StringIO(), default=lambda o: str(o)); print("OK")'` | **0** | `OK` (receipt value `{"x": "<object object at 0x…>"}`) | — |

Exact message check for (a): the stdlib message is **`Object of type bytes is not JSON serializable`** — the
Gate/v4-relevant substring is present verbatim, including the word `not`. (One earlier combined-shell run
displayed the same line with `not` elided by output interleaving; the isolated authoritative run above has it,
and it also matches the v3 crash message recorded in `corpus/lessons/round-93.md` M93-e and in
`corpus/lessons/round-93-verifier-spotcheck.md` line 27.)

**Contrast recorded as required:** (c) proves the `str()` fallback *would* succeed — the v4 writer's refusal of
`str()` is a deliberate stricter rule, not a stdlib requirement.

### 3.2 Additional probes (calibration of the quote's force)

| probe | what it does | exit | outcome |
|---|---|---|---|
| (d) `default` returns **bytes** (non-encodable) for `object()` | `default=lambda o: b"x"` | **12** | **`ValueError: Circular reference detected`** — *not* `TypeError` |
| (f) `default` raises `TypeError` explicitly | `def d(o): raise TypeError("Cannot serialize object of %s" % type(o).__name__)` | **1** | `TypeError: Cannot serialize object of object` (propagates cleanly) |
| (g) `default` returns a dict that still holds an unserializable object | `default=lambda o: {"k": object()}` | **1** (uncaught `RecursionError` → process exit 1; a separate `except BaseException` rerun reports exit **3**, `EXC_TYPE: RecursionError`, `EXC_MSG: maximum recursion depth exceeded`) | **`RecursionError: maximum recursion depth exceeded`** |
| (h) no `default`, `object()` value | `json.dump({"x": object()}, io.StringIO())` | **1** | `TypeError: Object of type object is not JSON serializable` |

**Calibration finding:** the stdlib does **not** enforce the "must return an encodable value" half of the quoted
sentence. A `default` hook that returns a non-encodable value yields `ValueError` (d) or `RecursionError` (g), not
`TypeError`. The quote states a **requirement on the hook author**; it is a contract the writer adopts, not an
enforced runtime behaviour. The v4 writer satisfies it by *raising* `TypeError` for every unknown type (probe f
is the shape v4 uses).

---

## 4 — The same source exercised through the actual v4 counter (declaration commit)

Clone (scratch only, not the lane):

```
git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
git -C "$S/clone" checkout -q dd4524916a0332bb65f83525532da1c1b8d709de
git -C "$S/clone" rev-parse --show-toplevel   # → /fast/scratch/hyaku/kaidoku-r94/ScoutS319/clone  ✔ fixture assertion
git -C "$S/clone" rev-parse HEAD              # → dd4524916a0332bb65f83525532da1c1b8d709de
```

`receipts/v4_hook_probe.py` (run `python3 -I -B`, `TMPDIR=$S/tmp`, exit 0) — the v4 `_default` and
`write_receipt` on this host:

```
v4 _default on bytes: {'bytes': 3, 'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}
v4 _default on object(): TypeError: Cannot serialize object of <class 'object'>
json.dump via v4 hook OK: {"fresh_cells": [{"output": {"bytes": 3, "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}}]}
str() fallback succeeds (contrast): {"x": "<object object at 0x7fa47e5808b0>"}
receipt exists: True | tmp left: False
reparse: {'bytes': 3, 'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}
write_receipt unknown type: TypeError: Cannot serialize object of <class 'object'>
bad receipt exists: False | bad tmp left: False
```

`receipts/v4_hook_probe2.py` (exit 0): the success path leaves a **complete, re-parseable** receipt and **no**
`.tmp`; the failure path leaves **neither** a receipt nor a `.tmp`. This independently confirms the QUALITY-189
keyword **“complete JSON or absent”** on this host.

`receipts/v3_crash.py` (exit 0, prints `TypeError: Object of type bytes is not JSON serializable`): reproduces the
M93-e mechanism directly — `tools/round-93/stop-boundary-repair-battery-v3.py:353` calls
`json.dump(receipt, fh, indent=1, sort_keys=True)` with **no** `default=`, so `fresh_cells[*].output` bytes
raise `TypeError` mid-write, leaving the truncated receipt.

### Frozen pin check (all read-only, at the declaration commit)

`sha256sum` over the lane files — **every frozen pin in `claims.json` matches**:

| file | observed sha256 | claims.json pin |
|---|---|---|
| `tools/round-94/stop-boundary-repair-battery-v4.py` | `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272` | same ✔ |
| `tools/round-94/c1-receipt-agreement.py` | `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9` | same ✔ |
| `tools/round-93/stop-boundary-repair-battery-v3.py` | `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3` | same ✔ |
| `tools/round-92/stop-boundary-repair-battery.py` | `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc` | same ✔ |
| `tools/round-92/stop-boundary-battery-v2.py` | `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874` | same ✔ |
| `tools/round-93/craft-citation-semantic.py` | `34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340` | same ✔ |
| `tools/round-89/depth-blocks-v2.py` | `359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f` | same ✔ |
| `tools/round-91/depth-blocks-v3.py` | `bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f` | same ✔ |
| `.ufo/waves/round-94/manifests/block33-after.json` | `9d72f9951d7aadf12a335b2e2177bcb7a7300c5c8c4f481640f9c721751f40ae` | same ✔ |

---

## 5 — Verdict per row

| row | question | verdict | evidence |
|---|---|---|---|
| V1 | Does the Gate's located quote appear **verbatim** in the fetched page? | **YES, after tag-strip + whitespace normalisation (2 occurrences); NO as a raw contiguous byte substring** (markup + line wrap). The Gate's wording is otherwise exact — no word differs. | §2.1–2.2; `receipts/probes.out`/`json.html` line 426 and 749 |
| V2 | Does the Gate's sha256 match? | **YES, exactly** — `8021264aedd0ae972ac10cc3ba950be85d95b62d4869289b4686bad62b9794c0`, twice, 116 296 bytes, HTTP 200, `last-modified` 2026-11-05 | §1 |
| V3 | Does the probe support “a default hook must return an encodable value or raise”? | **PARTLY.** The "return an encodable value" half is **not enforced by the stdlib**: a hook returning non-encodable data yields `ValueError` (d) / `RecursionError` (g), not `TypeError`. The "or raise" half is real: an explicit `TypeError` from the hook propagates (f), and with no hook at all the stdlib raises `TypeError: Object of type bytes is not JSON serializable` (a, h). A hook returning an encodable value works (b). The quoted sentence is a **requirement on the hook author**, which v4 adopts by raising `TypeError` for every unknown type — it is not a runtime guarantee the probe could show. | §3.1–3.2, §4 |
| V4 | Is the source anchored correctly? | **Partly.** `id="json.dump"` exists and holds the sentence (occurrence 1). The sentence is **not** under `json.dumps`; it is under `json.dump` (parameter list) and `json.JSONEncoder` (class description). Anchor to `json.dump` and/or `json.JSONEncoder`, not `json.dumps`. | §2.2–2.3 |
| V5 | Version label | Page says **Python 3.15.2 documentation**; host interpreter is **3.14.8**. The quoted wording is identical in the pinned 3.13/3.14/3.15 pages, so the version gap does not affect the proposition. The `/3/` alias bytes drift (S050 already drifted 3.15.0 → 3.15.2). | §2.4 |
| V6 | Registry fit for S319 | Id **S319 is free** (max existing S318). The **URL is already in scope via S050** with a different anchor/proposition; per the lane's S300/S303 precedent the row must be scoped as a materially distinct proposition with a distinct locator, or it risks the same duplicate-URL rejection. | §2.5 |

**Bottom line for the L1:** the S319 source re-opens clean — the Gate's sha is exact and the quote is exact in
meaning and wording (raw-substring caveat noted). The two things a landing row/knowledge entry should get right:
(1) anchor the quote to `json.dump` / `json.JSONEncoder`, **not** `json.dumps`; (2) state the page label
(3.15.2) and that the quote is a **contract on the `default` hook author**, not a stdlib-enforced guarantee —
the v4 writer's stricter `TypeError`-for-unknown-types rule is a deliberate choice, and the `str()` fallback the
writer refuses would in fact succeed (probe c).

---

## Files written by this seat

- `.ufo/waves/round-94/w1/ScoutS319.md` (this report)
- `.ufo/waves/round-94/w1/ScoutS319/receipts/json.html` — fetched S319 page (116 296 B, sha `8021264a…`)
- `.ufo/waves/round-94/w1/ScoutS319/receipts/json2.html` — second independent fetch (identical sha)
- `.ufo/waves/round-94/w1/ScoutS319/receipts/headers.txt` — response headers
- `.ufo/waves/round-94/w1/ScoutS319/receipts/json-3.14.html`, `json-3.13.html` — pinned-version comparison pages
- `.ufo/waves/round-94/w1/ScoutS319/receipts/probes.py`, `probes.out` — probes (a)(b)(c) + interpreter facts
- `.ufo/waves/round-94/w1/ScoutS319/receipts/probes2.py`, `probes2.out` — probes (d)(f)(g)(h)
- `.ufo/waves/round-94/w1/ScoutS319/receipts/v3_crash.py` — M93-e mechanism reproduction
- `.ufo/waves/round-94/w1/ScoutS319/receipts/v4_hook_probe.py`, `v4_hook_probe2.py` — v4 `_default` / `write_receipt` on host
- `.ufo/waves/round-94/w1/ScoutS319/receipts/pins-sha256.txt` — frozen pin check output

Scratch dir `/fast/scratch/hyaku/kaidoku-r94/ScoutS319` removed after copying receipts (including its `clone/`).
No lane file outside this seat directory was created, edited or deleted; no mutating git/jj command was run in the
lane (`git log/show/status/rev-parse` only). No tool was installed or upgraded (curl, python3 3.14.8 and git were
already present).
