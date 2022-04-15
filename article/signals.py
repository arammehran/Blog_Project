from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import Followers
from .models import Article, Notifications


@receiver(post_save, sender=Article)
def create_article(sender, instance, created, **kwargs):
    if created:
        follower_obj = Followers.objects.filter(author=instance.author).first()
        stuff = 'The author named "{}" has posted' \
                ' an Article with title "{}"'.format(instance.author.name, instance.title)
        notification_objects = [Notifications(author=instance.author, reader=one, content=stuff)
                                for one in follower_obj.reader.all()]
        Notifications.objects.bulk_create(notification_objects)


