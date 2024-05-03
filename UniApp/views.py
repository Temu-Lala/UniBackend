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
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Q

from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt
from .models import (
    UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile,
    LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message,
    CollegePost, CampusPost, UniversityPost, DepartmentPost,stortoken,IntegrationRequest
)
from .serializers import (
    UniversityProfileSerializer, CampusProfileSerializer, CollegeProfileSerializer,
    DepartmentProfileSerializer, LecturerCVSerializer, CustomUserSerializer,
    ReactionSerializer, CommentSerializer, ChatRoomSerializer, MessageSerializer,
    CollegePostSerializer, CampusPostSerializer, UniversityPostSerializer,
    DepartmentPostSerializer,TokenSerializer,IntegrationRequestSerializer
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
        except User.DoesNotExist:
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
            messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id).order_by('created_at')  # Update order_by clause here
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Sender ID and Recipient ID are required."}, status=status.HTTP_400_BAD_REQUEST)
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









@api_view(['POST'])
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
def fetch_department_profiles(request, college_profile_id):
    try:
        departments = DepartmentProfile.objects.filter(college_id=college_profile_id)
        serializer = DepartmentProfileSerializer(departments, many=True)
        return Response(serializer.data)
    except DepartmentProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



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