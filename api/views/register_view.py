from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.serializers import RegisterSerializer
from api.services.register_service import register_service


#TODO: Casos de erro: usuário já existe, senha fraca pros padrões do Django, e-mail não existe
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
    
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        jwt_tokens = register_service(serializer.save()) # pyright: ignore[reportArgumentType]
        return Response(jwt_tokens, status=status.HTTP_201_CREATED)
