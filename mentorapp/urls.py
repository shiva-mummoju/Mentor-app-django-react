from django.contrib import admin
from django.urls import path
from mentorapp.views import *
from .restViews import *
from mentorapp.serializers import *

from django.conf import settings
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from django.views.generic import TemplateView

urlpatterns_mentorapp = [
    # authentication

    # url(r'^', TemplateView.as_view(template_name="index.html")),

    url(r'^login/', obtain_jwt_token),
    url(r'^refresh-token/', refresh_jwt_token),

    path("api/college/<int:pk>/", college_list_json),
    path("api/college/", college_list_json),

    path("api/college/students/", StudentList.as_view()),
    # update (put) get or delete
    path("api/college/<int:college_id>/students/<int:pk>/", StudentList.as_view()),
    # create , post , get all students
    path("api/college/<int:college_id>/students/", StudentList.as_view()),

    path("mentorapp/colleges/", CollegeView.as_view(), name="colleges_html"),
    path("mentorapp/generic/colleges/", CollegeListView.as_view(), name="colleges_generic_html"),
    path("mentorapp/generic/colleges/<int:pk>/", CollegeStudentListView.as_view(), name="colleges_student_html"),
    path("mentorapp/generic/colleges/addcollege/", CreateCollegeView.as_view(), name="add_college_html"),
    path("mentorapp/generic/colleges/<int:college_id>/addstudent/", CreateStudentFormView.as_view(),
         name="add_student_html"),
    path("mentorapp/generic/colleges/edit/<int:pk>/", EditCollege.as_view(), name="edit_college_html"),
    path("mentorapp/generic/colleges/delete/<int:pk>/", DeleteCollege.as_view(), name="delete_college_html"),
    path("mentorapp/generic/colleges/<int:college_id>/student/edit/<int:pk>/", EditStudent.as_view(),
         name="edit_student_html"),
    path("mentorapp/generic/colleges/<int:college_id>/delete/<int:pk>/", DeleteStudent.as_view(),
         name="delete_student_html"),
    path("mentorapp/user/signup/", SignUpController.as_view(), name="signup_form_html"),
    path("mentorapp/user/login/", LoginController.as_view(), name="login_form_html"),
    path("mentorapp/user/logout/", LogoutView.as_view(), name="logout_html")
]
