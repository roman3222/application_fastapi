from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Настройки приложения, загружаемые из переменных окружения.
    """
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    KAFKA_BOOTSTRAP_SERVERS: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def get_db_url(self) -> str:
        """
        Возвращает URL для подключения к базе данных.
        :return: URL базы данных.
        """
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    def get_kafka_server(self) -> str:
        """
        Возвращает адрес сервера Kafka.
        :return:Адрес сервера Kafka.
        """
        return f"{self.KAFKA_BOOTSTRAP_SERVERS}"


settings = Settings()
