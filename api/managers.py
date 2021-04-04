from django.contrib.auth.models import BaseUserManager
from django.db import models


class Role(models.TextChoices):
    USER = 'user', 'пользователь'
    MODERATOR = 'moderator', 'модератор'
    ADMIN = 'admin', 'администратор'


class UserAccountManager(BaseUserManager):
    def create_user(self, email, role=Role.USER,
                    username=None, password=None):
        user = self.model(
            email=email, role=role, username=username, password=password
        )
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role=Role.USER,
                         username=None, password=None):
        user = self.create_user(
            email=email, role=role, username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
