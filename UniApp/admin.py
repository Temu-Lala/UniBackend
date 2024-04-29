from django.contrib import admin
from .models import (
    UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, 
    LecturerCV, GustUser, Reaction, Comment, ChatRoom, Message, 
    CollegePost, CampusPost, UniversityPost, DepartmentPost, 
    BaseComment
)

def approve_selected_universities(modeladmin, request, queryset):
    queryset.update(status='approved')

def reject_selected_universities(modeladmin, request, queryset):
    queryset.update(status='rejected')

approve_selected_universities.short_description = "Approve selected universities"
reject_selected_universities.short_description = "Reject selected universities"

@admin.register(UniversityProfile)
class UniversityProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']
    actions = [approve_selected_universities, reject_selected_universities]

admin.site.register(CampusProfile)
admin.site.register(CollegeProfile)
admin.site.register(DepartmentProfile)
admin.site.register(LecturerCV)
admin.site.register(GustUser)
admin.site.register(ChatRoom)
admin.site.register(Message)

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'reaction_type', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'body', 'created_on')

@admin.register(CollegePost)
class CollegePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'university', 'campus', 'college', 'department', 'content', 'created_at', 'updated_at')

@admin.register(CampusPost)
class CampusPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'university', 'campus', 'college', 'department', 'content', 'created_at', 'updated_at')

@admin.register(UniversityPost)
class UniversityPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'university', 'campus', 'college', 'department', 'content', 'created_at', 'updated_at')

@admin.register(DepartmentPost)
class DepartmentPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'university', 'campus', 'college', 'department', 'content', 'created_at', 'updated_at')
