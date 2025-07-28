from datetime import datetime
from typing import Any
from django.contrib.auth.models import User

from api.models.task_model import Task
from api.serializers import TaskSerializer


def get_task(task_id: int, user: User) -> Task | None:
    """Retrieves a task by ID if it belongs to the given user.

    Args:
        task_id (int): The ID of the task to retrieve.
        user (User): The user requesting the task.

    Returns:
        Task | None: The task if found, otherwise None.
    """
    try:
        return Task.objects.get(task_id=task_id, owner=user)
    except Task.DoesNotExist:
        return None
    
def save_task(task_serializer: TaskSerializer, tags: list[str], user: User) -> Task:
    """Saves a new task using validated serializer data and associates it with the user and tags.

    Args:
        task_serializer (TaskSerializer): A serializer instance with validated task data.
        tags (list[str]): A list of tag names matching existing Tag Models,\
        to associate with the given task.
        user (User): The user who owns the task.

    Returns:
        Task: The newly saved task instance.
    """
    task_dict: dict[str, Any] = task_serializer.validated_data # type: ignore
    task_dict["owner"] = user
    task_dict["status"] = "PENDING"
    task_dict["created_on"] = datetime.now().date()

    task_obj = task_serializer.save()    
    for tag in tags:
        task_obj.tags.add(tag)

    return task_obj
