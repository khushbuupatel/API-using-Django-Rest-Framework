from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
)

from .models import *
from .serializers import UserSerializer, GroupSerializer, ItemListSerializer, ExampleModelLessSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()
    return Response(status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def check_auth(request):
    return Response(status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class ItemListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """
    queryset = ItemList.objects.all().order_by('id')
    serializer_class = ItemListSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExampleModelLessView(viewsets.ViewSet):
    """
    A model-less API example
    A model-less API can be used when saving to a database is not necessary or data need additional processing
    """

    serializer_class = ExampleModelLessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        data = {
            'project_name': 'DataDisca Django Example',
            'total_head_count': 10,
            'start_date': datetime(2020, 5, 27),
            'location': 'Melbourne, Australia'
        }
        my_serializer = ExampleModelLessSerializer(data=data)
        if my_serializer.is_valid():
            return Response(my_serializer.data)
        else:
            return Response({'error': 'invalid data'})

    def create(self, request):
        data = request.data.dict()
        print(data)
        return Response(status=HTTP_201_CREATED)



