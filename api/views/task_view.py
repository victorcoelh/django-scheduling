from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth.models import User

from api.serializers import TaskSerializer
from api.services.task_service import get_task, save_task


class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request, task_id: int) -> Response:
        user: User = request.user
        task = get_task(task_id, user)
        
        if task is None:
            return Response(
                data={"message": f"Task {task_id} not found for user {user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(TaskSerializer(task).data)
    
    def patch(self, request: Request, task_id: int) -> Response:       
        user: User = request.user
        task = get_task(task_id, user)
        
        if task is None:
            return Response(
                data={"message": f"Task {task_id} not found for user {user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        cache.delete(f"user_{user.username}_schedule")
        return Response(serializer.data)
    
    def delete(self, request: Request, task_id: int) -> Response:
        user: User = request.user
        task = get_task(task_id, user)
        
        if task is None:
            return Response(
                data={"message": f"Task {task_id} not found for user {user.username}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        task.delete()        
        cache.delete(f"user_{user.username}_schedule")
        return Response(status=status.HTTP_200_OK)


class TaskListView(APIView):
    def post(self, request: Request) -> Response:
        user: User = request.user
        serializer = TaskSerializer(data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        task = save_task(serializer, request.data.get("tags"), user) # type: ignore
        cache.delete(f"user_{user.username}_schedule")
        return Response(TaskSerializer(task).data, status=200)
