**Initial Setup**

Enter your `OPEN_AI_API_KEY` and `OPEN_AI_ORGANIZATION_ID` in `/backend/platform/lib/data/openai.py`

1. From the root directory, navigate to the platform directory in your terminal
   / > `cd backend/platform` > /backend/platform

2. Install platform dependencies
   `poetry install`

3. Build the project
   `docker compose build`

4. Run the project
   `docker compose up -d`

5. Run DB migrations
   `docker compose exec platform alembic upgrade head`

6. Restart the project to reflect DB migrations
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
