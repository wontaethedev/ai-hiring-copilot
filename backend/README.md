**Initial Setup**

1. Create a .env file in `/backend` and populate fields `OPEN_AI_API_KEY` and `OPEN_AI_ORGANIZATION_ID`

2. From the root directory, navigate to the app-core directory in your terminal
   / > `cd backend/app-core` > /backend/app-core

3. Install app-core dependencies
   `poetry install`

4. Build the project
   `docker compose build`

5. Run the project
   `docker compose up -d`

6. Run DB migrations
   `docker compose exec app-core alembic upgrade head`

7. Restart the project to reflect DB migrations (unless you ran migrations in the container directly)
   `docker compose down && docker compose up -d`

**Additional Commands**

- `poetry run pytest` to run tests > May need to specify root path ie: `PYTHONPATH=. poetry run pytest`

**Stack Overview**

- Python
- FastAPI

- PostgreSQL
- SQLAlchemy
- Alembic

- Docker compose
- Poetry
