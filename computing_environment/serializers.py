from django.db.models import fields
from django.core.validators import FileExtensionValidator
from computing_environment.models.job import Job
from computing_environment.models.worker import Worker
from computing_environment.models.sub_job import SubJob
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'language', 'program']

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'processor', 'ram']

class SubJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    worker = WorkerSerializer(read_only=True)
    
    class Meta:
        model = SubJob
        fields = ['id', 'job', 'worker', 'settings', 'processor_usage', 'memory_usage']

class SubJobResultSerializer(serializers.Serializer):
    failed = serializers.BooleanField(default=False)
    result = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['zip', 'rar'])])
    avg_processor_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    avg_memory_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)

class JobReportSerializer(serializers.Serializer):
    processor_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    memory_usage = serializers.DecimalField(required=True, max_digits=5, decimal_places=2)
    processor = serializers.CharField(required=True, max_length=254)
    ram = serializers.CharField(required=True, max_length=10)
