from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.generics import UpdateAPIView
from app_user.serializers import PasswordSerializer
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK
)


class ChangePassword(UpdateAPIView):
    """
    Model based api view that allows the user to change the password
    """
    queryset = User.objects.all()
    serializer_class = PasswordSerializer

    def update(self, request):
        """
        This method respond to PUT/PATCH requests from the user to change their account password
        :param request:
        :return:
        """

        # serialize the request data passed
        user_details = self.get_serializer(data=request.data)

        # return response 400 if the data is not valid (i.e. if any of them are empty)
        if not user_details.is_valid():
            return Response({'error': 'Please provide username, password and New password'},
                            status=HTTP_400_BAD_REQUEST)

        # get the user credentials from the validated data
        username = user_details.validated_data.get("username")
        password = user_details.validated_data.get("password")
        new_password = user_details.validated_data.get("new_password")

        # authenticate the user with the entered details
        user = authenticate(username=username, password=password)

        # check if the username and current password are correct else return 400
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_400_BAD_REQUEST)

        # return http 400 if both old and new passwords are same
        if password == new_password:
            return Response({'error': 'New password cannot be same as old password'},
                            status=HTTP_400_BAD_REQUEST)

        # if the username are current password are correct then change password
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()

        # return success message
        return Response({'success': 'Password changed!'},
                        status=HTTP_200_OK)
