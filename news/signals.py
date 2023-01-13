from django.template.loader import render_to_string

from django.conf import settings
from .models import Post, PostCategory, User
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.dispatch import receiver
from datetime import datetime

from django.shortcuts import render

from .tasks import new_post_mailing


@receiver(post_save, sender=Post) # insted of using post_save.connect(notify_post_create, sender=Post) after fuction
def notify_post_create(sender, instance, created, **kwargs):
    # в зависимости от того, есть ли такой объект уже в базе данных или нет, тема письма будет разная
    if created:
        subject = f"'{instance.createTime.strftime('%H:%M:%S')} {instance.createTime.strftime('%d-%m-%Y')}: User: '{instance.author}' created a new Post"
    else:
        # subject = f"'{instance.editTime.strftime('%H:%M:%S')} {instance.editTime.strftime('%d-%m-%Y')}: User: '{instance.author}' changed the Post"
        subject = f"'{datetime.now().strftime('%H:%M:%S')} {datetime.now().strftime('%d-%m-%Y')}: User: '{instance.author}' changed the Post"

    mail_admins(
        subject=f"admin_notification: {subject}",
        message=f"Title: '{instance.topic}'\n\n'{instance.preview()}'",

    )
# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
# post_save.connect(notify_post_create, sender=Post)

@receiver(post_delete, sender=Post)
def notify_post_delete(sender, instance, **kwargs):
    subject = f"'{instance.createTime.strftime('%H:%M:%S')} {instance.createTime.strftime('%d-%m-%Y')}: {instance.author}'s post has been deleted"
    mail_admins(
        subject=subject,
        message=f"Title: '{instance.topic}'\n\n'{instance.content}'",
    )


# notifications for subscribers
def self_notification(preview, pk, topic, subscribers):
    category_list = Post.objects.filter(pk=pk).values_list('postCategory__name', flat=True)
    for subscriber in subscribers: # send e-mails for each subscriber separately
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f"{settings.SITE_URL}/news/{pk}",
                'category_list': f"{list(category_list)}",
            }
        )
        msg = EmailMultiAlternatives(
            subject=topic,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
# notifications for subscribers if new post
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add': # before we add the post
        categories = instance.postCategory.all()
        subscribers: list(str) = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        self_notification(instance.preview(), instance.pk, instance.topic, subscribers)


# notifications for subscribers if new post - Celery
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post_Celery(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add': # before we add the post
        new_post_mailing.delay(instance.pk)


