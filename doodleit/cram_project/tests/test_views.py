from django.test import TestCase
from cram.models import Doodle
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class DoodleViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testingDoodlr',
            email='testing@email.com',
            password='hdOrderpicker1!'
        )

        cls.testDoodle = Doodle.objects.create(
            title='test doodle',
            image='testing.png',
            doodlr=cls.user
        )
    
    def test_doodle_has_doodlr(self):
        print("Method: testing doodle has doodlr ")
        doodle=Doodle.objects.get(id=self.testDoodle.id)

        self.assertEqual(doodle.doodlr, self.user)
        self.assertEqual(doodle.doodlr.username, 'testingDoodlr')