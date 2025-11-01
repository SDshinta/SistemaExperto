from django import forms
from .models import Hecho, Regla

class HechoForm(forms.ModelForm):
    class Meta:
        model = Hecho
        fields = ['descripcion', 'pregunta']

class ReglaForm(forms.ModelForm):
    class Meta:
        model = Regla
        fields = ['hecho', 'conclusion', 'peso', 'explicacion_humana']  # ← Usa los campos REALES que declaraste en el modelo
        widgets = {
            'explicacion_humana': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_condicion(self):
        condicion = self.cleaned_data['condicion']
        hechos_test = {
            k: True for k in condicion.replace('and', ' ').replace('or', ' ').split()
        }
        try:
            eval(condicion, {}, hechos_test)
        except Exception as e:
            raise forms.ValidationError(f"La condición tiene un error de sintaxis: {e}")
        return condicion
