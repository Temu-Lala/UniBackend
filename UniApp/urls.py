from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from . import views
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet,  ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet  # Modify this line
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, CollegePostViewSet, CampusPostViewSet, UniversityPostViewSet, DepartmentPostViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from .views import add_comment,create_lecturer_cv,college_profiles_create,department_profiles_create,campus_profiles_create,update_user_profile,manage_integration_requests,send_integration_request,create_lecturer_cv
from rest_framework_simplejwt import views as jwt_views
from .views import login
from .views import edit_comment

router = DefaultRouter()
router.register(r'university-profiles', UniversityProfileViewSet)
router.register(r'campus-profiles', CampusProfileViewSet)
router.register(r'college-profiles', CollegeProfileViewSet)
router.register(r'department-profiles', DepartmentProfileViewSet)
router.register(r'GustUser', GustUserViewSet)
# router.register(r'lecturer-cv', LecturerCVViewSet)

router.register(r'college-posts', CollegePostViewSet)
router.register(r'campus-posts', CampusPostViewSet)
router.register(r'university-posts', UniversityPostViewSet)
router.register(r'department-posts', DepartmentPostViewSet)
router.register(r'reactions', ReactionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'chat-rooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup),
    # path('login/', views.login),
    path('test-view/', views.TestView),
    path('logout/', views.logout),
    path('user-profile/', views.user_profile),
    path('add-comment/', add_comment, name='add_comment'),
    path('groups/', views.group_list, name='groups'),
    # path('lecturer-cv/', create_lecturer_cv, name='lecturer_cv_create'),  # Add your custom view URL
    path('college_profiles/', college_profiles_create, name='college_profiles_create'),  # Add your custom view URL
    path('department_profiles/', department_profiles_create, name='department_profiles_create'),  # Add your custom view URL
    path('campus_profiles/', campus_profiles_create, name='campus_profiles_create'),  # Add your custom view URL
    path('university_profiles/', update_user_profile, name='university_profiles_create'),  # Add your custom view URL
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login.as_view(), name='login'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
       # URL pattern for sending integration requests
    path('integration_requests/', views.send_integration_request, name='send-integration-request'),
    # path('university-profiles/<int:university_profile_id>/campus_profiles/', campus_profiles_create),
    # URL pattern for university profile owners to manage integration requests
    path('manage_integration_requests/', views.manage_integration_requests, name='manage-integration-requests'),# path('register/', UniversityRegisterView.as_view()),  # Endpoint for university registration
    # path('Universitylogin/', UniversityLoginView.as_view(), name='organization_login'),
    # path('create-college-profile/', college_profiles_create, name='create_college_profile'),
    path('university-profiles/<int:university_profile_id>/campus-profiles/', views.fetch_campus_profiles, name='fetch_campus_profiles'),
    path('university-profiles/<int:university_profile_id>/campus-profiles/', views.fetch_campus_profiles, name='fetch_campus_profiles'),
    path('campus-profiles/<int:campus_profile_id>/college-profiles/', views.fetch_college_profiles, name='fetch_college_profiles'),
    # path('create-lecturer-cv/', views.create_lecturer_cv, name='create_lecturer_cv'),
    path('college-profiles/<int:college_profile_id>/department-profiles/', views.fetch_department_profiles),
    path('create-lecturer-cv/', create_lecturer_cv, name='create_lecturer_cv'),


]
