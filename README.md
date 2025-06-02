
# SupportAI — Quick Start

## 0. Create `.env` file

Create a `.env` file in the project root with your environment variables, for example:

```env
COHERE_API_KEY=...
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/postgres
```


## 1. Clone repository

```bash
git clone https://github.com/froozy3/SupportAI
cd SupportAI--master
```

## 2. Building and launching containers

```bash
docker-compose build
docker-compose up -d
```

## 3. Applying Database Migrations

```bash
docker exec -it supportai--master-backend-1 sh
cd /backend
alembic upgrade head
exit
```

## 4. Check if it’s working

- Backend is available at: [http://localhost:8000](http://localhost:8000)
- Frontend is available at: [http://localhost:3000](http://localhost:3000)


### Important Tips

- After changing models or migrations, always run step 3 (`alembic upgrade head`).
- When rebuilding containers, make sure to repeat steps 2 and 3.


