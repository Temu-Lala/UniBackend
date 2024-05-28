from rest_framework import serializers
from .models import UniversityProfile,UniversityRating,LabProfile,Follow,CampusRating,CollegeRating,DepartmentRating,LabRating,Notification,BasePost,stortoken,IntegrationRequest, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message, CollegePost, CampusPost, UniversityPost, DepartmentPost,LecturerPost
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import JWTToken

class UniversityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityProfile
        fields = '__all__'
class CampusProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusProfile
        fields = '__all__'

class UniversityRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityRating
        fields = ['id', 'user', 'university_profile', 'value', 'comment']  # Include 'comment' field in the serializer
class CampusRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusRating
        fields = ['id', 'user', 'campus_profile', 'value', 'comment']  # Include 'comment' field in the serializer

class CollegeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeRating
        fields = ['id', 'user', 'college_profile', 'value', 'comment']  # Include 'comment' field in the serializer

class DepartmentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentRating
        fields = ['id', 'user', 'department_profile', 'value', 'comment']  # Include 'comment' field in the serializer

class LabRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRating
        fields = ['id', 'user', 'labprofile_profile', 'value', 'comment']  # Include 'comment' field in the serializer



class CollegeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeProfile
        fields = '__all__'
class DepartmentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentProfile
        fields = '__all__'
class LabProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabProfile
        fields = '__all__'

class LecturerCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerCV
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should be write-only

    class Meta:
        model = GustUser
        fields = ['id', 'username', 'email', 'password']  # Add other fields as needed
        read_only_fields = ['id']  # ID field should be read-only

    def create(self, validated_data):
        user = GustUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            gender=validated_data.get('gender', ''),
            age=validated_data.get('age', None)
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
    
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
class CollegeFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GustUser
        fields = ['id', 'username', 'avatar']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'created_at']
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
class LecturerPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = LecturerPost
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
        
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
        
    
# serializers.py

from rest_framework import serializers
from .models import LabProfile, LabFile

class LabFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabFile
        fields = '__all__'

class LabProfileSerializer(serializers.ModelSerializer):
    files = LabFileSerializer(many=True, read_only=True)
    file_uploads = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = LabProfile
        fields = ['id', 'name', 'description', 'user', 'university_profile', 'campus_profile', 'college_profile', 'department_profile', 'files', 'file_uploads']

    def create(self, validated_data):
        files_data = validated_data.pop('file_uploads')
        lab_profile = LabProfile.objects.create(**validated_data)
        for file_data in files_data:
            file_type = 'photo' if file_data.content_type.startswith('image') else 'video' if file_data.content_type.startswith('video') else 'document'
            lab_file = LabFile.objects.create(file=file_data, file_type=file_type, lab_profile=lab_profile)
        return lab_profile

    def update(self, instance, validated_data):
        files_data = validated_data.pop('file_uploads', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.university_profile = validated_data.get('university_profile', instance.university_profile)
        instance.campus_profile = validated_data.get('campus_profile', instance.campus_profile)
        instance.college_profile = validated_data.get('college_profile', instance.college_profile)
        instance.department_profile = validated_data.get('department_profile', instance.department_profile)
        instance.save()

        if files_data:
            for file_data in files_data:
                file_type = 'photo' if file_data.content_type.startswith('image') else 'video' if file_data.content_type.startswith('video') else 'document'
                LabFile.objects.create(file=file_data, file_type=file_type, lab_profile=instance)
        return instance