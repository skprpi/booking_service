from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from accounts.models import Lesson
from api.serializers import LessonSerializer, ThinLessonSerializer
from rest_framework.views import APIView
from rest_framework import viewsets


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def list(self, request, *args, **kwargs):
        lessons = Lesson.objects.all()
        context = {'request': request}
        serializer = ThinLessonSerializer(lessons, many=True, context=context)
        return Response(serializer.data)
