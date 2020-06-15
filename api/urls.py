from django.urls import path, include
from rest_framework import routers

from .views import RegisterView, LoginView, LogoutView, OrganizationViewSet, ToDoListViewSet


router = routers.DefaultRouter()

router.register(r'organizations', OrganizationViewSet)
router.register(r'todo_lists', ToDoListViewSet, basename='todo_lists')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
