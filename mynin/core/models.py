from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)
    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(db_index=True, unique=True, max_length=256)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    mobile = models.CharField(max_length=256)

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.email}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Invitation(models.Model):
    name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    mobile = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} {self.email} {self.mobile}"

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

class Teamleader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team_points = models.IntegerField()
    votes = models.IntegerField()
    businness = models.CharField(max_length=128)
    reserve = models.IntegerField()

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Teamleader'
        verbose_name_plural = 'Teamleaders'

class ProfileStatus(models.Model):
    status = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.status}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    created = models.DateTimeField(default=timezone.now)
    registrations = models.IntegerField(blank=True, null=True)
    primary_points = models.IntegerField(default=0, blank=True, null=True)
    secondary_points = models.IntegerField(blank=True, null=True)
    team_points = models.IntegerField(blank=True, null=True)
    bonus_points = models.IntegerField(blank=True, null=True)
    status = models.ForeignKey(ProfileStatus, on_delete=models.CASCADE)
    teamleaders = models.ManyToManyField(Teamleader, blank=True)

    def initMember(self):
        if self.user is not None:
            self.primary_points = 5
    
    def __str__(self):
        return f"{self.user}, status: {self.status}"

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'


