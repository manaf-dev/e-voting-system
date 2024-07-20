from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver

from .models import Vote
from accounts.models import CustomUser

import logging

logger = logging.getLogger(__name__)


@receiver(signal=pre_save, sender=Vote)
def prevent_vote_change_receiver(sender, instance, **kwargs):
    if instance.pk:
        raise ValueError("Change of votes is not allowed.")


# @receiver(signal=pre_delete, sender=Vote)
# def prevent_vote_delete_receiver(sender, instance, **kwargs):
#     raise ValueError("Delete of votes is not allowed.")


# @receiver(signal=post_save, sender=CustomUser)
# def add_new_user(sender, instance, created, **kwargs):
#     if created:
#         logger.info(f"Admin added {instance.first_name} {instance.last_name}")
