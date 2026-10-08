from django import forms
from .models import ServicioMunicipal


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def clean(self, data, initial=None):
        if not data:
            return []
        files = data if isinstance(data, (list, tuple)) else [data]
        return [forms.ImageField.clean(self, uploaded_file, initial) for uploaded_file in files]


class ServicioMunicipalForm(forms.ModelForm):
    imagenes = MultipleImageField(
        required=False,
        label='Imágenes de evidencia',
        widget=MultipleImageInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

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