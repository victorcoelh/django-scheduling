from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.services.schedule_service import get_schedule_from_cache, schedule_service


class ScheduleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        user: User = request.user # type: ignore
        
        match get_schedule_from_cache(user):
            case None:
                return Response(schedule_service(user))
            case data:
                return Response(data)
