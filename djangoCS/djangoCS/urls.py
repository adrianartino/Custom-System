"""djangoCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from appCS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('inicio/', views.inicio),
    path('verAreas/', views.verAreas),
    path('agregarAreas/',views.agregarAreas),
    path('verEmpleados/', views.verEmpleados),
    path('agregarEmpleados/', views.agregarEmpleados),
    path('verEquipos/',views.verEquipos),
    path('agregarEquipos/', views.agregarEquipos),
    path('verImpresoras/', views.verImpresoras),
    path('agregarImpresoras/', views.agregarImpresoras),
    path('verInsumos/', views.verInsumos),
    path('agregarInsumos/', views.agregarInsumos),
    path('verProgramas/', views.verProgramas),
    path('agregarProgramas/', views.agregarProgramas),
    path('calendarioMant/',views.calendarioMant),
    path('formularioMant/', views.formularioMant),
    path('verCarta/', views.verCarta),
    path('agregarCarta/', views.agregarCarta),
    path("BitacoraEmpleados/", views.EmpleadosBitacora),
    path("BitacoraEquipos/", views.EquiposBitacora),
    path("BitacoraImpresoras/", views.ImpresorasBitacora),
    path("BitacoraMantenimiento/", views.MantenimientoBitacora),
    path("BitacoraCartuchos/", views.CartuchosBitacora),
    path("BitacoraCartas/", views.CartasBitacora),
    path("DescargarPDF/", views.descargarPDF)
    
]
