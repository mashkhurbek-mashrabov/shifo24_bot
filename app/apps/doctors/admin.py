from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models.doctors import Doctor, WorkSchedule
from .forms import DoctorForm


class WorkScheduleInline(admin.TabularInline):
    model = WorkSchedule
    extra = 0
    min_num = 1
    max_num = 7


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "display_photo", "status", "created_at")
    list_filter = ("specialization", "status", "created_at")
    search_fields = ("first_name", "last_name", "phone_number")
    search_help_text = _("Enter name to search")
    date_hierarchy = 'created_at'
    inlines = (WorkScheduleInline,)

    form = DoctorForm

    fieldsets = (
        (_('User Details'), {
            'fields': ('first_name', 'last_name', 'photo'),
        }),
        (_('Contact Details'), {
            'fields': ('phone_number', 'telegram_id'),
        }),
        (_('Address'), {
            'fields': ('address', ('lat', 'lng')),
        }),
        (_('Status'), {
            'fields': ('status',),
        }),
        (_('Specialization'), {
            'fields': ('specialization',),
        }),
        (_('Additional Info'), {
            'fields': (("lunch_start_time", "lunch_end_time"),),
        }),
        (_('Bio'), {
            'fields': ('bio',),
        }),
        (_('Creation date'), {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
            'description': format_html(
                f'<p style="color: green">{_('The date and time when the user was created')}.</p>'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('specialization',)

    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<a href='{obj.photo.url}' target='_blank'><img src='{obj.photo.url}' width='20' /></a>")
        else:
            return _("No photo")

    display_photo.short_description = _("Photo")
