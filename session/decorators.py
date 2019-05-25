import re

from rest_framework.response import Response
from rest_framework.views import status

from .models import SESSION_TYPES, SESSION_FEELINGS


def bad_req_message(message):
    return Response(
        data={"message": message}, status=status.HTTP_400_BAD_REQUEST)


def validate_data(*args, **kwargs):
    req = args[0].request.data
    run = kwargs['create']
    validation_regs = []
    if run or ('duration' in req):
        validation_regs.append(
            {'name': 'duration', 'pattern': r'^\d{0,2}-\d{0,2}-\d{0,2}$',
             'format': 'HH-MM-SS'})
    if run or ('date' in req):
        validation_regs.append(
            {'name': 'date', 'pattern': r'^\d{0,4}-\d{0,2}-\d{0,2}$',
             'format': 'YYYY-MM-DD'})
    for item in validation_regs:
        name, pattern, format_ = (
            item['name'], item['pattern'], item['format'])
        val = req.get(name, "")
        if not re.match(pattern, val):
            return bad_req_message(
                "Wrong {} format, use; {}".format(name, format_))

    if run or ('types' in req):
        types = req.get('types', "").split('|')
        session_types = [s[0] for s in SESSION_TYPES]
        for type_ in types:
            if type_ not in session_types:
                return bad_req_message(
                    "Invalid session type: {} \n Use any of these; {}".format(
                        type_, session_types)
                )

    if run or ('feeling' in req):
        feeling = req.get('feeling', "")
        session_feelings = [f[0] for f in SESSION_FEELINGS]
        if feeling not in session_feelings:
            return bad_req_message(
                "Invalid feeling value: {} \n Use any of these; {}".format(
                    feeling, session_feelings)
            )
    return 'validated'


def validate_create_data(fn):
    def decorated(*args, **kwargs):
        result = validate_data(create=True, *args, **kwargs)
        return fn(*args, **kwargs) if result == 'validated' else result

    return decorated


def validate_update_data(fn):
    def decorated(*args, **kwargs):
        result = validate_data(create=False, *args, **kwargs)
        return fn(*args, **kwargs) if result == 'validated' else result

    return decorated
