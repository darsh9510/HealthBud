from django.db import models
from django.contrib.auth.models import AbstractUser,User



class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=100)
    registration_year = models.IntegerField()
    state_medical_council = models.CharField(max_length=100)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)

class Rooms(models.Model):
    name = models.CharField(max_length=100)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True)
    participent = models.ManyToManyField(User, related_name='participent',null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Massage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['created_at']
