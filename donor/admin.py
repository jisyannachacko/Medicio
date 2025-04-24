from django.contrib import admin
from .models import Blood_Users, BloodRequest, Feedback
# Register your models here.

admin.site.register(Blood_Users)

admin.site.register(BloodRequest)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)