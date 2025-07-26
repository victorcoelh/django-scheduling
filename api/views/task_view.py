from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.core.cache import cache

from api.forms import TaskForm
from api.models import Task
from api.serializers import TaskSerializer


class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, task_id: int):
        task = Task.objects.get(
            task_id=task_id,
            owner=self.request.user
        )

        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def patch(self, request, task_id: int):       
        task = Task.objects.get(
            task_id=task_id,
            owner=self.request.user
        )
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"user_{request.user.username}_schedule")
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id: int):
        Task.objects.get(
            task_id=task_id,
            owner=self.request.user
        ).delete()
        
        cache.delete(f"user_{request.user.username}_schedule")
        return Response(status=200)


class TaskListView(APIView):
    def post(self, request):
        form = TaskForm(request.POST)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.status = "PENDING"
            obj.created_on = datetime.today()
            
            obj.save()
            
            for tag in request.POST.getlist("tags"):
                obj.tags.add(tag)

            cache.delete(f"user_{request.user.username}_schedule")

        else:
            print("invalid")
            print(form.errors)
            
        return Response(status=200)
