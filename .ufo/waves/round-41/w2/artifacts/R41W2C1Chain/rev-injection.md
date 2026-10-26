# `--rev` option injection: fails closed, no write reachable (R41W2C1Chain)

Round-41 wave-1 `R41C1Sentinel` F8 flagged that `fetch-vendor.py --rev` and the counters pass
a caller-supplied revision straight into `git`'s argv (`git -C <root> show <rev>:<path>`,
`git cat-file -e <rev>^{commit}`). Re-tested at tip.

`git show --output=<file>` *is* a write primitive on its own — proven read-only against the
lane, writing only into my scratch:

```
git -C <LANE> show "--output=$S/gitout1.txt"          # rc=0, 13 448 B written
git -C <LANE> show "--output=$S/gitout2.txt:plans"    # rc=0, file named 'gitout2.txt:plans'
```

But through the tools the injected value is always `<rev>:<frozen path>`, so the filename
gets `.ufo/waves/round-41/c1/carriers.json` appended and contains `/`:

```
git -C <LANE> show '--output=/…/gitinj/x:.ufo/waves/round-41/c1/carriers.json'
# fatal: could not open '…/x:.ufo/waves/round-41/c1/carriers.json' for writing: No such file
# rc=128, stdout 0
```

which makes the tool stop:

| tool | invocation | result |
|---|---|---|
| `fetch-vendor.py` | `--rev=--output=$S/gitinj/x` | exit **2**, nothing printed (load_spec: `returncode != 0 → SystemExit(2)`), no file |
| `c1-counter.py` | `--rev=--output=$S/gitinj/z` | exit **2**, `{"detail": "git cat-file -e --output=…: error: unknown option 'output=…'"}` |

`--rev --output=…` (space form) is rejected earlier by argparse (`expected one argument`).

So the injection is a denial/silent-exit vector, **not** an arbitrary write: reaching the
write would need the directories `x:.ufo/waves/round-41/c1/` to pre-exist, i.e. write access
the caller already has, and the bytes written would be `git show` output (a commit), never
vendor bytes. Both tools fail closed (exit 2, never `met_target`). Residual hardening only:
reject a revision that does not match `^[0-9a-f]{7,64}$` (or `--`-terminate the git argv)
before building the command.
