from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from todo_lists.models import Organization


class UsersManagersTests(TestCase):
    """
    Class that tests CustomUser model creation and validation
    """
    def test_create_user(self):
        user_model = get_user_model()

        Organization.objects.create(name='some company')
        user = user_model.objects.create_user(email='normal@user.com', organization='some company', password='foo')
        
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='', organization='some company', password='foo')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='good@mail.com', organization='not existing company', password='foo')
        with self.assertRaises(IntegrityError):
            user_model.objects.create_user(email='normal@user.com', organization='some company', password='foo1')

    def test_create_superuser(self):
        user_model = get_user_model()

        Organization.objects.create(name='some company')
        admin_user = user_model.objects.create_superuser('super@user.com', 'some company', 'foo')
        
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(email='super@user.com', organization='', password='foo')
