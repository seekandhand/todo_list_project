from django.contrib import admin

from .models import ToDoList, Organization


admin.site.register(ToDoList)
admin.site.register(Organization)
