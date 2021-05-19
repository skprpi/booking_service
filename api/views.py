from rest_framework import viewsets
from rest_framework.response import Response

from accounts.models import Lesson
from api.serializers import LessonSerializer, ThinLessonSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)
    # http_method_names = ['get', 'post']

    def list(self, request, *args, **kwargs):
        lessons = Lesson.objects.filter(student_pk=request.user.id) | Lesson.objects.filter(teacher_pk=request.user.id)
        context = {'request': request}
        serializer = ThinLessonSerializer(lessons, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(student_pk=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
