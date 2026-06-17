from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # anyone can register

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def get_queryset(self):
        # ownership rule — users only see their own tasks
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # automatically set owner to current user on create
        serializer.save(owner=self.request.user)