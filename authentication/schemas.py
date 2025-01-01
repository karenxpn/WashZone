from drf_spectacular.utils import extend_schema
from authentication.serializers.send_otp_body_serializer import SendOtpBodySerializer
from authentication.serializers.verify_otp_body_serializer import VerifyOTPBodySerializer

send_otp_schema = extend_schema(
        summary="Send OTP",
        description="Sends a One-Time Password (OTP) to the provided phone number. If the user does not exist, it creates a new user.",
        request=SendOtpBodySerializer,
        responses={
            200: {"type": "object", "properties": {"otp": {"type": "string"}}},
        },
    )

verify_otp_schema = extend_schema(
        summary="Verify OTP",
        description="Verifies the provided OTP for a phone number. On success, marks the phone as verified and returns a JWT access token.",
        request=VerifyOTPBodySerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "OTP verified successfully"},
                    "access": {"type": "string", "example": "jwt_access_token"}
                }
            },
        },
    )