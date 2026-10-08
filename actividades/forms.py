from django import forms
from .models import Actividad


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def clean(self, data, initial=None):
        if not data:
            return []
        files = data if isinstance(data, (list, tuple)) else [data]
        return [forms.ImageField.clean(self, uploaded_file, initial) for uploaded_file in files]


class ActividadForm(forms.ModelForm):
    imagenes = MultipleImageField(
        required=False,
        label='Imágenes de evidencia',
        widget=MultipleImageInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

    class Meta:
        model = Actividad
        fields = ('codigo_evidencia', 'titulo', 'descripcion', 'categoria')
        labels = {
            'codigo_evidencia': 'Código de evidencia',
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class