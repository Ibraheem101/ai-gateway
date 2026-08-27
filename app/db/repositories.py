from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ApiKey, AuditLog, User


class UserRepository:
    """Encapsulates all database operations for Users."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: str) -> User:
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)
        await self.session.flush()
        return user


class ApiKeyRepository:
    """Encapsulates all database operations for API Keys."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_api_key(self, key_hash: str, name: str, user_id: int) -> ApiKey:
        api_key = ApiKey(key_hash=key_hash, name=name, user_id=user_id)
        self.session.add(api_key)
        await self.session.flush()
        return api_key

    async def get_api_key_by_hash(self, key_hash: str) -> ApiKey | None:
        stmt = select(ApiKey).where(ApiKey.key_hash == key_hash, ApiKey.is_active.is_(True))
        result = await self.session.execute(statement=stmt)
        return result.scalar_one_or_none()

    async def list_user_api_keys(self, user_id: int) -> Sequence[ApiKey]:
        stmt = select(ApiKey).where(ApiKey.user_id == user_id)
        result = await self.session.execute(statement=stmt)
        return result.scalars().all()


class AuditLogRepository:
    """Encapsulates all database operations for Audit Logs."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_audit_log(
        self,
        user_id: int | None,
        endpoint: str,
        provider: str,
        status_code: int,
        response_time_ms: float,
        cached: bool,
    ) -> AuditLog:
        log_entry = AuditLog(
            user_id=user_id,
            endpoint=endpoint,
            provider=provider,
            status_code=status_code,
            response_time_ms=response_time_ms,
            cached=cached,
        )
        self.session.add(log_entry)
        await self.session.flush()
        return log_entry
