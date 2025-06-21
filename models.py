from sqlalchemy import ForeingKey, String, BigInteger  # noqa: F401
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine #  # noqa: F401


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tabLename__ = 'users'

    id: Mapped[int] = mapped_column(primarykey=True)
    tg_id = mapped_column(BigInteger)


class Task(Base):
    __tabLename__ = 'tasks'

    id: Mapped[int] = mapped_column(primarykey=True)
    title: Mapped[str] = mapped_column(String(128))
    completed: Mapped[bool] = mapped_column(default=False)
    user: Mapped[int] =mapped_column(ForeingKey('users.id', ondelete='CASCADE'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.medata.create_all)