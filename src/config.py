import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST: str | None = os.environ.get('DB_HOST')
DB_PORT: str | None = os.environ.get('DB_PORT')
DB_NAME: str | None = os.environ.get('DB_NAME')
DB_USER: str | None = os.environ.get('DB_USER')
DB_PASS: str | None = os.environ.get('DB_PASS')

REDIS_PORT: str | int | None = os.environ.get('REDIS_PORT')
REDIS_HOST: str | None = os.environ.get('REDIS_HOST')

RABBITMQ_HOST: str | None = os.environ.get('RABBITMQ_HOST')
RABBITMQ_USERNAME: str | None = os.environ.get('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD: str | None = os.environ.get('RABBITMQ_PASSWORD')
RABBITMQ_PORT: str | None = os.environ.get('RABBITMQ_PORT')
