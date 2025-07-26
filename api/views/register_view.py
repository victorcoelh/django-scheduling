from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from api.serializers import RegisterSerializer, UserSerializer
from api.tasks import send_welcome_email


#TODO: Fix typing issues
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            send_welcome_email.delay(user.email)
            
            tokens = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(tokens),
                "access": str(tokens.access_token)
            }
            
            return Response({
                "token": tokens,
                "user": UserSerializer(user).data,
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
