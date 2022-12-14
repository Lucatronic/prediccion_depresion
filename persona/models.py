# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telefono = models.CharField("Teléfono", max_length=15, blank=True, null=True)
    direccion = models.CharField("Dirección", max_length=50, blank=True, null=True)
    is_paciente = models.BooleanField(default=False)
    signup_confirmation = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.first_name + " " + self.last_name
 
    
class Paciente(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='paciente')
    ci = models.CharField(max_length=15, unique=True)
    
    class Meta:
        db_table = 'paciente'

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
  
class Doctor(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='doctor')
    ci = models.CharField(max_length=15, unique=True)
    
    class Meta:
        db_table = 'doctor'
        
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
        
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_paciente:
        Paciente.objects.get_or_create(user = instance)
    else:
        Doctor.objects.get_or_create(user = instance)
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_paciente:
        instance.paciente.save()
    else:
        instance.doctor.save()
