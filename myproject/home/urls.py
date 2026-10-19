from django.urls import path
from home import views

urlpatterns = [

   path("task4/", views.dashboard, name="dashboard"),
    path(
        "students/add/",
        views.add_student,
        name="add_student"
    ),
    path(
        "marks/add/",
        views.add_marks,
        name="add_marks"
    ),


]