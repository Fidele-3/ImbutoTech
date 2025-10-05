from django import forms
from ImbutoTech.models import ImbutoTechSession

class ImbutoTechSessionForm(forms.ModelForm):
    class Meta:
        model = ImbutoTechSession
        fields = ['date', 'sector']
