from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    PROJECT_NAME: str = "Super Ear"
    DEBUG: bool = True

    MONGODB_URI: MongoDsn = "mongodb://mongo:27017"  # type: ignore[assignment]
    MONGODB_DB_NAME: str = "super_ear"

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
