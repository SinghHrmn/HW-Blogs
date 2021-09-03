import asyncio
import json
import logging
from time import time

import aiohttp
from flask import jsonify, request

from . import app, utils
from .settings import (ACCEPTED_DIRECTIONS, ACCEPTED_KEYS, CACHE,
                       CACHE_TIMEOUT, ERROR_DIRECTION, ERROR_SORTBY,
                       ERROR_TAGS)

# Logger
logger = logging.getLogger(__name__)


@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"success": True}), 200


@app.route("/api/posts", methods=["GET"])
async def posts():
    # get all the arguments
    params = dict(request.args)

    # tags
    tags = params.get("tags", None)
    if not tags:
        return jsonify({"error": ERROR_TAGS}), 400
    tags = tags.split(",")

    key = params.get("sortBy", "id")

    # check if this is in range of acceptable values
    if key not in ACCEPTED_KEYS:
        return jsonify({"error": ERROR_SORTBY}), 400

    direction = params.get("direction", "asc")

    # check if it is in the acceptable values
    if direction not in ACCEPTED_DIRECTIONS:
        return jsonify({"error": ERROR_DIRECTION}), 400

    logger.debug(f"Fetching all posts related to tags: {tags}")

    responses = []

    # Fetch the data from api
    async with aiohttp.ClientSession() as session:
        requests = []
        for tag in tags:
            # Check if we have the tag in the cache
            if CACHE.get(tag, False):
                # Clear cache if we have crossed the TIMEOUT
                if int(time()) > CACHE[tag].get("time"):
                    CACHE[tag]["data"] = None
                    CACHE[tag]["time"] = 0

                    requests.append(utils.get(tag, session))
                else:
                    responses.append(CACHE[tag]["data"])
            else:
                requests.append(utils.get(tag, session))
        responses.extend(await asyncio.gather(*requests))

    final_resp = {"posts": []}

    for response in responses:
        for post in response.get("posts", []):
            if post not in final_resp["posts"]:
                final_resp["posts"].append(post)

    # Sort it according to options
    reverse = True if direction == "desc" else False
    final_resp["posts"] = sorted(
        final_resp["posts"], key=utils.sort_by[key], reverse=reverse
    )

    return final_resp
