"""
URL configuration for sistema_experto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from taller import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('diagnosticar/', views.diagnosticar, name='diagnosticar'),
    path('administrar/', views.administrar, name='administrar'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/usuario/', views.login_usuario_automatico, name='login_usuario_automatico'),
    path('editar_hecho/<int:id>/', views.editar_hecho, name='editar_hecho'),
    path('eliminar_hecho/<int:id>/', views.eliminar_hecho, name='eliminar_hecho'),
    path('editar_regla/<int:id>/', views.editar_regla, name='editar_regla'),
    path('eliminar_regla/<int:id>/', views.eliminar_regla, name='eliminar_regla'),
    path('seleccionar-modo/', views.seleccionar_modo, name='seleccionar_modo'),
    path('backward/', views.backward_inicio, name='backward_inicio'),
    path('editar-hecho-backward/<int:id>/', views.editar_hecho_backward, name='editar_hecho_backward'),
    path('editar-regla-backward/<int:id>/', views.editar_regla_backward, name='editar_regla_backward'),
    path('administrar-backward/', views.administrar_backward, name='administrar_backward'),
    path('eliminar-hecho-backward/<str:desc>/', views.eliminar_hecho_backward, name='eliminar_hecho_backward'),
    path('eliminar-regla-backward/<str:condicion>/<str:conclusion>/', views.eliminar_regla_backward, name='eliminar_regla_backward'),



]
