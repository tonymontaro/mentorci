from rest_framework.response import Response
from rest_framework.views import status


def validate_student_create_data(fn):
    def decorated(*args, **kwargs):
        name = args[0].request.data.get("name", "")
        email = args[0].request.data.get("email", "")
        if not name or not email:
            return Response(
                data={
                    "message": "Both email and name are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated
