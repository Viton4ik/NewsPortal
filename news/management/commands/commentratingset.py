
# python manage.py commentratingset --help
from django.core.management.base import BaseCommand, CommandError
from news.models import Comment, User


class Command(BaseCommand):
    help = 'This command will set the rating you need for Author you have chosen.' \
           'Also you can set the rating for Author comments'

    def add_arguments(self, parser):
        parser.add_argument('Author', type=str)

    def handle(self, *args, **options):
        global author
        rating = input(f'Put rating you would prefer to set for "{options["Author"]}": ')
        user = User.objects.get(username=options["Author"])
        try:
            for comment in Comment.objects.filter(commentUser=user):
                comment.rating = rating
                comment.save()
                self.stdout.write(self.style.SUCCESS(f'"{comment}" has been updated with new rating: "{rating}"'))
        except ValueError:
            self.stdout.write(self.style.ERROR(f'To set "rating" use numbers only!'))