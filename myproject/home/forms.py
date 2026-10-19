
from django import forms
from django.core.exceptions import ValidationError
from .models import Student1, Marks


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student1
        fields = [
            "roll_number",
            "full_name",
            "email",
            "phone",
            "department",
            "year",
            "date_of_birth",
            "address",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={"type": "date"}
            ),
            "address": forms.Textarea(
                attrs={"rows": 2}
            ),
            "phone": forms.TextInput(
                attrs={
                    "maxlength": "10",
                    "inputmode": "numeric"
                }
            ),
        }

    def clean_roll_number(self):
        roll = self.cleaned_data["roll_number"].strip().upper()

        if not roll.replace("-", "").replace("_", "").isalnum():
            raise ValidationError(
                "Use letters, numbers, hyphens or underscores."
            )

        return roll

    def clean_full_name(self):
        name = " ".join(
            self.cleaned_data["full_name"].split()
        )

        if not all(
            char.isalpha() or char in " .'-"
            for char in name
        ):
            raise ValidationError(
                "Enter a valid student name."
            )

        return name

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class MarksForm(forms.ModelForm):

    class Meta:
        model = Marks
        fields = [
            "student",
            "subject_code",
            "subject_name",
            "semester",
            "internal_marks",
            "external_marks",
        ]

        widgets = {
            "internal_marks": forms.NumberInput(
                attrs={"min": 0, "max": 30}
            ),
            "external_marks": forms.NumberInput(
                attrs={"min": 0, "max": 70}
            ),
        }

    def clean_subject_code(self):
        return self.cleaned_data["subject_code"].strip().upper()

    def clean(self):
        cleaned = super().clean()

        student = cleaned.get("student")
        subject = cleaned.get("subject_code")
        semester = cleaned.get("semester")

        if student and subject and semester:
            duplicate = Marks.objects.filter(
                student=student,
                subject_code__iexact=subject,
                semester=semester,
            )

            if self.instance.pk:
                duplicate = duplicate.exclude(
                    pk=self.instance.pk
                )

            if duplicate.exists():
                raise ValidationError(
                    "Marks already exist for this student, "
                    "subject and semester."
                )

        return cleaned
