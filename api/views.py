from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status, generics
from django.contrib.auth.models import User

from api.forms import TaskForm
from api.models import Task
from api.serializers import RegisterSerializer, TaskSerializer


class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
    
    
class ScheduleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        tasks = Task.objects\
            .filter(owner=self.request.user)\
            .order_by("date")

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id: int):
        Task.objects.get(
            task_id=task_id,
            owner=self.request.user
        ).delete()

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
        else:
            print("invalid")
            print(form.errors)
            
        return Response(status=200)
