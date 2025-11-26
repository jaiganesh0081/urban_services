from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

provideravailableschema = swagger_auto_schema(
    operation_summary="Get provider availability slots",
    operation_description="Returns the list of availability slots for a specific provider, filtered using provider_id.",
    manual_parameters=[
        openapi.Parameter(
            name="provider_id",
            in_=openapi.IN_QUERY,
            description="UUID of the provider",
            required=True,
            type=openapi.TYPE_STRING,
            format="uuid",
            example="e3a7f4d1-6f8b-4a1a-9db1-8c1c12345678"
        )
    ],
    responses={
        200: openapi.Response(
            description="Provider availability list",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid",
                                             example="b9131b3f-1140-4e17-9e5a-3fa99ddc1234"),
                        "provider_id": openapi.Schema(type=openapi.TYPE_STRING, format="uuid",
                                                      example="e3a7f4d1-6f8b-4a1a-9db1-8c1c12345678"),
                        "provider_name": openapi.Schema(type=openapi.TYPE_STRING, example="John Doe"),
                        "date": openapi.Schema(type=openapi.TYPE_STRING, format="date", example="2025-11-25"),
                        "start_time": openapi.Schema(type=openapi.TYPE_STRING, format="time", example="10:00"),
                        "end_time": openapi.Schema(type=openapi.TYPE_STRING, format="time", example="12:00"),
                    }
                )
            ),
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Provider availablity datas",
                    "data": [
                        {
                            "id": "b9131b3f-1140-4e17-9e5a-3fa99ddc1234",
                            "provider_id": "e3a7f4d1-6f8b-4a1a-9db1-8c1c12345678",
                            "provider_name": "John Doe",
                            "date": "2025-11-25",
                            "start_time": "10:00",
                            "end_time": "12:00"
                        }
                    ]
                }
            }
        ),

        400: openapi.Response(
            description="Missing provider_id",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "provider_id is required"
                }
            }
        ),

        404: openapi.Response(
            description="Provider not found",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Provider not found"
                }
            }
        )
    }
)
