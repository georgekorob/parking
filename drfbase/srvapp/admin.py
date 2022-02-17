from django.contrib import admin
from srvapp.models import CAMServer, AIServer, ANServer


# Register your models here.
admin.site.register(CAMServer)
admin.site.register(AIServer)
admin.site.register(ANServer)
