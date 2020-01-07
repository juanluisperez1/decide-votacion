from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    SEX_OPTIONS = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    PROVINCE_OPTIONS = (
        ('S', 'Sevillistán'),
        ('H', 'Huelvistán'),
	    ('C', 'Cadistán'),
    )

    EMPLOYMENT_OPTIONS = (
        ('M', 'Militant'),
        ('B', 'Baron'),
	    ('S', 'Senator'),
	    ('P', 'President'),
    )
    
    related_political_party = models.ForeignKey('voting.PoliticalParty', 
related_name='PoliticalParty',
 on_delete=models.CASCADE, blank=True, null=True)

    birthdate = models.DateField(('Birthdate'),null=True)

    sex = models.CharField(('Sex'),max_length=1,
 choices=SEX_OPTIONS, null=True)

    related_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
	
    province = models.CharField(('Province'),max_length=1,
 choices=PROVINCE_OPTIONS, null=True)
    
    employment = models.CharField(('Employment'),max_length=1,
 choices=EMPLOYMENT_OPTIONS, null=True, blank=True)

    def __str__(self):
        return "("+str(self.sex)+","+str(self.birthdate)+","+str(self.related_political_party)+")"


    def clean(self):
        if self.employment and not self.related_political_party:
            raise forms.ValidationError({'related_political_party':
["The related political party is required if you choose an Employment!"]})
