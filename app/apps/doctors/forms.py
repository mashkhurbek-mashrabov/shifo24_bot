from django import forms

from .models.doctors import Doctor

class DoctorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(attrs={"size": "70"})
        self.fields['last_name'].widget = forms.TextInput(attrs={"size": "70"})
        self.fields['address'].widget = forms.Textarea(attrs={"cols": "100", "rows": "5"})

    class Meta:
        model = Doctor
        fields = '__all__'
