
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
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta

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

        preguntas = Preguntas.objects.filter(id_encuesta = 1)

        preguntasMultiples = []
        preguntasAbiertas = []
        contadorPreguntas = 0
        for pregunta in preguntas:
            id_pregunta = pregunta.id_pregunta
            texto_pregunta = pregunta.pregunta
            tipo = pregunta.tipo

            if tipo== "M":
                preguntasMultiples.append([id_pregunta, texto_pregunta])
                contadorPreguntas = contadorPreguntas +1 
            else:
                preguntasAbiertas.append([id_pregunta, texto_pregunta])
                contadorPreguntas = contadorPreguntas +1 



        #Condicion para saber si el empleado ya contesto algo..

        empleadoTieneRespuestas = Respuestas.objects.filter(id_empleado = id_admin) #Consulta a la tabla de respuestas para ver si alguna tiene el id del empleado

        #Si el empleado ya tiene aunque sea una pregunta resuelta..
        if empleadoTieneRespuestas:
            aunqueseaunapregunta = True
            contadorRespuestas = 0
            for respuesta in empleadoTieneRespuestas:
                contadorRespuestas = contadorRespuestas + 1
            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "contadorRespuestas":contadorRespuestas})

        #Si el empleado no tiene ninguna pregunta resuelta
        else:
            #Mostrar solo la introducción.
            aunqueseaunapregunta = False
            introduccion = True
        
        
            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "introduccion":introduccion})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def guardarRespuesta(request):
    
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

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = ""
            nameInput = "respuesta"

            if request.POST.get(nameInput, False): #Checkeado
                respuesta = "SI"
            elif request.POST.get(nameInput, True): #No checkeado
                respuesta = "NO"

         

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def guardarRespuestaTextbox(request):
    
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

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = request.POST['respuestaText']

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

            numeroPreguntas = Preguntas.objects.filter(id_encuesta = 1)
            contadorPreguntas = 0
            for pregunta in numeroPreguntas:
                contadorPreguntas = contadorPreguntas +1

            respuestasEmpleado = Respuestas.objects.filter(id_empleado = id_admin) #4 registros

            contadorRespuestas = 0
            for respuesta in respuestasEmpleado:
                contadorRespuestas = contadorRespuestas +1

            if (contadorRespuestas == contadorPreguntas):
                registroEmpleadoCompletoEncuesta = EncuestaEmpleadoResuelta(id_empleado = Empleados.objects.get(id_empleado = id_admin), id_encuesta = Encuestas.objects.get(id_encuesta = 1))
                registroEmpleadoCompletoEncuesta.save()


        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
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
        
        datosRegistro = Carta.objects.filter(id_empleado = id_admin)
        
        empleados=[]
        equipos=[]
        
        for registros in datosRegistro:
            empleado= registros.id_empleado_id
            equipo = registros.id_equipo_id
            
            datosEmpleado = Empleados.objects.filter(id_empleado=empleado)
            for datos in datosEmpleado:
                nombres= datos.nombre
                apellido= datos.apellidos
                
            datosEquipos =Equipos.objects.filter(id_equipo=equipo)
            for datos in datosEquipos:
                marca=datos.marca
                modelo=datos.modelo
                
            empleados.append([nombres,apellido])
            equipos.append([marca, modelo])
        
        lista1=zip(datosRegistro,empleados,equipos)
        
        
        return render(request, "empleadosCustom/miEquipo/verCartaResponsiva.html", { "estaEnVerCarta": estaEnVerCarta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista1":lista1})
    
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
    
    

def documentosAplicablesATodos(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnVerDocumentos = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable1(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".xlsx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


            return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable2(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".docx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


            return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable3(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".pdf"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


            return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio