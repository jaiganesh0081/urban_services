from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

providerprofileschema = swagger_auto_schema(
    operation_summary="Create Provider Profile",
    operation_description=(
        "Creates a provider profile based on skills. "
        "Provider gives ONLY skill_ids. System automatically detects categories "
        "based on those skills and assigns them to the provider profile."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["skill_ids"],
        properties={
            "skill_ids": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="List of skill UUIDs selected by provider"
            ),
            "experience": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Provider experience (optional)"
            ),
            "address": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Provider address (optional)"
            ),
        },
        example={
            "skill_ids": [
                "5ecbe62c-f6a3-4250-b190-4cdfbaf7fde3",
                "1235f16a-b781-458f-b69e-231d79b3950d"
            ],
            "experience": "5 years",
            "address": "Labour Colony"
        }
    ),
    responses={
        201: openapi.Response(
            description="Provider profile successfully created",
            examples={
                "application/json": {
                    "message": "Provider profile successfully created",
                    "data": {
                        "categories": [
                            "plumbing-uuid",
                            "painting-uuid"
                        ],
                        "experience": "5 years",
                        "address": "Labour Colony"
                    },
                    "status_code": 201
                }
            }
        ),
        400: "Validation error",
        403: "Only providers can create this profile"
    }
)

availableslotschema = swagger_auto_schema(
    operation_summary="Create provider availability slot",
    operation_description="Allows a provider to create availability by specifying date, start time, and end time.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["date", "start_time", "end_time"],
        properties={
            "date": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="date",
                example="2025-11-25",
                description="Slot date (YYYY-MM-DD)"
            ),
            "start_time": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="time",
                example="10:00",
                description="Start time (HH:MM)"
            ),
            "end_time": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="time",
                example="12:00",
                description="End time (HH:MM)"
            ),
        }
    ),
    responses={
        201: openapi.Response(
            description="Slot availability created",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Slot availability as updated"
                }
            }
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Validation error",
                    "errors": {
                        "non_field_errors": [
                            "End time must be AFTER start time"
                        ]
                    }
                }
            }
        ),
        403: openapi.Response(
            description="Access denied",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "You are not authorized to perform this action"
                }
            }
        )
    }
)
