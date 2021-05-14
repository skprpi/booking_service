from rest_framework import serializers
from accounts.models import Price, Lesson


class LessonSerializer(serializers.ModelSerializer):
    student_pk = serializers.SerializerMethodField(read_only=True)
    teacher_pk = serializers.SerializerMethodField(read_only=True)


    def get_student_pk(self, obj):
        return str(obj.student_pk.email)

    def get_teacher_pk(self, obj):
        return str(obj.teacher_pk.email)

    class Meta:
        model = Lesson
        fields = '__all__'


class ThinLessonSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='lessons-detail')

    class Meta:
        model = Lesson
        fields = ('id', 'duration', 'start_datetime', 'url')

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'

