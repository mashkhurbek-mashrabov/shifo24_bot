from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from common.models.specialization import Specialization
from unfold.admin import ModelAdmin, TabularInline

admin.site.site_header = _('Shifo24 Admin')

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True


class SpecializationChildInline(TabularInline):
    model = Specialization
    extra = 1
    show_change_link = True
    tab = True


@admin.register(Specialization)
class SpecializationAdmin(ModelAdmin):
    list_display = ('name_uz', 'parent', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_uz', "name_ru" 'name_en')
    search_help_text = _("Enter name to search")
    ordering = ('order',)
    inlines = [SpecializationChildInline]
    list_select_related = ('parent',)

    compressed_fields = True
    warn_unsaved_form = True

    def get_inline_title(self):
        return "Custom title"
