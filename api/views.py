from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer
from todo_lists.models import Organization, ToDoList
from users.models import CustomUser
from .serializers import OrganizationSerializer, ToDoListSerializer


class RegisterView(CreateAPIView):
    """
    View for user registration with the given email, organization and password
    """
    model = CustomUser
    permission_classes = [AllowAny]

    serializer_class = UserSerializer


class LoginView(APIView):
    """
    View for user authorization with the given email, organization and password
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        organization = request.data.get('organization')
        password = request.data.get('password')

        # Authenticate uses custom backend
        user = authenticate(email=email, organization=organization, password=password)

        if user:
            login(request, user)
            return Response(data='Success', status=status.HTTP_200_OK)
        else:
            return Response(data='Invalid login', status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout view
    """
    def get(self, request):
        logout(request)
        return Response(data='User logged out', status=status.HTTP_200_OK)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given Organization details.

    list:
    Return a list of existing Organization instances.

    create:
    Create a new Organization instance.

    update:
    Updates an Organization instance (replace).

    partial_update:
    Updates an Organization instance partially.

    delete:
    Deletes an Organization instance.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ToDoListViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given ToDoList details.

    list:
    Return a list of existing ToDoList instances.

    create:
    Create a new ToDoList instance.

    update:
    Updates ToDoList instance (replace).

    partial_update:
    Updates ToDoList instance partially.

    delete:
    Deletes ToDoList instance.
    """
    serializer_class = ToDoListSerializer

    def get_queryset(self):
        return ToDoList.objects.filter(organization=self.request.user.organization_id)
