from django import forms
from main.forms import BootstrapModelForm

from .models import Report_Field


class ReportFieldForm(BootstrapModelForm):
    placeholders = {
        'link': 'Ссылка на документ или раздел системы',
        'link_description': 'Описание ссылки',
    }

    class Meta:
        model = Report_Field
        fields = (
            'content',
            'status',
            'link',
            'link_description',
        )

    def __init__(self, *args, **kwargs):
        field_type = kwargs.pop('field_type')
        super(ReportFieldForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = field_type.placeholder
        if field_type:
            self.label = field_type.name
            if not field_type.has_status:
                self.fields['status'].widget = forms.HiddenInput()
            if not field_type.has_url:
                self.fields['link'].widget = forms.HiddenInput()
                self.fields['link_description'].widget = forms.HiddenInput()

    def clean(self):
        super(ReportFieldForm, self).clean()
        link = self.cleaned_data.get("link")
        link_description = self.cleaned_data.get("link_description")
        if bool(link) != bool(link_description):
            raise forms.ValidationError('Поля "ссылка" и "описание ссылки" должны быть или пустые или заполнены вместе')
