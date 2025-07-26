from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache

from api.models import Task
from api.serializers import TaskSerializer


class ScheduleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user.username
        cache_key = f"user_{user}_schedule"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            print("Retrieved from Cache")
            return Response(cached_data)
        
        tasks = Task.objects\
            .filter(owner=self.request.user)\
            .order_by("date")
        tasks = TaskSerializer(tasks, many=True).data

        cache.set(cache_key, tasks, 600)
        return Response(tasks)
