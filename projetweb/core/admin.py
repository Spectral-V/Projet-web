from django.contrib import admin
from .models import Profile, Message, Room,Permission

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ('room_id',)
    
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('message_id',)

admin.site.register(Profile)
admin.site.register(Message, MessageAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Permission)
