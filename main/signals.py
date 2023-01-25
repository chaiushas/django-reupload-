from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Client

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)
        print('KWARGS: ', kwargs)


# Pakoregavus vartotoją, išsaugomas ir profilis
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.client.save()