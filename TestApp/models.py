from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

    GENDER_CHOICES = (('M','Male'),('F','Female'),('Other','Other'))

    profile_id = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100,blank=True,null=True)
    phone_no = models.CharField(max_length=22,unique=True,blank=True,null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length = 10,blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    profilepic= models.ImageField(upload_to='profile_pic',default='profile.jpg',null=True,blank=True)

    def __str__(self):
        return f'{self.profile_id.username}'

class PermanentAddress(models.Model):
    user_id = models.OneToOneField(Profile,on_delete=models.CASCADE)
    street_address = models.CharField(max_length = 200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length = 50)
    pincode = models.IntegerField()
    country = models.CharField(max_length = 100)

    def __str__(self):
        return self.city

class CompanyAddress(models.Model):
    user_id = models.OneToOneField(Profile,on_delete=models.CASCADE)
    street_address = models.CharField(max_length = 200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length = 50)
    pincode = models.IntegerField()
    country = models.CharField(max_length = 30)

    def __str__(self):
        return self.city

class Friends(models.Model):
    GENDER_CHOICES = (('M','Male'),('F','Female'),('Other','Other'))
    profile_id = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length = 100,blank=True,null=True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length = 10,blank=True,null=True)

    def __str__(self):
        return f'{self.name}'
