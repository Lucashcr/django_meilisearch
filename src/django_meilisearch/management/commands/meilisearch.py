from django.apps import apps
from django.core.management.base import BaseCommand

from django_meilisearch import client
from django_meilisearch.documents import Document


class Command(BaseCommand):
    help = "This command will help you to interact with MeiliSearch"
    
    ACTION_CHOICES = ["create", "delete", "populate", "clear"]

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="Action to perform")
        parser.add_argument("index", type=str, help="Index name (app_label.IndexClass)")

    def handle(self, *args, **kwargs):
        action = kwargs.get("action")
        
        index = kwargs.get("index")
        
        if action not in self.ACTION_CHOICES:
            self.stdout.write(self.style.ERROR(f"Invalid action: \"{action}\""))
            return
        
        if index is None:
            self.stdout.write(self.style.ERROR("Not enough arguments: Index name is required"))
            return
        
        if index not in Document.REGISTERED_INDEXES:
            self.stdout.write(self.style.ERROR(f"Index not found: \"{index}\""))
            return
        
        IndexCls = Document.REGISTERED_INDEXES[index]
        current_indexes = [index.uid for index in client.get_indexes()["results"]]
        
        if action == "create":
            if IndexCls.name in current_indexes:
                self.stdout.write(self.style.ERROR(f"Index already exists: \"{index}\""))
                return
            
            IndexCls.create()
            self.stdout.write(self.style.SUCCESS(f"Index created: \"{index}\""))
        
        if not IndexCls.name in current_indexes:
            self.stdout.write(self.style.ERROR(f"Index not found: \"{index}\""))
            return
        
        if action == "populate":
            count = IndexCls.populate()
            self.stdout.write(self.style.SUCCESS(f"Index populated: \"{index}\""))
            self.stdout.write(self.style.SUCCESS(f"Documents indexed: {count}"))
            return
        
        if action == "delete":
            client.delete_index(IndexCls.name)
            self.stdout.write(self.style.SUCCESS(f"Index deleted: \"{index}\""))
            return
        
        if action == "clear":
            client.get_index(IndexCls.name).delete_all_documents()
            self.stdout.write(self.style.SUCCESS(f"Index cleared: \"{index}\""))
            return
