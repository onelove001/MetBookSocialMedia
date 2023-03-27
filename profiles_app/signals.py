from .models import *
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save, sender=Relationship)
def add_friend(sender, instance, created, **kwargs):
    # sender_ = instance.sender
    # receiver_ = instance.receiver
    if instance.status == "accepted":
        instance.sender.friends.add(instance.receiver.user)
        instance.receiver.friends.add(instance.sender.user)
        instance.sender.save()
        instance.receiver.save()

