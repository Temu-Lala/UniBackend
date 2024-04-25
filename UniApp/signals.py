from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UniversityProfile, CampusProfile, CollegeProfile, DepartmentProfile, LecturerCV, GustUser

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        group = instance.groups.first()  # Assuming a user can only belong to one group
        if group:
            if group.name == 'University':
                UniversityProfile.objects.create(user=instance)
            elif group.name == 'Campus':
                CampusProfile.objects.create(user=instance)
            elif group.name == 'College':
                CollegeProfile.objects.create(user=instance)
            elif group.name == 'Department':
                DepartmentProfile.objects.create(user=instance)
            elif group.name == 'Lecturer':
                LecturerCV.objects.create(user=instance)
            elif group.name == 'GustUser':
                GustUser.objects.create(user=instance)
