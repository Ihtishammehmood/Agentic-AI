# n8n on Docker with Neon Postgres (Self-Hosted)

Spin up a production-ready n8n instance using Docker Compose and a managed Postgres database on [Neon](https://neon.tech).

> **What you get**
> - Persistent n8n data via a Docker volume
> - External Postgres on Neon (SSL enabled)
---

## File layout

```
.
├── docker-compose.yml
└── .env   # your secrets and settings (not committed)
```

## Prerequisites

- Docker and Docker Compose installed
- A Neon Postgres project with:
  - **Host**
  - **Port** (`5432` for direct connection, or `6432` for Neon’s pooled endpoint)
  - **Database name**
  - **Username**
  - **Password**
- An empty database (n8n will create its own tables)

---

## Step-by-step: run locally

1. **Create `.env`**
   Put your Neon credentials and basic settings in a `.env` file next to `docker-compose.yml`.

   > **Important:** Do not wrap values in quotes in `.env`.

   ```
   PGHOST
   PGDATABASE
   PGUSER
   PGPASSWORD
   PGPORT=5432
   PGSSLMODE
   PGCHANNELBINDING
   TZ
   GENERIC_TIMEZONE
   ```

2. **Start n8n**
   ```bash
   docker compose up -d
   ```

3. **Watch logs (first run will run DB migrations)**
   ```bash
   docker compose logs -f n8n
   ```
   Wait until you see messages indicating the server is listening on port **5678**.

4. **Open the UI**
   Visit: `http://localhost:5678`  
   Create your first user and you’re in.

5. **Stop / start later**
   ```bash
   docker compose stop    # stop
   docker compose start   # start again
   docker compose down    # stop and remove the container (keeps volume)
   ```
