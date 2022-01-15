from django.db.models.fields import DecimalField
from computing_environment.models.job import Job
from computing_environment.models.sub_job import SubJob
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'language', 'program', 'settings']

class SubJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubJob
        fields = ['result', 'job', 'avg_processor_usage', 'avg_memory_usage']


class JobReportSerializer(serializers.Serializer):
    processor_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    memory_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
