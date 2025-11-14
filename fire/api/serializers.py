# api/serializers.py
from rest_framework import serializers
from accounts.models import User
from objects.models import FireObject, ObjectType, ResponsiblePerson
from fire_safety.models import FireExtinguisher
from inspections.models import InspectionReport, InspectionPhoto
from normative.models import NormativeDocument
from notifications.models import Notification

# User minimal serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'phone']

# ObjectType
class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = ['id', 'name']

# FireObject
class FireObjectSerializer(serializers.ModelSerializer):
    object_type = ObjectTypeSerializer(read_only=True)
    object_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ObjectType.objects.all(), source='object_type', write_only=True
    )

    class Meta:
        model = FireObject
        fields = [
            'id', 'name', 'legal_address', 'actual_address', 'object_type', 'object_type_id',
            'fire_class', 'is_archived', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

# ResponsiblePerson
class ResponsiblePersonSerializer(serializers.ModelSerializer):
    assigned_by = UserSerializer(read_only=True)
    assigned_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_by', write_only=True, required=False, allow_null=True
    )
    fire_object_id = serializers.PrimaryKeyRelatedField(
        queryset=FireObject.objects.all(), source='fire_object', write_only=True
    )

    class Meta:
        model = ResponsiblePerson
        fields = ['id', 'fire_object', 'fire_object_id', 'name', 'position',
                  'phone_work', 'phone_mobile', 'email', 'assigned_by', 'assigned_by_id', 'assigned_at']
        read_only_fields = ['assigned_at', 'fire_object']

# FireExtinguisher
class FireExtinguisherSerializer(serializers.ModelSerializer):
    fire_object = FireObjectSerializer(read_only=True)
    fire_object_id = serializers.PrimaryKeyRelatedField(
        queryset=FireObject.objects.all(), source='fire_object', write_only=True
    )

    class Meta:
        model = FireExtinguisher
        fields = ['id', 'fire_object', 'fire_object_id', 'inventory_number', 'type',
                  'location', 'last_refill_date', 'next_check_date', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

# InspectionPhoto serializer (handles upload)
class InspectionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionPhoto
        fields = ['id', 'inspection', 'photo', 'caption']
        read_only_fields = ['id']

# InspectionReport
class InspectionReportSerializer(serializers.ModelSerializer):
    fire_object = FireObjectSerializer(read_only=True)
    fire_object_id = serializers.PrimaryKeyRelatedField(
        queryset=FireObject.objects.all(), source='fire_object', write_only=True
    )
    inspector = UserSerializer(read_only=True)
    inspector_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='inspector', write_only=True, required=False
    )
    photos = InspectionPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = InspectionReport
        fields = ['id', 'fire_object', 'fire_object_id', 'inspector', 'inspector_id',
                  'date', 'notes', 'status', 'pdf_file', 'photos', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'pdf_file', 'photos']

# NormativeDocument
class NormativeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormativeDocument
        fields = ['id', 'title', 'doc_number', 'issue_date', 'file', 'url', 'created_at']

# Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at', 'notification_type', 'content_type', 'object_id']
        read_only_fields = ['created_at']
