from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config.config import settings

# Создание async-движка.
engine = create_async_engine(settings.database_url)

# Фабрика асинхронных сессий.
# expire_on_commit=False позволяет обращаться к атрибутам ORM-объектов
# после commit без неявной повторной загрузки из базы.
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

