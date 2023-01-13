

from .models import Post, Category, User
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from celery import shared_task


@shared_task
def new_post_mailing(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    subscribers: list(str) = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]

    category_list = Post.objects.filter(pk=pk).values_list('postCategory__name', flat=True)
    for subscriber in subscribers:  # send e-mails for each subscriber separately
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': f"{post.preview()}",
                'link': f"{settings.SITE_URL}/news/{post.pk}",
                'category_list': f"{list(category_list)}",

            }
        )
        msg = EmailMultiAlternatives(
            subject=f"Celery task: {post.topic}",
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()



@shared_task
def week_mailing():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    # get all post for the last week
    posts = Post.objects.filter(createTime__gte=last_week)
    # get categories only once
    categories = set(posts.values_list('postCategory__name', flat=True))
    # get subscribers_id list
    subscribers_id = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    # for each subscriber in subscribers_id list
    for subscriber_id in subscribers_id:
        # get user e-mail
        user_mail_ = User.objects.filter(id=subscriber_id).values_list('email', flat=True)
        # get category list for this user
        category_list = Category.objects.filter(subscribers=subscriber_id).values_list('name', flat=True)
        # get category_id list for this user
        category_list_id = Category.objects.filter(subscribers=subscriber_id).values_list('id', flat=True)
        # get post for this category_id
        posts_ = Post.objects.filter(postCategory__in=category_list_id)
        # get week post for this user related to his categories
        week_posts = set(posts_)&set(posts)
        # check if this user is subscribed for these categories
        is_subscribed = any(item in category_list for item in categories)

        if is_subscribed:
            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts': week_posts,
                    'categories': list(category_list),

                }
            )
            msg = EmailMultiAlternatives(
                subject='Celery task: Weekly news',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=user_mail_,
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

