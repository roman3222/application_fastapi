import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from application.main import app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Создаем event loop для всех тестов."""
    import asyncio
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def db_engine():
    """Создаем асинхронный движок для базы данных."""
    engine = create_async_engine("postgresql+asyncpg://user_test:password_test@localhost/dbname_test")
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """Создаем асинхронную сессию для базы данных."""
    async with db_engine.connect() as connection:
        transaction = await connection.begin()
        AsyncSessionLocal = async_sessionmaker(
            bind=connection,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with AsyncSessionLocal() as session:
            yield session
        await transaction.rollback()


@pytest.mark.asyncio
async def test_create_application(client):
    data = {"user_name": "New Item", "description": "ololo"}
    response = await client.post("/applications/", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert "id" in response_data
    assert response_data["user_name"] == "New Item"
    assert response_data["description"] == "ololo"


@pytest.mark.asyncio
async def test_create_error_type_data(client):
    # Передаем тип int вместо ожидаемого str в поле user_name
    data = {"user_name": 123, "description": "ololo"}
    response = await client.post("/applications/", json=data)

    assert response.status_code == 422

    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)

    error_detail = response_data["detail"][0]
    assert error_detail["loc"] == ["body", "user_name"]
    assert error_detail["msg"] == "Input should be a valid string"
    assert error_detail["type"] == "string_type"


@pytest.mark.asyncio
async def test_get_applications_success(client):
    response = await client.get("/applications/", params={"page": 1, "size": 10})

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)

    assert "id" in response_data[0]
    assert "user_name" in response_data[0]
    assert "description" in response_data[0]
    assert "created_at" in response_data[0]


@pytest.mark.asyncio
async def test_get_applications_filter_by_user_name(client):
    response = await client.get("/applications/", params={"user_name": "New Item", "page": 1, "size": 10})
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    if response_data:
        for application in response_data:
            assert application["user_name"] == "New Item"


@pytest.mark.asyncio
async def test_get_applications_invalid_pagination(client):
    response = await client.get("/applications/", params={"page": 0, "size": -1})
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Invalid pagination parameters"


@pytest.mark.asyncio
async def test_get_applications_database_error(client, mocker):
    mocker.patch("application.crud.get_applications", side_effect=OperationalError("Database error", {}, {}))
    response = await client.get("/applications/", params={"page": 1, "size": 10})
    assert response.status_code == 503
    response_data = response.json()
    assert response_data["detail"] == "Database error"

@pytest.mark.asyncio
async def test_get_applications_empty_list(client, mocker):
    mocker.patch("application.crud.get_applications", return_value=[])
    response = await client.get("/applications/", params={"page": 1, "size": 10})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == []

@pytest.mark.asyncio
async def test_get_applications_logging(client, mocker):
    mock_info_logger = mocker.patch("application.main.info_logger.info")
    mock_error_logger = mocker.patch("application.main.error_logger.error")
    response = await client.get("/applications/", params={"page": 1, "size": 10})
    mock_info_logger.assert_called_once_with(
        "Request applications: user_name: None, page: 1, size: 10"
    )
    mock_error_logger.assert_not_called()
