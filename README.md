# CapybaraRAG 🐾

**A production-grade RAG system that answers questions about capybaras.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?logo=postgresql&logoColor=white)

---

## What is this

CapybaraRAG is an end-to-end Retrieval-Augmented Generation system built to explore what it actually takes to make RAG work well, not just work. The domain is intentionally narrow (capybara biology, habitat, behavior, care) so the interesting problems are retrieval quality, corpus construction, and failure mode analysis, not domain breadth.

Technically it demonstrates: vector similarity search over a curated corpus, server-sent event streaming from a FastAPI backend through a Next.js proxy to the browser, paragraph-level relevance filtering before indexing, distance thresholding for out-of-domain detection, and the groundwork for an eval harness to measure retrieval precision and answer quality systematically.

---

## Architecture

```
User Question
     │
     ▼
Next.js Frontend (:3000)
  CapyGPT chat UI — SSE consumer, streaming caret, thinking state
     │
     │  POST /api/ask  (Next.js rewrites to backend via BACKEND_URL)
     ▼
FastAPI Backend (:8000)
     │
     ├──► Sentence Transformers (local, all-MiniLM-L6-v2)
     │      Embed query into 384-dim vector
     │
     ├──► pgvector (Postgres)
     │      Cosine similarity search, top-K chunks
     │      Distance threshold 0.45: reject out-of-domain queries
     │
     └──► Claude Haiku (Anthropic API)
            Stream answer tokens back as SSE
     │
     ▼
Next.js Frontend
  Tokens render word-by-word, sources shown as chips after completion
```

---

## Tech stack

| Component | Technology | Why |
|---|---|---|
| Frontend | Next.js 15 (App Router) + TypeScript | SSE support, proxy rewrites, no CORS headaches in dev |
| Backend | FastAPI (Python) | Native async, first-class SSE via `StreamingResponse` |
| Vector DB | pgvector on Postgres | No new infra, Postgres is already there, sufficient at this scale |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Local, zero per-query cost, 384 dims is plenty for a focused corpus |
| LLM | Claude Haiku (Anthropic API) | Fast, cheap, good instruction following for citations |
| ORM/DB | SQLAlchemy + raw SQL for vector ops | pgvector's `<=>` operator doesn't go through ORMs cleanly |

---

## Project structure

```
capybara-rag/
├── .github/
│   └── workflows/
│       └── deploy.yml         # Builds and pushes Docker images to ghcr.io on push to main
├── backend/
│   ├── src/
│   │   ├── config.py          # Centralized path config (PROJECT_ROOT, DATA_DIR, etc.)
│   │   ├── database.py        # Postgres connection, table init, pgvector extension
│   │   ├── chunker.py         # Word-level sliding window chunking (200w / 50w overlap)
│   │   ├── embedder.py        # Batch embeds chunks and stores in pgvector
│   │   ├── retriever.py       # Cosine similarity search + distance threshold
│   │   ├── rag.py             # Prompt construction + Claude streaming
│   │   └── main.py            # FastAPI app — /health, /ask (SSE)
│   ├── Dockerfile
│   ├── entrypoint.sh          # Init DB schema, seed if empty, start API
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout, Google Fonts import
│   │   │   ├── page.tsx       # Chat state, SSE consumer, send logic
│   │   │   └── globals.css    # Design tokens, all component styles
│   │   ├── components/
│   │   │   ├── TopBar.tsx     # Wordmark + new chat button
│   │   │   ├── EmptyState.tsx # Hero onsen scene + suggested prompts
│   │   │   ├── AssistantMessage.tsx  # Avatar, streaming caret, source chips
│   │   │   ├── ThinkingPod.tsx       # "soaking" animation while backend retrieves
│   │   │   ├── Compose.tsx    # Autoresizing textarea, Enter-to-send
│   │   │   └── CapyInOnsen.tsx       # Hand-drawn SVG capybara scene
│   │   └── instrumentation.ts # Patches broken localStorage shim in dev
│   ├── Dockerfile
│   └── next.config.ts         # Rewrites /api/* to BACKEND_URL (defaults to localhost:8000)
├── docker-compose.yml         # Pulls pre-built images from ghcr.io (used on NAS)
├── data/
│   ├── raw/                   # 17 scraped source articles
│   ├── filtered/              # After paragraph-level capybara relevance filtering
│   └── chunks/                # chunks_size200_overlap50.json (105 chunks)
└── docs/
    └── findings.txt           # Running notes on retrieval quality and corpus decisions
```

---

## Getting started

### Prerequisites

- Docker

### With Docker Compose (recommended)

```bash
git clone https://github.com/C2H6Ethan/capybara-rag.git
cd capybara-rag
```

Create `.env` at the project root:

```env
ANTHROPIC_API_KEY=your_key_here
```

Create a `docker-compose.override.yml` to build images locally instead of pulling from the registry:

```yaml
services:
  db:
    ports:
      - "5433:5432"
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    image: null
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    image: null
```

Then start everything:

```bash
docker compose up -d
```

The first run will build the images and seed the database automatically. Open [http://localhost:3000](http://localhost:3000).

---

### Manual setup (without Docker)

#### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (for Postgres only)

#### 1. Clone and install

```bash
git clone https://github.com/C2H6Ethan/capybara-rag.git
cd capybara-rag
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

#### 2. Start Postgres with pgvector

```bash
docker run -d \
  --name capybara-postgres \
  -e POSTGRES_PASSWORD=capybara123 \
  -e POSTGRES_USER=capybara \
  -e POSTGRES_DB=capybaradb \
  -p 5433:5432 \
  pgvector/pgvector:pg16
```

#### 3. Environment variables

Create `.env` at the project root:

```env
DATABASE_URL=postgresql://capybara:capybara123@localhost:5433/capybaradb
ANTHROPIC_API_KEY=your_key_here
```

#### 4. Initialize the database

```bash
python backend/src/database.py
```

#### 5. Embed the corpus

```bash
python backend/src/embedder.py
```

Loads `data/chunks/chunks_size200_overlap50.json`, embeds all 105 chunks locally using `all-MiniLM-L6-v2`, and stores them in pgvector. Takes ~15 seconds on CPU.

#### 6. Start the backend

```bash
uvicorn backend.src.main:app --reload --port 8000
```

#### 7. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Deployment

On every push to `main`, GitHub Actions builds Docker images for `linux/amd64` and pushes them to GitHub Container Registry (`ghcr.io`). A Watchtower container on the NAS polls for new images every 5 minutes and restarts the affected containers automatically.

To deploy to a server, copy `docker-compose.yml` and a `.env` file with your API key, then run:

```bash
docker compose up -d
```

Subsequent deploys are fully automatic after a push.

---

## Data pipeline

```
Wikipedia / specialty sites
        │
        ▼
   data/raw/           17 articles scraped manually
        │
        ▼  paragraph-level filtering
        │  (keep only paragraphs with at least 1 capybara mention per 1000 words)
        ▼
   data/filtered/      14,313 words across 17 files
        │
        ▼  sliding window chunking (200 words, 50-word overlap)
        ▼
   data/chunks/        105 chunks
        │
        ▼  all-MiniLM-L6-v2 (local)
        ▼
   pgvector            105 x 384-dim embeddings
```

**Key finding:** The raw corpus was 27,229 words. After paragraph-level filtering, 14,313 words remained, so filtering removed about 47% of content as non-capybara noise. Without filtering, 7 of the 12 initial Wikipedia articles had fewer than 1 capybara mention per 1000 words, meaning the majority of chunks would have contained zero relevant information. Filtering before indexing, not after retrieval, was the right call.

Largest corpus contributors: `a-z-animals` (3,740w), `capybara_main` (2,137w), `thesprucepets` (1,830w), `animaldiversity` (1,441w). Coverage: biology, habitat, diet, behavior, reproduction, predators, conservation status, and pet care/husbandry.

---

## Key engineering decisions

- **Local embeddings over API:** `all-MiniLM-L6-v2` runs in ~15s locally for the full corpus and costs nothing per query. At this corpus size the quality difference vs. a hosted embedding API is negligible. If the corpus grew to millions of chunks and embedding quality became a bottleneck, that tradeoff changes.

- **pgvector over a dedicated vector DB:** Pinecone and Weaviate are operationally heavier for a 105-chunk corpus. pgvector gives cosine similarity search inside the Postgres instance that already holds everything else. At larger scale this is worth revisiting.

- **Distance threshold at 0.45:** Validated empirically: on-domain queries cluster at distances 0.20-0.38. The first out-of-domain test query (Antarctica) returned a best distance of 0.47. Threshold of 0.45 cleanly separates the two groups, causing the system to return a plain refusal rather than hallucinating an answer from unrelated chunks.

- **Paragraph-level filtering before indexing:** The alternative (index everything, rely on the distance threshold to filter out noise at query time) would let bad chunks through on queries that happen to be semantically adjacent to noisy content. Filtering the corpus first is a harder constraint and more honest about what the system actually knows.

- **Chunk size 200 words / 50-word overlap:** 200 words preserves enough context for a chunk to be self-contained (a capybara behavior or habitat description is usually 100-250 words). Smaller chunks lose context; larger chunks dilute the embedding. 50-word overlap ensures facts that span paragraph boundaries aren't split in a way that makes either chunk incomplete.

---

## Eval harness

Evaluation methodology is in progress. The plan:

- **Retrieval eval:** precision@K and recall@K against a labeled query set, tested across chunk size configurations (100/200/300 words)
- **Answer quality:** LLM-as-judge scoring (accuracy, citation correctness, refusal behavior on out-of-domain queries)
- **Citation drift detection:** Flag answers where Claude cites a source that doesn't directly support the specific claim. This was observed once during early testing (a selective feeding claim attributed to a prehistoric capybara source) and is a real failure mode in RAG systems.
- **Regression tracking:** Store scores per configuration so changes to chunking, embedding model, or prompt don't silently degrade quality

---

## What I learned

- **Corpus quality is the real bottleneck, not the model.** The hardest retrieval failures weren't about the embedding model or vector search, they were about gaps in the corpus. The care/husbandry queries underperformed because the source articles describe capybaras in the wild, not as pets. No amount of retrieval tuning fixes a missing data problem.

- **Retrieval quality varies systematically by query type.** Factual numeric queries (weight, size) perform well because the answer is a specific number that appears verbatim in one or two chunks. Behavioral and care queries are harder because the relevant information is distributed across multiple paragraphs and no single chunk contains the full answer. I'd want the eval harness to break results down by query type, not just report an average.

- **Citation drift is subtle and easy to miss.** In one early test, Claude cited a chunk about prehistoric giant capybaras as support for a claim about modern capybara diet. The answer was technically correct (the information came from elsewhere in the context) but the citation was wrong. This is the kind of failure that looks fine in demo but matters in production. The mitigation (instruct the model to only cite sources that directly support each specific claim) helps but doesn't fully solve it.

- **Distance thresholding for out-of-domain detection works better than I expected.** I was skeptical that a single scalar threshold would cleanly separate in-domain from out-of-domain queries, but the gap in the distance distribution is real and consistent across different query phrasings. The system correctly refuses "do capybaras live in Antarctica" rather than confabulating. That said, I haven't stress-tested it. Adversarial queries that are semantically adjacent to capybara content but factually out-of-scope are the likely failure mode.
