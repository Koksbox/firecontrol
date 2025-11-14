# api/views.py
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
from .serializers import (
    UserSerializer, ObjectTypeSerializer, FireObjectSerializer, ResponsiblePersonSerializer,
    FireExtinguisherSerializer, InspectionReportSerializer, InspectionPhotoSerializer,
    NormativeDocumentSerializer, NotificationSerializer
)
from accounts.models import User
from objects.models import ObjectType, FireObject, ResponsiblePerson
from fire_safety.models import FireExtinguisher
from inspections.models import InspectionReport, InspectionPhoto
from normative.models import NormativeDocument
from notifications.models import Notification
from .permissions import IsInspectorOrReadOnly, IsAssignedInspectorForObject

# Auth endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain_pair(request):
    """
    Логин: принимает username/email + password и возвращает JWT.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if not user:
        # попробуем по email
        try:
            u = User.objects.get(email=username)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            user = None
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_pin(request):
    pin = request.data.get('pin')
    if not pin or len(pin) < 4:
        return Response({'detail': 'PIN must be at least 4 digits'}, status=400)
    user = request.user
    user.set_pin(pin)
    user.save()
    return Response({'detail': 'PIN set'})

@api_view(['POST'])
@permission_classes([AllowAny])
def token_with_pin(request):
    """
    Получение токена по username + pin (быстрый вход).
    """
    username = request.data.get('username')
    pin = request.data.get('pin')
    if not username or not pin:
        return Response({'detail': 'username and pin required'}, status=400)
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        try:
            u = User.objects.get(email=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

    if not u.check_pin(pin):
        return Response({'detail': 'Invalid PIN'}, status=400)

    refresh = RefreshToken.for_user(u)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(u).data
    })

# FCM token register
from rest_framework.views import APIView
class PushTokenView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get('token')
        platform = request.data.get('platform', 'android')
        if not token:
            return Response({'detail': 'token required'}, status=400)
        # Сохраните token: можно создать модель Device/PushToken — здесь простая реализация:
        request.user.profile_fcm_token = token  # если нет модели — замените на ваш storage
        request.user.save()
        return Response({'detail': 'registered'})

# ViewSets
class ObjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer
    permission_classes = [IsAuthenticated]

class FireObjectViewSet(viewsets.ModelViewSet):
    queryset = FireObject.objects.all()
    serializer_class = FireObjectSerializer
    permission_classes = [IsAuthenticated, IsInspectorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        # фильтрация по архиву/поиск может быть на клиенте; API поддерживает query params
        is_archived = self.request.query_params.get('is_archived')
        q = self.request.query_params.get('q')
        if is_archived is not None:
            qs = qs.filter(is_archived=(is_archived.lower() in ['1', 'true', 'yes']))
        if q:
            qs = qs.filter(
                name__icontains=q
            )
        return qs

class ResponsiblePersonViewSet(viewsets.ModelViewSet):
    queryset = ResponsiblePerson.objects.all()
    serializer_class = ResponsiblePersonSerializer
    permission_classes = [IsAuthenticated, IsInspectorOrReadOnly]

    def perform_create(self, serializer):
        # если не указан assigned_by — ставим текущего
        serializer.save(assigned_by=self.request.user)

class FireExtinguisherViewSet(viewsets.ModelViewSet):
    queryset = FireExtinguisher.objects.all()
    serializer_class = FireExtinguisherSerializer
    permission_classes = [IsAuthenticated, IsInspectorOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        fire_object_id = self.request.query_params.get('fire_object_id')
        if fire_object_id:
            qs = qs.filter(fire_object_id=fire_object_id)
        return qs

class InspectionReportViewSet(viewsets.ModelViewSet):
    queryset = InspectionReport.objects.all().prefetch_related('photos')
    serializer_class = InspectionReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # автоматически назначаем инспектор текущим пользователем, если не указан
        inspector = self.request.user
        serializer.save(inspector=inspector)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_photo(self, request, pk=None):
        inspection = self.get_object()
        ser = InspectionPhotoSerializer(data=request.data)
        if ser.is_valid():
            ser.save(inspection=inspection)
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

class InspectionPhotoViewSet(viewsets.ModelViewSet):
    queryset = InspectionPhoto.objects.all()
    serializer_class = InspectionPhotoSerializer
    permission_classes = [IsAuthenticated]

class NormativeDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NormativeDocument.objects.all()
    serializer_class = NormativeDocumentSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ReadOnlyModelViewSet, mixins.UpdateModelMixin):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'detail': 'ok'})

# Simple sync endpoints (timestamp-based)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sync_changes(request):
    """
    Клиент передаёт ?since=ISO8601 и получает все изменения сущностей с updated_at > since.
    Формат: ?since=2025-11-01T12:00:00
    """
    since = request.query_params.get('since')
    try:
        since_dt = datetime.fromisoformat(since) if since else None
    except Exception:
        return Response({'detail': 'invalid since format, use ISO timestamp'}, status=400)

    def qset_to_data(qs, serializer_class):
        return serializer_class(qs, many=True, context={'request': request}).data

    data = {}
    if not since_dt:
        # при первом полном sync клиент может получить всё (ограничьте выборки)
        data['objects'] = qset_to_data(FireObject.objects.filter(is_archived=False), FireObjectSerializer)
        data['extinguishers'] = qset_to_data(FireExtinguisher.objects.filter(is_active=True), FireExtinguisherSerializer)
        data['inspections'] = qset_to_data(InspectionReport.objects.all().order_by('-date')[:200], InspectionReportSerializer)
        data['documents'] = qset_to_data(NormativeDocument.objects.all(), NormativeDocumentSerializer)
    else:
        data['objects'] = qset_to_data(FireObject.objects.filter(updated_at__gt=since_dt), FireObjectSerializer)
        data['extinguishers'] = qset_to_data(FireExtinguisher.objects.filter(updated_at__gt=since_dt), FireExtinguisherSerializer)
        data['inspections'] = qset_to_data(InspectionReport.objects.filter(updated_at__gt=since_dt), InspectionReportSerializer)
        data['documents'] = qset_to_data(NormativeDocument.objects.filter(created_at__gt=since_dt), NormativeDocumentSerializer)

    data['server_time'] = timezone.now().isoformat()
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sync_push_changes(request):
    """
    Клиент отправляет локальные изменения в формате:
    {
      "objects": [...],
      "extinguishers": [...],
      "inspections": [...],
    }
    Backend должен валидацию, создать/обновить записи и вернуть статусы per-item.
    """
    payload = request.data
    results = {'objects': [], 'extinguishers': [], 'inspections': []}

    # objects
    for obj in payload.get('objects', []):
        try:
            if 'id' in obj and obj['id']:
                instance = FireObject.objects.get(id=obj['id'])
                ser = FireObjectSerializer(instance, data=obj, partial=True)
            else:
                ser = FireObjectSerializer(data=obj)
            if ser.is_valid():
                saved = ser.save()
                results['objects'].append({'local_id': obj.get('local_id'), 'id': saved.id, 'status': 'ok'})
            else:
                results['objects'].append({'local_id': obj.get('local_id'), 'errors': ser.errors, 'status': 'error'})
        except Exception as e:
            results['objects'].append({'local_id': obj.get('local_id'), 'errors': str(e), 'status': 'error'})

    # extinguishers (аналогично)
    for ex in payload.get('extinguishers', []):
        try:
            if 'id' in ex and ex['id']:
                instance = FireExtinguisher.objects.get(id=ex['id'])
                ser = FireExtinguisherSerializer(instance, data=ex, partial=True)
            else:
                ser = FireExtinguisherSerializer(data=ex)
            if ser.is_valid():
                saved = ser.save()
                results['extinguishers'].append({'local_id': ex.get('local_id'), 'id': saved.id, 'status': 'ok'})
            else:
                results['extinguishers'].append({'local_id': ex.get('local_id'), 'errors': ser.errors, 'status': 'error'})
        except Exception as e:
            results['extinguishers'].append({'local_id': ex.get('local_id'), 'errors': str(e), 'status': 'error'})

    # inspections
    for ins in payload.get('inspections', []):
        try:
            if 'id' in ins and ins['id']:
                instance = InspectionReport.objects.get(id=ins['id'])
                ser = InspectionReportSerializer(instance, data=ins, partial=True)
            else:
                ser = InspectionReportSerializer(data=ins)
            if ser.is_valid():
                # сохраняем инспектора как текущего, если не передан
                saved = ser.save(inspector=request.user if not ser.validated_data.get('inspector') else ser.validated_data.get('inspector'))
                results['inspections'].append({'local_id': ins.get('local_id'), 'id': saved.id, 'status': 'ok'})
            else:
                results['inspections'].append({'local_id': ins.get('local_id'), 'errors': ser.errors, 'status': 'error'})
        except Exception as e:
            results['inspections'].append({'local_id': ins.get('local_id'), 'errors': str(e), 'status': 'error'})

    return Response({'results': results, 'server_time': timezone.now().isoformat()})
