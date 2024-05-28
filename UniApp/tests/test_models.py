from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from UniApp.models import (
    GustUser, Follow, JWTToken, Notification, UniversityProfile, CampusProfile, 
    CollegeProfile, DepartmentProfile, LecturerCV, IntegrationRequest, LabProfile,
    CollegePost, CampusPost, UniversityPost, DepartmentPost, LecturerPost, Comment,
    Reaction, ChatRoom, Message, UniversityRating, CampusRating, CollegeRating,
    DepartmentRating, LabRating, CollegeFollow
)
from django.utils import timezone

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        # Create a group to satisfy the foreign key constraint
        self.group = Group.objects.create(name='Test Group')
        
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.another_user = User.objects.create_user(username='anotheruser', password='testpass')
        
        self.university = UniversityProfile.objects.create(
            name='Test University',
            establishment_date='2000-01-01',
            location='Test Location',
            group_id=self.group.id,  # Use the created group's id
            user=self.user
        )
        
        self.campus = CampusProfile.objects.create(
            name='Test Campus',
            establishment_date='2000-01-01',
            location='Test Location',
            university=self.university,
            group_id=self.group.id,  # Use the created group's id
            user=self.user
        )
        
        self.college = CollegeProfile.objects.create(
            name='Test College',
            establishment_date='2000-01-01',
            location='Test Location',
            campus=self.campus,
            university=self.university,
            user=self.user
        )

    def test_gust_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.another_user.username, 'anotheruser')

    def test_gust_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    

    def test_jwttoken_creation(self):
        token = JWTToken.objects.create(user=self.user, token='abc123')
        self.assertEqual(str(token), f'Token for {self.user.username}')

    def test_notification_creation_on_university_save(self):
        self.university.save()
        notification = Notification.objects.filter(recipient=self.user).last()
        self.assertEqual(notification.message, 'You have a new rating on your university profile.')

    def test_university_profile_str(self):
        self.assertEqual(str(self.university), 'Test University')

    def test_campus_profile_str(self):
        self.assertEqual(str(self.campus), 'Test Campus')

    def test_college_profile_str(self):
        self.assertEqual(str(self.college), 'Test College')

   

    def test_comment_creation_and_notification(self):
        post = CollegePost.objects.create(
            title='Test Post',
            content='Test Content',
            user=self.user,
            college=self.college
        )
        comment = Comment.objects.create(
            content_object=post,
            author=self.another_user,
            body='Test Comment'
        )
        self.assertEqual(str(comment), f'Comment "{comment.body}" by {self.another_user.username}')
        notification = Notification.objects.filter(recipient=self.user).last()
        self.assertEqual(notification.message, 'Your post received a new comment.')

    def test_chatroom_user_addition(self):
        chat_room = ChatRoom.objects.create(name='Test Room')
        chat_room.users.add(self.user)
        self.assertIn(self.user, chat_room.users.all())

    
    def test_university_rating_creation_and_notification(self):
        rating = UniversityRating.objects.create(
            university_profile=self.university,
            value=5,
            user=self.another_user
        )
        self.assertEqual(rating.value, 5)
        notification = Notification.objects.filter(recipient=self.user).last()
        self.assertEqual(notification.message, 'You have a new rating on your university profile.')

    def test_follow_unique_constraint(self):
        Follow.objects.create(user=self.user, content_object=self.university)
        with self.assertRaises(Exception):
            Follow.objects.create(user=self.user, content_object=self.university)


