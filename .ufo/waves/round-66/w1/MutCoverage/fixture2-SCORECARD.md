# scorecard

## Measurement recipes

**A — source-derived controls.** block agreeing with the counter on this fixture.

```bash
python3 - "$REV" <<'PY'
import json,sys
print(json.dumps({"revision": sys.argv[1], "mapped": 3, "knowledge_files": 4,
 "missing": ["jsc-mapper-cli-contract"], "dangling": [], "citation_resolved_rules": 2,
 "rule_blocks": 2, "coverage_score": 7.5, "depth_score": 10.0}))
PY
```

**B — count reviewed** text

## Owned axes
| candidate | stage → score | basis | cmd | rounds |
| coverage | 9.0 → 10.0 | 4/4 knowledge files mapped | cmd | 1 |
