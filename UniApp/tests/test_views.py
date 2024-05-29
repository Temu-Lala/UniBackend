import datetime
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from UniApp.models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser, JWTToken
from UniApp.serializers import UniversityProfileSerializer, UniversityPostSerializer, CampusPostSerializer, CollegePostSerializer, DepartmentPostSerializer, LecturerPostSerializer, TokenSerializer
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

class CombinedTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = GustUser.objects.create_user(username='testuser', password='testpass')

    def test_successful_login(self):
        # Test successful login with valid credentials
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)
        # Check if the JWT token is saved in the database
        jwt_token = JWTToken.objects.filter(user=self.user).first()
        self.assertIsNotNone(jwt_token)

    def test_missing_credentials(self):
        # Test login with missing credentials
        response = self.client.post('/login/', {'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    

    def test_list_university_profiles(self):
        # Create some sample university profiles for testing
        UniversityProfile.objects.create(name='University A', location='Location A', establishment_date=now(), group_id=1, user_id=1)
        UniversityProfile.objects.create(name='University B', location='Location B', establishment_date=now(), group_id=1, user_id=1)

        # Send GET request to list all university profiles
        url = reverse('university_profile_list')
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the expected number of university profiles
        self.assertEqual(len(response.data), 2)

        # Check that the response data matches the serialized data of the created university profiles
        expected_data = UniversityProfileSerializer(UniversityProfile.objects.all(), many=True).data
        self.assertEqual(response.data, expected_data)

    def test_create_university_profile(self):
        # Define data for creating a new university profile
        new_profile_data = {
            'name': 'New University',
            'location': 'New Location',
            # Add other fields as required by your serializer
        }

        # Send POST request to create a new university profile
        url = reverse('university_profile_list')
        response = self.client.post(url, new_profile_data)

        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the new university profile is created in the database
        self.assertTrue(UniversityProfile.objects.filter(name='New University').exists())

        # Optionally, you can check that the response data matches the created university profile
        created_profile = UniversityProfile.objects.get(name='New University')
        self.assertEqual(response.data, UniversityProfileSerializer(created_profile).data)
    
    def setUp(self):
        self.url = reverse('university_profile_list')
        self.valid_payload = {
            'name': 'Test University',
            'location': 'Test Location',
            'establishment_date': '2022-05-27',
            'group_id': 1,
            'user_id': 1
        }
        self.invalid_payload = {
            'name': 'Test University',
            'location': 'Test Location',
            'establishment_date': '2022-05-27',
            'group_id': 1  # Missing 'user_id' field
        }

    def test_get_university_profiles(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_invalid_university_profile(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
