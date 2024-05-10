from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command will help you to interact with MeiliSearch"

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="Action to perform")

    def handle(self, *args, **kwargs):
        action = kwargs.get("action")
        self.stdout.write(f"Doing: {action}")
