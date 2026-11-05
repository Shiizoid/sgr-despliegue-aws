from django import forms
from .models import ServicioMunicipal, SolicitudServicio


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


class SolicitudServicioForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = ('servicio', 'telefono', 'descripcion')
        labels = {
            'servicio': 'Servicio solicitado',
            'telefono': 'Teléfono de contacto',
            'descripcion': 'Detalle de la solicitud',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5, 'maxlength': 1000}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = ServicioMunicipal.objects.filter(activo=True).order_by('nombre_servicio')
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'


class SolicitudEstadoForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = ('estado',)
        labels = {'estado': 'Estado'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget.attrs['class'] = 'form-select'