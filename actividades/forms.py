from django import forms
from .models import Actividad


class ActividadForm(forms.ModelForm):
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