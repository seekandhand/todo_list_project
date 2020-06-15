from django.db import models


class Organization(models.Model):
    """
    A table representing organizations
    """
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    """
    A table representing lines of ToDoList and information whether they were crossed out
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='todo_list')
    text = models.TextField(max_length=1000)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.id
