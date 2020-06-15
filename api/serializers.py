from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from todo_lists.models import Organization, ToDoList
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'organization', 'password']

    def create(self, validated_data):
        """
        Function validates organization_id field and adds it if necessary before saving, hashes password
        """
        try:
            organization_obj = Organization.objects.get(name=validated_data.get('organization'))
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                {'validation_error': 'You can not register a user if his organization does not exist'}
            )

        validated_data['organization_id'] = organization_obj
        validated_data['password'] = make_password(validated_data.get('password'))

        return super(UserSerializer, self).create(validated_data)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = ['id', 'text', 'is_finished']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Function sets organization field equal to the current user's organization and saves instance
        """
        validated_data['organization'] = self.context.get('request').user.organization_id

        return super(ToDoListSerializer, self).create(validated_data)
