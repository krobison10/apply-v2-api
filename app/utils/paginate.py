from ..config import *
from urllib.parse import urlencode


class PaginateUtil:
    @staticmethod
    def paginate(limit: int, offset: int = 0, total_results: int = 0, count: int = 0):
        base_url = request.host_url + "api" + request.path

        query_params = request.args.to_dict()

        prev_offset = max(offset - limit, 0)
        next_offset = offset + limit

        if query_params:
            query_params["limit"] = limit
        else:
            query_params = {"limit": limit, "offset": offset}

        prev_query_params = query_params.copy()
        next_query_params = query_params.copy()
        prev_query_params["offset"] = prev_offset
        next_query_params["offset"] = next_offset

        prev_url = (
            None
            if prev_offset >= offset
            else f"{base_url}?{urlencode(prev_query_params)}"
        )
        next_url = (
            None
            if (limit + offset) >= total_results
            else f"{base_url}?{urlencode(next_query_params)}"
        )

        metadata = {
            "limit": limit,
            "offset": offset,
            "count": count,
            "total_results": total_results,
            "links": {
                "prev": prev_url,
                "next": next_url,
            },
        }

        return metadata
