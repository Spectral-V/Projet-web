from django.contrib import admin
from .models import Profile, Message, Room

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ('room_id',)

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Room, RoomAdmin)