from django.db import models
from django.contrib.auth import get_user_model


class UniversityProfile(models.Model):
    cover_photo = models.ImageField(upload_to='university_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='university_profiles/', blank=True, null=True)
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
    cover_photo = models.ImageField(upload_to='campus_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='campus_profiles/', blank=True, null=True)
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
    cover_photo = models.ImageField(upload_to='college_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='college_profiles/', blank=True, null=True)
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

    def __str__(self):
        return self.name


class DepartmentProfile(models.Model):
    cover_photo = models.ImageField(upload_to='department_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='department_profiles/', blank=True, null=True)
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

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
        
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    cover_photo = models.ImageField(upload_to='user_covers/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    link = models.URLField(blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # Add any additional fields here

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




User = get_user_model()

class Chat(models.Model):
    title = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chats')
    is_group_chat = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    media_file = models.FileField(upload_to='media/', blank=True, null=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

class MessageReaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=255)

    class Meta:
        unique_together = ('message', 'user')

    def __str__(self):
        return f"{self.user.username} reacted to message: {self.message.id}"

class ChatMember(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('chat', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.chat.title}"
    
    
    
    
    

class LecturerCV(models.Model):
    avatar = models.ImageField(upload_to='lecturer_avatars/', blank=True, null=True)
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
    
    
    



User = get_user_model()

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_news')

    def __str__(self):
        return self.title

class MediaItem(models.Model):
    NEWS_TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Video'),
        ('text', 'Text')
    ]

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='media_items')
    media_type = models.CharField(max_length=10, choices=NEWS_TYPE_CHOICES)
    content = models.TextField()
    file = models.FileField(upload_to='news_media/', blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_media_type_display()} for News: {self.news.title}"

class MediaItemComment(models.Model):
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    avatar = models.ImageField(upload_to='comment_avatars/', blank=True, null=True)  # Added avatar field
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.media_item}"
class MediaItemLike(models.Model):
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='likes_relation')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.media_item}"

class MediaItemDislike(models.Model):
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='dislikes_relation')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} dislikes {self.media_item}"
