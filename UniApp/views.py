import json
from urllib.parse import unquote_plus
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import JWTToken
from UniApp.models import GustUser
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Q
from rest_framework import generics
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes

from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from .models import (
    UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile,
    LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message,
    CollegePost, Notification,LabProfile,CampusPost,CollegeFollow,Follow,BasePost,UniversityRating,CampusRating,DepartmentRating,CollegeRating,LabRating, UniversityPost, DepartmentPost,stortoken,IntegrationRequest,LecturerPost
)
from .serializers import (
    UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer,
    DepartmentProfileSerializer, LecturerCVSerializer, CustomUserSerializer,
    ReactionSerializer, CommentSerializer, ChatRoomSerializer, MessageSerializer,
    CollegePostSerializer, CampusPostSerializer, UniversityPostSerializer,
    DepartmentPostSerializer,NotificationSerializer,LabProfileSerializer,BasePostSerializer,UniversityRatingSerializer,CampusRatingSerializer,CollegeRatingSerializer,DepartmentRatingSerializer,LabRatingSerializer,TokenSerializer,IntegrationRequestSerializer,LecturerPostSerializer
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Permission

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django import forms
# Import user and post models 

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class UniversityProfileViewSet(viewsets.ModelViewSet):
    queryset = UniversityProfile.objects.all()
    serializer_class = UniversityProfileSerializer
class TokenViewSet(viewsets.ModelViewSet):
    queryset = stortoken.objects.all()
    serializer_class = TokenSerializer

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
class LecturerPostViewSet(viewsets.ModelViewSet):
    queryset = LecturerPost.objects.all()
    serializer_class = LecturerPostSerializer
 
class CollegePostViewSet(viewsets.ModelViewSet):
    queryset = CollegePost.objects.all()
    serializer_class = CollegePostSerializer

class CampusPostViewSet(viewsets.ModelViewSet):
    queryset = CampusPost.objects.all()
    serializer_class = CampusPostSerializer

class UniversityPostViewSet(viewsets.ModelViewSet):
    queryset = UniversityPost.objects.all()
    serializer_class = UniversityPostSerializer

class DepartmentPostViewSet(viewsets.ModelViewSet):
    queryset = DepartmentPost.objects.all()
    serializer_class = DepartmentPostSerializer

class GustUserViewSet(viewsets.ModelViewSet):
    queryset = GustUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        user = self.get_object()
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)

class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        sender = request.user
        recipient_id = request.data.get('recipient_id')
        content = request.data.get('content')
        
        if not recipient_id:
            return Response({"recipient_id": ["Recipient ID is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if not content:
            return Response({"content": ["Message content is required."]}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            recipient = GustUser.objects.get(id=recipient_id)
        except GustUser.DoesNotExist:
            return Response({"recipient_id": ["Recipient does not exist."]}, status=status.HTTP_400_BAD_REQUEST)
        
        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=content
        )
        
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @action(detail=False, methods=['get'])
    def user_messages(self, request):
        sender_id = request.query_params.get('sender_id')
        recipient_id = request.query_params.get('recipient_id')
        
        if sender_id and recipient_id:
            messages = Message.objects.filter(
                Q(sender_id=sender_id, recipient_id=recipient_id) | 
                Q(sender_id=recipient_id, recipient_id=sender_id)
            ).order_by('created_at')
            
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Sender ID and Recipient ID are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def contacts_with_chats(self, request):
        user = request.user
        messages = Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).values('sender', 'recipient').distinct()

        contact_ids = set()
        for message in messages:
            if message['sender'] != user.id:
                contact_ids.add(message['sender'])
            if message['recipient'] != user.id:
                contact_ids.add(message['recipient'])

        contacts = GustUser.objects.filter(id__in=contact_ids)
        # contacts_data = [{'id': contact.id, 'username': contact.username, 'avatar': contact.avatar.url if contact.avatar else None} for contact in contacts]
        contacts_data = [
    {
        'id': contact.id,
        'username': contact.username,
        # 'avatar': contact.avatar.url if contact.avatar else None
    }
    for contact in contacts
]
        return Response(contacts_data, status=status.HTTP_200_OK)
        
        

class login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Simple input validation
        if not username or not password:
            return Response({'success': False, 'errors': {'__all__': 'Username and password are required.'}}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'success': False, 'errors': {'__all__': 'Invalid username or password.'}}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        # Save token to database
        jwt_token = JWTToken.objects.create(user=user, token=token)

        # Serialize token data if needed
        serializer = TokenSerializer(jwt_token)

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)
    

class UserProfileAssociation(APIView):
    def get(self, request):
        # Get user based on authentication
        user = request.user

        # Check if the user is associated with a university profile
        try:
            university_profile = UniversityProfile.objects.get(user=user)
            return Response({'success': True, 'profile_type': 'university'}, status=status.HTTP_200_OK)
        except UniversityProfile.DoesNotExist:
            try:
                # Check if the user is associated with a campus profile
                campus_profile = CampusProfile.objects.get(user=user)
                return Response({'success': True, 'profile_type': 'campus'}, status=status.HTTP_200_OK)
            except CampusProfile.DoesNotExist:
                try:
                    # Check if the user is associated with a college profile
                    college_profile = CollegeProfile.objects.get(user=user)
                    return Response({'success': True, 'profile_type': 'college'}, status=status.HTTP_200_OK)
                except CollegeProfile.DoesNotExist:
                    try:
                        # Check if the user is associated with a department profile
                        department_profile = DepartmentProfile.objects.get(user=user)
                        return Response({'success': True, 'profile_type': 'department'}, status=status.HTTP_200_OK)
                    except DepartmentProfile.DoesNotExist:
                        try:
                            # Check if the user is associated with a lecturer CV
                            lecturer_cv = LecturerCV.objects.get(user=user)
                            return Response({'success': True, 'profile_type': 'lecturer'}, status=status.HTTP_200_OK)
                        except LecturerCV.DoesNotExist:
                            return Response({'success': True, 'profile_type': 'default'}, status=status.HTTP_200_OK)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, CollegePost, CampusPost, UniversityPost, DepartmentPost, LecturerPost

@api_view(['GET'])
def get_college_post_comments(request, post_id):
    comments = Comment.objects.filter(content_type__model='collegepost', object_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})

@api_view(['GET'])
def get_campus_post_comments(request, post_id):
    comments = Comment.objects.filter(content_type__model='campuspost', object_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})

@api_view(['GET'])
def get_university_post_comments(request, post_id):
    comments = Comment.objects.filter(content_type__model='universitypost', object_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})

@api_view(['GET'])
def get_department_post_comments(request, post_id):
    comments = Comment.objects.filter(content_type__model='departmentpost', object_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})

@api_view(['GET'])
def get_lecturer_post_comments(request, post_id):
    comments = Comment.objects.filter(content_type__model='lecturerpost', object_id=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response({'comments': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request):
    data = request.data
    post_id = data.get('postId')
    post_type = data.get('postType')
    comment_text = data.get('commentText')

    if not all([post_id, post_type, comment_text]):
        return Response({'error': 'Missing required data (postId, postType, commentText)'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve user from JWT token
        user = request.user

        # Determine the type of post and retrieve it
        post_model = None
        if post_type == 'college':
            post_model = CollegePost
        elif post_type == 'campus':
            post_model = CampusPost
        elif post_type == 'university':
            post_model = UniversityPost
        elif post_type == 'department':
            post_model = DepartmentPost
        elif post_type == 'lecturer':
            post_model = LecturerPost

        if post_model is None:
            return Response({'error': 'Invalid post type'}, status=status.HTTP_400_BAD_REQUEST)

        post = post_model.objects.get(pk=post_id)

        # Create the comment for the post
        comment = Comment.objects.create(
            content_object=post,
            author=user,
            body=comment_text
        )

        # Return the username of the comment author along with other comment details
        return Response({
            'id': comment.id,
            'body': comment.body,
            'author': user.username,
            'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
        }, status=status.HTTP_201_CREATED)

    except post_model.DoesNotExist:
        return Response({'error': f'{post_type.capitalize()} post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request):
    postId = request.data.get('postId')
    postType = request.data.get('postType')

    # Determine the model based on postType
    post_model = None
    if postType == 'college':
        post_model = CollegePost
    elif postType == 'campus':
        post_model = CampusPost
    elif postType == 'university':
        post_model = UniversityPost
    elif postType == 'department':
        post_model = DepartmentPost
    elif postType == 'lecturer':
        post_model = LecturerPost
    else:
        return Response({'error': 'Invalid post type'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post = post_model.objects.get(id=postId)
        # Increment the likes count
        post.likes += 1
        post.save()
        return Response({'message': 'Post liked successfully'}, status=status.HTTP_200_OK)
    except post_model.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_post(request):
    postId = request.data.get('postId')
    postType = request.data.get('postType')

    # Determine the model based on postType
    post_model = None
    if postType == 'college':
        post_model = CollegePost
    elif postType == 'campus':
        post_model = CampusPost
    elif postType == 'university':
        post_model = UniversityPost
    elif postType == 'department':
        post_model = DepartmentPost
    elif postType == 'lecturer':
        post_model = LecturerPost
    else:
        return Response({'error': 'Invalid post type'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post = post_model.objects.get(id=postId)
        # Increment the dislikes count
        post.dislikes += 1
        post.save()
        return Response({'message': 'Post disliked successfully'}, status=status.HTTP_200_OK)
    except post_model.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    if request.method == 'GET':
        try:
            # Retrieve the comment object to be edited
            comment = get_object_or_404(Comment, pk=comment_id)

            # Check if the user owns the comment
            if comment.author != request.user:
                return Response({'error': 'Unauthorized to view this comment'}, status=status.HTTP_403_FORBIDDEN)

            # Return the details of the comment
            return Response({
                'id': comment.id,
                'body': comment.body,
                'author': comment.author.username,
                'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        data = request.data
        comment_text = data.get('commentText')

        try:
            # Retrieve the comment object to be edited
            comment = get_object_or_404(Comment, pk=comment_id)

            # Check if the user owns the comment
            if comment.author != request.user:
                return Response({'error': 'Unauthorized to edit this comment'}, status=status.HTTP_403_FORBIDDEN)

            # Update the comment if commentText is provided
            if comment_text:
                comment.body = comment_text
                comment.save()

            # Return the details of the edited comment
            return Response({
                'id': comment.id,
                'body': comment.body,
                'author': comment.author.username,
                'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_post_object(post_type, post_id):
    """Helper function to fetch the post object based on the post type."""
    if post_type == 'college':
        return CollegePost.objects.get(id=post_id)
    elif post_type == 'campus':
        return CampusPost.objects.get(id=post_id)
    elif post_type == 'university':
        return UniversityPost.objects.get(id=post_id)
    elif post_type == 'department':
        return DepartmentPost.objects.get(id=post_id)
    elif post_type == 'lecturer':
        return LecturerPost.objects.get(id=post_id)
    else:
        raise ValueError("Invalid post type")


def share_post(request, post_type, post_id):
    try:
        post_model = {
            'college': CollegePost,
            'campus': CampusPost,
            'university': UniversityPost,
            'department': DepartmentPost,
            'lecturer': LecturerPost,
        }.get(post_type)

        if not post_model:
            return JsonResponse({'error': 'Invalid post type'}, status=400)

        post = get_object_or_404(post_model, id=post_id)
        share_link = request.build_absolute_uri(f'/share/{post_type}/{post_id}/')

        post.shares += 1
        post.save()

        return JsonResponse({'shareLink': share_link}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
@api_view(["POST"])
def copy_link(request):
    try:
        data = request.data
        share_link = data.get('shareLink')

        # Perform any additional validation or processing if needed

        # Return the shareable link for copying
        return JsonResponse({'shareLink': share_link}, status=200)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)
    
    
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    User = get_user_model()

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({'errors': {'username': 'Username already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists
    if User.objects.filter(email=email).exists():
        return Response({'errors': {'email': 'Email already exists.'}}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Assign the user to the selected group if group_id is provided in the request data
        group_id = request.data.get('group_id')
        if group_id:
            group = Group.objects.filter(id=group_id).first()
            if group:
                user.groups.add(group)
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        # Retrieve the authenticated user
        user = request.user
        
        # Extract data from the request
        data = request.data
        
        # Add the user ID to the data
        data['user'] = user.id
        
        # Serialize the data
        serializer = UniversityProfileSerializer(data=data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the serializer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def TestView(request):
    return Response({"message": "Test view page fgjhkjljboiughj"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Retrieve the user's JWT token
        jwt_token = JWTToken.objects.get(user=request.user)

        # Delete the JWT token
        jwt_token.delete()

        return Response({"message": "Logout successful."})
    except JWTToken.DoesNotExist:
        # JWT token does not exist, possibly user is already logged out
        return Response({"message": "User is already logged out."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Return the exception message
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
def group_list(request):
    groups = Group.objects.all()
    data = [{'id': group.id, 'name': group.name} for group in groups]
    return JsonResponse(data, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_user_into_group(request):
    if request.method == 'POST':
        group_name = request.data.get('group')  # Assuming you're sending data as JSON
        try:
            group = Group.objects.get(name=group_name)
            user = request.user  # Assuming you're using JWT authentication or similar
            user.groups.add(group)
            return Response({'message': f'User registered to {group_name} successfully'}, status=200)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)
    else:
        return Response({'error': 'Invalid request method'}, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def department_profiles_create(request):
    try:
        user = request.user
        university_id = request.data.get('university_id')
        campus_id = request.data.get('campus_profile_id')
        college_id = request.data.get('college_profile_id')
        
        # Check if the university, campus, and college exist
        university = UniversityProfile.objects.get(pk=university_id)
        campus = CampusProfile.objects.get(pk=campus_id)
        college = CollegeProfile.objects.get(pk=college_id)

        # Add the user ID, university ID, campus ID, and college ID to the department data
        department_data = request.data.copy()
        department_data['user'] = user.id
        department_data['university'] = university_id
        department_data['campus'] = campus_id
        department_data['college'] = college_id
        
        serializer = DepartmentProfileSerializer(data=department_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UniversityProfile.DoesNotExist:
        return Response({'error': 'University not found'}, status=status.HTTP_404_NOT_FOUND)
    except CampusProfile.DoesNotExist:
        return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)
    except CollegeProfile.DoesNotExist:
        return Response({'error': 'College not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import get_object_or_404


@api_view(['POST',"GET"])
@permission_classes([IsAuthenticated])
def campus_profiles_create(request):
    try:
        # Extract user and university profile ID from request data
        user = request.user
        university_profile_id = request.data.get('university_profile_id')

        # Create campus profile with associated university
        campus_data = request.data.copy()
        campus_data['user'] = user.id
        campus_data['university'] = university_profile_id  # Updated field name
        serializer = CampusProfileSerializer(data=campus_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def fetch_college_profiles(request, campus_profile_id):
    try:
        college_profiles = CollegeProfile.objects.filter(campus_id=campus_profile_id)
        serializer = CollegeProfileSerializer(college_profiles, many=True)
        return Response(serializer.data)
    except CollegeProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def fetch_campus_profiles(request, university_profile_id):
    try:
        campus_profiles = CampusProfile.objects.filter(university_id=university_profile_id)
        serializer = CampusProfileSerializer(campus_profiles, many=True)
        return Response(serializer.data)
    except CampusProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def college_profiles_create(request):
    try:
        user = request.user
        university_id = request.data.get('university_id')
        campus_id = request.data.get('campus_profile_id')
        
        # Check if the university and campus exist
        university = UniversityProfile.objects.get(pk=university_id)
        campus = CampusProfile.objects.get(pk=campus_id)

        # Add the user ID, university ID, and campus ID to the college data
        college_data = request.data.copy()
        college_data['user'] = user.id
        college_data['university'] = university_id
        college_data['campus'] = campus_id
        
        serializer = CollegeProfileSerializer(data=college_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UniversityProfile.DoesNotExist:
        return Response({'error': 'University not found'}, status=status.HTTP_404_NOT_FOUND)
    except CampusProfile.DoesNotExist:
        return Response({'error': 'Campus not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def campus_profiles_for_university(request, university_profile_id):
    try:
        campuses = CampusProfile.objects.filter(university__id=university_profile_id)
        serializer = CampusProfileSerializer(campuses, many=True)
        return Response(serializer.data)
    except CampusProfile.DoesNotExist:
        return Response({"message": "Campuses not found"}, status=404)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def create_lecturer_cv(request):
    try:
        university_id = request.data.get('university_id')
        campus_id = request.data.get('campus_profile_id')
        college_id = request.data.get('college_profile_id')
        department_id = request.data.get('department_profile_id')

        # Check if the associated profiles exist
        # Add more checks if needed
        UniversityProfile.objects.get(pk=university_id)
        CampusProfile.objects.get(pk=campus_id)
        CollegeProfile.objects.get(pk=college_id)
        DepartmentProfile.objects.get(pk=department_id)

        # Fetch the currently logged-in user
        user = request.user
        user_id = user.id  # Get the ID of the currently logged-in user

        # Add the user ID to the form data
        request.data['user'] = user_id
        request.data['university_profile'] = university_id
        request.data['campus_profile'] = campus_id
        request.data['college_profile'] = college_id
        request.data['department_profile'] = department_id

        serializer = LecturerCVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    except UniversityProfile.DoesNotExist:
        return JsonResponse({'error': 'University not found'}, status=404)
    except CampusProfile.DoesNotExist:
        return JsonResponse({'error': 'Campus not found'}, status=404)
    except CollegeProfile.DoesNotExist:
        return JsonResponse({'error': 'College not found'}, status=404)
    except DepartmentProfile.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_lecturer_cvs(request):
    try:
        # Retrieve all LecturerCV instances
        lecturer_cvs = LecturerCV.objects.all()

        # Serialize the data
        serializer = LecturerCVSerializer(lecturer_cvs, many=True)

        return JsonResponse(serializer.data, safe=False)  # safe=False for serializing lists

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['GET'])
def fetch_department_profiles(request, college_profile_id):
    try:
        departments = DepartmentProfile.objects.filter(college_id=college_profile_id)
        serializer = DepartmentProfileSerializer(departments, many=True)
        return Response(serializer.data)
    except DepartmentProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lecturer_cv(request, pk):
    try:
        lecturer_cv = LecturerCV.objects.get(pk=pk)

        # Check if the user has permission to edit this lecturer CV
        if lecturer_cv.user != request.user:
            return JsonResponse({'error': 'You do not have permission to edit this CV'}, status=403)

        # Serialize the existing data
        serializer = LecturerCVSerializer(lecturer_cv, data=request.data, partial=True)  # partial=True for partial updates

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)
    except LecturerCV.DoesNotExist:
        return JsonResponse({'error': 'Lecturer CV not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import LecturerCV
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lecturer_cv(request, pk):
    if request.method == 'DELETE':
        cv = get_object_or_404(LecturerCV, pk=pk)
        # Perform any necessary permission checks here
        cv.delete()
        return JsonResponse({'message': 'Lecturer CV deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def lab_profiles(request, lab_id=None):
    if request.method == 'POST':
        try:
            user = request.user
            university_id = request.data.get('university_id')
            campus_id = request.data.get('campus_profile_id')
            college_id = request.data.get('college_profile_id')
            department_id = request.data.get('department_profile_id')
            
            # Check if the university, campus, college, and department exist
            # You need to import the respective models here
            
            # Add the user ID, university ID, campus ID, college ID, and department ID to the lab data
            lab_data = request.data.copy()
            lab_data['user'] = user.id
            lab_data['university_profile'] = university_id
            lab_data['campus_profile'] = campus_id
            lab_data['college_profile'] = college_id
            lab_data['department_profile'] = department_id
            
            serializer = LabProfileSerializer(data=lab_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'GET':
        try:
            lab = LabProfile.objects.get(pk=lab_id)
            serializer = LabProfileSerializer(lab)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LabProfile.DoesNotExist:
            return Response({'error': 'Lab profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            lab = LabProfile.objects.get(pk=lab_id)
            serializer = LabProfileSerializer(lab, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabProfile.DoesNotExist:
            return Response({'error': 'Lab profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user_id = request.user.id  # Get the user ID from the authenticated request
    try:
        user = GustUser.objects.get(id=user_id)
        if request.method == 'GET':
            profile_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                # Add other fields as needed
            }
            return Response(profile_data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            # Update user profile data
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.email = request.data.get('email', user.email)
            user.username = request.data.get('username', user.username)
            # Add other fields as needed
            user.save()
            return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
    except GustUser.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_integration_request(request):
    try:
        campus_profile = request.user.campus_profile
        data = request.data
        data['campus'] = campus_profile.id
        serializer = IntegrationRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def manage_integration_requests(request):
    if request.method == 'GET':
        # Retrieve pending integration requests for the authenticated user's university
        university_profile = request.user.university_profile
        integration_requests = IntegrationRequest.objects.filter(university=university_profile, status='pending')
        serializer = IntegrationRequestSerializer(integration_requests, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Accept or reject an integration request
        request_id = request.data.get('request_id')
        action = request.data.get('action')  # 'accept' or 'reject'
        try:
            integration_request = IntegrationRequest.objects.get(id=request_id, university=request.user.university_profile)
            if action == 'accept':
                integration_request.status = 'accepted'
                # Perform any additional actions to integrate campus with university
                # For example, update campus profile to set university field
                integration_request.campus.university = integration_request.university
                integration_request.campus.save()
            elif action == 'reject':
                integration_request.status = 'rejected'
            integration_request.save()
            return Response({'message': f'Integration request {action}ed'}, status=200)
        except IntegrationRequest.DoesNotExist:
            return Response({'error': 'Integration request not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user

    # Extract the user ID from the request data
    request_data = request.data.copy()
    request_data['user'] = user.id  # Assign the user ID to the 'user' field

    # Check user association with University
    if UniversityProfile.objects.filter(user=user).exists():
        serializer = UniversityPostSerializer(data=request_data)
        if serializer.is_valid():
            # Save the post with the associated university profile
            university_profile = user.universityprofile_set.first()
            serializer.save(university=university_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check user association with Campus
    elif CampusProfile.objects.filter(user=user).exists():
        serializer = CampusPostSerializer(data=request_data)
        if serializer.is_valid():
            # Save the post with the associated campus profile
            campus_profile = user.campusprofile_set.first()
            serializer.save(campus=campus_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check user association with College
    elif CollegeProfile.objects.filter(user=user).exists():
        serializer = CollegePostSerializer(data=request_data)
        if serializer.is_valid():
            # Save the post with the associated college profile
            college_profile = user.collegeprofile_set.first()
            serializer.save(college=college_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check user association with Department
    elif DepartmentProfile.objects.filter(user=user).exists():
        serializer = DepartmentPostSerializer(data=request_data)
        if serializer.is_valid():
            # Save the post with the associated department profile
            department_profile = user.departmentprofile_set.first()
            serializer.save(department=department_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check user association with Lecturer
    elif LecturerCV.objects.filter(user=user).exists():
        serializer = LecturerPostSerializer(data=request_data)
        if serializer.is_valid():
            # Save the post with the associated lecturer profile
            lecturer_profile = user.lecturercv_set.first()
            serializer.save(lecturer=lecturer_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"error": "User is not associated with any hierarchy."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    user = request.user

    try:
        # Retrieve the post
        post = Post.objects.get(id=post_id)

        # Check if the user is the creator of the post
        if post.user != user:
            return Response({"error": "You don't have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the post
        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def university_profile_list(request):
    """
    List all university profiles or create a new university profile.
    """
    if request.method == 'GET':
        university_profiles = UniversityProfile.objects.all()
        serializer = UniversityProfileSerializer(university_profiles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UniversityProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def university_profile_detail(request, pk):
    """
    Retrieve, update or delete a university profile.
    """
    print('id', id, pk)
    university_profile = get_object_or_404(UniversityProfile, pk=id)
    print(university_profile)

    if request.method == 'GET':
        serializer = UniversityProfileSerializer(university_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UniversityProfileSerializer(university_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        university_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def university_rating(request):
    if request.method == 'POST':
        try:
            user = request.user
            university_id = request.data.get('university_id')
            rating_value = request.data.get('value')
            comment = request.data.get('comment', None)

            rating = UniversityRating.objects.create(
                user=user,
                university_profile_id=university_id,
                value=rating_value,
                comment=comment
            )
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            university_id = request.query_params.get('university_id')
            ratings = UniversityRating.objects.filter(university_profile_id=university_id)
            serializer = UniversityRatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            user = request.user
            comment_id = request.data.get('comment_id')
            new_comment = request.data.get('comment')

            comment = UniversityRating.objects.get(id=comment_id, user=user)
            comment.comment = new_comment
            comment.save()

            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        except UniversityRating.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def campus_rating(request):
    if request.method == 'POST':
        try:
            user = request.user
            campus_id = request.data.get('campus_id')
            rating_value = request.data.get('value')
            comment = request.data.get('comment', None)

            rating = CampusRating.objects.create(
                user=user,
                campus_profile_id=campus_id,
                value=rating_value,
                comment=comment
            )
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            campus_id = request.query_params.get('campus_id')
            ratings = CampusRating.objects.filter(campus_profile_id=campus_id)
            serializer = CampusRatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            user = request.user
            comment_id = request.data.get('comment_id')
            new_comment = request.data.get('comment')

            comment = CampusRating.objects.get(id=comment_id, user=user)
            comment.comment = new_comment
            comment.save()

            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        except CampusRating.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def college_rating(request):
    if request.method == 'POST':
        try:
            user = request.user
            college_id = request.data.get('college_id')
            rating_value = request.data.get('value')
            comment = request.data.get('comment', None)

            rating = CollegeRating.objects.create(
                user=user,
                college_profile_id=college_id,
                value=rating_value,
                comment=comment
            )
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            college_id = request.query_params.get('college_id')
            ratings = CollegeRating.objects.filter(college_profile_id=college_id)
            serializer = CollegeRatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            user = request.user
            comment_id = request.data.get('comment_id')
            new_comment = request.data.get('comment')

            comment = CollegeRating.objects.get(id=comment_id, user=user)
            comment.comment = new_comment
            comment.save()

            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        except CollegeRating.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def department_rating(request):
    if request.method == 'POST':
        try:
            user = request.user
            department_id = request.data.get('department_id')
            rating_value = request.data.get('value')
            comment = request.data.get('comment', None)

            rating = DepartmentRating.objects.create(
                user=user,
                department_profile_id=department_id,
                value=rating_value,
                comment=comment
            )
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'GET':
        try:
            department_id = request.query_params.get('department_id')
            ratings = DepartmentRating.objects.filter(department_profile_id=department_id)
            serializer = DepartmentRatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        try:
            user = request.user
            comment_id = request.data.get('comment_id')
            new_comment = request.data.get('comment')

            comment = DepartmentRating.objects.get(id=comment_id, user=user)
            comment.comment = new_comment
            comment.save()

            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        except DepartmentRating.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def lab_rating(request):
    if request.method == 'POST':
        try:
            user = request.user
            university_id = request.data.get('university_id')
            rating_value = request.data.get('value')
            comment = request.data.get('comment', None)

            rating = LabRating.objects.create(
                user=user,
                university_profile_id=university_id,
                value=rating_value,
                comment=comment
            )
            return Response({'message': 'Rating added successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'GET':
        try:
            university_id = request.query_params.get('university_id')
            ratings = LabRating.objects.filter(university_profile_id=university_id)
            serializer = LabRatingSerializer(ratings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            user = request.user
            comment_id = request.data.get('comment_id')
            new_comment = request.data.get('comment')

            comment = LabRating.objects.get(id=comment_id, user=user)
            comment.comment = new_comment
            comment.save()

            return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
        except LabRating.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    

@api_view(['POST'])
def follow_college(request, college_id):
    try:
        college = CollegeProfile.objects.get(pk=college_id)
        follow = CollegeFollow(user=request.user, college=college)
        follow.save()
        return Response({'message': 'Followed college successfully'}, status=status.HTTP_201_CREATED)
    except CollegeProfile.DoesNotExist:
        return Response({'error': 'College not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unfollow_college(request, college_id):
    try:
        college = CollegeProfile.objects.get(pk=college_id)
        follow = CollegeFollow.objects.get(user=request.user, college=college)
        follow.delete()
        return Response({'message': 'Unfollowed college successfully'})
    except CollegeProfile.DoesNotExist:
        return Response({'error': 'College not found'}, status=status.HTTP_404_NOT_FOUND)
    except CollegeFollow.DoesNotExist:
        return Response({'error': 'You are not following this college'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_follow_status(request, college_id):
    try:
        college = CollegeProfile.objects.get(pk=college_id)
        is_following = CollegeFollow.objects.filter(user=request.user, college=college).exists()
        return Response({'is_following': is_following})
    except CollegeProfile.DoesNotExist:
        return Response({'error': 'College not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    

@csrf_exempt
def password_reset_request(request):
    if request.method == "POST":
        try:
            data = request.body.decode('utf-8')
            print('Request body:', data)  # Debugging log
            data = json.loads(data)
            email = data.get('email', '')
            print('Received email:', email)  # Debugging log

            if email:
                associated_users = get_user_model().objects.filter(email=email)
                if associated_users.exists():
                    for user in associated_users:
                        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                        token = default_token_generator.make_token(user)
                        uidb64_param = urlsafe_base64_encode(force_bytes(user.pk))
                        token_param = default_token_generator.make_token(user)
                        reset_link = f"http://localhost:3000/password/new_password?uidb64={uidb64_param}&token={token_param}"
                        subject = "Password Reset Requested"
                        message = (
                            f"Dear {user.username},\n\n"
                            "You have requested to reset your password. Please follow this link to reset your password: "
                            f"http://localhost:3000/password/new_password?uidb64={uidb64_param}&token={token_param}" 
                            "\n If you didn't request this, please ignore this email.\n\n"
                            "Best regards,\n UniConnect Team"
                        )
                        print(f'Attempting to send email to {user.email}')  # Debugging log
                        try:
                            send_mail(
                                subject,
                                message,
                                settings.DEFAULT_FROM_EMAIL,
                                [user.email],  # Use the user's email from the database
                                fail_silently=False,
                            )
                            print(f'Email successfully sent to {user.email}')  # Debugging log
                        except Exception as e:
                            print(f'Error sending email to {user.email}: {e}')  # Debugging log
                            return JsonResponse({'error': f'Error sending email to {user.email}: {e}'}, status=500)
                    return JsonResponse({'message': 'Password reset link has been sent to your email.'})
                else:
                    print('No associated users found.')  # Debugging log
                    return JsonResponse({'error': 'No user is associated with this email address.'}, status=404)
            else:
                print('Email address is required.')  # Debugging log
                return JsonResponse({'error': 'Email address is required.'}, status=400)
        except Exception as e:
            print('Error:', e)  # Debugging log
            return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)
    else:
        print('Invalid request method.')  # Debugging log
        return JsonResponse({'error': 'Invalid request method.'}, status=400)



@csrf_exempt
def update_password(request, uidb64, token):
    if request.method == "POST":
        try:
            uidb64 = unquote_plus(uidb64)
            token = unquote_plus(token)

            try:
                data = request.body.decode('utf-8')
            except UnicodeDecodeError as e:
                print('Decoding error:', e)  # Debugging log
                return JsonResponse({'error': 'Invalid encoding in request body.'}, status=400)

            print('Request body:', data)  # Debugging log
            data = json.loads(data)
            new_password = data.get('password', '')
            print('Received password:', new_password)

            if new_password:
                try:
                    uid = urlsafe_base64_decode(uidb64).decode()
                    print(f'Decoded UID: {uid}')  # Debugging log
                    user = get_user_model().objects.get(pk=uid)
                    if default_token_generator.check_token(user, token):
                        user.set_password(new_password)
                        user.save()
                        return JsonResponse({'message': 'Password has been reset successfully.'})
                    else:
                        print('Invalid token.')  # Debugging log
                        return JsonResponse({'error': 'Invalid or expired token.'}, status=400)
                except (ValueError, OverflowError, get_user_model().DoesNotExist) as e:
                    print('Error:', e)  # Console log any errors
                    return JsonResponse({'error': 'Invalid user ID or token.'}, status=400)
            else:
                print('Password is required.')  # Console log if password is not provided
                return JsonResponse({'error': 'Password is required.'}, status=400)
        except Exception as e:
            print('Error:', e)  # Console log if an error occurs
            return JsonResponse({'error': 'An error occurred while processing the request.'}, status=500)
    else:
        print('Invalid request method.')  # Console log if request method is not POST
        return JsonResponse({'error': 'Invalid request method.'}, status=400)