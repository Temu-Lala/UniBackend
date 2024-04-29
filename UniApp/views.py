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

from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from .models import (
    UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile,
    LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message,
    CollegePost, CampusPost, UniversityPost, DepartmentPost,stortoken
)
from .serializers import (
    UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer,
    DepartmentProfileSerializer, LecturerCVSerializer, CustomUserSerializer,
    ReactionSerializer, CommentSerializer, ChatRoomSerializer, MessageSerializer,
    CollegePostSerializer, CampusPostSerializer, UniversityPostSerializer,
    DepartmentPostSerializer,TokenSerializer
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
# Import your user and post models (replace with your actual models)
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
        
        
        
class login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Simple input validation
        if not username or not password:
            return Response({'success': False, 'errors': {'__all__': 'Username and password are required.'}}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = GustUser.objects.filter(username=username, password=password).first()
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
# @api_view(['POST'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def add_comment(request):
#     """
#     API endpoint to add comments to posts.

#     Expects a POST request with the following JSON data in the request body:
#         - postId: ID of the post to comment on
#         - postType: Type of the post (e.g., 'college', 'campus')
#         - commentText: Text of the comment

#     Returns a JSON response with details of the created comment on success,
#     or an error message with status code on failure.
#     """
#     data = request.data
#     post_id = data.get('postId')
#     post_type = data.get('postType')
#     comment_text = data.get('commentText')

#     if not all([post_id, post_type, comment_text]):
#         return JsonResponse({'error': 'Missing required data (postId, postType, commentText)'}, status=400)

#     # Assuming you have a custom token field in your User model
#     token = request.headers.get('Authorization', '').split()[1]  # Extract the token

#     try:
#         user = GustUser.objects.get(auth_token=token)
#     except GustUser.DoesNotExist:
#         return JsonResponse({'error': 'Invalid token'}, status=401)

#     try:
#         # Determine the type of post and retrieve it
#         post_model = None
#         if post_type == 'college':
#             from .models import CollegePost
#             post_model = CollegePost
#         elif post_type == 'campus':
#             from .models import CampusPost
#             post_model = CampusPost
#         elif post_type == 'university':
#             from .models import UniversityPost
#             post_model = UniversityPost
#         elif post_type == 'department':
#             from .models import DepartmentPost
#             post_model = DepartmentPost

#         if post_model is None:
#             return JsonResponse({'error': 'Invalid post type'}, status=400)

#         post = post_model.objects.get(pk=post_id)

#         # Create the comment for the post
#         comment = Comment.objects.create(post=post, author=user, body=comment_text)

#         # Return the username of the comment author along with other comment details
#         return JsonResponse({
#             'id': comment.id,
#             'body': comment.body,
#             'author': user.username,  # Return username instead of user object
#             'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
#         })
#     except post_model.DoesNotExist:
#         return JsonResponse({'error': f'{post_type.capitalize()} post not found'}, status=404)
#     except Exception as e:
#         print(f"An error occurred: {e}")  # Log the error for debugging
#         return JsonResponse({'error': 'Internal server error'}, status=500)

   
   
   
   
   
@api_view(['POST'])
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
    user_id = request.user.id  # Get the user ID from the authenticated request

    if not all([post_id, post_type, comment_text]):
        return Response({'error': 'Missing required data (postId, postType, commentText)'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve user from JWT token
        user = request.user
        print (user)

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
            return Response({'error': 'Invalid post type'}, status=status.HTTP_400_BAD_REQUEST)

        post = post_model.objects.get(pk=post_id)

        # Create the comment for the post
        comment = Comment.objects.create(post=post, author=user, body=comment_text)
        user = GustUser.objects.get(id=user_id)
        print(user.first_name)

        # Return the username of the comment author along with other comment details
        return Response({
            'id': comment.id,
            'body': comment.body,
            'author': user.first_name,  # Return username instead of user object
            'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
        }, status=status.HTTP_201_CREATED)
    except post_model.DoesNotExist:
        return Response({'error': f'{post_type.capitalize()} post not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   
   
   
   
   
   
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    """
    API endpoint to fetch and edit an existing comment.

    For GET requests:
        - Fetches the comment data.

    For PUT requests:
        - Updates the comment.

    Expects a PUT request with the following JSON data in the request body:
        - commentText: Updated text of the comment (optional)

    Returns a JSON response with details of the edited comment on success,
    or an error message with status code on failure.
    """
    if request.method == 'GET':
        try:
            # Retrieve the comment object to be edited
            comment = Comment.objects.get(pk=comment_id)

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

        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        data = request.data
        comment_text = data.get('commentText')

        try:
            # Retrieve the comment object to be edited
            comment = Comment.objects.get(pk=comment_id)

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

        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   
   
   
   
   
   
   
   
   
   
   
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
        # Assign the user to the selected group if group_id is provided in the request data
        group_id = request.data.get('group_id')
        if group_id:
            group = Group.objects.filter(id=group_id).first()
            if group:
                user.groups.add(group)
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["POST"])
# def login(request):
#     data = request.data
#     username = data.get('username', None)
#     password = data.get('password', None)

#     if not username or not password:
#         return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#     authenticate_user = authenticate(username=username, password=password)

#     if authenticate_user is not None:
#         user = GustUser.objects.get(username=username)
#         serializer = CustomUserSerializer(user)

#         token, created_token = Token.objects.get_or_create(user=user)

#         response_data = {
#             'user': serializer.data,
#             'token': token.key if token else created_token.key
#         }

#         return Response(response_data)
#     else:
#         return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def TestView(request):
    return Response({"message": "Test view page fgjhkjljboiughj"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logs out the authenticated user by deleting their JWT token from the database.

    Returns:
        Response: A JSON response with a success message on successful logout or an error message if logout fails.
    """

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
def lecturer_cv_create(request):
    if request.method == 'POST':
        serializer = LecturerCVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def college_profiles_create(request):
    if request.method == 'POST':
        serializer = CollegeProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def department_profiles_create(request):
    if request.method == 'POST':
        user = GustUser.objects.get()

        serializer = DepartmentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def campus_profiles_create(request):
    try:
        # Retrieve the authenticated user
        user = request.user

        # Extract data from the request
        data = request.data

        # Retrieve the university profile associated with the user
        university_profile = UniversityProfile.objects.filter(user=user).first()

        if not university_profile:
            return Response({'error': 'University profile not found for the authenticated user'}, status=status.HTTP_404_NOT_FOUND)

        # Add the university profile ID to the data
        data['university'] = university_profile.id

        # Serialize the data
        serializer = CampusProfileSerializer(data=data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the serializer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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





# class AddToGroupView(APIView):
#     def post(self, request):
#         try:
#             # Authenticate user based on token
#             user = authenticate(request=request)
#             if user is None:
#                 return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

#             # Retrieve user and group IDs from request data
#             user_id = request.data.get('userId')
#             group_id = request.data.get('groupId')

#             # Retrieve user and group objects
#             user = User.objects.get(id=user_id)
#             group = Group.objects.get(id=group_id)

#             # Update user's group membership
#             user.groups.clear()  # Remove from existing groups
#             user.groups.add(group)  # Add to selected group

#             return Response({"message": "User group updated successfully"}, status=status.HTTP_200_OK)

#         except User.DoesNotExist:
#             return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Group.DoesNotExist:
#             return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

#         except Exception as e:
#             return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# def user_profile(request):
#     # Extract the token from the request headers
#     token_key = request.headers.get('Authorization').split()[1]
    
#     # Retrieve the token object based on the token key
#     token = Token.objects.get(key=token_key)
    
#     # Retrieve the user associated with the token
#     user = token.user
    
#     # Serialize the user profile
#     serializer = CustomUserSerializer(user)
    
#     # Return the serialized user profile in JSON format
#     return JsonResponse(serializer.data)

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