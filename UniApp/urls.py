from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from . import views
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet,  ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet  # Modify this line
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, CollegePostViewSet, CampusPostViewSet, UniversityPostViewSet, DepartmentPostViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from .views import add_comment

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
    path('login/', views.login),
    path('test-view/', views.TestView),
    path('logout/', views.logout),
    path('user-profile/', views.user_profile),
    path('add-comment/', add_comment, name='add_comment'),
    # path('register/', UniversityRegisterView.as_view()),  # Endpoint for university registration
    # path('Universitylogin/', UniversityLoginView.as_view(), name='organization_login'),
]
