from rest_framework import viewsets
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser, Post, Reaction, Comment, ChatRoom, Message
from .serializers import UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer, DepartmentProfileSerializer, LecturerCVSerializer, GustUserSerializer, PostSerializer, ReactionSerializer, CommentSerializer, ChatRoomSerializer, MessageSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from .models import GustUser 
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import tokens

class UniversityProfileViewSet(viewsets.ModelViewSet):
    queryset = UniversityProfile.objects.all()
    serializer_class = UniversityProfileSerializer

class CampusProfileViewSet(viewsets.ModelViewSet):
    queryset = CampusProfile.objects.all()
    serializer_class = CampusProfileSerializer

class CollegeProfileViewSet(viewsets.ModelViewSet):
    queryset = CollegeProfile.objects.all()
    serializer_class = CollegeProfileSerializer

class DepartmentProfileViewSet(viewsets.ModelViewSet):
    queryset = DepartmentProfile.objects.all()
    serializer_class = DepartmentProfileSerializer

class LecturerCVViewSet(viewsets.ModelViewSet):
    queryset = LecturerCV.objects.all()
    serializer_class = LecturerCVSerializer

class GustUserViewSet(viewsets.ModelViewSet):
    queryset = GustUser.objects.all()
    serializer_class = GustUserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except (ObjectDoesNotExist, TokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password)
#     if user:
#         # User authenticated successfully
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     else:
#         # Invalid credentials
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



