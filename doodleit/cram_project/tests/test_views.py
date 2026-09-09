from django.test import TestCase
from cram.models import Doodle
from django.contrib.auth.mixins import LoginRequiredMixin

class DoodleViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass