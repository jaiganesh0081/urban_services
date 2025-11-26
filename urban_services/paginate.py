from rest_framework.response import Response
from rest_framework import status


def paginate_data(request, data, default_page_size=10, key_name="data"):
    try:
        page = int(request.query_params.get("page", 1))
        page_size = request.query_params.get("page_size", str(default_page_size))

        if isinstance(page_size, str) and page_size.lower() == "all":
            return {
                "page": 1,
                "page_size": len(data),
                "total_items": len(data),
                "total_pages": 1,
                "showing_entries": f"Showing 1 to {len(data)} of {len(data)} entries",
                key_name: data
            }

        page = int(page)
        page_size = int(page_size)
        total_items = len(data)
        total_pages = (total_items + page_size - 1) // page_size

        if page < 1 or page_size < 1:
            return {
                "error": "Page and page_size must be positive integers",
                key_name: []
            }

        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        paginated_data = data[start_idx:end_idx]

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "showing_entries": f"Showing {start_idx + 1} to {end_idx} of {total_items} entries",
            key_name: paginated_data
        }

    except ValueError:
        return {
            "error": "Invalid page or page_size format. They must be integers.",
            key_name: []
        }
