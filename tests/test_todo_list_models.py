from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from todo_lists.models import Organization, ToDoList


class ToDoListTests(TestCase):
    """
    Class that tests Organization and ToDoList models creation and validation
    """
    def test_create_organization(self):
        organization = Organization.objects.create(name='some company')

        self.assertEqual(Organization.objects.get(id=organization.id).name, 'some company')

    def test_create_invalid_organization(self):
        invalid_organization1 = Organization(name='')
        Organization.objects.create(name='not unique')

        self.assertRaises(ValidationError, invalid_organization1.full_clean)
        self.assertRaises(IntegrityError, Organization(name='not unique').save)

    def test_create_todo_list(self):
        organization = Organization.objects.create(name='some company')

        todo_list_line1 = ToDoList.objects.create(organization=organization, text='1) Wake up', is_finished=True)
        todo_list_line2 = ToDoList.objects.create(organization=organization, text='2) Do yoga', is_finished=False)

        self.assertEqual(ToDoList.objects.get(id=todo_list_line1.id).text, '1) Wake up')
        self.assertEqual(ToDoList.objects.get(id=todo_list_line2.id).is_finished, False)

        with self.assertRaises(ValueError):
            ToDoList.objects.create(organization='not an object', text='1) Wake up', is_finished=True)
