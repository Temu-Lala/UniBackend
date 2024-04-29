from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from . import views
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet,  ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet  # Modify this line
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, CollegePostViewSet, CampusPostViewSet, UniversityPostViewSet, DepartmentPostViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from .views import add_comment,lecturer_cv_create,college_profiles_create,department_profiles_create,campus_profiles_create,update_user_profile
from rest_framework_simplejwt import views as jwt_views
from .views import login
from .views import edit_comment

router = DefaultRouter()
router.register(r'university-profiles', UniversityProfileViewSet)
router.register(r'campus-profiles', CampusProfileViewSet)
router.register(r'college-profiles', CollegeProfileViewSet)
router.register(r'department-profiles', DepartmentProfileViewSet)
router.register(r'lecturer-cvs', LecturerCVViewSet)
router.register(r'GustUser', GustUserViewSet)
router.register(r'college-posts', CollegePostViewSet)
router.register(r'campus-posts', CampusPostViewSet)
router.register(r'university-posts', UniversityPostViewSet)
router.register(r'department-posts', DepartmentPostViewSet)
router.register(r'reactions', ReactionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'chat-rooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup),
    # path('login/', views.login),
    path('test-view/', views.TestView),
    path('logout/', views.logout),
    path('user-profile/', views.user_profile),
    path('add-comment/', add_comment, name='add_comment'),
    path('groups/', views.group_list, name='groups'),
    path('lecturer-cv/', lecturer_cv_create, name='lecturer_cv_create'),  # Add your custom view URL
    path('college_profiles/', college_profiles_create, name='college_profiles_create'),  # Add your custom view URL
    path('department_profiles/', department_profiles_create, name='department_profiles_create'),  # Add your custom view URL
    path('campus_profiles/', campus_profiles_create, name='campus_profiles_create'),  # Add your custom view URL
    path('university_profiles/', update_user_profile, name='university_profiles_create'),  # Add your custom view URL
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login.as_view(), name='login'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit_comment'),

    # path('register/', UniversityRegisterView.as_view()),  # Endpoint for university registration
    # path('Universitylogin/', UniversityLoginView.as_view(), name='organization_login'),
]
