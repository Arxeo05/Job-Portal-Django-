from django.db import models
from django.contrib.auth.models import User
GENDER_CHOICES =(
    ("Male", "Male"),
    ("Female", "Female"),
)
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default="MALE")
    type = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.first_name

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,unique=True)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="")
    gender =  models.CharField(max_length=10,choices=GENDER_CHOICES,default="MALE")
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)

    def __str__ (self):
        return self.company_name

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    job_type =  models.CharField(max_length=10,default="FULL-TIME")
    salary = models.FloatField()
    image = models.ImageField(upload_to="")
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    city = models.CharField(max_length=100,default="")
    country = models.CharField(max_length=100,default="")
    skills = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    creation_date = models.DateField()

    def __str__ (self):
        return self.title

class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    resume = models.ImageField(upload_to="")
    apply_date = models.DateField()

    def __str__ (self):
        return str(self.applicant)
class Activity(models.Model):
    action = models.CharField(max_length=50)
    time = models.DateTimeField()
    actor = models.CharField(max_length=50)

    def __str__(self):
        return str(self.action)