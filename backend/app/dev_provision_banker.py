"""Provision a local banker account for development demonstrations only."""

import argparse
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.database import engine
from backend.app.core.security import hash_password
from backend.app.models import Base
from backend.app.models.user import User


async def provision(email: str, password: str, name: str, phone: str | None) -> None:
    if settings.app_env != "development":
        raise RuntimeError("Development banker provisioning is disabled unless APP_ENV=development")

    if not settings.database_url.startswith("sqlite"):
        raise RuntimeError("Development banker provisioning only supports the configured SQLite development database")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.email == email.lower()))
        user = result.scalar_one_or_none()
        if user is None:
            user = User(
                name=name,
                email=email.lower(),
                hashed_password=hash_password(password),
                phone=phone,
                role="banker",
                language="en",
                is_active=True,
                is_verified=True,
            )
            session.add(user)
        else:
            user.name = name
            user.hashed_password = hash_password(password)
            user.phone = phone
            user.role = "banker"
            user.is_active = True
            user.is_verified = True
        await session.commit()
        await session.refresh(user)
        print(f"DEVELOPMENT_BANKER_READY email={user.email} user_id={user.id} role={user.role}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Provision a banker account in development only")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="Development Banker")
    parser.add_argument("--phone", default=None)
    args = parser.parse_args()
    asyncio.run(provision(args.email, args.password, args.name, args.phone))


if __name__ == "__main__":
    main()
