from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import PerfilUsuario

ROLE_NAMES = ('Administrador', 'Supervisor', 'Administrativo')


class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    rol = forms.ModelChoiceField(
        label='Perfil',
        queryset=Group.objects.filter(name__in=ROLE_NAMES).order_by('name'),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['rol'].widget.attrs['class'] = 'form-select'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set((self.cleaned_data['rol'],))
        return user


class UsuarioUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')
    rol = forms.ModelChoiceField(
        label='Perfil',
        queryset=Group.objects.filter(name__in=ROLE_NAMES).order_by('name'),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'is_active': 'Cuenta activa',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].initial = self.instance.groups.filter(name__in=ROLE_NAMES).first()
        for field in self.fields.values():
            field.widget.attrs['class'] = (
                'form-check-input' if isinstance(field.widget, forms.CheckboxInput)
                else 'form-select' if isinstance(field, forms.ModelChoiceField)
                else 'form-control'
            )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if self._meta.model.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set((self.cleaned_data['rol'],))
        return user


class PerfilPropioForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    imagen = forms.ImageField(
        label='Foto de perfil',
        required=False,
        widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),
    )

    def __init__(self, *args, **kwargs):
        self.perfil = kwargs.pop('perfil')
        super().__init__(*args, **kwargs)
        self.fields['imagen'].initial = self.perfil.imagen
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        usuario = super().save(commit=commit)
        if commit:
            imagen = self.cleaned_data.get('imagen')
            if imagen is False:
                self.perfil.imagen.delete(save=False)
                self.perfil.imagen = ''
                self.perfil.save(update_fields=('imagen',))
            elif imagen:
                self.perfil.imagen = imagen
                self.perfil.save(update_fields=('imagen',))
        return usuario
