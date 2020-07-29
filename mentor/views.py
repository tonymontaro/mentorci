from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from .serializers import UserSerializer
from session.models import SessionLog
from .invoice import generate_invoice

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user.token = jwt_encode_handler(
            jwt_payload_handler(user)
        )
        serializer = UserSerializer(user)
        return serializer.data
    return False


class LoginView(generics.RetrieveAPIView):
    """
    POST auth/login/
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("email", "")
        password = request.data.get("password", "")
        user_data = login_user(request, username, password)
        if user_data:
            return Response(user_data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        fullname = request.data.get("fullname", "")
        bio = request.data.get("bio", "")
        username = email

        user_exist = login_user(request, username, password)
        if user_exist:
            return Response(user_exist)

        if not username and not password and not email:
            return Response(
                data={
                    "message": "email and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        new_user.profile.fullname = fullname
        new_user.profile.bio = bio
        new_user.profile.save()
        user_data = login_user(request, username, password)

        return Response(
            data=user_data,
            status=status.HTTP_201_CREATED
        )


class UpdateMentor(generics.UpdateAPIView):
    """
    PUT mentors/:id
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        try:
            mentor = self.queryset.get(pk=self.request.user.id)
            serializer = UserSerializer()
            updated_mentor = serializer.update(mentor, request.data)
            updated_mentor.token = jwt_encode_handler(
                jwt_payload_handler(updated_mentor)
            )
            return Response(UserSerializer(updated_mentor).data)
        except User.DoesNotExist:
            return Response(
                data={
                    "message": "Mentor with ID {} not found.".format(
                        kwargs["pk"])},
                status=status.HTTP_404_NOT_FOUND
            )


class Invoice(generics.CreateAPIView):
    """
    POST mentors/invoice
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        date = request.data['date']
        mentor_info = {
            'name': request.user.profile.fullname,
            'address': request.user.profile.address,
            'address_more': request.user.profile.address_more,
            'city': request.user.profile.city_country,
        }
        date_and_number = {
            'date': date,
            'number': request.data['number'],
        }

        year = int(date[:4])
        month = int(date[5:7])
        logs = SessionLog.objects.filter(
            date__year__gte=year,
            date__month__gte=month,
            date__year__lte=year,
            date__month__lte=month,
            mentor=self.request.user)
        mins_per_student = defaultdict(int)
        total_minutes = 0
        for log in logs:
            mins_per_student[log.student.name] += log.duration_in_mins
            total_minutes += log.duration_in_mins
        session_data = []
        for i, name in zip(range(len(mins_per_student)), mins_per_student):
            student_mins = mins_per_student[name]
            hours = int(student_mins // 60)
            mins = int(student_mins % 60)
            secs = int(60 * (student_mins % 60 - mins))
            hours = str(hours) if hours > 9 else '0' + str(hours)
            mins = str(mins) if mins > 9 else '0' + str(mins)
            secs = str(secs) if secs > 9 else '0' + str(secs)
            session_data.append(
                (i + 1, name, '', '', '{} : {} : {}'.format(hours, mins, secs)))

        hourly_fee = float(request.data['hourlyFee'])
        hours = total_minutes / 60
        totals = {
            'hours': round(hours, 2),
            'hourly_fee': hourly_fee,
            'total_amount': str(round(hours * hourly_fee, 3))[:-1],
        }
        pdf = generate_invoice(mentor_info, date_and_number, totals,
                               session_data)
        msg = EmailMessage("CodeInstitute Invoice - {}".format(date),
                           "Find the invoice attached.",
                           to=[request.user.email])
        msg.attach('Invoice-{}.pdf'.format(date), pdf, 'application/pdf')
        msg.content_subtype = "html"
        msg.send()
        return Response(
            data={"message": "Invoice sent."},
            status=status.HTTP_201_CREATED
        )

def home(request,url):
    print(url)
    return JsonResponse({'urlNotFound': url}, status=200)
