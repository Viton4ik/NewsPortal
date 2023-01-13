
import os
from celery import Celery
from celery.schedules import crontab


# связываем настройки Django с настройками Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

#  создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app = Celery('News_Portal')

# указываем пространство имен, чтобы Celery сам находил все необходимые настройки в
# общем конфигурационном файле settings.py. Он их будет искать по шаблону «CELERY_***».
app.config_from_object('django.conf:settings', namespace='CELERY')

# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'post_weekly_mailing_8am': {
        'task': 'news.tasks.week_mailing',
        # 'schedule': 5,
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (agrs),
    },
}

