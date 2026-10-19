





from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import date


class Student1(models.Model):

    DEPARTMENTS = [
        ("CSE", "CSE"),
        ("ECE", "ECE"),
        ("EEE", "EEE"),
        ("IT", "IT"),
        ("CIVIL", "Civil"),
        ("MECH", "Mechanical"),
        ("AIDS", "AI & Data Science"),
    ]

    YEARS = [
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year"),
    ]

    roll_number = models.CharField(
        max_length=20, unique=True
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{10}$",
                message="Enter exactly 10 digits."
            )
        ]
    )
    department = models.CharField(
        max_length=10, choices=DEPARTMENTS
    )
    year = models.CharField(
        max_length=10, choices=YEARS
    )
    date_of_birth = models.DateField()
    address = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        self.roll_number = self.roll_number.strip().upper()
        self.full_name = " ".join(self.full_name.split())
        self.email = self.email.strip().lower()

        if self.date_of_birth and self.date_of_birth >= date.today():
            raise ValidationError({
                "date_of_birth": "Date of birth must be in the past."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.roll_number} - {self.full_name}"


class Marks(models.Model):

    SEMESTERS = [
        (str(i), f"Semester {i}")
        for i in range(1, 9)
    ]

    student = models.ForeignKey(
        Student1,
        on_delete=models.CASCADE,
        related_name="marks"
    )
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)
    semester = models.CharField(
        max_length=1, choices=SEMESTERS
    )

    internal_marks = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(30)
        ]
    )
    external_marks = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(70)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject_code",
                    "semester"
                ],
                name="unique_student_subject_semester"
            )
        ]

    def clean(self):
        super().clean()

        self.subject_code = self.subject_code.strip().upper()
        self.subject_name = " ".join(self.subject_name.split())

        if not 0 <= self.internal_marks <= 30:
            raise ValidationError({
                "internal_marks": "Enter marks from 0 to 30."
            })

        if not 0 <= self.external_marks <= 70:
            raise ValidationError({
                "external_marks": "Enter marks from 0 to 70."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.internal_marks + self.external_marks

    @property
    def percentage(self):
        return self.total

    @property
    def grade(self):
        if self.total >= 90:
            return "A+"
        elif self.total >= 80:
            return "A"
        elif self.total >= 70:
            return "B"
        elif self.total >= 60:
            return "C"
        elif self.total >= 50:
            return "D"
        elif self.total >= 40:
            return "E"
        return "F"

    @property
    def result(self):
        if self.internal_marks >= 12 and self.total >= 40:
            return "Pass"
        return "Fail"

    def __str__(self):
        return (
            f"{self.student.roll_number} - "
            f"{self.subject_code} - Semester {self.semester}"
        )
