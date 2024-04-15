from django.contrib import admin
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, UserProfile, Post, Reaction, Comment, ChatRoom, Message

# Register your models here
admin.site.register(UniversityProfile)
admin.site.register(CampusProfile)
admin.site.register(CollegeProfile)
admin.site.register(DepartmentProfile)
admin.site.register(LecturerCV)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(ChatRoom)
admin.site.register(Message)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
