from rest_framework import viewsets
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from .models import (
    UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile,
    LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message,
    CollegePost, CampusPost, UniversityPost, DepartmentPost
)
from .serializers import (
    UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer,
    DepartmentProfileSerializer, LecturerCVSerializer, CustomUserSerializer,
    ReactionSerializer, CommentSerializer, ChatRoomSerializer, MessageSerializer,
    CollegePostSerializer, CampusPostSerializer, UniversityPostSerializer,
    DepartmentPostSerializer
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication

# Import your user and post models (replace with your actual models)
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

    @action(detail=True, methods=['get'])
    def get_messages_by_room(self, request, pk=None):
        room = self.get_object()
        messages = room.message_set.all()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_message_to_room(self, request, pk=None):
        room = self.get_object()
        data = request.data
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(room=room, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request):
    """
    API endpoint to add comments to posts.

    Expects a POST request with the following JSON data in the request body:
        - postId: ID of the post to comment on
        - postType: Type of the post (e.g., 'college', 'campus')
        - commentText: Text of the comment

    Returns a JSON response with details of the created comment on success,
    or an error message with status code on failure.
    """
    data = request.data
    post_id = data.get('postId')
    post_type = data.get('postType')
    comment_text = data.get('commentText')

    if not all([post_id, post_type, comment_text]):
        return JsonResponse({'error': 'Missing required data (postId, postType, commentText)'}, status=400)

    # Assuming you have a custom token field in your User model
    token = request.headers.get('Authorization', '').split()[1]  # Extract the token

    try:
        user = GustUser.objects.get(auth_token=token)
    except GustUser.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    try:
        # Determine the type of post and retrieve it
        post_model = None
        if post_type == 'college':
            from .models import CollegePost
            post_model = CollegePost
        elif post_type == 'campus':
            from .models import CampusPost
            post_model = CampusPost
        elif post_type == 'university':
            from .models import UniversityPost
            post_model = UniversityPost
        elif post_type == 'department':
            from .models import DepartmentPost
            post_model = DepartmentPost

        if post_model is None:
            return JsonResponse({'error': 'Invalid post type'}, status=400)

        post = post_model.objects.get(pk=post_id)

        # Create the comment for the post
        comment = Comment.objects.create(post=post, author=user, body=comment_text)

        # Return the username of the comment author along with other comment details
        return JsonResponse({
            'id': comment.id,
            'body': comment.body,
            'author': user.username,  # Return username instead of user object
            'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
        })
    except post_model.DoesNotExist:
        return JsonResponse({'error': f'{post_type.capitalize()} post not found'}, status=404)
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
        return JsonResponse({'error': 'Internal server error'}, status=500)

   
# @api_view(['GET'])
# def get_comments(request):
#     """
#     API endpoint to fetch comments for a specific post.

#     Expects a GET request with the following query parameters:
#         - postId: ID of the post to fetch comments for
#         - postType: Type of the post (e.g., 'college', 'campus', 'university', 'department')

#     Returns a JSON response with comments associated with the specified post.
#     """
#     post_id = request.query_params.get('postId')
#     post_type = request.query_params.get('postType')

#     if not all([post_id, post_type]):
#         return Response({'error': 'Missing required query parameters (postId, postType)'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Retrieve comments associated with the specified post
#         comments = Comment.objects.filter(post_id=post_id, post_type=post_type)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     except Comment.DoesNotExist:
#         return Response({'error': 'Comments not found for the specified post'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         print(f"An error occurred: {e}")  # Log the error for debugging
#         return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login(request):
    data = request.data
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    authenticate_user = authenticate(username=username, password=password)

    if authenticate_user is not None:
        user = GustUser.objects.get(username=username)
        serializer = CustomUserSerializer(user)

        token, created_token = Token.objects.get_or_create(user=user)

        response_data = {
            'user': serializer.data,
            'token': token.key if token else created_token.key
        }

        return Response(response_data)
    else:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def TestView(request):
    return Response({"message": "Test view page fgjhkjljboiughj"})

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "logout was successful"})

def group_list(request):
    groups = Group.objects.all()
    data = [{'id': group.id, 'name': group.name} for group in groups]
    return JsonResponse(data, safe=False)

def user_profile(request):
    # Extract the token from the request headers
    token_key = request.headers.get('Authorization').split()[1]
    
    # Retrieve the token object based on the token key
    token = Token.objects.get(key=token_key)
    
    # Retrieve the user associated with the token
    user = token.user
    
    # Serialize the user profile
    serializer = CustomUserSerializer(user)
    
    # Return the serialized user profile in JSON format
    return JsonResponse(serializer.data)
