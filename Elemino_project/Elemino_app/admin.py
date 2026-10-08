from django.contrib import admin

from .models import Performance


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('pet_id', 'pet_name', 'pet_type', 'owner_name', 'date_registered')
    search_fields = ('pet_name', 'owner_name', 'contact_number')
    list_filter = ('pet_type', 'gender')
