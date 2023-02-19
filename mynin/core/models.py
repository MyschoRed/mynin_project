from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


class Settings(models.Model):
    invite_price = models.DecimalField(decimal_places=2, max_digits=5)
    bank_account = models.CharField(max_length=128)
    due_date = models.CharField(max_length=9)
    company_name = models.CharField(max_length=64)
    ico = models.CharField(max_length=9)
    dic = models.CharField(max_length=11)
    ic_dph = models.CharField(max_length=14)

    def __str__(self):
        return f"Zoznam nastaveni"


"""
Pozvanie. Posle email s informaciami o registracii. 
Email obsahuje email.
"""
class Invitation(models.Model):
    email = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.email}"


"""
Toto este treba domysliet...
"""
# class Teamleader(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     team_points = models.IntegerField()
#     votes = models.IntegerField()
#     businness = models.CharField(max_length=128)
#     reserve = models.IntegerField()
#
#     def __str__(self):
#         return f"{self.user}"
#
#     class Meta:
#         verbose_name = 'Teamleader'
#         verbose_name_plural = 'Teamleaders'


"""
Nastavuje status na uzivatelskom profile. 
Vyber medzi Clen/Teamleader.
"""


class ProfileStatus(models.Model):
    status = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.status}"


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=16)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


"""
Uzivatelsky profil. Dedi uzivatela z User. 
Natavuje status z ProfileStatus.
Udrziava body pre jednotliveho uzivatela.
"""


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    created = models.DateTimeField(default=timezone.now)
    # status = models.ForeignKey(ProfileStatus, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    registrations = models.IntegerField(blank=True, null=True)
    primary_points = models.IntegerField(default=0, blank=True, null=True)
    secondary_points = models.IntegerField(default=0, blank=True, null=True)
    team_points = models.IntegerField(default=0, blank=True, null=True)
    bonus_points = models.IntegerField(default=0,blank=True, null=True)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # teamleaders = models.ManyToManyField(Teamleader, blank=True)
    def set_status(self):
        if self.registrations < 5:
            self.status = 'Clen'
        elif 5 <= self.registrations < 10:
            self.status = 'Teamleader I'
        elif 10 <= self.registrations < 50:
            self.status = 'Teamleader II'

        return self.status

    def initMember(self):
        if self.user is not None:
            self.primary_points = 5

    def __str__(self):
        return f"{self.user}, status: {self.status}"

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'


# class Credit(models.Model):
#     credit = models.DecimalField(decimal_places=2, max_digits=10)
#
#     def recharge(self, count):
#         credit = float(self.credit) + float(count)
#         return credit
#
#     def __str__(self):
#         return f"Kredit: {self.credit} EUR"
