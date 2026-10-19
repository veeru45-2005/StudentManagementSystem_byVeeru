
from django.contrib import admin


from .models import Student1, Marks


class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0


@admin.register(Student1)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "roll_number",
        "full_name",
        "department",
        "year",
        "email",
        "phone",
    )

    search_fields = (
        "roll_number",
        "full_name",
        "email",
    )

    list_filter = ("department", "year")

    inlines = [MarksInline]


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject_code",
        "subject_name",
        "semester",
        "internal_marks",
        "external_marks",
        "show_total",
        "grade",
        "result",
    )

    search_fields = (
        "student__roll_number",
        "student__full_name",
        "subject_code",
    )

    list_filter = ("semester",)

    @admin.display(description="Total")
    def show_total(self, obj):
        return obj.total

                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    

