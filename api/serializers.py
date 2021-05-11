from rest_framework import serializers
from accounts.models import Price, Lesson


class LessonSerializer(serializers.ModelSerializer):
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

