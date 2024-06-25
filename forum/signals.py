from django.db.models.signals import post_save
from django.dispatch import receiver

from forum.models import ForumComment, ForumLike
from support.models import Notification


@receiver(post_save, sender=ForumComment)
def create_forum_comment_instance(sender, instance, created, **kwargs):
    if created:
        if instance.parent_comment:
            Notification.objects.create(
                user=instance.parent_comment.author,
                title="New Reply",
                body=f"{instance.author.user_information.full_name} replied to your comment.",
            )
        else:
            Notification.objects.create(
                user=instance.forum.author,
                title="New Comment",
                body=f"{instance.author.user_information.full_name} commented on your forum.",
            )


@receiver(post_save, sender=ForumLike)
def create_forum_like_instance(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.forum.author,
            title="New Like",
            body=f"{instance.author.user_information.full_name} liked your forum - {instance.forum.title}",
        )
