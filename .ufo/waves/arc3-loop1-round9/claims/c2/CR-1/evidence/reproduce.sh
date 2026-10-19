#!/usr/bin/env bash
set -euo pipefail

EVIDENCE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUN="$(mktemp -d /var/tmp/kaidoku-cr1-sqlite-id.XXXXXX)"
trap 'rm -rf "$RUN"' EXIT
mkdir -p "$RUN/tmp" "$RUN/db-a" "$RUN/db-b" "$RUN/probes"
sqlite3 "$RUN/db-a/catalog.db" < "$EVIDENCE/fixture.sql"
cp "$RUN/db-a/catalog.db" "$RUN/db-b/catalog.db"

TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-sqlite-database "$RUN/db-a/catalog.db" --format json > "$RUN/probes/a1.json"
TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-sqlite-database "$RUN/db-a/catalog.db" --format json > "$RUN/probes/a2.json"
TMPDIR="$RUN/tmp" npx -y rea-agents@6.7.0 inspect-sqlite-database "$RUN/db-b/catalog.db" --format json > "$RUN/probes/b1.json"
sha256sum "$RUN/db-a/catalog.db" "$RUN/db-b/catalog.db"
node "$EVIDENCE/recompute.mjs" "$RUN/probes" "$RUN/db-a/catalog.db" "$RUN/db-b/catalog.db"
