from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from uuid import uuid4
from rest_framework.authtoken.models import Token
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser
from django.db import models

# class GustUser(AbstractUser):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#     ]
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     age = models.IntegerField(blank=True, null=True)
#     field_choices = models.CharField(max_length=255)  # Fields of study chosen by the student
#     health_condition = models.CharField(max_length=100)  # Health condition of the student
#     exam_result = models.IntegerField()  # Exam result of the student

#     def __str__(self):
#         return self.username
class GustUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
class AsStudent(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    field_choices = models.CharField(max_length=255)
    health_condition = models.CharField(max_length=100)
    exam_result = models.IntegerField()
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE, related_name='following')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f'{self.user.username} follows {self.content_type}#{self.object_id}'
class JWTToken(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token for {self.user.username}"


class Notification(models.Model):
    recipient = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

class UniversityProfile(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    HEALTH_CONDITION_SUPPORT_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    CATEGORY_CHOICES = (
        ('Applied', 'Applied'),
        ('Engineering', 'Engineering'),
        ('Comprehensive', 'Comprehensive'),
        ('Research', 'Research'),
        ('Science and Technology', 'Science and Technology'),
    )
    REGION_CHOICES = (
        ('Addis Abeba', 'Addis Abeba'),
        ('Dire Dawa', 'Dire Dawa'),
        ('Oromia', 'Oromia'),
        ('Amhara', 'Amhara'),
        ('Tigray', 'Tigray'),
        ('Afar', 'Afar'),
        ('Somali', 'Somali'),
        ('Benishangul-Gumuz', 'Benishangul-Gumuz'),
        ('SNNPR', 'SNNPR'),
        ('Harari', 'Harari'),
        ('Gambella', 'Gambella'),
    )
    CITY_CHOICES = (
        ('city1', 'City 1'),
        ('city2', 'City 2'),
        ('city3', 'City 3'),
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
    number_of_libraries = models.IntegerField(default=0)
    number_of_laboratories = models.IntegerField(default=0)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    pobox = models.CharField(max_length=255, blank=True)
    specific_place = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    health_condition_support = models.CharField(max_length=3, choices=HEALTH_CONDITION_SUPPORT_CHOICES)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=555)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(
            recipient=self.user,
            message='You have a new rating on your university profile.'
        )

    def __str__(self):
        return self.name

class CampusProfile(models.Model):
    HEALTH_CONDITION_SUPPORT_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    CATEGORY_CHOICES = (
        ('Applied', 'Applied'),
        ('Engineering', 'Engineering'),
        ('Comprehensive', 'Comprehensive'),
        ('Research', 'Research'),
        ('Science and Technology', 'Science and Technology'),
    )
    REGION_CHOICES = (
        ('Addis Abeba', 'Addis Abeba'),
        ('Dire Dawa', 'Dire Dawa'),
        ('Oromia', 'Oromia'),
        ('Amhara', 'Amhara'),
        ('Tigray', 'Tigray'),
        ('Afar', 'Afar'),
        ('Somali', 'Somali'),
        ('Benishangul-Gumuz', 'Benishangul-Gumuz'),
        ('SNNPR', 'SNNPR'),
        ('Harari', 'Harari'),
        ('Gambella', 'Gambella'),
    )
    CITY_CHOICES = (
        ('city1', 'City 1'),
        ('city2', 'City 2'),
        ('city3', 'City 3'),
    )
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
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    region = models.CharField(max_length=50, choices=REGION_CHOICES)
    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    pobox = models.CharField(max_length=255, blank=True)
    specific_place = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(
            recipient=self.user,
            message=f'You have a new rating on your Campus profile.'
        )
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
    university  = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.user,
            message=f'You have a new rating on your university profile.'
        )
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
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.user,
            message=f'You have a new rating on your university profile.'
        )
    def __str__(self):
        return self.name


class LecturerCV(models.Model):
    avatar = models.ImageField(upload_to='static/lecturer_avatars/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='static/lecturer_avatars/', blank=True, null=True)
    name = models.CharField(max_length=255)
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
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    university_profile = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    campus_profile = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    college_profile = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    department_profile = models.ForeignKey(DepartmentProfile, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.user,
            message=f'You have a new rating on your university profile.'
        )
    def __str__(self):
        return self.name



class IntegrationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Integration request from {self.campus.name} to {self.university.name}"





class LabProfile(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    university_profile = models.ForeignKey('UniversityProfile', on_delete=models.CASCADE)
    campus_profile = models.ForeignKey('CampusProfile', on_delete=models.CASCADE)
    college_profile = models.ForeignKey('CollegeProfile', on_delete=models.CASCADE)
    department_profile = models.ForeignKey('DepartmentProfile', on_delete=models.CASCADE)

    def __str__(self):
        return f'LabProfile {self.id}'

class LabFile(models.Model):
    FILE_TYPES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    lab_profile = models.ForeignKey(LabProfile, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='static/lab_files/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
class BasePost(models.Model):
    id = models.AutoField(primary_key=True)
    university = models.ForeignKey('UniversityProfile', on_delete=models.CASCADE, blank=True, null=True)
    campus = models.ForeignKey('CampusProfile', on_delete=models.CASCADE, blank=True, null=True)
    college = models.ForeignKey('CollegeProfile', on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey('DepartmentProfile', on_delete=models.CASCADE, blank=True, null=True)
    lecturer = models.ForeignKey('LecturerCV', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, null=True)
    link = models.URLField(blank=True, null=True)
    content = models.TextField()
    file = models.FileField(upload_to='static/post_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    user = models.ForeignKey('GustUser', on_delete=models.CASCADE)
    comments = GenericRelation('Comment')
    
    # New fields to store the names
    university_name = models.CharField(max_length=255, blank=True, null=True)
    campus_name = models.CharField(max_length=255, blank=True, null=True)
    college_name = models.CharField(max_length=255, blank=True, null=True)
    department_name = models.CharField(max_length=255, blank=True, null=True)
    lecturer_name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.university:
            self.university_name = self.university.name
        if self.campus:
            self.campus_name = self.campus.name
        if self.college:
            self.college_name = self.college.name
        if self.department:
            self.department_name = self.department.name
        if self.lecturer:
            self.lecturer_name = self.lecturer.name
        super().save(*args, **kwargs)
        Notification.objects.create(
            recipient=self.user,
            message=f'You have a new rating on your university profile.'
        )

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

class LecturerPost(BasePost):
    responding_to_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    author = models.ForeignKey('GustUser', on_delete=models.CASCADE, related_name='authored_comments')
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment "{self.body}" by {self.author.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(
            recipient=self.content_object.user,
            message=f'Your post received a new comment.'
        )



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



class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(GustUser, related_name='chat_rooms')


class Message(models.Model):
    sender = models.ForeignKey(GustUser, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(GustUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.recipient,
            message=f'You have a new messages '
        )
class UniversityRating(models.Model):
    id = models.AutoField(primary_key=True)
    university_profile = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE, related_name='university_ratings')
    value = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.university_profile.user,
            message=f'You have a new rating on your university profile.'
        )
class CampusRating(models.Model):
    id = models.AutoField(primary_key=True)
    campus_profile = models.ForeignKey(CampusProfile, on_delete=models.CASCADE, related_name='university_ratings')
    value = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.campus_profile.user,
            message=f'You have a new rating on your university profile.'
        )
class CollegeRating(models.Model):
    id = models.AutoField(primary_key=True)
    college_profile = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE, related_name='university_ratings')
    value = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.college_profile.user,
            message=f'You have a new rating on your university profile.'
        )
class DepartmentRating(models.Model):
    id = models.AutoField(primary_key=True)
    department_profile = models.ForeignKey(DepartmentProfile, on_delete=models.CASCADE, related_name='university_ratings')
    value = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.department_profile.user,
            message=f'You have a new rating on your university profile.'
        )
class LabRating(models.Model):
    id = models.AutoField(primary_key=True)
    labprofile_profile = models.ForeignKey(LabProfile, on_delete=models.CASCADE, related_name='university_ratings')
    value = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a notification for the user associated with the university profile
        Notification.objects.create(
            recipient=self.labprofile_profile.user,
            message=f'You have a new rating on your university profile.'
        )
        
        
        
        
class UniversityFollow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    university = models.ForeignKey(UniversityProfile, on_delete=models.CASCADE)  # Add this line

class CampusFollow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    campus = models.ForeignKey(CampusProfile, on_delete=models.CASCADE)
    

class CollegeFollow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    college = models.ForeignKey(CollegeProfile, on_delete=models.CASCADE)
    


class DepartmentFollow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentProfile, on_delete=models.CASCADE)
    
class LecturerFollow(models.Model):
    user = models.ForeignKey(GustUser, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(LecturerCV, on_delete=models.CASCADE)





class Advertisement(models.Model):
    STATUS_CHOICES = (
        ('opened', 'Opened'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/advertisements/images/', blank=True, null=True)
    video = models.FileField(upload_to='static/advertisements/videos/', blank=True, null=True)
    call_to_action = models.CharField(max_length=255, blank=True, null=True)
    target_audience = models.JSONField(blank=True, null=True)  # JSONField to store demographics and psychographics
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    platform = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    landing_page_url = models.URLField(blank=True, null=True)
    metrics_goals = models.JSONField(blank=True, null=True)  # JSONField to store objectives (e.g., clicks, conversions)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='opened')

    def __str__(self):
        return self.title