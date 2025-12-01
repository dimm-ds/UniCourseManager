from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import University, Course, UniversityCourse
from . import serializers


class UniversityViewSet(ModelViewSet):
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer

    @action(detail=True, methods=['get'], url_path='courses')
    def get_courses(self, request, pk=None):
        university = self.get_object()
        courses = UniversityCourse.objects.filter(university=university)
        serializer = serializers.DetailUniversityCourseSerializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='course_stats')
    def get_data(self, request, pk=None):
        university = self.get_object()
        courses = UniversityCourse.objects.filter(university=university)
        total_courses = courses.count()
        average_duration = courses.aggregate(
            avg_duration=Avg('duration_weeks')
        )['avg_duration'] or 0

        data = {
            'total_courses': total_courses,
            'average_duration': round(average_duration, 2)
        }

        serializer = serializers.MeanUniversityCourseSerializer(data)
        return Response(serializer.data)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer


class UniversityCourseViewSet(ModelViewSet):
    queryset = UniversityCourse.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["university__name", "course__title"]
    ordering_fields = ["duration_weeks", "semester", "course__title"]
    filterset_fields = {
        'course__title': ['exact', 'icontains'],
        'semester': ['exact', 'contains'],
        'duration_weeks': ['exact', 'gte', 'lte'],
    }

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH", "PUT"]:
            return serializers.BaseUniversityCourseSerializer
        return serializers.FullUniversityCourseSerializer


