from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

class Userreg(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=300, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    
class Creator(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, upload_to="profile")
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    
    
class Quiz_category(models.Model):
    cid=models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    category=models.CharField(max_length=100, null=True)
    

class Question(models.Model):
    question= models.CharField(max_length=100, null=True)
    op1=models.CharField(max_length=100, null=True)
    op2=models.CharField(max_length=100, null=True)
    op3=models.CharField(max_length=100, null=True)
    op4=models.CharField(max_length=100, null=True)
    answer=models.CharField(max_length=100, null=True)
    image = models.ImageField(null=True, upload_to="profile")
    cid=models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    qcid=models.ForeignKey(Quiz_category, on_delete=models.CASCADE, null=True)
    
    
class Answered_question(models.Model):
    answer= models.CharField(max_length=100, null=True)
    mark=models.CharField(max_length=100, null=True)
    cid=models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
    qcid=models.ForeignKey(Quiz_category, on_delete=models.CASCADE, null=True)
    question= models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    uid=models.ForeignKey(Userreg, on_delete=models.CASCADE,null=True)
    