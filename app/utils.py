import json
import logging
from time import time

from aiohttp import ClientSession
from .settings import BASE_URL, CACHE, CACHE_TIMEOUT

# logger
logger = logging.getLogger(__name__)

# Function to sort the object
sort_by = {
    "id": lambda obj: obj["id"],
    "reads": lambda obj: obj["reads"],
    "likes": lambda obj: obj["likes"],
    "popularity": lambda obj: obj["popularity"],
}


async def get(tag: str, session: ClientSession) -> dict:
    try:
        async with session.get(url=f"{BASE_URL}?tag={tag}") as response:
            logger.debug(f"fetching posts for tag <{tag}>")
            CACHE[tag] = {
                "data": json.loads(await response.read()),
                "time": int(time()) + CACHE_TIMEOUT,
            }
            return CACHE[tag]["data"]
    except Exception as e:
        logger.error(f"Unable to fetch tag {tag}, {e}")
