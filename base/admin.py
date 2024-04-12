from django.contrib import admin

# Register your models here.

from .models import Rooms
from .models import Topic
from .models import Message

admin.site.register(Rooms)
admin.site.register(Topic)
# meka default add wela thiynne e hinda one nha - admin.site.register(User)
admin.site.register(Message)
