from django.contrib.auth import login
from knox.views import LoginView as KnoxView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import User
from .permissions import IsAdminOrIsSelf
from .serializers import AdminSerializer, UserSerializer


class LoginView(KnoxView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['retrieve', 'partial_update', 'update']:
            return [IsAuthenticated(), IsAdminOrIsSelf()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action in ['list']:
            return AdminSerializer
        return UserSerializer
