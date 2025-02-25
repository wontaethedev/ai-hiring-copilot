import os
from dotenv import load_dotenv


load_dotenv()


class PostgresSettings:
  USER: str = os.getenv("POSTGRES_USER")
  PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
  DB: str = os.getenv("POSTGRES_DB")
  HOST: str = os.getenv("POSTGRES_HOST")
  PORT: int = int(os.getenv("POSTGRES_PORT"))


class OpenApiSettings:
  API_KEY: str = os.getenv("OPEN_AI_API_KEY")
  ORGANIZATION_ID: str = os.getenv("OPEN_AI_ORGANIZATION_ID")

postgres_settings = PostgresSettings()
open_api_settings = OpenApiSettings()
