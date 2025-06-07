from django.contrib import admin
from Spontana_App.models import Activity, MoodTimeEntry, UserProfile
from django.utils.html import format_html


# Register your models here.



# USER PROFILE ADMIN
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'num_adventures', 'bio', 'image_tag']
    search_fields = ['user__username']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        if obj.image:
            return obj.image.url
        return "No image"

    image_tag.short_description = 'Profile Image'

admin.site.register(UserProfile, UserProfileAdmin)



# MoodTimeEntry Admin
class MoodTimeEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'mood', 'duration']
    list_filter = ['mood', 'duration']
    search_fields = ['mood', 'duration']

admin.site.register(MoodTimeEntry, MoodTimeEntryAdmin)



# Activity Admin
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'mood_entry', 'duration']
    list_filter = ['mood_entry__mood']  
    search_fields = ['title', 'description']
    
admin.site.register(Activity, ActivityAdmin)


