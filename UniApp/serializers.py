# serializers.py

from rest_framework import serializers
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, UserProfile, Chat, Message, MessageReaction, LecturerCV, News, MediaItem, MediaItemComment, MediaItemLike, MediaItemDislike

class UniversityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityProfile
        fields = '__all__'

class CampusProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusProfile
        fields = '__all__'

class CollegeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeProfile
        fields = '__all__'

class DepartmentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentProfile
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MessageReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageReaction
        fields = '__all__'

class LecturerCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerCV
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = '__all__'

class MediaItemCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItemComment
        fields = '__all__'

class MediaItemLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItemLike
        fields = '__all__'

class MediaItemDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItemDislike
        fields = '__all__'
