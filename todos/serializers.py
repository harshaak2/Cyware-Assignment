# serializers are used to convert complex data types to Python data types that can be easily rendered into JSON/XML, or to other types

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
  class Meta: 
    model = Task
    fields = "__all__"
    read_only_fields = ['created_by', 'created_at']