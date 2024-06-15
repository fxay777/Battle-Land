from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.utils import timezone
from .lib import core
from uuid import uuid4

class UserManager(BaseUserManager):
    def create_user(self, email, uuid, password):
        if not email:
            raise ValueError("No email set")
        if not uuid:
            raise ValueError("No UUID set")
        if not password:
            raise ValueError("No password set")
        
        user = self.model(email=self.normalize_email(email), uuid=uuid)
        user.set_password(password)
        user.username = uuid
        user.is_active = True
        
        return user
    
    def create_superuser(self, email, uuid, password):
        user = self.create_user(email, uuid, password)
        user.is_superuser = True
        user.is_staff = True

        user.save()
        return user


def generate_token_id():
    return str(uuid4()).replace("-", "")


class RegisterToken(models.Model):
    id = models.CharField(primary_key=True, default=generate_token_id, max_length=36, editable=False)
    uuid = models.CharField(max_length=36)
    email = models.EmailField(max_length=254)
    creation_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class User(AbstractUser):
    uuid = models.CharField(max_length=36, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    lastUsername = models.CharField(max_length=36, blank=True, null=True)

    ip_address = models.CharField(max_length=50, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'uuid'

    def get_data(self):
        data = core.get_player_by_uuid(self.uuid)

        if self.lastUsername != data['name']:
            self.lastUsername = data['name']

        return data

    def has_permission(self, perm):
        default = core.get_default_rank()

        if perm in default['permissions']:
            return True

        rank = core.get_rank(core.get_player_by_uuid(self.uuid)['webData']['rank'])

        if perm in rank['permissions'] or "*" in rank['permissions']:
            return True
        return False

    def __str__(self):
        return self.uuid


class UserVisit(models.Model):
    viewed_by = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    visited_user = models.CharField(max_length=50)

    def __str__(self):
        return self.visited_user
