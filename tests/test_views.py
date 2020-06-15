from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase

from todo_lists.models import Organization, ToDoList


class RegistrationTestCase(APITestCase):
    """
    Class for testing valid and invalid usage of RegisterView, LoginView, LogoutView
    """
    def setUp(self):
        Organization.objects.create(name='Test Company')

    def test_registration_login_and_logout(self):
        data = {
            "email": "simple@email.com",
            "organization": "Test Company",
            "password": "foo"
        }

        response1 = self.client.post('/api/register/', data)
        response2 = self.client.post('/api/login/', data)
        response3 = self.client.get('/api/logout/')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_register_multiple_users(self):
        Organization.objects.create(name='Test Company 2')

        data1 = {
            "email": "simple1@email.com",
            "organization": "Test Company",
            "password": "foo"
        }
        data2 = {
            "email": "simple1@email.com",
            "organization": "Test Company 2",
            "password": "foo"
        }
        data3 = {
            "email": "simple2@email.com",
            "organization": "Test Company",
            "password": "foo"
        }

        response1 = self.client.post('/api/register/', data1)
        response2 = self.client.post('/api/register/', data2)
        response3 = self.client.post('/api/register/', data3)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_register_non_existing_organization(self):
        data = {
            "email": "simple@email.com",
            "organization": "non existing company",
            "password": "foo"
        }

        response = self.client.post('/api/register/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get('validation_error'),
            'You can not register a user if his organization does not exist',
        )

    def test_invalid_login(self):
        data = {
            "email": "simple@email.com",
            "organization": "Test Company 123",
            "password": "foo"
        }

        response = self.client.post('/api/register/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationTestCase(APITestCase):
    """
    Class for testing IsAuthenticated permission
    """
    def test_not_authenticated(self):
        response1 = self.client.get('/api/')
        response2 = self.client.get('/api/logout/')
        response3 = self.client.get('/api/organizations/')
        response4 = self.client.get('/api/todo_lists/')

        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response4.status_code, status.HTTP_403_FORBIDDEN)


class OrganizationViewTestCase(APITestCase):
    """
    Class for testing Organization CRUD
    """
    def setUp(self):
        self.organization1 = Organization.objects.create(name='Test Company')
        self.organization2 = Organization.objects.create(name='Test Company 2')

        data = {
            "email": "simple@email.com",
            "organization": "Test Company",
            "password": "foo"
        }

        self.client.post('/api/register/', data)
        self.client.post('/api/login/', data)

    def test_get_organizations(self):
        json_benchmark = [{'id': self.organization1.id, 'name': 'Test Company'},
                          {'id': self.organization2.id, 'name': 'Test Company 2'}]

        response = self.client.get('/api/organizations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_benchmark)

    def test_get_organization(self):
        json_benchmark = {'id': self.organization1.id, 'name': 'Test Company'}

        response = self.client.get('/api/organizations/' + str(self.organization1.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_benchmark)

    def test_post_organization(self):
        response = self.client.post('/api/organizations/', {'name': 'Test Company 3'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.get(name='Test Company 3').name, 'Test Company 3')

    def test_put_organization(self):
        response = self.client.put('/api/organizations/' + str(self.organization1.id) + '/', {'name': 'New Name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(id=self.organization1.id).name, 'New Name')

    def test_delete_organization(self):
        response = self.client.delete('/api/organizations/' + str(self.organization1.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            Organization.objects.get(id=self.organization1.id)


class ToDoListViewTestCase(APITestCase):
    """
    Class for testing ToDoList CRUD and
    that a user from a specific organization only gets access to a ToDoList of that organization
    """
    def setUp(self):
        self.organization1 = Organization.objects.create(name='Test Company 1')
        self.organization2 = Organization.objects.create(name='Test Company 2')

        self.todo_list_line1 = ToDoList.objects.create(
            organization=self.organization1,
            text='1) Wake up',
            is_finished=True,
        )
        self.todo_list_line2 = ToDoList.objects.create(
            organization=self.organization1,
            text='2) Do yoga',
            is_finished=False,
        )
        self.todo_list_line3 = ToDoList.objects.create(
            organization=self.organization2,
            text='Do nothing',
            is_finished=False,
        )

        data = {
            "email": "simple@email.com",
            "organization": "Test Company 1",
            "password": "foo"
        }

        self.client.post('/api/register/', data)
        self.client.post('/api/login/', data)

    def test_get_todo_lists(self):
        json_benchmark = [{'id': self.todo_list_line1.id, 'text': '1) Wake up', 'is_finished': True},
                          {'id': self.todo_list_line2.id, 'text': '2) Do yoga', 'is_finished': False}]

        response = self.client.get('/api/todo_lists/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_benchmark)

    def test_get_todo_list(self):
        json_benchmark = {'id': self.todo_list_line1.id, 'text': '1) Wake up', 'is_finished': True}

        response = self.client.get('/api/todo_lists/' + str(self.todo_list_line1.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), json_benchmark)

    def test_get_todo_list_from_another_organization(self):
        response = self.client.get('/api/todo_lists/' + str(self.todo_list_line3.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_todo_list(self):
        response = self.client.post('/api/todo_lists/', {'text': '3) Make breakfast', 'is_finished': False})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDoList.objects.get(text='3) Make breakfast').organization, self.organization1)

    def test_post_todo_list_to_another_organization(self):
        data = {'organization': self.organization2, 'text': '3) Make breakfast', 'is_finished': False}

        response = self.client.post('/api/todo_lists/', data)

        # ToDoList Line created anyway for the organization corresponding to the user
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ToDoList.objects.get(text='3) Make breakfast').organization, self.organization1)

    def test_put_todo_list(self):
        data = {'text': '2) Do yoga', 'is_finished': True}

        response = self.client.put('/api/todo_lists/' + str(self.todo_list_line2.id) + '/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ToDoList.objects.get(id=self.todo_list_line2.id).is_finished, True)

    def test_put_todo_list_from_another_organization(self):
        data = {'text': 'Stop procrastinating', 'is_finished': True}

        response = self.client.put('/api/todo_lists/' + str(self.todo_list_line3.id) + '/', data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todo_list(self):
        response = self.client.delete('/api/todo_lists/' + str(self.todo_list_line1.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(ObjectDoesNotExist):
            ToDoList.objects.get(id=self.todo_list_line1.id)

    def test_delete_todo_list_from_another_organization(self):
        response = self.client.delete('/api/todo_lists/' + str(self.todo_list_line3.id) + '/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
