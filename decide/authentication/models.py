from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    SEX_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    related_political_party = models.ForeignKey('voting.PoliticalParty', related_name='PoliticalParty', on_delete=models.CASCADE)
    birthdate = models.DateField(('Birthdate'),null=True)
    sex = models.CharField(('Sex'),max_length=1, choices=SEX_OPTIONS, null=True)
    related_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    def __str__(self):
        return "("+str(self.sex)+","+str(self.birthdate)+","+str(self.related_political_party)+")"
