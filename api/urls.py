from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_jwt.views import obtain_jwt_token
from mentor.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    re_path('api/(?P<version>(v1|v2))/', include('mentor.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('student.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('session.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('feedback.urls')),
    re_path(r'^(?P<url>.*)/$', home),
    re_path(r'^(?P<url>.*)$', home),
]
