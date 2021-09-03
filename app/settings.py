"""
author: Harmandeep Singh
github: https://github.com/SinghHrmn
"""

# App
PORT = 5000
DEBUG = False

# Cache
CACHE = {}
CACHE_TIMEOUT = 300  # seconds

# API
BASE_URL = "https://api.hatchways.io/assessment/blog/posts"
ACCEPTED_KEYS = ("id", "reads", "likes", "popularity")
ACCEPTED_DIRECTIONS = ("asc", "desc")
ERROR_TAGS = "Tags parameter is required."
ERROR_SORTBY = "sortBy parameter is Invalid."
ERROR_DIRECTION = "direction parameter is Invalid."
