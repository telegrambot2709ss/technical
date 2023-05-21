from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _

from apps.api.v1.auth import serializers


# Task 1 and 5
class LoginView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserRegisterView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'token': user.token,
        }, status=status.HTTP_201_CREATED)


class LogoutView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({'error': _("refresh token is required")}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            OutstandingToken.objects.filter(user=request.user).delete()
            return Response({"detail": _("User has been logged out.")}, status=status.HTTP_204_NO_CONTENT)
        except TokenError as e:
            return Response(
                {"error": _(f"Invalid token or token has already expired. {e}")},
                status=status.HTTP_400_BAD_REQUEST
            )
