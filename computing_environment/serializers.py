from computing_environment.models.job import Job
from computing_environment.models.job_result import JobResult
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'program', 'settings']

class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ['result', 'job']
