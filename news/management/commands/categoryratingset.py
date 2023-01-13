
# python manage.py categoryratingset --help
from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'This command will set the rating you need for the each post in chosen category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        global category
        rating = input(f'Put rating you would prefer to set for the posts in "{options["category"]}": ')
        category = Category.objects.get(name=options['category'])
        try:
            for post in Post.objects.filter(postCategory=category):
                post.rating = rating
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Post "{post.topic}" has been updated with new rating: "{rating}"'))
        except ValueError:
            self.stdout.write(self.style.ERROR(f'To set "rating" use numbers only!'))



