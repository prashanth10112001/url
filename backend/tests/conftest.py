import os

import pytest

from dotenv import load_dotenv

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlmodel import Session

load_dotenv(".env.test", override=True)

from app.main import app
from app.core.database import get_session
from app.core.cache import redis_client



TEST_DATABASE_URL = os.getenv("DATABASE_URL")

test_engine = create_engine(
    TEST_DATABASE_URL,
    echo=False
)

def override_get_session():

    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def clean_database():
    with Session(test_engine) as session:
        session.exec(
            text(
                "TRUNCATE TABLE "
                "url_clicks, urls, users "
                "RESTART IDENTITY CASCADE"
            )
        )
        session.commit()
    yield

    with Session(test_engine) as session:
            session.exec(
                text(
                    "TRUNCATE TABLE "
                    "url_clicks, urls, users "
                    "RESTART IDENTITY CASCADE"
                )
            )
            session.commit()


@pytest.fixture(autouse=True)
def clean_redis():

    redis_client.flushdb()

    yield

    redis_client.flushdb()

    
