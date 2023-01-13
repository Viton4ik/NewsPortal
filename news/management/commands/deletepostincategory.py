

# python manage.py deletepostincategory --help
from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'This command will delete all posts in chosen category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)


    def handle(self, *args, **options):
        global category
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? (yes/no) ')

        if answer == 'no':
            self.stdout.write(self.style.ERROR('Отменено'))
        else:
            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(postCategory=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Все новости в категории {category.name} успешно удалены'))
            except category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Не удалось найти категорию {category.name}'))