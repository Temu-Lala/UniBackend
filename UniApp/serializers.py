from rest_framework import serializers
from .models import UniversityProfile,BasePost,stortoken,IntegrationRequest, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message, CollegePost, CampusPost, UniversityPost, DepartmentPost
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import JWTToken

class UniversityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}} 

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

class LecturerCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerCV
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only

    class Meta:
        model = GustUser
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'gender', 'age']  # Add other fields as needed
        read_only_fields = ['id']  # ID field should be read-only

class JWTTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = JWTToken
        fields = ('id', 'user', 'token', 'created_at')
        read_only_fields = ('id', 'created_at')

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = stortoken
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'recipient', 'created_at']

class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePost
        fields = '__all__'

class CollegePostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = CollegePost

class CampusPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = CampusPost

class UniversityPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = UniversityPost

class DepartmentPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = DepartmentPost
class IntegrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationRequest
        fields = '__all__'