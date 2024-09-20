from django.core.management.base import BaseCommand

from django_meilisearch import client
from django_meilisearch.index import BaseIndex


class Command(BaseCommand):
    help = "This command will help you to interact with MeiliSearch"

    ACTION_CHOICES = [
        "acreate",
        "adestroy",
        "apopulate",
        "aclean",
        "arebuild",
        "create",
        "destroy",
        "populate",
        "clean",
        "rebuild",
    ]

    def add_arguments(self, parser):
        parser.add_argument("action", type=str, help="Action to perform")
        parser.add_argument(
            "indexes",
            nargs="*",
            type=str,
            help="Index names (index_name | app_label.IndexClass)",
        )
        parser.add_argument(
            "--yes",
            "-y",
            action="store_true",
            help="Confirm before executing the action",
        )

    def handle(self, *args, **kwargs):
        action = kwargs.get("action")
        indexes = kwargs.get("indexes")
        confirm = kwargs.get("yes")

        if action not in self.ACTION_CHOICES:
            self.error(f'Invalid action: "{action}"')
            return

        if not indexes:
            indexes = BaseIndex.INDEX_NAMES.keys()

        for index in indexes:
            if (
                index not in BaseIndex.REGISTERED_INDEXES
                and index not in BaseIndex.INDEX_NAMES
            ):
                self.error(f'Index not found: "{index}"')
                continue

            if index in BaseIndex.INDEX_NAMES:
                index = BaseIndex.INDEX_NAMES[index]

            IndexCls: BaseIndex = BaseIndex.REGISTERED_INDEXES[index]
            current_indexes = [index.uid for index in client.get_indexes()["results"]]

            if action == "acreate":
                if IndexCls.name in current_indexes:
                    self.error(f'Index already exists: "{index}"')
                    continue

                task = IndexCls.acreate()
                self.info(f'Index being created: "{index}"')
                self.info(f"Task ID: {task.uid}")
                continue

            elif action == "create":
                if IndexCls.name in current_indexes:
                    self.error(f'Index already exists: "{index}"')
                    continue

                task = IndexCls.create()
                if task.status == "failed":
                    self.error(f'Failed to create index: "{index}"')
                    self.error(f"Error: {task.details}")
                elif task.status == "succeeded":
                    self.success(f'Index created successfully: "{index}"')
                else:
                    self.info(f'Index creation status: "{index}"')
                    self.info(f"Details: {task.details}")
                continue

            elif IndexCls.name not in current_indexes:
                self.error(f'Index not found: "{index}"')
                continue

            if not confirm:
                self.question(
                    f'Are you sure you want to perform the action "{action}" on index "{index}"? (y/n):'
                )
                confirmation = input()
                if confirmation.lower() != "y":
                    self.error(
                        f'Action cancelled by user: "{action}" on index "{index}"'
                    )
                    continue

            if action == "apopulate":
                tasks = IndexCls.apopulate()
                count = sum(task.details["receivedIndexs"] for task in tasks)
                self.success(f'Index being populated: "{index}"')
                self.success(f"Indexs being indexed: {count}")
                self.info(f"Task IDs: {', '.join(str(task.uid) for task in tasks)}")

            elif action == "populate":
                tasks = IndexCls.populate()
                count = sum(task.details["indexedIndexs"] for task in tasks)

                if task.status == "failed":
                    self.error(f'Failed to populate index: "{index}"')
                    self.error(f"Error: {task.details}")
                elif task.status == "succeeded":
                    self.success(f'Index populated successfully: "{index}"')
                else:
                    if all(task.status == "succeeded" for task in tasks):
                        self.success(f'Index populated successfully: "{index}"')
                        self.success(f"Indexs indexed: {count}")
                        continue

                    for task in tasks:
                        if task.status != "succeeded":
                            self.error(f'Failed to populate index: "{index}"')
                            self.error(f"Error: {task.details}")

            elif action == "adestroy":
                task = IndexCls.adestroy()

                self.success(f'Index being destroyed: "{index}"')
                self.info(f"Task ID: {task.uid}")

            elif action == "destroy":
                task = IndexCls.destroy()

                if task.status == "failed":
                    self.error(f'Failed to destroy index: "{index}"')
                    self.error(f"Error: {task.details}")
                elif task.status == "succeeded":
                    self.success(f'Index destroyed successfully: "{index}"')
                else:
                    self.info(f'Index destroying status: "{task.status}"')
                    self.info(f"Details: {task.details}")

            elif action == "aclean":
                task = IndexCls.aclean()
                self.success(f'Index cleared: "{index}"')
                self.info(f"Task ID: {task.uid}")

            elif action == "clean":
                task = IndexCls.clean()
                count = task.details["deletedIndexs"]

                if task.status == "failed":
                    self.error(f'Failed to clean index: "{index}"')
                    self.error(f"Error: {task.details}")
                elif task.status == "succeeded":
                    self.success(f'Index cleaned successfully: "{index}"')
                    self.success(f"Indexs deleted: {count}")
                else:
                    self.info(f'Index destroying status: "{task.status}"')
                    self.info(f"Details: {task.details}")

            elif action == "arebuild":
                IndexCls.aclean()
                tasks = IndexCls.apopulate()
                count = sum(task.details["receivedIndexs"] for task in tasks)

                self.success(f'Index being rebuilt: "{index}"')
                self.success(f"Indexs being reindexed: {count}")
                self.info(f"Task ID: {task.uid}")

            elif action == "rebuild":
                IndexCls.clean()
                tasks = IndexCls.populate()
                count = sum(task.details["indexedIndexs"] for task in tasks)

                if task.status == "failed":
                    self.error(f'Failed to destroy index: "{index}"')
                    self.error(f"Error: {task.details}")
                elif task.status == "succeeded":
                    self.success(f'Index destroyed successfully: "{index}"')
                else:
                    self.info(f'Index destroying status: "{task.status}"')
                    self.info(f"Details: {task.details}")

            else:
                self.error(f'Invalid action: "{action}"')

    def error(self, message):
        self.stdout.write(self.style.ERROR(f"[ERROR]:   {message}"))

    def success(self, message):
        self.stdout.write(self.style.SUCCESS(f"[SUCCESS]: {message}"))

    def info(self, message):
        self.stdout.write(f"[INFO]:    {message}")

    def question(self, message):
        self.stdout.write(self.style.WARNING(f"[WARNING]: {message}"), ending=" ")
