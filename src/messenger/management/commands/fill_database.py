import uuid

import io
from random import choice

from django.core import files
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand

from messenger.models import File, Message, Chat, User


class Command(BaseCommand):

    help = 'Add new student(s) to the system'

    def add_arguments(self, parser):
        parser.add_argument('-l', '--len', type=int, default=10)

    def handle(self, *args, **options):
        faker = Faker()

        self.stdout.write('Start filling data')

        users = []
        for _ in range(options['len']):
            user = User()
            user.username = faker.profile()['username']
            user.first_name = faker.first_name()
            user.last_name = faker.last_name()
            user.email = faker.email()
            user.save()
            users.append(user)

        for _ in range(options['len']):
            chat = Chat()
            chat.title = faker.sentence()[0:40]
            chat.creator = choice(users)
            chat.save()

            for _ in range(100):
                message = Message()
                message.sender = choice(users)
                message.chat = chat
                message.message = faker.text()
                message.save()

                if faker.pybool():
                    image_file = io.BytesIO()
                    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
                    image.save(image_file, 'png')
                    image_file.name = 'test.png'
                    image_file.seek(0)

                    file = File()
                    file.document = files.File(image_file)
                    file.message = message
                    file.save()

        self.stdout.write('End filling data')
