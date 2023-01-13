import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category, User
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


# наша задача
def my_job():
    #  Your job processing logic here...
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(createTime__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    # subscribers_mail = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    subscribers_id = set(Category.objects.filter(name__in=categories).values_list('subscribers', flat=True))

    for subscriber_id in subscribers_id:
        user_ = User.objects.filter(id=subscriber_id).values_list('username', flat=True)
        user_mail_ = User.objects.filter(id=subscriber_id).values_list('email', flat=True)
        category_list = Category.objects.filter(subscribers=subscriber_id).values_list('name', flat=True)
        category_list_id = Category.objects.filter(subscribers=subscriber_id).values_list('id', flat=True)
        posts_ = Post.objects.filter(postCategory__in=category_list_id)
        week_posts = set(posts_)&set(posts)

        is_subscribed = any(item in category_list for item in categories)
        # if category_list not in categories:
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
                subject='Weekly news',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=user_mail_,
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="30"),#second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")