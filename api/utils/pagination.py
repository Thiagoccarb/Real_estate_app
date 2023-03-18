from fastapi import Request
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from typing import Tuple


async def get_pagination_links(request: Request, count: int) -> Tuple[str, str]:
    url = str(request.url)
    url_components = urlsplit(url)

    query_params = dict(parse_qsl(url_components.query))
    limit = int(query_params.get("limit", 10))
    offset = int(query_params.get("offset", 0))

    # Compute next page URL
    next_offset = offset + limit
    next_query_params = {
        **query_params,
        "offset": str(next_offset),
        "limit": str(limit),
    }
    next_url_components = url_components._replace(query=urlencode(next_query_params))
    next_url = urlunsplit(next_url_components) if next_offset < count else None

    # Compute previous page URL
    prev_offset = max(0, offset - limit)
    prev_query_params = {
        **query_params,
        "offset": str(prev_offset),
        "limit": str(limit),
    }
    prev_url_components = url_components._replace(query=urlencode(prev_query_params))
    prev_url = urlunsplit(prev_url_components) if offset > 0 else None

    return next_url, prev_url
