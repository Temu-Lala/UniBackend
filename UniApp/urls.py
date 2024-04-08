# urls.py

from django.urls import path, include
from rest_framework import routers
from .views import UniversityProfileViewSet, CampusProfileViewSet, CollegeProfileViewSet, DepartmentProfileViewSet, UserProfileViewSet, ChatViewSet, MessageViewSet, MessageReactionViewSet, LecturerCVViewSet, NewsViewSet, MediaItemViewSet, MediaItemCommentViewSet, MediaItemLikeViewSet, MediaItemDislikeViewSet
from django.conf import settings
from django.conf.urls.static import static
router = routers.DefaultRouter()
router.register(r'university-profiles', UniversityProfileViewSet)
router.register(r'campus-profiles', CampusProfileViewSet)
router.register(r'college-profiles', CollegeProfileViewSet)
router.register(r'department-profiles', DepartmentProfileViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'message-reactions', MessageReactionViewSet)
router.register(r'lecturer-cvs', LecturerCVViewSet)
router.register(r'news', NewsViewSet)
router.register(r'media-items', MediaItemViewSet)
router.register(r'media-item-comments', MediaItemCommentViewSet)
router.register(r'media-item-likes', MediaItemLikeViewSet)
router.register(r'media-item-dislikes', MediaItemDislikeViewSet)

urlpatterns = [
    path('', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)