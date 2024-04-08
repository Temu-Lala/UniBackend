# views.py

from rest_framework import viewsets
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, UserProfile, Chat, Message, MessageReaction, LecturerCV, News, MediaItem, MediaItemComment, MediaItemLike, MediaItemDislike
from .serializers import UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer, DepartmentProfileSerializer, UserProfileSerializer, ChatSerializer, MessageSerializer, MessageReactionSerializer, LecturerCVSerializer, NewsSerializer, MediaItemSerializer, MediaItemCommentSerializer, MediaItemLikeSerializer, MediaItemDislikeSerializer

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

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageReactionViewSet(viewsets.ModelViewSet):
    queryset = MessageReaction.objects.all()
    serializer_class = MessageReactionSerializer

class LecturerCVViewSet(viewsets.ModelViewSet):
    queryset = LecturerCV.objects.all()
    serializer_class = LecturerCVSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer

class MediaItemCommentViewSet(viewsets.ModelViewSet):
    queryset = MediaItemComment.objects.all()
    serializer_class = MediaItemCommentSerializer

class MediaItemLikeViewSet(viewsets.ModelViewSet):
    queryset = MediaItemLike.objects.all()
    serializer_class = MediaItemLikeSerializer

class MediaItemDislikeViewSet(viewsets.ModelViewSet):
    queryset = MediaItemDislike.objects.all()
    serializer_class = MediaItemDislikeSerializer
