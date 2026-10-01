from django import forms
from .models import ServicioMunicipal


class ServicioMunicipalForm(forms.ModelForm):
    class Meta:
        model = ServicioMunicipal
        fields = ('nombre_servicio', 'responsable', 'activo')
        labels = {
            'nombre_servicio': 'Nombre del servicio',
            'responsable': 'Responsable',
            'activo': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'