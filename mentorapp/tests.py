from django.test import TestCase

# Create your tests here.

from onlineapp.models import *
from mentorapp.serializers import CollegeSerializer

class CollegeTestcase(TestCase):
    def setUp(self):
        pass
    def test_college_serializer(self):
        vce = College.objects.get(acronym = "vce")
        teststr ='{"name": "Vasavi college of engineering", "location": "Hyderabad", "acronym": "vce", "contact": "contact@vce.edu"}'
        self.assertEqual( CollegeSerializer(vce).data ,teststr)
