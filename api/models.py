from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        unique=True,
        null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30, choices=Role.choices, default='user')
    bio = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserAccountManager()

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=200,
        blank=True, null=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=200,
        blank=True, null=True,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='Заголовок',
        max_length=200,
        blank=True, null=True,
    )
    year = models.SmallIntegerField()
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        db_index=False,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    text = models.TextField(blank=True,
                            null=True)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.score_avg = Review.objects.filter(title_id=self.title).aggregate(
            Avg('score')
        )
        self.title.rating = self.score_avg['score__avg']
        self.title.save()


class Comment(models.Model):
    text = models.TextField(blank=True,
                            null=True)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return self.text
