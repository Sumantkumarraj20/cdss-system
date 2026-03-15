#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   LOCAL_DATABASE_URL=postgres://user:pass@localhost/db \
#   DATABASE_URL=postgres://...neon... \
#   ./scripts/sync_to_neon.sh
#
# Copies the entire local DB into Neon using pg_dump/pg_restore.

if [[ -z "${LOCAL_DATABASE_URL:-}" ]]; then
  echo "LOCAL_DATABASE_URL is required" >&2
  exit 1
fi
if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "DATABASE_URL (Neon) is required" >&2
  exit 1
fi

TMP_DUMP=$(mktemp /tmp/cdss_dump.XXXXXX)
trap 'rm -f "$TMP_DUMP"' EXIT

echo "[1/3] Dumping local db -> $TMP_DUMP"
pg_dump "$LOCAL_DATABASE_URL" -Fc -f "$TMP_DUMP"

echo "[2/3] Restoring into Neon (this will clean existing objects)"
pg_restore --clean --if-exists --no-owner --no-privileges \
  -d "$DATABASE_URL" "$TMP_DUMP"

echo "[3/3] Done. Sample row counts:"
psql "$DATABASE_URL" -c "SELECT 'drugs' AS table, COUNT(*) FROM drugs UNION ALL SELECT 'diagnoses', COUNT(*) FROM diagnoses UNION ALL SELECT 'presentations', COUNT(*) FROM presentations;" || true
