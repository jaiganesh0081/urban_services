from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

providerserviceschema = swagger_auto_schema(
    operation_summary="Create a Service (Provider Only)",
    operation_description=(
        "Allows a provider to create a service under one of their categories. "
        "Provider must specify title, description, category, base fee, and duration. "
        "Backend automatically assigns the provider from the authenticated user."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["title", "description", "category_id", "base_fee", "estimated_duration"],
        properties={
            "title": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Name of the service"
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Detailed explanation of the service"
            ),
            "category_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Category ID (must belong to provider categories)"
            ),
            "base_fee": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="Base fee for the service"
            ),
            "estimated_duration": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="Estimated duration in minutes"
            )
        },
        example={
            "title": "Pipe Leakage Fix",
            "description": "Fix leaking pipes and joints",
            "category_id": "386dc510-0200-4cd9-8d94-8a3c832dd1c4",
            "base_fee": 300.00,
            "estimated_duration": 45
        }
    ),
    responses={
        201: openapi.Response(
            description="Service successfully created",
            examples={
                "application/json": {
                    "message": "Service created successfully",
                    "data": {
                        "id": "f1e2508e-1ea9-446d-81ea-135ddbb2b8e6",
                        "title": "Pipe Leakage Fix",
                        "category": "386dc510-0200-4cd9-8d94-8a3c832dd1c4",
                        "description": "Fix leaking pipes and joints",
                        "base_fee": "300.00",
                        "estimated_duration": 45
                    },
                    "status_code": 201
                }
            }
        ),
        400: "Validation Error (wrong category, missing fields, duplicates)",
        403: "Only providers can create services",
    }
)

category_id_param = openapi.Parameter(
    "category_id",
    openapi.IN_QUERY,
    description="Filter services by category ID",
    type=openapi.TYPE_STRING
)

search_param = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="Search services by title or description",
    type=openapi.TYPE_STRING
)

min_rating_param = openapi.Parameter(
    "min_rating",
    openapi.IN_QUERY,
    description="Filter services with provider rating >= min_rating",
    type=openapi.TYPE_NUMBER
)

min_fee_param = openapi.Parameter(
    "min_fee",
    openapi.IN_QUERY,
    description="Filter services where base_fee >= min_fee",
    type=openapi.TYPE_NUMBER
)

max_fee_param = openapi.Parameter(
    "max_fee",
    openapi.IN_QUERY,
    description="Filter services where base_fee <= max_fee",
    type=openapi.TYPE_NUMBER
)

page_param = openapi.Parameter(
    "page",
    openapi.IN_QUERY,
    description="Page number for pagination",
    type=openapi.TYPE_INTEGER,
    default=1
)

page_size_param = openapi.Parameter(
    "page_size",
    openapi.IN_QUERY,
    description="Number of items per page. Use 'all' to return entire dataset.",
    type=openapi.TYPE_STRING,
    default=10
)
service_list_example = {
    "message": "Available Services",
    "data": [
        {
            "category_id": "33f5a1ba-2c21-4e99-9a3d-9182d0021ab3",
            "category_name": "Electrical",
            "services": [
                {
                    "id": 1,
                    "title": "Fan Repair",
                    "description": "Fix ceiling fan noise or low speed issues",
                    "base_fee": 300,
                    "estimated_duration": "1 hour",
                    "provider_name": "Rahul Kumar",
                    "provider_rating": "4.5"
                },
                {
                    "id": 2,
                    "title": "Tube Light Installation",
                    "description": "Install LED tube lights",
                    "base_fee": 150,
                    "estimated_duration": "30 minutes",
                    "provider_name": "Kishore",
                    "provider_rating": "4.2"
                }
            ]
        },
        {
            "category_id": "44c8bc11-7b1f-45c2-8a2d-31d09214e12a",
            "category_name": "Plumbing",
            "services": [
                {
                    "id": 5,
                    "title": "Tap Fix",
                    "description": "Fix leaking or jammed taps",
                    "base_fee": 200,
                    "estimated_duration": "45 minutes",
                    "provider_name": "Arun",
                    "provider_rating": "4.8"
                }
            ]
        }
    ]
}
listserviceschema = swagger_auto_schema(
    manual_parameters=[
        category_id_param,
        search_param,
        min_rating_param,
        min_fee_param,
        max_fee_param,
        page_param,
        page_size_param,
    ],
    responses={
        200: openapi.Response(
            description="Grouped Service List",
            examples={
                "application/json": service_list_example
            }
        ),
        400: "Invalid filter or pagination values",
        401: "Authentication credentials were not provided",
    }
)
