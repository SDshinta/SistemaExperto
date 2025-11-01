from django.shortcuts import render, redirect
from .models import Hecho, Regla
from .forms import HechoForm, ReglaForm
from .motor_inferencia import motor_inferencia

from django import forms

from .backward_motor import HECHOS, REGLAS  # Importamos los datos globales


from django.contrib.auth.decorators import login_required, user_passes_test


from django.contrib.auth import login
from django.contrib.auth.models import User

# Para poder modificar HECHOS y REGLAS globales:
import sys
thismodule = sys.modules[__name__]

class HechoForm(forms.Form):
    descripcion = forms.CharField(label="Clave del hecho", max_length=100)
    pregunta = forms.CharField(label="Pregunta para el hecho", max_length=255)

class ReglaForm(forms.Form):
    condicion = forms.CharField(label="Condición (clave hecho)", max_length=100)
    conclusion = forms.CharField(label="Conclusión", max_length=255)
    explicacion = forms.CharField(label="Explicación", widget=forms.Textarea, required=False)

def login_usuario_automatico(request):
    try:
        # Buscamos el usuario ya registrado con username exacto 'Usuario'
        user = User.objects.get(username='Usuario')
        # Hacemos login automático sin password
        login(request, user)
        return redirect('seleccionar_modo')  # o a la vista que uses para diagnosticar
    except User.DoesNotExist:
        # Si no existe, redirigimos a login normal con mensaje de error
        return redirect('login')





# Función para saber si el usuario es administrador
def es_admin(user):
    return user.groups.filter(name='Administrador').exists()

# Función para saber si es usuario común
def es_usuario(user):
    return user.groups.filter(name='Usuario').exists()

@login_required
@user_passes_test(lambda u: es_admin(u) or es_usuario(u))
def index(request):
    hechos = Hecho.objects.all()
    es_admin_flag = es_admin(request.user)
    return render(request, 'index.html', {
        'hechos': hechos,
        'es_admin': es_admin_flag
    })


@login_required
@user_passes_test(lambda u: es_admin(u) or es_usuario(u))
def diagnosticar(request):
    es_admin_flag = es_admin(request.user)
    if request.method == 'POST':
        hechos_usuario = []
        hechos = Hecho.objects.all()
        faltantes = []

        for hecho in hechos:
            respuesta = request.POST.get(f'hecho_{hecho.id}')
            if respuesta is None:
                faltantes.append(hecho.pregunta)
            elif respuesta == 'no':  # "No" significa que el hecho negativo se cumple
                hechos_usuario.append(hecho.descripcion)

        if faltantes:
            return render(request, 'index.html', {
                'hechos': hechos,
                'es_admin': es_admin_flag,
                'error': "Debe responder todas las preguntas antes de continuar."
            })

        resultado = motor_inferencia(hechos_usuario)

        return render(request, 'diagnostico.html', {
            'resultado': resultado,
            'es_admin': es_admin_flag
        })
    return redirect('index')






@login_required
@user_passes_test(es_admin)
def administrar(request):
    hechos = Hecho.objects.all()
    reglas = Regla.objects.all()
    hecho_form = HechoForm()
    regla_form = ReglaForm()
    es_admin_flag = es_admin(request.user)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'hecho':
            hecho_form = HechoForm(request.POST)
            if hecho_form.is_valid():
                hecho_form.save()

        elif form_type == 'regla':
            regla_form = ReglaForm(request.POST)
            if regla_form.is_valid():
                regla_form.save()

        return redirect('administrar')

    return render(request, 'administrar.html', {
        'hechos': hechos,
        'reglas': reglas,
        'hecho_form': hecho_form,
        'regla_form': regla_form,
        'es_admin': es_admin_flag
    })

from django.shortcuts import get_object_or_404

@login_required
@user_passes_test(es_admin)
def editar_hecho(request, id):
    hecho = get_object_or_404(Hecho, pk=id)
    if request.method == 'POST':
        form = HechoForm(request.POST, instance=hecho)
        if form.is_valid():
            form.save()
            return redirect('administrar')
    else:
        form = HechoForm(instance=hecho)
    return render(request, 'editar_item.html', {'form': form, 'titulo': 'Editar Hecho'})

@login_required
@user_passes_test(es_admin)
def eliminar_hecho(request, id):
    hecho = get_object_or_404(Hecho, pk=id)
    hecho.delete()
    return redirect('administrar')

@login_required
@user_passes_test(es_admin)
def editar_regla(request, id):
    regla = get_object_or_404(Regla, pk=id)
    if request.method == 'POST':
        form = ReglaForm(request.POST, instance=regla)
        if form.is_valid():
            form.save()
            return redirect('administrar')
    else:
        form = ReglaForm(instance=regla)
    return render(request, 'editar_item.html', {'form': form, 'titulo': 'Editar Regla'})

@login_required
@user_passes_test(es_admin)
def eliminar_regla(request, id):
    regla = get_object_or_404(Regla, pk=id)
    regla.delete()
    return redirect('administrar')


@login_required
def seleccionar_modo(request):
    return render(request, 'seleccionar_modo.html')

from .backward_motor import backward_chaining

@login_required
def backward_inicio(request):
    # Mostrar la lista de conclusiones para elegir
    conclusiones = list({r['conclusion'] for r in REGLAS})  # usa la lista de reglas del backward_motor.py

    if request.method == 'POST':
        objetivo = request.POST.get('objetivo')
        respuestas_usuario = {}
        # Recolectar las respuestas de los hechos
        for hecho_key in HECHOS.keys():
            respuestas_usuario[hecho_key] = request.POST.get(hecho_key)

        confirmado, mensaje = backward_chaining(objetivo, respuestas_usuario)
        return render(request, 'backward_resultado.html', {
            'confirmado': confirmado,
            'mensaje': mensaje,
            'objetivo': objetivo
        })

    return render(request, 'backward_inicio.html', {
        'hechos': HECHOS,
        'conclusiones': conclusiones
    })

@login_required
@user_passes_test(es_admin)

def administrar_backward(request):
    # Accedemos a las estructuras globales
    hechos = thismodule.HECHOS
    reglas = thismodule.REGLAS

    hecho_form = HechoForm()
    regla_form = ReglaForm()

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "hecho":
            hecho_form = HechoForm(request.POST)
            if hecho_form.is_valid():
                desc = hecho_form.cleaned_data["descripcion"]
                preg = hecho_form.cleaned_data["pregunta"]
                # Añadimos o actualizamos en el diccionario global HECHOS
                hechos[desc] = preg
                return redirect("administrar_backward")

        elif form_type == "regla":
            regla_form = ReglaForm(request.POST)
            if regla_form.is_valid():
                cond = regla_form.cleaned_data["condicion"]
                conc = regla_form.cleaned_data["conclusion"]
                expl = regla_form.cleaned_data["explicacion"]

                # Actualizar o añadir regla: 
                # Si hay una regla con misma condición y conclusión, actualizamos la explicación, si no, añadimos nueva
                index = next((i for i, r in enumerate(reglas) if r["condicion"] == cond and r["conclusion"] == conc), None)
                if index is not None:
                    reglas[index]["explicacion"] = expl
                else:
                    reglas.append({"condicion": cond, "conclusion": conc, "explicacion": expl})
                return redirect("administrar_backward")

    return render(request, "administrar_backward.html", {
        "hecho_form": hecho_form,
        "regla_form": regla_form,
        "hechos": hechos,
        "reglas": reglas,
    })
    
# Opcional: Funciones para eliminar hechos y reglas
def eliminar_hecho_backward(request, desc):
    hechos = thismodule.HECHOS
    if desc in hechos:
        del hechos[desc]
        # También eliminar reglas asociadas a este hecho
        reglas = thismodule.REGLAS
        thismodule.REGLAS = [r for r in reglas if r["condicion"] != desc]
    return redirect("administrar_backward")

def eliminar_regla_backward(request, condicion, conclusion):
    reglas = thismodule.REGLAS
    thismodule.REGLAS = [r for r in reglas if not (r["condicion"] == condicion and r["conclusion"] == conclusion)]
    return redirect("administrar_backward")

def editar_hecho_backward(request, id):
    if request.method == 'POST':
        hechos_backward[id] = request.POST.get('descripcion')
        return redirect('administrar_backward')
    return render(request, 'editar_item.html', {
        'form_action': request.path,
        'label': 'Editar Hecho',
        'valor': hechos_backward[id]
    })

def editar_regla_backward(request, id):
    if request.method == 'POST':
        reglas_backward[id]['hecho'] = request.POST.get('hecho')
        reglas_backward[id]['conclusion'] = request.POST.get('conclusion')
        return redirect('administrar_backward')
    return render(request, 'editar_regla_manual.html', {
        'form_action': request.path,
        'label1': 'Hecho',
        'label2': 'Conclusión',
        'valor1': reglas_backward[id]['hecho'],
        'valor2': reglas_backward[id]['conclusion']
    })





