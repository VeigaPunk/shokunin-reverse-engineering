# SubstanceDEADSEATRECORD

Axes: **calibration, freshness, depth**. Scope: C1 / R18-DEADSEAT-RECORD only. No production files were changed; the mutation tests ran in temporary clones and those clones were removed.

## Result and independent re-derivation

**Observation.** At inspection, `HEAD` and `refs/heads/main` were `279e8b19c51658bfd05b9e31a1c0894ab2e70537`; B is `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. I derived the expected report set from Git objects at the fixed cutoff `a245bb00c581ae3423a10a055c77d4bc873918df`, independently of `s_deadseat`:

```text
python3 -I -B -c 'import json,subprocess; R="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; A="a245bb00c581ae3423a10a055c77d4bc873918df"; G=lambda *a:subprocess.check_output(["git","--no-optional-locks","-C",R,*a],text=True); print([(wave,len(reg),len(have),sorted(set(reg)-have),sorted(have-set(reg))) for wave,sub in (("wave1","w1"),("wave2","w2")) for reg,have in [(json.loads(G("show",f"{A}:.ufo/waves/round-18/{wave}-registration.json"))["members"],{x[:-3] for x in G("ls-tree","--name-only",f"{A}:.ufo/waves/round-18/{sub}").splitlines() if x.endswith(".md")})]])'  # exit 0
```

Output: W1 `89 registered / 89 reports / missing=[] / extra=[]`; W2 `98 / 94`, missing exactly `GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines`, `TruthREGISTRY`, extra `[]`. This agrees with the append-only correction at `SCORECARD.md:2487` and `corpus/lessons/round-19.md:60` (current dirty lesson line 61); the old integration snapshot remains at `SCORECARD.md:2462`.

The retained evidence is at `.ufo/waves/round-19/evidence/r18-dead-seats.json:4-8,10-17,34,36-46,49-58,61-70`. I also compared each evidence `cause` and its cited source pointers against the JSON block in the immutable `4f6c73f81ae8d31de18377d7ff57e4e10140ce48:.ufo/waves/round-19/w1/DeadSeatHistoryR18.md` blob:

```text
python3 -I -B -c 'import json,re,subprocess; R="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; M="279e8b19c51658bfd05b9e31a1c0894ab2e70537"; H="4f6c73f81ae8d31de18377d7ff57e4e10140ce48"; G=lambda *a:subprocess.check_output(["git","--no-optional-locks","-C",R,*a],text=True); t=G("show",f"{H}:.ufo/waves/round-19/w1/DeadSeatHistoryR18.md"); b=re.search(r"```json\n(.*?)\n```",t,re.S); a={s["seat"]:s for s in json.loads(b.group(1))["seats"]}; e=json.loads(G("show",f"{M}:.ufo/waves/round-19/evidence/r18-dead-seats.json")); print([(s["name"],s["cause"]==a[s["name"]]["error_line"],all(p in s["source"] for p in a[s["name"]]["evidence"])) for s in e["seats"]])'  # exit 0
```

All four tuples were `(name, True, True)`. Thus I found no false open or false close on the unmodified B/main evidence: B correctly has all seven routed defects open; the actual main correction's four missing-report names and retained causes match the immutable repo records.

Commands and exits for the strict counter (executed against frozen revisions in an isolated clone):

```text
# committed-main tool blob ae1651db86bf3c1262025f624b392c4851f4cb42
python3 -I -B /tmp/kr19-w2-SubstanceDEADSEATRECORD-committed-uz6ij9ae/lane/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SubstanceDEADSEATRECORD-committed-uz6ij9ae/lane --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict  # exit 1; open_count=7; DEADSEAT named/substance=false
python3 -I -B /tmp/kr19-w2-SubstanceDEADSEATRECORD-committed-uz6ij9ae/lane/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SubstanceDEADSEATRECORD-committed-uz6ij9ae/lane --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict  # exit 0; open_count=0; DEADSEAT named/substance=true

# frozen snapshot of the then-current worktree tool, SHA-256 8d94f6095d8623314a9608a9ecb1c4635073c87c99fe2449f7837583e43c04640
python3 -I -B /tmp/kr19-w2-SubstanceDEADSEATRECORD-frozen-xb7c_t16/routed-r18-observed.py --root /tmp/kr19-w2-SubstanceDEADSEATRECORD-frozen-xb7c_t16/lane --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict  # exit 1; open_count=7; DEADSEAT named/substance=false
python3 -I -B /tmp/kr19-w2-SubstanceDEADSEATRECORD-frozen-xb7c_t16/routed-r18-observed.py --root /tmp/kr19-w2-SubstanceDEADSEATRECORD-frozen-xb7c_t16/lane --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict  # exit 0; open_count=0; DEADSEAT named/substance=true
```

The worktree tool was modified relative to committed main (the tool path was `M`; committed blob `ae1651d…`, frozen worktree snapshot above). The current diff adds a check against the pinned `DeadSeatHistoryR18.md` cause/pointers (`routed-r18.py:288-299`); it is not in the committed main blob. Mutation findings below distinguish committed behavior from that worktree candidate.

## Findings

### P1 — `named()` treats any prefixed line as a correction

Committed main `routed-r18.py:304-309` and the worktree candidate `:353-358` only require a line beginning `- R18-DEADSEAT-RECORD:` in each document. They do not verify that either line actually corrects the status or is append-only. In the isolated clone I replaced both correction lines with `- R18-DEADSEAT-RECORD: false assertion`; the candidate still returned `named=true`, `substance=true`, `open_count=0`, strict exit **0** (mutation revision `81b3258de0c9d56814df2e700eed485905aa8bc1`). This is a false closed for the named-correction requirement, despite the real main text being accurate.

### P1 — committed main accepts fabricated cause/source strings

Committed main `routed-r18.py:253-260` checks only the set of `(wave,name)` pairs and that each `cause` and `source` is non-empty. A clone mutation retained the expected seats but replaced their per-seat metadata with fabricated non-empty cause/source strings; the committed-main counter returned `substance=true`, `open_count=0`, strict exit **0** (revision `edfeaa46e605e7057f1c5ee87f5c7def00540754`).

The current uncommitted worktree diff adds a meaningful guard: it compares `cause` to `error_line` and requires the pinned report's evidence pointers in `source` (`:288-299`). With frozen worktree snapshot SHA `8d94f6095d8623314a9608a9ecb1c4635073c87c99fe2449f7837583e43c04640`, fabricated cause/source reopened DEADSEAT (`76d05e3e8613ce83f0c8ee042f8ac9cf78bf14d7`, strict exit **1**, `open_count=1`); an empty cause also reopened it (`7fdd364f643830e1146f63ed869d3e83f82aa890`, exit **1**). This specific gap is fixed in the observed worktree candidate, not in committed main.

### P2 — duplicate seat records collapse to the expected set

Both committed `s_deadseat` (`:253-255`) and the candidate (`:281-283`) convert the evidence entries to a set and never check list cardinality/uniqueness. Duplicating a valid seat therefore leaves `got == want`. On the frozen candidate, an extra copy returned `substance=true`, `open_count=0`, strict exit **0** at `c3e09ba3af1d8f7a65728dc0b84eaf2072aaa1be`; the emitted reason even said **5** seats while the independently recomputed missing-report set contains four. This is a false closed for an exact-seat record.

### P2 — candidate does not validate the recorded terminal state

The worktree guard checks cause text and source-pointer inclusion, but not `terminal_state` or the summary's 3-error/1-abort distinction (`routed-r18.py:288-300`). Changing all four evidence `terminal_state` values to `fabricated-state`, while leaving names, causes and sources intact, still returned `substance=true`, strict exit **0** (`db11f00aa56f3d3cd840702e93804981e3ab6f3a`). This does not falsify the present correction; it shows the candidate's substance check does not bind all disposition details carried by its evidence record.

## Residual risk and verification gaps

- The cause/pointer check in the worktree candidate binds the evidence JSON to an immutable report blob, not to the underlying host-local transcript bytes. The report cites `/home/vgpnk/.omp/agent/sessions/...` JSONL locations (`r18-dead-seats.json:34,46,58,70`); I did not independently re-open those external JSONL files. Treat the checked chain as repo-record consistency, not independent transcript authenticity.
- LSP was unavailable: `read xd://lsp` returned `No such tool` and the mounted-device list had no LSP route. No references/definition/diagnostics checks were possible; grep was used only to locate literals, not as semantic proof.
- No builds, broad tests, installs, or production edits. Only the strict counter, raw Git-object recomputation, and targeted clone mutations above were exercised.