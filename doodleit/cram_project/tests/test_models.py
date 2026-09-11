from django.test import TestCase
from cram.models import User
from django.contrib.auth import get_user_model

#article used to help write these tests is here
# https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Django/Testing#locallibrary_tests

User = get_user_model()

class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        #set up non modified objects used by all test methods 
        User.objects.create_user(
            username="doodlrTesting",
            email="test@email.com",
            password="doodlrTesting"
        )

    def test_username_max_length(self):
        print("Method: testing username max_length")
        user = User.objects.get(username="doodlrTesting")
        max_length = user._meta.get_field('username').max_length
        self.assertEqual(max_length, 20)

    def test_profile_picture_not_empty(self):
        print("Method: testing not empty profile_picture")
        user = User.objects.get(username="doodlrTesting")
        user_image = user._meta.get_field('profile_picture')
        print(user.profile_picture)
        self.assertIsNotNone(user_image)

    def test_profile_picture_is_default(self):
        print("Method: testing if profile uses the default picture when value is left empty")
        user = User.objects.get(username="doodlrTesting")
        profile_picture= user._meta.get_field('profile_picture')
        print(profile_picture)
        