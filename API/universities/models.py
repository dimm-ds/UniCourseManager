import re
from django.db import models
from django.core.exceptions import ValidationError


def validate_semester_format(value):
    if not re.match(r'^(spring|autumn)_\d{4}$', value):
        raise ValidationError(
            'Semester must be in format: "spring_YYYY" or "autumn_YYYY"'
        )


class University (models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='unique_university_name_country')
        ]

    def __str__(self):
        return f'University {self.name} - {self.country}'


class Course (models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_course_title_name')
        ]

    def __str__(self):
        if len(self.description) < 100:
            desc = self.description
        else:
            desc = self.description[:100]
        return f'Course {self.title} - {desc}...'


class UniversityCourse(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20, validators=[validate_semester_format])
    duration_weeks = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'course', 'semester'],
                                    name='unique_course_per_university_semester'
                                    )
        ]

    def __str__(self):
        return f'{self.university.name} - {self.course.title} ({self.semester})'