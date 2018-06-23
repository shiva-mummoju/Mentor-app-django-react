from django.test import TestCase

# Create your tests here.

import os

import MySQLdb
import click
import django
from django.core.management import call_command
from openpyxl import load_workbook

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineproject.settings")
django.setup()
from onlineapp.models import *

manager = College.objects
queryset = College.objects.all()

print(queryset)
for i in queryset:
    print(i)
