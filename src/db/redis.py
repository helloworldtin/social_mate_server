from redis.asyncio import Redis

redis = Redis.from_url("redis://127.0.0.1:6379")


async def putOPTInRedis(OTP: str, userUID: str) -> None:
    await redis.set(userUID, OTP, ex=300)


async def getOTPFromRedis(userUID: str) -> str | None:
    OTP = await redis.get(userUID)
    if OTP is None:
        return None
    return OTP.decode("utf-8")
