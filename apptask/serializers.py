from rest_framework import serializers
from apptask.models import User
from apptask.models import Task

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'name'
                 )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id',
                  'description',
                  'state',
                  'user_id'
                 )