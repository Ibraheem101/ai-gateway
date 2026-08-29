import hashlib
import json
import logging
from typing import Any

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


def generate_prompt_hash(prompt: str, provider: str, model: str) -> str:
    """
    Generates a deterministic SHA-256 digest string using prompt, provider, and model.

    Returns a key string prefixed with cache:inference: (e.g., cache:inference:a3f12b...).
    """

    normalized_prompt = prompt.strip()
    normalized_provider = provider.strip().lower()
    normalized_model = model.strip().lower()

    combined_payload = f"{normalized_provider}:{normalized_model}:{normalized_prompt}"

    payload_bytes = combined_payload.encode("utf-8")
    hash_digest = hashlib.sha256(payload_bytes).hexdigest()

    return f"cache:inference:{hash_digest}"


class CacheService:
    def __init__(self, redis_client: Redis[str]) -> None:
        self.redis_client = redis_client

    async def get_cached_inference(
        self, prompt: str, provider: str, model: str
    ) -> dict[str, Any] | None:
        """Retrieve and deserialize cached json data from Redis"""
        if not self.redis_client:
            return None

        cache_key = generate_prompt_hash(prompt, provider, model)

        try:
            cached_data = await self.redis_client.get(cache_key)
            if cached_data:
                data = json.loads(cached_data)
                if isinstance(data, dict):
                    return data
        except Exception as e:
            logger.warning(f"Cache miss or error for key {cache_key}: {e}")

        return None

    async def set_cached_inference(
        self,
        prompt: str,
        provider: str,
        model: str,
        payload: dict[str, Any],
        ttl_seconds: int = 3600,
    ) -> None:
        """Serialize data to json and store it in redis with a TTL"""
        if not self.redis_client:
            return

        cache_key = generate_prompt_hash(prompt, provider, model)

        try:
            await self.redis_client.setex(
                name=cache_key,
                time=ttl_seconds,
                value=json.dumps(payload),
            )
        except Exception as e:
            logger.warning(f"Failed to set cache for key {cache_key}: {e}")
