from rest_framework import serializers
from .models import University, Course, UniversityCourse


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        read_only_fields = ["id"]
        fields = [
            "id",
            "name",
            "country"
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ["id"]
        fields = [
            "id",
            "title",
            "description"
        ]


class UniversityCourseSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks"
        ]


class UniversityCourseDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='course.title', read_only=True)
    description = serializers.CharField(source='course.description', read_only=True)

    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "title",
            "description",
            "semester",
            "duration_weeks"
        ]


class FullUniversityCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = UniversityCourse
        read_only_fields = ["id"]
        fields = [
            "id",
            "university",
            "course",
            "semester",
            "duration_weeks"
        ]


class UniversityCourseMeanSerializer(serializers.Serializer):
    total_courses = serializers.IntegerField()
    average_duration = serializers.FloatField()