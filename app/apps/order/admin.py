from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order
from doctors.models.rate import Rate
from .constants import OrderStatusChoices
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    MultipleChoicesDropdownFilter,
    RelatedDropdownFilter,
    MultipleRelatedDropdownFilter,
    RangeDateFilter
)


class RateInline(TabularInline):
    model = Rate
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = ('doctor', 'user', 'rate', 'created_at')


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['user', 'doctor', 'scheduled_date', 'status', "created_at"]
    search_fields = ['user__name', "user__phone_number"]
    search_help_text = _("Enter user name or phone number to search")
    date_hierarchy = 'created_at'
    list_select_related = ('user', 'doctor')
    inlines = [RateInline]

    compressed_fields = True
    warn_unsaved_form = True
    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = [
        ("status", MultipleChoicesDropdownFilter),
        ("doctor", RelatedDropdownFilter),
        ("specialization", MultipleRelatedDropdownFilter),
        ("scheduled_date", RangeDateFilter),
        ("created_at", RangeDateFilter),
    ]

    actions = ['action_accept', 'action_complete', 'action_reject']

    def action_accept(self, request, queryset):
        queryset.update(status=OrderStatusChoices.ACCEPTED)

    action_accept.short_description = _("Mark as Accepted")

    def action_complete(self, request, queryset):
        queryset.update(status=OrderStatusChoices.COMPLETED)

    action_complete.short_description = _("Mark as Completed")

    def action_reject(self, request, queryset):
        queryset.update(status=OrderStatusChoices.REJECTED)

    action_reject.short_description = _("Mark as Rejected")
