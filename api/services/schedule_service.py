from typing import Any

from django.contrib.auth.models import User
from django.core.cache import cache

from api.models.task_model import Task
from api.serializers import TaskSerializer
from api.utils.constants import CACHE_KEY


def get_schedule_from_cache(user: User) -> dict[str, Any] | None:
    """Retrieves the cached schedule data for a given user.

    Args:
        user (User): The user whose schedule is being requested.

    Returns:
        dict[str, Any] | None: The cached schedule data if available, otherwise None.
    """
    return cache.get(CACHE_KEY.format(user.username))

def schedule_service(user: User) -> list[dict[str, Any]]:
    """Fetches the user's schedule from the database and stores it in cache.
    This is used when no valid cached data is found. Results are cached 
    for 10 minutes.

    Args:
        user (User): The user whose schedule is being generated.

    Returns:
        list[dict[str, Any]]: A serialized list of the user's tasks ordered by date.
    """
    tasks = Task.objects\
        .filter(owner=user)\
        .order_by("date")

    tasks = TaskSerializer(tasks, many=True).data
    cache.set(CACHE_KEY.format(user.username), tasks, 600)
    return tasks # type: ignore
