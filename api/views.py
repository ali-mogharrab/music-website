from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer


class Logout(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        request.user.auth_token.delete()
        return Response(data={'message': 'User loged out successfully'})


class Users(APIView):

    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(instance=users, many=True)
        return Response(data=user_serializer.data)

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            message = {
                'message': 'User created successfully',
                'id': user.id,
                # send PUT request because profile has been created by profiles/signals.py
                'send PUT request to update profile': request.META['HTTP_HOST'] + '/api/profile/',
            }
            return Response(data=message, status=status.HTTP_201_CREATED)

        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    def get_user(self, pk):
        try:
            user = User.objects.get(id=pk)
            return user
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)
        user_serializer = UserSerializer(instance=user)
        return Response(data=user_serializer.data)

    def put(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(data=user_serializer.data)

        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(data={'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
