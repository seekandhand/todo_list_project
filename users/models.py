from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from todo_lists.models import Organization


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email and organization are unique identifiers
    for authentication instead of username
    """
    def create_user(self, email, organization, password=None):
        """
        Create and save a User with the given email, organization and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not organization:
            raise ValueError('Users must have an organization name')

        try:
            organization_obj = Organization.objects.get(name=organization)
        except Organization.DoesNotExist:
            raise ValueError('You can not register a user if his organization does not exist')

        user = self.model(
            email=self.normalize_email(email),
            organization=organization,
            organization_id=organization_obj,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, organization, password=None, id=None):
        """
        Create and save a SuperUser with the given email, organization and password
        """
        user = self.create_user(email=self.normalize_email(email), password=password, organization=organization)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Class that overrides default user model
    """
    email = models.EmailField(verbose_name='email', max_length=60)
    organization = models.CharField(max_length=100)
    organization_id = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
        db_column='organization_id',
    )
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'organization', ]

    objects = CustomUserManager()

    class Meta:
        unique_together = ['email', 'organization']

    def __str__(self):
        return self.email + ' - ' + self.organization

    def save(self, *args, **kwargs):
        """
        Additional validation that user has valid organization_id corresponding to organization name
        """
        try:
            organization_obj = Organization.objects.get(name=self.organization)
        except Organization.DoesNotExist:
            raise ValidationError(
                {'validation_error': "User's organization does not exist"}
            )

        if self.organization_id_id is None:
            self.organization_id = organization_obj

        super().save(*args, **kwargs)
