from django.urls import path
from .views import TaskDetailView, TaskListView, RegisterView, ScheduleView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("tasks/", TaskListView.as_view()),
    path("tasks/<int:task_id>", TaskDetailView.as_view()),
    path("schedule/", ScheduleView.as_view())
]
