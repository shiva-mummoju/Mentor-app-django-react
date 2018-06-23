from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.forms import PasswordInput, TextInput
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
# from mentorapp.models import *
from django.views import *
from onlineapp.models import *
from django.shortcuts import *
from rest_framework import routers, serializers, viewsets

# use the following code anywhere to debug in the code
import ipdb


# ipdb.set_trace()


class CollegeView(View):
    def get(self, request, *args, **kwargs):
        colleges = College.objects.all()
        return render(
            request,
            template_name='mentorapp_colleges.html',
            context={
                'colleges_list': colleges
            },
            content_type="text/html"
        )


class CollegeListView(LoginRequiredMixin, ListView):
    login_url = "/mentorapp/user/login/"
    model = College
    context_object_name = 'colleges_list'
    template_name = 'mentorapp_colleges.html'

    def get_context_data(self, **kwargs):
        context = super(CollegeListView, self).get_context_data(**kwargs)
        context.update({

            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class CollegeStudentListView(LoginRequiredMixin, DetailView):
    login_url = "/mentorapp/user/login/"
    model = College
    # context_object_name = 'student_list'
    template_name = 'college_student_list.html'

    # def get_object(self, queryset=None):
    #     # ipdb.set_trace()
    #     if(get_list_or_404(Student, college_id=self.kwargs.get('i', None))):
    #         return get_list_or_404(Student, college_id=self.kwargs.get('i', None))
    #     student = Student()
    #     return student

    def get_context_data(self, **kwargs):
        context = super(CollegeStudentListView, self).get_context_data(**kwargs)
        context.update({
            "college_id": self.kwargs.get('pk', None),
            "student_list": Student.objects.all().filter(college_id=self.kwargs.get('pk', None)),
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class AddCollegeForm(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['id']
        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your location'}),
            'acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your acronym'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your contact'}),
        }


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['id', 'dob', 'college']
        widget = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email'}),
            'db_folder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your db folder'}),
            'dropped_out': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'placeholder': 'enter if you are dropped out'}),
        }


class AddMockTestForm(forms.ModelForm):
    class Meta:
        model = Mocktest
        exclude = ['id', 'student', 'totals']


class CreateCollegeView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # login_url = "/login/"
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.add_college'
    permission_denied_message = "You cannot add college"
    template_name = 'college_form.html'
    model = College
    form_class = AddCollegeForm
    success_url = reverse_lazy('colleges_generic_html')


class CreateStudentFormView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.add_student'
    permission_denied_message = 'You cannot add student'
    template_name = 'add_student_form.html'
    model = Student
    form_class = AddStudentForm

    # success_url =
    def get_context_data(self, **kwargs):
        context = super(CreateStudentFormView, self).get_context_data(**kwargs)
        mock = AddMockTestForm()
        context.update({
            'student_form': context.get("form"),
            'mocktest_form': mock,
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context

    def post(self, request, *args, **kwargs):
        college_object = get_object_or_404(College, pk=kwargs.get("college_id"))
        student_form = AddStudentForm(request.POST)
        mock_form = AddMockTestForm(request.POST)
        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.college = college_object
            student.save()
            if mock_form.is_valid():
                mocktest = mock_form.save(commit=False)
                mocktest.student = student
                mocktest.totals = sum(mock_form.cleaned_data.values())
                mocktest.save()
        return redirect("colleges_student_html", college_object.id)


class EditCollege(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.change_college'
    permission_denied_message = "you cannot change the college"
    model = College
    template_name = "college_form.html"
    form_class = AddCollegeForm
    success_url = reverse_lazy('colleges_generic_html')


class DeleteCollege(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.delete_college'
    permission_denied_message = "you cannot delete a college"
    model = College
    template_name = "confirm_delete_college.html"
    success_url = reverse_lazy('colleges_generic_html')


class EditStudent(LoginRequiredMixin, UpdateView):
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.change_student'
    permission_denied_message = "you cannot edit a student"
    template_name = 'add_student_form.html'
    model = Student
    form_class = AddStudentForm

    def get_context_data(self, **kwargs):
        context = super(EditStudent, self).get_context_data(**kwargs)
        student = get_object_or_404(Student, id=self.kwargs.get('pk'))
        mocktest = get_object_or_404(Mocktest, student_id=self.kwargs.get('pk'))
        mock = AddMockTestForm(instance=mocktest)
        stu = AddStudentForm(instance=student)
        context.update({
            'student_form': stu,
            'mocktest_form': mock,
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context

    def post(self, request, *args, **kwargs):
        college_object = get_object_or_404(College, pk=kwargs.get("college_id"))
        mocktest = get_object_or_404(Mocktest, student_id=self.kwargs.get('pk'))
        student = Student.objects.get(id=self.kwargs.get('pk'))
        student_form = AddStudentForm(request.POST, instance=student)
        mock_form = AddMockTestForm(request.POST, instance=mocktest)
        if student_form.is_valid():
            student.save()
            if mock_form.is_valid():
                mocktest.totals = sum(mock_form.cleaned_data.values())
                mocktest.save()
        return redirect("colleges_student_html", college_object.id)


class DeleteStudent(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = "/mentorapp/user/login/"
    permission_required = 'onlineapp.delete_student'
    permission_denied_message = "you cannot delete a student"
    model = Student
    template_name = "confirm_delete_college.html"

    def post(self, request, *args, **kwargs):
        college_object = get_object_or_404(College, pk=kwargs.get("college_id"))
        Student.objects.get(id=self.kwargs.get('pk')).delete()
        return redirect("colleges_student_html", college_object.id)


class signupForm(forms.Form):
    firstname = forms.CharField(label="First Name", max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    secondname = forms.CharField(label="Second Name", max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Username", max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=100, widget=PasswordInput(attrs={'class': 'form-control'}))


class SignUpController(View):
    # login_url = "/mentorapp/user/login/"
    myform = signupForm()

    def get(self, request):
        return render(request, template_name='signup_form.html', context={'form': self.myform},
                      content_type="text/html")

    def post(self, request, *args, **kwargs):
        signupform = signupForm(request.POST)
        if signupform.is_valid():
            # create user
            user = User.objects.create_user(signupform.cleaned_data["username"], None,
                                            signupform.cleaned_data["password"],
                                            first_name=signupform.cleaned_data["firstname"],
                                            last_name=signupform.cleaned_data["secondname"])

            check = authenticate(request, username=signupform.cleaned_data["username"],
                                 password=signupform.cleaned_data["password"])
            if check is not None:
                pass
                login(request, user)
                return redirect("colleges_generic_html")
            else:
                return redirect("login_form_html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login_form_html")


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=100, widget=PasswordInput(attrs={'class': 'form-control'}))


class LoginController(View):
    myloginform = LoginForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("colleges_generic_html")
        return render(request, template_name="login_form.html", context={'form': self.myloginform},
                      content_type="text/html")

    def post(self, request, *args, **kwargs):
        # myloginform = LoginForm()

        mynewloginform = LoginForm(request.POST)
        if mynewloginform.is_valid():
            username = mynewloginform.cleaned_data["username"]
            password = mynewloginform.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("colleges_generic_html")
            else:
                return redirect("login_form_html")
