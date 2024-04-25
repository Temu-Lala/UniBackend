from rest_framework import serializers
from .models import UniversityProfile,BasePost, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message, CollegePost, CampusPost, UniversityPost, DepartmentPost
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

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

    def create(self, validated_data):
        return GustUser.objects.create_user(**validated_data)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
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
        fields = '__all__'

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
