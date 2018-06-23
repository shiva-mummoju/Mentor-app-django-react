from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from onlineapp.models import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# from StringIO import StringIO
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView



@csrf_exempt
def college_list_json(request, pk=0):
    if request.method == 'GET':
        if pk == 0:
            college = College.objects.all()
            print(college)
            ser_colleges = CollegeSerializer(college, many=True)
            return JsonResponse(ser_colleges.data, safe=False)
        try:
            colleges = College.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        ser_colleges = CollegeSerializer(colleges)
        return JsonResponse(ser_colleges.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        print("the data", data)
        serializer = CollegeSerializer(data=data)
        print("serializer", serializer)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "PUT":
        try:
            college = College.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = CollegeSerializer(college, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        try:
            college = College.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        college.delete()
        return HttpResponse(status=204)



class StudentList(APIView):
    # authentication_classes = (BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self,request,college_id =0 ,pk=0,format = None):
        if pk == 0 and college_id ==0:
            # get all the students of all colleges
            students = Student.objects.all()
            list_students = StudentDetailSerializer(students,many=True)
            return Response(list_students.data)
        elif college_id !=0 and pk != 0:
            # return only one particular student of one particular college
            student = Student.objects.get(id = pk)
            ser_student = StudentDetailSerializer(student)
            return Response(ser_student.data)
        else:
            # all the students of a particular college
            students  = Student.objects.all().filter(college_id = college_id)
            ser_student = StudentSerializer(students , many=True)
            return Response(ser_student.data)

    # insert a new student into the table
    def post(self, request ,college_id=0,pk=0,format=None ):
        if pk == 0 and college_id !=0 :
            ser = StudentDetailSerializer(data = request.data)
            if ser.is_valid():
                student = ser.save(college_id=college_id)
                student.save()
                print(ser.data)
                return Response(ser.data, status=201)
            return Response(ser.errors, status=400)

    # edit the student details. includeing the mocktest data
    def put(self,request, college_id = 0, pk =0, format = None):
        if college_id != 0 and pk !=0:
            student = Student.objects.get(id = pk)
            print(student , student.id)
            ser = StudentDetailSerializer(student,data=request.data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=201)
            return Response(ser.errors, status=400)

    def delete(self,request , college_id = 0, pk =0 , format = None):
        try:
            student = Student.objects.get(id=pk)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        student.delete()
        return HttpResponse(status=204)







