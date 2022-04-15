import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    """The Custom BaseManager Class"""
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=True)


class User(AbstractBaseUser, BaseModel):
    ROLE_OPTIONS = [('a', 'author'), ('r', 'reader')]
    name = models.CharField(max_length=255)
    email = models.EmailField(null=False, blank=False, unique=True)
    role = models.CharField(max_length=1, choices=ROLE_OPTIONS)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # All admins are staff
        return self.is_admin

    class Meta:
        """
        Verbose name and verbose plural
        """
        verbose_name = "User"
        verbose_name_plural = "User"


class Followers(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Followers_author")
    reader = models.ManyToManyField(User, related_name="Followers_reader")














