import json

from django.contrib import admin
from django.utils import timezone
from django.core.serializers import serialize
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    MultipleChoicesDropdownFilter,
    RangeDateTimeFilter, RangeDateFilter
)

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ('chat_id', 'user_name', 'language', 'created_at',)
    search_fields = ('username', 'chat_id', 'name', 'phone_number')
    search_help_text = _("Fields allowed for searching: name, chat ID, username, phone number.")
    actions = ('export_to_json',)
    date_hierarchy = 'created_at'

    compressed_fields = True
    warn_unsaved_form = True

    list_filter_submit = True
    list_filter = [
        ("language", MultipleChoicesDropdownFilter),
        ("step", ChoicesDropdownFilter),
        ("created_at", RangeDateFilter),
    ]

    fieldsets = (
        (_('User Details'), {
            'fields': ('chat_id', 'name', 'username', 'phone_number', 'language', 'step',)
        }),
        (_('Creation date'), {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
            'description': format_html(
                f'<p style="color: green">{_('The date and time when the user was created')}.</p>'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at',)

    def user_name(self, obj):
        if obj.username:
            return format_html("<a target='_blank' href='https://t.me/{0}'>{1}</a>", obj.username, obj.name)
        return obj.name or '-'

    user_name.short_description = _('Name')
    user_name.admin_order_field = 'name'
    user_name.allow_tags = True

    def export_to_json(self, request, queryset):
        """
        Exports a list of telegram users to a JSON file, including all fields.
        """
        # Serialize all fields by not specifying the 'fields' parameter
        data = serialize('json', queryset)

        parsed_data = json.loads(data)
        indented_data = json.dumps(parsed_data, ensure_ascii=False, indent=4)

        # Directly return the serialized JSON data
        response = HttpResponse(indented_data, content_type='application/json')
        timestamp = timezone.now().strftime('%d_%m_%Y')
        file_name = f'telegram_users_{timestamp}.json'
        response['Content-Disposition'] = f'attachment; filename={file_name}'

        return response

    export_to_json.short_description = _('Export to JSON')
