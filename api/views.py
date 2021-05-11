from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Lesson
from api.serializers import LessonSerializer
from rest_framework.views import APIView

class LessonListView(APIView):

    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LessonSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    def get_lesson_object(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, pk):
        lesson = self.get_lesson_object(pk)
        serializer = LessonSerializer(lesson)
        return Response(data=serializer.data)

    def put(self, request, pk):
        lesson = self.get_lesson_object(pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lesson = self.get_lesson_object(pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# @api_view(['GET', 'POST'])
# def lessons_list(request):
#     if request.method == 'GET':
#         lessons = Lesson.objects.all()
#         serializer = LessonSerializer(lessons, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = LessonSerializer(request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def lessons_detail(request, pk):
#     try:
#         lesson = Lesson.objects.get(pk=pk)
#     except Lesson.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = LessonSerializer(lesson)
#         return Response(data=serializer.data)
#     elif request.method == 'PUT':
#         serializer = LessonSerializer(lesson, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         lesson.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
