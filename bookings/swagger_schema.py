from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

bookingcreateschema = swagger_auto_schema(
    operation_summary="Create new booking",
    operation_description=(
        "Creates a service booking for a customer.\n"
        "Performs the following checks:\n"
        "1. Service exists\n"
        "2. Provider matches the service\n"
        "3. Provider is available on the selected date & time\n"
        "4. No conflicting booking exists during the time slot\n"
        "If all validations pass, a booking is created with status 'Pending'."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["service_id", "provider_id", "date", "start_time", "end_time"],
        properties={
            "service_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="uuid",
                description="UUID of the service being booked",
                example="e8c35986-40fe-4fbf-bcbb-7cb1c046c45c"
            ),
            "provider_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="uuid",
                description="UUID of the provider offering the service",
                example="2d9cdb68-f0e2-4210-b1e2-6a3b3ea498b1"
            ),
            "date": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="date",
                description="Booking date (YYYY-MM-DD)",
                example="2025-11-28"
            ),
            "start_time": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="time",
                description="Start time of the booking (HH:MM)",
                example="11:00"
            ),
            "end_time": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="time",
                description="End time of the booking (HH:MM)",
                example="12:00"
            ),
        },
        example={
            "service_id": "e8c35986-40fe-4fbf-bcbb-7cb1c046c45c",
            "provider_id": "2d9cdb68-f0e2-4210-b1e2-6a3b3ea498b1",
            "date": "2025-11-28",
            "start_time": "11:00",
            "end_time": "12:00"
        }
    ),
    responses={

        # SUCCESS RESPONSE (201)
        201: openapi.Response(
            description="Booking created successfully",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Booking created successfully",
                    "data": {
                        "booking_id": "bc57a58a-95de-4387-a28f-bcac1bbdfc26",
                        "service": {
                            "title": "Pipe Leakage Fix",
                            "base_fee": 300
                        },
                        "provider": {
                            "name": "Arun Kumar",
                            "rating": 4.5
                        },
                        "date": "2025-11-28",
                        "start_time": "11:00",
                        "end_time": "12:00",
                        "status": "Pending"
                    }
                }
            }
        ),

        # VALIDATION ERRORS (400)
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Validation error",
                    "errors": {
                        "non_field_errors": [
                            "Provider is not available during this time slot"
                        ]
                    }
                }
            }
        ),

        # UNAUTHORIZED (401)
        401: openapi.Response(
            description="Authentication required",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Authentication credentials were not provided"
                }
            }
        ),

        # FORBIDDEN FOR NON-CUSTOMERS (403)
        403: openapi.Response(
            description="Customers only",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Only customers can create bookings"
                }
            }
        ),
    }
)

bookingupdateschema = swagger_auto_schema(
    operation_summary="Update booking status",
    operation_description=(
        "Allows a provider to update the status of a booking.\n\n"
        "Valid status values:\n"
        "- Accepted\n"
        "- Rejected\n"
        "- Completed\n\n"
        "The provider can only update bookings assigned to them."
    ),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["booking_id", "status"],
        properties={
            "booking_id": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="uuid",
                example="b23fa212-1c79-4a49-a2d4-52e8ec3eef22",
                description="UUID of the booking to update"
            ),
            "status": openapi.Schema(
                type=openapi.TYPE_STRING,
                enum=["Accepted", "Rejected", "Completed"],
                example="Accepted",
                description="New booking status"
            ),
        }
    ),
    responses={
        200: openapi.Response(
            description="Booking status updated successfully",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Booking status updated successfully",
                    "data": {
                        "booking_id": "b23fa212-1c79-4a49-a2d4-52e8ec3eef22",
                        "previous_status": "Pending",
                        "updated_status": "Accepted",
                        "updated_at": "2025-02-10 14:20:30"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="Validation error",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Invalid status transition",
                    "errors": {
                        "status": [
                            "Cannot change status from Pending to Completed"
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
                    "message": "You are not authorized to update this booking"
                }
            }
        ),
        404: openapi.Response(
            description="Booking not found",
            examples={
                "application/json": {
                    "status": "error",
                    "message": "Booking not found"
                }
            }
        )
    }
)
