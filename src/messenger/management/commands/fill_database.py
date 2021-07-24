import io
from random import choice, randrange

from django.core import files
from django.core.management.base import BaseCommand
from faker import Faker
from PIL import Image

from messenger.models import Chat, File, Message, User


class Command(BaseCommand):

    help = "Add new student(s) to the system"

    def add_arguments(self, parser):
        parser.add_argument("-l", "--len", type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker("en_US")

        self.stdout.write("Start filling data")

        users = []
        for index in range(options["len"]):
            self.stdout.write(f"Process {index} line of User")

            user, _ = User.objects.get_or_create(username=faker.profile()["username"])
            user.first_name = faker.first_name()
            user.last_name = faker.last_name()
            user.email = faker.email()
            user.set_password("1234")
            user.save()
            users.append(user)

        for index in range(options["len"]):
            self.stdout.write(f"Process {index} line of Chat -> Message 10000 ->? File")

            chat = Chat()
            chat.title = faker.sentence()[0:40]
            chat.creator = choice(users)
            chat.save()

            for _ in range(randrange(10000)):
                message = Message()
                message.sender = choice(users)
                message.chat = chat
                message.message = faker.text()
                message.save()

                if choice([True, False]):
                    image_file = io.BytesIO()
                    image = Image.new(
                        "RGBA",
                        size=(100, 100),
                        color=(
                            randrange(255),
                            randrange(255),
                            randrange(255),
                        ),
                    )
                    image.save(image_file, "png")
                    image_file.name = "test.png"
                    image_file.seek(0)

                    file = File()
                    file.document = files.File(image_file)
                    file.message = message
                    file.save()

        self.stdout.write("End filling data")
