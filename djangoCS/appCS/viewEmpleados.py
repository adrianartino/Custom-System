
#Librerías
import mimetypes
import os
import base64
from io  import BytesIO

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras

#Librería para manejar archivos en Python
from django.core.files.base import ContentFile

#Librerías de fecha
from datetime import date, datetime
from datetime import timedelta
from calendar import calendar
from dateutil.relativedelta import relativedelta

#Archivo configuración Django
from django.conf import settings

#Correo
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Librerias reportes pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

#Libreria excel.
import xlwt


def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto


                
            

def principal(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnInicio = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def encuestas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

    

def equipo(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerEquipo = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes


        #Codigo de info equipos.
        datosEquipo = Equipos.objects.filter(id_empleado =id_admin)
        
        #Si hay un equipo asignado a es empleado...
        if datosEquipo: 
            tieneEquipo = True  

            #Sacar datos del empleado
            datosPropietario= Empleados.objects.filter(id_empleado=id_admin)
            for datos in datosPropietario:
                nombre= datos.nombre
                apellidos=datos.apellidos
                nombreEmpleado= nombre + " " + apellidos
                departamento=datos.id_area_id
                datosDepa= Areas.objects.filter(id_area=departamento)
                for datos in datosDepa:
                    nombreArea= datos.nombre
                    colorArea=datos.color



            #Sacar id de equipo para consultar renovación
            for dato in datosEquipo:
                id_equipo = dato.id_equipo

            #Sacar datos de renovación
            datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
            for datos in datosRenovacion:
                compra= datos.fecha_compra
                renovar=  datos.fecha_renov
                        
                    
            #Verificar si tiene mantenimientos.      
            mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo=id_equipo)
            if mantenimientos:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado, "nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "mantenimientos":mantenimientos, "datosEquipo": datosEquipo})
            else:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado,"nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "datosEquipo": datosEquipo})
                    
        else:
            noTieneEquipo = True
            return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "noTieneEquipo":noTieneEquipo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def carta(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCarta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        return render(request, "empleadosCustom/miEquipo/verCartaResponsiva.html", { "estaEnVerCarta": estaEnVerCarta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def directorio(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCorreos = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        empleadosActivos = Empleados.objects.filter(activo__icontains= "A", correo__icontains = "customco.com.mx")
        
        #empleados Actvos
        areasEnActivos = []
        datosAreasEnActivos = []
        
        for empleado in empleadosActivos:
            areasEnActivos.append(empleado.id_area_id)
            
        for id in areasEnActivos:
            datosArea = Areas.objects.filter(id_area = id) 
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnActivos.append([nombreArea, colorArea])
            
        lista = zip(empleadosActivos, datosAreasEnActivos)
        
        
        return render(request, "empleadosCustom/directorioCorreos/verDirectorio.html", { "estaEnVerCorreos": estaEnVerCorreos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista":lista})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio