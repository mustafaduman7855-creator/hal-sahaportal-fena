from django.contrib import admin
from .models import Facility, User, PublishRequest

admin.site.register(Facility)
admin.site.register(User)
admin.site.register(PublishRequest)
