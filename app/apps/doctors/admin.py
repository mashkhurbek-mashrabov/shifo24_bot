import json

from django.contrib import admin
from django.core.serializers import serialize
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils import timezone
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    MultipleChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
    RelatedDropdownFilter,
    RangeDateFilter,
    RangeNumericFilter,
)

from .models.doctors import Doctor, WorkSchedule
from .models.rate import Rate


# from .forms import DoctorForm


class WorkScheduleInline(TabularInline):
    model = WorkSchedule
    extra = 0
    min_num = 1
    max_num = 7
    tab = True


@admin.register(Doctor)
class DoctorAdmin(ModelAdmin):
    list_display = ("name", "display_photo", "average_rating", "status", "created_at")
    search_fields = ("first_name", "last_name", "phone_number")
    search_help_text = _("Enter name or phone number to search")
    date_hierarchy = 'created_at'
    inlines = (WorkScheduleInline,)
    list_filter_submit = True
    list_filter = [
        ("status", MultipleChoicesDropdownFilter),
        ("specializations", MultipleRelatedDropdownFilter),
        ("created_at", RangeDateFilter),
    ]

    # form = DoctorForm

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
        (_('Specializations'), {
            'fields': ('specializations',),
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
    filter_horizontal = ('specializations',)
    actions = ['action_activate', 'action_inactivate', 'action_reject', 'export_to_json']

    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<a href='{obj.photo.url}' target='_blank'><img src='{obj.photo.url}' width='20' /></a>")
        else:
            return _("No photo")

    display_photo.short_description = _("Photo")

    def action_activate(self, request, queryset):
        queryset.update(status='Active')

    action_activate.short_description = _("Activate selected doctors")

    def action_inactivate(self, request, queryset):
        queryset.update(status='Inactive')

    action_inactivate.short_description = _("Inactivate selected doctors")

    def action_reject(self, request, queryset):
        queryset.update(status='Rejected')

    action_reject.short_description = _("Reject selected doctors")

    def export_to_json(self, request, queryset):
        """
        Exports a list of doctors to a JSON file, including all fields.
        """
        # Serialize all fields by not specifying the 'fields' parameter
        data = serialize('json', queryset)

        parsed_data = json.loads(data)
        indented_data = json.dumps(parsed_data, ensure_ascii=False, indent=4)

        # Directly return the serialized JSON data
        response = HttpResponse(indented_data, content_type='application/json')
        timestamp = timezone.now().strftime('%d_%m_%Y')
        file_name = f'doctors_{timestamp}.json'
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        return response

    export_to_json.short_description = _('Export to JSON')


@admin.register(Rate)
class RateAdmin(ModelAdmin):
    list_display = ('doctor', 'user', 'rate', 'created_at')
    search_fields = ('doctor__first_name', 'doctor__last_name')
    search_help_text = _("Enter doctor name to search")
    date_hierarchy = 'created_at'
    list_select_related = ('doctor', 'user')
    list_filter_submit = True
    list_filter = (
        ('rate', RangeNumericFilter),
        ('order', RelatedDropdownFilter),
        ('created_at', RangeDateFilter),
    )

    compressed_fields = True
    warn_unsaved_form = True
