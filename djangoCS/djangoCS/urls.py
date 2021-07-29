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
from os import name
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
    path('asignarProgramas/', views.asignarProgramas),
    path('calendarioMant/',views.calendarioMant),
    path('formularioMant/', views.formularioMant),
    path('verCarta/', views.verCarta),
    path('agregarCarta/', views.agregarCarta),
    path("BitacorasEquipos/", views.BitacorasEquipos),
    path("BitacorasImpresoras/", views.BitacorasImpresoras),
    path("BitacorasEmpleados/", views.BitacorasEmpleados),
    path("BitacorasMantenimiento/", views.BitacorasMantenimiento),
    path("BitacorasCartuchos/", views.BitacorasCartuchos),
    path("BitacorasCartas/", views.BitacorasCartas),
    path("DescargarPDF/", views.descargarPDF),
    path("ProgramaPorArea/",views.ProgramasporArea),
    path("verProgramasPorArea/", views.verProgramasPorArea),
    path("guardarImagen/", views.guardarImagen),
    path("editarEquipo/", views.editarEquipo),
    path("editarEmpleado/", views.editarEmpleado),
    path("editarEmpleadoBd/", views.editarEmpleadoBd),
    path("editarImpresora/", views.editarImpresora),
    path("firmarCarta/", views.firmarCarta),
    path("salir/", views.salir, name="salir"),
    path("altaEmpleado/", views.altaEmpleado),
    path("bajaEmpleado/", views.bajaEmpleado)
    
    
]
