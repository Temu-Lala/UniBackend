# admin.py

from django.contrib import admin
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, UserProfile, Chat, Message, MessageReaction, LecturerCV, News, MediaItem, MediaItemComment, MediaItemLike, MediaItemDislike

admin.site.register(UniversityProfile)
admin.site.register(CampusProfile)
admin.site.register(CollegeProfile)
admin.site.register(DepartmentProfile)
admin.site.register(UserProfile)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(MessageReaction)
admin.site.register(LecturerCV)
admin.site.register(News)
admin.site.register(MediaItem)
admin.site.register(MediaItemComment)
admin.site.register(MediaItemLike)
admin.site.register(MediaItemDislike)
