from rest_framework import serializers
from accounts.models import Lesson
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


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

