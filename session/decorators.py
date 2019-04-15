import re

from rest_framework.response import Response
from rest_framework.views import status


def bad_req_message(message):
    return Response(
        data={"message": message}, status=status.HTTP_400_BAD_REQUEST)


def validate_session_create_data(fn):
    def decorated(*args, **kwargs):
        validation_regs = [
            {'name': 'duration', 'pattern': r'^\d{0,2}-\d{0,2}-\d{0,2}$',
             'format': 'HH-MM-SS'},
            {'name': 'date', 'pattern': r'^\d{0,2}-\d{0,2}-\d{0,4}$',
             'format': 'DD-MM-YYYY'},
        ]
        for item in validation_regs:
            name, pattern, format_ = (
                item['name'], item['pattern'], item['format'])
            val = args[0].request.data.get(name, "")
            if not re.match(pattern, val):
                return bad_req_message(
                    "Wrong {} format, use; {}".format(name, format_))
        return fn(*args, **kwargs)

    return decorated
