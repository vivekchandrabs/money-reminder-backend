from django.db import models
from django.contrib.auth.models import User
# Create your models here.

TYPE_OF_INTEREST = (
    (1, "Simple Interest"),
    (2, "Compound Interest"),
)

TIME_OF_INTEREST = (
    (1, "monthly"),
    (2, "Quarterly"),
    (3, "Half Yearly"),
    (4, "Annually"),
)

class FDAccountDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fd_name = models.CharField(max_length=100)
    principal = models.IntegerField(default=0)
    type_of_interest = models.IntegerField(choices=TYPE_OF_INTEREST, default=1)
    period = models.IntegerField(default=0)
    time_of_interest = models.IntegerField(choices=TIME_OF_INTEREST, default=1)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    bank = models.CharField(max_length=100, default=None, null=True, blank=True)
    branch = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.fd_name} | {self.principal} | {self.amount}"


class Interest(models.Model):
    fd = models.ForeignKey(FDAccountDetail, on_delete=models.CASCADE, null=True, blank=True)
    interest_amt = models.FloatField(default=0.0, null=True, blank=True)
    month = models.DateField(auto_now=True, null=True, blank=True)
    is_sent = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.fd.fd_name} | {self.interest_amt} | {self.month}"