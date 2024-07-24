from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, Task
from .permissions import IsClient, IsEmployee, IsManager 
import jwt, datetime
from .serializers import UserSerializer, LoginSerializer, TaskSerializer

class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            payload = {
                'id': user.id,
                'role': user.role,
                # for expiration of token
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
                # date at which this token is created
                'iat': datetime.datetime.now(datetime.timezone.utc) 
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def logout(self, request):
        # In token-based authentication, logout is typically handled client-side
        # by removing the token. Here we'll just return a success message.
        return Response({"message": "Successfully logged out."})
    
    @action(detail=False, methods=['get'])
    def user(self, request):
        # This action can be used to get the current user's details
        # You'll need to implement authentication to use this
        user = request.user
        return Response(UserSerializer(user).data)
    
class TaskViewSet(viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['post'], permission_classes = [IsAuthenticated, IsClient])
    def create_task(self,request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], permission_classes = [IsAuthenticated, IsManager])
    def edit_task(self, request, pk = None):
        task = self.get_object()
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], permission_classes = [IsAuthenticated, IsManager])
    def delete_task(self, request, pk=None):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['patch'], permission_classes = [IsAuthenticated, IsManager])
    def assign_task(self, request, pk=None):
        task = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        try:
            assigned_to = User.objects.get(id=assigned_to_id)
            task_assigned_to = assigned_to
            task.save()
            return Response(TaskSerializer(task).data)
        except User.DoesNotExist:
            return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['patch'], permission_classes = [IsAuthenticated, IsEmployee])
    def complete_task(self, request, pk=None):
        task = self.get_object()
        if task.assigned_to == request.user:
            task_completed = True
            task.save()
            return Response(TaskSerializer(task).data)
        return Response({'error': 'You are not assigned this task'}, status=status.HTTP_403_FORBIDDEN)



        
