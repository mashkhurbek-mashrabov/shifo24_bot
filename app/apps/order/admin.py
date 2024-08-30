from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order
# from .forms import OrderAdminForm

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # form = OrderAdminForm

    list_display = ['user', 'doctor', 'scheduled_date', 'status', "created_at"]
    list_filter = ['status', "scheduled_date", 'created_at']
    search_fields = ['user__name', "user__phone_number"]
    search_help_text = _("Enter user name or phone number to search")
    date_hierarchy = 'created_at'
    list_select_related = ('user', 'doctor')

    # fieldsets = (
    #     (None, {
    #         'fields': ('user', 'doctor', 'specialization', 'scheduled_date', 'status', 'note')
    #     }),
    #     (_('User Information'), {
    #         'fields': ('user_phone_number', 'user_chat_id'),
    #         'classes': ('collapse',)  # Optional: Collapse the section
    #     }),
    # )
    #
    # def get_readonly_fields(self, request, obj=None):
    #     if obj:  # Editing an existing object
    #         return self.readonly_fields + ('user_phone_number', 'user_chat_id')
    #     return self.readonly_fields
    #
    # def user_phone_number(self, obj):
    #     return obj.user.phone_number if obj and obj.user else '-'
    #
    # user_phone_number.short_description = _('User Phone Number')
    #
    # def user_chat_id(self, obj):
    #     return obj.user.telegram_id if obj and obj.user else '-'
    #
    # user_chat_id.short_description = _('User Chat ID')