from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common.models.specialization import Specialization

admin.site.site_header = _('Shifo24 Admin')

class SpecializationChildInline(admin.TabularInline):
    model = Specialization
    extra = 1
    show_change_link = True


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'parent', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_uz', "name_ru" 'name_en')
    search_help_text = _("Enter name to search")
    ordering = ('order',)
    inlines = [SpecializationChildInline]
    list_select_related = ('parent',)