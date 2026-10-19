from django.shortcuts import render,redirect


from django.db import IntegrityError, transaction
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages

from .models import Student1, Marks
from .forms import StudentForm, MarksForm


def dashboard(request):
    search = request.GET.get("q", "").strip()

    students = Student1.objects.all()

    if search:
        students = students.filter(
            Q(roll_number__icontains=search)
            | Q(full_name__icontains=search)
            | Q(email__icontains=search)
            | Q(department__icontains=search)
        )

    context = {
        "students": students,
        "marks_records": Marks.objects.select_related(
            "student"
        ).all(),
        "student_form": StudentForm(),
        "marks_form": MarksForm(),
        "total_students": Student1.objects.count(),
        "total_marks": Marks.objects.count(),
        "search": search,
    }

    return render(
        request,
        "task4.html",
        context
    )


@require_POST
def add_student(request):
    form = StudentForm(request.POST)

    if form.is_valid():
        try:
            with transaction.atomic():
                form.save()

            messages.success(
                request,
                "Student details saved successfully."
            )

        except IntegrityError:
            messages.error(
                request,
                "Roll number or email already exists."
            )

    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    return redirect("dashboard")


@require_POST
def add_marks(request):
    form = MarksForm(request.POST)

    if form.is_valid():
        try:
            with transaction.atomic():
                form.save()

            messages.success(
                request,
                "Student marks saved successfully."
            )

        except IntegrityError:
            messages.error(
                request,
                "Duplicate marks are not allowed."
            )

    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)

    return redirect("dashboard")
