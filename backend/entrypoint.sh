#!/bin/bash
set -e

echo "Initializing database schema..."
python -c "from backend.src.database import init_db; init_db()"

echo "Checking if database needs seeding..."
COUNT=$(python -c "
from backend.src.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    print(conn.execute(text('SELECT COUNT(*) FROM chunks')).scalar())
")

if [ "$COUNT" = "0" ]; then
    echo "Database empty — running embedder (this takes a few minutes on first run)..."
    python -c "
from backend.src.embedder import load_chunks, embed_and_store
chunks = load_chunks()
embed_and_store(chunks)
"
else
    echo "Database already seeded with $COUNT chunks, skipping embedder."
fi

echo "Starting API server..."
exec uvicorn backend.src.main:app --host 0.0.0.0 --port 8000
