from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Settings(models.Model):
    """
    Zakladne nastavenie aplikacie ku ktoremu ma pristup iba administrator.
    """
    invite_price = models.DecimalField(decimal_places=2, max_digits=5)
    bank_account = models.CharField(max_length=128)
    due_date = models.CharField(max_length=9)
    company_name = models.CharField(max_length=64)
    ico = models.CharField(max_length=9)
    dic = models.CharField(max_length=11)
    ic_dph = models.CharField(max_length=14)

    def __str__(self):
        return f"Zoznam nastaveni"


# class Teamleader(models.Model):
# """
# Toto este treba domysliet...
# """
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


class ProfileStatus(models.Model):
    """
    Nastavuje status na uzivatelskom profile.
    Vyber medzi Clen/Teamleader1/Teamleader2/Teamleader3...
    """
    status = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.status}"


class CustomUser(AbstractUser):
    """
    Uziavetelsky upraveny "uzivatel"
    """
    mobile = models.CharField(max_length=16)
    address = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=6)

    has_profile = models.BooleanField(default=False, null=None)
    is_email_verified = models.BooleanField(default=False, null=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.username}"


class UserProfile(models.Model):
    """
    Uzivatelsky profil. Dedi uzivatela z User.
    Natavuje status z ProfileStatus.
    Udrziava body pre jednotliveho uzivatela.
    Obdahuje inforamcie o stave kreditu.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    created = models.DateTimeField(default=timezone.now)
    # status = models.ForeignKey(ProfileStatus, on_delete=models.CASCADE)
    status = models.CharField(default='Clen', max_length=32)
    registrations = models.IntegerField(default=0, blank=True, null=True)
    primary_points = models.IntegerField(default=0, blank=True, null=True)
    secondary_points = models.IntegerField(default=0, blank=True, null=True)
    team_points = models.IntegerField(default=0, blank=True, null=True)
    bonus_points = models.IntegerField(default=0, blank=True, null=True)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_for_recharge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    variable_symbol = models.IntegerField(default=0)

    def set_status(self):
        if self.registrations < 5:
            self.status = 'Clen'
        elif 5 <= self.registrations < 10:
            self.status = 'Teamleader I'
        elif 10 <= self.registrations < 50:
            self.status = 'Teamleader II'
        return self.status

    def set_variable_symbol(self, pk):
        self.variable_symbol = 10000000 + int(pk)
        return self.variable_symbol

    def initMember(self):
        if self.user is not None:
            self.primary_points = 5

    def __str__(self):
        return f"{self.pk}, {self.user}, status: {self.status}"

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'


class Invitation(models.Model):
    """
    Pozvanie. Posle email s informaciami o registracii.
    Email obsahuje email.
    """
    email = models.CharField(max_length=256)
    inviter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.email}, pozval: {self.inviter}"


class Invoice(models.Model):
    """
    Nieco ako faktura. Pokyny pre zaplatenie na dobitie kreditu.
    """
    user_info = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    payment_info = models.ForeignKey(Settings, on_delete=models.CASCADE)
    value = models.CharField(max_length=12)
    due_date = models.DateField()
