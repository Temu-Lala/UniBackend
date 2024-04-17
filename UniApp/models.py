from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from uuid import uuid4
from django.contrib.auth.hashers import check_password

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
User = get_user_model()


# Define custom related names for groups and user_permissions

class UniversityProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/university_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/university_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    establishment_date = models.DateField()
    number_of_lectures = models.IntegerField(default=0)
    number_of_departments = models.IntegerField(default=0)
    number_of_campuses = models.IntegerField(default=0)
    number_of_colleges = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)

    def __str__(self):
        return self.name

class CampusProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/campus_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/campus_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    establishment_date = models.DateField()
    number_of_lectures = models.IntegerField(default=0)
    number_of_departments = models.IntegerField(default=0)
    number_of_campuses = models.IntegerField(default=0)
    number_of_colleges = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CollegeProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/college_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/college_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    establishment_date = models.DateField()
    number_of_lectures = models.IntegerField(default=0)
    number_of_departments = models.IntegerField(default=0)
    number_of_campuses = models.IntegerField(default=0)
    number_of_colleges = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DepartmentProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/department_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/department_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    establishment_date = models.DateField()
    number_of_lectures = models.IntegerField(default=0)
    number_of_departments = models.IntegerField(default=0)
    number_of_campuses = models.IntegerField(default=0)
    number_of_colleges = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LecturerCV(models.Model):
    avatar = models.ImageField(upload_to='static/lecturer_avatars/', blank=True, null=True)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    skills1 = models.CharField(max_length=255)
    skills2 = models.CharField(max_length=255)
    skills3 = models.CharField(max_length=255)
    skills4 = models.CharField(max_length=255)
    about = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    linkedin = models.URLField()
    education_background = models.CharField(max_length=255)
    background_description = models.TextField()
    education_background2 = models.CharField(max_length=255, blank=True, null=True)
    background_description2 = models.TextField(blank=True, null=True)
    education_background3 = models.CharField(max_length=255, blank=True, null=True)
    background_description3 = models.TextField(blank=True, null=True)
    languages = models.CharField(max_length=255)
    languages2 = models.CharField(max_length=255, blank=True, null=True)
    languages3 = models.CharField(max_length=255, blank=True, null=True)
    professional_experience = models.CharField(max_length=255)
    professional_experience2 = models.CharField(max_length=255, blank=True, null=True)
    professional_experience3 = models.CharField(max_length=255, blank=True, null=True)
    key_responsibilities = models.TextField()
    key_responsibilities2 = models.TextField(blank=True, null=True)
    key_responsibilities3 = models.TextField(blank=True, null=True)
    project1 = models.CharField(max_length=255)
    project_description1 = models.TextField()
    project2 = models.CharField(max_length=255, blank=True, null=True)
    project_description2 = models.TextField(blank=True, null=True)
    project3 = models.CharField(max_length=255, blank=True, null=True)
    project_description3 = models.TextField(blank=True, null=True)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GustUser(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  # Make email field unique
    password = models.CharField(max_length=128)  # You may want to use a more secure password field like Django's built-in hashed password field
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    cover_photo = models.ImageField(upload_to='static/user_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/user_profiles/', blank=True, null=True)
    link = models.URLField(blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)



    def __str__(self):
        return self.name

class Post(models.Model):
    NEWS_TYPE_CHOICES = [
        ('UNIVERSITY', 'University News'),
        ('CAMPUS', 'Campus News'),
        ('COLLEGE', 'College News'),
        ('DEPARTMENT', 'Department News'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    news_type = models.CharField(max_length=20, choices=NEWS_TYPE_CHOICES)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE, blank=True, null=True)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, blank=True, null=True)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(DepartmentProfile, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    file = models.FileField(upload_to='static/post_files/', blank=True, null=True)  # Change this as per your requirement
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    def __str__(self):
        return f"Post #{self.pk} - {self.get_news_type_display()}"

class Reaction(models.Model):
    REACTION_TYPES = [
        ('L', 'Like'),
        ('D', 'Dislike'),
        ('H', 'Haha'), # Add more reaction types as needed
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=1, choices=REACTION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

@require_POST
@login_required
def add_comment(request):
    data = request.POST
    post_id = data.get('postId')
    comment_text = data.get('commentText')
    
    if post_id and comment_text:
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.create(post=post, author=request.GustUser, body=comment_text)
            return JsonResponse({
                'id': comment.id,
                'body': comment.body,
                'author': comment.author.username,
                'created_on': comment.created_on.strftime("%Y-%m-%d %H:%M:%S")
            })
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Post does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
def __str__(self):
    return 'Comment "{}" by {}'.format(self.body, self.author)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(GustUser, related_name='chat_rooms')

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)