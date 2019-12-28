from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager
from curriculum.models import SkillItem,Experience

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))


class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    # def get_search_skillset(self):
    #     return self.skills

    # def get_search_experienceset(self):
    #     return self.experiences.only("title","entreprise")

    objects = UserManager()
