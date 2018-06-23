from django.contrib import admin
from django.urls import path
from onlineapp.views import *

from django.conf import settings
from django.conf.urls import include, url


urlpatterns_onlineapp = [
    # path('', main_page),
    # path('admin/', admin.site.urls),
    path('onlineapp/collegelist/', college_list),
    path('onlineapp/simplepage/', simple_function),
    path('onlineapp/studentlist/', student_list),
    path('onlineapp/studentlist/<int:id>/', get_student),
    path("onlineapp/students/<slug:acronym>", students_of_college),
    # url(r'^__debug__/', include(debug_toolbar.urls)),
    path("onlineapp/sessioncount8/", session_counter),
]