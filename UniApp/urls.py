from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet,LecturerPostViewSet
from . import views
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet,  ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet  # Modify this line
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, LecturerCVViewSet, GustUserViewSet, CollegePostViewSet, CampusPostViewSet, UniversityPostViewSet, DepartmentPostViewSet, ReactionViewSet, CommentViewSet, ChatRoomViewSet, MessageViewSet
from .views import add_comment,create_lecturer_cv,college_profiles_create,department_profiles_create,campus_profiles_create,update_user_profile,manage_integration_requests,send_integration_request,create_lecturer_cv
from rest_framework_simplejwt import views as jwt_views
from .views import login
from .views import edit_comment,UserProfileAssociation,NotificationList
from .views import create_post,delete_post,get_lecturer_cvs,update_lecturer_cv,store_user_into_group,copy_link
from .views import MessageViewSet
from .views import get_university_profile, update_university_profile,delete_university_profile
from .views import  get_campus_profile, update_campus_profile, delete_campus_profile
from .views import CollegeProfileCreateView, CollegeProfileRetrieveUpdateDeleteView
from .views import college_profiles_create
from .views import department_profile_detail, department_profiles_create
from .views import create_lecturer_cv, update_lecturer_cv, delete_lecturer_cv
from .views import search
from .views import LabProfileViewSet, LabFileViewSet
from .views import get_user_university_profile
from .views import get_profile
from .views import get_lab_profile_by_user
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import password_reset_request
from .views import update_password
from .views import AdvertisementViewSet


router = DefaultRouter()
router.register(r'university-profiles', UniversityProfileViewSet)
router.register(r'campus-profiles', CampusProfileViewSet)
router.register(r'college-profiles', CollegeProfileViewSet)
router.register(r'department-profiles', DepartmentProfileViewSet)
router.register(r'GustUser', GustUserViewSet)
# router.register(r'lecturer-cv', LecturerCVViewSet)
router.register(r'lecturer-posts', LecturerPostViewSet)
router.register(r'college-posts', CollegePostViewSet)
router.register(r'campus-posts', CampusPostViewSet)
router.register(r'university-posts', UniversityPostViewSet)
router.register(r'department-posts', DepartmentPostViewSet)
router.register(r'reactions', ReactionViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'chat-rooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'lecturer-cv', LecturerCVViewSet, basename='LecturerCV')
router.register(r'lab-profiles', LabProfileViewSet)
router.register(r'lab-files', LabFileViewSet)
router.register(r'advertisements', AdvertisementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.signup),
    # path('login/', views.login),
    path('test-view/', views.TestView),
    path('logout/', views.logout),
    path('user-profile/', views.user_profile),
    path('add-comment/', add_comment, name='add_comment'),
    path('store-user-into-group/', store_user_into_group, name='store_user_into_group'),

    path('groups/', views.group_list, name='groups'),
    # path('lecturer-cv/', create_lecturer_cv, name='lecturer_cv_create'),  # Add your custom view URL
    path('college_profiles/', college_profiles_create, name='college_profiles_create'),  # Add your custom view URL
    path('department_profiles/', department_profiles_create, name='department_profiles_create'),  # Add your custom view URL
    path('campus_profiles/', campus_profiles_create, name='campus_profiles_create'),  # Add your custom view URL
    path('university_profiles/', update_user_profile, name='university_profiles_create'),  # Add your custom view URL
    path('lab_profiles/', views.lab_profiles, name='lab_profiles'),
    path('lab_profiles/<int:lab_id>/', views.lab_profiles, name='lab_profile_detail'),
   
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', login.as_view(), name='login'),
    path('commentsedit/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
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
    path('create-post/', create_post, name='create_post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('get_lecturer_cvs/', get_lecturer_cvs, name='get_lecturer_cvs'),
    path('lecturer-cv/update/<int:pk>/', update_lecturer_cv, name='update_lecturer_cv'),
    path('lecturer-cv/delete/<int:pk>/', views.delete_lecturer_cv, name='delete_lecturer_cv'),
    path('university-profiles/<int:pk>/', views.university_profile_detail, name='universityprofile-detail'),
    path('api/user-profile/', UserProfileAssociation.as_view(), name='user_profile_association'),
    path('like-post/', views.like_post),
    path('dislike-post/', views.dislike_post),
    path('like-post/', views.like_post),
    path('dislike-post/', views.dislike_post),
    path('comments/college/<int:post_id>/', views.get_college_post_comments),
    path('comments/campus/<int:post_id>/', views.get_campus_post_comments),
    path('comments/university/<int:post_id>/', views.get_university_post_comments),
    path('comments/department/<int:post_id>/', views.get_department_post_comments),
    path('comments/lecturer/<int:post_id>/', views.get_lecturer_post_comments),
    # path('share-post/', share_post, name='share_post'),
    path('share-post/<str:post_type>/<int:post_id>/', views.share_post, name='share_post'),
    path('copy-link/', copy_link, name='copy_link'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('university_rating/', views.university_rating, name='university_rating'),
    path('campus_rating/', views.campus_rating, name='campus_rating'),
    path('college_rating/', views.college_rating, name='college_rating'),
    path('department_rating/', views.department_rating, name='department_rating'),
    path('lab_rating/', views.lab_rating, name='lab_rating'),
    path('notifications/', NotificationList.as_view(), name='notification-list'),

    path('follow-university-profile/<int:university_id>/', views.university_follow, name='university_follow'),
    path('unfollow-university-profile/<int:university_id>/', views.university_unfollow),  # Correct URL pattern
    path('check-follow-university-status/university/<int:university_id>/', views.university_check_follow_status, name='check_university_follow_status'),
    path('university_followers_count/<int:university_id>/', views.university_followers_count, name='university_follow_count'),
    
    
    path('follow-campus-profile/<int:campus_id>/', views.campus_follow, name='follow_campus_profile'),
    path('unfollow-campus-profile/<int:campus_id>/', views.campus_unfollow),  # Correct URL pattern
    path('check-follow-campus-status/campus/<int:campus_id>/', views.campus_check_follow_status, name='check_follow_status'),
    path('campus_followers_count/<int:campus_id>/', views.campus_followers_count, name='followers_count'),
    
    path('follow-college-profile/<int:college_id>/', views.follow_college, name='follow_college_profile'),
    path('unfollow-college-profile/<int:college_id>/', views.unfollow_college),  # Correct URL pattern
    path('check-follow-status/college/<int:college_id>/', views.college_check_follow_status, name='check_follow_status'),
    path('collage_followers_count/<int:college_id>/', views.collage_followers_count, name='followers_count'),
    
    path('follow-department-profile/<int:department_id>/', views.departmeent_follow, name='follow_departmet_profile'),
    path('unfollow-department-profile/<int:department_id>/', views.department_unfollow),  # Correct URL pattern
    path('check-follow-status/department/<int:department_id>/', views.department_check_follow_status, name='check_follow_status'),
    path('department_followers_count/<int:department_id>/', views.department_followers_count, name='followers_count'),
    
    path('follow-lecturer-profile/<int:lecturer_id>/', views.lecturer_follow, name='follow_lecturer_profile'),
    path('unfollow-lecturer-profile/<int:lecturer_id>/', views.lecturer_unfollow),  # Correct URL pattern
    path('check-follow-status/lecturer/<int:lecturer_id>/', views.lecturer_check_follow_status, name='check_follow_status'),
    path('followers_count/<int:lecturer_id>/', views.lecturer_followers_count, name='followers_count'),
    # path('recommend/', views.recommend_universities, name='recommend_universities'),
    # path('recommend_university/', recommend_university, name='recommend_university'),

    # path('university_profiles/', get_university_profile, name='get_university_profile'),
    # path('university_profiles/<int:pk>/', update_university_profile, name='update_university_profile'),
    # path('university-profiles/update/', update_university_profile, name='update_university_profile'),
    path('university-profile/', get_university_profile, name='get-university-profile'),
    path('university-profile/update/', update_university_profile, name='update-university-profile'),
    path('university-profile/delete/', delete_university_profile, name='delete-university-profile'),
    
    path('campus-profile/', get_campus_profile, name='get_campus_profile'),
    path('campus-profile/update/', update_campus_profile, name='update_campus_profile'),
    path('campus-profile/delete/', delete_campus_profile, name='delete_campus_profile'),


    path('college-profiles/', CollegeProfileCreateView.as_view(), name='create-college-profile'),
    path('college-profiles/<int:pk>/', CollegeProfileRetrieveUpdateDeleteView.as_view(), name='retrieve-update-delete-college-profile'),


    path('college_profiles/update/', views.user_college_profile, name='user_college_profile'),
    path('department-profiles/detail/', department_profile_detail),



    path('update-lecturer-cv/', update_lecturer_cv, name='update-lecturer-cv'),
    path('delete-lecturer-cv/', delete_lecturer_cv, name='delete-lecturer-cv'),
    
    
    path('api/search', search, name='search'),
    path('api/user-university-profile/', get_user_university_profile, name='user-university-profile'),
    path('api/get-profile/', get_profile, name='get-profile'),
    path('api/university-profiles/by-user/', UniversityProfileViewSet.as_view({'get': 'by_user'}), name='university-profile-by-user'),
    path('api/campus-profiles/by-user/', CampusProfileViewSet.as_view({'get': 'by_user'}), name='campus-profile-by-user'),
    path('api/college-profiles/by-user/', CollegeProfileViewSet.as_view({'get': 'by_user'}), name='college-profile-by-user'),
    path('api/department-profiles/by-user/', DepartmentProfileViewSet.as_view({'get': 'by_user'}), name='department-profile-by-user'),
    path('api/lecturer-cv/by-user/', LecturerCVViewSet.as_view({'get': 'by_user'}), name='lecturer-cv-by-user'),
    path('lab-profiles/by-user/', get_lab_profile_by_user, name='get_lab_profile_by_user'),

    path('contacts-with-chats/', views.MessageViewSet.contacts_with_chats, name='contacts_with_chats'),
    
    path('api/password_reset/', password_reset_request, name='password_reset_request'),
    
    path('reset/<uidb64>/<token>/', update_password, name='update_password'),
    
    #test
    path('university/profiles/', views.university_profile_list, name='university_profile_list'),
    path('recommendation/', views.recommend_universities_view, name='recommendation'),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) 