from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


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
