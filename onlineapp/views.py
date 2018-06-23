# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from onlineapp.models import *
from django.core.exceptions import ObjectDoesNotExist


@require_http_methods(["GET", "POST"])
def college_list(request):
    c = College.objects.values("name", "acronym")
    print(len(c))
    d = {"college": c}
    return render(request, "testfile.html", d, content_type='text/html')


@require_http_methods(["GET", "POST"])
def student_list(request):
    students = Student.objects.values("name", "email", "college__acronym")
    # print(students)
    d = {"student_list": students}
    return render(request, "studentlist.html", d, content_type='text/html')


@require_http_methods(["GET", "POST"])
def get_student(request, id):
    try:
        student = Student.objects.get(id=id)
        d = {"id": student.id, "name": student.name, "email": student.email, "db_folder": student.db_folder,
             "college": student.college.acronym}
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Student Details Not Found</h1>')
    return render(request, "studentdetails.html", d, content_type="text/html")


@require_http_methods(["GET", "POST"])
def students_of_college(request, acronym):
    student = Student.objects.filter(college__acronym=acronym).values("name", "email", "mocktest__totals").order_by(
        "mocktest__totals").reverse()
    d = {"students": student}
    return render(request, "studentsOfCollege.html", d, content_type="text/html")


@require_http_methods(["GET", "POST"])
def main_page(request):
    return HttpResponse("This is the main page")


@require_http_methods(["GET", "POST"])
def simple_function(request):
    return HttpResponse("This is the simple page")


#################### test views
# create
# noinspection SpellCheckingInspection
@require_http_methods(["GET", "POST"])
def session_counter(request):
    request.session.setdefault("counter", 0)
    callcount = request.session["counter"] + 1
    request.session["counter"] = callcount
    d = {"count": callcount}
    return render(request, "sessioncount.html", d, content_type="text/html")
