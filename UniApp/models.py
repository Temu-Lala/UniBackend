from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class GustUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

class JWTToken(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token for {self.user.username}"

class BaseComment(models.Model):
    author = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['created_on']

    def __str__(self):
        return 'Comment "{}" by {}'.format(self.body, self.author)
class UniversityProfile(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    cover_photo = models.ImageField(upload_to='static/university_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/university_profiles/', blank=True, null=True)
  
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    link = models.URLField(blank=True)
    establishment_date = models.DateField()
    number_of_lectures = models.IntegerField(default=0)
    number_of_departments = models.IntegerField(default=0)
    number_of_campuses = models.IntegerField(default=0)
    number_of_colleges = models.IntegerField(default=0)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Add status field
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CampusProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/campus_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/campus_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
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
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
class stortoken(models.Model):
    jwttokens = models.CharField(max_length=500)
class CollegeProfile(models.Model):
    cover_photo = models.ImageField(upload_to='static/college_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/college_profiles/', blank=True, null=True)
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return self.name

    def generate_token(self):
        return Token.objects.create(user=self)

class BasePost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE, blank=True, null=True)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, blank=True, null=True)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(DepartmentProfile, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    file = models.FileField(upload_to='static/post_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    def __str__(self):
        return f"Post #{self.pk}"

    class Meta:
        abstract = True

class CollegePost(BasePost):
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class CampusPost(BasePost):
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class UniversityPost(BasePost):
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class DepartmentPost(BasePost):
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class Reaction(models.Model):
    REACTION_TYPES = [
        ('L', 'Like'),
        ('D', 'Dislike'),
        ('H', 'Haha'),
    ]
    post = models.ForeignKey(
        CollegePost,  # Change this to the appropriate concrete subclass
        on_delete=models.CASCADE
    )
    reaction_type = models.CharField(max_length=1, choices=REACTION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    post = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

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
