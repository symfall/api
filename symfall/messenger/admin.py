from django.contrib import admin
from .models import User, Chat, Message, File
# Register your models here.
admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(File)