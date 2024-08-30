# from datetime import datetime
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django import forms
# from .models import Order
#
#
# class OrderAdminForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.pk:
#             # Adding read-only fields after creation
#             self.fields['user_phone_number'] = forms.CharField(
#                 label=_('User Phone Number'),
#                 initial=self.instance.user.phone_number,
#                 widget=forms.TextInput(attrs={'readonly': 'readonly'}),
#                 required=False
#             )
#             self.fields['user_chat_id'] = forms.CharField(
#                 label=_('User Chat ID'),
#                 initial=self.instance.user.telegram_id,
#                 widget=forms.TextInput(attrs={'readonly': 'readonly'}),
#                 required=False
#             )
#
#     def clean(self):
#         cleaned_data = super().clean()
#         if not self.instance.pk:
#             now = datetime.now()
#             if now < cleaned_data['scheduled_date']:
#                 raise forms.ValidationError(_('Scheduled date must be in the future'))
#         return cleaned_data
