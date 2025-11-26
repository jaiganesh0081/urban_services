from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

registerswaggerschema = swagger_auto_schema(
    operation_summary="Register a new user",
    operation_description="Creates a new user account with username, full_name, email, phone, role, password and confirm password.",

    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,

        required=["username", "email", "phone", "role", "password", "confirm_password"],

        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="jaiganesh008"
            ),
            "full_name": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="Jaiganesh Singaravelan",
                description="Optional full name of the user"
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="email",
                example="jaiganesh@example.com"
            ),
            "phone": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="8610595431"
            ),
            "role": openapi.Schema(
                type=openapi.TYPE_STRING,
                example="Customer",
                description="Allowed values: Customer or Provider"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="password",
                example="Pass@123"
            ),
            "confirm_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                format="password",
                example="Pass@123"
            )
        }
    ),

    responses={
        201: openapi.Response(
            description="User successfully Registered",
            examples={
                "application/json": {
                    "success": True,
                    "message": "User successfully Registered",
                }
            }
        ),
        400: openapi.Response(
            description="Validation Error",
            examples={
                "application/json": {
                    "success": False,
                    "message": "User is not registered",
                    "errors": {
                        "email": ["Email address already exists"]
                    }
                }
            }
        )
    }
)
